# Security Policy

## Supported versions

Security fixes are applied to the latest release and the `main` branch.

| Version | Supported |
|---|---|
| Latest release | Yes |
| `main` | Yes |
| Older releases | No |

## Report a vulnerability

Do not open a public issue for a vulnerability or accidentally committed secret.

Use GitHub's private vulnerability-reporting form:

<https://github.com/f12336414-ship-it/project-interview-extractor/security/advisories/new>

Include:

- the affected file, version, or commit;
- reproduction steps or a minimal proof of concept;
- expected impact;
- suggested mitigation, if known;
- whether the report itself contains sensitive data.

You should receive an acknowledgement within seven days. The maintainer will validate the report, coordinate remediation, and credit the reporter unless anonymity is requested. Public disclosure should wait until a fix or mitigation is available.

## Scope

Security concerns include unsafe handling of project secrets, prompt-driven data disclosure, validation bypasses, and workflow or supply-chain weaknesses. General output-quality issues belong in the public issue tracker after all private data is removed.
