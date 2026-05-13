# Pre-Task Initialization

> Part of the Study System. See [CLAUDE.md](../CLAUDE.md) for the top-level map.

Before starting any new Study System task (Phase 0), resolve the vault path and internalize past learnings.

## Vault Path Validation (Critical Gate)

1. Read `.obsidian-config.md`
2. Check the `VAULT_PATH:` value:
   - **Empty**: this is the first run. Proactively ask the user:
     - "This appears to be your first time using the Study System. I need your Obsidian vault path to proceed."
     - "Please provide the absolute path to your Obsidian vault (e.g., `/Users/name/obsidian` or `C:/Users/name/obsidian`)."
     - After user provides a path, write it to `.obsidian-config.md`:
       ```
       VAULT_PATH: "/the/path"
       ```
     - Re-read `.obsidian-config.md` to confirm
     - If still empty, STOP — do not proceed without a valid path
   - **Non-empty**: validate the directory exists:
     - `ls "{VAULT_PATH}"` — if missing, warn the user and ask for correction
3. Resolve `SYSTEM_ROOT` and `OUTPUT_PATH` from the config values. All subsequent path references must use the resolved values.

## Internalize Past Learnings

1. Read `.learnings/RULES.md` — compact, actionable rules from past sessions
2. Note what to do, what to avoid, what patterns to watch for

If `.learnings/RULES.md` doesn't exist yet, skip this step.
