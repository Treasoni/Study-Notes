---
name: update-workflow
description: 笔记更新编排层。定位目标笔记、解析结构、自动检测 INSERT/REFRESH 意图，调度 /update skill 执行更新。
---

# Skill: update-workflow（笔记更新编排）

> 完整工作流规范见 `docs/updating-notes.md`

## 触发时机

用户要求修改、添加或更新已有笔记内容时。

## 执行模型

本 skill 采用 **Operator Pattern**：主 Agent 作为编排调度员，`/update` skill 作为执行者。

1. **定位笔记** → 多级搜索（精确路径 → OUTPUT_PATH → 3-published/ → vault 根目录）
2. **检测意图** → INSERT（用户提供内容）或 REFRESH（内容过时）
3. **备份 + 调度 /update** → 传递结构解析结果和意图检测结果
4. **轻量验证** → 标题层级、wikilink 完整性、frontmatter
5. **展示 diff + 硬停止** → 等待用户确认

> 详见 `docs/updating-notes.md` Step 1-5 完整规范

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `note_query` | 笔记名称或完整路径 | ✅ |
| `user_content` | 用户提供的新内容（INSERT 模式） | INSERT 时必填 |
| `target_section` | 要刷新的章节名（REFRESH 模式） | REFRESH 时必填 |
| `update_mode` | 显式指定 INSERT/REFRESH（省略时自动检测） | ❌ |

## 禁止行为

- 不要跳过多级搜索，直接假设笔记不存在
- 不要跳过意图检测，直接执行更新
- 不要在 INSERT 模式下添加用户未提供的信息
- 不要修改不相关章节的内容
- 不要跳过验证步骤直接展示结果
- 不要跳过用户确认直接写入文件
