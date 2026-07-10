# Advanced Codex CLI Configuration (config.toml)

Source: https://learn.chatgpt.com/docs/config-file/config-advanced
Fetched: 2026-07-11

## Config and State Locations

`CODEX_HOME` (defaults to `~/.codex`) stores local state. Common files:
- `config.toml` — local configuration
- `auth.json` — file-based credential storage (or OS keychain)
- `history.jsonl` — if history persistence is enabled

## Configuration Precedence (highest to lowest)

1. CLI flags (`-c key=value`) — temporary overrides
2. Profile values
3. Project config (`.codex/config.toml`) — trusted projects only
4. User config (`~/.codex/config.toml`)
5. Built-in defaults

## Profiles

Profiles let you save named configuration layers. Use `--profile profile-name` to load `~/.codex/profile-name.config.toml`. Profile names support letters, numbers, hyphens, and underscores.

Example `~/.codex/deep-review.config.toml`:
```toml
model = "gpt-5.5"
model_reasoning_effort = "xhigh"
approval_policy = "on-request"
model_catalog_json = "/Users/me/.codex/model-catalogs/deep-review.json"
```

**Breaking change (>=0.134.0):** `--profile` no longer reads `[profiles.profile-name]` from `config.toml`. Use separate `profile-name.config.toml` files instead.

## One-off CLI Overrides

```bash
codex --model gpt-5.4
codex --config model='"gpt-5.4"'
codex --config sandbox_workspace_write.network_access=true
codex --config 'shell_environment_policy.include_only=["PATH","HOME"]'
```

Keys use dot notation for nested values. Values parse as TOML; failing that, treated as strings.

## Project Config Files (`.codex/config.toml`)

Codex walks from project root to CWD and loads every `.codex/config.toml` it finds. Closest file to CWD wins for same keys.

**Security**: Project configs load only when the project is trusted.

**Restricted keys** (ignored in project-local config): `openai_base_url`, `chatgpt_base_url`, `model_provider`, `model_providers`, `notify`, `profile`, `profiles`, and `otel`. These must go in user-level `~/.codex/config.toml`.

## Custom Model Providers

```toml
model = "gpt-5.4"
model_provider = "proxy"

[model_providers.proxy]
name = "OpenAI using LLM proxy"
base_url = "http://proxy.example.com"
env_key = "OPENAI_API_KEY"

[model_providers.local_ollama]
name = "Ollama"
base_url = "http://localhost:11434/v1"

[model_providers.mistral]
name = "Mistral"
base_url = "https://api.mistral.ai/v1"
env_key = "MISTRAL_API_KEY"
```

Reserved built-in provider IDs: `openai`, `ollama`, `lmstudio`.

### Command-backed Authentication

```toml
[model_providers.proxy.auth]
command = "/usr/local/bin/fetch-codex-token"
args = ["--audience", "codex"]
timeout_ms = 5000
refresh_interval_ms = 300000
```

The auth command receives no stdin, prints token to stdout.

### Amazon Bedrock

```toml
model_provider = "amazon-bedrock"
model = "<bedrock-model-id>"
[model_providers.amazon-bedrock.aws]
profile = "default"
region = "eu-central-1"
```

### Azure Provider

```toml
[model_providers.azure]
name = "Azure"
base_url = "https://YOUR_PROJECT.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"
query_params = { api-version = "2025-04-01-preview" }
wire_api = "responses"
request_max_retries = 4
stream_max_retries = 10
stream_idle_timeout_ms = 300000
```

### OSS Mode

Pass `--oss` to use local providers. Choose one with `--local-provider` per run or set:
```toml
oss_provider = "ollama"
```

## Model Reasoning, Verbosity, and Limits

```toml
model_reasoning_summary = "none"
model_verbosity = "low"
model_supports_reasoning_summaries = true
model_context_window = 128000
```

## Approval Policies and Sandbox

```toml
approval_policy = "untrusted"
approvals_reviewer = "user"
sandbox_mode = "workspace-write"
allow_login_shell = false
```

Granular approval policy:
```toml
approval_policy = { granular = { ... } }
```

### Workspace-Write Sandbox Config

```toml
[sandbox_workspace_write]
exclude_tmpdir_env_var = false
exclude_slash_tmp = false
writable_roots = ["/Users/YOU/.pyenv/shims"]
network_access = false
```

## Shell Environment Policy

```toml
[shell_environment_policy]
inherit = "none"
set = { PATH = "/usr/bin", MY_FLAG = "1" }
ignore_default_excludes = false
exclude = ["AWS_*", "AZURE_*"]
include_only = ["PATH", "HOME"]
```

## Project Root Detection

```toml
project_root_markers = [".git", ".hg", ".sl"]
project_root_markers = []  # Skip parent searching
```

## Project Instructions Discovery

```toml
project_doc_max_bytes = <number>
project_doc_fallback_filenames = ["CLAUDE.md", "AGENTS.md"]
```

## TUI Options

```toml
[tui]
notifications = true # or false, or restrict to specific types
notification_method = "auto" # or "osc9" or "bel"
notification_condition = "unfocused" # or "always"
animations = true
alternate_screen = false # "never" to keep scrollback
show_tooltips = false
```

## Notifications

```toml
notify = ["python3", "/path/to/notify.py"]
```

Fires on `agent-turn-complete`. The script receives a JSON argument.

**`notify` vs `tui.notifications`**: `notify` runs external programs; `tui.notifications` is built into TUI.

## History Persistence

```toml
[history]
persistence = "none"  # disable history saving
max_bytes = 104857600  # cap file size
```

## Observability (OpenTelemetry)

```toml
[otel]
environment = "staging"
exporter = "none"
log_user_prompt = false
```

Exporters: `none`, `{ otlp-http = { ... } }`, `{ otlp-grpc = { ... } }`.

## Anonymous Usage Metrics

```toml
[analytics]
enabled = false
```

## Feedback Controls

```toml
[feedback]
enabled = false
```

## Clickable Citations

```toml
file_opener = "vscode"
# Options: vscode, cursor, windsurf, vscode-insiders, none
```

## Hide/Surface Reasoning

```toml
hide_agent_reasoning = true
show_raw_agent_reasoning = true
```

## Hooks in config.toml

```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py"'
timeout = 30
statusMessage = "Checking Bash command"
```
