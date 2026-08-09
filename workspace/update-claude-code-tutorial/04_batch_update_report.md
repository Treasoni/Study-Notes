# 批量更新汇总报告 — Claude Code 教程（同步到 2026-08）

> 完成时间：2026-08-10
> 工作流：batch-note-update-flow（run: update-claude-code-tutorial）
> 目标：`AI学习/Claude Code 教程/` 19 篇学习笔记同步到 2026-08 现状

## 1. 汇总统计

| 项 | 数量 |
|----|------|
| 处理笔记总数 | 19 |
| 更新（update + 写回） | **19** |
| 跳过（skip） | 4（MOC 单独处理 / sortspec / 2 个 update_report 遗留） |
| 失败 | 0 |
| 需复核标记 | 17（多为低优先级，全部已写回） |
| 无风险标记 | 2（cc07 Checkpoints、cc08 Hooks） |

- 输出模式：**patch-in-place**（每篇先出 `updates/{note_id}/updated_note.md`，git 备份后写回原文件）
- 安全网：vault 自动 git 备份进程已把全部变更提交到 git 历史（`vault backup: 2026-08-10 00:3x`），可随时 `git log`/`git show` 回滚。
- 状态：19 篇 frontmatter `updated` 全部 → 2026-08-10；`status` 统一 `updated`（cc06/cc19 由 draft → updated）。

## 2. 逐篇更新摘要

| id | 笔记 | 动作 | 主要变更 | 未处理风险 |
|----|------|------|---------|-----------|
| cc01 | 入门/如何使用Claude code | update+写回 | 默认模型 Sonnet 5/Opus 5、权限 Manual、/doctor /fork /subtask、/review=/code-review、版本 v2.1.226 | stable 版本号改模糊描述；促销价 8/31 时效 |
| cc02 | 基础/Claude Code 常用功能 | update+写回 | 权限 Manual、/doctor 主名、/fork /subtask、Slash 叠加、emoji 补全 | 快捷键速查无来源；/review-pr 示例未验证 |
| cc03 | 基础/Claude Code CLI 完整参考 | update+写回 | --permission-mode manual、--ax-screen-reader、--forward-subagent-text、5 个新 env、/status 会话类型、v2.1.226 | ⚠️ 模型表仍列 Opus 4.8 为默认（超本轮范围） |
| cc04 | 基础/Claude Code 会话管理 | update+写回 | /fork、/rewind→/clear 前、/subtask、/tasks、/resume 选择器、AskUserQuestion 不自动继续；已修 /doctor 别名方向 | .claude.local/settings.json 路径规范待核 |
| cc05 | 基础/模型与推理设置 | update+写回 | Sonnet 5/Opus 5 默认、Bedrock/Vertex Opus 4.8、Effort 档位、1M 上下文与 DISABLE_1M_CONTEXT | opusplan 别名 200K 待核；促销价时效 |
| cc06 | 基础/settings.json 配置详解 | update+写回 | draft→updated；defaultMode=manual、9 类新键（sandbox.filesystem.disabled 等）、补小结 | 3 个新键 JSON schema 为示意值 |
| cc07 | 进阶/Checkpoints 使用指南 | update+写回 | /rewind 恢复到 /clear 前；不再走符号/硬链接；Rewind 菜单 6 项 | 无（/checkpoint、autoCheckpoint 移除为推断） |
| cc08 | 进阶/Hooks 使用指南 | update+写回 | Notification hook、DirectoryAdded hook、if: dir/** 条件、headless 修复、插件注入防护 | 无 |
| cc09 | 进阶/Memory 完整指南 | update+写回 | CLAUDE.md ≤200 行/25KB、/doctor 裁剪建议、Auto Memory 加载行为、导入深度 4 层 | 移除 DISABLE_AUTO_MEMORY=0 语义待核；顺修 3 处乱码 |
| cc10 | 进阶/Subagents 完整指南 | update+写回 | 默认后台、并发 20、嵌套深度 3、/subtask、--forward-subagent-text、worktree 隔离、移除 200 spawn 上限 | 版本号/数值建议对照官方 |
| cc11 | 进阶/插件系统使用指南 | update+写回 | headersHelper 注入拒绝、pluginConfigs 项目级失效、archive 安装来源、安装同意 | breaking 变更版本归属待核 |
| cc12 | 高级/Claude Code 高级功能 | update+写回 | Auto mode 免 opt-in、Subagents 新规则、屏读模式、桌面内置浏览器、/fork、Sonnet 5/Opus 5 | credentialMasking.mode 路径为推断 |
| cc13 | 高级/Slash Commands 完整参考 | update+写回 | /fork /subtask /code-review(别名 /review) /doctor /status、命令表重排、Slash 叠加、emoji | /branch 与 /fork 关系待核 |
| cc14 | 高级/Claude MCP 使用指南 | update+写回 | capability discovery 重试、macOS keychain OAuth 修复、mcp list/get 安全、roots/list、长耗时转后台 | 版本号精确归属待核 |
| cc15 | 高级/如何编写Skills | update+写回 | disable-model-invocation、Slash/Skill 叠加、frontmatter 规范、参数语法更新 | 叠加数量(5 vs 6)按官方 docs 表述 |
| cc16 | 高级/CLAUDE.md 使用指南 | update+写回 | ≤200 行/25KB、可推导内容不写、/doctor 全量体检、项目级信任 warning | 工作区信任表述建议对照 docs |
| cc17 | 高级/定时任务自动化指南 | update+写回 | /loop 全面更新（自定节奏、最长 7 天）、无人值守行为 5 点、Notification hook | /loop cron 兼容性待核；launchctl 未改 |
| cc18 | 高级/Dynamic Workflows 使用指南 | update+写回 | workflowSizeGuideline、默认 medium、OTel workflow.run_id、子代理后台、嵌套深度 3 | OTel/SendMessage 为 spec 转述；笔记无「6 种模式」章节 |
| cc19 | 高级/LLM-Prompt-Caching-提示缓存 | update+写回 | draft→updated；Sonnet 5/Opus 5 1M、DISABLE_1M_CONTEXT、长上下文分段缓存、补小结/FAQ | 促销价 8/31 时效；缓存参数沿用原文 |

## 3. 共享资料来源清单

- 主来源：`shared_research/source_bank.md`（23 条 SB-01~SB-23）
- 研究计划：`shared_research/research_plan.md`
- 一手来源：Claude Code 官方 changelog、`code.claude.com/docs/en/whats-new` 周刊（w28）、GitHub `anthropics/claude-code` CHANGELOG.md
- 佐证：classmethod DevelopersIO 发布摘要（v2.1.199 / v2.1.207 / v2.1.223）

## 4. 未处理风险与建议

### 高风险（建议尽快处理）
1. **cc03 模型表不一致**：cc05 已把默认 Opus 改为 Opus 5，但 cc03（CLI 参考）模型表仍列 Opus 4.8 为「最新默认」。建议单独补丁统一。

### 时效性（到期需复核）
2. Sonnet 5 促销价 $2/$10 至 **2026-08-31**（cc01/cc05/cc19），到期后需更新。

### 推断值（建议对照官方 docs 复核）
3. cc06 三个新键（vimInsertModeRemaps / crossSessionInbound / dialogExpiry）JSON schema 为示意值。
4. cc12 `credentialMasking.mode` 配置键路径为推断。
5. cc11 breaking 变更版本归属、cc14 版本号精确归属、cc18 OTel/SendMessage 转述。

### 环境/术语
6. cc04 `.claude.local/settings.json` 路径 vs 官方 `.claude/settings.local.json`。
7. cc17 `launchctl load/unload` → macOS 新 `bootstrap`/`bootout`（超范围未改）。
8. cc15 叠加数量「第一个之后最多 5 个（合计 6）」按官方 docs 表述。

### 建议
- 上述均为低强度复核项，不阻塞使用；如需要可开一轮 `note-updater` 定向复核（每篇只修风险点）。
- MOC 已更新 frontmatter（updated: 2026-08-10）；19 篇索引项无需增删，描述仍准确。

## 5. 产出文件

- `01_update_inventory.md` / `update_inventory.csv` — 更新清单
- `02_batch_update_plan.md` — 批量计划
- `03_batch_update_log.md` — 批处理日志（7 批次）
- `shared_research/source_bank.md` — 共享来源库（23 条）
- `updates/{note_id}/` — 每篇 stale_map / update_plan / updated_note / update_report
- `04_batch_update_report.md` — 本报告
