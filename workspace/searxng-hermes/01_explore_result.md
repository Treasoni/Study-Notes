# 阶段 1 探测结果 — SearXNG 自托管与 Hermes 接入

> 本文件是**中间产物（handoff artifact），不是权威终点**。
> 其中引文与数值请回 `sources/` 按行号核对；P2 起所有 `snippet-only` 条目必须先抓正文才能当证据用。
>
> 探测日期：2026-10-07 ｜ 运行：`searxng-hermes` ｜ 透镜数：3（L1 是什么 / L2 怎么搭 / L3 怎么接 Hermes）

---

## 一、候选清单（按透镜，已按 canonical URL 去重）

### L1 — SearXNG 是什么（概念与隐私模型）

| ID | 标题 | URL | tier | evidence_form | 日期 | 分 |
| --- | --- | --- | --- | --- | --- | --- |
| L1-1 | SearXNG Docs — Overview（`docs/index.rst`） | https://raw.githubusercontent.com/searxng/searxng/master/docs/index.rst | official | fetched | master 滚动，取回 2026-10-07 | 5 |
| L1-2 | Why use a private instance?（`docs/own-instance.rst`） | https://raw.githubusercontent.com/searxng/searxng/master/docs/own-instance.rst | official | fetched | 同上 | 5 |
| L1-3 | Configured Engines | https://docs.searxng.org/user/configured_engines.html | official | fetched | n/a | 4 |
| L1-4 | About SearXNG | https://docs.searxng.org/user/about.html | official | fetched | n/a | 4 |
| L1-5 | 上游仓库 `searxng/searxng`（README.rst + metadata） | https://github.com/searxng/searxng | primary | fetched | pushed 2026-10-07 | 4 |

职责提要：L1-1 给定义/不追踪不画像/Tor/2021 年中 fork 自 searx；L1-2 给隐私模型（请求脱敏、**IP 为实例 IP**、可走 Tor/代理、公共实例的信任代价）；L1-3 给引擎数；L1-4 给与 Google 的差别与不建画像；L1-5 给许可与治理。
`L1-5` upkeep：`pushed_at=2026-10-07T09:21:06Z, archived=false`。

### L2 — 怎么搭（SearXNG 自托管部署）

| ID | 标题 | URL | tier | evidence_form | 日期 | 分 |
| --- | --- | --- | --- | --- | --- | --- |
| L2-1 | Installation container (Docker) — 官方部署指南 | https://docs.searxng.org/admin/installation-docker.html | official | fetched | n/a | 5 |
| L2-2 | `container/docker-compose.yml` | https://raw.githubusercontent.com/searxng/searxng/master/container/docker-compose.yml | primary | fetched | 仓库 pushed 2026-10-07 | 5 |
| L2-3 | `settings.yml` — 位置与 `use_default_settings` | https://docs.searxng.org/admin/settings/settings.html | official | fetched | n/a | 5 |
| L2-4 | `settings_search` — `search.formats` | https://docs.searxng.org/admin/settings/settings_search.html | official | fetched | n/a | 5 |
| L2-5 | Installation Script（`utils/searxng.sh`，非容器） | https://docs.searxng.org/admin/installation-scripts.html | official | fetched | n/a | 4 |

**另抓取但未单列**（P2 应作为证据件纳入）：
- `docs/dev/search_api.html` —— 确证**未开启 json 时返回 403**、端点为 `GET /search?q=..&format=json`（**本地未落盘，P2 需重抓并落 sources/**）
- `container/settings.template.yml` —— `use_default_settings: true`，**无 `search.formats`**（即 JSON 确实默认关）
- `container/.env.example` —— 仅 `SEARXNG_VERSION` / `SEARXNG_HOST` / `SEARXNG_PORT`，且**全部被注释**
- `L2-2` upkeep：`pushed_at=2026-10-07T09:21:06Z, archived=false`

### L3 — 怎么接 Hermes + 验证排错

| ID | 标题 | URL | tier | evidence_form | 日期 | 分 |
| --- | --- | --- | --- | --- | --- | --- |
| L3-1 | Web Search & Extract（user-guide feature doc） | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/features/web-search.md | official | fetched | updated 2026-10-06 | 5 |
| L3-2 | Web Search & Extract（live docs 镜像） | https://hermes-agent.nousresearch.com/docs/user-guide/features/web-search | official | fetched | n/a | 5 |
| L3-3 | CLI Commands Reference — `hermes tools` | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/reference/cli-commands.md | official | fetched | updated 2026-10-07 | 4 |
| L3-4 | `optional-skills/research/searxng-search/SKILL.md` | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/optional-skills/research/searxng-search/SKILL.md | primary | fetched | v1.0.1 | 4 |
| L3-5 | `plugins/web/searxng/provider.py` | https://raw.githubusercontent.com/NousResearch/hermes-agent/main/plugins/web/searxng/provider.py | primary | fetched | 仓库 pushed 2026-10-07 | 4 |

职责提要：L3-1/L3-2 给接入全流程 + `SEARXNG_URL` + `search_backend`/`extract_backend` + 403 排错；L3-3 给 `hermes tools` 交互配置路径；L3-4 给 `curl` 直连 JSON 自检与 fallback 检测；L3-5 给**源码级证据**（`KEY_ENV=SEARXNG_URL`，仅有 search、无 extract）。
`L3-4` / `L3-5` upkeep：`pushed_at=2026-10-07T09:43:54Z, archived=false`。

### 去重记录

- **L3-1 与 L3-2 同源**（同一 `web-search.md` 的 raw 与渲染版）：正文引用统一挂 **L3-1**，L3-2 仅作"渲染一致"校验，不重复计为独立来源。
- **L1-2 与 L1-4 隐私表述重叠**：隐私模型以 **L1-2** 为主，L1-4 只保留"与 Google 差别 / 不共享第三方"这一独占要点。
- L1-5 的 AGPL-3.0 与定位句在 README.rst 与元数据中重复，只记一次。

### 全部为 `fetched`，无 `snippet-only`

本轮 15 条候选（去重后 13 个独立来源）**全部为 `fetched`**。P2 无需为"仅凭搜索摘要"的条目补抓；但仍需**重新落盘**：L1-1、L1-2、L2-2、L3-1、L3-3、L3-4、L3-5 以及 L2 的 `search_api.html` 必须存进 `workspace/searxng-hermes/sources/` 后按行号核对。

---

## 二、★ 待核实的矛盾与缺口（P2 必办）

| # | 事项 | 冲突/缺口 | P2 动作 |
| --- | --- | --- | --- |
| C1 | **引擎数** | Hermes 文档（L3-1）称 *"aggregates results from 70+ search engines"*；SearXNG 文档（L1-3）称 **261 个已配置、81 个默认启用**。两者口径不同 | 回 L3-1 与 L1-3 原文逐字核对，判定是"文档陈旧/口径不同",写作时分别标注归属，**不得混用成一个数** |
| C2 | **`SEARXNG_BASE_URL`** | Hermes 配方（L3-1）的 compose 写了 `SEARXNG_BASE_URL=http://localhost:8888/`；但 SearXNG 官方 `container/docker-compose.yml`（L2-2）、`container/.env.example`（L2-3 同批）**均未出现该键** | 核实该变量在 SearXNG 中的真实作用（是否必需 / 是否只是 `SERVER_NAME` 之类），**宁可写"官方编排未使用、Hermes 配方另加"也不得臆断** |
| C3 | **端口** | SearXNG 官方 compose（L2-2）**默认 8080**；`8888` 来自手册示例 `-p 8888:8080` 与 Hermes 配方 | 写作时明确"容器内 8080，宿主端口可任意映射"，避免读者以为 SearXNG 默认就是 8888 |
| G1 | `searx.space` 未采 | 公共实例列表（约 73 实例、含 Tor 隐藏服务）本批未列 | 若走"公共实例"分支才补；当前方向以自托管为主，列为可选 |
| G2 | DuckDuckGo 直比缺失 | L1-4 无与 DDG 的正面比较 | 写作时不虚构对比，只保留有来源的"与 Google / 元搜索聚合"表述 |
| G3 | docs 无发布日期 | SearXNG 官方文档页普遍无 `published/updated` | 引用时用"取回日期 2026-10-07"代替，不编造发布日期 |

---

## 三、方向菜单（请选一个）

> 说明：意图文件已定「概念 + 实战混合」。下面是在此前提下对**重心与范围**的选择。

**A. 全量主线（推荐）**
是什么 → 怎么搭 → 怎么接 Hermes → 验证排错，一篇完整上手笔记（约 5–6 章）。概念只做必要铺垫，重心在"跑起来并接上"。

**B. 偏实操精简**
弱化概念章（压成半章"一句话看懂 + 为什么自托管"），重点给**可照抄**的 Docker 部署 + JSON 开启 + Hermes 接入 + 排错清单。

**C. 概念先行**
先讲透元搜索原理与隐私模型（聚合机制、请求脱敏、实例 IP），部署侧只给最短可行路径与一句"细节见官方 Docker 文档"。

**D. A + 进阶加装**
在 A 基础上加一章进阶：引擎裁剪（261→按需）、改端口/反代、限流与反爬、公共实例 vs 自建对比表、`latest` 滚动更新与升级维护。

**推荐：A**（与"上手深度、够用即止、最省事接入"的意图最贴合）；若你想让笔记更薄、更快能用，选 **B**。

---

## 四、P2 预计范围

- **来源组**：约 13 个独立来源，分 3 组深读（L1 概念组 / L2 部署组 / L3 接入排错组），每组 1 个 delegate（≤3 delegates/phase）。
- **必办**：落盘 `sources/` → 逐字核对引文并记行号 → 重数 C1 的引擎数 → 定 C2 的 `SEARXNG_BASE_URL` → 重抓 `search_api.html`。
- **不做**：searx.space 公共实例清单（除非你选公共实例分支）、DuckDuckGo 正面比较（无来源）。
