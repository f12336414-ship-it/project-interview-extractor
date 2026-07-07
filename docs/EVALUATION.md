# Evaluation

## Scope

The project uses two complementary evaluation layers:

1. deterministic package validation;
2. model-behavior review against anonymized evaluation cases.

These layers answer different questions and must not be conflated.

## Automated package validation

Run:

```bash
python scripts/validate_repository.py
```

The repository validator delegates to the installable-skill validator and checks:

- skill frontmatter and directory naming;
- UI metadata and default invocation;
- UTF-8, final newlines, whitespace, heading progression, and balanced fences;
- local links and direct reference discoverability;
- evaluation-case structure and four-mode coverage;
- scoring tables summing to 100;
- forbidden placeholders and generated artifacts covered by repository policy.

CI runs this validator on Linux and Windows. Passing it proves package consistency, not semantic answer quality.

## Behavior evaluation

Files under `project-interview-extractor/evals/` define anonymized prompts, observable expected behavior, and failure signals. Current scenarios cover:

- weak and unsupported project claims;
- a detailed backend concurrency case;
- adaptive frontend mock-interview follow-up;
- sensitive material handling;
- AI-project resume optimization.

For a behavior-changing pull request, run the relevant prompt in a fresh context with the skill enabled. Record:

- model and Codex surface;
- prompt and supplied fixture;
- output or a link to a sanitized artifact;
- each expected criterion as pass, fail, or not applicable;
- any variance across repeated runs.

Do not provide the expected answer to the model under test. Do not use real secrets, personal data, or proprietary project content.

## Acceptance

A change is ready when:

- deterministic validation passes;
- no critical failure signal appears;
- truthfulness and privacy rules remain intact;
- new behavior has a regression fixture;
- limitations are stated instead of hidden.

Model outputs are probabilistic. A passing manual run is evidence, not a guarantee of identical future output.
