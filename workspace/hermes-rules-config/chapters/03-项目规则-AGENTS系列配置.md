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
