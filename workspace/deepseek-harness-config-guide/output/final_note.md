---
title: "DeepSeek-Harness 配置实战：像 Claude Code 一样接入 skills/hooks/mcp/rules"
tags: [deepseek-harness, ai, agent, 配置, 教程, claude-code, skills, hooks, mcp, rules]
created: 2026-08-15
updated: 2026-08-15
status: new
source_project: deepseek-harness
---

# DeepSeek-Harness 配置实战：像 Claude Code 一样接入 skills/hooks/mcp/rules

> [!summary] 本章导读
> 前面几章教你怎么「**写**」dsh 插件。这一章反过来：你已经有一整套 Claude Code 配置（CLAUDE.md、skills、hooks、MCP），怎么让 dsh **直接用起来**。核心答案一句话：**rules 和 skills 几乎零迁移，hooks 和 mcp 要绕一下 cordis.yml**。先说清 `.dsh` 到底管什么，再逐块给操作，最后给一份「照搬 Claude Code」的四步清单。

## 1. 先回答最要紧的问题：`.dsh` 是不是就是 `.claude`？

**是，但只是半个。** `.dsh` 是真实存在的「harness home」，但它只覆盖四块能力里的两块：

| 位置 | 身份 | 类比 Claude Code | 放什么 |
|---|---|---|---|
| `~/.dsh/`（可用 `$DSH_HOME` 覆盖） | 用户级 harness home | `~/.claude/` | 用户级 `AGENTS.md`、`skills/`、profiles、`cordis.patch.yml` |
| `<项目根>/.dsh/skills/` | 项目级技能源 | `.claude/skills/` | 只有 **skills** |

而 **rules 不是放 `.dsh` 里、hooks 和 mcp 也不是**：

| 能力 | Claude Code 放哪 | dsh 放哪 | 迁移成本 |
|---|---|---|---|
| **Rules** | 项目根 `CLAUDE.md` | 项目根 `AGENTS.md` **和** `CLAUDE.md` 默认都读 | **零迁移** |
| **Skills** | `.claude/skills/<name>/SKILL.md` | `.dsh/skills/<name>/SKILL.md` 或 `.agents/skills/` | 复制文件夹 |
| **Hooks** | `settings.json` 的 hooks / `hooks.json` | 桥接插件或原生 cordis 插件，配在 `cordis.yml` | 一行配置 |
| **MCP** | `.mcp.json` / `claude mcp add` | 每 server 一个 `dsh-mcp-client` 插件实例，配在 `cordis.yml` | 每 server 几行 |

> [!tip] 大白话
> `.dsh` 像门卫室：**用户级**是你自己的储物柜（`~/.dsh`），**项目级**只在墙上给你挂了个"技能栏"（`.dsh/skills`）。规则（AGENTS.md / CLAUDE.md）是贴在项目大门口的黑板；hooks 和 MCP 要走物业系统（`cordis.yml`）申请，不归门卫室管。

## 2. Rules：你的 CLAUDE.md 原样生效，零迁移

官方源码里 `instructionFileCandidates` 的默认值就是 **`['AGENTS.md', 'CLAUDE.md']`**[^1]——dsh 本来就把两个都当指令文件候选。它从 session 工作目录向上找最近的含 `.git` 的祖先作为项目根，逐个目录加载这些文件。

- 本地覆盖：同目录下 **`AGENTS.local.md` / `CLAUDE.local.md`** 在基础文件之后加载（覆盖同名目录的重复内容）[^1]；
- 用户级：固定读 **`~/.dsh/AGENTS.md`**（`$DSH_HOME` 下），所有项目共享[^2]；
- 开关：`workspaceContext` 配置控制自动加载与字节预算，设 `false` 可整体关闭[^3]。

> [!example] 实操
> 什么都不用做。你现在的 `CLAUDE.md` 在 dsh 里照常被读。想加「只在这个项目生效」的补充，再写一个 `AGENTS.md`；想加「机器级偏好」，写 `~/.dsh/AGENTS.md`。

## 3. Skills：建 `.dsh/skills/` 文件夹，格式和 Claude Code 兼容

dsh 的本地技能扫描按 rank 顺序 **first-wins**（同名取先命中的）[^2][^4]：

| Rank | 源 | 根目录 |
|---|---|---|
| 100 | project-dsh | `<项目根>/.dsh/skills` |
| 200 | project-agents | `<项目根>/.agents/skills` |
| 300 | custom | `Config.customSkillDirs` |
| 400 | user-dsh | `~/.dsh/skills` |
| 500 | user-agents | `~/.agents/skills` |
| 600 | bundled | 包内自带（`Config.bundledSkillDir`） |

**格式**与 Claude Code 一致：`<name>/SKILL.md`（或单文件 `<name>.md`），YAML frontmatter 里 **`name` / `description` 必填**，`whenToUse` 等可选；名字 kebab-case（`^[a-z0-9]+(?:-[a-z0-9]+)*$`）[^4]。

**机制**：目录被 watcher 监听，**新建即热加载**，不用重启。模型侧通过一个 `skill({name})` 工具按需加载正文——目录里只放 `name` + `description` 摘要（渐进式披露，不把全文塞进每轮请求）[^2]。

> [!example] 最小 skill
> ```
> .dsh/skills/my-skill/SKILL.md
> ```
> ```yaml
> ---
> name: my-skill
> description: Do something useful when the user asks for it.
> ---
> 正文指令……
> ```

> [!tip] 大白话
> 技能像「说明书抽屉」：抽屉外只贴标题（name）和一句话简介（description），模型看到简介觉得合适才拉开抽屉读全文。所以一个技能好不好用，简介写没写清楚很关键。

## 4. Hooks：两条路，先试「桥接复用」

dsh 的 hooks 有两套完全不同的玩法[^5]：

### 4.1 桥接复用你现成的 Claude Code hooks（迁移成本最低）

装 `@deepseek-ai/dsh-hooks-claude-code` 桥接插件，它把你 `hooks.json`（或 settings 的 `hooks` 键）里的 shell 命令 hooks 翻译成 dsh 的类型化扩展点[^5][^6]：

```yaml
- id: hooks-cc
  name: '@deepseek-ai/dsh-hooks-claude-code'
  config:
    configPath: ./hooks.json        # 你现成的 Claude Code hooks 配置
    # projectDir 省略时，默认把 CLAUDE_PROJECT_DIR 导出为 session 工作目录
```

> [!note] 这段写进哪个文件？
> 这个 `- id: hooks-cc` 块是 **cordis.yml 补丁文件里的插件行**，不是丢进 `.dsh/` 目录的独立文件。dsh 没有「一份完整配置」，是四层补丁树叠加（见 [[DeepSeek-Harness 配置体系]]），按生效范围选落点：

| 生效范围 | 写进哪个文件 | 怎么生效 |
|---|---|---|
| 项目里先试跑 | 项目根新建 `./cordis.yml` | `pnpm dsh web --patch ./cordis.yml` |
| 某个 profile 长期 | `~/.dsh/profiles/<name>/cordis.patch.yml` | 随该 profile 自动叠加（补丁树第②层） |
| 机器全局 | `~/.dsh/cordis.patch.yml` | 所有 profile 共享（补丁树第③层） |

> 两个前提：① 插件包要能解析——`name` 引用 npm 包 `@deepseek-ai/dsh-hooks-claude-code`，未安装先 `dsh plugin --profile <name> add @deepseek-ai/dsh-hooks-claude-code`；② `configPath: ./hooks.json` 是进程级、按启动 cwd 解析（见第 7 节坑 2），要么写绝对路径，要么在 `hooks.json` 所在目录启动。

支持的 hook 点：`SessionStart` / `UserPromptSubmit` / `PreToolUse` / `PostToolUse` / `Stop` / `SubagentStart` / `SubagentStop`[^6]。`CLAUDE_PROJECT_DIR` 会自动注入给 hook 进程，常见项目相对路径的 hook 不用改就能跑。

### 4.2 原生插件（更强大，但要点编程）

「原生 hook」就是普通的 cordis 插件，监听类型化扩展点并返回决策[^5]：

| 扩展点 | 用途 |
|---|---|
| `tools/pre-execute` | 权限门：allow / deny / ask |
| `tools/post-execute` | 改写展示内容或返回值 |
| `agent/pre-step` | 每步前的策略 |
| `agent/turn-stopping` | 结束前干预 |
| `subagent/start` / `subagent/end` | 子代理生命周期 |

```ts
ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
  if (!(await isAllowed(exec))) {
    return { kind: 'deny', reason: 'Denied by policy.' }
  }
  return next()
})
```

桥接是「兼容适配器，不是威力工具」——原生插件有类型化返回、完整 `ctx`、无序列化边界，更强大[^6]。你已经会写插件（见 [[DeepSeek-Harness 插件开发核心]]），需要自定义策略时走这条。

> [!note] 选择建议
> 想「原样跑起现有 hooks」→ 桥接；想「写新的、复杂的策略」→ 原生插件。

## 5. MCP：每个 server 一个 mcp-client 插件实例

dsh 不做「往 `.dsh` 里放个配置文件」这种魔法，MCP 是 **每个 server 在 `cordis.yml` 里挂一个 `@deepseek-ai/dsh-mcp-client` 实例**[^7]：

```yaml
- id: mcp-github
  name: '@deepseek-ai/dsh-mcp-client'
  config:
    serverName: github                # 必填，^[A-Za-z0-9_-]{1,32}$，跨实例唯一
    transport: stdio
    command: npx
    args: ['-y', '@modelcontextprotocol/server-github']
    env:
      GITHUB_TOKEN: '!!js process.env.GITHUB_TOKEN'

- id: mcp-web
  name: '@deepseek-ai/dsh-mcp-client'
  config:
    serverName: web
    transport: streamable-http
    url: http://localhost:3000/mcp
    headers:
      Authorization: '!!js `Bearer ${process.env.MCP_TOKEN}`'
```

模型看到的工具名是 **`mcp__<serverName>__<工具名>`**——和 Claude Code / Codex 的命名一致，权限规则可以按 `mcp__github__*` 这种前缀统一写[^7]。

- 生命周期：boot 时连接 → `listTools` → 注册；**HMR 热换**（改配置自动重连重注册）；支持自动重连（`reconnect.enabled: false` 可关）[^7]；
- **只桥接 Tools**，Resources / Prompts 暂不消费[^7]。

> [!tip] 大白话
> `serverName` 是你给每个 MCP server 起的本地小名（如 github、web）。它决定模型看到的前缀——起得短，模型看到的工具名就短，省 token。

## 6. 照搬 Claude Code：四步操作清单

把你现有的 Claude Code 配置迁到 dsh，按这个顺序来：

```bash
# ① Rules —— 什么都不用做
#    项目根 CLAUDE.md 自动被读；想加机器级规则写 ~/.dsh/AGENTS.md

# ② Skills —— 复制文件夹（项目级或用户级）
mkdir -p .dsh/skills
cp -r ~/.claude/skills/* .dsh/skills/

# ③ Hooks —— 在 cordis.yml 里加桥接插件（见 4.1）

# ④ MCP —— 在 cordis.yml 里每个 server 加一个实例（见 5）
```

然后按你的 profile 启动：

```bash
pnpm dsh --profile <name>          # Web 模式
# 或 headless
```

> [!tip] 大白话
> 这四步对应「黑板（rules）不用擦、说明书抽屉（skills）搬过来、门禁规则（hooks）找物业登记、外部工具（MCP）走申请流程」。前三步几分钟，第四步每接一个 server 花几分钟。

## 7. 三个坑（照搬前必看）

1. **hooks 桥接只跑 shell-form 的 `type: 'command'`**；`http` / `mcp_tool` / `prompt` / `agent` 类型的 hook 会被解析但跳过；`updatedInput`（工具入参改写）不生效，只记录告警[^6]。
2. **`configPath` 是进程级**：启动时读一次，相对路径按进程启动 cwd 解析；**不会**像 Claude Code 那样按 session 自动发现项目里的 `hooks.json`（官方标记 `TODO(per-session-hook-config)`）[^6]。
3. **MCP 只桥接 Tools**：Resources / Prompts 不会出现在 dsh 里；MCP server 的工具描述烂就是烂，dsh 原样透传（garbage-in-garbage-out）[^7]。

---

## 本章小结

> [!summary]
> - `.dsh` = 用户级 harness home（`~/.dsh`，`$DSH_HOME` 可覆盖）+ 项目级技能源（`.dsh/skills`），**不是** hooks/mcp 的配置入口；
> - **Rules**：项目根 `AGENTS.md` 和 `CLAUDE.md` 默认都读，`CLAUDE.md` 零迁移；本地覆盖 `AGENTS.local.md`/`CLAUDE.local.md`；用户级 `~/.dsh/AGENTS.md`；
> - **Skills**：`.dsh/skills/<name>/SKILL.md`（或 `.agents/skills/`），格式与 Claude Code 兼容，热加载；扫描优先级 项目 `.dsh` > 项目 `.agents` > custom > 用户 `.dsh` > 用户 `.agents` > bundled；
> - **Hooks**：桥接插件 `dsh-hooks-claude-code` 直接复用 hooks.json（只跑 shell command、无入参改写）；原生 cordis 插件监听 `tools/pre-execute` 等扩展点更强大；
> - **MCP**：每 server 一个 `dsh-mcp-client` 实例配在 `cordis.yml`，工具名 `mcp__<serverName>__<tool>`，只桥接 Tools。

相关：[[DeepSeek-Harness 配置体系]] · [[DeepSeek-Harness 与ClaudeCode对照迁移]] · [[DeepSeek-Harness 插件开发核心]] · [[Claude Code MOC]]

---

## 更新记录

- 2026-08-15：4.1 补充「这段写进哪个文件」落点说明（试跑 `--patch` / profile `cordis.patch.yml` / home `cordis.patch.yml` 三层 + 两个前提坑）。
- 2026-08-15：新建。基于官方源码（agent-instructions / skills subsystem / extension-cookbook / config-catalog / mcp-client）核对。

---

[^1]: 素材来源：`packages/context/agent-instructions/src/config.ts`（`instructionFileCandidates` / `localInstructionFileCandidates` 默认值），2026-08-15 抓取。
[^2]: 素材来源：`docs/subsystems/skills.md`（本地发现优先级、格式、skill({name}) 工具），2026-08-15 抓取。
[^3]: 素材来源：`docs/config-catalog.md`（`workspaceContext` 配置），2026-08-15 抓取。
[^4]: 素材来源：Agent Note `2026-07-05-skill-system`（`.dsh`/`.agents` 扫描、frontmatter 契约），2026-08-15 抓取。
[^5]: 素材来源：`docs/cookbook/extension-cookbook.md`（hook 扩展点与 feature→mechanism 映射表），2026-08-15 抓取。
[^6]: 素材来源：Agent Note `2026-06-30-hook-bridges`（dsh-hooks-claude-code 支持的点、坑、TODO），2026-08-15 抓取。
[^7]: 素材来源：Agent Note `2026-07-07-mcp-client-plugin`（每 server 一实例、`mcp__<serverName>__<tool>` 命名、只桥接 Tools），2026-08-15 抓取。
