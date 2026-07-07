# Contributing

Thank you for helping improve Project Interview Extractor. Contributions should make the skill more accurate, evidence-aware, concise, or useful across real interview contexts.

## Before opening an issue

- Search existing issues first.
- Remove credentials, personal data, proprietary source code, and confidential project details.
- For security vulnerabilities, use the private process in [SECURITY.md](SECURITY.md).
- For behavior problems, include a minimal anonymized prompt, the observed output, and the expected behavior.

## Development workflow

1. Fork the repository and create a focused branch from `main`.
2. Make the smallest coherent change.
3. Add or update an evaluation case under `project-interview-extractor/evals/` when behavior changes.
4. Run the package validator:

   ```bash
   python scripts/validate_repository.py
   ```

5. Review the truthfulness, privacy, and progressive-disclosure rules in `SKILL.md`.
6. Open a pull request using the repository template.

## Skill design rules

- Keep `project-interview-extractor/SKILL.md` focused on essential runtime instructions.
- Put detailed methods and templates in directly linked files under `references/`.
- Do not add README, changelog, installation, or governance files inside the installable skill directory.
- Do not introduce claims, metrics, ownership, or production outcomes that the supplied evidence cannot support.
- Keep reference nesting one level deep.
- Prefer standard-library validation; justify any new runtime or CI dependency.

## Evaluation changes

An evaluation case must contain:

- an input or initial input section;
- expected behavior stated as observable criteria;
- failure signals or completion conditions;
- no real credentials, personal information, or proprietary material.

Evaluation fixtures describe expected model behavior. They are not automatically scored model benchmarks. Explain manual behavior testing in the pull request when the change affects interview logic.

## Pull request expectations

- Keep each pull request focused.
- Explain what changed, why it changed, and how it was validated.
- Update English and Chinese user documentation together when user-facing behavior changes.
- Confirm that your contribution can be distributed under Apache-2.0.

By submitting a contribution, you agree that it is licensed under the repository's [Apache License 2.0](LICENSE).
