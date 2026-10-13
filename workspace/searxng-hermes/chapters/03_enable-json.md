## 第 3 章：开启 JSON API —— Hermes 的硬前提

### 3.1 结论先行：这一步不做，后面全白干

SearXNG 出厂只把结果输出成**网页**（`html`），而 Hermes 只吃 **JSON**。这两边对不上，第 4 章就会接不进去。所以这一章要做的就一件事：把 SearXNG 的 JSON 输出打开——**这一步不做，后面全部白搭**。而且它改的是配置文件——得打开 `settings.yml` 改一行、再重启容器让它生效。

### 3.2 概念：`settings.yml` 从哪来、怎么「只写覆盖」

SearXNG 启动时按固定顺序找它的配置文件 `settings.yml`：先看环境变量 `SEARXNG_SETTINGS_PATH` 指定的**完整路径**，没有就找 `/etc/searxng/settings.yml`；这两个都读不到，才回落到镜像自带的出厂文件。[^c3-a] 这就是为什么我们在第 2 章强调「容器里一定有一份 `/etc/searxng/settings.yml`」——首启时 entrypoint 已经替你生成好了。

关键心智模型是 `use_default_settings: true`：**打开它之后，你自己的 `settings.yml` 只需要写「要覆盖的那几项」，其余全部继承出厂默认**。[^c3-b] 官方安装模板里最简的 `settings.yml` 就短短几行：一个 `use_default_settings: true`，加一个 `server:` 块（`secret_key` 与 `image_proxy`）——注意它**没有** `search.formats`，这正是 JSON 默认关着的原因。[^c3-c]

实体落点：同一份 `settings.yml`，在容器里和宿主的哪个位置——改的时候两处都要对上：

| 位置 | 路径 |
| --- | --- |
| 容器内 | `/etc/searxng/settings.yml` |
| 宿主（路径① Hermes 配方） | `~/searxng/searxng/settings.yml` |
| 宿主（路径② 官方编排） | `./searxng/core-config/settings.yml` |

> [!tip] 大白话
> `use_default_settings: true` 就像**只填变更单**：出厂默认是一整套齐备的家具，你只在这张单子上写「多买一把椅子」，其余不用重抄一遍。所以改 JSON，只要在单子上补一行，不是把整份配置重写。

### 3.3 照抄：改配置 → 重启（本册两条路径都能省掉 `docker cp`）

> [!tip] 先说结论：本册两条路径都不用「取回 / 写回」
> 本册两条路径都把**宿主的一个目录挂到了容器的 `/etc/searxng/`**：路径① 挂的是 `~/searxng/searxng/`，路径② 挂的是 `./searxng/core-config/`。[^c3-j] 所以 `docker compose up -d` 起来之后，容器生成的那份 `settings.yml` **本来就落在你宿主上**——直接拿编辑器打开改就行，不需要先「取回来」。[^c3-k] 下面的 `docker cp` 只在**你没有把 `/etc/searxng` 挂到宿主**时才需要（那种情况下配置只活在容器里，复制出来改才不至于一重启就丢）。官方 Docker 安装文档里，路径② 的配置这步也是让你直接编辑 `core-config/settings.yml`，并没有 `docker cp`。[^c3-l]

**（可选）第一步，把容器里生成的配置取回宿主**——只有容器没把 `/etc/searxng` 挂到宿主时才需要（容器名按你的实际来：路径① 是 `searxng`，路径② 是 `searxng-core`）：[^c3-d]

```bash
docker cp searxng:/etc/searxng/settings.yml ~/searxng/searxng/settings.yml
```

**第二步，在文件里追加这段覆盖块**——`search.formats` 同时保留 `html` 并加上 `json`：[^c3-e]

```yaml
search:
  formats:
    - html
    - json
```

**第三步，文件的完整样子应该类似下面这样**（`use_default_settings: true` + 一个 `server:` 块 + 刚加的 `search:` 块），只要结构对上即可：[^c3-f]

```yaml
# ~/searxng/searxng/settings.yml
use_default_settings: true

server:
  secret_key: "abcdef12345678"
  image_proxy: true

search:
  formats:
    - html
    - json
```

**第四步，让它生效**——两条路径的配置文件已经是同一份，重启容器即可；只有你**真的**在第一步用 `docker cp` 把文件取出来过（未挂载的情况），才需要先写回、再重启：[^c3-g]

```bash
# 仅在未挂载、且前面确实用 docker cp 取出过时才需要这一行：
docker cp ~/searxng/searxng/settings.yml searxng:/etc/searxng/settings.yml
docker restart searxng
```

重启完成后，就能用第 5 章那条 `curl` 自检了。

### 3.4 最容易踩的坑：不开 JSON 就是 403

出厂 `settings.yml` 里 `search.formats` 只有一行 `- html`（上面那行 `# formats: [html, csv, json, rss]` 是**注释**，不生效）。[^c3-h] 结果就是：**不带 `format=json` 的请求会拿到 `403 Forbidden`**，因为那个格式是「未设置」的。[^c3-i]

所以以后一旦在第 4 章看到 `403`，第一反应就是回到 3.3 检查 `search.formats` 里到底有没有 `json`。

> [!warning] 公共实例尤其要注意
> 很多**公共** SearXNG 实例干脆禁用了这些机器可读格式，[^c3-i] 这也是官方建议生产环境自托管的原因之一。

### 3.5 引文对照（原文 / 中译 / 出处）

> 「出处」列写 `来源ID · sources/文件名:行`。本章每条引文都查得到具体来源，因此**没有用到 `—`**（`—` 表示「来源不明、宁空不猜」）。本章所引来源快照的取回日期均为 2026-10-07。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `If you want to consume the results as JSON, CSV, or RSS, you need to set the format parameter accordingly.` | 如果你想以 JSON、CSV 或 RSS 消费结果，就需要相应设置 format 参数。 | L2-6 · sources/l2-6_search_api.html:444-445 |
| 2 | `Requesting an unset format will return a 403 Forbidden error. Be aware that many public instances have these formats disabled.` | 请求一个未启用的格式会返回 403 Forbidden 错误；注意许多公共实例已禁用这些格式。 | L2-6 · sources/l2-6_search_api.html:446-448 |
| 3 | `SearXNG ships with JSON output disabled by default. Copy the generated config and enable it:` | SearXNG 出厂默认关闭 JSON 输出；把生成的配置复制出来并启用它。 | L3-1 · sources/l3-1_web-search.md:185 |
| 4 | `If use_default_settings: true is present, the file only contains your overrides. All other settings are inherited from the built-in defaults.` | 如果存在 use_default_settings: true，文件里就只包含你的覆盖项，其余设置都继承内置默认。 | L3-1 · sources/l3-1_web-search.md:193 |
| 5 | `You should see something like 10 results. If you get a 403 Forbidden, JSON format is still disabled — recheck step 4.` | 你应看到类似 10 results 的输出；若得到 403 Forbidden，说明 JSON 格式仍未启用——回去重查第 4 步。 | L3-1 · sources/l3-1_web-search.md:235 |

[^c3-a]: SearXNG Docs · settings.yml location（`l2-3_settings.html:451-457`）
[^c3-b]: SearXNG Docs · use_default_settings（`l2-3_settings.html:460-501`）
[^c3-c]: SearXNG 官方安装模板（`l2-7_settings.template.yml:1-8`，全文件无 `search.formats`）
[^c3-d]: Hermes Docs · Web Search · 第 4 步取回配置（`l3-1_web-search.md:187-189`）
[^c3-e]: Hermes Docs · Web Search · 追加的覆盖块（`l3-1_web-search.md:196-201`）
[^c3-f]: Hermes Docs · Web Search · 最简完整样例（`l3-1_web-search.md:205-219`）
[^c3-g]: Hermes Docs · Web Search · 写回并重启（`l3-1_web-search.md:223-225`）
[^c3-h]: 出厂 `settings.yml` 的 `search.formats` 仅 `- html`（`l2-10_searx-settings-default.yml:83-86`）
[^c3-i]: Search API 未设 format 返回 403，且许多公共实例禁用（`l2-6_search_api.html:444-448`）
[^c3-j]: 两条路径都把宿主目录挂到容器 `/etc/searxng`：路径① `l3-1_web-search.md:170-173`（`./searxng:/etc/searxng:rw`）；路径② `l2-2_container-docker-compose.yml:14-15`（`./core-config/:/etc/searxng/:Z`）
[^c3-k]: 首启会把模板生成进配置目录（`l2-9_entrypoint.sh:80-93`）——该目录正是挂载点，故生成物直接落在宿主
[^c3-l]: SearXNG 官方 Docker 安装文档 · 配置这步直接编辑宿主文件（`l2-1_installation-docker.html:527`）
