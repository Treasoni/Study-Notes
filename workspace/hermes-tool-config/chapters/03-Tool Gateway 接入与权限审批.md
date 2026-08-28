# 第 3 章 Tool Gateway 接入与权限审批

前两章我们把 Hermes 的工具入口（config.yaml + `.env` + `hermes tools`）和内置 toolsets 摸清了：每个工具要么用你自己的直连 key，要么依赖某个后端。但一台机器要同时配 Firecrawl、FAL、Browser Use、OpenAI TTS……五六套账号，光是注册和充值就劝退不少人。这一章解决的就是这个问题：用 Nous Portal 的 Tool Gateway 一次 OAuth 把四类云能力聚合起来，再把「云能力 + 安全审批」一次装好。你会学会接入、校验、理解 selection key 的路由机制，以及如何配一套不会乱放行的审批体系。

## 3.1 Tool Gateway 是什么：一次 OAuth 聚合四类云后端

### 先分清两个「gateway」，这是本章最容易踩的概念坑

Hermes 文档里有两个都叫 gateway 的东西，名字像、本质完全无关：

| 维度 | Tool Gateway（本册主题） | 平台接入 gateway（《上手实战》第 6 章） |
| --- | --- | --- |
| 正式名称 | Nous Portal Tool Gateway | 消息平台网关（messaging gateway） |
| 配置入口 | `hermes setup --portal` / `hermes tools` | `hermes gateway setup` |
| 作用层 | **工具执行层**（tool-execution layer） | **会话入口层**（界面层） |
| 干的事 | 把 web 搜索/图像/TTS/云浏览器等工具调用路由到 Nous 托管的云端后端 | 把 Telegram / WhatsApp / Discord 等 IM 接进来，让用户能隔空对话 |
| 是否付费 | 是，Nous Portal 订阅 | 否 |
| 典型键 | `web.backend: nous` 这类 selection key | `TELEGRAM_ALLOWED_USERS`、`GATEWAY_ALLOWED_USERS` |
| 两者关系 | 与界面无关，CLI/Telegram/API 全都能用 | 只是接入渠道之一 |

一句话区分：**Tool Gateway 管的是「工具调用走谁家后端」，平台 gateway 管的是「用户从哪个聊天软件进来」**。文档里专门有一句 FAQ：Tool Gateway 作用于工具执行层、而非 CLI 层，所以 Telegram/Discord/API server 只要能调工具，都透明受益（来源 S3）。平台接入 gateway 的细节在 [[Hermes Agent 上手实战/06-多平台接入与定时任务]]，本册不展开；后面提到「网关」均指 Tool Gateway。

> [!tip] 大白话
> 把 Tool Gateway 想成一张**园区一卡通**：食堂（网页搜索/Firecrawl）、打印店（图像/FAL）、广播站（TTS）、网咖（云浏览器/Browser Use）都能刷这一张卡，不用分别去四家店办卡、充值、对账。所以一次 OAuth 登录 = 一个订阅 = 四类云能力全通。

### 4 + 1 类云后端

Tool Gateway 随每个付费 Nous Portal 订阅附带，聚合了四类后端（来源 S3、S7）：

| 工具 | 背后 partner | 你能拿到什么 |
| --- | --- | --- |
| Web 搜索 & 全文抓取 | Firecrawl | 代理级搜索 + 整页提取，不用自己的 Firecrawl key，也不用盯 rate limit |
| 图像生成 | FAL | 一个端点下 9 个模型（FLUX 2 Klein 9B / FLUX 2 Pro / Z-Image Turbo / Nano Banana Pro / GPT Image 1.5 / GPT Image 2 / Ideogram V3 / Recraft V4 Pro / Qwen Image） |
| 文本转语音 TTS | OpenAI TTS | `text_to_speech` 工具直接用，Telegram 语音回复、音频流水线都靠它 |
| 云浏览器自动化 | Browser Use | `browser_navigate` / `browser_click` / `browser_type` / `browser_vision` 全套，不需要 Browserbase 账号 |

外加一个**可选 add-on**：云终端沙箱（Modal，serverless shell 执行），不随默认包走，需要时用 `hermes setup terminal` 或 config.yaml 单独配。所以官方文档一处写「四类」、一处写「五类」，其实是 **4 + 1**，不是矛盾（来源 S3、S7）。

图像生成默认模型是 **FLUX 2 Klein 9B**（ID：`fal-ai/flux-2/klein/9b`），主打快、够用。要换别的模型不用改配置，调用 `image_generate` 工具时传对应模型 ID 即可覆盖，实时清单以 `hermes tools` → Image Generation 为准（来源 S3）。

### 网关不是锁定，是快捷键

Tool Gateway 是**按工具（per-tool）可选**的，不是全有或全无。你完全可以「网页搜索和图像走 Nous，TTS 用自己的 ElevenLabs key，浏览器用自己的 Browserbase」混搭（来源 S3、S7）。订阅过期时，走网关的工具会停摆并给出指向 Portal 的明确报错，此时要么续订、要么在 `hermes tools` 里切回直连 key（来源 S3）。`hermes portal open` 可以随时打开订阅管理页看各工具用量与账单。

## 3.2 实操：`hermes setup --portal` 完整接入

### 前置条件

- 已装好 Hermes（沿用《上手实战》第 2 章 Docker 场景），并已有 Nous Portal 账号（没有先去 portal.nousresearch.com/manage-subscription 订阅）。
- 本机有浏览器（OAuth 回调需要），或在远程机器上备好 SSH 端口转发（见 3.5）。

**你不需要准备任何第三方 key**——没有 OpenAI key、没有 Firecrawl 账号、没有 FAL key、没有 Browser Use 账号，这正是网关的意义（来源 S12）。

### 一条命令，五步走完

```bash
hermes setup --portal
```

这条命令内部做五件事（来源 S7、S12）：

1. 打开浏览器到 portal.nousresearch.com 走 OAuth 登录
2. 把 refresh token 存到 `~/.hermes/auth.json`（唯一落盘的凭据）
3. 在 `~/.hermes/config.yaml` 里设 `model.provider: nous`
4. 让你挑一个默认 agentic 模型（如 `anthropic/claude-sonnet-4.6`）
5. 打开 Tool Gateway（web / image / TTS / browser 四类路由）

跑完直接回终端，`hermes chat` 就能用。装完的 config.yaml 长这样（来源 S7）：

```yaml
# ~/.hermes/config.yaml
model:
  provider: nous                       # 推理走 Nous
  default: anthropic/claude-sonnet-4.6 # 或你挑的模型
  base_url: https://inference-api.nousresearch.com/v1
```

> [!tip] 大白话
> `hermes setup --portal` 像**一次性的「入学报到」**：先刷脸（OAuth 登录），领一张长期饭卡（refresh token 存 auth.json），然后系统自动把你所有食堂窗口（各工具）都开通了。所以之后每次吃饭（调工具）都不用再出示身份证明，刷卡（JWT）就行。

### 已在用别的 provider？`hermes model` 三条路都通

`hermes setup --portal` 是全新安装的一站式路径；已有 OpenRouter/Anthropic 配置的用户可以用 `hermes model` 在 provider 列表里挑 Nous Portal，浏览器登录后即可**并存**多个 provider，会话中随时 `/model` 切换（来源 S7）。选 Nous 模型时，Hermes 会弹出**网关工具的逐项清单**：

- 你已显式指向其他后端（如 `web.backend: searxng`）的工具**永远不会被勾选**，不会被误覆盖；
- 仅用 env 配置（如 `SEARXNG_URL`）的工具以**未勾选**状态出现，标注保留你自己的后端；
- 只有真正没配置过的工具默认**预勾选**；
- 清单里取消勾选的偏好会存进 `tool_gateway_declined_tools`，下次换 Nous 模型不会反悔。

（来源 S3）

`hermes tools` 则是**点菜式**路径：Nous-managed 后端（Web/Image/Video/TTS/Browser）即使你从未登录过 Portal 也恒在列表里，选中某行若未登录就当场内联拉起 Portal 登录——它只登录并开你点的那一个工具，**不会**切推理 provider，也**不会**提示全开（来源 S3、S7）。若你希望某个工具直连，同一行选 partner 名（如 `fal`、`firecrawl`）即可。

### 校验：`hermes portal tools` / `hermes portal info`

```bash
hermes portal info        # 登录状态 + 订阅 + 模型 + 网关路由概览
hermes portal tools       # 网关目录，per-tool 当前路由
hermes portal status      # portal info 的别名
hermes portal             # 无子命令 = hermes auth add nous --type oauth 的别名
```

接入成功后 `hermes portal info` 的输出，关键在最后几行**每行都应显示 "via Nous Portal"**（来源 S7、S12）：

```
  Nous Portal
  ───────────
  Auth:    ✓ logged in
  Portal:  https://portal.nousresearch.com
  Model:   ✓ using Nous as inference provider

  Tool Gateway
  ────────────
  Web search & extract  via Nous Portal
  Image generation      via Nous Portal
  Text-to-speech        via Nous Portal
  Browser automation    via Nous Portal
```

`hermes portal tools` 会显示 per-tool 路由：走订阅的显示 `via Nous Portal`，用你自己 key 的显示 partner 名（`firecrawl`、`browserbase` 等）。任何一行不是 "via Nous Portal" 而你又**确实想走网关**，回 `hermes tools` 把该工具改选 Nous Subscription 即可（来源 S12）。

> [!warning] 易错点
> 校验时看到 `Model: currently openrouter` 而不是 `using Nous as inference provider`，说明 OAuth 成功但 `model.provider` 漂移到别的 provider 了。修复：`hermes config set model.provider nous` 或 `hermes model` 重选 Nous Portal，再 `hermes portal info` 复核（来源 S12）。

## 3.3 selection key 机制：每个工具类别只有一个路由开关

### 五个 selection key

每个工具类别有**且仅有一个** provider 选择键，由 `hermes tools` 选择器（或桌面 GUI）写入 config.yaml。选 **Nous Subscription** 存的值是 `nous`；选直连（BYOK）行存的是 vendor 名（`fal`、`firecrawl`、`openai`、`browser-use`…）（来源 S3）：

```yaml
# ~/.hermes/config.yaml 中相关段落
web:
  backend: nous               # 网页搜索/提取 → Tool Gateway
image_gen:
  provider: nous              # 图像生成 → Tool Gateway
tts:
  provider: nous              # 文本转语音 → Tool Gateway
stt:
  provider: nous              # 语音转文本 → Tool Gateway
browser:
  cloud_provider: nous        # 云浏览器 → Tool Gateway
```

### 最重要的坑：runtime 恒用「存储的选择」，`.env` 直连 key 被忽略

这句话值得单独划重点：**凭据存在与否，永远不会选择或改道某个类别**。也就是说：

- `image_gen.provider: nous` 时，`.env` 里躺着的 `FAL_KEY` **被忽略**；
- 反过来，`image_gen.provider: fal` 但没设 `FAL_KEY`，会报一个清晰错误而**不会静默回退**到网关：

```
image_gen is configured to use fal (set via hermes tools), but FAL_KEY is not set. Run 'hermes tools' to change it.
```

（来源 S3、S7）

一旦某个类别写过 selection key，往 `.env` 加 key 不会改变路由——只有 `hermes tools`（或直接编辑该 key）才改。**从未配置过的类别**（selection key 从未写入）才按已有凭据自动探测，行为与旧版一致（来源 S3）。

> [!tip] 大白话
> selection key 像**铁轨上的道岔**：道岔指向哪条轨，火车就固定走哪条；轨道旁边堆着再多的备用车票（`.env` 直连 key）也没用，车不看你兜里有什么票。所以想换路线，只能去搬道岔（`hermes tools`），而不是往兜里再塞一张票。

> [!warning] 易错点
> 「我把 `FAL_KEY` 加进 `.env` 了，为什么图像还是不走我的 key？」——因为 `image_gen.provider` 仍是 `nous`，路由以存储选择为准。切回直连：`hermes tools` → Image Generation → 选 `fal`，你的 key 立刻重新生效。旧的 key 不用删，切走只是被忽略而已（来源 S3）。

### 旧的 `use_gateway: true` 已废弃

早期版本用每个工具一个 `use_gateway: true` 布尔值控制是否走网关。这个 flag **已 deprecated**（来源 S3、S7）：

- 官方**不再写入**它，`hermes tools` 重写某类别配置时会把它从该类别里移除；
- 旧配置里残留的 `use_gateway: true` 在**读取时等价于 `nous`**，老配置还能继续工作；
- 新配置**不要写** `use_gateway`，一律在 `hermes tools` 里选 provider。

另外，旧文档提过一个环境变量 `HERMES_ENABLE_NOUS_MANAGED_TOOLS`，但官方当前文档全文检索不到它，疑似也已废弃——**本处标注待核实**，一切以 `hermes doctor` 输出与当前官方 Tool Gateway 文档为准。

## 3.4 凭据与令牌生命周期：JWT、quarantine、重新登录

### refresh token → short-lived JWT

走网关后，`~/.hermes/auth.json` 里那个 refresh token 是磁盘上**唯一**的凭据。每次推理/工具调用，Hermes 都从它临时 mint 一个 short-lived JWT，而不是直接复用一把长期 API key。刷新、mint、对瞬时 401 自动重试全部自动，你全程看不到 token（来源 S7）。

> [!tip] 大白话
> refresh token 是**长期有效的门禁卡**（存 auth.json），JWT 是每次进门**现办的临时工牌**。工牌几分钟就作废、随处用也不怕被抄；门禁卡丢了才需要挂失重办。所以磁盘上只放一张卡，比散落十几把钥匙安全得多。

### 失效 → quarantine → re-authentication required

如果 Portal 使 refresh token 失效（改密码、手动 revoke、会话过期），Hermes 会把失效 token **本地隔离（quarantine）**，停止反复重放，避免刷出一连串 401；下一次调用会给出清晰的「**re-authentication required**」提示。此时重登一次即可：

```bash
hermes auth add nous
```

成功登录后隔离自动清除。如果想彻底清掉本地凭据重来：

```bash
hermes auth logout nous    # 抹掉本地 refresh token
```

（来源 S7、S12）

> [!warning] 易错点
> 会话中途看到 "re-authentication required"，不用重启容器、不用删配置文件——直接 `hermes auth add nous` 重新登录，下一次请求就用新凭据了。别去手改 `auth.json`，那是 OAuth 流程管理的文件。

### Profiles 与多用户

用 Hermes profiles 的话，Portal refresh token 通过共享 token store **自动跨 profile 共享**，登录一次所有 profile 生效；但每台机器上不同**人类用户**各占一个 home 目录、各持一份 `~/.hermes/auth.json`，互不共享——这是刻意保留的安全边界（来源 S7、S12）。

## 3.5 自托管网关与远程 OAuth

### 自托管网关的环境变量

如果你在跑一个自托管的 Nous 兼容网关（企业部署/开发环境），在 `~/.hermes/.env` 里覆盖端点（来源 S3）：

```bash
# ~/.hermes/.env
TOOL_GATEWAY_DOMAIN=your-domain.example.com   # 网关域名
TOOL_GATEWAY_SCHEME=https                     # http 或 https
TOOL_GATEWAY_USER_TOKEN=your-token            # 一般由 Portal 登录自动填充
FIRECRAWL_GATEWAY_URL=https://...             # 单独覆盖 Firecrawl 这一个端点
```

普通订阅用户**不需要**碰这些键——它们是给自定义基础设施准备的（来源 S3）。

### 远程 / 无头机器上的 OAuth

OAuth 需要浏览器，但回环回调跑在 Hermes 所在的机器上。SSH 进服务器、Cloud Shell、Codespaces、EC2 Instance Connect 等场景有两种办法（来源 S7、S12）：

```bash
# 方案 A：SSH 端口转发（推荐）——本地终端执行
ssh -N -L 8642:127.0.0.1:8642 user@remote-host

# 然后回到远程机器上
hermes setup --portal    # 把打印出的 URL 粘到本地浏览器打开

# 方案 B：device-code 登录——适合没有浏览器回环的环境
hermes auth add nous --type oauth
# 登录完成后重新跑 hermes setup --portal 把 provider + 网关接上
```

完整的 OAuth-over-SSH 指南还覆盖 ProxyJump 链、mosh/tmux、ControlMaster 的坑，详见官方 OAuth over SSH 文档（来源 S12）。

## 3.6 审批体系 approvals：把「危险命令」管起来

网关把云能力放开了，安全闸门就得跟上。Hermes 的审批体系围绕 `approvals` 配置块展开，工作方式如下。

### 三种模式：`smart`（默认）/ `manual` / `off`

```yaml
# ~/.hermes/config.yaml
approvals:
  mode: smart                     # smart | manual | off
  timeout: 300                    # 等待用户批复的秒数（默认 300）
  cron_mode: deny                 # cron 无人值守碰到危险命令：deny | approve
  single_query_mode: deny         # -q 单轮会话：deny | approve
  mcp_reload_confirm: true        # /reload-mcp 前确认（会失效 MCP 工具缓存）
  destructive_slash_confirm: true # /clear、/new、/reset、/undo 前确认
```

| 模式 | 行为 |
| --- | --- |
| **smart**（默认） | 用一个辅助 LLM 评估风险：低风险命令（如 `python -c "print('hello')"`）当次自动放行；真危险的命令自动拒绝；拿不准的升级为人工提示 |
| **manual** | 危险命令一律弹窗等你批准 |
| **off** | 关闭所有审批，等价于 `--yolo`，所有命令无提示执行——只建议在可信环境（CI/CD、容器）用 |

（来源 Sec）

> [!tip] 大白话
> `approvals.mode: smart` 像**分级安检**：普通行李（低风险命令）直接过；危险品（危险命令）拦下人工复核；而真·违禁品（hardline blocklist）是安检口永久拒收的黑名单，谁来了都不放行。所以默认配置下你能少打扰、又不至于裸奔。

### CLI 审批流：`[o]nce / [s]ession / [a]lways / [d]eny`

命中危险命令时，交互式 CLI 内联弹出审批，默认选 **deny**（来源 Sec）：

```
  ⚠️  DANGEROUS COMMAND: recursive delete

      rm -rf /tmp/old-project

      [o]nce  |  [s]ession  |  [a]lways  |  [d]eny

      Choice [o/s/a/D]:
```

- **once**：只放行这一次执行
- **session**：本次会话内放行该模式
- **always**：写入永久 allowlist（存到 config.yaml 的 `command_allowlist`）
- **deny**（默认）：拦截

`always` 会把模式存进 `~/.hermes/config.yaml`：

```yaml
# 永久放行的危险命令模式
command_allowlist:
  - systemctl
```

事后用 `hermes config edit` 审查/移除。还有个贴心命令 `hermes approvals suggest`：扫描历史批准记录（`~/.hermes/state.db`）把高频批准聚合为 allowlist 提案，默认只读、必须显式 `--apply 1,3` 才落盘，破坏性类别永远不进提案（来源 Sec）。

### 超时默认 fail-closed

危险命令弹出审批后，`approvals.timeout`（默认 **300 秒**）内没有回复，命令**默认被拒**——fail-closed，宁可放过不可放错（来源 Sec）。`cron_mode` 与 `single_query_mode` 默认都是 `deny`，保证无人值守场景下危险命令一律被挡。

### 消息平台批准/拒绝

在 Telegram/Discord 等消息平台上，agent 把危险命令详情发到聊天里等你在对话中回复：

- 批准：回复 `yes` / `y` / `approve` / `ok` / `go`
- 拒绝：回复 `no` / `n` / `deny` / `cancel`

网关运行时，Hermes 会自动设置 `HERMES_EXEC_ASK=1` 环境变量来启用这一流程（来源 Sec）。

### hardline blocklist：永不可覆盖的底线

有些命令后果不可逆（不可恢复的磁盘清空、fork bomb、直接写块设备），Hermes **拒绝执行**，且不受以下任何开关影响（来源 Sec）：

- `--yolo` / `/yolo` 打开
- `approvals.mode: off`
- cron 无人值守 `approve` 模式
- 用户明确点 "allow always"

这个列表（`tools/approval.py::UNRECOVERABLE_BLOCKLIST`）在审批层**之前**就触发，没有覆盖开关。典型模式：`rm -rf /` 及变体、`rm -rf --no-preserve-root /`、bash fork bomb（`:(){ :|:& };:`）、对挂载根设备 `mkfs.*`、`dd if=/dev/zero of=/dev/sd*`、把不可信 URL 管道给 rootfs 顶层的 `sh`。命中时工具调用会返回解释性错误、什么都不执行——如果你真的在跑「擦盘重装」流水线，去 agent 之外手动执行（来源 Sec）。

与 hardline 配套的用户侧武器是 `approvals.deny`：一串 glob 模式，**先于** `--yolo` / `/yolo` / `approvals.mode: off` 生效，用来实现「yolo-with-exceptions」（来源 Sec）：

```yaml
approvals:
  deny:
    - "git push --force*"    # 注意：模式一定要用引号包起来
    - "*curl*|*sh*"
    - "dd if=* of=/dev/*"
```

> [!warning] 易错点
> `approvals.deny` 的 YAML 模式**必须加引号**。裸开头的 `*` 是 YAML 别名会解析失败；`{`、`!`、`: ` 也各有 YAML 含义。shell 类内容单引号最稳。另外 deny 规则只作用于能触达主机的后端（local、SSH、host-mounted Docker），隔离容器后端根本不走这道守卫（来源 Sec）。

### 容器后端跳过危险命令检查

在 `docker` / `singularity` / `modal` / `daytona` / `vercel_sandbox` 后端里，**危险命令检查被跳过**——因为容器本身就是安全边界，容器里再危险的操作也伤不到宿主机（来源 Sec）。所以如果你用 `terminal.backend: docker`（第 2 章讲过「容器内的容器」），会发现 `approvals` 提示明显变少：这是设计使然，不是漏配。反过来，`local` 与 `ssh` 后端保留完整检查。

> [!warning] 与第 6 章的接驳
> `approvals.off` 与 YOLO 的三入口（`hermes --yolo`、会话内 `/yolo` toggle、`HERMES_YOLO_MODE=1`）会在第 6 章《Skills 与工具关系 · 安全基线》统一收束，那里还会给出 Docker 场景的完整安全检查清单。本章先把「审批怎么配」装好，第 6 章负责「整机怎么锁」。

## 本章小结

- **两个 gateway 不是一回事**：Tool Gateway（Nous Portal，聚合云工具后端，作用在工具执行层）vs 平台接入 gateway（`hermes gateway setup`，接 Telegram/WhatsApp 等 IM，作用在会话入口层）。
- **一次 OAuth 聚合 4+1 类云能力**：Web 搜索/Firecrawl、图像/FAL、TTS、云浏览器/Browser Use，外加可选 add-on 云终端/Modal；图像默认 FLUX 2 Klein 9B，per-call 传模型 ID 可覆盖。
- **`hermes setup --portal` 五步走**：OAuth → `auth.json` 落盘 → `model.provider: nous` → 默认模型 → 开网关；`hermes model` 可全开清单，`hermes tools` 逐工具点菜。
- **selection key 是唯一路由开关**：`web.backend` / `image_gen.provider` / `tts.provider` / `stt.provider` / `browser.cloud_provider`，选 Nous 存 `nous`；runtime 恒用存储选择，`.env` 直连 key 被忽略、缺 key 报错不静默回退。
- **凭据生命周期**：refresh token 存 `~/.hermes/auth.json`，每次调用 mint short-lived JWT；失效即 quarantine 并提示 re-authentication required，`hermes auth add nous` 重登；远程环境用 `ssh -L 8642` 端口转发或 `hermes auth add nous --type oauth`。
- **审批体系**：`approvals.mode` 三档（smart/manual/off）、CLI `[o]nce/[s]ession/[a]lways/[d]eny`、超时 300s fail-closed、消息平台 yes/no 回复、hardline blocklist 永不可覆盖、容器后端跳过危险命令检查。

下一章我们从「用现成工具」转向「造自己的工具」：先判断什么时候该写 skill、什么时候才值得写 tool，然后照抄一个最小注册模板，把自定义工具暴露到 `hermes tools` 里。
