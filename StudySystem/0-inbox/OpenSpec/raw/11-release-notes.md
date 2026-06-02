Source: https://github.com/Fission-AI/OpenSpec/releases

# Release Notes

## v1.3.1 -- Path and Telemetry Fixes (patch, ~May 2026)

### Fixed
- **Canonical artifact paths** -- Workflow artifact paths now resolve through native `realpath`, so symlinks and case-insensitive filesystems no longer cause mismatches during `apply` and `archive`.
- **Glob artifact outputs** -- Apply instructions with glob artifact outputs resolve correctly. Literal outputs are enforced as file paths.
- **Hidden spec requirements** -- Validation now detects requirements nested inside fenced code blocks or otherwise hidden in main specs.
- **Clean `--json` output** -- Spinner progress no longer leaks into stderr when `--json` is passed.
- **Silent telemetry in firewalled networks** -- PostHog errors are swallowed with a 1s timeout, and retries/remote config are disabled.
- **Telemetry config on XDG and Windows** -- Honors `XDG_CONFIG_HOME` on Linux and `%APPDATA%` on Windows.
- **Glob-special characters in paths** -- Directory paths containing glob metacharacters are now escaped before matching.

### New Contributors
- @swithek, @furaul

## v1.3.0 -- New Tool Integrations (major)

### New Features
- **Junie support** -- Generate tool and command files for JetBrains Junie.
- **Lingma IDE support** -- Configuration support for the Lingma IDE.
- **ForgeCode support** -- Tool support for ForgeCode.
- **IBM Bob support** -- Tool support for the IBM Bob coding assistant.

### Fixed
- **OpenCode directory** -- OpenCode adapter now uses `.opencode/commands/` (plural).
- **`openspec status` with no changes** -- Exits gracefully instead of throwing.
- **Copilot auto-detection** -- No longer triggers from a bare `.github/` directory.
- **pi.dev command generation** -- Command reference transforms and template argument passing now work correctly.
- **Shell completions opt-in** -- Completion install is now opt-in, avoiding PowerShell encoding corruption.

## v1.2.0 (February 2026)

Introduced the OPSX (OpenSpec eXperience) workflow system with action-based artifact management:
- Artifact Graph and state machine (BLOCKED/READY/DONE)
- Dynamic instruction assembly from context + rules + templates
- New commands: `/opsx:new`, `/opsx:continue`, `/opsx:ff`, `/opsx:verify`, `/opsx:sync`, `/opsx:bulk-archive`, `/opsx:onboard`
- Legacy `/openspec:*` commands still supported but OPSX recommended
- Support for custom schemas and schema forking
- Cross-repo coordination workspaces (beta)
- Multi-language support via Instruction Enrichment Pipeline
- 28k+ GitHub stars at release

## v1.1.0

- Enhanced tool integration with adapter system
- Multiple bug fixes and stability improvements

## v1.0.0 (Initial Stable Release, ~Late 2025)

- First stable release of OpenSpec
- Core workflow: proposal -> apply -> archive
- Support for Claude Code, Cursor, Windsurf, GitHub Copilot
- Delta spec system with ADDED/MODIFIED/REMOVED sections
- Spec-driven development framework
