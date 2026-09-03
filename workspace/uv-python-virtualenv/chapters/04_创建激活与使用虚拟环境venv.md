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

[^c4-b4]: Using Python environments（uv 官方文档，创建 / 激活 / 自动发现 / 发现顺序 / --system）— <https://docs.astral.sh/uv/pip/environments/>
[^c4-c5]: MS Learn about_Execution_Policies（PowerShell 执行策略官方说明）— <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies>
[^c4-c6]: astral-sh/uv issues #7829 等（社区讨论，Windows/conda 操作经验；CMD 激活行为非官方文档原文，属通行补录）— <https://github.com/astral-sh/uv>
