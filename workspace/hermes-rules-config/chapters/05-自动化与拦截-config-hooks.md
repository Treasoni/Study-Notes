## 第五章 自动化与拦截 — 配置 config.yaml hooks

前几章搭好的 `SOUL.md`、`AGENTS.md`、`config.yaml` 权限块，本质都是"**静态告诉模型该怎么做**"——它们进入系统提示，靠模型自觉遵守。这一章要解决的是另一个问题：**当模型要执行某个工具、或某个回合要发给 LLM 时，怎么在进程层面用确定性代码拦截、改写或注入**。答案就是 hooks：在关键生命周期点运行自定义代码，做阻塞危险命令、自动格式化、注入上下文这类"规则文件管不到"的事。这一章以你在 Claude Code 里配过的 `settings.json` hooks 为对照锚点，把 Hermes 的 hook 体系讲透，重点是 `config.yaml` 里的 shell hooks——它和 Claude Code 的 hooks 是同源思路，还额外兼容 Claude Code 风格的返回 JSON。

### 5.1 四类 hook 系统总览（对照 Claude Code settings.json hooks）

先看地图。Hermes 不止一套 hook，而是**四套并存**，注册位置、运行范围、语言、能力各不相同[^c5-1]：

| 系统 | 注册位置 | 运行范围 | 语言 | 典型用途 | 能拦截工具 / 注入上下文？ |
| --- | --- | --- | --- | --- | --- |
| **Gateway Event Hooks** | `~/.hermes/hooks/<name>/` 下的 `HOOK.yaml` + `handler.py` | 仅 Gateway（Telegram/Discord/Slack/WhatsApp/Teams） | Python | 日志、告警、webhook、`BOOT.md` 启动清单 | 否 |
| **Plugin Hooks** | 插件 `register()` 里调 `ctx.register_hook("pre_tool_call", fn)` | CLI + Gateway | Python | 工具拦截、指标、护栏 | 是（`pre_tool_call` 可 block / modify） |
| **Shell Hooks** | `~/.hermes/config.yaml` 的 `hooks:` 块，指向 shell 脚本 | CLI + Gateway | 任意（Bash / Python / Go 二进制） | 阻塞危险命令、自动格式化、上下文注入 | 是（`pre_tool_call` 可 block / modify） |
| **Outbound Webhooks** | `~/.hermes/config.yaml` 的 `hooks.outbound:` 列表 | CLI + Gateway | 无（对外 HTTP POST） | 推送签名生命周期事件到 CI / 仪表盘 / 另一个 Hermes | 否（只观察，不改变流程） |

> [!tip] 大白话
> 把 hook 想成**过安检**：Gateway 钩子像"保安只在自己负责的那栋楼（Gateway）上班"；插件钩子和 shell 钩子是"全场巡逻的保安"，工具调用前都能把你拦下来检查；outbound webhook 则是"大楼门口的公告屏"，只对外广播消息，不管人。所以真要"拦工具"或"塞上下文"，认准**插件钩子**和**shell 钩子**这两类。

一个贯穿四类的总原则：**hook 回调出错会被隔离并记日志，不会让 agent 崩溃**。但"隔离"不等于"无害"——directive/control 类钩子能改变流程，transform 类钩子能替换内容，shell 的 `pre_tool_call` 钩子能 block 或 fail-closed[^c5-1]。

和 Claude Code `settings.json` hooks 对照，定位最准的锚点如下：

| Claude Code（settings.json） | Hermes | 说明 |
| --- | --- | --- |
| `hooks.PreToolUse` / `hooks.PostToolUse` | `pre_tool_call` / `post_tool_call` | 同一语义：工具执行前 / 后。事件名一个 PascalCase、一个 snake_case |
| `hooks.UserPromptSubmit` | `pre_llm_call` | 官方明确：`UserPromptSubmit` 不是 Hermes 的独立事件，`pre_llm_call` 在相同位置触发且已支持上下文注入[^c5-10] |
| matcher + command 数组 | `hooks.<event>` 列表里的 `matcher` + `command` | 同源思路：正则匹配工具，命中才跑脚本 |
| hook stdout 的 `{"decision": "block", "reason": ...}` | 直接照收，内部归一化 | S8 原文就叫 "Claude-Code style" |
| `failClosed` 拼写（Cursor/Claude Code 兼容） | `fail_closed` 同样接受 | 配置层兼容 |

> 对照要点：Claude Code 把 hook 都塞进 `settings.json` 一个 `hooks` 键；Hermes 拆成四套，各有各的注册方式和权限边界。**CLI 会话里真正可用的只有插件钩子和 shell 钩子**——Gateway 钩子只在 gateway 进程加载，你 `hermes chat` 跑 CLI 时它不会触发[^c5-2]。所以日常想拦命令、自动格式化，直接学 shell hooks 就够了。

### 5.2 shell hooks 配置 schema：`hooks.<event>` 与 matcher/command/timeout/fail_closed

shell hooks 是本章主角。**注册入口**在 CLI 启动（`hermes_cli/main.py`）和 gateway 启动（`gateway/run.py`）时调用 `agent.shell_hooks.register_from_config(cfg)`；它和 Python 插件钩子走同一个 dispatcher，天然共存[^c5-4]。完整 schema 如下[^c5-4]：

```yaml
# ~/.hermes/config.yaml
hooks:
  <event_name>:             # 必须是 VALID_HOOKS 之一（插件钩子事件全集）
    - matcher: "<regex>"             # 可选；仅 pre_tool_call / post_tool_call 使用
      command: "<shell command>"     # 必填；经 shlex.split 切分，shell=False 子进程运行
      timeout: <seconds>             # 可选；默认 60，上限 300（超出 clamp + warning）
      fail_closed: <bool>            # 可选；默认 false。仅 pre_tool_call 有效
      # `failClosed` 拼写同样接受（Cursor / Claude Code 兼容）

hooks_auto_accept: false   # 顶层；首次使用征询同意（见 5.3）
```

逐字段拆解：

| 字段 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- |
| `matcher` | 否 | 无（匹配全部） | 正则字符串，**仅 `pre_tool_call` / `post_tool_call` 使用**，用来匹配工具名（tool_name） |
| `command` | 是 | — | 用 `shlex.split` 切词、`shell=False` 起子进程——**不经过 shell 解释**，所以不要写 `|`、`&&`、`$(...)` 这类 shell 语法；缺 `command` 的条目直接 skip + warning |
| `timeout` | 否 | 60 秒 | 单个 shell hook 的独立超时；>300 被 clamp 并告警 |
| `fail_closed` | 否 | `false` | 只对 `pre_tool_call` 有意义；配到别的 event 上，config 解析时 warning 并忽略 |
| `hooks_auto_accept` | 顶层 | `false` | 首次使用征询同意开关（5.3 详述） |

校验行为（都有 warning，不崩）：

- 事件名必须是插件钩子事件全集里的一个，typo 会得到 "Did you mean X?" 提示并被跳过[^c5-4]。
- 单条 entry 里未知 key 被忽略；缺 `command` 是 skip-with-warning[^c5-4]。
- `timeout > 300` 被 clamp 并告警；`fail_closed: true` 用在非 `pre_tool_call` 事件上警告并忽略——因为**只有能 block 的事件才谈得上 fail-closed**（目前就是 `pre_tool_call`）[^c5-4][^c5-7]。

> [!warning] 不要写 shell 语法进 command
> `command` 是 `shlex.split` + `shell=False` 跑的，`|`、`&&`、`>`、`$(...)` 都不会被解释。你要写的逻辑请放进脚本文件（比如 `~/.hermes/agent-hooks/xxx.sh`），`command` 只写 `"~/.hermes/agent-hooks/xxx.sh"` 这一条调用。这和 Claude Code 的 `hooks.command` 传整条字符串的行为不同，刚迁过来的人最容易在这踩坑。

> [!tip] 大白话
> 把 `shell=False` 想成**去食堂打菜**：`shlex.split` 是"把你说的话按空格拆成一份菜名清单"（`["black", "a.py"]`），后厨严格按清单出菜；而 shell 解释是"把整句话抄给一个会自由发挥的大厨"（可能偷偷执行 `&&` 后面的命令）。Hermes 选前者，安全得多，代价是 command 里不能写管道。

### 5.3 `hooks_auto_accept: false` 与首次使用征询同意

shell hook 会以**你的完整用户凭据**执行（和 cron 条目、shell alias 同一信任边界），所以 Hermes 默认不让你悄悄跑任何脚本。机制是**首次使用征询同意**[^c5-8]：

- 每个唯一的 **`(event, command)` 对**第一次出现时，弹窗征询用户同意；
- 同意结果持久化到 `~/.hermes/shell-hooks-allowlist.json`；
- 之后的运行（CLI 或 gateway）不再询问。

> [!tip] 大白话
> 这就像**访客登记**：一个新脚本第一次进大门要登记（问一次"同意跑这个脚本吗"），登记在案之后，同一对 `(event, command)` 再来就直接刷脸进。注意登记的是"命令字符串"本身，不是脚本内容——脚本被改了也会照放行（见下）。

**三个逃生口，任意一个即可跳过交互式询问**[^c5-8]：

| 方式 | 写法 | 适用场景 |
| --- | --- | --- |
| CLI 参数 | `hermes --accept-hooks chat` | 交互式一次性放行 |
| 环境变量 | `HERMES_ACCEPT_HOOKS=1` | shell / CI 里批量放行 |
| config 开关 | `hooks_auto_accept: true` | 明确信任自己所有脚本，长期生效 |

**非 TTY 运行（gateway / cron / CI）必须三选一**——否则新加的 hook 会**静默地保持未注册**并打 warning，你的拦截/格式化/注入根本没生效，还不报错[^c5-8]。这是最容易"配了没反应"的坑之一。

**脚本编辑被静默信任**：allowlist 键在精确命令字符串上，不看脚本哈希，所以磁盘上改脚本不会作废同意。`hermes hooks doctor` 会标记 mtime 漂移，帮你发现"这个脚本被改过，要不要重新审视"[^c5-8]。

**手动 allowlisting**（非 TTY / 服务账号部署，无法交互应答时）——直接写 `~/.hermes/shell-hooks-allowlist.json`，格式是 `approvals` 数组，每条记录 `event` 和**精确的** `command` 字符串[^c5-8]：

```json
{
  "approvals": [
    {
      "event": "post_llm_call",
      "command": "/home/hermes/.hermes/hooks/my-hook.py"
    }
  ]
}
```

> [!warning] 手动 allowlist 的格式陷阱
> `command` 必须与配置里的命令字符串**逐字符一致**；文档明确警告：那种"以路径为 key、带 `sha256` 字段的对象"**不是**期望格式，不会批准成功。写完用 `hermes hooks list` 核对。另外 `revoke` 的生效要**下次重启**。

配套的 `hermes hooks` 命令族（S8 与 S7 两份文档都列了，合并如下）[^c5-9][^c5-13]：

| 命令 | 作用 |
| --- | --- |
| `hermes hooks list`（别名 `ls`） | 列出已配置 hooks：matcher、timeout、consent 状态；outbound 目标是否签名也会列出 |
| `hermes hooks test <event> [--for-tool X] [--payload-file F]` | 用合成 payload 触发所有匹配该 event 的 hook，打印**解析后**的返回（`parsed` 行就是 dispatcher 实际收到的 block 形状） |
| `hermes hooks revoke <command>`（别名 `remove`/`rm`） | 移除所有匹配 `<command>` 的 allowlist 条目（下次重启生效） |
| `hermes hooks doctor` | 逐个检查：exec 位、allowlist 状态、mtime 漂移、JSON 输出有效性、粗略执行耗时 |

### 5.4 `pre_tool_call` 实战：block / modify，JSON stdin→stdout，超时 fail-closed

`pre_tool_call` 在**每次工具执行前一刻**触发——内置工具和插件工具都算。模型一次并行调 3 个工具，它就触发 3 次。插件钩子的回调签名是 `def fn(tool_name, args, task_id, **kwargs)`[^c5-1]。

**JSON 线协议**：事件每次触发，Hermes 为每个匹配的 hook（matcher 允许时）起一个子进程，把 JSON payload 通过 **stdin** 喂进去，再从 **stdout** 读回 JSON。stdin 的形状是固定的[^c5-5]：

```json
{
  "hook_event_name": "pre_tool_call",
  "tool_name": "terminal",
  "tool_input": {"command": "rm -rf /"},
  "session_id": "sess_abc123",
  "cwd": "/home/user/project",
  "extra": {"task_id": "...", "tool_call_id": "..."}
}
```

- 非工具事件（`pre_llm_call`、`subagent_stop`、session 生命周期）时，`tool_name` 和 `tool_input` 为 `null`[^c5-5]。
- `extra` 字典携带该事件的全部事件专属 kwargs（`user_message`、`conversation_history`、`child_role`、`duration_ms`…）；不可序列化的值会字符串化而不是省略[^c5-5]。

**stdout 返回两种能力：block（需 message）与 modify（改写 tool_input）**：

```json
// block —— 需要非空 message
{"action": "block", "message": "Reason the tool call was blocked"}

// modify —— 改写工具参数，浅合并进原始 tool_input
{"action": "modify", "args": {"new_string": "fixed content"}}
```

语义细节（照 S8 原文）[^c5-1]：

- **block**：`block` 要求非空 `message`，命中后工具被短路，这段文字作为**返回给模型的错误**。多个回调时**第一个有效的 block 胜出**（Python 插件先注册、shell hooks 后注册，所以平局时 Python 的 block 优先）[^c5-11]。aggregator 一看到任何回调产出 `{"action":"block","message":非空}` 就返回。
- **approve**：`{"action":"approve","message":"...","rule_key":"可选:作用域"}` 会把调用升级到现有的人类审批门；`message`/`rule_key` 可省，且**拒绝、超时或门故障都 fail-closed**[^c5-1]。
- **modify**：返回的 `args` 字典会被**浅合并**进原始工具参数再执行。多个 modify 钩子会**累积**——每个钩子各改各的 key，都保留；若两个钩子改同一个 key，**后注册的赢**[^c5-1]。

**超时 fail-closed**：这是安全语义的核心。两个超时层要分清[^c5-1][^c5-4]：

| 层 | 默认值 | pre_tool_call 超时行为 |
| --- | --- | --- |
| Python 插件回调 | `plugins.hook_callback_timeout` 默认 30s（设 0 禁用，上限 600） | 超时或仍在上次超时后运行 → **fail-closed：阻塞工具**（不会在无策略决定的情况下放行） |
| shell hook 单条 entry | `timeout` 默认 60s（上限 300） | 默认 **fail-open**：warning 并放行；配 `fail_closed: true` 才阻塞（见 5.2 与下） |

**Exit code 2 = block（Claude Code / Cursor 兼容）**：`pre_tool_call` hook 以退出码 2 结束，即使 stdout 没有任何 block JSON，也会阻塞工具。block 消息按优先级解析：①stdout block JSON 的 `reason`/`message` → ②stderr 的前 400 字符 → ③兜底文案 `"Blocked by shell hook."`[^c5-6]。因此**最简单的阻塞钩子**是这样：

```bash
#!/usr/bin/env bash
echo "policy violation: rm -rf is not permitted" >&2
exit 2
```

对非 `pre_tool_call` 事件，exit 2 就当普通非零退出码处理：warning + 仍解析 stdout[^c5-6]。

**fail-open vs fail-closed 语义表**（shell hooks，S8 原文）[^c5-7]：

| 失败情形 | 默认 fail-open | `fail_closed: true` |
| --- | --- | --- |
| command 找不到 / 不可执行 | warning，放行 | **block** |
| 超时 | warning，放行 | **block** |
| stdout 不是合法 JSON（如 stack trace） | warning，放行 | **block** |
| 正常退出 + 合法 no-op JSON（`{}`） | 放行 | 放行 |

配了 `fail_closed: true` 的阻塞消息格式为 `hook <command> failed closed: <reason>`。**为什么默认是 fail-open**：对观测类 hook（记日志）这是对的默认值；但对安全闸门是错的——"崩溃的密钥扫描器不能静默放行它本该审查的工具调用"[^c5-7]。

```yaml
hooks:
  pre_tool_call:
    - matcher: "terminal|write_file|patch"
      command: "~/.hermes/agent-hooks/secret-scan.sh"
      timeout: 10
      fail_closed: true
```

> [!warning] 拦截用的钩子必须 fail-closed
> 凡是你当作"安全门"的 `pre_tool_call` 钩子，务必显式 `fail_closed: true`。脚本崩了、超时了、输出不是 JSON，都意味着"门坏了"——fail-open 默认值会让门直接敞开放行，等于白装。这是文档反复强调的安全语义。

### 5.5 Claude-Code 兼容双形状：`{"decision":"block","reason":...}` 与 `{"action":"block","message":...}`

从 Claude Code 迁过来最舒服的一点：**Hermes 的 shell hooks 直接收 Claude Code 风格返回，内部归一化**。同一意图两种写法都行[^c5-5][^c5-1]：

| 意图 | Hermes 规范（canonical） | Claude-Code 风格 |
| --- | --- | --- |
| block | `{"action": "block", "message": "..."}` | `{"decision": "block", "reason": "..."}` |
| modify | `{"action": "modify", "args": {...}}` | `{"decision": "modify", "tool_input": {...}}` |
| pre_llm_call 注入 | `{"context": "..."}` 或裸字符串 | 同左（`UserPromptSubmit` 无独立形状） |
| pre_verify 继续 | `{"action": "continue", "message": "..."}` | `{"decision": "block", "reason": "..."}`（阻止停下 = 继续） |

stdout 完整示例（可直接抄）[^c5-5]：

```json
// Block a pre_tool_call（两种形状都接受，内部归一化）：
{"decision": "block", "reason":  "Forbidden: rm -rf"}   // Claude-Code 风格
{"action":   "block", "message": "Forbidden: rm -rf"}   // Hermes 规范

// Modify a pre_tool_call —— 改写 tool args 后再分发：
{"action": "modify", "args": {"new_string": "fixed content"}}         // Hermes 规范
{"decision": "modify", "tool_input": {"new_string": "fixed content"}} // Claude-Code 风格

// Inject context for pre_llm_call：
{"context": "Today is Friday, 2026-04-17"}

// Keep the agent going at the verify gate（pre_verify，两种形状都接受）：
{"action": "continue", "message": "Run the formatter, then finish."}
{"decision": "block",  "reason":  "Run the formatter, then finish."}

// Silent no-op —— 任何空输出 / 不匹配的输出都行：
{}
```

归一化规则：`modify` 双形状最终都归一成 `{"action": "modify", "args": {...}}`[^c5-1]。`block` 双形状最终都归一成 `{"action": "block", "message": 非空}`。**malformed JSON、非零退出码、超时都只打 warning，永不中止 agent 主循环**[^c5-5]。

> [!tip] 大白话
> 这就像**写接口时兼容两套字段名**：前端发 `reason`、后端认 `message`，网关层把它们翻译成同一个内部对象。你把 Claude Code 的 hook 脚本原样搬过来，Hermes 也能读懂它的 `decision` / `reason` / `tool_input`——迁移成本几乎为零。

### 5.6 实战示例：拦截危险命令、自动格式化、`pre_llm_call` 注入上下文

最后给三个能直接落地的工作示例（全部出自 S8 原文），都遵循约定把脚本放在 `~/.hermes/agent-hooks/` 下，方便审计[^c5-10]。

**示例 1：拦截危险 `terminal` 命令**（`pre_tool_call` + matcher + timeout）——正则命中 `rm -rf /` 即输出 block JSON：

```yaml
# ~/.hermes/config.yaml
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "~/.hermes/agent-hooks/block-rm-rf.sh"
      timeout: 5
```

```bash
#!/usr/bin/env bash
# ~/.hermes/agent-hooks/block-rm-rf.sh
payload="$(cat -)"
cmd=$(echo "$payload" | jq -r '.tool_input.command // empty')
if echo "$cmd" | grep -qE 'rm[[:space:]]+-rf?[[:space:]]+/'; then
  printf '{"decision": "block", "reason": "blocked: rm -rf / is not permitted"}\n'
else
  printf '{}\n'
fi
```

要点：`matcher: "terminal"` 只对 terminal 工具触发；用 `jq` 从 stdin payload 里取 `tool_input.command`；非命中走 `{}` 无操作分支。想让脚本自身崩溃也不放行，把这条 entry 加上 `fail_closed: true`。

**示例 2：写文件后自动格式化 Python**（`post_tool_call` + matcher）——每次 `write_file` / `patch` 命中就调 black：

```yaml
# ~/.hermes/config.yaml
hooks:
  post_tool_call:
    - matcher: "write_file|patch"
      command: "~/.hermes/agent-hooks/auto-format.sh"
```

```bash
#!/usr/bin/env bash
# ~/.hermes/agent-hooks/auto-format.sh
payload="$(cat -)"
path=$(echo "$payload" | jq -r '.tool_input.path // empty')
if [[ "$path" == *.py ]] && command -v black >/dev/null 2>&1; then
  black "$path" 2>/dev/null
fi
printf '{}\n'
```

> [!warning] 格式化只改磁盘，不改模型已读到的内容
> 文档明确提醒：agent 在上下文中对该文件的视图**不会**自动重读——reformat 只影响磁盘文件，后续的 `read_file` 才会读到格式化后的版本。所以别指望这一发格式化能让模型"看见"自己的错误输出。

**示例 3：每回合注入 `git status` 上下文**（`pre_llm_call`，Claude-Code `UserPromptSubmit` 的等价物）——把未提交变更塞进用户消息，模型一开场就知道工作区脏不脏：

```yaml
# ~/.hermes/config.yaml
hooks:
  pre_llm_call:
    - command: "~/.hermes/agent-hooks/inject-cwd-context.sh"
```

```bash
#!/usr/bin/env bash
# ~/.hermes/agent-hooks/inject-cwd-context.sh
cat /dev/null   # 丢弃 stdin payload
if status=$(git status --porcelain 2>/dev/null) && [[ -n "$status" ]]; then
  jq --null-input --arg s "$status" \
    '{context: ("Uncommitted changes in cwd:\n" + $s)}'
else
  printf '{}\n'
fi
```

要点：`pre_llm_call` 的注入点**永远是用户消息，绝不进系统提示**——这是有意的设计，系统提示跨回合保持不变，prompt 缓存才能命中[^c5-1]。多个插件都返回 context 时，按插件目录名字母序用**双换行**拼接[^c5-1]。`matcher` 不用于 `pre_llm_call`，因为它是按工具匹配的，非工具事件直接不写 `matcher`。

**安全与优先级收尾**（这两条决定了你该多谨慎）：

- **信任边界**：shell hooks 用你的完整用户凭据运行，和 cron / shell alias 同级别。文档建议：只引用自己写或审过的脚本；脚本放 `~/.hermes/agent-hooks/` 方便审计；拉完共享配置先跑 `hermes hooks doctor`；团队共享 config.yaml 时，审 `hooks:` 段的 PR 要像审 CI 配置一样[^c5-11]。
- **优先级**：Python 插件钩子先于 shell hooks 注册，平局时 Python 的 block 决定优先；第一个有效 block 即返回[^c5-11]。想让某种策略绝对优先，用插件钩子而不是 shell 钩子。

**验证路径**（呼应第六章，先给三个最常用的）：

```bash
hermes hooks list                 # 看注册了哪些、consent 状态
hermes hooks test pre_tool_call --for-tool terminal   # 合成 payload 试跑，看 parsed block 形状
hermes hooks doctor               # 体检：exec 位 / allowlist / mtime 漂移 / JSON 有效性
```

> [!summary]
> - Hermes 有四套 hook：Gateway（仅 gateway）、Plugin、**Shell hooks（config.yaml `hooks:` 块，CLI+Gateway 可用）**、Outbound Webhooks。要拦截/注入就用 shell 或 plugin。
> - shell hook schema：`hooks.<event>: [{matcher, command, timeout(默认60/上限300), fail_closed(默认false，仅 pre_tool_call)}]`；`command` 走 `shlex.split` + `shell=False`，不经过 shell 解释。
> - JSON 线协议：payload 从 **stdin** 进、结果从 **stdout** 出；`pre_tool_call` 返回 block（需非空 message）或 modify（浅合并进 `tool_input`）；非工具事件 `tool_name`/`tool_input` 为 `null`。
> - `hooks_auto_accept: false` 时每个 `(event, command)` 对首次要征询同意，持久化到 `~/.hermes/shell-hooks-allowlist.json`；gateway/cron/CI 等非 TTY 环境必须用 `--accept-hooks` / `HERMES_ACCEPT_HOOKS=1` / `hooks_auto_accept: true` 三选一，否则新 hook 静默失效。
> - 兼容双形状：Claude-Code 的 `{"decision":"block","reason":...}`、`{"decision":"modify","tool_input":...}` 与 Hermes 的 `{"action":"block","message":...}`、`{"action":"modify","args":...}` 都被接受并内部归一化；exit code 2 也能 block（最简单阻塞钩子）。
> - 拦截型钩子务必 `fail_closed: true`；shell hooks 脚本用你的完整用户凭据运行，审 `hooks:` 段要像审 CI 配置。

**下一步**：hook 配好只是第一步——怎么确认它真的进了 dispatcher、返回形状对不对、在 `--safe-mode` 下会不会消失，需要一套验证命令。下一章 第六章 验证与排错 — 让规则确实生效，将用 `hermes doctor` / `hermes config check` / `hermes prompt-size` 把"配置 → 验证 → 对照 safe-mode"的完整回路走通。

[^c5-1]: [S8 Event Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — 四类 hook 系统总览、插件钩子目录、pre_tool_call 返回语义、pre_llm_call 注入位置与多插件拼接。
[^c5-2]: [S8 Event Hooks — Gateway Event Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — Gateway 钩子仅 gateway 加载、handler 规则、wildcard 匹配。
[^c5-3]: [S8 Event Hooks — Plugin Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — `ctx.register_hook()`、`plugins.hook_callback_timeout`（默认 30s，上限 600）、observer/transform/directive 分类。
[^c5-4]: [S8 Event Hooks — Shell Hooks 配置 schema](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — `hooks.<event>` schema、VALID_HOOKS 校验、timeout/fail_closed 语义、`shlex.split` + `shell=False`。
[^c5-5]: [S8 Event Hooks — JSON wire protocol](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — stdin payload 形状、stdout 返回示例、malformed 行为。
[^c5-6]: [S8 Event Hooks — Exit code 2 = block](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — Claude Code / Cursor 兼容的 exit 2 阻塞与消息优先级。
[^c5-7]: [S8 Event Hooks — Fail-open vs fail-closed](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — 默认 fail-open、fail_closed 反转、失败情形对照表、`hook <command> failed closed` 消息。
[^c5-8]: [S8 Event Hooks — Consent model](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — (event, command) 首次征询、allowlist 文件、三个逃生口、脚本编辑静默信任、手动 allowlist 格式。
[^c5-9]: [S8 Event Hooks — The hermes hooks CLI](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — list / test / revoke / doctor 命令说明。
[^c5-10]: [S8 Event Hooks — Worked examples](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — 自动格式化、拦截 rm -rf、git status 注入、subagent 日志四例；`UserPromptSubmit` 等价说明。
[^c5-11]: [S8 Event Hooks — Security / Ordering and precedence](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — 完整凭据信任边界、脚本路径约定、Python 插件先于 shell hooks 注册。
[^c5-12]: [S8 Event Hooks — Outbound Webhooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — `hooks.outbound:` 配置、HMAC 签名、交付语义（notify-only、一次重试、不跟随重定向）。
[^c5-13]: [S7 CLI Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md) — `hermes hooks` 子命令、`--safe-mode` / `--ignore-user-config` / `--ignore-rules` 隔离开关。
