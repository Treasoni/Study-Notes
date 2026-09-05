# 《uv 常用命令速查手册》学习笔记大纲

> 笔记类型：常用命令速查手册（命令族骨架 + 场景速查混合，组织主线 D）
> 笔记定位：**参考/工具型**，非叙事型教程。四种叙事模板中与「实战笔记」最接近，但按官方命令族而非学习阶段组织，因此不套用单一模板，采用混合结构（已与用户确认方向 D）。
> 预计总篇幅：约 25–32 页（中文 Markdown，页面估算随排版浮动）
> 章节数：9（正文第 1–7 章 + 附录 A/B）
> 目标深度：上手（覆盖日常 80% 场景）｜读者：已有 uv 基础（已读过「uv 配置虚拟环境」笔记）
> 素材抓取日期：2026-09-05（uv 迭代快，定稿时标注以 `uv --version` 对应官方文档为准）

## 组织结构与防重复约定

本手册分三块，明确区分「命令族骨架」「场景速查」「附录」，避免同一内容写两遍：

1. **命令族骨架（第 1–6 章）**：按官方命令族组织，是**每个命令参数、选项、坑的唯一详述地**。每章末尾配「常用场景组合」子节（本族内部怎么组合用）。
2. **场景速查（第 7 章）**：纯检索索引。14 条「我要…」各自只给「场景 → 1 行命令 → 锚点（→ 见 §x.y）」。**不重复展开参数**，参数一律跳回命令族章。
3. **附录（A/B）**：迁移对照 + CI 片段，供特定读者取用。

锚点约定：正文用 § 编号标注（如 §2.4）。Obsidian 定稿时由 chapter-writer 把 `§2.4` 映射为 `[[#标题]]` 或「见「项目命令族 · uv run」」文本链接。素材引用采用「02 素材 §x.y + research-cache 编号（01–10）」两级标注。

与既有笔记的关系：已有 `python/如何用uv配置Python虚拟环境.md`（虚拟环境配置实战）。本篇是命令速查手册，只给 `uv venv` 命令面，不重讲原理，用「→ 见既有笔记」交叉引用。

---

———— 第一部分：命令族骨架（正文第 1–6 章）————

## 第 1 章 快速上手：5 条命令跑通日常（引子，可选轻量）

- **篇幅**：短（约 1–2 页）
- **覆盖要点**：本手册怎么读（约定 + 版本提示 + 与既有笔记关系）；5 条核心命令总览表；60 秒端到端最小流程（建项目 → 加依赖 → 写脚本 → 运行）
- **素材引用**：02 素材 §1、§3.1、§3.2、§9；research-cache 05_docs_astral_sh.md、09_docs_astral_sh.md(cli: run≈474/init≈947/venv≈10071)
- **代码示例**：2 个 —— ① 5 命令 × 用途 × 详述章的总览表（表格内嵌命令）；② 端到端流程代码块（`uv init demo && cd demo` → `uv add requests` → 4 行 `main.py` → `uv run main.py`）
- **子节结构（H3）**：
  - §1.1 阅读约定：版本提示、§ 锚点约定、交叉引用既有笔记
  - §1.2 5 条核心命令总览（uv init / uv add / uv run / uv sync / uv venv，各一行用途，深度指向第 2–3 章）
  - §1.3 60 秒端到端最小流程（给读者「原来就这么简单」的整体心智模型；不做选项展开）

## 第 2 章 项目命令族：init / add / remove / run / sync / lock / tree / export

- **篇幅**：长（约 6–7 页）
- **覆盖要点**：四文件关系（pyproject + .python-version → uv.lock → .venv）与 `uv run` 自动同步心智模型；8 条命令各自用途、常用参数、最小示例、注意点；`uv run` vs `uv sync` 分工；本族常用场景组合（日常循环 / 彻底重建环境 / 复现拉取）
- **素材引用**：02 素材 §3.1、§5、§6(坑 1–5)、§9；research-cache 05_docs_astral_sh.md、09_docs_astral_sh.md(cli: init≈947/add≈1127/remove≈1541/run≈474/sync≈2222/lock≈2704/tree≈3417/export≈3007)、08_cpython666_github_io.md、10_realpython_com.md
- **代码示例**：约 10 个最小示例，示例主题 = 8 条命令各 1 个 + 1 个重建环境组合；全部 1–3 行
- **子节结构（H3）**：
  - §2.1 先修：四个文件的职责（表格式对照：pyproject=声明 / .python-version=解释器 / uv.lock=锁定解析 / .venv=安装现场；`uv.lock` 提交 VCS）
  - §2.2 `uv init` —— 新建项目（默认生成物、`--vcs none`、已有目录 `cd mydir && uv init`、遇已有 pyproject 报错）
  - §2.3 `uv add` / `uv remove` —— 增删依赖（版本约束 `==`、`--dev`、`-r requirements.txt`、git 源、`--editable ../lib`、`--upgrade`、`--no-sync`/`--frozen` 旁路）
  - §2.4 `uv run` —— 统一执行入口（免 activate、运行前自动校验/同步、选项须置命令前、PEP 723 内联依赖、`--env-file`）
  - §2.5 `uv sync` —— 同步 .venv（默认 exact 删多余包、`--inexact`、`--locked` vs `--frozen`）
  - §2.6 `uv lock` —— 只解析锁文件不安装（`--upgrade-package`、日常不必手跑）
  - §2.7 `uv tree` / `uv export` —— 依赖树查看与导出 requirements.txt（tree 的 `-d`/`--invert`/`--package`；export 默认先 re-lock 除非 `--frozen`）
  - §2.8 常用场景组合（本族）：① 日常循环 = `uv add` + `uv run`（自动同步）；② 彻底重建 = `rm -rf .venv && uv sync`；③ CI/复现 = `uv sync --locked`（详见附录 B）。只给组合不给 14 条清单式内容（那是第 7 章职责）

## 第 3 章 Python 版本与虚拟环境：uv python / uv venv

- **篇幅**：中（约 3–4 页）
- **覆盖要点**：`uv venv` 创建环境（默认 `.venv`、命名、`--python` 缺则自动下载、activate 与否、删除重建）；`uv python` 的 install/list/find（managed Python、`--default`）；`uv python pin` 固定项目/全局 Python（`.python-version`、`--global`）；解释器发现顺序简表；与既有笔记交叉引用
- **素材引用**：02 素材 §3.2、§6(坑 2)；research-cache 04_docs_astral_sh.md、05_docs_astral_sh.md、06_docs_astral_sh.md、09_docs_astral_sh.md(cli: python install≈6783/find≈7059/pin≈7174/venv≈10071)
- **代码示例**：约 6 个 —— ① `uv venv`（默认 + 命名）；② `uv venv --python 3.11`；③ activate/deactivate（bash 与 PowerShell 两行对照）；④ `uv python install 3.12`（+`--default`）；⑤ `uv python find`；⑥ `uv python pin 3.12` / `--global`
- **子节结构（H3）**：
  - §3.1 `uv venv` —— 创建虚拟环境（无需 activate、uv 自动发现 `.venv`；手动激活写法；已存在先删重建；`.python-version` 决定解释器）→ 原理细节链到既有笔记
  - §3.2 `uv python` —— 安装/列出/查找解释器（install/list/find、`--default` 才装 `python`/`python3` 命令）
  - §3.3 `uv python pin` —— 固定版本（写 `.python-version`；`--global` 用户级）+ 解释器发现顺序简表（`.venv` → managed 目录 → PATH → Windows 注册表）
  - §3.4 常用场景组合（本族）：装指定版本后建 venv；`rm -rf .venv && uv sync` 重建（指向第 2 章）

## 第 4 章 临时与全局工具：uvx / uv tool / uv run --with

- **篇幅**：中（约 3–4 页）
- **覆盖要点**：`uvx`（= `uv tool run`）临时运行工具进隔离环境不持久；`uvx --from` / `uvx --with`；`uv run --with` 在项目环境里跑带临时依赖的脚本；`uv tool install/list/upgrade/uninstall/update-shell` 持久安装与 PATH；三者分工决策（临时工具 vs 项目内钉版本 vs 常驻工具）；工具不影响当前项目
- **素材引用**：02 素材 §3.3、§6(坑 8、9)；research-cache 07_docs_astral_sh.md、09_docs_astral_sh.md(run≈474)
- **代码示例**：约 6 个 —— ① `uvx ruff check .`；② `uvx --from httpie http`；③ `uvx --with mkdocs-material mkdocs`；④ `uv run --with requests script.py`；⑤ `uv tool install ruff`；⑥ `uv tool list` + `uv tool update-shell`
- **子节结构（H3）**：
  - §4.1 `uvx` —— 临时跑工具（`uv tool run` 别名、`--from` 指定包/版本、`--with` 附加依赖）
  - §4.2 `uv run --with` —— 项目环境内的一次性额外依赖（PEP 723 脚本头的另一种做法）
  - §4.3 `uv tool` —— 常驻全局工具（install/upgrade/list/uninstall/update-shell、`uv tool dir --bin`、工具不进项目 import 是预期）
  - §4.4 分工决策 + 常用场景组合（本族）：一次性临时工具 → uvx；pytest/mypy 等需钉进项目 → uv run；ruff 等常驻 → uv tool install

## 第 5 章 缓存与索引/镜像：uv cache / 索引配置

- **篇幅**：中（约 3–4 页）
- **覆盖要点**：`uv cache dir/clean/prune`（`prune --ci` 清预构建 wheel）；旁路开关 `--refresh` / `--reinstall` / `--no-cache` 何时用；索引四种写法（pyproject `[[tool.uv.index]]` / CLI `--index`/`--default-index` / 环境变量 `UV_INDEX`/`UV_DEFAULT_INDEX` / 旧 `--index-url` 兼容）；default 索引语义（default=true 即排除 PyPI）；索引凭据；国内镜像（只给官方写法 + 「以镜像服务说明为准」，不写死易失效 URL）
- **素材引用**：02 素材 §3.4、§3.5、§6、§7、§8(缺口)；research-cache 01_docs_astral_sh.md、02_docs_astral_sh.md、08_cpython666_github_io.md、09_docs_astral_sh.md
- **代码示例**：约 5 个 —— ① `uv cache dir` / `uv cache clean` / `uv cache prune --ci`（可合 1 组）；② `uv sync --refresh`（含与 `--reinstall` 对比）；③ pyproject `[[tool.uv.index]]` TOML 片段；④ `export UV_DEFAULT_INDEX=...`；⑤ CLI `--default-index` 单次覆盖
- **子节结构（H3）**：
  - §5.1 `uv cache` —— 定位/清理/剪枝（dir/clean/prune、`--ci` 场景）
  - §5.2 缓存旁路开关（`--refresh` 重验证仍写缓存、`--reinstall` 强装、`--no-cache`；多数场景 `--refresh` 更优）
  - §5.3 索引与国内镜像（四种写法优先级、default 语义、凭据环境变量；社区写法不一致 → 以官方 indexes 文档为准的「注意」框）
  - §5.4 常用场景组合（本族）：CI 末尾 `uv cache prune --ci`；换镜像后单次 `--default-index` 验证（指向附录 B）

## 第 6 章 构建发布与 pip 兼容层：uv build / uv publish / uv pip

- **篇幅**：中（约 2–3 页）
- **覆盖要点**：`uv build` 构建 sdist+wheel（`--sdist`/`--wheel`）；`uv publish` 上传（`--index testpypi`、`--token`/可信发布、TestPyPI 依赖旧导致解析失败的坑）；`uv pip` 兼容层（install/compile/sync、`--system` 或 `UV_SYSTEM_PYTHON=1`、需先有 venv）；「项目内加依赖勿用 `uv pip install`，走 `uv add`」告诫
- **素材引用**：02 素材 §3.6、§6(坑 1、10)；research-cache 03_docs_astral_sh.md、08_cpython666_github_io.md、09_docs_astral_sh.md、10_realpython_com.md
- **代码示例**：约 5 个 —— ① `uv build`（默认同建 sdist+wheel）；② `uv publish`；③ `uv publish --index testpypi --token ...`；④ `uv pip install -r requirements.txt`（venv 内）+ `uv pip install --system` 对照；⑤ `uv pip list` / `uv pip compile` 简例
- **子节结构（H3）**：
  - §6.1 `uv build` —— 构建发行包
  - §6.2 `uv publish` —— 发布到索引（含 TestPyPI 坑）
  - §6.3 `uv pip` —— pip 兼容层（适用边界：已有 venv / 系统环境；pip-tools 用户对应 compile/sync）
  - §6.4 常用场景组合（本族）：构建发布链 `uv build` → `uv publish`；「勿用 uv pip install 加项目依赖」告诫框（坑 1）

---

———— 第二部分：场景速查（第 7 章）————

## 第 7 章 场景速查：14 条「我要…」（跨族检索入口）

- **篇幅**：长（约 4–5 页，条目短、表格/代码密集，散文极少）
- **覆盖要点**：14 条「我要…」每一条 = 「场景一句话 → 1–2 行命令 → 跳转锚点」；本部分是手册的**前门索引**，参数详解一律 `→ 见 §x.y`，不重复第 2–6 章内容；开头给 1 句使用说明（先按场景查这里，再看锚点进正文）
- **素材引用**：02 素材 §4（14 条直接取自该节，源自 10/08 实战闭环）+ 各命令族锚点（§3.1–§3.6）
- **代码示例**：14 个超短 snippet（每条 1–2 行命令；命令族章已展开的选项不在此重复）
- **子节结构（H3，每条即一个子节）**：
  - §7.1 我要新建项目 → `uv init`（→ 见 §2.2）
  - §7.2 我要加/删依赖 → `uv add requests` / `uv remove requests`（→ 见 §2.3）
  - §7.3 我要免激活跑脚本/命令 → `uv run main.py`（→ 见 §2.4）
  - §7.4 我要进/重建虚拟环境 → `uv venv`；`rm -rf .venv && uv sync`（→ 见 §3.1、§2.5）
  - §7.5 我要安装/固定指定 Python → `uv python install 3.12` / `uv python pin 3.12`（→ 见 §3.2、§3.3）
  - §7.6 我要临时跑一个工具 → `uvx ruff`；`uv run --with requests script.py`（→ 见 §4.1、§4.2）
  - §7.7 我要常驻安装全局工具 → `uv tool install ruff`（→ 见 §4.3）
  - §7.8 我要升级某包/更新锁 → `uv lock --upgrade-package requests`；`uv add --upgrade`（→ 见 §2.6、§2.3）
  - §7.9 我要可复现拉取环境 → `uv sync --locked`（只读用 `--frozen`）（→ 见 §2.5）
  - §7.10 我要导出 requirements.txt → `uv export -o requirements.txt`（→ 见 §2.7）
  - §7.11 我要清理缓存 → `uv cache clean` / `uv cache prune --ci`（→ 见 §5.1）
  - §7.12 我要构建并发布包 → `uv build` → `uv publish`（→ 见 §6.1、§6.2）
  - §7.13 我要配国内镜像 → `export UV_DEFAULT_INDEX=...`（→ 见 §5.3，URL 以镜像服务说明为准）
  - §7.14 我要在 CI 里一键装 uv 并同步 → setup-uv + `uv sync --locked`（→ 见附录 B）

---

———— 附录 ————

## 附录 A：pip / venv / conda / poetry → uv 迁移对照

- **篇幅**：中（约 2–3 页，表驱动）
- **覆盖要点**：按旧工具分组迁移对照表（venv / pip / pip-tools / pipx / conda / poetry）；conda→uv 专项注意（勿照抄间接依赖、先 `conda deactivate` 再迁移）；来源标注（官方无集中对照表，本表为社区操作经验 + Real Python 佐证，以官方文档为准）
- **素材引用**：02 素材 §5（对照表）、§6(坑 6、7)、§7；research-cache 08_cpython666_github_io.md（主）、10_realpython_com.md（佐）
- **代码示例**：0 个独立长代码块；对照命令以表格行内嵌（约 18 行映射）+ 可选 1 组 conda→uv 三步迁移演练（`uv init` → `uv python pin` → `uv sync`，3 行）
- **子节结构（H3）**：
  - A.1 venv / pip / pip-tools / pipx 用户对照（`python -m venv`→`uv venv`、`pip install X`→`uv add X`、`pip-compile/sync`→`uv pip compile/sync`、`pipx install`→`uv tool install`/`uvx`）
  - A.2 conda 用户对照（`conda create -n app python=3.12`→`uv init app` + `uv python pin 3.12`、`conda activate`→免激活 `uv run`、`conda env update`→`uv sync` 等）+ 迁移注意
  - A.3 poetry 用户对照（`add/remove/lock/shell`→`uv add/remove/lock/run`，模型一致；标注社区来源、以官方为准）
  - A.4 迁移建议小结（从「直接依赖」起步，间接依赖交 `uv lock`）

## 附录 B：GitHub Actions CI 片段

- **篇幅**：短（约 1–2 页）
- **覆盖要点**：`astral-sh/setup-uv` action 用法（`version`、`enable-cache: true`、`python-version`）；同步 + 测试段（`uv sync --locked --all-extras --dev` + `uv run pytest`）；缓存 key `hashFiles('uv.lock')`；job 末尾 `uv cache prune --ci`；`--locked` vs `--frozen` 在 CI 的语义；备选 `actions/setup-python` + `python-version-file` 写法
- **素材引用**：02 素材 §3.7、§6(坑 5)；research-cache 03_docs_astral_sh.md、09_docs_astral_sh.md(sync≈2222)、10_realpython_com.md
- **代码示例**：1 个完整 workflow YAML（约 20–30 行，含 setup-uv / enable-cache / sync --locked / pytest / cache prune --ci）+ 1 个 `actions/setup-python` 备选片段
- **子节结构（H3）**：
  - B.1 最小 workflow（astral-sh/setup-uv 版，完整 YAML）
  - B.2 关键点说明（`--locked` 校验 lock 一致性 vs `--frozen` 只读跳过；缓存 key 与 prune --ci 的配合）
  - B.3 备选：`actions/setup-python` + `python-version-file` 用法

---

## 学习路径说明

> 本手册为速查/参考性质，以下路径用于指导写作顺序与读者定位；定稿时可在 Obsidian 中折叠成开头一段 20 字内的「使用说明」，不必作为独立正文章节。

### 前置要求
- 已有 uv 基础：理解 uv 替代 pip/venv 的角色，已发布过「uv 配置虚拟环境」笔记（第 3 章会交叉引用，不重复原理）
- 已安装 uv（版本以抓取日 2026-09-05 对应文档为参考，正文给出 `uv --version` 自查提示）
- 基本 Python 项目概念：pyproject.toml、虚拟环境、依赖锁定

### 学完能做什么
- 覆盖日常 80% 高频命令：建项目、加删依赖、免激活跑脚本、重建/进虚拟环境、装指定 Python、临时与常驻工具、清缓存、配索引/镜像、构建发布
- 用「场景速查」当入口快速检索，按锚点跳回命令族正文看参数细节
- pip/venv/conda/poetry 老用户按附录 A 迁移；有 CI 需求按附录 B 直接粘贴片段

### 建议学习顺序（含预估）
1. 先读第 1 章（5 分钟）：建立「uv init → add → run」整体心智
2. 顺序读第 2–3 章（约 40 分钟）：项目命令族 + venv/python，是本手册主体
3. 按需读第 4–6 章（各约 15–20 分钟）：工具、缓存/镜像、构建发布（用到再精读）
4. 第 7 章作为常驻检索页（日常查表用），读完正文后整体过一遍即可（约 10 分钟）
5. 迁移用户看附录 A；CI 用户看附录 B（均为按需取用）
6. 速查手册不要求线性读完；写作顺序即上述 1→5，每章自洽可独立查阅

## 待写作阶段补的缺口（来自 02 素材 §8）
- 国内镜像具体 URL 未从权威源核对：附录/§5.3 只给官方配置写法 + 指引，不写死易失效 URL（除非发布前补 TUNA/阿里官方帮助页来源）
- poetry 逐命令官方对照缺失：附录 A.3 标注社区来源、以官方为准
