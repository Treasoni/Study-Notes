# 如何使用 Matt Pocock Skills - 探测结果（P1）

> 收集时间: 2026-08-01
> 阶段: 阶段 1 探测式收集
> 说明: 方向已在 00_intent.md 中确认（5 个方向），本文件记录探测到的实际可获取信源与候选资料。

---

## 一、方向候选资料

### 方向 1：安装与接入

**探测发现**：Matt Pocock Skills 有**两种互斥安装方式**，本质是「可编辑副本 vs 只读自动更新」：

| 方式 | 命令/操作 | 特点 |
|------|-----------|------|
| npx 安装器 | `npx skills@latest add mattpocock/skills` | 可编辑普通文件写入仓库；`npx skills update` 拉取更新 |
| Plugin 市场 | `/plugin install` 或 `claude plugins install mattpocock-skills` | 只读、自动更新 |

- 装完后每仓库跑一次 `/setup-matt-pocock-skills`，配置 issue tracker（GitHub/Linear/本地）、标签、文档保存位置。
- 两种方式**二选一**，否则技能重复。
- Plugin 路线分发 22 个 skill（plugin.json v1.2.0）：engineering 17 + productivity 5。

### 方向 2：调用与触发

**探测发现**：核心 skill 的触发方式已确认：

| Skill | 触发 | 作用 |
|-------|------|------|
| `/ask-matt` | user | 路由器，推荐最合适的 skill/flow |
| `/implement` | user | 基于 spec/tickets 实现，内部驱动 `/tdd` → `/code-review` → commit |
| `/grill-with-docs` | user | 有状态盘问，副产品产出 ADR + 词汇表 |
| `/grilling` | model | 核心盘问原语，触发词如 "grill me" |
| `/handoff` | user | 压缩会话为交接文档，写入系统临时目录 |

- 调用边界：user-invoked 可调用 model-invoked，**不可调用另一个 user-invoked**。

### 方向 3：配置与定制

**探测发现**：
- `CLAUDE.md`：结构/发布规范（plugin.json 与 package.json 版本同步、`claude plugin validate`、`link-skills.sh` 符号链接）。
- `CONTEXT.md`：项目术语词汇表，由 `/grill-with-docs`、`/domain-modeling` 更新。
- 装后需按仓库配置 `/setup-matt-pocock-skills`（issue tracker、标签、文档路径）。

### 方向 4：工作流实战

**探测发现**：ask-matt 主流程（idea → ship）：
1. `/grill-with-docs` 盘问打磨
2. 需要原型 → `/handoff` → `/prototype` → `/handoff` 返回
3. 多会话 → `/to-spec` → `/to-tickets` → 每 ticket 一次 `/implement`；单会话直接 `/implement`
4. `/implement` 内部 `/tdd` → `/code-review` → commit
- 步骤 1-3 须在同一上下文窗口内；临近上限用 `/handoff` 后开新会话。

### 方向 5：常见问题与排错

**探测发现**：
- 最常踩的坑：grill 类技能「话痨」（简单问题触发长访谈）→ 社区建议 grill 改 opt-in、直接告诉 agent "我时间不够"。
- 模型差异大（如 Opus 4.6 正常 / 4.7 表现差）。
- skills.sh CLI 只能装最新版，无法回退旧版，需手动复制。
- Skill vs Plugin 混淆：Skill 是能力模块（跨 Claude.ai/API/Code），Plugin 是分发容器（仅 Claude Code）。

---

## 二、候选资料清单（粗筛）

| # | 标题 | URL | 评分 | 来源类型 |
|---|------|-----|------|---------|
| 1 | mattpocock/skills README | https://github.com/mattpocock/skills | 5/5 | 官方文档 |
| 2 | Discover and install prebuilt plugins | https://code.claude.com/docs/en/discover-plugins | 5/5 | 官方文档 |
| 3 | Create and distribute a plugin marketplace | https://code.claude.com/docs/en/plugin-marketplaces | 4/5 | 官方文档 |
| 4 | 一行命令即可安装 19 个 Claude Code Skill（腾讯云） | https://cloud.tencent.com.cn/developer/article/2697381 | 4/5 | 技术博客 |
| 5 | I Tried the Claude Code Skills Repo（dev.to） | https://dev.to/evan-dong/i-tried-the-claude-code-skills-repo-that-got-77k-stars-here-is-what-works-and-what-does-not-57a4 | 4/5 | 技术博客 |
| 6 | improve-codebase-architecture 被 grill-me 改坏（Issue #274） | https://github.com/mattpocock/skills/issues/274 | 5/5 | 社区讨论 |
| 7 | Skills vs Plugins（claude-code-extensions） | https://github.com/johnlarkin1/claude-code-extensions/blob/main/claude-docs/skills-vs-plugins.md | 5/5 | 技术博客 |
| 8 | Claude Code Skills vs MCP vs Plugins: Complete Guide | https://www.morphllm.com/claude-code-skills-mcp-plugins | 4/5 | 技术博客 |

---

## 三、下一步

- 方向菜单已确认（5 个方向，与意图文件一致）。
- 深度收集（P2）将精读评分 ≥4 的候选资料 + 拉取仓库原始 SKILL.md 文件作为使用示例。
