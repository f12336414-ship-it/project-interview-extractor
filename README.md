# Project Interview Extractor

[![Validate](https://github.com/f12336414-ship-it/project-interview-extractor/actions/workflows/validate.yml/badge.svg)](https://github.com/f12336414-ship-it/project-interview-extractor/actions/workflows/validate.yml)
[![CodeQL](https://github.com/f12336414-ship-it/project-interview-extractor/actions/workflows/codeql.yml/badge.svg)](https://github.com/f12336414-ship-it/project-interview-extractor/actions/workflows/codeql.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

An evidence-first Codex skill that turns real software project material into interview-ready narratives, project-specific questions, follow-up chains, resume bullets, and STAR stories without inventing experience.

[简体中文](README.zh-CN.md)

## Why it exists

Project interviews are rarely about reciting framework trivia. Interviewers test whether a candidate understands the business context, owned specific work, can explain technical trade-offs, and can defend claims under follow-up questions.

This skill helps candidates:

- separate confirmed facts from inference and missing evidence;
- analyze architecture, data, interfaces, performance, reliability, security, and engineering practices;
- generate project-specific questions rather than generic trivia;
- practice multi-level mock interviews one question at a time;
- improve resume bullets and STAR stories without overstating ownership or results.

## Modes

| Mode | Best for | Main output |
|---|---|---|
| Quick | Fast preparation | Summary, 10 likely questions, 5 follow-ups, 3 highlight candidates |
| Deep | Full project preparation | Architecture, evidence, question chains, answers, resume bullets, STAR stories, score |
| Mock interview | Spoken-answer practice | One adaptive question at a time with feedback |
| Resume optimization | Resume editing | Evidence-bounded bullets, level variants, and interview risks |

## Install

Clone the repository, then copy the skill directory into your Codex skills directory.

### macOS and Linux

```bash
git clone https://github.com/f12336414-ship-it/project-interview-extractor.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R project-interview-extractor/project-interview-extractor \
  "${CODEX_HOME:-$HOME/.codex}/skills/project-interview-extractor"
```

### Windows PowerShell

```powershell
git clone https://github.com/f12336414-ship-it/project-interview-extractor.git
$skills = if ($env:CODEX_HOME) { "$env:CODEX_HOME\skills" } else { "$env:USERPROFILE\.codex\skills" }
New-Item -ItemType Directory -Force $skills | Out-Null
Copy-Item -Recurse -Force ".\project-interview-extractor\project-interview-extractor" "$skills\project-interview-extractor"
```

Restart Codex after installation if the skill is not discovered immediately.

## Use

Codex slash commands are built-in session controls. This project exposes portable skill subcommands through `$project-interview-extractor` instead of pretending to register a new slash command. You can also select the skill with `/skills`, then enter the subcommand and options.

| Command | Purpose |
|---|---|
| `help` | Show commands, options, defaults, and examples |
| `chat` | Run a realistic, adaptive mock interview one question at a time |
| `bank` | Write an all-dimension question, follow-up, and answer handbook to Markdown |
| `analyze` | Run quick or deep project analysis |
| `resume` | Produce evidence-bounded resume content |
| `review` | Review the candidate's latest answer |
| `export` | Export the current session or report to Markdown |

Run a realistic interview with feedback at the end:

```text
$project-interview-extractor chat --role backend --level senior --rounds 12 --feedback end
```

Generate a comprehensive developer study handbook:

```text
$project-interview-extractor bank --role backend --level senior --coverage exhaustive --output docs/backend-interview-bank.md
```

The `bank` command checks 17 dimensions, marks non-applicable areas with reasons, and writes project-specific questions, conservative answers, three-level follow-ups, risks, learning notes, and self-tests. “All dimensions” is a measurable coverage contract, not a claim to enumerate infinitely many phrasings.

You can provide any combination of a README, source tree, resume description, architecture document, API or database schema, Git history, code snippets, or an oral project explanation.

## Truthfulness model

The skill classifies important claims as confirmed, single-source, inferred, or hypothetical. Source code can demonstrate that a capability exists; it cannot prove who designed it, whether it ran in production, or what business result it achieved. Metrics, ownership, incidents, and production outcomes remain unconfirmed until evidence supports them.

Sensitive values are redacted. The skill must not reproduce or use credentials found in project material.

## Repository layout

```text
project-interview-extractor/
├── project-interview-extractor/  # Installable Codex skill
│   ├── SKILL.md
│   ├── agents/
│   ├── evals/
│   ├── references/
│   └── scripts/
├── docs/                         # Evaluation and release process
└── .github/                      # CI, security, and contribution automation
```

## Validate

No third-party Python package is required:

```bash
python scripts/validate_repository.py
```

The repository validator checks community files, workflows, metadata, UTF-8, Markdown structure, internal links, command documentation, 17-dimension question-bank coverage, evaluation coverage, and scoring totals. See [Evaluation](docs/EVALUATION.md) for the boundary between automated package checks and model-behavior review.

## Contributing and security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Use GitHub issues for reproducible bugs and feature proposals. Do not disclose credentials or private project material in public issues; follow [SECURITY.md](SECURITY.md) for confidential vulnerability reports.

## License

Licensed under the [Apache License 2.0](LICENSE).
