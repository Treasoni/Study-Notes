# 批处理日志：DeepSeek-Harness 教程排版重排

> 批 1（全部一次，9 个文件）· patch-in-place · 2026-08-15

## 处理记录

| # | 文件 | 动作 | 结果 |
|---|---|---|---|
| 1 | DeepSeek-Harness 是什么.md | title + H1 → `第 1 章：心智模型` | ✅ |
| 2 | DeepSeek-Harness 安装与快速上手.md | title + H1 → `第 2 章：环境准备` | ✅ |
| 3 | DeepSeek-Harness 插件开发核心.md | title + H1 → `第 3 章：插件开发核心` | ✅ |
| 4 | DeepSeek-Harness 配置体系.md | title + H1 → `配置专册 · 配置体系` | ✅ |
| 5 | DeepSeek-Harness 与ClaudeCode对照迁移.md | title + H1 → `第 4 章：实战` | ✅ |
| 6 | DeepSeek-Harness 配置实战.md | title + H1 → `配置专册 · 配置实战` | ✅ |
| 7 | DeepSeek-Harness 常见坑与速查.md | title + H1 → `第 5 章：速查与排错` | ✅ |
| 8 | README.md | 计数 5+2、清单补录配置实战、阅读顺序、系列约定 | ✅ |
| 9 | DeepSeek-Harness MOC.md | 顶部描述、04·A/04·B 标注、学习路径图 | ✅ |

## 需复核
- 无（全部为标题/导航改动，正文技术内容未触碰）

## 交叉引用核验
- 文件名未变 → 所有 `[[wikilink]]` 仍按文件名解析，不破链；
- 主章 01–05 编号未变 → 正文内「第 X 章」/「5.1」式引用保持有效；
- 配套专册内部编号（配置体系 1–4 / 配置实战 1–7）保持不变 → 专册内部交叉引用（如「见第 7 节坑 2」）不受影响。
