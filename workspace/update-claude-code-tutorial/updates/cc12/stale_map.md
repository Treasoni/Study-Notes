# Stale Map — cc12 「Claude Code 高级功能」

> note_id: cc12
> 更新目标：2026-08 现状
> 来源库适用条目：SB-01、SB-02、SB-03、SB-05、SB-06、SB-07、SB-14、SB-15
> 补充条目（核对「其它过时点」时引用）：SB-04、SB-08、SB-13

## 保留（Keep）

| 区块 | 理由 |
|------|------|
| Planning Mode 全节 | 内容与 2026-08 现状一致，无冲突 |
| Extended Thinking 激活方式 / 查看推理 / 实际示例 | 未过时，仅「模型支持」子节需更新 |
| Background Tasks 全节 | 与当前 docs 一致 |
| Scheduled Tasks 全节（/loop、cron 限制、禁用） | 与当前 docs 一致 |
| Dynamic Workflows 全节 | 与当前 docs 一致（2026-05-28 GA 等） |
| Headless Mode 全节 | 与当前 docs 一致 |
| Interactive Features（快捷键、Vim、Bash 模式） | 未过时 |
| Voice Dictation 全节 | 未过时 |
| Computer Use 全节 | 研究预览描述仍适用 |
| Artifacts 全节 | 未过时 |
| Remote Control 全节 | 未过时 |
| Git Worktrees 全节 | 未过时（Worktree 隔离的安全细节并入新增 Subagents 节） |
| Managed Settings 全节 | 未过时 |
| Checkpoints & Rewind 全节 | 未过时 |
| Plugins 全节 | 未过时 |
| 完整目录结构示例 / 相关文档 / 参考资料 | 未过时 |

## 更新（Update）

| 位置 | 过时点 | 依据 |
|------|--------|------|
| frontmatter | `updated: 2026-07-12` → `2026-08-10`；`status` 保持 `updated` | 任务要求 |
| Mermaid 图 | 缺 Accessibility 节点 | SB-15 |
| Extended Thinking · 模型支持表 | 缺 Opus 5；Sonnet 5 未标注为默认；未提默认模型事实 | SB-01、SB-02 |
| Configuration · 环境变量 | `ANTHROPIC_MODEL=claude-opus-4-8`、`ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-8` 已过时 | SB-01、SB-02 |
| Auto Mode · 正式发布 callout | 「2026 年 7 月起已支持 Bedrock/Vertex/Foundry」未提免 opt-in | SB-03 |
| Auto Mode · 默认阻止操作表 | 缺 transcript 篡改、命令替换灾难性删除保护 | SB-14 |
| Auto Mode | 缺 AskUserQuestion 默认不再自动继续 | SB-14 |
| Desktop App · 核心功能表 | 缺桌面端内置浏览器 | SB-14 |
| Sandboxing · 配置示例 | 缺 `sandbox.filesystem.disabled`、凭据 `mode: "mask"` | SB-13（+SB-12 转述） |
| Permission Modes 表 / 使用场景表 / 最佳实践 / 完整配置示例 | `default` 权限模式已改名 `manual` | SB-04（补充核对） |

## 新增（Add）

| 位置 | 新增内容 | 依据 |
|------|----------|------|
| Scheduled Tasks 之后 | 新增「Session Management（会话管理）」节：`/fork` | SB-08 |
| Dynamic Workflows 之后 | 新增「Subagents（子代理）」节：默认后台、并发 20、嵌套 3、`/subtask`、`--forward-subagent-text`、worktree 隔离安全 | SB-06、SB-07、SB-05 |
| Voice Dictation 之后 | 新增「无障碍（Screen Reader）」节 | SB-15 |
| 文末 | 追加「## 更新记录」 | 任务要求 |

## 删除（Delete）

无整段删除。仅部分表格内旧值被替换（见更新列），不改动结构。

## 备注 / 风险

- Permission Modes `default→manual` 依据 SB-04（该条目不在任务给定的适用清单内，但属于「核对其它过时点一并修正」的明确过时点，故一并处理并单独标注）。
- Auto Mode 的 `--enable-auto-mode` 启动方式保留（来源库未显示其被移除），仅更新 callout 说明第三方平台免 opt-in。
