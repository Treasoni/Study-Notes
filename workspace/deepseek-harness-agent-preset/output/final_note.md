---
title: "DeepSeek-Harness Agent Preset 实操：选、换、造"
tags: [deepseek-harness, ai, agent, preset, 教程]
created: 2026-08-16
updated: 2026-08-16
status: updated
source_project: deepseek-harness
---

# DeepSeek-Harness Agent Preset 实操：选、换、造

> [!summary] 导读
> [[DeepSeek-Harness 配置体系|配置体系]] 的配套实操专册。上一篇讲了 preset「是什么」——会话级能力组合、4 个内置预设、目录结构；这篇专讲「怎么用」：**怎么选**（4 个预设的真实身份）、**怎么换**（切换 / 默认 / 重链）、**怎么造**（复制目录 / copy API / 真实示例 + 验证步骤）。

## 0. 一分钟结论

- **preset 就是一个目录**：`agent.cordis.yml`（必需，插件行装配清单）+ 可选 `preset.yml`（只放展示文本），id = 目录名；
- **写自己的 = 复制 → 改清单 → 换名字**：官方 preset 只读，复制到用户根 `~/.dsh/.agent-presets/<id>/` 再改；
- **规范做法**：`ctx.agentPresets.copy('standard', 'my-preset', '名字')`——`cordis` 创造模式就是干这个的；
- **写完立即可见**：preset 发现不缓存，完全重启 dsh 后在会话选择器里选用。

## 1. 选：4 个官方 preset 的真实身份

四个内置预设不是四个代码分支，而是 `apps/cli/config/agent-presets/` 下的四个目录。它们的关系一句话：**`standard` 是唯一母版，`code` 与 `cordis` 是它的完整副本，`minimal` 是独立构造的双工具极简版**。

| 预设 | 官方中文名 | 本质 | 一句话适用 |
|---|---|---|---|
| `standard` | 标准模式 | 全量编码 Agent（母版） | 日常默认，什么都能干 |
| `code` | PTC 模式 | standard 完整副本 + Code Mode SDK | 重工程：模型用 TS 程序组合多步操作 |
| `cordis` | 创造模式 | standard 完整副本 + 自指创作能力 | 造 preset：运行时检查 + 内存试验插件 |
| `minimal` | 极简模式 | 双工具固定提示词（独立构造） | 测试 / RL 对齐；**仅 POSIX，Windows 不可用** |

> [!tip] 怎么选
> 拿不准就用 `standard`。想「轻一点」**不要**选 minimal（它连 compaction 都没有，是给模型测试用的），而是复制 standard 自己裁掉工具——这正是这篇专册要教的事。

### 1.1 standard 的真实装配清单（母版）

`standard/agent.cordis.yml` 是插件行的顶层列表，几大类[^1]：

| 类 | 插件行（id → 包名） | 关键 config |
|---|---|---|
| 身份 | `persona` → `@deepseek-ai/dsh-persona` | 文本模板含 `{{model}}` / `{{cwd}}` |
| 指令 | `agent-instructions` → `@deepseek-ai/dsh-agent-instructions` | `maxBytes: 65536` |
| Shell | `tool-bash` → `@deepseek-ai/dsh-tool-bash` | win32 禁用 |
| Shell | `tool-pwsh` → `@deepseek-ai/dsh-tool-pwsh` | 非 win32 禁用 |
| 文件 | `tool-fs` / `tool-fs-search` | fs-search `sampleOverCapGlobResults: false` |
| 后台任务 | `tool-jobs` | — |
| Skills | `skill-filesystem` / `tool-skill` | — |
| 目标 | `tool-goal` | — |
| 计划组 | `plan-mode` → `@deepseek-ai/dsh-plan-mode` | `isolate: { planMode: true }` |
| 压缩组 | `compaction-basic` / `command-compact` / `tool-result-pruner` | pruner `thresholdChars: 8192 / headChars: 4096 / tailChars: 1024` |
| 委派组 | `tool-subagent-control` / `tool-subagent` / `tool-subagent-fork` / `tool-subagent-codex`(禁用) / `tool-subagent-claude-code`(禁用) / `workflow-worker-thread` / `tool-workflow` / `tool-ralph` | `isolate: { workflowEngine: true }`；subagent `provider: spawn, backgroundMode: continuable` |
| 其余 | `tool-ask-user` / `tool-todo` / `tool-web` | todo `allowParallelInProgress: true`；web `fetch: false, searchTimeoutMs: 60000` |

### 1.2 code 与 cordis：都是 standard 的完整副本

- **`code`**：standard 全量 + **Code Mode SDK**——把工具以「模型可用 TS 程序组合多步操作」的方式呈现。目录内容与 standard 相同，差异在运行时 SDK 呈现层；
- **`cordis`**：standard 全量 + 三样增量：① 定制的 `persona`（加入「两平面模型」：编辑属于 HOST composition 还是 AGENT PRESET，authoring 规则）；② `tool-cordis`（读实时运行时、临时挂载/卸载插件——官方标注是**信任边界而非沙箱**，把会话当 shell 访问）；③ `skill-filesystem` 带装配创作 skill（`customSkillDirs` 指向 preset 自己的 `skills/`）。

### 1.3 minimal：不是 standard 的子集，是独立构造

`minimal/agent.cordis.yml` 只有三组插件[^2]：

```yaml
- id: persona            # complete: true → 唯一系统提示段
  name: '@deepseek-ai/dsh-persona'
  config:
    text: You are a helpful software engineer assistant.
    complete: true
    includeRuntimeContext: false

- id: persistent-shell   # cordis:group, isolate: { terminals: true }
  name: cordis:group
  group: true
  isolate:
    terminals: true
  config:
    - id: pty
      name: '@deepseek-ai/dsh-terminal'
    - id: terminal-bash
      name: '@deepseek-ai/dsh-terminal-bash'
      config: { timeoutMs: 300000 }
    - id: persistent-bash
      name: '@deepseek-ai/dsh-tool-bash-persistent'
      config: { timeoutMs: 300000 }

- id: filesystem         # cordis:group, isolate: { fs: true }
  name: cordis:group
  group: true
  isolate:
    fs: true
  config:
    - id: fs-local
      name: '@deepseek-ai/dsh-fs-local'
      config:
        cwd: !!js process.env.DSH_CWD ?? process.cwd()
    - id: str-replace-editor
      name: '@deepseek-ai/dsh-tool-str-replace-editor'
      config: { maxOutputChars: 16000 }
```

「极简」是靠**少装配**做出来的：没有 compaction、没有 web、没有 skill、没有计划/委派。它要 POSIX terminal 底座，**Windows 上不可用**。

## 2. 换：切换与默认

| 场景 | 做法 |
|---|---|
| 会话创建时 | 会话选择器列出各 preset 摘要，挑一个 |
| 设默认 | 配置层写 `agent-presets: { default: <id> }`（默认 preset 是**用户设置**，覆盖部署工程默认） |
| 空 agent 重链 | `ctx.agentPresets.recompose(agentCtx, id)`——只能重链还没产出任何内容的 agent |
| 已产出后改 | 网关返回 `agent-preset-locked`，换不了 |

会话实际运行的 preset 由 `resolveSessionPreset(session)` 解析（读的是解析结果，不是创建头）；会话中途也能切——扫描事件日志找最新的 `agent-preset/selected` 事件，找不到就回退到会话头默认。

## 3. 造：写自己的 preset

### 3.1 前置认知

**目录结构**：preset 目录 = `agent.cordis.yml` + 可选 `preset.yml` + 附带资产（skill 目录、插件文件）。

**三条解析规则**（写清单前必须知道）[^3]：

1. 插件行的**包名**（`@deepseek-ai/dsh-*`）从宿主组合的 base URL 解析，不从 preset 目录解析——所以本地 preset 也能拿到 `node_modules` 里的 harness 包；
2. **相对路径**从 preset 自身目录解析——附带的插件文件 / skill 目录跟着 preset 走；
3. **绝对路径**转 `file:` URL 供 ESM 导入。

**id 与根**：id = 目录名，必须匹配 `[a-z0-9][a-z0-9-]*`，非法目录名被跳过；用户预设放 `~/.dsh/.agent-presets/<id>/`（`$DSH_HOME` 默认 `~/.dsh`），由 `includeUserRoot`（默认 true）追加为 user 根。

### 3.2 路线 A：复制目录（社区通用做法）

```bash
mkdir -p ~/.dsh/.agent-presets
# 官方预设源码在 <dsh 仓库>/apps/cli/config/agent-presets/ 下
cp -R <dsh 仓库>/apps/cli/config/agent-presets/standard ~/.dsh/.agent-presets/my-coding/
# 编辑 ~/.dsh/.agent-presets/my-coding/agent.cordis.yml —— 删/加插件行
# 编辑 ~/.dsh/.agent-presets/my-coding/preset.yml —— 改 name/description
# 完全重启 dsh，在会话选择器中选用
```

> [!warning] 内置 preset 不要直接改
> 部署随附的内置 preset 是只读的，**升级会覆盖**；想改就复制一份再改，这是官方明确的做法。

### 3.3 路线 B：`ctx.agentPresets.copy(from, id, name?)`（规范做法）

这是官方「**唯一的创作写入**」API——调用方只给两个 id 加一个可选名字，从不手写 composition 文本。它自动做四件事[^3]：

1. **校验**：id 合法 / 未占用 / 源存在，三者任一失败即拒绝；
2. **收紧权限**：文件 `0o600`、目录 `0o700`；
3. **解符号链接**（自包含）；
4. **重写 `preset.yml`**：保留源的 description，丢弃源的 name 和 roster `order`。

```ts
// 在插件代码里（cordis 创造模式就是干这个的）
ctx.agentPresets.copy('standard', 'my-coding', '我的编码模式')
```

### 3.4 真实示例：造一个「本地聚焦」preset

目标：从 `standard` 派生一个「去网页、去子代理/工作流」的本地聚焦版——只留文件 + Shell + 规划 + 压缩，删掉 `tool-web` 和委派组。

**第 1 步：复制**

```bash
mkdir -p ~/.dsh/.agent-presets
cp -R <dsh 仓库>/apps/cli/config/agent-presets/standard ~/.dsh/.agent-presets/local-focus/
```

**第 2 步：改 `agent.cordis.yml`**——删掉 `tool-web` 行和整个委派组：

```yaml
# 删除前的行（local-focus 版直接删掉这几段）：
- id: tool-web
  name: '@deepseek-ai/dsh-tool-web'
  config:
    fetch: false
    searchTimeoutMs: 60000

# 委派组整段删除：
- id: tool-subagent-control
  name: '@deepseek-ai/dsh-tool-subagent-control'
# ...（tool-subagent* / workflow-worker-thread / tool-workflow / tool-ralph 全部删除）
```

保留计划组、压缩组、`tool-ask-user` / `tool-todo` / `tool-goal`——本地聚焦但仍是「能规划、能追问、能长对话」的完整 agent。

**第 3 步：改 `preset.yml`**

```yaml
---
name: 本地聚焦
description: standard 的精简版：去掉网页检索与子代理/工作流，只留本地文件、Shell、计划与压缩能力。
order: 1
---
```

**第 4 步：验证**

```bash
# 完全重启 dsh（preset 发现不缓存，重启即可见）
pnpm dsh
# 在会话选择器中应看到「本地聚焦」；选它进入会话
```

进会话后确认两件事：工具列表里**没有** `web_search` / `subagent` / `workflow`，且 `plan_mode` 等规划工具还在。

> [!tip] 坏了的 preset 不会静默消失
> `agent.cordis.yml` 缺失或不可解析时，preset 会列出并标注 `broken` 原因，id 仍被占用直到你删掉目录——所以写坏了大不了删目录重建，不会污染别的预设。

## 4. 验证与排错速查

| 症状 | 原因 | 处理 |
|---|---|---|
| 新 preset 不在选择器里 | 没重启 / 目录名非法 | 完全重启；检查 id 是否匹配 `[a-z0-9][a-z0-9-]*` |
| 选择器显示 `broken` | `agent.cordis.yml` 缺失或不可解析 | 修文件或删目录重建 |
| 会话里没有预期的工具 | 包名解析失败 / 插件行拼错 | 包名走宿主 base URL，别用相对路径引 harness 包 |
| 切 preset 失败 `agent-preset-locked` | agent 已产出过内容 | 换一个空 agent，或从头建会话 |
| `copy()` 被拒 | id 非法 / 已占用 / 源不存在 | 逐个核对三项 |

## 5. 避坑清单

- **别改内置 preset**：升级会覆盖；复制一份再改；
- **`minimal` 是测试用的**，Windows 不可用；要「轻」就复制 standard 自己裁；
- **`cordis` 的 `tool-cordis` 是信任边界**：官方明确「把该 preset 的会话当 shell 访问」，别在不可信环境用它；
- **写完要完全重启 dsh**：preset 发现不缓存，但会话选择器在新进程才刷新；
- **preset.yml 只放展示文本**：id 是目录名、trust 来自根，这两个写在 preset.yml 里没用。

## 6. 小结

> [!summary]
> - **选**：`standard` 是母版，`code` / `cordis` 是它的完整副本，`minimal` 是独立构造的双工具极简版（仅 POSIX，测试用）；
> - **换**：会话选择器临时选、`agent-presets: { default: <id> }` 设默认、`recompose()` 重链空 agent（产出过就锁）；
> - **造**：preset 即目录，写自己的 = 复制官方 → 改 `agent.cordis.yml` → 改 `preset.yml` → 放 `~/.dsh/.agent-presets/<id>/`；规范做法是 `ctx.agentPresets.copy(from, id, name?)`；
> - **验证**：完全重启后从会话选择器选用，坏文件会显示 `broken`，写坏了删目录重建。

相关：[[DeepSeek-Harness 配置体系|配置体系（preset 是什么）]] → 本册（preset 怎么造）→ [[DeepSeek-Harness 插件开发核心|插件开发核心（装配的插件从哪来）]]。

---

## 更新记录

- 2026-08-16：新建。依据官方 preset 文档 `packages/preset/agent-presets/README.zh.md` 与内置 `standard` / `minimal` / `cordis` 的 `agent.cordis.yml` 源码核对；与配置体系 §2.1 互为表里。

---

[^1]: 素材来源：官方内置 `standard/agent.cordis.yml`（2026-08-16 抓取）。
[^2]: 素材来源：官方内置 `minimal/agent.cordis.yml`（2026-08-16 抓取）。
[^3]: 素材来源：DeepSeek Harness 官方 preset 文档 `packages/preset/agent-presets/README.zh.md`（2026-08-16 抓取）。
