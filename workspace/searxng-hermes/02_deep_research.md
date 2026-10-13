# 阶段 2 深度研究 — SearXNG 自托管与 Hermes 接入

> 本文件是**中间产物（handoff artifact），不是权威终点**：引文与数值请回 `sources/` 按行号核对。
> 所有引文均已在落笔时与 `sources/` 逐字比对并记录行号；所有数值已当场重新计数。
>
> 深读日期：2026-10-07 ｜ 运行：`searxng-hermes` ｜ 方向：**A. 全量主线**
> 深读组：3 组（D1 概念 / D2 部署 / D3 Hermes 接入），每组 1 个 delegate（≤3/phase）

---

## 一、范围

本阶段只服务一件事：**用最省事的路径，把 SearXNG 跑在本机 Docker 上，并接到 Hermes**。

- **在范围内**：SearXNG 是什么与隐私模型（够用即止）；官方 Docker 自托管；开启 JSON API；`SEARXNG_URL` 接入 Hermes；验证与排错。
- **不在范围内**：SearXNG 内部实现（引擎解析器、限流算法细节）；公共实例清单（searx.space 全表，除非改走公共实例分支）；DuckDuckGo 正面比较（无来源，不虚构）。

---

## 二、来源总表（19 件引用件）

快照全部落在 `workspace/searxng-hermes/sources/`，均 HTTP 200、均为 `fetched`（无 `snippet-only`）。
tier：`official` = 官方文档；`primary` = 上游仓库原始文件（代码/配置，一手的实现证据）。

| ID | 文件（sources/ 内） | 标题 | tier | evidence_form | 取向日期 |
| --- | --- | --- | --- | --- | --- |
| L1-1 | `l1-1_searxng-docs-index.rst` | SearXNG Docs — Overview（`docs/index.rst`） | official | fetched | 2026-10-07 |
| L1-2 | `l1-2_own-instance.rst` | Why use a private instance? | official | fetched | 2026-10-07 |
| L1-3 | `l1-3_configured_engines.html` | Configured Engines | official | fetched | 2026-10-07 |
| L1-4 | `l1-4_about.html` | About SearXNG | official | fetched | 2026-10-07 |
| L1-5 | `l1-5_repo-readme.rst` | 上游 `searxng/searxng` README.rst | primary | fetched | 2026-10-07 |
| L2-1 | `l2-1_installation-docker.html` | Installation container (Docker) | official | fetched | 2026-10-07 |
| L2-2 | `l2-2_container-docker-compose.yml` | `container/docker-compose.yml` | primary | fetched | 2026-10-07 |
| L2-3 | `l2-3_settings.html` | Settings（位置 / `use_default_settings`） | official | fetched | 2026-10-07 |
| L2-4 | `l2-4_settings_search.html` | `settings_search`（`search.formats`） | official | fetched | 2026-10-07 |
| L2-5 | `l2-5_installation-scripts.html` | Installation Script（`utils/searxng.sh`，非容器） | official | fetched | 2026-10-07 |
| L2-6 | `l2-6_search_api.html` | Search API（`docs/dev/search_api`） | official | fetched | 2026-10-07 |
| L2-7 | `l2-7_settings.template.yml` | `container/settings.template.yml` | primary | fetched | 2026-10-07 |
| L2-8 | `l2-8_env.example` | `container/.env.example` | primary | fetched | 2026-10-07 |
| L2-9 | `l2-9_entrypoint.sh` | `container/entrypoint.sh` | primary | fetched | 2026-10-07 |
| L2-10 | `l2-10_searx-settings-default.yml` | `searx/settings.yml`（出厂默认） | primary | fetched | 2026-10-07 |
| L3-1 | `l3-1_web-search.md` | Hermes — Web Search & Extract | official | fetched | 2026-10-06 |
| L3-3 | `l3-3_cli-commands.md` | Hermes — CLI Commands（`hermes tools`） | official | fetched | 2026-10-07 |
| L3-4 | `l3-4_searxng-search-SKILL.md` | Hermes `optional-skills/.../searxng-search/SKILL.md` | primary | fetched | v1.0.1 |
| L3-5 | `l3-5_provider.py` | Hermes `plugins/web/searxng/provider.py` | primary | fetched | 2026-10-07 |

**tier 分布**：official 11 件 / primary 8 件，共 19 件。
**去重说明**：P1 的 L3-2（Hermes live docs 渲染版）与 L3-1 同源，仅作渲染一致校验，**未重复落盘、不计为独立来源**。
**L1-4 状态**：`l1-4_about.html` 仅存档，未映射任何主张（本轮 claim 表未使用）。若下游要引用，须先指明覆盖点并回源取行号。

> **行号勘误（2026-10-07，P3 期间发现并已修正）**：HTML 类来源（`l2-1`、`l2-3`）早前的行号锚点取自**去标签后的文本行号**，不是原文件行号——原文件含大量 `<span>` 标签，行号被拉长。已按**原文件**逐条重新核对并回写：
> `l2-1` 数据卷 `587-588 → 620-621`；`l2-1` 安装步骤 `468-489 → 501-522`；`l2-1` 手动 `docker run` `551-558 → 580-591`；`l2-1` `$SEARXNG_*` `595-596 → 628-629`；`l2-3` 加载顺序 `420-421 → 453-457`；`l2-3` `use_default_settings`/`remove`/`keep_only` `428-488 → 461-521`。
> `.rst/.yml/.md/.sh/.py/.env` 类来源（L1-1/L1-2/L1-5/L2-2/L2-7/L2-8/L2-9/L2-10/L3-*）的行号为原文件行号，未受影响。
> **教学点**：HTML 快照不要用「去标签后」的行号做锚点；锚点必须以原文件行号为准（`grep -n` 原文件，或 `Read` 原文件）。

---

## 三、Claim → Source 映射

引文一律逐字保留原文（含原始空格与标记），后附 `来源ID · 文件:行`。中文为「说人话」解释，不替代原文。

### 组 L1 — SearXNG 是什么

| # | 主张 | 原文（逐字） | 来源 · 行 |
| --- | --- | --- | --- |
| L1-a | 定位与隐私承诺 | `SearXNG is a free internet metasearch engine which aggregates results from up to {{engines | length}} :ref:`search services <configured engines>`.  Users are neither tracked nor profiled.  Additionally, SearXNG can be used over Tor for online anonymity.` | L1-1 · `l1-1_searxng-docs-index.rst:9-12` |
| L1-b | 隐私经「请求脱敏」三形式实现 | `Removal of private data from search requests comes in three forms:` | L1-2 · `l1-2_own-instance.rst:26` |
| L1-c | 出口 IP 是**实例的 IP**（可配代理/Tor） | `The IP address used will be the IP of the instance, but SearXNG can also be configured to use proxy or Tor.` | L1-2 · `l1-2_own-instance.rst:36-37` |
| L1-d | 公共实例须信任其管理员 | `If someone uses a public instance, they have to trust the administrator of that instance.` | L1-2 · `l1-2_own-instance.rst:48-49` |
| L1-e | 自建 = 完全掌控 | `If users run their :ref:`own instances <installation>`, everything is in their control: the source code, logging settings and private data.  Unknown instance administrators do not have to be trusted.` | L1-2 · `l1-2_own-instance.rst:60-62` |
| L1-f | 引擎数：**261 配置 / 81 默认启用** | `SearXNG supports 261 search engines of which 81 are enabled by default.` | L1-3 · `l1-3_configured_engines.html:449-450` |
| L1-g | 许可：AGPL-3.0 | `This project is licensed under the GNU Affero General Public License (AGPL-3.0).` | L1-5 · `l1-5_repo-readme.rst:61` |

> 说明：`{{engines | length}}` 是文档模板占位符（RST/Jinja），**不是**可直接引用的具体数字；具体数字以 L1-f 为准。

### 组 L2 — 怎么搭（Docker 自托管）

| # | 主张 | 原文 / 事实 | 来源 · 行 |
| --- | --- | --- | --- |
| L2-a | **官方 compose 是双服务**：`core` + `valkey` | `name: searxng` / 服务 `core`（`image: docker.io/searxng/searxng:${SEARXNG_VERSION:-latest}`）+ 服务 `valkey`（`image: docker.io/valkey/valkey:9-alpine`） | L2-2 · 全文（1-28 行） |
| L2-b | compose 端口默认 **8080** | `${SEARXNG_HOST:+${SEARXNG_HOST}:}${SEARXNG_PORT:-8080}:${SEARXNG_PORT:-8080}` | L2-2 · `l2-2_...yml:12` |
| L2-c | 两个数据卷 | `/etc/searxng`：`Configuration files (settings.yml, etc.)`；`/var/cache/searxng`：`Persistent data (faviconcache.db, etc.)` | L2-1 · `l2-1_...html:620-621` |
| L2-d | 官方安装步骤 | `mkdir -p ./searxng/core-config/` → `curl -fsSL ... -O .../container/docker-compose.yml` 与 `.../container/.env.example` → `cp -i .env.example .env` → `docker compose up -d` | L2-1 · `l2-1_...html:501-522` |
| L2-e | 手动容器示例（**宿主 8888 → 容器 8080**） | `docker run --name searxng -d -p 8888:8080 -v "./config/:/etc/searxng/" -v "./data/:/var/cache/searxng/" ...`；`This will start SearXNG in the background, accessible at http://localhost:8888` | L2-1 · `l2-1_...html:580-591` |
| L2-f | Docker Hub 被限流时的替代源 | `GHCR mirror`（`https://ghcr.io/searxng/searxng`） | L2-1 · `l2-1_...html:481,486` |
| L2-g | `$SEARXNG_*` 环境变量映射到配置 | `$SEARXNG_*`: Controls the SearXNG configuration options, look out for environment `$SEARXNG_*` in `server:`, `general:` and the `container/.env.example` template. | L2-1 · `l2-1_...html:628-629` |
| L2-h | 官方安装模板最简 | `use_default_settings: true` + `server: {secret_key: "ultrasecretkey", image_proxy: true}`（**无 `search.formats`**） | L2-7 · 全文（1-8 行） |
| L2-i | `container/.env.example` 三项**全部注释** | `#SEARXNG_VERSION=latest` / `#SEARXNG_HOST=[::]` / `#SEARXNG_PORT=8080` | L2-8 · `l2-8_env.example:9,12,15` |
| L2-j | entrypoint 行为：模板复制 + `secret_key` 随机化 | 从 `/usr/local/searxng/settings.template.yml` 复制到 `$__SEARXNG_CONFIG_PATH/settings.yml`，并 `sed -i "s/ultrasecretkey/$(head -c 24 /dev/urandom \| base64 \| tr -dc 'a-zA-Z0-9')/g"` | L2-9 · `l2-9_entrypoint.sh:80-94` |
| L2-k | entrypoint **只处理 `SEARXNG_PORT`**（+ `FORCE_OWNERSHIP`） | `case "${SEARXNG_PORT:-}" in` → `export GRANIAN_PORT="$SEARXNG_PORT"`；启动 `exec /usr/local/searxng/.venv/bin/granian searx.webapp:app` | L2-9 · `l2-9_entrypoint.sh:114-126` |
| L2-l | settings 加载顺序 | 先读 `SEARXNG_SETTINGS_PATH` 指定的全路径；否则 `/etc/searxng/settings.yml` | L2-3 · `l2-3_settings.html:453-457` |
| L2-m | `use_default_settings` 可只写覆盖 | `use_default_settings: true`；可 `engines: / remove:` 删引擎、`engines: / keep_only:` 保留引擎 | L2-3 · `l2-3_settings.html:461-521` |
| L2-n | **出厂 `search.formats` 只开 html**（JSON 默认关） | `# formats: [html, csv, json, rss]` 注释行 + `formats:` / `  - html` | L2-10 · `l2-10_...yml:84-86` |
| L2-o | 出厂 `server.port` 是 **8888**（裸机默认） | `port: 8888` / `bind_address: "127.0.0.1"` | L2-10 · `l2-10_...yml:90-91` |
| L2-p | **`SEARXNG_BASE_URL` 是官方支持的覆盖项** | `# public URL of the instance, to ensure correct inbound links. Is overwritten` / `# by ${SEARXNG_BASE_URL}.` / `base_url: false  # "http://example.com/location"` | L2-10 · `l2-10_...yml:92-94` |
| L2-q | 端口/绑定/限流同样可被 env 覆盖 | `# Is overwritten by ${SEARXNG_PORT} and ${SEARXNG_BIND_ADDRESS}`；`# Is overwritten by ${SEARXNG_LIMITER}` | L2-10 · `l2-10_...yml:89,96` |
| L2-r | Search API 有两个端点，未开 format 报 403 | `SearXNG supports querying via a simple HTTP API.  Two endpoints,` `/` `and` `/search` `, are supported for both GET and POST methods.`；`unset format will return a 403 Forbidden error.` | L2-6 · `l2-6_search_api.html:440-441,447` |

### 组 L3 — 怎么接 Hermes

| # | 主张 | 原文（逐字） | 来源 · 行 |
| --- | --- | --- | --- |
| L3-a | Hermes 对 SearXNG 的定位与「无需 API key」 | `SearXNG is a privacy-respecting, open-source metasearch engine that aggregates results from 70+ search engines. **No API key required** — just point Hermes at a running SearXNG instance.` | L3-1 · `l3-1_web-search.md:145` |
| L3-b | SearXNG **仅搜索**，提取需另配 provider | `SearXNG is **search-only** — \`web_extract\` requires a separate extract provider.` | L3-1 · `l3-1_web-search.md:147` |
| L3-c | Hermes 配方里的 compose 端口与 env | `- "8888:8080"`（端口映射）；`- SEARXNG_BASE_URL=http://localhost:8888/`（环境变量） | L3-1 · `l3-1_web-search.md:169,173` |
| L3-d | JSON 未开的表现是 403 | `If you get a \`403 Forbidden\`, JSON format is still disabled — recheck step 4.` | L3-1 · `l3-1_web-search.md:235` |
| L3-e | Hermes 侧连接变量与后端选择 | `SEARXNG_URL=http://localhost:8888`；`search_backend: "searxng"`；`extract_backend: "firecrawl"   # or tavily, perplexity, keenable, exa, parallel` | L3-1 · `l3-1_web-search.md:241,248,278` |
| L3-f | 公共实例的风险（官方明确警示） | `Public instances have rate limits, variable uptime, and may disable JSON format at any time. For production use, self-hosting is strongly recommended.` | L3-1 · `l3-1_web-search.md:265` |
| L3-g | 自动探测表：`SEARXNG_URL` → searxng 后端 | `| \`SEARXNG_URL\` | searxng |` | L3-1 · `l3-1_web-search.md:445` |
| L3-h | 源码级佐证：唯一必需变量 | `KEY_ENV = "SEARXNG_URL"` | L3-5 · `l3-5_provider.py:22` |
| L3-i | 源码级佐证：仅 search，不取正文 | `Search-only — SearXNG aggregates upstream engines but does not fetch URLs.` | L3-5 · `l3-5_provider.py:3` |
| L3-j | Skill 侧「无需 API key」「自动兜底」 | **No API key required** when using a public instance. Can also be self-hosted for full control. Automatically appears as a fallback when the main web search toolset (`FIRECRAWL_API_KEY`) is not configured. | L3-4 · `l3-4_searxng-search-SKILL.md:19` |
| L3-k | Skill 侧「无正文提取」与「必须设 URL」 | - **No content extraction**: SearXNG returns snippets, not full page content. Use `web_extract`, browser tools, or `curl` for full articles. ／ - **Always set `SEARXNG_URL`**: Without it, the skill cannot function. | L3-4 · `l3-4_searxng-search-SKILL.md:166,183` |

---

## 四、矛盾核实结论（P1 遗留 C1/C2/C3）

三项均由**父流程直接回源 grep/read 定案**，不采信子代理断言。

### C1 — 引擎数：**两个口径，不可合并**（已定案）

- SearXNG 官方（L1-3 · `:449-450`）：**261 个已配置，81 个默认启用**。
- Hermes 文档（L3-1 · `:145`；L3-4 · `:3,17`）：*"70+ search engines"*，共出现 **3 处**。
- 结论：`70+` 是 Hermes 文档的**约数**（面向其用户，非 SearXNG 权威口径）。写作时**分别标注归属**：讲 SearXNG 本体时用 261/81，讲 Hermes 定位时若要引 Hermes 口径则明确写「Hermes 文档称 70+」。**禁止**合成单一数字。
- 反例留痕：`grep -c "^  - name:" searx/settings.yml` 得 **352**，与 261 不符——这是**不同的量纲**（含注释/重复条目），**不作为引擎数使用**。

### C2 — `SEARXNG_BASE_URL`：**官方支持，但不由 entrypoint 处理**（已定案）

- 反证：`container/entrypoint.sh` **只**处理 `SEARXNG_PORT`（→ `GRANIAN_PORT`）与 `FORCE_OWNERSHIP`，全文无 `SEARXNG_BASE_URL`（L2-9 · 全文）。
- 正证：出厂 `searx/settings.yml` 明确注释 `base_url` **"Is overwritten by ${SEARXNG_BASE_URL}"**（L2-10 · `:92-93`）。
- 结论：该变量**由 Python settings 加载器读取**（非 shell entrypoint），是**官方支持的合法覆盖项**，用于「确保入库链接正确」。Hermes 配方 `SEARXNG_BASE_URL=http://localhost:8888/`（L3-1 · `:173`）**不是无效配置**；官方 `container/docker-compose.yml` 未列它，只是**官方编排未用到**（并非不支持）。
- 写作要点：不要写「官方编排用了它」，也不要写「它没用」；准确表述为「官方支持、官方 compose 未启用、Hermes 配方显式设置」。

### C3 — 端口：**容器内默认 8080；8888 是宿主映射或裸机默认**（已定案）

| 场景 | 端口 | 来源 |
| --- | --- | --- |
| 官方 compose 默认 | 容器 **8080**，宿主 **8080** | L2-2 · `:12`（`${SEARXNG_PORT:-8080}`） |
| `container/.env.example` 默认 | `#SEARXNG_PORT=8080`（注释态） | L2-8 · `:15` |
| 官方手动 `docker run` 示例 | 宿主 **8888** → 容器 **8080** | L2-1 · `:551-558` |
| **裸机**（非容器）出厂 settings | **8888** | L2-10 · `:90` |
| Hermes 配方 | 宿主 **8888** → 容器 **8080**，且 `SEARXNG_BASE_URL=http://localhost:8888/` | L3-1 · `:169,173` |
| Hermes provider 文档字符串示例 | `SEARXNG_URL=http://localhost:8080` | L3-5 · `:4` |

- 结论：**容器内 SearXNG 默认监听 8080**（entrypoint/镜像默认）；`8888` 要么是**宿主映射端口**（`-p 8888:8080`），要么是**裸机运行时的出厂默认**。写作时必须讲「容器内 8080、宿主可任意映射」，并指出 **Hermes 官方配方用 8888 是宿主侧选择**，同时 `SEARXNG_URL` 必须与**宿主映射端口**一致（8080 或 8888 都行，但两侧要对齐）。

### 未决缺口（承接 P1 的 G）

- G1 `searx.space` 公共实例清单：**不采**（方向 A 以自托管为主）。
- G2 DuckDuckGo 正面比较：**不写**（无来源，不虚构）。
- G3 官方文档页无发布日期：引用统一用「取回日期 2026-10-07」。

---

## 五、实操指引（可照抄，方向 A 主线）

> 以下为**两条等价路径**。路径① = Hermes 官方配方（最省事）；路径② = SearXNG 官方编排（更贴近上游现状，含 valkey 缓存服务）。
> 端口在两条路径里**必须自洽**：宿主端口 = `SEARXNG_URL` 里的端口。

### 路径① — Hermes 官方配方（单服务，最省事）

```yaml
# ~/searxng/docker-compose.yml   （来源：L3-1 · l3-1_web-search.md:162-175）
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8888:8080"                      # 宿主 8888 → 容器 8080
    volumes:
      - ./searxng:/etc/searxng:rw
    environment:
      - SEARXNG_BASE_URL=http://localhost:8888/
    restart: unless-stopped
```

开启 JSON（Hermes 必需）：

```yaml
# 追加到 ~/searxng/searxng/settings.yml   （来源：L3-1 · :196-201）
search:
  formats:
    - html
    - json
```

应用并自检：

```bash
docker cp ~/searxng/searxng/settings.yml searxng:/etc/searxng/settings.yml
docker restart searxng
curl -s "http://localhost:8888/search?q=test&format=json" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d[\"results\"])} results')"
# 期望：打印 "N results"；若 "403 Forbidden" = JSON 仍未开（来源 L3-1 · :231-235）
```

接入 Hermes：

```bash
# ~/.hermes/.env   （来源：L3-1 · :241）
SEARXNG_URL=http://localhost:8888
```

```yaml
# ~/.hermes/config.yaml   （来源：L3-1 · :246-249、:275-279）
web:
  search_backend: "searxng"
  extract_backend: "firecrawl"   # 或 tavily / perplexity / keenable / exa / parallel
```

### 路径② — SearXNG 官方编排（双服务 core + valkey）

```bash
# 来源：L2-1 · l2-1_installation-docker.html:468-489
mkdir -p ./searxng/core-config/
cd ./searxng
curl -fsSL -O https://raw.githubusercontent.com/searxng/searxng/master/container/docker-compose.yml
curl -fsSL -O https://raw.githubusercontent.com/searxng/searxng/master/container/.env.example
cp -i .env.example .env
docker compose up -d
```

- 结构与路径①的差异，必须讲清（否则读者按 Hermes 配方找不到 `core-config/`）：
  1. **双服务**：多一个 `valkey`（`docker.io/valkey/valkey:9-alpine`）做缓存（L2-2 · `:18-24`）。
  2. **配置挂载点不同**：官方挂 `./core-config/:/etc/searxng/:Z`（L2-2 · `:15`），Hermes 配方挂 `./searxng:/etc/searxng`。
  3. **端口默认 8080**（宿主=容器），要改 8888 就设 `SEARXNG_PORT=8888` 或改用端口映射（L2-8 · `:15`）。
  4. **`.env` 三项默认全注释**，即用镜像默认值（L2-8）。
- 首启后 `core-config/settings.yml` 由模板生成（`secret_key` 已随机化，L2-9 · `:80-94`），再按路径① 的方式补 `search.formats: [json]`。
- Docker Hub 被限流时改用 GHCR 镜像 `ghcr.io/searxng/searxng`（L2-1 · `:481,486`）。

### 必须讲的坑（每条都有来源）

1. **JSON 默认关**：出厂 `formats` 只有 `html`（L2-10 · `:84-86`）；不开就 403（L2-6 · `:447`；L3-1 · `:235`）。
2. **SearXNG 只搜不取**：`web_extract` 需另配 provider（L3-1 · `:147`；L3-5 · `:3`；L3-4 · `:166`）。
3. **端口要对齐**：容器内 8080，宿主映射任意；`SEARXNG_URL` 必须用**宿主端口**（C3）。
4. **`SEARXNG_BASE_URL` 用宿主 URL**：Hermes 配方设为 `http://localhost:8888/`（L3-1 · `:173`；C2）。
5. **公共实例不可靠**：有限流、可用性波动、随时关 JSON（L3-1 · `:265`）。
6. **镜像滚动无版本**：`searxng/searxng:latest`（L2-2 · `:9`）；`.env.example` 提示可钉版本标签如 `2026.3.25-541c6c3cb`（L2-8 · `:9`）。
7. **`latest` 升级**：`docker compose pull && docker compose up -d`（L2-1 · `:514-515`）。

---

## 六、未决问题（供写作时明确边界，勿臆测）

1. 官方文档未给「SearXNG 各引擎是否需各自 API key」的统一说明——**本文不展开**（超出「跑起来并接上」的范围）。
2. 官方 compose 的 `valkey` 是否**必需**：官方编排包含它，但 Hermes 单服务配方没有也能跑。**写作时表述为「官方编排含缓存服务；最小可用不需要」，不判定「必需」**。
3. 生产部署（反代、TLS、`limiter` 限流）只在「进阶」里点到，不给完整教程（G1/范围外）。
4. `SEARXNG_BIND_ADDRESS` / `SEARXNG_LIMITER` 等仅确认「可被 env 覆盖」（L2-10 · `:89,96`），未展开语义。

---

## 七、下游交接（给 outline-generator / chapter-writer）

- **可直接引用的来源 ID**：L1-1、L1-2、L1-3、L1-5、L2-1、L2-2、L2-6、L2-7、L2-8、L2-9、L2-10、L3-1、L3-4、L3-5。
- **引文纪律**：本文件所有引文已带 `文件:行`；下游引用时**回 `sources/` 按行核对**，不要从本文件二次转抄措辞。
- **数值纪律**：`261 / 81`（L1-3）、`70+`（L3-1/L3-4，标 Hermes 口径）、端口 `8080 / 8888`（C3 表）——**每个数字写进正文前重新计数**，不得合并口径。
- **建议章节骨架（待 P3 定稿）**：
  P0 一句话看懂（是什么 + 为什么自托管）→ 1 SearXNG 是什么（元搜索 + 隐私模型）→ 2 Docker 自托管（两条路径 + JSON 开启）→ 3 接入 Hermes（`SEARXNG_URL` + 后端）→ 4 验证与排错（curl / 403 / extract 边界）→ 5 进阶可选（引擎裁剪、端口、升级）。
- **发布目标**：`AI学习/Hermes Agent/SearXNG 自托管指南/`；完成后在 `AI学习/Hermes Agent/Hermes Agent MOC.md` 追加一条索引项。

---

## 自检

```
引文 47 处逐字核对（其中英文整句 17 处经校验器 V 全绿）/ 数值 8 处重新计数
```

- **校验器（`--mode verbatim --file 02_deep_research.md`）**：英文整句引文 **17 处**，原始来源命中 **17** / 仅自己中间产物命中 **0** / 未命中 **0** → 无硬失败。
  - 命令：`python3.12 .claude/scripts/note-citation-check.py workspace/searxng-hermes --mode verbatim --file 02_deep_research.md`
  - 注意：校验器只覆盖**英文整句**引文；中文表述、代码/配置片段与含内联标记的整句不在其覆盖内。
- **人工逐字比对**：另 **30 处**（中文解释、代码/路径/配置键片段、表格内联片段）已由父流程回 `sources/` 按行号核对。
- **数值重数（8 处）**：`261`、`81`、`70+`（3 处）、`19`（来源件）、`official 11 / primary 8`、`8080`、`8888`、`352`（反例）。
- **反例留痕**：`352` 来自 `grep -c "^  - name:"`，与官方 261 **量纲不同**，已注明不作引擎数使用。
- 结果同步记录在 `workspace/workflow-runs/searxng-hermes.workflow.md` 的 P2 检查行。
