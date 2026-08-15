# 批量更新计划：DeepSeek-Harness 教程排版重排

> 方案 A（章+配套）已确认 · 目标：统一标题风格、同步导航、修正编号约定

## 目标标题模板

- 主章（01–05）：`DeepSeek-Harness 插件开发 · 第 X 章：主题——副题`
- 配套专册：`DeepSeek-Harness 配置专册 · 配置体系——副题` / `· 配置实战——副题`
- frontmatter `title` 与 H1 **保持一致**

## 逐文件动作

| # | 文件 | 现状 title | 目标 title（=H1） |
|---|---|---|---|
| 1 | 是什么.md | DeepSeek-Harness 插件开发：心智模型 | `DeepSeek-Harness 插件开发 · 第 1 章：心智模型——插件树 vs 单体 + 扩展` |
| 2 | 安装与快速上手.md | DeepSeek-Harness 插件开发：环境准备 | `DeepSeek-Harness 插件开发 · 第 2 章：环境准备——源码运行路径` |
| 3 | 插件开发核心.md | DeepSeek-Harness 插件开发核心 | `DeepSeek-Harness 插件开发 · 第 3 章：插件开发核心——从 apply(ctx) 到发布` |
| 4 | 配置体系.md | DeepSeek-Harness 配置体系 | `DeepSeek-Harness 配置专册 · 配置体系——补丁树、Profile 与 bundle` |
| 5 | 与ClaudeCode对照迁移.md | DeepSeek-Harness 插件开发实战：自定义工具插件 | `DeepSeek-Harness 插件开发 · 第 4 章：实战——从零写一个自定义工具插件（每一步对照 Claude Code）` |
| 6 | 配置实战.md | DeepSeek-Harness 配置实战：像 Claude Code… | `DeepSeek-Harness 配置专册 · 配置实战——像 Claude Code 一样接入 skills/hooks/mcp/rules` |
| 7 | 常见坑与速查.md | DeepSeek-Harness 插件开发速查与排错 | `DeepSeek-Harness 插件开发 · 第 5 章：速查与排错` |

## 导航文件动作

### README.md
1. 「这是什么」计数：「5 篇独立分册 + 1 篇配置专册」→「5 篇主章分册 + 2 篇配置专册」；「产出形态」同步；
2. 「分册清单」：新增第 7 行《配置实战》（04·配套），序号列同步；
3. 「推荐阅读顺序」：主路径在 04 后补《配置实战》；急用路径同步；
4. 「系列约定」：「节编号与章号同步」改写为「主章节号与章号同步；配套专册使用独立编号（1–N）」；
5. title 保持「DeepSeek-Harness 插件开发教程 · 系列导览」。

### DeepSeek-Harness MOC.md
1. 顶部描述：「共 5 篇独立分册 + 系列导览」→「5 篇主章分册 + 2 篇配置专册 + 系列导览」；
2. 「04 实战项目」两篇加标注：`04·A 对照迁移` 与 `04·B 配置实战`（README/MOC 编号对齐）；
3. 学习路径图与阅读顺序核对，补《配置实战》已在序中（确认即可）。

## 交叉引用检查（改动后核验）
- 各章「下一章」/「本章小结」双链：文件名未变，双链不破；核对显示文本是否需按新章节号微调（如「第 5 章 5.1」→ 保持，专册内部编号不动）；
- 配置实战内「见第 7 节坑 2」为专册内部引用，保持不变。

## 覆盖风险与确认项
- 全部为**标题与导航**改动，不动正文技术内容；风险低；
- 双链按文件名解析，改 title/H1 不破坏链接；
- 需用户确认：本计划（P2 检查点）。

## 处理批次
- 批 1（全部一次）：7 篇 title/H1 + README + MOC = 9 个文件。
