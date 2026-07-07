#!/usr/bin/env python3
"""Validate this skill package with Python standard-library checks only."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = (
    Path(sys.argv[1]).resolve()
    if len(sys.argv) == 2
    else Path(__file__).resolve().parents[1]
)
SKILL = ROOT / "SKILL.md"
ERRORS: list[str] = []
PLACEHOLDER_PATTERN = re.compile(
    r"\b(?:" + "|".join(("TO" + "DO", "T" + "BD", "FIX" + "ME")) + r")\b"
    + "|"
    + "lorem "
    + "ipsum"
    + "|"
    + "待办"
    + "占位",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    ERRORS.append(message)


def read_utf8(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"cannot read UTF-8 file {path.relative_to(ROOT)}: {exc}")
        return ""
    if text.startswith("\ufeff"):
        fail(f"UTF-8 BOM is not allowed: {path.relative_to(ROOT)}")
    if text and not text.endswith("\n"):
        fail(f"missing final newline: {path.relative_to(ROOT)}")
    return text


def quoted_yaml_value(text: str, key: str) -> str | None:
    match = re.search(rf'^\s*{re.escape(key)}:\s*"([^"]*)"\s*$', text, re.MULTILINE)
    return match.group(1) if match else None


def check_frontmatter(skill_text: str) -> str:
    match = re.match(r"\A---\n(.*?)\n---\n", skill_text, re.DOTALL)
    if not match:
        fail("SKILL.md must start with YAML frontmatter")
        return ""

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = re.match(r"^([a-z_]+):\s*(.+)$", line)
        if not field:
            fail(f"unsupported frontmatter line: {line!r}")
            continue
        fields[field.group(1)] = field.group(2).strip()

    if set(fields) != {"name", "description"}:
        fail(f"frontmatter fields must be name and description, got {sorted(fields)}")
    name = fields.get("name", "")
    if name != ROOT.name:
        fail(f"skill name {name!r} must match directory {ROOT.name!r}")
    if not re.fullmatch(r"[a-z0-9-]{1,63}", name):
        fail(f"invalid skill name: {name!r}")
    if len(fields.get("description", "")) < 30:
        fail("frontmatter description is too short to trigger reliably")
    return name


def check_openai_yaml(name: str) -> None:
    path = ROOT / "agents" / "openai.yaml"
    text = read_utf8(path)
    display_name = quoted_yaml_value(text, "display_name")
    short_description = quoted_yaml_value(text, "short_description")
    default_prompt = quoted_yaml_value(text, "default_prompt")

    if not display_name:
        fail("agents/openai.yaml needs a quoted display_name")
    if not short_description or not 25 <= len(short_description) <= 64:
        fail("short_description must contain 25-64 characters")
    if not default_prompt or f"${name}" not in default_prompt:
        fail(f"default_prompt must mention ${name}")


def check_markdown(path: Path, text: str) -> None:
    relative = path.relative_to(ROOT)
    if PLACEHOLDER_PATTERN.search(text):
        fail(f"placeholder marker found: {relative}")

    in_fence = False
    previous_heading = 0
    saw_heading = False
    fences = 0
    for number, line in enumerate(text.splitlines(), start=1):
        if re.search(r"[ \t]+$", line):
            fail(f"trailing whitespace: {relative}:{number}")
        if "\t" in line:
            fail(f"tab character: {relative}:{number}")
        if line.startswith("```"):
            fences += 1
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = re.match(r"^(#{1,6})\s+", line)
        if heading:
            level = len(heading.group(1))
            if not saw_heading and level != 1:
                fail(f"first heading must be H1: {relative}:{number}")
            if previous_heading and level > previous_heading + 1:
                fail(f"heading level jump: {relative}:{number}")
            previous_heading = level
            saw_heading = True

    if fences % 2:
        fail(f"unbalanced code fences: {relative}")
    if not saw_heading:
        fail(f"Markdown file has no heading: {relative}")

    for match in re.finditer(r"\[[^\]]+\]\((?!https?://|#)([^)]+)\)", text):
        target = match.group(1).split("#", 1)[0]
        if target and not (path.parent / target).resolve().exists():
            fail(f"broken local link in {relative}: {target}")


def check_references(skill_text: str) -> None:
    linked = {
        (SKILL.parent / match).resolve()
        for match in re.findall(r"\[[^\]]+\]\((references/[^)#]+)(?:#[^)]+)?\)", skill_text)
    }
    for path in sorted((ROOT / "references").glob("*.md")):
        if path.resolve() not in linked:
            fail(f"reference is not linked directly from SKILL.md: {path.name}")
        text = read_utf8(path)
        if len(text.splitlines()) > 100 and "## 目录" not in "\n".join(text.splitlines()[:20]):
            fail(f"long reference needs a table of contents near the top: {path.name}")


def check_evals() -> None:
    evals = sorted((ROOT / "evals").glob("*.md"))
    if len(evals) < 5:
        fail("at least five distinct evaluation cases are required")
    combined = ""
    for path in evals:
        text = read_utf8(path)
        combined += "\n" + text
        if not re.search(r"^## (?:输入|初始输入)$", text, re.MULTILINE):
            fail(f"eval needs an input section: {path.name}")
        if "## 预期行为" not in text:
            fail(f"eval needs expected behavior: {path.name}")
        if "## 失败信号" not in text and "## 完成条件" not in text:
            fail(f"eval needs failure signals or completion conditions: {path.name}")
    for mode in ("快速模式", "深度模式", "模拟面试模式", "简历优化模式"):
        if mode not in combined:
            fail(f"eval coverage is missing {mode}")


def sum_first_table(section: str) -> int:
    values = []
    for line in section.splitlines():
        match = re.match(r"^\|\s*[^|]+\|\s*(\d+)\s*\|", line)
        if match:
            values.append(int(match.group(1)))
    return sum(values)


def check_scoring() -> None:
    text = read_utf8(ROOT / "references" / "scoring-rubrics.md")
    project = re.search(
        r"## 项目面试准备度（100 分）(.*?)(?=\n## )", text, re.DOTALL
    )
    answer = re.search(r"## 单次回答质量（100 分）(.*?)(?=\n## )", text, re.DOTALL)
    if not project or sum_first_table(project.group(1)) != 100:
        fail("project-readiness scoring weights must sum to 100")
    if not answer or sum_first_table(answer.group(1)) != 100:
        fail("answer-quality scoring weights must sum to 100")


def main() -> int:
    if len(sys.argv) > 2:
        print("Usage: validate_package.py [skill-directory]", file=sys.stderr)
        return 2
    if not ROOT.is_dir():
        print(f"[FAIL] skill directory does not exist: {ROOT}")
        return 1

    expected_top_level = {"SKILL.md", "agents", "evals", "references", "scripts"}
    actual_top_level = {path.name for path in ROOT.iterdir()}
    unexpected = actual_top_level - expected_top_level
    if unexpected:
        fail(f"unexpected top-level entries: {sorted(unexpected)}")

    skill_text = read_utf8(SKILL)
    name = check_frontmatter(skill_text)
    check_openai_yaml(name)

    markdown_files = sorted(ROOT.rglob("*.md"))
    for path in markdown_files:
        check_markdown(path, read_utf8(path))

    check_references(skill_text)
    check_evals()
    check_scoring()

    if ERRORS:
        for error in ERRORS:
            print(f"[FAIL] {error}")
        print(f"\n{len(ERRORS)} validation error(s).")
        return 1

    print(
        f"[PASS] {ROOT.name}: {len(markdown_files)} Markdown files, "
        f"{len(list((ROOT / 'evals').glob('*.md')))} eval cases."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
