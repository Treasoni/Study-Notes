---
title: "第 3 章 装与接：Node 门槛、setup、MCP 与 CLI"
tags:
  - AI学习
  - 逆向工程
  - REA
  - MCP
  - AI工具
created: 2026-10-13
updated: 2026-10-13
status: 已完成
source_project: rea-reverse-engineering
---

> [[REA 逆向工程 MOC|📖 返回目录]] · [[02-能分析什么-22类目标全景|⬅ 上一章]] · [[04-实战一-静态JS与Electron分析|下一章 ➡]]

# 第 3 章 装与接：Node 门槛、setup、MCP 与 CLI

前两章讲清了 REA 是什么、能拆哪 22 类目标，但工具还停在「货架上」——你的 AI agent 还不知道它的存在。本章就是「装与接」这一步：先过 Node 版本这道硬门槛，再用一条 `setup` 命令把 REA 接进你的 agent，最后分清「配置改了哪里」和「接好之后怎么用」。

> [!tip] 大白话
> 把这一章想成「给新买的电器插电、连 Wi-Fi」：插头规格不对（Node 版本不符），怎么按开关都白搭；连上网络（MCP 注册）之后，你才谈得上用它。所以顺序不能乱——先过门槛，再接入。

## 一、第一道门槛：Node 版本对不上，一切免谈

REA 是靠 Node.js 跑的（npm 包 `rea-agents`），所以它对运行环境有明确要求：支持 **`Node.js` 22.x（≥22.19）、24.x（≥24.11）、26+**；而 **23、25 以及预发布版（prerelease）不支持**（出处见 `sources/docs_installation.md:848`）。

注意这是「偶数大版本 + 补丁下限」的写法：不是「22 以上都行」，而是 22 这一代至少要 22.19、24 这一代至少要 24.11，被跳过的 23、25 干脆不要用。

装之前先自查，免得装到一半才发现版本不符：

```bash
# 在终端查看当前 Node 版本
node -v
```

如果打印出 `v22.19.0`、`v24.11.0`、`v26.0.0` 这类，就合格；若是 `v23.x` / `v25.x`，或 `v22.18.x` 及以下，先换版本再往下走。还有一条省心的提示：REA 只用「跟当前运行时配套的那个 npm」，**从不擅自升级 Node、npm 或 Homebrew**（`sources/docs_installation.md:848`），你不必担心它把你的环境改乱。

> [!tip] 大白话
> 把 Node 版本想成电器插头的规格：22.19、24.11 是「合格插头」的型号，23、25 是「规格怪、插不进」的型号。所以不是越新越好，是「对上号才通电」。

为什么要求长得这么「挑」？因为 REA 要长期跟 Node 的运行时行为打交道，只能承诺在它**测试过**的那几代上工作。把版本写死成「偶数大版本 + 补丁下限」，是为了让「我这一版到底跑不跑得起来」有确切答案，而不是给你一个含糊的「大概能跑」。对读者的实际意义是：**别用奇数版与预发布版冒险**，出了怪问题也很难归因。

## 二、一次接进你的 agent：`setup`

过了门槛，接入就一条命令（`sources/README.md:65`）：

```bash
# 首次接入：把 REA 注册到你的 AI agent
npx rea-agents setup
```

它不是「一键装完不吭声」，而是一段**让你把关的三步交互**（`sources/docs_installation.md:20`）：先选要配置的 agent → 复核它给出的路径与改动计划 → 批准。原文与中译见章末引文表。

这里有两点新手最容易忽略：

- **两次确认是分开的**。npm 下载这个包要你批准一次，REA 的 `setup` 真正改配置（或装 Hopper）前会再问一次（`sources/docs_installation.md:20`）。别以为「点了第一次」后面就自动放行。
- **选择列表本身有讲究**。多选里，已经存在 REA 注册的客户端默认勾选；新检测到的客户端只是「被看到」，默认**不**勾选——检测是给上下文用的，不等于授权你多注册一个（`sources/docs_installation.md:31`）。

`setup` 完成后会做三件事（`sources/README.md:68`，原文与中译见章末引文表）：加入 REA 的 MCP server、加入配套的工作流指引、并**备份**你原有的配置。最后一步别忘：**重启它点名的那几个 agent**，注册才会生效。

顺带记一句：`setup` 是可以重复运行的。以后要升级 REA，重跑一遍当前版本的 `setup`，它会刷新旧的注册，再让你重启客户端（`sources/docs_installation.md:811`）。所以「注册」不是一次性的死配置，而是跟着版本走的。

> [!warning] 接完别急着怪「没反应」
> 配置写好了但没重启 agent，是新手最常见的「明明装了却用不了」。看到 `setup` 的完成信息后，按它点名的客户端逐个重启一遍再验证。

### 怎么确认真的接上了

重启只是第一步，最好再做个「合上回路」的验证：

1. **看客户端**：在 agent 的 MCP / 工具列表里，应该能看到一个名为 `rea` 的 server。
2. **看命令行**：装好后在终端敲 `rea --help`，能列出命令就说明 CLI 这条路也通了。
3. **真问一句**：对你接好的 agent 提一个需要「看目标」的需求，看它是否真的去调 REA，而不是凭记忆瞎编。

三条里有一条不通，就回到上一节核对：是不是版本没换、是不是某个客户端忘了重启。这三步能挡掉绝大多数「以为装好了」的错觉。

## 三、它到底改了你配置里的什么

如果你用的是支持手动配置的客户端，`setup` 本质上就是往 MCP 配置里加了这么一段（`sources/docs_installation.md:799`）：

```json
{
  "mcpServers": {
    "rea": {
      "command": "npx",
      "args": ["-y", "rea-agents@6.4.0", "mcp"]
    }
  }
}
```

也就是说，agent 启动时用 `npx -y rea-agents@6.4.0 mcp` 把 REA 作为一个 MCP server 拉起来。这里有一条**版本纪律**必须知道：持久化的注册要锁定一个**确切**版本，而不是 `@latest`（`sources/docs_installation.md:811`，原文与中译见章末引文表）。

| 写法 | 后果 |
| --- | --- |
| `rea-agents@6.4.0`（确切版本） | 每次启动都是同一版，行为可预期 |
| `rea-agents@latest` | 哪天发新版就悄悄漂移，排查问题时版本对不上 |

`setup` 默认就是这么做的：它写入的注册会**钉在「执行 setup 的那个版本」**上（`sources/docs_installation.md:811`）。写进配置的当前参考版本是 **`rea-agents 6.4.0`**（发布检查日 2026-10-11，`sources/docs_installation.md:207`）。想更新旧注册，就用当前版本的 `setup` 重跑一遍，再重启客户端。

为什么非要钉死版本？因为 MCP 注册是「长期驻留」的配置——写一次，之后每次开 agent 都按它启动。若写成 `@latest`，某天上游发新版，你的 agent 就悄悄换了 REA 的版本，先前跑通的用法可能行为变了却没人提醒。钉死确切版本，等于给整套环境拍了一张**可回溯的快照**，出问题时能以版本为线索定位。

> [!tip] 大白话
> 把版本锁定想成配药时记下「药厂 + 批号」：只写「某某药」迟早会拿到换了配方的同名产品；记死批号，疗效对不上时才有据可查。所以配置里那串 `@6.4.0` 不是啰嗦，是你的「批号」。

## 四、接好之后怎么用：CLI 与 MCP 两条路

接入完成后，你有两条等价的路：

- **走 agent（MCP）**：直接对你的 AI agent 提需求，它自己经 MCP 调 REA。
- **走命令行（CLI）**：装好后直接用 `rea` 命令，CLI 复用与 agent 完全相同的那套工作流。

两条路不是「二选一」，而是同一套能力的两个入口：

| | 走 agent（MCP） | 走命令行（CLI） |
| --- | --- | --- |
| 你怎么用 | 用自然语言提需求 | 敲具体命令 |
| 谁来编排步骤 | agent 自己决定调哪个工具 | 你自己选命令、看参数 |
| 适合场景 | 边聊边查、让 agent 顺带解释 | 想可复现、可脚本化，或手上没有 agent |
| 底层工作流 | 同一套 | 同一套（复用） |

命令行的入口很朴素——不知道有哪些命令时：

```bash
rea --help
```

如果不想全局安装，就用 `npx` 临时运行（`sources/docs_cli.md:9`）：

```bash
# <command> 换成具体命令名；这是不装全局的一次性运行方式
npx -y rea-agents@latest <command>
```

本章只讲「入口」，具体命令留到后面实战章和第 8 章速查表。

## 五、必须分清的一对数字：21 个客户端 ≠ 17 个 client IDs

这一节是全篇最容易读错的地方，请停一下。

- **21**：`setup` 可配置的客户端**共 21 个**（`sources/docs_installation.md:266`）。列表里包括 Claude Code、Claude Desktop、Codex、Cursor、Gemini CLI、Windsurf、VS Code、GitHub Copilot CLI、Qwen Code 等。
- **17**：这是 **`6.4.0` 这个版本**的注册表包，实际接受 dry-run 安装计划的 **client ID 数量**（`sources/docs_installation.md:209`，原文与中译见章末引文表）。

两者**作用域不同**：21 说的是「setup 能配多少个客户端」，17 说的是「某一个版本在这一批里实际通过了多少」。它们不是矛盾，更不能合成一句「支持 17/21 个客户端」。

另外单独记一条：客户端表里的 **`dsh`（DeepSeek Harness）只是 main 分支上已支持，npm 6.4.0 里并不包含它**（`sources/docs_installation.md:290`）；拿 `@latest` 去配 `dsh`，会报「不支持的客户端」，得等 6.4.0 之后的发布版本。

> [!warning] 别把两个数缝在一起
> 「21」说的是可配置客户端的宽度，「17」说的是 6.4.0 该版本实际接受的 client ID 数。看到别处写「支持 17/21 个客户端」，那是把两个不同作用域的数混着念了。

## 六、新手常见坑速查

把这一章最容易踩的四个坑收成一张表，装的时候对照着看：

| 症状 | 多半原因 | 怎么办 |
| --- | --- | --- |
| 装不上或报环境错 | Node 版本不在 22.x（≥22.19）/ 24.x（≥24.11）/ 26+ | 用 `node -v` 确认，换到合格版本 |
| 装了但 agent「没反应」 | 忘了重启 agent | 按 `setup` 完成信息点名的客户端逐个重启 |
| 行为时好时坏、排查时版本对不上 | 注册写成了 `@latest` | 改成确切版本，如 `rea-agents@6.4.0` |
| 想配 `dsh` 却报「不支持」 | 6.4.0 里还不含 `dsh` | 等 6.4.0 之后的发布版本 |

## 这一章讲了什么

- 硬门槛：Node **22.x（≥22.19）/ 24.x（≥24.11）/ 26+**；**23、25 与预发布不支持**。
- 接入一条命令 `npx rea-agents setup`，流程是「选 agent → 复核计划 → 批准」，且 npm 下载批准与 setup 批准**各自独立**。
- setup 会加 MCP server + 工作流指引、备份原配置，完成后要**重启 agent**。
- 版本纪律：注册锁定**确切版本**，当前参考 **`rea-agents 6.4.0`**（2026-10-11），手动注册形如 `npx -y rea-agents@6.4.0 mcp`。
- 客户端口径：setup 可配置 **21** 个；**17** 是 6.4.0 该版本 dry-run 实际接受的 client ID 数，**勿混述**；`dsh` 仅 main、6.4.0 不含。

## 下一章预告

工具接好了，该动真格了。第 4 章会带你跑第一条零原生引擎的实战——对一个 JavaScript / Electron 应用做静态分析，看懂「点一下导出」背后跨进程的 IPC 链路，并学会怎么读它返回的证据。

---

## 引文对照（原文 / 中译 / 出处）

> 「出处」列标注引文逐字所在的来源文件与行号；查不到来源的写 `—`（宁空不猜）。产品文件名（如 `rea-agents`）不是来源件，故不进本表。

| 序号 | 原文 | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | “Choose the agents to configure, review the proposed paths and changes, and approve the plan.” | 先选要配置的 agent，复核计划的路径与改动，再批准该计划。 | `sources/docs_installation.md:20` |
| 2 | “Setup adds REA's MCP server and matching workflow instructions, with backups of existing configuration. Restart your agent afterward.” | setup 会加入 REA 的 MCP 服务和配套工作流指引，并备份原有配置；完成后重启 agent。 | `sources/README.md:68` |
| 3 | “Persistent registrations should use one exact package version.” | 写进 agent 配置的注册应锁定一个确切包版本。 | `sources/docs_installation.md:811` |
| 4 | “The actual registry package accepted dry-run setup plans for the 17 client IDs in that release, including Qwen Code, Pi and Hermes.” | 该版本的注册表包实际接受了针对 17 个 client ID 的 dry-run 安装计划，含 Qwen Code、Pi 与 Hermes。 | `sources/docs_installation.md:209` |
