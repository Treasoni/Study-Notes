## 第 6 章 构建发布与 pip 兼容层：uv build / uv publish / uv pip

前几章解决的是「把依赖装进 `.venv`、把脚本跑起来」——那是**消费包**的视角。当你的项目是一个库、或想作为包分发给别人 `uv add` / `pip install` 时，还需要站到**生产包**的视角：把源码打成可发布的发行包，上传到索引，并处理发布前后的一连串校验。本章三条命令族正好覆盖这条链路：`uv build`（本地打包）、`uv publish`（上传索引）、`uv pip`（给仍在用 `requirements.txt` 工作流的场景一个 pip 风格入口）。前两者做的是「把包交出去」，`uv pip` 则是 uv 里与项目工作流平行的一套兼容接口。

> 版本说明：本章命令与输出对应 2026-09-05 抓取的官方文档；uv 迭代快，细节以 `uv --version` 对应的文档为准（阅读约定见第 1 章）。

### §6.1 `uv build` —— 构建发行包

一句话定位：`uv build` 按 PEP 517 构建规范，把项目源码在本地打成**发行包**（distribution）。发行包分两种，先看构建后多出来的 `dist/` 目录，就能直观区分[^c6-01][^c6-02]：

```text
demo-pkg/                          # 构建前：项目源码 + 元数据
├── pyproject.toml
└── src/demo_pkg/__init__.py

demo-pkg/                          # uv build 之后：多了 dist/
├── pyproject.toml
├── dist/
│   ├── demo_pkg-0.1.0.tar.gz            # sdist：源码包
│   └── demo_pkg-0.1.0-py3-none-any.whl  # wheel：预构建分发
└── src/demo_pkg/__init__.py
```

- **sdist**（source distribution，`.tar.gz`）：装的是**源码**。用户拿到后要现场编译，所以任何平台通用，但装起来慢。
- **wheel**（`.whl`）：装的是**已构建产物**，即装即用；但产物可能绑定平台/解释器（名字里的 `py3-none-any` 表示纯 Python、平台无关）。跨平台分发时通常要为各平台各构建一个 wheel。

默认执行一次 `uv build`，会**同时**产出 sdist 和 wheel：先由源码目录构建 sdist，再基于这个 sdist 构建 wheel[^c6-01]：

```bash
# 在项目根目录执行；SRC 省略时默认为当前目录
$ uv build
Building source distribution...
Successfully built dist/demo_pkg-0.1.0.tar.gz
Successfully built dist/demo_pkg-0.1.0-py3-none-any.whl
```

想只构建其中一种，用 `--sdist` / `--wheel` 控制；两者可组合为 `uv build --sdist --wheel`（都从源码构建，默认就是这一种）[^c6-01]：

```bash
# 只出源码包（例如只想让别人替你做平台相关编译）
$ uv build --sdist

# 只出 wheel（例如只在自己要用的平台上分发）
$ uv build --wheel
```

构建的前提是 pyproject 里有 `[build-system]` 和可分发元数据。`uv init` 近版本默认会把项目设为可打包（自动带 `[build-system]`）；专为「要分发成库」设计的是 `uv init --lib`（生成 `src/` 布局 + 构建骨架）；而当初用 `--no-package` 建的纯应用没有 `[build-system]`，直接 `uv build` 会报缺构建后端[^c6-03]。拿不准时跑一次 `uv build` 即可，报错信息会指出缺什么。

> [!tip] 大白话
> 打包 = 给源码「装箱发货」。sdist 是「原料 + 菜谱」——把生的寄过去，对方拿到在自己厨房（目标机器）开火做；wheel 是「预制菜」——做好密封，对方微波炉一热（即装即用）就能吃。`uv build` 默认两样都给你打包好：既照顾想自己下厨的（sdist），也照顾图省事的（wheel）。

### §6.2 `uv publish` —— 发布到索引（含 TestPyPI 坑）

`uv build` 打好的包还躺在本地 `dist/`，`uv publish` 负责把它们**上传到包索引**（默认 PyPI），上传后别人就能 `uv add` / `pip install` 到你的包。它替代了传统 `pip` 时代的 `twine` 角色，一条命令完成上传[^c6-04]。

```bash
# 默认上传 dist/ 下所有 sdist 与 wheel 到 PyPI
$ uv publish
```

> [!note] 上传地址 ≠ 下载地址
> 包索引有两个不同 URL：下载走 simple API（如 `https://pypi.org/simple/`），上传走独立的 legacy 端点（如 `https://upload.pypi.org/legacy/`）。`uv publish` 的 `--publish-url` 指上传端点，默认就是 PyPI 的 legacy URL；`--check-url` 用于在上传前查重、跳过已存在的同名文件[^c6-04]。

裸跑 `uv publish` 前需要凭据。本地最常用 **API token**，用 `--token` 传入（等价于把用户名写成 `__token__`、密码写成 token）；token 也可通过环境变量 `UV_PUBLISH_TOKEN` 提供，避免写进 shell 历史或 CI 日志[^c6-06]：

```bash
# token 走命令行（本地一次试传方便）
$ uv publish --token pypi-xxxxxxxx

# token 走环境变量（CI 里更安全，secret 注入）
$ export UV_PUBLISH_TOKEN=pypi-xxxxxxxx
$ uv publish
```

正式发布前先发到 **TestPyPI**（试运行的演练场）验收是标准做法。先在 `pyproject.toml` 声明一个名为 `testpypi` 的上传目标[^c6-08]：

```toml
[[tool.uv.index]]
name = "testpypi"
url = "https://test.pypi.org/simple/"          # 下载用（查重）
publish-url = "https://test.pypi.org/legacy/"  # 上传用
explicit = true                                # 不显式点名就不参与解析
```

`uv publish` 的 `--index <名字>` 会去配置里找这个名字的索引，用它的 `publish-url` 上传[^c6-05]：

```bash
# --index 指向 §6.2 配置里的 testpypi；需先在 TestPyPI 注册账号并生成 API token
$ uv publish --index testpypi --token pypi-xxxxxxxx
```

两点注意：TestPyPI 上**包名必须唯一**，已存在的名字上传会失败，验收用的包名常需起得特别些；`explicit = true` 让 `testpypi` 只在被点名时参与解析，默认解析仍走 PyPI——这正好避开下面的坑[^c6-08]。

> [!warning] 坑 10：从 TestPyPI 安装自己的包，常因「那里的依赖太旧」解析失败
> TestPyPI 不是 PyPI 的镜像，而是独立的演练场，上面很多第三方包没有或停留在远古版本。假设你的包声明 `requests>=2.32.3`，但 TestPyPI 上最新的 `requests` 只有 `2.5.4.1`——当你用 TestPyPI 当唯一索引去 `uv pip install` 自己的包时，解析器找不到满足要求的 `requests`，直接报 `No solution found when resolving dependencies`[^c6-09]。
> 绕法：先把新版本的依赖从**默认 PyPI** 装好，让它在环境里已满足，再仅用 TestPyPI 装你自己的包：
> ```bash
> # ① 先从 PyPI 装好满足版本要求的依赖
> $ uv pip install requests
> # ② 再用 TestPyPI 当默认索引装自己的包（requests 已满足，无需再去 TestPyPI 找）
> $ uv pip install --default-index https://test.pypi.org/simple/ demo-pkg
> ```
> 根因是 uv 默认的 `first-index` 防依赖混淆策略：一个包只认第一个命中它的索引，TestPyPI 先命中了旧的 `requests` 就不会再回 PyPI 找[^c6-09]。

> [!tip] 大白话
> `uv publish` = 把打好的包**上架到商店**。PyPI 是正式营业的大超市，TestPyPI 是「试营业的演练场」——先摆上去看看包装有没有问题，但它货架上别人的货（第三方依赖）不全、也旧。token 是商店给你的**门禁卡**（用户名固定刷 `__token__`，卡号就是 token）；在 CI 里还有「可信发布」这种不掏卡、由 GitHub/GitLab 替你刷脸的进门方式。

CI 里发布一般不开明文 token，而是用**可信发布（trusted publishing）**：由 GitHub Actions / GitLab CI/CD 环境自动换取短期上传凭据，`uv publish --trusted-publishing` 默认 `automatic`，检测到受支持环境就自动尝试[^c6-07]。官方示例把 `build` 与 `publish` 拆成两个 job，让持有 `id-token: write` 的发布 job 不与构建 job 共享权限，缩小供应链攻击面；PyPI 项目设置里需按 GitHub 配置添加对应的 Trusted Publisher[^c6-07]。CI 片段见附录 B。

### §6.3 `uv pip` —— pip 兼容层

第 2–3 章的项目工作流（`uv add` + `uv sync` + `uv.lock`）是 uv 的推荐用法，但并非唯一。uv 还内置一套 **pip 兼容接口**——`uv pip install` / `uninstall` / `list` / `freeze` / `compile` / `sync`……让老 pip 用户照旧习惯、用上 uv 的解析速度；它也面向「没有项目、只有环境」的场景：临时 `.venv`、只靠 `requirements.txt` 的旧式布局、以及 CI 裸机上的系统 Python[^c6-10]。

和 pip 最大的区别是**目标环境意识**：`uv pip` 面向「某个已存在的 Python 环境」，**不面向项目**——它不会读 `pyproject.toml` 帮你维护依赖声明，也不会写 `uv.lock`。默认它把包装进「当前目录或任一父目录里找到的虚拟环境」（`.venv` / `VIRTUAL_ENV`）；**若找不到任何虚拟环境，会报错**——它不像 `uv run` 那样帮你自动建环境。没有环境时先 `uv venv`（见 §3.1），或在 CI/系统环境用 `--system` 显式指定[^c6-10]：

```bash
# 场景 A：项目/目录下已有 .venv（或已 activate），默认装进它，无需任何开关
$ uv pip install -r requirements.txt

# 场景 B：没有 venv，就是要装进系统 Python（CI 裸机常用）
$ uv pip install --system -r requirements.txt

# 等价写法：设一次环境变量，之后所有 uv pip 调用都按系统 Python 处理
$ export UV_SYSTEM_PYTHON=1
```

`--system` 让 uv 改用系统 `PATH` 上找到的第一个 Python；官方标注它**面向 CI**，会改动系统 Python 安装，需谨慎[^c6-10]。GitHub Actions 里用 `uv pip` 时，官方就是建议所有调用都加 `--system` 或设 `UV_SYSTEM_PYTHON=1`[^c6-10]。

> [!tip] 大白话
> `uv pip` 是给 pip 老司机的**同款驾驶位、换了 uv 引擎**：方向盘和踏板（命令与参数）沿用 pip 习惯，踩下去提速的是 uv 的解析和缓存。但要记住它只负责「把某个包装进某个环境」，**不负责记购物清单**（项目依赖声明/锁文件）。记清单是 `uv add` 的活儿，两个岗位别串。

`uv pip` 还替 pip-tools 用户提供了对应的两个命令（迁移对照见附录 A）：`compile` 把松散的输入钉成精确清单，`sync` 让环境精确等于清单[^c6-11]：

```bash
# 等价 pip-compile：把直接依赖 requirements.in 编译成钉死的 requirements.txt（含全部间接依赖）
$ uv pip compile requirements.in -o requirements.txt

# 等价 pip-sync：让环境与 requirements.txt 完全一致（清单外多装的会被删掉）
$ uv pip sync requirements.txt

# 查看/导出环境（对应 pip list / pip freeze）
$ uv pip list
$ uv pip freeze
```

> [!note] 与项目工作流怎么接
> 在 uv 项目里想要一份 `requirements.txt`，正规走 `uv export -o requirements.txt`（见 §2.7，默认先重新解析锁文件）；拿这份产物去喂 `uv pip sync` 就是「项目锁定结果 → 别的环境」的搬运路径。`uv pip compile` 更多服务「没有项目、纯 requirements.in 工作流」的老式布局。

### §6.4 常用场景组合（本族）+ 一条告诫

本族一条主线是**发布链**，从打包到验收再到正式上架：

```bash
# ① 本地打包 → dist/（见 §6.1）
$ uv build

# ② 先发 TestPyPI 验收（见 §6.2；包名需唯一、注意依赖旧坑）
$ uv publish --index testpypi --token pypi-xxxxxxxx

# ③ 确认无误后正式发 PyPI（CI 里可用可信发布免 token，见附录 B）
$ uv publish
```

> [!warning] 坑 1：在 uv 项目里加依赖，别用 `uv pip install`，走 `uv add`
> 这是最常见的误用。`uv pip install requests` 会把包**只装进当前环境**，但不写 `pyproject.toml`、不更新 `uv.lock`；下次 `uv sync` 按锁文件把环境同步回精确状态时，这个「没登记」的包会被当成多余包**删掉**（`uv sync` 默认 exact 会清多余包，见 §2.5）。加依赖请用 `uv add requests`（写声明 + 解析锁 + 安装一条龙，见 §2.3）。`uv pip` 接口适合非项目环境、临时验收、CI 里按 `requirements.txt` 装依赖，唯独不适合给 uv 项目加依赖[^c6-12]。

| 对比维度 | `uv add`（项目工作流） | `uv pip install`（兼容层） |
|---|---|---|
| 作用对象 | 项目（`pyproject.toml` + `uv.lock` + `.venv`） | 某个已存在的 Python 环境 |
| 写 `pyproject.toml` | 是 | 否 |
| 更新 `uv.lock` | 是 | 否 |
| 之后 `uv sync` 的结局 | 保留 | 被当多余包删除（默认 exact） |
| 适用场景 | 在 uv 项目里加依赖 | 非项目环境 / 临时验收 / CI 装 `requirements.txt` |

> [!summary] 本章小结
> - `uv build` 一次默认同建 sdist + wheel 到 `dist/`；`--sdist` / `--wheel` 可只出其一；前提是 pyproject 里有 `[build-system]`。
> - `uv publish` 上传 `dist/` 到索引（默认 PyPI）；`--token` 或 `UV_PUBLISH_TOKEN` 提供凭据，CI 里用可信发布免明文 token。
> - 先用 `pyproject.toml` 配 `testpypi` 索引（`name`/`url`/`publish-url`/`explicit`），再 `uv publish --index testpypi --token ...` 试发；TestPyPI 上依赖旧会导致安装你的包时解析失败，先装好新依赖即可绕过。
> - `uv pip` 是面向「已存在环境」的兼容层：默认装进找到的 `.venv`，系统环境要 `--system` 或 `UV_SYSTEM_PYTHON=1`；`compile` / `sync` 对应 pip-tools 的 `pip-compile` / `pip-sync`。
> - 一条红线：uv 项目里加依赖走 `uv add`，别用 `uv pip install`（不写声明、不更新锁，还会被下次 `uv sync` 清掉）。

下一章进入场景速查：14 条「我要…」把第 2–6 章所有命令族串成一个前门索引——先按场景查到这里，再跳回对应小节看参数细节。

