# 第 1 章 opencode 是什么——定位、架构与 Claude Code 全面对比

如果你已经熟练使用 Claude Code，第一次打开 opencode 时最该问的问题不是"它怎么装"，而是"它凭什么存在"——同一个模型，为什么要换一个工具跑？这一章先回答这个问题：opencode 不是 Claude Code 的换皮克隆，而是一套在"开源、模型解耦、默认行动"三个哲学点上与 Claude Code 分道扬镳的 AI 编码代理。看懂这几个分叉点，后面所有配置差异都会变得顺理成章。

## 定位与核心卖点

opencode 的自我定位是 "The open source AI coding agent"——**MIT 开源**，来自 SST 团队，GitHub 195K+ stars、16M+ 月活开发者 [opencode 官网](https://opencode.ai)。这第一句话就已经和 Claude Code 划清界限：Claude Code 是 Anthropic 的闭源专有产品，opencode 则是你可以审计、复刻、修改的开放项目。

但它和"又一个开源 AI 编码工具"最大的区别，是**将 agent 框架与模型解耦**：

- **Claude Code**：只跑 Claude。官方没有开放模型接入层，本地模型只能靠脆弱的社区代理。
- **opencode**：75+ LLM providers（经 Models.dev）+ Ollama + 任意 OpenAI 兼容端点，通过 `provider/model` 格式自由组合 [GitHub README](https://github.com/anomalyco/opencode)。

对你这样的 Claude Code 用户，这个差异意味着两件事：其一，你已经习惯的 Claude 模型可以直接在 opencode 里继续用（配好 API key 即可）；其二，你不再被单一模型绑定——同一项目里，规划用 Sonnet、批量编辑用便宜模型、分诊用 Haiku，是完全受支持的用法。

> [!tip] 大白话
> 把"agent 框架"想成手机操作系统，把"模型"想成手机上的应用。Claude Code 是 iPhone——系统和应用是同一家做的，好用但封闭；opencode 是 Android——系统开源，你能装任何厂家的应用。所以同一个 Claude 模型在两边都能跑，但只有 opencode 让你随便换别的"应用"。

## 客户端/服务器架构与三种界面（TUI / 桌面 / IDE）

opencode 采用**客户端/服务器分离**架构：一个单后端（server）同时驱动三种前端——终端 TUI、桌面应用、VS Code / Cursor 扩展；后端通过 HTTP API 对外暴露，所以也支持把 TUI 挂到远程 Docker 会话（`opencode attach`）[官方文档](https://opencode.ai/docs/)。

对比 Claude Code：Claude Code 的 CLI 与 VS Code 扩展本质上是同一个进程的不同入口，没有清晰的"后端可被多前端共享"边界。而 opencode 的 TUI 是它的主战场，支持**多会话并行**——同一个项目可以同时启动多个 agent 处理不同任务，这在 Claude Code 里只能靠开多个终端窗口近似实现。

> [!tip] 大白话
> 把 server 想成厨房，把 TUI/桌面/IDE 想成不同的出餐窗口。Claude Code 是每个窗口自己搭了个灶台，opencode 是几个窗口共用同一个厨房——菜是同一个厨房做的，你只是换个窗口取餐。

## 内置双 Agent：build（全权限）与 plan（只读）

Claude Code 没有原生的"模式"概念，读写权限全靠每步弹窗询问。opencode 把模式下沉到了 Agent 层，内置两个 Agent，**Tab 键一键切换** [GitHub README](https://github.com/anomalyco/opencode)：

| Agent | 定位 | 权限行为 |
|-------|------|----------|
| `build`（默认） | 全权限干活 | 文件编辑、命令执行默认放行 |
| `plan`（只读） | 分析、出方案 | 文件编辑默认拒绝，bash 需要询问 |

你可以在 plan 模式下让 agent 先读代码、给方案，确认后再切到 build 执行——这正好对应你在 Claude Code 里"先聊清楚再放权限"的工作习惯，但 opencode 把它变成了一个显式的模式开关，而不是靠权限弹窗反复确认。

子代理方面，opencode 内置一个 `general` 通用子代理，通过 `@general` 在消息中调用（对应 `subagent_depth` 配置，默认 1 层）。Claude Code 的 Subagent 需要你在 `.claude/agents/` 里自己定义，opencode 则把"通用助手"这个默认角色内置了，自定义 Agent（第 8 章）是可选增强。

> [!tip] 大白话
> build 像装修队——进场就动手；plan 像设计师——只画图纸、不动墙。Claude Code 让你每次动手前都签一次字（权限弹窗），opencode 干脆设了两道门：想先看图纸就走 plan，想直接施工就走 build。

## LSP 回喂 + Git 快照安全网

这是 opencode "默认行动"哲学的底层支撑，两个机制配合：

**LSP 回喂**：opencode 自动加载项目的语言服务器（LSP），每次编辑后把编译器诊断（报错、警告、类型错误）**回喂给模型**，下一轮迭代里模型自我纠正 [GitHub README](https://github.com/anomalyco/opencode)。Claude Code 没有内建这个闭环，模型"睁眼瞎写"，只能靠你手动把编译错误贴回去。

**Git 快照安全网**：opencode 的默认权限是"行动，用 /undo 回滚"——它不靠权限弹窗挡你，而是靠 git 快照兜底。每次改动前打快照，出错 `/undo` 一键回到上一个安全点（和 Claude Code 的 `/undo` 一样基于 Git，但前者是兜底机制、后者是补救工具，哲学的先后顺序反过来了）。

> [!tip] 大白话
> LSP 回喂是"每次改完立刻有人检查作业并告诉你哪里错了"；Git 快照是"游戏自动存档"。Claude Code 的做法是每次行动前问你"确定吗"，opencode 的做法是"你先玩，存档我给你记着，玩崩了读档就行"。

## 与 Claude Code 的整体对比

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

### "速度 vs 彻底"的取舍

这个取舍没有绝对优劣，取决于你的场景：

- 追求**快速迭代**（改一个 bug、加一个功能，想尽快看到结果）→ Claude Code 的"只验证自己改动"更合拍；
- 追求**交付质量**（重构、改完不想留回归、测试覆盖要求高）→ opencode 的"跑全套验证"虽然慢，但"写测试 94 个 vs 73 个"这种差距说明它确实更彻底。

值得注意的是**成本**：每 token 单价 ≠ 总成本。opencode 更慢意味着更多 token 消耗，但它的架构支持**逐步路由**（progressive routing）——规划、批量编辑、分诊分别用不同模型（如便宜小模型干机械活、强模型干关键判断），这是第 6 章的核心内容，也是从 Claude Code 迁移后控制成本的主要手段 [DeepInfra](https://deepinfra.com/blog/claude-code-alternative)。

> [!tip] 大白话
> Claude Code 像快刀手——刀起刀落，只确认自己切的那块；opencode 像细活师傅——每改一处都端上来让你验一遍整体，慢但稳。选哪个，看你今天是想快点吃上饭，还是想保证这桌菜不翻车。

## 本章小结

- opencode 是 MIT 开源、将 agent 框架与模型解耦的 AI 编码代理，最大卖点是"一套框架跑任意模型"。
- 客户端/服务器分离架构：一个后端驱动 TUI、桌面、IDE 三种界面，TUI 支持多会话并行。
- 内置 build（全权限）/ plan（只读）双 Agent，Tab 切换，把"先分析后执行"变成显式模式。
- LSP 回喂 + Git 快照是"默认行动"哲学的兜底：边写边自检、出错可回滚，而不是靠权限弹窗拦截。
- 同模型实测：opencode 慢近一倍但更彻底（写测试 94 vs 73 个）；取舍取决于你要速度还是要质量。

## 下一章预告

定位清楚了，下一步是把它跑起来。下一章讲安装、升级与认证：一键脚本的目录优先级、各平台包管理器、`opencode auth login` 与凭据存储，以及一个你必须提前知道的坑——Anthropic 已把部分 OAuth 凭据限定给 Claude Code 专用。
