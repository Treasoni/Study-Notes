# cc05 过时点映射（Stale Map）

- **note_id**: cc05
- **笔记**: `AI学习/Claude Code 教程/02-基础功能/Claude Code 模型与推理设置.md`
- **更新日期**: 2026-08-10
- **更新目标**: 同步到 2026-08 模型现状（默认 Sonnet 5 / Opus 5、第三方平台 Opus 4.8 + Auto mode 免 opt-in、1M 上下文、Effort 档位标注）

## 依据条目

| 来源 | 内容 |
|------|------|
| SB-01 | Sonnet 5 成为 Claude Code 默认模型，原生 1M 上下文，促销价 $2/$10 每 Mtok 至 2026-08-31 |
| SB-02 | `claude-opus-5` 成为默认 Opus 模型，1M 上下文，fast 模式 $10/$50 每 Mtok |
| SB-03 | Bedrock / Vertex / Claude Platform on AWS 默认模型 Opus 4.8；Auto mode 免 `CLAUDE_CODE_ENABLE_AUTO_MODE`，可用 `disableAutoMode` 关闭 |
| SB-20 | Sonnet 5 / Opus 5 原生 1M；`CLAUDE_CODE_DISABLE_1M_CONTEXT` 对所有原生 1M 模型强制回 200K 自动压缩 |
| claude-api skill | 当前模型表：Sonnet 5 `claude-sonnet-5` 1M、Opus 5 `claude-opus-5` 1M、Opus 4.8 `claude-opus-4-8` 1M、Haiku 4.5 `claude-haiku-4-5` **200K**；Effort `xhigh` 自 Opus 4.7 加入、是 Claude Code 默认档 |

## 过时点清单（更新）

| # | 位置 | 原文（过时） | 问题 | 处置 |
|---|------|-------------|------|------|
| 1 | frontmatter `updated` | `2026-08-07` | 需同步到本次更新 | 改为 `2026-08-10` |
| 2 | 模型别名表 `default` 行 | 自动选择（Max: Opus 4.8, 其他: Sonnet 5） | SB-02：默认 Opus 已升级为 Opus 5 | 改为 Max: **Opus 5** |
| 3 | 模型别名表 `opus` 行 | Claude Opus 4.8 | SB-02：默认 Opus 模型为 `claude-opus-5` | 改为 **Claude Opus 5** |
| 4 | 模型别名表 `haiku` 行 | Token 上下文 1M | Haiku 4.5 上下文实为 200K（claude-api 权威表） | 改为 **200K**（顺带修正既有错误） |
| 5 | 启动参数完整模型名示例 | `claude --model claude-opus-4-6` / `claude-sonnet-4-6` | 已是旧版本，当前默认模型为新系列 | 改为 `claude-opus-5` / `claude-sonnet-5` |
| 6 | Effort 表 `xhigh` 行 | 极深推理（Opus 4.7/4.8 支持） | Opus 5 / Sonnet 5 也支持，且为 Claude Code 默认档 | 更新标注为 Opus 5 / Opus 4.7+ / Sonnet 5；Claude Code 默认档 |
| 7 | Effort 表 `max` 行 | 最大推理（Opus 4.6+ 支持） | Opus 5 / Sonnet 5 支持 | 更新标注为 Opus 5 / Opus 4.6+ / Sonnet 5 |
| 8 | 第三方平台 env 示例 | `claude-opus-4-6`（含 `[1m]` 写法） | SB-03：第三方平台默认 Opus 4.8 | 改为 `claude-opus-4-8`；Bedrock sonnet 示例改为 `claude-sonnet-5` |
| 9 | modelOverrides 示例 key | `"claude-opus-4-6"` | 同上 | 改为 `claude-opus-4-8`（sonnet key 改 `claude-sonnet-5`） |
| 10 | LLM Gateway 示例 | `my-gateway/claude-opus-4-6` | 默认 Opus 已升级 | 改为 `my-gateway/claude-opus-5` |
| 11 | 模型能力声明示例描述 | `'Opus 4.6 routed through a Bedrock custom endpoint'` | 对齐第三方默认 | 改为 `'Opus 4.8 routed...'` |
| 12 | 自定义模型显示名称示例 | `'Opus 4.6 routed through a Bedrock custom endpoint'` | 同上 | 改为 `'Opus 4.8 routed...'` |
| 13 | 1M 上下文段落开头 | Opus 4.6 和 Sonnet 4.6 支持 100 万 token | SB-20：Sonnet 5 / Opus 5 原生 1M | 改为 Opus 5 / Sonnet 5 / Opus 4.8 |
| 14 | 1M 完整模型名示例 | `/model claude-sonnet-4-6[1m]` / `claude-opus-4-6[1m]` | 同上 | 改为 `claude-sonnet-5[1m]` / `claude-opus-5[1m]` |
| 15 | 1M 计费说明 | 前 200K 标准费率 / 超 200K 长上下文定价 | 新模型 1M 为原生能力，按标准费率计费，无长上下文附加定价 | 改为原生 1M 计费说明 + Sonnet 5 促销价 |
| 16 | 1M 禁用说明 | `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` 只有命令 | SB-20：强制回 200K 自动压缩 | 补充说明覆盖所有原生 1M 模型并自动压缩 |
| 17 | VSCode 别名表 | Sonnet 4.6 / Opus 4.6 | 同 #3/#5 | 改为 Sonnet 5 / Opus 5 |
| 18 | VSCode Effort 支持说明 | Effort Level 仅支持 Opus 4.6 和 Sonnet 4.6 | 过时 | 改为支持 Opus 5 / Sonnet 5 及 4.6+ 系列，`xhigh` 需 4.7+ / Opus 5 / Sonnet 5 |
| 19 | opusplan 流程图 | 使用 Opus 4.6 / Sonnet 4.6 | 同 #3 | 改为 Opus 5 / Sonnet 5 |
| 20 | 性能调优建议 #3 | 注意 200K 后的额外计费 | 过时 | 改为 1M 原生能力、标准费率、无额外长上下文费 |

## 新增点

| # | 位置 | 新增内容 | 依据 |
|---|------|---------|------|
| N1 | 核心概念末尾 | `[!tip] 大白话`（默认 Sonnet 5，需要更强用 `/model opus` 切 Opus 5） | 用户偏好 + SB-01/02 |
| N2 | 模型别名表后 | `[!tip] 大白话`（`default` 行为：Max=Opus 5、普通=Sonnet 5；别名指向最新版） | 用户偏好 + SB-01/02 |
| N3 | Effort 表后 | `[!tip] 大白话`（Effort = 思考深度；Claude Code 默认 xhigh） | 用户偏好 + claude-api |
| N4 | 第三方平台「官方云平台配置」段 | `[!info] 2026-08 更新`：第三方默认 Opus 4.8；Auto mode 免 opt-in；`disableAutoMode` 关闭 | SB-03 |
| N5 | 1M 上下文段 | `[!tip] 大白话`（1M 可装下大型仓库；Sonnet 5 / Opus 5 原生 1M；`[1m]` 为兼容写法）+ Sonnet 5 促销价 | SB-01/20 + 用户偏好 |
| N6 | 更新记录 | 追加 2026-08-10 行 | 规范 |

## 保留（无过时证据）

- **Fallback 模型**：`--fallback-model` / `fallbackModels` 用法未变
- **Extended Thinking 关键词表**（think / think hard / think harder / ultrathink）：无来源确认变更，保留原文
- **自定义 API 端点**（`env` / `ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN`）：仍为官方写法
- **`providers` / `defaultProvider` 非官方警告**：仍成立
- **禁用自适应推理**（`CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`）：无来源确认变更
- **常见问题、参考资料、相关文档**：无过时内容
- **opusplan 别名行 Token 上下文（200K）**：无来源确认变更，保留但列入复核项
