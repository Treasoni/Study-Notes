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

[^c6-1]: uv 官方迁移指南 · From pip to a uv project — https://docs.astral.sh/uv/guides/migration/pip-to-project/
[^c6-2]: uv 官方 · Using Python environments（环境发现顺序）— https://docs.astral.sh/uv/pip/environments/
[^c6-3]: uv GitHub issues #7829 / #11315 / #15783（conda 共存操作经验，社区观点）— https://github.com/astral-sh/uv
