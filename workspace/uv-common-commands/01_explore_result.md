# uv 的常用命令 - 探测结果（P1）

> run_id: uv-common-commands · 主题：uv 的常用命令 · 形式：常用命令速查手册 · 深度：上手 · 检索日期：2026-09-05
> 状态：方向菜单待用户选择

## 探测镜头

| 镜头 | 关注点 | 返回 |
|------|--------|------|
| A 官方命令全景 | project / python / venv / config 子命令族 | 4 条 |
| B 场景速查实践 | 日常 recipe、cheatsheet、国内镜像、常见坑 | 5 条 |
| C 迁移与生态 | pip/venv/conda/poetry→uv、uv tool/uvx、cache、CI | 5 条 |

## 去重后候选来源（按评分排序）

| # | 来源 | URL | Tier | 日期 | 分 | 镜头 |
|---|------|-----|------|------|----|----|
| 1 | uv CLI Reference | docs.astral.sh/uv/reference/cli/ | official | 持续更新 | 5 | A |
| 2 | Working on projects | docs.astral.sh/uv/guides/projects/ | official | 2026-09-04 | 5 | A/B |
| 3 | Using tools（uvx / uv tool） | docs.astral.sh/uv/guides/tools/ | official | 2025-12-02 | 5 | B/C |
| 4 | Caching | docs.astral.sh/uv/concepts/cache/ | official | 2026-08-25 | 5 | C |
| 5 | Using uv in GitHub Actions | docs.astral.sh/uv/guides/integration/github/ | official | 2026-09-04 | 5 | C |
| 6 | Python versions | docs.astral.sh/uv/concepts/python-versions/ | official | 2026-07-25 | 4 | A |
| 7 | Package indexes（镜像/索引） | docs.astral.sh/uv/concepts/indexes/ | official | 2026-08-14 | 4 | B |
| 8 | Using environments（uv venv） | docs.astral.sh/uv/pip/environments/ | official | 2026-03-24 | 4 | A |
| 9 | Real Python: Managing Python Projects With uv | realpython.com/python-uv/ | implementation | 2025 | 4 | B |
| 10 | astral-sh/setup-uv（GitHub Action） | github.com/astral-sh/setup-uv | primary | release v10.0.1 | 4 | C |
| 11 | cpython666: uv 从基础到精通（Conda 用户迁移） | cpython666.github.io/python/libs/uv.html | community | 2026-07 | 3 | C |
| 12 | CSDN 深山技术宅：uv 安装与国内镜像 | blog.csdn.net/jjj_web/article/details/149312129 | community | 2026-08-03 | 2 | B |

备选：Dartmouth uv cheatsheet（dartmouth-libraries.github.io/python-setup/setup/uv_cheatsheet.html，community，2026-01-13）——结构贴近速查表，可视需要补充。

## 方向菜单（请选择笔记组织主线）

- **A. 官方命令骨架速查**：以 uv CLI 子命令族分节（project / python / venv / tool / cache / index / publish…），每节 = 用途一句话 + 命令表 + 最小示例。覆盖最全，检索靠目录。
- **B. 场景速查**：按「我要做什么」组织（新建项目 / 加删依赖 / 跑脚本 / 进 .venv / 装指定 Python / 临时跑工具 / 装全局工具 / 清缓存 / 配国内镜像 / CI）。最贴「日常 80%」。
- **C. 迁移对照速查**：以 pip/venv/conda/poetry 用户视角给「旧命令 → uv 命令」对照表为主干，配 uvx / CI。
- **D. 命令族骨架 + 场景速查混合（推荐）**：主体按官方命令族保证覆盖，每族配「常用场景」子节与示例；附录放 pip/venv 对照与 CI 片段。

## 覆盖缺口（P2 需补 / final note 需标注）

1. 官方无集中「pip/venv/poetry→uv」对照表 → 迁移小节需自建对照表，或引用第三方并标注操作经验（#11）。
2. 国内镜像配置的社区帖写法不一致（uv.toml vs pyproject.toml；UV_INDEX_URL vs UV_DEFAULT_INDEX）→ 以官方 indexes 文档（#7）为准，把差异写入「常见坑」。
3. uv 迭代快（命令/行为随版本变化）→ final note 标注抓取日期 2026-09-05，并提示以 `uv --version` 对应的官方文档为准。

## P2 规模估算

- 核心精读源：官方 5–6 篇（#1-#8 中选）+ 实施 1 篇（#9）+ 社区 1–2 篇（#11/#12，仅操作经验）。
- 产出：约 15–20 条命令族/场景条目，每条含命令、最小示例、注意点，足以支撑「上手」档速查手册正文。
