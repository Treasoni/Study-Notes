---
title: 从 Claude Code 迁移到 DeepSeek-Reasonix
topic: DeepSeek-Reasonix 配置教程
type: migration
difficulty: 高级
tags: [DeepSeek-Reasonix, Claude Code, 迁移, 命令对照, 概念对照, 成本对比]
created: 2026-08-10
updated: 2026-08-10
status: new
source_project: deepseek-reasonix-tutorial
---

# 从 Claude Code 迁移到 DeepSeek-Reasonix

> [!info] 文档定位
> 本文是「04-高级功能」层的对比迁移核心章：面向已熟练使用 Claude Code、想上手或整体迁移到 DeepSeek-Reasonix 的用户，把「心智模型 → 命令/概念对照 → 配置迁移步骤 → 交互差异 → 成本对比 → 迁移清单」一次讲清。它回链 [[DeepSeek-Reasonix 是什么]]（产品定位与缓存心智模型）、[[DeepSeek-Reasonix 使用指南]]（安装与 setup）、[[DeepSeek-Reasonix 前缀缓存与成本优化]]（成本推导）、[[DeepSeek-Reasonix 权限模式指南]]（权限语义）。命令与概念细节在各章已展开，本章只做对照与迁移路径、不重复定义；成本数据直接标注出处、不重做推导。全篇事实以官方文档与社区实测为限，不做超出信源的断言。

本章要解决的核心问题：**一个 Claude Code 老用户，把日常命令、配置、交互习惯迁到 Reasonix，最少需要改什么、哪些能原样保留、哪些必须换思路？**

## 一、迁移心智模型：同类 harness，不同的后端与优化目标

先把预期摆正：Reasonix 不是 Claude Code 的「换皮」，而是同一类东西（终端 AI 编程 agent harness）的另一个实现。底层哲学一致——都用计划模式、权限、工作区沙箱与逐轮 checkpoint 保证长时自治运行可读、可撤销；但有**三处实质不同**，决定了哪些能平移、哪些要重学：

1. **后端不同**。Claude Code 是通用多模型闭源 harness，默认对接 Anthropic 模型；Reasonix 是 DeepSeek 原生 agent，围绕 DeepSeek 前缀缓存深度调优（精确字节前缀匹配、命中按未命中的 ~10% 计费，原理见 [[DeepSeek-Reasonix 是什么]] 与 [[DeepSeek-Reasonix 前缀缓存与成本优化]]）。它的 provider 机制是**插件式**的，可以在 `reasonix.toml` 里声明其他 OpenAI/Anthropic 兼容端点——官方文档未出现「不支持非 DeepSeek 后端」的显式断言，教程按 provider 声明机制为准，不做绝对断言。
2. **成本模型不同**。Claude Code 走订阅（Pro/Max 套餐）或 API 按量二选一；Reasonix 走 DeepSeek API 按量 + 前缀缓存打折。缓存命中率直接决定账单，「保持上下文前缀稳定」因此从优化项变成了纪律要求（详见第六节）。
3. **生态与版本不同**。Reasonix 的命令与概念大量对齐 Claude Code（见 PR #6431 的对照），但 `CLAUDE.md` 记忆、`settings.json` hooks、`.claude/skills` 目录等资产不会自动平移，需要手动迁移（见第四节）；且 v1 与 main-v2 两版文档的命令列表不同，自查要依赖应用内 `/help`。

> [!tip] 大白话
> 把 Claude Code 和 Reasonix 想成**两家不同车厂的轿车**：都是四个轮子一个方向盘（都是终端 agent harness），你一上车就会开；但一台烧油、一台纯电，仪表盘、补能方式和保养周期全不一样。
> 所以「迁移」不是换辆车那么简单——驾驶习惯（命令）大部分通用，但「补能方式」（后端与成本模型）和「保养手册」（配置与生态）必须重新学。

## 二、命令对照表：大部分能平移，少数要记新写法

官方对齐 PR #6431 让两边的命令高度一致。逐项对照如下（Reasonix 侧以官方 CLI 参考为限）：

| Claude Code | Reasonix | 说明 |
|---|---|---|
| `claude` | `reasonix` | 交互式 CLI（TUI） |
| `claude -p "<task>"` | `reasonix -p "<task>"` / `reasonix run "<task>"` | 一次性/无头模式 |
| `claude --output-format json` | `reasonix --output-format json` | Reasonix 另支持 `stream-json` |
| `claude --allowed-tools <t>` | `reasonix --allowed-tools <t>` | session 作用域的权限放行（可重复） |
| `claude --add-dir <path>` | `reasonix --add-dir <path>` | 追加可写目录（可重复） |
| `claude --permission-mode <m>` | `reasonix --permission-mode <m>` | auto / acceptEdits / dontAsk / plan / bypassPermissions 等 |
| `claude --continue` | `reasonix --continue`（`-c`） | 恢复最近会话 |
| `claude --resume` | `reasonix --resume=true/false`、`--resume [QUERY]`（`-r`） | 会话选择器 / 按子串恢复 |
| `claude --model` | `reasonix --model NAME` | 选 provider 或 `provider/model` |
| `/model`、`/provider`、`/resume` | 对齐（picker 方向键 / Vim / `Ctrl+P` / `Ctrl+N`） | 交互习惯一致 |
| Ask / Auto / YOLO 审批 | `configOptions.tool_approval` = ask / auto / yolo | 经 ACP 协议暴露（见第 11 章） |
| `Shift+Tab` 模式循环 | Ask → Auto → Plan | `Ctrl+Y` 独立切 YOLO |

成对示例，帮助建立直觉：

```bash
# Claude Code
claude -p "把 main.go 的 TODO 实现掉" --allowed-tools "Bash(git diff:*)" --add-dir ./shared

# Reasonix 对应写法
reasonix run "把 main.go 的 TODO 实现掉" --allowed-tools "Bash(git diff:*)" --add-dir ./shared
```

> [!note] 三个需要重新记的差异
> 1. `-p` 在 Reasonix 里是 `--print`（只输出最终答案）；无头执行更常用 `reasonix run`。
> 2. `--resume` 既支持 `--resume=true/false` 布尔写法，也支持 `--resume [QUERY]` 按子串选会话。
> 3. `--output-format` 多了 `stream-json` 流式形态，CI 消费方式更多样。

## 三、概念对照表：CLAUDE.md、权限、profile、hooks 各对应什么

| 概念 | Claude Code | DeepSeek-Reasonix |
|---|---|---|
| 记忆文件 | `CLAUDE.md`（项目根） | `REASONIX.md` / `AGENTS.md`（会话内 `/init` 生成） |
| 协作模式 | 交互模式 / Plan 模式 | `normal` / `plan` / `goal` 三态 |
| 工具审批 | Ask / Auto / YOLO | `ask` / `auto` / `yolo`（同为三态） |
| 权限模式 | default / acceptEdits / plan / bypassPermissions / dontAsk | manual(ask) / auto / acceptEdits / dontAsk / plan / bypassPermissions（6 种） |
| 工作模式 | —（无对应三档） | profile：`economy` / `balanced` / `delivery`（TUI 内 `/work-mode` 热切换） |
| Hooks 配置 | `settings.json` hooks | `<Reasonix home>/settings.json`（全局）+ `<project>/.reasonix/settings.json`（项目） |
| 技能目录 | `.claude/skills/` | `[skills] paths` 声明（如 `~/my-skills`） |
| MCP 配置 | `claude mcp add` / `.mcp.json` | `reasonix.toml [[plugins]]` 或 ACP `mcpServers` |
| 项目配置 | `settings.json` / `.claude/` | `reasonix.toml` + `<project>/.reasonix/settings.json` |
| 会话内命令 | `/init`、`/compact`、`/permissions`、`/model` | `/init`、`/model`、`/provider`、`/resume`、`/work-mode`、`/effort` 等（v1/main-v2 命令列表不同，见第 4 章） |

> [!tip] 大白话
> 把 `CLAUDE.md` 和 `REASONIX.md` 想成**同一份「新员工入职手册」的两个版本**：内容都是「这个项目有什么规矩」，只是印刷方换了。
> 所以迁移时不能复制粘贴——Reasonix 认的是自己生成的 `REASONIX.md`/`AGENTS.md`，要先进会话跑 `/init` 让它按自己的格式生成，再把你原来的规矩灌进去。

## 四、配置迁移步骤：五步把家搬过去

**1. 安装 + 首次配置**

```bash
npm i -g reasonix                  # 或 brew install esengine/reasonix/reasonix
reasonix setup                     # provider、模型、API Key、连接测试、默认模型
```

关键差异在 **API Key 存储位置**：Reasonix 的 config 只存 `api_key_env` **变量名**，真实密钥放在全局 `<Reasonix home>/.env`（macOS/Linux `~/.reasonix/`，Windows `%AppData%\reasonix\`）；项目 `.env` 只作 MCP/plugin 的 `${VAR}` 展开来源，**不导入 provider key**。

**2. 项目指令：CLAUDE.md → `/init`**

不要手写复制。进入 `reasonix code .` 后运行 `/init`，生成 `REASONIX.md` / `AGENTS.md`，再把你原来 `CLAUDE.md` 里的项目规矩翻译进去。

**3. Hooks：settings.json → settings.json**

两边的 hooks 都在 `settings.json`，但文件位置不同：

```bash
# Claude Code：~/.claude/settings.json
# Reasonix：<Reasonix home>/settings.json（全局）+ <project>/.reasonix/settings.json（项目）
```

把 hooks 定义平移到新位置即可，注意 Reasonix 支持项目级覆盖。

**4. MCP servers：`.mcp.json` / `claude mcp add` → `reasonix.toml [[plugins]]`**

Reasonix 声明外部 stdio 插件走 `reasonix.toml`：

```toml
[[plugins]]
name = "example"
command = "reasonix-plugin-example"
```

或在 ACP 会话里带 `mcpServers`（MCP over ACP，见第 11 章）。原先的 MCP 字段若是旧格式，会被忽略并在保存时移除——直接按新格式重写。

**5. 技能目录：`.claude/skills/` → `[skills] paths`**

```toml
[skills]
paths = ["~/my-skills", "../shared/skills"]   # 把旧 skills 目录加进来
# excluded_paths = ["~/.agents/skills"]
# disabled_skills = ["review"]
```

迁移完跑一次体检：

```bash
reasonix doctor    # 检查 API / 配置 / hooks / 项目
```

> [!warning] 别复制粘贴，要走生成
> `CLAUDE.md`、`.claude/settings.json`、`.mcp.json`、`.claude/skills/` 这些 Claude Code 资产**不会自动读入 Reasonix**。Reasonix 认自己的路径与格式，每一类都要「换位置 + 换格式」。旧字段（如 `agent.auto_plan`、`agent.max_steps`、MCP 旧字段）会被忽略并在保存时移除，改用新写法（如 `--max-steps`）。

> [!tip] 大白话
> 把迁移想成**跨省搬家**：你的家具（CLAUDE.md、hooks、skills、MCP）都还在，但新城市的房子（Reasonix）插座布局和门锁规格不一样。
> 所以不能把旧家的开关直接拆过来装——每样东西都要「到了新家按新规格重新接一遍」，最后 `reasonix doctor` 就是搬家后的水电验收。

## 五、交互差异：快捷键、权限切换、/work-mode、preset

操作手感上，Reasonix 刻意向 Claude Code 靠拢，但有四处要重新适应：

**1. 权限模式循环：`Shift+Tab`**
Reasonix 同样用 `Shift+Tab` 循环 **Ask → Auto → Plan**，且 `Ctrl+Y` 可独立切到 YOLO（bypassPermissions）——注意它是「独立切换」，不在循环序列里。

**2. 6 种权限模式**
Reasonix 有 6 种权限模式：`manual/ask`（弹审批）、`auto`（自动批准普通操作）、`acceptEdits`（只放行文件编辑）、`dontAsk`（拒绝不弹窗）、`plan`（只读 Plan）、`bypassPermissions`（YOLO）。命令行用 `--permission-mode MODE` 指定，`--yolo` 是 bypassPermissions 别名，`--auto`/`-y` 是 auto 别名（**不能与显式 `--permission-mode` 组合**）。语义细节见 [[DeepSeek-Reasonix 权限模式指南]]。

**3. 工作模式 `/work-mode`**
Reasonix 有 Claude Code 没有的 **profile 三档**：`economy` / `balanced` / `delivery`，TUI 内 `/work-mode` 热切换（`/profile` 为兼容别名），命令行用 `--profile economy|balanced|delivery`。日常用默认 `balanced`，长时自治跑重活可上 `delivery`，省 token 用 `economy`（详见第 7 章）。

**4. `/preset`（v1）与 `/effort`（推理深度）**
`/preset auto|flash|pro` 是 **v1 特有**的会话命令，用来快速换预设；`/effort` 控制推理深度（DeepSeek 档位 high|max）。**注意**：官方没有 smart/fast/max 三档，那是社区对 `/effort` 的通俗说法。v1 与 main-v2 的命令列表不同，以应用内 `/help`、`/keys` 为实时权威。

其他手感：picker 选择器方向键 / Vim / `Ctrl+P` / `Ctrl+N` 与 Claude Code 一致；编辑门控 `y/n` 接受/丢弃待定编辑、`u` 撤销最近自动应用批次；图片粘贴 mac/Linux `Ctrl+V`、Windows `Alt+V`。

> [!tip] 大白话
> 把权限切换想成**工位门禁的几种卡**：Ask 是每次进门要刷脸，Auto 是普通房间随便进，Plan 是只准看图纸不动手，YOLO 是万能卡。
> `Shift+Tab` 就是在 Ask→Auto→Plan 三张卡之间循环换；`Ctrl+Y` 是「紧急情况摸出万能卡」——但它仍要遵守 `deny` 黑名单、沙箱和必须人工审批的工具，不是真的无法无天。

## 六、成本对比：计费模型不同，数据要看口径

Claude Code 与 Reasonix 的成本模型在结构上就不同：

| 维度 | Claude Code | DeepSeek-Reasonix |
|---|---|---|
| 计费模型 | 订阅制（Pro/Max 套餐）或 API 按量 | DeepSeek API 按量 + 前缀缓存打折 |
| 成本敏感点 | 套餐额度 / API token 单价 | **缓存命中率**（命中按未命中的 ~10% 计费） |
| 长会话成本 | 上下文随轮次线性增长、全价计费 | 长会话输入成本约 **1/5**（前缀命中） |

DeepSeek 侧的关键单价与实测（口径务必看清，完整推导回链 [[DeepSeek-Reasonix 前缀缓存与成本优化]]）：

- **单价差**：DeepSeek **缓存价约 ¥0.02/1M token vs 未缓存 ¥1/1M**，约 **50 倍**单价差——这就是「保命中率 = 省钱」的直接原因。
- **命中率区间**：Reasonix 社区/官方口径下命中率约 **94%–99.8%**（无纪律 agent 基线 <20%）。
- **用户实测（Issue #7907 对账）**：8/8 命中率 **99.6%**；全天 158 请求成本 **¥1.37**、单请求 **¥0.00869**（约 1 分钱/轮）；优化后成本再降 **-55~60%**。
- **项目自报（智源报道，非独立评测）**：单日 4.35 亿输入 token 命中率 **99.82%**；同等工作量 **$61 → $12**（约 2 折，节省约 80%）。

> [!warning] 成本数据一定要带口径
> **$61 → $12、99.82%** 来自智源 BAAI 报道转述的**项目自报数据、非独立评测**，可视为「理想工况上限参考」；**¥1.37/全天、99.6%、¥0.00869/请求** 来自 **Issue #7907 真实用户对账**，参考价值更高。做成本决策时务必区分两者，别把宣传口径当实测结论。

> [!tip] 大白话
> 把缓存命中想成**熟客会员价**：DeepSeek 的缓存 = 熟客（命中）1 折、生客（未命中）全价，差价约 50 倍。
> 所以 Reasonix 的省钱逻辑和 Claude Code 完全不同——不是「选哪个套餐」，而是「让每次请求都当熟客」。前缀稳、命中率高，长会话输入成本压到约 1/5；前缀一乱，直接回全价。

## 七、迁移清单与常见坑

**迁移清单（勾选式）**：

- [ ] 安装并 `reasonix setup`（API Key 存全局 `<Reasonix home>/.env`，config 只存变量名）
- [ ] `reasonix code .` → `/init` 生成 `REASONIX.md`/`AGENTS.md`，把 CLAUDE.md 规矩翻译进去
- [ ] 命令逐项替换：`claude -p` → `reasonix run`；`--output-format` 多一个 `stream-json`；`--resume` 支持布尔/按子串
- [ ] Hooks 平移到 `<Reasonix home>/settings.json` + `<project>/.reasonix/settings.json`
- [ ] MCP 按 `reasonix.toml [[plugins]]`（或 ACP `mcpServers`）重写；旧 MCP 字段会被移除
- [ ] `.claude/skills/` → `[skills] paths` 声明
- [ ] 权限模式与快捷键重新适应：`Shift+Tab` 循环 Ask→Auto→Plan、`Ctrl+Y` 独立 YOLO
- [ ] 按需选 profile：默认 `balanced`，长任务 `delivery`，省 token `economy`
- [ ] `reasonix doctor` 体检通过

**常见坑**：

1. **API Key 存错地方**：Reasonix 只认全局 `.env` 的真实密钥 + config 里的变量名；项目 `.env` 不导入 provider key。把 key 写进 `reasonix.toml` 是错的。
2. **直接复制 CLAUDE.md**：Reasonix 认自己生成的 `REASONIX.md`/`AGENTS.md`，要走 `/init`。
3. **v1 / main-v2 命令列表不同**：`/init`、`/plan`、`/mode`、`/budget`、`/preset` 在 main-v2 的 CLI.zh-CN **未收录**；先查应用内 `/help`、`/keys`，别照抄旧文档。
4. **`--auto` 不能与显式 `--permission-mode` 组合**；`--allowed-tools` 是权限覆盖不是 schema 过滤。
5. **`deny` 优先级最高**：配置里的 `deny` 永远压过 CLI 的 `allow` / `--allowed-tools`。
6. **无人值守忘开 `--auto`**：无头模式 fail-closed，默认拒绝写操作且审批超时默认 infinite，任务会卡住或失败。
7. **旧字段废弃**：`agent.auto_plan`、`agent.max_steps`、MCP 旧字段会被忽略并在保存时移除，改用 `--max-steps`。
8. **Windows 沙箱差异**：Reasonix 不在 Windows 提供 OS 级 Bash 沙箱，`bash="enforce"` 解析为 off。

---

一句话收束：命令能平移 80%，但「记忆文件要重新生成、API Key 换位置、缓存命中率成了新的成本变量」这三件事，是迁移时最需要换思路的地方。对着清单做一遍 + `reasonix doctor` 验收，就能把日常工作切过来。

## 常见问题

**Q：能把 CLAUDE.md 直接复制成 REASONIX.md 吗？**
A：不建议。Reasonix 用 `/init` 生成 `REASONIX.md` / `AGENTS.md`，有自己的格式与生成逻辑。正确做法是先进会话 `/init`，再把原 CLAUDE.md 里的项目规矩翻译进生成的文件。

**Q：迁移后成本一定会比 Claude Code 低吗？**
A：不能一概而论。Reasonix 的成本优势来自 DeepSeek 前缀缓存（命中按未命中的 ~10% 计费），前提是命中率够高（真实用户对账 99.6%，项目自报 99.82%）。无纪律地重排上下文、重写旧日志会打回 <20%，成本优势消失。关键单价：缓存价约 ¥0.02/1M vs 未缓存 ¥1/1M（约 50 倍差）。

**Q：`--auto` 和 `--permission-mode auto` 能一起用吗？**
A：不能。`--auto`（`-y`）就是 `--permission-mode auto` 的别名，同时指定属于重复；`--auto` 也不能与其他显式 `--permission-mode` 组合。

**Q：v1 和 main-v2 的命令为什么不一样？**
A：Reasonix 有两套文档（v1 CLI-REFERENCE 与 main-v2 CLI.zh-CN），命令列表不同，例如 `/init`、`/budget`、`/preset` 是 v1 特有。以应用内 `/help`、`/keys` 为实时权威。

## 相关文档

- [[DeepSeek-Reasonix 是什么]]：产品定位、设计哲学与缓存心智模型
- [[DeepSeek-Reasonix 使用指南]]：安装、`reasonix setup`、日常速查表
- [[DeepSeek-Reasonix 前缀缓存与成本优化]]：缓存原理、三区设计、成本实测口径
- [[DeepSeek-Reasonix 权限模式指南]]：6 种权限模式与 Shift+Tab / Ctrl+Y 交互
- [[DeepSeek-Reasonix CLI 完整参考]]：命令全集与启动参数定义

## 参考资料

- [esengine/DeepSeek-Reasonix 官方仓库](https://github.com/esengine/DeepSeek-Reasonix)
- 对齐 PR #6431（命令/概念与 Claude Code 对齐）：https://github.com/esengine/DeepSeek-Reasonix/pull/6431
- 成本实测 Issue #7907（用户对账）：https://github.com/esengine/DeepSeek-Reasonix/issues/7907
- 智源 BAAI 报道（项目自报，非独立评测）：https://hub.baai.ac.cn/view/54971
- 官方文档：`main-v2/README.zh-CN.md`、`v1/docs/CLI-REFERENCE.md`、`main-v2/docs/CLI.zh-CN.md`、`main-v2/reasonix.example.toml`

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-08-10 | 创建初稿（高级功能篇第 13 章，对比迁移核心章） |
