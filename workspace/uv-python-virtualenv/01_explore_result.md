# uv 配置 Python 虚拟环境 - P1 探测结果

> 工作流：learning-note-flow · run_id: uv-python-virtualenv
> 创建时间：2026-09-03 · 阶段：P1 探测式收集

## 一、候选信源（按视角分组，已按 URL 去重）

### 视角 A：概念定位 —— uv 是什么、为什么用、与 venv/pip/poetry/conda 的关系

| # | 标题 | 来源 | Tier | 日期 | 分 | 说明 |
|---|------|------|------|------|----|------|
| A1 | [uv 官方文档 Overview](https://docs.astral.sh/uv/) | Astral | official | 2026-03 | 5 | Rust 编写的 Python 包/项目管理器，声称替代 pip/pip-tools/pipx/poetry/pyenv/twine/virtualenv；projects/scripts/tools/pip 四层接口 |
| A2 | [uv: Python packaging in Rust](https://astral.sh/blog/uv) | Astral（Charlie Marsh） | official | 2024-02 | 5 | 官方发布博客："Cargo for Python" 愿景、设计动机与路线图 |
| A3 | [The pip interface](https://docs.astral.sh/uv/pip/) | Astral | official | 2024-08 | 4 | uv 与 pip 关系：`uv pip` 是 drop-in 替代，但 uv 不依赖/不调用 pip |
| A4 | [I Replaced Pip, Virtualenv, and Poetry With uv](https://www.kdnuggets.com/i-replaced-pip-virtualenv-and-poetry-with-uv-heres-why) | KDnuggets | blog | unknown | 3 | 实践迁移体验，理解何时/为何换用 uv |
| A5 | [conda/poetry/uv/pip 四种工具对比（中文）](https://juejin.cn/post/7550880557300383782) | 掘金社区 | community | unknown | 4 | 中文选型对比，覆盖 conda 维度（社区经验，仅作参考） |

### 视角 B：核心实操 —— 安装 uv、指定 Python 版本、创建/激活/停用虚拟环境

| # | 标题 | 来源 | Tier | 日期 | 分 | 说明 |
|---|------|------|------|------|----|------|
| B1 | [Installation](https://docs.astral.sh/uv/getting-started/installation/) | Astral | official | unknown | 5 | curl / PowerShell `irm` / pipx / pip / brew / winget / scoop；升级与卸载 |
| B2 | [Installing Python](https://docs.astral.sh/uv/guides/install-python/) | Astral | official | unknown | 4 | `uv python install 3.12`、多版本、`--default`、缺失自动下载 |
| B3 | [Python versions](https://docs.astral.sh/uv/concepts/python-versions/) | Astral | official | unknown | 5 | `uv python pin` 写 `.python-version`、版本请求格式、managed/system Python |
| B4 | [Using Python environments](https://docs.astral.sh/uv/pip/environments/) | Astral | official | unknown | 5 | `uv venv`、按 shell 的激活/停用命令、默认 `.venv` 自动发现 |
| B5 | [Working on projects](https://docs.astral.sh/uv/guides/projects/) | Astral | official | unknown | 4 | `uv init`→`uv sync`/`uv run` 全流程，`.venv` 自动创建与激活 |

### 视角 C：进阶与坑 —— 依赖管理、迁移、镜像/缓存、IDE 与 CI

| # | 标题 | 来源 | Tier | 日期 | 分 | 说明 |
|---|------|------|------|------|----|------|
| C1 | [Working on projects（复用 B5）](https://docs.astral.sh/uv/guides/projects/) | Astral | official | 2026-09 | 5 | pyproject.toml vs requirements.txt、uv.lock、`uv add/sync/run` 工作流 |
| C2 | [From pip to a uv project](https://docs.astral.sh/uv/guides/migration/pip-to-project/) | Astral | official | unknown | 5 | 从 pip/requirements.txt 迁移：`uv add -r requirements.txt`、CI 改造 |
| C3 | [Using uv in GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/) | Astral | official | unknown | 4 | `astral-sh/setup-uv`、`uv sync --locked`、缓存持久化 |
| C4 | [Package indexes](https://docs.astral.sh/uv/concepts/indexes/) | Astral | official | 2026-08 | 4 | 镜像/索引配置；pip index-url 对 uv 不生效，须用 uv 自身配置 |
| C5 | [Caching](https://docs.astral.sh/uv/concepts/cache/) | Astral | official | unknown | 4 | 缓存目录（Windows 在 `%LOCALAPPDATA%\uv\cache`）、`UV_CACHE_DIR`、`cache clean/prune` |

## 二、方向菜单

**A. 概念定位优先** — uv 是什么、设计动机、与 pip/venv/poetry/conda 的关系（A1-A5）
**B. 上手实操优先** — 安装 → 建项目 → 建虚拟环境 → 激活/停用 → 装依赖，全程可跟做（B1-B5）
**C. 进阶工程化优先** — pyproject/uv.lock 工作流、迁移、镜像与缓存坑、CI 接入（C1-C5）

> 注：主题为「上手实操 + 概念实战结合」时，通常按 A→B→C 顺序都覆盖；本菜单决定 P2 深度收集的重点配比。

## 三、覆盖缺口

- **中文镜像源实际可用性**：官方文档给出配置语法，但国内常用镜像（清华/阿里）的 uv 接入样例需补充验证。
- **conda 并存场景**：仅 A5 社区帖覆盖，缺少权威说明（适合作为选型对比的小节）。
- **Windows 特有坑**：激活命令官方有；PowerShell 执行策略、PATH 冲突等散落社区，P2 需针对性补 1-2 条经验源。
- **IDE 接入**：VS Code/PyCharm 选择 `.venv` 解释器的说明暂缺官方直接资料。

## 四、P2 范围估算

- 按 A/B/C 三方向各取 2-3 个核心官方源深读：预计 **6-9 个源** 进入 P2。
- 额外补缺：镜像源中文实践、Windows 激活坑、conda 并存（各 ≤2 条），预计 **+2-4 条**。
- 主要依赖 **docs.astral.sh/uv 官方文档**（≥90%），博客/社区仅作背景与经验佐证。
