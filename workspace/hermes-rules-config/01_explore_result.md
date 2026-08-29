# Hermes 规则配置 - 阶段 1 探测结果

> 主题：Hermes 的规则配置（rules / CLAUDE.md 这类如何配置）
> 运行：hermes-rules-config · P1 探测式收集
> 日期：2026-08-30

## 一、探测透镜与结论摘要

三个独立视角并行探测（每个 5 条候选，去重后 10 条唯一来源，**全部为官方文档 tier 1**）：

### Lens A · 规则/指令文件体系

Hermes 有**两层指令载体**，职责分明：

1. **全局身份文件 `SOUL.md`**：位于 `~/.hermes/SOUL.md`（或 `$HERMES_HOME/SOUL.md`），作为系统提示 **slot #1** 注入，缺省自动 seed、永不被覆盖、**只从 HERMES_HOME 读取，不从工作目录探测** —— 即"身份全局跟随，不可按项目改变"。
2. **项目级上下文文件（Context Files）**：从工作目录按**优先级链**发现，`先匹配优先（first-match-wins）`：
   `.hermes.md`/`HERMES.md`（沿 git root 上溯）→ `AGENTS.override.md`（个人、gitignored，替代 AGENTS.md）→ `AGENTS.md` → `CLAUDE.md` → `.cursorrules`。并支持**目录链渐进发现**（git root → CWD）。

### Lens B · 分层加载与作用域

- 配置优先级：**CLI 参数 > `config.yaml` > `.env` > 内置默认**。
- **Managed Scope**：管理员可在 `/etc/hermes/{config.yaml,.env}`（`HERMES_MANAGED_DIR` 可重定位）钉住键值，**压过用户配置与环境变量**（叶级合并）。
- **Profiles**：`~/.hermes/profiles/<name>/` 每个 profile 有独立 config.yaml/.env/SOUL.md/skills/memories/sessions，通过 `HERMES_HOME` 切换 —— "全局 vs 本地"主要按 **profile 实例** 而非项目解析。
- 项目上下文文件是唯一**工作目录作用域**的输入。

### Lens C · 与 Claude Code 对照 + 验证

| Claude Code | Hermes Agent 对应 |
| --- | --- |
| `CLAUDE.md`（记忆/指令） | `SOUL.md`（持久身份）+ 项目上下文文件 `.hermes.md`/`AGENTS.md`/`CLAUDE.md` |
| `.claude/rules/`（分层规则） | 项目上下文文件优先级链 + `platform_hints` |
| `settings.json`（权限/hooks/env） | `~/.hermes/config.yaml`（含 `hooks:` 块、`command_allowlist`）+ `~/.hermes/.env` |
| hooks（生命周期 shell） | config.yaml 的 shell hooks + plugin/gateway/webhook；`hermes hooks list/test/doctor` |
| 迁移工具 | **`hermes import-agent claude-code`**（自动转 `~/.claude` → Hermes） |

**验证/排错命令**：`hermes doctor [--fix]`、`hermes config check`/`migrate`、`hermes config get KEY --json`、`hermes status`、`hermes prompt-size`（离线查看组装后的系统提示字节构成，最接近"检查已加载的规则"）、`hermes hooks list/test/revoke/doctor`；隔离开关 `--ignore-rules` / `--ignore-user-config` / `--safe-mode`。

---

## 二、候选来源清单（去重后）

| # | 来源 | Tier | 覆盖 |
| --- | --- | --- | --- |
| S1 | [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality) | 官方 | SOUL.md 机制、14 内置预设、personality 覆盖层 |
| S2 | [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) | 官方 | 项目规则文件优先级链、目录链、SOUL.md vs AGENTS.md 分工 |
| S3 | [Prompt Assembly（开发指南）](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly) | 官方 | 10 层系统提示组装顺序、规则注入位置、缓存 |
| S4 | [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) | 官方 | config.yaml/.env 分层、`hermes config set/get/check`、HERMES_HOME 布局 |
| S5 | [Managed Scope](https://hermes-agent.nousresearch.com/docs/user-guide/managed-scope) | 官方 | 管理员全局覆盖层 `/etc/hermes`、叶级合并 |
| S6 | [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) | 官方 | 多 agent 实例、per-profile 配置/SOUL.md |
| S7 | [CLI Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md) | 官方 | `hermes config` / `doctor` / `prompt-size` / `hooks` 等验证命令 |
| S8 | [Event Hooks](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/hooks.md) | 官方 | hooks 四类系统、`pre_tool_call` 阻塞/改写、Claude-Code 兼容响应 |
| S9 | [Import from other agents](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/import-from-other-agents.md) | 官方 | `hermes import-agent claude-code` 映射表 |
| S10 | [Use SOUL.md with Hermes](https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes) | 官方 | SOUL.md 结构建议（Identity/Style/Avoid/Defaults）、第三方 persona 映射 |

> 注：docs 站点在探测环境中偶发抓取受限，Lens B/C 通过 GitHub raw 源（`website/docs/`）交叉验证，内容一致。版本锚定 v0.20.x。

---

## 三、方向菜单（请选择 P2 深度收集聚焦点）

- **A. 规则文件体系全解**：SOUL.md + 项目上下文文件（.hermes.md/AGENTS.md/CLAUDE.md）+ profiles —— 纯 Hermes 视角，讲清"有哪些入口、各自职责、怎么落地"。
- **B. Claude Code → Hermes 对照迁移**：以你熟悉的 CLAUDE.md/.claude/rules/settings.json/hooks 为锚，逐项映射 + `hermes import-agent claude-code` 实战迁移。
- **C. 分层加载机制深入**：优先级链、git-root→CWD、Managed Scope、Profiles 作用域、platform_hints —— 理解"规则为什么这样生效"。
- **D. 实战配置 + 验证闭环**：从零配一套规则（SOUL.md + AGENTS.md + hooks + 权限），用 `hermes doctor` / `config check` / `prompt-size` 验证生效。

> 推荐组合：**B + D**（对照迁移 + 实战验证）最贴合你"用过 Claude Code、上手、实战配置指南"的目标。

---

## 四、覆盖缺口

- **社区实操经验**：当前候选全为官方文档；若有"配置不生效"的真实排错案例，P2 可补充 1-2 条社区来源。
- **hooks 具体配置示例**：S8 覆盖机制，但"具体 hooks 写进 config.yaml 的格式"需 P2 深挖。
- **import-agent 迁移边界**：S9 有映射表，但"迁移后需手工修什么"（如 SOUL.md 措辞、platform_hints）待 P2 验证。

## 五、P2 预估范围

- 核心深读 3-5 篇：S1、S2、S3、S7、S9（按所选方向调整）。
- 产出 `02_deep_research.md`：范围、来源表、claim/source 映射、矛盾点、实践指导、开放问题、下游交接。
- 预计全官方来源为主，必要时补 1-2 条社区实操。
