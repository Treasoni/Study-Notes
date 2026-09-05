## 第 4 章 临时与全局工具：uvx / uv tool / uv run --with

前两章的 `uv run` / `uv sync` 都围绕「项目」展开：先声明依赖，再在 `.venv` 里跑。但日常还有两类命令工具不走项目流程：一是只想**临时**跑一下别人写好的 CLI（比如 ruff），又不想弄脏当前项目；二是想把某个高频工具**长久**装进系统、随时敲命令就能用。本章讲 uv 的三件套 —— `uvx`（临时）、`uv tool`（常驻）、`uv run --with`（项目内临时加依赖）—— 以及它们之间的选用边界。

> 版本说明：本章命令与输出对应 2026-09-05 抓取的官方文档；uv 迭代快，细节以 `uv --version` 对应的文档为准（阅读约定见第 1 章）。

### §4.1 `uvx` —— 临时跑工具

`uvx` 是 `uv tool run` 的别名，两者行为完全一致[^c4-1]。它的作用一句话概括：**把某个包提供的命令行工具装进一个临时、隔离的环境里运行，跑完不留下任何东西**，不写 `pyproject.toml`、不碰你的 `.venv`、不进当前项目。

最简单的用法，命令名与包名一致时直接写：

```bash
# 临时拉一个隔离环境装 ruff，并对当前目录做 lint 检查
$ uvx ruff check .
```

> [!tip] 大白话
> 把 `uvx` 想成「叫外援在门外的临时工位干活」：需要 ruff 时，uv 在项目**外面**搭一个一次性的小隔间，把 ruff 请进去干活；活干完隔间拆掉。你项目里的大工位（`.venv`、`pyproject.toml`）一根头发都没动。所以工具不会进项目，项目也 `import` 不到它——这是设计使然，不是装坏了。

#### 命令名 ≠ 包名：用 `--from`

多数时候包名和命令名相同（`ruff` 包提供 `ruff` 命令），但有时不同：`http` 命令由 `httpie` 包提供。这时要 `--from` 指明「从哪个包里找命令」[^c4-1]：

```bash
# http 命令来自 httpie 这个包，用 --from 指明
$ uvx --from httpie http https://example.org

# 指定版本：命令名后跟 @ 只能写精确版本
$ uvx ruff@0.3.0 check .

# 需要版本范围（或带 extras、git 源）时，一律改用 --from + PEP 440 写法
$ uvx --from 'ruff>0.2,<0.4' ruff check .
```

要点：`uvx ruff@0.3.0` 的 `@` 语法**只能表达精确版本**；要表达范围、extra 或 git 源，用 `--from`[^c4-1]。`--from` 和 `@` 后面的命令参数跟在命令名之后，uvx 原样透传给工具，不会误解析。

> [!tip] 大白话
> 命令名是「菜名」，包名是「店名」。多数时候菜名和店名相同，直接喊 `uvx 菜名`；当这道菜在别家店（`http` 命令由 `httpie` 包提供），就用 `--from 店名 菜名` 告诉 uv 去哪家点。想点某个具体批次（精确版本 `ruff@0.3.0`）就写批号，想限定一个区间只能走 `--from`。

#### 给工具附加依赖：用 `--with`

有些工具的能力要靠额外依赖才完整。例如 `mkdocs` 默认不含 material 主题，临时跑文档站时用 `--with` 把主题一起装进这次隔离环境[^c4-1]：

```bash
# mkdocs-material 只对这一次运行生效，mkdocs 默认自带里没有它
$ uvx --with mkdocs-material mkdocs build
```

#### 与常驻安装的关系

如果你已经用 `uv tool install ruff`（见 §4.3）装过 ruff，直接敲 `uvx ruff` 会**复用已装版本**，而不是再拉一个临时环境；想强制走临时环境用 `--isolated`[^c4-2]。另外注意：`uvx` 只是 `uv tool run` 的缩写，其余工具操作（install / list / upgrade…）都必须写完整的 `uv tool` 前缀[^c4-1]。

### §4.2 `uv run --with` —— 项目内的一次性额外依赖

`uv run` 在第 2 章是「项目统一执行入口」：用项目 `.venv` 跑命令，跑前自动同步（见 §2.4）。给它加 `--with <pkg>`，语义变成：**在项目环境之上，临时叠一层额外依赖**去跑这条命令/脚本。这层依赖不进 `pyproject.toml`、不进 `uv.lock`，且允许与项目既有依赖冲突（uv 把它放在一个独立的临时层里解析）[^c4-2]。

典型场景：你的项目依赖里没有 `requests`，但某个一次性脚本想用它抓个数据，你又不想为这一次把 `requests` 永久加进项目：

```python
# demo.py —— 一次性脚本：想用 requests，但不想改动项目依赖
import requests

r = requests.get("https://httpbin.org/json")
print("status:", r.status_code)
```

```bash
# 在项目目录内执行：requests 只对这次运行可见
$ uv run --with requests demo.py
status: 200
```

`uv run --with` 与 PEP 723 的关系：§2.4 提到脚本顶部可以用 `# /// script` 内联声明依赖，让脚本自带依赖随文件走。`--with` 是它的**另一种做法**——依赖不写进文件、只在命令行临时给。取舍：脚本要分享/提交就优先 PEP 723 头（依赖跟着文件走）；只是自己临时跑一次，用 `--with` 更省事、文件保持干净。

> [!tip] 大白话
> 项目环境是你布置好的常驻工位（依赖都摆在桌面上）。`--with requests` 等于「临时从隔壁借一台 `requests` 计算器用一下」，用完还回去，工位布置不变——`pyproject.toml` 和 `uv.lock` 一行都不会多。

> [!note] 与 uvx 的区别
> `uvx` 跑的是「别人的命令行工具」，与项目完全隔离；`uv run --with` 跑的是**在项目语境里的脚本/命令**，底层复用项目环境，只是临时多给几个包。若脚本/命令需要能 `import` 你项目自己的代码（典型如 `pytest`），必须用 `uv run`，不能用 `uvx`——这正是 §4.4 的核心分界。

### §4.3 `uv tool` —— 常驻全局工具

`uvx` 每次都现装，高频工具这么用就浪费了。`uv tool install` 把工具**持久**安装到一个独立虚拟环境里，并把可执行文件链接到「工具 bin 目录」（该目录在 PATH 上），之后脱离 uv 直接敲命令即可[^c4-1]。

```bash
# 常驻安装 ruff：装进独立环境，可执行链到 PATH
$ uv tool install ruff

# 装完直接可用（不再需要 uvx 前缀）
$ ruff --version

# 升级 / 卸载
$ uv tool upgrade ruff
$ uv tool uninstall ruff
```

与 `uvx` 的一个关键差别：`uv tool install` 操作的是**包**，会把该包提供的**所有**可执行一起装（如 `httpie` 会同时提供 `http`、`https`、`httpie` 三个命令）；而 `uvx` 只跑你点名的那一个命令[^c4-1]。

想知道工具装在哪，用这两个查询命令（输出因机器而异，直接跑即可看到自己机器上的值）：

```bash
# 工具独立环境所在目录（Windows 默认在 %APPDATA%\uv\data\tools 一带）
$ uv tool dir

# 可执行文件（被链到 PATH 的 bin 目录）位置
$ uv tool dir --bin
```

> [!warning] 坑 8：工具不进项目，`import` 失败是预期
> `uv tool install ruff` 之后，`ruff` 命令可用，但在**项目里** `python -c "import ruff"` 会报 `ModuleNotFoundError`。这是隔离设计：工具住在自己的独立环境里，模块不会注入当前项目，从而避免不同工具的依赖互相打架[^c4-1]。同理 `uvx` 临时跑的工具也不会影响当前项目。想给项目加真正可 import 的依赖，走 `uv add`（见 §2.3）。

> [!tip] 大白话
> `uv tool install` = 给工具一个**常驻工位 + 门口名牌**：工具本身住进自己的独立小房间（`uv tool dir`），但把「ruff」这块名牌挂到大楼门禁（PATH 上的 bin 目录），你随时喊名字它就应。它只在自己的房间上班，不会搬进你项目的办公室——所以项目里 `import ruff` 找不到，很正常。

#### 命令不在 PATH：`uv tool update-shell`

装完后如果直接敲 `ruff` 报 `command not found`，通常是**工具 bin 目录没在 PATH 上**。安装时 uv 会显示警告，此时用 `uv tool update-shell` 把该目录写进 shell 配置文件（如 `~/.bashrc`）[^c4-1][^c4-2]：

```bash
# 装完发现敲命令找不到 → bin 目录不在 PATH
$ ruff --version
command not found: ruff

# 修复：把工具可执行目录登记进 shell 配置
$ uv tool update-shell

# 之后新开一个终端即可直接使用
```

> [!warning] 坑 9：`update-shell` 之后仍找不到，多半是没开新终端
> `update-shell` 是修改配置文件，不会给**当前已打开**的终端立刻生效。若配置文件里已有登记段落但 PATH 仍没有，`update-shell` 会直接报错——这时重开终端（或 `source` 配置文件）即可。工具可执行目录的准确位置随时用 `uv tool dir --bin` 查询[^c4-2]。

### §4.4 三者分工决策 + 常用场景组合

| 需求 | 用哪个 | 装到哪 | 是否持久 | 会不会影响项目 |
|---|---|---|---|---|
| 一次性临时跑个工具，不碰项目 | `uvx ruff` | 临时隔离环境 | 否（跑完即弃，缓存可复用） | 否 |
| 工具需要能 import 项目自身 / 要钉进项目（pytest、mypy） | `uv run pytest`（pytest 先用 `uv add --dev pytest` 钉进 dev 依赖） | 项目 `.venv` | 依赖随项目声明 | 是（这正是目的） |
| 项目里临时多一个包跑一次性脚本，不想改声明 | `uv run --with requests demo.py` | 项目 `.venv` 之上的临时层 | 否（不写 `pyproject`/`uv.lock`） | 临时可见 |
| 常驻、跨项目的高频命令行工具（ruff、httpie、mkdocs） | `uv tool install ruff` | `uv tool dir` 独立环境 + bin 链到 PATH | 是 | 否（import 不到） |

判断顺序很简单：**临时工具 → `uvx`**；**要复用项目代码、或要把测试工具钉进项目 → `uv run`**；**天天用的全局 CLI → `uv tool install`**[^c4-1]。分界线一句话：`uvx` 把工具和你的项目隔离开，所以凡是「工具必须看见你的项目代码」（pytest 要 import 被测模块）就**不能**用 `uvx`，要用 `uv run`。

本族常用场景组合：

1. **先试后装**：拿不准某个工具好不好用，先用 `uvx` 试用；确认高频后再 `uv tool install` 转正。
2. **临时 lint / 格式化**：不想给项目加 dev 依赖时，`uvx ruff check .`、`uvx ruff format .` 随用随走。
3. **项目内测试链**：`uv add --dev pytest` → `uv run pytest`（pytest 能 import 项目自身；CI 里配合 `uv sync --locked`，见附录 B）。
4. **一次性数据处理脚本**：项目里临时缺包又不值得改声明，`uv run --with pandas demo.py`。

> [!summary] 本章小结
> - `uvx` 是 `uv tool run` 的别名：临时、隔离、不留痕；命令名≠包名用 `--from`，附加依赖用 `--with`。
> - `uv run --with <pkg>` 在项目环境之上临时叠依赖跑脚本，不写 `pyproject`/`uv.lock`，是 PEP 723 脚本头的 CLI 替代做法。
> - `uv tool install` 持久装全局工具：独立环境 + 可执行链到 bin；`uv tool dir --bin` 可查位置。
> - 两个「预期内」的坑：工具模块不会进项目（`import` 失败正常）；命令不在 PATH 时用 `uv tool update-shell` 并重开终端。
> - 分工口诀：临时→`uvx`；要 import 项目/钉进项目（pytest）→`uv run`；常驻 CLI→`uv tool install`。

下一章进入「缓存与索引/镜像」：装包时 uv 从哪拉、装过的包去哪缓存、缓存怎么清——`uv cache` 与索引配置。

