# 批量更新意图 · DeepSeek-Harness 教程重写（插件开发导向）

## 用户确认（2026-08-15）

| 字段 | 值 |
|---|---|
| source_path | `AI学习/DeepSeek-Harness 教程/` |
| source_scope | all（README + 5 分册 + MOC，共 7 篇） |
| source_glob | `*.md` |
| update_goal | 以「写自己的 dsh 插件」为目标全套重构教程，用 Claude Code 经验做桥接 |
| 插件目标 | **dsh 插件**（DeepSeek-Harness 插件：`apply(ctx)` + `cordis.yml` patch） |
| 重写形态 | **全套重构**（章节职责重新设计，不只深化 3.8） |
| destination_mode | **patch-in-place**（原地覆盖现有 7 个文件） |
| batch_size | 3（分 3 批：1-3 章 / 4-5 章 / README+MOC） |
| shared_research | **yes**（插件开发需补充官方一手资料） |
| moc_path | `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC.md`（并同步父级 `AI学习/00-索引/AI学习 MOC.md`） |

## 背景

- 现有一整套 5 篇分册 + 系列导览，定位是「熟悉 Claude Code 的用户，快速上手 dsh 或评估换还是留」。
- 用户真实目标转变：**写自己的 dsh 插件**，且主要熟悉 Claude Code。
- 因此整套教程从「换还是留 / 快速上手」重构为「从 Claude Code 视角学会写 dsh 插件」。

## 重写主线（初步设计）

| 现有文件 | 新职责 |
|---|---|
| README.md | 系列导览：插件开发导向 |
| DeepSeek-Harness 是什么.md | Ch1 心智模型：dsh 插件树 vs Claude Code 单体+扩展 |
| DeepSeek-Harness 安装与快速上手.md | Ch2 环境准备：源码运行路径（写插件前提）+ 基础配置 |
| DeepSeek-Harness 配置体系.md | Ch3 插件开发核心：apply(ctx)、cordis.yml patch、三种形态、inject、工具注册 |
| DeepSeek-Harness 与ClaudeCode对照迁移.md | Ch4 实战项目：写一个完整示例插件（Claude Code 对照） |
| DeepSeek-Harness 常见坑与速查.md | Ch5 插件开发速查与排错 |
| DeepSeek-Harness MOC.md | 更新索引 |

## 约束

- patch-in-place，但**保留文件名**，避免破坏既有双链（`AI学习 MOC`、`Claude Code MOC`、分册间互链）。
- 不复制整篇旧笔记进上下文；每篇用 stale map 定位需重写段落。
- 保留用户原有写作风格：YAML frontmatter、Callout、大白话 tip、更新记录、脚注。
