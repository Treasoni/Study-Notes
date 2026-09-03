---
title: 如何用 uv 配置 Python 虚拟环境
tags:
  - python
  - uv
  - 虚拟环境
  - 包管理
  - 学习笔记
created: 2026-09-03
updated: 2026-09-03
status: 已完成
source_project: uv-python-virtualenv
---

# 如何用 uv 配置 Python 虚拟环境

> 面向用过 venv/pip 或 conda 的读者；概念+实战结合、上手实操；全文 7 章顺序阅读，第 5 章含最小可复现 demo。

## 目录

1. 第 1 章 uv 是什么——从 venv/pip/conda 到 uv 的坐标
2. 第 2 章 安装 uv
3. 第 3 章 用 uv 管理 Python 版本与 `.python-version`
4. 第 4 章 创建、激活与使用虚拟环境 `.venv`
5. 第 5 章 项目工作流——`pyproject.toml`、`uv.lock` 与最小可复现 demo
6. 第 6 章 从 pip/venv/conda 平滑迁移到 uv
7. 第 7 章 进阶简谈——索引镜像、缓存与 CI

---

## 第 1 章 uv 是什么——从 venv/pip/conda 到 uv 的坐标

> 面向读者：已用过 venv/pip 或 conda 的开发者。本章是定位章，只谈概念与坐标，不执行命令。

你大概已经习惯这样的流程：`python -m venv .venv` 建环境，`pip install` 装包，再用 `requirements.txt` 锁版本。这套组合能用，但工具多、速度慢、各管一摊。uv 是 Astral 公司用 Rust 编写的「极快 Python 包与项目管理器」，官方目标就是让你少装一长串工具[^c1-a1]。这一章不敲命令，只把 uv 放进你已有的知识坐标：它是什么、和 pip/conda 是什么关系、凭什么快、以及该不该换。

## 1.1 uv 是什么 / 不是什么

uv 的定位很直白：**一个工具取代 pip、pip-tools、pipx、poetry、pyenv、twine、virtualenv**[^c1-a1]——把「建环境、装包、锁版本、管理 Python 版本、跑单文件工具」收进同一个二进制。它由 Astral 出品、Rust 编写，作者的设计动机是做一个「a Cargo for Python」[^c1-a2]。

但它**不是** pip 的又一个封装，也**不是** conda 的全功能替代；它和 pip 的真实边界见 1.3，与 conda 的分工见 1.5。

> [!tip] 大白话：把 uv 想成一把瑞士军刀
> 以前你桌上是一排工具：螺丝刀管建环境（venv）、扳手管装包（pip）、尺子管锁版本（pip-tools）。uv 把它们收进一个刀柄，需要哪件抽哪件。所以它想取代的不是「某一件工具」，而是「那一整排工具」。

## 1.2 四个接口总览

uv 难一句话说清，是因为它对外其实是**四个接口**，分别服务不同场景[^c1-a1]：

| 接口 | 面向场景 | 说明 |
| --- | --- | --- |
| Projects | 项目开发 | 管 `pyproject.toml` 与跨平台锁文件 `uv.lock`（`uv init` / `uv add` / `uv sync` / `uv run`） |
| Scripts | 单文件脚本 | 依赖写进脚本文件的内联声明，随文件走 |
| Tools | 跑命令行工具 | `uvx`（即 `uv tool run`），对标 pipx |
| pip 接口 | 兼容已有习惯 | `uv pip` / `uv venv`，低层兼容层，面向「只想替换 pip」的人 |

前三个偏「项目级」用法；最后一个接口让你现在用 pip/venv 的习惯也能无缝落地，是多数人换过来的第一步。

## 1.3 uv 与 pip 的真实关系

社区常说「uv 是 pip 的替代品」——方向对，但要带边界。

uv **不依赖、也不调用 pip**[^c1-a3]。`uv pip` 是对常见 pip / pip-tools / virtualenv 命令的 drop-in 替代：命令长得一样、用起来一样，底层却是用 Rust 重新实现的。同时官方明确：它**不精确实现**被替代工具的全部行为，越偏离常见工作流，差异越大[^c1-a3]。所以 Overview 页的「drop-in」是泛指，pip 接口页才把范围收敛到 common commands[^c1-a1][^c1-a3]。

> [!tip] 大白话：drop-in 想成「同款插口的充电器」
> 接口形状一样，插上去就能用；但里面电路是自研的，不是把原厂充电器拆开照抄。日常「插上就用」没问题，冷门功能别指望 100% 一致。

## 1.4 性能基准（分清口径）

快是 uv 的第一卖点，但数字要**分口径**看[^c1-a2]：

- **暖缓存**（同一批包此前下载/解析过）：比 pip/pip-tools 快 **80–115x**；
- **无缓存**（冷启动、全要现下载）：快 **8–10x**；
- **创建虚拟环境**：比 `python -m venv` 快约 **80x**，且不依赖本机预装 Python。

而官网 Overview 写的「10–100x」是跨场景**概数**[^c1-a1]，别跟上面的分场景数字混用。结论：uv 不是只在理想条件下快，而是越「缓存命中」越夸张。

> [!tip] 大白话：暖缓存想成「点常点的外卖」
> 头一回要下锅现做（无缓存），之后商家连你口味都记住了，出餐自然快几十倍。uv 把「下载 + 解析 + 组装」都缓存起来，重复安装同一批依赖时只剩本地搬运。

## 1.5 选型坐标（社区观点，仅供参考）

以下坐标**不是官方定位**，来自社区对比帖的总结[^c1-a4]：

| 你的场景 | 社区常用选择 |
| --- | --- |
| 日常纯 Python 开发 | uv |
| 发布库 / 应用 | poetry，或 uv + hatch |
| 数据科学 / ML | conda / mamba |
| 旧项目兼容、求稳 | pip + venv |
| 使用 conda 时 | 留意 Anaconda 的商业许可，社区建议 Miniconda + conda-forge |

一句话：uv 的主场是「纯 Python、想要快与可复现锁文件」；数据科学 / ML 场景社区仍倾向 conda 系，uv 与 conda 如何共存分工留到第 6 章展开。

## 1.6 写给想换过来的人

若决定试，先做三个「习惯预告」（细节后几章展开）：

1. **不再手动 activate**：当环境叫默认名 `.venv` 时，uv 会自动发现并复用，手动激活对 uv 自身常常不是必需；
2. **不再用 pip 装包**：项目依赖改用 `uv add` / `uv sync`，写进 `pyproject.toml` 并生成 `uv.lock`；
3. **用 `uv run` 取代「先 activate 再 python」的双命令**：一条命令在项目环境里跑脚本或测试。

其中第 3 条是换过来后最快能感受到的「手感变化」。

### 本章小结

- uv 是 Astral 用 Rust 写的包与项目管理器，目标是把 pip / pip-tools / pipx / poetry / pyenv / twine / virtualenv 收进一个工具。
- 对外是 Projects / Scripts / Tools / pip 四个接口，可当「项目工具」用，也可当「pip 兼容层」用。
- 它不依赖、不调用 pip；drop-in 覆盖常见命令，冷门行为不保证一致。
- 性能口径要分开：暖缓存 80–115x、无缓存 8–10x、建 venv 约 80x；Overview「10–100x」只是概数。
- 选型看场景：日常纯 Python 用 uv，发库用 poetry / uv+hatch，数据科学用 conda / mamba，旧项目兼容用 pip+venv（社区观点）。

下一章开始动手：全平台安装 uv，并处理 Windows 下安装时最容易踩的执行策略问题。

---

## 第 2 章 安装 uv

> 本章目标：把 uv 装到本机并验证可用。读完你将掌握「独立安装器 + 包管理器」两条安装路径、对应的两种升级通道，以及两个高频注意事项。

第 1 章建立了 uv 的坐标，动手第一步是安装。uv 是 Rust 编写的独立可执行程序，官方提供全平台统一的安装方式，也支持接入你已有的包管理器[^c2-b1]。本章按「安装 → 验证 → 升级 → 注意事项」推进，你只需选一条路径执行。

### 2.1 独立安装器（官方推荐）

独立安装器会下载 uv 的可执行文件到用户目录，**不需要预先装 Python**，这是它相比 `pip install` 的一个关键差异。

**macOS / Linux**（bash/zsh）：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

`curl` 下载官方安装脚本，`| sh` 把脚本交给当前 shell 执行。想装指定版本，可在 URL 中插入版本号，如 `https://astral.sh/uv/0.12.9/install.sh`（具体版本以你需要的为准，装完用 `uv --version` 核对）。

**Windows**（PowerShell 一行）：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

`irm`（`Invoke-RestMethod`）下载脚本，`iex`（`Invoke-Expression`）执行它。

> [!tip] 大白话：`-ExecutionPolicy ByPass` 只是一次性门禁卡
> 把 PowerShell 的「执行策略」想成大楼门禁的权限等级。`ByPass` **不是**帮你把门禁永久调松，而是像一张「前台访客卡」——只放行你正在执行的这一条命令，跑完即失效，系统原本的策略设置分毫未动。所以这条命令可以放心用。

### 2.2 包管理器方式

若你已在用某个包管理器，也可以让它接管 uv，后续升级跟随该包管理器的节奏：

```bash
# macOS：Homebrew
brew install uv

# Windows：winget（系统自带）
winget install --id=astral-sh.uv -e

# Windows：scoop
scoop install main/uv

# 通用：pipx（需先有 Python + pipx 环境）
pipx install uv
```

各自的适用场景：Homebrew 适合 macOS（及装了 brew 的 Linux）；winget 是 Windows 开箱即用的选择；scoop 适合已用 scoop 管理便携软件的 Windows 用户；pipx 适合「机器上已有一套 Python + pipx」的人——虽然 uv 的目标之一正是取代 pipx，但用 pipx 装 uv 仍是官方认可的一条通道，便于集中管理。

> [!tip] 大白话：安装通道决定升级通道
> 把安装 uv 想成装空调：独立安装器像厂商直接派人上门，自带全套、独立维护；包管理器像走物业统一采购，装在哪、何时升级都听物业安排。两条路都通，但**升级方式跟着安装方式走**——这正是 2.3 的核心。

### 2.3 验证与升级

装完先确认版本：

```bash
uv --version
```

能看到类似 `uv 0.x.y` 的输出即安装成功。

升级命令取决于当初的安装方式[^c2-b1]：

- 独立安装器安装 → uv 自己升级自己：

```bash
uv self update
```

- 其它方式（如 pipx）→ 当作普通包升级：

```bash
pip install --upgrade uv
```

> 用 brew / winget / scoop 安装的，升级直接走对应包管理器（如 `brew upgrade uv`），规则与其它包完全一致。

顺带埋个伏笔：每次 uv 发布都会冻结它「认识」的 Python 版本集，升级 uv 往往是让新版 uv 能管理更新 Python 版本的前提，第 3 章会再遇到。

### 2.4 注意事项

**1) `UV_NO_MODIFY_PATH=1`：关掉 shell profile 改写**

独立安装器（以及 `uv self update`）默认会在你的 shell 配置文件里追加 uv 的 PATH 条目，让下次开终端就能直接用 `uv`。如果你不希望它动配置文件（例如 PATH 由自己统一管理），安装前设这个环境变量：

```bash
# macOS / Linux
UV_NO_MODIFY_PATH=1 curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows PowerShell
$env:UV_NO_MODIFY_PATH = "1"
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> [!tip] 大白话：`UV_NO_MODIFY_PATH=1` = 只装别挪
> 默认安装器像一支装修队：装完 uv 还「顺手帮你把家具（PATH 配置）挪到顺手的位置」。多数人觉得贴心；若你的配置有自己的规矩，设 `UV_NO_MODIFY_PATH=1` 等于叮嘱一句「只装别挪」。

**2) Windows `-ExecutionPolicy ByPass` 只影响当前命令**

PowerShell 默认执行策略可能是 `Restricted`，会阻止脚本运行。安装命令里的 `-ExecutionPolicy ByPass` 只对**本次启动的 powershell 进程**放行，不会修改系统执行策略[^c2-c5]。若之后手动运行 `.ps1`（例如第 4 章激活虚拟环境的 `Activate.ps1`）仍被拦，那是另一回事，修复方法到第 4 章展开。

### 本章小结

- 独立安装器：macOS/Linux 用 `curl -LsSf https://astral.sh/uv/install.sh | sh`；Windows 用 `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`，且 `ByPass` 不改系统策略。
- 包管理器：`brew install uv` / `winget install --id=astral-sh.uv -e` / `scoop install main/uv` / `pipx install uv`，按平台与习惯选一条即可。
- 验证：`uv --version`。
- 升级随安装通道：独立安装器用 `uv self update`，其它用 `pip install --upgrade uv`（或对应包管理器）。
- 不想被改 shell 配置时，安装前设 `UV_NO_MODIFY_PATH=1`。

### 下一章预告

uv 已经能跑了。它的另一个野心是「连 Python 本身一起管」——下一章我们用它安装指定版本的解释器，并用 `.python-version` 把每个项目钉在对应版本上。

---

## 第 3 章 用 uv 管理 Python 版本与 `.python-version`

过去管 Python 版本靠系统预装、pyenv 源码编译或 conda，项目一多就乱，还常出现"这台机器能跑、那台跑不了"。本章回答三个问题：Python 从哪来、版本听谁的、怎么让每个目录声明自己想要的版本。

### 3.1 为什么需要：把 Python 装成"托管"的

很多坑源于"解释器得先于工具存在"。uv 反其道：它不依赖系统预装 Python，而是内置一套 Python 下载与管理能力，使用的是 **python-build-standalone**——由 Astral 预编译、自包含、免安装的解释器发行版。[^c3-B2] 你装的是 uv，Python 则在第一次需要时由 uv 自动下载，放进自己的托管目录，一台新机器装上 uv 就等于随时能调出任意版本的 Python。

> [!tip] 大白话
> 把 uv 托管的 Python 想成"应用商店里预装好的 App"，不用你自己去官网下载安装包再配置环境变量。所以"装 uv"和"装 Python"解绑了——先有 uv，Python 随用随取。

### 3.2 核心命令：install / list / upgrade

```bash
uv python install            # 装最新，仅版本化入口 python3.13
uv python install --default  # 额外装 python / python3 入口
uv python install 3.12       # 装指定版本
uv python install 3.11 3.12  # 一次装多个
uv python install pypy@3.13  # 其它实现（PyPy）
uv python list               # 列出可用/已安装
uv python upgrade 3.12       # preview：升级 3.12 的 patch
```

`--default` 决定是否生成不带版本号的 `python`/`python3` 入口，方便在 shell 里直接调用。想让普通 shell 的 `python` 也指向托管版本，可执行 `uv python update-shell` 更新 shell 配置。[^c3-B2]

### 3.3 版本请求语法

install、venv、pin 接受的"版本"其实是一段**版本请求**（version request），常用写法：[^c3-B3]

- `3.12`：3.12 的最新 patch，不精确锁死小版本
- `>=3.12,<3.13`：范围约束
- `cpython@3.12`：指定 CPython 实现
- 解释器路径：直接给某个 python 可执行文件路径

```bash
uv python find '>=3.11'   # 查看这段请求实际解析到哪个解释器
```

> [!tip] 大白话
> 把版本请求想成点单时的描述：`3.12` 是"来一份最新的 3.12"，`>=3.12,<3.13` 是"3.12 到 3.13 之间的都行"。uv 按描述去匹配货架上有的解释器，而不是死等一个精确文件。

### 3.4 `.python-version`：让目录声明版本

```bash
uv python pin 3.12           # 在当前目录生成 .python-version
uv python pin --global 3.12  # 写用户级配置，作为默认版本
```

`uv python pin` 的产物就是 `.python-version`，内容是"版本请求"而非精确小版本，这样 `3.12` 能自动吃到后续 patch 更新。uv 在决定用哪个解释器时，会从**当前目录逐级向上**查找最近的 `.python-version`——父目录声明、子目录可以继承。[^c3-B3]

> [!tip] 大白话
> `.python-version` 像贴在某层楼的"点单标签"。uv 从你站的位置往上逐级翻找，谁最近就听谁的——不用每个房间都贴。

### 3.5 查找优先级与开关

本机没有请求的版本时会自动下载吗？查找顺序与开关如下：[^c3-B3]

- 查找顺序：**managed 目录 → PATH → Windows 注册表 / Microsoft Store**，默认策略 `python-preference=managed`，即优先用 uv 自己托管的版本
- 缺失自动下载：下面的命令在本机没有 3.11 时会先自动下载再建环境 [^c3-B2]
- 强制只用系统解释器：加 `--no-managed-python`，不走托管目录、不自动下载 [^c3-B2]

```bash
uv venv --python 3.11     # 缺 3.11 时先自动下载，再建 .venv
uv venv --python 3.11 --no-managed-python  # 只用 PATH / 系统解释器
```

### 3.6 易错点：新版本 Python ≠ 换个命令就能装

每个 uv 发布都会**冻结**它认识的可用版本集。新版 Python 发布后，旧版 uv 去装会报"版本不可用"——不是网络问题，而是旧 uv 根本不认识这个新版本，此时要升级 uv 本身。版本够不够新，以 `uv --version` 为准。[^c3-B2]

> [!tip] 大白话
> 把 uv 想成播放器、Python 想成光盘：老播放器（老 uv）放不了新格式的光盘（新版 Python）。换个新播放器（升级 uv）才读得出来。

### 本章小结

- uv 内置 Python 管理（python-build-standalone），无需预装解释器。
- `uv python install / list / upgrade` 负责装、查、升；`--default` 控制是否生成 `python`/`python3` 入口。
- 版本参数是"请求"语法：`3.12`、`>=3.12,<3.13`、`cpython@3.12`、解释器路径都合法。
- `uv python pin` 写 `.python-version`（`--global` 写用户级），uv 自当前目录向上逐级查找。
- 查找优先级：managed → PATH → Windows 注册表 / Microsoft Store；`--no-managed-python` 强制只用系统解释器。
- 新版 Python 需新版 uv 才认识，版本以 `uv --version` 为准。

下一章把"解释器"升级成"隔离环境"：用 `uv venv` 一行建出 `.venv`，并列清楚 Windows / macOS / Linux 的激活与停用命令。

---

## 第 4 章 创建、激活与使用虚拟环境 `.venv`

> 面向读者：已会用 venv/pip 或 conda。本章动手建环境，并回答一个绕不开的困惑——到底要不要手动 activate。

前两章已装好 uv、并能按需安装指定版本的 Python。本章解决动手第一问：把这些 Python 版本装进「每个项目一个」的隔离环境 `.venv`，掌握三种创建方式、全平台激活与停用，以及 uv 自动发现与手动激活的真实分工。

### 4.1 创建虚拟环境：默认、自定义名、指定版本

`uv venv` 是 uv 版的 `python -m venv`，默认在当前目录生成隐藏目录 `.venv`；若本机没有目标 Python，它会自动下载后再建，无需你先手动安装[^c4-b4]。三种常见姿势：

```bash
uv venv                  # 默认建 .venv
uv venv my-name          # 自定义目录名/路径
uv venv --python 3.11    # 指定版本；缺则自动下载
```

自定义名适合需要非默认目录的项目，代价是之后的激活与自动发现都要手动指向它。

### 4.2 全平台激活与停用

激活的本质，是把该环境存放命令的目录插进 shell 的 PATH 最前，让 `python`、`pip` 落到环境内部。macOS/Linux（bash/zsh/fish/csh）与 Windows（PowerShell/CMD）并列给出[^c4-b4]：

```bash
source .venv/bin/activate        # macOS/Linux bash/zsh
source .venv/bin/activate.fish   # fish
source .venv/bin/activate.csh    # csh/tcsh
```

```powershell
.venv\Scripts\activate           # Windows PowerShell（uv 官方当前写法）
.\.venv\Scripts\Activate.ps1     # PowerShell 显式 .ps1（venv 通行写法）
```

```bat
.\.venv\Scripts\activate.bat     # Windows CMD
```

退出统一用：

```bash
deactivate
```

> [!tip] 大白话：activate 像给命令解析换一张指向新家的地图
> activate 不神秘——它把你 shell 找命令的 PATH 最前段换成 `.venv` 的 `Scripts`/`bin` 目录，`python`/`pip` 随之指进环境；`deactivate` 撤掉这段、恢复系统默认。

补充：CMD 的 `activate.bat` 与显式 `Activate.ps1` 属 Python venv 通行写法；uv 官方文档当前只给 PowerShell 一行 `.venv\Scripts\activate`，此处按实操经验并列补全、便于查用[^c4-c6]。

### 4.3 uv 自动发现：激活对 uv 常非必需

环境名是默认 `.venv` 时，uv 会**自动发现并复用**——`uv venv` 之后直接 `uv pip install ruff` 也能正确装进 `.venv`，不必先激活[^c4-b4]。要分清两类消费者：IDE、你在 shell 敲的 `python`、非 uv 工具看的是「激活状态」；uv 命令看的是「目录约定」。前者需要 activate，后者不需要。

> [!tip] 大白话：把 `.venv` 想成固定钥匙位
> uv 每次进门先摸默认钥匙位（`.venv`），摸到就直接用，不用你掏出门禁卡再刷一次（手动激活）。但 IDE 不认识这个约定，仍要你亲自「开门」。

### 4.4 环境发现顺序

会变更环境的 uv 命令，按以下顺序找环境[^c4-b4]：

1. 激活的 `VIRTUAL_ENV`（你手动激活的环境）；
2. 激活的 conda `CONDA_PREFIX`；
3. 当前目录或最近父目录的 `.venv`。

含义：若你手动激活了 A 环境，再在 B 项目里跑 uv，它用的是 A 而不是 B 的 `.venv`。

### 4.5 `--system` 的适用场景与限制

```bash
uv pip install --system ruff   # 装进系统解释器（约等 --python $(which python)）
```

`--system` 专供 CI、容器这类没有项目环境的场景[^c4-b4]。限制：它绕过了默认保护——不带 `--system` 时 uv 会**忽略非虚拟解释器**，防止误装进系统 Python。

### 4.6 Windows 坑：PowerShell 执行策略挡 `Activate.ps1`

Windows 上 PowerShell 默认执行策略 `Restricted` 会拦截 `Activate.ps1`，报「禁止运行脚本」。修复（仅对当前用户生效）[^c4-c5]：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

`RemoteSigned` 放行本地脚本与带可信签名的远程脚本。省事路线：不碰策略，改用 `uv run` 免激活（见 4.3），这也是社区更推荐的做法[^c4-c6]。

> [!tip] 大白话：执行策略像小区门卫
> `Restricted` 是门卫谁都不放；`RemoteSigned` 放行「本楼住户（本地脚本）」和「持可信证件的外人（有签名脚本）」。只在当前用户开这个口子即可，不必全局放行。

### 本章小结

- `uv venv` 建默认 `.venv`；`my-name` / `--python 3.11` 自定义；缺 Python 自动下载。
- 激活命令分平台：Unix `source .venv/bin/activate`（及 `.fish`/`.csh`）；Windows PS `.venv\Scripts\activate` 或 `Activate.ps1`、CMD `activate.bat`；`deactivate` 退出。
- 默认名 `.venv` 时 uv 自动发现并复用，激活对 uv 常非必需；shell 与 IDE 仍要激活。
- 环境发现顺序：`VIRTUAL_ENV` → `CONDA_PREFIX` → 就近 `.venv`。
- `--system` 给 CI/容器，绕过「忽略非虚拟解释器」保护，别在本地滥用。
- Windows 激活被执行策略挡：`RemoteSigned -Scope CurrentUser`，或干脆 `uv run` 免激活。

下一章进入项目工作流：`uv init` / `uv add` / `uv sync` / `uv run` 与跨平台锁文件 `uv.lock`——届时你会发现手动激活基本可以「退休」了。

---

## 第 5 章 项目工作流——`pyproject.toml`、`uv.lock` 与最小可复现 demo

前面几章把 uv 装好、让它接管 Python 版本，也手动建过 `.venv`。但真实项目里你不会天天手动建环境——需要把「项目要什么依赖、锁到哪个版本、怎么跑」固化成可提交 Git 的产物，这正是 uv 的 Projects（项目模式）接口[^c5-A1]。本章用 `hello-demo` 把 `uv init` 产物、`pyproject.toml`、`uv.lock` 和 add/remove/sync/run 日常循环走通，最后给一个从零跑通的最小 demo。

### 5.1 `uv init`：一条命令生成一个规范项目

在空目录执行（官方示例为 `hello-world`，本章统一 `hello-demo`，结构一致[^c5-B5]）：

```bash
uv init hello-demo && cd hello-demo
```

uv 一次生成这些产物[^c5-B5]：

```text
hello-demo/
├── .gitignore          # Python/uv 常用忽略项（.venv、__pycache__ 等）
├── .python-version     # 记录本项目用哪个 Python 版本
├── pyproject.toml      # 项目元信息 + 依赖声明
├── README.md
└── src/
    └── hello_demo/
        └── __init__.py
```

- `.gitignore` 预填好忽略项，避免把 `.venv` 误提交进 Git。
- `.python-version` 钉住本项目的 Python 版本，后续建 `.venv` 用哪个解释器以它为准。
- `src/hello_demo/` 是 src 布局：包代码收进 `src/` 下，避免从仓库根意外导入。

此刻**还没有 `uv.lock`**——它要等第一次 `uv add` / `uv sync` / `uv run` / `uv lock` 才自动生成[^c5-B5]。

> [!tip] 大白话
> `uv init` 像开发商交付「毛坯房 + 水电图纸」：目录、版本约定、忽略规则一次备齐，你只管填代码、声明依赖。相比自己 `mkdir` + 手写 `requirements.txt`，它先把容易漏的坑堵上。

### 5.2 `pyproject.toml`：用 `[project].dependencies` 声明依赖

`uv init` 生成的 `pyproject.toml` 大致如下（以你本机 uv 生成的为准）：

```toml
# pyproject.toml（uv init 生成、尚未加依赖）
[project]
name = "hello-demo"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []
```

`[project].dependencies` 声明**直接依赖**（PEP 621）：只写项目直接要的包，传递依赖交给解析器。

```bash
uv add requests
```

这一条命令完成三件事：把依赖写进 `dependencies`（形如 `"requests>=2.32.0"`，数值以解析结果为准）、生成/更新 `uv.lock`、把包装进 `.venv`[^c5-B5]。

与传统 `requirements.txt` 的关键差异：

| 维度 | `pyproject.toml` | `requirements.txt` |
|---|---|---|
| 项目身份 | 含 name/version/requires-python | 只有一列包需求 |
| 消费方 | uv/构建后端均读，单一事实源 | 主要给 `pip install -r` |
| 直接 vs 传递 | 只声明直接依赖，锁定交给 lockfile | 常用 freeze 把传递依赖拍平 |
| 版本策略 | 声明范围，精确锁定另存 uv.lock | 范围与 pin 混在一文件 |

> [!tip] 大白话
> `pyproject.toml` 是**购物清单**：写清要买什么、接受什么价位范围。`uv.lock` 是**结账小票**：每件商品具体版本、校验和多少。老式 `requirements.txt` 常把清单和小票糊在同一张纸上，一改就乱。

### 5.3 `uv.lock`：跨平台精确锁，提交、别手改

要点[^c5-B5]：

- **跨平台精确锁定**：uv 把整棵依赖树在 Windows / macOS / Linux 上的确切版本、来源与哈希都解析进同一份 lockfile。提交后任何人 clone、任何 CI 上 `uv sync`，装出的都是同一套。
- **提交版本库**：它就是该入库的文件（`.gitignore` 不会忽略它）。
- **不要手改**：它是机器生成的一致性快照，手改会让 lockfile 与 pyproject 对不上。升级走命令（5.4），别用编辑器。

> [!tip] 大白话
> `uv.lock` 是**配方的定格照**：把「每批料用的哪个批次」拍下来存进 Git。手改它像手改银行对账单——不该做，要改走正规流程。有了它，换电脑、同事 clone、CI 构建都不至于「在我这能跑、在你那炸」。

### 5.4 日常循环：add / remove / sync / lock

依赖的增删改都通过命令完成，命令会同步维护 pyproject、uv.lock、.venv 三处：

```bash
uv add requests                 # 加入依赖（三处同步更新）
uv add 'requests==2.31.0'       # 带精确版本约束（== 两侧加引号防 shell 展开）
uv remove requests              # 移除依赖
uv sync                         # 按 pyproject/uv.lock 把 .venv 同步到一致
uv lock --upgrade-package requests   # 只升级 requests 一个包（更新 uv.lock）
```

- `uv add` / `uv remove` 自动同步三处；要精确钉版本就用 `uv add 'requests==2.31.0'`[^c5-B5]。
- `uv sync` 是「按单收货」：别人 clone 仓库后跑它（或直接 `uv run`），就能得到一致环境[^c5-B5]。
- `uv lock --upgrade-package requests` 单包升级；想全量升级用 `uv lock --upgrade`。锁更新后想让 `.venv` 里的包也换新，再跑一次 `uv sync`。

### 5.5 `uv run`：免激活 + 一致性校验

```bash
uv run hello-demo
uv run python -c "import requests; print(requests.__version__)"
```

- **免手动激活**：自动发现项目 `.venv`（默认名 `.venv` 时自动复用[^c5-B4]）并在其中跑命令，Windows 上绕开「执行策略挡 `Activate.ps1`」的坑。
- **每次运行前校验** lockfile ↔ pyproject ↔ 环境是否一致，不一致先补齐再执行[^c5-B5]。首次 `uv run` / `uv sync` / `uv lock` 会自动创建 `.venv` 和 `uv.lock`[^c5-B5]。
- 第一行执行 uv 默认模板注册的同名命令入口（console script），会打印一句问候语；若你的模板没注册该入口，用第二行同样能验证链路。
- 默认**不清理多余包**：自动补装按需补齐，不会删掉 `.venv` 里 lockfile 之外的包[^c5-B5]。

> [!tip] 大白话
> `uv run` 像**刷临时工牌进项目专柜**：每次进门，闸机自动核对清单（pyproject）、小票（uv.lock）和柜里存货（.venv）是否一致，不一致先补货再放行。所以可以忘掉「先 activate 再跑」的两步——一条 `uv run` 搞定。

### 5.6 最小可复现 demo：从零到跑通

在**全新空目录**把主线串起来（安装细节见第 2 章）：

```bash
# 1) 安装 uv（macOS/Linux；Windows 用下方 powershell 替代）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2) 安装并钉住 Python 3.12
uv python install 3.12 && uv python pin 3.12

# 3) 初始化项目 + 显式创建虚拟环境（项目流中 uv add/sync 也会自动建 .venv，这里显式演示）
uv init hello-demo && cd hello-demo && uv venv

# 4) 加依赖并直接运行（无需手动 activate）
uv add requests
uv run python -c "import requests; print(requests.__version__)"
```

Windows 用户把第 1 步替换为：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

每步产物：

| 步骤 | 命令 | 产生/改变的产物 |
|---|---|---|
| 1 | 安装 uv | `uv` 可执行程序（`uv --version` 验证） |
| 2 | `uv python install 3.12` + pin | 托管 CPython 3.12 + `.python-version` |
| 3 | `uv init` + `uv venv` | 项目骨架（`.gitignore` / `.python-version` / `pyproject.toml` / `README` / `src/hello_demo/`）+ `.venv` |
| 4 | `uv add` + `uv run` | pyproject 依赖声明 + **`uv.lock` 首次生成** + `.venv` 内装好 requests；`uv run` 输出版本号 |

最后输出形如 `2.32.3`（以你实际解析到的版本为准）。跑完后把 `pyproject.toml` 和 `uv.lock` 一起提交进 Git——任何人 clone 后 `uv sync` 就能装出和你此刻一致的环境，这就是「最小可复现」的含义。

### 本章小结

- `uv init` 生成 `.gitignore` / `.python-version` / `pyproject.toml` / `README` / src 布局；`uv.lock` 待首次 add/sync/run/lock 才出现。
- `pyproject.toml` 的 `[project].dependencies` 只声明直接依赖；与 `requirements.txt` 的差别在身份元信息与 lockfile 分工。
- `uv.lock` 是跨平台精确锁：提交版本库、勿手改，可复现性靠它保证。
- 日常循环是 `uv add` / `uv remove` / `uv sync` / `uv lock --upgrade-package requests`，命令自动同步 pyproject、uv.lock、.venv 三处。
- `uv run` 免激活、每次校验一致性，默认只补装不清理多余包。

下一章把镜头转向「旧项目」：如何把 `requirements.txt` + venv/conda 的老工作流平滑迁到 pyproject + uv.lock 的项目模式。

---

## 第 6 章 从 pip/venv/conda 平滑迁移到 uv

第 5 章带你从零建了 uv 项目；但现实里你大概率背着若干 venv+pip 甚至 conda 的存量工程。本章讲老项目如何低成本切到 uv：把旧依赖清单语义对齐到 `pyproject.toml` + `uv.lock`，日常命令换手，无需推翻全部习惯。

### 6.1 迁移路线图：旧项目 → uv 项目

存量 pip/venv 项目迁到 uv 项目流，官方迁移指南给出的主干只有四步[^c6-1]：

```bash
cd my-old-project
uv init                      # 补出 pyproject.toml / .python-version 骨架
uv add -r requirements.in    # 把顶层依赖声明进 pyproject.toml
uv add --dev -r requirements-dev.in   # dev 依赖单独分组（见 6.3）
uv sync                      # 依 pyproject/uv.lock 建/同步 .venv 与 uv.lock
uv run python -m pytest      # 之后的命令都走 uv run
```

对照第 5 章项目流：`uv add` 把依赖**声明**进 `pyproject.toml` 并写锁，`uv sync` 按 `pyproject + uv.lock` 一键建好 `.venv`，`requirements.txt` 的手工维护循环从此退役。

> [!tip] 大白话
> 把迁移想成「搬家重装修」：`uv init` 是给老房子补一张新户型图（`pyproject.toml`），旧家具清单（requirements）重新登记一遍，`uv sync` 按新图纸统一配齐——而不是把每件旧家具原样搬进去。所以重点是「按新分类重新登记」，不是「照旧复制」。

### 6.2 requirements 迁移：导 `.in` 源清单，用 `-c` 保留旧锁

这是迁移中最容易踩的语义坑。先分清两种文件：

- `requirements.in`：**源清单**，只写顶层直接依赖，由人维护。
- `requirements.txt`：**锁定产物**，`pip freeze` 风格，含全部间接依赖与精确版本。

uv 项目里对应关系是：`pyproject.toml` = 源清单，`uv.lock` = 锁。所以迁移要导入**源清单**，而不是把锁文件整体当直接依赖再解析一遍：

```bash
# 情形 A：有 .in 源清单，直接导入
uv add -r requirements.in

# 情形 B：只有 .txt 锁定文件 → 源清单与旧锁一起给，旧锁作约束
uv add -r requirements.in -c requirements.txt
```

`-c requirements.txt` 把旧锁定当作**约束文件（constraints）**传入：uv 解析以旧版本为边界，避免整体浮动升级；新 `uv.lock` 收敛后旧 `.txt` 即可退役[^c6-1]。

> [!tip] 大白话
> `.in` 是「购物清单」（你想买什么），`.txt` 是「收银小票」（每件精确到条码）。迁移时照购物清单买；小票只当「别比这贵」的参考上限（`-c`）。直接拿小票当清单照抄，等于把上次凑单的结果原样固化，下次就没法理性升级了。

### 6.3 dev 依赖分组

测试、lint、文档构建这类依赖不该和运行依赖混在一起。迁移时把 dev 清单单独导入：

```bash
uv add --dev -r requirements-dev.in   # 示意：requirements-dev.in 为 dev 源清单
```

`--dev` 让包进入独立的开发依赖分组，与主依赖分开记录；开发期 `uv sync`/`uv run` 会一并装进 `.venv`（第 7 章 CI 命令会再见 dev 参数）。

### 6.4 日常命令替换表

切换后最常改的五个动作：

| 场景 | 旧做法（pip/venv） | 新做法（uv） | 备注 |
|---|---|---|---|
| 给项目加依赖 | `pip install requests` | `uv add requests` | 自动更新 pyproject + uv.lock + .venv |
| 按清单装齐依赖 | `pip install -r requirements.txt` | `uv sync` | 依 pyproject/uv.lock，不再手维护清单 |
| 跑测试 | `python -m pytest` | `uv run python -m pytest` | 免手动激活 |
| 激活环境 | `source .venv/bin/activate`（macOS/Linux）/ `.venv\Scripts\activate`（Windows） | `uv run ...` | 项目命令不再需要 activate |
| 低层临时装包（非项目流） | `pip install ...` | `uv pip install ...` | 第 1 章介绍的 pip 兼容接口 |

> [!tip] 大白话
> 把「手动激活」想成戴工牌进办公区，下班再摘。`uv run` 是每次命令自动给你刷一张临时工牌，跑完即走——所以「戴牌 → 跑命令 → 摘牌」三步并成一步。

### 6.5 与 conda 并存：uv 管包、conda 管环境

先分清 uv 的两类命令行为不同[^c6-2]：

- **pip 兼容层**（`uv pip` / `uv venv`）：变更环境的命令按发现顺序找环境——激活的 `VIRTUAL_ENV` → 激活的 conda `CONDA_PREFIX` → 当前/最近父目录的 `.venv`。所以当你激活了某个 conda 环境、又没有 `VIRTUAL_ENV` 时，`uv pip install` 会装进**当前 conda 环境**。
- **项目工作流**（`uv sync` / `uv add` / `uv run`）：默认只操作项目自己的 `.venv`，**不跟随 conda**。

据此推荐的共存分工：**uv 管 PyPI/Python 包**（解析、锁定、纯 Python 包），**conda 管 CUDA、编译器这类需贴系统库的包**；避免同环境两套包管理器混装。

> [!warning] `UV_PROJECT_ENVIRONMENT` 的坑
> 有人想让项目命令直接装进当前 conda 环境，就设置 `UV_PROJECT_ENVIRONMENT` 指向 conda 前缀。社区 issue 经验（uv issues #7829/#11315/#15783）显示：当该变量指向的目录**非空且不是标准 PEP 405 venv** 时，uv 会直接报错；即使绕过去也等于放弃了 `.venv` 隔离[^c6-3]。**不要把它当常规推荐用法**——真想装进 conda 环境，用上面的 `uv pip` 兼容层即可，别把项目 `sync` 指过去。

> [!tip] 大白话
> uv 和 conda 分家管：conda 像物业管水电和承重墙（CUDA、编译器要贴着系统库走），uv 像软装管家具（PyPI 包）。物业不用替你挑沙发，软装队也别去砸承重墙——同一间房两拨人同时施工必打架。

### 6.6 迁移坑速查

| 坑 | 后果 | 解法 |
|---|---|---|
| 激活 `.venv` 后混用系统 `pip install` | uv 与 pip 双轨污染 `.venv`/系统 | 统一用 uv；项目依赖一律 `uv add` |
| `uv add -r requirements.txt` 直接导锁文件 | 把历史锁定当直接依赖**重解析**，版本漂移 | 导入 `.in` 源清单；或 `-c requirements.txt` 保留旧锁 |
| 手改 `uv.lock` | 锁与 pyproject 失配，可复现性丢失 | 升级走 `uv add` / `uv lock`，不手改 |
| `uv.lock` 不入库 | 队友/CI 无法复现同一套依赖 | 把 `uv.lock` 提交进版本库[^c6-1] |
| 在 conda 环境跑 `uv sync` 指望装进 conda | 不生效（项目流默认只动 `.venv`） | 用 `uv pip` 兼容层；用 `UV_PROJECT_ENVIRONMENT` 前先确认语义 |

### 本章小结

- 迁移主干四步：`uv init` → `uv add -r <源清单>` → `uv add --dev -r <dev清单>` → `uv sync`，之后全走 `uv run`。
- 导入依赖认准 `.in` 源清单；只剩 `.txt` 时用 `-c` 把它当约束保留旧锁，别直接 `add -r` 锁文件。
- 日常命令替换：`pip install` → `uv add`，`pip install -r` → `uv sync`，`python -m pytest` → `uv run python -m pytest`，手动 activate → `uv run`。
- 与 conda 共存：`uv pip` 跟随激活的 conda，项目 `uv sync` 只动 `.venv`；uv 管 PyPI 包、conda 管 CUDA/编译器，避免同环境混装。
- `UV_PROJECT_ENVIRONMENT` 指到非空非 PEP 405 venv 会报错（社区 issue 经验），不要作为常规方案。

下一章进入进阶简谈：国内镜像与索引怎么配、缓存目录与清理、GitHub Actions 接入，最后把全书坑汇总成一张速查表。

---

## 第 7 章 进阶简谈——索引镜像、缓存与 CI

本章解决三个从"本地跑通"走向"日常与团队协作"的现实问题：国内网络下如何让 uv 从镜像源快速取包、uv 的缓存存在哪里又该如何清理、以及怎样把第 5 章的 `uv sync`/`uv run` 变成 GitHub Actions 里可复现的 CI。读完你会得到一张覆盖第 3/4/6/7 章常见坑的汇总速查表，日后遇到问题先查表再动手。

### 7.1 镜像与索引：让 uv 从哪下载包

**先把坑摆出来：pip 的 `index-url` 不作用于 uv。** 很多从 pip 迁过来的人第一反应是改 `pip config` 或 `index-url`，但 uv 不读 pip 配置。给 uv 指定索引要走它自己的两套入口：`pyproject.toml` 的 `[[tool.uv.index]]`，或环境变量 `UV_DEFAULT_INDEX` / `UV_INDEX`。[^c7-C2]

> [!tip] 大白话
> 把"索引"想成固定的进货市场。pip 里配的 index-url 是写给"旧市场"的地址，uv 这个新摊贩根本不看；你得亲口告诉 uv 去哪个市场进货（`[[tool.uv.index]]` 或 `UV_DEFAULT_INDEX`），它才会去那里拿货。

**在 pyproject.toml 声明索引：**

```toml
# pyproject.toml
[[tool.uv.index]]
name = "my-mirror"                             # 索引名，后面环境变量/凭据会引用它
url = "https://mirror.example.com/simple"      # 占位符，替换为你实际使用的镜像 URL
default = true                                 # 设为默认源，移除 PyPI 兜底
```

`default = true` 的含义：不再把官方 PyPI 当作兜底源，凡是没有显式匹配到其它索引的包，都只从这个源解析。若只声明索引而不设 `default`，PyPI 仍然是兜底源。[^c7-C2]

**环境变量写法（通用写法 + 国内镜像提示）：**

```bash
# 单默认源：URL 替换为清华、阿里云等国内实际可用的镜像地址
export UV_DEFAULT_INDEX="https://mirror.example.com/simple"

# 命名索引：<name>=<url> 形式，供凭据/精确匹配引用
export UV_INDEX="my-mirror=https://mirror.example.com/simple"
```

> [!note] 国内镜像 URL 说明
> 官方文档未给出清华/阿里等国内镜像的 uv 配置样例，上面的 `mirror.example.com` 是占位符，请替换为你所在网络实际可用的镜像地址后再使用。Windows PowerShell 对应写法是 `$env:UV_DEFAULT_INDEX="..."`；要长期生效就写入系统环境变量，而非仅当前会话。

**私有源凭据：走环境变量，不写入 uv.lock。** 若索引需要认证，用 `UV_INDEX_{name}_USERNAME` 与 `UV_INDEX_{name}_PASSWORD`（`{name}` 即 `[[tool.uv.index]]` 里的索引名）。凭据只存在于本机/CI 环境，不会进入会被提交版本库的 `uv.lock`。[^c7-C2]

> [!tip] 大白话
> 凭据像保险箱钥匙：把钥匙写进仓库（uv.lock）等于把钥匙贴在门上。`UV_INDEX_xxx_USERNAME/_PASSWORD` 让钥匙由环境单独保管，仓库里只留"去哪家市场"的地址。

### 7.2 缓存：存在哪里、怎么清理

uv 把下载的包、构建产物等缓存在本机。默认位置：

- Windows：`%LOCALAPPDATA%\uv\cache`
- macOS/Linux：`$XDG_CACHE_HOME/uv`（未设置 `XDG_CACHE_HOME` 时为 `~/.cache/uv`）

可以用 `UV_CACHE_DIR` 环境变量覆盖默认位置，例如在 CI 里指向可跨任务持久化的目录。[^c7-C3]

```bash
uv cache clean          # 清空全部缓存
uv cache prune          # 只删除"不再需要"的缓存条目
uv cache prune --ci     # CI 专用：保留可复用的、删掉冗余的
uv sync --refresh       # 强制忽略缓存重新解析/下载（用于缓存异常时）
```

> [!tip] 大白话
> 缓存是"提前囤货的仓库"：装过的包先放仓库，下次直接取，不必重新联网下载。仓库满了或有脏货就 `clean` 全清、`prune` 只清不要的；`--refresh` 则是"这次别信仓库，重新进货"。

缓存出现异常（比如下载中断留下坏条目导致解析报错）时，优先 `uv sync --refresh`，而不是 `--no-cache`。`--no-cache` 等于放弃整套缓存机制、每次都全量重下，慢且浪费。[^c7-C3]

### 7.3 CI 接入（简述）

在 GitHub Actions 中，官方推荐使用 `astral-sh/setup-uv` 安装 uv，开启 `enable-cache` 复用缓存，再以 `uv sync --locked` 同步依赖、`uv run pytest` 跑测试。[^c7-C4]

```yaml
# .github/workflows/ci.yml（节选）
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # 具体版本 tag 与 uv version 均以官方仓库实际发布为准
      - uses: astral-sh/setup-uv@v6
        with:
          version: "0.12.9"      # 可选：固定 uv 版本；省略则取最新
          enable-cache: true     # 缓存 uv 自身与依赖下载，加速后续运行
      - name: Install locked dependencies
        run: uv sync --locked --all-extras --dev
      - name: Run tests
        run: uv run pytest
```

`--locked` 的意义：要求本次解析结果必须与 `uv.lock` 完全一致，若 `pyproject.toml` 与锁文件不一致则直接失败——这正是"防漂移"的关键。任何人在 CI 里改了依赖却没更新锁文件，CI 会红掉，而不是悄悄装上未锁定的新版本。[^c7-C4]

> [!tip] 大白话
> `--locked` 像签合同前的核对：uv.lock 是合同，`uv sync --locked` 是"只按合同办事，合同对不上就拒绝开工"。这样团队里不会有人偷偷用了合同外的新版本还不自知。

### 7.4 常见坑汇总速查表

汇总第 3/4/6/7 章涉及的高频坑（编号与各章正文一致），一表可扫：

| # | 出处 | 坑 | 一句话解法 |
|---|------|----|-----------|
| 1 | 第 4 章 | Windows PowerShell 执行策略挡 `.ps1` 激活 | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`，或改用 `uv run` 免激活 |
| 2 | 第 7 章 | 以为 `pip index-url` / `pip config` 对 uv 生效 | 用 `[[tool.uv.index]]` 或 `UV_DEFAULT_INDEX` / `UV_INDEX` |
| 3 | 第 6 章 | 手动激活后混用系统 pip 装包 | 双轨会污染 .venv；统一用 uv add/sync/run |
| 4 | 第 6 章 | `uv add -r requirements.txt` 导致版本重解析 | 导 `.in` 源清单；`.txt` 用 `-c` 作约束保留旧锁 |
| 5 | 第 5/6 章 | `uv.lock` 手工修改或没入库 | 提交版本库、勿手改，更新走 `uv lock` |
| 6 | 第 6 章 | conda 环境内项目 `uv sync` 不跟随 conda | 分工：uv 管 PyPI/Python 包、conda 管 CUDA/编译器；用 `UV_PROJECT_ENVIRONMENT` 前先确认语义 |
| 7 | 第 3 章 | 新大版本 Python 不被旧 uv 识别 | 先升级 uv（每个 uv 发布冻结可用版本集，以 `uv --version` 为准） |
| 8 | 第 7 章 | 私有源凭据写进 uv.lock/仓库 | 用 `UV_INDEX_{name}_USERNAME` / `UV_INDEX_{name}_PASSWORD` 环境变量注入 |
| 9 | 第 7 章 | 缓存一异常就上 `--no-cache` | 优先 `uv sync --refresh`；定期 `uv cache prune --ci` / `clean` 控制磁盘 |

### 本章小结

- pip 的 `index-url` 对 uv 不生效；换镜像/私有源用 `[[tool.uv.index]]`（`default = true` 可移除 PyPI 兜底）或 `UV_DEFAULT_INDEX` / `UV_INDEX`。
- 私有索引凭据经 `UV_INDEX_{name}_USERNAME/_PASSWORD` 注入环境，避免进入 `uv.lock`。
- 缓存默认在 `%LOCALAPPDATA%\uv\cache`（Windows）与 `$XDG_CACHE_HOME/uv`（Unix），`UV_CACHE_DIR` 可覆盖；缓存异常优先 `--refresh` 而非 `--no-cache`。
- CI 用 `astral-sh/setup-uv` + `enable-cache`，`uv sync --locked --all-extras --dev` 防 lockfile 漂移，`uv run pytest` 跑测试。

至此，从安装 uv、管理 Python 版本、创建虚拟环境、项目工作流到迁移与进阶的"镜像 / 缓存 / CI"三件套已全部覆盖。这份笔记到这里可以当作随时回来查阅的命令手册：把第 3/4/6/7 章末尾的坑表当作快速索引，遇到问题先查表、再动手。

---

## 相关笔记

- [[Python MOC]] — Python 学习笔记索引地图

---

## 参考来源

[^c1-a1]: uv Overview（官方文档，定位 / 四接口 / 概数出处）— <https://docs.astral.sh/uv/>
[^c1-a2]: uv: Python packaging in Rust（Astral 官方博客，分场景性能基准出处）— <https://astral.sh/blog/uv>
[^c1-a3]: The pip interface（uv 官方文档，uv 与 pip 真实关系）— <https://docs.astral.sh/uv/pip/>
[^c1-a4]: conda / poetry / uv / pip 对比（社区文章，仅作选型参考）— <https://juejin.cn/post/7550880557300383782>
[^c2-b1]: uv 官方文档 · Installation（全平台安装 / 升级 / 卸载）：https://docs.astral.sh/uv/getting-started/installation/ （来源表 B1）
[^c2-c5]: Microsoft Learn · about_Execution_Policies（PowerShell 执行策略说明）：https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies （来源表 C5）
[^c3-B2]: Installing Python（官方文档）：https://docs.astral.sh/uv/guides/install-python/
[^c3-B3]: Python versions（官方文档）：https://docs.astral.sh/uv/concepts/python-versions/
[^c4-b4]: Using Python environments（uv 官方文档，创建 / 激活 / 自动发现 / 发现顺序 / --system）— <https://docs.astral.sh/uv/pip/environments/>
[^c4-c5]: MS Learn about_Execution_Policies（PowerShell 执行策略官方说明）— <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies>
[^c4-c6]: astral-sh/uv issues #7829 等（社区讨论，Windows/conda 操作经验；CMD 激活行为非官方文档原文，属通行补录）— <https://github.com/astral-sh/uv>
[^c5-A1]: [Overview — uv 官方文档](https://docs.astral.sh/uv/)
[^c5-B4]: [Using Python environments — uv 官方文档](https://docs.astral.sh/uv/pip/environments/)
[^c5-B5]: [Working on projects — uv 官方文档](https://docs.astral.sh/uv/guides/projects/)
[^c6-1]: uv 官方迁移指南 · From pip to a uv project — https://docs.astral.sh/uv/guides/migration/pip-to-project/
[^c6-2]: uv 官方 · Using Python environments（环境发现顺序）— https://docs.astral.sh/uv/pip/environments/
[^c6-3]: uv GitHub issues #7829 / #11315 / #15783（conda 共存操作经验，社区观点）— https://github.com/astral-sh/uv
[^c7-C2]: uv 官方文档 · Package indexes — https://docs.astral.sh/uv/concepts/indexes/
[^c7-C3]: uv 官方文档 · Caching — https://docs.astral.sh/uv/concepts/cache/
[^c7-C4]: uv 官方文档 · uv in GitHub Actions — https://docs.astral.sh/uv/guides/integration/github/
