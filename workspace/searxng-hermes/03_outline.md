# 学习笔记大纲：《SearXNG 自托管与 Hermes 接入》

> 运行：`searxng-hermes` ｜ 笔记类型：**概念 + 实战混合**（`concept` + `practice`）｜ 学习深度：**上手（够用即止）**
> 方向：**A. 全量主线**（是什么 → 怎么搭 → 怎么接 Hermes → 验证排错 → 进阶可选）
> 发布目标：`AI学习/Hermes Agent/SearXNG 自托管指南/`（完成后在 `AI学习/Hermes Agent/Hermes Agent MOC.md` 追加索引项）
> 篇幅合计：**约 6700–9900 字** ｜ 章节数：**6**
>
> 本章纲所有素材引用均带 **来源 ID + `sources/` 文件:行** 锚点，已逐条回源核对（核对中发现深研文件若干行号漂移，见文末「需用户确认的问题」。1 处来源 `L1-4` 在深研 claim 表中未映射任何主张，默认不使用）。
>
> 写作契约（`note-style.md` + `note-system.md`）在各章中展开为：开篇 3 句内「一句话看懂」；比喻先于术语；术语首次出现即解释；概念与动手分离（动手小节标「**新手可跳过**」）；抽象概念给实体落点（文件内容 / 目录树 / 命令输出 / 对比表）；每章末附「引文对照（原文 / 中译 / 出处）」表（出处查不到写 `—`）。

---

## 章节总览

| 章号 | 标题 | 篇幅（字数区间） | 主要来源 ID |
| --- | --- | --- | --- |
| 第 1 章 | SearXNG 是什么：一句话看懂 + 隐私模型 | 800–1200（短） | L1-1, L1-2, L1-3, L1-5 |
| 第 2 章 | 动手：用 Docker 把 SearXNG 跑起来 | 1800–2600（长） | L3-1, L2-1, L2-2, L2-8, L2-9, L2-10 |
| 第 3 章 | 开启 JSON API —— Hermes 的硬前提 | 1000–1500（中） | L2-10, L2-4, L2-7, L2-3, L2-6, L3-1 |
| 第 4 章 | 接入 Hermes：把搜索后端指向本地实例 | 1000–1400（中） | L3-1, L3-3, L3-4, L3-5 |
| 第 5 章 | 验证与排错：curl、403 与 extract 边界 | 1200–1800（中） | L3-1, L2-6, L3-4, L3-5 |
| 第 6 章 | 进阶可选：引擎裁剪、端口、升级与公共实例 | 900–1400（中） | L2-3, L2-10, L2-1, L2-2, L2-8, L1-2, L3-1 |

篇幅分布：1 短 / 1 长 / 4 中 —— 概念章（第 1 章）最短，动手主章（第 2 章）最长，其余均匀，无「全短」或「全长」堆叠。

---

## 第 1 章：SearXNG 是什么：一句话看懂 + 隐私模型

- **篇幅**：800–1200 字（短）
- **章节定位**：概念章。建立「元搜索 / 聚合器 / 实例 / 脱敏」心智模型，为后面「动手」提供唯一动机。
- **素材引用**：
  - L1-1 · `sources/l1-1_searxng-docs-index.rst:9-12`（定位：「free internet metasearch engine…aggregates results from up to …search services；Users are neither tracked nor profiled；可用于 Tor」）
  - L1-2 · `sources/l1-2_own-instance.rst:24-37`（隐私经「请求脱敏」三形式实现，:26；随机浏览器 profile，:33-35；出口 IP 为实例 IP，:36-37）
  - L1-2 · `sources/l1-2_own-instance.rst:48-50`（公共实例须信任其管理员）
  - L1-2 · `sources/l1-2_own-instance.rst:60-62`（自建 = 完全掌控：源码 / 日志设置 / 私有数据）
  - L1-3 · `sources/l1-3_configured_engines.html:449-450`（SearXNG 本体口径：261 配置 / 81 默认启用）
  - L1-5 · `sources/l1-5_repo-readme.rst:61`（许可 AGPL-3.0）
- **代码示例**：无（概念章不放命令，避免打断阅读）

**结构（≤3 级）**

- `### 1.1 一句话看懂`
  - 开篇 3 句内交付：SearXNG 是把「搜什么、谁在搜」替你挡在门外的元搜索引擎，自托管 = 把中介换成你自己控制的那个。
- `### 1.2 元搜索是什么（比喻先于术语）`
  - 比喻：把 SearXNG 想成「只帮你跑腿、不留姓名的前台」，你去问它，它替你分别去 Google / Bing / 维基等门口各问一遍，再把答案汇总给你，但那几家看到的不是「你」。
  - 比喻后「所以……」回到实际意义 → 再给术语：metasearch engine（元搜索引擎）、aggregator（聚合器）。
- `### 1.3 隐私模型：三次「脱敏」`
  - 「脱敏」三形式（:26）+ 随机浏览器 profile（:33-35）+ 出口 IP 为实例 IP（:36-37）。
  - 实体落点：一张「同一句话在不同方案里，谁看得见」对比表（普通搜索引擎 / 公共 SearXNG 实例 / 自建实例 × 搜索服务看得见什么 / 实例管理员看得见什么）。
- `### 1.4 自建还是用别人的实例（谁值得信任）`
  - 公共实例须信任管理员（:48-50）→ 自建 = 完全掌控（:60-62）。
  - 冻结口径落点：SearXNG 本体规模 = **261 个已配置 / 81 个默认启用**（L1-3 :449-450）。此处**不提** Hermes 的「70+」（留到第 4 章并标注 Hermes 归属），禁止把两个口径合成一个数字。
  - 顺带一句：许可 AGPL-3.0（L1-5 :61）。
- `### 1.5 名词扫盲表`
  - 术语首次出现即解释的集中落点：元搜索、聚合器、实例（instance）、脱敏、AGPL-3.0、Tor。
- `### 1.6 引文对照（原文 / 中译 / 出处）`
  - 本章英文整句逐字原文 + 中译 + `文件:行`；出处查不到写 `—`。

---

## 第 2 章：动手：用 Docker 把 SearXNG 跑起来

- **篇幅**：1800–2600 字（长）
- **章节定位**：动手主章。给两条等价路径，并**点明官方 compose 是双服务 `core` + `valkey`、配置挂载 `./core-config/`（与 Hermes 单服务配方不同）**。
- **素材引用**：
  - L3-1 · `sources/l3-1_web-search.md:149-181`（「Option A — Self-host with Docker (recommended)」：建目录 :155-158、compose 块 :162-175、`SEARXNG_BASE_URL` 环境变量 :173）
  - L2-1 · `sources/l2-1_installation-docker.html:490-528`（官方 compose 安装步骤：mkdir/core-config :500-502、下载 compose+.env.example :504-507、cp .env :511-517、up -d :519-524）
  - L2-2 · `sources/l2-2_container-docker-compose.yml:1-28`（双服务 `core` + `valkey`：端口 `${SEARXNG_PORT:-8080}` 在 :12；valkey 服务 :18-24；镜像 tag `${SEARXNG_VERSION:-latest}` 在 :9；配置挂载 `./core-config/:/etc/searxng/:Z` 在 :15）
  - L2-1 · `sources/l2-1_installation-docker.html:616-622`（两个数据卷：`/etc/searxng` = 配置文件；`/var/cache/searxng` = 持久数据）
  - L2-1 · `sources/l2-1_installation-docker.html:579-591`（官方手动 `docker run` 示例：宿主 `-p 8888:8080`，:585；「accessible at http://localhost:8888」，:591）
  - L2-1 · `sources/l2-1_installation-docker.html:624-633`（`$SEARXNG_*` 映射 server/general 配置；`$FORCE_OWNERSHIP` 属主修正）
  - L2-8 · `sources/l2-8_env.example:8-15`（`#SEARXNG_VERSION=latest` :9、`#SEARXNG_HOST=[::]` :12、`#SEARXNG_PORT=8080` :15 —— 三项默认全注释）
  - L2-9 · `sources/l2-9_entrypoint.sh:80-97`（首启从 `/usr/local/searxng/settings.template.yml` 生成 `settings.yml`，:84-91，并把 `ultrasecretkey` 随机化，:93）
  - L2-9 · `sources/l2-9_entrypoint.sh:114-124`（entrypoint 只处理 `SEARXNG_PORT` → `GRANIAN_PORT`，:116-124）
  - L2-10 · `sources/l2-10_searx-settings-default.yml:88-94`（裸机出厂 `port: 8888` :90、`bind_address: "127.0.0.1"` :91；`base_url` 注释「Is overwritten by ${SEARXNG_BASE_URL}」:92-93）
  - L2-1 · `sources/l2-1_installation-docker.html:476-487`（Docker Hub 被限流时改用 `ghcr.io/searxng/searxng`，:481,486）
- **代码/命令示例（本章出现的块）**：
  1. `bash` — 建工作目录（`mkdir -p ~/searxng/searxng`；来源 L3-1 :156-157）
  2. `yaml` — **路径① Hermes 单服务** `docker-compose.yml`（`8888:8080` + `./searxng:/etc/searxng:rw` + `SEARXNG_BASE_URL=http://localhost:8888/`；来源 L3-1 :162-175）
  3. `bash` — `docker compose up -d`（L3-1 :180）
  4. `bash` — **路径② 官方编排**四条命令（mkdir `./searxng/core-config/` → curl 下载 compose + `.env.example` → `cp -i .env.example .env` → `docker compose up -d`；来源 L2-1 :500-524）
  5. `yaml` — 官方 compose **关键差异片段**（双服务 `core`+`valkey`、`./core-config/` 挂载、`${SEARXNG_PORT:-8080}`；来源 L2-2 :7-24）
  6. `bash` — `docker compose ps`（观察 `searxng-core` / `searxng-valkey` 与 `0.0.0.0:8080->8080/tcp`；来源 L2-1 :551-556）
- **结构（≤3 级）**：
  - `### 2.1 先选一条路`
    - 路径①（Hermes 单服务配方，最省事）vs 路径②（SearXNG 官方双服务编排）；一句话说清差异与适用。
  - `### 2.2 概念：容器第一次启动时发生了什么`
    - 首启 entrypoint 从模板生成 `settings.yml` 并随机化 `secret_key`（L2-9 :84-93）→ 所以「配置要用 `docker cp` 取回来改」，不是从零手写。
    - 实体落点：一张「容器内路径 / 宿主路径」挂载目录树（`/etc/searxng` ↔ 宿主 `./searxng` 或 `./core-config/`；`/var/cache/searxng` ↔ 数据卷）。
  - `### 2.3 路径① 照抄：Hermes 单服务`
    - 建目录 → 写 `docker-compose.yml` → `docker compose up -d` → 打开 `http://localhost:8888`。
    - **新手可跳过**（只想最快跑通的人照抄即可）。
  - `### 2.4 路径② 官方编排，及与路径① 的 4 处差异`
    - 按官方四步走；然后逐条对照：① 多一个 `valkey` 缓存服务（L2-2 :18-24）；② 挂载点是 `./core-config/:/etc/searxng/:Z`（L2-2 :15），**不是** `./searxng`；③ 端口默认宿主=容器=8080，要 8888 就设 `SEARXNG_PORT=8888`（L2-2 :12；L2-8 :15）；④ `.env` 三项默认全注释，即用镜像默认（L2-8 :8-15）。
    - **新手可跳过**。
  - `### 2.5 端口口径（对比表，全篇冻结）`
    - 表格四行：官方 compose 默认（容器 8080 / 宿主 8080，L2-2 :12）｜官方手动 run 示例（宿主 8888 → 容器 8080，L2-1 :585）｜**裸机**出厂 settings（8888，L2-10 :90）｜Hermes 配方（宿主 8888 → 容器 8080，L3-1 :169）。
    - 结论句：**容器内一律 8080；8888 要么是宿主映射端口、要么是裸机出厂默认**；`SEARXNG_URL` 必须与宿主端口一致（本句在第 4、5 章原样复用，不改写）。
  - `### 2.6 引文对照（原文 / 中译 / 出处）`

---

## 第 3 章：开启 JSON API —— Hermes 的硬前提

- **篇幅**：1000–1500 字（中）
- **章节定位**：把「出厂默认只给 html」这个坑单独成章，因为它是接入失败的头号原因。
- **素材引用**：
  - L2-10 · `sources/l2-10_searx-settings-default.yml:83-86`（出厂 `search.formats` 只开 `html`；`# formats: [html, csv, json, rss]` 为注释行）
  - L2-4 · `sources/l2-4_settings_search.html:438-457`（`search:` 块文档；`formats:` 在 :455-456）
  - L3-1 · `sources/l3-1_web-search.md:183-201`（第 4 步「Enable the JSON API format」；`docker cp` 取回 :189；追加覆盖块 :196-201；完整样例 :205-219）
  - L2-7 · `sources/l2-7_settings.template.yml:1-8`（官方安装模板最简：`use_default_settings: true` + `server.secret_key` / `image_proxy`，**无** `search.formats`）
  - L2-3 · `sources/l2-3_settings.html:451-458`（`settings.yml` 加载顺序：`SEARXNG_SETTINGS_PATH` 全路径 → `/etc/searxng/settings.yml` → 兜底出厂文件）
  - L2-3 · `sources/l2-3_settings.html:460-501`（`use_default_settings: true` 时「用户文件只写覆盖」，其余继承默认）
  - L2-6 · `sources/l2-6_search_api.html:444-448`（未设 `format` → 403 Forbidden；很多公共实例禁用这些格式）
- **代码/命令示例（本章出现的块）**：
  1. `bash` — `docker cp searxng:/etc/searxng/settings.yml ~/searxng/searxng/settings.yml`（取回生成的配置；L3-1 :189）
  2. `yaml` — 追加覆盖块 `search.formats: [html, json]`（L3-1 :196-201）
  3. `yaml` — 完整最简 `settings.yml` 样例（`use_default_settings: true` + `secret_key` + `formats`；L3-1 :205-219）
  4. `bash` — `docker cp` 写回 + `docker restart`（L3-1 :224-225）
- **结构（≤3 级）**：
  - `### 3.1 结论先行：这一步不做，后面全白干`
    - 3 句内说清：SearXNG 出厂只输出网页（`html`），Hermes 只吃 JSON；两者对不上，第 4 章接不进去。
  - `### 3.2 概念：settings.yml 从哪来、怎么「只写覆盖」`
    - 加载顺序（L2-3 :451-458）+ `use_default_settings: true` 的心智模型（L2-3 :460-501）。
    - 实体落点：一份真实的最简 `settings.yml` 文件内容（L2-7 全文）+「容器内 `/etc/searxng/settings.yml` ↔ 宿主文件」路径对照。
  - `### 3.3 照抄：取回 → 改 → 写回 → 重启`
    - 四个命令块连起来，末尾进第 5 章的自检 curl。
    - **新手可跳过**。
  - `### 3.4 最容易踩的坑：不开 JSON 就是 403`
    - 出厂只开 html（L2-10 :83-86）→ 未开 format 返回 403（L2-6 :444-448）；提示「403 时回头看 3.3」。
  - `### 3.5 引文对照（原文 / 中译 / 出处）`

---

## 第 4 章：接入 Hermes：把搜索后端指向本地实例

- **篇幅**：1000–1400 字（中）
- **章节定位**：动手收口章。只讲「一个环境变量 + 一个后端选择」，并锁定 Hermes 侧口径。
- **素材引用**：
  - L3-1 · `sources/l3-1_web-search.md:145`（Hermes 对 SearXNG 的定位 + 「**No API key required**」；此处出现 Hermes 口径「70+ search engines」，写作时**必须标 Hermes 归属**）
  - L3-1 · `sources/l3-1_web-search.md:237-251`（第 7 步：`SEARXNG_URL=http://localhost:8888` :241；`web.search_backend: "searxng"` :248；「Or set via `hermes tools` → Web Search & Extract → SearXNG」:251）
  - L3-1 · `sources/l3-1_web-search.md:270-281`（「Pair SearXNG with an extract provider」；`web.extract_backend: "firecrawl"` 及备选清单 :278）
  - L3-1 · `sources/l3-1_web-search.md:437-449`（自动探测表：`SEARXNG_URL` → `searxng`，:445）
  - L3-3 · `sources/l3-3_cli-commands.md:99`（顶层命令 `hermes tools`：Configure enabled tools per platform）
  - L3-4 · `sources/l3-4_searxng-search-SKILL.md:17-19`（Skill 侧：70+ 引擎、**No API key required**、当 `FIRECRAWL_API_KEY` 未配置时自动作为兜底出现）
  - L3-5 · `sources/l3-5_provider.py:1-22`（源码级佐证：模块 docstring 示例 `SEARXNG_URL=http://localhost:8080` :4；`KEY_ENV = "SEARXNG_URL"` :22 —— 唯一必需变量）
- **代码/命令示例（本章出现的块）**：
  1. `bash` / `.env` — `~/.hermes/.env` 写入 `SEARXNG_URL=http://localhost:8888`（L3-1 :240-241）
  2. `yaml` — `~/.hermes/config.yaml` 的 `web.search_backend` / `web.extract_backend`（L3-1 :246-249、:275-279）
  3. `bash` — `hermes tools`（交互选择 Web Search & Extract → SearXNG；L3-3 :99、L3-1 :251）
- **结构（≤3 级）**：
  - `### 4.1 一句话看懂：一个环境变量就能接上`
    - Hermes 侧唯一必需的是 `SEARXNG_URL`（源码 `KEY_ENV`，L3-5 :22），且**无需 API key**（L3-1 :145）。
  - `### 4.2 概念：Hermes 怎么挑搜索后端`
    - 自动探测逻辑的实体落点：一张「环境里有什么 → 自动选哪个后端」表（节选，含 `SEARXNG_URL` → `searxng`；L3-1 :437-449）。
    - 冻结口径：讲 Hermes 规模时写「Hermes 文档称 70+」（L3-1 :145；L3-4 :17），**不改写为 SearXNG 官方口径**；SearXNG 本体数字仍以第 1 章的 261/81 为准。
  - `### 4.3 动手：改 .env + config.yaml（或走 `hermes tools`）`
    - 三条路径等价：手改 `.env` + `config.yaml`，或 `hermes tools` 交互选择。
    - **新手可跳过**。
  - `### 4.4 关键分界：SearXNG 只负责「搜」`
    - 明确预告：正文提取（`web_extract`）走的是**另一个** provider（L3-1 :147、:270-281），第 5 章细讲。
  - `### 4.5 引文对照（原文 / 中译 / 出处）`

---

## 第 5 章：验证与排错：curl、403 与 extract 边界

- **篇幅**：1200–1800 字（中）
- **章节定位**：自检 + 症状对照表。让读者不靠猜就能定位「没接上」的原因。
- **素材引用**：
  - L3-1 · `sources/l3-1_web-search.md:228-235`（第 6 步：`curl …?format=json` + python 解析结果数；期望「10 results」；403 = JSON 仍未开，回看第 4 步）
  - L2-6 · `sources/l2-6_search_api.html:439-448`（两个端点 `/` 与 `/search`，均支持 GET/POST；未设 format → 403；很多公共实例禁用格式）
  - L3-1 · `sources/l3-1_web-search.md:147`（SearXNG **search-only** —— `web_extract` 需另配 provider）
  - L3-5 · `sources/l3-5_provider.py:1-3`（源码 docstring：`Search-only — SearXNG aggregates upstream engines but does not fetch URLs.`）
  - L3-4 · `sources/l3-4_searxng-search-SKILL.md:163-169`（Limitations：实例不可达则搜索失败；**无正文提取**，只回 snippets；公共实例限流；引擎覆盖取决于实例配置）
  - L3-4 · `sources/l3-4_searxng-search-SKILL.md:171-179`（Troubleshooting 表：`SEARXNG_URL` 未设 / Connection refused / 空结果 / 响应慢 / `json` 不支持）
  - L3-4 · `sources/l3-4_searxng-search-SKILL.md:181-184`（Pitfalls：**Always set `SEARXNG_URL`** :183；查询需 URL 编码）
  - L3-1 · `sources/l3-1_web-search.md:264-266`（官方警示：公共实例有限流、可用性波动、可能随时禁用 JSON；生产建议自托管）
- **代码/命令示例（本章出现的块）**：
  1. `bash` — 自检 `curl -s "http://localhost:8888/search?q=test&format=json" | python3 -c "…print(f'{len(d[\"results\"])} results')"`（L3-1 :231-232）
  2. `bash` — 看日志 `docker compose logs -f core` / `docker container logs -f searxng`（L2-1 :559、:601）
  3. `bash` — 进容器排查 `docker compose exec -it --user root core /bin/sh -l`（L2-1 :563）
- **结构（≤3 级）**：
  - `### 5.1 一句话看懂：一条 curl 就知道接得对不对`
  - `### 5.2 自检：期望输出长什么样`
    - 实体落点：命令 + 真实输出样例（`N results`）；讲清「打印出数字 = JSON 通了」。
  - `### 5.3 症状 → 病因 → 处置（对照表）`
    - 403 Forbidden → JSON 未开 → 回第 3 章（L3-1 :235；L2-6 :447）
    - Connection refused → 容器没起或 URL 错（L3-4 :176）
    - 空结果 → 实例挡了该查询，换实例或自建（L3-4 :177）
    - 响应慢 → 公共实例过载，自建或换实例（L3-4 :178）
    - `json` 格式不支持 → 版本旧，试 `format=rss` 或升级（L3-4 :179）
  - `### 5.4 边界：`web_extract` 不走 SearXNG`
    - 双证（官方文档 L3-1 :147 + 源码 L3-5 :3）+ Skill 侧同一结论（L3-4 :166），说明「搜得到 ≠ 取得到正文」，要另配 extract provider。
  - `### 5.5 引文对照（原文 / 中译 / 出处）`

---

## 第 6 章：进阶可选：引擎裁剪、端口、升级与公共实例

- **篇幅**：900–1400 字（中）
- **章节定位**：可选加深。只点到能自洽使用的程度，不做生产部署完整教程。
- **素材引用**：
  - L2-3 · `sources/l2-3_settings.html:502-516`（`use_default_settings` 下 `engines.remove`，示例移除 `google`）
  - L2-3 · `sources/l2-3_settings.html:517-533`（`engines.keep_only`，示例只留 `google` + `duckduckgo`）
  - L2-10 · `sources/l2-10_searx-settings-default.yml:88-97`（`port` / `bind_address` :89-91；`base_url` 被 `${SEARXNG_BASE_URL}` 覆盖 :92-93；`limiter` 被 `${SEARXNG_LIMITER}` 覆盖 :96）
  - L2-1 · `sources/l2-1_installation-docker.html:537-543`（更新 compose/.env 模板）
  - L2-1 · `sources/l2-1_installation-docker.html:545-549`（升级服务：`docker compose down` → `pull` → `up -d`）
  - L2-8 · `sources/l2-8_env.example:8-9`（可钉具体版本标签，例 `2026.3.25-541c6c3cb`）
  - L2-2 · `sources/l2-2_container-docker-compose.yml:9`（镜像 `${SEARXNG_VERSION:-latest}` 滚动更新）
  - L2-2 · `sources/l2-2_container-docker-compose.yml:18-24`（官方编排含 `valkey` 缓存服务）
  - L1-2 · `sources/l1-2_own-instance.rst:52-55`（公共实例无保护更易被滥用，招致 CAPTCHA 或封 IP，结果变少）
  - L3-1 · `sources/l3-1_web-search.md:255-266`（Option B 公共实例 + 官方 caution 全文）
- **代码/命令示例（本章出现的块）**：
  1. `yaml` — `use_default_settings` 下 `engines.remove` / `engines.keep_only` 片段（L2-3 :505-514、:519-530）
  2. `bash` — 升级：`docker compose down && docker compose pull && docker compose up -d`（L2-1 :546-548）
  3. `.env` — 钉版本：`SEARXNG_VERSION=2026.3.25-541c6c3cb`（L2-8 :8-9）
- **结构（≤3 级）**：
  - `### 6.1 改端口与暴露方式`
    - 复述第 2.5 节的端口口径（不改写），再给 `${SEARXNG_PORT}` / `${SEARXNG_BIND_ADDRESS}` / `${SEARXNG_BASE_URL}` / `${SEARXNG_LIMITER}` 四个可覆盖项（L2-10 :89-96）。
  - `### 6.2 裁剪引擎`
    - `remove` 与 `keep_only` 两条路；对比表（只写「想屏蔽某引擎用 remove／想只留几个用 keep_only」）。
  - `### 6.3 升级与固定版本`
    - `latest` 滚动 vs 钉 tag；官方编排含 `valkey` 缓存服务，但**最小可用不需要**（措辞：官方编排含缓存服务；最小可用不需要——不判定「必需」）。
  - `### 6.4 自建 vs 公共实例`
    - 只引官方风险陈述（限流 / 可用性波动 / 随时关 JSON / 易被 CAPTCHA 或封 IP）；**不写 DuckDuckGo 正面比较**（无来源，不臆造）。
  - `### 6.5 引文对照（原文 / 中译 / 出处）`

---

## 学习路径说明

### 前置要求
- 会用 `docker` / `docker compose`（意图文件已确认用户有 Docker 自托管经验）。
- 熟悉 Hermes 配置体系：`SOUL.md` / `AGENTS.md` / `config.yaml` / `.env`。
- 本机可与 Hermes 同机跑本地 Docker（`localhost:8888`）。

### 学完能做什么
- 用 Docker 在本机跑起一个 SearXNG 实例，并说清官方双服务（`core` + `valkey`）与 Hermes 单服务配方的差异。
- 把 SearXNG 出厂关闭的 JSON 格式打开，并用一条 `curl` 自检通过。
- 用 `SEARXNG_URL` 把 Hermes 的搜索后端指向本地实例，且**不配置任何 API key**。
- 遇到 403 / Connection refused / 空结果时，按症状对照表定位原因。
- 说清「SearXNG 只管搜索、`web_extract` 需另配 provider」的边界。

### 建议学习顺序
1. 第 1 章（约 5 分钟）——建立动机与心智模型。
2. 第 2 章（约 20 分钟）——照抄路径①跑通；有精力再看路径②。
3. 第 3 章（约 10 分钟）——开 JSON，这是接 Hermes 的前置。
4. 第 4 章（约 10 分钟）——改 `.env` / `config.yaml` 接上 Hermes。
5. 第 5 章（约 10 分钟）——curl 自检 + 排错。
6. 第 6 章（可选，约 10 分钟）——按需加深。
- 第 2–4 章为强顺序：端口口径与 JSON 状态会在下游章节原样复用，**不要跳读**（跳读会导致 `SEARXNG_URL` 与宿主端口对不上）。

---

## 跨章口径冻结表

> 下表为第 2–6 章共用口径。写作时**逐字沿用**，不得改写、不得合并、不得重算。每条右侧「来源锚点」为回源核对过的行号。

| # | 口径 | 冻结写法 | 来源锚点 | 禁止 |
| --- | --- | --- | --- | --- |
| F1 | 引擎数（SearXNG 本体） | 261 个已配置 / 81 个默认启用 | L1-3 · `l1-3_configured_engines.html:449-450` | 不得与 70+ 合成单一数字；不得使用 352（量纲不同） |
| F2 | 引擎数（Hermes 文档口径） | 「Hermes 文档称 70+」（须标 Hermes 归属） | L3-1 · `l3-1_web-search.md:145`；L3-4 · `l3-4_searxng-search-SKILL.md:3,17` | 不得写成 SearXNG 官方口径 |
| F3 | 端口（容器内） | 容器内默认监听 8080 | L2-2 · `l2-2_container-docker-compose.yml:12`；L2-8 · `l2-8_env.example:15` | 不得说容器内是 8888 |
| F4 | 端口（宿主） | 宿主映射端口可任意；8888 = 宿主映射或裸机出厂默认 | L3-1 · `l3-1_web-search.md:169`；L2-1 · `l2-1_installation-docker.html:585`；L2-10 · `l2-10_searx-settings-default.yml:90` | 不得把宿主 8888 说成容器内端口 |
| F5 | `SEARXNG_URL` 对齐 | 必须等于**宿主映射端口**（8080 或 8888 皆可，两侧一致） | L3-1 · `l3-1_web-search.md:241`；L3-5 · `l3-5_provider.py:22` | 不得与宿主端口不一致 |
| F6 | `SEARXNG_BASE_URL` | 官方支持项（由 `settings.yml` 的 `base_url` 被其覆盖）；**官方 compose 未启用**；**Hermes 配方显式设置** | L2-10 · `l2-10_searx-settings-default.yml:92-93`；L3-1 · `l3-1_web-search.md:173` | 不得写「官方编排用了它」，也不得写「它没用」 |
| F7 | 官方 compose 结构 | 双服务 `core` + `valkey`，配置挂载 `./core-config/`（与 Hermes 单服务配方不同） | L2-2 · `l2-2_container-docker-compose.yml:7-24`（挂载 :15） | 不得与 Hermes 单服务配方混为一谈 |
| F8 | 能力边界 | SearXNG **仅 search-only**；`web_extract` 需另配 provider | L3-1 · `l3-1_web-search.md:147`；L3-5 · `l3-5_provider.py:3`；L3-4 · `l3-4_searxng-search-SKILL.md:166` | 不得写 SearXNG 能取正文 |
| F9 | 许可 | AGPL-3.0 | L1-5 · `l1-5_repo-readme.rst:61` | — |
| F10 | 取回日期 | 官方文档页无发布日期，引用统一写「取回日期 2026-10-07」 | 全 `sources/` 快照 | 不得臆造发布日期 |

---

## 需用户确认的问题

1. **章节数 6 是否保留？** 我按方向 A 的 5 条主线拆成 6 章（把「开启 JSON」从第 2 章独立出来，因为它是接入失败头号原因）。若想压到 5 章，我会把第 3 章并入第 2 章末节——请确认取 6 还是 5。
2. **第 2 章两条路径的主次。** 意图备注写「走最省事路径」，但冻结口径要求点明官方 compose 双服务差异。我按「路径①（Hermes 单服务）为主、路径②（官方双服务）作对照」处理。是否同意？
3. **深研行号漂移，是否以本大纲为准并回写修正 `02_deep_research.md`？** 我逐条回源核对时发现 5 处行号与 `sources/` 实际不符，本大纲已改用核对后的行号：
   - L2-c 数据卷：深研写 `l2-1:587-588` → 实为 `l2-1:616-622`（586-587 是 run 示例里的 `-v` 挂载）
   - L2-d 官方安装步骤：深研写 `l2-1:468-489` → 实为 `l2-1:500-528`
   - L2-e 手动 `docker run`：深研写 `l2-1:551-558` → 实为 `l2-1:579-591`（551-558 是 `docker compose ps` 输出）
   - L2-g `$SEARXNG_*` 环境变量：深研写 `l2-1:595-596` → 实为 `l2-1:624-633`
   - L2-l settings 加载顺序：深研写 `l2-3:420-421` → 实为 `l2-3:451-458`
4. **来源 `L1-4`（`l1-4_about.html`）未使用。** 它在深研 claim 表中没有映射任何主张，我默认不用。若要引用它（如「About SearXNG」的某个具体说法），请指明要覆盖的点，我再回源取行号。
5. **名词扫盲表与「引文对照」表的体例。** 按 `note-style.md`（术语首次出现即解释）与 `note-system.md`（成句英文引文一律给中译、每章末留档原文）这两条默认执行：第 1 章加「名词扫盲表」，每章末加「引文对照（原文 / 中译 / 出处）」表。是否接受？若不想要中译留档，请明说（会偏离项目默认规则）。
6. **发布目标沿用。** 最终笔记发到 `AI学习/Hermes Agent/SearXNG 自托管指南/`，完成后在 `AI学习/Hermes Agent/Hermes Agent MOC.md` 追加一条索引项。确认沿用？

---

> 下一步：用户确认本大纲后，进入 P4 逐章写作（建议顺序：第 1 章 → 第 2 章 → 第 3 章 → 第 4 章 → 第 5 章 → 第 6 章，第 2–4 章强顺序不可跳读，每章写完停下等确认）。逐章 dispatch 时必须附本文件「跨章口径冻结表」全表。
