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

[^c3-B2]: Installing Python（官方文档）：https://docs.astral.sh/uv/guides/install-python/
[^c3-B3]: Python versions（官方文档）：https://docs.astral.sh/uv/concepts/python-versions/
