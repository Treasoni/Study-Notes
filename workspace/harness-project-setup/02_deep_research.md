# 深度收集结果 - 从零搭建 DeepSeek-Harness 工程

> 运行：harness-project-setup | 阶段：P2 深度收集 | 日期：2026-08-16
> 方向：**专门针对 DeepSeek-Harness**（方向调整后重做）
> 核心问题：开始一个 dsh 项目，先创建哪些文件？skills 放在哪里？hooks / subagents / rules / AGENTS 怎么配？

## 一、范围

以 dsh 官方仓库与子系统文档（B1-B3，tier 1）为权威基线，叠加用户 vault 已整理的 dsh 笔记（D1-D7，tier 2 实测），回答"先建哪些文件 + 每个文件怎么填"的文件级事实。已排除：通用 Claude Code 官方文档（S1-S5，方向调整前误用，本版不再作为主干）、社区模板（C1-C3）。

## 二、源表

| ID | 标题 | URL | 层级 | 抓取日期 |
|----|------|-----|------|----------|
| B1 | dsh 官方 `AGENTS.md`（仓库总纲） | https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/AGENTS.md | 1 | 2026-08-16 |
| B2 | dsh skills 子系统文档 | https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/docs/subsystems/skills.md | 1 | 2026-08-16 |
| B3 | dsh config-catalog（cordis.yml 可配键） | https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/docs/config-catalog.md | 1 | 2026-08-16 |
| D1 | 你的笔记《配置实战-接入skills-hooks-mcp-rules》 | `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness 插件开发教程/03-配置实战-接入skills-hooks-mcp-rules.md` | 2 | 2026-08-16 |
| D2 | 你的笔记《配置体系-补丁树Profile与bundle》 | `.../02-配置体系-补丁树Profile与bundle.md` | 2 | 2026-08-16 |
| D3 | 你的笔记《Agent Preset 实操》 | `.../12-实战-写自己的AgentPreset.md` | 2 | 2026-08-16 |
| D4 | 你的笔记《Subagent 教程》（README+第2章+第7章） | `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness Subagent 教程/*` | 2 | 2026-08-16 |
| D5 | 你的笔记《是什么 / 安装 / 最小骨架》 | `AI学习/DeepSeek-Harness 教程/{是什么,安装与快速上手,插件开发教程/05-实战-起步-最小骨架与脚手架}.md` | 2 | 2026-08-16 |

## 三、claim/来源映射（按脚手架主题组织）

### 3.1 心智模型：dsh 是"空壳 + 插件树"，不是"核心 + 扩展"

| Claim | 来源 |
|-------|------|
| dsh = `Model + Harness = Agent` 里的 Harness；不是模型/API 客户端，而是组织文件/终端/网页/工具调用/上下文的运行框架 | D5 |
| 核心公式："DeepSeek Harness is a plugin-based agent harness on vendored Cordis: **everything is a plugin**"；无特权核心，模型适配器/工具注册表/会话日志/Agent loop/沙箱均可替换 | B1, D5 |
| **写插件 ≠ 改配置文件**：能力本身是 TypeScript 代码，`cordis.yml` patch 只是"装载"手段 | D5 |
| 新增行为走扩展点而非改 loop："Plugins, not loop changes: new behavior goes on documented extension points" | B1 |
| 注册是 effect：每个贡献走 `ctx.effect()` / `ctx.on()`，registry 的 `register()` 返回 disposer | B1 |

### 3.2 指令入口：AGENTS.md / CLAUDE.md / rules（零迁移区）

| Claim | 来源 |
|-------|------|
| `instructionFileCandidates` 默认 `['AGENTS.md', 'CLAUDE.md']`——dsh 默认两个都当指令文件候选；从 session 工作目录向上找含 `.git` 的最近祖先作项目根，逐目录加载 | B3, D1 |
| 本地覆盖：同目录 `AGENTS.local.md` / `CLAUDE.local.md` 在基础文件之后加载；`localInstructionFileCandidates` 空则禁用 overlay | B3, D1 |
| 用户级：固定读 `~/.dsh/AGENTS.md`（`dshHome`，默认 `$DSH_HOME` 或 `~/.dsh`） | B3, D1 |
| `workspaceContext` 控制自动加载与字节预算：`maxBytes`（UTF-8 字节上限，非正数/非有限禁用）、`maxSourceBytes`、`projectRootMarkers`；设 `false` 可整体关闭（hermetic prompts） | B3, D1 |
| 官方仓库自身：根 `AGENTS.md` + `CLAUDE.md` symlink 到 AGENTS.md（root/packages/examples 三处），edit 真文件 | B1 |
| **迁移结论：你的 CLAUDE.md 在 dsh 里原样生效，零迁移** | D1 |

### 3.3 Skills 放置与结构（dsh 版）

| Claim | 来源 |
|-------|------|
| 本地技能扫描按 rank first-wins：`100 project-dsh <root>/.dsh/skills` → `200 project-agents <root>/.agents/skills` → `300 custom Config.customSkillDirs` → `400 user-dsh <dshHome>/skills` → `500 user-agents <agentsHome>/skills` → `600 bundled Config.bundledSkillDir` | B2, D1 |
| 项目根 = 最近含 `.git` 的祖先；无 `.git` 用当前 cwd；`ctx.fs` 存在时 git-root walk 走 fs 服务 | B2 |
| 格式与 Claude Code 兼容：目录 bundle `<name>/SKILL.md` 或单文件 `<name>.md`；名字 kebab-case `^[a-z0-9]+(?:-[a-z0-9]+)*$`；不支持嵌套 `**/SKILL.md` 递归发现 | B2 |
| **frontmatter 只强制两键**：`disable-model-invocation` 与 `user-invocable`（精确 kebab-case），缺省均视为 `true`；两键皆 false 则该 skill 只能被受信 `ctx.skills.get()` 调用 | B2 |
| 机制：目录被 watcher 监听，**新建即热加载**（模型侧 `write`/`edit` 观测同步失效、host watcher 覆盖 IDE/Git/shell/外部进程）；模型通过 `skill({name})` 工具按需加载正文（目录只放摘要，渐进式披露） | B2, D1 |
| 全文不缓存：registry 的每次 `get()` 重读当前正文；资源文件（bundle 下 scripts/assets）不作为 catalog 变更 | B2 |
| 同一层内同名按 rank → provider order → local order 决出；跨层最近层赢（"nearest layer's entry wins a duplicate skill name outright"）；runtime 条目 outrank user 条目 | B2 |

### 3.4 Hooks（两条路：桥接复用 vs 原生插件）

| Claim | 来源 |
|-------|------|
| **hook ⊂ 插件**：dsh 一切能力都是 cordis 插件（容器），hook 只是"监听扩展点、返回决策"的那类职责；桥接插件与 MCP client 是插件但不是 hook | D1 |
| 桥接插件 `@deepseek-ai/dsh-hooks-claude-code`：`configPath` 指向 hooks.json 或 settings 的 `hooks` 键；`pluginRoot` 替换 `${CLAUDE_PLUGIN_ROOT}`；`projectDir` 替换 `${CLAUDE_PROJECT_DIR}` 并导出为 env；`defaultTimeoutMs` 默认 600000 | B3, D1 |
| 桥接支持的 hook 点：`SessionStart / UserPromptSubmit / PreToolUse / PostToolUse / Stop / SubagentStart / SubagentStop` | D1 |
| **桥接只跑 shell-form `type: 'command'`**：`http` / `mcp_tool` / `prompt` / `agent` 类型被解析但跳过；`updatedInput` 入参改写不生效只告警 | D1 |
| `configPath` 进程级：启动读一次，相对路径按进程启动 cwd 解析，不按 session 自动发现项目 hooks.json（官方 `TODO(per-session-hook-config)`） | B3, D1 |
| 原生插件（更强大）：`ctx.on('tools/pre-execute', ...)` 返回 `{kind:'deny',reason}` 或 `next()`；扩展点：`tools/pre-execute`(权限门 allow/deny/ask)、`tools/post-execute`、`agent/pre-step`、`agent/turn-stopping`、`subagent/start`/`subagent/end` | D1 |
| 选择建议：想"原样跑起现有 hooks"→ 桥接；想"写新的复杂策略"→ 原生插件 | D1 |

### 3.5 MCP（每个 server 一个 mcp-client 实例）

| Claim | 来源 |
|-------|------|
| `@deepseek-ai/dsh-mcp-client`：每 server 一个插件实例配在 cordis.yml；`serverName`（`mcp__<serverName>__<rawName>` 命名空间，`[A-Za-z0-9_-]{1,32}`，跨实例唯一） | B3, D1 |
| transport 二选一：`stdio`（command/args/env/cwd）或 `streamable-http`（url/headers）；`toolCallTimeoutMs`、`failOnStartupError`、`reconnect`（enabled 默认 true / initialDelayMs 500 / maxDelayMs 30000 / maxAttempts 10） | B3 |
| 生命周期：boot 连接 → listTools → 注册；HMR 热换（改配置自动重连重注册）；**只桥接 Tools**，Resources/Prompts 暂不消费 | D1 |
| 迁移成本：每 server 几行；权限规则可按 `mcp__github__*` 前缀统一写 | D1 |

### 3.6 Subagents（ctx.subagents + SubagentProvider，dsh 版）

| Claim | 来源 |
|-------|------|
| **对比 Claude Code**：Claude Code 从 `.claude/agents/*.md` 自动发现，dsh 用 `ctx.subagents.registerProvider` 显式注册（effect-scoped：移除阻止新 start、不撤销已返回 run） | D4 |
| `SubagentProvider` 契约五块：`name` 唯一注册名；`capabilities` 四 flag（outputSchema/depthLimit/toolFilter/persona）为启动期静态声明，缺则请求对应能力的 start 被 `UNSUPPORTED_CAPABILITY` 响亮拒绝；`inheritsParentContext` 只是"是否注入父对话种子"的描述性标注（不担保工具/服务/权限继承）；`start()` 发布后返回 handle、发布前失败必须清理；`prepareContinuable?` 存在即能力 | D4 |
| 现成 provider 家族：`spawn`（in-process 四项全支持、无父历史）、`fork`（inheritsParentContext:true）、`acp`（独立子进程、零能力）、`dsh-sdk`（完整 peer harness、全 false、可 `maxDepth:'provider-managed'`） | D4 |
| 工具化：`dsh-tool-subagent` 把 provider 暴露成模型可调能力；一个 provider 绑一个 `toolName`（全局唯一）；maxDepth 默认 3、0 禁止委派；后台 one-shot 结果经 task 工具回传 | D4 |
| 消费语义：`SubagentRun` 一次性前台委派，await 后**必须 dispose**；result 不因 child 级失败 reject（`stopReason:'error'` 正常 resolve）；output 取最后一个非空 assistant 消息；stopReason 五值（completed/aborted/error/max-tokens/refusal），非 completed 可能不完整 | D4 |

### 3.7 配置体系：补丁树 / Profile / Agent Preset

| Claim | 来源 |
|-------|------|
| dsh **没有"一份完整配置"**，是四层 YAML 补丁在空根上叠加：① bundle 补丁（profile.bundles 点名）→ ② profile 自身 `cordis.patch.yml` → ③ home 级 `$DSH_HOME/cordis.patch.yml` → ④ `--patch <path>`（按 argv 顺序）；"Later layers win per row"，**整行替换不做深合并** | D2 |
| 排查利器：`dsh --profile <name> --dump-config` / `--dump-default-config` 摊开合成结果 | D2 |
| **Profile（进程级）管装哪些 bundle**；**Agent Preset（会话级）管会话用什么能力**（工具/提示词/skill/子代理）；两轴正交 | D2, D3 |
| preset 即目录：`agent.cordis.yml`（插件行装配清单，必需）+ 可选 `preset.yml`（仅展示文本），id=目录名 `[a-z0-9][a-z0-9-]*`；用户预设放 `~/.dsh/.agent-presets/<id>/`；内置 4 个：standard（母版）/ code / cordis / minimal（双工具极简、仅 POSIX、`complete:true` 单句提示） | D2, D3 |
| 内置 preset 只读，升级会覆盖；写自己的 = 复制 → 改清单 → 换名；规范做法 `ctx.agentPresets.copy(from, id, name?)`；写完完全重启 dsh 后在会话选择器选用；`agent-presets: {default: <id>}` 设默认 | D2, D3 |
| 插件接收配置：`Config` 接口 + **Schemastery** schema（不能用普通对象），默认值写 schema 上；坏配置响亮失败（fiber FAILED）；HMR 热替换 | D2 |

### 3.8 工程脚手架：从空目录开始一个 dsh 项目先建哪些文件

| Claim | 来源 |
|-------|------|
| **开发期**：dsh 源码仓库 clone → `pnpm install` → `pnpm run build` → `pnpm dsh web`（默认 http://127.0.0.1:3080）；写插件必须源码运行路径，npx 无仓库上下文跑不了 `--patch` 开发循环 | D5 |
| 最小插件 2 文件 = 插件模块 `src/index.ts`（`export const name` + `export function apply(ctx)`）+ 注册 patch `dev-cordis.patch.yml`（`- insert:` 注册）；patch `name` 必须绝对路径，相对路径**静默失效无报错** | D5 |
| `--patch` 相对路径按 dsh 源码仓库根解析（不是当前 shell 目录）；`pnpm dsh web` 是 `--profile web` 硬编码别名；验证信号 = 日志 `[<name>] plugin loaded!` | D5 |
| 只使用不开发：`npx @deepseek-ai/dsh web`；`pip install deepseek-harness-sdk`（Python 3.10+，仅 Linux x64/arm64 或 macOS 14+ arm64）；**认准官方包名 `@deepseek-ai/dsh` / `deepseek-harness-sdk`**，同名第三方包非官方 | D5 |
| Web UI 首配两步：Settings→Models 填 API Key（write-only，明文存 `$DSH_HOME/.credentials.yaml`）；Choose workspace 选项目目录（不选无法开始会话） | D5 |
| 用户级 harness home：`~/.dsh/`（`$DSH_HOME` 覆盖），含用户级 AGENTS.md、skills/、profiles/、.agent-presets/、cordis.patch.yml | D1, D2, D3 |
| 项目级技能源：`<项目根>/.dsh/skills/`；`dshHome` / `agentsHome`（`~/.agents`）由 skill-filesystem provider 配置 | B3, D1 |

## 四、矛盾与坑（dsh 版）

1. **patch `name` 相对路径静默失效**：不报错不警告，模块永远加载不上 → 第一步就写绝对路径（D5）。
2. **`--patch` 相对路径按仓库根解析**：从插件目录跑 `--patch ./dev-cordis.patch.yml` 会 ENOENT；要在仓库根给全相对路径（D5）。
3. **hooks 桥接只跑 shell command**：`http`/`mcp_tool`/`prompt`/`agent` 类型被跳过；`updatedInput` 不生效只告警（D1）。
4. **`configPath` 进程级**：启动读一次，不按 session 发现项目 hooks.json（官方 TODO）；相对路径按启动 cwd 解析，要么写绝对路径、要么在 hooks.json 目录启动（B3, D1）。
5. **MCP 只桥接 Tools**：Resources/Prompts 不出现；server 工具描述烂就是烂，garbage-in-garbage-out（D1）。
6. **补丁按行替换不做深合并**：同 id 整行覆盖，不是 Git 式字段合并；拿不准用 `--dump-config`（D2）。
7. **内置 preset 只读**：升级会覆盖；`minimal` 是测试用的、仅 POSIX、Windows 不可用；要"轻"复制 standard 自己裁（D3）。
8. **subagent 能力不匹配响亮失败**：`UNSUPPORTED_CAPABILITY` 是选错 provider，不是重试能解决；`outputSchema` 请求了不保证 `structured`；`inheritsParentContext` 名不副实（D4）。
9. **subagent 系列包无默认导出**：Cordis loader 解包会隐藏命名 `inject` 元数据；用命名导出（D4）。
10. **同名第三方包**：`pip install deepseek-harness`、`npx @deepseek-harness/mcp` 均非官方（D5）。
11. **developer preview 破坏性变更**："THERE WILL BE COMPATIBILITY-BREAKING CHANGES"；反馈走 GitHub Discussions，不开 Issues（D5, D4）。

## 五、实践指导（dsh 工程落地清单）

1. **先定使用 vs 开发**：只用 → `npx @deepseek-ai/dsh web`；要写插件/挂自定义 hooks/mcp → 源码路径（clone → pnpm install → build）。
2. **项目根指令文件**：`AGENTS.md` 或直接复用现有 `CLAUDE.md`（默认都读，零迁移）；想加项目专属规则写 `AGENTS.md`；机器级写 `~/.dsh/AGENTS.md`。
3. **项目级技能**：`mkdir -p .dsh/skills`，把要用的 skill 按 `<name>/SKILL.md`（或 `<name>.md`）放进去；格式与 Claude Code 兼容，目录热加载。
4. **hooks**：有现成 Claude Code hooks.json → 桥接插件一行接入（`@deepseek-ai/dsh-hooks-claude-code` + `configPath`）；要新策略 → 原生 cordis 插件监听 `tools/pre-execute` 等。
5. **MCP**：每 server 一个 `@deepseek-ai/dsh-mcp-client` 实例配在 cordis.yml，`serverName` 起短省 token。
6. **subagents**：先选 provider（spawn/fork/acp/dsh-sdk），用 `dsh-tool-subagent` 暴露给模型；要能力强制走 in-process；要跨 turn 续写走 continuable。
7. **配置落点**：试跑 `--patch ./cordis.yml`；长期用 profile `~/.dsh/profiles/<name>/cordis.patch.yml` 或 home 级 `~/.dsh/cordis.patch.yml`；`dsh plugin --profile <name> add` 管理 bundle。
8. **agent preset**：会话能力组合用 `agent-presets: {default: <id>}`；自定义 preset 复制到 `~/.dsh/.agent-presets/<id>/`。
9. **验证**：`pnpm dsh web` → Web UI 首配（Key + workspace）→ 新建会话跑通；headless 用 `pnpm dsh --profile headless "task"`（退出码 0/1）。

## 六、开放问题（大纲阶段需决策）

1. 笔记是**"使用 dsh 的工程脚手架"**（项目里建 AGENTS.md/.dsh/skills/cordis.yml 配 hooks/mcp/subagent）还是**"写 dsh 插件/扩展"**（源码路径建插件骨架）？你的问题问的是前者（工程脚手架），但 vault 已有笔记偏后者。
2. 是否需要把 subagent 单独成章展开（provider 选型/契约），还是只在"工程骨架"里给一句话挂载方式？vault 已有完整 Subagent 分册，可能只需指路。
3. 是否包含"对照 Claude Code 迁移表"作为贯穿线索（每节 dsh 配置 ↔ Claude Code 等价物）？你的 vault 笔记都是这个风格。
4. 笔记粒度：清单 + 每文件骨架级示例（上手），不含完整插件代码。

## 七、下游交接（handoff）

- **大纲生成（P3）**：以 §五 的 9 步落地清单为骨架，按用户问题顺序组织：先建哪些文件 → skills 放哪 → hooks → subagents → rules/AGENTS → 坑位 → 最小骨架 → Obsidian 发布。
- **素材引用**：每章用 §三 claim 表按主题引用（B1-B3 + D1-D5）；§四坑位作为各章"常见坑"。
- **代码示例**：从 D1-D5（你的 vault 笔记）提取真实 dsh 文件结构做目录树/配置片段；B2/B3 提供官方契约细节。
- **待用户确认**：§六 开放问题在 P3 大纲确认时逐项敲定。
