## 附录 A：pip / venv / conda / poetry → uv 迁移对照

本附录给两类读者：**老工具用户想换到 uv**（venv/pip/pip-tools/pipx 在 A.1，conda 在 A.2，poetry 在 A.3），以及**迁移前想规划怎么切**（A.4 小结）。用法很简单——找到你正在用的旧命令，照表换成右边 uv 写法；每个 uv 命令的参数、坑和组合都在正文锚点里，本附录只做「旧 → 新」映射，不再展开。

> [!note] 来源与时效声明
> 官方目前**没有**集中发布的「pip/venv/conda/poetry → uv」逐命令对照表。下面 A.1–A.3 的命令映射，主体整理自社区迁移指南（cpython666.github.io，2026-07），属**操作经验**而非官方承诺；uv「一个工具整合 venv + pip + pip-tools + pipx + poetry 类能力」的定位有 Real Python 佐证[^ca-1][^ca-2]。命令细节一律以 `uv --version` 对应的官方文档为准（项目指南 docs.astral.sh/uv/guides/projects/、CLI 参考 docs.astral.sh/uv/reference/cli/）。

读表前先记住两个心智模型，它们能解释表里 80% 的「为什么要这么换」：

- **旧工具各管一段，uv 一段管到底**：搭环境（venv/conda）、装包（pip）、锁清单（pip-tools）、全局工具（pipx）、解释器版本（pyenv/conda），在 uv 里收敛成一个工具 + 三个文件（pyproject 声明 / uv.lock 锁 / .venv 现场，关系见 §2.1）。
- **分清「项目级」与「环境级」**：`uv add` 是项目级——写声明、更新锁、装现场三件事一起做；`uv pip install` 是低层兼容层——只动当前环境，**不**更新 pyproject/lock。迁移旧项目时最常犯的错，就是把后者当 `pip install` 用。

> [!tip] 大白话：旧工具链是四个各管一段的部门，uv 是认「项目目录」的跟班
> 把 venv、pip、pip-tools、pipx 想成四个各管一段的人：一个搭环境、一个装包、一个整理精确清单、一个管全局工具；uv 一个人把四份工全包了。它认的不是「你激活了哪个环境」，而是「你在哪个项目目录里」——目录里声明（pyproject）和锁（uv.lock）齐全，就自动把环境配好。所以老习惯里「先激活再操作」那一步，在 uv 里大多变成直接 `uv run`。

### A.1 venv / pip / pip-tools / pipx 用户对照

这组用户迁移成本最低：命令几乎一一对应，差异只在「要不要先 activate」和「项目级 vs 环境级」这两点。

| 旧习惯 | 换成 uv | 说明（锚点） |
| --- | --- | --- |
| venv：`python -m venv .venv` | `uv venv` | 默认就建 `.venv`；可用 `--python 3.12` 指定解释器、缺则自动下载 → §3.1 |
| venv：`source .venv/bin/activate`（PowerShell 为 `Activate.ps1`） | 免激活，直接 `uv run ...` | uv 自动发现项目 `.venv`；只有 IDE 需指解释器路径时才手动激活 → §2.4、§3.1 |
| pip：`pip install X` | 项目级 `uv add X`；环境级 `uv pip install X` | 项目内加依赖走 `uv add`（写 pyproject + 锁）；`uv pip install` 只改环境不动声明，勿用它加项目依赖 → §2.3、§6.3 |
| pip：`pip install -r requirements.txt` | 项目级 `uv add -r requirements.txt`；环境级 `uv pip install -r` | 迁移旧 requirements 首选 `uv add -r`，一次性转为声明 → §2.3、§6.3 |
| pip-tools：`pip-compile` + `pip-sync` | `uv pip compile` + `uv pip sync` | uv 的 pip 兼容层保留这组低层命令；项目内更推荐 pyproject + `uv sync`（一条命令替代两步）→ §6.3、§2.5 |
| pipx：`pipx install X` | `uv tool install X` | 常驻全局工具；装完命令不在 PATH 先 `uv tool update-shell` → §4.3 |
| pipx：`pipx run X` | `uvx X`（= `uv tool run`） | 临时跑一次、不落盘、不污染项目 → §4.1 |

### A.2 conda 用户对照

conda 迁移的**心智差异最大**：conda 维护的是「带名字的全局环境」（`conda activate app`），uv 维护的是「项目目录里的 `.venv`」。所以迁移的本质是把你原来写在 `environment.yml` 里的一坨东西，拆到三个文件里：

- **Python 版本** → `.python-version`（用 `uv python pin` 写，见 §3.3）；
- **纯 Python / PyPI 包** → `pyproject.toml`（用 `uv add` 声明，见 §2.3）；
- **二进制 / 系统依赖**（`cudatoolkit`、编译器、GDAL/FFmpeg 库等）→ 留在 conda 或交给系统包管理器 / Docker[^ca-3]。

| conda 习惯 | 换成 uv | 说明（锚点） |
| --- | --- | --- |
| `conda create -n app python=3.12` | `uv init app && cd app` + `uv python pin 3.12` | 命名环境 → 项目目录；`python=` 版本号写进 `.python-version` → §2.2、§3.3 |
| `conda activate app` | 免激活，直接 `uv run ...` | 在项目目录内 uv 自动用 `.venv`，不需要「激活名」→ §2.4 |
| `conda install X` | `uv add X` | 写声明 + 更新锁 + 装环境 → §2.3 |
| `conda remove X` | `uv remove X` | → §2.3 |
| `conda env update -f environment.yml` | `uv sync` | 依赖来源从 yml 换成 pyproject + uv.lock → §2.5 |
| `conda env export` | 提交 `pyproject.toml` + `uv.lock` | `uv.lock` 是精确跨平台锁；clone 后用 `uv sync --locked` 复现 → §2.1、§7.9 |
| `conda list` | `uv pip list`（已装包）或 `uv tree`（依赖树） | → §6.3、§2.7 |
| `conda run -n app python x.py` | `uv run python x.py` | → §2.4 |
| `conda env remove -n app` | 删除 `.venv` | 下次 `uv sync` 自动重建，环境本就是一次性现场 → §3.1 |

conda 老用户迁第一个小项目时，通常就是下面三步（`uv add` 会自动同步 `.venv` 并生成 `uv.lock`，等价你原来分开跑的 `conda env update`）：

```bash
uv init app && cd app     # 1. 项目目录替代命名环境
uv python pin 3.12        # 2. python=3.12 → 写入 .python-version
uv add requests pandas    # 3. 只加直接依赖；间接依赖交给 uv 解析
```

迁完先验证解释器没指错（应指向项目 `.venv`，而不是残留的 conda 环境）：
`uv run python -c "import sys; print(sys.executable)"`[^ca-3]

**conda 迁移注意**（都来自社区实战踩坑，见深度素材坑 6、7）[^ca-4]：

- **勿照抄全部间接依赖**：`conda list` 里包含大量间接依赖和 conda 自己的底层包。只添加代码里**直接 import 或直接依赖**的包，间接依赖交给 `uv lock` 解析；照单全抄会让迁移第一步就带上垃圾依赖。
- **先 `conda deactivate` 再迁移**：若终端默认显示 `(base)`，先退出，避免 conda 的激活态串进 uv 项目、让 uv 把依赖装进 conda 环境。可选 `conda config --set auto_activate_base false`。
- **勿混用安装器管同一环境**：不要在同一环境里既 `pip install`/`conda install` 又用 uv——uv 管理的 `.venv` 只能由 uv 维护，混用会导致「实际装了 X，但 pyproject/lock 没记录 X」的分叉。
- **勿为「迁移干净」强行卸载 conda**：两个工具先共存、逐项目迁移；二进制依赖暂时继续用 conda 管完全没问题。

> [!tip] 大白话：迁移只点你要的菜，配菜交给后厨
> 把 `conda list` 想成前一桌客人留下的完整账单——上面既有你点的菜（requests、pandas），也有后厨配好的调料和半成品（一大堆底层依赖）。照单全抄既不卫生也易错。迁移时只点你真正要的菜（代码里直接 import 的包），间接依赖让 uv 的后厨按 `uv.lock` 现配。

### A.3 poetry 用户对照

poetry 用户迁移成本最低，因为**模型本来就一致**：pyproject 声明 + 锁文件 + `run` 执行。多数命令只是换个名字。注意：poetry 的逐命令官方对照同样没有集中发布，下表为按命令面整理的近似表，**以官方为准**[^ca-6]。

| poetry 习惯 | 换成 uv | 说明（锚点） |
| --- | --- | --- |
| `poetry add X` | `uv add X` | 同样写声明 + 更新锁 + 装环境 → §2.3 |
| `poetry remove X` | `uv remove X` | → §2.3 |
| `poetry lock` | `uv lock` | 只重解析锁文件、不安装；日常不必手跑 → §2.6 |
| `poetry install` | `uv sync` | 按锁文件同步 `.venv` → §2.5 |
| `poetry shell` | `uv run ...` | uv 没有「常驻子 shell」：每次 `uv run` 起一个子进程跑完即退，免激活 → §2.4 |
| `poetry run X` | `uv run X` | `run` 的执行入口在 uv 里收敛为统一的 `uv run` → §2.4 |

两点差异提醒：一是 poetry 的 `shell` 会给你一个已激活的交互终端，uv 刻意不做这件事（要长驻终端就显式激活 `.venv`，写法见 §3.1）；二是 poetry 锁文件与 uv.lock 不通用，迁移后以 `uv.lock` 为准，老锁文件别提交。

### A.4 迁移建议小结

> [!tip] 大白话：.venv 是租来的临时工位，pyproject + uv.lock 才是你的档案
> 把 `.venv` 想成临时工位：随时可退租重租，桌子怎么摆（装了哪些包）都看你档案里怎么写（pyproject + uv.lock），重新入职（`uv sync`）就自动恢复原样。所以团队协作、换机器、上 CI 都只认「档案」，不认任何人的「现场」。这也正是 conda 时代「维护一个带名字的环境」要改掉的惯性。

1. **从「直接依赖」起步**：只收集代码直接 import / 直接依赖的包，间接依赖全部交给 `uv lock`。手头有质量较好的 `requirements.txt` 可直接 `uv add -r requirements.txt`；conda 用户可用 `conda env export --from-history` 看历史直接依赖[^ca-3][^ca-4]。
2. **二进制与系统依赖单独放**：CUDA、编译器、GDAL/FFmpeg 这类不是 PyPI 包，继续留给 conda / 系统包管理器 / Docker，uv 只管 Python 依赖[^ca-3]。
3. **别混用安装器管同一环境**：同一 `.venv` 里不要既 pip/conda 又 uv；conda 用户先 `conda deactivate` 再跑 uv，避免激活态串环境[^ca-4][^ca-5]。
4. **现场可丢、档案要提交**：`.venv` 随时 `rm -rf .venv && uv sync` 重建（见 §7.4）；提交 `pyproject.toml` + `uv.lock` 才是团队可复现的依据。
5. **conda 不必急着卸载**：先共存、逐项目迁移，等确认无碍再逐步离开。
6. **迁完先验证**：`uv run pytest` 跑通测试；`uv run python -c "import sys; print(sys.executable)"` 确认解释器指向项目 `.venv`，而不是 conda 残留。

迁移完成、日常命令上手后，下一步多半是把项目放进 CI——附录 B 给了一份可直接粘贴的 GitHub Actions 片段（setup-uv + `uv sync --locked` + 缓存清理），照抄即可。

