---
title: DeepSeek-Reasonix CLI 完整参考
topic: DeepSeek-Reasonix
type: reference
difficulty: 上手
tags:
  - DeepSeek-Reasonix
  - CLI
  - 参考手册
  - 速查
created: 2026-08-10
updated: 2026-08-10
status: new
source_project: deepseek-reasonix-tutorial
---

# DeepSeek-Reasonix CLI 完整参考

> [!info] 文档定位
> 一份可查询的 CLI 全量参考：命令全集、启动参数、无头模式与结构化输出。本系列中「命令细节」的唯一权威章，其他章涉及命令时只引用不复制。关联：[[DeepSeek-Reasonix 使用指南]]、[[DeepSeek-Reasonix 会话与交互]]、[[DeepSeek-Reasonix 自动化与 CI]]。

本章面向已熟悉 Claude Code 的用户，把 `reasonix` 的命令与启动参数整理成速查手册。不必一次背完，把它当字典：遇到命令先查表，再对照参数说明。注意 v1 与 main-v2 的 CLI 文档命令列表存在差异，本章以官方 CLI 参考为准，实时权威始终是应用内 `/help` 与 `/keys`。

## 一、命令总览速查表

| 命令 | 用途 | 示例 |
|------|------|------|
| `reasonix` / `reasonix code [dir]` | 交互式代码模式 TUI（默认入口） | `reasonix code .` |
| `reasonix chat` | 纯聊天，无文件系统/shell | `reasonix chat` |
| `reasonix run "<task>"` | 无头一次性执行，CI 友好 | `reasonix run "把 main.go 的 TODO 实现掉"` |
| `reasonix setup` | 首次配置向导 | `reasonix setup` |
| `reasonix doctor` | 健康检查（API/配置/hooks/项目） | `reasonix doctor` |
| `reasonix upgrade` / `update` | 升级（update 为别名） | `reasonix upgrade --check` |
| `reasonix acp` | ACP stdio 后端，供编辑器/IDE | `reasonix acp --model deepseek-pro` |
| `reasonix sessions` | 会话列表管理 | `reasonix sessions` |
| `reasonix prune-sessions --days N` | 清理 N 天前的会话 | `reasonix prune-sessions --days 7` |
| `reasonix stats [transcript]` | 一次性 cost/cache 分解 | `reasonix stats` |
| `reasonix mcp list/search/install/inspect/browse` | MCP 服务管理 | `reasonix mcp list` |
| `reasonix replay <jsonl>` | 转录重放 | `reasonix replay session.jsonl` |
| `reasonix diff <a> <b>` | 两次转录/会话对比 | `reasonix diff a.jsonl b.jsonl` |
| `reasonix commit` | git add + commit（LLM 写提交信息） | `reasonix commit` |
| `reasonix index` | 本地语义索引 | `reasonix index` |

> [!tip] 大白话
> 把 `reasonix run` 想成「叫了个临时工，把活交代完，他干完只交结果就下班」。它不进入交互界面、不等着你按键，专为脚本和 CI 准备。

## 二、交互模式：code vs chat

`reasonix` 有两个交互入口，差别只在「要不要碰你的项目文件」。

| 模式 | 命令 | 能力范围 | 适用场景 |
|------|------|---------|---------|
| 代码模式 | `reasonix code [dir]` | 完整 TUI：文件系统、shell、工具、会话管理（默认） | 日常写代码、改项目 |
| 聊天模式 | `reasonix chat` | 纯对话，**无文件系统/shell** | 问问题、讨论方案、不碰文件 |

代码模式是默认入口，`reasonix` 与 `reasonix code .` 等价（`.` 表示把当前目录作为工作区根）。聊天模式刻意隔离文件系统与 shell，适合只想和模型聊清思路、不想让模型动文件的场景。

## 三、启动参数详解

以下参数适用于 `code` / `chat` / `run` / `acp` 等命令：

| 参数 | 作用 |
|------|------|
| `--model NAME` | 选 provider 或 `provider/model` |
| `--profile economy\|balanced\|delivery` | 运行时工作模式 |
| `--effort LEVEL` | 覆盖推理强度 |
| `--max-steps N` | 工具调用轮数上限，`0`=自动 |
| `--dir PATH` | 工作区根目录 |
| `--add-dir PATH` | 追加可写目录（可重复） |
| `-c` / `--continue` | 恢复最近会话 |
| `-r` / `--resume [QUERY]` | 会话选择器 / 按子串恢复 |
| `--copy` | 复制会话在可写副本继续 |
| `--allowed-tools RULES` | 仅本次会话权限放行（可重复） |
| `--permission-mode MODE` | `ask/auto/acceptEdits/dontAsk/plan/bypassPermissions` |
| `--yolo` | 跳过权限（bypassPermissions 别名） |
| `-p` / `--print` | 一次性只输出最终答案 |
| `--output-format text\|json\|stream-json` | 结构化输出格式 |
| `--auto` / `-y` | permission-mode auto 别名（不能与显式 `--permission-mode` 组合） |
| `--budget <usd>` | 会话成本上限（80% 警告 / 100% 拒绝）【v1】 |
| `--ablate LIST` | 基准测量，禁用子系统（测量工具，非调优开关） |
| `--trajectory PATH` / `--metrics PATH` | 事件流 / 指标输出 |
| `--events-jsonl PATH` | 脱敏生命周期遥测（不能与 `--output-format` 组合） |

几个容易混淆的点：

- `--model` 支持 `deepseek`（provider 名）或 `deepseek/deepseek-v4-pro`（provider/model）两种写法。
- `--profile` 三档是 `economy`（初始只带 9 个工具）/`balanced`（默认）/`delivery`（完整工具面 + 稳定能力代理），**不是**社区流传的 smart/fast/max——那是 `--effort` 的俗称。
- `--budget` 仅在 v1 文档收录，main-v2 下以 `/help` 为准。
- `--continue` 与 `--resume` 都是恢复会话：前者直接恢复最近一次；后者弹选择器或按子串定位；`--copy` 则在可写副本上继续，不污染原会话。
- 参数优先级最高：`flag > ./reasonix.toml > 全局 ~/.reasonix/config.toml > 内置默认`，命令行传参可以覆盖配置文件。

> [!tip] 大白话
> `--allowed-tools` 像「临时门禁卡」：只给这次会话发一张卡，能进哪几扇门（工具）说得很清楚；但它不改变门本身——工具都还在，只是这次没放行。所以它是**权限放行**，不是**删除工具**。

## 四、无头与管道模式

无头（headless）模式让你不打开 TUI 也能跑一次完整任务，是 CI 与脚本的入口。

直接给任务：

```bash
reasonix run "把 main.go 的 TODO 实现掉"
```

`-p` / `--print` 让输出只保留最终答案，方便接管道：

```bash
reasonix run -p "修复这个函数的 bug" | jq .
```

管道输入同样支持——从 stdin 读任务：

```bash
echo "帮我生成项目的 README" | reasonix run
```

无人值守必须显式放行权限，否则默认 fail-closed 会拒绝写操作：

```bash
reasonix run --auto "批量重命名所有测试文件"
# 等价：reasonix run -y "..." / reasonix run --permission-mode auto "..."
```

> [!note] 退出码约定
> 无头模式用退出码区分失败类型：**参数错误退出码 `2`**，**状态/查询错误退出码 `1`**。脚本里可以据此分流：先查参数用法，再查运行状态。

## 五、结构化输出

配合 `--output-format`，无头模式可以输出机器可解析的结果。格式三选一：`text`（纯文本）、`json`（一次性结果对象）、`stream-json`（流式事件）。

```bash
reasonix run --output-format json "统计 src/ 下的 Go 文件数"
```

result 对象字段（节选自官方 CLI 参考）：

| 字段 | 含义 |
|------|------|
| `type` | 消息类型，结果为 `"result"` |
| `subtype` | 结果子类型 |
| `is_error` | 是否错误结果 |
| `duration_ms` | 耗时（毫秒） |
| `num_turns` | 完成所用轮数 |
| `result` | 最终答案文本 |
| `session_id` | 本次会话 ID |
| `total_cost` | 会话总成本 |
| `currency` | 货币（ISO 代码） |
| `total_cost_usd` | 美元计成本（同值不换算） |
| `usage` | token 用量：`input` / `output` / `cache_read_input` / `cache_creation_input` |

`--events-jsonl PATH` 把脱敏的生命周期遥测写入指定文件，用于观测事件流；它与 `--output-format` **互斥**，不能同时使用。`--trajectory PATH` / `--metrics PATH` 则分别输出事件流与指标。

> [!tip] 大白话
> `--output-format json` 像「让助手把交班报告写成表格而不是口头汇报」：耗时、轮数、成本、token 用量各占一格，机器直接读表，不用人肉解析一段自然语言。

## 六、常见坑

1. **`--auto` 不能与显式 `--permission-mode` 组合**。`--auto` 本身就是 `permission-mode auto` 的别名，再写一个 `--permission-mode` 属于重复指定，应二选一。
2. **`--events-jsonl` 不能与 `--output-format` 组合**。两者都试图接管输出通道，只能用一个。
3. **`--allowed-tools` 是权限覆盖，不是 schema 过滤**。它只决定「这次会话放行哪些工具」，不改变可用工具集合；且配置里的 `deny` 永远压过 CLI 的 `allow`。
4. **`--ablate` 是测量工具，不是调优开关**。它用于基准测量、禁用某个子系统来定位问题；禁用子系统只会让 Reasonix 更差，日常别开着它跑。
5. **废弃旧字段**：`agent.auto_plan`、`agent.max_steps` 及 MCP 旧字段会被忽略并在保存时移除，改用 `--max-steps`。
6. **版本差异**：v1 与 main-v2 的 CLI 文档命令列表不同，`--budget` 等参数仅在特定版本收录。遇到「命令不存在」，先跑应用内 `/help`、`/keys` 确认真实命令集。

> [!tip] 大白话
> `--ablate` 像「把机器拆下一个零件来跑测试」：目的是搞清楚哪个零件起了多大作用（测量），不是让机器跑得更好。天天拆零件跑生产，机器当然更差。

## 常见问题

**Q: `reasonix code` 和 `reasonix chat` 到底差在哪？**
A: 代码模式带文件系统与 shell，可读写项目文件、执行命令；聊天模式纯对话，刻意隔离文件系统与 shell，适合只聊方案不碰文件。

**Q: 脚本里怎么区分「参数写错了」和「运行出错了」？**
A: 看退出码：参数错误退出码 `2`，状态/查询错误退出码 `1`。

**Q: 为什么 `--auto` 和 `--permission-mode auto` 不能一起写？**
A: `--auto` 本身就是 `permission-mode auto` 的别名，两个都写属于重复指定同一件事，CLI 不允许组合。

**Q: 我想在 CI 里拿到 token 用量和成本，用哪个参数？**
A: 用 `--output-format json` 解析 result 对象里的 `usage` 与 `total_cost` / `total_cost_usd`；要完整生命周期遥测则用 `--events-jsonl PATH`（注意二者互斥）。

## 相关文档

- [[DeepSeek-Reasonix 使用指南]] — 安装、setup、第一个会话与日常速查
- [[DeepSeek-Reasonix 会话与交互]] — 会话模型、斜杠命令、快捷键
- [[DeepSeek-Reasonix 自动化与 CI]] — 无头模式与结构化输出接入 CI 流水线

## 参考资料

- 官方 CLI 参考：`v1/docs/CLI-REFERENCE.md`、`main-v2/docs/CLI.zh-CN.md`
- 官方仓库：https://github.com/esengine/DeepSeek-Reasonix
- 对齐 PR（命令与 Claude Code 对齐）：https://github.com/esengine/DeepSeek-Reasonix/pull/6431

## 更新记录

- 2026-08-10：初稿，基于官方 CLI 参考（v1 + main-v2）整理命令全集、启动参数、无头模式与结构化输出。
