# uv 常用命令速查手册

> 面向已有 uv 基础的读者（已了解 uv 与 pip/venv 的关系）。本文是命令速查/参考手册：正文第 1–6 章按命令族展开，第 7 章是 14 条「我要…」跨族检索入口，附录 A/B 提供迁移对照与 CI 片段。素材抓取于 2026-09-05，命令细节以你本机 `uv --version` 对应的官方文档为准。阅读约定见 §1.1。

## 目录

1. [[#第 1 章 快速上手：5 条命令跑通日常]]
2. [[#第 2 章 项目命令族：init / add / remove / run / sync / lock / tree / export]]
3. [[#第 3 章 Python 版本与虚拟环境：uv python / uv venv]]
4. [[#第 4 章 临时与全局工具：uvx / uv tool / uv run --with]]
5. [[#第 5 章 缓存与索引/镜像：uv cache / 索引配置]]
6. [[#第 6 章 构建发布与 pip 兼容层：uv build / uv publish / uv pip]]
7. [[#第 7 章 场景速查：14 条「我要…」（跨族检索入口）]]
8. [[#附录 A：pip / venv / conda / poetry → uv 迁移对照]]
9. [[#附录 B GitHub Actions CI 片段]]

---

## 第 1 章 快速上手：5 条命令跑通日常

uv 的命令面比 pip/venv 大一圈，第一眼容易劝退。但日常 80% 的动作其实只被 5 条命令覆盖。本章先用一张总览表 + 一段 60 秒端到端流程，帮你建立「原来就这么简单」的整体心智；具体参数与坑留给第 2–3 章展开。

### §1.1 阅读约定

**本手册怎么读**：这是一份速查手册（参考/工具型），不是顺序教程，每章自洽、可独立查阅。正文第 2–6 章按命令族组织——每条命令的参数、选项与坑只在对应章节详细写一遍；第 7 章是 14 条「我要…」跨族检索入口，只给「场景 → 命令 → 锚点」，参数一律跳回命令族章；附录 A/B 给迁移对照与 CI 片段。检索优先路径：先到第 7 章按场景定位，再沿锚点进正文看细节。

**版本提示**：uv 迭代很快（本手册素材抓取于 2026-09-05），命令细节以你本机版本为准。先跑 `uv --version` 确认版本，再对照官方 CLI 参考（docs.astral.sh/uv/reference/cli/）。[^c1-01]

**§ 锚点约定**：正文用 `§x.y` 指代「第 x 章 y 节」（如 `§2.4` = 第 2 章第 4 节）。素材出处用「02 素材 §x.y + research-cache 编号」两级标注，方便回溯原始资料。[^c1-02]

**与既有笔记的关系**：虚拟环境「怎么建、要不要 activate、Python 解释器怎么选」的原理性展开见 [[如何用uv配置Python虚拟环境]]，本篇只给 `uv venv` 等命令面，不重复讲原理。

### §1.2 5 条核心命令总览

下表 5 条覆盖日常 80%：建项目、加依赖、跑脚本（免激活）、手动同步环境、建虚拟环境。后面所有命令族章都是在这 5 条上的扩展。[^c1-02]

| 命令 | 一句话用途 | 详见 |
|------|-----------|------|
| `uv init` | 新建项目骨架：生成 `pyproject.toml`、`.python-version` 等 | §2.2 |
| `uv add <包>` | 加依赖：写 `pyproject.toml` → 更新 `uv.lock` → 装进 `.venv` 一步到位 | §2.3 |
| `uv run <命令/脚本>` | 免 activate 在项目环境执行，跑前自动校验并同步 | §2.4 |
| `uv sync` | 手动把 `.venv` 与 `uv.lock` 同步到一致（默认精确同步） | §2.5 |
| `uv venv` | 创建虚拟环境（默认 `.venv`），不激活也能被 uv 自动发现 | §3.1 |

> [!tip] 大白话
> 把 `uv run` 想成公司前台：你说「跑 main.py」，它先自动核对门禁（依赖齐不齐），缺了当场补，再放你进去——所以你永远不用自己 `activate`。日常循环本质只有两步：`uv add` 声明要什么 + `uv run` 去执行；`uv venv` / `uv sync` 是你要手动精细控制时才出手的工具。

### §1.3 60 秒端到端最小流程

把下面一段从头跑到尾，就能直观感受「建项目 → 加依赖 → 写脚本 → 运行」的最小闭环（bash/macOS/Linux 粘贴版）：

```bash
# ① 新建项目 demo 并进入（生成 pyproject.toml、.python-version、README、src/demo/）
uv init demo && cd demo

# ② 加依赖 requests：写 pyproject → 解析 uv.lock → 装进 .venv，一步到位
uv add requests

# ③ 在项目根新建 4 行脚本 main.py
cat > main.py <<'EOF'
import requests

resp = requests.get("https://api.github.com")
print(resp.status_code)  # 期望输出：200
EOF

# ④ 免 activate 直接跑：uv 先自动同步环境，再在 .venv 里执行
uv run main.py
```

拆开看每步在干什么：

- **第①步后**，目录里还**没有** `.venv` 和 `uv.lock`——它们「懒创建」，直到第一次跑 sync 类命令（`uv run` / `uv sync` / `uv lock`）才出现。[^c1-03]
- **第②步** `uv add` 同时做三件事：写进 `pyproject.toml`、解析出精确的 `uv.lock`、安装进 `.venv`。这正是它和 `pip install` 最大的区别——不会只装包而不同步声明。[^c1-04]
- **第④步**的等价写法是 `uv run python main.py`；对以 `.py` 结尾的参数，uv 自动按脚本交给 Python 解释器执行。Windows 用户若不想用 heredoc，可先 `uv sync` 建好环境，再用编辑器新建 `main.py`，最后执行 `uv run main.py`。[^c1-05]

> [!tip] 大白话
> 把 `.venv` 想成随手能重建的工地。uv 手上有 `pyproject.toml` + `uv.lock` 两张「图纸」，`uv run` / `uv sync` 随时能照图重新搭环境，所以 `.venv` 删了不心疼；真正要提交进 Git 的是 `uv.lock`（详见 §2.1、§3.1）。

> [!summary] 本章小结
> - uv 命令面虽大，日常 80% 由 5 条命令驱动：`init` / `add` / `run` / `sync` / `venv`。
> - `uv run` 是统一入口：免 activate、跑前自动同步；以 `.py` 结尾的参数按脚本执行。
> - `uv add` 一步做三件事：写 `pyproject.toml`、解析 `uv.lock`、安装进 `.venv`。
> - `.venv` 与 `uv.lock` 首次 sync 类命令才懒创建；`.venv` 可随时删除，uv 会照锁文件重建。
> - 本手册定位速查：命令族详述（第 2–6 章）→ 场景检索（第 7 章）→ 附录 A/B。

**下一章预告**：进入第一块主体——项目命令族。先理清 `pyproject.toml` / `.python-version` / `uv.lock` / `.venv` 四个文件谁管什么，再逐条拆 `init` / `add` / `run` / `sync` 的常用参数。

---

