# Agent 调用规范

## Agent 列表

| Agent | 用途 | 前置依赖 |
|-------|------|----------|
| `outline-generator` | 生成学习笔记大纲 | `00_intent.md` + `02_deep_research.md` |
| `chapter-writer` | 分批写作，每批 ≤3 章（章间确认保留） | `00_intent.md` + `02_deep_research.md` + `03_outline.md` |
| `note-assembler` | 组装章节成完整笔记 | `chapters/` 目录 + `00_intent.md` |

## 调用流程

```
research-collector → outline-generator → chapter-writer → note-assembler → note-beautifier
       ↓                    ↓                  ↓                 ↓
02_deep_research.md   03_outline.md    chapters/*.md    output/final_note.md
```

## 核心规则

1. **前置检查**：调用 agent 前必须确认依赖文件已就绪
2. **分批确认**：chapter-writer 每批最多写 3 章；每章写完后停下等用户确认，确认后由**同一子代理续写**下一章（不重读已在上文中的材料）；运行时不支持续写时，一次写完本批 ≤3 章后统一确认
3. **不跳步**：不可跳过前置阶段直接调用下游 agent
4. **大纲确认**：outline-generator 生成大纲后等待用户确认

## 错误处理

| 情况 | 处理 |
|------|------|
| 缺少前置文件 | 提示用户先完成上游阶段 |
| 大纲未确认 | 等待确认后再继续 |

## 关联技能

- `research-collector` — 提供 `02_deep_research.md`
- `note-beautifier` — 处理 `final_note.md` 发布到 Obsidian
- `workflow-orchestrator` — 编排完整流程
