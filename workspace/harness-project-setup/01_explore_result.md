# 探测式收集结果 - 从零搭建 Agent Harness 工程

> 运行：harness-project-setup | 阶段：P1 探测式收集 | 日期：2026-08-16

## 一、探测视角与候选资料

### 视角 A：Claude Code 官方工程结构（3 个 subagent 并行产出）

| # | 标题 | URL | 层级 | 相关度 | 评分 |
|---|------|-----|------|--------|------|
| A1 | Memory — CLAUDE.md / AGENTS.md / rules 官方规范 | https://code.claude.com/docs/en/memory | 1 | 官方规范加载层级、@AGENTS.md 桥接、.claude/rules/ 按需加载 | 5 |
| A2 | Skills — SKILL.md 格式与 .claude/skills | https://code.claude.com/docs/en/skills | 1 | SKILL.md frontmatter、allowed-tools、按需加载 | 5 |
| A3 | Hooks reference — 生命周期与 settings.json 注册 | https://code.claude.com/docs/en/hooks | 1 | PreToolUse/PostToolUse/Stop/SessionStart 生命周期 | 5 |
| A4 | Create custom subagents — .claude/agents | https://code.claude.com/docs/en/sub-agents | 1 | 子代理 frontmatter 规范 + 内置代理清单 | 5 |
| A5 | Set up Claude Code in monorepo/large codebase | https://code.claude.com/docs/en/large-codebases | 1 | per-directory CLAUDE.md、.claude/skills、rules 落位 | 5 |

### 视角 B：DeepSeek-Harness 配置结构与 Claude Code 对照

| # | 标题 | URL | 层级 | 相关度 | 评分 |
|---|------|-----|------|--------|------|
| B1 | DeepSeek-Harness 官方 AGENTS.md（仓库总纲） | https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/AGENTS.md | 1 | "一切皆插件"、cordis.yml 配置层、.agents/ ↔ .claude/ | 5 |
| B2 | dsh skills 子系统文档 | https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/docs/subsystems/skills.md | 1 | 六个扫描根 + SKILL.md 契约 + 热加载 | 5 |
| B3 | dsh config-catalog（cordis.yml 可配键全表） | https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/docs/config-catalog.md | 1 | workspaceContext、hooks 桥接、mcp-client、presets | 4 |
| B4 | learn-dsh —— 中文 22 课拆解（与 Claude Code 对照） | https://github.com/onychen/learn-dsh | 3 | 中文教学、Profile/Bundle 组装、hook 拦截 | 4 |
| B5 | 你的笔记《03-配置实战-接入skills-hooks-mcp-rules》 | `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness 插件开发教程/03-配置实战-接入skills-hooks-mcp-rules.md` | 2 | 你已整理的 Claude Code→dsh 文件级迁移清单 | 5 |

### 视角 C：社区实战模板与最佳实践

| # | 标题 | URL | 层级 | 相关度 | 评分 |
|---|------|-----|------|--------|------|
| C1 | coleam00/harness-engineering-demo（最小可运行脚手架） | https://github.com/coleam00/harness-engineering-demo | 3 | .claude/skills + hooks + subagent + settings.json 骨架 | 5 |
| C2 | WxqKb/cow-harness（中文可迁移 harness 模板） | https://github.com/WxqKb/cow-harness | 3 | 多项目模板、.ai-harness 档案、Claude/Codex/Cursor 适配 | 5 |
| C3 | IgniteUI/ai-repo-structure（AGENTS.md 优先仓库范例） | https://github.com/IgniteUI/ai-repo-structure | 3 | AGENTS.md/.claude/.github 分层 + adopt-this-repo 技能 | 4 |
| C4 | HumanLayer — Skill Issue: Harness Engineering | https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents | 2 | SKILL.md 目录树、Stop hook 脚本、渐进式配置 | 4 |

### 视角 D：本地活体范本（本 vault 自身，实测）

| 组件 | 位置 | 说明 |
|------|------|------|
| 跨 runtime 指令源 | `AGENTS.md` + `CLAUDE.md` | AGENTS.md 为 canonical source，声明双套配置隔离与同步 |
| Skills | `.claude/skills/{name}/SKILL.md` + `manifest.yaml` | 20+ 技能，每技能入口 SKILL.md |
| Rules | `.claude/rules/{common,obsidian}/` | 分层规则（skill-invocation/agent-invocation/env/prompt-cache/note-system...） |
| Agents | `.claude/agents/{name}.md` + `manifest.yaml` | chapter-writer/note-assembler/outline-generator |
| Hooks | `.claude/hooks/*.py` + `.claude/settings.json` | 注册 SessionStart/Stop/SessionEnd 三个 hook |
| Workflows | `.claude/workflows/{id}/workflow.md` + `routing.yaml` | 3 个命名工作流，state file 在 `workspace/workflow-runs/` |
| 跨 runtime 同步 | `.codex/` + `.agent-sync/` | 镜像 + 校验脚本（sync_agents.py/bootstrap.py） |

## 二、方向菜单（请选择）

| 选项 | 方向 | 说明 | 推荐度 |
|------|------|------|--------|
| **A** | 官方规范 + 本地范本综合实战 | 以 Claude Code 官方文档（A1-A5）为权威基线，以本 vault（视角 D）为活体范本，产出"先建哪些文件 + 每个文件怎么填"的完整骨架 | ⭐ 推荐 |
| **B** | 模板复制适配 | 直接用社区模板（C1/C2/C3）复制最小可运行骨架再改造，最快落地 | |
| **C** | 跨 runtime 对照（Claude Code ↔ DeepSeek-Harness） | 以 B 组官方文档 + 你的 B5 笔记为轴，搞懂同一套 harness 配置在每个 runtime 的等价位置，通用性最强 | |
| **D** | A+B+C 三合一大全 | 最完整，产出规模最大 | |

## 三、覆盖缺口与 P2 预计范围

**已知缺口**：
- 官方各文档 URL 稳定但无发布日期（持续更新文档），P2 抓取时标注"访问日期 2026-08-16"。
- learn-dsh（B4）是简化 Python 教学实现，非真实 TS+Cordis dsh，引用时需标注。
- 模板类仓库（C1/C2/C3）无明确版本/日期，P2 需抓取实际目录树核对结构是否过时。
- 未纳入：LangChain《Anatomy of an Agent Harness》（概念清单、无脚手架）、brandonavant guide（分步指南为主）——与本笔记"复制即用"目标不符。

**P2 预计范围**：3-5 个核心源深抓（A1-A5 官方文档为主，按所选方向增补），产出骨架目录树、各文件关键内容样例、常见坑清单。

---

*候选记录由 3 个并行探测 agent 产出，全部 URL 已验证可达；本地范本为实测结构。*
