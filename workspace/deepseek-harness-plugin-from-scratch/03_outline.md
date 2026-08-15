---
title: DeepSeek-Harness 从零写插件（空目录手写全文件）
topic: deepseek-harness-plugin-from-scratch
direction: A（渐进式从零：先最小 2 文件跑通 → 再补工程化 → 打包安装）
created: 2026-08-15
status: confirmed
note_type: 实战教学分册
---

# 《DeepSeek-Harness 从零写插件：空目录手写全文件》

> 笔记类型：实战教学分册（learning-note / outline 模式）
> 预计总篇幅：约 12,000–15,000 字（用户已确认压缩到中量：核心章 2/3/4/6/7 保详细，过渡章 1/8/9 精简）
> 章节数：9 章（8 章教学 + 1 章分工说明）
> 核心承诺：**不依赖 example-plugin 脚手架**，从一个空目录手写所有文件，走通 写→配→验证→打包→安装

---

## 一致性基线（全篇固定，与《插件实战》可对照）

| 项 | 固定值 | 说明 |
| --- | --- | --- |
| tool name（模型可见） | `git_log` | defineTool 的 `name` |
| 诊断名 / 加载日志 | `export const name = 'git-log-plugin'` | 加载日志 `[git-log-plugin] plugin loaded!` |
| 包名（package.json name） | `dsh-git-log-plugin` | bundle patch 的 `name` 必须等于它 |
| patch id | `git-log` | patch yml 中 `- insert:` 的 `id` |
| config 默认值 | `maxCommits: Schema.number().default(5)` | 见第 4 章 |

**四名分离**：`git-log-plugin`（诊断/日志）≠ `dsh-git-log-plugin`（包）≠ `git-log`（patch id/实例）≠ `git_log`（模型可见工具名）。

---

## 第 1 章：结果预览——从零建的插件 vs 脚手架改造

**节目标**：读完能一眼看出「从零建的插件」由哪几个文件组成，并能在「改造 vs 从零」两条路线间互相对照着读，先看到终点长什么样。

**小节**
- 1.1 为什么还要「从零」写一遍：依赖脚手架的幻觉
- 1.2 终点长什么样：8 个文件的清单 + 4 个名字 + 基线表
- 1.3 双路线对照表：《插件实战》改造（example-plugin）vs 本篇从零（空目录）

**篇幅**：短（约 600 字）——过渡章，终点清单 + 对照表为主

**素材引用**：S11（V2）、S1（O1）、S13（V4）

**代码示例清单**：无（对照表 + 文件清单为主）

**大白话类比建议**：
- [!tip] example-plugin 像「装修好的样板间」，从零像「清水房自己走水电」；本篇先给你一张「户型图（最终文件清单）」
- [!note] 这在 Claude Code 里相当于：不用官方插件 starter 模板、自己手写插件入口文件与 manifest

**关键坑**：
- 不要一上来就复制脚手架文件——会失去对「每个文件为什么存在」的理解
- 脚手架的 dev/bundle 双 patch 不是独立插件的起点，最小只需 1 份 patch（见第 2 章）

**前置要求**：需先读 [[DeepSeek-Harness 插件实战]]（了解改造路线的成品）；[[DeepSeek-Harness 插件开发核心]]（apply / inject / defineTool 术语）

**双链**：[[DeepSeek-Harness 插件实战]]、[[DeepSeek-Harness 插件开发核心]]、[[DeepSeek-Harness 配置体系]]

---

## 第 2 章：第 1 步——空目录 + 最小 2 文件跑通

**节目标**：读完能在一个空目录里用 2 个文件（`src/index.ts` + 最小 patch yml）让 dsh 把插件加载起来，并在终端看到 `[git-log-plugin] plugin loaded!`。

**小节**
- 2.1 建目录：`mkdir git-log-plugin && cd git-log-plugin`（命令在 dsh 源码仓库根目录执行）
- 2.2 写 `src/index.ts` 最小版：`import type { Context } from '@deepseek-ai/cordis'` + `export const name` + `export function apply(ctx)` + `console.log`
- 2.3 写最小 patch yml：`- insert:` 注册，`name` 必须是**绝对路径**（相对路径静默失效）
- 2.4 加载命令：`pnpm dsh web --patch ./dev-cordis.patch.yml` → 开 http://127.0.0.1:3080 看日志
- 2.5 校准认知：「plugin loaded!」是插件自身的 `console.log`，不是 dsh 框架/CLI 的特性

**篇幅**：长（约 2,300 字）——全篇第一个关键里程碑，逐行讲解

**素材引用**：S1（O1）、S14（V5）、S11（V2§5.1）

**代码示例清单**：`src/index.ts` 最小版；`dev-cordis.patch.yml` 最小 patch；`pnpm dsh web --patch` 终端命令与期望输出

**大白话类比建议**：
- [!tip] patch 里的绝对路径 name 像门禁卡必须写门牌号；相对路径 = 不存在的房间，刷了没反应还不报错
- [!note] 这在 Claude Code 里相当于：`export function apply(ctx)` ≈ 插件入口的初始化钩子，`console.log` 加载日志 ≈ 插件被 require 时打的启动日志

**关键坑**：
- `name` 必须是绝对路径，相对路径**静默失效**（无报错、无警告）
- `pnpm dsh web` 需在 dsh 源码仓库根目录执行（开发期不用 npx）
- `dsh web` 是 `--profile web` 的硬编码别名

**大纲落定决策**：最小 patch 文件名定为 `dev-cordis.patch.yml`（从第一步就用 dev 前缀，避免第 5 步再改名）。

**前置要求**：源码环境已跑通（系列前言）；会基本 pnpm 命令；需先读 [[DeepSeek-Harness 插件开发核心]]

**双链**：[[DeepSeek-Harness 插件实战]]、[[DeepSeek-Harness 常见坑与速查]]

---

## 第 3 章：第 2 步——加工具 git_log

**节目标**：读完能独立写出一个被 dsh 正确注册、模型可见的工具 `git_log`，并理解 defineTool 五件套与 execute 契约。

**小节**
- 3.1 文件归属：工具本体放 `src/tools/git-log.ts`（工厂），`src/index.ts` 做注册中心
- 3.2 defineTool 五件套：`name` / `description` / `parameters` / `output` / `execute`
- 3.3 `parameters` 与 `output`：类 JSON-schema（属性级 `required` 布尔）；`output.schema` + `output.render`
- 3.4 `execute(args)` 契约：返回 **唯一 canonical JSON 值**（不返回内容块）；抛错 / 非法值 = isError
- 3.5 `index.ts` 升级：`inject = ['tools']` + `ctx.tools.register(defineTool({...}))`
- 3.6 四名分离落地：`git-log-plugin` / `dsh-git-log-plugin` / `git-log` / `git_log`

**篇幅**：长（约 2,600 字）——五件套 + 契约是本篇核心，需配合真实代码

**素材引用**：S4（O4）、S5（O5）、S13（V4）、S11（V2）

**代码示例清单**：`src/tools/git-log.ts` 完整工厂；`src/index.ts` 注册段（inject + register）；`parameters`/`output` schema 片段；`execute` 正确 vs 错误写法对照

**大白话类比建议**：
- [!tip] defineTool 像「给机器人写岗位说明书」——名字、职责、输入输出格式；execute 是「真干活的人」，只把结果（canonical 值）交回去，不要自己排版
- [!note] 这在 Claude Code 里相当于：Claude Code 插件里 `tools` 数组的 name/description/parameters + 处理函数；`inject=['tools']` ≈ 初始化时拿到工具注册表引用

**关键坑**：
- `execute` 返回 **canonical 值**而不是内容块（框架按 `output.schema` 序列化）
- 基础设施失败要 `throw`（=isError，注册表捕获，不泄漏给模型）；业务成功态放 canonical 值
- `inject` 没写 `['tools']` 时 `ctx.tools` 是 undefined，register 直接报错
- schema 会自动流入系统提示词组装，不需要手拼 description

**前置要求**：第 2 章；需先读 [[DeepSeek-Harness 插件开发核心]] 的 apply 三形态 / defineTool 契约

**双链**：[[DeepSeek-Harness 插件开发核心]]、[[DeepSeek-Harness 插件实战]]

---

## 第 4 章：第 3 步——加 Config 可调参数

**节目标**：读完能让插件拥有可配置项 `maxCommits`，能用 patch 的 `config` 块传值、在代码里读取，并掌握官方 `.required()` 口径。

**小节**
- 4.1 Config 两段式：`export interface Config` + `export const Config: Schema<Config> = Schema.object({...})`
- 4.2 默认值写 schema：`maxCommits: Schema.number().default(5)`
- 4.3 **校准注记**：必填用 `.required()`（官方从不用 `.required(true)` 或 `.optional()`，可选用 TS `?`）；标注与《插件实战》§4 旧口径（`.required(true)`）的差异，本篇以官方为准
- 4.4 在 patch 的 `config` 块传值（第 2 章的 dev patch 先加；bundle patch 在第 5 步定型时复制同一 config 块）——两份 patch 传值位置一致
- 4.5 apply 里读取完整校验后的 config：`ctx.config.maxCommits`
- 4.6 坏配置行为：插件加载时跑 schema → ValidationError / fiber FAILED / 永不半启动

**篇幅**：中（约 1,900 字）

**素材引用**：S6（O6）、S7（O7）、S11（V2）

**代码示例清单**：`interface Config` + `Schema.object` 两段式；`Schema.number().default(5)`；patch 的 `config` 块；apply 读取 config；坏配置报错输出对照

**大白话类比建议**：
- [!tip] schema 像「配置体检表」——插件加载时先体检（校验），不合格直接拒之门外（ValidationError / fiber FAILED），绝不半启动
- [!note] 这在 Claude Code 里相当于：插件的 settings schema（zod 校验），`Schema.number().default(5)` ≈ `z.number().default(5)`；patch 传值 ≈ settings.json 里配置插件

**关键坑**：
- 必填用 `.required()`，**不用** `.required(true)` / `.optional()`（校准注记，标注与旧笔记差异）
- 禁止导出普通对象作 Config（缺 Standard Schema 接口）
- 坏配置 → ValidationError / fiber FAILED，永不半启动
- apply 总收到完整校验后的 config，无需在 apply 里二次校验

**前置要求**：第 3 章；需先读 [[DeepSeek-Harness 配置体系]]

**双链**：[[DeepSeek-Harness 配置体系]]、[[DeepSeek-Harness 插件实战]]

---

## 第 5 章：第 4 步——验证命令链

**节目标**：读完能用四条命令把「插件有没有被加载、配置在哪一层、端到端通不通」验清楚。

**小节**
- 5.1 `pnpm dsh web --patch ./dev-cordis.patch.yml` 复跑：确认 `[git-log-plugin] plugin loaded!`
- 5.2 `dsh --profile demo --dump-config`：分层打印（bundle 各层 → profile patch → home 级 → `--patch` 叠加）
- 5.3 `dsh --profile demo --dump-default-config`：只看 bundle 层（不含 profile/home/patch）
- 5.4 `dsh --profile headless "<task>"`：一次性任务端到端，stdout 打印文本，退出码 **0 = completed / 1 = otherwise**；无任务文本 = usage 错误
- 5.5 读 dump 输出的要点：文件名注释、`!!js` 不求值、stderr 报未命中

**篇幅**：中（约 1,600 字）

**素材引用**：S8（O8）、S11（V2§5）

**代码示例清单**：四条验证命令 + 期望输出/退出码对照；`--dump-config` 分层输出片段

**大白话类比建议**：
- [!tip] dump-config 像「验房验收单」——每层配置像每道工序，一层层打勾；headless 退出码 0/1 像「验收合格 / 不合格」章
- [!note] 这在 Claude Code 里相当于：`claude config list` 之类看合并后配置的调试手段；headless 退出码 ≈ CLI 命令的退出码约定

**关键坑**：
- 命令统一在 dsh 源码仓库根目录执行
- `--dump-config` 是全层，`--dump-default-config` 只看 bundle 层——别搞反
- headless 无任务文本 = usage 错误（不是正常返回）
- dump 输出里 `!!js` 不求值、未命中配置走 stderr

**大纲落定决策**：headless 验证默认用**文本对照**，不做 Web UI 截图。

**前置要求**：第 4 章；需先读 [[DeepSeek-Harness 常见坑与速查]]

**双链**：[[DeepSeek-Harness 常见坑与速查]]、[[DeepSeek-Harness 配置体系]]

---

## 第 6 章：第 5 步——工程化补齐

**节目标**：读完能把 2 个文件长成完整可构建的独立插件工程（package.json + tsconfig + files 白名单 + 双 patch），跑通 `pnpm install && pnpm run build` 产出 `dist/`。

**小节**
- 6.1 package.json 最小字段：`name` / `version` / `main=dist/index.js` / `types=dist/index.d.ts` / `dsh.bundle.patch="./cordis.patch.yml"` / `scripts.build=tsc` / `scripts.prepare=npm run build`
- 6.2 依赖双份：`cordis` / `dsh-tools` / `schemastery` 进 peerDependencies + devDependencies
- 6.3 tsconfig：`target=ES2022` / `module=ESNext` / `moduleResolution=Bundler` / `declaration=true` / `outDir=dist` / `rootDir=src` / `strict=true`
- 6.4 files 白名单：`["dist","cordis.patch.yml"]`
- 6.5 双 patch 定型：`dev-cordis.patch.yml`（绝对路径，开发期 `--patch`）vs `cordis.patch.yml`（`name = dsh-git-log-plugin`，打包用）；把第 4 章的 config 块同步复制到 bundle patch
- 6.6 **校准注记**：O2 的 monorepo 内建包规范（lib/types、extends 根 tsconfig、references、constraints，**不含 dsh.bundle.patch**）不适用于独立插件，本篇只教独立插件规范

**篇幅**：长（约 2,000 字）

**素材引用**：S10（V1）、S2（O2 校准）、S3（O3）、S11（V2§6）

**代码示例清单**：package.json 全字段；tsconfig 全字段；files 白名单；双 patch 文件内容对照；`pnpm install && pnpm run build` 命令与 dist/ 产物结构

**大白话类比建议**：
- [!tip] 工程化像「给手工作坊上流水线」——package.json 是营业执照、tsconfig 是生产标准、build 是出厂质检（产出 dist/）
- [!note] 这在 Claude Code 里相当于：任何 npm 插件的工程化（main/types/files 字段）；`dsh.bundle.patch` ≈ 包里声明「我是 dsh 插件」的激活清单

**关键坑**：
- 四名分离：`export const name`（诊断）≠ package.json name（包）≠ patch id（实例）≠ defineTool name（模型可见）
- **bundle patch 的 `name` 必须等于 package.json 的 `name`**（`dsh-git-log-plugin`），否则装进去不激活
- cordis / dsh-tools / schemastery 要 peer + dev **双份**
- 不要照搬 O2 的 monorepo 规范（extends 根 tsconfig、references、constraints）

**前置要求**：第 2–4 章内容；需先读 [[DeepSeek-Harness 插件实战]] §6

**双链**：[[DeepSeek-Harness 插件实战]]、[[DeepSeek-Harness 常见坑与速查]]

---

## 第 7 章：第 6 步——打包发布安装

**节目标**：读完能把插件打成 tarball、用 `dsh plugin add` 装进 profile 并跑通，且知道 git 源安装的三道坎。

**小节**
- 7.1 bundle vs profile：作者造 bundle（npm 包贡献一层配置），用户 boot profile（声明有序 bundles）；二者互斥
- 7.2 四层补丁树：bundles 各层（列表序）→ profile 的 cordis.patch.yml → home 级 → `--patch` 叠加；每层应用于空条目表，后层**整行替换**不做字段级深合并
- 7.3 打包：`pnpm pack` 打 tarball（或 npm publish 到 registry）
- 7.4 安装：`dsh plugin --profile demo add <tarball>`；转发 pnpm 全动词；tarball / 本地目录安装无需 allowBuilds
- 7.5 跑通已装插件：`dsh --profile demo`（profile 由 `dsh plugin` 自动维护对账，**永不手写**）
- 7.6 git 源安装三坑：①拉源码不拉产物 → 作者须 `prepare` 自包含构建；②pnpm≥10 拒跑 git 依赖 prepare → 把打印的包 key 抄进 profile 的 pnpm-workspace.yaml `allowBuilds` 再重跑；③`#sha` 钉 commit

**篇幅**：长（约 2,200 字）

**素材引用**：S3（O3）、S9（O9）、S12（V3）、S14（V5）、S11（V2§6）

**代码示例清单**：`pnpm pack` 输出；`dsh plugin --profile demo add` 命令；`allowBuilds` yml 片段；`dsh --profile demo` 跑通输出

**大白话类比建议**：
- [!tip] bundle 像「已装修的户型包」、profile 像「你选好哪些户型包进自己家」；`dsh plugin add` 像「物业帮你把包装进门」
- [!note] 这在 Claude Code 里相当于：bundle ≈ npm 插件包，profile ≈ 用户安装的插件集合；`allowBuilds` ≈ 包管理器信任「安装后要跑构建脚本」的插件

**关键坑**：
- bundle patch 的 `name` 必须 = package.json name（Node 从 profile node_modules 解析已装代码）
- profile 永不手写，`dsh plugin` 自动对账
- git 安装三坑：prepare 自包含构建 / pnpm≥10 allowBuilds / `#sha` 钉 commit
- 后层 patch 整行替换、不做字段级深合并——改配置容易「以为改了但被覆盖」
- 缺 dsh 声明的包仅装为普通依赖 + 一次告警，不激活层

**大纲落定决策**：git 安装坑以官方文档为准，教学里标注「未实测」。

**前置要求**：第 6 章；需先读 [[DeepSeek-Harness 配置体系]]（bundle/profile 心智模型）

**双链**：[[DeepSeek-Harness 配置体系]]、[[DeepSeek-Harness 常见坑与速查]]

---

## 第 8 章：小结与下一步

**节目标**：读完能完整复盘整个从零流程（写→配→验→打包→装），并知道下一步往哪深入。

**小节**
- 8.1 全文件清单回顾：从 2 文件到完整工程的每一次增量
- 8.2 一条命令链串起来：`dsh web --patch` → `--dump-config` → headless → `pnpm pack` → `dsh plugin add`
- 8.3 下一步：更多工具 / 配置实战 / 发布到 npm registry / 官方模板 `dsh-plugin-*`

**篇幅**：短（约 500 字）

**素材引用**：S1（O1）、S3（O3）

**代码示例清单**：无（回顾清单 + 命令链速查表为主）

**大白话类比建议**：
- [!tip] 把全篇压缩成一张「从零到装好」的路线图，卡在哪一步就翻回哪一章
- [!note] 这在 Claude Code 里相当于：一篇插件的「从模板 starter 到 npm 发布」的完整 SOP 回顾

**关键坑**：无新坑（回顾为主）；唯一提醒：忘了「四名分离」或「bundle patch name = 包名」就回来翻第 6、7 章

**前置要求**：本篇全部章节

**双链**：[[DeepSeek-Harness 插件开发核心]]、[[DeepSeek-Harness 配置实战]]、[[DeepSeek-Harness 插件实战]]

---

## 第 9 章：与《插件实战》的分工

**节目标**：读完能清晰知道《插件实战》与《从零写插件》两篇分册各自的定位，按需选读或对照读。

**小节**
- 9.1 双路线对照：改造（example-plugin 脚手架起步）vs 从零（空目录手写全文件）——终点一致、路径不同
- 9.2 本篇刻意不教的：脚手架自带文件、O2 的 monorepo 内建包规范（lib/types / references / constraints）
- 9.3 两篇配合的读法：已有《插件实战》基础 → 跳过第 1 章直接上手；从零读者 → 本篇为主、插件实战做对照验证
- 9.4 共同基线保证可对照：同一 `git_log` / 同一四名分离 / 同一 `maxCommits=5`

**篇幅**：短（约 500 字）

**素材引用**：S11（V2）、S12（V3）

**代码示例清单**：无（对照表为主）

**大白话类比建议**：
- [!tip] 两篇像同一道菜的「半成品加工版」与「全流程生做版」——菜一样，一个省事、一个练基本功
- [!note] 这在 Claude Code 里相当于：「用官方模板改」vs「从零手写」两条学习路线互补

**关键坑**：不要混用两篇的规范——独立插件规范（V1）与 monorepo 内建包规范（O2）是两套，本篇只按独立插件规范

**前置要求**：已读或准备读 [[DeepSeek-Harness 插件实战]]

**双链**：[[DeepSeek-Harness 插件实战]]、[[DeepSeek-Harness 配置体系]]

---

## 学习路径说明

### 前置要求
- 已读系列理论分册：[[DeepSeek-Harness 插件开发核心]]、[[DeepSeek-Harness 配置体系]]、[[DeepSeek-Harness 配置实战]]
- 读过 [[DeepSeek-Harness 插件实战]]（改造路线）——本篇是姊妹篇，两篇对照读效果最好（不是硬性前提）
- dsh 源码仓库已 clone 并 `pnpm install` 跑通（开发期验证命令统一在源码根目录执行）
- 已装 pnpm ≥ 10（涉及第 7 章 git 依赖的 allowBuilds 坑）

### 学完能做什么
- 从空目录手写出一个完整的 dsh 插件（含工具 `git_log` + 配置 `maxCommits`），走通 写→配→验证→打包→安装 全链路
- 独立处理三个最常踩的坑：patch 绝对路径、四名分离、git 安装的 prepare / allowBuilds / #sha
- 读懂官方文档（Your first plugin / tool / config / publish）并自行扩展插件
- 理解 bundle vs profile 分层与四层补丁树，能排查「配置为什么没生效」

### 建议学习顺序
- 首次阅读按章节顺序 1→9（渐进式从零的主线是顺序依赖，不建议跳）
- 已有《插件实战》基础：可跳过第 1 章对照表，从第 2 章直接开始
- 每章先看「节目标」再动手；第 5 章的验证命令链建议真机完整跑一遍
- 预估耗时：约 3–5 小时（含动手）；只看不练约 1.5 小时

---

## 素材脚注表（S1–S14）

| 脚注 | 源编号 | 来源 | 类型 | 层级 |
| --- | --- | --- | --- | --- |
| S1 | O1 | `docs/user/develop/basic/index.zh.md`（Your first plugin） | official | 5 |
| S2 | O2 | `docs/cookbook/adding-a-package.md`（monorepo 内建包规范，仅校准） | official | 5 |
| S3 | O3 | `docs/user/develop/basic/publish.md`（bundle/profile/发布/安装/git 坑） | official | 5 |
| S4 | O4 | `docs/user/develop/basic/tool.md`（defineTool 五件套） | official | 5 |
| S5 | O5 | `docs/cookbook/adding-a-tool.md`（execute 契约） | official | 5 |
| S6 | O6 | `docs/user/develop/basic/config.md`（Config schema，`.required()` 校准） | official | 5 |
| S7 | O7 | `docs/cordis-tutorial/05-config.md`（ValidationError / fiber FAILED） | official | 4 |
| S8 | O8 | `apps/cli/reference/README.md`（dsh CLI 全家族 / 验证命令语法） | official | 5 |
| S9 | O9 | `docs/architecture.md`（bundle/profile 分层 / 四层补丁树） | official | 4 |
| S10 | V1 | `example-plugin/`（package.json / tsconfig / dev / bundle patch） | vault | 4 |
| S11 | V2 | 《DeepSeek-Harness 插件实战》 | vault | 4 |
| S12 | V3 | 《DeepSeek-Harness 配置体系》 | vault | 3 |
| S13 | V4 | 《DeepSeek-Harness 插件开发核心》 | vault | 4 |
| S14 | V5 | 《DeepSeek-Harness 常见坑与速查》 | vault | 3 |

---

## 大纲落定决策（未决问题）

| 未决问题 | 落定 | 写入章节 |
| --- | --- | --- |
| 最小 2 文件时 patch 命名 | 定为 `dev-cordis.patch.yml`（第一步就用 dev 前缀，避免后改名） | 第 2 章 |
| headless 验证是否需 Web UI 截图 | 默认文本对照，不截图 | 第 5 章 |
| git 安装坑是否真机复现 | 以官方文档为准，教学标注「未实测」 | 第 7 章 |
| `.required()` 口径 | 以官方 O6 为准写 `.required()`；保留「无 `.optional()`、可选靠 TS `?`」；校准注记标注与《插件实战》§4（`.required(true)`）差异 | 第 4 章 |
| O2 与独立插件两套规范 | 只教独立插件规范（V1）；O2 仅作校准注记排除 | 第 6 章 |
| 预计篇幅（用户确认压缩） | 压缩到中量：总约 12,000–15,000 字；核心章（2/3/4/6/7）保详细，过渡章（1/8/9）精简 | 全篇 |
