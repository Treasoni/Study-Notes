---
url: "https://eduhub.deeptutor.info/how-to-use/maintain"
title: "Maintain: update & roll back — How to use EduHub"
scraped_at: 2026-09-01T15:29:20+00:00
---

Guide contents
Quick start


Publish & maintain
  * [Maintain: update & roll back](https://eduhub.deeptutor.info/how-to-use/maintain)


Using inside DeepTutor


# Maintain: update & roll back
deeptutor skills update: lists your published skills, pick one, then roll back to an older version or publish a new one.
## The update flow
update is interactive: after sign-in it lists the skills your account has published; pick one, then choose “roll back” or “upgrade”. Upgrading walks the publish tagging flow with every facet pre-filled from the skill's current labels.

```
deeptutor skills update
#  Pick a skill: 1.socratic-tutor v1.2.0 …
#  What to do? 1.Roll back  2.Publish a new version
# for an upgrade, pass the new version's folder
deeptutor skills update ./my-skill
```

## Versions & rollback
  * Versions use semver and coexist; pin with @version on install, latest by default.
  * latest defaults to the highest semver; “roll back” moves the latest pointer to an older published version without creating a new one.
  * Note: publishing a higher version afterwards moves latest forward again (npm-like semantics).


## Ownership & scan
Once a slug exists, only its owner (or an admin) can publish new versions or roll back. Every upload passes a static scan; suspicious patterns (pipe-to-shell, env exfiltration, native executables…) are flagged for the installer's import gate to weigh.
