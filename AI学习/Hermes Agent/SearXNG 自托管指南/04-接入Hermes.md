---
title: "第 4 章：接入 Hermes：把搜索后端指向本地实例"
tags:
  - AI学习
  - Agent
  - Hermes
  - SearXNG
  - 自托管
created: 2026-10-07
updated: 2026-10-07
status: 已完成
source_project: searxng-hermes
---

> [[03-开启JSON-API|⬅ 上一章]] · [[README|📖 返回目录]] · [[05-验证与排错|下一章 ➡]]

# 第 4 章：接入 Hermes：把搜索后端指向本地实例

## 4.1 一句话看懂：一个环境变量就能接上

上一章开好了 JSON，这一章把 Hermes 的搜索后端指向你本机的实例。好消息是：**Hermes 侧唯一必需的设置就是一个环境变量 `SEARXNG_URL`**，指向你的实例地址即可，**不需要任何 API key**。[^c4-a] 源码里也印证了这一点——SearXNG provider 声明的「唯一必需环境变量」正是 `SEARXNG_URL`。[^c4-b]

## 4.2 概念：Hermes 怎么挑搜索后端

Hermes 选择「用哪个搜索引擎」有一套优先级：显式配置（`web.search_backend`）优先，其次是共享的 `web.backend`，最后才是**根据环境变量自动探测**。[^c4-c] 也就是说，只要你设了 `SEARXNG_URL`，即使不写任何配置，Hermes 也会自动认出 SearXNG。自动探测表节选如下：[^c4-d]

| 环境里有什么 | 自动选哪个后端 |
| --- | --- |
| `SEARXNG_URL` | `searxng` |
| `FIRECRAWL_API_KEY` 或 `FIRECRAWL_API_URL` | `firecrawl` |
| `TAVILY_API_KEY` | `tavily` |
| （什么都没设） | keyless ring：`exa` / `parallel` / `firecrawl` / `keenable` |

这里有个容易混淆的**口径**要单独说清。**Hermes 文档称它聚合 70+ 个搜索引擎**（这是 Hermes 自己的说法）；而 **SearXNG 本体的规模是第 1 章那个口径——261 个已配置、81 个默认启用**。两者**归属不同、不要合并成一个数字**，本文也只在讲 Hermes 定位时才提「70+」。

> [!tip] 大白话
> 「自动探测」就像**插上什么设备、系统自动切到哪个输入源**：你插了 `SEARXNG_URL` 这根线，Hermes 就自动把搜索切到 SearXNG，不用你去设置里挑。

## 4.3 动手：改 `.env` + `config.yaml`（或走 `hermes tools`）

**第一步，把实例地址写进 `~/.hermes/.env`**（端口必须与第 2 章的**宿主端口**一致）：[^c4-e]

```bash
# ~/.hermes/.env
SEARXNG_URL=http://localhost:8888
```

**第二步，在 `~/.hermes/config.yaml` 里把搜索后端指到 `searxng`**（顺带配好提取后端，见 4.4）：[^c4-f]

```yaml
# ~/.hermes/config.yaml
web:
  search_backend: "searxng"
  extract_backend: "firecrawl"   # 或 tavily / perplexity / keenable / exa / parallel
```

**第三步（替代写法），也可以走交互命令**——不用手改文件，直接在命令行里选：[^c4-g]

```bash
hermes tools
# 交互里选：Web Search & Extract → SearXNG
```

三条路等价，任选其一。接完后用第 5 章的 `curl` 自检即可确认通了。

## 4.4 关键分界：SearXNG 只负责「搜」

一定要记住这条边界：**SearXNG 只做搜索，不负责提取网页正文**。官方明确写了它是 search-only，`web_extract` 需要**另一个** provider。[^c4-a2] 源码 docstring 同样注明：它只是聚合上游引擎，**并不会去抓取 URL**。[^c4-h]

所以 `web_search`（搜索）可以由 SearXNG 承担，而 `web_extract`（取正文）要单独配一个 provider——就是 4.3 里那行 `extract_backend: "firecrawl"`。第 5 章会把这个边界讲透。

> [!warning] 别把「搜得到」当成「取得到」
> SearXNG 返回的是标题、链接和**摘要片段**，不是整页正文。[^c4-i] 想拿全文，得靠 `web_extract` 那一路。

## 4.5 引文对照（原文 / 中译 / 出处）

> 「出处」列写 `来源ID · sources/文件名:行`。本章每条引文都查得到具体来源，因此**没有用到 `—`**（`—` 表示「来源不明、宁空不猜」）。本章所引来源快照的取回日期均为 2026-10-07。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `SearXNG is a privacy-respecting, open-source metasearch engine that aggregates results from 70+ search engines. No API key required — just point Hermes at a running SearXNG instance.` | SearXNG 是一个尊重隐私的开源元搜索引擎，聚合来自 70+ 个搜索引擎的结果；无需 API key——只要把 Hermes 指向一个正在运行的 SearXNG 实例。（注：此处的「70+」是 Hermes 文档口径） | L3-1 · sources/l3-1_web-search.md:145 |
| 2 | `SearXNG is search-only — web_extract requires a separate extract provider.` | SearXNG 只做搜索——web_extract 需要单独的提取 provider。 | L3-1 · sources/l3-1_web-search.md:147 |
| 3 | `Search-only — SearXNG aggregates upstream engines but does not fetch URLs.` | 仅搜索——SearXNG 聚合上游引擎，但并不抓取 URL。 | L3-5 · sources/l3-5_provider.py:3 |
| 4 | `No API key required when using a public instance. Can also be self-hosted for full control.` | 使用公共实例时无需 API key；也可以自托管以获得完全掌控。 | L3-4 · sources/l3-4_searxng-search-SKILL.md:19 |
| 5 | `No content extraction: SearXNG returns snippets, not full page content. Use web_extract, browser tools, or curl for full articles.` | 不提供正文提取：SearXNG 返回的是摘要片段，而非整页内容；要取全文请用 web_extract、浏览器工具或 curl。 | L3-4 · sources/l3-4_searxng-search-SKILL.md:166 |

[^c4-a]: Hermes Docs · Web Search · SearXNG 定位（`l3-1_web-search.md:145`）
[^c4-a2]: Hermes Docs · Web Search · 「search-only」边界（`l3-1_web-search.md:147`）
[^c4-b]: Hermes 源码 · `plugins/web/.../searxng.py` 的 `KEY_ENV`（`l3-5_provider.py:20-22`）
[^c4-c]: Hermes Docs · Web Search · 后端优先级（`l3-1_web-search.md:426-431`）
[^c4-d]: Hermes Docs · Web Search · 自动探测表（`l3-1_web-search.md:437-449`）
[^c4-e]: Hermes Docs · Web Search · 第 7 步 `SEARXNG_URL`（`l3-1_web-search.md:239-241`）
[^c4-f]: Hermes Docs · Web Search · `search_backend` / `extract_backend`（`l3-1_web-search.md:246-249,275-279`）
[^c4-g]: Hermes Docs · CLI · `hermes tools`（`l3-3_cli-commands.md:99`）；交互入口（`l3-1_web-search.md:251`）
[^c4-h]: Hermes 源码 · `l3-5_provider.py:1-3`
[^c4-i]: SearXNG Search Skill · Limitations（`l3-4_searxng-search-SKILL.md:165-169`）
