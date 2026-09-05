## 第 3 章 Python 版本与虚拟环境：uv python / uv venv

上一章把 `pyproject.toml` / `.python-version` / `uv.lock` / `.venv` 四个文件的关系串了起来（→ 见 §2.1），但没有回答一个关键问题：**`.venv` 里的解释器到底从哪来，项目的 Python 版本怎么固定**。本章补上这两块地基——`uv venv`（建环境）与 `uv python`（管解释器）。读完你会明白两件事：日常在项目里几乎不用手动 `activate`；换机器、换同事环境时，Python 版本靠一个 `.python-version` 文件就能复现。

### §3.1 `uv venv` —— 创建虚拟环境

`uv venv` 对应旧工具链的 `python -m venv`，但 uv 本身不依赖 Python，所以「没有装任何 Python 也能建出环境」。默认在当前目录生成 `.venv`，主要用法如下：[^c3-01]

```bash
# 项目根生成 .venv；若 .venv 已存在（且是虚拟环境），uv 会先删后建一个全新的空环境
uv venv

# 指定名字/路径建到别处（不再叫 .venv）
uv venv my-name          # 生成 ./my-name/ 目录，activate 后的提示符也叫 my-name
uv venv /tmp/demo-venv   # 建到绝对路径
```

注意「先删后建」的边界：目标路径**已经是一个虚拟环境**时 uv 会直接覆盖重建；但目标路径**非空却不是虚拟环境**时默认会报错，需要 `--clear` 清空重建，或 `--allow-existing` 不清空直接往里写（后者一般不建议）。[^c3-04]

解释器版本由 `--python` 决定，本机没有对应版本时 **uv 会自动下载**（详见 §3.2 的 managed Python），不用你先去装：[^c3-02]

```bash
uv venv --python 3.11            # 要 3.11：没有就自动下载，再用它建 .venv
uv venv -p 3.11                  # -p 是 --python 的短写
uv venv --python 3.11.9          # 钉到精确补丁版
uv venv --python '>=3.10,<3.13'  # 给一个范围，取首个满足的解释器
```

`--python` 没给时，uv 会按项目里的 `pyproject.toml`（`requires-python`）与 `.python-version` 决定版本；这两者的优先级关系见 §3.3。

**用不用 activate？** 这是 uv 与传统工作流最大的体验差异：uv 会在当前目录及上级目录自动发现 `.venv` 并用它执行命令（`uv run` / `uv sync` / `uv pip install`），所以**不激活也能用**。[^c3-03] 手动激活只在你想要裸命令 `python` / `pip` 也指向这个环境、或 IDE 终端需要时才有意义：

```bash
# macOS / Linux（bash、zsh）
source .venv/bin/activate
deactivate
```

```powershell
# Windows PowerShell
.venv\Scripts\activate
deactivate
```

关于激活脚本具体改了什么 PATH、`.venv` 目录结构长什么样，原理性展开见 [[如何用uv配置Python虚拟环境]]，本篇只给命令面。

> [!tip] 大白话
> 把 `.venv` 想成项目自带的一套工具箱，uv 每次开工自己就知道去 `.venv` 里拿工具，不用你先「登记」（activate）。手动 `activate` 只是让系统里的裸 `python` / `pip` 也指向这套工具箱，方便你在终端直接敲。所以日常用 `uv run` 时，不激活完全没关系。

> [!warning] 坑：`uv venv` 只建空环境
> 在项目里跑 `uv venv` 只会得到一个**没装依赖**的空环境，它不会读 `pyproject.toml` / `uv.lock`。要「建好 + 装齐依赖」应走第 2 章的重建组合 `rm -rf .venv && uv sync`（→ 见 §2.5、§3.4），或干脆用 `uv run` 让 uv 自动同步（→ 见 §2.4）。[^c3-13]

### §3.2 `uv python` —— 安装 / 列出 / 查找解释器

先补一对概念：uv 自己下载并管理的 Python 叫 **managed**（装在 uv 的数据目录里）；机器上其它来源的 Python（系统自带、pyenv、conda 装的）对 uv 一律算 **system**。uv 默认偏好 managed，但已有 system 也好过联网重新下载（详见 §3.3 发现顺序）。[^c3-05]

**安装 `uv python install`**：往 uv 数据目录装 managed Python，并把 `python3.x` 这类命令放进 PATH 目录：[^c3-06]

```bash
uv python install 3.12            # 装 3.12 的最新补丁（managed）
uv python install 3.9 3.11        # 一次装多个
uv python install 3.12 --default  # 额外生成 python3 / python 命令（默认只生成 python3.12）
```

几个要点：[^c3-06]

- 默认只提供带次版本后缀的 `python3.12`；想要 `python3` 和 `python` 这类通用名，必须加 `--default`（若一次请求多个版本会报错）。
- 可执行命令所在目录用 `uv python dir --bin` 查看；若它不在 PATH 里，`uv python update-shell` 可帮你补上。
- uv 绑定的可下载版本列表随每次 uv 发布固定，遇到「想装的新版本找不到」通常是 uv 版本太旧，升级 uv 即可。
- **多数时候不必手动 install**：任何命令请求一个没装的版本，uv 都会自动下载。`install` 的实际价值是：预先装好供离线/慢网使用、把 `python3.x` 命令暴露给其它工具、用 `--default` 接管 `python`。

**列出 `uv python list`**：默认同时显示「已安装」和「本平台可下载」：[^c3-07]

```bash
uv python list                    # 已安装 + 可下载
uv python list --only-installed   # 只看已装
uv python list 3.13               # 按请求过滤
```

**查找 `uv python find`**：输出 uv「当前会优先使用」的解释器绝对路径，等价于帮你回答「我这条命令会落在哪个 Python 上」：[^c3-08]

```bash
uv python find
# macOS/Linux 示例：~/.local/share/uv/python/cpython-3.12.5-macos-aarch64-none/bin/python3.12
# Windows 示例：C:\Users\<你>\AppData\Local\uv\python\cpython-3.12.5-x86_64-pc-windows-msvc\python.exe
# （具体路径以你本机 uv python find 输出为准）

uv python find '>=3.11'   # 找满足范围的一个
uv python find --system   # 跳过虚拟环境，只看系统解释器
```

`uv python` 各子命令接受统一的**版本请求格式**，常用的几种：[^c3-09]

| 写法 | 含义 |
|------|------|
| `3` | 3.x 里最新的一个（uv 已收录的大版本） |
| `3.12` | 3.12 的最新补丁 |
| `3.12.9` | 精确到补丁 |
| `>=3.10,<3.13` | 满足范围即可（install 时也会用） |
| `pypy` | PyPy 实现（CPython 之外的实现） |

> [!tip] 大白话
> 把 managed Python 想成 uv 自带的「货源仓库」：`uv python install` 是进货，`uv venv --python 3.12` 和 `uv python find` 是取货。取货时发现仓库没有、网络又通，uv 会顺手先进货再用——所以多数时候你根本不用记得先 `install`。

### §3.3 `uv python pin` —— 固定版本 + 解释器发现顺序

`uv python pin` 把一个版本写进项目根目录的 `.python-version` 文件（内容就一行），它是第 2 章「四文件关系」里解释器声明的落点（→ 见 §2.1）。[^c3-10]

```bash
uv python pin 3.12            # 当前目录写入 .python-version（内容一行：3.12）
uv python pin                 # 不带参数 = 查看当前 pin（没有 .python-version 会报错）
uv python pin 3.12 --global   # 写入用户级配置目录，作为全局兜底版本
```

写入后的 `.python-version` 就是一行纯文本：

```
3.12
```

行为要点：[^c3-10][^c3-11]

- pin 时 uv 会拿请求与项目的 `requires-python` 校验，冲突会报错。
- 建议写**纯版本号**（如 `3.12`）而不是复杂请求：uv 支持的请求格式比 pyenv 等工具更宽，写成纯版本号才能让其它读 `.python-version` 的工具（pyenv、CI）也认。
- `.python-version` 的查找是「从工作目录逐级向上找」，都没有再落到用户配置目录的全局 pin；查找不越过项目/工作区边界。
- 全局 pin（`--global`）写入目录：Linux/macOS 为 `XDG_CONFIG_HOME/uv`，Windows 为 `%APPDATA%/uv`。

那么「一次命令到底用哪个版本」由两个层次决定：**先定版本请求，再按发现顺序找解释器**。

版本请求来源优先级：

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 高 | 命令行 `--python` / 环境变量 `UV_PYTHON` | 单次覆盖，最明确 |
| 中 | `.python-version`（`pin` 写） | 项目根 → 上级目录 → 用户级全局 pin |
| 低 | `pyproject.toml` 的 `requires-python` | 只声明下限，取第一个兼容版本 |

解释器发现顺序（`uv python find` 即按此返回第一个命中者）：[^c3-12]

| 顺序 | 查找对象 | 说明 |
|------|----------|------|
| 1 | 虚拟环境：激活的 `VIRTUAL_ENV`，或当前/上级目录的 `.venv` | 允许用 venv 的命令先检查它是否满足请求 |
| 2 | uv managed Python（`uv python dir` 目录） | 默认偏好 managed（`python-preference=managed`） |
| 3 | PATH 上的系统 Python：`python` / `python3` / `python3.x` | pyenv、conda 装的也算 system |
| 4 | Windows 注册表 / Microsoft Store（`py --list-paths`） | 仅 Windows，按 PEP 514 注册 |

两点补充理解这个表：system 搜索取「第一个兼容」而不是最新；managed 与 system 都没有满足的版本时，uv 才会联网下载。想强制只用 managed 加 `--managed-python`，只想用系统解释器加 `--no-managed-python` / `--system`（→ 也见 `uv python find --system`）。[^c3-12]

> [!tip] 大白话
> 把 `.python-version` 想成贴在项目门口的一张便签，上面写着「本项目用 3.12」。便签跟着 Git 走，团队其他人或 CI 拉下代码，uv 一进门看到便签就照 3.12 执行——这就避免了「在我机器上能跑、在你机器上就炸」的版本漂移。

### §3.4 常用场景组合（本族）

**① 给项目装一个指定 Python 并固定下来**（三步，前两步可互换顺序）：

```bash
uv python install 3.12   # 可选：预装 managed 3.12（不装也行，下一步会自动下载）
uv venv --python 3.12    # 用 3.12 建 .venv
uv python pin 3.12       # 写 .python-version，把版本锁给整个团队
```

**② 项目里彻底重建环境**（比 `uv venv` 更常用）：因为 `uv venv` 只建空环境、不装依赖，项目里的「推倒重来」应让 uv 照 `uv.lock` 一次装齐：[^c3-13]

```bash
rm -rf .venv && uv sync   # 删掉旧环境，按锁文件重建并装齐（→ 见 §2.5）
```

**③ 什么时候才手动 `uv venv`？** 在正式项目里其实很少手敲——`uv run` / `uv sync` 会自动创建 `.venv`（→ 见 §2.4）。`uv venv` 的价值在：非项目目录想隔离、想要自定义名字/位置的裸环境、或建好一个空环境后给 `uv pip` 兼容层用（→ 见 §6.3）。

> [!summary] 本章小结
> - `uv venv` 建空环境：默认 `.venv`；目标路径已是虚拟环境会先删后建，非空非 venv 才需 `--clear`。
> - uv 自动发现 `.venv`，无需 activate；手动激活写法：bash `source .venv/bin/activate`、PowerShell `.venv\Scripts\activate`，退出用 `deactivate`。
> - `uv python install` 装 managed Python，默认只生成 `python3.x`，`--default` 才给 `python3` / `python`；`list` / `find` 分别负责列出与定位解释器。
> - `uv python pin` 写 `.python-version`（`--global` 落用户级）；版本请求优先级：`--python` > `.python-version` > `requires-python`。
> - 解释器发现顺序：`VIRTUAL_ENV`/`.venv` → managed 目录 → PATH → Windows 注册表；默认偏好 managed、其次 system、最后才联网下载。
> - 项目里「重建且装齐」用 `rm -rf .venv && uv sync`，而不是 `uv venv`。

**下一章预告**：环境与解释器都搞定了，接下来看怎么「用完即走」——`uvx` 临时跑工具、`uv run --with` 给脚本临时加依赖、`uv tool` 常驻装全局工具，三者怎么分工。

