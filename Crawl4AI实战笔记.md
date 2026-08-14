---
title: 本次会话实战笔记：资料收集工具选型与 Crawl4AI 接入
tags:
  - Crawl4AI
  - 资料收集
  - MCP
  - research-collector
  - 学习笔记自动化
created: 2026-08-14
updated: 2026-08-14
status: 规划完成（实施在另一窗口）
source_project: study-system
---

# 本次会话实战笔记：资料收集工具选型与 Crawl4AI 接入

> [!summary]
> 本次会话围绕「学习笔记自动化系统」的资料收集链路，依次完成了：① 厘清 WebFetch / Skill / MCP 三者的定位区别；② 为本项目选型开源工具；③ 制定「Crawl4AI 接入 research-collector 精读阶段」的落地方案。本笔记按会话实际发生的内容记录，实施由另一窗口执行。

## 1. 核心概念：WebFetch vs Skill vs MCP

> [!note] 三者不是同层级的"三个选项"，而是「零件 / 流程 / 扩展能力」的关系

| | 定位 | 类比 |
|---|---|---|
| **WebFetch** | Claude Code 内置的单步工具：抓单个 URL → 转 Markdown → 小模型回答 | 一把螺丝刀 |
| **Skill** | 打包的方法论 + 流程 + 项目规范，内部编排多个工具 | 说明书 + 整个工具箱 |
| **MCP** | 协议，把外部工具/数据源接进 Claude Code，扩展原生没有的能力 | 新买的电动工具 |

关键认知：

- **Skill 内部会调用 WebFetch**——`research-collector` 的精读阶段（Phase 2）就是用 WebFetch 深读的，所以不是"二选一"
- WebFetch 只管"读某个确定 URL"，不做搜索、去重、过滤、综合、落盘
- Skill 解决的是"从**未知位置**系统性找资料"，还有 token 优化（隔离 subagent + 150 字摘要约束）
- MCP 解决的是 WebFetch 做不到的能力：JS 动态渲染、登录态、真实浏览器 DOM、调 API

选型建议：已知 URL 快读 → WebFetch；系统性研究 → research-collector；动态页/认证/数据库 → MCP。

## 2. 开源项目选型

按用户选定的方向「**资料收集/研究工具** + **AI/Agent 工作流工具**」检索后选出：

### 资料收集 / 研究工具

| 项目 | 落点 |
|---|---|
| **Crawl4AI** | 强化 research-collector 精读：批量并发、干净 Markdown、结构化提取、本地缓存（本次选定） |
| **Trafilatura** | 轻量正文净化，不想上重型爬虫时的备选 |
| **Firecrawl** | 自托管 API 服务，自带反爬，可作 MCP 接入 |
| **RSSHub** | 万物转 RSS，配合 [[N8N定时抓取热点资讯指南]] 扩展数据源 |
| **ScrapeGraphAI** | AI 驱动爬虫，自然语言指定提取字段的备选 |

### AI / Agent 工作流工具

| 项目 | 落点 |
|---|---|
| **anthropics/skills** | 官方 skills 仓库，用其最佳实践复盘本项目 50+ 自定义 skill |
| **fastmcp** | Python 构建 MCP server，可把收集逻辑包装成自建 MCP |
| **playwright-mcp** | 浏览器自动化 MCP，和现有 `browser-cdp` 互补/替代 |
| **DeerFlow** | 深度研究多智能体框架，作为**架构参考**（非替换） |
| **context7** | 给 LLM 提供最新库文档，写技术笔记时降低幻觉 |
| **awesome-mcp-servers** | MCP 生态目录索引 |

> [!tip] 当时给出的落地优先级
> ① Crawl4AI（质变）→ ② anthropics/skills（审 skill 体系）→ ③ playwright-mcp 或 fastmcp（二选一）。RSSHub 是零改代码的补充。

## 3. 环境探查结果

实施前探查到的本机事实：

- conda 26.5.3 位于 `C:\Users\zhq\miniconda3`，仅 `base` 环境
- Git Bash 的 PATH 里**没有 conda**，需用绝对路径调用 `Scripts/conda.exe`
- 无系统 Python/pip；有 `uv 0.12.3`（本次未采用）
- `research-collector` 为本地自研 skill，**不在** `skills-lock.json` 管理内，无 `.codex/` 镜像 → 可直接改 `.claude/skills/`，无需同步

## 4. Crawl4AI 接入 research-collector 方案

### 4.1 安装（conda）

```bash
CONDA="/c/Users/zhq/miniconda3/Scripts/conda.exe"
"$CONDA" create -n crawl4ai python=3.12 -y
BASE="$("$CONDA" info --base)"
ENV_PY="$BASE/envs/crawl4ai/python.exe"
"$ENV_PY" -m pip install -U crawl4ai
"$ENV_PY" -m playwright install chromium   # ~150MB，装一次
```

### 4.2 代码改动

```text
.claude/skills/research-collector/
├── SKILL.md                  # Phase 2 精读改为 crawl.sh 主路径 + WebFetch 回退
├── manifest.yaml             # subprocess: none → allow
└── scripts/                  # 新增
    ├── setup.sh              # 一键安装
    ├── crawl.sh              # bash 启动器：解析 conda → 定位 env python
    └── crawl.py              # Crawl4AI 封装 CLI
```

核心调用（2026 新版 API，需防御性兼容新旧 markdown 字段）：

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async with AsyncWebCrawler(config=BrowserConfig(browser_type="chromium", headless=True)) as crawler:
    result = await crawler.arun(url=url, config=CrawlerRunConfig(
        word_count_threshold=10,
        excluded_tags=["form", "nav"],
        remove_overlay_elements=True,
    ))
    markdown = getattr(getattr(result, "markdown", None), "raw_markdown", None) or result.markdown
```

### 4.3 使用形态

```bash
# 单 URL → stdout / 文件
crawl.sh --url "https://example.com"
crawl.sh --url "https://example.com/article" --output ./a.md

# 批量 3-5 篇 → 输出目录（共享浏览器，一次并发）
crawl.sh --url "https://a.com/p1" --url "https://b.com/p2" --output-dir ./crawl-out/
```

### 4.4 验证清单

```bash
"$BASE/envs/crawl4ai/python.exe" -c "import crawl4ai; print(crawl4ai.__version__)"  # ① 安装校验
crawl.sh --url https://example.com                                                    # ② 单 URL 冒烟
crawl.sh --url https://example.com --url https://example.org --output-dir /tmp/crawl-test  # ③ 批量冒烟
```

## 5. 当前状态与后续

- ✅ 本窗口完成：概念辨析、选型、环境探查、落地方案、本笔记
- ⏳ 另一窗口执行：conda 环境安装、脚本创建、SKILL.md / manifest.yaml 修改、验证
- 完成后建议：把本笔记 `status` 更新为「已完成」，并补充实测输出与踩坑记录

## 相关笔记

- [[N8N定时抓取热点资讯指南]] — 定时采集链路
- [[Marker PDF转换教学案例]] — 文档处理链路
- [[RSS使用指南]] — RSS 数据源
