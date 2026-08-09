# cc05 更新计划（Update Plan）

- **note_id**: cc05
- **模式**: 局部 patch（不重写未过时段落）
- **产出**: `updates/cc05/updated_note.md`（先写工作区，不直接改原 vault 文件）

## 编辑步骤（按文件顺序）

### 1. frontmatter
- `updated: 2026-08-07` → `2026-08-10`
- `status: updated` 保持不变

### 2. 核心概念
- 在「通俗理解」比喻框后新增：
  `> [!tip] 大白话（2026-08 更新）` — 默认 Sonnet 5；需要最强推理用 `/model opus` 切 Opus 5

### 3. 模型别名系统（表格）
| 行 | 变更 |
|----|------|
| `default` | Max: Opus 4.8 → **Opus 5** |
| `opus` | Claude Opus 4.8 → **Claude Opus 5** |
| `haiku` | Token 上下文 1M → **200K**（修正既有错误） |
| `sonnet` / `sonnet[1m]` / `opusplan` | 保留 |

- 表格后新增 `[!tip] 大白话`：`default` 行为 + 别名指向最新版

### 4. 模型切换方式
- 方式二（启动时指定）：完整模型名示例 `claude-opus-4-6` / `claude-sonnet-4-6` → `claude-opus-5` / `claude-sonnet-5`
- 方式三（环境变量）：在示例后追加一行 `export ANTHROPIC_MODEL=claude-opus-5`，说明 ANTHROPIC_MODEL 也接受完整模型名

### 5. Effort Level 表
- `xhigh` 行：`（Opus 4.7/4.8 支持）` → `（Opus 5 / Opus 4.7+ / Sonnet 5；Claude Code 默认档）`
- `max` 行：`（Opus 4.6+ 支持）` → `（Opus 5 / Opus 4.6+ / Sonnet 5）`
- `medium` 行：删除 `（Opus/Sonnet 默认）`（Claude Code 默认实为 xhigh，避免误导）
- 表后新增 `[!tip] 大白话`：Effort = 思考深度；Claude Code 默认 xhigh

### 6. 第三方平台配置
- 「官方云平台配置」段开头新增 `[!info] 2026-08 更新`：第三方默认 Opus 4.8；Auto mode 免 `CLAUDE_CODE_ENABLE_AUTO_MODE`；可用 `"disableAutoMode": true` 关闭（SB-03）
- 方式一 env 示例：`claude-opus-4-6` → `claude-opus-4-8`；Bedrock ARN `us.anthropic.claude-opus-4-6-v1` → `...-4-8-v1`；Bedrock sonnet `us.anthropic.claude-sonnet-4-6-v1` → `...-5-v1`；`claude-opus-4-6[1m]` → `claude-opus-4-8[1m]`
- 方式二 modelOverrides：key `claude-opus-4-6` → `claude-opus-4-8`，`claude-sonnet-4-6` → `claude-sonnet-5`
- LLM Gateway：`my-gateway/claude-opus-4-6` → `my-gateway/claude-opus-5`
- 模型能力声明 + 自定义显示名称：描述文本 `Opus 4.6 routed...` → `Opus 4.8 routed...`

### 7. 扩展上下文（1M Tokens）
- 首句：`Opus 4.6 和 Sonnet 4.6 支持 100 万 token` → `Opus 5 / Sonnet 5 / Opus 4.8 原生支持 100 万 token`
- 完整模型名示例：`claude-sonnet-4-6[1m]` / `claude-opus-4-6[1m]` → `claude-sonnet-5[1m]` / `claude-opus-5[1m]`
- 新增 `[!tip] 大白话`（1M 可装下大型仓库；`[1m]` 为兼容写法）
- 计费说明重写：Sonnet 5 促销价 $2/$10（至 2026-08-31，之后 $3/$15）；Opus 5 标准价 $5/$25（fast $10/$50）；1M 为原生能力按标准费率，无长上下文附加定价；订阅超额度另计
- 禁用 1M 上下文：补充说明 `CLAUDE_CODE_DISABLE_1M_CONTEXT` 对全部原生 1M 模型强制回 200K 并自动压缩

### 8. VSCode 插件配置
- 别名表：`sonnet` → Claude Sonnet 5；`opus` → Claude Opus 5
- Effort 支持说明：`仅支持 Opus 4.6 和 Sonnet 4.6` → 支持 Opus 5 / Sonnet 5 及 4.6+ 系列；`xhigh` 需 Opus 4.7+ / Opus 5 / Sonnet 5

### 9. 推理模式详解 - opusplan
- 流程图：`使用 Opus 4.6` → `使用 Opus 5`；`使用 Sonnet 4.6` → `使用 Sonnet 5`

### 10. 配置最佳实践
- 性能调优建议 #3：`注意 200K 后的额外计费` → `1M 是模型原生能力，按标准费率计费，无额外长上下文附加费`

### 11. 更新记录
- 追加一行：`| 2026-08-10 | 同步 2026-08 模型现状：默认模型更新为 Sonnet 5 / Opus 5（原生 1M）；第三方平台（Bedrock/Vertex/AWS）默认 Opus 4.8 且 Auto mode 免 opt-in；Effort 档位标注更新；CLAUDE_CODE_DISABLE_1M_CONTEXT 强制回 200K 自动压缩；Haiku 上下文修正为 200K |`

## 不修改的段落

- Fallback 模型、Extended Thinking 关键词表、自定义 API 端点、providers 警告、常见问题、参考资料、相关文档

## 风险与假设

1. **opusplan 别名 Token 上下文（200K）**：未找到来源确认其随 Opus 5 / Sonnet 5 变化，保留原文，列入复核项
2. **Extended Thinking 关键词 Token 预算**（1.5K/3K/8K/16K）：无来源确认，保留原文，建议后续用官方 docs 复核
3. **第三方平台 sonnet 模型 ID**：Bedrock ARN 格式（`us.anthropic.claude-sonnet-5-v1`）为示例，实际 ID 以云平台控制台为准
4. **计费说明**：基于 claude-api 当前价格表，促销价到 2026-08-31 有时效性，后续需跟进
