---
title: 如何用 uv 配置 Python 虚拟环境（学习大纲）
type: outline
note_type: 概念+实战结合
project_slug: uv-python-virtualenv
audience: 有了解（用过 venv/pip 或 conda，想换用 uv）
depth: 上手实操
direction: A+B 为主（概念定位 + 上手实操），C 简述
chapter_count: 7
created: 2026-09-03
status: draft
---

# 学习笔记大纲：如何用 uv 配置 Python 虚拟环境

> 笔记类型：概念+实战结合
> 面向读者：用过 venv/pip 或 conda，想切换到 uv 的开发者
> 学习深度：上手实操——能完整走通「安装 uv → 管理 Python 版本 → 创建/激活虚拟环境 → 安装管理依赖 → 日常使用」
> 预计总篇幅：全文约 5000–6000 字
> 章节数：7
> 素材来源：`02_deep_research.md` 来源表（A1..C6），写作时以官方文档为准、社区源须标注

## 大纲说明

- 本文是大纲（写作路线图），不是最终笔记正文；章节号按 `第 N 章` 组织，写作时每章展开为 Obsidian Markdown。
- 组织方式：概念 + 实战结合，主体按「产物/工具链动作」推进（uv 可执行程序 → `.python-version` → `.venv` → `pyproject.toml` + `uv.lock` → 迁移与进阶），C 方向素材压缩进第 6、7 两章简述。
- 平台标注：以 Windows 为主（PowerShell/CMD），macOS/Linux 命令并列标注，不省略任何平台激活命令。
- 最小可复现 demo（install → python version → venv → add → run）集中放在第 5 章 5.6，作为全书主线案例。
- 每章写作须链回官方文档 URL（见 `02_deep_research.md` 来源表），速度数字需区分「分场景基准」与「概数」出处。
- 常见坑清单（研究文件第 7 节）分散到对应章节；第 7 章末尾提供汇总速查表。

## 第 1 章：uv 是什么——从 venv/pip/conda 到 uv 的坐标

- **篇幅**：中（约占全文 10%）
- **覆盖要点**：uv 的定位与设计动机、四个接口总览、uv 与 pip 的真实关系与边界、性能快在哪、与 venv/pipenv/poetry/conda 的选型坐标、何时不必用 uv
- **素材引用**：#A1、#A2、#A3、#A4
- **代码示例**：无（本章为概念定位，不执行命令；最多给 `uv --help` 顶层命令名作接口示意）

### 建议子结构
- 1.1 uv 是什么 / 不是什么：Astral 出品、Rust 编写，目标「一个工具取代 pip / pip-tools / pipx / poetry / pyenv / twine / virtualenv」
- 1.2 四个接口总览：Projects（项目 + lockfile）、Scripts（单文件内联依赖）、Tools（`uvx`）、pip 兼容层（`uv pip` / `uv venv`）
- 1.3 uv 与 pip 的真实关系：不依赖、不调用 pip；对 common pip/pip-tools/virtualenv 命令 drop-in；偏离常见工作流越远差异越大
- 1.4 性能基准（注明口径）：暖缓存 80–115x、无缓存 8–10x、建 venv 快 ~80x；Overview「10–100x」为概数，写入时分开表述
- 1.5 选型坐标（社区观点，标注来源）：日常纯 Python 开发用 uv；发库用 poetry 或 uv+hatch；数据科学/ML 用 conda/mamba；旧项目兼容用 pip+venv；conda 注意 Anaconda 商业许可
- 1.6 写给「想换过来的人」：哪些习惯要改（不再手动 activate、不再用 pip 装包、用 `uv run` 取代双命令）

## 第 2 章：安装 uv

- **篇幅**：短（约占全文 8%）
- **覆盖要点**：全平台安装命令、验证安装、升级与卸载、`UV_NO_MODIFY_PATH`、Windows 安装与执行策略的关系
- **素材引用**：#B1（主）、#C5（PowerShell `-ExecutionPolicy ByPass` 仅限本次，不改系统策略）
- **代码示例**：有（下列命令必须出现：`curl -LsSf https://astral.sh/uv/install.sh | sh`、`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`、`brew install uv`、`winget install --id=astral-sh.uv -e`、`uv --version`、`uv self update`、`pip install --upgrade uv`）

### 建议子结构
- 2.1 独立安装器（官方推荐）：macOS/Linux curl 一行；Windows PowerShell 一行
- 2.2 包管理器方式：brew / winget / scoop / pipx（各自适用场景）
- 2.3 验证与升级：`uv --version`；`uv self update`（独立安装器）vs `pip install --upgrade uv`
- 2.4 注意事项：`UV_NO_MODIFY_PATH=1` 关闭 shell profile 改写；Windows `-ExecutionPolicy ByPass` 仅作用于该命令

## 第 3 章：用 uv 管理 Python 版本与 `.python-version`

- **篇幅**：中（约占全文 12%）
- **覆盖要点**：为何 uv 自带 Python 管理、install/list/upgrade 实操、缺失自动下载、`.python-version` 与 `uv python pin`、版本请求语法、查找优先级
- **素材引用**：#B2、#B3
- **代码示例**：有（必须出现：`uv python install 3.12`、`uv python install`、`uv python list`、`uv python pin 3.12`、`uv python pin --global 3.12`、`uv python upgrade 3.12`、`uv venv --python 3.11`（缺则自动下载））

### 建议子结构
- 3.1 为什么需要：无需预装 Python（python-build-standalone），解决多项目多版本问题
- 3.2 核心命令：`uv python install [版本]`、`uv python list`、`uv python upgrade`；`--default` 是否生成 `python`/`python3` 入口
- 3.3 版本请求语法：`3.12`、`>=3.12,<3.13`、`cpython@3.12`、解释器路径
- 3.4 `.python-version` 产物：`uv python pin` 写当前目录、`--global` 写用户级；uv 自当前目录向上逐级查找
- 3.5 查找优先级与开关：managed 目录 → PATH → Windows 注册表/Microsoft Store；`--no-managed-python`
- 3.6 易错点：大版本 Python 需要新版 uv 才认识（每个 uv 发布冻结可用版本集），版本以 `uv --version` 为准

## 第 4 章：创建、激活与使用虚拟环境 `.venv`

- **篇幅**：中（约占全文 15%）
- **覆盖要点**：`uv venv` 三种创建方式、全平台激活/停用命令、uv 自动发现 vs 手动激活、环境发现顺序、`--system`、Windows PowerShell 执行策略坑
- **素材引用**：#B4（主）、#C5、#C6（Windows 激活经验补充）
- **代码示例**：有（必须出现：`uv venv`、`uv venv my-name`、`uv venv --python 3.11`；Windows 激活 `.venv\Scripts\activate`（PS）、`.\.venv\Scripts\activate.bat`（CMD）、`.\.venv\Scripts\Activate.ps1`；macOS/Linux `source .venv/bin/activate`（bash/zsh）、`activate.fish`；`deactivate`；修复命令 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`）

### 建议子结构
- 4.1 创建虚拟环境：默认 `.venv`、自定义名/路径、`--python` 指定版本（缺则自动下载）
- 4.2 激活与停用（全平台并列给出）：Windows PowerShell / CMD、macOS/Linux bash/zsh/fish；`deactivate`
- 4.3 uv 的自动发现逻辑：默认名 `.venv` 时 uv 命令直接复用，手动激活对 uv 自身常非必需
- 4.4 环境发现顺序：激活的 `VIRTUAL_ENV` → 激活的 conda `CONDA_PREFIX` → 当前/最近父目录 `.venv`
- 4.5 `--system` 的适用场景（CI/容器）与限制
- 4.6 Windows 激活坑：PowerShell 执行策略 Restricted 挡 `Activate.ps1` → `RemoteSigned` 或改用 `uv run` 免激活

## 第 5 章：项目工作流——`pyproject.toml`、`uv.lock` 与最小可复现 demo

- **篇幅**：长（约占全文 25%）
- **覆盖要点**：`uv init` 生成物、`pyproject.toml` 依赖声明、`uv.lock` 语义、add/remove/sync/run/lock 日常循环、`uv run` 免激活与一致性校验、从零到跑通的最小 demo
- **素材引用**：#B5（主）、#A1（接口总览呼应）、#B4（自动发现复用）
- **代码示例**：有（必须出现：`uv init hello-demo`、`uv add requests`、`uv add 'requests==2.31.0'`、`uv remove requests`、`uv sync`、`uv run hello-demo`、`uv run python -c "import requests; print(requests.__version__)"`、`uv lock --upgrade-package requests`；最小 demo 见下）
- **最小可复现 demo（5.6 落地）**：install → python version → venv → add → run
  ```bash
  # 1) install uv（详见第 2 章，Windows 用 powershell 一行）
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # 2) python version
  uv python install 3.12 && uv python pin 3.12
  # 3) venv（项目流中 uv add/sync 也会自动建 .venv，这里显式演示）
  uv init hello-demo && cd hello-demo && uv venv
  # 4) add + run
  uv add requests
  uv run python -c "import requests; print(requests.__version__)"
  ```

### 建议子结构
- 5.1 `uv init`：生成 `.gitignore` / `.python-version` / `pyproject.toml` / `README` / src 布局
- 5.2 `pyproject.toml`：`[project].dependencies` 声明依赖；与 `requirements.txt` 的差异
- 5.3 `uv.lock`：跨平台精确锁定文件；应提交版本库、勿手改；保证可复现性
- 5.4 日常循环：`uv add`（自动更新 lock 与 .venv）、`uv remove`、`uv sync`、`uv lock --upgrade-package`
- 5.5 `uv run` 语义：每次运行校验 lockfile ↔ pyproject ↔ 环境一致性；默认不清理多余包
- 5.6 最小可复现 demo：上述命令串，标注每步产出物（.python-version / .venv / uv.lock）

## 第 6 章：从 pip/venv/conda 平滑迁移到 uv

- **篇幅**：中（约占全文 15%）
- **覆盖要点**：迁移路线、requirements 迁移要点（`.in` vs `.txt`、`-c` 约束）、dev 依赖、`uv run` 取代手动 activate、与 conda 共存分工、迁移常见坑
- **素材引用**：#C1（主）、#B4（自动发现/发现顺序）、#C6（conda 共存操作经验）
- **代码示例**：有（必须出现：`uv init` + `uv add -r requirements.in`、`uv add --dev -r requirements-dev.in`、以 `-c requirements.txt` 保留旧锁定、`uv run python -m pytest`；警示示例 `UV_PROJECT_ENVIRONMENT` 非空非 PEP405 venv 会报错）

### 建议子结构
- 6.1 迁移路线图：venv+pip 旧项目 → `uv init` + 声明依赖 + `uv sync`
- 6.2 requirements 迁移：应导入 `.in`（源清单）而非 `.txt`；`.txt` 用 `-c` 作约束保留旧锁
- 6.3 dev 依赖分组：`uv add --dev -r ...`；与主依赖分离
- 6.4 日常命令替换表：`pip install` → `uv add`、`pip install -r` → `uv sync`、`python -m pytest` → `uv run pytest`、手动 activate → `uv run`
- 6.5 与 conda 并存：`uv pip` 跟随激活的 `CONDA_PREFIX`；项目命令 `uv sync` 默认只操作 `.venv`；推荐分工（uv 管 PyPI/Python 包，conda 管 CUDA/编译器），避免同环境混装
- 6.6 迁移坑速查：混用系统 pip 污染 .venv、`uv add -r requirements.txt` 重解析版本、uv.lock 手改/不入库等（映射坑清单 #3 #4 #5 #6）

## 第 7 章：进阶简谈——索引镜像、缓存与 CI

- **篇幅**：中（约占全文 15%）
- **覆盖要点**：自定义索引/国内镜像配置、缓存目录与清理、GitHub Actions 接入、进阶坑汇总速查表
- **素材引用**：#C2、#C3、#C4
- **代码示例**：有（必须出现：`pyproject.toml` 的 `[[tool.uv.index]]` 片段（含 `default = true` 语义）、环境变量 `UV_DEFAULT_INDEX` / `UV_INDEX`、`uv cache clean`、`uv cache prune --ci`、GitHub Actions 片段 `astral-sh/setup-uv@…` + `enable-cache` + `uv sync --locked` + `uv run pytest`）

### 建议子结构
- 7.1 镜像与索引：pip 的 index-url 不作用于 uv；`[[tool.uv.index]]` 声明、`default = true` 移除 PyPI 兜底；环境变量写法（给国内镜像通用写法 + 提示替换 URL）；凭据用 `UV_INDEX_{name}_USERNAME/_PASSWORD`，不写入 uv.lock
- 7.2 缓存：Windows `%LOCALAPPDATA%\uv\cache` 与 Unix `$XDG_CACHE_HOME/uv`；`UV_CACHE_DIR` 覆盖；`uv cache clean` / `prune` / `prune --ci`；异常时优先 `--refresh` 而非 `--no-cache`
- 7.3 CI 接入（简述）：`astral-sh/setup-uv` + `enable-cache`；`uv sync --locked --all-extras --dev` + `uv run pytest`；`--locked` 保证 lockfile 不漂移
- 7.4 常见坑汇总速查表：汇总第 3/4/6 章出现的坑 + 本章坑（#1..#7），一表可扫

## 学习路径说明

### 前置要求
- 会用 venv/pip 或 conda 创建、激活、停用虚拟环境并安装包
- 理解 `requirements.txt`、`pip install` 与「解释器 / 环境 / 包」的基本关系
- 会使用 Windows PowerShell（或 CMD）与 macOS/Linux shell 中的至少一种

### 学完能做什么
- 用一条命令安装 uv，并管理多个 Python 版本（`uv python install/pin`）
- 快速创建虚拟环境（`uv venv`）并掌握全平台激活/停用命令
- 从零初始化项目，用 `uv add` / `uv sync` / `uv run` 完成依赖声明、锁定与执行
- 把旧 pip/venv 项目平滑迁移到 uv，并理解与 conda 并存时的分工
- 配置国内镜像、清理缓存、在 GitHub Actions 中用 uv 做可复现构建
- 独立排查 Windows 激活、PATH、索引、缓存等高频坑

### 建议学习顺序
- 按 第1 → 第7 章顺序阅读；第 1 章可快速浏览（面向已有 venv/conda 经验的读者）
- 时间估计：第 1–2 章约 30 分钟；第 3–4 章约 45 分钟；第 5 章含 demo 约 60 分钟（动手跑通最小 demo）；第 6 章约 45 分钟（迁移演练）；第 7 章约 30 分钟（可首次跳过，按需回看）
- 上手建议：读完第 4 章即可开始日常使用；第 5 章 demo 务必亲手跑一遍；第 6、7 章按需查阅

## 附录（写作时用）

- 素材引用统一用研究文件来源表 ID（A1..C6）；每章末尾链回官方文档锚点（如 #the-pip-interface、#discovery-of-python-environments）。
- 速度表述规范：分场景数字（暖缓存 80–115x / 无缓存 8–10x）为主文，「10–100x」注明为 Overview 概数。
- Windows CMD 激活行、镜像 URL 具体值等无权威出处项，写入时按研究文件第 8 节「未决问题」处理并加注。
