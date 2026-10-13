## 第 6 章：进阶可选：引擎裁剪、端口、升级与公共实例

> [!tip] 新手可跳过
> 这一章是**可选加深**：前五章已经能让你跑通并接上 Hermes。这里只点到「能自洽使用」的程度，不讲生产部署的完整教程。照抄默认值也能用，读这一章是为了让你知道**还能往哪些方向调**。

### 6.1 改端口与暴露方式

端口这件事在第 2.5 节已经钉死，这里原样复述、不改写：

> **一句话钉死：容器内一律 8080；8888 要么是宿主映射端口、要么是裸机出厂默认**；`SEARXNG_URL` 必须与宿主端口一致。

在这一口径之上，裸机出厂 `settings.yml` 里有四个 `server:` 项可以被对应环境变量覆盖，等于给了你四个「不改文件、只改 `.env`」的调节旋钮：[^c6-a]

| 出厂配置项 | 含义 | 被哪个环境变量覆盖 |
| --- | --- | --- |
| `port`（出厂 8888） | 监听端口 | `${SEARXNG_PORT}` |
| `bind_address`（出厂 `"127.0.0.1"`） | 绑定地址 | `${SEARXNG_BIND_ADDRESS}` |
| `base_url`（出厂 `false`） | 对外公开的 URL | `${SEARXNG_BASE_URL}` |
| `limiter`（出厂 `false`） | 限流、拦部分机器人 | `${SEARXNG_LIMITER}` |

其中 `base_url` 的边界要按第 2 章的口径理解：它**是官方支持的覆盖项**（由 `settings.yml` 的 `base_url` 被环境变量覆盖），但**官方 compose 并未启用它**，是 Hermes 配方**显式设置**的。

> [!tip] 大白话
> 这四个旋钮就像**空调面板**：机器内部有一份默认设定（`settings.yml` 里写死的 8888 / 127.0.0.1），但墙上那排按钮（`SEARXNG_*` 环境变量）能直接盖过它——你一般只按按钮，不用拆开机器改焊点。

### 6.2 裁剪引擎

SearXNG 默认启用的引擎很多（本体规模见第 1 章：261 个已配置 / 81 个默认启用）。如果你只想用其中几个、或者想屏蔽某个不喜欢的引擎，可以用两条互补的路子，在 `settings.yml` 里二选一：[^c6-b]

```yaml
# 在 settings.yml 里，两种写法二选一

# 方式 A：从默认引擎里「移除」某个（示例：移除 google）
use_default_settings:
  engines:
    remove:
      - google

# 方式 B：只「保留」指定的几个引擎（示例：只留 google 与 duckduckgo）
use_default_settings:
  engines:
    keep_only:
      - google
      - duckduckgo
```

两条路的取舍其实很简单：

| 你的需求 | 用哪个 | 怎么想 |
| --- | --- | --- |
| 想屏蔽某几个引擎，其余照旧 | `engines.remove` | 黑名单：列出**不要**的 |
| 想只留少数引擎，其余都不要 | `engines.keep_only` | 白名单：列出**只要**的 |

记住一件事：**某个引擎到底能不能用，取决于这台实例的配置**——同一个引擎，在别人的实例上开着、在你的实例上可能被禁用。所以「搜不到某个来源」时，先想想是不是它被你（或实例）裁掉了。[^c6-c]

### 6.3 升级与固定版本

官方编排默认用的是滚动镜像标签 `${SEARXNG_VERSION:-latest}`：不指定版本时，`pull` 到的永远是最新镜像。[^c6-d] 想升级服务，标准三步是「停 → 拉新 → 起」：[^c6-e]

```bash
docker compose down
docker compose pull
docker compose up -d
```

如果你更想要**可复现**的部署（比如怕某天新版本改了行为），就在 `.env` 里钉一个具体版本号，镜像标签里那个文档给过的例子长这样：[^c6-f]

```bash
# ~/searxng/.env（或官方编排目录下的 .env）
SEARXNG_VERSION=2026.3.25-541c6c3cb
```

顺带说清 `valkey`：**官方编排里确实带了一个 `valkey` 缓存服务，但最小可用不需要它**。这里只做事实陈述，不判定它「必需」还是「不必需」——你按官方模板照跑，它就是编排的一部分。

### 6.4 自建 vs 公共实例

前面一直默认你走自建（Option A）。如果你动过「直接蹭一个公共实例」的念头，先看官方给的这一段警示：公共实例有限流、可用性会波动，还可能**随时把 JSON 格式关掉**；因此生产环境强烈建议自托管。[^c6-g]

还有一条更底层的理由：**没有防护的公共实例，其搜索服务更容易被滥用**，结果就是上游服务对这台实例抛出 CAPTCHA、甚至封掉它的 IP，于是所有经它发出的查询都只会返回更少的结果。[^c6-h]

所以真要临时用公共实例，正确姿势是**只挑那些明确开了 JSON 格式的**（官方目录在 searx.space，可按此过滤），并且接受「它随时可能变」这个前提。换句话说，公共实例适合救急，不适合长期依赖。

> [!warning] 别把公共实例当默认方案
> 你没法控制别人的实例：它可能限你的流、可能今天开着 JSON 明天关掉。要稳定，自建才是终点。

### 6.5 引文对照（原文 / 中译 / 出处）

> 「出处」列写 `来源ID · sources/文件名:行`。本章每条引文都查得到具体来源，因此**没有用到 `—`**（`—` 表示「来源不明、宁空不猜」）。本章所引来源快照的取回日期均为 2026-10-07。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `It is possible to remove some engines from the default settings.` | 可以从默认设置里移除一些引擎。 | L2-3 · sources/l2-3_settings.html:502 |
| 2 | `As an alternative, it is possible to specify the engines to keep. In the following example, SearXNG has only two engines:` | 作为一种替代方案，可以指定要保留的引擎；在下面的例子里，SearXNG 只保留两个引擎。 | L2-3 · sources/l2-3_settings.html:517 |
| 3 | `public instances without proper protection are more vulnerable to abuse of the search service, which may cause the external service to enforce CAPTCHAs or to ban the IP address of the instance.` | 缺乏恰当防护的公共实例，其搜索服务更容易被滥用，进而可能招致上游服务对其实施 CAPTCHA 校验、或封禁该实例的 IP 地址。 | L1-2 · sources/l1-2_own-instance.rst:52-55 |
| 4 | `Public instances have rate limits, variable uptime, and may disable JSON format at any time. For production use, self-hosting is strongly recommended.` | 公共实例有限流、可用性波动，且可能随时禁用 JSON 格式；生产环境强烈建议自托管。 | L3-1 · sources/l3-1_web-search.md:265 |

[^c6-a]: 出厂 `settings.yml` 的 `server:` 覆盖项（`l2-10_searx-settings-default.yml:88-97`）
[^c6-b]: SearXNG Docs · settings · `engines.remove` / `engines.keep_only`（`l2-3_settings.html:502-533`）
[^c6-c]: SearXNG Search Skill · Engine coverage（`l3-4_searxng-search-SKILL.md:168`）
[^c6-d]: 官方 compose · 镜像 `${SEARXNG_VERSION:-latest}`（`l2-2_container-docker-compose.yml:9`）
[^c6-e]: SearXNG Docs · Installation with Docker · 升级服务（`l2-1_installation-docker.html:545-549`）
[^c6-f]: `container/.env.example` · 钉版本标签（`l2-8_env.example:8-9`）
[^c6-g]: Hermes Docs · Web Search · 公共实例 caution（`l3-1_web-search.md:255-266`）
[^c6-h]: SearXNG Docs · Own Instance · 公共实例被滥用风险（`l1-2_own-instance.rst:52-55`）
