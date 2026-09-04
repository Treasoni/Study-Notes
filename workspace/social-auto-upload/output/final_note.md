---
title: social-auto-upload 配置与使用指南
tags: [教程, 自动化, social-auto-upload, CLI, GitHub项目]
created: 2026-09-05
updated: 2026-09-05
status: 完成
source_project: social-auto-upload
---

# social-auto-upload 配置与使用指南

这是一份围绕 GitHub 开源项目 social-auto-upload 的实战笔记，覆盖从项目定位、环境安装、`sau` CLI 发布第一条抖音、全平台命令参考、登录态与 Cookie 机制，到常见坑与排错的全流程。读者定位为零基础到有了解的配置使用者，深度为「快速上手（部署 + 跑通）」。全文一律以 **uv + patchright + `sau` CLI** 的当前主线为准，仓库里的旧 Web 版与多数第三方教程仅作对照，请勿照搬旧命令与旧配置。

## 目录

1. [第 1 章 项目简介与能做什么](#第-1-章-项目简介与能做什么)
2. [第 2 章 环境要求与安装](#第-2-章-环境要求与安装)
3. [第 3 章 快速跑通：配置 conf.py 并发布第一条抖音视频](#第-3-章-快速跑通配置-conf-py-并发布第一条抖音视频)
4. [第 4 章 平台能力矩阵与 CLI 命令参考](#第-4-章-平台能力矩阵与-cli-命令参考)
5. [第 5 章 登录态与 Cookie 机制](#第-5-章-登录态与-cookie-机制)
6. [第 6 章 常见坑与排错](#第-6-章-常见坑与排错)
7. [第 7 章 结语：版本口径与下一步](#第-7-章-结语版本口径与下一步)

---

## 第 1 章 项目简介与能做什么

如果你要把同一条视频分别发到抖音、B 站、小红书，每个平台都要打开网页、登录、填标题、等上传，做几次就会发现这是纯粹的重复劳动。本章先用最短篇幅讲清 social-auto-upload 是什么、靠什么原理省事、覆盖哪些平台，并点出读后续章节前必须知道的一条「版本口径」。

### 1.1 项目定位与工作原理

social-auto-upload 是一个开源「多平台内容自动上传」工具：把「逐个打开网页做分发」的高频重复劳动，固化成 **Python 脚本 + 浏览器自动化**。核心能力：**视频上传、图文上传、定时发布**。

运行机制要先记住：它不是调用各平台公开 API 直传，而是基于 **patchright 驱动浏览器，像真人一样登录并操作各平台上传页**；登录态以 Cookie 文件保存，账号模型是「一个账号名 = 一个账号文件」。所以它能自动分发，但绕不开平台自身的登录与风控。

> [!note] 一句话理解
> 它不是各平台官方接口的聚合器，而是「一个会自动操作浏览器的脚本，替你去上传」——你手工点开 N 个网页做的事，它照着脚本自动做一遍。

> [!tip] 大白话
> 把 Cookie 登录态想成小区门禁卡：第一次你亲自去物业登记（扫码 / 短信登录）领卡，之后脚本代你进门只刷卡、不用重新登记。前提是卡本身有效——所以它是替「已登录好的你」干活，而不是绕过平台。

项目现状：约 **14.8k star / 2.5k fork，MIT 协议**（调研缓存值，以仓库实时为准）。2026-03 作者回归后大重构：统一为 CLI 入口 **`sau`**，浏览器驱动从 playwright 迁到 **patchright**，主线默认 **headless（无头）** 运行。本笔记的命令与配置全部基于这套新主线（[仓库主页](https://github.com/dreammis/social-auto-upload)）。

### 1.2 支持平台一览与版本口径提醒

项目覆盖 **11 个平台**，其中 **10 个已接入 `sau` CLI**：抖音、Bilibili、小红书、快手、视频号、百家号、支付宝生活号、微博、虎扑、YouTube（YouTube 按 [docs/CLI.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/CLI.md) 判定已接入，README 行文有遗漏，以最新代码为准）。**TikTok 尚未接入 CLI**，只能走历史遗留的 Chrome example。各平台「支持视频 / 图文 / 定时发布」的能力差异，留到第 4 章用矩阵表展开。

> [!warning] 版本口径提醒
> 2026 年这次重构变动很大：本笔记一律以 **README + docs/install.md + docs/CLI.md** 的当前主线（uv + patchright + `sau` CLI）为准。你搜到的大多数第三方教程，以及仓库里的旧 Web 版（legacy-web）、requirements.txt，基本停留在 pip + playwright + Web 版旧时代，命令和配置已对不上，只能当对照看。

### 本章小结

- social-auto-upload 把「多平台手工分发」固化为 Python 脚本 + 浏览器自动化的自动上传工具。
- 核心能力：视频上传、图文上传、定时发布。
- 运行机制：patchright 浏览器自动化 + Cookie 登录态，而非公开 API 直传。
- 覆盖 11 个平台，10 个已接入 `sau` CLI；TikTok 走历史 Chrome example、未接入 CLI。
- 读后续章节请认准 CLI 重构主线，旧 Web 版 / 第三方教程仅作对照。

下一章进入动手环节：讲清跑这个项目需要哪些环境（Python 版本、浏览器驱动等），并按当前主线一步步把 `sau` 装起来。

---

## 第 2 章 环境要求与安装

上一章确认了项目能做什么，这一章进入动手环节：先把「能跑起来」的环境配好。环境只有几样硬性要求，真正要敲的命令也就七八条；装完用 `sau --help` 自检一下，环境就算就绪。文末我会专门用一张表讲清新旧安装路径的差别，防止你在网上搜到的旧教程里走错门。

### 2.1 环境硬性要求

**Python 版本：`>=3.10,<3.13`**

项目的 [pyproject.toml](https://github.com/dreammis/social-auto-upload/blob/main/pyproject.toml) 明确锁定 Python `>=3.10,<3.13`，即 3.10 / 3.11 / 3.12 可用，**3.13 不可用**（依赖/驱动尚未跟上）。动手前先 `python --version` 确认一下。

> [!tip] 大白话
> 把 Python 版本范围想成小区门禁只认 3.10 / 3.11 / 3.12 三档卡，拿 3.13 的新卡暂时刷不进去。所以先看版本号，不在范围内就装对应版本，别等装到一半报错再回头。

**包管理：uv（官方推荐主线）**

项目推荐用 uv 而不是裸 pip：uv 同时承担「建虚拟环境 + 装依赖 + 注册命令」三件事，比 pip + venv 手动组合省事。如果本机还没装 uv，先去 uv 官方文档装好（`uv --version` 能出号即可），这一步与项目本身无关，属于前置工具。

> [!tip] 大白话
> 把 `uv venv` 想成给项目开一间独立工位：所有依赖都装在自己工位上，不跟系统里其他 Python 项目混放。所以同时装好几个项目互不污染，哪天删掉这个目录也不会弄脏全局环境。

**浏览器驱动：patchright chromium（需单独下载）**

项目用 patchright 驱动浏览器执行上传（第 1 章提过，驱动从 playwright 迁到了 patchright）。所以光装 Python 包不够，还得额外下载它自带的 chromium 内核：

```bash
patchright install chromium
```

国内网络下载慢或失败时，先设镜像再跑。注意：这个环境变量的名字**仍然是 `PLAYWRIGHT_DOWNLOAD_HOST`**，因为 patchright 复用了 playwright 的下载设施（[docs/install.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/install.md)）——照原样用即可，别自作主张改成 `PATCHRIGHT_` 前缀。

> [!tip] 大白话
> 把 npmmirror 镜像想成国内「自提点」：chromium 本来要从官方仓库跨国取货，容易超时或断线；镜像站点先把货备到国内，你本地去取就快多了。变量名带不带 PLAYWRIGHT 只是门牌号沿用，你把它改成别的名字反而取不到货。

**biliup：B 站专属，无需手动安装**

biliup 只在用到 B 站时才会介入：首次运行会自动下载对应二进制，之后会自动检查上游更新，全程不用你手动装。

**系统：Windows / Linux / macOS 均覆盖**

安装命令分 PowerShell（Windows）与 bash（Linux/macOS）两套写法，见 2.2。

### 2.2 安装步骤（uv 主线）

下面两条命令块是完整安装序列，先整体看一遍（先睹为快）：**Windows 用户整段复制 PowerShell 块，Linux/macOS 用户复制 bash 块，全程在项目根目录 `social-auto-upload` 下执行**。前置条件：已装好 uv 与 git。

```powershell
# Windows（PowerShell）——在你想存放项目的目录下执行
git clone https://github.com/dreammis/social-auto-upload.git
cd social-auto-upload

# 1. 创建并激活虚拟环境
uv venv
.venv\Scripts\activate

# 2. 以可编辑模式安装项目，注册 sau 命令（同时装好全部依赖）
uv pip install -e .

# 3. 下载浏览器驱动 chromium（国内先设 npmmirror 镜像；变量名沿用 PLAYWRIGHT 前缀）
$env:PLAYWRIGHT_DOWNLOAD_HOST = "https://npmmirror.com/mirrors/playwright"
patchright install chromium

# 4. 生成个人配置文件
cp conf.example.py conf.py

# 5. 验证安装
sau --help
```

```bash
# Linux / macOS（bash）——在你想存放项目的目录下执行
git clone https://github.com/dreammis/social-auto-upload.git
cd social-auto-upload

# 1. 创建并激活虚拟环境
uv venv
source .venv/bin/activate

# 2. 以可编辑模式安装项目，注册 sau 命令（同时装好全部依赖）
uv pip install -e .

# 3. 下载浏览器驱动 chromium（镜像只需对本条命令生效；也可 export 成全局变量）
PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright" patchright install chromium

# 4. 生成个人配置文件
cp conf.example.py conf.py

# 5. 验证安装
sau --help
```

逐条拆讲几个关键步骤：

**① `uv venv` + 激活**：在当前目录生成 `.venv` 虚拟环境。激活后，后面的 `uv pip`、`patchright`、`sau` 都装/跑在这个隔离环境里。之后新开终端若发现 `sau` 找不到，多半是忘了重新激活。

**② `uv pip install -e .`**：`-e` 是「可编辑安装」，相当于给项目本体做了个软链，代码改动不用重装；同时它会读取 [pyproject.toml](https://github.com/dreammis/social-auto-upload/blob/main/pyproject.toml)，把全部依赖装好，并把入口命令 `sau` 注册进当前环境。命令里那个 `.` 指「当前这个项目文件夹」。

> [!tip] 大白话
> `uv pip install -e .` 好比把工具直接挂在工作台上，而不是搬进仓库锁起来：工具改完随手能用，不用每次改完再「重新搬一遍」。所以开发期都用 `-e`，发布时才考虑普通安装。

**③ `patchright install chromium`**：把 patchright 自带的 chromium 内核下载到本地（体积一两百 MB 量级，随版本而定）。网络不通就先设 `PLAYWRIGHT_DOWNLOAD_HOST` 镜像（即上面两块中的写法）；网络顺畅也可以不设镜像直接下载。

**④ `cp conf.example.py conf.py`**：把官方配置模板复制成你的个人配置。`conf.py` 是个人文件、不纳入版本库，真正编辑它要到第 3 章。

**⑤ `sau --help` 验证**：能打印出以 `Usage:` 开头、并列出 `douyin` / `bilibili` / `xiaohongshu` 等平台子命令的帮助信息，就说明 `sau` 已注册、环境就绪。

> [!tip] 装完先冒个烟
> 把 `sau --help` 想成新装软件的「开机自检」：不报 `command not found`、能列出子命令，就说明环境通了。若报错，优先检查两件事：当前终端有没有激活 `.venv`；`uv pip install -e .` 有没有成功执行。更深的排错留给第 6 章。

（以上命令序列以 [docs/install.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/install.md) 为准；个别提示语、chromium 体积随版本变化，以最新代码与实测为准。）

### 2.3 新旧安装路径差异（避免走错教程）

为什么单开一节讲「别走错」？2026-03 这次重构前后差异极大：网上大量第三方教程，以及仓库历史遗留的旧 Web 版（`docs/legacy-web.md`）与 `requirements.txt`，基本还停在「pip + playwright + Web 版」时代。按旧教程操作，命令和配置都对不上新主线。差别集中在四个维度：

| 维度 | 新主线（推荐，本文口径） | 旧路径（历史遗留） |
|------|--------------------------|--------------------|
| 依赖管理 | [pyproject.toml](https://github.com/dreammis/social-auto-upload/blob/main/pyproject.toml) + `uv pip install -e .` | `requirements.txt` + `pip install -r requirements.txt` |
| 浏览器驱动 | patchright，需执行 `patchright install chromium` | playwright |
| Chrome 来源 | 默认用 patchright 自带 chromium；`LOCAL_CHROME_PATH` 只是**可选**复用本机 Chrome | 依赖 `LOCAL_CHROME_PATH` 指向本机 Chrome，不设就跑不起来 |
| 入口 | `sau` CLI（命令行为主） | Web 版（Flask+Vue）/ examples 脚本 |

> [!warning] 认准新主线的信号
> 凡是教程让你 `pip install -r requirements.txt`、装 `playwright`、或强调「必须设置 LOCAL_CHROME_PATH 才能跑」，它基本是重构前的旧路径。可以对照着理解思路，但命令与配置别照抄——尤其别把「Python 3.13 装不上」「一定要本机 Chrome」当成新主线的结论。一切以 [README](https://github.com/dreammis/social-auto-upload) 与 [docs/install.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/install.md) 的当前版本为准。

### 本章小结

- 环境硬性要求：Python `>=3.10,<3.13`（3.13 不可用）、uv 包管理、patchright chromium 驱动；系统三平台均可，biliup 不用手装。
- 安装主线：`git clone` → `uv venv` 并激活 → `uv pip install -e .` → `patchright install chromium` → `cp conf.example.py conf.py` → `sau --help` 验证。
- 国内下载 chromium 慢时设 `PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright"`，变量名仍带 PLAYWRIGHT 前缀，照抄即可。
- `uv pip install -e .` 一次完成「装依赖 + 注册 `sau`」；`sau --help` 能列出平台子命令即安装成功。
- 新旧路径差异在四件事：pyproject+uv vs requirements+pip、patchright vs playwright、默认 chromium vs 强制 LOCAL_CHROME_PATH、`sau` CLI vs Web 版/examples；认准新主线，旧教程只作对照。

下一章把装好的环境真正用起来：编辑 `conf.py` 的最小配置，跑通「登录 → 校验 → 发布」，上传你的第一条抖音视频。

---

## 第 3 章 快速跑通：配置 conf.py 并发布第一条抖音视频

按上一章的安装步骤，你已经完成 `git clone`、建好虚拟环境、注册 `sau` 命令、并用 `cp conf.example.py conf.py` 生成了自己的配置文件。这一章把工具真正「跑起来」：先搞懂 `conf.py` 里 6 个配置键哪些要动，再走一遍「登录 → 校验 → 上传」三步，把第一条抖音视频发出去。抖音是 CLI 里功能最完整的主线平台，拿它做首次闭环验证最合适——只要能发出一条抖音，就说明「配置 → 登录态 → 发布」整条链路是通的。

### 3.1 conf.py 需要关心什么

`conf.py` 是 `sau` 启动时读取的普通 Python 配置文件，位于项目根目录。好消息是官方 [conf.example.py](https://github.com/dreammis/social-auto-upload/blob/main/conf.example.py) 极简，只有 **6 个顶层键**，不需要理解一大坨配置项。

六个顶层键速查表如下：

| 配置键 | 默认值 | 含义 | 快速上手何时改 |
|--------|--------|------|----------------|
| `BASE_DIR` | `Path(__file__).parent.resolve()` | 项目根目录基准，运行时用它解析项目内各路径 | 不用改，也不要把路径写死 |
| `XHS_SERVER` | `"http://127.0.0.1:11901"` | 仅小红书旧流程用的本地服务地址 | 新 CLI 主线用不到，保持默认 |
| `LOCAL_CHROME_PATH` | `""`（空） | 复用本机已装 Chrome 时填可执行文件路径；留空用 patchright 自带 chromium | 想用本机 Chrome 才填，如 `C:/Program Files/Google/Chrome/Application/chrome.exe` |
| `LOCAL_CHROME_HEADLESS` | `True` | 是否无头运行：`True` 后台不弹窗，`False` 弹出可见浏览器窗口 | 首次登录被风控 / 扫码总失败时临时设 `False` |
| `DEBUG_MODE` | `True` | 调试开关，打开时过程输出更详细 | 保持 `True`；在无头服务器上排错时与 `LOCAL_CHROME_HEADLESS` 搭配调整 |
| `YT_PROXY` | `None` | 仅 YouTube 流程用的显式代理 | 上 YouTube 连不上时填，如 `"http://127.0.0.1:7890"` |

> [!tip] 大白话：headless 是什么
> 把浏览器想成一个替你上传的店员。`headless=True` 就是让店员在后台小黑屋里干活，你看不到操作过程、但它照常工作；`headless=False` 就是把小黑屋换成前台玻璃窗，你能亲眼看着它点哪、填哪。风控严的平台对「看不见的店员」更警惕，所以登录总失败时，先把它请到前台（headed）操作一次。

#### 快速上手真正要动的只有 3 个

- **`LOCAL_CHROME_PATH`**：默认留空即可，工具用安装时下载的 patchright chromium。只有当 chromium 下载失败、或你明确想复用本机 Chrome 时才需要填；Windows 路径在 Python 字符串里推荐用 `/` 分隔（如 `C:/Program Files/...`），避免反斜杠转义问题。
- **`LOCAL_CHROME_HEADLESS`**：默认 `True`，日常发布不用管；唯一常见改动是首次登录不顺畅时临时改 `False`（见 3.3）。
- **`DEBUG_MODE`**：保持默认 `True`，出错时能看到更多过程信息，排错成本最低。

其它三个键（`BASE_DIR`、`XHS_SERVER`、`YT_PROXY`）默认值就是正确值：前两个自动解析或仅旧流程用，最后一个只有碰 YouTube 才涉及（第 6 章再展开）。

#### 边界提醒：别往 conf.py 里乱加键

官方 `conf.example.py` **没有** DB、日志路径、各平台 Cookie 路径之类的配置键。账号模型是**「一个 `account_name` = 一个账号文件」**：你给账号起什么名字，工具就把这个账号的登录态单独存成一个文件，落在 `cookies/[平台]/[平台]_[account].json`。例如 `sau douyin login --account demo` 登录成功后，Cookie 会写到 `cookies/douyin/douyin_demo.json`（精确路径以实测 / `sau --help` 为准）。

> [!warning] 别乱加 conf 键
> `conf.py` 是脚本按固定键名读取的，不是自由填写的配置单。凭直觉加上 `DB_PATH`、`COOKIE_DIR`、`LOG_LEVEL` 这类键，脚本不会读它，只会留下「我明明配了为什么没生效」的假象。遇到配置问题先查官方 `conf.example.py` 里有没有这个键，而不是自己造一个。

> [!tip] 大白话：account_name 与账号文件
> 把 `account_name` 想成门禁卡上的卡号。卡号叫 `demo`，门卫（工具）就把 `demo` 的出入记录单独放一个抽屉；叫 `work` 就另开一个抽屉，互不串号。登录态（Cookie）就是抽屉里的那张卡——想要几个账号就建几个卡号，想删账号就删对应文件。

### 3.2 发布第一条抖音（跑通闭环）

配置确认无误后进入正题。先准备一个测试视频，例如在项目根目录放一个 `demo.mp4`（随便一段短视频即可），然后依次执行下面三条命令：

```bash
# 第 1 步：准备登录态。首次运行会进入抖音登录流程，扫码或短信登录一次
sau douyin login --account demo

# 第 2 步：校验登录态。确认 demo 账号的 Cookie 还有效，适合在每次发布前快速跑一遍
sau douyin check --account demo

# 第 3 步：发布。不传 --schedule 表示立即发布，而不是定时发布
sau douyin upload-video --account demo --file demo.mp4 --title "第一条测试视频" --desc "用 social-auto-upload 自动上传的验证视频"
```

以上是 bash 写法；在 Windows PowerShell 里把每条命令写成一行即可（PowerShell 不用 `\` 续行），含义不变。

三个动作各管一段（[docs/install.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/install.md)、[docs/CLI.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/CLI.md)）：

- **`login`**：准备登录态。首次使用必须跑一次，它打开浏览器走到抖音登录页，等你扫码或收短信。成功后登录态落盘成 Cookie 文件，之后不必每次都登。
- **`check`**：校验登录态。它加载 Cookie 并导航到抖音上传/发布页，判断当前账号是否还能用。适合发布前快速跑一遍，避免发到一半才发现登录早失效了。
- **`upload-video`**：发布视频。带上 `--file`、`--title`、`--desc` 即可；**不传 `--schedule` 就是立即发布**（定时发布是第 4 章的主题）。Cookie 有效时，它会直接走到发布页填标题、描述、传文件。

预期行为大致是：`login` 出现二维码或要求短信码 → `check` 返回「有效 / 失效」之类的结论 → `upload-video` 打印上传进度并在结束时报成功。三步都顺利的话，登录抖音创作者后台（creator.douyin.com）应该能在作品列表里看到这条视频。

> [!note] 成功判定以 CLI 输出 / 实测为准
> 官方 README / install.md / CLI.md 都没有定义命令的输出格式、退出码或「成功标志」——没有一份文档告诉你哪行输出算成功。因此判据是：**upload 命令结束时看终端有没有「上传成功」类提示，再到创作者后台作品列表复核**，两条都对上才算真成功。不要依赖某个固定的返回码或 JSON 字段。

> [!tip] 大白话：这三步在干嘛
> 把发布想成去办事大厅：`login` 是「先领号、做人脸登记」拿到入场资格；`check` 是「到闸机口刷一下卡」确认资格还有效；`upload-video` 才是「去柜台交材料」。闸机都过不去时别急着怪交材料的窗口——多半是卡（Cookie）过期了。

一点实操提示：`--file demo.mp4` 这类相对路径，默认按你**执行命令时所在的目录**解析（确切规则以实测为准）。建议先 `cd` 到项目根目录再跑，省得路径写错；视频放在别处时直接用绝对路径最稳妥。

### 3.3 登录验证的最小闭环

第一步 `login` 是整条链路里唯一需要「人参与」的地方。抖音登录主要有两种验证方式，对应两种喂法：

**方式一：短信验证码 → `verify_code.txt`**

当登录流程触发短信验证时，工具会在项目根目录等你放一个 `verify_code.txt` 文件。做法：

1. 手机收到验证码后，在项目根目录新建 `verify_code.txt`，文件内容只写验证码本身；
2. 工具读到后自动完成验证，并**自动删除这个文件**（下一次登录需要新的验证码，不能复用）。

> [!tip] 大白话：verify_code.txt
> 把验证码想成递给门卫的一次性字条：你写好塞进门缝（项目根目录），门卫看完当场撕掉（自动删除）。所以它天生适合自动化——agent 场景下，程序只要向你要到码、写进这个文件，就能替你把登录走完，而且不留残余。

**方式二：二维码 / 扫码**

另一种情况是登录页出二维码：工具生成二维码图片，你用抖音手机 App 扫一下、在手机上确认即可。在自己电脑上跑时通常能直接看到二维码；如果是在无界面环境（服务器或 agent 场景），工具会把二维码图片**直接展示给操作者扫**，扫完自动继续。

**headless 登录被风控时的临时对策**

如果按默认 `LOCAL_CHROME_HEADLESS = True` 登录，扫码后一直超时、或提示「二维码异常」，通常是平台风控识别了无头浏览器（[GitHub Issue #224](https://github.com/dreammis/social-auto-upload/issues/224)，属真实案例、详见第 6 章）。临时对策是切到有头模式登一次：

```python
# conf.py —— 首次登录被风控时，临时把这一行改成 False
LOCAL_CHROME_HEADLESS = False   # 登录成功、Cookie 落盘后，改回 True 即可
```

登录态一旦成功落盘成 Cookie 文件，后续 `check` 和 `upload-video` 都只读文件、不再需要扫码，所以你可以把 `LOCAL_CHROME_HEADLESS` 改回 `True`，继续无头发布。这套「复用真实登录态、不硬刚风控」的思路，以及 Cookie 到底怎么存、`check` 凭什么判断失效，留到第 5 章专门讲透。

### 本章小结

- `conf.py` 只有 6 个顶层键，实际常动的只有 `LOCAL_CHROME_PATH`、`LOCAL_CHROME_HEADLESS`、`DEBUG_MODE` 三个。
- 官方 conf 没有 DB / 日志 / Cookie 路径键；「一个 `account_name` = 一个账号文件」，Cookie 落在 `cookies/[平台]/[平台]_[account].json`，不要臆造键名。
- 抖音跑通闭环 = `login`（准备登录态）→ `check`（校验登录态）→ `upload-video --file/--title/--desc`（不传 `--schedule` 即立即发布）。
- 登录两种喂法：短信码写进项目根目录 `verify_code.txt`（用完自动删）；二维码图片直接展示给人扫。
- headless 登录被风控时：临时把 `LOCAL_CHROME_HEADLESS` 设 `False` 用有头模式登一次，登录态落盘后改回 `True`；成功与否以 CLI 输出 / 实测为准。

单平台 demo 只是开始：抖音能这么跑，是因为它是 CLI 里功能最全的平台，其它平台命令长得几乎一样，但「能不能发图文、能不能定时、有什么专属参数」各有取舍。下一章用一张平台能力总表加 CLI 命令速查，把这套「login → check → upload」的单平台经验直接推广到全平台。

---

## 第 4 章 平台能力矩阵与 CLI 命令参考

第 3 章用抖音走通了「配置-登录-发布」的最小闭环，但抖音只是 11 个平台里的一个。一旦想把同一条内容铺到 B 站、小红书、视频号，问题立刻变成：每个平台的命令怎么拼？哪些平台能发图文、能定时？本章把 11 个平台的能力差异和 `sau` 命令收成一套「速查层」：先给平台能力总表，再拆 CLI 通用结构，接着给发布参数速查，最后点出一个文档缺口——成功/失败到底怎么判定。

### 4.1 平台能力总表（11 平台）

先给结论性地图。下表覆盖 11 个平台，列头含义：

- **CLI 前缀** = `sau` 后第一段，即平台子命令名（如抖音是 `sau douyin …`）；
- **视频 / 图文 / 定时发布** = 平台侧能力（README 能力矩阵口径）；
- **CLI 接入** = 当前 `sau` 主线是否已接入（未接入则只能用历史 example）。

| 平台 | CLI 前缀 | 视频 | 图文 | 定时发布 | CLI 接入 | 说明 |
|------|---------|:--:|:--:|:--:|:--:|------|
| 抖音 | `douyin` | ✅ | ✅ | ✅ | ✅ | 主线能力最完整；图文另支持 BGM / notef |
| Bilibili | `bilibili` | ✅ | ❌ | ✅ | ✅ | 自动下载 biliup；`--tid` 分区必填（示例 249） |
| 小红书 | `xiaohongshu` | ✅ | ✅ | ✅ | ✅ | 浏览器版；旧流程才需 XHS_SERVER |
| 快手 | `kuaishou` | ✅ | ✅ | ✅ | ✅ | — |
| 视频号 | `tencent` | ✅ | ❌ | ✅ | ✅ | CLI 前缀是 `tencent`；可传 `--collection` / `--draft` |
| 百家号 | `baijiahao` | ✅ | ❌ | ❌ | ✅ | 可传 `--collection` |
| 支付宝生活号 | `alipay` | ✅ | ❌ | ❌ | ✅ | 需先开通生活号创作 |
| 微博 | `weibo` | ✅ | ❌ | ❌ | ✅ | 标题 ≤ 30 字 |
| 虎扑 | `hupu` | ✅ | ❌ | ❌ | ✅ | 标题 4–40 字 |
| YouTube | `youtube` | ✅ | ❌ | ❌ | ✅ | 浏览器自动化操作 Studio；可传 `--playlist` / `--visibility`；被墙需 `YT_PROXY` |
| TikTok | （无） | ✅ | ❌ | ✅（矩阵列） | ❌ | 走历史 Chrome example，未接入 CLI |

读这张表最有价值的一条信息：**图文能力很稀缺，只有抖音 / 小红书 / 快手三行是 ✅**。想做图文分发，先圈定这三个平台即可；其余平台表格里直接标了 ❌，不用浪费时间找图文参数。

> [!warning] 版本口径：两处能力冲突以最新代码为准
> ① **YouTube 实际有 CLI**：README 快速开始段列「已接入 CLI」时漏写了 YouTube，但同一段给了 `sau youtube` 示例、CLI.md 也含 youtube——判定为有 CLI（推断）。② **TikTok 定时发布未接入 CLI**：README 能力矩阵把 TikTok 定时发布标成 ✅，但 CLI.md 的 `--schedule` 支持表里没有 TikTok——现状是「平台侧支持、工具侧还没接」。以上均为易变 / 推断信息，以仓库最新代码为准（[README](https://github.com/dreammis/social-auto-upload) / [docs/CLI.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/CLI.md)）。

> [!tip] 大白话：怎么读这张能力表
> 把每一行想成该平台的「报名规则清单」：哪些玩法它收（✅）、哪些不收（❌）。所以它不回答「哪个平台最好」，只回答「你手上这条内容在这个平台能不能发」——视频几乎哪都能发，图文却只有三家里能发。

### 4.2 CLI 通用结构

`sau` 把所有平台收成了同一套命令骨架：

```bash
sau <platform> <action> --account <account_name> [参数]
```

- `<platform>`：平台子命令名，即 4.1 表的「CLI 前缀」列；
- `<action>`：要做的动作；
- `--account <account_name>`：**通用必选**，指定用哪个账号身份。一个 `account_name` 对应一份独立的账号文件（Cookie），互不干扰——这是第 3 章「一个账号名 = 一个账号文件」模型在命令层的体现。

每个平台发布前的基本动作是固定「三件套」：

```bash
# 以抖音为例：login（准备登录态）→ check（校验登录态）→ upload-video（发布）
sau douyin login --account demo
sau douyin check --account demo
sau douyin upload-video --account demo --file demo.mp4 --title "示例标题" --desc "示例描述"
```

| 子命令 | 作用 | 备注 |
|--------|------|------|
| `login` | 准备登录态 | 首次要扫码 / 短信验证（短信验证码写项目根目录 `verify_code.txt`） |
| `check` | 校验登录态是否有效 | 平台出现登录 UI 即判失效；判定细节见第 5 章 |
| `upload-video` | 发布视频 | 不传 `--schedule` 就立即发布 |
| `upload-note` | 发布图文 | 仅抖音 / 快手 / 小红书支持 |

通用运行参数有三个，控制浏览器「怎么跑」：

| 参数 | 含义 | 默认 | 典型用途 |
|------|------|------|----------|
| `--headless` | 无头运行，不弹出浏览器窗口 | 默认 | 日常发布、服务器部署 |
| `--headed` | 有头运行，弹出真实浏览器窗口 | 关 | 登录被风控时临时打开看现场 |
| `--debug` | 打印调试信息 | 关 | 排错定位 |

**多账号并发**：每个 `--account` 是独立账号文件、不共享登录态，所以可以同时跑多条命令处理不同账号。比如想给两个抖音号发同一条视频，就开两个终端各指定一个 `--account`，或写进脚本并行执行——账号之间互不干扰。

> [!tip] 大白话：命令骨架想成「去柜台办事」
> `sau <platform> <action> --account <name>` 就像「到 XX 平台柜台办 XX 业务，报上你的会员号」：`<platform>` 是去哪个柜台，`<action>` 是办什么事，`--account` 是报哪张卡。同一个平台有几个号，就分几次报不同会员号，各办各的。

### 4.3 发布参数速查

发布参数分三层：视频通用参数 → 图文专用参数（仅三平台）→ 各平台扩展参数。先记通用层，再按平台查扩展层。

**视频通用参数**（`upload-video`）：

```bash
sau <platform> upload-video --account demo \
  --file video.mp4 \      # 必填：本地视频路径
  --title "标题" \         # 必填：标题
  --desc "描述" \          # 必填：描述
  --tags "科技,AI"         # 可选：标签，逗号分隔
```

**图文专用参数**（`upload-note`，仅抖音 / 快手 / 小红书）：

```bash
# 图文参数名从 --desc 换成 --note；图片用 --images 一次传多张
sau douyin upload-note --account demo \
  --images a.png b.png \   # 必填：图片路径，空格分隔多张
  --title "图文标题" \
  --note "图文正文"

# 抖音图文额外选项：--notef 传图文文件、--bgm 指定背景音乐
sau douyin upload-note --account demo \
  --images a.png b.png --title "标题" --note "正文" \
  --notef content.md --bgm "卡农"
```

一个容易记的元数据约定：**视频的正文 = title + desc + tags，图文的正文 = title + note + tags**。所以图文命令里没有 `--desc`，取而代之的是 `--note`。

**各平台扩展参数**：在通用参数之上，个别平台多了自己的选项，多为平台功能入口（分区、合集、可见性等）。

| 平台 | 扩展参数 | 说明 |
|------|---------|------|
| Bilibili | `--tid <分区id>` | 投稿分区，必填；示例 `249`。文档标「必填」，实际是否仍强制需实测 |
| YouTube | `--playlist <id>` / `--visibility <值>` | 投到指定播放列表 / 设置可见性；被墙网络需在 conf.py 配 `YT_PROXY` |
| 视频号 | `--collection` / `--draft` | 可选；精确语义以最新代码 / 实测为准 |
| 百家号 | `--collection` | 可选 |
| 支付宝生活号 | `--collection` | 可选；平台侧需先开通生活号创作 |
| 抖音 | `--product-link` / `--product-title` | 商品链接 / 商品标题（带货挂链场景） |

**定时发布**：在支持定时的平台上，传 `--schedule` 就切换为定时策略，不传则立即发布。参数是**绝对时间**：

```bash
# 格式固定为 "YYYY-MM-DD HH:MM"，传未来绝对时间，到点自动发布
sau douyin upload-video --account demo \
  --file demo.mp4 --title "标题" --desc "描述" \
  --schedule "2026-09-06 20:00"
```

CLI 的定时支持矩阵（比 4.1 能力矩阵更窄，以 CLI.md 为准）：

| 平台 | `--schedule` 定时 | 覆盖内容 |
|------|:--:|------|
| 抖音 `douyin` | ✅ | 视频 + 图文 |
| 快手 `kuaishou` | ✅ | 视频 + 图文 |
| 小红书 `xiaohongshu` | ✅ | 视频 + 图文 |
| Bilibili `bilibili` | ✅ | 仅视频 |
| 视频号 `tencent` | ✅ | 仅视频 |
| 百家号 `baijiahao` | ❌ | — |
| 支付宝生活号 `alipay` | ❌ | — |
| 微博 `weibo` | ❌ | — |
| 虎扑 `hupu` | ❌ | — |
| YouTube `youtube` | ❌ | CLI.md 支持表未列（能力矩阵亦为 ❌） |
| TikTok | 不可用 | 能力矩阵标 ✅，但未接入 CLI |

> [!tip] 大白话：把 `--schedule` 想成「预约上架」
> 传了 `--schedule "YYYY-MM-DD HH:MM"`，命令就从「现在立刻发」变成「到点自动发」；不传才是立即发布。作者提到定时时间计算默认按「第二天」策略处理边界——也就是约的是未来某天的绝对时刻，跨天 / 边界情况按此推算。具体边界以实测为准。

### 4.4 成功/失败判定缺口

看到这里，你可能会想找一张「成功输出长什么样、失败退出码是多少」的表——但翻遍 README、docs/install.md、docs/CLI.md，**都没有说明命令的输出格式、退出码或成功标志**。这是当前文档的一个真实缺口（[docs/CLI.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/CLI.md)）。

所以本笔记不臆造任何返回约定，实践上按下面三步确认：

1. **以 CLI 输出 / 实测为准**：跑一次上传，观察当前版本实际打印了什么；
2. **回平台侧确认**：发布后到对应平台的创作者后台 / 作品页看作品是否真的出现，这是最硬的判据；
3. **需要代码级判定时再看实现**：想写脚本判断成功与否，去读对应平台 uploader 实现或 `sau_cli.py`，而不是猜 JSON 字段。

> [!warning] 别采信「返回 0 即成功」这类说法
> 因为文档没定输出 / 退出码约定，任何第三方教程写的成功判定格式都可能对不上你的版本。遇到这类说法，先在自己环境实测一次再采信；平台改版或项目升版后，判定方式也可能变（机制详见第 5、6 章）。

### 本章小结

- 11 个平台里 10 个已接入 `sau` CLI（YouTube 按 CLI.md 判定已接入，README 行文漏写）；TikTok 未接入，走历史 example。
- 图文能力仅抖音 / 小红书 / 快手三平台支持；其余平台只能发视频。
- CLI 统一结构 `sau <platform> <action> --account <name>`，`--account` 通用必选；动作固定为 login → check → upload-video / upload-note 三件套。
- 视频参数通用 `--file / --title / --desc`，图文用 `--images / --title / --note`；平台扩展参数（B 站 `--tid`、视频号 `--collection / --draft`、YouTube `--playlist / --visibility` 等）按扩展表查。
- 定时发布用 `--schedule "YYYY-MM-DD HH:MM"`；CLI 支持抖音 / 快手 / 小红书 / B站 / 视频号，百家号 / 支付宝 / 微博 / 虎扑不支持。
- 成功 / 失败判定文档缺口未补：以 CLI 输出 / 实测为准，发布后回平台侧确认。

下一章从「命令怎么拼」转向「为什么时灵时不灵」：登录态到底存在哪、`check` 凭什么判断失效、Cookie 过期和平台风控怎么绕——把第 3、4 章里 `login` 那一步背后的机制讲透。

---

## 第 5 章 登录态与 Cookie 机制

第 3 章你跑通了 `login → check → upload-video` 的最小闭环，但多半只知其然：`login` 到底把登录态存到了哪里？`check` 凭什么判断「已失效」？一旦平台风控拦下自动化登录，还有什么逃生通道？本章把这三件事讲透——它们是理解第 6 章所有排错案例的前提。

### 5.1 登录态存储与账号模型

第 3 章反复强调过一个模型：**一个 `account_name` = 一个账号文件**。落到磁盘上，这个「账号文件」是一份 JSON，固定放在 `cookies/[平台]/[平台]_[account].json`（具体目录/文件名的拼写以最新代码为准）。比如抖音建了 `demo` 和 `work` 两个账号，结构大致是这样：

```text
cookies/
├── douyin/
│   ├── douyin_demo.json     # --account demo 的抖音登录态
│   └── douyin_work.json     # --account work 的抖音登录态
├── xiaohongshu/
│   └── xiaohongshu_demo.json
└── kuaishou/
    └── kuaishou_demo.json
```

有两点值得记住：

1. **目录和文件都按「平台 + 账号名」分区**，所以同一平台可以并存多个账号，多账号并发时 `--account` 就是挑选对应文件的钥匙。
2. **这份 JSON 不是一串普通 cookie，而是 patchright/playwright 的 `storage_state` 序列化结果**——里面除了各站点的 cookie，还包含 localStorage 等浏览器本地状态。抖音的登录态有一部分就放在 localStorage 里，所以抖音专用导出脚本会连 localStorage 一起带走。

这也回头印证了 conf.py 的极简设计：官方配置里**没有**「cookie 路径」这类键，因为路径规则是写死在代码里的约定。你只需保证 `--account` 的名字和登录时一致，脚本自己会去对应位置找文件，不要臆造或手工改名。

> [!tip] 大白话：cookie 文件里不只有 cookie
> cookie 是平台发你的「临时工牌」，证明你登录过；localStorage 则是浏览器本地「储物柜里的便签」，是站点自己记的小账本。抖音既发工牌、又往便签上写字，所以它的登录态文件要把「工牌 + 便签」一起存，缺一样都可能被当成陌生人。

### 5.2 `check` 怎么判失效

`check` 并不会打开 cookie 文件逐项核对有效期，而是**开着浏览器导航到该平台的发布/上传页，看页面是否出现登录 UI**：出现了，就判定 cookie 已失效；没出现，就认为还能用。以抖音为例，`sau douyin check --account demo` 会进入创作服务平台的发布页，如果页面冒出「扫码登录」字样，check 即报未登录。

各平台靠什么元素判失效，是跟着页面改版走的易变信息。下表是调研时（2026-09）代码里的失效信号，使用前**以最新代码为准**：

| 平台（CLI 前缀） | 典型失效信号 | 说明 |
|---|---|---|
| 抖音 `douyin` | 页面出现「扫码登录」 | 登录框弹出即判失效 |
| 快手 `kuaishou` | 「机构服务」选择器 | 出现该元素视为未进入创作者后台 |
| 视频号 `tencent` | 「微信小店」 | 出现视为停在登录页/非目标页 |
| 小红书 `xiaohongshu` | 「手机号 / 扫码登录」 | 出现登录面板即判失效 |

> [!warning] `check` 看的是间接证据，存在竞态误判
> 用「页面上有没有登录 UI」反推「cookie 有没有失效」，本质是看间接证据，而不是核对 cookie 本身。页面加载稍慢、平台改版让选择器对不上（[Issue #230](https://github.com/dreammis/social-auto-upload/issues/230)），check 都可能在 cookie 仍然有效时误报 `invalid`（[#224](https://github.com/dreammis/social-auto-upload/issues/224) 讨论区也多次出现，属真实案例，勿当必然）。真遇到「明明刚登录过、check 却说失效」，先 `git pull` 升到最新代码，再去 Issues 搜同款症状。社区讨论给出的改进方向是改判 `sessionid` 这类登录 cookie 是否存在，而不是看 UI 文案——但这仍是 issue 中的建议，是否合入以最新代码为准。

> [!tip] 大白话：check 像个「看动作」的保安
> check 不查你工牌的签发日期，而是看「有没有人朝闸机走」：画面里一出现「扫码登录」四个字，它就当你还没进门。所以闸机还没完全打开、或保安一时眼花（页面加载慢、改版），它也会误拦明明有卡的人。

### 5.3 高风控逃生通道：CDP 9222 导出真实浏览器登录态（抖音）

自动化登录最怕平台风控。headless 环境下抖音、快手常出现「扫码后二维码异常 / 登录超时」（[#224](https://github.com/dreammis/social-auto-upload/issues/224)，真实案例），无头浏览器的指纹太明显，平台不给你完成登录。此时不要硬刚，改用**真实浏览器登录态复用**：让真人在 VNC/桌面里用真实 Chrome 登录一次，再把这份登录态「导出」给自动化用。完整流程三步：

```bash
# ① 在 VNC / 桌面环境启动真实 Chrome，开启 Remote Debugging Port 9222
#   （Linux 服务器示例；Windows 换成 chrome.exe 的全路径）
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/douyin-profile"
```

② 在弹出的 Chrome 里手动登录 `creator.douyin.com`（扫码或短信均可），确认进到创作服务平台后再继续；③ 登录态就绪后，在项目根目录执行导出与校验：

```bash
# ③ 连接 9222，抽取 cookie + localStorage，写成 uploader 可读的 storage_state JSON
bash export_douyin_cookie.sh --account demo

# ④ 校验这份登录态是否被认可
sau douyin check --account demo
```

原理：9222 是 Chrome 的 **Remote Debugging Port（远程调试端口）**。Chrome 开启该端口后，外部程序就能通过 CDP（Chrome DevTools Protocol）向它询问「当前浏览器里有哪些 cookie、哪些 localStorage」。[`export_douyin_cookie.sh`](https://github.com/dreammis/social-auto-upload) 做的事就是：连上 `http://127.0.0.1:9222`，用 CDP 的 `Network.getAllCookies` 拿到全部 cookie，再在页面里执行 JS 抽出 localStorage，最后打包成和 `sau douyin login` 写出的同款 JSON，落到 `cookies/douyin/douyin_<account>.json`。之后 `check` 与 `upload-video` 走无头浏览器加载这份 JSON，等于自动化替身「借」到了真实登录凭证。

> [!tip] 大白话：别让替身再闯一次门禁
> 把 headless 自动化想成「替身演员」，把 VNC 里那台真实 Chrome 想成「本尊」。替身自己去走扫码登录，保安（风控）一眼识破；CDP 9222 的做法是让替身直接**复刻本尊的门禁卡**——本尊只登录一次，导出脚本把整套凭证拷给替身，之后替身刷卡进场。脚本目前针对抖音（`export_douyin_cookie.sh`），其它平台思路相同、脚本各异。

### 5.4 短信验证码与扫码

自动化登录还常遇到两类需要「真人」介入的关卡：短信验证码和扫码。工具的处理方式是把它们变成显式的「喂给 / 扫给」动作，而不是偷偷破解。

**短信验证码：`verify_code.txt` 喂码。** 平台会向手机发验证码，脚本不替你收短信，而是停在「等待输入验证码」状态，去项目根目录找 `verify_code.txt`。你把收到的验证码写进这个文件，脚本读到后自动填入并提交；**验证完成后文件会被自动删除**，避免残留敏感信息，下次需要就再写一张。

**扫码：直接把二维码展示给你。** 需要扫码时，脚本会把二维码图片显示出来（桌面 / agent 场景），你掏出手机 App 扫一下即可；工具不会去做 OCR 之类的事。

这两类机制背后是同一条心法：**登录被风控时，优先「复用真实浏览器登录态」，而不是硬刚自动化**。扫码 / 短信只是第一道坎；headless 指纹、异地 IP、海外登录（小红书 [Issue #226](https://github.com/dreammis/social-auto-upload/issues/226)）都可能让自动化登录在半路被拦。与其反复调参重试，不如退一步——用 5.3 的 CDP 9222 导出，或把 `LOCAL_CHROME_HEADLESS` 临时设 `False` 走有头浏览器，让「人登录一次，机器接管以后」。

> [!tip] 大白话：验证码靠「传纸条」
> 脚本没有读短信的本事，它只认项目根目录里那张叫 `verify_code.txt` 的小纸条。你收到验证码就写上去，脚本读完纸条就撕掉（自动删除），下次要用再写一张。

### 本章小结

- 登录态落盘为 `cookies/[平台]/[平台]_[account].json`，本质是 patchright/playwright 的 `storage_state` JSON，抖音导出还带 localStorage；目录/文件命名规则以最新代码为准。
- `check` 不核对 cookie 有效期，而是导航到发布/上传页看是否出现登录 UI；各平台失效信号（抖音「扫码登录」/ 快手「机构服务」/ 视频号「微信小店」/ 小红书「手机号 / 扫码登录」）属易变信息，以最新代码为准。
- `check` 判失效存在竞态缺陷（[#224](https://github.com/dreammis/social-auto-upload/issues/224) / [#230](https://github.com/dreammis/social-auto-upload/issues/230)）：有效 cookie 也可能被误判 `invalid`，先升最新代码再排查。
- 高风控场景别硬刚自动化：VNC 开真实 Chrome 登录 `creator.douyin.com` → `bash export_douyin_cookie.sh --account <name>` → `sau douyin check`，本质是通过 CDP 9222 用 `Network.getAllCookies` + JS 把真实登录态导出成兼容 JSON。
- 短信验证码走根目录 `verify_code.txt` 喂码、验证后自动删除；扫码直接把二维码展示给用户扫。

下一章把这些机制落到真实运维上：headless 登录被识别、创作者中心改版导致选择器失效、视频号二维码 iframe、海外登录被 ban……每一条坑都能对应到本章的某个机制——先懂机制再看案例，排错才不会像无头苍蝇。

---

## 第 6 章 常见坑与排错

装好环境、写对 `conf.py`、命令也会敲之后，真正会卡住你的通常不是命令本身，而是三类外部变化：**登录被平台风控拦截、平台页面改版导致脚本找不对元素、部署环境（Python / 浏览器驱动 / 网络）的小毛病**。这三类问题症状往往很像——都是「卡住、超时、报错」，但处理策略完全不同。所以本章先给一条排错心法（先归类、定策略，再动手），再给两张速查表：一张是 GitHub Issues 里真实用户踩过的坑（按「案例」看待，勿当通论），一张是部署环境里的通用问题。

### 6.1 排错心法（先定策略再动手）

遇到报错先别急着反复重试——先回答一个问题：**这是「登录/风控问题」、「页面元素问题」还是「环境问题」？** 判断错了方向，重试多少次都是在原地打转。下面两条心法覆盖前两类最高频的场景。

**心法一：登录被风控 → 优先复用真实浏览器登录态（CDP 9222 / headed），不要硬刚自动化**

这个项目的本质是「脚本替已登录好的你上传」，绕不开平台登录与风控。平台对「无头、脚本化」的登录动作很敏感：`headless` 模式尤其容易被识别为机器人，表现为扫码后提示二维码异常、超时，或直接 ban 登录。关键认知是——**这类问题靠调整自动化参数往往解决不了，越硬刚越容易被标记**。正确策略是第 5 章那条逃生通道：用 VNC 开一个真实 Chrome 登录 `creator.douyin.com`，再用 `export_douyin_cookie.sh` 把登录态导出给脚本复用；或者临时改用 `--headed` / `LOCAL_CHROME_HEADLESS=False` 手工登录一次。

> [!tip] 大白话
> 把自动化登录想成「派机器人去物业办门禁卡」：物业一眼看出是机器人，故意不给办；你再派第二个机器人去，大概率连你一起被记名。正确做法是你本人（真实浏览器）去办一次卡，然后把卡（Cookie 登录态）交给脚本——之后脚本只刷卡、不办卡。所以登录被卡住时，先走「真实浏览器登录态」通道，别让脚本反复硬闯。

**心法二：平台改版导致元素失效 → 先升到最新代码，再查 Issues / PR**

这类工具靠识别页面上的按钮文案、class、DOM 结构来操作上传页，本质是「按图索骥」。平台一改版（比如抖音创作者中心改版），代码里那张「图」就过期了，脚本会一直等一个已经不存在或换位置的元素，表现就是超时、找不到元素。此时先确认自己跑的是不是最新代码：

```bash
# 先升到最新代码再排错（editable 安装下源码即代码；依赖有变就重装一次）
git pull
uv pip install -e .
```

升到最新仍复现，再去 GitHub Issues/PR 搜关键词——平台改版是社区高频问题，多半已有人报过，甚至已有修复或临时方案。判断依据以仓库实时状态为准。

> [!warning] 版本依赖
> Issues / PR 是「某个时刻」的快照：你本地仓库的版本、平台改版进度、作者是否已修复，三个变量都在动。查 Issue 先看它的创建时间、对应的代码版本、当前 Open / Closed 状态，别拿几个月前的结论直接套当前代码。这个仓库在重构后迭代很快，排错的第一步永远是「先假设你代码旧了」。

> [!tip] 大白话
> 平台改版导致元素失效，可以想成「你手里的路书是照着旧路牌写的：道路翻修后路牌挪了位置，照着走就迷路」。所以先确认地图（代码）是不是最新版，再翻 Issues 看别人有没有标出新路牌的位置——而不是原地反复试走。

### 6.2 真实用户案例坑（GitHub Issues，当「案例」看）

下面这张表来自 GitHub Issues 中真实用户报的坑。强调「案例」是因为**每条都是特定版本、特定时间点、特定环境下的个体现象**：有的还 Open、有的修复刚 Closed、有的修复建议尚未确认合入。它们最有价值的地方是**帮你快速对号入座**——看到同款症状时知道往哪个方向查，而不是当作普适结论直接下判断。核实方式：去仓库 Issues 搜对应 `#` 号，看它当前的状态与讨论。

| 坑（案例） | 影响 | 症状 | 状态 / 方案 |
| --- | --- | --- | --- |
| headless 登录被识别（[#224](https://github.com/dreammis/social-auto-upload/issues/224)） | 抖音 / 快手 | 扫码后提示「二维码异常」作废，或长时间超时 | **Open**；属「登录被风控」，走 CDP 9222 复用真实 Chrome 登录态，或临时 headed 登录 |
| 创作者中心改版选择器失效（[#230](https://github.com/dreammis/social-auto-upload/issues/230)） | 抖音 | `login` 等待「扫码登录」超时、扫码后仍超时 | **Open**；[PR#229](https://github.com/dreammis/social-auto-upload/pull/229) 提议「多级选择器回退 + networkidle 等待 + 200s 超时」，合入状态未确认 |
| 登录判定竞态（案例：#224/#230） | 抖音 | 登录态其实有效，`check` 却误判 invalid | Open；社区建议改判 `sessionid` 类关键 cookie，以最新代码为准 |
| 二维码 iframe 切到 qrconnect（[#252](https://github.com/dreammis/social-auto-upload/issues/252)） | 视频号 | 报「未获取到视频号登录二维码地址」 | [#252](https://github.com/dreammis/social-auto-upload/issues/252) → [PR#253](https://github.com/dreammis/social-auto-upload/pull/253) 已 **Closed**：识别 qrconnect iframe，把相对路径转 data URL |
| 非 ASCII 路径读不了二维码 | Windows 部署的扫码场景 | OpenCV `imread` 对含中文等非 ASCII 的路径**静默失败**，拿不到二维码 | 参照 PR#253 附带思路（`np.fromfile` + `cv2.imdecode`）；低成本规避：部署目录避免中文/特殊字符 |
| 小红书海外登录被 ban（[#226](https://github.com/dreammis/social-auto-upload/issues/226)） | 小红书 | 提示「暂不支持海外用户登录」 | [#226](https://github.com/dreammis/social-auto-upload/issues/226) → [PR#233](https://github.com/dreammis/social-auto-upload/pull/233)：把 creator 域名做成可配置（切 `rednote.com`），合入状态未确认 |
| B 站投稿过于频繁 21566（[#210](https://github.com/dreammis/social-auto-upload/issues/210)） | Bilibili | 投稿报错码 21566，冷却后再传、重新登录仍可能触发 | **Open**；疑似 APP/服务端侧风控，仓库内暂无确定修复 |
| Google 登录风控（[#220](https://github.com/dreammis/social-auto-upload/issues/220)） | TikTok / YouTube | 密码登录被拦，提示「此浏览器不安全」 | **Open**；社区建议真实浏览器登录后复用登录态，不硬刚自动化 |

这张表怎么用：遇到同款症状，先按「状态 / 方案」列的行动方向处理；若你的代码版本比 Issue 新、仍复现，就在对应 Issue 下补充你的环境信息，或搜更新的 Issue/PR。不要因为某个坑曾经「Closed」就断定当前代码一定没这个问题——改版是持续发生的。

### 6.3 部署环境坑（通用项）

排除了登录与改版，剩下多是环境问题。下面这张表只收「通用项」——不依赖某个平台、不依赖某个具体 commit，多数是 Python 工具链与浏览器驱动的经典问题（主要来自社区部署排错经验与 [docs/install.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/install.md) 对照）。

| 坑（部署环境） | 出现场景 | 修复 / 规避 |
| --- | --- | --- |
| f-string 反斜杠 `SyntaxError` | Python **< 3.12**：f-string 表达式里直接写反斜杠 | 先把含反斜杠的值赋给变量，再放进 f-string；或把 Python 升到 3.12（仍满足主线 `<3.13` 约束） |
| venv 创建失败：ensurepip 缺失 | Linux 精简环境（如 Debian/Ubuntu 容器）建虚拟环境报错 | 装系统包 `python3.x-venv`（及 `distutils`）后重试 |
| pip 装 setuptools 卡住 | 旧版 pip 装依赖时卡在 setuptools | 先升级 pip 再重试（见下方命令） |
| Chromium 下载 404 / ECONNRESET | `patchright install chromium` 连不上官方下载源 | 走 npmmirror 镜像重装，或手动下载解压后用 `LOCAL_CHROME_PATH` 指向本机 Chrome（见下方命令） |
| 无头模式下行为不对 | 服务器 headless 跑，登录/上传表现异常 | 检查 `conf.py`：确认 `LOCAL_CHROME_HEADLESS=True`，并把 `DEBUG_MODE` 设为 `False` 搭配（纯无头排错时别开调试等待逻辑） |
| YouTube 连不上（被墙） | 仅 YouTube：Studio 打不开/超时 | `conf.py` 设 `YT_PROXY="http://127.0.0.1:7890"` 显式代理；chromium 不吃系统代理，必须显式给 |

对应的几条修复命令：

```bash
# pip 装 setuptools 卡住：先升级 pip 再重试
pip install --upgrade pip

# Chromium 下载 404 / 断流：走 npmmirror 国内镜像（变量名仍带 PLAYWRIGHT 前缀，照用）
# bash:
PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright" patchright install chromium
# PowerShell:
# $env:PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright"; patchright install chromium
```

> [!tip] 大白话
> Chromium 下载失败可以想成「国际快递被卡在海关」：文件本身没问题，是运输线路不通。npmmirror 镜像相当于国内中转仓，先到国内仓库再发给你，路就通了。实在连镜像也折腾不动，就用本机已装好的 Chrome（`LOCAL_CHROME_PATH`），相当于「不网购，直接去楼下便利店买」。

**一条要警惕的「版本陷阱」**：网上流传的第三方部署排错文（常见于 CSDN）里，常能看到「建议用 Python 3.8」的结论。那类文章针对的是早期 commit 的旧代码；当前主线要求 **Python `>=3.10,<3.13`（3.13 不可用）**，两者直接冲突。照搬旧文的版本结论会把环境装坏——正确的做法是只取其中的**通用部分**（镜像下载、ensurepip、f-string、Chrome 路径），**丢弃版本结论**，版本口径一律以本笔记第 2 章与仓库 [docs/install.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/install.md) 为准。

### 本章小结

- 排错先归类再动手：先判断是「登录/风控」「页面改版」还是「环境问题」，方向对了重试才有意义。
- 登录被风控 → 复用真实浏览器登录态（CDP 9222 导出 / headed），不要硬刚自动化。
- 平台改版元素失效 → 先 `git pull` 升最新代码，再按关键词查 Issues / PR，别拿旧 Issue 结论套新代码。
- GitHub Issues 的坑是「案例」不是「通论」：每条都绑定特定版本与时间点，注意 `#` 号当前 Open / Closed 状态，修复建议（PR#229/#233 等）合入与否需以仓库实时状态确认。
- 部署环境坑多为通用问题：f-string（Python<3.12）、ensurepip、pip 卡 setuptools、Chromium 下载走 npmmirror 镜像、无头行为不对查 `LOCAL_CHROME_HEADLESS` + `DEBUG_MODE` 组合、YouTube 连不上设 `YT_PROXY`。
- 第三方排错文的「Python 3.8」建议针对旧 commit，与现主线 `>=3.10,<3.13` 冲突，勿照搬。

下一章进入收尾：把贯穿全文的「版本口径」再收拢一次，列一份仍待实测的存疑清单，并给出下一步可以往哪些方向继续。

---

## 第 7 章 结语：版本口径与下一步

第 1 章就提醒过：这次大重构把项目切成了「新 CLI 主线」与「旧 Web 版」两个世界。读完全篇，值得最后收一次口——要装得对、跑得通、排得掉错，前提始终是认准文档口径，并把文档没写死的地方亲手实测。本章把全篇的存疑点集中成一张待办清单，再给出接下来可以往哪走。

### 7.1 版本口径与待实测清单

全文命令与配置一律以 **README + docs/install.md + docs/CLI.md** 的当前主线为准。但仓库之外的信息未必同步：sap-doc 文档站与多数第三方教程停留在旧 pip + playwright + Web 版时代，只能当背景对照，不能照敲——例如 CSDN 排错文建议 Python 3.8，与主线 `>=3.10,<3.13` 直接冲突。

写作时我基于文档做了几处推断，下面这些文档没有写死，动手前请在最新代码上实测确认：

- **YouTube 是否真接入 CLI**：README 行文漏列，但 install/CLI 文档含 `sau youtube`，推断已接入，待确认。
- **TikTok 定时发布**：能力矩阵标 ✅，但当前 CLI 未接入，仍走历史 Chrome example。
- **B 站 `--tid` 是否仍必填**：文档示例恒带 `--tid 249`，未说明缺省行为。
- **CLI 成功/失败判定格式**：README/install/CLI 均未说明输出格式、退出码或成功标志，只能以 CLI 输出或实测为准。

> [!warning] 版本口径
> 识别新旧教程有个速判法：命令以 `sau` 开头、依赖走 `uv`、浏览器驱动是 patchright——才属于当前主线；看到 pip + requirements.txt、Web 版、强依赖 LOCAL_CHROME_PATH 的写法，先默认它已过时，别照着执行。

### 7.2 下一步方向

跑通抖音只是起点。后续扩展大致四条线，难度递增：

1. **横向扩平台 / 扩账号**：同一 `sau` 用不同 `--account` 并发多账号，再逐个接入快手、小红书、B 站。
2. **组合定时发布**：`--schedule "YYYY-MM-DD HH:MM"` 仅抖音/快手/小红书/B站/视频号生效，可规划错峰分发节奏。
3. **服务化部署**：登录态固化进 cookie 后，上无头服务器跑 `--headless`，或用 Docker 封装环境。
4. **跟进上游**：平台风控与改版是常态，升最新代码 + 盯 Issues/PR，比硬刚自动化更省力。

进一步资源：

- GitHub README：[dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload)
- 安装与配置：[docs/install.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/install.md)
- CLI 参考：[docs/CLI.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/CLI.md)
- 真实坑位与更新：[GitHub Issues](https://github.com/dreammis/social-auto-upload/issues)

> [!tip] 大白话：先跑通抖音再扩展
> 把抖音想成「样板间」——它是主线维护最全、样例最多的平台。先在样板间把「配置 → 登录 → 发布」整条动线走顺，再拿同一套路子去试别的平台；真出了坑，你才知道是平台的问题还是自己配置的问题，而不是两个变量一起糊成一团。

### 本章小结

- 认准主线文档（README + install.md + CLI.md）；sap-doc 与第三方教程多为旧版，仅作对照。
- 四处存疑点——YouTube CLI、TikTok 定时、B 站 `--tid`、CLI 成功判定——均已标注「需实测 / 升最新代码确认」。
- 扩展路线：多平台 / 多账号 → 定时组合 → 无头 / Docker 部署 → 跟进上游 Issues/PR。
- 一手资料始终在 GitHub 仓库：README、docs、Issues 三者足够撑起后续排错。
