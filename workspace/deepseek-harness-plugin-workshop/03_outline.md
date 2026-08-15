---
title: "DeepSeek-Harness 插件实战 · 从脚手架到打包发布"
note_type: 实战
target_reader: 已读理论分册、源码环境已跑通（pnpm dsh web --patch 可用）、但从未独立写出插件的用户
estimated_words: 约 2400 字（不含代码块）
chapter_count: 7
tags: [deepseek-harness, ai, agent, 插件, 教程, 实战]
created: 2026-08-15
updated: 2026-08-15
status: draft
source_project: deepseek-harness
---

# DeepSeek-Harness 插件实战 · 从脚手架到打包发布

> [!summary] 本章导读
> 本分册是系列的「实战收尾」：不从头写（那是 [[DeepSeek-Harness 与ClaudeCode对照迁移|第 4 章]] 的活），而是把 `example-plugin`（repo_status）**改造成你自己的工具**，走通 **写 → 配 → 验证 → 打包 → 安装** 全链路。
> 每步都给：可复现命令 + 预期输出 + 出错排查。全文用 `git_log`（最近提交概览）做示范工具——它与 repo_status 同为 git 家族，改动最小、最容易照做；你的真实工具可以是任何 `defineTool` 能表达的东西（笔记检索、目录统计、API 封装）。

---

### 第一节：先看结果——你要做出什么

- **目标**：读完本节，读者能一眼看懂整条链路要交付什么（一个会出现在 Web UI 里的新工具 + 一个可安装的 bundle），并建立「基于脚手架改造」的全局心智。
- **篇幅**：约 300 字
- **素材引用**：#S7, #S8, #S9, #S5
- **代码示例**：有——目标命令链总览（8 步，照抄版）+ `git_log` 调用后的预期输出片段
- **关键坑**：无（预览性质）
- **大白话/类比**：bundle = 料理包；profile = 上菜顺序单；defineTool = 教模型一个新招式

### 第二节：环境确认 + 拷贝脚手架（5 分钟热身）

- **目标**：读者确认自己的源码环境可用，并把 vault 里的 `example-plugin` 拷贝进工作区，得到一个「自己的插件目录」。
- **篇幅**：约 300 字
- **素材引用**：#S7, #S1, #S11
- **代码示例**：有——`cp -r` 拷贝命令、`pnpm dsh web --patch ./example-plugin/dev-cordis.yml`、预期输出 `[repo-status-plugin] plugin loaded!`
- **关键坑**：开发期不要用 `npx @deepseek-ai/dsh`，`--patch` 循环必须在源码仓库根目录跑；patch 的 `name` 必须是**绝对路径**（相对路径静默失效）
- **大白话/类比**：拷贝脚手架 = 领一套带精装修的模板房，先住进去再改

### 第三节：写——把 repo_status 改造成 git_log

- **目标**：读者独立完成一次「最小改造」：新建 `src/tools/git-log.ts` 写 `defineTool`，改 `src/index.ts` 注册，并把工具名/描述/包名换成自己的。
- **篇幅**：约 500 字
- **素材引用**：#S1, #S8, #S7, #S11
- **代码示例**：有——完整 `src/tools/git-log.ts`（name/description/parameters/output/execute，`execute` 跑 `git log --oneline -n <max>`）、`src/index.ts` 的 import + `ctx.tools.register` 改动
- **关键坑**：**四处名字混淆**（`export const name` 诊断名 / package.json `name` 包名 / patch `id` 实例 id / defineTool `name` 模型可见工具名）；工具契约：execute 只返回 canonical 单值，render 负责转文本，基础设施失败直接 throw
- **大白话/类比**：defineTool = 教模型一个新招式；四处 name = 身份证 vs 工牌 vs 花名

### 第四节：配——Config schema 加可调参数 + patch 传值

- **目标**：读者给 `git_log` 增加一个可调参数（如 `maxCommits` 提交上限），写进 Config schema，并在 dev / bundle 两份 patch 里传值，理解「不硬编码可调值」的设计原则。
- **篇幅**：约 400 字
- **素材引用**：#S2, #S9, #S7, #S11, #S4
- **代码示例**：有——`src/index.ts` 的 Config interface + Schemastery schema（`Schema.number().default()`）、`dev-cordis.yml` 与 `cordis.patch.yml` 的 `config:` 传值块
- **关键坑**：Schemastery 没有 `.optional()`，必填要显式 `.required(true)`；**补丁树整行替换、不做深合并**（覆盖要重写所有需要的 key）；坏配置加载即响亮失败（ValidationError / fiber FAILED）
- **大白话/类比**：Config schema = 岗位说明书/入职登记表；`config:` 传值 = 入职时在表上填你想要的默认值

### 第五节：验证——加载、看配置层、让模型真正调用

- **目标**：读者用命令链验证四件事：插件加载成功、配置层确实注入、模型能在 Web UI 里调用 `git_log`、headless 端到端真实生效；并学会用排查表定位失败。
- **篇幅**：约 400 字
- **素材引用**：#S1, #S9, #S7, #S11, #S12
- **代码示例**：有——`pnpm dsh web --patch`（plugin loaded!）、`pnpm dsh --profile web --patch ... --dump-config`（出现 `git-log` 行）、`dsh --profile headless "任务"` 端到端、错误排查表（markdown 表格）
- **关键坑**：**模块找不到静默丢失**（先查拼写再 `--dump-config`）；`inject` 服务未就绪 → PENDING 不加载；`--patch` 配错可能静默失败（无输出=先查绝对路径）；HMR 改配置热替换、旧实例注册自动清理
- **大白话/类比**：`--dump-config` = 切开千层饼看每一层；`--profile headless` = 不点页面、直接问一句看它答不答得上来

### 第六节：打包——bundle 打包 + profile 安装 + git 安装的坑

- **目标**：读者把自己的插件装进 profile，产出可复现的「本地目录安装」路径（build → `dsh plugin add` → `--dump-config` 验证层）；并理解 git 安装为何有坑、如何规避。
- **篇幅**：约 400 字
- **素材引用**：#S5, #S9, #S7, #S11
- **代码示例**：有——`cd example-plugin && pnpm install && pnpm run build`（产出 dist/）、`dsh plugin --profile demo add ./example-plugin`、`dsh --profile demo --dump-config`（应见 `# == dsh-git-log-plugin` 层）、git 安装警示命令（`add github:you/repo#<sha>`）
- **关键坑**：**git 安装拉源码不跑 build** → 包必须带 `prepare` 脚本；pnpm≥10 需 `allowBuilds` 放行（发一张「在我机器上跑代码」的门禁卡）；`#<sha>` 钉 commit 保证可复现；bundle patch 的 `name` 必须等于 package.json `name`
- **大白话/类比**：bundle = 料理包，profile = 上菜顺序单；allowBuilds = 发一张「在我机器上跑代码」的门禁卡

### 第七节：小结与下一步——换成你自己的工具

- **目标**：读者回顾 A→C 全链路，拿到「把任意想法变成 dsh 工具」的通用 checklist，并知道发布后如何同步系列 README 与 MOC。
- **篇幅**：约 200 字
- **素材引用**：#S2, #S11, #S7
- **代码示例**：无（一张「下一步换工具」对照表：API 封装 / 笔记检索 / 目录统计 / 构建脚本）
- **关键坑**：回看第二节的绝对路径、第三节的四处名字、第六节的 allowBuilds，形成自查清单
- **大白话/类比**：改造脚手架 = 拿到模板房的钥匙后，自己决定每间房用来做什么

---

## 与第 4 章互补（避免重复）

- **第 4 章 [[DeepSeek-Harness 与ClaudeCode对照迁移]]**：主线是**从零写**——手把手搭骨架 → greet → repo_status → 配置 → 打包，每步对照 Claude Code 视角，适合想理解「插件到底怎么长出来」的读者。
- **本分册**：主线是**基于脚手架改造 + 打包发布**——直接拿现成 `example-plugin` 改造成自己的工具，聚焦 **A→C 完整链路** 与「每步可复现命令 + 预期输出 + 出错排查」。不再重复从零搭骨架（那是第 4 章的职责），读者若没读过第 4 章也可直接照做，但建议先读以便理解为什么这样写。

## 学习路径说明

### 前置要求（先读这些分册）
- [[DeepSeek-Harness 安装与快速上手|第 2 章]]：源码环境已就绪（clone → pnpm install → pnpm run build），`pnpm dsh web --patch` 能跑通。
- [[DeepSeek-Harness 插件开发核心|第 3 章]]：apply(ctx) / 生命周期 / inject / defineTool / 工具契约——本分册不重复讲概念。
- [[DeepSeek-Harness 配置体系|配置体系专册]]：补丁树、Config schema、bundle / profile 术语——第四节、第六节直接使用这些词。
- （可选）[[DeepSeek-Harness 常见坑与速查|第 5 章]]：需要排查命令时随时查。

### 学完能做什么
- 把一个 `example-plugin` 脚手架改造成自己的工具插件（`git_log` 及任意同构工具），走通写 → 配 → 验证 → 打包 → 安装全链路。
- 熟练使用验证命令链：`--patch` 加载、`--dump-config` 看配置层、Web UI 调用、headless 端到端。
- 掌握打包发布的正确姿势与坑：`prepare` / `allowBuilds` / `#<sha>` 钉 commit / bundle patch name 匹配。

### 建议学习顺序
- 第一节 → 第二节（约 15 分钟）：看目标、拷脚手架、确认环境。
- 第三节 → 第四节（约 60 分钟）：写 `git_log` + 加配置项，改完用第五节命令验证。
- 第五节（约 20 分钟）：完整验证 + 用排查表过一遍可能的失败。
- 第六节（约 30 分钟）：打包装进 profile，观察 `# == dsh-...` 层。
- 第七节（约 5 分钟）：小结 + 选一个自己的工具开始改造。
- 总计约 2 小时（不含挑自己工具的时间）。
