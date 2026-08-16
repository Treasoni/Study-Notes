# 深度素材：写自己的 DeepSeek-Harness Agent Preset

> 收集日期：2026-08-16 · 来源层级：官方 preset 文档 + 官方内置 preset 源码（一手）

## 1. Preset 目录结构（官方 preset 文档）

- preset = 一个目录，目录名即 id（必须 `[a-z0-9][a-z0-9-]*`）
- `agent.cordis.yml`（必需）：装配清单 = **插件行的顶层列表**
- `preset.yml`（可选）：只承载展示文本 `name` / `description`；`id` 是目录名、`trust` 来自根，二者在 preset.yml 里不可写
- 附带资产（skill 目录、插件文件）随目录迁移
- 读取失败（缺失/格式错/类型错/空）→ 降级为「无元数据」，选择器回退用 id 显示

## 2. agent.cordis.yml 解析规则

- **包名**（`@deepseek-ai/dsh-*`）：从宿主组合的 base URL 解析，不从 preset 目录解析
- **相对路径**：从 preset 自身目录解析 → 附带的插件文件 / skill 目录跟着 preset 走
- **绝对路径**：转 `file:` URL 供 ESM 导入（处理 POSIX / Windows 盘符 / UNC）

## 3. 官方 4 preset 的真实身份

### standard（母版）— `apps/cli/config/agent-presets/standard/agent.cordis.yml`

| 类 | 插件行（id → 包名） | 关键 config |
|---|---|---|
| 身份 | `persona` → `@deepseek-ai/dsh-persona` | text 模板含 `{{model}}`/`{{cwd}}` |
| 指令 | `agent-instructions` → `@deepseek-ai/dsh-agent-instructions` | `maxBytes: 65536` |
| Shell | `tool-bash` → `@deepseek-ai/dsh-tool-bash` | win32 禁用 |
| Shell | `tool-pwsh` → `@deepseek-ai/dsh-tool-pwsh` | 非 win32 禁用 |
| 文件 | `tool-fs` / `tool-fs-search` | fs-search `sampleOverCapGlobResults: false` |
| 后台任务 | `tool-jobs` | — |
| Skills | `skill-filesystem` / `tool-skill` | — |
| 目标 | `tool-goal` | — |
| 计划组 | `plan-mode` → `@deepseek-ai/dsh-plan-mode` | `isolate: { planMode: true }` |
| 压缩组 | `compaction-basic` / `command-compact` / `tool-result-pruner` | pruner `thresholdChars: 8192 / headChars: 4096 / tailChars: 1024` |
| 委派组 | `tool-subagent-control` / `tool-subagent`(spawn) / `tool-subagent-fork`(fork) / `tool-subagent-codex`(disabled) / `tool-subagent-claude-code`(disabled) / `workflow-worker-thread` / `tool-workflow` / `tool-ralph` | `isolate: { workflowEngine: true }`；subagent `provider: spawn, backgroundMode: continuable`；ralph `subagentProvider: spawn, maxRounds: 64` |
| 其余 | `tool-ask-user` / `tool-todo` / `tool-web` | todo `allowParallelInProgress: true`；web `fetch: false, searchTimeoutMs: 60000` |

### minimal（极简）— 双工具固定提示词

`agent.cordis.yml` 结构（非 standard 副本，独立构造）：
- `persona` → `@deepseek-ai/dsh-persona`：`text: "You are a helpful software engineer assistant."` + `complete: true` + `includeRuntimeContext: false`
  - `complete: true` = 组装后这个人设被恢复为**唯一**系统提示段，其他装配监听器插不进提示文本
  - `includeRuntimeContext: false` = 不注入运行时上下文快照
- `persistent-shell`（`cordis:group`，`isolate: { terminals: true }`）：pty + terminal-bash + persistent-bash（均 `timeoutMs: 300000`）
- `filesystem`（`cordis:group`，`isolate: { fs: true }`）：fs-local（`cwd: process.env.DSH_CWD ?? process.cwd()`）+ str-replace-editor（`maxOutputChars: 16000`）
- 无 compaction、无 web、无 skill、无计划/委派；**需要 POSIX terminal 底座，Windows 不可用**

### code（PTC 模式）— standard 完整副本

- 全部 standard 能力 + Code Mode SDK（模型用 TS 程序组合多步操作）
- 经 Code Mode SDK 呈现，非目录级差异（目录结构与 standard 相同，差异在运行时 SDK）

### cordis（创造模式）— standard 完整副本 + 自指

相比 standard 的增量（其余原样不变）：
- `persona` 定制：加「两平面模型」（HOST composition vs AGENT PRESET）——编辑属于哪一平面、authoring 规则（复制 shipped preset、放用户 `.agent-presets/`、先加载 `editing-cordis-compositions` skill）
- `tool-cordis` → `@deepseek-ai/dsh-tool-cordis`：读实时运行时、临时挂载/卸载插件；头注释：「信任边界而非沙箱，把该 preset 的会话当 shell 访问」
- `skill-filesystem` → `@deepseek-ai/dsh-skill-filesystem`：`customSkillDirs: [baseUrl/skills]`——装配创作 skill 随 preset 走

## 4. 创作 API：`ctx.agentPresets.copy(from, id, name?)`

- **唯一创作写入**：输入只有两个 id（from + 目标 id）+ 可选展示名；调用方从不直接提供 composition 文本
- 复制整目录到第一个 user-trust 根
- 自动做四件事：
  1. 校验 id 合法（`[a-z0-9][a-z0-9-]*`）/ 未占用 / 源存在（三者任一失败即拒绝）
  2. 收紧权限：文件 `0o600`、目录 `0o700`
  3. 解符号链接（自包含）
  4. 重写 `preset.yml`：保留源 description、丢弃源 name 和 roster `order`
- `cordis` 创造模式即此用途：运行时检查 + 内存试验插件 + 据此组合新 preset

## 5. 选择 / 切换 / 生效

- 会话创建时：会话选择器列出各 preset 摘要；`resolveSessionPreset(session)` 解析**实际运行** preset（读解析结果，不是创建头）
- 会话中途切换：扫描会话事件日志找最新 `agent-preset/selected` 事件，回退到会话头默认
- 设默认：配置层 `agent-presets: { default: <id> }`（默认 preset 是用户设置，覆盖部署工程默认）
- 空 agent 重链：`ctx.agentPresets.recompose(agentCtx, id)`；产出过内容后网关返回 `agent-preset-locked`
- 挂在 agent：agent 工厂 `setup(agentCtx)` 里 `mount(agentCtx, id?)`
- **发现不缓存**：`list()` / `resolve()` 每次重读目录 → 新写 preset 立即可见；`agent.cordis.yml` 缺失/不可解析 → 列出并标 `broken` reason，id 仍被占用直到删目录

## 6. 配置命名空间

- `default`（必填）：未指定时使用的 preset id
- `roots`（默认 `[]`）：扫描目录按优先级排序
- `includeUserRoot`（默认 `true`）：追加 `<dshHome>/.agent-presets` 为 user 根

## 关键引用（官方 URL）
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/preset/agent-presets/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/config/agent-presets/standard/agent.cordis.yml
- https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/config/agent-presets/standard/preset.yml
- https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/config/agent-presets/minimal/agent.cordis.yml
- https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/config/agent-presets/cordis/agent.cordis.yml
- 关联 vault 笔记：`AI学习/DeepSeek-Harness 教程/DeepSeek-Harness 配置体系.md` §2.1
