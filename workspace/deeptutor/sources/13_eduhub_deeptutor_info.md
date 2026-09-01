---
url: "https://eduhub.deeptutor.info/eduhub-skill-manager.md"
scraped_at: 2026-09-01T15:29:33+00:00
---


```
# EduHub Skill Manager

> This Markdown is written for AI agents. Follow it when a user asks you to create, package, publish, install, or verify a Codex-compatible skill on EduHub.
>
> Public URL: `https://eduhub.deeptutor.info/eduhub-skill-manager.md`
> Published EduHub skill slug: `eduhub-skill-manager`

EduHub hosts skill packages. A skill package is a folder with `SKILL.md` at its root, plus optional support files such as references, examples, templates, or scripts. Your job is to turn the user's idea into a valid skill, publish it safely, and verify that another agent can install it.

---

## 1. Ground Rules

- Verify live registry state with `eduhub` commands. Do not rely on memory.
- Never write tokens, cookies, API keys, `.npmrc`, or login secrets into the skill folder.
- If the user pasted a token into chat, use it only for the requested action and recommend rotating it afterward.
- Use permissively licensed upstream content only. Preserve attribution when copying or adapting content.
- Do not copy GPL/AGPL or unlicensed source text unless the user explicitly confirms compatibility and authorization.
- Keep the package minimal: include only files the skill needs at runtime.

---

## 2. Create The Skill Folder

Create a folder named with a lowercase hyphenated slug:

```text
my-skill/
â”œâ”€â”€ SKILL.md
â””â”€â”€ optional-support-files...
```

`SKILL.md` must have YAML frontmatter with at least:

```markdown
---
name: my-skill
description: State what this skill does and when an agent should use it.
---

# My Skill

Give the agent concrete operating instructions.
```

Write the body as an executable playbook for an agent:

- Say when to use the skill.
- Say what to do first, next, and last.
- Include rules, anti-patterns, and validation steps.
- Move long reference material into support files and link to them from `SKILL.md`.

If open-source material is copied or adapted, add `ATTRIBUTION.md` with:

- original author
- project name
- license
- source URL
- what was copied or changed

---

## 3. Choose Classification Metadata

Choose classification before publishing. Ask the user only when the right answer is not clear from the skill.

Tracks:

- `academics`: study, tutoring, writing, practice, assessment.
- `companions`: motivation, reflection, planning, wellbeing support.
- `skills-interests`: coding, music, hobbies, public speaking, practical skills.
- `educators`: teacher/admin tools, lesson planning, rubrics, skill-management workflows.

Languages:

- `zh`
- `en`
- `ja`
- `other`

Optional metadata:

- `domains`: broad domains or custom domain strings.
- `stages`: learner stages such as K12, university, adult.
- `forms`: interaction styles such as tutor, practice, companion, tool.
- `tags`: search keywords.

---

## 4. Check Login

Search and install do not require login. Publishing does.

Check current login:

```bash
eduhub whoami
```

If not logged in, ask the user to run:

```bash
eduhub login
```

For CI or a user-provided CLI token:

```bash
eduhub login --token <token>
```

For self-hosted registries only:

```bash
eduhub login --registry https://<your-hub>
```

---

## 5. Dry Run Before Publishing

Always dry-run first:

```bash
eduhub skill publish ./my-skill --dry-run
```

If running non-interactively, pass required choices explicitly:

```bash
eduhub --no-input skill publish ./my-skill \
  --track educators \
  --language en \
  --tags agent,codex,skills,eduhub \
  --changelog "Initial release" \
  --dry-run
```

Inspect the dry-run output:

- slug is correct
- version is correct
- track and language are correct
- file count is expected
- zip size is reasonable

Fix the package before publishing if any of these are wrong.

---

## 6. Publish

After dry-run passes, publish:

```bash
eduhub --no-input skill publish ./my-skill \
  --track educators \
  --language en \
  --tags agent,codex,skills,eduhub \
  --changelog "Initial release"
```

For updates, increment semver:

```bash
eduhub --no-input skill publish ./my-skill \
  --version 1.0.1 \
  --track educators \
  --language en \
  --changelog "Describe the update"
```

Do not reuse a version number for meaningfully different content.

---

## 7. Verify The Published Skill

Verify registry detail:

```bash
eduhub skill inspect <slug>
```

Verify search:

```bash
eduhub search <query>
```

Verify install into a temporary directory:

```bash
eduhub install <slug> --workdir /private/tmp/eduhub-install-check --dir skills
test -f /private/tmp/eduhub-install-check/skills/<slug>/SKILL.md
```

If the target machine is not macOS/Linux or `/private/tmp` does not exist, choose a normal temporary directory for that environment.

---

## 8. Final Response To The User

Report:

- slug
- version
- registry
- track and language
- install command
- verification commands and results
- any limitations or follow-up the user must do, such as logging in or rotating a pasted token

If publishing fails, stop and report the exact command and error. Do not keep retrying with destructive or speculative changes.

```

