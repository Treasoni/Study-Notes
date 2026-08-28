---
title: "Hermes Agent（Nous Research）上手实战"
tags:
  - AI学习
  - Agent
  - Hermes
  - 上手实战
created: 2026-08-28
updated: 2026-08-28
status: 已完成
source_project: hermes-agent
---

# Hermes Agent（Nous Research）上手实战

这份笔记围绕 Nous Research 出品的开源 AI agent——Hermes Agent 整理而成。与"装好即定型"的传统 agent 不同，Hermes 的核心卖点是内置学习回路：越用越懂你、越用越能干活。全篇按 定位 → 安装 → 模型配置 → 记忆闭环 → 技能体系 → 多平台自动化 → 委派并行 → 部署进阶 → 常见坑 → 身份定制与多 Agent → 命令速查 的顺序展开，十章正文加一个附录，帮助你从零跑通 Hermes，并理解它"用着用着自己变强"的机制。

## 目录

1. [定位与核心理念：一个会自我改进的 agent](#定位与核心理念一个会自我改进的-agent)
2. [安装与第一跑：从命令到首次对话](#安装与第一跑从命令到首次对话)
3. [模型 Provider 配置：打破模型锁定](#模型-provider-配置打破模型锁定)
4. [记忆与学习闭环：跨会话成长](#记忆与学习闭环跨会话成长)
5. [技能体系：把经验沉淀为可复用资产](#技能体系把经验沉淀为可复用资产)
6. [多平台接入与定时任务：从"你找它"到"它找你"](#多平台接入与定时任务从你找它到它找你)
7. [委派与并行：子代理与 execute_code](#委派与并行子代理与-executecode)
8. [部署进阶：Docker、多后端与安全基线](#部署进阶docker多后端与安全基线)
9. [常见坑与最佳实践](#常见坑与最佳实践)
10. [身份定制与多 Agent：SOUL.md、Profiles 与 Bot Mode](#身份定制与多-agentsoulmdprofiles-与-bot-mode)
11. [附录：Hermes Agent 常用命令速查](#附录hermes-agent-常用命令速查)

## 定位与核心理念：一个会自我改进的 agent

Claude Code、Cursor、[[OpenClaw核心概念|OpenClaw]] 把"会调用工具"变成了标配，但能力边界大多是静态的：装什么插件、配什么 MCP，就停在那层。Hermes Agent 想回答另一个问题——agent 能不能像人一样，用着用着自己变强？本章讲清它是什么、与主流 agent 的差异，以及"学习回路"意味着什么。

### 是什么：Nous Research 出品的"成长型" agent

Hermes Agent 是 Nous Research 出品的开源 AI agent，标语 "The agent that grows with you"（与你一同成长的 agent）。它不绑本地：官方定位可跑在 $5 低配 VPS、GPU 集群甚至 serverless，云端虚拟机里经 Telegram 对话即用（来源 S1）。

### 差异：核心不是"更多工具"，而是"内置学习回路"

你熟悉的 agent 工具，卖点通常是更长上下文、更丰富工具生态、更好 IDE 集成。Hermes 的差异化在于把"自我改进"做成内置机制：任务后自动沉淀经验、调整技能，下次再用上。联创 Karan 称之为"自我改进系统"，而非向 prompt 灌输任意策略（来源 S16）。

> [!tip] 大白话
> 把 Claude Code 想成出厂配好工具的瑞士军刀；把 Hermes 想成一个会记工作笔记的新员工，做完活自己总结改进。卖点不是"刀多"，而是"会涨经验"。

### 学习闭环五要素：成长的循环怎么转

官方称这条路径为"封闭学习回路"，五个环节：从经验创建技能 → 使用中自改进 → 自我提示持久化知识 → 搜索历史对话 → 跨会话构建用户模型（来源 S1）。实现清单：agent 策展记忆 + 周期 nudge；复杂任务后自动建技能；技能自改进；SQLite FTS5 检索历史会话 + LLM 摘要做跨会话回忆；Honcho 用户建模；技能兼容 agentskills.io 开放标准（来源 S1）。第四、五章逐一展开。

> [!tip] 大白话
> 想成健身房训练计划：练完（任务）→ 记录动作（写记忆/建技能）→ 下回照着改（技能自改进）→ 翻旧笔记（FTS5）→ 教练懂你（Honcho）。单看不稀奇，串成自动循环才是差异化。

### 自改进的实质：改的是技能层，不是模型权重

泼盆冷水：这里的"成长"不改变模型权重。源码阅读确认，成长发生在技能与框架层——可复用知识文档与调度框架——而非模型本身；v0.16 起方向从"技能增长"转向"筛选与折叠"，以控制上下文开销（来源 S15）。

> [!tip] 大白话
> 别以为它会像训练大模型那样变聪明。想成一个人换了套更好用的笔记方法——大脑没变，方法论升级了。

### 营销口径与版本提示

"唯一带内置学习回路的 agent"是官方营销表述；官方访谈也承认竞品为 OpenClaw（技能可迁移）、Claude Code 和 Codex（来源 S1、S16）。判断强弱要看机制而非口号；本笔记涉及后端数量、Vercel Sandbox 的内容均以 v0.20.x 文档为准。

### 本章小结

- Hermes 是 Nous Research 出品的开源 agent，主打"与你一同成长"，可跑 $5 VPS 到 serverless。
- 与 Claude Code / OpenClaw 的核心差异是"内置学习回路"。
- 学习闭环五要素：建技能、自改进、持久化知识、历史检索、用户建模。
- 自改进在技能/框架层而非模型权重；v0.16 起强调"筛选与折叠"。
- "唯一带学习回路"是营销表述，竞品为 OpenClaw / Claude Code / Codex。

下一章进入实战：用一行命令装好 Hermes、跑通第一次对话，并选择 Windows 原生与 WSL2 路线。

## 安装与第一跑：从命令到首次对话

第一章认识了 Hermes Agent"带学习回路"的定位。这一章动手：装好、跑通第一次对话，并解决 Windows 用户在原生与 WSL2 之间的选择。

### 2.1 平台安装

Linux / macOS / WSL2 / Termux 用一行脚本 [^c2-1][^c2-2]：

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Windows 原生用 PowerShell [^c2-2]：

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

macOS / Windows 也可用官方 Desktop 安装器；纯 CLI 用户之后随时 `hermes desktop` 补装图形界面。

> [!tip] 大白话：装 Hermes 像"全包装修队"——你只管下订单，uv、Python、Node、ripgrep、ffmpeg 它自己搬，不用一件件采购。

### 2.2 安装器做了什么

自动装 uv、Python 3.11、Node.js 22、ripgrep、ffmpeg，Windows 另有便携 MinGit，无需手动装 Python / Node。唯一硬前置是 Git（非 Windows）；Linux 另需 curl + xz-utils，桌面应用需 g++/build-essential。Nix 不再显式支持 [^c2-2]。

### 2.3 目录布局

- 代码 `~/.hermes/hermes-agent/`；可执行文件 `~/.local/bin/hermes`（root 模式 `/usr/local/lib/hermes-agent/`）
- 数据与配置 `~/.hermes/`；Windows 原生 `%LOCALAPPDATA%\hermes`

> [!tip] 大白话：`~/.hermes/` 是"固定收纳位"——配置、密钥、记忆、技能一个抽屉放齐，备份排查都看它。

### 2.4 第一跑：`hermes setup --portal`

```bash
source ~/.bashrc
hermes setup --portal
```

`source` 让 hermes 进 PATH；`setup --portal` 一次完成 OAuth 登录 + Nous Provider + 开启 Tool Gateway，最快打通，之后 `hermes` 直接开聊 [^c2-2]。

> [!tip] 大白话：`setup --portal` 像"办一张通票"——登录、模型、工具通道一次认证齐活。

### 2.5 Windows 原生 vs WSL2

官方口径有矛盾 [^c2-1][^c2-2]：README 称原生"无需 WSL"；providers 文档称需 Unix 环境、应在 WSL2 内运行；安装文档把原生标为 early beta（以 v0.20.x 文档为准）。**推荐**：原生可跑，但模型服务与稳定性以 WSL2 为准，求稳选 WSL2。

预提示：Defender / Bitdefender / 腾讯管家常把 uv.exe（Astral 未签名 Rust 二进制）误报为病毒 [^c2-3][^c2-4]；白名单加**整个文件夹**而非文件哈希（uv 每版本哈希都变），必要时 `gh attestation verify` 校验。

### 2.6 常用命令速查

```bash
hermes doctor          # 诊断环境，排错第一步
hermes model           # 完整模型向导
hermes setup           # 重走设置向导
hermes tools           # 查看工具配置
hermes gateway setup   # 多平台网关配置
hermes config set|get  # 读写 config.yaml
```

### 本章小结

- 一条命令装完，自动带齐 uv / Python / Node / ripgrep / ffmpeg，唯一硬前置是 Git。
- 记住根目录 `~/.hermes/`（Windows 原生 `%LOCALAPPDATA%\hermes`）。
- `source ~/.bashrc` + `hermes setup --portal` 最快打通首次对话。
- Windows 原生标 early beta，求稳用 WSL2；uv.exe 被误报时白名单加文件夹。
- 排错先 `hermes doctor`。

下一章进入模型 Provider 配置：config.yaml 与 .env 的分工，以及用 Nous Portal / OpenRouter / Ollama 打破模型锁定。

---

[^c2-1]: GitHub README（S1）：https://github.com/NousResearch/hermes-agent
[^c2-2]: 官方安装文档（S2）：`/docs/getting-started/installation`
[^c2-3]: Windows 相关 Issue #16201（S14）
[^c2-4]: CSDN Windows 实操（S18）：uv.exe 误报与白名单

## 模型 Provider 配置：打破模型锁定

用 agent 的人最烦被一家模型绑死：换供应商就得重配一遍。Hermes 把模型层做成了可插拔的——配置只认两个文件，Provider 全家桶覆盖云端、本地与自建端点，任何 OpenAI-compatible 服务都能接入。本章讲清配置唯一来源、六类 Provider 的接法，以及 WSL2 下连 Windows 宿主模型服务的网络细节。

### 配置唯一来源：config.yaml + .env，密钥永不混进配置

Hermes 的模型配置只有一个权威位置：`~/.hermes/config.yaml`。三个文件分工明确：`config.yaml` 只写"模型在哪、怎么连"（模型名、provider、base_url）；API key 一律放 `~/.hermes/.env`，密钥不会暴露给模型；OAuth 登录凭据由程序自动写入 `~/.hermes/auth.json`，通常无需手工编辑。旧的环境变量 `LLM_MODEL` 已被移除，不要再依赖它（来源 S5）。

```yaml
# ~/.hermes/config.yaml（最小示意，键名以 hermes doctor 输出为准）
model: my-default-model   # 默认模型名
provider: nous-portal     # 走哪个 provider
base_url: ""              # custom / 直连端点时填
```

```bash
# ~/.hermes/.env（密钥清单，与 config 分离）
OPENROUTER_API_KEY=sk-or-xxxx
OPENAI_API_KEY=sk-xxxx
ANTHROPIC_API_KEY=sk-ant-xxxx
```

> [!tip] 大白话
> 把 config.yaml 想成「装修图纸」（模型在哪、怎么连），把 .env 想成「保险箱」（只放钥匙）。钥匙从不混进图纸，换机器、同步、备份都只操心这两个文件。

这套"配置与密钥分离"的设计，是后面容器化、远程后端部署安全基线的前提。配置排错从 `hermes doctor` 开始，它会诊断配置与密钥是否齐全（来源 S5）。

### Provider 全家桶：一条命令接六种模型来源

至少要配一个 LLM provider 才能跑。官方推荐首选项是 Nous Portal：一次 OAuth 登录覆盖 300+ 模型，还捆绑了 Tool Gateway，一条龙最省事。其余选择（来源 S5）：

| Provider | 配置要点 |
|---|---|
| Nous Portal | OAuth 登录，推荐；覆盖 300+ 模型 + Tool Gateway |
| OpenRouter | `.env` 放 `OPENROUTER_API_KEY` |
| OpenAI 直连 | `.env` 放 `OPENAI_API_KEY`，provider 用 `openai-api` |
| Anthropic | 三种认证：Claude Max OAuth / `ANTHROPIC_API_KEY` / `ANTHROPIC_TOKEN`；**Claude Pro 订阅不能走 OAuth** |
| custom | 任意 OpenAI-compatible 端点，配 `base_url` |
| 本地 Ollama | `base_url: http://localhost:11434/v1`，且 `context_length ≥ 64000` |

选型没有对错，只有场景：追求省事选 Nous Portal；已有 OpenAI / OpenRouter 额度直接填 key；隐私敏感或离线场景用本地 Ollama；公司自建网关只要是 OpenAI-compatible 就能当 custom 接进来。注意 Anthropic 的认证分三种，Claude Max 订阅可走 OAuth，Claude Pro 不行，得用 `ANTHROPIC_API_KEY` 或 `ANTHROPIC_TOKEN`。

> [!tip] 大白话
> 把 provider 想成「加油站」：同一套 OpenAI-compatible 格式就像同一种油，可以加中石油、加壳牌、加自家发电机（Ollama）。Hermes 不绑死一家——换油只改配置文件，不换车。

### 会话外向导 vs 会话内切换

两个入口要分清（来源 S5）：会话外运行 `hermes model`，是完整向导，可增删 provider、改默认模型；会话内输入 `/model`，只在"已配置项"之间快速切换，不能新增。换句话说，`hermes model` 是"配管工"（新增、删除、设默认），`/model` 是"换开关"（已装好的水龙头之间切换）。新 provider 配好后，会话内就能立刻用 `/model` 切过去。

### WSL2 访问 Windows 宿主模型服务

在 WSL2 里跑 Hermes、想连 Windows 上运行的 Ollama 等服务时（来源 S5）：

- Win11 22H2+ 推荐开 **mirrored 模式**，网络共享，直接 `localhost` 即可，无需改配置；
- NAT 模式要用**主机 IP**（不是 localhost），且服务必须绑定 `0.0.0.0` 才能被 WSL2 访问，例如启动 Ollama 时设 `OLLAMA_HOST=0.0.0.0:11434`。

```yaml
# ~/.hermes/config.yaml（WSL2 → Windows 宿主 Ollama，NAT 模式）
provider: custom
base_url: http://<主机IP>:11434/v1
context_length: 64000
```

注意两处 `base_url` 不同：纯 Linux 本机是 `localhost:11434`；WSL2 连 Windows 宿主时要用主机 IP。mirrored 模式省心但要求 Win11 22H2+；NAT 模式通用性更强，代价是多配一步。

> [!tip] 大白话
> 把 WSL2 想成「隔壁房间」：mirrored 模式像打通隔断墙，说 localhost 就能串门；NAT 模式像还得报出整栋楼门牌号（主机 IP），并让服务把门开在 0.0.0.0 才对整栋楼可见。

### 本章小结

- 配置唯一来源是 `~/.hermes/config.yaml` + `~/.hermes/.env`，密钥永不进配置文件；`LLM_MODEL` 已移除。
- Nous Portal OAuth 一条龙最省事；OpenRouter / OpenAI / Anthropic / custom / Ollama 各有接法，Claude Pro 不能走 OAuth。
- 会话外 `hermes model` 管增删与默认，会话内 `/model` 管快速切换。
- WSL2 连 Windows 模型服务：mirrored 模式直连 localhost；NAT 模式用主机 IP + 服务绑 0.0.0.0（如 `OLLAMA_HOST`）。

下一章进入 Hermes 最核心的差异化——记忆与学习闭环，看它如何跨会话"用着用着自己变强"。

## 记忆与学习闭环：跨会话成长

真正让 Hermes Agent 区别于"每次都要重新认识你"的普通 agent 的，是它的记忆与学习闭环：一次对话结束后，经验被沉淀进记忆文件、技能被自动改进，下一次会话一睁眼就能接着用。本章拆解这条闭环的四个环节——内置记忆两文件、`memory` 工具、跨会话检索 `session_search`、外置记忆 Honcho——以及驱动这一切的后台自我改进审查。[^c4-1][^c4-2][^c4-3]

### 4.1 内置记忆两文件：MEMORY.md 与 USER.md

Hermes 的内置记忆是文件式的，存在 `~/.hermes/memories/`，只有两个文件：

- `MEMORY.md`：agent 自己的笔记，约 2200 字符（约 800 tokens），记"我学到的事、我做过的事"。
- `USER.md`：用户画像，约 1375 字符（约 500 tokens），记"这位用户的偏好与需求"。[^c4-1]

> [!tip] 大白话
> 把 MEMORY.md 想成 agent 的**工作日志**，USER.md 想成它给你建的**用户档案**——一个记"我学到/我做过啥"，一个记"这位用户是谁、偏好啥"。所以每次新会话，agent 一睁眼就先读这两本，就知道自己是谁、在跟谁说话。

容量上，memory 建议保持 8-15 条、user 保持 5-10 条；单文件容量超过 80% 时，官方建议先合并再继续写。精确重复的条目会被自动拒绝，避免记忆膨胀。[^c4-1]

### 4.2 memory 工具：只写不读的便签

`memory` 工具只有三个动作：`add` / `replace` / `remove`，**没有 read**——因为记忆已在会话启动时自动注入 system prompt，agent 不需要（也不能）主动去查。`replace` 和 `remove` 用 `old_text` 做**唯一子串匹配**定位旧条目：

```json
// 示意：memory 工具调用（精确字段以 v0.20.x 文档为准）
{ "action": "add",     "kind": "memory", "text": "用户偏好 TypeScript，禁止 any" }
{ "action": "replace", "old_text": "用户偏好 TypeScript",
  "text": "用户偏好 TypeScript 且用 pnpm" }
{ "action": "remove",  "old_text": "已过时条目的唯一子串" }
```

记忆**不会自动压缩**：写入超限会返回错误，agent 必须在**同一回合**先合并/删除再重试。所有条目都要经过注入/渗出威胁扫描，含不可见 Unicode 的条目直接阻断。[^c4-1]

### 4.3 冻结快照与前缀缓存

会话启动时，两个文件会被"冻结"成快照注入 system prompt，整个会话内不再变化——这是为了保住前缀缓存（prompt 前缀不变即可复用缓存，省 token）。写入会立即落盘，但要到下一个会话才会被重新快照、才可见。[^c4-1]

> [!tip] 大白话
> 把冻结快照想成开会前拍的**合影**——会议期间谁换了发型都不影响这张照片。因为会话内记忆永不变化，模型才能复用同一段前缀缓存，省下每轮重复计算的 token；你写的记忆当天落盘，但要到下次开会（新会话）才重新拍照。

### 4.4 跨会话检索：session_search + SQLite FTS5

记忆文件只存"结论"，想翻历史对话原文靠 `session_search`：它在 SQLite `~/.hermes/state.db` 上做 FTS5 全文检索，返回的是**真实消息**，无摘要、无截断。成本对比很悬殊：内置记忆每提示约 1300 tokens 固定开销，而一次 session_search 约 20ms 且免费——所以"该翻历史就翻历史"，别把细节都塞进记忆。[^c4-1]

> [!tip] 大白话
> 把 session_search 想成给整个聊天记录装的**全文搜索引擎**——它搜的是聊天记录原件（真实消息），不是二手摘要，所以搜到的内容能直接引用、不会失真。

### 4.5 外置记忆与 Honcho：从"记住"到"理解"

内置记忆之外，Hermes 支持外置 memory provider。注意一个数字矛盾：memory-providers 页面自称提供 **8 个**，实际对比表列了 **9 个**（Honcho/OpenViking/Mem0/Hindsight/Holographic/RetainDB/ByteRover/Supermemory/Memori），以 v0.20.x 文档为准。无论选哪个，**同一时刻只激活一个外置 provider，而内置记忆始终并行**。[^c4-2]

其中最值得单独说的是 Honcho（plastic-labs 的 AI-native 记忆后端）：它采用 **dialectic（辩证）建模**，在每次对话后推理"用户是谁"，存的是**"结论而非对话"**——对用户画像做增量提炼，而不是流水账。[^c4-3]

> [!tip] 大白话
> 把 Honcho 想成一位**观察员**而不是速记员——它不逐字记录你们聊了什么，而是在对话后琢磨"这个人到底想要什么"，沉淀成结论。下回直接按结论办事，比翻聊天记录高效得多。

它有三个正交旋钮，控制"多快推理、多深推理、上下文怎么注入"：

```yaml
# ~/.hermes/config.yaml 片段（取值语义以 v0.20.x 文档为准）
memory:
  provider: honcho
  honcho:
    contextCadence: 5        # 多少轮注入一次 base 层用户上下文
    dialecticCadence: 20     # 多少轮跑一次 dialectic 推理
    dialecticDepth: 3        # 单次推理沉淀的用户结论深度
```

`hybrid` / `context` / `tools` 三种召回模式，分别控制检索时用哪种信号（混合 / 纯上下文 / 纯工具行为）。[^c4-3]

### 4.6 后台自我改进审查与 /journey

闭环的最后一环在"对话之外"：**每轮之后**都有一次后台自我改进审查，agent 可能自动写记忆、改进技能。这触碰了"自我修改"的敏感红线，所以有 `write_approval` 把门：要么**前台内联确认**，要么 **staged 到 `/memory pending`** 供你批阅后再落地。[^c4-1]

想看成长轨迹用 `/journey`：它是一个时间线视图，删除某条 memory 块即从时间线移除；被归档的技能也可以从这里恢复——成长的每一步都可追溯、可回滚。[^c4-1]

### 本章小结

- 内置记忆就两个文件：`MEMORY.md`（agent 笔记，约 800 tokens）+ `USER.md`（用户画像，约 500 tokens），容量超 80% 先合并。
- `memory` 工具只写不读（add/replace/remove），`replace/remove` 用 `old_text` 唯一子串匹配，超限须同回合合并重试。
- 冻结快照保前缀缓存：会话内不变、立即落盘、下会话才可见。
- 翻历史用 `session_search`（SQLite FTS5，约 20ms、免费），别用固定约 1300 tokens 开销的记忆存细节。
- 外置 provider 号称 8 个实列 9 个，同一时刻只激活一个、内置始终并行；Honcho 用"结论而非对话"的 dialectic 建模。
- 后台自我改进审查由 `write_approval` 把关，`/journey` 可回溯每一次成长。

下一章进入技能体系：看经验如何被沉淀为按需加载的 SKILL.md 资产，以及 agent 如何用 `/learn` 与 `skill_manage` 让技能自我进化。

---

[^c4-1]: Hermes Agent 内置记忆文档，`https://hermes-agent.nousresearch.com/docs/user-guide/features/memory`
[^c4-2]: Hermes Agent Memory Providers 文档，`https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers`
[^c4-3]: Hermes Agent Honcho 文档，`https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho`

## 技能体系：把经验沉淀为可复用资产

上一章的记忆让 agent 记住"你是谁、聊过什么"，本章的技能则让 agent 记住"这件事该怎么做"。技能是 Hermes 学习闭环的核心载体：它把一次性的操作经验，变成下次自动加载、直接照做的可复用资产。

### 5.1 技能是什么：按需加载的"知识文档"

[[Skills 是什么|技能]]（skill）不是代码插件，而是一份 Markdown 知识文档（SKILL.md），告诉 agent 在什么场景下、按什么步骤做什么。它只在相关时被加载，这叫**渐进式披露**——用多少 token 加载多少，而不是把全部说明常驻在上下文里烧钱。技能格式兼容 agentskills.io 开放标准，社区生态的技能可直接拿来用。

> [!tip] 大白话
> 把技能想成"菜谱"：不做菜时它静静躺在抽屉里（不占 token），要做菜才翻出来照着做（按需加载）。所以"渐进式披露"= 平时不占地方、用时才摊开，省下的就是每次对话的 token 成本。

### 5.2 三级加载：L0 → L1 → L2

Hermes 用三级加载把"有哪些技能"到"精读技能细节"拆成三档成本：

| 级别 | 调用 | 作用 |
|---|---|---|
| L0 | `skills_list()` | 约 3k tokens，只列出技能名与一句话描述 |
| L1 | `skill_view(name)` | 读单个技能的主体 SKILL.md |
| L2 | `skill_view(name, path)` | 按路径读该技能的某个参考文件 |

已安装技能会自动注册成斜杠命令，会话里直接 `/技能名` 调用；单条消息最多叠加 5 个技能，避免上下文被撑爆。设计意图很直白：列表足够便宜所以每次可用；SKILL.md 只在你可能用到时才展开；references 留给真正需要细节的场景。

> [!tip] 大白话
> 三级加载像图书馆查资料：先在检索屏看书名列表（L0，最省），看中一本取下来翻目录和简介（L1），还不够再翻到指定章节细读（L2）。不会查个书名就把整本百科全书复印一遍。

### 5.3 用 /learn 沉淀经验

对话中直接输入即可生成技能：

```
/learn ./notes/my-stack        # 从本地目录生成
/learn https://example.com/guide  # 从 URL 生成
/learn 从刚才的流程            # 从当前会话流程生成
```

大资料建议做成**知识库技能**：一个瘦 SKILL.md 只写索引与用法，正文按章拆进 `references/` 目录，配合 L2 按路径精读，避免一次性加载整本手册。

> [!tip] 大白话
> 瘦 SKILL.md 像论文的"摘要 + 目录"，references/ 才是正文。先读摘要决定要不要看，再看哪一章——避免把整本书倒进脑子里。

### 5.4 SKILL.md 规范：frontmatter + 正文五段

```yaml
# SKILL.md（以 v0.20.x 文档为准）
---
name: my-deploy
description: 用 Docker 部署 Hermes 并保持配置持久化
version: 1.0.0
author: me
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes: {}   # metadata.hermes.* 命名空间，按需扩展
---
```

正文固定五段，顺序即 agent 的执行路径：

1. **When to Use** 何时该用这个技能
2. **Quick Reference** 快速参考（关键命令/参数）
3. **Procedure** 操作步骤
4. **Pitfalls** 易错点（把踩过的坑写进来）
5. **Verification** 怎么验证做成功了

### 5.5 skill_manage：agent 自建自改技能

`skill_manage` 工具让 agent 自己建/改/删技能——这就是第四章"自改进循环"里的程序记忆部分：任务做完，agent 把经验沉淀成技能，下一次同类任务直接复用。开启 `skills.write_approval` 后，每次写技能都需你前台确认或进入待批区，形成人工审批门，防止 agent 悄悄改掉你信任的行为。这也印证了前面说的"成长发生在技能层而非模型权重"：改进的是它积累的资产，不是模型本身。

> [!tip] 大白话
> `skills.write_approval` 像"改别人代码要先过 code review"：agent 有权限自己写技能，但写之前要你点同意，避免它自作主张改掉核心流程。

### 5.6 Skills Hub 多源安装与安全扫描

```bash
# 从 Skills Hub 安装（具体子命令以 v0.20.x 文档为准）
hermes skills install <skill-name>        # 默认全量安全扫描后加载
hermes skills install <skill-name> --force  # ⚠️ dangerous 判定下 --force 也无法绕过
```

Skills Hub 聚合多源：official / skills.sh / well-known / GitHub / clawhub / lobehub / browse-sh / url。每次安装做全量安全扫描；一旦判定 `dangerous`，即使加 `--force` 也拒绝安装——这道安全闸是硬底线。

> [!tip] 大白话
> Skills Hub 像"应用商店"：下载前先过一遍杀毒。被标 `dangerous` 的应用就算你强按"仍然安装"也装不上，因为开发者把这道闸做成硬保险，不可关闭。

### 5.7 条件激活与项目级信任

- `fallback_for_toolsets`：声明某高级工具缺失时，自动激活免费替代技能顶替。
- `required_environment_variables`：声明技能所需密钥，值存 `~/.hermes/.env` 不暴露给模型，自动透传 terminal / execute_code 沙箱。
- 项目级技能：需先 `hermes skills trust` 授权才加载，加载优先级 project → local → external_dirs。

### 本章小结

- 技能是按需加载的 Markdown 知识文档，"渐进式披露"省 token，兼容 agentskills.io
- 三级加载 L0 列表 → L1 概览 → L2 精读；已装技能自动成为斜杠命令，单消息最多叠加 5 个
- `/learn` 一键从目录/URL/会话生成技能；大资料用瘦 SKILL.md + references/ 逐章拆分
- SKILL.md = frontmatter（name/description/version/author/license/platforms/metadata.hermes.*）+ 五段正文
- `skill_manage` + `skills.write_approval` 构成带审批的自改进；Skills Hub 多源安装且 `dangerous` 不可 `--force` 绕过

技能让 agent"越用越顺手"，但要它在你不盯着时也主动干活，还得把技能挂到多平台网关上。下一章进入第六章：多平台接入与定时任务——从"你找它"变成"它找你"。

[^c5-1]: S8：官方 skills 文档 `/docs/user-guide/features/skills`
[^c5-2]: S13：官方技能开发规范 `/docs/developer-guide/creating-skills`

## 多平台接入与定时任务：从"你找它"到"它找你"

前五章里，都是你主动打开终端去找 Hermes 聊天。本章把交互模式反过来：接入 Gateway 网关后，agent 常驻在 Telegram、Discord 等平台上"等你来找它"；配上 cron 定时任务后，它甚至到点主动干活、把结果推给你——从"你找它"变成"它找你"。两件事都能在对话里用自然语言配置，是 Hermes 相比 Claude Code / OpenClaw 顺手的地方（来源 S6、S7）。

### 6.1 Gateway 多平台接入

#### 接入：一个进程连 20+ 平台

跑 `hermes gateway setup` 交互式配置，向导引导你选定平台并生成凭证。配置完成后，一个 gateway 进程同时连接 20+ 平台：Telegram、Discord、Slack、WhatsApp、Signal、Email 等（来源 S6）。配好之后你就不用再守着终端——agent 常驻在云端或本地，掏出手机在任何接入平台发消息就能对话。bot 要真正干活需要两样东西：**model provider**（模型入口）+ **tool provider**（工具网关）。如果用 Nous Portal，OAuth 一次捆绑两者，省去分开配置（来源 S6）。

> [!tip] 大白话
> 把 gateway 想成总机接线员：一根电话线接 20 多个分机（平台），你在任意一个平台发消息，总机都转到同一个 agent。绑定 Nous Portal 等于一次性办好了"话费套餐"——模型和工具一起开通，不用跑两趟。

#### 授权：默认拒绝 + DM 配对

Gateway 是默认 deny 白名单：任何平台上的陌生消息一概不理，只有你主动授权过的账号能对话。授权方式是先在 CLI 会话里跑配对命令，把平台发来的配对码审批通过：

```bash
hermes gateway setup                    # 交互式配置平台接入
hermes pairing approve telegram <code>  # 审批 Telegram 配对请求
```

> [!tip] 大白话
> 把配对想成小区门禁：默认访客全拦下，只有你到物业（CLI）确认过的车牌才放行。所以你在 Telegram 上给 bot 发消息不会立刻有反应——得先在终端里批准它。

#### 常驻与自愈边界

Gateway 设计为常驻服务，官方建议用 systemd（Linux）或 launchd（macOS）托管；日志在 `~/.hermes/logs/gateway.log`。无头 VM 上以 user service 方式跑，并执行 `loginctl enable-linger`，让用户会话在无人登录时也保持运行（来源 S6）：

```ini
# systemd user service 骨架（示意；实际 Unit 名与 ExecStart 以 `hermes gateway install` 生成为准）
[Unit]
Description=Hermes Gateway
After=network-online.target

[Service]
Restart=on-failure

[Install]
WantedBy=default.target
```

macOS 端还有个小坑：装完新工具后要重跑 `hermes gateway install` 固化 PATH，否则重启后的 gateway 可能找不到新装的命令（来源 S6）。

一个必须记住的坑：每个平台适配器都有**熔断器**，连续失败会熔断该平台；熔断后**不会自动恢复**，必须手动在会话里执行 `/platform resume` 重新接通（来源 S6）。所以 gateway 挂了一晚上没响应，先查 `gateway.log` 再看是否熔断。

> [!tip] 大白话
> 熔断器想成烧断的保险丝：短路时它主动断开保护设备，但保险丝不会自己长回去。平台反复报错被熔断后，你得手动换一根（`/platform resume`），别干等。

### 6.2 cron 定时任务

#### 自然语言定义调度

cron 能力通过统一的 `cronjob` 工具暴露，在对话里用自然语言建/停/改/删，不用碰 crontab 语法（来源 S7）。调度支持四种格式：

| 格式 | 示例 | 含义 |
|------|------|------|
| 相对延迟 | `30m` / `2h` | 从现在起 30 分钟 / 2 小时后跑一次 |
| 间隔 | `every 2h` | 每 2 小时循环一次 |
| cron 表达式 | `0 9 * * *` | 标准 crontab 写法，如每天 9 点 |
| ISO 时间戳 | `2026-09-01T08:00:00` | 指定某一时刻 |

#### 结果自动投递

任务结果自动投递到绑定的 20+ 平台（origin / local / telegram / slack / whatsapp / email / dingtalk / feishu / wecom 等），**agent 不自己发消息**（来源 S7）。`context_from` 把上一任务输出作为下一任务的输入，链成流水线；`continuity=true` 时注入自己上次的输出，防止对同一事件重复报告（来源 S7）。

> [!tip] 大白话
> 想成设好闹钟的自动取件机器人：到点出门、取完快递、把东西放回你常看的门口（平台），全程不用你守着。`context_from` 是"把上次取到的单子带给下一次"，`continuity=true` 是"上回说过的事这回复述一遍"。

#### 模型解析与 fails closed

每次运行前要决定"让哪个模型干活"，解析顺序：任务 pin → `cron.model` → 全局默认。关键安全语义：未 pin 的任务在创建时**快照**全局默认模型，之后你改了默认模型，会让任务 fails closed——跳过运行、零推理消耗，而不是悄悄用新模型跑（来源 S7），从根上避免配置漂移引发的意外行为。任务派发前还会做配置校验：校验失败的任务被标记为 `blocked_config`，只发一条告警、零 LLM 调用，不会反复空跑烧 token（来源 S7）。

> [!tip] 大白话
> 想成保险单：创建任务时按当时价格"锁定"了模型，之后你改价（换默认模型）不会自动生效，任务宁可停跑也不偷偷换。省下的 token 是真金白银，行为可预期更重要。

#### no_agent 脚本模式与 wakeAgent 门

很多定时任务根本不需要 LLM。`no_agent` 模式按计划直接跑脚本，**零 LLM 调用**：脚本 stdout 原文投递到平台，空输出 = 静默 tick（不打扰），非零退出才告警（来源 S7）。更省的是 `wakeAgent` 预检门：先跑一段轻量检查，若脚本输出如下 JSON，则跳过本轮 LLM，适合高频轮询的零成本门控：

```json
{"wakeAgent":false}
```

> [!tip] 大白话
> 把 no_agent 想成自动售货机：到点就吐货（跑脚本），不需要店员（LLM）在场。`wakeAgent` 是售货机门口的感应器：感应到没人（false）就不启动，省电（token）。

#### 运行机制与实现细节

任务清单存在 `~/.hermes/cron/jobs.json`，执行历史进 `executions.db`；gateway 每 60 秒 tick 一次检查到期任务，最小调度粒度约为一分钟。cron 会话默认不能再建 cron（防递归）；带 `workdir` 的任务在指定目录**串行**执行，并自动注入该目录的 AGENTS.md / CLAUDE.md，让脚本吃到项目上下文（来源 S7）。

### 本章小结

- Gateway 一个进程连 20+ 平台，`hermes gateway setup` 配置；Nous Portal 一次捆绑 model + tool provider。
- 默认 deny：陌生消息一律不理，用 `hermes pairing approve telegram <code>` 审批配对。
- Gateway 用 systemd / launchd 托管，日志在 `~/.hermes/logs/gateway.log`；无头 VM 记得 `loginctl enable-linger`。
- 平台适配器熔断不自动恢复，需手动 `/platform resume`。
- `cronjob` 工具自然语言管理定时任务，四种调度格式；结果自动投递、agent 不自发消息。
- 模型解析 fails closed：默认模型变更后任务跳过运行、零推理；`no_agent` 模式零 LLM，`wakeAgent` 预检门把高频轮询成本压到近乎零。

下一章把"并行"接进来：委派与 execute_code，让一个 agent 派出多个子代理同时干活。

## 委派与并行：子代理与 execute_code

单个 agent 的上下文是有限的，串行处理多件事又慢又费 token。这一章解决"如何把一个 agent 变成一支队伍"：用 `delegate_task` 把任务拆给[[SubAgent子代理|隔离子代理]]并行处理，用 `execute_code` 把重复步骤写成脚本程序化调用工具，同时守住资源与安全底线。[^c7-S10][^c7-S12]

### 7.1 delegate_task：把任务外包给隔离子代理

`delegate_task` 会拉起一个**隔离子代理**：全新会话（对父会话历史零知晓）、继承父代理的工具权限、运行在独立终端，最终只有一段摘要回到主上下文，中间过程不会污染父上下文。

> [!tip] 大白话
> 把子代理想成外包的临时工：工位（独立终端）和门禁权限（继承的工具权限）都是临时发的，但它看不到你们公司的聊天记录（父会话历史），只交回一份结案报告（摘要）。所以它干活再啰嗦，也不占用你（主上下文）的注意力。

并行批处理有三个默认行为：最多 **3 个并发**、结果**按输入顺序返回**、**顶层委托在后台自动运行**（主对话可继续，不必干等）。成本策略是经典的"frontier 规划 + 廉价 worker"：让贵模型负责拆任务派活，子代理统一用一个便宜模型执行——通过 `delegation.model` 全局 pin 住，子代理自己不能选工具集和模型。[^c7-S10]

```python
# delegate_task 并行委派示意（调用格式以 v0.20.x 文档为准）
delegate_task(
    prompt=[
        "总结 02_deep_research.md 3.3 节的委派要点",
        "列出 S10 文档中的资源限制默认值",
        "提取 3.4 节的安全硬性要求",
    ],
)
# 默认最多 3 并发，结果按输入顺序返回；顶层委托后台自动运行，主对话可继续。
```

### 7.2 execute_code：用脚本程序化调用工具

`execute_code` 让你写一段 Python 脚本，在脚本里直接调用 `web_search` / `read_file` / `write_file` / `patch` / `terminal` 等工具，经 **Unix socket RPC** 与 agent 通信。关键设计：只有脚本里的 `print()` 输出会回到 LLM 上下文，**中间结果一律不进上下文**，省掉大量搜索、读写、跑命令的 token 开销。[^c7-S12]

> [!tip] 大白话
> 把 execute_code 想成一条自动流水线：你把原料（Python 脚本）丢进流水线入口，它自己调用搜索、读写、跑命令完成中间工序，只有末端打好标签的成品（print 出来的内容）送到你眼前。中间半成品不经过你的办公桌，自然不占地方（token）。

```python
# execute_code 脚本（工具签名示意，以 v0.20.x 文档为准）
def main():
    hits = web_search("hermes-agent delegation")   # 搜索结果只留在脚本内
    content = read_file("notes.md")                # 读文件，不进主上下文
    patch("notes.md", "hermes", "Hermes Agent")    # 程序化改文件
    result = terminal("python -m pytest -q")       # 跑命令拿退出码
    print(result)                                  # 只有 print() 回到 LLM
```

执行模式有两种：`project`（默认，用会话工作目录 + 当前 VIRTUAL_ENV/CONDA 解释器，适合日常改动）和 `strict`（临时隔离目录，适合不可信代码）。

### 7.3 资源限制与安全不变量

execute_code 有默认资源上限：超时 **300s**（SIGTERM → 5s 宽限 → SIGKILL）、stdout **50KB**、stderr **10KB**、工具调用 **50 次**，均可配置（以 v0.20.x 文档为准）。全局 pin 与限制的配置示意：

```yaml
# ~/.hermes/config.yaml（片段，以 v0.20.x 文档为准）
delegation:
  model: <worker-model-id>   # 全局 pin：所有子代理统一用这个廉价模型
# execute_code 默认限制：超时 300s / stdout 50KB / stderr 10KB / 工具调用 50 次，均可配置
```

安全上两条不变量：一是子进程环境会**剔除 KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL/PASSWD/AUTH 等敏感变量**，防止密钥泄漏给脚本；二是工具白名单**禁止递归调用 execute_code / delegate_task / [[MCP协议|MCP]]**，防止脚本再开子代理造成失控级联。[^c7-S12]

> [!tip] 大白话
> 第一条像给脚本发"限权工牌"：名字带 KEY、TOKEN、SECRET 的保险箱统统上锁，脚本想看也看不到。第二条像"外包不能再转包"：脚本能调工具，但不能自己再雇一批子代理，防止一层层套娃把系统拖垮。

一个重要的可靠性提醒（**分版本**）：v0.18 及之前，**委托结果跨重启不可靠**——进程重启不会续跑未完成的子代理；需要持久执行的场景（如定时巡检）请用第六章的 `cronjob` 或 background terminal。**v0.19 起**，后台委托已支持跨重启持久化：子代理结果经 ownership-checked ledger 恢复并在重启后继续投递；gateway 若在发送中途崩溃，交付义务账本会在下次启动补发，堵住消息静默丢失 [^c7-S19]。因此新版本下顶层委托可作轻量并行手段，但周期调度仍以 `cronjob` 为持久方案。

### 本章小结

- `delegate_task` 用隔离子代理做并行：全新会话、继承权限、只回摘要，主上下文不被污染。
- 默认最多 3 并发、结果按输入序返回、顶层委托后台自动运行。
- "frontier 规划 + 廉价 worker"：`delegation.model` 全局 pin，子代理不能自选工具集。
- `execute_code` 用 Python 脚本程序化调工具，只有 `print()` 回上下文，中间结果省 token。
- 资源限制与安全不变量是默认护栏；跨重启不可靠，持久执行交给 cronjob / background terminal。

下一章进入部署进阶：在 Docker 中跑 Hermes、暴露 OpenAI 兼容 API，并落实安全基线。

[^c7-S10]: S10：Hermes Agent 官方文档 *Delegation*（`docs/user-guide/features/delegation`）。
[^c7-S12]: S12：Hermes Agent 官方文档 *Code Execution*（`docs/user-guide/features/code-execution`）。
[^c7-S19]: S19：Hermes Agent v0.19.0（Quicksilver）发布说明，https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.20

## 部署进阶：Docker、多后端与安全基线

前几章 Hermes 跑在本地 CLI 里，属于"随开随用"。本章解决常驻部署问题：用 Docker 把 Hermes 跑成 7×24 服务、通过 API server 对外提供 OpenAI 兼容接口、在多种终端后端之间做选择，并守住一条不能妥协的安全基线（来源 S11、S17）。

### Docker 的两种用途：先分清你要哪种

Docker 里跑 Hermes 有两种诉求完全不同，别混为一谈（来源 S11）：

1. **跑 Hermes 本体**：把整个 agent 装进容器，作为常驻服务对外提供 Gateway / API。
2. **只当 terminal 后端**：Hermes 本身仍在宿主机跑，但所有命令执行丢进一个**单常驻沙箱容器**，隔离文件系统与依赖。

第二种延续第七章 `execute_code` / terminal 的隔离思路，适合"不想让 agent 直接在宿主上跑命令"的场景。

> [!tip] 大白话
> 把 Docker 想成两种租房：一种是整租，agent 全家搬进容器过日子；另一种是厨房外包，agent 住外边，只在专用的厨房里做饭（执行命令）。先想清楚要哪种，再写 docker run。

### 数据卷持久化：镜像无状态，配置不丢

跑本体的关键是一条挂载：容器内 `/opt/data` 挂到宿主 `~/.hermes`，里面是全部状态——`.env`、`config.yaml`、`SOUL.md`、`sessions/`、`memories/`、`skills/`、`home/`、`cron/`、`hooks/`、`logs/` 等。镜像本身无状态，升级只换镜像、不碰数据卷，配置自然保留（来源 S11）：

```bash
# 首次初始化：只做一次
mkdir -p ~/.hermes
docker run --rm -it \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent:latest setup

# 常驻运行 Gateway
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent:latest gateway run
```

> [!tip] 大白话
> 把数据卷想成外接保险箱：容器是随时可拆换的装修房，保险箱（`~/.hermes`）里的东西一直留着。所以不用慌"升级丢配置"——pull 新镜像重装修即可。

镜像本身内置得很全：基于 debian:13.4，带 Python 3.13（uv 管理）、Node 26、Playwright/Chromium、openssh-client 与 s6-overlay；还附带 docker-cli，可把 `/var/run/docker.sock` 挂进容器去驱动宿主 Docker——相当于"容器里的 agent 再调 Docker"的嵌套玩法（来源 S11）。

### 首次配置：跑一遍 setup 向导

镜像无状态，配置全在数据卷里，所以第一次运行先建目录、挂载并跑配置向导——**这一步只做一次**，之后所有配置与密钥都落在宿主机 `~/.hermes`：

```bash
mkdir -p ~/.hermes
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent setup
```

向导交互项（来源 S11）：

- **Setup mode**：选 Quick setup（provider、model 与 messaging 一次配完）
- **Model provider**：OpenAI / Anthropic / DeepSeek / xAI / 阿里云 等，任选一家
- **Messaging platform**：本地先跳过，之后要接 Telegram / Discord 再跑 `hermes gateway setup`

向导结束会写两个文件：`~/.hermes/config.yaml` 存"模型在哪、怎么连"，`~/.hermes/.env` 存 API key——与第三章"配置与密钥分离"同一套基线；容器内路径对应 `/opt/data/config.yaml` 与 `/opt/data/.env`（来源 S11）。

> [!tip] 大白话
> 向导像"办入住手续"：选好模型供应商、登记门禁（API key）。钥匙进保险箱（.env）、房号进登记本（config.yaml），办完一次，之后每次开容器都认这个身份。

### 日常使用：进容器开聊

配好后最直接的用法是交互式开聊（来源 S11）：

```bash
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent
```

容器已在后台跑（gateway 模式）时，也可进容器直接调 hermes 二进制 `/opt/hermes/.venv/bin/hermes`（来源 S11）：

```bash
docker exec -it hermes /opt/hermes/.venv/bin/hermes
```

容器内排错与配置命令与本地 CLI 一致，入口是 `hermes doctor`（来源 S11）：

```bash
hermes doctor                  # 诊断配置与密钥是否齐全，排错第一步
hermes model                   # 会话外完整模型向导（增删 provider、设默认）
hermes tools                   # 查看已启用工具
hermes config get <key>        # 读 config.yaml
hermes config set <key> <val>  # 写 config.yaml
```

> [!tip] 大白话
> 把容器里的 hermes 命令想成酒店客房服务电话：房间（容器）可以换，拨号方式（命令）不变。数据卷在，身份和家当就一直在。

### Docker Compose：推荐的长期部署方式

如果要长期运行，建议用 Compose 管理容器生命周期。先在宿主机创建 `~/hermes-stack/compose.yaml`：

```yaml
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    command: gateway run

    volumes:
      - ${HOME}/.hermes:/opt/data
      # 按需挂载宿主机项目目录；路径替换为实际目录
      # - /path/to/your/project:/work:rw

    # 只绑定到宿主机本地；只使用 Telegram/Discord 时可以删除这一段
    ports:
      - "127.0.0.1:8642:8642"

    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
```

初始化并启动：

```bash
mkdir -p ~/.hermes ~/hermes-stack
cd ~/hermes-stack

# 首次运行配置向导
docker compose run --rm hermes setup

# 后台启动
docker compose up -d

# 查看日志
docker compose logs -f hermes
```

如果要接 Open WebUI 或其他 OpenAI-compatible 客户端，先在 `~/.hermes/.env` 中加入：

先生成一串随机密钥：

```bash
openssl rand -hex 32
```

复制命令输出的 **64 位字符串**，再编辑配置文件：

```bash
nano ~/.hermes/.env
```

加入下面三行，把 `API_SERVER_KEY` 等号后的内容替换成刚才复制的字符串：

```env
API_SERVER_ENABLED=true
API_SERVER_HOST=0.0.0.0
API_SERVER_KEY=把刚才生成的64位字符串粘贴到这里
```

保存后收紧文件权限：

```bash
chmod 600 ~/.hermes/.env
```

> [!warning] 密钥不是占位文本
> 不要把 `把刚才生成的64位字符串粘贴到这里` 或尖括号原样写入；它只是示意。该密钥是 Hermes API 的 Bearer Token，不是模型 Provider 的 API Key，也不要发到聊天、Git 或截图中。

然后重新创建服务使配置生效：

```bash
cd ~/hermes-stack
docker compose up -d --force-recreate
```

宿主机客户端使用 `http://127.0.0.1:8642/v1`；API Key 填 `API_SERVER_KEY`。API server 具有终端等完整工具权限，不能无认证暴露公网（来源 S11）。

### 排查 `PermissionError: /opt/hermes/.env`

如果启动时出现：

```text
PermissionError: [Errno 13] Permission denied: '/opt/hermes/.env'
```

这通常不是 `API_SERVER_KEY` 的格式问题，而是 Hermes 误读了镜像内部的安装目录。用户配置和密钥应位于宿主机 `~/.hermes/.env`，容器内对应 `/opt/data/.env`；`/opt/hermes` 是镜像的只读安装树，不要对它执行 `chmod` 或写入密钥（来源 S11）。

先检查容器挂载，输出中不要包含 `.env` 文件内容：

```bash
cd ~/hermes-stack
docker inspect hermes --format \
  '{{range .Mounts}}{{println .Source " -> " .Destination}}{{end}}'
```

正常应看到：

```text
宿主机的 ~/.hermes -> /opt/data
```

不应出现任何指向 `/opt/hermes` 或 `/opt/hermes/.env` 的挂载。Compose 的核心挂载应保持为：

```yaml
volumes:
  - ${HOME}/.hermes:/opt/data
```

修正挂载后，拉取镜像并重建：

```bash
docker compose pull
docker compose down --remove-orphans
docker compose up -d --force-recreate
docker compose logs -f hermes
```

如果仍然报错，可用临时 shell 检查两个路径是否存在及权限，不要打印文件内容：

```bash
docker compose run --rm --no-deps \
  --entrypoint /bin/sh hermes -lc '
    for f in /opt/hermes/.env /opt/data/.env; do
      if [ -e "$f" ]; then ls -l "$f"; else echo "MISSING: $f"; fi
    done
  '
```

日志中的 `config predates version 12` 是独立的旧配置警告。先备份配置，再按向导重新生成：

```bash
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.backup
docker compose run --rm hermes setup
```

升级时执行：

```bash
cd ~/hermes-stack
docker compose pull
docker compose up -d
```

`~/.hermes` 是持久化数据目录，删除或更新容器不会丢失配置、记忆和会话。Compose 的完整部署方式以官方 Docker 文档为准（来源 S11）。

### 让容器访问宿主机目录：bind mount

容器默认看不到宿主机上的其他目录。若要让 Hermes 读取或修改宿主机项目，在 Compose 的 `volumes` 下增加一条挂载：

```yaml
volumes:
  - ${HOME}/.hermes:/opt/data
  - /path/to/your/project:/work:rw
```

其中 `/path/to/your/project` 是宿主机路径，`/work` 是容器内路径。只读场景使用 `:ro`：

```yaml
- /path/to/your/project:/work:ro
```

挂载后重新创建容器并验证：

```bash
cd ~/hermes-stack
docker compose up -d --force-recreate
docker exec hermes sh -lc 'ls -la /work'
```

如果希望 Gateway 默认在该目录工作，可在 `~/.hermes/config.yaml` 中设置：

```yaml
terminal:
  backend: local
  cwd: /work
```

这里的 `local` 指 Hermes 容器内部，而不是宿主机。之后应让 Hermes 使用 `/work/...` 路径，不要使用宿主机原始路径。macOS Docker Desktop 可能需要先在 **Settings → Resources → File Sharing** 中允许该目录；Linux 下若出现权限错误，应为专用工作目录授予容器用户相应权限，不要直接使用 `chmod 777`。

> [!warning] 挂载权限
> `:rw` 允许 agent 修改甚至删除宿主机文件。只需要分析内容时优先使用 `:ro`，不要把整个宿主机 Home 目录或 `/` 挂载进容器。

### Gateway 模式：暴露 OpenAI 兼容 API

`-p 8642:8642` 暴露的是 Hermes 的 API server（Gateway 模式）：OpenAI 兼容 API + 健康端点，容器内由 s6-overlay 监督进程，崩溃自动重启。官方建议同时打开 `tool_loop_guardrails.hard_stop_enabled`，给死循环工具调用一个硬停止兜底（来源 S11）。

```bash
# API server 环境变量：安全硬性要求，三个缺一不可
-e API_SERVER_ENABLED=true \
-e API_SERVER_HOST=0.0.0.0 \
-e API_SERVER_KEY=<至少8位强密钥>
```

> [!tip] 大白话
> `API_SERVER_KEY` 想成门禁卡：`API_SERVER_HOST=0.0.0.0` 等于把门开到公网，没门禁卡谁都能进。所以官方强制三件套——开门、绑公网、必须刷 8 位以上密钥。

### 安全硬性要求：一次真实事故

把 API 绑到 `0.0.0.0` 意味着暴露公网，因此安全要求是硬性的：`API_SERVER_ENABLED=true` + `API_SERVER_HOST=0.0.0.0` + `API_SERVER_KEY` ≥8 位，三者缺一不可（来源 S11）。dashboard（`HERMES_DASHBOARD=1`，端口 9119）同理：非环回绑定必须配认证，否则 fail-closed 拒绝启动。dashboard 内置三种认证方式：basic auth（`HERMES_DASHBOARD_BASIC_AUTH_USERNAME` + `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD`，可加 `HERMES_DASHBOARD_BASIC_AUTH_SECRET` 固定会话）、Nous Portal OAuth（设 `HERMES_DASHBOARD_OAUTH_CLIENT_ID` 即启用）、自建 OIDC（`HERMES_DASHBOARD_OIDC_ISSUER` + `HERMES_DASHBOARD_OIDC_CLIENT_ID`）；旧的 `HERMES_DASHBOARD_INSECURE=1` 已废弃为 no-op。这不是危言耸听——2026-06 就曾发生未认证仪表盘被扫描器发现、植入 SSH 后门的事件（来源 S11）。部署到公网前，把这条当检查清单逐项打勾；起容器后先用健康端点做一次存活探活，确认 API 正常再放行流量（来源 S11）。把原则记成一句话：**凡是暴露到非 loopback 的入口，要么有认证，要么 fail-closed 拒绝启动**——宁可不服务，也不裸奔（来源 S11）。

### 多容器 / 多 profile：数据目录是排他锁

一个高频坑：**禁止两个 gateway 容器挂同一个数据目录**，并发写不被支持。官方推荐单容器多 profile，但各 profile 的 API server 默认都绑 8642，必须为每个 profile 设独立 `API_SERVER_PORT`（来源 S11）。

镜像权限模型：`/init` 以 root 启动，随后经 `s6-setuidgid` 降权为 hermes 用户（UID 10000）；默认拒绝 root 启动 gateway（可用 `HERMES_ALLOW_ROOT_GATEWAY=1` 覆盖，但不建议）；`/opt/hermes` 安装树只读不可变。这是"最小权限"落到容器里的标准做法（来源 S11）。

> [!tip] 大白话
> 想成物业规矩：管理员（root）只在开荒时进门，之后所有住户都用普通工牌（UID 10000）。配置和数据分开，才是安全的长期租约。

### 多后端清单与版本漂移

README 宣称支持 7 种终端后端：local / Docker / SSH / Singularity / Modal / Daytona / Vercel Sandbox（来源 S1）。其中 Modal / Daytona 提供 serverless 持久化——空闲休眠、按需唤醒，适合不想常驻 VPS 的场景（来源 S17）。

但这份清单**会漂移**：v0.15.0 曾移除 Vercel Sandbox 后又回归，`terminal-backends` 文档页也已 404。所有涉及后端数量、Vercel 的内容一律**以 v0.20.x 文档为准**（来源 S1）。把后端同步到远程（Docker/SSH/Modal/Daytona）时还要防凭据泄露：`~/.hermes` 同时含 `.env` 密钥与 `auth.json` OAuth token，必须配置 ignore 排除，否则凭据进入不受控基础设施（来源 S17）。

Docker terminal 后端配置示例（作为第二种用途，来源 S11/S12）：

```yaml
# ~/.hermes/config.yaml —— 让命令执行进 Docker 沙箱
terminal:
  backend: docker
  docker_image: hermes-agent:latest
  docker_volumes:
    - /path/to/work:/work
  docker_run_as_host_user: true
  docker_persist_across_processes: true
  docker_orphan_reaper: true
```

skills 目录与凭据文件会被自动**只读 bind-mount** 进沙箱，避免容器内 agent 篡改（来源 S11/S12）。`docker_persist_across_processes` 控制容器是否跨 Hermes 进程存活，`docker_orphan_reaper` 负责回收孤儿进程，配合第 4 章凭据只放 `~/.hermes/.env` 的基线一起用，才能让沙箱既隔离又不丢状态（来源 S11/S12）。

### 资源建议与升级策略

- 内存：1GB 起、2-4GB 推荐；浏览器自动化最耗内存，跑 Playwright 场景直接按推荐档预留。
- 数据卷：500MB 起步，建议预留 2GB；`sessions/` 与 `logs/` 会随使用持续增长，预留留足。

升级路径：pull 新镜像 → 重建容器，数据保留在卷里；配置自动迁移并生成**时间戳备份**，出问题可回滚（来源 S11）。

### 本章小结

- Docker 两种用途：跑 Hermes 本体，或只作 terminal 后端沙箱。
- `/opt/data` 挂 `~/.hermes` 实现"镜像无状态、升级不丢配置"。
- Gateway 模式 `-p 8642:8642` 暴露 OpenAI 兼容 API + 健康端点，s6-overlay 崩溃自重启。
- 安全三件套：`API_SERVER_ENABLED=true` + `API_SERVER_HOST=0.0.0.0` + `API_SERVER_KEY` ≥8 位；dashboard 非环回绑定必须认证。
- 禁止两个 gateway 共用一个数据目录；多 profile 各设独立 `API_SERVER_PORT`；容器以 hermes（UID 10000）运行。
- 后端数量与 Vercel 相关描述以 v0.20.x 文档为准。
- 首次配置跑一次 `setup` 向导（Quick setup 选 provider/model/messaging）；日常 `docker run -it ... hermes` 进容器开聊，排错先 `hermes doctor`。

下一章收尾：把前八章散落的坑集中成一张清单——Windows 杀软误报、文件锁、凭据泄露、systemd 反模式与版本漂移总原则。

## 常见坑与最佳实践

> 前八章把 Hermes 的安装、模型、记忆、技能、自动化与部署都跑通了，本章直给结论：先排掉 Windows 与凭据这两类代价最高的坑，再给 systemd、熔断器、版本漂移等高频陷阱的兜底方案，最后是一份可照着抄的安全基线速查。

### Windows 原生还是 WSL2：结论先行

README 称原生"无需 WSL"，providers 文档却要求"需要 Unix 环境，Windows 用户应在 WSL2 内运行"，安装文档又给原生标了 early beta[^c9-s1][^c9-s5]。三处口径不一致的结论是：**原生能跑通 CLI，但模型服务、开发链路与稳定性以 WSL2 为准**。除非只是轻量试用，否则直接装进 WSL2，能省掉后续绝大部分平台类排查。

> [!tip] 大白话
> 把 WSL2 想成住在 Windows 里的一台 Linux 小电脑。原生模式像是"在别人家客厅摆摊"，能摆但处处受主人规矩限制；WSL2 是"自己租了一间房"，规矩少、好折腾。想要稳定地跑模型服务和开发链，就选 WSL2。

### 杀软误报：把 uv.exe 当成病毒

Defender / Bitdefender / 腾讯管家会把 `uv.exe`（Astral 未签名的 Rust 二进制）误报为病毒[^c9-s1][^c9-s18]。处理要点：

- 白名单加**整个 Hermes 安装/缓存文件夹**，而不是按文件哈希——uv 每个版本哈希都变，按哈希加每次升级都要重加。
- 仍不放心就用官方校验兜底：`gh attestation verify` 核对二进制来源。

### Windows 文件锁：更新报 access denied

Issue #16201 记录了 Windows/Git Bash 下 uv.exe、hermes.exe 更新替换时报 access denied（os error 5）的问题[^c9-s14]。成因是运行中的进程锁住了待替换文件。实践上：**更新前先关闭所有 Hermes 进程**（CLI、gateway、桌面端）再执行更新，可避开绝大多数文件锁冲突。

> [!tip] 大白话
> 这就像想换掉抽屉里正被手按住的旧文件——手不拿开，文件就换不了。更新前先关掉 Hermes，就是先把"手"拿开。

### 凭据泄露风险：`~/.hermes` 不能整箱上传

`~/.hermes` 同时存放 `.env`（API 密钥）与 `auth.json`（OAuth token）[^c9-s5]。一旦把该目录同步到远程后端（Docker / SSH / Modal / Daytona）或云盘，且没有配置 ignore，密钥就会进入不受控基础设施[^c9-s17]。这是成本最高的一类坑——泄露的模型 key 会被盗刷。

> [!tip] 大白话
> `~/.hermes` 像你的保险箱，钥匙（.env）和门禁卡（auth.json）都放在一起。把它整箱拖进云盘或远程服务器却不设 ignore，等于把保险箱钥匙插在锁孔上出门。同步前必须把密钥文件排除在外。

### systemd 反模式与无头 VM

- 勿加 `ExecStopPost` kill drop-in——gateway 崩溃被强杀后，配合自动重启会陷入无限重启循环[^c9-s6]。
- 无头 VM 上把 gateway 跑成 user service，并执行 `loginctl enable-linger`，让用户会话在无登录时也保持存活。
- macOS 用 launchd 静态固化 PATH：装完新工具后记得重跑 `hermes gateway install` 刷新 PATH，否则 gateway 找不到新命令。

> [!tip] 大白话
> `ExecStopPost` kill 相当于给服务装了"一停下就补刀"的机关枪；配合自动重启，服务刚爬起来就被自己人打死，永远起不来。改成只负责拉起来的方式（user service + linger），服务才站得住。

### 其他高频坑

- **熔断器不自动恢复**：平台适配器熔断后要手动 `/platform resume`，否则该平台一直拒活[^c9-s6]。
- **手动 clone 时 venv 放源码树外**：agent 的相对路径清理会误删运行中的环境[^c9-s1]。
- **后台进程不真正保活**：默认 24h 后（`bg_process_max_age_hours`）后台进程不再阻止会话自动重置——它只是被忽略、不是被 kill，别指望它持续干活[^c9-s6]。

### 版本漂移总原则

后端数量、Vercel Sandbox、`terminal-backends` 页面路径等都在随版本变动（v0.15.0 曾移除 Vercel 后端、文档页 404 后迁移）[^c9-s1][^c9-s14]。凡涉及上述内容，一律标注"以 v0.20.x 文档为准"，并留意版本号变化导致的旧配置（如 `VERCEL_TOKEN`）失效。

### 安全基线速查

| 项 | 做法 |
|----|------|
| 密钥存放 | 只放 `~/.hermes/.env`，不写进 config.yaml |
| 远程后端同步 | exclude 密钥文件（.env / auth.json） |
| Docker gateway | 非 root 运行 + `API_SERVER_KEY` ≥8 位 + dashboard 强制认证 |

### 本章小结

- Windows 稳定性以 WSL2 为准；杀软白名单加整个文件夹，更新前先关进程。
- `~/.hermes` 是保险箱：同步远程后端必须先 exclude 密钥文件。
- systemd 勿加 `ExecStopPost` kill；无头 VM 用 user service + `loginctl enable-linger`。
- 熔断器、后台进程都有"不自动恢复 / 不真正保活"的边界，别依赖它们兜底。
- 版本敏感信息一律标注"以 v0.20.x 文档为准"。

下一章进入身份定制与多 Agent：用 SOUL.md 定义全局人格、用 Profiles 拆出多套隔离实例、用 Bot Mode 把多个 agent 编排成能协作的 bot。

[^c9-s1]: GitHub README — NousResearch/hermes-agent
[^c9-s5]: 官方文档 /docs/integrations/providers
[^c9-s6]: 官方文档 /docs/user-guide/messaging
[^c9-s14]: GitHub Issue #16201（Windows/Git Bash 更新文件锁）
[^c9-s17]: 阿里云开发者社区：Hermes 多后端部署运维
[^c9-s18]: CSDN：Hermes Agent Windows 实操经验

## 身份定制与多 Agent：SOUL.md、Profiles 与 Bot Mode

前九章把 Hermes 当"一个 agent"在用。这一章把它变成"任意多个、每个性格不同"的 agent：用 `SOUL.md` 定义全局人格、用 Profiles 拆出多套完全隔离的实例、用 Bot Mode（v0.20.3+）把这些实例编排成能互相协作的命名 bot。[^c10-1][^c10-2][^c10-3]

### SOUL.md：全局人格定制

Hermes 的"我是谁、怎么说话"由 `SOUL.md` 决定：它作为 system prompt 的 **slot #1** 被**原样注入、无任何包装文字**，并**完全替换**内置默认人格（"You are Hermes Agent..."）。文件缺失、为空或加载失败时才回退内置人格 [^c10-1]。

- **位置**：只读全局文件 `~/.hermes/SOUL.md`（自定义 home 时为 `$HERMES_HOME/SOUL.md`）；Docker 部署对应 `/opt/data/SOUL.md`
- **生命周期**：首次运行自动播种初始文件，之后**永不覆盖**；编辑只在**新会话**生效（进行中的会话不变，保住前缀缓存）
- **安全**：注入前过 prompt-injection 扫描（经典注入、promptware/C2、角色劫持模式一律阻断）
- **与 AGENTS.md 分工**：SOUL.md 放"处处适用"的人格与语气（如"说话直接"、"不写营销腔"）；AGENTS.md 放"只属于某项目"的约定（如"用 pytest 不用 unittest"、"API 跑在 8000 端口"）。规则一句话：**处处适用 → SOUL.md；单项目专属 → AGENTS.md**[^c10-1]

```markdown
# ~/.hermes/SOUL.md（内容示意；以 v0.20.x 文档为准）
你是 Hermes Agent，但说话直接、不写营销腔。
不确定时明确说"我不确定"，并把推测与证据分开。
```

官方提供 4 套起步人格模板：**Pragmatic Engineer**（直接、简洁、拒绝奉承）、**Research Partner**（好奇、诚实标注不确定性）、**Teacher/Explainer**（耐心、从直觉讲到细节）、**Tough Reviewer**（严格、直白优于外交）[^c10-1]。建议流程：先修剪种子文件、写 4-8 行语气与默认值，跑几轮对话再迭代，别一次性堆满。`/personality` 与 SOUL.md 互补：SOUL.md 是持久基线，`/personality` 只做临时切换。

> [!tip] 大白话
> SOUL.md 像"入职时签的性格说明书"：它决定 agent 是毒舌工程师还是耐心老师，全局生效、跨项目不变。想换性格就改这一份文件，重启会话生效；AGENTS.md 则是"每个项目的工作手册"，只在那个项目里生效。

### Profiles：一套 Hermes 变多套

Profiles 让一台机器上跑**多套完全隔离**的 Hermes 实例，每套拥有独立的 `HERMES_HOME` 目录：自己的 config.yaml（模型/工具）、.env（密钥）、SOUL.md（人格），以及 memories/sessions/skills/cron/gateway 状态 [^c10-2][^c10-4]。

```bash
hermes profile create coder               # 新建空白 profile
hermes profile create research --clone    # 复制当前 config / SOUL / .env
hermes profile create writing --clone-all # 全量快照（含记忆 / 技能）
hermes profile use coder                  # 设为默认（粘性生效）
coder chat                                # 直接以该 profile 开聊（自动生成别名）
hermes -p coder chat                      # 或显式指定
hermes profile list | show | rename | delete
hermes profile export coder               # 打包 tar.gz 用于迁移
hermes profile import coder.tar.gz
```

官方推荐的典型组合：`coder`（技术/简洁）、`personal`（日常/友好）、`research`（细致/谨慎）、`writing`（文档创作），每个 profile 配一份契合的 SOUL.md [^c10-4]。

**v0.19 起还能做 profile 级消息路由**：一个 gateway、一个 bot token，把不同 guild/频道/线程路由到不同 profile，彼此 config/技能/记忆/密钥完全隔离——例如同一个 bot 同时服务 `work` 与 `personal` 两套身份 [^c10-2]。

> [!tip] 大白话
> 把 Profiles 想成"同一套软件开多个用户账号"：每个账号有自己的桌面（配置）、钥匙串（密钥）、人设（SOUL.md）和聊天记录（记忆）。想切就切，互不串台；想搬家就 `export` 打个包带走。

### Bot Mode（v0.20.3+）：把 Profiles 变成能协作的 Bot

Bot Mode 从桌面版 v0.20.3 起默认开启：把 Profiles 升级成一张**命名 Bot 花名册**——每个 bot 可设头像、pin 模型、启用技能、配独立 SOUL.md、挂调度计划 [^c10-3]。Bot 之间通过持久的 **Agent Inbox** 通信，支持 2-6 个 bot 的**多 agent 协作房间**，并可跨 bot `@mention` 交接任务：

```bash
hermes -p <bot> chat -c "Agent Inbox"     # 以某 bot 身份进 Inbox 频道协作
```

> [!tip] 大白话
> 把 Bot Mode 想成"给每个分身起名字、发工牌、组项目群"：以前的 Profiles 是互不认识的同事，Bot Mode 让它们能拉群、@人、交接活。

### 本章小结

- `SOUL.md` 是全局人格：system prompt slot #1、原样注入、替换默认身份；只读 `~/.hermes/SOUL.md`，永不覆盖、新会话生效、注入前过扫描。
- SOUL.md 管"处处适用的人格"，AGENTS.md 管"单项目约定"；官方给 4 套人格模板，`/personality` 做临时切换。
- Profiles 是完全隔离的实例：`hermes profile create/use/export/import` 等；v0.19 起支持一个 gateway 按频道路由到不同 profile。
- Bot Mode（v0.20.3+）把 Profiles 变成命名 bot 花名册：头像、模型 pin、SOUL、调度；Agent Inbox + 2-6 bot 协作房间，`@mention` 交接。

下一章是附录：常用命令速查表，把全书高频命令收拢成一张可随时查阅的表。

[^c10-1]: 官方 SOUL.md 指南：https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/use-soul-with-hermes.md
[^c10-2]: Hermes Agent v0.19.0（Quicksilver）发布说明：https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.20
[^c10-3]: Hermes Agent v0.20.x 发布说明（Bot Mode、桌面工作台、A2A、webhook）：https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.27
[^c10-4]: 掘金：Hermes Profiles 多 Agent 配置指南 https://juejin.cn/post/7631497675088740387

## 附录：Hermes Agent 常用命令速查

> 面向已读完正文、需要回查的读者。命令/指令全部来自研究素材与正文各章；涉及后端数量、页面路径等易漂移内容以 v0.20.x 文档为准。

### 安装与配置

| 命令/指令 | 用途 | 所在章节 |
| --- | --- | --- |
| `curl -fsSL https://hermes-agent.nousresearch.com/install.sh \| bash` | Linux/macOS/WSL2/Termux 一行安装（自动装 uv、Python 3.11、Node 22、ripgrep、ffmpeg） | ch2 |
| `iex (irm https://hermes-agent.nousresearch.com/install.ps1)` | Windows 原生 PowerShell 安装 | ch2 |
| `source ~/.bashrc` | 安装后刷新 PATH，之后直接 `hermes` 开聊 | ch2 |
| `hermes setup` | 交互式初始化配置向导 | ch2 |
| `hermes setup --portal` | 最快打通：OAuth 登录 + Nous Provider + Tool Gateway 一次搞定 | ch2 |
| `hermes doctor` | 环境诊断（配置最小集的第一步） | ch2 |
| `hermes desktop` | 纯 CLI 安装后随时补装桌面版 | ch2 |
| `hermes model` | 会话外模型完整向导（切换/新增 provider，不锁定） | ch3 |

### 配置管理

| 命令/指令 | 用途 | 所在章节 |
| --- | --- | --- |
| `hermes config get <key>` | 读取配置（唯一来源 `~/.hermes/config.yaml`） | ch3 |
| `hermes config set <key> <value>` | 写入配置项 | ch3 |
| `/model` | 会话内切换已配置的模型 | ch3 |

### 工具与网关

| 命令/指令 | 用途 | 所在章节 |
| --- | --- | --- |
| `hermes tools` | 查看/管理已启用工具 | ch2 |
| `hermes gateway setup` | 交互式配置多平台网关（Telegram/Discord/Slack/WhatsApp…） | ch6 |
| `hermes pairing approve telegram <code>` | DM 配对：把用户加入默认 deny 白名单 | ch6 |
| `hermes gateway install` | 固化/重装 gateway 服务（macOS 装新工具后重跑以更新 PATH） | ch6 |
| `/platform resume` | 手动恢复熔断后不自动恢复的平台适配器 | ch6 |

### 技能

| 命令/指令 | 用途 | 所在章节 |
| --- | --- | --- |
| `/learn` | 从本地目录/URL/会话流程自动生成技能 | ch5 |
| `/skills` | 查看已装技能（观察"学习闭环"的入口） | ch5 |
| `hermes skills trust` | 信任项目级技能后才会加载 | ch5 |
| `skill_manage` | 工具：agent 自建/改/删技能（程序记忆，自改进循环） | ch5 |
| `skills.write_approval` | 配置项：技能写入审批门（开启后前台内联确认或进 `/memory pending`） | ch5 |

### 记忆

| 命令/指令 | 用途 | 所在章节 |
| --- | --- | --- |
| `/journey` | 学习闭环时间线（删 memory 块即移除、技能归档可恢复） | ch4 |
| `/memory pending` | 查看后台自我改进 stage 的待确认写操作 | ch4 |
| `memory add` | 写入记忆条目（无 read，自动注入上下文） | ch4 |
| `memory replace` | 用 `old_text` 唯一子串匹配替换记忆 | ch4 |
| `memory remove` | 删除记忆（`old_text` 唯一子串匹配） | ch4 |
| `session_search` | SQLite FTS5 跨会话检索真实消息（约 20ms、免费） | ch4 |

### 委派与代码执行

| 命令/指令 | 用途 | 所在章节 |
| --- | --- | --- |
| `delegate_task` | 隔离子代理并行批处理（默认最多 3 并发、仅最终摘要回主上下文） | ch7 |
| `execute_code` | Python 脚本程序化调用工具（web_search/read_file/write_file/patch/terminal…；仅 `print()` 返回） | ch7 |

### cron 定时任务

| 命令/指令 | 用途 | 所在章节 |
| --- | --- | --- |
| `cronjob` | 工具：自然语言建/停/改/删定时任务（相对延迟 30m/2h、间隔 every 2h、cron 表达式、ISO 时间戳） | ch6 |

### 身份定制与多 Agent

| 命令/指令 | 用途 | 所在章节 |
| --- | --- | --- |
| `~/.hermes/SOUL.md` | 全局人格文件（system prompt slot #1，原样注入、新会话生效） | ch10 |
| `/personality` | 临时切换人格（SOUL.md 是持久基线，此命令只做临时覆盖） | ch10 |
| `hermes profile create <name> [--clone\|--clone-all]` | 新建隔离 profile（可选复制配置 / 全量快照） | ch10 |
| `hermes -p <name> chat` | 以指定 profile 开聊 | ch10 |
| `hermes profile use <name>` | 设为默认 profile（粘性生效） | ch10 |
| `hermes profile list/show/rename/delete` | 管理 profile 生命周期 | ch10 |
| `hermes profile export <name>` / `import <file.tar.gz>` | 打包 / 导入 profile（跨机器迁移） | ch10 |
| `hermes -p <bot> chat -c "Agent Inbox"` | Bot Mode：以命名 bot 身份进 Inbox 协作（v0.20.3+） | ch10 |

### 部署与安全

| 命令/指令 | 用途 | 所在章节 |
| --- | --- | --- |
| `docker run`（`-v ~/.hermes:/opt/data`） | 使用官方镜像部署 Hermes，挂载宿主配置持久化、升级不丢 | ch8 |
| `docker compose run --rm hermes setup` | Compose 首次初始化配置向导 | ch8 |
| `docker compose up -d` | Compose 后台启动 Hermes Gateway | ch8 |
| `docker compose pull && docker compose up -d` | 拉取新镜像并升级，保留宿主持久化数据 | ch8 |
| `-v /path/to/your/project:/work:rw` | 将宿主机项目目录挂载到容器内 `/work` | ch8 |
| `-p 8642:8642` | Gateway 模式暴露 OpenAI 兼容 API + 健康端点 | ch8 |
| `API_SERVER_ENABLED=true` + `API_SERVER_HOST=0.0.0.0` + `API_SERVER_KEY`（≥8 位） | API 服务器安全基线（dashboard 非环回绑定必须配认证） | ch8 |

### 杂项

| 命令/指令 | 用途 | 所在章节 |
| --- | --- | --- |
| `gh attestation verify <binary>` | 校验安装器/uv.exe 的 GitHub 签名（应对杀软误报） | ch9 |
| `loginctl enable-linger` | 无头 VM 保持 user systemd service 常驻 | ch9 |

> 提示：涉及后端数量、Vercel Sandbox、页面路径（如 `terminal-backends`）等易漂移项，务必以 v0.20.x 文档为准；版本漂移与防坑细节见第九章。
