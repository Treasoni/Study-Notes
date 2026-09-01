---
url: "https://eduhub.deeptutor.info/how-to-use/agent-publish"
title: "Let an agent do it — How to use EduHub"
scraped_at: 2026-09-01T15:28:58+00:00
---

Guide contents
Quick start


Publish & maintain
  * [Maintain: update & roll back](https://eduhub.deeptutor.info/how-to-use/maintain)


Using inside DeepTutor


# Let an agent do it
Give your agent one prompt or an online Markdown guide, then let it create, tag, publish, and verify the skill.
## Option 1: copy this prompt
Use this with agents that can edit files and run commands, such as Codex, Claude Code, or DeepTutor. Copy it, then fill in your skill idea.
PROMPT

```
Help me turn the idea below into an EduHub skill and publish it to EduHub.
Follow this online guide exactly: https://eduhub.deeptutor.info/eduhub-skill-manager.md
My skill idea:
[Write the topic, target users, use cases, source material, and constraints here.]
Requirements:
1. Create a valid skill folder with SKILL.md at the root.
2. Write clear name and description frontmatter; the description must say what the skill does and when it should trigger.
3. Choose track, language, domains, stages, forms, and tags based on the content. If uncertain, explain your recommendation and ask me.
4. If using open-source content, only use permissively licensed sources and preserve author, project, license, link, and adaptation notes.
5. Before publishing, run eduhub skill publish ./<skill-dir> --dry-run.
6. If I am not logged in to EduHub, guide me through eduhub login. Never write tokens into files or replies.
7. Publish only after the dry run passes.
8. After publishing, verify with eduhub skill inspect, eduhub search, and eduhub install into a temp directory.
9. Finish with the slug, version, install command, and verification result.
```

## Option 2: send a Markdown link
If the prompt feels too long, or you want the agent to read the latest workflow every time, send it this Markdown link.
PROMPT

```
Read and strictly follow this EduHub skill creation and publishing guide:
https://eduhub.deeptutor.info/eduhub-skill-manager.md
Then turn my idea into a skill and publish it:
[Write the topic, target users, use cases, source material, and constraints here.]
```

[Open the online Markdown guide →](https://eduhub.deeptutor.info/eduhub-skill-manager.md)
## What the agent should do
  * Shape your material into a valid skill folder containing SKILL.md.
  * Choose the track, language, domains, stages, forms, and search keywords.
  * Run a dry run first; if login is needed, guide you through eduhub login.
  * After publishing, verify with inspect, search, and install into a temp directory.


