# Stale Map — cc02（Claude Code 常用功能）

> 分析日期：2026-08-10
> 基线：`shared_research/source_bank.md` 适用条目 SB-04 / SB-08 / SB-09 / SB-10 / SB-11 / SB-12
> 策略：局部 patch，保留原结构、写作风格与未过时内容，不重写整篇。

## 保留（Keep）

| 区块 / 条目 | 原因 |
|-------------|------|
| CLI 启动模式（交互 / 单次 / 打印） | 启动参数未过时 |
| 快捷键速查全表 | source_bank 无快捷键变更来源，未发现过时项 |
| 功能特性总览（功能对比表 / 使用场景组合） | 功能集合仍成立 |
| 文件操作（Read / Edit / Write） | 工具名未变 |
| 代码搜索（Glob / Grep） | 未变 |
| Git 集成（`/commit`） | 未变 |
| Checkpoint/Rewind 机制（含限制、三种模式、vs Git） | 核心概念未变（SB-22 边界行为不改变本文描述） |
| Extended Thinking | 未变 |
| CLAUDE.md 记忆文件层级 | 未变 |
| 操作步骤 / 常见问题 / 概念辨析 / 最佳实践 | 未过时 |
| 参考资料 / 相关文档 / 安装快速参考 | 链接与仓库结构不在本次更新范围 |

## 更新（Update）

| 位置 | 现状 | 更新为 | 依据 |
|------|------|--------|------|
| frontmatter `updated` | 2026-07-12 | 2026-08-10 | 更新任务要求 |
| frontmatter `tags` | `[claude, ai, 工具使用, claude-code]` | `["claude", "ai", "工具使用", "claude-code"]`（元素加双引号） | YAML 特殊字符规范 |
| CLI 启动参数块 | 无权限模式示例 | 增加 `claude --permission-mode manual` | SB-04 |
| CLI 段（新增 tip） | 无权限模式说明 | 增加「权限模式（大白话）」tip：Default→Manual、`--permission-mode manual`、`"defaultMode": "manual"` | SB-04 |
| 系统与监控表 `/checkup` | 「/checkup 系统诊断（/doctor 别名）」 | 「/doctor 全量环境体检（/checkup 为别名）」 | SB-10 |
| 代码与 Git 表 `/review` | 「审查当前代码变更」 | 「/code-review 的别名，不会自动运行，需手动调用」 | SB-09 |
| 高级功能表 `/code-review` | 「报告正确性错误，--fix 直接修复」 | 注明「作为后台子代理运行，需手动触发」 | SB-09 |
| 高级功能表 `/checkup`（重复行） | 「自诊断与优化」 | 删除，主名合并到 `/doctor` | SB-10 |

## 删除（Delete）

| 位置 | 原因 |
|------|------|
| 高级功能表中重复的 `/checkup` 行 | 与系统监控表 `/doctor` 重复；主名已改为 `/doctor` |

## 新增（Add）

| 位置 | 内容 | 依据 |
|------|------|------|
| Slash 命令速查段首 | tip「新交互细节」：Slash/Skill 叠加（最多 5 个前置）、emoji 短码补全（`:thumbsup:`）、`/status` 显示会话类型 | SB-11、SB-12、SB-10 |
| 高级功能表 | `/fork`（把当前对话复制到新后台会话） | SB-08 |
| 高级功能表 | `/subtask`（在会话内启动子代理） | SB-08 |
| 文末 | `## 更新记录`（2026-08-10 变更摘要） | 更新任务要求 |

## 未改动（明确排除）

- 快捷键速查：无变更来源，全部保留。
- `/review-pr`：非内置命令示例，无来源判定其过时，保留。
- 安装快速参考：基于 claude-howto 仓库结构，不在本次范围。
- Checkpoint 持久化「30 天清理」、上下文「200K~1M tokens」描述：与 SB 不冲突，保留。
