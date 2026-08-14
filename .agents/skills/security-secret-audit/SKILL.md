---
name: security-secret-audit
description: Audit a Git repository for exposed API keys, tokens, passwords, private keys, project-owned source/configuration risks, and sensitive-file policy gaps without printing secret values. Use when asked to check project security, scan for API leaks, review files before committing or pushing, investigate a credential leak, or assess high-confidence project risks.
---

# Security Secret Audit

Run the bundled scanner before a commit, whenever a credential leak is suspected, and when assessing project security. Treat every finding as sensitive: do not paste matched values into messages, issues, commits, or logs.

## Workflow

1. Read the repository instructions, `.gitignore`, and `git status --short`.
2. Resolve the installed skill directory, then run its bundled `scripts/audit-secrets.sh`. Do not hard-code a profile-specific path such as `.claude/skills`.

3. Scan the relevant scope:

```bash
# Current tracked and non-ignored files; default credential mode.
"$AUDITOR"

# Only the staged content; use immediately before committing.
"$AUDITOR" --staged

# Every unique file version reachable from Git history; use after a suspected past leak.
"$AUDITOR" --history

# Project security: credential scan plus project-owned source/configuration risks.
"$AUDITOR" --project

# CI gate: project-risk findings are blocking in strict mode.
"$AUDITOR" --project --strict

# Low-risk repair only: preview then append a credential ignore block to .gitignore.
"$AUDITOR" --project --fix
```

4. Report findings by file, line, rule name, and scope only. Never reveal credential values.
5. For a current-file finding, remove the secret from tracked content, move it to an ignored local configuration file, and add a sanitized example when configuration documentation is needed.
6. For a history finding, revoke or rotate the credential first. Then explain that deleting the current file is insufficient and rewrite history only with explicit user authorization.
7. `--strict` and `--fix` require `--project`. CI uses `--project --strict` and never uses `--fix`.
8. `--fix` may only add or replace the marked, idempotent local-credential ignore block in `.gitignore`. It keeps `.env.example`, `.env.sample`, `.env.template`, and their named variants trackable. It never deletes secrets, rotates or revokes credentials, rewrites Git history, stages files, commits, or pushes. If a credential finding exists, it skips the fix because ignoring the file is insufficient.
9. In `--project` mode, `.obsidian/plugins/**` is third-party vendor code: it remains in the credential scan but is excluded from heuristic source-risk rules. Re-run the same scan after remediation. A clean credential scan is required before staging or committing.

## Scanner Contract

- Exit `0`: no credential findings. In non-strict project mode, risk findings are warnings so they can be triaged.
- Exit `2`: potential credential found, or a project risk found under `--strict`; stop the commit or push.
- Exit `1`: scanner error; treat it as a failed security check and investigate before proceeding.
- Output is intentionally redacted to `scope:path:line:rule`; the scanner never prints matched content. Credential rules cover provider formats, private keys, JWTs, and named literals in configuration-like files. Project rules cover disabled TLS validation, shell command execution, permissive CORS, world-writable permissions, sensitive-data logging, tracked credential files, and a missing local-credential ignore block.

## Limitations

The bundled patterns are a high-signal baseline, not proof that a repository is secret-free or risk-free. They do not perform dependency/CVE analysis or replace threat modeling. When a remote, CI system, or package ecosystem is available, add maintained secret, dependency, and SAST scanners as independent controls. Do not add real credentials to allowlists; rotate false-positive-looking credentials only after confirming ownership and validity.
