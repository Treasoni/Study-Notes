# Design: Gitignore 与 README 清理

## 修复方案

### 1. `.gitignore` 更新

排除以下开发流程文件：

| 排除项 | 原因 |
|--------|------|
| `openspec/changes/` (非 archive) | 进行中的 change 提案，开发过程产物 |
| `openspec/changes/archive/` | 已归档的 change，开发历史 |
| `.comet.yaml` | Comet 状态文件，会话级产物 |
| `.codegraph/` | CodeGraph 自动生成的索引数据库 |
| `docs/superpowers/` | 开发流程产生的 plans/specs/reports |
| `package-lock.json` | 锁文件，已在 gitignore 中 |
| `.claude/settings.local.json` | 本地权限配置，已在 gitignore 中 |
| `*.log` | 日志文件 |
| `.comet/` | Comet 运行时目录 |

保留以下核心文件：
- `CLAUDE.md`、`.study-config.yaml`、`.obsidian-config.md` — 配置
- `.claude/skills/`（核心 skill）— 系统定义
- `.claude/agents/` — 子代理定义
- `templates/` — 笔记模板
- `docs/`（核心文档）— 工作流文档
- `.learnings/RULES.md` — 自我学习规则
- `scripts/` — 验证脚本

### 2. `README.md` 重写

新结构：
1. **项目简介** — 一句话说明 + 核心特性
2. **快速开始** — 3 步上手（clone → 配置 → 使用）
3. **工作流程** — 研究驱动型 + 心得笔记型
4. **笔记类型** — 5 种单一类型 + 混合类型
5. **自治级别** — Level 0-3 表格
6. **目录结构** — 精简的 Vault 内目录树
7. **核心 Skill** — 表格列出关键 skill
8. **设计原则** — 简要列出
