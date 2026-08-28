# 第 2 章 内置工具与 toolsets 全解（terminal 后端与 Docker）

第 1 章我们建立了整体心智模型：tool 是「可执行能力」，配置入口分三层（config.yaml 行为 / `.env` 密钥 / `hermes tools` 运行时选择）。这一章我们把 Hermes 内置的约 86 个工具逐个类别过一遍，然后把最容易绕晕的 **terminal 后端** 与 **「容器内的容器」** 讲透，最后给你一份凭据速查表和输出截断配置，目标是让你能按自己的 Docker 场景把常用工具一次开齐。文中的配置键、命令与环境变量全部原样照抄，版本锚定 v0.20.x；不同版本若出现出入，一律以 `hermes doctor` 输出为准。

## 2.1 工具类别地图

Hermes 内置了约 **86 个工具**，可用性随平台、凭据、启用的 toolset 变化（来源 S2）。它们不是平铺的一堆函数，而是按**逻辑 toolset**（工具集）分组，方便你按平台整体开关。这 86 个的构成大致是：10 个 browser 核心工具 + 2 个 CDP 门控工具、4 个 file 工具、4 个 Home Assistant 工具、2 个 terminal 工具、11 个桌面 GUI 工具、2 个 web 工具、5 个飞书工具、7 个 Spotify 工具、5 个元宝工具、12 个 kanban 工具、3 个 project 工具、2 个 Discord 工具、3 个视频工具，外加一批独立工具（`memory`、`clarify`、`delegate_task`、`execute_code`、`cronjob`、`session_search`、`skill_view`/`skill_manage`/`skills_list`、`text_to_speech`、`image_generate`、`vision_analyze`、`video_analyze`、`todo`、`computer_use`、`x_search`）等（来源 S2）。

先看类别地图（来源 S1）：

| 类别 | 代表工具 | 干什么 |
|---|---|---|
| **Web** | `web_search`、`web_extract` | 搜索网页、抓取页面正文 |
| **X Search** | `x_search` | 搜 X(Twitter) 帖子与话题（opt-in，需 xAI 凭据）|
| **Terminal & Files** | `terminal`、`process`、`read_file`、`patch`、`write_file`、`search_files` | 执行命令、读写与修改文件 |
| **Browser** | `browser_navigate`、`browser_snapshot`、`browser_vision` 等 | 交互式浏览器自动化（文本 + 视觉）|
| **Media** | `vision_analyze`、`image_generate`、`text_to_speech` | 多模态分析与生成 |
| **Agent 编排** | `todo`、`clarify`、`execute_code`、`delegate_task` | 规划、澄清、代码执行、子代理委派 |
| **Memory & recall** | `memory`、`session_search` | 跨会话持久记忆与历史会话检索 |
| **Automation** | `cronjob` | 定时任务（create/list/update/pause/resume/run/remove）|
| **Integrations** | `ha_*`、MCP 服务器工具 | Home Assistant、MCP 等外部集成 |

> [!tip] 大白话：toolset 就是「工具箱里的抽屉」
> 把每个工具想成一把具体的工具——钳子、螺丝刀、电钻。toolset 是把相关工具收进同一格抽屉：`web` 抽屉里是 `web_search` 和 `web_extract`，`file` 抽屉里是 `read_file`/`write_file`/`patch`。`--toolsets "web,terminal"` 的意思就是「这次只带这两格抽屉出门」，其余工具即便注册了也不会被调用。

挑几个你几乎天天用的类别展开看（工具语义来源 S2）：

- **Web**：`web_search` 默认返回最多 5 条结果（title/URL/描述），可传 `limit`（1–100）；查询会透传给后端，所以 `site:`、`filetype:pdf`、`"exact phrase"` 这类操作符是否生效取决于后端支持。`web_extract` 把网页转成干净的 Markdown（不做 LLM 摘要，快），**直接支持 PDF URL**（arXiv 论文可直接传链接）；页面在 15000 字符预算内整体返回，更大的页面返回 head+tail 窗口并落盘，单次最多 5 个 URL。
- **Terminal & Files**：`terminal` 执行 shell 命令、文件系统在多次调用间保持；`background=true` 可跑长任务，配合 `process` 工具管理（list/poll/wait/log/kill/write）。文件侧官方反复强调：**别用** `cat`/`head`/`tail`（用 `read_file`）、别用 `grep`/`rg`/`find`（用 `search_files`）、别用 `sed`/`awk`（用 `patch`）、别用 `echo`/`cat heredoc`（用 `write_file`）。`patch` 用模糊匹配（9 种策略）做定点替换并返回 unified diff，小空白差异不会破坏它；`read_file` 带行号分页，超过约 100K 字符会在行边界截断并给 `next_offset`；`write_file` 是**整文件覆盖**，改单处用 `patch`。
- **Browser**：12 个工具里 10 个是核心，`browser_navigate` 必须先调用初始化会话，之后的 `browser_snapshot`（无障碍树 + ref ID）→ `browser_click`/`browser_type` 是标准链路；`browser_vision` 截图让模型看页面（处理 CAPTCHA、复杂布局）。另外 2 个（`browser_cdp`、`browser_dialog`）要 CDP 端点可达才注册，`browser_cdp` 是发原始 DevTools 协议命令的逃生舱。
- **Agent 编排**：`todo` 管会话内任务清单（3 步以上复杂任务用）；`clarify` 在拿不准时反问用户（单/多选、开放式三种模式，还能一次批量问 2–5 个问题）；`execute_code` 跑一段能程序化调用 Hermes 工具的 Python——当你需要 3 次以上工具调用且有中间处理逻辑、或要先过滤大输出再进上下文时用它；`delegate_task` 派生子代理（独立上下文、独立终端、只回最终摘要）。
- **Memory & recall**：`memory` 保存跨会话的持久信息（会话开始时出现在系统提示里）；`session_search` 在本地会话库做 FTS5 全文检索，直接返回 DB 里的真实消息，不调 LLM。
- **Automation**：`cronjob` 是统一定时任务管理器，支持 skill 背书的任务；cron 任务在**全新会话**里跑，没有当前聊天上下文。

**常用 toolset 清单**（来源 S1）：`web`、`search`、`terminal`、`file`、`browser`、`vision`、`image_gen`、`skills`、`tts`、`todo`、`memory`、`session_search`、`cronjob`、`code_execution`、`delegation`、`clarify`、`homeassistant`、`messaging`、`spotify`、`discord`、`discord_admin`、`debugging`、`safe`。每一项都能在 `hermes tools` 里看到并开关；不同平台预设会预装不同组合，最终以 `hermes tools` 的实际输出为准。

除了一类一类的内置 toolset，还有两类**动态生成**的 toolset：

- **平台预设 toolset**：例如 `hermes-cli`（命令行默认组合）、`hermes-telegram`（Telegram 平台组合）。平台预设决定「这个平台默认开哪些工具集」，`hermes tools` 交互界面就是按平台预设展示的（来源 S1）。
- **MCP 动态 toolset `mcp-<server>`**：接入一个 MCP 服务器后，只要它贡献了至少 1 个工具，就会生成一个运行时 toolset，名字形如 `mcp-github`，工具前缀统一是 `mcp__<server>__`（双下划线，如 `mcp__github__create_issue`）（来源 S2、S4）。第 5 章会专门讲 MCP。

**几个默认关闭、需要 opt-in 的工具集**，别指望它们一上来就在列表里：

- `x_search`：默认关闭，需在 `hermes tools` 里选 **🐦 X (Twitter) Search** 开启；且只有配了 xAI 凭据（`XAI_API_KEY` 或 xAI Grok OAuth / SuperGrok / Premium+ 登录）时 schema 才会注册（来源 S2）。
- `video` / `video_gen`：同样不是 `hermes-cli` 默认集。`video_analyze` 走 `--toolsets video`；`video_generate`、`xai_video_edit`、`xai_video_extend` 走 `--toolsets video_gen` 或在 `hermes tools` → Video Generation 里开（来源 S2）。

## 2.2 terminal 后端选择

`terminal` 是 Hermes 最重要的工具——它在「某个环境」里执行 shell 命令。这个「环境」就是 **terminal 后端**。Hermes 支持 7 种后端（来源 S1）：

| 后端 | 说明 | 适用场景 |
|---|---|---|
| `local` | 本机执行（**默认**）| 开发、可信任务 |
| `docker` | 隔离容器 | 安全、可复现 |
| `ssh` | 远程服务器 | 沙箱、让 agent 远离它自己的代码 |
| `singularity` | HPC 容器 | 集群计算、rootless |
| `modal` | 云端执行 | 无服务器、弹性扩展 |
| `daytona` | 云沙箱工作区 | 持久远程开发环境 |
| `vercel_sandbox` | Vercel Sandbox 云 microVM | 云执行 + 快照文件系统持久化 |

后端在 config.yaml 里通过 `terminal.backend` 选择，配套三个最常用键：

```yaml
# ~/.hermes/config.yaml
terminal:
  backend: local    # 或: docker, ssh, singularity, modal, daytona, vercel_sandbox
  cwd: "."          # 工作目录
  timeout: 180      # 单条命令超时（秒）
```

> [!tip] 大白话：terminal 后端就是「agent 的手伸到哪干活」
> `terminal` 工具本身只有一个（名字不变），变的只是命令跑在哪台机器上。`local` = 手就在你电脑上，直接动你的文件；`docker` = 手伸进一个隔离的集装箱，动不到你宿主机；`ssh` = 手伸到远程服务器。切后端只是换「干活地点」，`terminal`/`process`/`read_file` 这些工具名一个都不用改。

> [!warning] 非交互 shell 的坑：慢启动文件会让每条命令超时
> agent 跑命令用的是**非交互 shell**（没有 TTY、没人按回车）。`.bashrc`/`.zshrc` 里若有大段初始化（nvm、版本管理器）、会弹提示的块（`read`、`tmux attach`）或无条件打印横幅，就会让每一条 `git status` 都变慢甚至挂死。官方建议在 rc 文件顶部加标准守卫（来源 S1）：
> ```bash
> # ~/.bashrc —— 放在文件靠前位置
> case $- in
>   *i*) ;;                      # 交互式：继续往下
>   *) return ;;                 # 非交互：到此为止
> esac
> # 重/交互式初始化放在守卫下面
> ```
> 若你的终端里命令正常、agent 却一跑就超时，shell 初始化是第一排查对象。Zsh 用户把登录专属配置放 `.zprofile`、交互专属放 `.zshrc`、`.zshenv` 保持最小（它每个 shell 都跑）。

各后端还有各自的配置入口：ssh 的凭据写在 `~/.hermes/.env`（见 2.4）；singularity 用 `terminal.singularity_image`（SIF 文件，可 `apptainer build ~/python.sif docker://python:3.11-slim` 预构建）；modal 需要 `uv pip install modal` 并 `modal setup`；daytona 用 `DAYTONA_API_KEY` 与 `terminal.daytona_image`；vercel_sandbox 需要三个 token（`VERCEL_TOKEN`/`VERCEL_PROJECT_ID`/`VERCEL_TEAM_ID`）且 runtime 只能是 `node24`、`node22`、`python3.13`，`container_disk` 必须留默认 `51200`（来源 S1、S5）。

**背景进程管理**与 terminal 工具配套使用（来源 S1）：

```bash
# 起一个后台长任务，返回 {"session_id": "proc_abc123", "pid": 12345}
terminal(command="pytest -v tests/", background=true)

# 之后全部用 process 工具管理
process(action="list")                # 列出所有运行中进程
process(action="poll", session_id="proc_abc123")   # 查状态+新输出
process(action="wait", session_id="proc_abc123")   # 阻塞到结束
process(action="log", session_id="proc_abc123")    # 完整输出
process(action="kill", session_id="proc_abc123")   # 终止
process(action="write", session_id="proc_abc123", data="y")   # 发输入
```

`pty=true` 还能开 PTY 模式跑交互式 CLI（如 Codex、Claude Code）。需要 sudo 时会被要求输密码（会话内缓存），或在 `~/.hermes/.env` 里设 `SUDO_PASSWORD`。

## 2.3 Docker 后端：一个持久容器复用 terminal/file/execute_code

对 Docker 用户来说，这一节是本册最关键的一节。先记住一句话：**docker 后端 = 一个跨工具复用的持久容器**（来源 S1、S11）。

### 关键区分：宿主机跑 Hermes 容器 vs 容器内的容器

这是最容易绕晕的地方，拆开讲：

1. **宿主机跑 Hermes 容器**：你在宿主机上用 `docker run ... -v ~/.hermes:/opt/data` 跑起 Hermes 本体（《上手实战》第 2 章的做法）。此时 Hermes 进程住在容器 A 里，配置文件落在挂载的 `~/.hermes`。
2. **容器内的容器**：Hermes 里再设 `terminal.backend: docker`。这意味着 Hermes 的 `terminal`、`file`、`execute_code` 工具会再去 Docker daemon 拉起**第二个容器 B**，命令都在 B 里执行。B 才是 agent 干活的沙箱，A 只是 Hermes 程序的「壳」。

两者互不冲突，甚至可以叠加：你在容器 A 里跑 Hermes，A 内部再让 agent 起容器 B 干活，形成「套娃」。

> [!tip] 大白话：「容器内的容器」就是套娃
> 你已经用 Docker 把 Hermes 装进一个盒子里（容器 A），现在 `terminal.backend: docker` 是让 Hermes 再往盒子里开一个更小的盒子（容器 B），agent 的所有命令都在小盒子里跑。小盒子打砸了也不影响你宿主机，更不影响 Hermes 的配置文件——这就是「容器即边界」的由来。而且这个 B 不是每条命令开一个新的，它像「网吧包月卡」一样长期保留：这次装过的依赖、进过的目录，下次再来都还在。

### 持久容器语义与生命周期

docker 后端**不是**每条命令起一个新容器，而是**只起一个长命容器**（`docker run -d ... sleep infinity`），然后把每一条 `terminal`、每次 `file` 读写、每个 `execute_code` 都通过 `docker exec` 路由进同一个容器（来源 S1）。这意味着：

- `pip install foo` 装一次，整个会话、甚至跨 Hermes 进程重启都在；
- `cd /workspace/project` 之后，下一次 `ls` 看到的就是那个目录；
- 后台进程（npm watcher、dev server、长跑 pytest）跨工具调用存活；
- `/new`、`/reset`、`delegate_task` 子代理共享同一个容器（来源 S1、S11）。

默认情况下（`docker_persist_across_processes: true`），关闭会话时容器**不会被删除**，下次启动 Hermes 会通过容器标签（`hermes-agent=1`、`hermes-task-id`、`hermes-profile`）毫秒级重新挂上。容器只在 4 种情况下被真正 `docker rm -f`（来源 S11）：

| 触发条件 | 何时发生 |
|---|---|
| `docker_persist_across_processes: false` | 显式每进程隔离，每次 cleanup 都 stop + rm |
| 空闲回收（`lifetime_seconds`，默认 300s）| 仅非持久模式下；持久模式容器跳过空闲清扫 |
| 启动时孤儿回收 | 只清 **Exited** 的 hermes 容器（> 2×lifetime），跑着的一律不碰 |
| 手动操作 | `docker rm -f`、`docker system prune`、Docker Desktop 重启 |

### 配置：docker_image 与容器资源键

docker 后端的核心配置（来源 S1、S5、S11）：

```yaml
# ~/.hermes/config.yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"  # 默认镜像
  # 资源限制
  container_cpu: 1            # CPU 核数（默认 1，0 = 不限）
  container_memory: 5120      # 内存 MB（默认 5GB）
  container_disk: 51200       # 磁盘 MB（默认 50GB）
  container_persistent: true  # 持久化 /workspace 与 /root（默认 true）

  # 可选：显式转发宿主环境变量进容器（密钥别用 docker_env 字面量）
  docker_forward_env:
    - "GITHUB_TOKEN"
  # 可选：挂载宿主目录 host:container[:ro]
  docker_volumes:
    - "/home/user/projects:/workspace/projects"
```

几个要点：

- **默认镜像**是 `nikolaik/python-nodejs:python3.11-nodejs20`（来源 S5、S11）；文档示例有时用 `python:3.11-slim`，按需换即可。
- **`docker_forward_env` vs `docker_env`**：前者把宿主环境变量的**值**转发进容器（密钥不出现在配置文件里），后者在 config 里写死字面 `KEY=value`（静态开关用）。密钥务必用 `docker_forward_env`；skill 里声明了 `required_environment_variables` 的变量会自动转发，不需要你手动列（来源 S5、S11）。
- **`container_persistent: false`** 会切换成「每会话一个新容器」，会话结束即删，适合把沙箱当作会话间安全边界（来源 S11）。
- **profile 隔离**：容器标签带 `hermes-profile`，不同 profile 的容器互不可见、互不回收；若要让多个受信 profile 故意共用同一个容器，设置相同的 `docker_shared_container_key`（注意：先启动的 profile 的镜像/挂载设置生效，后来的 profile 直接挂上，不同设置被忽略）（来源 S11）。
- **容器安全加固**：所有容器后端都加 `--cap-drop ALL`（只加回 `DAC_OVERRIDE`/`CHOWN`/`FOWNER`）、`--security-opt no-new-privileges`、`--pids-limit 256`、`/tmp` 512MB 与 `/var/tmp` 256MB 的限容 tmpfs（来源 S1、Sec）。

> [!warning] 容器后端会跳过危险命令检查——容器即边界
> 当 terminal 后端是 `docker`/`singularity`/`modal`/`daytona`/`vercel_sandbox` 时，**危险命令审批会被跳过**，因为容器本身就是安全边界，容器里的破坏性命令伤不到宿主机（来源 Sec）。这意味着：切到 docker 后端后，`rm -rf` 之类命令不会再弹审批——它打砸的只是那个小盒子。这与第 6 章的安全基线（YOLO、hardline blocklist、approvals 模式）直接相关，第 6 章会给出 Docker 场景的完整安全检查清单。

## 2.4 凭据要求速查

工具「能不能注册成功」由 **check_fn** 门禁决定：凭据没配、插件没装、端点不可达，工具就不会出现在 `hermes tools` 里。下面按类给速查表，全部写到 `~/.hermes/.env`。

**Web 搜索**（`web_search` / `web_extract`，满足其一即可注册）（来源 S2、S5）：

| 凭据 | 说明 |
|---|---|
| `EXA_API_KEY` | Exa，AI 原生搜索与正文提取 |
| `PARALLEL_API_KEY` | Parallel.ai，AI 原生搜索 |
| `FIRECRAWL_API_KEY` | Firecrawl，抓取 + 云浏览器 |
| `TAVILY_API_KEY` | Tavily，可选；选 Tavily 为后端后无 key 也能用（keyless）|
| `BRAVE_SEARCH_API_KEY` | Brave Search，免费额度 |
| `SEARXNG_URL` | 自托管 SearXNG 地址，**免费无需 key** |

**图像生成**（`image_generate`，后端可选其一）（来源 S2）：

| 凭据 | 说明 |
|---|---|
| `FAL_KEY` | fal.ai |
| `OPENAI_API_KEY` | OpenAI |
| Codex OAuth | OpenAI Codex 登录 |
| xAI OAuth | xAI（Grok）登录 |
| `KREA_API_KEY` | Krea 2 |

**SSH 后端**（terminal.backend: ssh 时，写在 `~/.hermes/.env`）（来源 S1、S5）：

| 变量 | 说明 |
|---|---|
| `TERMINAL_SSH_HOST` | 远程主机名 |
| `TERMINAL_SSH_USER` | SSH 用户名 |
| `TERMINAL_SSH_KEY` | 私钥路径（如 `~/.ssh/id_rsa`）|
| `TERMINAL_SSH_PORT` | 端口（默认 22）|

**其它工具的注册条件**（check_fn 门禁，来源 S2）：

| 工具 | 注册条件 |
|---|---|
| `computer_use` | `cua-driver` 在 `$PATH`（用 `hermes tools` 安装）|
| `spotify_*` | 先跑一次 `hermes auth spotify`（OAuth）|
| `x_search` | `XAI_API_KEY` 或 xAI Grok OAuth（SuperGrok / Premium+）|
| `browser_cdp` / `browser_dialog` | 会话启动时有可用的 CDP 端点（`/browser connect`、`browser.cdp_url`、Browserbase、Camofox）|
| `video_generate` / `xai_video_edit` / `xai_video_extend` | 启用 video_gen 插件 + 对应凭据（`XAI_API_KEY` 或 `FAL_KEY`）|
| `discord` / `discord_admin` | `DISCORD_BOT_TOKEN`（+ 对应 bot 权限）|
| `feishu_doc` / `feishu_drive` | Feishu 应用凭据（且仅在飞书评论处理场景）|
| `kanban_*` | 被 kanban dispatcher 拉起（`HERMES_KANBAN_TASK`）或 profile 显式启用 `kanban` toolset |
| `desktop_ui` / `project` | 仅 Hermes 桌面应用会话 |

> [!tip] 大白话：check_fn 就是「门禁卡」
> 工具有没有资格出现在列表里，先看门禁卡刷不刷得过：`web_search` 的卡是「任意一个搜索 key」，`computer_use` 的卡是「装了 cua-driver」，`spotify` 的卡是「OAuth 授权过」。卡刷不过，工具就闷在注册表里不露面——不是坏了，是没给它开门。

**排错提示：`hermes tools` 不显示某工具，查三条件**（来源 S1、S2）：

1. **注册成功**——check_fn 门禁是否通过（凭据、插件、CDP 端点是否就绪）；
2. **会话权限**——所在 toolset 在当前平台是否已启用，且没被 `agent.disabled_toolsets` 或平台预设裁掉；
3. **任务确实需要**——有些工具即使注册并启用了，也只在具体任务里被模型真正调用，列表按平台/会话裁剪，显示与否不必然等于「能不能用」。

另外两个值得知道的工具结果行为（来源 S1）：一是 **信号死亡会被翻译成人话**——`-9`/`137` 变成「terminated by signal 9: SIGKILL —— 通常是内核 OOM killer 或显式 kill -9」，段错误、SIGTERM、管道断裂同理，排障时不用再猜数字；二是 **UTF-16 文本会被转码而非拒读**——`read_file` 能识别 Windows 记事本/PS 重定向产生的 UTF-16 并转成 UTF-8 展示，结果里带转换提示，编辑后会以 UTF-8 写回。

## 2.5 输出截断与溢出

工具输出是塞进模型上下文的，太大就会浪费 token 甚至爆窗。Hermes 用**两层机制**管这事：截断 + 溢出落盘（来源 S11）。

**输出截断三键**（config.yaml）：

```yaml
tool_output:
  max_bytes: 50000        # terminal 输出上限（字符）
  max_lines: 2000         # 单次 read_file 的分页上限
  max_line_length: 2000   # read_file 行号视图中每行字符上限
```

- `max_bytes`（默认 50000，约 12–15K token）：当一条 `terminal` 命令的 stdout+stderr 超过此值，Hermes 保留**前 40% + 后 60%**，中间插入一行 `[OUTPUT TRUNCATED]`。
- `max_lines` / `max_line_length`：限制 `read_file` 一次能读多少行、每行显示多长，防止单次读文件灌爆上下文。

大上下文模型可调高，小上下文模型调低（来源 S11）：

```yaml
# 大上下文模型（200K+）
tool_output:
  max_bytes: 150000
  max_lines: 5000

# 小本地模型（16K 上下文）
tool_output:
  max_bytes: 20000
  max_lines: 500
```

**溢出落盘（spillover）**：截断是「丢中间」，而超大的**工具结果**不丢，全量存盘。通用单结果溢出阈值是 **100,000 字符**，小上下文模型自动按比例下调。全量输出存到 `$HERMES_HOME/cache/spillover/`，上下文里只放「预览 + 文件路径」，你可以用 `read_file`（带 offset/limit）或 `execute_code` 再去取完整内容（来源 S11）。

MCP 工具的结果用更紧的独立阈值 **50,000 字符**（MCP 服务器常返回超大的未分页数据），可用 `tool_budget.mcp_result_size_chars` 覆盖：

```yaml
tool_budget:
  mcp_result_size_chars: 50000   # mcp_* 工具的溢出阈值
```

MCP 阈值总是被通用阈值封顶，所以调高它也不会超过当前模型窗口允许的范围。另外还有两点补丁性质的行为（来源 S11）：

- **provider 侧截断提示**：当 MCP 或 web 工具结果里自带截断标记（`...N more items`、`"has_more": true`、`saved to sandbox`），Hermes 会在结果末尾追加一行提示，提醒「看到的数据不完整，先分页/拉取再当作全量」。
- **结果引用 stub**：当同一条工具调用再次发出且返回字节级相同的重复结果时，重复载荷不再整段进上下文，而是变成指向先前结果的短引用（工具名、`tool_call_id`、参数摘要，必要时带 spillover 路径）。工具仍然每次真实执行，所以轮询语义不变。

> [!tip] 大白话：截断像「打印店预算」，落盘像「先存仓库」
> 长命令输出超预算了，打印店不会整份给你，只印前 40% 和后 60%，中间夹一张 `[OUTPUT TRUNCATED]` 纸条。而**超大结果**更聪明——不硬塞进你的上下文，而是把全文存进仓库（`cache/spillover/`），只给你一张「货单 + 仓库地址」，需要时再去取。什么都不丢，只是不占你桌面（上下文）。

## 2.6 行为与安全 env

一批影响工具行为的 env 写在 `~/.hermes/.env`（来源 S5）：

| 变量 | 默认 | 作用 |
|---|---|---|
| `HERMES_MAX_ITERATIONS` | `500` | 每次对话最大 tool-call 迭代次数（v0.20 起由 90 提至 500）|
| `HERMES_SAFE_MODE` | — | 排障模式：跳过插件发现、MCP 服务器加载、shell-hook 注册，等价 `--safe-mode` |
| `HERMES_WRITE_SAFE_ROOT` | 未设 | **硬拦** `write_file`/`patch` 写越界（不走审批、无提示），多目录用 `:` 分隔 |
| `HERMES_REDACT_SECRETS` | `true` | 在工具输出、日志、回复中打码密钥 |

其中 `HERMES_WRITE_SAFE_ROOT` 最容易被误用（来源 S5）：

- 官方 Docker 镜像会设 `HERMES_WRITE_SAFE_ROOT=/opt/data`（配合 `HERMES_HOME=/opt/data`），让 agent 跑不出挂载的数据卷；
- **别为了好玩把它加进 `~/.hermes/.env`**——一旦指向某个项目目录，agent 再想写 `~/.hermes/cron/jobs.json`、`~/.hermes/skills/` 或 profile 下的脚本，全部会报 `outside HERMES_WRITE_SAFE_ROOT`；
- 确实要既放行工作区又放行 Hermes 状态，就把两个前缀都列上：`HERMES_WRITE_SAFE_ROOT=/path/to/project:/home/you/.hermes`。

其余值得随手记的行为 env（来源 S5）：`HERMES_YOLO_MODE=1` 等价 `--yolo`（跳过危险命令审批，第 6 章展开）；`HERMES_DISABLE_FILE_STATE_GUARD=1` 关掉 `patch`/`write_file` 的「文件自上次读取后已变化」守卫；`DELEGATION_MAX_CONCURRENT_CHILDREN` 控制 `delegate_task` 批量并行的最大子代理数（默认 3）；`SUDO_PASSWORD` 让 sudo 免交互（在 `~/.hermes/.env` 里设，仅限可信环境）。

**全局禁用 toolset**：如果你想要一个「到处都关掉 X」的总开关，而不是去 `hermes tools` 里编辑十几个平台行，用 config.yaml 的 `agent.disabled_toolsets`（来源 S11）：

```yaml
agent:
  disabled_toolsets:
    - memory       # 隐藏 memory 工具 + MEMORY_GUIDANCE 注入
    - web          # 任何平台都没有 web_search / web_extract
```

它在平台预设（`platform_toolsets`）**之后**生效，所以哪怕某平台保存的配置里还列着 `web`，这里也会把它强制移除。留空或不写就是 no-op（来源 S11）。这也是第 6 章安全基线「全局禁用」的先导，第 6 章会展开它与 YOLO / hardline 的配合。

> [!warning] HERMES_SAFE_MODE 会关掉你的自定义能力
> 它叫「安全模式」其实更接近「排障模式」：一开就跳过插件、MCP、shell hook 全部加载。用它来二分定位「是不是我加的某个插件/服务器把启动搞挂的」，但别长期开着，否则 MCP 与插件能力全部消失（来源 S5）。

## 2.7 实操：把 terminal 切到 docker 后端并调容器资源

现在把你本机 Hermes 的干活地点从 `local` 切到 `docker`，并调好资源。假设 Hermes 已按《上手实战》第 2 章跑通。

**步骤 1：写配置**（两条命令等价于编辑 config.yaml）

```bash
hermes config set terminal.backend docker
hermes config set terminal.docker_image nikolaik/python-nodejs:python3.11-nodejs20
```

也可以直接编辑 `~/.hermes/config.yaml`，效果一样：

```yaml
# ~/.hermes/config.yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  container_cpu: 2            # 你本机核多就给 2 核
  container_memory: 8192      # 8GB
  container_disk: 51200       # 保持默认
  container_persistent: true  # 持久化，装一次依赖长期有效
  timeout: 180
```

**步骤 2：验证容器被拉起并打上标签**

```bash
hermes chat -q "echo hello from sandbox && python3 --version"
docker ps --filter label=hermes-agent=1
```

第一次工具调用时 Hermes 会 `docker run -d ... sleep infinity` 拉起容器；`docker ps` 应能看到打了 `hermes-agent=1` 等标签的容器。再次 `cd` 装依赖，跨命令、跨会话验证持久性：

```bash
hermes chat -q "pip install requests && pwd"
hermes chat -q "python3 -c 'import requests; print(requests.__version__)'"   # 第二次会话里还能 import
```

**步骤 3（可选）：显式转发一个 token 进容器**

```bash
hermes config set terminal.docker_forward_env '["GITHUB_TOKEN"]'
```

把 token 名写进 config，值仍留在宿主 `~/.hermes/.env`——这样容器里能用 `$GITHUB_TOKEN`，但配置文件里看不到明文。

> [!warning] 三个常见坑
> 1. **忘了 Docker daemon**：docker 后端要求 Docker Desktop / Docker Engine 在跑，Hermes 探测 `$PATH` 及常见 macOS 安装路径；两个都装了想用非默认的，用 `HERMES_DOCKER_BINARY=podman`（或完整路径）指定（来源 S5、S11）。
> 2. **切换后审批消失是正常的**：docker 后端会跳过危险命令检查（容器即边界，见 2.3），别以为配置坏了。
> 3. **`container_disk` 别乱调**：它要求 overlay2 + XFS 配额支持；Vercel Sandbox 后端更是明确不支持自定义磁盘大小，留默认 `51200` 即可（来源 S1、S11）。

---

## 本章小结

- 内置约 **86 个工具**按 toolset 分组，类别地图为 Web / X Search / Terminal&Files / Browser / Media / Agent 编排 / Memory / Automation / Integrations；另有平台预设 toolset（`hermes-cli` 等）与 MCP 动态 toolset `mcp-<server>`（工具前缀 `mcp__<server>__`）。
- **`x_search` 与 `video`/`video_gen` 是 opt-in 工具集**，默认不在 `hermes-cli` 集里；`x_search` 还需 xAI 凭据才会注册 schema。
- **terminal 后端**有 7 种（`local` 默认 / `docker` / `ssh` / `singularity` / `modal` / `daytona` / `vercel_sandbox`），配置键 `terminal.backend` / `cwd` / `timeout`；后台长任务用 `background=true` + `process` 工具管理。
- **docker 后端 = 一个持久容器**，跨 `terminal` / `file` / `execute_code` 复用（`docker exec` 进同一容器）；`container_persistent: false` 才切换为每会话一容器。默认镜像 `nikolaik/python-nodejs:python3.11-nodejs20`，资源键 `container_cpu` / `container_memory` / `container_disk` / `container_persistent`。
- **凭据写 `~/.hermes/.env`**：web 搜索（`EXA`/`PARALLEL`/`FIRECRAWL`/`TAVILY`/`BRAVE`/`SEARXNG`）、图像（`FAL`/`OPENAI`/Codex/xAI/`KREA`）、SSH（`TERMINAL_SSH_*`）；工具不显示按「注册成功 / 会话权限 / 任务确实需要」三条件排查。
- **输出管理两层**：`tool_output.max_bytes/max_lines/max_line_length` 负责截断（terminal 保留前 40% + 后 60%）；超大结果 spillover 落盘 `$HERMES_HOME/cache/spillover/`，MCP 用 `tool_budget.mcp_result_size_chars`（默认 50000）。全局禁用用 `agent.disabled_toolsets`。

**下一章预告**：你已经能按需把内置工具开齐，接下来要解决「云能力」——Nous Portal 的 Tool Gateway 一次 OAuth 聚合 web 搜索、图像、TTS、云浏览器，再配上 approvals 审批体系。第 3 章我们就接网关、配审批。
