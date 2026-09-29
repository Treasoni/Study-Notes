# P1 探测结果 — 自托管 AI Agent 平台选型

- **运行**: `ai-agent-platform-selection`（learning-note-flow）
- **阶段**: P1 探测式收集
- **检索日期**: 2026-09-29
- **派发**: 3 个并行探测代理（透镜 1 = Octop 单平台；透镜 2 = OpenClaw × Hermes 对照 + 本地存量；透镜 3 = 横向选型依据）

---

## 0. 一句话结论

探测材料指向一个结论：**这三者大概率不在同一层**。「不知道用哪个」里有相当一部分是**范畴错误**——在 OpenClaw / Hermes 之间问「用哪个」是个有效但很窄的问题，而 Octop 回答的是另一个问题（多人怎么共用一个 agent 平台）。

> ⚠️ 状态：这是**推断**，不是已核实的结论。P2 的核心任务就是验证或推翻它（见 §5 待裁决项）。

---

## 1. 候选来源表（按 URL 去重，合并三透镜）

| # | 标题 | URL | 层级 | 相关性 | 日期 | 分 |
|---|---|---|---|---|---|---|
| 1 | Octop README_CN.md | https://github.com/TencentCloud/Octop/blob/main/README_CN.md | 官方/一手 | 定位语 + Highlights/Overview/Core Technology/Features/Roadmap/Quick Start，可判定「平台 vs 助手」 | 2026-09-29 | 4 |
| 2 | Octop docs/architecture.md | https://github.com/TencentCloud/Octop/blob/main/docs/architecture.md | 官方/一手 | 五层分层（Surface/API/Domain/Reusable libs/Storage）、单进程启动树、per-user 隔离（JWT + `agents.user_id` 行级归属）、Storage 双后端、§6 harness teams | 2026-09-24 | **5** |
| 3 | Octop docs/adr/001、002 | https://github.com/TencentCloud/Octop/tree/main/docs/adr | 官方/一手 | 单进程无外部队列的设计决策；SQLite / PostgreSQL 控制面选型 | 2026-07-25 | 4 |
| 4 | Octop plugins/README.md | https://github.com/TencentCloud/Octop/blob/main/plugins/README.md | 官方/一手 | 扩展体系实证：`plugin.yaml` 契约、`kind ∈ {tool, skill, hook}`、`setup(ctx)` API、可选 `ui/dist` 前端注入、6 个示例插件 | 2026-09-24 | 4 |
| 5 | octop-harness / octop-memory / octop-gateway 三库 | https://github.com/TencentCloud/octop-harness | 官方/一手 | 三个可复用库已独立公开：agent runtime（LangGraph）、分层/跨会话记忆、IM 通道桥接 | 2026-09-24 | **5** |
| 6 | OpenClaw README | https://github.com/openclaw/openclaw | 官方/一手 | 自述「个人 AI 助手」；Gateway 为本地控制平面；CLI/UI/节点经 WS 接入；多渠道 | 活跃 | **5** |
| 7 | OpenClaw Docs · Team setup | https://docs.openclaw.ai/start/teams | 官方/一手 | **多用户轴的直接答案**：一个 Gateway = 一个信任域，「团队运行是配置而非独立版本」，多用户含归属/分配/在场，互不信任须一租户一 Gateway | — | **5** |
| 8 | OpenClaw Docs · Gateway architecture | https://docs.openclaw.ai/concepts/architecture | 官方/一手 | Gateway 单守护进程、每主机唯一、串行执行 session → 是「控制平面」而非纯 agent 内核 | — | 4 |
| 9 | Hermes Agent README | https://github.com/NousResearch/hermes-agent | 官方/一手 | 「The agent that grows with you」；内置学习回路、自建技能、Honcho 用户建模、多终端后端；**提供 `hermes claw migrate` 从 OpenClaw 迁移** | v2026.9.24 | **5** |
| 10 | Hermes Docs · Gateway internals / developer guide | https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals | 官方/一手 | 内核为 AIAgent 中心的 agent-loop；CLI/Gateway/API/Batch 共用一个内核 → harness/运行时形态 | — | 4 |
| 11 | ~~知乎：对比 OpenClaw 与 Hermes-Agent 的设计哲学~~ **【P2 降级：抓取失败】** | https://zhuanlan.zhihu.com/p/2047204065948471698 | **不可用** | **P2 三路抓取均失败**（`crawl.sh` / curl+浏览器 UA / WebFetch 全 403，且搜索引擎确认该链接未被索引）。P1 该条**仅来自搜索摘要，从未取得原文** → **不得作为引文来源**。替代佐证见 `research/openclaw/community/01_cloud_tencent_cn.md`（2026-04-13，仅标题与导语可用） | 未获取 | ~~4~~ **0** |
| 12 | 腾讯云开发者社区：三个 Agent Harness 框架对比 | https://cloud.tencent.cn/developer/article/2674122 | 社区 | 把 OpenClaw、Hermes、OpenHuman 同归为「Agent Harness」，比进程/线程模型、记忆层数、技能生成方式 | — | 4 |
| 13 | arXiv 2606.20683 · From QA to Task Completion: A Survey on Agent System and Harness Design | https://arxiv.org/abs/2606.20683 | 权威 | **选型框架底稿**：agent 能力 = 「模型–harness 配对」属性；harness 拆为观察/上下文/控制/动作/状态/验证六项职责 | 2026-06 | **5** |
| 14 | 知乎问题：ai agent 的架构好像都差不多啊？有啥比较特别的吗？ | https://www.zhihu.com/question/1959742114519844109 | 社区 | 中文社区正面处理「同质化」（≈你的原问题）：用 LLM 接口范式、ReAct 收敛、MCP 标准化、token 成本约束解释架构趋同 | ~2025 | 4 |
| 15 | HN · Revenge of the GPT Wrappers: Defensibility in a world of commoditized AI models | https://news.ycombinator.com/item?id=42971442 | 社区 | 模型商品化后 agent 应用还剩什么护城河（135 分 / 44 评论） | 2025-02-07 | 4 |
| 16 | OpenHands software-agent-sdk Issue #3112 | https://github.com/OpenHands/software-agent-sdk/issues/3112 | 一手 | 项目自身 issue 对比「自托管 OpenHands」与「本地 CLI Claude Code」在工具集/系统提示/耗时上的边界 | 开帖日期未确认 | 4 |
| 17 | Agenta-AI/awesome-ai-agent-platforms | https://github.com/Agenta-AI/awesome-ai-agent-platforms | 一手 | 按 AI coworker / agent builder / workflow automation / browser agent / coding agent 分类，标注许可证与托管形态 —— 现成的平台分层坐标 | 持续更新 | 4 |

**未计入上表、留待 P2 取舍的媒体稿**：AlphaSignal 英文报道（2026-09-19）、腾讯云发布稿《Octop 1.0》（`cloud.tencent.cn/developer/article/2743438`）、36kr 英文稿（2026-09-17）。

---

## 2. 本地存量（第一手材料，非外部来源）

这是本次探测**最有价值的发现**：你已经写过大量 Hermes 笔记，而 OpenClaw 侧**零素材**。

| 路径 | 概要 |
|---|---|
| `workspace/hermes-agent/output/final_note.md` | 已完成笔记：Hermes 定位、安装、模型、记忆闭环、技能、多平台、部署 |
| `workspace/hermes-agent/chapters/01_定位与核心理念.md` | **已含 OpenClaw 作为竞品的定位对照段落，可直接复用** |
| `workspace/hermes-agent/research/` | 7 份官方抓取原文（GitHub README、honcho、memory-providers、messaging 等），抓取于 2026-08-27 |
| `workspace/hermes-tool-config/chapters/` | 6 章工具体系：内置工具/toolsets、Tool Gateway 审批、自定义工具、MCP 排错 |
| `workspace/hermes-home-assistant/chapters/02-三方对照轴.md` | **已有「三方对照轴」方法论，是「同层判断」的本地先例** |
| `workspace/hermes-home-assistant/output/final_note.md` | 已完成笔记：Hermes 接 Home Assistant，含三方对照轴与 MCP 落地 |
| `workspace/hermes-docker-deploy/chapters/` | 10 章部署笔记：镜像/数据卷、Gateway 常驻、微信/企微/飞书/QQ 接入 |
| `workspace/hermes-rules-config/output/final_note.md` | 已完成笔记：SOUL、AGENTS 规则体系、从 Claude Code 迁移 |
| `workspace/workflow-runs/hermes-*.workflow.md` | 6 个 hermes 相关 run，P0–P7 全部已完成 |

**关键空白**：本地**无任何 OpenClaw 专属项目或素材**，OpenClaw 仅散见于上述笔记的对比段落。

---

## 3. 对诊断假设的证据支持（来自 P0）

P0 假设是：*不是产品同质，而是使用者的场景划分尚未建立，工具先于场景落位。*

探测材料支持这个方向，并进一步给出**更强的版本**：

> ⚠️ **本表已于 P2 复核，两行原判断被推翻或降级**（详见 §3.1）。P1 当时的表述以删除线标出。

| 观察 | 支撑来源 |
|---|---|
| **OpenClaw 官方发布专页，对 Hermes 做 17 轴 source-verified 对照**（钉在 Hermes commit `6defe7eb6c`，reviewed 2026-08-27）——**同层的最强证据** | `docs.openclaw.ai/start/why-openclaw/openclaw-and-hermes-agent` |
| OpenClaw 官方称 "The recurring comparison is [Hermes Agent]" | 同上 / `research/openclaw/extra2/01_docs_openclaw_ai.md` |
| Hermes 官方**内置从 OpenClaw 迁移的命令** `hermes claw migrate` | #9 + 源码 `hermes_cli/claw.py` |
| **双向迁移**：OpenClaw 也能从 Hermes 导入记忆（`import existing local memory from Codex, Claude Code, and Hermes`） | `research/openclaw/extra/02_docs_openclaw_ai.md:26` |
| OpenClaw 与 Hermes 被第三方同归为「Agent Harness」 | #12（社区，2026-05-26） |
| ~~Hermes 侧承认竞品为 OpenClaw~~ → 修正：**双方官方都已把对方立为对照物** | 见上两行 |
| ~~社区已存在「Hermes 指挥、OpenClaw 执行」的互补用法~~ → **降级**：原 #11 抓取失败，替代源仅存标题与导语 | `community/01`（2026-04-13），**非 #11** |
| Octop 是「multiple users **and** agents」的平台，含 per-user 隔离与 harness teams | #1 #2 #5 |
| **Octop 在 OpenClaw 与 Hermes 全部已抓取官方材料中零提及**（grep 计数 0） | 双向 grep 复核 |

### 3.1 P1 被推翻/降级的两处（来源纪律修正）

| # | P1 原表述 | P2 复核结果 |
|---|---|---|
| 1 | 「Hermes 侧**无官方多用户/多租户文档**（仅 PR 与第三方封装）」 | **错误**。Hermes 官方有多用户文档（allowlist 准入、`Admins vs Regular Users` 分级、per-user profile 路由）。精确说法：**有官方多用户准入/分级，无多租户**（`tenant`/`multi-tenant`/`SaaS` 全目录 grep 零命中）。已在 `01b_thesis_verification.md` 完整记录 |
| 2 | 「社区已存在『Hermes 指挥、OpenClaw 执行』的互补用法」（来源 #11 知乎） | **降级**。#11 三路抓取全失败且未被搜索引擎索引，P1 该条**仅来自搜索摘要**。替代源仅存标题与导语可用，**不足以支撑该断言** |

### 3.2 新增高价值来源：OpenClaw 官方 17 轴对照表（**有立场，需标注**）

`docs.openclaw.ai/start/why-openclaw/openclaw-and-hermes-agent` 是本次探测的最高价值单品，且**必须按有立场来源处理**：

- **性质**：OpenClaw 单方制作，钉在 Hermes commit `6defe7eb6c`（reviewed 2026-08-27）。页面自述 "not a live adversarial test or a guarantee about every deployment"，页脚另注 "Responses are generated using AI and may contain mistakes."
- **不可当第三方中立评测使用**。表内含对 Hermes 不利内容（如引述 CVE-2026-14625 vendor non-response、v0.8.0 用户自审报告、更新器/gateway 内存泄漏 issue 编号）。
- **但轴的选择本身即证据**：两产品被放在同一组属性上逐项对照 —— 这组属性就是「同层」的操作性定义。
- **其中 `Roles and multi-user` 行直接印证主线 T′**：
  - OpenClaw：`Configured person-level role ceilings and default role; scopes and session attribution; experimental per-tenant fleet cells`
  - Hermes：`Equal trust within an adapter's authorized set; slash-command controls and separate profiles, including profile multiplexing`
  - → **两家的「多用户」确实不是一回事**，与 T′ 独立吻合。
- **尚缺 Hermes 侧的反驳或回应**（见缺口）

→ **推断（待 P2 验证）**：OpenClaw 与 Hermes 同层（单机常驻的个人助手 / harness），Octop 是另一层（多用户平台）。若成立，则「三者该选哪个」的问法本身需要先拆成两层来问。

---

## 4. 覆盖缺口

**Octop**
- 页面级/功能级 ACL 与 Token 额度模型**仅见于媒体稿**，一手文档未见对应规范
- 多用户并发下的 SQLite 写锁行为、沙箱边界缺可信一手来源

**OpenClaw / Hermes**
- Hermes 侧**无官方「多用户/多租户」文档**（仅 PR #30077/#16728 与第三方封装 hermes-tenant / multi-user-agent / Helm 一租户一 release）
- 「两者同层」**缺官方交叉表述**，目前靠第三方与迁移命令佐证
- 真实迁移/选型反馈**仅自媒体**，可信度低

**横向**
- 未找到正面处理「同质化错觉」的同行评审级研究
- 自托管平台「多用户 / 权限 / 常驻服务」边界的公开一手对比材料稀少
- 中文社区仅零散问答，无成型选型框架

---

## 5. P2 待裁决项（冲突，不得静默合并）

| # | 冲突 | 各方说法 | 处理要求 |
|---|---|---|---|
| C1 | Octop harness 核心是否开源 | 社区普遍称「harness 核心未开源」**vs** `octop-harness`/`octop-memory`/`octop-gateway` 已于 2026-09-24 公开 | 两者**时间点不同**，不得合并；P2 读仓库与 Releases 裁决 |
| C2 | 各项目 Star 数 | 自媒体口径 **6 万 ~ 24 万+**，互相矛盾；GitHub API 直读为 openclaw 390,772 / hermes-agent 249,977 | 数据严重不一致 → **标注为不可靠，不作为选型证据**（star 数本就不是好的选型依据，可在笔记中作为「反例」点出） |
| C3 | 谁做产品 / 谁做研究基础设施 | 自媒体互相矛盾 | 只采信一手仓库与官方文档表述 |

---

## 6. 环境限制（重要，影响 P2 可行性）

- **`WebFetch` 对以下域名被网络策略拦截**：`github.com`、`raw.githubusercontent.com`、`docs.openclaw.ai`、`hermes-agent.nousresearch.com`（两个代理均独立报告）
- **绕行方案已实测可用**：`crawl4ai` 环境正常（`scripts/crawl.sh --help` exit 0），且**成功抓取了被拦截域名的真实正文**（已实测抓到 Octop `docs/architecture.md` 全文）
- 因此 **P2 必须走 `.claude/skills/research-collector/scripts/crawl.sh`**，不走 `WebFetch`
- 附带影响：透镜 2 的来源 #9 / #10 的 URL 与日期来自**仓库内既有的官方抓取文件**（抓取于 2026-08-27），非本次实时抓取 —— P2 需重新抓取以确认时效

---

## 7. 方向菜单

请选一个（可组合，直接说编号）：

### A. 分层归位 + 场景决策树 —— **推荐**
**主线**：先给 agent 领域分层（本地 CLI / 个人助手 harness / 多用户平台），再给每层内部的选型依据，最后落到一棵决策树。**把你的困惑本身作为案例解剖**——为什么「感觉都一样」，以及为什么这个感觉部分是范畴错误。

- 框架底稿现成：arXiv #13 的 harness 六职责 + awesome-list #17 的平台分类
- Hermes 侧素材几乎免费（本地 6 个已完成 run + 多篇笔记）
- OpenClaw 侧需从零收集（本地零素材），Octop 侧需抓一手文档
- **成本：中**。回答的是元问题，可复用性最高

### B. 同层二选一专篇（OpenClaw vs Hermes）
只回答「我手上这两个到底该留哪个」。含逐轴对照（记忆/技能/通道/隔离）、迁移路径（`hermes claw migrate` 实测）、以及第三方提出的「互补用法」是否成立。
- **成本：低–中**。但结论可能偏向「差别不大，看你更在意哪根轴」

### C. Octop 单平台深挖
Octop 是唯一没接触过的，且**它的文档最完整**（五层架构 + ADR + 三个独立库 + 插件契约 + harness teams）。写成「Octop 是什么、它的多用户/多 agent 到底怎么实现、值不值得引入」。
- **成本：中**。一手文档齐全且 crawl 可抓

### D. 企业多人场景专篇
从你「用于一些企业工作」这个**真实需求**出发，直接回答「企业多人用 agent 该选什么」：Octop vs OpenClaw 多租户配置 vs 第三方封装，含权限/数据隔离/运维成本。
- **成本：中–高**，但最贴你的实际痛点

> **我的建议**：选 **A**，并把 B / C 作为 A 内部的两章 —— 这样既回答了「怎么选」，又不丢「具体这两个怎么选」和「Octop 到底行不行」的落地答案。若你更在意马上能用上的结论，选 **D**。

---

## 8. P2 预估规模

| 方案 | 核心来源数 | 预计章节 | 主要风险 |
|---|---|---|---|
| A | 8–10 | 6–8 | OpenClaw 一手素材需从零抓，且其文档深度未知 |
| B | 5–6 | 4–5 | 结论可能「差别不大」，需靠具体轴撑住价值 |
| C | 6–7 | 5–6 | Octop 较新，第三方实践反馈几乎为零 |
| D | 8–12 | 6–8 | 企业场景的一手权限/隔离证据最稀缺（§4 缺口） |
