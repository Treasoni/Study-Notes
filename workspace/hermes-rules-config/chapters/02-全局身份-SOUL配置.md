## 第二章 全局身份 — 配置 `~/.hermes/SOUL.md`

第一章把地图铺开了：Hermes 的指令载体分两类——全局 `SOUL.md`（身份）与项目上下文文件（项目知识）。这一章动手配置第一块拼图：全局身份 `~/.hermes/SOUL.md`。对照 Claude Code，这相当于把"全局指令"升级成"身份"——它不是追加一段规则，而是直接决定 **Hermes 是谁、怎么说话**。

### 2.1 位置与加载：只从 `$HERMES_HOME` 加载、不探测 CWD

**文件位置**（来自 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)）：

| 场景 | 路径 |
| --- | --- |
| 默认 | `~/.hermes/SOUL.md` |
| 自定义 home 目录 | `$HERMES_HOME/SOUL.md` |

**加载规则**（官方原文要点）：

- 只从当前实例的 `HERMES_HOME` 加载 `SOUL.md`，**不探测当前工作目录（CWD）**——你在哪个目录启动 Hermes，身份都一样
- 加载成功后内容进入系统提示**第 1 槽位（slot #1）**，**替换**掉内置硬编码默认身份
- `SOUL.md` 是真正的"每用户/每实例身份"，不是"附加规则层"

**为什么这么设计**（官方原话精神）：如果 `SOUL.md` 从"你恰好启动的目录"加载，换个项目人格就变了；只从 `HERMES_HOME` 加载，人格就属于 Hermes 实例本身，可预测。官方甚至把教学话术浓缩成一句：*"Edit `~/.hermes/SOUL.md` to change Hermes' default personality."*

> [!tip] 大白话
> 把 SOUL.md 想成**员工工牌**：你进哪个会议室（项目目录）都戴着同一张工牌；工牌只从 HR 系统（`HERMES_HOME`）发，不会因为换了会议室就换人。所以"你是谁"不随项目漂移——这正是它和项目上下文文件最根本的分工。

**对照 Claude Code**：

- Claude Code 的全局 `CLAUDE.md` 是"追加式"指令，且项目根 `CLAUDE.md` 会被主动发现
- Hermes 的 `SOUL.md` 是"替换式"身份：占据系统提示最前面的身份位，且**刻意不做 CWD 探测**
- 记忆口诀：Claude Code 的全局配置是"加规则"，Hermes 的 SOUL.md 是"换人格"

**动手确认**：先确认文件落点即可（验证命令族在第六章统一讲）：

```bash
ls -la ~/.hermes/SOUL.md
```

### 2.2 自动 seed 与"已有文件永不覆盖"的边界

三条行为规则（来自 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)）：

1. 如果 `SOUL.md` **不存在**，Hermes 自动创建一个 **starter** `SOUL.md`
2. 如果 **已存在**，**永不被覆盖**——升级、重装、重复启动都不会动它
3. 加载逻辑以"文件是否存在 + 是否可读"为分支（详见 2.4 的回退行为）

边界再划清楚一点：

- **seed 只发生在"文件缺失"时**；文件一旦存在，后续所有运行都不再写它
- **空文件 ≠ 会被覆盖**：文件仍在磁盘上，只是不会被当作身份注入（回退到内置默认身份，见 2.4）
- **想"恢复出厂"**：自己删掉文件，下次运行 Hermes 会重新 seed 一个默认的

> [!tip] 大白话
> "自动 seed + 永不覆盖"想成**保险箱**：Hermes 第一次见你没有保险箱，就放一个空的进去（starter）；之后你往里存什么它都不碰。升级只是"搬家"，不会顺手清空你的保险箱。

> [!note] 实战意义
> 这给了你一个很舒服的写配置节奏：直接编辑 `~/.hermes/SOUL.md`，反复保存都安全。如果哪天觉得"我的 SOUL.md 被重置了"，先排查两个更可能的原因：是不是自己删了文件？是不是在项目里建了个 `SOUL.md`（那个位置根本没被加载）？

### 2.3 该写什么：SOUL.md vs AGENTS.md 职责判断

这是官方文档里最强调的区分（*"This is the most important distinction"*），对照 Claude Code 的全局 vs 项目指令：

| 内容类型 | 该放哪 | Claude Code 对照 |
| --- | --- | --- |
| 身份 / 语气 / 风格 / 沟通默认 / 人格级行为 | **SOUL.md** | 全局 `CLAUDE.md` / 记忆 |
| 项目架构 / 编码约定 / 工具偏好 / 仓库特定工作流 / 命令·端口·路径·部署笔记 | **AGENTS.md** | 项目根 `CLAUDE.md` / `.claude/rules` |

**官方判断规则**就一句话：

- **跟随你到处走 → SOUL.md**
- **属于某个项目 → AGENTS.md**

**SOUL.md 里"少放"清单**（官方点名不要写的）：

- 一次性项目指令
- 文件路径
- 仓库约定
- 临时工作流细节

**好的 SOUL 文件特征**：跨上下文稳定；广到能适用很多对话；具体到能实质塑造声线；聚焦沟通与身份，而非任务指令。

**官方示例**（可直接照抄改成自己的，来源 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)）：

```markdown
# ~/.hermes/SOUL.md

# Personality

You are a pragmatic senior engineer with strong taste.
You optimize for truth, clarity, and usefulness over politeness theater.

## Style
- Be direct without being cold
- Prefer substance over filler
- Push back when something is a bad idea
- Admit uncertainty plainly
- Keep explanations compact unless depth is useful

## What to avoid
- Sycophancy
- Hype language
- Repeating the user's framing if it's wrong
- Overexplaining obvious things

## Technical posture
- Prefer simple systems over clever systems
- Care about operational reality, not idealized architecture
- Treat edge cases as part of the design, not cleanup
```

> [!tip] 大白话
> 把这两份文件想成**人设 vs 岗位说明书**：SOUL.md 是"你雇的这个人性格怎样、说话什么风格"；AGENTS.md 是"在这个项目里该干哪些活、走哪条流程"。人设跟着人走，说明书跟着岗位（项目）走。

### 2.4 内容约束：注入安全扫描、截断、空文件回退

**注入方式**：`SOUL.md` 内容**原样（verbatim）注入**系统提示第 1 槽位，不套任何 wrapper 文案（[Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)）。但这不代表能随便写——注入前要过两关。

**第一关：注入安全扫描（prompt-injection scanning）**。`SOUL.md` 与其他上下文文件一样，注入前被扫描提示注入模式（[Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly) 明确列出：不可见 Unicode、"忽略之前的指令"、凭据外泄尝试等）。官方特意提示：**别试图往 SOUL.md 里夹带奇怪的元指令**，把它保持为纯 persona/声线。

> [!warning] 素材边界（按深度素材"四、矛盾点"处理）
> `[BLOCKED: ...]` 的"命中即不加载"行为，官方文档是明确写给**项目上下文文件**的（第三章展开）；SOUL.md 文档只强调"扫描后原样注入"。本章按"同样走扫描、命中行为以第三章 context-files 为准"处理，不做超出素材的断言。深度素材第三、四条差异（override 位置、AGENTS.md 发现范围）与本 SOUL.md 章节无冲突。

**第二关：截断（truncation）**。`load_soul_md()` 的加载逻辑（来自 [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly) 的 `agent/prompt_builder.py` 简化版）长这样：

```python
# agent/prompt_builder.py (simplified)

def load_soul_md() -> Optional[str]:
    soul_path = get_hermes_home() / "SOUL.md"
    if not soul_path.exists():
        return None
    content = soul_path.read_text(encoding="utf-8").strip()
    content = _scan_context_content(content, "SOUL.md")   # Security scan
    content = _truncate_content(content, "SOUL.md")       # Cap scales with model context window (20k floor); config override wins
    return content
```

截断规则（与项目上下文文件同一套机制，[Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)）：

| 规则 | 取值 |
| --- | --- |
| 上限键 | `context_file_max_chars`，在 `config.yaml` 里**显式设置始终优先** |
| 未设置时 | 随模型上下文窗口**动态缩放**：下限 **20,000** 字符、上限 **500K** 字符 |
| 截断方式 | **70/20 头/尾保留** + 截断标记（保留头部 70%、尾部 20%，中间以标记代替） |

**空文件回退**：文件不存在、为空、纯空白、或读取失败 → 回退到**内置默认身份**（"You are Hermes Agent, an intelligent AI assistant created by Nous Research..."）。`skip_context_files` 场景（如 subagent/委派）同样回退。`load_soul_md()` 返回内容后，会替换硬编码的 `DEFAULT_AGENT_IDENTITY`。

**不重复注入**：`SOUL.md` 只在系统提示中出现**一次**（身份槽位），不会在项目上下文文件区重复出现——`build_context_files_prompt(skip_soul=True)` 显式防止重复。

> [!tip] 大白话
> 截断想成**装行李箱**：箱子（上下文窗口）装不下，就把长文案的头尾（70/20）保留、中间砍掉并留个"此处已截断"标记。所以别把 SOUL.md 写成一本小说——它站在系统提示最前面（stable 层），越精简越省 token、越利于提示缓存。

### 2.5 personality 预设与自定义 personalities

**SOUL.md vs `/personality`**（来自 [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)）：

- `SOUL.md` = **持久默认人格**（baseline voice）
- `/personality` = **会话级覆盖层**（temporary mode switch）——临时改/补当前系统提示，**不动 SOUL.md 文件**

官方给的典型用法：

- 默认 SOUL 保持务实，教课/辅导时 `/personality teacher`
- 默认 SOUL 保持简洁，头脑风暴时 `/personality creative`

**内置 personality 预设**（`/personality` 可切换，全平台可用）：

| Name | Description |
| --- | --- |
| helpful | Friendly, general-purpose assistant |
| concise | Brief, to-the-point responses |
| technical | Detailed, accurate technical expert |
| creative | Innovative, outside-the-box thinking |
| teacher | Patient educator with clear examples |
| kawaii | Cute expressions, sparkles, and enthusiasm ★ |
| catgirl | Neko-chan with cat-like expressions, nya~ |
| pirate | Captain Hermes, tech-savvy buccaneer |
| shakespeare | Bardic prose with dramatic flair |
| surfer | Totally chill bro vibes |
| noir | Hard-boiled detective narration |
| uwu | Maximum cute with uwu-speak |
| philosopher | Deep contemplation on every query |
| hype | MAXIMUM ENERGY AND ENTHUSIASM!!! |

**命令**（CLI 与消息平台通用）：

```
/personality          # 无参数：列出可用预设 + 标记当前激活项
/personality concise
/personality teacher
/personality none      # 清除激活的覆盖，回到 SOUL.md 基线（next message 生效）
/personality default   # 同上（none / default / neutral 三个等价）
/personality neutral
```

**自定义 personalities**：在 `~/.hermes/config.yaml` 的 `agent.personalities` 下加你自己的预设（或复用内置名来覆盖它）：

```yaml
# ~/.hermes/config.yaml
agent:
  personalities:
    codereviewer: |
      You are a meticulous code reviewer. Identify bugs, security issues,
      performance concerns, and unclear design choices. Be precise and constructive.
```

然后切换：

```
/personality codereviewer
```

**两个容易搞混的点**（官方明确区分）：

- 选择结果以**名字**存在 `display.personality`；personalities **永不触碰** `agent.system_prompt`
- `agent.system_prompt` 是"你自己手写一份系统提示"的保留通道，**只在没有任何 personality 被选中时生效**
- 会话级覆盖在**下一条消息**生效
- **升级注意**：旧版本在各平台保存人格状态不一致；升级后首次运行会把已保存的 personality **一次性重置为 `none`**（迁移日志会打印清掉了哪个），想要就 `/personality <name>` 重新启用。手动 `agent.system_prompt` 永不被触碰

> [!tip] 大白话
> 把 SOUL.md 想成**手机默认主题**，`/personality` 想成**临时换肤**——换皮肤不改系统，关掉（`none`）就回到默认主题。而 `agent.system_prompt` 是"你自己重写系统"的保留通道，选了皮肤时它不生效。

**推荐配置组合**（官方 Recommended workflow）：

1. `~/.hermes/SOUL.md` 写一个深思过的全局人设
2. 项目指令放 `AGENTS.md`
3. 只在需要临时切模式时用 `/personality`

> [!summary] 本章小结
> - `SOUL.md` 是 Hermes 的**全局身份**：只在 `$HERMES_HOME` 加载、不探测 CWD，占据系统提示第 1 槽位、替换内置默认身份——"身份不随项目漂移"。
> - 文件缺失时 Hermes **自动 seed** 一个 starter；已存在则**永不覆盖**；想重置就自己删文件。
> - 职责判断一句话：**跟随你到处走 → SOUL.md；属于某个项目 → AGENTS.md**。SOUL.md 放语气/风格/沟通默认，别放路径、仓库约定、一次性指令。
> - 注入前过两道关：**注入安全扫描** + **截断**（`context_file_max_chars` 优先，否则随模型窗口 20k~500k，70/20 头尾保留）；空/空白/读取失败回退内置默认身份，且只注入一次。
> - `/personality` 是会话级临时覆盖：内置十余种预设，也可在 `config.yaml` 的 `agent.personalities` 自定义；它不动 SOUL.md，也不碰 `agent.system_prompt`。

**下一步**：全局身份配好了，接下来第三章配**项目规则**——项目上下文文件（AGENTS.md 系列）的优先级链、目录链合并与渐进发现。这两层合起来，就是 Hermes 的"全局 + 项目"完整规则骨架。
