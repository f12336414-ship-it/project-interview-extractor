# Releasing

The project follows Semantic Versioning.

## Version policy

- Patch: wording, evaluation, or validation fixes that preserve expected behavior.
- Minor: backward-compatible modes, outputs, role coverage, or analysis capabilities.
- Major: incompatible invocation, directory, evidence model, or output-contract changes.

## Release checklist

1. Ensure `main` is current and CI passes.
2. Run `python scripts/validate_repository.py` locally.
3. Review behavior-changing evaluation cases in a fresh context.
4. Update `CHANGELOG.md` and documentation.
5. Confirm the installable skill contains no generated or repository-only files.
6. Create a signed or annotated `vMAJOR.MINOR.PATCH` tag.
7. Publish GitHub release notes from the changelog.
8. Verify installation from a fresh clone.

Do not publish a release containing known credential exposure or unresolved truthfulness regressions.
