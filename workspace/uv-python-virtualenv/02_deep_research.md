# uv 配置 Python 虚拟环境 - P2 深度素材

> 工作流：learning-note-flow · run_id: uv-python-virtualenv
> 创建时间：2026-09-03 · 阶段：P2 深度收集
> 方向：A+B 为主（概念定位 + 上手实操），C 简述
> 本文件为下游素材，非最终笔记；写作时以官方文档为准，社区源须标注。

## 1. Scope

覆盖：uv 概念定位 → 安装 → Python 版本管理 → 虚拟环境创建/激活 → 项目工作流（pyproject/uv.lock）→ 迁移/镜像/缓存/CI/Windows 与 conda 共存简述。
信源以 **docs.astral.sh/uv 官方文档** 为锚（10 页 + 1 官方博客 + 1 MS Learn），社区/issue 仅补 Windows 与 conda 操作经验。

## 2. 来源表

| ID | 标题 | URL | Tier | 用途 |
|----|------|-----|------|------|
| A1 | uv Overview | https://docs.astral.sh/uv/ | official | 定位、四层接口、能力总览 |
| A2 | uv: Python packaging in Rust | https://astral.sh/blog/uv | official | 动机、性能基准、路线图 |
| A3 | The pip interface | https://docs.astral.sh/uv/pip/ | official | uv 与 pip 的真实关系 |
| A4 | conda/poetry/uv/pip 对比 | https://juejin.cn/post/7550880557300383782 | community | 选型坐标（社区观点） |
| B1 | Installation | https://docs.astral.sh/uv/getting-started/installation/ | official | 全平台安装/升级/卸载 |
| B2 | Installing Python | https://docs.astral.sh/uv/guides/install-python/ | official | uv python install/list/upgrade |
| B3 | Python versions | https://docs.astral.sh/uv/concepts/python-versions/ | official | .python-version、pin、版本请求 |
| B4 | Using Python environments | https://docs.astral.sh/uv/pip/environments/ | official | uv venv、激活/停用、自动发现 |
| B5 | Working on projects | https://docs.astral.sh/uv/guides/projects/ | official | init/sync/add/run/lock 全流程 |
| C1 | From pip to a uv project | https://docs.astral.sh/uv/guides/migration/pip-to-project/ | official | pip/requirements 迁移 |
| C2 | Package indexes | https://docs.astral.sh/uv/concepts/indexes/ | official | 镜像/索引配置 |
| C3 | Caching | https://docs.astral.sh/uv/concepts/cache/ | official | 缓存目录/清理/UV_CACHE_DIR |
| C4 | uv in GitHub Actions | https://docs.astral.sh/uv/guides/integration/github/ | official | CI 接入 |
| C5 | MS Learn about_Execution_Policies | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies | official | Windows PS 执行策略 |
| C6 | uv issues #7829/#11315/#15783 等 | https://github.com/astral-sh/uv | community | conda 共存操作经验 |

Tier 构成：official 13 · community 2。所有 material claim 均可回溯到上表。

## 3. 概念定位（A）

- uv = Astral 出品的 Rust 编写"极快 Python 包与项目管理器"，官方宣称一个工具取代 pip/pip-tools/pipx/poetry/pyenv/twine/virtualenv，支持 Win/macOS/Linux [A1]。
- 四个接口：Projects（项目/工作区/lockfile）、Scripts（单文件脚本内联依赖）、Tools（`uvx` = `uv tool run`，类 pipx）、pip interface（`uv pip`/`uv venv`，低层兼容层）[A1]。
- 设计动机："a Cargo for Python"；起步刻意做 pip/pip-tools drop-in，再扩展项目 API [A2]。
- **uv 与 pip 关系**：`uv pip` 是对 common pip/pip-tools/virtualenv 命令的 drop-in 替代，但 **"uv does not rely on or invoke pip"**，纯自行实现接口；且"不精确实现被替代工具全部行为"，偏离常见工作流越远差异越大 [A3]。
- 性能基准：暖缓存快 80-115x、无缓存 8-10x（对照 pip/pip-tools）；建 venv 比 `python -m venv` 快 ~80x 且不依赖 Python [A2]。Overview 概数"10-100x" [A1]。
- 版本管理：uv 自带安装/管理 Python（python-build-standalone 发行版），无需预装 Python [B2][B3]。
- 选型坐标（社区 A4，仅参考）：日常纯 Python 开发优先 uv；发布库/应用 poetry 或 uv+hatch；数据科学/ML 用 conda/mamba；旧项目兼容用 pip+venv。conda 注意 Anaconda 商业许可，用 Miniconda+conda-forge。
- 历史：Astral 接管 Rye，Rye 基于 uv 并提供迁移路径 [A2]。

## 4. 实操素材（B，重点）

### 4.1 安装 uv
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# 指定版本
curl -LsSf https://astral.sh/uv/0.12.9/install.sh | sh
```
```powershell
# Windows PowerShell（一键）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
```bash
# 包管理器 / pip
brew install uv                       # macOS
winget install --id=astral-sh.uv -e   # Windows
scoop install main/uv                 # Windows
pipx install uv
```
- 升级：独立安装器支持 `uv self update`；其它方式 `pip install --upgrade uv`。自更新可能改写 shell profile，可用 `UV_NO_MODIFY_PATH=1` 关闭 [B1]。

### 4.2 Python 版本管理
```bash
uv python install            # 装最新，仅版本化入口 python3.13
uv python install --default  # 额外装 python/python3 入口
uv python install 3.12
uv python install 3.11 3.12  # 一次多个
uv python install pypy@3.13  # 其它实现
uv python list               # 列出可用/已安装
uv python upgrade 3.12       # preview：升级 patch
```
- 缺失自动下载：`uv venv` 无 Python 时会先自动下载再建环境；强制只用系统解释器用 `--no-managed-python` [B2]。
- `.python-version`：`uv python pin` 在当前目录生成；`--global` 写用户级。uv 从当前目录向上逐级查找。版本请求支持 `3.12`、`>=3.12,<3.13`、`cpython@3.12`、解释器路径等 [B3]。
- 查找优先级：managed 目录 → PATH → Windows 注册表/Microsoft Store；默认 `python-preference=managed` [B3]。

### 4.3 虚拟环境创建与激活
```bash
uv venv                  # 默认 .venv
uv venv my-name          # 自定义名/路径
uv venv --python 3.11    # 指定版本；缺则自动下载
```
```bash
source .venv/bin/activate        # macOS/Linux bash/zsh
source .venv/bin/activate.fish   # fish
source .venv/bin/activate.csh    # csh/tcsh
```
```powershell
.venv\Scripts\activate           # Windows PowerShell（当前官方文档写法）
.\.venv\Scripts\Activate.ps1     # PowerShell 显式 .ps1
.\.venv\Scripts\activate.bat     # Windows CMD
```
```bash
deactivate                       # 退出
```
- 默认名 `.venv` 时，后续 uv 命令自动发现并复用，**手动激活对 uv 自身常非必需**（`uv venv` 后可直接 `uv pip install ruff`）[B4]。
- 环境发现顺序（变更环境的命令）：激活的 `VIRTUAL_ENV` → 激活的 conda `CONDA_PREFIX` → 当前/最近父目录 `.venv` [B4]。
- `--system` 装系统环境（约等 `--python $(which python)`），供 CI/容器；无 `--system` 时忽略非虚拟解释器 [B4]。

### 4.4 项目工作流（推荐路线）
```bash
uv init hello-world && cd hello-world
# 生成 .gitignore/.python-version/pyproject.toml/README/src/hello_world/__init__.py
uv add requests            # 声明依赖，更新 uv.lock 与 .venv
uv add 'requests==2.31.0'  # 带约束
uv remove requests
uv sync                    # 依 pyproject/uv.lock 建/同步 .venv
uv run hello-world         # 在项目环境跑命令（自动 sync 校验）
uv run example.py
uv lock --upgrade-package requests   # 单包升级
uv build                   # 构建发行包
```
- 首次 `uv run`/`uv sync`/`uv lock` 自动创建 `.venv` 与 `uv.lock` [B5]。
- `.venv` 隔离依赖；`uv.lock` 是**跨平台精确锁定文件，应提交版本库、勿手改**；`.python-version` 决定建 venv 用版本 [B5]。
- `uv run` 每次运行前校验 lockfile↔pyproject↔环境一致性；默认不清理多余包 [B5]。

## 5. 进阶简述（C）

- 迁移：`uv init` + `uv add -r requirements.in`（应导 `.in` 非 `.txt`，`.txt` 用 `-c` 作约束保留旧锁）；dev 依赖 `uv add --dev -r ...`；`uv run` 取代手动 activate [C1]。
- 镜像/索引：pip 的 index-url **不作用于 uv**；需在 pyproject `[[tool.uv.index]]` 声明，`default = true` 移除 PyPI 兜底；env：`UV_DEFAULT_INDEX`/`UV_INDEX`（`<name>=<url>`）。凭据用 `UV_INDEX_{name}_USERNAME/_PASSWORD`，不写入 uv.lock [C2]。
- 缓存：Windows 默认 `%LOCALAPPDATA%\uv\cache`，Unix `$XDG_CACHE_HOME/uv`；`UV_CACHE_DIR` 覆盖；`uv cache clean`/`prune`/`prune --ci`；缓存异常优先 `--refresh` 而非 `--no-cache` [C3]。
- CI：`astral-sh/setup-uv` + `enable-cache`，`uv sync --locked --all-extras --dev` + `uv run pytest`；`--locked` 保证 lockfile 不漂移 [C4]。
- Windows 激活坑：PowerShell 执行策略默认 Restricted 会禁跑 `Activate.ps1`；修复 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`；或干脆 `uv run` 免激活 [C5][C6]。
- conda 共存：`uv pip` 会跟随激活的 conda（`CONDA_PREFIX`），但项目命令 `uv sync` 默认只操作 `.venv`；推荐分工——uv 管 PyPI/Python 包、conda 管 CUDA/编译器等系统包，避免同环境混装 [B4][C6]。

## 6. 跨源矛盾 / 需注意

- **速度表述**：概数"10-100x"[A1] vs 官方分场景"无缓存 8-10x / 暖缓存 80-115x"[A2]。写作采用分场景数字并注明概数出处。
- **drop-in 程度**：Overview 泛称 drop-in [A1]；pip 接口页限定"common commands 且不精确实现全部行为"[A3]。社区弱化此边界[A4]。
- **lockfile 语义随版本演进**：2024 博客称当时无平台无关 lockfile（同 pip-tools）[A2]；当前版文档 uv.lock 已是 universal 跨平台锁 [B5][C1]。写作按当前版表述。
- **"uv 是否基于 pip"**：官方明确不依赖不调用 pip [A3]；社区常把 uv 简单说成 pip 替代者——本质一致但需带官方边界。
- Windows 激活：uv 官方当前文档统一写作 `.venv\Scripts\activate`（PowerShell）；CMD `activate.bat` 与显式 `Activate.ps1` 属 Python venv 通行写法，已据 MS/practise 补录但非本页原文，写作时建议标注或并入"常见坑"。

## 7. 常见坑清单（写作建议）

1. Windows PowerShell 执行策略挡 `.ps1` 激活 → `RemoteSigned -Scope CurrentUser` 或 `uv run` 免激活。
2. 误以为 `pip config`/`index-url` 对 uv 生效 → 必须用 `[[tool.uv.index]]`/`UV_DEFAULT_INDEX`。
3. 手动激活后混用系统 pip 装包 → uv 与 pip 双轨污染 .venv；统一用 uv。
4. `uv add -r requirements.txt` 重解析版本 → 用 `.in` 文件或 `-c requirements.txt` 保留锁定。
5. uv.lock 手工修改 / 不入库 → 丢失可复现性。
6. conda 环境内项目 `uv sync` 不跟随 conda → 用 `UV_PROJECT_ENVIRONMENT` 前先确认语义（issue 显示非空非 PEP405 venv 会报错）。
7. 大版本 Python 下载需要 uv 升级到能识别该版本的 uv 版本（每个 uv 发布冻结可用版本集）。

## 8. 未决问题

- uv 当前精确版本号（文档出现 0.12.9 示例）；写作时建议以用户实际安装版本为准，命令可加"版本以 `uv --version` 为准"注。
- Windows CMD 激活行的权威出处待定（uv 官方文档当前只给 PowerShell 行）。
- 镜像源（清华/阿里）接入 uv 的具体 URL 配置样例，官方文档未给中文镜像示例；需在章节写作时以 `UV_DEFAULT_INDEX` 形式给出通用写法并提示替换为国内镜像。

## 9. 下游交接（handoff）

建议大纲结构（供 outline-generator）：
1. uv 是什么 & 为什么值得用（A1-A4）
2. 安装 uv（B1）
3. uv 管理 Python 版本 + .python-version（B2、B3）
4. 创建/激活/停用虚拟环境（B4）— Windows/CMD/PS/macOS/Linux 命令齐全
5. 项目工作流：init/add/sync/run/lock（B5）+ 最小可复现 demo
6. 进阶简述：迁移/镜像/缓存/CI + Windows 与 conda 坑（C1-C6）

每章素材可引用上表 ID。官方文档 URL 与锚点（如 #the-pip-interface、#discovery-of-python-environments）已记录，写作时直接链回原文。
