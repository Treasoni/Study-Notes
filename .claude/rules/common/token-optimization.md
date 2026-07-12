# Token Optimization Rules

本项目的目标是稳定产出学习笔记，同时尽量降低 token 消耗。

## Default Strategy

1. 先读 `todo.md`、`00_intent.md`、`03_outline.md` 的相关小段，不整篇加载所有素材。
2. 读取 `02_deep_research.md` 时优先用 `rg` 定位章节相关引用，只加载当前章节需要的片段。
3. 逐章写作时一次只处理一章；不要把所有章节、全部素材和最终笔记同时放进上下文。
4. 每个阶段产出结构化中间文件，后续阶段优先引用文件路径和锚点，而不是重复粘贴全文。
5. 子代理只返回结构化摘要、链接、引用编号和判断，不返回长网页正文。
6. 更新旧笔记时先做 diff/变更摘要，再局部改写过时段落。

## Prompt Cache Strategy

See `.claude/rules/common/prompt-cache.md` for the complete prompt cache strategy and the stable subagent template.

## File Loading Budget

| 文件 | 默认读取方式 |
| --- | --- |
| `todo.md` | 全读，体量小 |
| `00_intent.md` | 全读，体量小 |
| `01_explore_result.md` | 只读摘要和用户选择 |
| `02_deep_research.md` | 按关键词/引用编号局部读取 |
| `03_outline.md` | 全读或当前章节局部读取 |
| `chapters/*.md` | 一次只读当前章节和相邻章节摘要 |
| `output/final_note.md` | 仅在组装、更新、发布时读取必要段落 |

## Output Rules

- 研究阶段保留链接和 100-200 字摘要，不保存网页全文，除非用户明确要求。
- 章节文件里用引用编号指向 `02_deep_research.md`，不要重复复制长素材。
- 更新报告只记录 changed/unchanged/stale 三类，不复述整篇笔记。
