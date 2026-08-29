# Hermes 规则配置实战指南

> 本篇是一份面向已用过 Claude Code 的读者的 Hermes 规则配置实战指南。它覆盖 Hermes 规则体系的完整链路：SOUL.md 全局身份、AGENTS.md 项目规则、从 Claude Code 一键导入、config.yaml hooks 自动化，以及验证与排错。
> 全文以 Claude Code 的 CLAUDE.md / .claude/rules / settings.json / hooks 为对照锚点，适合想快速把已有 Claude Code 心智模型迁移到 Hermes 的读者。
> 建议按 01→06 顺序阅读：第一、二章建立"身份 vs 项目知识"的心智模型，第三到五章逐个落地；第六章的验证命令族可在实际配置时穿插使用，每配完一个文件就验证一次。

## 目录

1. [第一章 先看地图 — Hermes 规则体系定位与文件地图](#第一章-先看地图-hermes-规则体系定位与文件地图)
2. [第二章 全局身份 — 配置 ~/.hermes/SOUL.md](#第二章-全局身份-配置-hermessoulmd)
3. [第三章 项目规则 — 配置项目上下文文件（AGENTS.md 系列）](#第三章-项目规则-配置项目上下文文件-agentsmd-系列)
4. [第四章 对照迁移 — 从 Claude Code 一键导入](#第四章-对照迁移-从-claude-code-一键导入)
5. [第五章 自动化与拦截 — 配置 config.yaml hooks](#第五章-自动化与拦截-配置-configyaml-hooks)
6. [第六章 验证与排错 — 让规则确实生效](#第六章-验证与排错-让规则确实生效)

---

## 第一章 先看地图 — Hermes 规则体系定位与文件地图

> 篇幅：短 · 定位：总览地图 · 素材引用：S1, S2, S3, S9

你已经熟悉 Claude Code 的 `CLAUDE.md`、`.claude/rules`、`settings.json`、hooks 分层配置，但别急着照搬——Hermes 把"给 agent 的指令"拆成了另一套结构：**身份**与**项目知识**分开存放、分开加载。本章先给你一张地图：有哪些文件、各自管什么、怎么对照你已有的 Claude Code 心智模型。具体怎么配，留给后面各章逐个深入。

### 1.1 两类指令载体：SOUL.md（身份） vs 项目上下文文件（项目知识）

Hermes 把所有指令载体分成两类，存放位置和加载方式完全不同 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality) [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)。

**第一类：全局身份 — `SOUL.md`**

- 它是 agent 的**主身份（primary identity）**，占据系统提示的第 1 号槽位（slot #1），替换内置默认身份 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality) [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)。
- 只从 `HERMES_HOME`（默认 `~/.hermes/`）加载，**不探测当前工作目录**——你的"人设"不会因为换个项目就漂移 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality) [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)。
- 首次运行缺省自动 seed 一个默认文件；只要你已有该文件，它**永不覆盖** [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)。
- 职责：语气、沟通风格、直接程度、如何处理不确定/分歧——**"跟随你到处走"** 的东西 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)。

**第二类：项目上下文文件（Context Files）— `AGENTS.md` 系列**

- 每个会话按优先级链加载**一种**项目上下文文件（first-match wins，详见 1.3）[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)。
- 职责：项目架构、编码约定、工具偏好、命令/端口/路径、部署注意事项——**"属于某个项目"** 的东西 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)。

判断规则一句话：**"跟随你到处走 → SOUL.md；属于某个项目 → AGENTS.md"** [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)。补充一点：会话内临时切换语气用 `/personality` 预设，它只是叠加层，不替代 `SOUL.md` 这个持久默认身份 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)。

> [!tip] 大白话
> 把 `SOUL.md` 想成**员工的人设卡**——性格、语气、说话风格，跟到哪都带着；把 `AGENTS.md` 想成**这家公司的项目手册**——这个项目的架构、命令、端口、哪些文件别碰。所以"人设"永远只有一个（放在 `~/.hermes/`），而"项目手册"每个项目各有一份。

### 1.2 与 Claude Code 配置体系的对照总览表

下面是贯穿整本笔记的对照锚点，先混个眼熟，细节后续章节展开（映射关系来源：[Import from other agents](https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents)、[Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)、[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)、[Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)）：

| Claude Code | Hermes | 说明 |
| --- | --- | --- |
| `CLAUDE.md`（项目根指令） | `AGENTS.md` / `.hermes.md` | 项目上下文文件；`.hermes.md` 优先级更高 |
| 全局 `CLAUDE.md` / 记忆 | `SOUL.md` + `MEMORY.md` | `SOUL.md` 身份槽 #1；`MEMORY.md` 跨会话记忆快照 |
| `.claude/rules/` 分层规则 | 项目上下文文件优先级链 + 目录链 / 渐进子目录发现 | 组织方式不同，效果类似"越具体越优先" |
| `settings.json` 权限 | `config.yaml` 的 `command_allowlist` / `approvals.deny` + `.env` 密钥 | 权限白/黑名单在 config，密钥在 `.env` |
| `settings.json` hooks | `config.yaml` 的 `hooks:` shell hooks | 兼容 Claude-Code 风格返回形状 |
| `claude config` | `hermes config set/get/check` | CLI 改配置/验证命令族 |
| 迁移工具 | `hermes import-agent claude-code` | 一键导入 `~/.claude` 配置 |

> [!tip] 大白话
> 把 Claude Code 的三件套（`CLAUDE.md` / `settings.json` / hooks）想成**一家公司**：`CLAUDE.md` 是公司制度手册，`settings.json` 是 IT 权限系统，hooks 是门禁监控。Hermes 不是给这些改个名，而是**重排了抽屉**：人设（`SOUL.md`）单独放一个抽屉，项目手册（`AGENTS.md`）放另一个，权限和 hooks 统一进 `config.yaml`。所以对照时别找同名文件，要看"这个抽屉管什么"。

### 1.3 文件位置地图

**Hermes 侧（全局，默认 `~/.hermes/`）**

```text
~/.hermes/
├── SOUL.md            # 身份（slot #1）；缺省自动 seed，已有永不覆盖
├── config.yaml        # 配置中心：command_allowlist / approvals.deny / hooks / mcp_servers / platform_hints ...
├── MEMORY.md          # 跨会话记忆快照
├── USER.md            # 用户画像快照
├── .env               # 密钥：provider 凭证、MCP 密钥（import 永不写入）
└── skills/            # 技能（import 的 Claude Code skills 落到 claude-code-imports/<name>/）
```

注：若设置了 `HERMES_HOME` 环境变量，以上根目录整体移到 `$HERMES_HOME/`，`SOUL.md` 即 `$HERMES_HOME/SOUL.md` [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)。`MEMORY.md`/`USER.md` 是官方建议的持久化面 [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)；密钥写 `~/.hermes/.env`、skills 落在 `~/.hermes/skills/` [Import from other agents](https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents)。

**项目侧（项目根 / 各级目录）**

```text
项目根（git root 或 CWD）
├── .hermes.md 或 HERMES.md   # 项目指令，最高优先级，沿 git root 上溯查找
├── AGENTS.override.md        # 个人覆盖（通常 gitignored），替代已提交的 AGENTS.md
├── AGENTS.md                 # 主项目上下文文件
├── CLAUDE.md                 # Claude Code 上下文（自动兼容，无需改名）
└── .cursorrules / .cursor/rules/*.mdc  # Cursor 约定（自动兼容）
```

要点：每会话项目上下文只加载**一种**，`first-match wins`（从上往下第一个命中的生效）；`SOUL.md` 永远独立加载，作为身份 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)。

> [!tip] 大白话
> 把项目侧的优先级链想成**查词典只认第一个命中的词条**：`.hermes.md` 是"自创词优先"，`AGENTS.md` 是通用词，`CLAUDE.md`、`.cursorrules` 是"别的字典里的词条"。Hermes 每个会话只挑第一个出现的读，不会把好几本字典全塞进系统提示。

### 1.4 推荐工作流总览

官方 Recommended workflow 的扩展版，也是本笔记各章的先后顺序 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality) [CLI Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md)：

1. **全局身份** — 编辑 `~/.hermes/SOUL.md`（缺省已 seed）：放语气/风格/立场，别放项目细节 → 第 2 章
2. **项目规则** — 项目根写 `AGENTS.md`；monorepo 子目录逐层加；想要个人差异写 gitignored 的 `AGENTS.override.md` → 第 3 章
3. **兼容复用** — 已有 `CLAUDE.md` / `.cursorrules` 直接生效、无需改名（优先级低于 `.hermes.md` / `AGENTS.md`）→ 第 3 章
4. **迁移** — `hermes import-agent claude-code --dry-run` 预览 → 确认 → 导入 → 按报告补密钥 → 第 4 章
5. **自动化/拦截** — `config.yaml` 加 `hooks:` shell hooks（拦截危险命令、自动格式化、注入上下文）→ 第 5 章
6. **验证** — `hermes doctor` → `hermes config check` → `hermes prompt-size` 看规则是否进入系统提示；被干扰时用 `--safe-mode` 对照 → 第 6 章

> [!summary] 本章小结
> - Hermes 指令载体分两类：全局 `SOUL.md`（身份）与项目上下文文件（`AGENTS.md` 系列，项目知识）；判断规则是"跟随你到处走 → SOUL.md；属于某个项目 → AGENTS.md"。
> - 对照锚点：`CLAUDE.md` → `AGENTS.md` / `.hermes.md`；全局 `CLAUDE.md` / 记忆 → `SOUL.md` + `MEMORY.md`；`settings.json` → `config.yaml`；hooks 在 `config.yaml` `hooks:`；迁移用 `hermes import-agent claude-code`。
> - 文件地图：`~/.hermes/` 放身份与配置（`SOUL.md` / `config.yaml` / `MEMORY.md` / `.env` / `skills/`）；项目根放上下文文件（`.hermes.md` → `AGENTS.override.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`）。
> - 项目上下文每会话只加载一种（first-match wins）；`SOUL.md` 独立加载、永不覆盖、不随项目漂移。
> - 推荐路径：SOUL.md → AGENTS.md → 兼容复用 → 迁移 → hooks → 验证。

**下一步**：从全局身份开始动手——下一章配置 `~/.hermes/SOUL.md`，讲清它何时生效、何时不会，以及内容约束与 personality 预设。

---

## 第二章 全局身份 — 配置 `~/.hermes/SOUL.md`

第一章把地图铺开了：Hermes 的指令载体分两类——全局 `SOUL.md`（身份）与项目上下文文件（项目知识）。这一章动手配置第一块拼图：全局身份 `~/.hermes/SOUL.md`。对照 Claude Code，这相当于把"全局指令"升级成"身份"——它不是追加一段规则，而是直接决定 **Hermes 是谁、怎么说话**。

### 2.1 位置与加载：只从 `$HERMES_HOME` 加载、不探测 CWD

**文件位置**（来自 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)）：

| 场景 | 路径 |
| --- | --- |
| 默认 | `~/.hermes/SOUL.md` |
| 自定义 home 目录 | `$HERMES_HOME/SOUL.md` |

**加载规则**（官方原文要点）：

- 只从当前实例的 `HERMES_HOME` 加载 `SOUL.md`，**不探测当前工作目录（CWD）**——你在哪个目录启动 Hermes，身份都一样
- 加载成功后内容进入系统提示**第 1 槽位（slot #1）**，**替换**掉内置硬编码默认身份
- `SOUL.md` 是真正的"每用户/每实例身份"，不是"附加规则层"

**为什么这么设计**（官方原话精神）：如果 `SOUL.md` 从"你恰好启动的目录"加载，换个项目人格就变了；只从 `HERMES_HOME` 加载，人格就属于 Hermes 实例本身，可预测。官方甚至把教学话术浓缩成一句：*"Edit `~/.hermes/SOUL.md` to change Hermes' default personality."*

> [!tip] 大白话
> 把 SOUL.md 想成**员工工牌**：你进哪个会议室（项目目录）都戴着同一张工牌；工牌只从 HR 系统（`HERMES_HOME`）发，不会因为换了会议室就换人。所以"你是谁"不随项目漂移——这正是它和项目上下文文件最根本的分工。

**对照 Claude Code**：

- Claude Code 的全局 `CLAUDE.md` 是"追加式"指令，且项目根 `CLAUDE.md` 会被主动发现
- Hermes 的 `SOUL.md` 是"替换式"身份：占据系统提示最前面的身份位，且**刻意不做 CWD 探测**
- 记忆口诀：Claude Code 的全局配置是"加规则"，Hermes 的 SOUL.md 是"换人格"

**动手确认**：先确认文件落点即可（验证命令族在第六章统一讲）：

```bash
ls -la ~/.hermes/SOUL.md
```

### 2.2 自动 seed 与"已有文件永不覆盖"的边界

三条行为规则（来自 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)）：

1. 如果 `SOUL.md` **不存在**，Hermes 自动创建一个 **starter** `SOUL.md`
2. 如果 **已存在**，**永不被覆盖**——升级、重装、重复启动都不会动它
3. 加载逻辑以"文件是否存在 + 是否可读"为分支（详见 2.4 的回退行为）

边界再划清楚一点：

- **seed 只发生在"文件缺失"时**；文件一旦存在，后续所有运行都不再写它
- **空文件 ≠ 会被覆盖**：文件仍在磁盘上，只是不会被当作身份注入（回退到内置默认身份，见 2.4）
- **想"恢复出厂"**：自己删掉文件，下次运行 Hermes 会重新 seed 一个默认的

> [!tip] 大白话
> "自动 seed + 永不覆盖"想成**保险箱**：Hermes 第一次见你没有保险箱，就放一个空的进去（starter）；之后你往里存什么它都不碰。升级只是"搬家"，不会顺手清空你的保险箱。

> [!note] 实战意义
> 这给了你一个很舒服的写配置节奏：直接编辑 `~/.hermes/SOUL.md`，反复保存都安全。如果哪天觉得"我的 SOUL.md 被重置了"，先排查两个更可能的原因：是不是自己删了文件？是不是在项目里建了个 `SOUL.md`（那个位置根本没被加载）？

### 2.3 该写什么：SOUL.md vs AGENTS.md 职责判断

这是官方文档里最强调的区分（*"This is the most important distinction"*），对照 Claude Code 的全局 vs 项目指令：

| 内容类型 | 该放哪 | Claude Code 对照 |
| --- | --- | --- |
| 身份 / 语气 / 风格 / 沟通默认 / 人格级行为 | **SOUL.md** | 全局 `CLAUDE.md` / 记忆 |
| 项目架构 / 编码约定 / 工具偏好 / 仓库特定工作流 / 命令·端口·路径·部署笔记 | **AGENTS.md** | 项目根 `CLAUDE.md` / `.claude/rules` |

**官方判断规则**就一句话：

- **跟随你到处走 → SOUL.md**
- **属于某个项目 → AGENTS.md**

**SOUL.md 里"少放"清单**（官方点名不要写的）：

- 一次性项目指令
- 文件路径
- 仓库约定
- 临时工作流细节

**好的 SOUL 文件特征**：跨上下文稳定；广到能适用很多对话；具体到能实质塑造声线；聚焦沟通与身份，而非任务指令。

**官方示例**（可直接照抄改成自己的，来源 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)）：

```markdown
# ~/.hermes/SOUL.md

# Personality

You are a pragmatic senior engineer with strong taste.
You optimize for truth, clarity, and usefulness over politeness theater.

## Style
- Be direct without being cold
- Prefer substance over filler
- Push back when something is a bad idea
- Admit uncertainty plainly
- Keep explanations compact unless depth is useful

## What to avoid
- Sycophancy
- Hype language
- Repeating the user's framing if it's wrong
- Overexplaining obvious things

## Technical posture
- Prefer simple systems over clever systems
- Care about operational reality, not idealized architecture
- Treat edge cases as part of the design, not cleanup
```

> [!tip] 大白话
> 把这两份文件想成**人设 vs 岗位说明书**：SOUL.md 是"你雇的这个人性格怎样、说话什么风格"；AGENTS.md 是"在这个项目里该干哪些活、走哪条流程"。人设跟着人走，说明书跟着岗位（项目）走。

### 2.4 内容约束：注入安全扫描、截断、空文件回退

**注入方式**：`SOUL.md` 内容**原样（verbatim）注入**系统提示第 1 槽位，不套任何 wrapper 文案（[Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)）。但这不代表能随便写——注入前要过两关。

**第一关：注入安全扫描（prompt-injection scanning）**。`SOUL.md` 与其他上下文文件一样，注入前被扫描提示注入模式（[Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly) 明确列出：不可见 Unicode、"忽略之前的指令"、凭据外泄尝试等）。官方特意提示：**别试图往 SOUL.md 里夹带奇怪的元指令**，把它保持为纯 persona/声线。

> [!warning] 素材边界（按深度素材"四、矛盾点"处理）
> `[BLOCKED: ...]` 的"命中即不加载"行为，官方文档是明确写给**项目上下文文件**的（第三章展开）；SOUL.md 文档只强调"扫描后原样注入"。本章按"同样走扫描、命中行为以第三章 context-files 为准"处理，不做超出素材的断言。深度素材第三、四条差异（override 位置、AGENTS.md 发现范围）与本 SOUL.md 章节无冲突。

**第二关：截断（truncation）**。`load_soul_md()` 的加载逻辑（来自 [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly) 的 `agent/prompt_builder.py` 简化版）长这样：

```python
# agent/prompt_builder.py (simplified)

def load_soul_md() -> Optional[str]:
    soul_path = get_hermes_home() / "SOUL.md"
    if not soul_path.exists():
        return None
    content = soul_path.read_text(encoding="utf-8").strip()
    content = _scan_context_content(content, "SOUL.md")   # Security scan
    content = _truncate_content(content, "SOUL.md")       # Cap scales with model context window (20k floor); config override wins
    return content
```

截断规则（与项目上下文文件同一套机制，[Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)）：

| 规则 | 取值 |
| --- | --- |
| 上限键 | `context_file_max_chars`，在 `config.yaml` 里**显式设置始终优先** |
| 未设置时 | 随模型上下文窗口**动态缩放**：下限 **20,000** 字符、上限 **500K** 字符 |
| 截断方式 | **70/20 头/尾保留** + 截断标记（保留头部 70%、尾部 20%，中间以标记代替） |

**空文件回退**：文件不存在、为空、纯空白、或读取失败 → 回退到**内置默认身份**（"You are Hermes Agent, an intelligent AI assistant created by Nous Research..."）。`skip_context_files` 场景（如 subagent/委派）同样回退。`load_soul_md()` 返回内容后，会替换硬编码的 `DEFAULT_AGENT_IDENTITY`。

**不重复注入**：`SOUL.md` 只在系统提示中出现**一次**（身份槽位），不会在项目上下文文件区重复出现——`build_context_files_prompt(skip_soul=True)` 显式防止重复。

> [!tip] 大白话
> 截断想成**装行李箱**：箱子（上下文窗口）装不下，就把长文案的头尾（70/20）保留、中间砍掉并留个"此处已截断"标记。所以别把 SOUL.md 写成一本小说——它站在系统提示最前面（stable 层），越精简越省 token、越利于提示缓存。

### 2.5 personality 预设与自定义 personalities

**SOUL.md vs `/personality`**（来自 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)）：

- `SOUL.md` = **持久默认人格**（baseline voice）
- `/personality` = **会话级覆盖层**（temporary mode switch）——临时改/补当前系统提示，**不动 SOUL.md 文件**

官方给的典型用法：

- 默认 SOUL 保持务实，教课/辅导时 `/personality teacher`
- 默认 SOUL 保持简洁，头脑风暴时 `/personality creative`

**内置 personality 预设**（`/personality` 可切换，全平台可用）：

| Name | Description |
| --- | --- |
| helpful | Friendly, general-purpose assistant |
| concise | Brief, to-the-point responses |
| technical | Detailed, accurate technical expert |
| creative | Innovative, outside-the-box thinking |
| teacher | Patient educator with clear examples |
| kawaii | Cute expressions, sparkles, and enthusiasm ★ |
| catgirl | Neko-chan with cat-like expressions, nya~ |
| pirate | Captain Hermes, tech-savvy buccaneer |
| shakespeare | Bardic prose with dramatic flair |
| surfer | Totally chill bro vibes |
| noir | Hard-boiled detective narration |
| uwu | Maximum cute with uwu-speak |
| philosopher | Deep contemplation on every query |
| hype | MAXIMUM ENERGY AND ENTHUSIASM!!! |

**命令**（CLI 与消息平台通用）：

```
/personality          # 无参数：列出可用预设 + 标记当前激活项
/personality concise
/personality teacher
/personality none      # 清除激活的覆盖，回到 SOUL.md 基线（next message 生效）
/personality default   # 同上（none / default / neutral 三个等价）
/personality neutral
```

**自定义 personalities**：在 `~/.hermes/config.yaml` 的 `agent.personalities` 下加你自己的预设（或复用内置名来覆盖它）：

```yaml
# ~/.hermes/config.yaml
agent:
  personalities:
    codereviewer: |
      You are a meticulous code reviewer. Identify bugs, security issues,
      performance concerns, and unclear design choices. Be precise and constructive.
```

然后切换：

```
/personality codereviewer
```

**两个容易搞混的点**（官方明确区分）：

- 选择结果以**名字**存在 `display.personality`；personalities **永不触碰** `agent.system_prompt`
- `agent.system_prompt` 是"你自己手写一份系统提示"的保留通道，**只在没有任何 personality 被选中时生效**
- 会话级覆盖在**下一条消息**生效
- **升级注意**：旧版本在各平台保存人格状态不一致；升级后首次运行会把已保存的 personality **一次性重置为 `none`**（迁移日志会打印清掉了哪个），想要就 `/personality <name>` 重新启用。手动 `agent.system_prompt` 永不被触碰

> [!tip] 大白话
> 把 SOUL.md 想成**手机默认主题**，`/personality` 想成**临时换肤**——换皮肤不改系统，关掉（`none`）就回到默认主题。而 `agent.system_prompt` 是"你自己重写系统"的保留通道，选了皮肤时它不生效。

**推荐配置组合**（官方 Recommended workflow）：

1. `~/.hermes/SOUL.md` 写一个深思过的全局人设
2. 项目指令放 `AGENTS.md`
3. 只在需要临时切模式时用 `/personality`

> [!summary] 本章小结
> - `SOUL.md` 是 Hermes 的**全局身份**：只在 `$HERMES_HOME` 加载、不探测 CWD，占据系统提示第 1 槽位、替换内置默认身份——"身份不随项目漂移"。
> - 文件缺失时 Hermes **自动 seed** 一个 starter；已存在则**永不覆盖**；想重置就自己删文件。
> - 职责判断一句话：**跟随你到处走 → SOUL.md；属于某个项目 → AGENTS.md**。SOUL.md 放语气/风格/沟通默认，别放路径、仓库约定、一次性指令。
> - 注入前过两道关：**注入安全扫描** + **截断**（`context_file_max_chars` 优先，否则随模型窗口 20k~500k，70/20 头尾保留）；空/空白/读取失败回退内置默认身份，且只注入一次。
> - `/personality` 是会话级临时覆盖：内置十余种预设，也可在 `config.yaml` 的 `agent.personalities` 自定义；它不动 SOUL.md，也不碰 `agent.system_prompt`。

**下一步**：全局身份配好了，接下来第三章配**项目规则**——项目上下文文件（AGENTS.md 系列）的优先级链、目录链合并与渐进发现。这两层合起来，就是 Hermes 的"全局 + 项目"完整规则骨架。

---

## 第三章 项目规则 — 配置项目上下文文件（AGENTS.md 系列）

> 篇幅：长 · 定位：项目级规则核心 · 素材引用：S2, S3

上一章我们把"跟随你到处走"的身份放进了 `~/.hermes/SOUL.md`。现在处理另一半：**"属于某个项目"** 的规则。在 Claude Code 里，这一半是 `CLAUDE.md` + `.claude/rules/` 的分层体系；在 Hermes 里，它是一套 `AGENTS.md` 系列上下文文件，加载规则完全不同——**每次会话只挑一种**、**目录越深越优先**、**用到哪个子目录才注入哪个**。这章把这些机制逐个讲透，给出可以直接照抄的示例，并标出官方文档里两处容易踩坑的差异。

### 3.1 优先级链：`.hermes.md` → `AGENTS.override.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`

Hermes 支持 6 种项目上下文文件（`SOUL.md` 是身份、永远独立加载，不算在内）。它们之间的选择和发现方式如下 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)：

| 文件 | 用途 | 发现方式 |
| --- | --- | --- |
| `.hermes.md` / `HERMES.md` | 项目指令（**最高优先级**） | 沿 git root 上溯 |
| `AGENTS.override.md` | 个人、按目录覆盖 AGENTS.md（通常 gitignored） | 启动时 CWD + 会话中渐进子目录 |
| `AGENTS.md` | 项目指令、约定、架构（**主项目上下文文件**） | 启动时 CWD + 会话中渐进子目录 |
| `CLAUDE.md` | Claude Code 上下文文件（同样被识别） | 启动时 CWD + 会话中渐进子目录 |
| `.cursorrules` | Cursor IDE 编码约定 | 仅 CWD |
| `.cursor/rules/*.mdc` | Cursor IDE 规则模块 | 仅 CWD |

优先级链是 **first-match-wins**：从高到低扫，**每会话只加载一种**，第一个命中的生效，其余全部忽略 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)。

```text
.hermes.md / HERMES.md     ← 最高优先级（Hermes 原生）
AGENTS.override.md         ← 个人覆盖（替代 AGENTS.md）
AGENTS.md                  ← 主项目上下文文件
CLAUDE.md                  ← Claude Code 兼容
.cursorrules / .cursor/rules/*.mdc  ← Cursor 兼容（最低）
```

**这与 Claude Code 的关键差异**：Claude Code 里 `CLAUDE.md` 和 `.claude/rules/*.md` 是**合并加载**的（顶层指令 + 分层规则叠加）；Hermes 里这 6 种文件是**互斥**的——同一目录下放了 `.hermes.md` 就不会再读 `AGENTS.md`，放了 `AGENTS.md` 就不会再读 `CLAUDE.md`。所以"分层规则"在 Hermes 不是靠同目录多文件叠加实现的，而是靠 3.3 的**目录链**和 3.4 的**渐进子目录发现**。

> [!tip] 大白话
> 把优先级链想成**查词典只认第一个命中的词条**：`.hermes.md` 是你自己写的"专属词条"排最前，`AGENTS.md` 是通用词条，`CLAUDE.md`、`.cursorrules` 是"别家词典里的词条"排最后。Hermes 每个会话只抄第一本翻到的词典，不会把五本全塞进系统提示。

加载成功后，最终拼进系统提示的样式大致是这样 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)：

```text
# Project Context

The following project context files have been loaded and should be followed:

## AGENTS.md

[Your AGENTS.md content here]

## .cursorrules

[Your .cursorrules content here]

[Your SOUL.md content here]
```

注意：`SOUL.md` 的内容是直接插入、不带额外包裹文字；系统提示组装的三层（stable → context → volatile）里，这些项目上下文文件属于 **context 档**，夹在身份与记忆快照之间 [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)。

`.hermes.md` 还有一个特殊点：它的 **YAML frontmatter 会被剥掉**——官方说这是"为未来 config override 预留的能力"，当前只当普通指令读取，不要依赖 frontmatter 行为 [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)。

> [!warning] 文档差异（官方两页不一致）
> developer-guide 的 `build_context_files_prompt()` 代码片段只列了 `.hermes.md → AGENTS.md → CLAUDE.md → .cursorrules` **四档，没有 `AGENTS.override.md`**；而 user-guide 明确把 `AGENTS.override.md` 列为 `.hermes.md` 之后的第二优先 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)。**以 user-guide 为准**——override 是较新特性，developer-guide 的代码片段是简化示意。

### 3.2 `AGENTS.override.md`：个人差异又不动仓库文件的方案

如果你进了一个团队仓库，`AGENTS.md` 是别人提交的约定，但你本地有自己的偏好（用 `pnpm` 不用 `npm`、提交前跑自己的 lint）——改仓库里的 `AGENTS.md` 会污染 PR，Claude Code 里你多半会往 `.claude/rules` 或全局 `CLAUDE.md` 里塞个人层。Hermes 的答案是 **`AGENTS.override.md`**：**只要它存在，就整体替代同目录下已提交的 `AGENTS.md`**，加载它 `instead of` 仓库文件 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)。

```text
my-project/                    (git 仓库)
├── AGENTS.md                  ← 团队提交的约定（被 override 整体替代）
├── AGENTS.override.md         ← 你的个人覆盖（已 gitignore）
└── .gitignore
```

`.gitignore` 加一行：

```gitignore
AGENTS.override.md
```

`AGENTS.override.md` 内容示例（格式与 AGENTS.md 完全一致，Markdown 即可）：

```markdown
# 个人覆盖（不进仓库）

本机专属约定，替代仓库根 AGENTS.md 使用。

## 工具偏好
- 包管理用 `pnpm`，不用 `npm`
- 提交前跑 `make lint-local`
- 测试用 `pnpm test -- --runInBand`

## 端口
- 前端 dev server 跑在 5173，不是仓库默认的 3000
```

> [!tip] 大白话
> 把 `AGENTS.override.md` 想成**贴在团队手册上的个人便利贴**：手册（`AGENTS.md`）还在仓库里躺着，但你翻开手册时看到的先是你自己的便利贴，它把整页盖住了。这样你的偏好只在你机器上生效，别人 checkout 仓库完全看不到。

两个要点：

1. **是"替代"不是"合并"**：override 存在即完全取代 `AGENTS.md`，不会把两者拼接。所以 override 里要写**完整**的约定，而不是"在团队基础上改两行"。官方原话：override 被加载 `instead of` the committed file [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)。
2. **按目录生效**：它和 `AGENTS.md` 一样支持渐进子目录发现（见 3.4），可以在不同子目录放不同的 override，实现"进到某个包就用某套个人偏好"。

### 3.3 目录链合并：git root → CWD 逐层加载、深层优先、相同副本去重

在 Claude Code 里，"子项目特定规则"通常靠 `.claude/rules` 的 glob 或 memory 提示来划。Hermes 用**物理目录层级**表达"越具体越优先"：当工作目录在 git 仓库内时，**会话启动时**会加载一条 `AGENTS.md` 的**合并链**——git root 的 `AGENTS.md` 在最前，之后逐层到当前工作目录，**越深越靠后、越具体** [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)。

```text
monorepo/                    (git root，cwd = packages/webapp/)
├── AGENTS.md              ← 最先加载（仓库级通用约定）
└── packages/
    ├── AGENTS.md          ← 第二个加载
    └── webapp/
        └── AGENTS.md      ← 最后加载（最具体，优先权最高）
```

细节规则 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)：

- **每份文件带来源头（provenance header）**，例如 `## ../../AGENTS.md`，让模型知道这条规则来自哪一层。
- **相同内容的副本去重**：链上若有内容一模一样的 `AGENTS.md`（比如各子目录复制了同一份），只保留一份，避免重复占用 token。
- **非 git 仓库只看 CWD**：不在 git 里时，只检查当前工作目录，**父目录一律不查**。因此一个放在 `/tmp` 或 `$HOME` 的 `AGENTS.md` **永远不会泄漏**进无关会话——这是和"父目录上溯"恰好相反的安全边界。

一份可直接照抄的仓库根 `AGENTS.md`（官方示例结构 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)）：

```markdown
# Project Context

这是一个 Next.js 14 前端 + Python FastAPI 后端的全栈应用。

## Architecture
- 前端：Next.js 14 App Router，代码在 `/frontend`
- 后端：FastAPI，使用 SQLAlchemy ORM，代码在 `/backend`
- 数据库：PostgreSQL 16
- 部署：Docker Compose，跑在 Hetzner VPS

## Conventions
- 前端代码一律 TypeScript strict mode
- Python 遵循 PEP 8，所有地方都要写类型注解
- API 返回值统一 `{data, error, meta}` 形状
- 测试放 `__tests__/`（前端）或 `tests/`（后端）

## Important Notes
- 永远不要直接改 migration 文件 —— 用 Alembic 命令生成
- `.env.local` 里有真实 API key，禁止提交
- 端口：前端 3000，后端 8000，数据库 5432
```

官方对 AGENTS.md 写作的建议，正好也是排错清单 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)：

1. **保持精简**——agent 每轮都会读它，别超过 `context_file_max_chars`；
2. **用 `##` 分节**——architecture / conventions / important notes；
3. **给具体例子**——代码模式、API 形状、命名约定；
4. **写明"不要做什么"**——"never modify migration files directly" 这类负面指令往往比正面指令更值钱；
5. **列出关键路径和端口**——agent 跑终端命令时直接用；
6. **随项目演进更新**——过时的上下文比没有上下文更糟。

> [!warning] 文档差异（启动 vs 会话中的发现范围）
> developer-guide 的优先级表写 `AGENTS.md` 的搜索范围是 **"CWD only"**；而 user-guide 明确：git 仓库内**启动时做目录链合并**（git root → CWD），**会话中再做渐进子目录发现**（3.4）[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)。两处描述的是**不同阶段**的机制：S3 只描述了启动时"看 CWD"，S2 补全了目录链 + 会话中动态发现。**以 S2 的完整描述为准**；这也解释了为什么"放个 AGENTS.md 在子目录里，启动时没进系统提示"——它要等你进到那个子目录才注入（3.4）。

### 3.4 渐进子目录发现：会话中按需注入

这是 Hermes 项目上下文最聪明的设计。**启动时只把 CWD 的 `AGENTS.md` 放进系统提示**；当 agent 在会话中通过 `read_file`、`terminal`、`search_files` 等工具进入子目录时，才把该目录的上下文文件**在变得相关的那一刻**注入对话 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)。

```text
my-project/
├── AGENTS.md              ← 启动时加载（进系统提示）
├── frontend/
│   └── AGENTS.md          ← agent 读到 frontend/ 文件时才被发现
├── backend/
│   └── AGENTS.md          ← agent 读到 backend/ 文件时才被发现
└── shared/
    └── AGENTS.md          ← agent 读到 shared/ 文件时才被发现
```

两个直接收益 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)：

- **系统提示不膨胀**——子目录提示只在需要时出现；
- **保住 prompt 缓存**——系统提示跨轮保持稳定，不因为一次性塞进所有子目录规则而失效。

实现机制（`agent/subdirectory_hints.py` 的 `SubdirectoryHintTracker`，官方 6 步 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)）：

```text
1. 路径提取    → 每次工具调用后，从参数（path / workdir / shell 命令）里提取文件路径
2. 祖先上溯    → 检查该目录 + 最多 5 级父目录（碰到已访问过的目录就停）
3. 命中加载    → 找到 AGENTS.md / CLAUDE.md / .cursorrules，每个目录取第一个命中
4. 安全扫描    → 与启动文件同一套注入扫描
5. 截断        → 单文件上限 8,000 字符
6. 注入        → 追加到该次工具结果里，模型自然在上下文里看到
```

关键行为：

- **每目录至多检查一次**（per session），不会反复注入同一目录的规则；
- **上溯 5 级**：读 `backend/src/main.py` 会连带发现 `backend/AGENTS.md`，即使 `backend/src/` 自己没有任何上下文文件；
- **截断上限 8,000 字符/文件**——注意这个上限远小于启动文件的 `context_file_max_chars`（见 3.5），子目录提示要写得比根级更短；
- **子目录文件同样过安全扫描**，恶意文件会被拦截 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)。

> [!tip] 大白话
> 把渐进子目录发现想成**图书馆查书只翻到你正在用的那本**：你不是把整馆的书一次性搬到桌上，而是走到哪排书架才抽那本书出来翻。所以根目录的"馆藏总览"（`AGENTS.md`）一进门就给你，某本子目录的书（`backend/AGENTS.md`）等你走到那个分区才递过来。

monorepo 的每个子包可以有自己的 `AGENTS.md`（官方 Per-Subdirectory Context 示例 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)）：

```markdown
# Frontend Context   (frontend/AGENTS.md)
- 包管理用 `pnpm`，不用 `npm`
- 组件放 `src/components/`，页面放 `src/app/`
- 用 Tailwind CSS，禁止内联样式
- 跑测试：`pnpm test`
```

```markdown
# Backend Context   (backend/AGENTS.md)
- 依赖管理用 `poetry`
- 启动 dev server：`poetry run uvicorn main:app --reload`
- 所有端点都要写 OpenAPI docstrings
- 数据库模型放 `models/`，schema 放 `schemas/`
```

对照 Claude Code：Claude Code 也是"用到相关文件才带出对应上下文"，但 Hermes 把这条机制**显式化、量化**了——每目录一次、上溯 5 级、单文件 8000 字符。你在 Claude Code 里要靠 memory 或手写规则模拟的"进入子目录才有子约定"，在 Hermes 里是内置行为。

### 3.5 注入安全扫描与 `[BLOCKED: ...]` 行为

所有上下文文件——启动文件、渐进发现文件、`SOUL.md`——在注入前都要过**提示注入安全扫描**。命中的文件**不加载**，并在对话里留下一条 `[BLOCKED: ...]` 标记 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)。

扫描器检查的模式（官方列举）：

| 类别 | 示例模式 |
| --- | --- |
| 指令覆盖 | `ignore previous instructions`、`disregard your rules` |
| 欺骗模式 | `do not tell the user` |
| 系统提示覆盖 | `system prompt override` |
| 隐藏 HTML 注释 | `<!-- ignore instructions -->` |
| 隐藏 div | `<div style="display:none">` |
| 凭证外泄 | `curl ... $API_KEY` |
| 秘密文件访问 | `cat .env`、`cat credentials` |
| 不可见字符 | 零宽空格、双向覆盖符、词连接符 |

命中后的拦截消息长这样（官方示例 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)）：

```text
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

同一套扫描也作用于会话中渐进发现的子目录文件——**恶意文件一律拦截** [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)。

**截断**也是这道闸门的一部分。超过字符上限的文件按 **70% 头 + 20% 尾**截断，中间 10% 是截断标记（显示字符数并建议用文件工具读全文）[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)：

| 限制 | 值 |
| --- | --- |
| 启动文件单文件上限 | 显式设置 `context_file_max_chars` 时用它；否则随模型上下文窗口动态缩放（**floor 20,000 / ceiling 500,000 字符**） |
| 截断比例 | 头 70% / 尾 20% |
| 截断标记 | 中间 10%，显示字符数、建议用文件工具 |
| 渐进发现文件单文件上限 | **8,000 字符**（见 3.4） |

截断消息示例 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)：

```text
[...truncated AGENTS.md: kept 14000+4000 of 25000 chars. Use file tools to read the full file.]
```

> [!warning] 别把扫描器当绝对防线
> 官方明确警告：这套扫描只防**常见**注入模式，**不能替代人工审查共享仓库里的上下文文件**。从别人仓库拉下来的 `AGENTS.md`，尤其是不认识的项目，务必先自己读一遍再让 agent 加载 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)。这跟你审查不熟悉的 `CLAUDE.md` 是一个道理。

> [!tip] 大白话
> 把安全扫描想成**机场安检**：行李（上下文文件）过机器，检测到违禁词（`ignore previous instructions`、`cat .env`）就直接拦下不上飞机，广播里喊一句"这件行李被拦了"（`[BLOCKED: ...]`）。但安检不是保险箱——别人托你带的行李，你最好自己拆开看一眼。

### 3.6 兼容复用：已有 `CLAUDE.md` / `.cursorrules` 无需改名直接生效

从 Claude Code 或 Cursor 迁移过来的项目，**不需要给任何文件改名**。Hermes 原生识别另外两家的约定文件 [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)：

- **`CLAUDE.md`**：作为项目上下文文件被识别，发现方式是"启动时 CWD + 会话中渐进子目录"，`AGENTS.md` 能用的地方它都能用；
- **`.cursorrules` / `.cursor/rules/*.mdc`**：项目根存在且没有更高优先级上下文文件（`.hermes.md`、`AGENTS.md`、`CLAUDE.md`）时，作为项目上下文加载——你的既有 Cursor 约定自动生效。

但优先级链意味着一个**容易踩的坑**：同一目录下放了 `AGENTS.md` 后，`CLAUDE.md` 就不再被加载了（first-match-wins）。所以：

| 你的目标 | 做法 |
| --- | --- |
| Hermes 直接用你现有配置，零改动 | 什么都不用改，`CLAUDE.md` / `.cursorrules` 自动生效 |
| 让 Hermes 优先读自己的项目规则 | 加 `AGENTS.md`（此时同目录 `CLAUDE.md` 降级为不加载） |
| 同仓库同时服务 Claude Code 和 Hermes | 保留 `CLAUDE.md` 给 Claude Code；给 Hermes 用 `AGENTS.md`（更高优先）或 `.hermes.md` |
| 全仓库统一一套规则、多个 agent 都能读 | 用通用名 `AGENTS.md` 作为主文件，Hermes 直接认；`CLAUDE.md` 作为 Claude Code 专属补充 |

> [!tip] 大白话
> 把兼容复用想成**酒店客房的三孔插座**：你从别的酒店带来的充电器（`CLAUDE.md`、`.cursorrules`）不用换插头直接能用。但如果你自己带了转换头（`AGENTS.md`），它就优先占用了那个插座——原来的插头就得让位。

对照 Claude Code 的 `.claude/rules` 分层：你在 Claude Code 里用 glob 划出的"每个模块一套规则"，在 Hermes 里就翻译成 3.3 + 3.4 的**目录链 + 渐进发现**——把 `.claude/rules/frontend/*.md` 换成 `frontend/AGENTS.md`，语义相同但物理位置更直观。已有的 `CLAUDE.md` 不需要改结构，只是优先级上低于 `AGENTS.md`。

如果你是从 Claude Code 迁配置过来，项目侧的 `CLAUDE.md` **不需要 `import-agent` 处理**（它会被直接识别）；第四章的 `hermes import-agent claude-code` 管的是 `~/.claude` 的全局层（记忆、权限、skills），项目文件这边你已经在这章搞定了。

> [!summary] 本章小结
> - **优先级链 first-match-wins**：`.hermes.md` → `AGENTS.override.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`，每会话只加载一种；`SOUL.md` 作为身份独立加载。官方两页文档对 override 位置描述不一致，**以 user-guide 为准**。
> - **`AGENTS.override.md`** 是"个人差异又不动仓库文件"的方案：存在即**整体替代**同目录 `AGENTS.md`（不是合并），记得 gitignore。
> - **目录链**：git 仓库内启动时按 git root → CWD 合并加载 `AGENTS.md`，深层在后更具体；每份带来源头、相同副本去重；**非 git 仓库只看 CWD，父目录不泄漏**。S3 的 "CWD only" 只描述启动，会话中还有渐进发现，**以 S2 完整描述为准**。
> - **渐进子目录发现**：会话中按需注入（每目录至多一次、上溯 5 级、单文件 8000 字符），保住系统提示稳定与 prompt 缓存。
> - **安全扫描**：指令覆盖、隐藏 HTML、凭证外泄、零宽字符等命中即 `[BLOCKED: ...]` 不加载；启动文件上限 `context_file_max_chars`（默认动态 20k–500k），截断 70/20 头尾。
> - **兼容复用**：已有 `CLAUDE.md` / `.cursorrules` 直接生效、无需改名；注意加了 `AGENTS.md` 会让同目录 `CLAUDE.md` 停止加载。

**下一步**：你已经能手写 Hermes 的项目上下文文件了——接下来把已有的 Claude Code 配置整体搬过来：第四章「对照迁移 — 从 Claude Code 一键导入」讲 `hermes import-agent claude-code` 的映射表、preview-first 行为与"凭证永不导入"的安全边界。

---

## 第四章 对照迁移 — 从 Claude Code 一键导入

第三章讲到 Hermes 能**直接识别**项目里已有的 `CLAUDE.md` / `.cursorrules`，但那是"单个文件被顺手复用"。如果你的整套 Claude Code 配置——全局指令、`settings.json` 权限、MCP 服务器、skills——都要搬到 Hermes，手动照前两章的对照表一个个誊抄既慢又容易漏。这一章教你用 `hermes import-agent claude-code` 一条命令完成迁移，并讲清它**导什么、怎么导、坚决不导什么**（密钥永不导入），让你迁移后心里有底。

### 4.1 导入映射表：你的每个配置去了哪

`hermes import-agent claude-code` 读取 `~/.claude`，把 Claude Code 的各类配置按一张固定映射表搬进 Hermes。[^c4-1] 先记住一句话：**它不是魔法，而是照着映射表搬运**——每一类配置都有明确的落点：

| Claude Code（`~/.claude`） | Hermes 落点 | 说明 |
| --- | --- | --- |
| `CLAUDE.md`（**全局**指令） | `~/.hermes/memories/MEMORY.md` 记忆条目 | 注意是**记忆条目**，不是 `SOUL.md` |
| `settings.json` → `permissions.allow`（`Bash(...)` 规则） | `config.yaml` → `command_allowlist` | 只导 `Bash(...)`，非 Bash 规则见 4.3 |
| `settings.json` → `permissions.deny`（`Bash(...)` 规则） | `config.yaml` → `approvals.deny` | 同上，只导 Bash 类 |
| `mcpServers`（来自 `~/.claude.json` **和** `settings.json`） | `config.yaml` → `mcp_servers` | 来源是**两个文件**，不是只看 settings.json |
| `skills/<name>/`（含 `SKILL.md` 的目录） | `~/.hermes/skills/claude-code-imports/<name>/` | 逐个 skill 目录整体拷入 |
| `commands/*.md`（斜杠命令） | **跳过**，附提示 | 官方建议：把它们转成 skill |

两个容易看走眼的地方：

- **全局 `CLAUDE.md` 不会变成 `SOUL.md`。** 第二章说过 `SOUL.md` 是"身份"，它只在缺省时自动 seed、已有文件永不覆盖——导入器不会动它。你在 `~/.claude/CLAUDE.md` 里写的全局指令会被变成 `MEMORY.md` 的记忆条目，在系统提示组装时以记忆快照（slot #5）注入。也就是说：**身份不迁移，全局指令迁移为记忆**。
- **`commands/*.md`（斜杠命令）默认不迁移。** 它只报告"已跳过"，并建议你把常用斜杠命令改造成 skill。如果你依赖大量 slash commands，这一步需要手工整理。

> [!tip] 大白话
> 把 `import-agent` 想成**搬家公司照着清单搬家**：你的每个"物件"（全局指令、权限、MCP、skills）都有固定的新房间（`MEMORY.md`、`config.yaml`、`~/.hermes/skills/...`）。所以它不会猜，只会按 4.1 这张对照表一件件放好——你提前知道每件东西去了哪，就不会搬家后找不到。

先睹为快，完整命令族如下（逐条拆解见 4.2–4.4）：

```bash
hermes import-agent                      # 自动探测 ~/.claude 或 ~/.codex
hermes import-agent claude-code          # 从 ~/.claude 导入
hermes import-agent codex                # 从 ~/.codex 导入
hermes import-agent claude-code --dry-run          # 仅预览，不写任何文件
hermes import-agent codex --source /path/to/.codex # 自定义源目录
hermes import-agent claude-code --overwrite --yes  # 覆盖冲突 + 跳过确认
```

（`codex` 分支同理，映射表见官方文档，本章聚焦 `claude-code`。）

### 4.2 导入行为：预览优先、合并而非替换

导入器和 `hermes claw migrate` 一样遵循 **preview-first（预览优先）** 模式：执行任何写入前，先打印一份**逐条计划**；`--dry-run` 永远不碰磁盘。[^c4-1]

```bash
# 第一步永远是预览：看清单，不落盘
hermes import-agent claude-code --dry-run

# 确认无误后再真正导入（交互式会逐条确认）
hermes import-agent claude-code

# 非交互环境（CI/脚本）：必须显式 --yes 才会越过预览继续
hermes import-agent claude-code --yes
```

四条核心行为，导入报告的"注意"区就靠它们解读：[^c4-1]

| 行为 | 含义 | 你要做的 |
| --- | --- | --- |
| **Preview first, always** | 先打印完整计划；非交互会话**停在预览**，除非传 `--yes` | 先 `--dry-run` 看清单，再正式导入 |
| **Merges, not replaces** | 记忆条目与已有 `MEMORY.md` **去重**；allow/deny 模式与 `config.yaml` 现有内容**合并** | 不会清空你已有的记忆和权限，可放心重复跑 |
| **Conflicts skipped by default** | 已存在的 MCP server / skill 报为 **conflict 并跳过** | 想覆盖就加 `--overwrite` |
| **Malformed files don't abort** | 坏掉的 `settings.json` 变成报告里的**单条错误**，其余照常导入 | 看到单条 error 不必慌张，修好对应文件再重跑即可 |

> [!tip] 大白话
> 把"合并而非替换"想成**往同一个本子上追加笔记**：记忆条目如果跟原来重复就不抄第二遍，权限清单是"添加上去"而不是"先把原来的擦掉"。所以这条命令是**安全的增量操作**，放心用它，最多是清单多几行，不会毁掉你已有的 Hermes 配置。

### 4.3 Bash 前缀规则转 glob

Claude Code 的权限规则长这样：`Bash(npm run test:*)`——括号里是**命令前缀**，意思是"允许/拒绝一切以 `npm run test:` 开头的命令"。Hermes 不用前缀匹配，用的是 **glob（通配符）**，所以导入器会自动做一次翻译：[^c4-1]

| Claude Code（前缀） | Hermes（glob） |
| --- | --- |
| `Bash(npm run test:*)` | `npm run test*` |

翻译规则拆开看：

- `Bash(...)` 外壳被剥掉——Hermes 的 `command_allowlist` / `approvals.deny` 本来只管命令，不需要 Bash 包装。
- 前缀里的 `:` 按 glob 语义处理：`npm run test:*` 变成 `npm run test*`（`*` 匹配任意字符，包括 `:` 之后的整段）。
- `settings.json` 里 `permissions.allow` 的 Bash 规则 → `command_allowlist`；`permissions.deny` 的 Bash 规则 → `approvals.deny`。

**非 `Bash(...)` 的权限规则不会被导入。** `Read(...)`、`WebFetch` 这类规则拦的是 Claude 专用工具，Hermes 里没有一一对应物，所以导入报告会标成 **unmapped（未映射）** 而非导入。[^c4-1]

> [!tip] 大白话
> 把 `Bash(npm run test:*)` 想成**门禁卡上写的一句话**："所有以 `npm run test:` 开头的命令都放行"。Hermes 的保安不认"句子"，只认**通配符清单**，于是导入器把这句话翻译成门禁表里的一行 `npm run test*`。同一个意思，换了一种写法——`Read` / `WebFetch` 这种"别的门的钥匙"在 Hermes 没有对应的门，就被标注"此物未映射"，而不是硬塞进来。

### 4.4 凭证永不导入：密钥要自己补

这是迁移**最重要**的一条边界。[^c4-1]

> [!warning] 凭证安全
> **API 密钥和凭证永不导入。** 凭证文件（`~/.claude/.credentials.json`、`~/.codex/auth.json`）**根本不会被读取**；MCP server 的环境变量或 header 中凡是名字看起来像密钥的（`*_TOKEN`、`*_API_KEY`、`Authorization` 等）都会被**剔除**，并在导入报告里**逐条列出**，让你有意识地重新加回。这样做的目的是防止密钥被静默复制进 Hermes 配置文件——要加，就得你亲手、明确地加。

被剔除的密钥怎么补？官方给了两条路：[^c4-1]

```bash
# 方式一：手动写进 .env
# 先用命令确认 .env 路径（通常是 ~/.hermes/.env）
hermes config env-path
# 然后编辑该文件，例如：
#   ANTHROPIC_API_KEY=sk-ant-...
#   YOUR_MCP_SERVER_TOKEN=...

# 方式二：交互式引导补全
hermes setup          # 完整向导（首次运行/重配，当前值作默认，回车保留）
hermes setup model    # 只补模型/provider 段
```

> [!tip] 大白话
> 把 `.credentials.json` 想成**保险箱**：搬家公司根本不打开它，也不把里面的钱搬走。他们只会在清单上写"这个保险箱你没搬"，并把保险箱外壳上贴的标签（`*_TOKEN`、`*_API_KEY`）念给你听——意思是"这些钥匙你回头自己放进 Hermes 的保险柜（`~/.hermes/.env`）"。**所以：迁移永远不会替你保管密钥，也永远不会让你的密钥躺进别人的配置文件。**

### 4.5 导入后核对清单

跑完导入，对照这份清单逐项验收（前几项靠导入报告，后几项靠命令验证）：

- [ ] **报告逐条看一遍**：哪些条目会写入、哪些被跳过（`commands/*.md`）、哪些标了 `unmapped`、哪些密钥名被剔除。
- [ ] **记忆已合并**：`~/.hermes/memories/MEMORY.md` 里出现了新记忆条目，且与原有条目去重（不重复）。
- [ ] **权限已合并**：`config.yaml` 的 `command_allowlist` / `approvals.deny` 已包含翻译后的 glob（用 `hermes config get` 抽查，如 `hermes config get command_allowlist`）。
- [ ] **MCP 已列出**：`config.yaml` → `mcp_servers` 有对应 server；同时确认其**密钥名**（`*_TOKEN` / `*_API_KEY` / `Authorization`）确实没被带入。
- [ ] **skills 已落位**：`~/.hermes/skills/claude-code-imports/<name>/` 目录存在；报告里的 conflict 项，决定是否用 `--overwrite` 重跑。
- [ ] **斜杠命令被跳过**：`commands/*.md` 未迁移；把常用的那几个转成 skill（`hermes skills`）。
- [ ] **密钥已手工补**：`~/.hermes/.env`（`hermes config env-path` 确认路径）或 `hermes setup model`。
- [ ] **基础验证**：`hermes doctor` 无致命错误（第六章会系统讲验证命令族）。

> [!summary] 本章小结
> - `hermes import-agent claude-code` 按一张固定映射表迁移：全局 `CLAUDE.md` → `MEMORY.md` 记忆、`Bash(...)` 权限 → `command_allowlist` / `approvals.deny`、`mcpServers` → `mcp_servers`、skills → `~/.hermes/skills/claude-code-imports/`，`commands/*.md` 跳过。
> - 行为是**预览优先 + 合并而非替换**：先 `--dry-run` 看计划；记忆去重、allow/deny 合并；冲突默认跳过（`--overwrite` 覆盖）；坏文件只报单条错误，不中止整体导入。
> - `Bash(npm run test:*)` 这类**前缀规则**会被翻译成 glob `npm run test*`；`Read(...)` / `WebFetch` 等非 Bash 规则标注 **unmapped**，不导入。
> - **凭证永不导入**：`.credentials.json` 不读、密钥名（`*_TOKEN` / `*_API_KEY` / `Authorization`）剔除并列出，由你手动补到 `~/.hermes/.env` 或 `hermes setup`。
> - 迁移完按 4.5 核对清单验收，重点确认密钥没有静默流入配置。

**下一步**：配置导进来只是起点——导入的 `config.yaml` 里其实还有一大块没讲的能力：**hooks**。下一章进入第五章，用 `config.yaml` 的 `hooks:` 配置 shell hooks，实现对危险命令的拦截与自动化。

[^c4-1]: [Import from other agents | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents) — 映射表、导入行为、Bash 前缀转 glob、凭证永不导入
[^c4-2]: [CLI Commands Reference | Hermes Agent](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md) — `hermes import-agent` 选项、`hermes setup`、`hermes config env-path`

---

## 第五章 自动化与拦截 — 配置 config.yaml hooks

前几章搭好的 `SOUL.md`、`AGENTS.md`、`config.yaml` 权限块，本质都是"**静态告诉模型该怎么做**"——它们进入系统提示，靠模型自觉遵守。这一章要解决的是另一个问题：**当模型要执行某个工具、或某个回合要发给 LLM 时，怎么在进程层面用确定性代码拦截、改写或注入**。答案就是 hooks：在关键生命周期点运行自定义代码，做阻塞危险命令、自动格式化、注入上下文这类"规则文件管不到"的事。这一章以你在 Claude Code 里配过的 `settings.json` hooks 为对照锚点，把 Hermes 的 hook 体系讲透，重点是 `config.yaml` 里的 shell hooks——它和 Claude Code 的 hooks 是同源思路，还额外兼容 Claude Code 风格的返回 JSON。

### 5.1 四类 hook 系统总览（对照 Claude Code settings.json hooks）

先看地图。Hermes 不止一套 hook，而是**四套并存**，注册位置、运行范围、语言、能力各不相同[^c5-1]：

| 系统 | 注册位置 | 运行范围 | 语言 | 典型用途 | 能拦截工具 / 注入上下文？ |
| --- | --- | --- | --- | --- | --- |
| **Gateway Event Hooks** | `~/.hermes/hooks/<name>/` 下的 `HOOK.yaml` + `handler.py` | 仅 Gateway（Telegram/Discord/Slack/WhatsApp/Teams） | Python | 日志、告警、webhook、`BOOT.md` 启动清单 | 否 |
| **Plugin Hooks** | 插件 `register()` 里调 `ctx.register_hook("pre_tool_call", fn)` | CLI + Gateway | Python | 工具拦截、指标、护栏 | 是（`pre_tool_call` 可 block / modify） |
| **Shell Hooks** | `~/.hermes/config.yaml` 的 `hooks:` 块，指向 shell 脚本 | CLI + Gateway | 任意（Bash / Python / Go 二进制） | 阻塞危险命令、自动格式化、上下文注入 | 是（`pre_tool_call` 可 block / modify） |
| **Outbound Webhooks** | `~/.hermes/config.yaml` 的 `hooks.outbound:` 列表 | CLI + Gateway | 无（对外 HTTP POST） | 推送签名生命周期事件到 CI / 仪表盘 / 另一个 Hermes | 否（只观察，不改变流程） |

> [!tip] 大白话
> 把 hook 想成**过安检**：Gateway 钩子像"保安只在自己负责的那栋楼（Gateway）上班"；插件钩子和 shell 钩子是"全场巡逻的保安"，工具调用前都能把你拦下来检查；outbound webhook 则是"大楼门口的公告屏"，只对外广播消息，不管人。所以真要"拦工具"或"塞上下文"，认准**插件钩子**和**shell 钩子**这两类。

一个贯穿四类的总原则：**hook 回调出错会被隔离并记日志，不会让 agent 崩溃**。但"隔离"不等于"无害"——directive/control 类钩子能改变流程，transform 类钩子能替换内容，shell 的 `pre_tool_call` 钩子能 block 或 fail-closed[^c5-1]。

和 Claude Code `settings.json` hooks 对照，定位最准的锚点如下：

| Claude Code（settings.json） | Hermes | 说明 |
| --- | --- | --- |
| `hooks.PreToolUse` / `hooks.PostToolUse` | `pre_tool_call` / `post_tool_call` | 同一语义：工具执行前 / 后。事件名一个 PascalCase、一个 snake_case |
| `hooks.UserPromptSubmit` | `pre_llm_call` | 官方明确：`UserPromptSubmit` 不是 Hermes 的独立事件，`pre_llm_call` 在相同位置触发且已支持上下文注入[^c5-10] |
| matcher + command 数组 | `hooks.<event>` 列表里的 `matcher` + `command` | 同源思路：正则匹配工具，命中才跑脚本 |
| hook stdout 的 `{"decision": "block", "reason": ...}` | 直接照收，内部归一化 | S8 原文就叫 "Claude-Code style" |
| `failClosed` 拼写（Cursor/Claude Code 兼容） | `fail_closed` 同样接受 | 配置层兼容 |

> 对照要点：Claude Code 把 hook 都塞进 `settings.json` 一个 `hooks` 键；Hermes 拆成四套，各有各的注册方式和权限边界。**CLI 会话里真正可用的只有插件钩子和 shell 钩子**——Gateway 钩子只在 gateway 进程加载，你 `hermes chat` 跑 CLI 时它不会触发[^c5-2]。所以日常想拦命令、自动格式化，直接学 shell hooks 就够了。

### 5.2 shell hooks 配置 schema：`hooks.<event>` 与 matcher/command/timeout/fail_closed

shell hooks 是本章主角。**注册入口**在 CLI 启动（`hermes_cli/main.py`）和 gateway 启动（`gateway/run.py`）时调用 `agent.shell_hooks.register_from_config(cfg)`；它和 Python 插件钩子走同一个 dispatcher，天然共存[^c5-4]。完整 schema 如下[^c5-4]：

```yaml
# ~/.hermes/config.yaml
hooks:
  <event_name>:             # 必须是 VALID_HOOKS 之一（插件钩子事件全集）
    - matcher: "<regex>"             # 可选；仅 pre_tool_call / post_tool_call 使用
      command: "<shell command>"     # 必填；经 shlex.split 切分，shell=False 子进程运行
      timeout: <seconds>             # 可选；默认 60，上限 300（超出 clamp + warning）
      fail_closed: <bool>            # 可选；默认 false。仅 pre_tool_call 有效
      # `failClosed` 拼写同样接受（Cursor / Claude Code 兼容）

hooks_auto_accept: false   # 顶层；首次使用征询同意（见 5.3）
```

逐字段拆解：

| 字段 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- |
| `matcher` | 否 | 无（匹配全部） | 正则字符串，**仅 `pre_tool_call` / `post_tool_call` 使用**，用来匹配工具名（tool_name） |
| `command` | 是 | — | 用 `shlex.split` 切词、`shell=False` 起子进程——**不经过 shell 解释**，所以不要写 `|`、`&&`、`$(...)` 这类 shell 语法；缺 `command` 的条目直接 skip + warning |
| `timeout` | 否 | 60 秒 | 单个 shell hook 的独立超时；>300 被 clamp 并告警 |
| `fail_closed` | 否 | `false` | 只对 `pre_tool_call` 有意义；配到别的 event 上，config 解析时 warning 并忽略 |
| `hooks_auto_accept` | 顶层 | `false` | 首次使用征询同意开关（5.3 详述） |

校验行为（都有 warning，不崩）：

- 事件名必须是插件钩子事件全集里的一个，typo 会得到 "Did you mean X?" 提示并被跳过[^c5-4]。
- 单条 entry 里未知 key 被忽略；缺 `command` 是 skip-with-warning[^c5-4]。
- `timeout > 300` 被 clamp 并告警；`fail_closed: true` 用在非 `pre_tool_call` 事件上警告并忽略——因为**只有能 block 的事件才谈得上 fail-closed**（目前就是 `pre_tool_call`）[^c5-4][^c5-7]。

> [!warning] 不要写 shell 语法进 command
> `command` 是 `shlex.split` + `shell=False` 跑的，`|`、`&&`、`>`、`$(...)` 都不会被解释。你要写的逻辑请放进脚本文件（比如 `~/.hermes/agent-hooks/xxx.sh`），`command` 只写 `"~/.hermes/agent-hooks/xxx.sh"` 这一条调用。这和 Claude Code 的 `hooks.command` 传整条字符串的行为不同，刚迁过来的人最容易在这踩坑。

> [!tip] 大白话
> 把 `shell=False` 想成**去食堂打菜**：`shlex.split` 是"把你说的话按空格拆成一份菜名清单"（`["black", "a.py"]`），后厨严格按清单出菜；而 shell 解释是"把整句话抄给一个会自由发挥的大厨"（可能偷偷执行 `&&` 后面的命令）。Hermes 选前者，安全得多，代价是 command 里不能写管道。

### 5.3 `hooks_auto_accept: false` 与首次使用征询同意

shell hook 会以**你的完整用户凭据**执行（和 cron 条目、shell alias 同一信任边界），所以 Hermes 默认不让你悄悄跑任何脚本。机制是**首次使用征询同意**[^c5-8]：

- 每个唯一的 **`(event, command)` 对**第一次出现时，弹窗征询用户同意；
- 同意结果持久化到 `~/.hermes/shell-hooks-allowlist.json`；
- 之后的运行（CLI 或 gateway）不再询问。

> [!tip] 大白话
> 这就像**访客登记**：一个新脚本第一次进大门要登记（问一次"同意跑这个脚本吗"），登记在案之后，同一对 `(event, command)` 再来就直接刷脸进。注意登记的是"命令字符串"本身，不是脚本内容——脚本被改了也会照放行（见下）。

**三个逃生口，任意一个即可跳过交互式询问**[^c5-8]：

| 方式 | 写法 | 适用场景 |
| --- | --- | --- |
| CLI 参数 | `hermes --accept-hooks chat` | 交互式一次性放行 |
| 环境变量 | `HERMES_ACCEPT_HOOKS=1` | shell / CI 里批量放行 |
| config 开关 | `hooks_auto_accept: true` | 明确信任自己所有脚本，长期生效 |

**非 TTY 运行（gateway / cron / CI）必须三选一**——否则新加的 hook 会**静默地保持未注册**并打 warning，你的拦截/格式化/注入根本没生效，还不报错[^c5-8]。这是最容易"配了没反应"的坑之一。

**脚本编辑被静默信任**：allowlist 键在精确命令字符串上，不看脚本哈希，所以磁盘上改脚本不会作废同意。`hermes hooks doctor` 会标记 mtime 漂移，帮你发现"这个脚本被改过，要不要重新审视"[^c5-8]。

**手动 allowlisting**（非 TTY / 服务账号部署，无法交互应答时）——直接写 `~/.hermes/shell-hooks-allowlist.json`，格式是 `approvals` 数组，每条记录 `event` 和**精确的** `command` 字符串[^c5-8]：

```json
{
  "approvals": [
    {
      "event": "post_llm_call",
      "command": "/home/hermes/.hermes/hooks/my-hook.py"
    }
  ]
}
```

> [!warning] 手动 allowlist 的格式陷阱
> `command` 必须与配置里的命令字符串**逐字符一致**；文档明确警告：那种"以路径为 key、带 `sha256` 字段的对象"**不是**期望格式，不会批准成功。写完用 `hermes hooks list` 核对。另外 `revoke` 的生效要**下次重启**。

配套的 `hermes hooks` 命令族（S8 与 S7 两份文档都列了，合并如下）[^c5-9][^c5-13]：

| 命令 | 作用 |
| --- | --- |
| `hermes hooks list`（别名 `ls`） | 列出已配置 hooks：matcher、timeout、consent 状态；outbound 目标是否签名也会列出 |
| `hermes hooks test <event> [--for-tool X] [--payload-file F]` | 用合成 payload 触发所有匹配该 event 的 hook，打印**解析后**的返回（`parsed` 行就是 dispatcher 实际收到的 block 形状） |
| `hermes hooks revoke <command>`（别名 `remove`/`rm`） | 移除所有匹配 `<command>` 的 allowlist 条目（下次重启生效） |
| `hermes hooks doctor` | 逐个检查：exec 位、allowlist 状态、mtime 漂移、JSON 输出有效性、粗略执行耗时 |

### 5.4 `pre_tool_call` 实战：block / modify，JSON stdin→stdout，超时 fail-closed

`pre_tool_call` 在**每次工具执行前一刻**触发——内置工具和插件工具都算。模型一次并行调 3 个工具，它就触发 3 次。插件钩子的回调签名是 `def fn(tool_name, args, task_id, **kwargs)`[^c5-1]。

**JSON 线协议**：事件每次触发，Hermes 为每个匹配的 hook（matcher 允许时）起一个子进程，把 JSON payload 通过 **stdin** 喂进去，再从 **stdout** 读回 JSON。stdin 的形状是固定的[^c5-5]：

```json
{
  "hook_event_name": "pre_tool_call",
  "tool_name": "terminal",
  "tool_input": {"command": "rm -rf /"},
  "session_id": "sess_abc123",
  "cwd": "/home/user/project",
  "extra": {"task_id": "...", "tool_call_id": "..."}
}
```

- 非工具事件（`pre_llm_call`、`subagent_stop`、session 生命周期）时，`tool_name` 和 `tool_input` 为 `null`[^c5-5]。
- `extra` 字典携带该事件的全部事件专属 kwargs（`user_message`、`conversation_history`、`child_role`、`duration_ms`…）；不可序列化的值会字符串化而不是省略[^c5-5]。

**stdout 返回两种能力：block（需 message）与 modify（改写 tool_input）**：

```json
// block —— 需要非空 message
{"action": "block", "message": "Reason the tool call was blocked"}

// modify —— 改写工具参数，浅合并进原始 tool_input
{"action": "modify", "args": {"new_string": "fixed content"}}
```

语义细节（照 S8 原文）[^c5-1]：

- **block**：`block` 要求非空 `message`，命中后工具被短路，这段文字作为**返回给模型的错误**。多个回调时**第一个有效的 block 胜出**（Python 插件先注册、shell hooks 后注册，所以平局时 Python 的 block 优先）[^c5-11]。aggregator 一看到任何回调产出 `{"action":"block","message":非空}` 就返回。
- **approve**：`{"action":"approve","message":"...","rule_key":"可选:作用域"}` 会把调用升级到现有的人类审批门；`message`/`rule_key` 可省，且**拒绝、超时或门故障都 fail-closed**[^c5-1]。
- **modify**：返回的 `args` 字典会被**浅合并**进原始工具参数再执行。多个 modify 钩子会**累积**——每个钩子各改各的 key，都保留；若两个钩子改同一个 key，**后注册的赢**[^c5-1]。

**超时 fail-closed**：这是安全语义的核心。两个超时层要分清[^c5-1][^c5-4]：

| 层 | 默认值 | pre_tool_call 超时行为 |
| --- | --- | --- |
| Python 插件回调 | `plugins.hook_callback_timeout` 默认 30s（设 0 禁用，上限 600） | 超时或仍在上次超时后运行 → **fail-closed：阻塞工具**（不会在无策略决定的情况下放行） |
| shell hook 单条 entry | `timeout` 默认 60s（上限 300） | 默认 **fail-open**：warning 并放行；配 `fail_closed: true` 才阻塞（见 5.2 与下） |

**Exit code 2 = block（Claude Code / Cursor 兼容）**：`pre_tool_call` hook 以退出码 2 结束，即使 stdout 没有任何 block JSON，也会阻塞工具。block 消息按优先级解析：①stdout block JSON 的 `reason`/`message` → ②stderr 的前 400 字符 → ③兜底文案 `"Blocked by shell hook."`[^c5-6]。因此**最简单的阻塞钩子**是这样：

```bash
#!/usr/bin/env bash
echo "policy violation: rm -rf is not permitted" >&2
exit 2
```

对非 `pre_tool_call` 事件，exit 2 就当普通非零退出码处理：warning + 仍解析 stdout[^c5-6]。

**fail-open vs fail-closed 语义表**（shell hooks，S8 原文）[^c5-7]：

| 失败情形 | 默认 fail-open | `fail_closed: true` |
| --- | --- | --- |
| command 找不到 / 不可执行 | warning，放行 | **block** |
| 超时 | warning，放行 | **block** |
| stdout 不是合法 JSON（如 stack trace） | warning，放行 | **block** |
| 正常退出 + 合法 no-op JSON（`{}`） | 放行 | 放行 |

配了 `fail_closed: true` 的阻塞消息格式为 `hook <command> failed closed: <reason>`。**为什么默认是 fail-open**：对观测类 hook（记日志）这是对的默认值；但对安全闸门是错的——"崩溃的密钥扫描器不能静默放行它本该审查的工具调用"[^c5-7]。

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal|write_file|patch"
      command: "~/.hermes/agent-hooks/secret-scan.sh"
      timeout: 10
      fail_closed: true
```

> [!warning] 拦截用的钩子必须 fail-closed
> 凡是你当作"安全门"的 `pre_tool_call` 钩子，务必显式 `fail_closed: true`。脚本崩了、超时了、输出不是 JSON，都意味着"门坏了"——fail-open 默认值会让门直接敞开放行，等于白装。这是文档反复强调的安全语义。

### 5.5 Claude-Code 兼容双形状：`{"decision":"block","reason":...}` 与 `{"action":"block","message":...}`

从 Claude Code 迁过来最舒服的一点：**Hermes 的 shell hooks 直接收 Claude Code 风格返回，内部归一化**。同一意图两种写法都行[^c5-5][^c5-1]：

| 意图 | Hermes 规范（canonical） | Claude-Code 风格 |
| --- | --- | --- |
| block | `{"action": "block", "message": "..."}` | `{"decision": "block", "reason": "..."}` |
| modify | `{"action": "modify", "args": {...}}` | `{"decision": "modify", "tool_input": {...}}` |
| pre_llm_call 注入 | `{"context": "..."}` 或裸字符串 | 同左（`UserPromptSubmit` 无独立形状） |
| pre_verify 继续 | `{"action": "continue", "message": "..."}` | `{"decision": "block", "reason": "..."}`（阻止停下 = 继续） |

stdout 完整示例（可直接抄）[^c5-5]：

```json
// Block a pre_tool_call（两种形状都接受，内部归一化）：
{"decision": "block", "reason":  "Forbidden: rm -rf"}   // Claude-Code 风格
{"action":   "block", "message": "Forbidden: rm -rf"}   // Hermes 规范

// Modify a pre_tool_call —— 改写 tool args 后再分发：
{"action": "modify", "args": {"new_string": "fixed content"}}         // Hermes 规范
{"decision": "modify", "tool_input": {"new_string": "fixed content"}} // Claude-Code 风格

// Inject context for pre_llm_call：
{"context": "Today is Friday, 2026-04-17"}

// Keep the agent going at the verify gate（pre_verify，两种形状都接受）：
{"action": "continue", "message": "Run the formatter, then finish."}
{"decision": "block",  "reason":  "Run the formatter, then finish."}

// Silent no-op —— 任何空输出 / 不匹配的输出都行：
{}
```

归一化规则：`modify` 双形状最终都归一成 `{"action": "modify", "args": {...}}`[^c5-1]。`block` 双形状最终都归一成 `{"action": "block", "message": 非空}`。**malformed JSON、非零退出码、超时都只打 warning，永不中止 agent 主循环**[^c5-5]。

> [!tip] 大白话
> 这就像**写接口时兼容两套字段名**：前端发 `reason`、后端认 `message`，网关层把它们翻译成同一个内部对象。你把 Claude Code 的 hook 脚本原样搬过来，Hermes 也能读懂它的 `decision` / `reason` / `tool_input`——迁移成本几乎为零。

### 5.6 实战示例：拦截危险命令、自动格式化、`pre_llm_call` 注入上下文

最后给三个能直接落地的工作示例（全部出自 S8 原文），都遵循约定把脚本放在 `~/.hermes/agent-hooks/` 下，方便审计[^c5-10]。

**示例 1：拦截危险 `terminal` 命令**（`pre_tool_call` + matcher + timeout）——正则命中 `rm -rf /` 即输出 block JSON：

```yaml
# ~/.hermes/config.yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "~/.hermes/agent-hooks/block-rm-rf.sh"
      timeout: 5
```

```bash
#!/usr/bin/env bash
# ~/.hermes/agent-hooks/block-rm-rf.sh
payload="$(cat -)"
cmd=$(echo "$payload" | jq -r '.tool_input.command // empty')
if echo "$cmd" | grep -qE 'rm[[:space:]]+-rf?[[:space:]]+/'; then
  printf '{"decision": "block", "reason": "blocked: rm -rf / is not permitted"}\n'
else
  printf '{}\n'
fi
```

要点：`matcher: "terminal"` 只对 terminal 工具触发；用 `jq` 从 stdin payload 里取 `tool_input.command`；非命中走 `{}` 无操作分支。想让脚本自身崩溃也不放行，把这条 entry 加上 `fail_closed: true`。

**示例 2：写文件后自动格式化 Python**（`post_tool_call` + matcher）——每次 `write_file` / `patch` 命中就调 black：

```yaml
# ~/.hermes/config.yaml
hooks:
  post_tool_call:
    - matcher: "write_file|patch"
      command: "~/.hermes/agent-hooks/auto-format.sh"
```

```bash
#!/usr/bin/env bash
# ~/.hermes/agent-hooks/auto-format.sh
payload="$(cat -)"
path=$(echo "$payload" | jq -r '.tool_input.path // empty')
if [[ "$path" == *.py ]] && command -v black >/dev/null 2>&1; then
  black "$path" 2>/dev/null
fi
printf '{}\n'
```

> [!warning] 格式化只改磁盘，不改模型已读到的内容
> 文档明确提醒：agent 在上下文中对该文件的视图**不会**自动重读——reformat 只影响磁盘文件，后续的 `read_file` 才会读到格式化后的版本。所以别指望这一发格式化能让模型"看见"自己的错误输出。

**示例 3：每回合注入 `git status` 上下文**（`pre_llm_call`，Claude-Code `UserPromptSubmit` 的等价物）——把未提交变更塞进用户消息，模型一开场就知道工作区脏不脏：

```yaml
# ~/.hermes/config.yaml
hooks:
  pre_llm_call:
    - command: "~/.hermes/agent-hooks/inject-cwd-context.sh"
```

```bash
#!/usr/bin/env bash
# ~/.hermes/agent-hooks/inject-cwd-context.sh
cat /dev/null   # 丢弃 stdin payload
if status=$(git status --porcelain 2>/dev/null) && [[ -n "$status" ]]; then
  jq --null-input --arg s "$status" \
    '{context: ("Uncommitted changes in cwd:\n" + $s)}'
else
  printf '{}\n'
fi
```

要点：`pre_llm_call` 的注入点**永远是用户消息，绝不进系统提示**——这是有意的设计，系统提示跨回合保持不变，prompt 缓存才能命中[^c5-1]。多个插件都返回 context 时，按插件目录名字母序用**双换行**拼接[^c5-1]。`matcher` 不用于 `pre_llm_call`，因为它是按工具匹配的，非工具事件直接不写 `matcher`。

**安全与优先级收尾**（这两条决定了你该多谨慎）：

- **信任边界**：shell hooks 用你的完整用户凭据运行，和 cron / shell alias 同级别。文档建议：只引用自己写或审过的脚本；脚本放 `~/.hermes/agent-hooks/` 方便审计；拉完共享配置先跑 `hermes hooks doctor`；团队共享 config.yaml 时，审 `hooks:` 段的 PR 要像审 CI 配置一样[^c5-11]。
- **优先级**：Python 插件钩子先于 shell hooks 注册，平局时 Python 的 block 决定优先；第一个有效 block 即返回[^c5-11]。想让某种策略绝对优先，用插件钩子而不是 shell 钩子。

**验证路径**（呼应第六章，先给三个最常用的）：

```bash
hermes hooks list                 # 看注册了哪些、consent 状态
hermes hooks test pre_tool_call --for-tool terminal   # 合成 payload 试跑，看 parsed block 形状
hermes hooks doctor               # 体检：exec 位 / allowlist / mtime 漂移 / JSON 有效性
```

> [!summary]
> - Hermes 有四套 hook：Gateway（仅 gateway）、Plugin、**Shell hooks（config.yaml `hooks:` 块，CLI+Gateway 可用）**、Outbound Webhooks。要拦截/注入就用 shell 或 plugin。
> - shell hook schema：`hooks.<event>: [{matcher, command, timeout(默认60/上限300), fail_closed(默认false，仅 pre_tool_call)}]`；`command` 走 `shlex.split` + `shell=False`，不经过 shell 解释。
> - JSON 线协议：payload 从 **stdin** 进、结果从 **stdout** 出；`pre_tool_call` 返回 block（需非空 message）或 modify（浅合并进 `tool_input`）；非工具事件 `tool_name`/`tool_input` 为 `null`。
> - `hooks_auto_accept: false` 时每个 `(event, command)` 对首次要征询同意，持久化到 `~/.hermes/shell-hooks-allowlist.json`；gateway/cron/CI 等非 TTY 环境必须用 `--accept-hooks` / `HERMES_ACCEPT_HOOKS=1` / `hooks_auto_accept: true` 三选一，否则新 hook 静默失效。
> - 兼容双形状：Claude-Code 的 `{"decision":"block","reason":...}`、`{"decision":"modify","tool_input":...}` 与 Hermes 的 `{"action":"block","message":...}`、`{"action":"modify","args":...}` 都被接受并内部归一化；exit code 2 也能 block（最简单阻塞钩子）。
> - 拦截型钩子务必 `fail_closed: true`；shell hooks 脚本用你的完整用户凭据运行，审 `hooks:` 段要像审 CI 配置。

**下一步**：hook 配好只是第一步——怎么确认它真的进了 dispatcher、返回形状对不对、在 `--safe-mode` 下会不会消失，需要一套验证命令。下一章 第六章 验证与排错 — 让规则确实生效，将用 `hermes doctor` / `hermes config check` / `hermes prompt-size` 把"配置 → 验证 → 对照 safe-mode"的完整回路走通。

[^c5-1]: [S8 Event Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — 四类 hook 系统总览、插件钩子目录、pre_tool_call 返回语义、pre_llm_call 注入位置与多插件拼接。
[^c5-2]: [S8 Event Hooks — Gateway Event Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — Gateway 钩子仅 gateway 加载、handler 规则、wildcard 匹配。
[^c5-3]: [S8 Event Hooks — Plugin Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — `ctx.register_hook()`、`plugins.hook_callback_timeout`（默认 30s，上限 600）、observer/transform/directive 分类。
[^c5-4]: [S8 Event Hooks — Shell Hooks 配置 schema](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — `hooks.<event>` schema、VALID_HOOKS 校验、timeout/fail_closed 语义、`shlex.split` + `shell=False`。
[^c5-5]: [S8 Event Hooks — JSON wire protocol](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — stdin payload 形状、stdout 返回示例、malformed 行为。
[^c5-6]: [S8 Event Hooks — Exit code 2 = block](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — Claude Code / Cursor 兼容的 exit 2 阻塞与消息优先级。
[^c5-7]: [S8 Event Hooks — Fail-open vs fail-closed](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — 默认 fail-open、fail_closed 反转、失败情形对照表、`hook <command> failed closed` 消息。
[^c5-8]: [S8 Event Hooks — Consent model](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — (event, command) 首次征询、allowlist 文件、三个逃生口、脚本编辑静默信任、手动 allowlist 格式。
[^c5-9]: [S8 Event Hooks — The hermes hooks CLI](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — list / test / revoke / doctor 命令说明。
[^c5-10]: [S8 Event Hooks — Worked examples](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — 自动格式化、拦截 rm -rf、git status 注入、subagent 日志四例；`UserPromptSubmit` 等价说明。
[^c5-11]: [S8 Event Hooks — Security / Ordering and precedence](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — 完整凭据信任边界、脚本路径约定、Python 插件先于 shell hooks 注册。
[^c5-12]: [S8 Event Hooks — Outbound Webhooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — `hooks.outbound:` 配置、HMAC 签名、交付语义（notify-only、一次重试、不跟随重定向）。
[^c5-13]: [S7 CLI Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md) — `hermes hooks` 子命令、`--safe-mode` / `--ignore-user-config` / `--ignore-rules` 隔离开关。

---

## 第六章 验证与排错 — 让规则确实生效

前五章我们把 SOUL.md、AGENTS.md、config.yaml hooks 都配好了，但"写进文件"和"真正生效"是两回事：规则文件放进目录，不代表它进入了系统提示；配置改了一行，不代表运行中的会话会立刻读到。这一章回答一个核心问题：**怎么证明我的规则确实被 Hermes 加载了？没生效时又怎么定位是哪里断了？** 我们会先认识 Hermes 的验证命令族，再用 `hermes prompt-size` 离线确认规则是否进了系统提示，最后给出一套完整的"配置 → 验证 → 对照 safe-mode"排查工作流。

---

### 6.1 验证命令族：`hermes doctor [--fix]` / `hermes config ...` / `hermes status`

Hermes 把"配置健康度、配置值本身、运行时状态"拆成了三组命令，对应你在 Claude Code 里分别靠"看日志、看 settings.json、看 `/status`"才能拼出来的信息。三者分工如下（命令与用途均出自 [CLI Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md)）：

| 命令 | 用途 | 关键选项 |
| --- | --- | --- |
| `hermes doctor [--fix]` | 诊断配置与依赖问题 | `--fix`：尽量自动修复 |
| `hermes config show` | 显示当前全部配置值 | — |
| `hermes config edit` | 用你的编辑器打开 `config.yaml` | — |
| `hermes config get <key> [--json]` | 按 dotted key 读取单个值（如 `hermes config get model.default`） | `--json`：机器可读 |
| `hermes config set <key> <value>` | 写入单个配置值 | — |
| `hermes config unset <key>` | 删除某个键，恢复内置默认 | — |
| `hermes config path` / `env-path` | 打印配置文件 / `.env` 文件路径 | — |
| `hermes config check` | 检查缺失或过期的配置 | — |
| `hermes config migrate` | 交互式补充新版本引入的配置项 | — |
| `hermes status [--all] [--deep]` | 查看 agent、auth、平台运行状态 | `--all`（可分享的脱敏格式）、`--deep`（跑更慢的深度检查） |

> [!tip] 大白话：把 `hermes doctor` 想成"给 Hermes 做年度体检"。
> 它量血压（配置文件能不能正常解析）、查肝功能（依赖包有没有装齐），发现小毛病还能顺手开药（`--fix` 自动修复）。所以**配置一改完，先跑它**，别急着进对话。

#### 6.1.1 `hermes doctor` — 配置体检

```bash
# 只诊断，报告问题
hermes doctor

# 诊断并尝试自动修复
hermes doctor --fix
```

它针对的是"配置和依赖"层面：配置文件语法、缺少的依赖、可疑的键。`--fix` 会在它认为安全的地方自动修补。诊断通过不代表规则一定进入了系统提示——那是 6.2 的 `hermes prompt-size` 的职责，`doctor` 只保证"配置这台机器本身没坏"。

#### 6.1.2 `hermes config` — 配置值的读写查

这套子命令相当于把 Claude Code 里"手动编辑 settings.json + 猜哪个键生效"替换成显式的读写查：

```bash
# 看全量配置
hermes config show

# 按 dotted key 定向读一个键（推荐，比 show 更聚焦）
hermes config get model.default

# 写一个键；删一个键（恢复内置默认）
hermes config set terminal.backend docker
hermes config unset terminal.backend

# 打印两个关键文件的真实路径，排查"改错文件"问题
hermes config path
hermes config env-path

# 检查缺失或过期的配置项；新版本升级后跑 migrate 补新键
hermes config check
hermes config migrate
```

> [!warning] 配置"没生效"先查路径。
> 如果你不确定自己在编辑哪个文件，先跑 `hermes config path` 和 `hermes config env-path` 确认。改错了位置（比如手滑建了个 `~/.hermes/config.example.yaml`），`config show` 会立刻暴露——你改的值根本没出现在输出里。

#### 6.1.3 `hermes status` — 运行时状态一览

```bash
hermes status          # 常规状态：agent / auth / 平台
hermes status --all    # 全量详情，可分享的脱敏格式
hermes status --deep   # 更深的检查，耗时更长
```

`status` 回答的是"运行时我连上了什么"：认证有没有失效、平台桥接是否在线。它不负责校验规则内容，但"规则该生效却没生效"有时是运行时问题（比如 auth 失败导致走错 profile），先瞄一眼状态能排除这类干扰。

> [!note] 配套的诊断命令（求助时用）
> 除了上面三组，还有两个"打包快照"命令值得记：`hermes dump [--show-keys]` 输出一段可直接粘贴到 GitHub issue / Discord 的纯文本配置摘要（版本、OS、模型、API key 是否已设、features、config overrides 等，`--show-keys` 显示脱敏的 key 前缀）；`hermes debug share [--local]` 把系统信息 + 最近日志打包上传生成分享链接（`--local` 只在本地打印不上传）。两者都出自 [CLI Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md)，是升级求助时的标准姿势。

---

### 6.2 用 `hermes prompt-size [--platform][--json]` 离线确认 SOUL.md / AGENTS.md 进入系统提示

这是全章最关键的一条验证命令。它把 Hermes **真正会发给模型的那段系统提示**原样构建出来，然后按块拆成字节数（[CLI Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md)）：

```bash
hermes prompt-size [--platform name] [--json]
```

- **System prompt total**：完整组装后的系统提示总量（身份、引导、skills index、context files、memory、profile、timestamp）。
- **Skills index**：`<available_skills>` 块，装了大量 skills 时常常是最大的单块。
- **Memory / user profile**：你的 `MEMORY.md` / `USER.md` 快照。
- **Prompt tiers**：stable / context / volatile 三档，对应第三章提到的缓存分层。
- **Tool schemas**：所有启用工具的 JSON 描述（每次调用的另一大半固定负载）。

**关键特性：完全离线。** 不发 API 请求、没有凭证也能跑（`Runs entirely offline — no API call, works with no credentials configured`）。这意味着它可以在动手改规则前、改完立即验证，零成本、可反复执行。

```bash
# CLI 平台（默认）的人类可读构成
hermes prompt-size

# 模拟某个消息平台的提示（平台 hint 不同，字节可能不同）
hermes prompt-size --platform telegram

# 脚本用的机器可读输出
hermes prompt-size --json
```

#### 怎么用 `prompt-size` 证明"我的规则进去了"

规则文件的加载位置在系统提示的固定层里，见 [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly) 的 10 层组装：SOUL.md 是 **Layer 1 身份（stable 档第一块）**，项目上下文文件（AGENTS.md / CLAUDE.md / .cursorrules）是 **Layer 8（context 档）**。所以验证思路就是看这两块的字节有没有出现：

```bash
# ① 在项目根目录（放着 AGENTS.md）跑一次
cd ~/my-project
hermes prompt-size
# → System prompt total / context files 相关字节应该把 AGENTS.md 算进去

# ② 用全局开关 --ignore-rules 跳过规则注入，再跑一次，对比总量
hermes --ignore-rules prompt-size
```

两次的 **System prompt total 差值**，就是你当前目录这条规则链实际贡献的字节数。差值为 0，说明规则根本没被识别（多半是 6.4 的路径/优先级问题）；有差值，说明规则确实进入了系统提示。[CLI Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md) 的原话也确认了这一点：`Context files (AGENTS.md, .cursorrules) in your current directory also count toward the total.`

> [!tip] 大白话：`hermes prompt-size` 就是给系统提示"称体重"。
> 你把规则塞进系统提示，就像往行李箱里塞衣服——称一次体重就知道塞没塞进去。`--ignore-rules` 是"把行李箱清空再称一次"，两次差值就是规则的分量。

> [!warning] 别拿它当"内容对错"检测器。
> `prompt-size` 只告诉你"规则**进了**提示"，不告诉你"模型**遵守了**规则"。字节数对了之后，行为是否正确还得靠真实对话测试（6.5 第 5 步）。

> [!note] 想让提示变小怎么办
> skills index 和 tool schemas 会随启用的 skills/tools 数量线性膨胀。如果 `prompt-size` 显示这两块过大，官方建议：`hermes tools` 关掉不用的 toolset、`hermes skills` 卸载不需要的 skill。规则文件本身太长则会被截断（见 6.4.3）。

---

### 6.3 隔离排错开关：`--ignore-rules` / `--ignore-user-config` / `--safe-mode`

规则验证通过但行为仍不对时，下一步是**隔离变量**：到底是"我的自定义配置"导致的，还是"Hermes 本身"就这样？Hermes 给了三档递进的隔离开关（[CLI Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md)）：

| 开关 | 禁用/跳过的范围 | 仍然保留的 | 典型用途 |
| --- | --- | --- | --- |
| `--ignore-rules` | 自动注入的 `AGENTS.md`、`SOUL.md`、`.cursorrules`、memory、preloaded skills | 用户 config、`.env` 凭证 | 判断问题是否来自规则/记忆注入 |
| `--ignore-user-config` | `~/.hermes/config.yaml`，回退内置默认 | `.env` 凭证仍加载 | 隔离 CI 运行、可复现 bug 报告、第三方集成 |
| `--safe-mode` | **全部**自定义：user config、规则/记忆注入、插件、shell hooks、MCP servers | —（隐含前两者） | 判断"是我的配置问题还是 Hermes 本身" |

三个开关在调用层面有区别：`--ignore-user-config` 和 `--ignore-rules` 是**全局选项**（`hermes [global-options] command`，对任意子命令生效）；`--safe-mode` 是 **`hermes chat` 的选项**，作用于对话会话。

```bash
# 跳过规则注入，复现"没有我那些规则时的行为"
hermes chat --ignore-user-config --ignore-rules -q "Repro without my personal setup"

# 终极对照：禁用全部自定义，判断 bug 是谁的
hermes chat --safe-mode -q "Is this bug mine or Hermes'?"
```

#### 对照 Claude Code 排查法

在 Claude Code 里排查"规则没生效"，你多半会做这几件事：检查 CLAUDE.md 放的位置对不对、确认是不是被更高优先级的同名文件覆盖、临时把 `.claude/settings.json` 里的 hooks/权限关掉做对照、换个干净目录复现。这套"先隔离变量、再做对照实验"的思路，在 Hermes 里就是上面三档开关：

| Claude Code 排查手段 | Hermes 对应物 |
| --- | --- |
| 临时改名 / 禁用某条 hook 看行为是否变化 | `hermes chat --ignore-user-config`（跳过整个 config.yaml） |
| 把 CLAUDE.md 从目录移走看是否还生效 | `hermes chat --ignore-rules`（跳过全部规则注入） |
| 怀疑是配置污染，想回到"出厂状态"对照 | `hermes chat --safe-mode`（禁用全部自定义） |

对照实验的核心口诀：**先在最干净的档位（`--safe-mode`）复现**。如果干净档位下问题依旧，说明是 Hermes 自身或环境问题，别在自己的配置里空转；如果干净档位下问题消失，再逐档加回来（先 `--ignore-user-config`、再 `--ignore-rules`），找到引入问题的那一层。

> [!tip] 大白话：把 `--safe-mode` 想成"装修被叫停，先看毛坯房"。
> 你的配置是装修（规则、插件、hooks、MCP），Hermes 本身是毛坯房。房子漏水，是先怪装修还是先怪水管？`--safe-mode` 就是把你请的施工队全部撤场，只看毛坯房——漏不漏一目了然。

> [!warning] `--ignore-user-config` 不清空凭证，别拿它当"裸奔"。
> 官方明确写了 `Credentials in .env are still loaded`。它只跳过 `config.yaml`，`.env` 里的 API 凭证照常加载——所以它适合"复现配置问题"，不适合"确认没泄露任何自定义状态"。

---

### 6.4 常见坑：规则未生效、优先级/覆盖顺序理解错误、被安全扫描拦截、与内置默认冲突

#### 6.4.1 规则"没生效"——先查位置和时机

- **SOUL.md 只认 `HERMES_HOME`**。它从 `~/.hermes/SOUL.md`（或 `$HERMES_HOME/SOUL.md`）加载，**不会探测工作目录**（[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)）。把 SOUL.md 放到项目目录里 = 永不生效。
- **非 git 仓库只看 CWD**。AGENTS.md 只在 git 仓库里做目录链合并；不在 git 仓库时，只有工作目录本身被检查，父目录的 AGENTS.md 不会泄漏进来（[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)）。在 `/tmp` 或 `$HOME` 放 AGENTS.md 想全局生效，是常见误区。
- **子目录规则是"渐进发现"的**。启动时只把 CWD 的上下文文件放进系统提示；进入子目录后，该目录的 AGENTS.md / CLAUDE.md / .cursorrules 才按需注入（每目录至多一次、上溯至多 5 级、单文件 8000 字符截断）（[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)）。所以**启动时 `prompt-size` 看不到子目录规则是正常现象**，别误判为失效。

#### 6.4.2 优先级 / 覆盖顺序理解错误

- **每次会话只加载一种项目上下文（first-match-wins）**：`.hermes.md`/`HERMES.md` → `AGENTS.override.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`（[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)）。只要 `.hermes.md` 存在，你精心写的 AGENTS.md / CLAUDE.md / .cursorrules 就**全部不加载**——这是最常踩的坑。
- **`AGENTS.override.md` 是"替代"不是"叠加"**：它和已提交的 AGENTS.md 同时存在时，override **替代** AGENTS.md（[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)）。想个人差异又不动仓库文件，就用它；但别指望两者内容合并。
- **目录链里"深者优先"**：git 根 → CWD 的 AGENTS.md 按顺序合并，更深层的文件出现在提示后面、更具体、优先（[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)）。以为"根目录规则优先级最高"是理解反了。

> [!tip] 大白话：first-match-wins 就像"只有一个门禁卡能进门"。
> 门禁系统从上到下只认**第一张**有效的卡。你兜里揣了 AGENTS.md、CLAUDE.md、.cursorrules 三张卡，但只要第一张 `.hermes.md` 在，门禁只认它，后面几张掏都不掏。

#### 6.4.3 被安全扫描拦截或截断

所有上下文文件注入前都过**安全扫描**（[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)），命中以下模式直接整文件丢弃：

| 扫描类别 | 示例模式 |
| --- | --- |
| 指令覆盖尝试 | `ignore previous instructions`、`disregard your rules` |
| 欺骗模式 | `do not tell the user` |
| 系统提示覆盖 | `system prompt override` |
| 隐藏 HTML 注释 / div | `<!-- ignore instructions -->`、`<div style="display:none">` |
| 凭据外泄 | `curl ... $API_KEY` |
| 秘密文件访问 | `cat .env`、`cat credentials` |
| 不可见字符 | 零宽空格、双向覆盖符、word joiners |

拦截时会在提示里留下占位：

```
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

此外还有**截断**：文件超过 `context_file_max_chars`（配置里显式设置时用它；否则随模型窗口动态，floor 20,000 / ceiling 500,000 字符）按 70% 头 + 20% 尾 + 10% 标记截断（[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)）。**规则里写在文件末尾的内容可能被截掉**，提示会出现：

```
[...truncated AGENTS.md: kept 14000+4000 of 25000 chars. Use file tools to read the full file.]
```

> [!warning] "规则没生效"先看有没有 `[BLOCKED:` 或 `[...truncated`。
> 这两个标记不会让 Hermes 报错，只在系统提示里静默出现。规则被安全扫描拦截、或长规则被截断，是最隐蔽的"失效"原因——先用 6.2 的 `prompt-size` 对比总量，再在对话里问 agent 能否复述规则内容，定位是不是被拦/被截。

#### 6.4.4 与内置默认冲突

- **空 SOUL.md = 不加任何东西**；SOUL.md 不存在时回退到内置默认身份 `DEFAULT_AGENT_IDENTITY`（[Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)）。想"删掉自定义身份"时，`unset` 配置键也是同理：`hermes config unset <key>` 恢复内置默认。
- **subagent 委托会跳过 SOUL.md**：`skip_context_files` 设置（如 subagent 委托）时，SOUL.md 不加载、改用硬编码默认身份（[Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)）。所以"主会话听我的 SOUL.md，subagent 却不听"是设计行为。
- **`platform_hints` 里 `replace` 优先于 `append`**，畸形条目会被防御性忽略、回退默认（[Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)）。写坏一个平台的 hint 不会拖垮整个提示组装。
- **hooks 的 consent/revoke 改动"下次重启生效"**：`hermes hooks revoke` 移除的是 `~/.hermes/shell-hooks-allowlist.json` 里的允许项，文档明确写 `takes effect on next restart`（[CLI Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md)）。改完没重启就测，会误以为没生效。

---

### 6.5 一条完整的"配置 → 验证 → 对照 safe-mode"工作流

把上面所有命令串成一条可重复执行的工作流。每配完一章规则，就跑一遍；怀疑出问题时，从第 4 步开始做二分。

```text
① 配置         写 / 改 SOUL.md、AGENTS.md、config.yaml
   ↓
② 静态体检     hermes doctor            → 配置与依赖有没有问题
               hermes config check      → 有没有缺失/过期配置
   ↓
③ 定向确认     hermes config get <key>  → 某个键的值是不是我写的
               hermes config path       → 确认改对了文件
   ↓
④ 规则入提示   hermes prompt-size                → 项目目录下跑一次
               hermes --ignore-rules prompt-size → 再跑一次对比总量
               差值>0 ⇒ 规则确实进了系统提示；差值=0 ⇒ 回 6.4 查位置/优先级
   ↓
⑤ 行为测试     hermes chat -q "复述你的规则里关于 X 的要求"
               字节在 ≠ 行为对；行为不对才进入第 6 步
   ↓
⑥ 对照排查     hermes chat --safe-mode -q "复现同一个问题"
               ├─ 干净档位仍出错 ⇒ 问题在 Hermes 自身/环境，别改配置了
               └─ 干净档位正常   ⇒ 逐步加回
                   hermes chat --ignore-user-config -q "复现"   # 是 config 还是规则？
                   hermes chat --ignore-rules -q "复现"          # 是规则注入吗？
   ↓
⑦ hooks 专项   hermes hooks list            # 看 matcher/timeout/consent 状态
               hermes hooks doctor          # 查 exec 位/allowlist/mtime/JSON/耗时
               hermes hooks test pre_tool_call  # 用合成负载试触发
   ↓
⑧ 升级求助     hermes dump --show-keys | 粘贴给 issue/Discord
               hermes debug share --local   # 或上传生成分享链接
```

各命令对应的排查结论：

| 命令 | 通过 = | 不通过 = |
| --- | --- | --- |
| `hermes doctor` | 配置/依赖健康 | 先修配置，别急着调规则 |
| `hermes config check` | 无缺失/过期项 | 按提示补键，必要时 `hermes config migrate` |
| `hermes prompt-size`（差值对比） | 规则字节进入系统提示 | 回 6.4.1 / 6.4.2 查位置与优先级 |
| `hermes chat --safe-mode` | 问题源自你的自定义 | 问题在 Hermes 自身或环境 |
| `hermes hooks doctor` | hooks 脚本本身健康 | 查 exec 位 / allowlist / 脚本 JSON 合法性 |

> [!warning] 二分排查只动一个变量。
> 第 6 步里 `--ignore-user-config` 和 `--ignore-rules` 要**分别单独跑**，不要一上来就两个一起加——一起加等于直接跳到 `--safe-mode`，反而分不清是 config 还是规则注入引起的。先隔离到"复现/不复现"的边界，再定位到具体那一层。

---

> [!summary] 本章总结
> - 验证三件套分工明确：`hermes doctor [--fix]` 查配置与依赖健康，`hermes config show/get/set/unset/check/path` 读写查配置值，`hermes status` 看运行时状态；升级求助用 `hermes dump` / `hermes debug share`。
> - `hermes prompt-size [--platform][--json]` 完全离线、零成本，是证明"规则进入系统提示"的最直接手段：对比 `hermes prompt-size` 与 `hermes --ignore-rules prompt-size` 的总字节差，差值就是规则链的真实贡献。
> - 隔离排错三档开关：`--ignore-rules`（跳过规则/记忆注入）、`--ignore-user-config`（跳过 config.yaml，`.env` 凭证仍加载）、`--safe-mode`（禁用全部自定义，仅 `hermes chat`）。先在最干净档位复现，再逐档加回。
> - 常见"失效"坑：位置错误（SOUL.md 只认 HERMES_HOME、非 git 只看 CWD）、优先级理解错（first-match-wins 只加载一种、override 是替代不是叠加）、被安全扫描拦截（`[BLOCKED: ...]`）或长规则被截断（`[...truncated`）、与内置默认冲突（空 SOUL.md 回退默认身份、subagent 跳过 SOUL.md、hooks revoke 重启才生效）。
> - 完整工作流是"配置 → 静态体检 → 定向确认 → 入提示验证 → 行为测试 → safe-mode 对照 → hooks 专项 → 升级求助"八步，每步都有对应命令和明确结论。

**下一步**：到这里，本笔记的主线已经闭环——从第一章的文件地图，到第二、三章配置全局身份与项目规则，第四章从 Claude Code 迁移，第五章接上 hooks 自动化，再到本章的验证与排错。你可以在实际配置时把第六章穿插使用：每配完一个文件就用 `hermes prompt-size` 验证一次，出了问题用 `--safe-mode` 做对照。如果想回看完整链路，回到本笔记的目录（Hermes Agent MOC）从头梳理；当你有把握让规则"可验证地生效"时，就可以把这套流程固化成语录或 skill，让每次配置都走同一条检查清单。
