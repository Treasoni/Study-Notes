Source: https://gigazine.net/gsc_news/en/20251026-openspec/

# How to Generate Consistent Code Using OpenSpec

**Date:** October 26, 2025
**Publication:** GIGAZINE
**Language:** English

## Overview

OpenSpec makes it easy to introduce the AI-based coding method "Specification-Driven Development (SDD)" -- an approach where code is generated from specifications to ensure consistency and reduce bugs.

## Walkthrough: Kitchen Timer App

The article walks through building a browser-based kitchen timer using OpenSpec.

### Step 1: Edit `openspec/project.md`

Describe purpose and specs. Example project.md:

> Purpose: "Provide a simple and highly visible timer for use in home and commercial kitchens via a web browser."

Features: 1/3/5 minute buttons, large countdown display, button press resets during countdown.

Tech stack: HTML5, JavaScript (ES6), CSS3.

### Step 2: Propose a change

For GitHub Copilot Chat:

```
/openspec-proposal Create a UI
```

This generates a `create-ui` folder inside the `changes` directory with:
- **proposal.md** -- Summary, motivation, scope, references
- **design.md** -- "A minimal, single-page web app using vanilla HTML/CSS/JS. No frameworks."
- **tasks.md** -- Six tasks: scaffolding files, implementing UI, countdown/reset logic, CSS, manual testing, validating spec.md
- **spec.md** -- Requirements including timer UI, buttons, countdown, reset, large font, accessibility

### Step 3: Validate

Instruct "Please validate" to have OpenSpec check the content. Gaps or corrections can be resolved via AI chat or direct editing.

### Step 4: Generate code

```
/openspec-apply
```

Code is automatically generated. The kitchen timer "was completed with just one instruction." Errors can be corrected through AI chat.

### Step 5: Archive

```
/openspec-archive
```

Archiving marks the proposal as complete. Future spec changes require a new proposal.

## Key Insight

"You can use OpenSpec only for the parts where you want to keep a history" and proceed with regular methods for the rest, which "can be expected to improve the efficiency and quality of the entire project."
