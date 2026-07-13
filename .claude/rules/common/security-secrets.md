# Secret Safety

## Non-Negotiable Rules

1. Never write, stage, commit, push, echo, log, or paste a real API key, token, password, private key, connection string, session cookie, or credential-bearing configuration value.
2. Store runtime secrets only in ignored local files or the approved secret manager. Commit a sanitized `.env.example` or configuration template when documentation is needed.
3. Use descriptive placeholders such as `your-key-here`; never use a shortened prefix or suffix from a real credential as an example.
4. Treat an existing tracked credential as compromised. Revoke or rotate it before any history cleanup; removal from the current file alone does not make it safe.
5. Do not suppress a scanner finding by adding a real credential to an allowlist. Resolve the cause or document a sanitized fixture instead.

## Required Checkpoints

1. Before staging a change that adds or edits configuration, authentication, deployment, CI, integration, backup, or plugin files, run:

```bash
.claude/skills/security-secret-audit/scripts/audit-secrets.sh
```

2. Immediately before every commit, run:

```bash
.claude/skills/security-secret-audit/scripts/audit-secrets.sh --staged
```

3. A scanner exit code other than `0` blocks the commit or push. Exit `2` means potential credentials were found; exit `1` means the check is unreliable and must be fixed first.
4. After a suspected past leak, run `audit-secrets.sh --history`, rotate any real credential found, then request explicit authorization before rewriting shared history.

## Enforcement

- `.githooks/pre-commit` runs the staged scan and blocks unsafe commits once `core.hooksPath` is set to `.githooks`.
- `.claude/scripts/git-autocommit.sh` runs the same staged scan before its automated commit.
- This rule is a behavioral safeguard, not a replacement for repository CI or provider-side secret scanning.
