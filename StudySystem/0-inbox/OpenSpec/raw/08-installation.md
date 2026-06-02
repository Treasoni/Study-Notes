Source: https://github.com/Fission-AI/OpenSpec (README section)
and https://www.npmjs.com/package/@fission-ai/openspec

# Installation Guide

## Prerequisites

- **Node.js** >= 20.19.0
- Any of: **npm**, **pnpm**, **yarn**, **bun**, or **nix**

## Installation Methods

### Method 1: Global npm install (recommended)

```bash
npm install -g @fission-ai/openspec@latest
```

### Method 2: Using other package managers

```bash
# pnpm
pnpm add -g @fission-ai/openspec@latest

# yarn
yarn global add @fission-ai/openspec@latest

# bun
bun add -g @fission-ai/openspec@latest
```

### Method 3: Using npx (no install)

```bash
npx @fission-ai/openspec@latest init
```

### Method 4: Nix

Supported via `flake.nix` in the repository for a reproducible development shell that includes `nodejs_20` and `pnpm_9`.

## Verify Installation

```bash
openspec --version
```

## Initialize in Your Project

```bash
cd your-project
openspec init
```

This creates the `openspec/` directory structure with:
- `specs/` — main specs directory
- `changes/` — active changes directory
- `config.yaml` — project configuration
- Tool-specific skill/command files (e.g., `.claude/skills/`, `.cursor/commands/`)

## Updating

```bash
npm install -g @fission-ai/openspec@latest
openspec update   # Apply changes to project
```

## Windows Notes

On Windows, use **Git Bash** or **WSL** (Windows Subsystem for Linux) for the best experience.

## Post-Installation

The CLI is packaged with all templates and adapters bundled — no network access required after installation. After `openspec init`, you immediately have access to slash commands like `/opsx:propose` in your AI coding assistant.

## Package Information

- **Name:** `@fission-ai/openspec`
- **Registry:** npm
- **License:** MIT
- **Latest stable:** v1.3.1
- **Requires:** Node.js 20.19.0+
