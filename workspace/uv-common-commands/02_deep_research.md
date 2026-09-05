# uv 的常用命令 - 深度素材（P2）

> run_id: uv-common-commands · 主题：uv 的常用命令 · 形式：常用命令速查手册（命令族+场景混合）· 深度：上手 · 检索日期：2026-09-05
> 组织主线（用户已选 D）：正文按 uv 命令族保证覆盖，每族配「常用场景」子节与示例；附录加 pip/venv 对照与 CI 片段。

## 1. 范围与目标

面向有 uv 基础（已发布过虚拟环境配置笔记）的中文读者，产出一份「上手 80% 场景」的 uv 常用命令速查手册。核心 = 命令族（project / python / venv / tool(uvx) / cache / index）+ 场景速查子节 + 迁移对照附录。

## 2. 来源清单

缓存目录：`workspace/uv-common-commands/research-cache/`

| 缓存文件 | 来源 | Tier | 角色 |
|------|------|------|------|
| 01_docs_astral_sh.md | docs.astral.sh/uv/concepts/cache/ | official | 缓存命令 |
| 02_docs_astral_sh.md | docs.astral.sh/uv/concepts/indexes/ | official | 镜像/索引配置 |
| 03_docs_astral_sh.md | docs.astral.sh/uv/guides/integration/github/ | official | CI 片段 |
| 04_docs_astral_sh.md | docs.astral.sh/uv/concepts/python-versions/ | official | uv python 族 |
| 05_docs_astral_sh.md | docs.astral.sh/uv/guides/projects/ | official | 项目工作流主线 |
| 06_docs_astral_sh.md | docs.astral.sh/uv/pip/environments/ | official | uv venv / 环境发现 |
| 07_docs_astral_sh.md | docs.astral.sh/uv/guides/tools/ | official | uv tool / uvx |
| 08_cpython666_github_io.md | cpython666.github.io/python/libs/uv.html | community | Conda→uv 迁移、中文速查 |
| 09_docs_astral_sh.md | docs.astral.sh/uv/reference/cli/（819KB） | official | CLI 权威签名（grep 定向使用） |
| 10_realpython_com.md | realpython.com/python-uv/ | implementation | 实战生命周期、坑 |

## 3. 素材地图（命令族 → 要点 → 来源）

### 3.1 project 命令族
- **uv init**：生成 `pyproject.toml`/`.python-version`/`.gitignore`/`README`/`src/<pkg>/`；`.venv` 与 `uv.lock` 首次 sync 类命令时惰性创建。`uv init --vcs none`。已有 pyproject 会报错。SRC: 05, 09-cli(init≈947)
- **uv add / uv remove**：写 pyproject + 同步 uv.lock + .venv。支持 `uv add 'requests==2.31.0'`、`git+https://...`、`-r requirements.txt`、`--editable ../lib`、`--dev pytest`、`--upgrade`；`--frozen`/`--no-sync` 旁路。SRC: 05, 09-cli
- **uv run**：项目环境执行，调用前自动校验/同步 pyproject↔lock↔.venv，无需 activate。选项须放命令前。PEP 723 内联依赖脚本进临时隔离环境。`uv run --with requests script.py`、`--env-file .env`、`--no-sync`。SRC: 05, 09-cli(run≈474), 08
- **uv sync**：手动同步 .venv ↔ lock；默认 exact（删多余包）；`--inexact` 保留；默认先 re-lock 除非 `--locked`/`--frozen`。SRC: 09-cli(sync≈2222), 05
- **uv lock**：只解析并更新 uv.lock 不安装；`uv lock --upgrade-package requests`。SRC: 09-cli(lock≈2704)
- **uv tree / uv export**：依赖树（`-d 2`、`--invert`、`--package`）；导出 requirements.txt / cyclonedx（`uv export -o requirements.txt`，默认先 re-lock 除非 `--frozen`）。SRC: 09-cli(tree≈3417, export≈3007), 08
- **四文件关系**：pyproject + .python-version 声明「要什么」→ `uv lock` 解析成精确 uv.lock → `uv sync` 装进 .venv；uv.lock 提交 VCS。SRC: 05
- **uv run vs uv sync**：一次性命令/脚本用 uv run（自动同步但不清多余包）；要 activate 后长时间手跑或 CI 建环境用 uv sync。SRC: 05, 09-cli

### 3.2 uv python / uv venv
- **uv python install / list / find / pin**：install 下载 uv 托管 Python（managed），`--default` 才装 `python`/`python3`；pin 写 `.python-version`（`--global` 用户级）；find 输出解释器路径。发现顺序：VIRTUAL_ENV/`.venv` → managed 目录 → PATH → Win 注册表；默认偏好 managed，system 优先于重新下载。SRC: 04, 09-cli(install≈6783, find≈7059, pin≈7174)
- **uv venv**：默认建 `.venv`；`uv venv my-name`、`--python 3.11`（缺则自动下载）；已存在先删重建；有 `.python-version` 用它决定解释器；无需 activate，uv 自动发现 `.venv`。激活：`source .venv/bin/activate`（Win `PS> .venv\Scripts\activate`）/ `deactivate`。SRC: 06, 05, 09-cli(venv≈10071)
- 与旧笔记衔接：`python/如何用uv配置Python虚拟环境.md` 已有 .venv 配置实战，本篇只做命令速查，不重复长篇原理。

### 3.3 tool / uvx
- **uvx**（= uv tool run）：临时运行工具，装入临时隔离环境不持久。`uvx ruff`、`uvx --from httpie http`、`uvx --with mkdocs-material mkdocs`、`uvx 'ruff==0.3.0' check`。SRC: 07, 09-cli
- **uv tool install / upgrade / list / uninstall / update-shell**：持久装工具、可执行链入 bin（`uv tool dir --bin`）；模块不会进当前项目（`import` 失败是预期）。SRC: 07
- **分工**：一次性临时工具 → uvx；需要在项目环境里跑且版本钉进项目（pytest/mypy）→ uv run；常驻工具（ruff）→ uv tool install。SRC: 07

### 3.4 uv cache
- `uv cache dir` 定位；`uv cache clean [pkg]` 全清/按包清；`uv cache prune` 清未用条目+集中环境；`uv cache prune --ci` 清预构建 wheel 留源码编译 wheel（CI 末尾推荐）。SRC: 01, 09-cli
- 旁路：`--refresh`（重验证仍写缓存）、`--reinstall`（忽略已装版本强制重装）、`--no-cache`（临时缓存，多数场景用 --refresh 更优）。SRC: 01

### 3.5 index / 镜像
- 四种写法：pyproject `[[tool.uv.index]]`；CLI `--index`/`--default-index`；环境变量 `UV_INDEX`/`UV_DEFAULT_INDEX`；兼容旧 `--index-url`/`--extra-index-url`。CLI/环境变量优先于配置文件；default 索引恒最低优先级；设某索引 default=true 即排除 PyPI。凭据 `UV_INDEX_<NAME>_USERNAME/PASSWORD`。SRC: 02
- 国内镜像：官方文档无集中镜像清单；社区帖子写法不一（uv.toml vs pyproject、UV_INDEX_URL vs UV_DEFAULT_INDEX）→ 速查以「UV_DEFAULT_INDEX + --default-index」官方写法为准，具体 URL 标为「以镜像服务说明为准」。SRC: 02, 08

### 3.6 build / publish / pip 兼容层
- `uv build [SRC]`：默认同建 sdist+wheel；`--sdist`/`--wheel` 控制。SRC: 09-cli
- `uv publish [FILES]`：上传 dist/，`--index testpypi`、`--token`/`--trusted-publishing`。SRC: 09-cli, 03, 10
- `uv pip install`：pip 兼容层，需先有 venv；CI/系统环境加 `--system` 或 `UV_SYSTEM_PYTHON=1`。注意：项目内新增依赖应走 `uv add`，勿用 `uv pip install`（不更新 pyproject/lock）。SRC: 03, 09-cli, 10, 08

### 3.7 CI（GitHub Actions）
- `astral-sh/setup-uv`：输入 `version`、`enable-cache: true`、`python-version`；或 `actions/setup-python` + `python-version-file`。
- 同步测试：`uv sync --locked --all-extras --dev` + `uv run pytest`。`--locked` 断言 lock 与声明一致（CI 校验用）；`--frozen` 直接用现有 lock 不检查（只读快）。SRC: 03, 09-cli(sync)
- 缓存 key `hashFiles('uv.lock')`，job 末尾 `uv cache prune --ci`。SRC: 03

## 4. 场景速查条目建议（供 P3 大纲直接用）

来自 10/08 实战闭环，推荐按「我要…」组织子节：
1. 新建项目 → `uv init`；已有目录 `cd mydir && uv init`
2. 加/删依赖 → `uv add requests` / `uv add -r requirements.txt` / `uv remove`
3. 跑脚本/命令（免 activate）→ `uv run main.py`
4. 进/重建虚拟环境 → `uv venv --python 3.12`；`rm -rf .venv && uv sync`
5. 装指定 Python / 固定版本 → `uv python install 3.12` / `uv python pin 3.12`
6. 临时跑工具 → `uvx ruff` / `uv run --with requests script.py`
7. 常驻全局工具 → `uv tool install ruff`
8. 更新锁/升级某包 → `uv lock --upgrade-package requests`；`uv add --upgrade`
9. 可复现拉取 → `uv sync`（`--locked`/`--frozen` 视场景）
10. 导出 requirements → `uv export -o requirements.txt`
11. 清缓存 → `uv cache clean` / `uv cache prune --ci`
12. 构建发布 → `uv build` → `uv publish`
13. 配国内镜像 → `UV_DEFAULT_INDEX=...` / pyproject `[[tool.uv.index]]`
14. CI 一键装 uv + sync → setup-uv + `uv sync --locked`（附录给片段）

## 5. 迁移对照表（附录素材）

| 旧工具 | 旧命令 | uv 命令 |
|--------|--------|---------|
| venv | python -m venv | uv venv |
| pip | pip install X | 项目级 uv add X（环境级 uv pip install） |
| pip | pip install -r req.txt | uv add -r req.txt（项目级）/ uv pip install -r |
| pip-tools | pip-compile / pip-sync | uv pip compile / uv pip sync |
| pipx | pipx install X | uv tool install X（临时 uvx） |
| conda | conda create -n app python=3.12 | uv init app && uv python pin 3.12 |
| conda | conda activate | 免激活 uv run |
| conda | conda install/remove | uv add/remove |
| conda | conda env update -f env.yml | uv sync |
| conda | conda list | uv pip list / uv tree |
| conda | conda env export | 提交 pyproject + uv.lock |
| poetry | poetry add/remove/lock/shell | uv add/remove/lock/run（模型一致） |

注：pip/venv/poetry→uv 集中对照表官方无，上表来自 08（社区）为主、10 为佐证，写 final note 时标为迁移速查且以官方为准。

## 6. 常见坑与最佳实践（可写进速查「注意」列）

1. 勿在 uv 项目里用 `uv pip install` 加依赖（不同步 pyproject/lock）；新项目默认 `uv add`。
2. `.venv` 可丢弃：删后 `uv sync`/`uv run` 自动重建。
3. `uv.lock` 提交 Git、勿手改。
4. `uv init` 遇已有 pyproject 报错，先移走。
5. CI 优先 `uv sync --locked`；只想用现有 lock 才 `--frozen`。
6. 勿混用 pip/conda install 与 uv 管理同一环境；conda 残留先 `conda deactivate`。
7. 从 conda 迁移勿照抄全部间接依赖，只加直接 import 的包。
8. `uvx` 装工具不影响当前项目（import 失败是预期）。
9. `uv tool install` 后命令不在 PATH → `uv tool update-shell`。
10. 发布到 TestPyPI 可能因其上依赖版本旧解析失败，先装新依赖再 publish。

## 7. 矛盾点 / 需注意

- 国内镜像配置写法在社区不一致（uv.toml vs pyproject；UV_INDEX_URL 已废弃名 vs UV_DEFAULT_INDEX）→ 以官方 indexes 文档为准，并把差异写进「常见坑」。
- 官方文档无集中迁移对照表 → 自建表需标注社区来源为操作经验。
- uv 版本迭代快：命令细节以抓取日（2026-09-05）对应文档为准，final note 标注版本提示。

## 8. 覆盖缺口（P3 写作/后续收集时补）

- 国内镜像具体 URL（清华/阿里）未从权威源核对 → final note 只给官方配置写法 + 指引，避免写死易失效 URL；或后续用 TUNA/阿里官方帮助页补一条来源。
- poetry 逐命令官方对照缺失 → 若用户强调，可在发布前补官方 poetry 迁移声明或标注社区来源。

## 9. 下游交接

- **大纲建议（方向 D）**：§1 项目命令族（init/add/remove/run/sync/lock/tree/export）→ §2 uv venv 与 uv python → §3 uv tool/uvx → §4 uv cache/index → §5 uv build/publish/uv pip → §6 场景速查（上述 14 条）→ §7 迁移对照附录 → §8 CI 片段附录。
- 精读行号锚点：09-cli 各命令 grep 行号已记录（uv run≈474、init≈947、add≈1127、remove≈1541、sync≈2222、lock≈2704、export≈3007、tree≈3417、python install≈6783、find≈7059、pin≈7174、venv≈10071）；写作需要时可在 `research-cache/09_docs_astral_sh.md` 按行定位精确参数。
- 素材与 final note 的引用编号：建议 final note 用脚注编号，来源映射本文件 §2 表。
