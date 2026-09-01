# 第 5 章补充素材（EduHub 技能生态 + My Agents 调度外部 agent）

> 阶段：P2 补充收集（learning-note-flow / run_id: deeptutor）
> 收集日期：2026-09-01
> 目标：为 03_outline.md 第 5 章 5.3（My Agents）与 5.5（EduHub 技能生态）写作补齐实操细节
> 素材引用：[S1]（复用已有 GitHub README）+ 新增 [S7]–[S13]，原始抓取见 `sources/07~13_*.md`

## 1. 补充范围

本次针对大纲标记的两个素材缺口补收集：EduHub 技能生态（Agent-Skills 格式、搜索/安装/发布、安全门）与 My Agents（连接外部 agent 实时调度、导入 Claude Code/Codex 历史会话），并连带补齐 CLI/SDK 驱动 DeepTutor 的入口（对应 5.4）。

## 2. 源表（新增 S7–S13）

| ID | 标题 | URL | 发布方 | 层级(Tier) | 日期 | 相关性说明 |
|----|------|-----|--------|-----------|------|-----------|
| S7 | Overview — How to use EduHub | https://eduhub.deeptutor.info/how-to-use/overview | EduHub 官方 | Tier 1 | 2026-09-01 抓取 | Agent-Skills 包格式定义；搜索/安装免登录、发布需登录；ClawHub 协议 |
| S8 | EduHub 首页（Make any agent your lifelong tutor） | https://eduhub.deeptutor.info/ | EduHub 官方 | Tier 1 | 2026-09-01 抓取 | 72 技能 / 4 大 track；独立 eduhub CLI（npm）用法；Web 上传入口；示例技能 |
| S9 | 代理交接 CLI agent-handoff（中文文档） | https://docs.deeptutor.info/zh-cn/cli/agent-handoff/ | DeepTutor 官方文档 | Tier 1 | 2026-09-01 抓取 | 外部 agent 驱动 DeepTutor：SKILL.md 交接、Claude Code/Codex/OpenCode/Hermes 接入、session 交接、JSON 事件流解析 |
| S10 | 我的智能体 My Agents / Subagents（中文文档） | https://docs.deeptutor.info/zh-cn/explore/subagents/ | DeepTutor 官方文档 | Tier 1 | 2026-09-01 抓取 | My Agents 两件事：连接 9 种 live harness / 导入 Claude Code+Codex 历史；consult_subagent 机制、Max rounds、`@` 引用 |
| S11 | Let an agent do it（让 agent 代发技能） | https://eduhub.deeptutor.info/how-to-use/agent-publish | EduHub 官方 | Tier 1 | 2026-09-01 抓取 | 通过 prompt 或在线指南让 Codex/Claude Code 等创建、发布、验证技能；dry-run 前置流程 |
| S12 | Maintain: update & roll back | https://eduhub.deeptutor.info/how-to-use/maintain | EduHub 官方 | Tier 1 | 2026-09-01 抓取 | 版本 semver 与 rollback 语义、slug 所有权、上传静态扫描 |
| S13 | EduHub Skill Manager（面向 agent 的完整指南） | https://eduhub.deeptutor.info/eduhub-skill-manager.md | EduHub 官方 | Tier 1 | 2026-09-01 抓取 | SKILL.md 字段规范；track/language/domains/stages/forms/tags；eduhub login/publish/inspect/search/install 全套命令 |

复用说明：[S1] = 已有 GitHub README（`sources/06_github_com.md`），EduHub/My Agents/CLI 相关段落见其 `Ecosystem`、`My Agents`、`CLI` 章节。

## 3. claim→source 映射

### 3.1 EduHub 技能生态（Agent-Skills 格式）

- 技能 = 一个含 `SKILL.md`（YAML frontmatter + Markdown playbook）的文件夹 + 可选支持文件；**格式开放、非 DeepTutor 专属**，任何说该格式的 registry 都能成为技能源。→ S1, S7
- EduHub 是 DeepTutor 官方的**教育技能社区/registry**，内建为默认 hub；裸 slug 或 `eduhub:` 前缀都解析到它。→ S1
- EduHub 说 **ClawHub 协议**，同时扮演"独立 registry + DeepTutor 内建"两种角色。→ S1, S7
- 现状规模：72 个技能、4 大 track（Academics / Companions / Skills & Interests / For Educators）；示例技能：`socratic-tutor`、`flashcard-deck`、`essay-feedback`。→ S8
- **搜索/安装免登录**；仅发布需登录（用于署名与保护 slug 所有权）。→ S7, S13
- 浏览器内入口：**Learning Space → Skills → Import from EduHub**，浏览目录并直接下载进技能库（过安全门）。→ S1
- 终端搜索/安装（DeepTutor CLI，单数 `skill`）：
  - `deeptutor skill search "socratic tutor"`（搜默认 hub EduHub）
  - `deeptutor skill install socratic-tutor`（fetch → verify → register）
  - `deeptutor skill install eduhub:socratic-tutor@1.2.0`（钉 hub + 版本）
  - `deeptutor skill list`（本地技能及其 hub 来源）
  → S1
- 兼容 ClawHub：`deeptutor skill search "..." --hub clawhub`、`deeptutor skill install clawhub:git-release-notes@1.0.1`；多个发布者同名 slug 时用全限定引用 `clawhub:<ownerHandle>/<slug>`。→ S1
- 自定义 registry：在 `data/user/settings/skill_hubs.json` 加 `type:"clawhub"`（指向任意兼容 HTTP API，EduHub/ClawHub 都讲它）或 `type:"command"`（包装 registry 自带的 fetch CLI）；`"default"` 指定裸 slug 用哪个 hub；全部走同一导入安全门。→ S1
- 发布自有技能（DeepTutor CLI）：`deeptutor skill login`（浏览器登录 EduHub）→ `deeptutor skill publish ./my-skill`（交互选 track + tags 后上传）→ `deeptutor skill update`（回滚或发新版）。→ S1
- 非 DeepTutor 的 agent 也能直接消费：独立 `eduhub` CLI，如 `npx eduhub install socratic-tutor`。→ S1, S8

### 3.2 导入安全门（safety gate）

- 无论来源，每次导入在触碰工作区前都过**同一道安全门**：→ S1
  1. 先查 registry 的 **security verdict**，被标记的包拒绝，除非显式 `--allow-unverified`；
  2. 归档**防御性解压**（zip-slip / zip-bomb 防护）+ **文本/脚本后缀白名单**，二进制永不落进工作区；
  3. frontmatter 规范化为 DeepTutor schema 并**剥离 `always:`**，下载的技能不能强制注入每个 system prompt；
  4. 来源（hub、版本、verdict、安装时间）写入 **`.hub-lock.json`** 供审计与更新。
- 多用户部署下：导入落进调用者自己的技能库；admin 分配的技能保持 grant-scoped 只读。→ S1

### 3.3 发布与版本维护（EduHub）

- `deeptutor skills update`（交互，复数形式）：登录后列出你发布过的技能，选"回滚"或"升级"；升级会从当前标签预填发布表单。→ S12
- 版本 **semver 并存**，安装用 `@version` 钉版，默认取 latest；rollback 把 latest 指针移到旧版本（不新建版本），之后再发更高版本会再前移（npm 式语义）。→ S12
- 一旦 slug 存在，**只有所有者（或 admin）**能发新版或回滚。→ S12
- 每次上传都过**静态扫描**：可疑模式（pipe-to-shell、env 外泄、原生可执行文件等）会被标记，交给安装方的 import gate 权衡。→ S12
- 让 agent 代发：把 prompt 或在线指南（`eduhub-skill-manager.md`）交给 Codex/Claude Code/DeepTutor，先 `eduhub skill publish --dry-run`，通过后再发布，再用 `inspect` / `search` / `install` 到临时目录验证。→ S11, S13

### 3.4 SKILL.md 规范（面向技能创作者）

- 至少 `name` + `description` 两个 frontmatter 字段；正文写成可执行的 playbook（何时用、先做什么再做什么、规则/反模式/验证步骤），长资料移到支持文件并在 SKILL.md 里链接。→ S13
- 分类元数据：track（academics / companions / skills-interests / educators）、language（zh / en / ja / other）、可选 domains / stages（K12, university, adult）/ forms（tutor, practice, companion, tool）/ tags。→ S13
- 授权约束：只用 permissive 许可素材；复制/改写须附 `ATTRIBUTION.md`（原作者、项目、许可、源 URL、改了什么）；不引入 GPL/AGPL/无许可文本；包保持最小。→ S13
- 命令集：`eduhub whoami` / `eduhub login` / `eduhub login --token <token>` / `eduhub --no-input skill publish ./my-skill --track ... --language ... --tags ... --changelog ... [--dry-run]` / `eduhub skill inspect <slug>` / `eduhub search <query>` / `eduhub install <slug> --workdir <dir> --dir skills`。→ S13

### 3.5 My Agents：连接外部 agent 实时调度

- My Agents 把其他 agent 变成 DeepTutor 的上下文，做**两件不同的事**：连接 live agent（实时咨询）+ 导入历史会话。→ S1, S10
- 可连接的 live agent：本机 **9 种 harness**（Claude Code、Codex、Antigravity CLI、Kimi CLI、opencode、MiMo Code、Hermes Agent、OpenClaw、DeepSeek Harness）之一，或你自己的 Partner。→ S1, S10
- 咨询时 DeepTutor **不是粘贴对话记录，而是真的运行那个 agent** 并把工作流式回传到 Activity 面板；底层是聊天循环里的 **`consult_subagent`** 工具多轮驱动。→ S1, S10
- 聊天内触发：输入框工具栏的 **Agent 胶囊**（机器人图标）选中 agent 并设 **"Max rounds DeepTutor may ask"**（本次来回轮数上限）；或直接输 `@` 做单轮就地 @。→ S1, S10
- 咨询 Claude Code：在其自己的工作目录运行（读文件 / grep / 对真实仓库推理），工具调用流式进活动面板，DeepTutor 收拢结论。→ S10
- 咨询 Partner：把问题送进伙伴自己的会话，伙伴用其 soul、资料库、私有记忆工具（`partner_search`、`partner_read`）与技能（`read_skill`）作答；一个聊天线程绑定一个伙伴会话，追问延续同一段对话。→ S10
- UI 位置：左侧栏 **My Agents**；历史版本在 v1.4.6 曾位于 `/space/agents`，v1.4.7 提升为顶级 `/agents`。→ S1（release notes）, S10

### 3.6 My Agents：导入历史会话

- 导入已有的 **Claude Code 与 Codex 对话**，每个来源呈现为有名字的 agent，可搜索、可打开、可续聊、可在聊天里引用。→ S1, S10
- 操作路径：**Add agent** → 给 agent 起名 → **按天选择要导入的日期**；之后 **Refresh** 会重新同步所选天数并拉进当天新对话。→ S1, S10
- 导入的 agent 显示来源、对话数、上次同步时间；可"打开一段对话续聊"、"刷新拉新"、"通过 `+` → My Agents 在任意轮引用"。→ S10
- 引用时 DeepTutor 把导入会话当作**第三方对话记录**读取（"仍是他们的对话，DeepTutor 不会第一人称代入"）。→ S1, S10

### 3.7 CLI/SDK 驱动入口（对应 5.4）

- CLI 双入口：`deeptutor chat`（交互 REPL）、`deeptutor run <capability> "<msg>"`（单轮退出）；共用 `--capability` / `--tool` / `--kb` / `--config`。→ S1
- `--format json` 输出 **NDJSON**（每行一事件：`content` / `tool_call` / `tool_result` / `done` 等，每行带 `session_id`）；headless 下 `ask_user` 暂停自动空回复，不挂起。→ S1, S9
- 多轮串联：从 `done` 事件抓 `session_id`，后续 `deeptutor run ... --session "$SID"` 复用同一 session 上下文（含对话历史与分支）。→ S1, S9
- 仓库根 `SKILL.md`（约 200 / 203 行）是给"会用 tool 的 LLM"的交接文档：When to Use、Prerequisites、Commands、REPL Slash Commands、Typical Workflows；Claude Code / Codex / OpenCode 在项目根看到会**自动读取**。→ S1, S9
- 原生不认 `SKILL.md` 的框架（LangChain / AutoGen / 自定义 loop）：把 `deeptutor run --format json` 包成 tool 定义即可。→ S1, S9
- 在 Claude Code 里做成固定 subagent：`.claude/agents/study-agent.yaml`（`tools: [Bash, Read, Write]`，system_prompt 指示先读 SKILL.md、用 `deeptutor run ... --format json`）。→ S9
- Codex / OpenCode：项目根放 SKILL.md + 自然语言提示；OAuth provider 用 `deeptutor provider login openai-codex`（浏览器 OAuth，token 存工作区）。→ S9
- 云端/沙箱 agent 需要放行 provider endpoint（OpenAI `api.openai.com:443`、Anthropic、Gemini、Azure 各自 443，本地 Ollama/vLLM 见 `model_catalog.json`）；RAG 密集还要放行搜索 provider（Tavily/Brave/Jina/Serper/Perplexity/SearXNG/DuckDuckGo）。→ S9

## 4. 实操要点（给 chapter-writer 的可执行速查）

### 4.1 EduHub：格式 / 搜索 / 安装 / 发布 / 安全门

- **格式**：技能文件夹根放 `SKILL.md`（frontmatter `name`+`description` + Markdown playbook），可选支持文件；slug 用小写连字符。→ S13
- **搜索/浏览**：浏览器 `Learning Space → Skills → Import from EduHub`；或终端 `deeptutor skill search "<词>"`。→ S1
- **安装**：`deeptutor skill install <slug>`（裸 slug 默认 EduHub；`eduhub:<slug>@<version>` 钉版；`clawhub:<owner>/<slug>` 走 ClawHub）。→ S1
- **发布**：`deeptutor skill login` → `deeptutor skill publish ./my-skill`（交互选 track + tags）→ `deeptutor skill update`（回滚 / 发新版）。→ S1, S12
- **安全门**：每个导入过 ① registry verdict（flagged 需 `--allow-unverified`）② zip 防护 + 后缀白名单 ③ 剥离 `always:` ④ 写 `.hub-lock.json`。→ S1
- **非 DeepTutor 使用**：`npm i -g eduhub`（或 `npx eduhub …`）；Web 上传入口 `eduhub.deeptutor.info/upload`。→ S8

### 4.2 My Agents：调度外部 agent 与导入历史

- **连接 live agent**：`My Agents → Connect agent` → 选 9 种本地 harness 之一或 Partner。→ S10
- **聊天内咨询**：Agent 胶囊选 agent → 设 Max rounds；或直接 `@` 单轮。→ S10
- **导入历史**：`Add agent` → 命名 → 按天选择 → 之后 `Refresh` 同步新对话。→ S10
- **引用导入会话**：聊天里 `+` → My Agents → 选一段，DeepTutor 以第三方视角读取（不代入）。→ S10
- **反向：外部 agent 驱动 DeepTutor**：项目根放 `SKILL.md`（Claude Code/Codex/OpenCode 自动读），或包成 LangChain/AutoGen tool；长程任务用 `--format json` + `--session`。→ S1, S9

## 5. 存疑 / 未解决点

1. **CLI 单复数混用**：README（S1）用单数 `deeptutor skill search/install/publish`；EduHub 官方文档则混用 `deeptutor skills install`（S7）、`deeptutor skills update`（S12）、`eduhub skills search/install`（S8）与 `eduhub skill publish/inspect`（S13）。写作以 README 官方命令表（单数 `deeptutor skill`）为基准，并提示读者不同文档存在单复数混用。→ 推断（基于 S1/S7/S8/S12/S13 对比）
2. **数字为抓取快照**：EduHub 首页称"72 skills / 4 tracks"（S8），是 2026-09-01 时点数据；写作标注"以官网为准"，避免数字漂移。→ S8
3. **harness 清单随版本变化**："9 种本地 harness"以当前版本为准；v1.5.3 release note 曾提"Gemini、Kimi、opencode、MiMo"四款 coding CLI 加入 My Agents，与 README 当前 9 种清单不完全同口径。→ S1（release notes）
4. **技能如何挂载到运行时未详述**：EduHub 安装后的技能经 `read_skill` 工具被读取（S1 上下文工具清单），但"安装后技能如何进入 agent loop / 如何被系统提示引用"在本次补收集源中无进一步细节；如需深入建议查官方 Learning Space / Personalization 文档或实测。→ 推断
5. **术语口径**：README 称导入会话为 "third-party transcript"（S1），官方中文文档称"第三方对话记录 / 仍是他们的对话"（S10）；写作统一中文表述即可，并点出"导入会话不并入 DeepTutor 自己的声音"。→ S1, S10
6. **Skill 的目标口径**：S13 把技能描述为 "Codex-compatible skill"，而 DeepTutor 侧统一称 Agent-Skills / ClawHub 协议；三者关系写作时一句带过即可（开放式格式 + ClawHub 协议 + Codex 兼容）。→ S13, S1
