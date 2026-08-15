---
title: "DeepSeek-Harness 从零写插件：空目录手写全文件"
tags: [deepseek-harness, ai, agent, 插件, 教程, 实战, 从零]
created: 2026-08-15
updated: 2026-08-15
status: published
source_project: deepseek-harness
---

# DeepSeek-Harness 从零写插件：空目录手写全文件

> [!summary] 本章导读
> 本分册是系列的第二条实战路径：与 [[DeepSeek-Harness 插件实战|插件实战]]（脚手架改造）相对，本篇**从空目录手写全部文件**，走通 **写 → 配 → 验证 → 打包 → 安装** 全链路。两篇共用同一示范工具 `git_log`、同一四名分离基线、同一 `maxCommits=5`，可逐文件对照——「改造」省事、「从零」练基本功。
> 每步都给：可复现命令 + 预期输出 + 出错排查。最小 2 文件起步（`src/index.ts` + `dev-cordis.patch.yml`），第 3 步加工具、第 4 步加配置、第 5 步工程化、第 6 步打包安装。
> **前置要求**：建议先读 [[DeepSeek-Harness 插件开发核心|第 3 章]]（插件概念：apply / inject / defineTool）与 [[DeepSeek-Harness 配置体系|配置体系专册]]（补丁树 / bundle / profile 术语）；排查时随时查 [[DeepSeek-Harness 常见坑与速查|第 5 章]]。想走改造捷径的读者先读 [[DeepSeek-Harness 插件实战|插件实战]]。

## 目录

- [[#第 1 章：结果预览——从零建的插件 vs 脚手架改造|第 1 章]]
- [[#第 2 章：第 1 步——空目录 + 最小 2 文件跑通|第 2 章]]
- [[#第 3 章：第 2 步——加工具 git_log|第 3 章]]
- [[#第 4 章：第 3 步——加 Config 可调参数|第 4 章]]
- [[#第 5 章：第 4 步——验证命令链|第 5 章]]
- [[#第 6 章：第 5 步——工程化补齐|第 6 章]]
- [[#第 7 章：第 6 步——打包发布安装|第 7 章]]
- [[#第 8 章：小结与下一步|第 8 章]]
- [[#第 9 章：与《插件实战》的分工|第 9 章]]

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

| #   | 文件                     | 作用                                                     | 首次出现  |
| --- | ---------------------- | ------------------------------------------------------ | ----- |
| 1   | `src/index.ts`         | 插件入口 + 注册中心（name / apply / inject / Config / register） | 第 2 章 |
| 2   | `src/tools/git-log.ts` | 工具本体：defineTool 工厂                                     | 第 3 章 |
| 3   | `dev-cordis.patch.yml` | 开发期 patch：`name` 用绝对路径，`--patch` 加载                    | 第 2 章 |
| 4   | `cordis.patch.yml`     | bundle patch：`name` = 包名，打包激活用                         | 第 6 章 |
| 5   | `package.json`         | 工程声明：name / main / types / dsh.bundle.patch / scripts  | 第 6 章 |
| 6   | `tsconfig.json`        | 编译配置：ES2022 / ESNext / Bundler / strict                | 第 6 章 |
| 7   | `pnpm-lock.yaml`       | 依赖锁文件（`pnpm install` 生成）                               | 第 6 章 |
| 8   | `dist/`                | 构建产物（`pnpm run build` 生成）                              | 第 6 章 |

文件归属沿袭 [[DeepSeek-Harness 插件开发核心]]：`src/index.ts` 是注册中心，工具本体放 `src/tools/*.ts`。最值得注意的是 4 个名字各管各的、不能混，这是全系列最高频的坑：

| 名字                   | 写在哪                        | 职责                                           |
| -------------------- | -------------------------- | -------------------------------------------- |
| `git-log-plugin`     | `export const name`        | 诊断名 / 加载日志 `[git-log-plugin] plugin loaded!` |
| `dsh-git-log-plugin` | package.json `name`        | 包名；bundle patch 的 `name` 必须等于它               |
| `git-log`            | patch yml 的 `- insert:` id | patch id / 实例名                               |
| `git_log`            | defineTool 的 `name`        | 模型可见的工具名                                     |

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

## 第 2 章：第 1 步——空目录 + 最小 2 文件跑通

这一章是全篇的第一个关键里程碑。目标只有一个：用一个空目录、两个文件，让 dsh 在启动时真的把「你写的插件」加载起来，并在日志里看到 `[git-log-plugin] plugin loaded!`。这一步不碰任何脚手架、不建 `package.json`、不编译——纯粹验证「空目录 + 2 文件 → 加载」这条链路是通的。走通它，后面所有章节（加工具、加配置、打包安装）才有地基。

### 2.1 建目录：`mkdir git-log-plugin && cd git-log-plugin`

先明确一个前置：所有开发期的验证命令（`pnpm dsh ...`）都要在 **dsh 源码仓库根目录**执行，因为我们用的是源码仓库自带的 dsh CLI，而不是全局装的 npx 版本；而且 `--patch ./xxx.patch.yml` 的相对路径按仓库根目录解析（2.4 详述）。所以插件目录也建在源码仓库根目录下面：

```bash
# 在 dsh 源码仓库根目录执行
mkdir git-log-plugin
cd git-log-plugin
```

> [!tip] 大白话
> 把源码仓库想成「整栋楼」，`git-log-plugin/` 是你刚租下来的一间毛坯房。你得在这栋楼里干活没错，但「住哪间、门牌号多少」是后面 patch 里要写清楚的事——现在先把房间建出来。

目录名直接用 `git-log-plugin`，对应一致性基线里的「诊断名」：后面 `export const name` 也用同一个名字，第一步就对齐，免得后面再改。注意这一步我们**不需要** `package.json`——那是第 6 章工程化才出现的东西，现在两文件起步最干净。

### 2.2 写 `src/index.ts` 最小版

插件本体是一个普通的 TypeScript 模块。先建 `src/` 目录，再写入口文件：

```bash
mkdir -p src
```

```ts
// src/index.ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'git-log-plugin'

export function apply(ctx: Context) {
  console.log(`[${name}] plugin loaded!`)
}
```

逐行拆开看：

1. `import type { Context } from '@deepseek-ai/cordis'` — 纯类型导入：`import type` 保证编译后这行直接被擦掉。`Context` 只是给 `apply` 参数做类型标注，运行时的上下文对象由 cordis 自己注入，你不 import 也会拿到它。
2. `export const name = 'git-log-plugin'` — 插件在日志/诊断里的名字，也就是四名分离的**第一个名字（诊断名）**[^S11]。它 ≠ 包名 `dsh-git-log-plugin` ≠ patch id `git-log` ≠ 工具名 `git_log`。这一章只用得上它，但先把「四个名字是四件事」记牢，第 3、6 章会逐个落地。这条基线来自系列里的 [[DeepSeek-Harness 插件实战]]，两篇可以对照读。
3. `export function apply(ctx: Context)` — 插件入口。cordis 加载到插件后调用它。`ctx` 是上下文句柄，这一章还只拿它做占位，第 3 章开始用它取工具注册表 `ctx.tools`。
4. `console.log(\`[${name}] plugin loaded!\`)` — 插件自己的加载日志。模板串展开后就是 `[git-log-plugin] plugin loaded!`，这里的 `name` 正是第 2 步的常量——日志前缀和诊断名天然一致。

> [!note] 这在 Claude Code 里相当于
> `export function apply(ctx)` ≈ 插件入口的初始化钩子——就像 Claude Code 插件加载时执行的那个初始化回调；`console.log` 打出的加载日志 ≈ 插件模块被 require/import 时打印的启动日志。它们共同证明一件事：**你的代码真的被宿主加载并执行了**。

### 2.3 写最小 patch yml：`- insert:` 注册

模块写好了，但 dsh 还不知道它的存在——`src/index.ts` 只是躺在文件系统里的一份文件。patch 文件就是「登记表」：用 `- insert:` 把插件注册进运行时的那张配置表。在 `git-log-plugin/` 根目录写 `dev-cordis.patch.yml`——文件放在插件目录里没问题，只要命令里给的是相对**仓库根目录**的完整路径（即 2.4 的 `./git-log-plugin/dev-cordis.patch.yml`）：

> [!tip] 大白话
> 把两个文件的分工想成「员工本人」和「前台登记表」：`src/index.ts` 是员工本人（会干活），patch yml 是登记表（写上「这号人今天来上班」）。只有登记过（`- insert:`），员工才会被叫去 apply；没登记，本事再大也白搭。

```yaml
# dev-cordis.patch.yml
- insert:
    - id: git-log
      name: '<你的 deepseek-harness 仓库绝对路径>/git-log-plugin/src/index.ts'
```

逐行看：

- `- insert:` — patch 的最小编排动作：「往配置表里插一行」。patch 文件就是一个动作列表，`- insert:` 是其中一种；这一章只用得到它。具体字段以官方最小骨架为准，见脚注 [^S1]。
- `- id: git-log` — 这一条目的实例 id，也就是四名分离的**第三个名字（patch id）**。它标识「这个实例」，和 `export const name` 的 `git-log-plugin` 是两回事：一个是「这个插件叫什么」，一个是「这张登记表里这一行叫什么」。
- `name:` — **关键**：必须填 `src/index.ts` 的**绝对路径**。把 `<你的 deepseek-harness 仓库绝对路径>` 换成你机器上的真实路径（macOS 形如 `/Users/你/deepseek-harness/git-log-plugin/src/index.ts`，Linux 形如 `/home/你/deepseek-harness/...`）。

为什么必须绝对路径：patch 的 `name` 会被加载器**直接当文件系统路径**去定位模块，它不会相对工作目录做任何换算[^S14]。写相对路径等于指了一个「在加载器眼里不存在」的地址。

> [!warning] 易错点：name 必须是绝对路径，相对路径静默失效
> 把 `name` 写成 `./git-log-plugin/src/index.ts` 或 `src/index.ts`，**不会报错，也不会警告**——只是模块永远加载不上，日志里永远没有 `[git-log-plugin] plugin loaded!`。这种「没报错的静默」是新手最容易被消耗时间的地方：你以为配置生效了，其实那行根本没被加载。第一步就写绝对路径，能省掉后面所有迷惑。

> [!tip] 大白话
> patch 里的绝对路径 `name` 像门禁卡必须写门牌号：你得写「楼栋 + 房间号」这种绝对地址。写相对路径等于拿一张写着「自己屋里」的门禁卡去刷——这栋楼里根本没有一间叫「自己屋里」的房间，刷了没反应，还不报错。所以：要么写 `src/index.ts` 的完整绝对路径，要么等第 6 章换成按包名安装的写法（bundle patch），那条路不用绝对路径。

### 2.4 加载命令：在仓库根目录跑 `pnpm dsh web --patch`

**先切回 dsh 源码仓库根目录**（`git-log-plugin/` 的上一级）再运行。`--patch` 的相对路径按**仓库根目录**解析，不是相对当前 shell 目录——文件在 `git-log-plugin/` 里，就得写相对根目录的完整路径 `./git-log-plugin/dev-cordis.patch.yml`；直接写 `./dev-cordis.patch.yml` 会去找 `<仓库根>/dev-cordis.patch.yml`，报 `ENOENT`：

```bash
# 在 dsh 源码仓库根目录执行（git-log-plugin/ 的上一级）
pnpm dsh web --patch ./git-log-plugin/dev-cordis.patch.yml
```

期望输出（时间戳/日志级别格式随版本略有差异，关键是那行 `[git-log-plugin] plugin loaded!`）：

```text
[12:00:01] INFO  loading plugin git-log (cordis)
[12:00:01] INFO  [git-log-plugin] plugin loaded!
[12:00:01] INFO  Web UI listening on http://127.0.0.1:3080
```

命令会一直前台运行（Web 服务）。看到三行日志后，浏览器打开 http://127.0.0.1:3080，在 Web UI 的日志/控制台面板里也能看到同样的 `[git-log-plugin] plugin loaded!`。验证完 `Ctrl+C` 退出即可。

三个必须讲清的要点：

1. **为什么命令必须在仓库根目录执行**：`--patch` 的相对路径按 **dsh 源码仓库根目录**解析（`loadOverlayPatches` 直接把它当文件系统路径），不是相对当前 shell 目录。所以即使文件在 `git-log-plugin/dev-cordis.patch.yml`，从插件目录里跑 `--patch ./dev-cordis.patch.yml` 也会解析成 `<仓库根>/dev-cordis.patch.yml` 而 `ENOENT`；正确写法是在根目录给全相对路径 `--patch ./git-log-plugin/dev-cordis.patch.yml`。开发期**不用 npx**——`pnpm dsh` 会向上找到 workspace 根部的 dsh CLI（即使从插件目录发起也能找到命令本体），但这只保证「命令找得到」，不保证「补丁路径指得对」。反过来，如果插件目录建在源码仓库**外面**，`pnpm dsh` 就连命令都找不到了[^S11]。
2. **`dsh web` 是 `dsh --profile web` 的硬编码别名**：`web` 不是某个参数值，是 CLI 层写死的快捷方式，含义是「用 web 这个 profile 跑起来并开 Web 服务」。想换 profile 就写 `dsh --profile <名字> --patch ...`，第 5 章会用到。
3. **为什么 patch 文件叫 `dev-cordis.patch.yml`**：大纲落定的命名——第一步就用 `dev-` 前缀，给第 5 步的打包 patch（bundle patch，`cordis.patch.yml`）留好命名空间，避免以后改名。现在这份就是「开发期手工挂载」的 dev patch，用 `--patch` 指定路径加载。

### 2.5 校准认知：「plugin loaded!」是插件自己的日志

重要校准：`[git-log-plugin] plugin loaded!` 这行**完全是插件自己写的**——就是 `src/index.ts` 里那句 `console.log`。dsh 只负责「找到模块 → 调用 apply」，它不会替你打任何带你自己名字前缀的日志，框架/CLI 里也不存在「加载插件就打印 hello」这种特性[^S1]。

这个认知直接决定排错方向：

- **看到这行** → 模块被加载了，`apply` 被调了，链路通。
- **没看到这行** → 先别怀疑 dsh，大概率是模块根本没被加载：检查 patch 的 `name` 绝对路径是否写对、`--patch` 是否在仓库根目录执行且路径写全（文件在插件目录下要带 `git-log-plugin/` 前缀，如 `./git-log-plugin/dev-cordis.patch.yml`）。对照 [[DeepSeek-Harness 常见坑与速查]] 里的排错顺序，第一步先查「登记表」，而不是查「dsh」。

> [!note] 这在 Claude Code 里相当于
> 插件被 require 时打的那条启动日志本来就是你写的，宿主不会替你发明日志——同理，`plugin loaded!` 这个文本是你 `console.log` 出来的，别把它当成 dsh 自带能力去依赖。哪天你想改这行字，改的是自己插件里的 `console.log`，而不是 dsh 的任何配置。

### 本章小结

- 最小 2 文件 = 插件模块 `src/index.ts` + 注册 patch `dev-cordis.patch.yml`，不依赖脚手架、不需要 `package.json`。
- `export const name`（`git-log-plugin`）是四名分离的**诊断名**；patch 的 `id`（`git-log`）是实例 id，两个名字不是一回事。
- patch 的 `name` 必须写 `src/index.ts` 的**绝对路径**，相对路径静默失效（无报错无警告）——第一步就写对，能避开最经典的排查陷阱。
- 加载命令在 **dsh 源码仓库根目录**执行 `pnpm dsh web --patch ./git-log-plugin/dev-cordis.patch.yml`：`--patch` 相对路径按仓库根目录解析，文件在插件目录里就要写相对根目录的完整路径，直接写 `./dev-cordis.patch.yml` 会 `ENOENT`；开发期不用 npx；`dsh web` 是 `--profile web` 的硬编码别名。
- `[git-log-plugin] plugin loaded!` 是插件自身的 `console.log`，不是 dsh 的特性；看不到它时先查 patch 路径，而不是怀疑 dsh。

下一步：插件能被加载了，但它还没有任何「能力」。第 3 章给它加第一个工具 `git_log`——把 `apply(ctx)` 升级成真正的注册中心，用 `ctx.tools.register` 把工具挂给模型。这两个文件会升级成三个文件，四名分离也从「知道」变成「落地」。

## 第 3 章：第 2 步——加工具 git_log

第 2 章的插件只能打印一行 `[git-log-plugin] plugin loaded!`，对模型来说它"存在但没用"。这一章我们把插件变成一个**真正能给模型干活**的插件：注册一个模型可见、可调用的工具 `git_log`。你会亲手写下 defineTool 五件套，理解 `execute` 的 canonical 值契约，并弄清楚为什么 `inject = ['tools']` 少写一行就会崩。这是全篇第一个"插件 ≠ 工具"的转折点。

### 3.1 文件归属：工具本体放 `src/tools/git-log.ts`，`src/index.ts` 做注册中心

第 2 章只有一个文件 `src/index.ts`。现在要加工具，第一个问题是"代码放哪"。沿用 [[DeepSeek-Harness 插件开发核心]] 的文件归属约定[^S13]：

- `src/index.ts`：**注册中心**。负责 `apply(ctx)`、声明 `inject`、把工具注册进 `ctx.tools`，以及打加载日志。它只做"组装"，不做具体业务。
- `src/tools/git-log.ts`：**工具工厂**。导出一个返回 `defineTool({...})` 结果的函数，例如 `gitLogTool()`。一个文件一个工具，工厂每次调用返回一个新实例，状态天然隔离。

先建目录（第 2 章只建过 `src/`，现在要新增 `tools/` 子目录，和 §2.2 的 `mkdir -p src` 一个套路）：

```bash
mkdir -p src/tools
```

为什么工具本体要写成"工厂函数"，而不是直接导出一个 defineTool 对象？因为注册发生在 `apply` 阶段，工厂把"定义"和"注册"分开：`git-log.ts` 只负责"这个工具长什么样"，`index.ts` 负责"在什么时候把它装进去"。这也是第 4 章把配置传进工厂的入口。

> [!note] 这在 Claude Code 里相当于
> `src/index.ts` ≈ 插件入口文件，负责初始化；`src/tools/*.ts` ≈ 独立拆出去的"工具定义 + 处理函数"模块，入口只管注册。

### 3.2 defineTool 五件套：name / description / parameters / output / execute

`defineTool` 是 dsh-tools 提供的工具描述 DSL，它收**一个**配置对象，对象里有五个字段[^S4]：

| 字段 | 作用 | 模型可见吗 |
| --- | --- | --- |
| `name` | 工具唯一标识，模型在对话里用它发起调用 | 是 |
| `description` | 一句话说明工具何时该用、怎么用 | 是 |
| `parameters` | 声明入参的结构与约束（类 JSON-schema） | 是 |
| `output` | 声明返回值的结构 + 怎么把结果渲染成文本 | 是（schema 部分） |
| `execute` | 真正干活的函数，接收已校验的 args，返回 canonical 值 | 否 |

`name` 就是我们一致性基线里模型可见的 `git_log`；`description` 写得越清楚，模型越不会在错误场景调用它；`parameters` / `output` 负责把"模型侧契约"和"代码侧契约"对齐；`execute` 是唯一有副作用的字段。

> [!note] 先睹为快：完整 `src/tools/git-log.ts`
> 下面整份代码就是这一章要写进 `git-log-plugin/src/tools/git-log.ts` 的**完整文件**。先整体扫一遍，看清五件套长在同一个 `defineTool({...})` 对象里；§3.3、§3.4 再逐段拆开讲，**每段都出自这份文件**。

```ts
// git-log-plugin/src/tools/git-log.ts
import { defineTool } from 'dsh-tools'
import { execFile } from 'node:child_process'
import { promisify } from 'node:util'

const execFileAsync = promisify(execFile)

export function gitLogTool() {
  return defineTool({
    name: 'git_log',
    description: '查看指定 Git 仓库最近的 5 次提交',
    parameters: {
      type: 'object',
      properties: {
        path: {
          type: 'string',
          description: '目标 Git 仓库的绝对路径',
          required: true, // 属性级 required 布尔
        },
      },
    },
    output: {
      schema: {
        type: 'object',
        properties: {
          commits: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                hash: { type: 'string' },
                message: { type: 'string' },
              },
            },
          },
        },
      },
      render(value) {
        // value 是 execute 返回的 canonical 值；这里才做"给人看"的排版
        const lines = value.commits.map((c) => `${c.hash} ${c.message}`)
        return [{ type: 'text', text: lines.join('\n') || '(no commits)' }]
      },
    },
    async execute(args) {
      try {
        const { stdout } = await execFileAsync('git', ['log', '--oneline', '-n', '5'], {
          cwd: args.path,
        })
        const commits = stdout
          .trim()
          .split('\n')
          .filter(Boolean)
          .map((line) => {
            const [hash, ...rest] = line.split(' ')
            return { hash, message: rest.join(' ') }
          })
        // ✅ 业务成功态：返回 canonical 值，框架按 output.schema 序列化
        return { commits }
      } catch (err) {
        // ✅ 基础设施失败：throw = isError，注册表捕获，不泄漏给模型
        throw new Error(`git log 执行失败: ${(err as Error).message}`)
      }
    },
  })
}
```

这一章要新建的文件只有这一个：`src/tools/git-log.ts`（先建 `tools/` 子目录）。它**只导出 `gitLogTool` 工厂**，不含任何注册逻辑——怎么把它装进插件，由 §3.5 的 `src/index.ts` 完成。

> [!tip] 大白话：defineTool 是给机器人写岗位说明书
> 把 defineTool 想成「给机器人写一份岗位说明书」：名字（`name`）写在工牌上，职责（`description`）写清楚什么时候叫它，输入输出格式（`parameters`/`output`）是交接班的单据模板。机器人读到说明书就知道自己是什么岗位。而 `execute` 是「真干活的人」——它不需要操心怎么排版汇报，只要把结果按单据格式交回去就行。

> [!note] 这在 Claude Code 里相当于
> Claude Code 插件里 `tools` 数组的每一项：`name`/`description`/`parameters` 声明工具元数据，外加一个处理函数负责实际调用。`defineTool` 只是把"元数据 + 处理函数"打包成一条更严格的 DSL。

### 3.3 parameters 与 output：类 JSON-schema；output.schema + output.render

`parameters` 写在 `src/tools/git-log.ts` 的 `defineTool({...})` 里（完整文件见 §3.2「先睹为快」）。它是**类 JSON-schema** 结构：顶层 `type: 'object'`，`properties` 里每个属性用 `{ type, description, required }` 描述，其中 `required` 是**属性级的布尔值**，而不是 JSON-schema 传统的数组[^S4]：

```ts
parameters: {
  type: 'object',
  properties: {
    path: {
      type: 'string',
      description: '目标 Git 仓库的绝对路径',
      required: true, // 属性级 required 布尔
    },
  },
},
```

`output` 同样写在 `defineTool({...})` 里，由两部分组成[^S4]：

- `output.schema`：声明 `execute` 返回的 **canonical 值**长什么样，同样用类 JSON-schema。框架用它对返回值做校验与序列化。
- `output.render(value)`：把 canonical 值**转换**成给模型/界面展示的文本块 `[{ type: 'text', text: value }]`。canonical 值负责"机器可读"，render 负责"人可读"，两者职责分开。

```ts
output: {
  schema: {
    type: 'object',
    properties: {
      commits: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            hash: { type: 'string' },
            message: { type: 'string' },
          },
        },
      },
    },
  },
  render(value) {
    // value 是 execute 返回的 canonical 值；这里才做"给人看"的排版
    const lines = value.commits.map((c) => `${c.hash} ${c.message}`)
    return [{ type: 'text', text: lines.join('\n') || '(no commits)' }]
  },
},
```

有个省力点值得记住：`parameters` 的 schema 会**自动流入系统提示词的组装**，`description` 也会被模型读到，所以你不需要在 `description` 里手工复述参数格式——否则既重复、又容易在两处改漏[^S5]。

> [!tip] 大白话：canonical 值 vs render
> `execute` 像仓库管理员，只交「入库单」（结构化数据，canonical 值）；`render` 像前台文员，把入库单誊成给老板看的报表。管理员绝不该自己写报表——否则换个展示形式（终端、Web UI、JSON）就全乱了。

### 3.4 execute(args) 契约：返回唯一 canonical JSON 值；抛错 / 非法值 = isError

`execute` 是五件套里唯一"干活"的字段，写在 `src/tools/git-log.ts` 的 `defineTool({...})` 里（完整文件见 §3.2「先睹为快」），它的契约是整个框架正确性的关键[^S4][^S5]：

1. **返回唯一 canonical JSON 值**：`execute(args)` 必须返回 `output.schema` 声明的那一个 JSON 值（我们的例子是 `{ commits: [...] }`），**不返回内容块**。框架拿到返回值后按 `output.schema` 序列化，再丢给 `output.render` 渲染。你如果在 `execute` 里提前返回 `[{ type: 'text', ... }]`，那是个数组，和 `output.schema` 对不上，会被判为非法值。
2. **`args` 是只读、已校验的**：框架根据 `parameters` schema 推断 `args` 类型、调用前自动校验；你的代码里不要改它。
3. **抛错 / 返回非法值 = isError**：注册表会捕获 `execute` 抛出的异常，标记为 `isError` 返回给上层，**不会把堆栈泄漏给模型**。
4. **基础设施失败要 `throw`**：git 没装、目录不是仓库、命令超时——这些是"环境问题"，不是"业务结果"，必须 `throw`，让框架标记失败。
5. **业务成功态放 canonical 值**：git 跑通了但仓库没有任何提交，这不是失败，返回 `{ commits: [] }` 即可——空结果也是成功。

```ts
async execute(args) {
  try {
    const { stdout } = await execFileAsync('git', ['log', '--oneline', '-n', '5'], {
      cwd: args.path,
    })
    const commits = stdout
      .trim()
      .split('\n')
      .filter(Boolean)
      .map((line) => {
        const [hash, ...rest] = line.split(' ')
        return { hash, message: rest.join(' ') }
      })
    // ✅ 业务成功态：返回 canonical 值，框架按 output.schema 序列化
    return { commits }
  } catch (err) {
    // ✅ 基础设施失败：throw = isError，注册表捕获，不泄漏给模型
    throw new Error(`git log 执行失败: ${(err as Error).message}`)
  }
}
```

反着写是三个最典型的错误：

```ts
// ❌ 错误 1：execute 返回内容块，而不是 canonical 值
async execute(args) {
  const commits = await readCommits(args.path)
  return [{ type: 'text', text: commits.join('\n') }] // 数组 ≠ output.schema 声明的对象 → isError
}

// ❌ 错误 2：把失败塞进返回值，而不是 throw
async execute(args) {
  try {
    return { commits: await readCommits(args.path) }
  } catch (err) {
    return { commits: [], error: String(err) } // 字段超纲 + 掩盖失败，模型会误以为成功
  }
}

// ❌ 错误 3：吞掉错误返回空结果
async execute(args) {
  try {
    return { commits: await readCommits(args.path) }
  } catch {
    return { commits: [] } // 基础设施失败被伪装成"没有提交"
  }
}
```

另一个注册即生效的细节：`ctx.tools.register` 是**注册即 effect**，插件 fiber 卸载时工具会自动注销，你不用手动清理[^S5]。

> [!tip] 大白话：为什么 execute 不能自己排版
> 把 execute 想成流水线上的工人：他的活儿是「做出零件」（canonical 值），质检（`output.schema`）负责验收，包装（`output.render`）负责装箱。工人如果既做零件又自己写包装箱，质检就形同虚设——这次是纸箱、下次是木箱，下游全乱了。所以「只交零件，不碰包装」。

### 3.5 index.ts 升级：inject = ['tools'] + ctx.tools.register(...)

工具写好了，还要在 `src/index.ts` 里注册。注册动作两件事：声明 `inject = ['tools']`，然后 `ctx.tools.register(...)`[^S4]。

```ts
// src/index.ts
import type { Context } from '@deepseek-ai/cordis'
import { gitLogTool } from './tools/git-log'

export const name = 'git-log-plugin' // 诊断名：加载日志用

// 关键：声明依赖 'tools'，框架会先初始化工具注册表再调 apply
export const inject = ['tools']

export function apply(ctx: Context) {
  // 到这里 ctx.tools 一定可用（inject 保证）
  ctx.tools.register(gitLogTool())
  console.log('[git-log-plugin] plugin loaded!')
}
```

`inject` 是 cordis 的依赖注入声明。写 `['tools']` 的意思是"我的 `apply` 需要工具注册表就绪才能跑"，框架会保证执行顺序。**少写这一行会怎样？** `ctx.tools` 是 `undefined`，`ctx.tools.register(...)` 直接抛 `Cannot read properties of undefined`——而且是在加载阶段炸，插件起不来。这类错误发生在 apply 里，比工具执行时抛错更难排查，因为看起来像"框架崩了"。

> [!note] 这在 Claude Code 里相当于
> `inject = ['tools']` ≈ 插件初始化时显式声明"我需要工具注册表这个依赖"，拿到一个注册表引用来注册自己的工具。区别是 Claude Code 里注册顺序更宽松，而 cordis 用 `inject` 把顺序契约写死了。

### 3.6 四名分离落地

现在你的工程里已经有多个名字在同时流动，把它们钉死才不会在第 6、7 章打包安装时翻车。这一章真正"活"的名字有两个，另外两个会在后续章节出现，先建立完整心智模型[^S11]：

| 名字       | 固定值                  | 出现位置                                        | 本章状态        |
| -------- | -------------------- | ------------------------------------------- | ----------- |
| 诊断名      | `git-log-plugin`     | `export const name`，加载日志 `[git-log-plugin]` | ✅ 已用（第 2 章） |
| 包名       | `dsh-git-log-plugin` | package.json `name`                         | ⏳ 第 6 章     |
| patch id | `git-log`            | patch yml 的 `- insert: id`                  | ✅ 已用（第 2 章） |
| 工具名      | `git_log`            | `defineTool.name`，模型可见                      | ✅ 本章新增      |

记住一句话：**`git-log-plugin` ≠ `dsh-git-log-plugin` ≠ `git-log` ≠ `git_log`**。前三个连字符命名各管各的（日志 / 包 / 补丁实例），只有 `git_log` 是下划线命名且直接暴露给模型。工具名是模型和你的代码之间的协议，一旦发布再改，所有依赖它的对话历史都会失效——所以 `git_log` 从这一章起就是冻结值，和 [[DeepSeek-Harness 插件实战]] 保持同一基线[^S11]。

## 本章小结

- 文件归属：工具本体放 `src/tools/git-log.ts`（工厂导出），`src/index.ts` 只做注册中心，职责分离（[^S13]）。
- `defineTool` 五件套：`name` / `description` / `parameters` / `output` / `execute`；`parameters` 用属性级 `required` 布尔，`output` 拆成 `schema`（canonical 值结构）+ `render`（转文本块）（[^S4]）。
- `execute` 契约：返回 `output.schema` 声明的**唯一 canonical JSON 值**，不返回内容块；基础设施失败 `throw`（=isError，注册表捕获不泄漏给模型），业务成功态放 canonical 值（[^S5]）。
- `src/index.ts` 升级：`export const inject = ['tools']` + `ctx.tools.register(gitLogTool())`；漏写 `inject` 会让 `ctx.tools` 为 `undefined`，加载阶段直接崩。
- 四名分离落地：`git-log-plugin`（诊断）≠ `dsh-git-log-plugin`（包）≠ `git-log`（patch id）≠ `git_log`（模型可见工具名），`git_log` 从本章起冻结。

下一章，我们会给 `git_log` 加一个可调参数 `maxCommits`——届时 execute 里那句写死的 `-n 5` 会换成读取配置，正式引入 Config schema，把 [[DeepSeek-Harness 插件开发核心]] 的"插件 ≠ 工具"再往"可配置"推一步。

## 第 4 章：第 3 步——加 Config 可调参数

第 2 章让插件被加载、第 3 章给它装上了工具 `git_log`。可 `git_log` 现在一次只会看最近 5 条提交——用户想改成 10 条，难道要改代码重新加载？这章解决的就是「不改代码也能调参数」：给插件加可配置项 `maxCommits`，通过 patch 的 `config` 块传值、在 apply 里读取。这正是 dsh 插件与一段硬编码脚本的分水岭：任何「两个部署可能想要不同值」的东西，都应该是配置字段，而不是写死的常量[^S6]。

### 4.1 Config 两段式：`export interface Config` + `export const Config`

插件的配置项由「两个同名导出」共同声明：`export interface Config` 描述类型，`export const Config: Schema<Config> = Schema.object({...})` 描述运行时校验与默认值[^S6]。类型只在编译期存在、会被擦除；schema 在插件加载时真实运行。两者同名，dsh 的 patch loader 拿到运行时校验器，你写代码时拿到类型提示[^S7]。

```ts
// src/index.ts（新增部分；name 与 apply 第 2、3 章已有）
import type { Context } from '@deepseek-ai/cordis'
import Schema from '@deepseek-ai/schemastery'   // 新增依赖

export interface Config {
  maxCommits: number
}

export const Config: Schema<Config> = Schema.object({
  maxCommits: Schema.number().default(5),
})
```

注意两点。第一，`Schema.object({...})` 的返回值要标注成 `Schema<Config>`，让每个字段和 interface 互相核对，写错字段名或类型在编译期就能暴露。第二，**不要导出普通对象作 Config**：`export const Config = { maxCommits: 5 }` 只是个 plain object，没有实现 Standard Schema 接口，Cordis 无法用它校验，插件不会被正确加载[^S6][^S7]。第二段必须是 `Schema.object({...})` 这类校验器。

> [!tip] 大白话
> 把 schema 想成一张「配置体检表」。插件加载时先体检：字段名、类型对不对？缺的项用默认值补上？全部合格才放行开工。不合格直接拒之门外，绝不让你带病半启动——4.6 会看到被拒时报错长什么样。

> [!note] 这在 Claude Code 里相当于
> 插件入口里声明 settings schema（用 zod 校验）：类型与运行时校验合在一个定义里，读配置的代码永远拿到的都是「已验证」的值。

### 4.2 默认值写 schema：`Schema.number().default(5)`

关键约定：**默认值写在 schema 上，不写在业务逻辑里**[^S6]。`Schema.number().default(5)` 表示「这是一个 number，调用方没传时自动填 5」。于是 patch 里漏传 `maxCommits`，插件照样拿到 5；传了就优先用传的值。官方给的判断标准很直接：`cordis.yml`（或 patch）能不能不改代码就改变这个值——能，它才配叫配置字段；不能，就该把它做成配置项[^S6]。反例是 `const LIMIT = 5` 这种硬编码常量。

> [!note] 这在 Claude Code 里相当于
> `Schema.number().default(5)` ≈ `z.number().default(5)`：默认值由校验器统一管理，读配置时永远有值，业务代码不需要再写 `?? 5` 这种兜底。

### 4.3 校准注记：必填用 `.required()`，不用 `.required(true)` / `.optional()`

schema 里的字段默认都是可选的。必填的字段用 `.required()` 显式标记；可选的字段在 interface 层用 TS 的 `?` 表示，**不要**在 schema 上写 `.optional()`。官方从不用 `.required(true)` 这种带参数的写法[^S6]。

```ts
export const Config: Schema<Config> = Schema.object({
  apiKey: Schema.string().required(),     // 必填：缺了直接校验失败
  maxCommits: Schema.number().default(5), // 可选：不写 .required()，且有默认值
})
```

> [!warning] 校准注记（与《插件实战》§4 的口径差异）
> 本地 [[DeepSeek-Harness 插件实战]] §4 的口径是「无 `.optional()`，必填用 `.required(true)`」[^S11]。官方 O6 明确：必填一律 `.required()`，从不用 `.required(true)` 或 `.optional()`。本篇以官方为准，对照旧笔记时请留意这一处差异。

| 写法 | 含义 | 本篇 |
| --- | --- | --- |
| `.required()` | 必填 | 采用（官方口径） |
| `.required(true)` | 必填 | 不用（旧笔记写法） |
| `.optional()` | 可选 | 不用（官方从不用） |
| TS `?` | 可选 | 采用（interface 层） |

### 4.4 在 patch 的 `config` 块传值

配置值不写在代码里，而是由 patch 的 `config` 块传进来。回到第 2 章的 `dev-cordis.patch.yml`，给 `git-log` 条目补上 `config`，键名与 interface 字段一一对应[^S6]：

```yaml
# dev-cordis.patch.yml（开发期，用 --patch 加载）
- insert:
    - id: git-log
      name: '/Users/me/git-log-plugin/src/index.ts'   # 绝对路径（第 2 章）
      config:
        maxCommits: 10   # 覆盖 schema 默认的 5
```

`config` 是插件条目下与 `id` / `name` 同层的一个块。这一步先只改 dev patch；第 5 步把 bundle patch（`cordis.patch.yml`，其 `name` 将是包名 `dsh-git-log-plugin`）定型时，把同一份 `config` 块原样复制过去——两份 patch 传值的位置完全一致，装成包后用户也在同一个位置配置[^S11]。

### 4.5 apply 里读取完整校验后的 config

插件加载时 schema 先跑一遍；校验通过后，Cordis 把「填好默认值、校验过的完整 config」作为 apply 的第二参数传进来[^S7]：

```ts
export function apply(ctx: Context, config: Config) {
  // config 已校验 + 已填默认值，直接读
  const limit = config.maxCommits
  ctx.tools.register(gitLog(ctx, config))   // 整个 config 传给第 3 章的工具工厂
  console.log(`[git-log-plugin] plugin loaded! maxCommits=${limit}`)
}
```

核心认知：**apply 总收到完整校验后的 config**[^S7]。patch 漏传 `maxCommits`，它自动被 `default(5)` 填成 5；patch 传 `10`，到手就是 10。所以 apply 里不需要、也不应该再手写一遍 config 校验——那是 schema 的活，重复校验既啰嗦，又容易和 schema 口径不一致。官方文档里 config 始终以 apply 第二参数的形式出现（O6、O7 都是 `apply(ctx, config)`）；若在旧资料里看到 `ctx.config` 的写法，那是早期框架的习惯，本篇按官方签名来。

> [!note] 这在 Claude Code 里相当于
> patch 的 `config` 块 ≈ 在 settings.json 里给插件写配置；apply 第二参数收到的 config ≈ 插件初始化时框架注入的「默认值 + 用户覆盖」合并结果。

### 4.6 坏配置行为：ValidationError / fiber FAILED / 永不半启动

把 config 传错，插件不会带病运行——schema 在插件加载时就执行，坏配置直接让加载失败[^S6][^S7]：

```yaml
# dev-cordis.patch.yml —— 故意传错类型
- insert:
    - id: git-log
      name: '/Users/me/git-log-plugin/src/index.ts'
      config:
        maxCommits: 'ten'   # 错：number 字段传了字符串
```

加载时 dsh 打印：

```text
ValidationError: invalid config:
  - $.maxCommits expected number but got string (at maxCommits)
```

随后这个插件的 fiber 进入 FAILED，加载流程报错退出，插件**永不半启动**[^S7]。好处是配置错误在加载那一刻就被精确抓出，而不是运行到一半才诡异崩掉，或带着错误配置静默跑很久。这也是 [[DeepSeek-Harness 配置体系]] 里「fail loud」原则的落地。

> [!tip] 大白话
> 还是那张「配置体检表」。你填「身高：十厘米」这种明显不合格的项，体检当场打回、贴出不合格单（ValidationError），连门都不让进（fiber FAILED）。绝不会出现「先进来上班、干着干着才发现不合格」的半启动状态。

## 本章小结

- Config 是「两段式」：`export interface Config` 管类型，`export const Config: Schema<Config> = Schema.object({...})` 管运行时校验与默认值，两者同名。
- 默认值写在 schema 上：`Schema.number().default(5)`，patch 漏传时自动补默认值，业务逻辑不写兜底。
- 必填用 `.required()`；官方从不用 `.required(true)` 或 `.optional()`，可选用 TS `?`（与《插件实战》§4 旧口径不同，以官方为准）。
- 传值走 patch 的 `config` 块；dev patch 与 bundle patch 传值位置一致。
- apply 的第二参数就是完整校验后的 config，直接读、别二次校验；坏配置 → ValidationError / fiber FAILED，永不半启动。

配置能声明、能传、能读了，可怎么确认它真的生效、又落在哪一层？下一章用 `--dump-config` 把分层配置一张张打出来验一遍。

## 第 5 章：第 4 步——验证命令链

写到这里，`git_log` 工具和 `maxCommits` 配置都「写出来了」，但**写出来不等于跑通了**。这一章用 dsh 自带的四条验证命令，把三件事分别验清楚：插件有没有被加载、配置最终落在哪一层、端到端能不能用。这是全篇最值得真机完整跑一遍的部分——后面第 6 步打包、安装出了问题，都要回到这几条命令来定位。

### 5.1 复跑 `pnpm dsh web --patch ./git-log-plugin/dev-cordis.patch.yml`：确认 `[git-log-plugin] plugin loaded!`

从第 2 章到第 4 章，`src/index.ts` 里已经注册了 `git_log` 工具、加了 `maxCommits` 配置，`dev-cordis.patch.yml` 里也补上了对应的 `config` 块。加载命令和之前完全一样，仍然在 **dsh 源码仓库根目录**执行（开发期不用 npx；命令根目录、绝对路径这些坑清单见 [[DeepSeek-Harness 常见坑与速查]]）[^S11]：

```bash
pnpm dsh web --patch ./git-log-plugin/dev-cordis.patch.yml
```

启动后终端应再次看到插件自身的加载日志：

```text
[git-log-plugin] plugin loaded!
```

注意：这条日志是 `src/index.ts` 里 `console.log` 打出来的，不是 dsh 框架/CLI 的功能（第 2 章校准过）。`dsh web` 是 `--profile web` 的硬编码别名，方便本地起一个带 Web UI 的开发实例[^S8]。看到日志只说明「模块被加载了」，工具和配置到底对不对，要靠下面三条命令。

### 5.2 `dsh --profile demo --dump-config`：分层打印（bundle 各层 → profile patch → home 级 → `--patch` 叠加）

dsh 的配置不是单个文件，而是**四层补丁树**叠出来的：bundle 各层（按列表序）→ profile patch → home 级 → `--patch` 叠加，后层对前层做整行替换、不做字段级深合并[^S8]。想知道某条配置最终从哪一层来、合并成什么样，用 `--dump-config` 看全量：

```bash
# --dump-config 打印全量分层；加 --patch 把开发期补丁作为最顶层叠进来
# （不加的话，还在开发中的 git-log 层看不到）
dsh --profile demo --dump-config --patch ./git-log-plugin/dev-cordis.patch.yml
```

输出按层打印，每层都带来源文件注释，大致长这样（示意，实际输出以你的环境为准）：

```yaml
# from bundle 层（列表序，最低）
# from <harness-home>/profiles/demo/cordis.patch.yml   ← profile patch 层
# from <harness-home>/cordis.yml                        ← home 级
# from ./git-log-plugin/dev-cordis.patch.yml              ← --patch 叠加（最顶层）
- insert:
    - id: git-log
      name: <绝对路径>/src/index.ts
      config:
        maxCommits: 5
```

逐层核对下来，你能看到 `git-log` 这条来自 `--patch` 层、`maxCommits` 最终等于 5。四层补丁树的完整心智模型见 [[DeepSeek-Harness 配置体系]]。

> [!tip] 大白话
> 把 `--dump-config` 想成「验房验收单」——每层配置像每道工序（水电、木工、油漆），验收单按施工顺序一层层打勾，最后这张单子就是房子的最终状态。所以它能直接告诉你：`git-log` 是哪个文件贡献的、`maxCommits` 最终等于几。

### 5.3 `dsh --profile demo --dump-default-config`：只看 bundle 层（不含 profile/home/patch）

这条和 5.2 一字之差，含义**相反**。`--dump-default-config` 只看 bundle 层，不含 profile patch、home 级，也不含 `--patch` 叠加[^S8]：

```bash
dsh --profile demo --dump-default-config
```

它回答的是「各 bundle 作者默认贡献了什么配置」，与用户侧任何定制无关。开发期你的 `dev-cordis.patch.yml` 还没打进 bundle，所以这条命令里看不到 `git-log` 是**正常的**；等第 6 章工程化、把补丁打进包之后，再跑它就能核对「我这个包到底声明了哪一层配置」。

> [!warning] 别搞反
> `--dump-config` = 全层（含 profile / home / `--patch`）；`--dump-default-config` = 只看 bundle 层。两个命令只差一个词，用途完全不同。

> [!note] 这在 Claude Code 里相当于
> `--dump-config` / `--dump-default-config` 类似 `claude config list` 这类「看合并后配置」的调试手段——排查「我改的配置到底生效没有」时，先看合并结果，而不是凭感觉猜。

### 5.4 `dsh --profile headless "<task>"`：一次性任务端到端，stdout 打印文本，退出码 **0 = completed / 1 = otherwise**；无任务文本 = usage 错误

前三条验「加载」和「配置」，这条验「端到端能不能用」。headless 模式直接执行一个一次性任务，结果文本打印到 stdout：

```bash
dsh --profile headless "用 git_log 工具查看当前仓库最近的 5 次提交"
echo $?
# 0  ← 上一条命令的退出码
```

成败只看退出码[^S8]：

| 退出码 | 含义 |
| --- | --- |
| 0 | completed（任务完成） |
| 1 | otherwise（失败 / 异常 / usage 错误） |

headless 也是 dsh 自动初始化 profile 的入口之一（缺 profile 时按模板建），所以就算 `demo` profile 还没手动建过，这一条也能直接跑通[^S8]。**关键坑：无任务文本是 usage 错误**，不是「正常返回」：

```bash
dsh --profile headless
# usage 错误：缺少任务文本，退出码为 1（otherwise）
```

> [!tip] 大白话
> headless 的退出码 0/1 像验收时盖的章——0 是「验收合格」，1 是「不合格」。脚本里可以直接 `if dsh --profile headless "任务"; then ...` 当布尔判断用，放进 CI 或批处理都很顺手。

> [!note] 这在 Claude Code 里相当于
> headless 的 0/1 退出码约定，和所有 CLI 命令一致——脚本判断成功失败看退出码，而不是去解析 stdout 文本。

### 5.5 读 dump 输出的要点：文件名注释、`!!js` 不求值、stderr 报未命中

真跑起来之后，读 dump 输出记住三个要点[^S8]：

1. **文件名注释**：每层输出前都有 `# from ...` 注释标明来源文件，「这条配置谁定义的」靠它定位。
2. **`!!js` 不求值**：dump 是诊断视图，遇到 `!!js` 这类 YAML 标签会**原样打印、不求值**；它只在 dsh 真正加载配置、执行对应代码时才有意义，别把 dump 里的原样标签当成运行时值。
3. **未命中走 stderr**：查找某条配置/条目未命中时，dsh 把提示打到 **stderr** 而不是 stdout。排查时别只盯 stdout——把 `2>&1` 或终端报错区一起看了才完整。

把四条命令串起来，就是这张验证速查表：

| 要验证什么          | 用哪条命令                                                                            |
| -------------- | -------------------------------------------------------------------------------- |
| 插件被加载          | `pnpm dsh web --patch ./git-log-plugin/dev-cordis.patch.yml`                     |
| 配置合并成什么样       | `dsh --profile demo --dump-config --patch ./git-log-plugin/dev-cordis.patch.yml` |
| bundle 默认贡献了什么 | `dsh --profile demo --dump-default-config`                                       |
| 端到端能不能用        | `dsh --profile headless "<task>"`                                                |

### 本章小结

- 四条验证命令分工明确：`dsh web --patch` 验「加载」，`--dump-config` 验「配置落在哪一层」，`--dump-default-config` 验「bundle 默认贡献」，headless 验「端到端」。
- `--dump-config` 是全层（bundle → profile → home → `--patch`），`--dump-default-config` 只看 bundle 层——别搞反。
- headless 退出码 0 = completed、1 = otherwise；无任务文本是 usage 错误，不是正常返回。
- dump 输出带文件名注释、`!!js` 不求值、未命中配置走 stderr。
- 命令统一在 dsh 源码仓库根目录执行，开发期不用 npx。

验证通过，插件在开发态就「能用」了。但它现在还依赖源码仓库和绝对路径，不是一个正经可分发的东西——下一章我们把插件工程化补齐（package.json + tsconfig + build 产出 `dist/`），为第 6 步打包安装铺路。

## 第 6 章：第 5 步——工程化补齐

前四步我们从空目录一路写到了 `src/index.ts`（注册中心）、`src/tools/git-log.ts`（工具）和 `dev-cordis.patch.yml`（开发期补丁），插件已经能在 `dsh web --patch` 下加载。但严格说，它还是一堆能跑的 TypeScript 文件——没有 `package.json` 的目录不具备「被安装、被打包、被发布」的资格。第 5 步就是补上工程化三件套：`package.json`（含依赖双份与 files 白名单）、`tsconfig.json`、双 patch（dev + bundle），让项目从「手工作坊」升级成「流水线」。

> [!note] 本章要创建 / 生成哪些文件
> 手写 **3 个新文件** + **2 个生成物**，全部落在 `git-log-plugin/` 目录内：

| 文件                 | 类型   | 作用                                                      | 小节   |
| ------------------ | ---- | ------------------------------------------------------- | ---- |
| `package.json`     | 新增手写 | 工程声明：name / main / types / `dsh.bundle.patch` / scripts | §6.1 |
| `tsconfig.json`    | 新增手写 | 编译配置：ES2022 / ESNext / Bundler / strict                 | §6.2 |
| `cordis.patch.yml` | 新增手写 | bundle patch：`name` = 包名，随包发布                           | §6.3 |
| `pnpm-lock.yaml`   | 生成   | 依赖锁文件（`pnpm install` 产出）                                | 构建一节 |
| `dist/`            | 生成   | 构建产物（`pnpm run build` 产出）                               | 构建一节 |

**沿用不新建**：`src/index.ts`（第 2/3 章）、`src/tools/git-log.ts`（第 3 章）、`dev-cordis.patch.yml`（第 2 章，§6.3 定型为 dev 版）。

> [!tip] 大白话
> 工程化像给手工作坊上流水线：`package.json` 是营业执照（注册身份、声明经营范围），`tsconfig` 是生产标准（统一怎么编译），`npm run build` 是出厂质检（产出 `dist/` 合格品）。没有这些，产品再能用也进不了市场。

### 6.1 package.json：工程声明（最小字段 / 依赖双份 / files 白名单）

package.json 一个文件里装三件事：**最小字段**（身份与入口）、**依赖双份**（peer + dev）、**files 白名单**（发布带什么）。下面依次讲。

#### 6.1.1 最小字段

在插件目录根新建 `package.json`。独立插件的最小字段（[^S10]）如下：

```json
{
  "name": "dsh-git-log-plugin",
  "version": "0.1.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "dsh.bundle.patch": "./cordis.patch.yml",
  "files": ["dist", "cordis.patch.yml"],
  "scripts": {
    "build": "tsc",
    "prepare": "npm run build"
  },
  "peerDependencies": {
    "cordis": "*",
    "dsh-tools": "*",
    "schemastery": "*"
  },
  "devDependencies": {
    "cordis": "*",
    "dsh-tools": "*",
    "schemastery": "*",
    "typescript": "^5.0.0"
  }
}
```

逐字段看，最关键的是前五个：

| 字段                 | 值                    | 作用                                             |
| ------------------ | -------------------- | ---------------------------------------------- |
| `name`             | `dsh-git-log-plugin` | 包名，全篇四名分离里的「包」；**bundle patch 的 `name` 必须等于它** |
| `version`          | `0.1.0`              | 语义化版本，打包 / 发布必需                                |
| `main`             | `dist/index.js`      | Node 解析这个包的入口——必须是**编译产物**，不是 `src/index.ts`   |
| `types`            | `dist/index.d.ts`    | 类型入口，配合 `declaration` 由 tsc 自动产出               |
| `dsh.bundle.patch` | `./cordis.patch.yml` | **声明自己是 dsh 插件**的字段，指向随包发布的 bundle 补丁          |
| `scripts.build`    | `tsc`                | 编译命令                                           |
| `scripts.prepare`  | `npm run build`      | 安装 / 发布前自动先构建——这是第 7 章 git 源安装「自包含构建」的前提       |

`dsh.bundle.patch` 是这个包能被 dsh 识别为 bundle 的关键：dsh 安装一个 bundle 时读这个字段找到补丁文件，把它作为一层配置合并进去。没有它，包只是普通 npm 依赖。

注意这里出现的是四名分离里的第二个名字：`export const name = 'git-log-plugin'`（诊断 / 日志）≠ `dsh-git-log-plugin`（包，本节）≠ `git-log`（patch id / 实例）≠ `git_log`（defineTool 的模型可见工具名）。四个名字各管一段，后面小节会逐个用到（尤其 §6.3 双 patch 定型时的包名）。

> [!note] 这在 Claude Code 里相当于
> 任何 npm 插件 / CLI 工程都有的 `main` / `types` / `files` 字段，Claude Code 插件同样要声明入口；`dsh.bundle.patch` ≈ 在包里写一句「我是 dsh 插件，这是我的激活清单」，相当于 Claude Code 插件里的激活 / manifest 声明。

#### 6.1.2 依赖双份：cordis / dsh-tools / schemastery

插件源码里用到三个核心包：`cordis`（插件框架运行时）、`dsh-tools`（工具 DSL / 注册辅助）、`schemastery`（Config schema）。它们**同时出现在 peerDependencies 和 devDependencies**（[^S10]）：

- **peerDependencies**：声明「运行时靠宿主提供什么」。dsh 宿主环境已自带这三者，插件不该再打包一份重复副本，否则会出现「框架是 A 版、插件用 B 版」的版本割裂。
- **devDependencies**：声明「构建时需要装什么」。`src/` 直接 import 它们，`tsc` 编译时必须能解析到类型和符号，所以开发目录里也要有一份实例。

> [!tip] 大白话
> 双份依赖像「简历里写会用 Excel（peer，声明能力）+ 自己电脑上真装了 Excel（dev，干活要用）」。宿主提供的是工作电脑里的 Excel，你编译时用的是自己装的那份——两边都要有。

版本号不要照抄：`*` 是占位，要和你的 dsh 源码仓库 `pnpm-lock.yaml` 实际解析到的版本对齐（源码仓库内 `dsh-tools` 通常以 `workspace:*` 形式存在）。另外 `scripts.build` 用的是 `tsc`，所以 `typescript` 进 `devDependencies`（生产环境不需要编译器，不进 peer）；如果工具用到 Node 内置模块（如 `child_process` 跑 `git log`），再补 `@types/node`。

#### 6.1.3 files 白名单：只发布该带的

`files: ["dist", "cordis.patch.yml"]` 声明「打进 tarball 的只有这两样」（[^S10]）：

- `dist/`：编译产物，`main` / `types` 都指向这里，消费者只需要产物，不需要 `src/`。
- `cordis.patch.yml`：bundle patch，`dsh.bundle.patch` 指向的文件必须在包里。
- **不在**白名单里的 `dev-cordis.patch.yml`、`src/`、`tsconfig.json` 都不会进包：dev patch 里是机器相关的绝对路径，打进包既无意义，装到别的机器还容易误触发。

> [!tip] 大白话
> files 白名单像登机行李清单：只带 `dist/`（成品）和 `cordis.patch.yml`（激活卡）上飞机，`src/`（图纸）和 `dev-cordis.patch.yml`（本地临时工牌）留在家里。清单外一律不托运，装包体积小、也少泄密。

`package.json` 的三个子节到此齐了：**最小字段（6.1.1）→ 依赖双份（6.1.2）→ files 白名单（6.1.3）**。下一个文件是 `tsconfig.json`——它决定 `dist/` 怎么从 `src/` 产出。

### 6.2 tsconfig：一份能产出 dist/ 的编译配置

新建 `tsconfig.json`。独立插件的最小配置（[^S10]）：

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true
  },
  "include": ["src"]
}
```

各字段为什么这么设：

- `target: ES2022`：输出语法级。插件跑在 Node 端，ES2022 覆盖现代 Node 语法，不必降级。
- `module: ESNext` + `moduleResolution: Bundler`：源码用 ESM 的 `import` / `export` 写，输出保持 ESM 模块形态，并让 tsc 按 Bundler 模式解析依赖。
- `declaration: true`：编译时同时产出 `.d.ts`——对应 `package.json` 的 `types`。
- `outDir: dist` + `rootDir: src`：`src/` 结构原样映射到 `dist/`，把 `main` 和 `types` 两个入口串起来。
- `strict: true`：全量严格检查。插件是写给框架的代码，类型安全直接关系到 execute 契约的正确性（第 3 章讲过的 canonical 值校验，靠类型先兜底）。

> [!note] 这在 Claude Code 里相当于
> `tsconfig` 就是项目的「生产标准」，Claude Code 插件的工程化同样需要 `tsconfig` + `tsc` 构建链；`declaration` 产出的 `.d.ts` 相当于给插件 API 留了类型文档。

### 6.3 双 patch 定型：dev 用绝对路径，bundle 用包名

第 2 章只用了 `dev-cordis.patch.yml`，现在补第二份 `cordis.patch.yml`。两者结构完全一致，**唯一实质区别是插件条目的 `name`**：

`dev-cordis.patch.yml`（开发期，`pnpm dsh web --patch` 手动叠加用）：

```yaml
- insert:
    - id: git-log
      name: '/absolute/path/to/git-log-plugin/src/index.ts'   # 绝对路径（同第 2 章）
      config:
        maxCommits: 5
```

`cordis.patch.yml`（bundle 补丁，随包发布，`dsh.bundle.patch` 指向它）：

```yaml
- insert:
    - id: git-log
      name: dsh-git-log-plugin
      config:
        maxCommits: 5
```

两个关键点：

1. **`config` 块与第 4 章完全同步**：两份 patch 的 `config` 都要有 `maxCommits`，开发期行为与发布后行为一致——你验证的是什么，用户装到的就是什么。schema 默认值仍是第 4 章定死的 `maxCommits: Schema.number().default(5)`，patch 里的 `maxCommits: 5` 是显式覆盖值，两份 patch 保持一致。
2. **bundle patch 的 `name` 必须等于 `package.json` 的 `name`（`dsh-git-log-plugin`）**（[^S3]）。这是本节最容易被忽视的坑：dsh 装好 bundle 后，Node 要从 profile 的 `node_modules` 里按这个 `name` 解析已装代码；写错（沿用绝对路径、或写成 `git-log-plugin`）就会**装进去但不激活**——没有报错，只是静默不生效（[^S11]，四名分离基线见 [[DeepSeek-Harness 插件实战]]，这类坑也收录在 [[DeepSeek-Harness 常见坑与速查]]）。

`id: git-log` 仍是补丁实例 id（四名分离里的第三个名字），在补丁树「整行替换」机制里用于定位目标行——第 7 章展开。

> [!note] 这在 Claude Code 里相当于
> `dsh.bundle.patch` + `cordis.patch.yml` 的 `name` ≈ 包里声明「我是 dsh 插件」并给出激活清单；`name` 必须等于包名，相当于激活记录里的标识符必须能对应到 `node_modules` 里真实存在的那个包。

### 6.4 校准注记：独立插件 ≠ monorepo 内建包

dsh 仓库的 `docs/cookbook/adding-a-package.md` 讲的是**在 deepseek-harness 仓库内部新增内建包**的规范：用 `lib/`、`types/` 目录结构、`extends` 根 tsconfig、`references` 项目引用、`constraints` 依赖约束——这套规范**不适用于**独立插件，也不会用 `dsh.bundle.patch`（[^S2]）。

本篇只教独立插件规范（V1 example-plugin 那套：`src/` + `tsc` + `dist/` + `dsh.bundle.patch`）。**不要**把 `references` / `constraints` / extends 根 tsconfig 搬进独立插件——那会让一个本该独立发布的小包背上 monorepo 的耦合。

### 构建一次，看 dist/ 产物

补齐上述文件后，在插件目录执行：

```bash
pnpm install && pnpm run build
```

`pnpm run build` 执行 `tsc`，按 `tsconfig.json` 编译 `src/`，得到：

```
dist/
├── index.js
├── index.d.ts
└── tools/
    ├── git-log.js
    └── git-log.d.ts
```

看到这个结构，说明 `main: dist/index.js` 和 `types: dist/index.d.ts` 指向的文件真实存在了，插件已具备被 `pnpm pack` 打包、被 `dsh plugin add` 安装的资格。下一步（第 7 章）进入打包安装。

## 本章小结

- `package.json` 是工程化地基：`main` / `types` 指向 `dist/` 产物，`dsh.bundle.patch` 声明「我是 dsh 插件」，`prepare` 保证安装前自动构建。
- `cordis` / `dsh-tools` / `schemastery` 必须 **peer + dev 双份**：peer 声明运行时靠宿主提供，dev 保证构建时能解析到。
- `tsconfig` 用 `ES2022 + ESNext + Bundler + declaration + outDir + rootDir + strict`，一次编译产出 `.js` + `.d.ts`，串起 `main` 和 `types`。
- `files` 白名单只放 `dist/` 和 `cordis.patch.yml`；`dev-cordis.patch.yml` 带绝对路径，不进包。
- **双 patch 定型**：dev patch 的 `name` 用绝对路径，bundle patch 的 `name` 必须等于 `package.json` 的 `name`（`dsh-git-log-plugin`），且两边 `config` 块完全同步——否则装进去不激活。

## 第 7 章：第 6 步——打包发布安装

前几章我们一直在 dsh 源码仓库里用 `--patch` 跑插件，插件活得好好的，但这是"临时工"状态：换台机器、或想分享给别人，都无从谈起。这一章把 `dsh-git-log-plugin` 收尾成能分发的产物：先讲清 **bundle**（作者造包）与 **profile**（用户搭家）的分工，再走一遍四层补丁树如何决定"最终配置长什么样"，最后用 `pnpm pack` 打 tarball、用 `dsh plugin` 装进 profile 并跑通，并单独交代 git 源安装的三道坎。

### 7.1 bundle vs profile：作者造包，用户搭家

先说两个最容易混的概念，它们**互斥**，各管一件事：

- **bundle**：一个 npm 包，作者在里面声明 `dsh.bundle.patch`（即上一章定型的 `cordis.patch.yml`），等于"这个包贡献一层配置"。作者造 bundle，负责把配置随包分发出去。
- **profile**：Harness home 下的一个命名目录，里面声明 `dsh.profile.bundles` 的**有序列表**，决定"这台机器要激活哪些 bundle、按什么顺序"。用户 boot profile，负责组装自己的环境。

我们第 6 章做的事就是"作者面"：把 `dsh-git-log-plugin` 的 `cordis.patch.yml` 挂在 `dsh.bundle.patch` 字段上，包一装、profile 一激活，这一层配置就进来了。[^S3] 官方架构文档把 profile 描述为"命名配置集合"，bundle 是它的一个来源，两者正交。[^S9]

这里有个决定成败的硬规则，务必记牢：**bundle patch 里的 `name` 必须等于 package.json 的 `name`**。对我们是 `dsh-git-log-plugin` 对 `dsh-git-log-plugin`。原因是 dsh 安装时把 bundle 装进 profile 的 `node_modules`，加载 patch 时 Node 靠这个 `name` 去 `node_modules` 里解析已装代码——对不上，层就静默不激活。[^S11]

> [!tip] 大白话
> bundle 像「已装修的户型包」——开发商（作者）把墙、水电、软装（配置）都做进包里；profile 像「你选好哪些户型包进自己家」——你按顺序选 3 个包，决定家里装成什么样。作者造包、用户搭家，各管各的。

> [!note] 这在 Claude Code 里相当于
> bundle ≈ npm 插件包（自带一份"安装后如何配置"的声明）；profile ≈ 你在插件市场里装进自己环境的插件集合。作者发布插件，用户选择装哪些。

### 7.2 四层补丁树：后层整行替换

上一章你已经在 `--dump-config` 里见过"分层打印"。补丁树完整地有**四层**，按序叠加：

| 层序  | 层                            | 内容                                                  |
| --- | ---------------------------- | --------------------------------------------------- |
| ①   | bundles 各层                   | 按 profile 声明的列表顺序，逐 bundle 应用各自的 `cordis.patch.yml` |
| ②   | profile 的 `cordis.patch.yml` | profile 目录里自己的 patch，覆盖 bundle 层                    |
| ③   | home 级                       | Harness home 层面的通用配置                                |
| ④   | `--patch` 叠加                 | 命令行临时追加的 patch，优先级最高                                |

关键语义：**每层都作用于一张空条目表，后层按 id 定位目标行、整行替换，不做字段级深合并**。[^S9] 意思是——配置不是"一层叠一层地做字段合并"，而是按 patch 条目的 `id` 找到那一行，整个替换掉。如果 bundle 层给 `git-log` 写了 `config: { maxCommits: 5 }`，profile 层想改成 10，它必须写**同一 id 的完整行**（含要保留的所有字段），而不是只写 `maxCommits: 10` 指望"合并"。

> [!tip] 大白话
> 四层补丁树像「千层饼」：每层饼都是独立的，后压上去的层不是跟下面融合，而是把同一块位置整个盖住。你以为"只改了一个参数"，实际是把那一整行配置都换掉了。

这也解释了最常见的排查盲区：改完配置发现不生效——不是没加载，而是**前层被后层整行顶掉**，或者你改的是 bundle 层、被 profile/home 层覆盖了。遇到"我以为改了但被覆盖"，先去 `dsh --profile demo --dump-config` 看 `git-log` 那一行最终落在哪层。另外注意：如果 profile 里声明了一个**没有 `dsh.bundle.patch` 声明**的普通包，dsh 只把它装成普通依赖、给一次告警，**不会**把它当成配置层激活。[^S3]

### 7.3 打包：pnpm pack 打 tarball

发布有两条路：推到 npm registry（长期分享），或 `pnpm pack` 打个 tarball（临时分发 / 自用）。后者不用注册表，最适合验证流程。在第 6 章工程目录根目录执行：

```bash
pnpm pack
```

输出类似（产物受第 6 章 `files` 白名单限制，只有 `dist/` 和 `cordis.patch.yml`）：

```bash
Tarball Contents:

120B package.json
3.2kB dist/index.js
1.1kB dist/index.d.ts
1.5kB cordis.patch.yml

Tarball Details
name: dsh-git-log-plugin
version: 0.1.0
packageSize: 5.8 kB
unpackedSize: 16.4 kB
totalFiles: 4

npm notice
npm notice 📦  dsh-git-log-plugin@0.1.0
npm notice Tarball Contents
npm notice 120B  package.json
npm notice 3.2kB dist/index.js
npm notice 1.1kB dist/index.d.ts
npm notice 1.5kB cordis.patch.yml
npm notice Total Files: 4
npm notice == Tarball Contents ==
```

这一步顺便自检了第 6 章的 `files` 白名单：如果 `dist/index.js` 没打进去，说明构建没跑或白名单写错——tarball 里没有产物，装进 profile 就是个空壳。包名 `dsh-git-log-plugin` 与 bundle patch 的 `name` 一致，才谈得上激活。

### 7.4 安装：dsh plugin --profile demo add

拿到 tarball（路径记作 `/path/to/dsh-git-log-plugin-0.1.0.tgz`），用 `dsh plugin` 命令族装进一个名为 `demo` 的 profile：

```bash
dsh plugin --profile demo add /path/to/dsh-git-log-plugin-0.1.0.tgz
```

`dsh plugin` 内部**转发 pnpm 的完整动词**（add / remove 等），所以语法基本可以按 pnpm 的习惯写：装 tarball 写文件路径，装 registry 包写包名，装 git 源写 `git+https://...#sha`（见 7.6）。tarball 和本地目录两种安装方式**不需要** `allowBuilds` 放行——因为产物已经在那里，没有"装完再跑构建脚本"这一步。[^S14][^S8] 从源码仓库根目录跑 `dsh plugin` 依旧成立。

> [!tip] 大白话
> `dsh plugin add` 像「物业帮你把包装进门」——你不需要自己研究入户线路、强弱电怎么走，物业（dsh plugin 命令）按规矩把包放进正确的位置（profile 的 node_modules 和 bundles 列表）并登记在册。

### 7.5 跑通已装插件：dsh --profile demo

装完后直接带 profile 启动，看插件自身的加载日志：

```bash
dsh --profile demo
```

正常会看到类似输出（诊断名是第 1 章定的 `git-log-plugin`）：

```bash
[info] profile "demo" loaded, bundles: dsh-git-log-plugin
[git-log-plugin] plugin loaded!
[info] Harness is running. Press Ctrl+C to exit.
```

此刻插件已不再是"开发期 `--patch` 注入"，而是真正作为 bundle 从 profile 激活。这里有一条贯穿全章的纪律：**profile 永不手写**——它的 `dsh.profile.bundles` 列表、`node_modules`、`pnpm-workspace.yaml` 全由 `dsh plugin` 命令自动维护对账。你想加包、换版本、删包，都走 `dsh plugin --profile demo <add|remove|...>`，而不是去改 profile 目录里的文件；手写很容易写坏对账关系，装进去却不激活。[^S3][^S12]

### 7.6 git 源安装三坑（未实测）

`dsh plugin --profile demo add git+https://github.com/you/dsh-git-log-plugin.git#v0.1.0` 这类 git 源安装很方便，但有三道坎。**以下内容以官方 publish 文档为准，本篇教学未真机复现，动手时以实际报错为准**[^S3]：

**坑①：git 源拉的是源码，不是产物。** git 依赖只 clone 仓库源码，不会带上 `dist/`。所以作者必须在 package.json 里提供 `scripts.prepare`（第 6 章已配：`"prepare": "npm run build"`），让安装方 clone 后自动自包含构建。没有 prepare，装进来只有源码、没有可加载的 `dist/index.js`。

**坑②：pnpm ≥ 10 默认拒跑 git 依赖的 prepare 构建脚本。** 这是 pnpm 的安全策略：外来 git 依赖要跑任意构建脚本，必须先显式放行。当你 `dsh plugin add` 一个 git 源包时，pnpm 会在终端打印一串需要放行的包 key（如 `dsh-git-log-plugin`）并拒绝继续；你要把打印的包 key 抄进 profile 的 `pnpm-workspace.yaml` 的 `allowBuilds` 列表，再重跑安装命令：

```yaml
# profile 的 pnpm-workspace.yaml（由 dsh plugin 维护，此处仅示意放行字段）
allowBuilds:
  dsh-git-log-plugin: true
```

放行后重跑 `dsh plugin --profile demo add git+...#sha`，prepare 才会被允许执行。tarball / 本地目录安装没有这一步，因为产物不需要现场构建。

**坑③：用 `#sha` 钉 commit。** git 依赖默认跟着分支走，哪天仓库变了你本地就悄悄升级，配置可能突然对不上。规范做法是钉死一个 commit 或 tag：`git+...#<40 位 commit sha>` 或 `...#v0.1.0`，保证每次安装的是同一份代码。[^S3]

> [!note] 这在 Claude Code 里相当于
> `allowBuilds` ≈ 包管理器对「安装后要跑构建脚本」的插件逐包给信任；不信任就不让脚本跑。Claude Code 生态里安装需要原生编译或构建钩子的包时，同样会遇到类似的放行确认。

## 本章小结

- **bundle（作者造包，贡献一层配置）与 profile（用户搭家，声明有序 bundles）互斥**；bundle patch 的 `name` 必须等于 package.json 的 `name`，Node 才能从 profile 的 `node_modules` 解析到已装代码。[^S3][^S11]
- **四层补丁树**：bundles 各层 → profile patch → home 级 → `--patch`；后层按 id **整行替换**、不做字段级深合并，排查"配置没生效"先 `--dump-config` 看目标行落在哪层。[^S9]
- **打包用 `pnpm pack`**（受 `files` 白名单约束）或 `npm publish`；**安装用 `dsh plugin --profile demo add <tarball>`**，tarball / 本地目录无需 `allowBuilds`。[^S3]
- **profile 由 `dsh plugin` 自动对账，永不手写**；缺 dsh 声明的包只装为普通依赖 + 一次告警，不激活层。[^S12]
- **git 源安装三坑（未实测）**：prepare 自包含构建、pnpm≥10 的 `allowBuilds` 放行、`#sha` 钉 commit。[^S3]

下一章把全篇压缩成一张「从零到装好」的路线图，串起 `dsh web --patch` → `--dump-config` → headless → `pnpm pack` → `dsh plugin add` 这条完整命令链。

## 第 8 章：小结与下一步

前面 7 章从空目录一步步把插件「写 → 配 → 验证 → 打包 → 装」走通，这一章没有新代码、没有新命令，只做一次完整复盘：收拢全文件增量、命令链和下一步方向——卡在哪一步，就翻回哪一章。

### 8.1 全文件清单回顾：从 2 文件到完整工程的每一次增量

整条路线只有 6 次增量，手写文件从 2 个长到 6 个，构建后再产出 `dist/`，终点共 8 个文件：

| 阶段 | 章节 | 新增/修改 | 文件 |
| --- | --- | --- | --- |
| ① 最小跑通 | 第 2 章 | 新增 2 个 | `src/index.ts` + `dev-cordis.patch.yml` |
| ② 加工具 | 第 3 章 | 新增 1 个 | `src/tools/git-log.ts`；`src/index.ts` 升级为注册中心 |
| ③ 加配置 | 第 4 章 | 不新增 | `src/index.ts` 加 `Config` schema；两份 patch 加 `config` 块 |
| ④ 验证 | 第 5 章 | 不新增 | 四条验证命令 |
| ⑤ 工程化 | 第 6 章 | 新增 3 个 | `package.json` + `tsconfig.json` + `cordis.patch.yml`；build 产出 `dist/` |
| ⑥ 打包安装 | 第 7 章 | 不新增 | `pnpm pack` → `dsh plugin add` |

起点是最小 2 文件骨架 [^S1]。第 ⑤ 步定型双 patch：`dev-cordis.patch.yml`（开发期绝对路径）与 `cordis.patch.yml`（bundle，`name = dsh-git-log-plugin`）。文件归属沿用 [[DeepSeek-Harness 插件开发核心]]：工具进 `src/tools/`，`src/index.ts` 做注册中心。

### 8.2 一条命令链串起来：`dsh web --patch` → `--dump-config` → headless → `pnpm pack` → `dsh plugin add`

从开发到交付，五条命令按顺序就是整条流水线：

| 顺序 | 命令 | 作用 | 章节 |
| --- | --- | --- | --- |
| 1 | `pnpm dsh web --patch ./git-log-plugin/dev-cordis.patch.yml` | 开发期加载，看 `[git-log-plugin] plugin loaded!` | 第 2 章 |
| 2 | `dsh --profile demo --dump-config` | 分层打印合并后配置 | 第 5 章 |
| 3 | `dsh --profile headless "<task>"` | 一次性任务端到端（退出码 0/1） | 第 5 章 |
| 4 | `pnpm pack` | 打成 tarball | 第 7 章 |
| 5 | `dsh plugin --profile demo add <tarball>` | 装进 profile 并对账 | 第 7 章 |

前三条在 dsh 源码仓库根目录执行，后两条在插件工程里执行；打包安装机制来自官方 bundle/profile 文档 [^S3]。

### 8.3 下一步：更多工具 / 配置实战 / 发布到 npm registry / 官方模板 `dsh-plugin-*`

按「补全当前插件 → 走向真实发布」排四个方向：

1. **更多工具**：按第 3 章 defineTool 五件套继续加，一个插件可注册多个工具。
2. **配置实战**：按第 4 章扩展 Schema 类型，把参数做成可配，对照 [[DeepSeek-Harness 配置实战]]。
3. **发布到 npm registry**：第 7 章只演示 `pnpm pack`，改走 `npm publish`，任何 profile 即可 `dsh plugin add dsh-git-log-plugin` 安装。
4. **官方模板 `dsh-plugin-*`**：现在回头看脚手架能读懂每个文件为何存在——从零练理解，模板提速度，与 [[DeepSeek-Harness 插件实战]] 对照读。

> [!tip] 大白话
> 把全篇压成一张「从零到装好」的路线图：先 2 个文件把插件点亮（第 2 章），再长出手脚（工具）、装上旋钮（配置）、验过合格（第 5 章）、搭好流水线（第 6 章）、装箱送货（第 7 章）。卡在哪一步，就翻回哪一章——8.1 的表格就是索引。

> [!note] 这在 Claude Code 里相当于
> 一篇插件的「从模板 starter 到 npm 发布」完整 SOP 回顾：入口初始化（apply）→ 注册工具 → 配置校验（schema）→ 本地验证 → 工程化打包 → 发布安装，每一步都有 Claude Code 插件开发现实可对照。

唯一要回翻的坑：忘了「四名分离」或「bundle patch name = 包名」就翻第 6、7 章——前者管名字，后者管装进去能不能激活。

## 本章小结

- 从零到装好共 6 次增量，手写文件 2 → 6 个，加 `dist/` 产物共 8 个文件。
- 一条命令链覆盖开发到交付：`web --patch` → `--dump-config` → headless → `pnpm pack` → `dsh plugin add`。
- 四名分离（`git-log-plugin` / `dsh-git-log-plugin` / `git-log` / `git_log`）与「bundle patch name = 包名」是唯一要回翻的坑。
- 下一步四条路：更多工具、配置实战、npm 发布、官方模板 `dsh-plugin-*`。
- 至此你能脱离脚手架，从空目录独立造出带 `git_log` 工具与 `maxCommits` 配置的 dsh 插件。

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

## 注释

[^S1]: O1 · 官方 `docs/user/develop/basic/index.zh.md`（Your first plugin）：最小 2 文件骨架（`import type { Context } from '@deepseek-ai/cordis'` + `export const name` + `export function apply(ctx)`）、`- insert:` 注册、`pnpm dsh web --patch` 加载命令；官方 index 不覆盖 package.json/tsconfig/打包（工程化缺口是本分册增量）。

[^S2]: O2 · `docs/cookbook/adding-a-package.md`：monorepo 内建包规范（lib/types、extends 根 tsconfig、references、constraints），本篇仅作校准排除，不适用于独立插件。

[^S3]: O3 · 官方 `docs/user/develop/basic/publish.md`：bundle/profile、发布、安装与 bundle patch `name` 规则（含 git 源安装坑）。

[^S4]: O4 · 官方 `docs/user/develop/basic/tool.md`：defineTool 五件套；parameters 属性级 required；output.schema + output.render。

[^S5]: O5 · 官方 `docs/cookbook/adding-a-tool.md`：execute 契约（canonical 值 / throw=isError / 注册即 effect / schema 自动流入系统提示词）。

[^S6]: O6 · 官方 `docs/user/develop/basic/config.md`（"Plugin configuration"）：Config 两段式、`.default()` 默认值、`.required()` 必填口径、禁止导出普通对象作 Config。

[^S7]: O7 · 官方 `docs/cordis-tutorial/05-config.md`（Cordis 教程第 5 章）：`config` 块、ValidationError 输出、fiber FAILED、apply 总收到完整校验后的 config。

[^S8]: O8 · 官方 `apps/cli/reference/README.md`：dsh CLI 全家族与验证命令精确语法。

[^S9]: 官方 `docs/architecture.md`：bundle/profile 分层 / 四层补丁树。

[^S10]: V1 · `example-plugin/` 的真实独立插件工程字段（`package.json` / `tsconfig` / dev 与 bundle patch），vault 素材。

[^S11]: V2 · 《DeepSeek-Harness 插件实战》：从 example-plugin 脚手架改造出同一插件的教学分册，本篇对照路线。一致性基线（`git_log` / 四名分离 / `maxCommits=5`）、验证命令在 dsh 源码仓库根目录执行、开发期不用 npx、bundle patch name = 包名；其 §4 旧口径 `.required(true)` 与本篇不同，以官方为准。见 [[DeepSeek-Harness 插件实战]]。

[^S12]: V3 · 《DeepSeek-Harness 配置体系》：bundle / profile 分层心智模型的来源，也用于界定独立插件规范与 O2 内建包规范的边界。见 [[DeepSeek-Harness 配置体系]]。

[^S13]: V4 · 《DeepSeek-Harness 插件开发核心》：文件归属（src/index.ts 注册中心、src/tools/*.ts 工具工厂）/ apply 三形态 / defineTool 契约。

[^S14]: V5 · 《DeepSeek-Harness 常见坑与速查》：patch `name` 必须绝对路径、相对路径静默失效、dsh 命令族排错顺序与 `dsh plugin` 命令族。

## 更新记录

- 2026-08-15 创建（学习笔记工作流 P5 组装）
- 2026-08-15 美化发布（P6：补 frontmatter / 导读 Callout，同步系列 README 与 MOC）
- 2026-08-15 修正 2.3/2.4/2.5/5/8 与本章小结：`--patch` 相对路径按 dsh 源码仓库根目录解析，命令须在仓库根目录执行；补丁文件在 `git-log-plugin/` 下，路径要写成 `./git-log-plugin/dev-cordis.patch.yml`（在插件目录内跑或直接写 `./dev-cordis.patch.yml` 都报 `ENOENT`）
- 2026-08-15 第 3 章结构优化：§3.1 补「先建 `src/tools/` 目录」命令（与 §2.2 的 `mkdir -p src` 一致）；§3.2 新增完整 `src/tools/git-log.ts`「先睹为快」（可运行全代码），§3.3/§3.4 逐段拆解均标注所属文件位置
- 2026-08-15 第 6 章补章首「要创建/生成哪些文件」清单：手写 3（package.json / tsconfig.json / cordis.patch.yml）+ 生成 2（pnpm-lock.yaml / dist/），标明落点与所属小节，并列出沿用不新建的文件
- 2026-08-15 第 6 章结构重构：原 §6.2（依赖双份）与 §6.4（files 白名单）并入 §6.1 package.json 大节，作为子节 6.1.2 / 6.1.3；后续小节顺延为 §6.2 tsconfig / §6.3 双 patch / §6.4 校准注记
