# cc05 更新报告（Update Report）

- **note_id**: cc05
- **笔记**: `AI学习/Claude Code 教程/02-基础功能/Claude Code 模型与推理设置.md`
- **更新日期**: 2026-08-10
- **更新方式**: 局部 patch（未重写未过时段落，保留原结构和写作风格）
- **输出**: `updates/cc05/updated_note.md`（未改动原 vault 文件）

## 变更摘要

共定位 **20 处过时点 + 6 处新增**，全部已应用：

### 模型默认值（核心）
- `default` 别名：Max 档默认 **Opus 5**（原 Opus 4.8）
- `opus` 别名：**Claude Opus 5**（原 Opus 4.8）
- `sonnet` 别名保持 Claude Sonnet 5（已是 2026-06 默认，无变化）
- 完整模型名示例全部从 `claude-opus-4-6` / `claude-sonnet-4-6` 更新为 `claude-opus-5` / `claude-sonnet-5`

### 第三方平台（SB-03）
- 新增说明：Bedrock / Vertex / Claude Platform on AWS 默认模型为 **Opus 4.8**；**Auto mode 免 `CLAUDE_CODE_ENABLE_AUTO_MODE`**，可用 `"disableAutoMode": true` 关闭
- env / modelOverrides / 能力声明 / 显示名称示例中的 `claude-opus-4-6` → `claude-opus-4-8`
- LLM Gateway 示例 → `claude-opus-5`

### Effort Level（update_goal 第 4 点）
- `xhigh` 标注：Opus 4.7/4.8 → **Opus 5 / Opus 4.7+ / Sonnet 5；Claude Code 默认档**
- `max` 标注：Opus 4.6+ → **Opus 5 / Opus 4.6+ / Sonnet 5**
- VSCode「Effort Level 仅支持 Opus 4.6 和 Sonnet 4.6」已更新

### 1M 上下文（SB-20）
- 段落首句更新为 **Opus 5 / Sonnet 5 / Opus 4.8 原生支持 1M**
- 完整模型名示例更新为 `claude-sonnet-5[1m]` / `claude-opus-5[1m]`
- 计费说明重写：Sonnet 5 促销价 $2/$10（至 2026-08-31，之后 $3/$15）、Opus 5 $5/$25（fast $10/$50）、1M 为原生能力按标准费率
- `CLAUDE_CODE_DISABLE_1M_CONTEXT` 补充：对所有原生 1M 模型强制回 200K 自动压缩

### 其他
- **Haiku 上下文修正为 200K**（原文误写 1M，依据 claude-api 权威模型表）
- opusplan 流程图 → Opus 5 / Sonnet 5
- 性能调优建议 #3 计费表述更新
- frontmatter `updated` → 2026-08-10
- 追加 `## 更新记录` 2026-08-10 行
- 核心概念新增 3 处 `[!tip] 大白话`（用户偏好）

## 依据来源

- SB-01（Sonnet 5 默认 + 促销价）、SB-02（Opus 5 默认）、SB-03（第三方 Opus 4.8 + Auto mode）、SB-20（1M 上下文与 `CLAUDE_CODE_DISABLE_1M_CONTEXT`）
- claude-api skill 当前模型表与 Effort 档位说明（用于 Haiku 上下文、xhigh/max 支持模型）

## 风险项

1. **opusplan 别名 Token 上下文（200K）**：无来源确认是否随 Opus 5 / Sonnet 5 升级，保留原文。若两者均为原生 1M，opusplan 上下文可能已变，需官方 docs 复核。
2. **Extended Thinking 关键词 Token 预算**（1.5K/3K/8K/16K）：无来源确认，保留原文。新模型走 adaptive thinking，关键词机制可能已弱化，建议后续用官方 docs 复核。
3. **第三方平台 sonnet 模型 ID**：Bedrock ARN（`us.anthropic.claude-sonnet-5-v1`）为示例占位，实际 ID 以云平台控制台为准。
4. **计费时效性**：Sonnet 5 促销价 $2/$10 到 2026-08-31 截止，之后恢复 $3/$15；后续需跟进。

## needs-review

**是（建议复核，低优先级）**。主要变更均有 SB-01/02/03/20 与 claude-api 权威表支撑，可信度高；仅上述 4 项风险（opusplan 上下文、Extended Thinking 关键词预算、第三方 sonnet ARN 示例、促销价时效）建议人工或官方 docs 复核后再写回原文件。
