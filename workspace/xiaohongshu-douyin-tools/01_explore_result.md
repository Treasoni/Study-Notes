# 01 - 探测结果（P1 Explore）

> run_id: `xiaohongshu-douyin-tools` ｜ learning-note-flow P1
> 主题：经营小红书和抖音的开源项目与工具盘点
> 探测日期：2026-09-05
> 说明：3 个独立透镜（自动发布 / 内容生产 / 数据运营）并行探测，候选均经 GitHub 页面直连核实；灰产/无法核实项已排除。

## 一、候选清单（按场景归类，已按 URL 去重）

### 场景 1 · 自动发布 / 多平台分发

| # | 工具 | 类型 | 协议 | 维护 / star | 部署 | 覆盖 | 主要风险 | 评分 | URL | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **social-auto-upload** (dreammis) | CLI+Web 分发 | MIT | 一般(2026-03 重构中) / ~15k★ | 源码 pip+Playwright，Vue3+Flask | 11+ 平台（含抖音/小红书） | Cookie 登录态、平台风控、页面/接口变动 | 5 | https://github.com/dreammis/social-auto-upload | 生态最完整，另见 vault 既有配置笔记 |
| 2 | MediaPublishPlatform (funfan0517) | Web 运营面板 | MIT | unknown / ~153★ | Docker / 源码 | 9 平台 | 同分发类 | 3 | https://github.com/funfan0517/MediaPublishPlatform | 可视化批量+定时，star 少需自测 |
| 3 | omnipost (rehatRobot) | 分发二开 | MIT | 较新(仅 1 commit) / ~46★ | 源码 | 增头条/搜狐/知乎 | 依赖上游同步 | 2 | https://github.com/rehatRobot/omnipost | social-auto-upload 衍生增量 |

### 场景 2 · 内容生产（AI 图文/短视频/剪辑）

| # | 工具 | 类型 | 协议 | 维护 / star | 部署 | 覆盖 | 主要风险 | 评分 | URL | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | **MoneyPrinterTurbo** (harry0703) | 文字一键成片 | MIT | 活跃 / ~120k★ | Docker / 源码 | 通用（适配竖屏） | 素材版权、质量依赖 LLM | 5 | https://github.com/harry0703/MoneyPrinterTurbo | 文案→配音→字幕→素材全自动 |
| 5 | FunClip (modelscope) | ASR 字幕驱动剪辑 | MIT | 活跃 v2.2.1(2026-09-01) / ~6k★ | 源码 + Gradio | 通用（二次剪辑） | 本地推理需 GPU | 4 | https://github.com/modelscope/FunClip | 基于 FunASR，句段定位剪辑 |
| 6 | ShortGPT (RayVentura) | 短视频生成框架 | MIT | 一般(2025-02 后近停更) / ~8k★ | 源码 | 通用（YT/TikTok 向） | 依赖外部 API | 3 | https://github.com/RayVentura/ShortGPT | 架构参考；无中文/小红书调性优化 |

### 场景 3 · 内容生产 + 分发 + 运营一体化

| # | 工具 | 类型 | 协议 | 维护 / star | 部署 | 覆盖 | 主要风险 | 评分 | URL | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 | **AiToEarn** (yikart) | AI 内容营销 Agent 平台 | MIT | 活跃 v2.5.0(2026-06) / ~26k★ | Docker compose 一键 / 源码 / SaaS | 14+ 平台（含抖音/小红书） | 部分能力/Agent 依赖云服务与第三方模型 Key；自动化分发受风控 | 4 | https://github.com/yikart/AiToEarn | 生成-分发-汇总数据一体化；有商业托管版 |

### 场景 4 · 数据采集 / 分析 / 运营

| # | 工具 | 类型 | 协议 | 维护 / star | 部署 | 覆盖 | 主要风险 | 评分 | URL | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|
| 8 | **MediaCrawler** (NanmiCoder) | 数据采集器 | NON-COMMERCIAL（禁商用） | 活跃 / ~64k★ | 源码 uv+Playwright/CDP（无官方 Docker） | 7 平台（小红书/抖音/快手/B站等） | 采集合规、平台反爬、登录态 | 5 | https://github.com/NanmiCoder/MediaCrawler | 中文社媒采集事实标准；对标/选题/评论分析底层数据源 |
| 9 | xhs_douyin_content (cwjcw) | 自账号数据分析 | GPL-3.0 | 一般 / ~303★ | 源码 pip+扫码登录态 | 抖音+小红书 | 创作者中心接口变动；自账号合规风险较低 | 4 | https://github.com/cwjcw/xhs_douyin_content | 抓自己创作者中心每作品指标→Excel 日报，补开放 API 缺口 |
| 10 | CreatorHub (3441293738) | 评论/私信/多账号面板 | unknown | 活跃 / ~1.9k★ | 源码 FastAPI 本地 | 抖音/小红书/快手/视频号 | 较高：自动回复/私信/搬运有灰产边界，需低频防风控 | 4 | https://github.com/3441293738/creatorhub | 统一管作品/粉丝/私信/评论+关键词采集 |
| 11 | Visual_MediaCrawler (persist-1) | 采集可视化看板 | 非商用（继承上游） | 小众 / ~69★ | 源码 uv+npm+uvicorn | 7 平台 | 同 MediaCrawler | 3 | https://github.com/persist-1/Visual_MediaCrawler | MediaCrawler 可视化改造，爬取+展示一体 |

## 二、方向菜单（P2 深研范围，请选择）

- **A. 全景盘点（推荐）**：以上述 4 大场景组织全篇，每场景给 Top 工具 + 选型建议；P2 深挖 7 个核心候选（social-auto-upload、AiToEarn、MoneyPrinterTurbo、FunClip、MediaCrawler、CreatorHub、xhs_douyin_content），边缘候选（MPP、ShortGPT、Visual_MediaCrawler、omnipost）作简评。
- **B. 聚焦「AI 生产 → 自动发布」链路**：围绕 MoneyPrinterTurbo + AiToEarn + social-auto-upload 的端到端组合，P2 只深挖这 3-4 个，偏实战组合推荐。
- **C. 聚焦「数据与合规」视角**：以 MediaCrawler 生态 + xhs_douyin_content + 官方开放平台 SDK 为线，讲透数据采集边界、自账号指标与合规路径；P2 深挖数据侧 3-4 个 + 开放平台资料。

## 三、覆盖缺口（P2 需说明或补源）

1. **素材/脚本管理**：开源空白、商业 SaaS 主导（已按规则不列灰产），笔记中标注为「开源空白」。
2. **官方开放平台数据分析**：抖音有官方 OpenAPI SDK（如 SKIT.FlurlHttpClient.ByteDance / dy-java 系），但无成熟自部署数据分析工具；小红书无通用公开官方数据 API —— 建议作为「合规路径」独立讨论而非工具条目。
3. **高灰产风险项已排除**：MediaMate（自动点赞/关注/评论/群控）不入库；CreatorHub/AiToEarn 的一键互动/分发踩自动化红线，收录时均需标注风控与封号风险。

## 四、估算 P2 范围

- 核心源：官方 GitHub README / Docs / Release（每个候选 1-2 个主源），共约 10-14 个源。
- 补充源：开放平台文档（抖音开放平台 1-2 篇）、合规讨论（平台规则/风控）1-2 篇。
- 产出：`02_deep_research.md`（scope、源表、声明/源映射、矛盾点、实践指引、开放问题、下游交接）。
