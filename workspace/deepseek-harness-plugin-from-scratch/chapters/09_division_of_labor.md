## 第 9 章：与《插件实战》的分工

前 8 章从空目录手写全文件，走完了「写 → 配 → 验证 → 打包 → 安装」整条链路；而系列里的另一篇《DeepSeek-Harness 插件实战》[^S11] 则是从 example-plugin 脚手架改造出同一个插件。本篇不重复讲脚手架知识，只把两篇的分工、配合读法和可对照的共同基线说清楚。

### 9.1 双路线对照：改造 vs 从零——终点一致、路径不同

| 维度 | 改造路线（《插件实战》） | 从零路线（本篇） |
| --- | --- | --- |
| 起点 | example-plugin 脚手架 | 空目录 |
| 第一步 | 复制脚手架、删改自带文件 | 手写 `src/index.ts` + 最小 patch |
| 终点 | 同一插件：工具 `git_log` + 配置 `maxCommits` | 同一插件：工具 `git_log` + 配置 `maxCommits` |
| 收获 | 脚手架里每个文件是干什么的 | 每个文件为什么必须存在 |

> [!tip] 大白话
> 两篇像同一道菜的「半成品加工版」与「全流程生做版」——菜一样，一个省事、一个练基本功。想快速吃到嘴，走《插件实战》；想学会从备菜到出锅的全过程，走本篇。

### 9.2 本篇刻意不教的

- **脚手架自带文件**：eslint 配置、tsconfig 的细化选项、dev/bundle 双 patch 之外的约定文件——这些属于改造路线的讲解范围，从零路线按需才引入。
- **O2 的 monorepo 内建包规范**：`lib/types` 目录、extends 根 tsconfig、references、constraints。这是 deepseek-harness 仓库**内部建包**的规范，**不含** `dsh.bundle.patch`；独立插件只按 V1 规范走（`dist/` + `dsh.bundle.patch`）[^S12]。两套规范不要混用，本篇只教独立插件规范。

> [!note] 这在 Claude Code 里相当于
> 「用官方模板改」vs「从零手写」两条学习路线互补：前者省时间，后者建立对每个文件为何存在的理解。

### 9.3 两篇配合的读法

- **已有《插件实战》基础**：跳过第 1 章的对照表，从第 2 章直接上手；本篇每一步都能与《插件实战》的成品对号入座。
- **从零读者**：以本篇为主线，读到 defineTool、Config schema、bundle 概念时，回翻《插件实战》做对照验证，两条线互相印证。

### 9.4 共同基线保证可对照

两篇共用同一套基线，因此终点严格一致：模型可见工具名 `git_log`、诊断名 `export const name='git-log-plugin'`、包名 `dsh-git-log-plugin`、patch id `git-log`、config 默认 `maxCommits: Schema.number().default(5)`，以及「四名分离」`git-log-plugin` ≠ `dsh-git-log-plugin` ≠ `git-log` ≠ `git_log`。任一章节，都能把本篇文件与《插件实战》成品逐文件对照，不会出现「名字对不上」的困惑。

## 本章小结

- 两篇是同一终点的两条路径：改造（脚手架起步）省事，从零（空目录手写）练基本功，选哪条看学习目标。
- 本篇刻意不教脚手架自带文件与 O2 的 monorepo 内建包规范；独立插件只按 V1 规范，两套规范不可混用。
- 已有《插件实战》基础可跳过第 1 章直接上手；从零读者以本篇为主、《插件实战》作对照验证。
- 共同基线（同一 `git_log` / 同一四名分离 / 同一 `maxCommits=5`）保证两篇任意一步都能逐文件对照。

---

[^S11]: V2《DeepSeek-Harness 插件实战》：从 example-plugin 脚手架改造出同一插件的教学分册，是本篇的对照路线。见 [[DeepSeek-Harness 插件实战]]。
[^S12]: V3《DeepSeek-Harness 配置体系》：bundle / profile 分层心智模型的来源，用于界定 9.2 中独立插件规范与 O2 内建包规范的边界。见 [[DeepSeek-Harness 配置体系]]。
