# 探测原始记录 05：三条实现路线的可抄配方

> **性质**：原始证据记录，**不是**阶段 1 的交付物 `01_explore_result.md`，不推进任何阶段状态。
> **来源**：后台核验子代理（配方探测），核对日期 2026-09-18。所有代码块**逐字取自一手源，未做美化**。
> **引用纪律**：标「拼接，需核对」的代码块是子代理组合而成、无一手示例，正文引用前必须实机验证。

## 路线 1｜自建 SKILL.md（smart-home 类）

**适用场景**：能力已由某个 CLI 提供（openhue CLI、ha CLI 等），只需教会 agent 怎么调；不改任何代码。

**真实目录位置**（`website/docs/user-guide/features/skills.md`）：

```
~/.hermes/skills/                  # Single source of truth
├── mlops/                         # Category directory
│   ├── axolotl/
│   │   ├── SKILL.md               # Main instructions (required)
│   │   ├── references/            # Additional docs
```

项目级：`<project-root>/.hermes/skills/` 或 `<project-root>/.agents/skills/`，首次需 `hermes skills trust`。

三级加载（同源）：`Level 0: skills_list() → [{name, description, category}, ...] (~3k tokens)` / `Level 1: skill_view(name)` / `Level 2: skill_view(name, path)`。

**可用骨架**（逐字取自 `optional-skills/smart-home/openhue/SKILL.md`；该目录实际只有 SKILL.md 一个文件）：

```markdown
---
name: openhue
description: "Control Philips Hue lights, scenes, rooms via OpenHue CLI."
version: 1.0.1
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Smart-Home, Hue, Lights, IoT, Automation]
    homepage: https://www.openhue.io/cli
prerequisites:
  commands: [openhue]
---

# OpenHue CLI

## When to Use
## Common Commands
## Notes
```

正文五段固定顺序（`creating-skills` 页）：`## When to Use` / `## Quick Reference` / `## Procedure` / `## Pitfalls` / `## Verification`。

**前置条件与安装**：`hermes skills install official/<category>/<skill>`（catalog 页原句："install via `hermes skills install official/<category>/<skill>`"）。smart-home 类别下官方只有 openhue 一个（"## smart-home | **openhue** | Control Philips Hue lights, scenes, rooms via OpenHue CLI."）。**不存在 Home Assistant 官方 skill。**

## 路线 2｜MCP

**适用场景**：直接用现成 MCP server（HA 官方 `mcp_server` 或社区 ha-mcp）。

**Hermes 侧根结构**（逐字，`website/docs/reference/mcp-config-reference.md`）：

```yaml
mcp_servers:
  <server_name>:
    command: "..."      # stdio servers
    args: []
    env: {}

    # OR
    url: "..."          # HTTP servers
    headers: {}
    enabled: true
    timeout: 120
    connect_timeout: 60
    supports_parallel_tool_calls: false
    tools:
      include: []
      exclude: []
      resources: true
      prompts: true
```

`trust` 原文："Trust tier: `full` (default) or `untrusted`. On an `untrusted` server, every write-capable tool call ... requires user approval ... Unrecognized values are treated as `untrusted` (fail-closed)"。过滤："If both are set, `include` wins."

**CLI**（逐字，`reference/cli-commands.md`）：

```bash
hermes mcp add <name> [--url URL] [--command CMD] [--auth oauth|header] [--args ...]
hermes mcp test <name>
hermes mcp login <name>
```

会话内重载：`/reload-mcp`。

**HA 官方 server 端点**（逐字，`home-assistant/home-assistant.io` 的 `source/_integrations/mcp_server.markdown`）：`/api/mcp`，Assist 恒为 `/api/mcp/assist`；OAuth 用 IndieAuth，"It must never be your Home Assistant instance URL."

**拼接，需核对** —— 把 HA 端点接到 Hermes 的配置块，两边文档都无此组合示例（`optional-mcps/` 目录里**没有** homeassistant 条目）：

```yaml
# 拼接，需核对：Hermes mcp_servers 结构 + HA mcp_server 的 url
mcp_servers:
  homeassistant:
    url: "https://<your_home_assistant_external_url>/api/mcp"
    auth: oauth
    trust: untrusted
```

## 路线 3｜自定义 plugin

**适用场景**：要加一个 MCP 和 skill 都表达不了的原生工具（精确执行、二进制/流式、需走审批面）。

**最小可运行示例**（逐字，`website/docs/user-guide/features/plugins.md`）：

```yaml
# ~/.hermes/plugins/hello-world/plugin.yaml
name: hello-world
version: "1.0"
description: A minimal example plugin
```

```python
# ~/.hermes/plugins/hello-world/__init__.py
def register(ctx):
    schema = {
        "name": "hello_world",
        "description": "Returns a friendly greeting for the given name.",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Name to greet"}},
            "required": ["name"],
        },
    }

    def handle_hello(params, **kwargs):
        del kwargs
        name = params.get("name", "World")
        return json.dumps({"success": True, "greeting": f"Hello, {name}!"})

    ctx.register_tool(
        name="hello_world",
        toolset="hello_world",
        schema=schema,
        handler=handle_hello,
    )
```

签名原文："`ctx.register_tool(name=..., toolset=..., schema=..., handler=...)`"。**必须显式启用**（plugins 默认 opt-in）：`hermes plugins enable <name>`，或写进 `plugins.enabled`。校验：`hermes plugins doctor . --ci`。

## 来源

| 内容 | 路径/URL |
|---|---|
| plugin 最小示例、`ctx.*` 表、opt-in | `raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/features/plugins.md` |
| register_tool 完整用法、plugin.yaml v2 | `.../website/docs/developer-guide/plugins/index.md` |
| mcp_servers 根结构、trust、命名 | `.../website/docs/reference/mcp-config-reference.md` |
| MCP quick start、presets、toolset `mcp-<server>` | `.../website/docs/user-guide/features/mcp.md` |
| `hermes mcp` 子命令表 | `.../website/docs/reference/cli-commands.md` |
| L0/L1/L2、SKILL.md 格式、目录树、external_dirs、project-local | `.../website/docs/user-guide/features/skills.md` |
| openhue SKILL.md 全文 | `.../optional-skills/smart-home/openhue/SKILL.md` |
| HA `/api/mcp`、OAuth client_id | `raw.githubusercontent.com/home-assistant/home-assistant.io/current/source/_integrations/mcp_server.markdown` |
| ha-mcp 安装方式、readonly 后缀 | `raw.githubusercontent.com/homeassistant-ai/ha-mcp/master/README.md` |

## 待核对

1. **MCP 工具命名前缀三处冲突（同一仓库内）**：`mcp.md` 写 `mcp_<server_name>_<tool_name>` 并给表（`mcp_filesystem_read_file`）；`mcp-config-reference.md` 写 `mcp__<server>__<tool>`；`guides/use-mcp-with-hermes.md` 实际示例 `mcp_chrome_devtools_win_list_pages`（单下划线 + 连字符未净化）。**未定论**，写正文前必须实机 `hermes doctor` / `/tools list` 验证
2. **`ctx.call_mcp` 的 server 名来源**：plugins.md 注释写 `# server name from mcp.servers`，但配置键是 `mcp_servers`。疑为文档笔误
3. **`hermes mcp add` 是否写 `trust`**：CLI 表只列 `--url/--command/--auth/--args`，无 `--trust`
4. **`hermes mcp add --preset`**：`mcp.md` 有 `--preset codex`，`cli-commands.md` 子命令表未列（同 probe-02 第 7 条）
5. **HA + Hermes 拼接块**：`url` + `auth: oauth` 是否足以走通 HA 的 IndieAuth（callback port / client_id 由哪一侧决定）**完全未验证**
6. **ha-mcp 接 Hermes**：README 的 Setup Wizard 覆盖 15+ 客户端，**未确认是否含 Hermes**；`/private_<random>` 与 `/readonly` 后缀能否直接填进 `mcp_servers.url` 未验证
7. **`optional-skills/smart-home/DESCRIPTION.md`** 内容未读，不确定是否含类别级 frontmatter 规范
8. **`creating-skills.md`（20KB）因 raw.githubusercontent 429 未取到全文**；其 frontmatter 字段清单（`related_skills`、`requires_tools`、`blueprint.schedule`、`required_credential_files` 等）来自 WebFetch 摘要，**需回源逐字确认**
