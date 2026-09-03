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

[^c5-A1]: [Overview — uv 官方文档](https://docs.astral.sh/uv/)
[^c5-B4]: [Using Python environments — uv 官方文档](https://docs.astral.sh/uv/pip/environments/)
[^c5-B5]: [Working on projects — uv 官方文档](https://docs.astral.sh/uv/guides/projects/)
