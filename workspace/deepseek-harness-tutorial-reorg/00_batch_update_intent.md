# 批量更新意图：DeepSeek-Harness 教程排版与结构重排

## 用户原始请求
- "我这个笔记看的好混乱，你重新修改排版和笔记"（指向 `AI学习/DeepSeek-Harness 教程/`）

## P0 确认参数（2026-08-15 用户已确认）
- **source_path**：`AI学习/DeepSeek-Harness 教程/`
- **source_scope**：目录内全部 Markdown（9 个：7 篇正文 + README + MOC）；`example-plugin/` 脚手架不改
- **update_goal**：统一排版与结构——① 同步 README/MOC（补录《配置实战》，计数改 5+2）；② 统一 7 篇 frontmatter title 与 H1 风格；③ 编号结构方案 A（章+配套）；④ 检查交叉引用
- **destination_mode**：patch-in-place（直接改原笔记）
- **batch_size**：全部一次处理
- **shared_research**：no（纯排版，无需新资料）

## 结构方案（用户已选 A：章+配套）
- 保留「5 主章 + 2 配置专册」框架，**不改文件名**
- 编号统一：主章 01–05；配套专册 03·配套《配置体系》、04·配套《配置实战》
- 标题统一模板：
  - 主章：`DeepSeek-Harness 插件开发 · 第 X 章：主题——副题`
  - 专册：`DeepSeek-Harness 配置专册 · 配置体系——副题` / `· 配置实战——副题`

## 诊断摘要（P1 扫描确认）
| 问题 | 涉及文件 |
|---|---|
| README 漏收录《配置实战》，计数「5+1」不符实际 | README.md |
| MOC 顶部自述「共 5 篇分册」不符实际（实际 7 篇） | DeepSeek-Harness MOC.md |
| MOC 的 04 挂两篇 vs README 04 一篇，编号打架 | README.md / MOC |
| 标题风格不统一（第 4 章 H1「实战：…」无系列前缀；有的章有「——副题」有的没有） | 全部 7 篇正文 |
| 配套专册独立编号（1–N）与 README「节编号与章号同步」约定冲突 | README.md（约定要改写） |
