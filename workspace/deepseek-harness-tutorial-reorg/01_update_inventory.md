# 更新清单：DeepSeek-Harness 教程排版重排

> 扫描范围：`AI学习/DeepSeek-Harness 教程/*.md`（9 个）· 扫描时间：2026-08-15
> 机器清单：`update_inventory.csv`（同目录）

## 清单总览

| # | 文件 | 定位 | frontmatter title（现状） | H1（现状） | updated | 动作 |
|---|---|---|---|---|---|---|
| 1 | README.md | 系列导览 | DeepSeek-Harness 插件开发教程 | DeepSeek-Harness 插件开发教程 · 系列导览 | 2026-08-15 | update |
| 2 | DeepSeek-Harness MOC.md | 索引 | DeepSeek-Harness 教程 MOC | DeepSeek-Harness 教程 MOC | 2026-08-15 | update |
| 3 | DeepSeek-Harness 是什么.md | 第1章 | DeepSeek-Harness 插件开发：心智模型 | DeepSeek-Harness 插件开发：心智模型——插件树 vs 单体 + 扩展 | 2026-08-15 | update |
| 4 | DeepSeek-Harness 安装与快速上手.md | 第2章 | DeepSeek-Harness 插件开发：环境准备 | DeepSeek-Harness 插件开发：环境准备——源码运行路径 | 2026-08-15 | update |
| 5 | DeepSeek-Harness 插件开发核心.md | 第3章 | DeepSeek-Harness 插件开发核心 | DeepSeek-Harness 插件开发核心：从 apply(ctx) 到发布 | 2026-08-15 | update |
| 6 | DeepSeek-Harness 配置体系.md | 03·配套 | DeepSeek-Harness 配置体系 | DeepSeek-Harness 配置体系：补丁树、Profile 与 bundle | 2026-08-15 | update |
| 7 | DeepSeek-Harness 与ClaudeCode对照迁移.md | 第4章 | DeepSeek-Harness 插件开发实战：自定义工具插件 | 实战：从零写一个自定义工具插件（每一步对照 Claude Code） | 2026-08-15 | update |
| 8 | DeepSeek-Harness 配置实战.md | 04·配套 | DeepSeek-Harness 配置实战：像 Claude Code 一样接入 skills/hooks/mcp/rules | 同左 | 2026-08-15 | update |
| 9 | DeepSeek-Harness 常见坑与速查.md | 第5章 | DeepSeek-Harness 插件开发速查与排错 | DeepSeek-Harness 插件开发速查与排错 | 2026-08-15 | update |

## 状态标记

- **ready**：9/9（全部已通读，改动点明确）
- **skip**：`example-plugin/`（脚手架代码，非排版对象）

## 一致性检查发现

1. README「5 篇分册 + 1 篇配置专册」+ 清单 6 行 → 实际 7 篇，缺《配置实战》；
2. MOC 顶部「共 5 篇独立分册 + 系列导览」→ 实际 5 主章 + 2 专册；
3. MOC「04 实战项目」两篇 vs README「04」一篇；
4. 标题前缀/副题风格：第 4 章 H1 无「DeepSeek-Harness 插件开发」前缀；第 5 章 H1 无副题；第 1/2 章 title 带「插件开发：」而第 3/5 章 title 不带；
5. README「系列约定 · 节编号与章号同步」与两本专册独立编号（1–N）冲突。
