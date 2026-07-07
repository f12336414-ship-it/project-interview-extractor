#!/usr/bin/env python3
"""Validate open-source repository structure without third-party packages."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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

REQUIRED = {
    ".editorconfig",
    ".gitattributes",
    ".github/CODEOWNERS",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/dependabot.yml",
    ".github/workflows/codeql.yml",
    ".github/workflows/validate.yml",
    ".gitignore",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "LICENSE",
    "NOTICE",
    "README.md",
    "README.zh-CN.md",
    "SECURITY.md",
    "SUPPORT.md",
    "docs/EVALUATION.md",
    "docs/RELEASING.md",
    "project-interview-extractor/SKILL.md",
}

TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml"}
TEXT_NAMES = {
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    "CODEOWNERS",
    "LICENSE",
    "NOTICE",
}

ALLOWED_ACTIONS = {
    "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
    "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1",
    "github/codeql-action/init@54f647b7e1bb85c95cddabcd46b0c578ec92bc1a",
    "github/codeql-action/analyze@54f647b7e1bb85c95cddabcd46b0c578ec92bc1a",
}


def fail(message: str) -> None:
    ERRORS.append(message)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_utf8(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"cannot read UTF-8 file {relative(path)}: {exc}")
        return ""
    if text.startswith("\ufeff"):
        fail(f"UTF-8 BOM is not allowed: {relative(path)}")
    if text and not text.endswith("\n"):
        fail(f"missing final newline: {relative(path)}")
    return text


def text_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES:
            files.append(path)
    return sorted(files)


def check_required_files() -> None:
    for item in sorted(REQUIRED):
        if not (ROOT / item).is_file():
            fail(f"required repository file is missing: {item}")


def check_text_quality(path: Path, text: str) -> None:
    if PLACEHOLDER_PATTERN.search(text):
        fail(f"placeholder marker found: {relative(path)}")
    for number, line in enumerate(text.splitlines(), start=1):
        if re.search(r"[ \t]+$", line):
            fail(f"trailing whitespace: {relative(path)}:{number}")
        if "\t" in line:
            fail(f"tab character: {relative(path)}:{number}")


def check_markdown_links(path: Path, text: str) -> None:
    for match in re.finditer(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)", text):
        raw_target = match.group(1).split("#", 1)[0]
        target = raw_target.strip("<>")
        if target and not (path.parent / target).resolve().exists():
            fail(f"broken local link in {relative(path)}: {raw_target}")


def check_workflows() -> None:
    workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    for path in workflows:
        text = read_utf8(path)
        if "permissions:" not in text:
            fail(f"workflow must declare least-privilege permissions: {relative(path)}")
        if "pull_request_target:" in text:
            fail(f"pull_request_target is not allowed: {relative(path)}")
        for action in re.findall(r"^\s*uses:\s*([^\s#]+)", text, re.MULTILINE):
            if action not in ALLOWED_ACTIONS:
                fail(f"unreviewed or unpinned GitHub Action in {relative(path)}: {action}")


def check_repository_contract() -> None:
    license_text = read_utf8(ROOT / "LICENSE")
    if "Apache License" not in license_text or "Version 2.0" not in license_text:
        fail("LICENSE is not the Apache License 2.0 text")

    readme = read_utf8(ROOT / "README.md")
    for heading in ("## Install", "## Use", "## Validate", "## Contributing and security"):
        if heading not in readme:
            fail(f"README.md is missing {heading}")

    dependabot = read_utf8(ROOT / ".github" / "dependabot.yml")
    if 'package-ecosystem: "github-actions"' not in dependabot:
        fail("Dependabot must monitor GitHub Actions")

    for form in ("bug_report.yml", "feature_request.yml"):
        text = read_utf8(ROOT / ".github" / "ISSUE_TEMPLATE" / form)
        for key in ("name:", "description:", "body:"):
            if key not in text:
                fail(f"issue form {form} is missing {key}")


def check_generated_artifacts() -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.name in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}:
            fail(f"generated directory is present: {relative(path)}")
        if path.is_file() and path.suffix.lower() in {".pyc", ".tmp", ".bak", ".swp"}:
            fail(f"generated file is present: {relative(path)}")


def check_skill_package() -> None:
    validator = ROOT / "project-interview-extractor" / "scripts" / "validate_package.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        fail("installable skill validation failed:\n" + result.stdout + result.stderr)
    elif result.stdout.strip():
        print(result.stdout.strip())


def main() -> int:
    check_required_files()
    for path in text_files():
        text = read_utf8(path)
        check_text_quality(path, text)
        if path.suffix.lower() == ".md":
            check_markdown_links(path, text)
    check_workflows()
    check_repository_contract()
    check_generated_artifacts()
    check_skill_package()

    if ERRORS:
        for error in ERRORS:
            print(f"[FAIL] {error}")
        print(f"\n{len(ERRORS)} repository validation error(s).")
        return 1

    print(f"[PASS] repository: {len(text_files())} text files checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
