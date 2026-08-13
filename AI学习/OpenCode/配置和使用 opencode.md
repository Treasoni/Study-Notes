---
title: 配置和使用 opencode——从 Claude Code 迁移实战指南
tags:
  - opencode
  - AI编程
  - ClaudeCode迁移
  - 实战笔记
created: 2026-08-13
updated: 2026-08-13
status: 已完成
source_project: opencode-config-and-usage
---

# 配置和使用 opencode：从 Claude Code 迁移到 opencode 实战指南

> 笔记类型：实战笔记 ｜ 学习深度：精通 ｜ 主线：Claude Code → opencode 迁移

这份实战笔记面向**已经熟练使用 Claude Code、正在转向 opencode** 的你。全书以「Claude Code → opencode 迁移」为主线，按「环境搭建（第 1-3 章）→ 核心功能（第 4-5 章）→ 进阶优化（第 6-8 章）→ 运维排错（第 9 章）」的结构组织为 9 章：从 opencode 的定位与架构讲起，依次覆盖安装认证、配置体系、常用命令、权限系统、自定义 provider、MCP 集成、Skills 与自定义 Agent，最后以常见坑与排错清单收尾。每章都穿插与 Claude Code 的对照表和 `[!tip]`「大白话」类比，帮你把已有的肌肉记忆快速翻译到 opencode，而不是从零重学。

建议按顺序阅读（第 3、4 章依赖第 2 章的可运行环境；第 5-8 章相对独立可穿插）；第 9 章排错清单建议迁移过程中随用随查。

> [!note] 相关笔记
> - [[Claude Code MOC]] — Claude Code 配置与使用索引
> - [[Codex MOC]] — Codex 配置与使用索引
> - [[ModelScope-Ollama-ClaudeCode部署指南]] — 本地/开源模型部署实践

## 目录

1. [第 1 章：opencode 是什么——定位、架构与 Claude Code 全面对比](#第-1-章opencode-是什么定位架构与-claude-code-全面对比)
   - [定位与核心卖点](#定位与核心卖点)
   - [客户端/服务器架构与三种界面](#客户端服务器架构与三种界面tui--桌面--ide)
   - [内置双 Agent：build（全权限）与 plan（只读）](#内置双-agentbuild全权限与-plan只读)
   - [LSP 回喂 + Git 快照安全网](#lsp-回喂--git-快照安全网)
   - [与 Claude Code 的整体对比](#与-claude-code-的整体对比)
2. [第 2 章：安装、升级与认证——从零到能跑](#第-2-章安装升级与认证从零到能跑)
   - [安装：一键脚本与包管理器矩阵](#安装一键脚本与包管理器矩阵)
   - [升级与卸载](#升级与卸载)
   - [认证方式与凭据存储](#认证方式与凭据存储)
   - [模型列表查看与 Anthropic OAuth 限制](#模型列表查看与-anthropic-oauth-限制)
3. [第 3 章：配置体系 opencode.json——从 settings.json 迁移](#第-3-章配置体系-opencodejson从-settingsjson-迁移)
   - [3.1 先找到配置：JSONC 与 $schema](#31-先找到配置jsonc-与-schema)
   - [3.2 8 层配置优先级：合并而非替换](#32-8-层配置优先级合并而非替换)
   - [3.3 核心配置键逐个讲解](#33-核心配置键逐个讲解)
   - [3.4 变量替换：{env:VAR} 与 {file:path}](#34-变量替换envvar-与-filepath)
   - [3.5 基础配置示例逐行解读](#35-基础配置示例逐行解读)
   - [3.6 Claude Code 配置迁移映射](#36-claude-code-配置迁移映射)
4. [第 4 章：常用命令与工作流——Claude Code 命令对照速查](#第-4-章常用命令与工作流claude-code-命令对照速查)
   - [4.1 TUI 交互模式与消息语法（@ / !）](#41-tui-交互模式与消息语法--)
   - [4.2 内置 slash 命令速查表](#42-内置-slash-命令速查表)
   - [4.3 非交互 run 模式与 CI](#43-非交互-run-模式与-ci)
   - [4.4 服务与远程模式](#44-服务与远程模式)
   - [4.5 会话、统计与 agent 管理](#45-会话统计与-agent-管理)
   - [4.6 opencode ↔ Claude Code 命令对照表（本章核心）](#46-opencode--claude-code-命令对照表本章核心)
5. [第 5 章：权限系统——从「默认询问」到「默认允许」](#第-5-章权限系统从默认询问到默认允许)
   - [5.1 三值模型：allow / ask / deny](#51-三值模型allow--ask--deny)
   - [5.2 三层语法：从全局到带通配符](#52-三层语法从全局到带通配符)
   - [5.3 15 个权限键与默认基线盘点](#53-15-个权限键与默认基线盘点)
   - [5.4 收紧默认权限：从宽松到可控](#54-收紧默认权限从宽松到可控)
   - [5.5 与 Claude Code 权限模型的差异](#55-与-claude-code-权限模型的差异)
6. [第 6 章：自定义 provider 与模型路由](#第-6-章自定义-provider-与模型路由)
   - [自定义 OpenAI 兼容 provider：一个示例看懂](#自定义-openai-兼容-provider一个示例看懂)
   - [provider 引用格式：provider-id/model-id](#provider-引用格式provider-idmodel-id)
   - [npm 与 baseURL：两个最容易配错的关键约束](#npm-与-baseurl两个最容易配错的关键约束)
   - [认证备选：/connect 图形化配置](#认证备选connect-图形化配置)
   - [多模型逐步路由控成本](#多模型逐步路由控成本)
   - [模型不出现的排查要点](#模型不出现的排查要点)
7. [第 7 章：MCP 集成——把外部工具接进来](#第-7-章mcp-集成把外部工具接进来)
   - [mcp 配置键与两种类型（local / remote）](#mcp-配置键与两种类型local--remote)
   - [command 数组与 environment 环境变量](#command-数组与-environment-环境变量)
   - [OAuth 三种模式与 token 存储](#oauth-三种模式与-token-存储)
   - [mcp CLI 子命令族与 Claude Code 差异](#mcp-cli-子命令族与-claude-code-差异)
8. [第 8 章：Skills、自定义 Agent 与 AGENTS.md](#第-8-章skills自定义-agent-与-agentsmd)
   - [AGENTS.md 原生加载（与 CLAUDE.md 对应）](#agentsmd-原生加载与-claudemd-对应)
   - [SKILL.md 发现顺序与 frontmatter](#skillmd-发现顺序与-frontmatter)
   - [skill 调用语法与权限](#skill-调用语法与权限)
   - [自定义 Agent 与 hooks 限制](#自定义-agent-与-hooks-限制)
   - [跨工具复用（Claude Code / OpenCode / Cursor / Codex）](#跨工具复用claude-code--opencode--cursor--codex)
9. [第 9 章：常见坑与故障排查](#第-9-章常见坑与故障排查)
   - [认证失败：{env:VAR} 空串破坏 auth.json 回退](#认证失败envvar-空串破坏-authjson-回退)
   - [模型不出现的排查清单](#模型不出现的排查清单)
   - [常见配置坑与版本回归](#常见配置坑与版本回归)
   - [Anthropic OAuth 限定 Claude Code 提醒](#anthropic-oauth-限定-claude-code-提醒)
   - [从 Claude Code 迁移的差异提醒](#从-claude-code-迁移的差异提醒)
- [附录：参考来源](#附录参考来源)

---

## 第 1 章：opencode 是什么——定位、架构与 Claude Code 全面对比

如果你已经熟练使用 Claude Code，第一次打开 opencode 时最该问的问题不是"它怎么装"，而是"它凭什么存在"——同一个模型，为什么要换一个工具跑？这一章先回答这个问题：opencode 不是 Claude Code 的换皮克隆，而是一套在"开源、模型解耦、默认行动"三个哲学点上与 Claude Code 分道扬镳的 AI 编码代理。看懂这几个分叉点，后面所有配置差异都会变得顺理成章。

### 定位与核心卖点

opencode 的自我定位是 "The open source AI coding agent"——**MIT 开源**，来自 SST 团队，GitHub 195K+ stars、16M+ 月活开发者 [opencode 官网](https://opencode.ai)。这第一句话就已经和 Claude Code 划清界限：Claude Code 是 Anthropic 的闭源专有产品，opencode 则是你可以审计、复刻、修改的开放项目。

但它和"又一个开源 AI 编码工具"最大的区别，是**将 agent 框架与模型解耦**：

- **Claude Code**：只跑 Claude。官方没有开放模型接入层，本地模型只能靠脆弱的社区代理。
- **opencode**：75+ LLM providers（经 Models.dev）+ Ollama + 任意 OpenAI 兼容端点，通过 `provider/model` 格式自由组合 [GitHub README](https://github.com/anomalyco/opencode)。

对你这样的 Claude Code 用户，这个差异意味着两件事：其一，你已经习惯的 Claude 模型可以直接在 opencode 里继续用（配好 API key 即可）；其二，你不再被单一模型绑定——同一项目里，规划用 Sonnet、批量编辑用便宜模型、分诊用 Haiku，是完全受支持的用法。

> [!tip] 大白话
> 把"agent 框架"想成手机操作系统，把"模型"想成手机上的应用。Claude Code 是 iPhone——系统和应用是同一家做的，好用但封闭；opencode 是 Android——系统开源，你能装任何厂家的应用。所以同一个 Claude 模型在两边都能跑，但只有 opencode 让你随便换别的"应用"。

### 客户端/服务器架构与三种界面（TUI / 桌面 / IDE）

opencode 采用**客户端/服务器分离**架构：一个单后端（server）同时驱动三种前端——终端 TUI、桌面应用、VS Code / Cursor 扩展；后端通过 HTTP API 对外暴露，所以也支持把 TUI 挂到远程 Docker 会话（`opencode attach`）[官方文档](https://opencode.ai/docs/)。

对比 Claude Code：Claude Code 的 CLI 与 VS Code 扩展本质上是同一个进程的不同入口，没有清晰的"后端可被多前端共享"边界。而 opencode 的 TUI 是它的主战场，支持**多会话并行**——同一个项目可以同时启动多个 agent 处理不同任务，这在 Claude Code 里只能靠开多个终端窗口近似实现。

> [!tip] 大白话
> 把 server 想成厨房，把 TUI/桌面/IDE 想成不同的出餐窗口。Claude Code 是每个窗口自己搭了个灶台，opencode 是几个窗口共用同一个厨房——菜是同一个厨房做的，你只是换个窗口取餐。

### 内置双 Agent：build（全权限）与 plan（只读）

Claude Code 没有原生的"模式"概念，读写权限全靠每步弹窗询问。opencode 把模式下沉到了 Agent 层，内置两个 Agent，**Tab 键一键切换** [GitHub README](https://github.com/anomalyco/opencode)：

| Agent | 定位 | 权限行为 |
|-------|------|----------|
| `build`（默认） | 全权限干活 | 文件编辑、命令执行默认放行 |
| `plan`（只读） | 分析、出方案 | 文件编辑默认拒绝，bash 需要询问 |

你可以在 plan 模式下让 agent 先读代码、给方案，确认后再切到 build 执行——这正好对应你在 Claude Code 里"先聊清楚再放权限"的工作习惯，但 opencode 把它变成了一个显式的模式开关，而不是靠权限弹窗反复确认。

子代理方面，opencode 内置一个 `general` 通用子代理，通过 `@general` 在消息中调用（对应 `subagent_depth` 配置，默认 1 层）。Claude Code 的 Subagent 需要你在 `.claude/agents/` 里自己定义，opencode 则把"通用助手"这个默认角色内置了，自定义 Agent（第 8 章）是可选增强。

> [!tip] 大白话
> build 像装修队——进场就动手；plan 像设计师——只画图纸、不动墙。Claude Code 让你每次动手前都签一次字（权限弹窗），opencode 干脆设了两道门：想先看图纸就走 plan，想直接施工就走 build。

### LSP 回喂 + Git 快照安全网

这是 opencode "默认行动"哲学的底层支撑，两个机制配合：

**LSP 回喂**：opencode 自动加载项目的语言服务器（LSP），每次编辑后把编译器诊断（报错、警告、类型错误）**回喂给模型**，下一轮迭代里模型自我纠正 [GitHub README](https://github.com/anomalyco/opencode)。Claude Code 没有内建这个闭环，模型"睁眼瞎写"，只能靠你手动把编译错误贴回去。

**Git 快照安全网**：opencode 的默认权限是"行动，用 /undo 回滚"——它不靠权限弹窗挡你，而是靠 git 快照兜底。每次改动前打快照，出错 `/undo` 一键回到上一个安全点（和 Claude Code 的 `/undo` 一样基于 Git，但前者是兜底机制、后者是补救工具，哲学的先后顺序反过来了）。

> [!tip] 大白话
> LSP 回喂是"每次改完立刻有人检查作业并告诉你哪里错了"；Git 快照是"游戏自动存档"。Claude Code 的做法是每次行动前问你"确定吗"，opencode 的做法是"你先玩，存档我给你记着，玩崩了读档就行"。

### 与 Claude Code 的整体对比

综合 [DeepInfra 的替代定位分析](https://deepinfra.com/blog/claude-code-alternative) 与官方文档，逐维度对比如下：

| 维度 | opencode | Claude Code |
|------|----------|-------------|
| 开源/许可 | MIT 开源，可审计/复刻/修改 | 专有闭源 |
| 模型支持 | 75+ providers + Ollama + 任意 OpenAI 兼容端点 | 仅 Claude（官方）；本地模型靠脆弱社区代理 |
| 默认权限 | "行动，用 /undo 回滚"，透明可审计优先 | 默认只读，写文件/跑命令前询问 |
| 配置体系 | 声明式 `opencode.json`，8 层优先级合并 | CLI 命令 + `claude mcp add`，settings.json |
| 上下文文件 | `AGENTS.md`（原生加载） | `CLAUDE.md` |
| 扩展机制 | 5 类扩展点：命令、Skills、插件、自定义 Agent、MCP | 官方插件/扩展，闭环生态 |
| 速度/正确性 | 求彻底（跑全套测试验证），更慢但可检查 | 求速度，更快但可能只验证自己的改动 |
| 官方支持 | 社区/开源（SST/Anomaly），迭代快、偶发 bug | Anthropic 官方，打磨完善 |

**同模型实测**（[Builder.io 基准](https://www.builder.io/blog/opencode-vs-claude-code)，Claude Sonnet 4.5、4 个任务）：

| 任务 | Claude Code | opencode |
|------|-------------|----------|
| 跨文件重命名 | 3m6s | 3m13s |
| Bug 修复 | 41s | 40s |
| 重构 | 2m10s | 3m16s |
| 写测试 | 73 个，3m12s | 94 个，9m11s |
| **总计** | **9m9s** | **16m20s** |

结论一句话："**Claude Code 为速度而生，opencode 为彻底而生**"——opencode 会跑 `pnpm install` 加全部存量测试来验证改动，Claude Code 只验证自己改的那部分 [Builder.io](https://www.builder.io/blog/opencode-vs-claude-code)。

#### "速度 vs 彻底"的取舍

这个取舍没有绝对优劣，取决于你的场景：

- 追求**快速迭代**（改一个 bug、加一个功能，想尽快看到结果）→ Claude Code 的"只验证自己改动"更合拍；
- 追求**交付质量**（重构、改完不想留回归、测试覆盖要求高）→ opencode 的"跑全套验证"虽然慢，但"写测试 94 个 vs 73 个"这种差距说明它确实更彻底。

值得注意的是**成本**：每 token 单价 ≠ 总成本。opencode 更慢意味着更多 token 消耗，但它的架构支持**逐步路由**（progressive routing）——规划、批量编辑、分诊分别用不同模型（如便宜小模型干机械活、强模型干关键判断），这是第 6 章的核心内容，也是从 Claude Code 迁移后控制成本的主要手段 [DeepInfra](https://deepinfra.com/blog/claude-code-alternative)。

> [!tip] 大白话
> Claude Code 像快刀手——刀起刀落，只确认自己切的那块；opencode 像细活师傅——每改一处都端上来让你验一遍整体，慢但稳。选哪个，看你今天是想快点吃上饭，还是想保证这桌菜不翻车。

### 本章小结

- opencode 是 MIT 开源、将 agent 框架与模型解耦的 AI 编码代理，最大卖点是"一套框架跑任意模型"。
- 客户端/服务器分离架构：一个后端驱动 TUI、桌面、IDE 三种界面，TUI 支持多会话并行。
- 内置 build（全权限）/ plan（只读）双 Agent，Tab 切换，把"先分析后执行"变成显式模式。
- LSP 回喂 + Git 快照是"默认行动"哲学的兜底：边写边自检、出错可回滚，而不是靠权限弹窗拦截。
- 同模型实测：opencode 慢近一倍但更彻底（写测试 94 vs 73 个）；取舍取决于你要速度还是要质量。

> **下一章预告**：定位清楚了，下一步是把它跑起来。下一章讲安装、升级与认证：一键脚本的目录优先级、各平台包管理器、`opencode auth login` 与凭据存储，以及一个你必须提前知道的坑——Anthropic 已把部分 OAuth 凭据限定给 Claude Code 专用。

---

## 第 2 章：安装、升级与认证——从零到能跑

> [!summary] 本章导读
> 第一章明确了 opencode 的定位与架构。这一章把环境真正跑起来：先安装，再升级与卸载，最后完成认证——这是从「了解」到「能跑」的最后一公里。全程对照你熟悉的 Claude Code 操作习惯给出，处处可以类比。

### 安装：一键脚本与包管理器矩阵

#### 一键脚本（推荐）

opencode 官方提供一条安装脚本，思路和 Claude Code 的 `curl -fsSL ... | bash` 一致：

```bash
curl -fsSL https://opencode.ai/install | bash
```

脚本会自动选择一个安装目录，优先级从高到低：

```
$OPENCODE_INSTALL_DIR   # 显式指定，最高优先
  → $XDG_BIN_DIR        # 遵循 XDG 规范的用户 bin 目录
  → $HOME/bin           # 用户个人 bin
  → $HOME/.opencode/bin # 兜底目录
```

> [!tip] 大白话
> 把安装目录想成「快递柜」。系统先看你有没有在 `$OPENCODE_INSTALL_DIR` 这个柜子上贴指定标签，贴了就放那里；没贴就按默认顺序一个个找——先 XDG 柜、再 `~/bin` 柜，最后实在没有就放到 `~/.opencode/bin` 这个临时柜。所以想让 `opencode` 命令系统级可用，直接告诉脚本装到哪里：

```bash
OPENCODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://opencode.ai/install | bash
```

`OPENCODE_INSTALL_DIR` 相当于 Claude Code 用 `npm i -g` 时的全局前缀——它决定二进制落在哪个目录、`opencode` 命令在哪些 shell 里能直接敲出来。[安装方式见官方文档](https://opencode.ai)

#### 各平台包管理器矩阵

不用官方脚本的话，也可以用系统包管理器，体验更贴合平台习惯：

| 平台 | 命令 | 说明 |
|------|------|------|
| 通用（Node） | `npm i -g opencode-ai@latest` | 也可用 bun / pnpm / yarn 装同名包 |
| macOS / Linux | `brew install anomalyco/tap/opencode` | 官方推荐 tap，更新更快 |
| macOS / Linux | `brew install opencode` | Homebrew 官方 formula，稍滞后 |
| Windows | `scoop install opencode` | Windows 上推荐 |
| Windows | `choco install opencode` | Chocolatey |
| Arch Linux | `sudo pacman -S opencode` | 官方仓库稳定版 |
| Arch Linux | `paru -S opencode-bin` | AUR，二进制接近最新版 |
| Nix | `nix run nixpkgs#opencode` | 免安装，临时运行 |

两条提醒：安装前先移除 0.1.x 之前的旧版本，避免残留二进制与新版本冲突；桌面版目前仍是 BETA，本章不展开。

### 升级与卸载

#### 升级：opencode upgrade

```bash
opencode upgrade                # 升级到最新版
opencode upgrade 1.1.50         # 升级到指定版本（版本回归降级也用它）
opencode upgrade --method curl  # 指定升级方式
```

`--method` 可选 `curl | npm | pnpm | bun | brew`，需要和当初的安装方式一致——brew 装的用 brew 升、npm 装的用 npm 升，否则可能升不上去或产生双份二进制。

#### 卸载：opencode uninstall

```bash
opencode uninstall                  # 卸载，默认保留配置和数据
opencode uninstall --keep-config    # (-c) 保留配置文件
opencode uninstall --keep-data      # (-d) 保留会话/凭据等数据
opencode uninstall --dry-run        # 只打印会删什么，不真删
opencode uninstall --force          # 不提示直接删
```

> [!tip] 大白话
> 把 `--keep-config` / `--keep-data` 想成「搬家时要不要带走书和笔记」；`--dry-run` 是「先列一份要扔的清单给你看，你再决定动不动手」。卸载前先 dry-run 一遍，能避免误删——这跟 Claude Code 的卸载体验一样，都是「留后路」的设计。

### 认证方式与凭据存储

opencode 的认证模型与 Claude Code 基本同构：CLI 登录 + 本地存凭据 + TUI 内补录，三件套。

#### auth login / list / logout

```bash
opencode auth login                           # 交互式登录，默认 Anthropic
opencode auth login --provider anthropic      # 指定 provider
opencode auth login -p openai -m api-key      # 指定 provider 与认证方式
opencode auth list        # 等价 auth ls，查看已登录的 provider
opencode auth logout      # 登出当前 provider
```

- `--provider/-p`：要登录的 provider（anthropic、openai 等）。
- `--method/-m`：认证方式，API key 类 provider 通常填 `api-key`。

凭据统一存在 `~/.local/share/opencode/auth.json`（对应 Claude Code 的 `~/.claude/.credentials.json`）。opencode 启动时按「auth.json 凭据 → 环境变量 key → 项目 `.env` 文件 key」的顺序加载，后者补充前者，不互相覆盖。[CLI 参考见官方文档](https://opencode.ai/docs/cli)

> [!tip] 大白话
> 把 `auth.json` 想成你的「门禁卡包」，所有 provider 的 key 都集中放在这一个卡包里。`auth login` 是去物业登记办卡，`auth list` 是翻看手里有哪几张卡，`auth logout` 是把某张卡作废。环境变量和 `.env` 里的 key 相当于你兜里揣的备用卡——卡包丢了，兜里那张还能刷。

#### TUI 内 /connect

不敲 CLI 也行，TUI 交互模式里输入 `/connect`，等价于 Claude Code 的 `/login`——交互式选 provider、粘贴 key，opencode 自动写回 `auth.json`。好处是不用记 provider 的完整 ID，菜单里直接挑。

#### 服务端认证：OPENCODE_SERVER_PASSWORD

`opencode serve` / `opencode web` 起的无头服务默认需要认证，用环境变量设密码：

```bash
OPENCODE_SERVER_PASSWORD="your-password" opencode serve
```

这是 HTTP Basic Auth，用户名固定为 `opencode`，密码就是上面设的 `OPENCODE_SERVER_PASSWORD`。相当于给远程后端上了一把锁，防止未授权的人挂到你的会话上。Claude Code 没有直接对应物（它没有这种自托管无头服务模式）。

### 模型列表查看与 Anthropic OAuth 限制

#### opencode models

```bash
opencode models                # 列出所有 provider 的模型
opencode models anthropic      # 只看某个 provider
opencode models --refresh      # 强制刷新模型缓存
```

输出格式为 `provider/model`（如 `anthropic/claude-sonnet-4-5`），这正是配置文件和 `-m` 参数里要用的写法。模型列表来自 Models.dev，首次拉取有缓存；新增模型没出现时，先 `--refresh`。

#### Anthropic OAuth 限制提醒

迁移时最容易踩的坑：**Anthropic 已把部分 OAuth 凭据限定为 Claude Code 专用**，在 opencode 里用 Claude 模型不能直接沿用那个 OAuth。正确做法是去 console.anthropic.com 生成 API key，再 `opencode auth login`（或后续章节里配置 `apiKey`）。这解释了很多用户「Claude Code 里好好的，换 opencode 就 401」的现象。[详见 GitHub 仓库](https://github.com/anomalyco/opencode)

> [!tip] 大白话
> 把 Anthropic 的 OAuth 想成「A 商场专属年卡」，只认 Claude Code 这一家店；opencode 是 B 商场，你的 A 商场年卡在 B 商场刷不了。想进 B 商场，就得去前台（console.anthropic.com）重新办一张通用卡——也就是 API key。

### 本章小结

- 安装用一键脚本最简单，目录优先级 `$OPENCODE_INSTALL_DIR → $XDG_BIN_DIR → $HOME/bin → $HOME/.opencode/bin`；要系统级安装就显式设 `OPENCODE_INSTALL_DIR`。
- 包管理器矩阵覆盖 npm / brew tap / scoop / choco / pacman / Nix，按平台选，升级方式要与安装方式保持一致。
- `opencode upgrade` 升级、`opencode uninstall` 卸载，配合 `--keep-config` / `--keep-data` / `--dry-run` 做到「可回退、不误删」。
- 认证三件套：`auth login/list/logout` 走 CLI，`/connect` 走 TUI（对应 Claude Code 的 `/login`），凭据统一存 `~/.local/share/opencode/auth.json`。
- `opencode models` 输出 `provider/model` 格式；在 opencode 里用 Claude 模型需 API key，OAuth 已被 Anthropic 限定给 Claude Code。

> **下一章预告**：环境跑通了，下一步把 Claude Code 的配置体系搬到 opencode：第三章详解 `opencode.json` 的 8 层优先级、核心配置键，以及和 `settings.json` / `CLAUDE.md` 的迁移映射——这是从「能跑」到「顺手」的关键一步。

---

## 第 3 章：配置体系 opencode.json——从 settings.json 迁移

前两章你已经装好 opencode、完成认证并跑通了第一个会话。现在遇到的核心问题是：怎么把在 Claude Code 里积累的整套配置体系搬过来？Claude Code 的配置散落在 `~/.claude/settings.json`、项目级 `.claude/settings.local.json`、`CLAUDE.md` 和 `mcpServers` 里；而 opencode 把行为收敛到一份声明式 JSONC 文件 `opencode.json`，用 8 层优先级做合并。本章逐层拆开这套体系，并把 Claude Code 的每一项配置翻译成 opencode 的写法。

### 3.1 先找到配置：JSONC 与 $schema

opencode 的配置是**一份带注释的 JSON 文件**（JSONC，JSON with Comments），位置按作用域不同有三层落点：

| 作用域 | 路径 | 对应 Claude Code |
|--------|------|------------------|
| 全局 | `~/.config/opencode/opencode.json` | `~/.claude/settings.json` |
| 项目 | 项目根 `opencode.json`（向上找最近 Git 目录） | `.claude/settings.local.json` |
| 远程/组织 | `.well-known/opencode` | 企业托管 settings |

文件第一行通常是 `$schema`，它指向 JSON Schema 定义，让编辑器（VS Code 等）在你写配置时实时校验字段名和类型：

- `https://opencode.ai/config.json` — 运行时配置 schema
- `https://opencode.ai/tui.json` — TUI 界面配置 schema（状态栏、主题等界面项）

> [!tip] 大白话：把 `$schema` 想成作文考试的评分标准
> 把 `$schema` 想成作文考试的评分标准——编辑器拿着这份标准帮你检查哪句拼错了、哪个字段名不规范。所以配置第一行写 `$schema` 不是为了运行，而是为了让编辑器在写配置时就报错，把「字段名打错、类型写错」这类坑挡在运行之前。

### 3.2 8 层配置优先级：合并而非替换

这是 opencode 配置体系与 Claude Code 最本质的差异。Claude Code 是「用户 settings + 项目 settings + 托管 settings」三处叠加；opencode 把叠加拆成了 **8 层**，从高到低：

| 优先级 | 配置来源 | 说明 |
|-------|----------|------|
| 1（最高） | macOS 托管偏好（MDM `ai.opencode.managed`） | 公司/组织强制下发 |
| 2 | 托管配置文件（macOS `/Library/Application Support/opencode/`、Linux `/etc/opencode/`、Windows `%ProgramData%\opencode`） | 管理员统一部署 |
| 3 | `OPENCODE_CONFIG_CONTENT` 环境变量 | 内联一段配置 JSON，适合 CI/临时覆盖 |
| 4 | `.opencode` 目录 | 项目级扩展目录（agents、commands、plugins…），等价于 Claude Code 的 `.claude/` |
| 5 | 项目根 `opencode.json` | 从当前目录向上找最近 Git 目录 |
| 6 | `OPENCODE_CONFIG=/path/to/config.json` | 显式指定一份配置文件 |
| 7 | 全局 `~/.config/opencode/opencode.json` | 你的个人默认配置 |
| 8（最低） | 远程 `.well-known/opencode` | 组织默认基线 |

关键规则：**配置是合并（merge）而非替换（replace）**。高层配置只覆盖与低层冲突的键，低层配置里高层没提的部分依然生效。项目覆盖全局、全局覆盖远程、托管设置覆盖一切。

> [!tip] 大白话：把 8 层配置想成公司群发的 8 条通知
> 把 8 层配置想成公司群发的通知：总部（托管）的最大、部门（项目）次之、你个人（全局）最小；小通知和大通知冲突时以大为准，但大通知没管到的事项照常执行。所以配置是层层叠加，改项目里的 `opencode.json` 就能覆盖全局默认，不必担心「动了这层就推倒重来」。

这个合并机制带来一个实用推论：**你不需要在项目里复制整份全局配置**。全局放通用偏好（默认模型、通用 provider），项目只写差异项（项目专属 model、权限收紧、MCP），两者自动叠加。

### 3.3 核心配置键逐个讲解

opencode.json 顶层键大致分五类：模型、接入层、行为扩展、安全边界、外部集成。

#### 模型与智能体：model / small_model / default_agent / subagent_depth

| 键 | 作用 | 默认值 |
|----|------|--------|
| `model` | 主模型，格式 `provider/model`（如 `anthropic/claude-sonnet-4-5`） | 无 |
| `small_model` | 轻量任务模型（上下文压缩、小规模分诊等），省钱 | 无 |
| `default_agent` | 默认启动的 agent | `build`（无效时回退） |
| `subagent_depth` | 子代理递归深度 | `1` |

`small_model` 没有 Claude Code 的直接对应，是 opencode 控成本的关键：把开销小的杂活甩给便宜模型，主模型专注重活。这也是第 1 章提到的「逐步路由控成本」的配置基础。

#### provider：模型接入层

`provider` 定义「如何连接某个模型供应商」，是 opencode 模型解耦的落地处（Claude Code 无对应——它只认 Anthropic）。每个 provider 是一个对象：

- `options.apiKey`：API key，支持 `{env:VAR}`、`{file:path}`，或留空走 `/connect` 图形化认证。
- `options.timeout`：请求超时，默认 `300000` ms。
- `options.chunkTimeout`：流式分块超时。
- `disabled_providers` / `enabled_providers`：禁用/启用供应商列表（`disabled_providers` 优先）。

> [!tip] 大白话：把 provider 想成电源插头转换器
> 把 provider 想成电源插头转换器——不同厂商的 API「插座规格」各不相同，opencode 靠 provider 配置让同一套框架插进 Anthropic、OpenAI、本地 Ollama 等任何插座。所以换模型不用换工具，改一行 `provider` 引用即可。

#### agent 与 command：扩展行为

- `agent`：自定义智能体，字段为 `description`、`model`、`prompt`、`tools`；也可以用 Markdown 文件定义（第 8 章细讲）。
- `command`：自定义 Slash 命令，字段为 `template`（提示模板）、`description`、`agent`、`model`。

两者分别对应 Claude Code 的 `.claude/agents/*.md` 与自定义 slash 命令，只是 opencode 把它们声明式地收进了配置。

#### permission 与 tools：安全边界

- `permission`：opencode 的权限核心，三值模型 `allow` / `ask` / `deny`。**默认全部允许**（比 Claude Code 宽松得多），需要主动收紧，例如 `{ "edit": "ask", "bash": "ask" }`。
- `tools`：旧式布尔开关，如 `{ "write": false }`；**v1.1.1 起废弃并并入 `permission`**。

权限系统是第 5 章的主题，这里只需记住：迁移时别沿用 Claude Code 的「默认询问」心智，opencode 默认放开、靠 `/undo` 兜底，安全靠你自己写 `permission` 收紧。

#### mcp / plugin / instructions：外部集成

- `mcp`：MCP server 配置，等价于 Claude Code 的 `mcpServers`（第 7 章细讲）。
- `plugin`：npm 插件数组，opencode 的官方扩展点之一（Claude Code 无直接对应）。
- `instructions`：指令文件路径/glob 数组，把额外的上下文文件注入会话（类似追加多份 `CLAUDE.md`）。

#### 其余键：server / shell / snapshot / autoupdate / share 等

这些键在官方文档中仅有键名、缺少展开说明，按命名和使用场景可理解如下（以 `https://opencode.ai/docs/config` 为准）：

| 键 | 大致用途 |
|----|----------|
| `server` | `opencode serve` 无头服务器的相关配置 |
| `shell` | 执行 bash 命令所用的 shell 配置 |
| `snapshot` | Git 快照安全网（`/undo` 支撑）的行为配置 |
| `autoupdate` | 是否自动升级、升级通道 |
| `share` | 会话分享（`/share`）的配置 |
| `formatter` | 代码格式化器配置 |
| `lsp` | LSP 集成的行为配置 |
| `compaction` | 上下文压缩策略配置 |
| `experimental` | 实验性功能开关 |

### 3.4 变量替换：{env:VAR} 与 {file:path}

配置里允许两种占位符，在加载时被替换成真实值：

- `{env:VARIABLE_NAME}` → 环境变量的值；**未设置则为空字符串**。
- `{file:path}` → 文件内容；相对路径以配置文件所在目录为基准，支持 `/` 与 `~`。

> [!tip] 大白话：把 `{env:VAR}` 想成便签上的「见附件」
> 把 `{env:VAR}` 想成便签上的「见附件」——配置文件里不写真密钥，只写占位符，运行时去环境变量里取。所以密钥留在 shell 环境里，`opencode.json` 可以放心提交 Git，别人拿到你的配置也看不到 key。而 `{file:path}` 相当于「钥匙在保险箱里」，适合从本地文件读密钥。

注意这里的坑：第 9 章会展开 issue #34388——如果环境变量未设置，`{env:VAR}` 会被替换成空串 `""`，而 provider 回退 auth.json 用严格相等 `=== undefined`，空串会阻断回退导致 401。**用 `{env:VAR}` 时务必保证变量已导出**。

### 3.5 基础配置示例逐行解读

这是一份「从 Claude Code 迁过来的最小可用配置」，JSONC 格式允许注释：

```jsonc
{
  // 1. 编辑器校验：字段名/类型写错立刻标红
  "$schema": "https://opencode.ai/config.json",

  // 2. 主模型：格式 provider/model，对应 Claude Code settings 的 "model"
  "model": "anthropic/claude-sonnet-4-5",

  // 3. 轻量模型：压缩上下文等杂活用便宜模型
  "small_model": "anthropic/claude-haiku-4-5",

  // 4. 接入层：告诉 opencode 怎么连 Anthropic
  "provider": {
    "anthropic": {
      "options": {
        // 5. 密钥从环境变量读，不写死、可提交 Git
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  },

  // 6. 安全边界：opencode 默认全允许，这里主动收紧到"改动前询问"
  "permission": {
    "edit": "ask",
    "bash": { "*": "ask", "rm *": "deny" }
  },

  // 7. 额外上下文：把 docs 下的说明文档注入会话
  "instructions": ["docs/**/*.md"]
}
```

逐行要点：

1. **`$schema`** 让编辑器校验配置（见 3.1）。
2. **`model`** 决定默认智能体用哪个模型，格式必须是 `provider/model` 两段式。
3. **`small_model`** 承担轻量任务，是 opencode 控成本的第一道闸。
4. **`provider.anthropic.options`** 声明连接 Anthropic 所需的参数。
5. **`apiKey: "{env:ANTHROPIC_API_KEY}"`** 从环境变量注入密钥（见 3.4），对应 Claude Code 的 `apiKeyHelper` 注入思路。
6. **`permission`** 收紧默认的「全允许」：改文件、跑命令前询问，`rm *` 直接拒绝。这是从 Claude Code 迁移时最容易忽略的一步。
7. **`instructions`** 注入额外上下文文件，等效于把多份 `CLAUDE.md` 一起塞给模型。

配合第二份示例看变量替换的 `{file:}` 用法（自定义 OpenAI 兼容 provider 时的密钥读取）：

```jsonc
{
  "provider": {
    "venice": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "https://api.venice.ai/api/v1",
        "apiKey": "{file:~/.secrets/venice.key}" // 从本地文件读，支持 ~
      }
    }
  }
}
```

### 3.6 Claude Code 配置迁移映射

#### 配置体系对照

| 作用域 | Claude Code | opencode |
|--------|-------------|----------|
| 全局设置 | `~/.claude/settings.json` | `~/.config/opencode/opencode.json` |
| 项目设置 | `.claude/settings.local.json` | 项目根 `opencode.json` |
| 上下文/指令 | `CLAUDE.md` | `AGENTS.md`（原生加载） |
| 项目扩展目录 | `.claude/`（skills、agents、commands） | `.opencode/` |
| 托管/企业 | Enterprise managed settings | 8 层中的 1、2、8 层 |

#### settings.json → opencode.json 键级映射表

| Claude Code settings | opencode.json | 差异说明 |
|----------------------|---------------|----------|
| `model` | `model` / `small_model` | opencode 多了轻量模型位 |
| `permissions.allow/deny/ask`（数组式） | `permission`（三值 + glob） | 模型差异大，见第 5 章 |
| `apiKeyHelper` | `provider.<id>.options.apiKey` | 注入方式从脚本改为 `{env:}` / `{file:}` |
| `env` | 无顶层键 | 改用 `{env:VAR}` 引用 + shell 环境 |
| `mcpServers` | `mcp` | 见第 7 章 |
| `hooks` | `hooks` | 仅支持 4 个共享 hook，见第 8 章 |
| `includeCoAuthoredBy` / `cleanupPeriodDays` 等 | 无直接对应 | 忽略 |
| `enableAllProjectSkills` | 无需开关 | Skills 按 6 个位置自动发现，见第 8 章 |

#### CLAUDE.md → AGENTS.md

- `CLAUDE.md` 是 Claude Code 的上下文文件；opencode 原生加载 **`AGENTS.md`**，`/init` 也会生成它（第 2 章的 `/init` 命令）。
- 迁移时直接把 `CLAUDE.md` 内容搬进 `AGENTS.md` 即可，两份文件的写法（项目规范、指令、注意事项）互通。
- 额外的上下文文件可用 `instructions` 键按 glob 追加。

#### 迁移三步清单

1. **搬默认**：把全局 `~/.claude/settings.json` 的 `model`、provider 认证翻译到 `~/.config/opencode/opencode.json`。
2. **搬项目**：项目级 `.claude/settings.local.json` 的差异项（模型、权限、MCP）翻译到项目根 `opencode.json`。
3. **搬上下文与权限**：`CLAUDE.md` → `AGENTS.md`；把 Claude Code 的 `permissions` 数组翻译成 opencode 的 `permission` 三值+glob（务必主动收紧默认的「全允许」）。

### 本章小结

- opencode 用一份 JSONC 文件 `opencode.json` 收敛配置，`$schema` 让编辑器实时校验，`config.json` 管运行时、`tui.json` 管界面。
- 配置按 8 层优先级**合并而非替换**：项目覆盖全局、全局覆盖远程、托管设置最大；改项目文件即可覆盖全局默认。
- 核心键分五类：`model`/`small_model`（模型）、`provider`（接入层）、`agent`/`command`（行为扩展）、`permission`/`tools`（安全边界）、`mcp`/`plugin`/`instructions`（外部集成）。
- 变量替换 `{env:VAR}`（环境变量，未设置变空串）与 `{file:path}`（文件内容，支持 `~`）是「密钥不进配置文件」的关键。
- 迁移三步：搬全局 → 搬项目 → 搬上下文（`CLAUDE.md`→`AGENTS.md`）并重写权限；`permission` 默认全允许，务必主动收紧。

> **下一章预告**：配置体系搬完了，接下来是日常使用：第 4 章把 Claude Code 的命令逐个翻译成 opencode 的 TUI 交互、slash 命令和 `opencode run` 非交互模式，并给出完整命令对照速查表。

---

## 第 4 章：常用命令与工作流——Claude Code 命令对照速查

如果你已经熟练使用 Claude Code，这一章是全篇迁移的核心：把日常肌肉记忆中的 `claude`、`claude -p`、`/clear`、`/cost` 一一翻译到 opencode 的对应命令。本章按使用频率从高到低覆盖五个工作流层次——TUI 交互、slash 命令、非交互 run、服务/远程模式、会话与统计——最后给出一张完整的 opencode ↔ Claude Code 对照表，作为日后速查索引。

> [!tip] 大白话
> 把 opencode 的命令体系想成"同款菜系、不同菜单"：Claude Code 是你在熟店背熟的菜单，opencode 是隔壁新开的同菜系餐厅。菜谱（功能）大多对应，只是菜名（命令名）和上菜顺序（语法）略有不同。所以本章的重点不是"学新命令"，而是"翻译旧命令"——这也是为什么对照表放在最后压轴。

### 4.1 TUI 交互模式与消息语法（@ / !）

#### 启动

TUI 是 opencode 的默认交互界面，与 Claude Code 的 `claude` 一样：

```bash
# 当前目录启动
opencode

# 指定项目目录启动
opencode /path/to/project
```

与 Claude Code 相同，opencode 会向上查找最近的 Git 仓库根目录作为项目根；TUI 支持多会话并行——同一项目可同时启动多个 agent，彼此独立（[opencode GitHub 仓库](https://github.com/anomalyco/opencode)）。

#### @ 附加文件

在输入框里用 `@` 附加文件到当前消息，语法与 Claude Code 一致，`@` 后跟相对或绝对路径，支持 Tab 补全：

```
@src/main.go 请 review 这个文件的边界条件
```

#### ! 执行 shell

以 `!` 开头直接执行 shell 命令（结果返回 TUI），适合"先看看再提问"：

```
!ls -la
!git log --oneline -5
!cat opencode.json
```

> [!tip] 大白话
> 把 `@` 想成"把文件递给 AI 看"，把 `!` 想成"让 AI 先替我跑个命令看结果"。前者是喂输入（给材料），后者是拿输出（看现场）。Claude Code 里 `!` 也有类似语义，但 opencode 把它做成一等公民——不进入对话流，直接执行并展示结果。

### 4.2 内置 slash 命令速查表

TUI 内所有内置命令以 `/` 开头；`ctrl+x` 是 leader 键（先按 `ctrl+x`，再按功能字母）。常用命令如下（[opencode TUI 文档](https://opencode.ai/docs/tui)）：

| 命令 | 用途 | 快捷键 | Claude Code 对应 |
|------|------|--------|------------------|
| `/init` | 创建/更新 `AGENTS.md` | — | `/init` → `CLAUDE.md` |
| `/new` | 开启新会话 | `ctrl+x n` | `/clear` |
| `/sessions` | 切换/恢复历史会话 | `ctrl+x l` | `claude --resume` |
| `/compact` | 压缩上下文 | `ctrl+x c` | `/compact` |
| `/undo` | 撤销最近一次操作（Git 支撑） | `ctrl+x u` | `/undo` |
| `/redo` | 重做 | `ctrl+x r` | — |
| `/models` | 切换模型 | `ctrl+x m` | `/model` |
| `/connect` | 添加/配置 provider | — | `/login` |
| `/share` | 生成会话分享链接 | — | — |
| `/export` | 导出当前会话为 Markdown | `ctrl+x x` | `--output-format text` |
| `/exit` | 退出 TUI | `ctrl+x q` | `Ctrl+D` / `/exit` |

> [!tip] 大白话
> `ctrl+x` 想成"呼出快捷键菜单的开关"：先按它，再按功能字母，就像先按 `Ctrl` 再按 `C`。你不需要背全部快捷键——记住 `ctrl+x n`（新会话）和 `ctrl+x c`（压缩）两个最高频的就够起步。

注意几个语义差异：

- `/compact` 在两边都存在，但 opencode 的压缩策略受 `compaction` 配置键控制，细节与 Claude Code 略有不同。
- `/undo` 在 opencode 依赖 Git 快照，Claude Code 同样基于 Git——迁移成本为零。
- `/new` 与 Claude Code `/clear` 语义近似但不完全等价：`/new` 是"开新会话"，旧会话仍可通过 `/sessions` 找回；`/clear` 更接近"清空当前上下文"。opencode 的会话模型天然保留历史，这是它更接近 Cursor 的地方。

### 4.3 非交互 run 模式与 CI

`opencode run` 对应 `claude -p`，是脚本、CI、自动化里的主力（[opencode CLI 参考](https://opencode.ai/docs/cli)）。

#### 基本用法

```bash
# 单次提示，等价 claude -p "…"
opencode run "Explain the use of context in Go"

# 结构化输出（原始事件流，供脚本解析）
opencode run --format json "list every TODO with file and line"

# 指定 agent 与模型（用轻量模型做只读审计）
opencode run --agent plan --model anthropic/claude-haiku-4-5 "audit src/"

# 附加文件审查
opencode run -f src/main.go "review this file"

# 继续上次会话
opencode run -c
```

`--format json` 的输出是事件流（每条消息按类型打标签），比 `--format default` 适合脚本消费：

```bash
$ opencode run --format json "count TODO in src/" | jq 'select(.type=="message") | .message.content'
"Found 3 TODO comments in src/: lines 12, 47, 88."
```

#### 常用参数

| 参数 | 说明 | Claude Code 对应 |
|------|------|------------------|
| `--format default\|json` | 输出格式；json 为事件流 | `--output-format json` |
| `-m/--model provider/model` | 指定模型 | `-m/--model` |
| `--agent` | 指定 agent（build/plan/自定义） | 无直接对应 |
| `--variant` | 使用同一模型的变体 | — |
| `-f/--file <path>` | 附加文件作为输入 | `claude -p < file` |
| `-c/--continue` | 继续上次会话 | `-p --continue` |
| `-s/--session <id>` | 指定会话 | `--resume` |
| `--auto` | 自动批准未被 deny 的权限请求 | `--dangerously-skip-permissions` |
| `--attach <url>` | 挂到运行中的 server | 无对应 |

#### CI 示例

`--auto` 只应在 CI 中使用，是 Claude Code `--dangerously-skip-permissions` 的对应物。典型 GitHub Actions 用法：

```yaml
# .github/workflows/code-review.yml
name: opencode-review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: curl -fsSL https://opencode.ai/install | bash
      - run: |
          opencode run --format json \
            --model anthropic/claude-haiku-4-5 \
            --auto \
            "review the diff in this PR, list blocking issues" \
            | tee /tmp/review.json
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

注意 `--auto` 的边界：它自动批准**未被显式 deny** 的请求，显式 deny 仍然生效（素材 #8）——所以在 CI 里配合收紧的 `permission` 配置，比 Claude Code 的 `--dangerously-skip-permissions` 多一层保险。

> [!tip] 大白话
> `--auto` 想成"进门亮工牌的临时工"：公司门禁（权限系统）里白名单（allow）和黑名单（deny）都有效，只是不再逐个弹窗询问。这和 Claude Code 的"危险跳过权限"是同一个目的，但 opencode 保留了 deny 底线——相当于"门禁升级但没拆掉黑名单"。

### 4.4 服务与远程模式

这是 Claude Code 没有直接对应的一组能力，来自第 1 章的客户端/服务器架构（[opencode GitHub 仓库](https://github.com/anomalyco/opencode)）：

```bash
# 无头 API 服务器（给外部程序调用）
opencode serve

# 无头服务器 + Web 界面
opencode web

# 把本地 TUI 挂到远程后端（支持远程 Docker 会话）
opencode attach [url]

# ACP（Agent Client Protocol）服务器——让支持 ACP 的客户端接入
opencode acp

# GitHub 集成：生成 CI 工作流 / 在 CI 中运行
opencode github install
opencode github run
```

- `serve`/`web`/`attach` 基于"单后端驱动多个前端"的架构：`attach` 特别适合"本地 TUI + 远程服务器（如 Docker 容器）"的场景，官方用例是远程开发机。
- `github install` 会生成一份 GitHub Actions 工作流模板；`github run` 在 CI 中执行。
- `acp` 是 agent 间协议服务器，接入支持 ACP 的 IDE/客户端。

### 4.5 会话、统计与 agent 管理

```bash
# 会话列表 / 删除（配合 TUI 里的 /sessions）
opencode session list
opencode session delete <id>

# token 用量与成本统计（--days 指定窗口）
opencode stats
opencode stats --days 30

# 引导创建自定义 agent（等价手写 Markdown 文件）
opencode agent create
opencode agent list

# 其他子命令族（第 7、8 章展开）
opencode mcp add/list/auth/logout/debug
opencode plugin add <module>        # 插件管理
opencode pr <number>                # 直接处理 PR
```

这些在 Claude Code 中大多没有直接 CLI 等价：成本统计对应 `/cost`（TUI 内）、自定义 agent 对应手写 `.claude/agents/*.md`、会话管理只能靠 `--resume`/`--continue`。

### 4.6 opencode ↔ Claude Code 命令对照表（本章核心）

把前四节的映射汇总成一张完整速查表（[社区 CLI 速查 opencode-primer](https://github.com/wesammustafa/opencode-primer)）。**语义为近似对应，不是逐字等价**；标注"无直接对应"的能力是 opencode 独有，迁移时留意：

| 场景 | opencode | Claude Code |
|------|----------|-------------|
| 启动交互 TUI | `opencode` | `claude` |
| 指定项目启动 | `opencode <path>` | `claude <path>` |
| 非交互单次提示 | `opencode run "…"` | `claude -p "…"` |
| JSON 结构化输出 | `opencode run --format json` | `claude -p --output-format json` |
| 继续上次会话 | `opencode run -c` | `claude -p --continue` |
| 指定会话 | `opencode run -s <id>` | `claude --resume` |
| CI 自动批准 | `opencode run --auto` | `claude -p --dangerously-skip-permissions` |
| 指定模型 | `opencode run -m provider/model` | `claude -m model` |
| 生成项目规范 | `/init` → `AGENTS.md` | `/init` → `CLAUDE.md` |
| 新会话 | `/new` | `/clear` |
| 会话历史 | `/sessions` | `claude --resume` |
| 压缩上下文 | `/compact` | `/compact` |
| 撤销/重做 | `/undo` / `/redo` | `/undo` |
| 切换模型 | `/models` 或 `ctrl+x m` | `/model` |
| 登录/添加 provider | `/connect`、`auth login` | `/login` |
| 成本统计 | `opencode stats` | `/cost` |
| MCP 管理 | `opencode mcp add/list/auth` | `claude mcp add/list/get` |
| 自定义 agent | `opencode agent create` | 手写 `.claude/agents/*.md` |
| 分享/导出会话 | `/share` / `/export` | 无直接对应 |
| 无头服务模式 | `opencode serve`/`web`/`attach`/`acp` | 无直接对应 |
| GitHub CI | `opencode github install/run` | 无直接对应 |
| 插件管理 | `opencode plugin add` | 官方插件生态 |

> [!tip] 大白话
> 这张表就是你的"翻译词典"。迁移期把它贴在终端旁边：看到 Claude Code 命令就查左列，敲的是右列。记住三个最高频替换即可覆盖 80% 日常——`claude -p` → `opencode run`、`/clear` → `/new`、`claude -m` → `opencode run -m`。剩下的按需查表，用两周就变成肌肉记忆。

### 本章小结

- TUI 交互与 Claude Code 高度同构：`@` 附加文件、`!` 执行 shell，`ctrl+x` 是 leader 键。
- slash 命令大多能一一对应，差异集中在 `/new`（对应 `/clear`）、`/models`（对应 `/model`）与 `/sessions`（Claude Code 无直接对应）。
- 非交互 `opencode run` 是 `claude -p` 的等价物；`--auto` 是 `--dangerously-skip-permissions` 的更安全版本（保留 deny 底线）。
- `serve`/`web`/`attach`/`acp`/`github` 是 Claude Code 没有的服务/远程能力，来自其客户端/服务器架构。
- 核心速查对照表见 4.6 节，迁移期建议常驻手边。

> **下一章预告**：下一章进入权限系统：默认"行动、用 /undo 回滚"的 opencode 如何收紧成你熟悉的"默认询问"，这是从 Claude Code 迁移时最容易踩坑的差异点。

---

## 第 5 章：权限系统——从「默认询问」到「默认允许」

在 Claude Code 里，写文件、跑命令前总会弹权限确认，你已经习惯了"默认逐次询问"的节奏；切到 opencode 后你会发现弹窗几乎不出现——因为它的默认哲学是"先行动，用 `/undo` 兜底"。本章要解决的核心问题就两个：opencode 的权限系统到底怎么运作，以及从 Claude Code 迁移时如何把默认宽口径收紧到安全范围。

### 5.1 三值模型：allow / ask / deny

opencode 每个权限键的取值只有三个：

| 值 | 行为 | 对应 Claude Code 的体验 |
|----|------|------------------------|
| `allow` | 自动放行，不询问 | 等价于 `--dangerously-skip-permissions` 永久开启 |
| `ask` | 弹窗询问，确认后才执行 | Claude Code 的默认常态 |
| `deny` | 直接阻断，连问都不问 | 等价于被 `deny` 规则命中 |

这个三值模型比 Claude Code 简单——Claude Code 用数组式规则判断"这条请求符不符合某条规则"，opencode 则是给每个操作直接打上三色标签，心智负担小得多。

> [!tip] 大白话（三值模型）
> 把权限想成公司门禁的三种态度：`allow` 是看到工牌直接放行，`ask` 是刷卡要保安确认，`deny` 是直接拦下不用聊。所以给某个操作选哪个值，决定了 agent 干这活时是"无感通过"、"打断你一下"还是"根本不让干"。

### 5.2 三层语法：从全局到带通配符

`permission` 键支持三层写法，粒度逐层变细。

**第一层，顶层字符串**——整个 `permission` 块只有一个值，作用于所有权限键：

```json
"permission": "allow"
```

等价于把全部权限键设为 `allow`，这正是 opencode 的默认行为。

**第二层，工具级对象**——按权限键分别指定：

```json
"permission": { "bash": "allow", "edit": "deny" }
```

**第三层，带通配符对象**——对同一个键内的具体操作做匹配：

```json
"permission": {
  "bash": { "*": "ask", "git *": "allow", "npm *": "allow", "rm *": "deny" }
}
```

这一层的 key 是"命令模式串"，value 是 `allow`/`ask`/`deny`。第二、三层可以混用：同一个键既写了全局值，又写了模式对象时，模式对象优先。

> [!tip] 大白话（三层语法）
> 把三层想成"公司制度的三级细化"：顶层是"全公司默认"，中层是"每个部门一条规定"，底层是"某部门里某项具体动作怎么处理"。opencode 从最细的那层开始匹配，所以第三层能精确管到"`git push` 允许、`rm -rf` 拒绝"这种细颗粒度。

#### last matching rule wins 与通配符

第三层匹配规则是 **last matching rule wins**——多条规则同时命中时，写在后面的那条生效。这解释了为什么示例里 catch-all `"*"` 要放在最前：它先兜底，后面的具体规则再覆盖它。

通配符只有三个：

- `*`：匹配任意数量字符
- `?`：匹配单个字符
- `~` / `$HOME`：开头展开成用户主目录路径

> [!warning] 易错点：带参命令必须带 `*`
> `"grep"` 只匹配无参数调用，`"grep *"` 才匹配 `grep pattern file` 这种带参形式。从 Claude Code 迁移过来的人最容易漏掉这个 `*`——漏了之后规则看似生效，实际从未命中。

> [!tip] 大白话（last matching rule wins）
> 把规则列表想成"越到后面越具体的值班清单"：前面的 `*` 是"谁来都先记一笔"，后面写明的 `rm *` deny 是"看到 rm 直接拉黑"。opencode 从后往前看，最后一条命中的说了算——所以兜底放最前、特例放最后。

### 5.3 15 个权限键与默认基线盘点

opencode 的权限键共 15 个（v1.1.1 起，旧的 `tools` 布尔配置废弃并入 `permission`）：

`read`、`edit`、`glob`、`grep`、`bash`、`task`、`skill`、`lsp`、`question`、`webfetch`、`websearch`、`external_directory`、`doom_loop`、`todowrite`

其中大部分与 Claude Code 的权限维度对应（读文件、改文件、跑 shell、发请求……），`doom_loop`（同一工具连续调用 3 次）与 `external_directory`（访问项目目录之外的文件）是 opencode 特有。

**默认基线（关键认知）**：

- **绝大多数默认 `allow`**——比 Claude Code 宽松得多，这是迁移时最大的心理落差来源
- `doom_loop` 与 `external_directory` 默认 `ask`
- `.env` 系文件默认 `deny`：`*.env`、`*.env.*` 一律拒绝，`*.env.example` 放行（示例文件不含密钥）

> [!tip] 大白话（.env 默认 deny）
> 把 `.env` 想成保险箱，里面的密钥是压箱底的房产证。opencode 默认对保险箱"上锁"——任何工具想读 `.env` 相关文件都被拒，但 `*.env.example` 这种"空壳示例"是开放的。所以你在 Claude Code 里"反正会弹窗确认"的密钥读取，在 opencode 里可能直接变成 `deny`，更安全，但有时也会卡住正常调试，心里要有数。

### 5.4 收紧默认权限：从宽松到可控

如果你还不习惯"默认允许"，迁移第一步就是把全局默认从 `allow` 改成 `ask`，再逐步放行白名单命令：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "*": "ask",
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm *": "allow",
      "rm *": "deny",
      "git push *": "deny"
    }
  }
}
```

逐行解读这个"迁移安全配置"：

1. `"*": "ask"` 全局兜底：所有没单独列出的操作都弹窗，把 opencode 拉回 Claude Code 的询问节奏
2. `"git *": "allow"` / `"npm *": "allow"`：放行日常高频的无风险命令，避免每个 `git status` 都打断你
3. `"rm *": "deny"`：删除类命令直接阻断
4. `"git push *": "deny"`：关键点——它写在 `git *` **之后**，按 last matching rule wins 覆盖前面的放行。推送到远程是红线，不管前面放行了多少 `git` 子命令

> [!tip] 大白话（收紧配置）
> 把兜底 `"*": "ask"` 想成"双保险"：就算你在下面漏写了某个危险命令的规则，最外层的 `ask` 也会兜住它，agent 必须先问你一声才动手。所以这套配置的精髓是"**兜底写 `ask` 或 `deny`，白名单写 `allow`，具体规则放在兜底后面**"。

#### --auto 与 CI 自动批准

非交互模式下的 `--auto` 会自动批准"未被显式 `deny`"的权限请求，官方文档明确标注**仅用于 CI**：

```bash
opencode run --auto --format json "run the full test suite"
```

它的语义与 Claude Code 的 `claude -p --dangerously-skip-permissions` 类似，但有一个关键区别：

- `--auto` **不会绕过显式 `deny`**——`deny` 仍是硬性红线
- 只有 `ask` 会被自动批准，`deny` 依然阻断

所以在 CI 里，`--auto` + 收紧的 `permission` 是"无人值守自动跑、但危险操作仍被拦"的组合拳：日常命令全部放行提速，`rm`/`git push` 这类命令即使在流水线里也被拦死。

#### Agent 级权限优先级

全局 `permission` 之外，还可以给单个 agent 单独配权限：

```json
{
  "agent": {
    "plan": {
      "permission": { "edit": "deny", "bash": "ask" }
    }
  }
}
```

**Agent 级权限（`agent.<name>.permission`）优先于全局**。这很适合给只读分析型 agent（如 `plan`）强制"只读"，给 `build` 保留全权限。权限是跟着 agent 走的，不是跟着会话走的——同一会话里切到 `plan`，它的只读限制立刻生效。

### 5.5 与 Claude Code 权限模型的差异

| 维度 | opencode | Claude Code |
|------|----------|-------------|
| 规则形态 | 工具名 + 输入 glob 模式 | 数组式规则，顺序无关 |
| 冲突策略 | last matching rule wins（后面覆盖前面） | deny 优先（任何 deny 都赢） |
| 默认基线 | 大多数 `allow`，只对 `.env` / `doom_loop` / `external_directory` 收紧 | 默认只读，写文件/跑命令逐次询问 |
| 输入级匹配 | 强（支持 glob 通配符、`?`、`~` 展开） | 弱（规则匹配不够精细） |
| CI 自动批准 | `run --auto`（不绕过 deny） | `-p --dangerously-skip-permissions`（全跳过） |
| 配置位置 | 声明式 `opencode.json` 的 `permission` 键 | `settings.json` 的 `permissions` 数组 + 逐次弹窗 |

一句话总结迁移认知：**Claude Code 是"默认拦、白名单放行"；opencode 是"默认放、黑名单拦截 + 局部白名单收紧"**。前者保护过度但安全，后者高效但需要你自己把红线画出来——这正是本章 5.4 节那套配置存在的意义。

### 本章小结

- opencode 用三值 `allow`/`ask`/`deny`，比 Claude Code 的数组式规则更简洁直观
- 三层语法从全局字符串到带通配符对象，粒度可下探到 `git push *`；匹配规则 last matching rule wins，兜底放最前、特例放最后
- 带参命令必须写 `*` 后缀（`"grep *"` 才匹配带参调用），是最常见的漏配点
- 默认基线宽松：大多 `allow`，`.env` 默认 `deny`，`doom_loop`/`external_directory` 默认 `ask`；迁移第一步是改成 `"*": "ask"` 兜底
- `--auto` 只批准 `ask`、不绕过 `deny`；Agent 级权限优先于全局，适合给只读 agent 强制约束

> **下一章预告**：权限管住"agent 能干什么"，接下来要管"用哪个模型干"。第六章讲自定义 provider 与多模型逐步路由，把成本和能力也一并调度起来。

---

## 第 6 章：自定义 provider 与模型路由

上一章把权限系统调到了自己舒服的基线，这一章解决一个更根本的问题：opencode 到底能跑哪些模型？答案比 Claude Code 开放得多——**任何 OpenAI 兼容端点都能接进来**，这正是"模型与框架解耦"卖点的落地。本章通过一个完整示例，带你自定义 provider、理解两个关键约束，并学会用多模型路由控制成本。

### 自定义 OpenAI 兼容 provider：一个示例看懂

在 Claude Code 里，你要换模型基本被锁死在 Anthropic 生态；opencode 则允许你在 `opencode.json` 的 `provider` 键里声明任意 OpenAI 兼容服务商。下面是一个完整示例，接入 Venice AI 的一个 GLM 模型 [Venice AI opencode 集成文档](https://docs.venice.ai/guides/integrations/opencode)：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "venice/zai-org-glm-5-1",
  "provider": {
    "venice": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Venice AI",
      "options": {
        "baseURL": "https://api.venice.ai/api/v1",
        "apiKey": "{env:VENICE_API_KEY}"
      },
      "models": {
        "zai-org-glm-5-1": { "name": "GLM 5.1" }
      }
    }
  }
}
```

逐行拆解：

- `provider.venice`：provider 的**内部 ID**，你自己起名，全局唯一。
- `npm`：告诉 opencode 用哪个 AI SDK 驱动去对话，接 OpenAI 兼容服务一律填 `@ai-sdk/openai-compatible`。
- `options.baseURL`：该服务商**兼容 OpenAI 的 API 根路径**，必须是官方 v1 端点。
- `options.apiKey`：密钥。优先用 `{env:VAR}` 从环境变量读（比把密钥写死在配置里安全得多）。
- `models`：这个 provider 下可用模型的 map。key 是 `model-id`，`name` 只是展示名。

> [!tip] 大白话
> 把 provider 想成「门禁卡办理处」：`npm` 告诉门禁系统读哪种卡格式，`baseURL` 告诉它刷卡机装在哪栋楼，`apiKey` 是发到你手里的门禁卡。三样齐了，任何长得像 OpenAI 的楼你都能刷卡进去——所以「任意 OpenAI 兼容端点」并不是玄学，只是把这套门禁配置标准化了。

### provider 引用格式：provider-id/model-id

配好之后，所有需要指定模型的地方都用**斜杠拼接**的格式：

```bash
opencode run -m venice/zai-org-glm-5-1 "重构 src/lib"
```

其中 `venice` 是上一步你自己起的 provider ID，`zai-org-glm-5-1` 是 `models` map 里的 key。`/models`（或 `ctrl+x m`）切换模型、`opencode models [provider]` 查看可用模型，输出都是这种 `provider/model` 格式 [opencode CLI 文档](https://opencode.ai/docs/cli)。

**命名冲突要注意**：provider ID 是全局命名空间。你自定义的 ID 不能和内置的 `anthropic`、`openai` 等重名，否则会覆盖内置 provider。

### npm 与 baseURL：两个最容易配错的关键约束

自定义 provider 九成的问题出在这两个字段 [opencode 认证与 provider 排错](https://opencode.ai/docs/config)：

| 字段 | 正确写法 | 配错的后果 |
|------|---------|-----------|
| `npm` | 恒为 `@ai-sdk/openai-compatible`（接兼容端点时） | SDK 与端点不匹配，协议解析失败 |
| `baseURL` | 服务商官方的 v1 兼容端点（如 `.../api/v1`） | endpoint 对不上，404 / 401 |

> [!tip] 大白话
> `baseURL` 就像「导航填的收货地址」——差一个 `/v1` 后缀、多个一级目录，包裹就送不到。`npm` 则像「快递公司」，兼容端点统一走 OpenAI 这家快递，别自己换别的公司。

### 认证备选：/connect 图形化配置

不想手写 `apiKey`？TUI 里输入 `/connect`，选 **Other**，填 provider ID，粘贴密钥即可完成认证。此时凭据写入 `~/.local/share/opencode/auth.json`，你就可以把配置里的 `options.apiKey` 删掉，让 provider 回退到已存的凭据。

> [!warning] 两种写法别双写冲突
> `{env:VAR}` 与 `/connect` 二选一即可。混用时若 env 未导出，会被替换成空串 `""`，而 provider 回退逻辑用的是严格相等 `=== undefined`——空串会**吞掉** auth.json 里已存好的凭据，导致 401（issue [#34388](https://github.com/anomalyco/opencode/issues/34388)）。用 `{env:VAR}` 就保证该变量在启动 opencode 的同一个 shell 里已导出。

### 多模型逐步路由控成本

opencode 支持给不同任务配不同模型，从根上控制 token 成本 [opencode vs Claude Code 实测对比](https://www.builder.io/blog/opencode-vs-claude-code)。核心思路是**把贵的推理留给真正需要它的步骤**：

- **规划（plan）**：用强模型做架构分析，只读不写，一次规划价值最高。
- **批量编辑 / 机械重构**：用便宜的小模型（`small_model`），改完靠测试兜底。
- **分诊（triage）/ 摘要 / 日志分析**：最便宜的快模型，量大也不心疼。

```bash
# 一次性计划任务用便宜模型跑（只读分析，风险低）
opencode run --agent plan -m openai/gpt-4o-mini "审计 src/ 的循环依赖"
```

配合第三章讲过的 `small_model`（轻量任务默认模型）和 `--agent plan`，你可以在不降低主任务质量的前提下，把次要步骤的 token 花费降一个数量级。

> [!tip] 大白话
> 逐步路由就像「装修分工」：画图纸请大师傅（强模型，一次到位），砌墙让普通工人干（便宜模型，活干对就行），搬垃圾找临时工（最便宜）。不是所有活都得让顶配专家做——成本瞬间就下来了。

### 模型不出现的排查要点

配完发现 `/models` 里看不到你的模型？按这个顺序查 [opencode provider 排错](https://opencode.ai/docs/config)：

1. **`models` map 是否注册**：没在 `provider.<id>.models` 里声明的模型不会出现在列表里。
2. **API key 是否在同一个 shell 导出**：`{env:VAR}` 读的是启动 opencode 的进程环境，换个 shell 就丢。
3. **是否在项目目录运行**：只有从项目根（最近的 Git 目录）启动，才会加载项目的 `opencode.json`；在别的目录启动只会读到全局配置。
4. **`baseURL` / `npm` 是否配错**：端点对不上，provider 初始化就失败，模型自然不出现。

### 本章小结

- opencode 通过 `provider` 键接入任意 OpenAI 兼容服务商，`npm` 恒填 `@ai-sdk/openai-compatible`，`baseURL` 必须指向官方 v1 端点。
- 模型统一用 `provider-id/model-id` 引用；自定义 provider ID 不能与内置 provider 重名。
- 认证可用 `{env:VAR}` 或 `/connect` 图形化完成，但两者别混用，避免空串吞掉 auth.json 凭据。
- 用「规划用强模型、批量/分诊用便宜模型」的路由思路，可在不降质的前提下显著控制 token 成本。
- 模型不出现时，按「models map → shell 环境变量 → 项目目录 → 端点配置」四步排查。

> **下一章预告**：下一章进入 MCP 集成，看看怎么把外部工具（文件系统、数据库、各种 API）以标准协议接进 opencode，让 agent 的触手伸得更远。

---

## 第 7 章：MCP 集成——把外部工具接进来

**本章问题**：在 Claude Code 里你已经习惯了 `claude mcp add/list/get`，到了 opencode 如何把同一套 MCP server 接进来？本章讲清 opencode 的 `mcp` 配置键、local/remote 两种类型、`command` 数组与 `environment` 键、OAuth 三种模式，以及从 `mcpServers` 迁移的完整对照。

### mcp 配置键与两种类型（local / remote）

opencode 在 `opencode.json` 中用顶层 `mcp` 键声明 MCP server（Claude Code 对应 `mcpServers`）[opencode MCP 文档](https://opencode.ai/docs/mcp)。与 Claude Code 最大的不同是：**每一项必须带 `type` 字段**，用来区分两种传输方式：

- `local`：以子进程方式启动（STDIO 协议）。server 作为本地子进程运行，与 opencode 通过标准输入输出通信。适合跑在本机的工具，如文件系统、Git 辅助工具。
- `remote`：以 HTTP/SSE 协议连接远程 URL。server 部署在远端，通过 `url` 访问，适合多人共享的工具服务。

> [!tip] 大白话
> 把 MCP server 想成「智能家电的插线板」：opencode 不内置这些技能，但通过统一插口把外部能力接进来。`local` 是把一个助手直接请进家里住（子进程，走内部的传话管道 STDIO）；`remote` 是打电话给远端的客服中心（HTTP/SSE）。

#### local 配置示例

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "filesystem": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "environment": { "NODE_ENV": "production" },
      "timeout": 30000
    }
  }
}
```

#### remote 配置示例

```json
{
  "mcp": {
    "remote-tools": {
      "type": "remote",
      "url": "https://mcp.example.com/v1",
      "headers": { "X-API-Key": "sk-..." }
    }
  }
}
```

### command 数组与 environment 环境变量

两个与 Claude Code 直接冲突的写法，迁移时最容易踩坑：

1. **`command` 用数组，不用字符串**。Claude Code 里 `"command": "npx -y @modelcontextprotocol/server-filesystem /tmp"` 是整条 shell 命令；opencode 要求拆成 `["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"]`。这样做是为了避免 shell 注入——参数不经过 shell 解析，原样传给子进程。
2. **环境变量键叫 `environment`，不叫 `env`**。Claude Code 用 `env`，opencode 用 `environment`。

> [!tip] 大白话
> `command` 用数组就像餐厅点菜：Claude Code 是「你对着厨房喊一嗓子」——喊话内容会被完整转述（存在歧义和注入风险）；opencode 是把菜名逐个写在单子上递给厨房——每道菜都是独立的一项，不存在被「带偏」的解析空间。

`timeout` 默认 30000ms（30 秒），超过即视为子进程启动失败；遇到首次 `npx` 拉包较慢时可适当调大。语义与 Claude Code 的 `claude mcp add --timeout` 一致。

#### 实战：把一条 `claude mcp add` 迁移过来

假设你在 Claude Code 里跑过这条命令：

```bash
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /tmp --env NODE_ENV=production
```

迁移到 opencode 分三步：把键名换成 `mcp`、补上 `"type": "local"`、把 command 和 env 按新格式改写。注意 `claude mcp add` 里的 `--env` 是命令参数，而 opencode 要求放在 `environment` 块里：

```json
{
  "mcp": {
    "filesystem": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "environment": { "NODE_ENV": "production" },
      "timeout": 30000
    }
  }
}
```

相比 Claude Code 把配置写进 `.mcp.json`，opencode 的 `mcp` 块直接落在 `opencode.json`，因此能享受第 3 章讲过的 8 层配置优先级——例如项目级覆盖全局、不同项目可以各自声明不同的 server。

### OAuth 三种模式与 token 存储

远程 MCP server 往往需要认证。opencode 内建 OAuth 流程，支持三种模式 [opencode MCP 文档](https://opencode.ai/docs/mcp)：

| 模式 | 配置 | 说明 |
|------|------|------|
| 自动发现（默认） | 不配置 `oauth` | 按 RFC 7591 动态注册客户端，自动走 OAuth 授权流程 |
| 预注册客户端 | `"oauth": { "clientId": "..." }` | server 要求固定 clientId，跳过动态注册 |
| 禁用 | `"oauth": false` | 不做 OAuth，改用 API key 等静态凭据认证 |

> [!tip] 大白话
> OAuth token 像「临时工牌」：进门（连上远程 server）时 opencode 帮你自动申请一张，到期自动换新。`clientId` 是「你有专属工牌编号」；`oauth: false` 是「不用工牌，直接刷门禁卡（API key）」。

**token 存储位置**：`~/.local/share/opencode/mcp-auth.json`，与全局认证凭据 `auth.json` 分开存放。排查授权问题时直接看这个文件。

注意：**用 API key（如 `headers`）认证的远程 server 必须显式 `"oauth": false`**，否则 opencode 默认先尝试 OAuth 流程，可能与你预期的认证方式冲突。这也是排查远程 server「连不上」时优先检查的三件事之一：`type` 是否写对、`url` 是否可达、`oauth` 是否与认证方式匹配。

#### local 还是 remote？怎么选

判断依据很简单：server 是否与你的项目运行在同一台机器上。文件系统、Git、数据库扫描这类工具用 `local`（子进程直连，延迟低、无网络暴露）；团队共享的服务、需要集中鉴权的工具用 `remote`（统一部署，客户端只存 URL 与凭据）。如果拿不准，先用 `local` 起步，后续再改为 `remote` 迁移成本很低——两者只是 `type` 与连接字段不同。

### mcp CLI 子命令族与 Claude Code 差异

`opencode mcp` 是一族子命令，比 Claude Code 的 `claude mcp add/list/get` 更完整 [OpenCode GitHub](https://github.com/anomalyco/opencode)：

```bash
opencode mcp list                  # 列出所有 server 及连接状态
opencode mcp debug <name>          # 诊断某个 server 的配置与连接
opencode mcp auth                  # 手动触发 OAuth 授权
opencode mcp logout                # 清除已存的 token
opencode mcp add ...               # 通过 CLI 添加 server（等价于写配置）
```

`mcp list` 用四种状态符号快速定位问题：

- `✓ connected`：已连接可用
- `○ disabled`：已配置但被禁用
- `⚠ needs_auth`：需要授权（未登录或 token 过期）
- `✗ failed`：连接失败，用 `mcp debug` 查原因

遇到 `⚠ needs_auth` 先跑 `opencode mcp auth` 走一遍授权；遇到 `✗ failed` 跑 `opencode mcp debug <name>`，它会打印 server 的解析结果与实际连接错误，比对着配置文件猜高效得多。整个排查闭环与 Claude Code 的 `claude mcp get` + `--verbose` 思路一致，只是命令名不同。

#### mcpServers → mcp 迁移对照表

| 维度 | Claude Code | opencode |
|------|-------------|----------|
| 配置键 | `mcpServers` | `mcp`（每项必须带 `type`） |
| command 形式 | 字符串（shell 解析） | 数组（无 shell，防注入） |
| 环境变量键 | `env` | `environment` |
| OAuth | 依赖 server 端 URL 流程 | 内建自动发现（RFC 7591）/ clientId / 禁用 |
| token 存储 | `~/.claude.json` / 浏览器会话 | `~/.local/share/opencode/mcp-auth.json` |
| CLI | `claude mcp add/list/get` | `opencode mcp add/list/debug/auth/logout` |
| 配置落点 | `.mcp.json` / `claude mcp add` 写入 | `opencode.json` 的 `mcp` 键 |

### 本章小结

- opencode 的 `mcp` 键对应 Claude Code 的 `mcpServers`，但每项必须带 `type`（`local` STDIO 子进程 / `remote` HTTP/SSE）。
- `command` 用数组防 shell 注入，环境变量键是 `environment`，`timeout` 默认 30000ms。
- OAuth 三模式：自动发现（默认，RFC 7591）/ 预注册 `clientId` / `oauth: false` 禁用；token 存 `~/.local/share/opencode/mcp-auth.json`。
- `opencode mcp list/debug/auth/logout` 提供完整子命令族，`list` 用四种状态符号快速定位连接问题。

> **下一章预告**：外部工具已经接进来了，下一步是把「内部能力」标准化——Skills、自定义 Agent 与 `AGENTS.md`，看它们如何像 Claude Code 的 Skills 与子代理一样被发现和复用。

---

## 第 8 章：Skills、自定义 Agent 与 AGENTS.md

对熟悉 Claude Code 的你来说，`CLAUDE.md` 和 `.claude/skills/` 是日常定制的两大支柱。这一章把这两根支柱搬到 opencode：`AGENTS.md` 如何原生加载、SKILL.md 的六个发现位置怎样兼容你的存量技能、`skill()` 怎么调用、自定义 Agent 与 hooks 有哪些限制。把这些差异吃透，你就能把 Claude Code 的整套定制"平移"到 opencode，而不是从零重写。

### AGENTS.md 原生加载（与 CLAUDE.md 对应）

opencode 原生读取 `AGENTS.md` 作为项目上下文文件，语义上等价于 Claude Code 的 `CLAUDE.md`。在 TUI 里执行 `/init` 会创建或更新项目的 `AGENTS.md`——对照表里它正是 Claude Code `/init` 生成 `CLAUDE.md` 的对应物。

| 操作 | opencode | Claude Code |
|------|----------|-------------|
| 项目上下文文件 | `AGENTS.md` | `CLAUDE.md` |
| 生成命令 | `/init` | `/init` |

一个值得注意的差异：`AGENTS.md` 是跨工具的标准文件名（Cursor、Codex、opencode 都在读），所以同一份项目规范天然能在多个工具间复用；而 `CLAUDE.md` 是 Anthropic 专属约定，出了 Claude Code 就没用了。[官方 Skills 文档](https://opencode.ai/docs/skills)

> [!tip] 大白话
> 把 `AGENTS.md` 想成「给 AI 同事的项目说明书」——和 `CLAUDE.md` 是同一件东西，只是牌子换成了行业通用款。所以你在 Claude Code 里写在 `CLAUDE.md` 的"项目怎么跑、有哪些约定"，原样搬进 `AGENTS.md` 就能在 opencode 生效，还能顺带给别的工具看。

### SKILL.md 发现顺序与 frontmatter

SKILL.md 的存放模式是 `<base>/skills/<name>/SKILL.md`，opencode 按六个位置发现技能：

1. 项目 `.opencode/skills/`
2. 全局 `~/.config/opencode/skills/`
3. 项目 `.claude/skills/`
4. 全局 `~/.claude/skills/`
5. 项目 `.agents/skills/`
6. 全局 `~/.agents/skills/`

> [!tip] 大白话
> 把六个位置想成「厨房里六个调料抽屉」——只要技能放进任何一个抽屉，opencode 都能翻到。重点看第三、四个抽屉：`.claude/skills` 被 opencode 直接兼容读取，你在 Claude Code 里攒下的技能一个都不用搬，它自己就能找到。

frontmatter 字段比 Claude Code 更精简，只认五个：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 小写 + 连字符（如 `git-release`） |
| `description` | 是 | 1-1024 字符，模型据此决定何时调用 |
| `license` | 否 | 技能许可 |
| `compatibility` | 否 | 兼容的工具/版本 |
| `metadata` | 否 | 自由扩展信息 |

素材中缺一个完整的最小 SKILL.md 示例，这里补一个最小可用的：

```markdown
---
name: git-release
description: Create a semantic version release, tag it, push tags, and print a changelog.
license: MIT
compatibility:
  - opencode
  - claude-code
metadata:
  author: you
---

## What it does

Cuts a new release: bumps the version, commits, tags, pushes, and prints a short changelog.

## Steps

1. Read `package.json` to confirm the current version.
2. Ask the user for the next version.
3. Run `npm version <next>` and `git push --tags`.
4. Print the commit list since the last tag as the changelog.
```

要点：`name` 必须小写 + 连字符（模型用它在 `skill()` 里精确点名），`description` 是模型判断"什么时候该用这个技能"的唯一依据，值得写清楚触发场景。

### skill 调用语法与权限

模型在对话中通过 `skill()` 函数调用技能：

```
skill({ name: "git-release" })
```

技能是否允许被执行，由权限键 `permission.skill` 控制，三值 `allow` / `ask` / `deny` 加通配符，沿用第五章的"last matching rule wins"规则：

```json
{
  "permission": {
    "skill": { "*": "ask", "git-release": "allow" }
  }
}
```

上面配置的含义：默认所有技能先弹窗询问，只有 `git-release` 直接放行。

> [!tip] 大白话
> `skill()` 想成「给熟练工友打内线电话」——模型拨号（写 `skill({ name: ... })`），总机（`permission.skill`）决定这通电话是直接接通还是先请示你。所以技能写好了不算完，权限放行才真正可用。

### 自定义 Agent 与 hooks 限制

自定义 Agent 有两种定义方式：Markdown 文件或 `agent create` 命令。

**Markdown 文件**：放在 `.opencode/agents/`（项目）或 `~/.config/opencode/agents/`（全局），用 frontmatter 声明属性，正文是系统提示词：

```markdown
---
model: anthropic/claude-sonnet-4-5
description: 只读代码审查助手，不改代码
---

你是资深工程师，只做分析、给出修改建议，不执行任何编辑。
```

**CLI 引导**：`opencode agent create` 交互式创建，可用 `--permissions` / `--tools` 指定该 agent 的权限与工具；`opencode agent list` 查看已有 agent。这比 Claude Code 手写 `.claude/agents/*.md` 多了一条可视化入口。[官方 Agents 文档](https://opencode.ai/docs/agents)

此外也能在 `opencode.json` 里用 `agent` 键声明式定义（字段为 `description`、`model`、`prompt`、`tools`），与第三、五章的配置体系一脉相承。

**hooks 限制**：opencode 只支持 4 个共享 hook，Claude Code 的整套 hooks 体系不会照搬：

| hook | 大致用途 | 对应 Claude Code 思路 |
|------|----------|----------------------|
| `guard-shell` | shell 命令执行前守卫 | PreToolUse 守卫 |
| `guard-read-large` | 大文件读取守卫 | 超大读取保护 |
| `inject-types-on-read` | 读取时注入类型上下文 | 上下文注入 |
| `check-on-edit` | 编辑后检查 | PostToolUse |

迁移提醒：如果现有 Claude Code 配置挂了很多自定义 hook，只有这 4 个在 opencode 有对应物，其余要么换用权限规则（第五章），要么用插件机制替代。

> [!tip] 大白话
> hooks 想成「机场安检口」——opencode 目前只开了四个口（上表），你在 Claude Code 里装的那一排"特殊通道"（自定义 hook）大多过不来。迁移前先盘点：哪些守卫能落到这四个口子上，哪些要改写成权限规则。

### 跨工具复用（Claude Code / OpenCode / Cursor / Codex）

把整套 skills/agents/guardrails 做成"一套资产、多工具适配"是更省力的终局，典型思路是 spine 这类适配器项目：以工具无关的 `.agents/skills/` 和 `AGENTS.md` 为核心，通过薄适配层接到各工具的加载机制。[spine 项目](https://github.com/kenoxa/spine)

结合本章的六个发现位置，推荐一条渐进迁移路径：

1. **零改动过渡**：先保留技能在 `.claude/skills/`（位置 3/4），opencode 直接读取，Claude Code 也照常工作——双工具并行期无感知。
2. **工具无关化**：把希望跨工具复用的技能挪到 `.agents/skills/`（位置 5/6），项目规范交给 `AGENTS.md`，让 Cursor / Codex 也能消费。
3. **薄适配层**：工具间差异（`skill()` 语法、permission 键名、hook 名）用适配器抹平，核心资产只维护一份。

这样，你花在 Claude Code 上的定制沉淀不会锁死在单一工具里，换工具只是换适配层，而不是重写资产。

### 本章小结

- `AGENTS.md` 是 opencode 原生加载的项目上下文文件，`/init` 生成，对应 Claude Code 的 `CLAUDE.md`，且是跨工具标准文件名。
- SKILL.md 有六个发现位置，其中 `.claude/skills/` 被 opencode 兼容读取，存量技能零迁移即用。
- frontmatter 只认五个字段：`name`（必填，小写+连字符）、`description`（必填）、`license`、`compatibility`、`metadata`。
- 技能用 `skill({ name: "..." })` 调用，`permission.skill` 控制 allow/ask/deny；自定义 Agent 用 Markdown 文件或 `agent create`。
- hooks 仅支持 4 个共享 hook，Claude 专属 hooks 不生效；用 `.agents/skills/` + 适配器可实现跨工具复用。

> **下一章预告**：下一章进入收尾：把迁移过程中最容易踩的认证失败、模型不出现、配置误配整理成排错清单，作为你在 opencode 里"随用随查"的手册。

---

## 第 9 章：常见坑与故障排查

迁移到 opencode 的过程中，绝大多数「卡住」的时刻都不是功能不会用，而是认证、配置与两套工具概念错位导致的。本章把最容易踩的坑整理成排查清单，建议迁移期间随用随查。

### 认证失败：{env:VAR} 空串破坏 auth.json 回退

这是 opencode 社区最典型的认证坑（[Issue #34388](https://github.com/anomalyco/opencode/issues/34388)）。

**复现路径**：
1. 用 `opencode auth login` 存好 API key（写入 `~/.local/share/opencode/auth.json`）
2. 在 `opencode.json` 里把 provider 配成 `"apiKey": "{env:MY_API_KEY}"`
3. 启动时该环境变量未导出 → 报错 `Failed to initialize provider`，最终 401

**根因**：`{env:VAR}` 在变量未设置时被替换为**空字符串 `""`**，而 opencode 判断「是否需要回退到 auth.json」用的是严格相等 `=== undefined`。空串不是 `undefined`，于是回退逻辑被短路——auth.json 里明明存好的凭据被白白跳过。

**教训**：
- 自定义 provider 用 `{env:VAR}` 时，务必确认该变量在启动 opencode 的**同一 shell** 中已导出（可先 `echo $MY_API_KEY` 验证）
- 或者干脆不用 `{env:}`，直接依赖 `auth login` / `/connect` 写入 auth.json，**二选一，别双写**

> [!tip] 大白话
> 把 auth.json 想成一个保险箱，key 就锁在里面。`{env:VAR}` 是在告诉 opencode「钥匙在环境变量这个抽屉里」。如果抽屉是空的（变量未设置），opencode 打开空抽屉发现没钥匙，但因为空串也算「有位置可找」，它不会回头去开保险箱。所以：要么抽屉里真有钥匙，要么别指这个抽屉，直接让它开保险箱。

### 模型不出现的排查清单

配置了自定义 provider 后模型列表里看不到它，按顺序查：

- [ ] **models map 是否注册**：provider 配置里要显式列出模型（`"models": { "model-id": { "name": "..." } }`），只配 baseURL 不会自动拉取模型列表
- [ ] **API key 是否在同一 shell 导出**：尤其非交互 `run` 模式会继承启动时的环境，换个终端就丢
- [ ] **是否在项目目录内启动**：`opencode.json` 从当前目录向上找最近 Git 目录加载，在项目外启动读不到项目级 provider 配置
- [ ] **刷新模型缓存**：`opencode models --refresh` 排除旧缓存干扰

### 常见配置坑与版本回归

- **baseURL / npm 配错**：OpenAI 兼容 provider 的 `npm` 必须保持 `@ai-sdk/openai-compatible`，`baseURL` 必须指向官方 `.../v1` 端点。两者改错会导致 endpoint 不匹配，请求打到不存在的路由，表现类似 404 / 认证失败。
- **密钥含换行/空白**（[issue #25757](https://github.com/anomalyco/opencode/issues/25757)）：从管理后台复制 key 常带尾随换行，粘贴进 env 或配置后认证静默失败。用 `echo -n "$KEY" | wc -c` 对比长度，或 `tr -d '[:space:]'` 清理后再试。
- **`{env:}` 与 auth.json 双写冲突**：同时配置 `"apiKey": "{env:...}"` 和已登录的 auth.json，两个来源不一致时行为难预期。选一种方式作为唯一凭据来源。
- **版本回归破坏认证**：个别版本（如 1.1.49）引入过认证回归。升级后突然 401，先 `opencode --version` 确认版本，再 `opencode upgrade <旧版本>` 降级验证是否为版本问题，确认后等修复版再升。

> [!tip] 大白话
> `{env:}` 和 auth.json 同时存在，就像给门装了两把方向不一致的锁：你以为是「双保险」，实际是「双后门」——任一处出错整扇门都打不开。认证来源保持单一，比什么都稳。

### Anthropic OAuth 限定 Claude Code 提醒

Anthropic 已把部分 OAuth 凭据限定为 **Claude Code 专用**。把 Claude Code 里 `/login` 的账号登录态直接拿给 opencode 用，可能认证通过却拿不到模型权限，或直接被拒。

> [!tip] 大白话
> Claude Code 的登录态像公司的员工门禁卡，只在自家公司（Anthropic 官方工具）有效。opencode 是「外包访客」，得走自己的访客通道（API key）。别拿员工卡去刷外包公司的门。

**做法**：在 opencode 里用 Claude 模型时，优先走 `opencode auth login`（选 anthropic 填 API key）或 `/connect`，而不是复用 Claude Code 的 OAuth 登录态。

### 从 Claude Code 迁移的差异提醒

| 迁移点 | Claude Code | opencode | 典型坑 |
|--------|-------------|----------|--------|
| 项目上下文 | `CLAUDE.md` | `AGENTS.md` | 只搬了 CLAUDE.md 没改名，上下文文件不生效 |
| 默认权限 | 写文件/跑命令前询问 | 默认 allow，靠 git 快照 `/undo` 兜底 | 以为「默认询问」，实际全自动执行 |
| 非交互批准 | `-p --dangerously-skip-permissions` | `run --auto`（仅 CI） | 在本地交互环境滥用 `--auto` |
| 配置方式 | `settings.json` + `claude mcp add` | 声明式 `opencode.json` 8 层合并 | 习惯用命令改配置，找不到对应键 |
| 模型指定 | `-m model` | `-m provider/model` | 漏写 provider 前缀 |
| 权限规则 | 数组式、deny 优先 | glob + last matching wins | 沿用 Claude Code 的规则顺序，被后面的规则意外覆盖 |

迁移初期最常见的「事故」不是功能 bug，而是**权限基线差异**：opencode 默认比 Claude Code 宽松得多——`.env` 系文件默认 deny，但其余大多数动作默认放行。强烈建议迁移首周先把权限收紧（`"permission": { "*": "ask", ... }`，详见第五章），确认行为符合预期再逐步放开。

### 本章小结

- 认证失败先查 `{env:VAR}`：未设置会变空串，短路 auth.json 回退（issue #34388）；凭据来源保持单一
- 模型不出现按四条清单排查：models map 注册、同一 shell 导出 key、项目目录内启动、刷新缓存
- 密钥清理换行空白、baseURL/npm 保持官方端点、版本回归用降级验证
- opencode 用 Claude 走 API key，不依赖 Claude Code 专属 OAuth
- 迁移最危险的是权限基线差异：默认比 Claude Code 宽松，先收紧再放开

> **结语**：至此，从定位、安装、配置、命令、权限、provider、MCP 到 Skills 与排错，你已拥有从 Claude Code 完整迁移到 opencode 的地图。剩下的就是动手实践——把这份指南放在手边，迁移路上随用随查。

---

## 附录：参考来源

以下链接为各章引用的官方文档、技术博客与社区 Issue（已去重），按主题分组：

### 官方文档与仓库

- opencode 官网（安装脚本、产品定位）：https://opencode.ai
- opencode GitHub 仓库（README、Issue、Anthropic OAuth 限制说明）：https://github.com/anomalyco/opencode
- opencode 官方文档（架构、客户端/服务器、三种界面）：https://opencode.ai/docs/
- opencode CLI 参考（认证、run、models 等子命令）：https://opencode.ai/docs/cli
- opencode TUI 文档（slash 命令、快捷键）：https://opencode.ai/docs/tui
- opencode 配置文档（config 键、provider 排错）：https://opencode.ai/docs/config
- opencode MCP 文档（mcp 配置键、OAuth 模式）：https://opencode.ai/docs/mcp
- opencode Skills 文档（AGENTS.md、SKILL.md 发现位置与 frontmatter）：https://opencode.ai/docs/skills
- opencode Agents 文档（自定义 Agent）：https://opencode.ai/docs/agents

### 技术博客与实测

- DeepInfra《Claude Code 替代定位分析》：https://deepinfra.com/blog/claude-code-alternative
- Builder.io《opencode vs Claude Code 实测对比》：https://www.builder.io/blog/opencode-vs-claude-code
- Venice AI opencode 集成文档：https://docs.venice.ai/guides/integrations/opencode

### 社区资源与 Issue

- opencode-primer（社区 CLI 速查表）：https://github.com/wesammustafa/opencode-primer
- spine（跨工具复用适配器）：https://github.com/kenoxa/spine
- Issue #34388（`{env:VAR}` 空串破坏 auth.json 回退）：https://github.com/anomalyco/opencode/issues/34388
- Issue #25757（密钥含换行/空白导致认证失败）：https://github.com/anomalyco/opencode/issues/25757
