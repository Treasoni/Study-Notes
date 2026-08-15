## 第 1 章：结果预览——从零建的插件 vs 脚手架改造

读完《插件实战》之后很容易陷入「假会」：照着 example-plugin 改改能跑，但换个空目录就不知道从哪里下手。本章先给你一张「户型图」——从零建的插件到终点由哪些文件组成、四个名字各管什么——再把改造路线与从零路线摆在一起对照着读，让你在看具体代码之前先看见终点。

### 1.1 为什么还要「从零」写一遍：依赖脚手架的幻觉

example-plugin 脚手架把文件都配好了，这既是方便也是陷阱。复制脚手架文件，你拿到的是「结果」，丢的是「为什么」：每个文件为什么存在、哪两个名字必须相等、为什么 patch 的 `name` 要用绝对路径，都被模板藏了起来。真正的理解发生在从空目录开始、一个文件一个文件把它们造出来的过程里。[^S13]

另一个常见误解：脚手架的 dev/bundle 双 patch 看起来像「标准配置」，但它不是独立插件的起点。最小起步只需 1 份 patch（`dev-cordis.patch.yml`），bundle patch 是第 6 章才补上的工程化产物。[^S1]

> [!tip] 大白话
> example-plugin 像「装修好的样板间」，拖进去就能住，但你看不见水电管线怎么走；从零像「清水房自己走水电」，慢，但每一根管子的走向都长在你脑子里。所以本篇开头先给你一张「户型图」——最终文件清单——知道目的地再动工。

> [!note] 这在 Claude Code 里相当于
> 相当于不用官方插件 starter 模板，而是自己在空目录手写插件入口文件与 manifest。模板帮你生成的骨架，如果只是复制而不理解，换一个插件照样不会写——本篇就是补这份理解。

### 1.2 终点长什么样：8 个文件的清单 + 4 个名字 + 基线表

本篇终点是一个可构建、可打包、可安装的独立插件工程，到第 6 章成型时共 8 个文件（6 个手写 + 2 个生成）：

| # | 文件 | 作用 | 首次出现 |
| --- | --- | --- | --- |
| 1 | `src/index.ts` | 插件入口 + 注册中心（name / apply / inject / Config / register） | 第 2 章 |
| 2 | `src/tools/git-log.ts` | 工具本体：defineTool 工厂 | 第 3 章 |
| 3 | `dev-cordis.patch.yml` | 开发期 patch：`name` 用绝对路径，`--patch` 加载 | 第 2 章 |
| 4 | `cordis.patch.yml` | bundle patch：`name` = 包名，打包激活用 | 第 6 章 |
| 5 | `package.json` | 工程声明：name / main / types / dsh.bundle.patch / scripts | 第 6 章 |
| 6 | `tsconfig.json` | 编译配置：ES2022 / ESNext / Bundler / strict | 第 6 章 |
| 7 | `pnpm-lock.yaml` | 依赖锁文件（`pnpm install` 生成） | 第 6 章 |
| 8 | `dist/` | 构建产物（`pnpm run build` 生成） | 第 6 章 |

文件归属沿袭 [[DeepSeek-Harness 插件开发核心]]：`src/index.ts` 是注册中心，工具本体放 `src/tools/*.ts`。最值得注意的是 4 个名字各管各的、不能混，这是全系列最高频的坑：

| 名字 | 写在哪 | 职责 |
| --- | --- | --- |
| `git-log-plugin` | `export const name` | 诊断名 / 加载日志 `[git-log-plugin] plugin loaded!` |
| `dsh-git-log-plugin` | package.json `name` | 包名；bundle patch 的 `name` 必须等于它 |
| `git-log` | patch yml 的 `- insert:` id | patch id / 实例名 |
| `git_log` | defineTool 的 `name` | 模型可见的工具名 |

四名分离：`git-log-plugin` ≠ `dsh-git-log-plugin` ≠ `git-log` ≠ `git_log`。加上 config 默认值，就是与 [[DeepSeek-Harness 插件实战]] 可对照、与 [[DeepSeek-Harness 配置体系]] 的 Schema 口径一致的全篇一致性基线：[^S11]

| 项 | 固定值 |
| --- | --- |
| tool name（模型可见） | `git_log` |
| 诊断名 / 加载日志 | `export const name = 'git-log-plugin'` |
| 包名（package.json name） | `dsh-git-log-plugin` |
| patch id | `git-log` |
| config 默认值 | `maxCommits: Schema.number().default(5)` |

> [!tip] 大白话
> 4 个名字像「身份证号 / 小区名 / 门牌号 / 工牌名」：包名是身份证号（全局唯一）、patch id 是小区名（指哪一栋）、诊断名是门牌号（日志里怎么称呼你）、tool name 是工牌名（模型看到的你）。混用一个，要么装不进去，要么模型叫不出你——从第 2 章起，每个文件都要让这四样对号入座。

### 1.3 双路线对照表：《插件实战》改造（example-plugin）vs 本篇从零（空目录）

| 维度 | 《插件实战》改造 | 本篇从零 |
| --- | --- | --- |
| 起点 | `example-plugin/` 脚手架 | 空目录 |
| 第一个动作 | 改文件 | `mkdir` 后写第 1 个文件 |
| 对文件的理解 | 复制后替换，容易漏「为什么」 | 亲手建每个文件，逐行讲原因 |
| patch 起点 | dev/bundle 双 patch 都在 | 先 1 份 `dev-cordis.patch.yml`，bundle 后补 |
| 终点 | 同一个 `git_log` 插件 | 同一个 `git_log` 插件 |
| 适合人群 | 想快速出活 | 想掌握每个文件为什么存在 |

两条路线终点一致、路径不同，共享同一一致性基线（`git_log` / 四名分离 / `maxCommits=5`），所以可以互相对照着读 [[DeepSeek-Harness 插件实战]] 与本篇。从第 2 章起，本篇将在一个空目录里把这张户型图一砖一瓦搭起来。

## 本章小结

- 脚手架能让你快速跑通，但复制文件会丢掉「每个文件为什么存在」的理解；从零是把这份理解补回来。
- 最小起步只需 1 份 patch（`dev-cordis.patch.yml`），dev/bundle 双 patch 不是独立插件的起点。
- 本篇终点 = 8 个文件（6 手写 + 2 生成），先记住这张「户型图」再动工。
- 四名分离是最高频的坑：`git-log-plugin` ≠ `dsh-git-log-plugin` ≠ `git-log` ≠ `git_log`；加 `maxCommits=5` 构成全篇一致性基线。
- 两条路线终点一致、路径不同：改造省事、从零练基本功，靠同一基线可互相参照。

## 脚注

[^S1]: O1 · deepseek-harness 官方文档 `docs/user/develop/basic/index.zh.md`（Your first plugin）——最小 2 文件骨架与加载命令，本篇「最小只需 1 份 patch」的出处。
[^S11]: V2 · 《DeepSeek-Harness 插件实战》——一致性基线（`git_log` / 四处名字 / `maxCommits=5`）与验证命令链。
[^S13]: V4 · 《DeepSeek-Harness 插件开发核心》——文件归属 / apply 三形态 / defineTool 契约。
