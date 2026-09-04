# social-auto-upload P1 探测结果

> 项目：social-auto-upload（dreammis/social-auto-upload）
> 阶段：P1 探测式收集
> 日期：2026-09-05
> 探测视角：① 项目概览 ② 快速上手 ③ 配置与常见坑

## 核心发现

- **项目本质**：用 Python + 浏览器自动化，把「AI agent 临时解析网页做多平台分发」的高频重复劳动固化成脚本，自动上传视频/图文到多个短视频/内容平台并支持定时发布。
- **当前主线**：仓库近期做了大重构 —— 统一为 **CLI（`sau` 命令）+ skills** 架构；旧的 Flask+Vue Web 版已保留但**非当前主线、不保证可运行**。README 为当前权威源。
- **活跃度**：约 14.8k star / 2.5k fork / MIT 协议，2026 年持续活跃。
- **运行机制**：Python（uv 管理，>=3.10,<3.13）+ `patchright`（Playwright 分支）+ `stealth.min.js` 反检测；按 `account_name` 分账号 cookie 登录，多账号可并发；以 headless 为主攻方向。

### 支持平台矩阵（README 一手口径）
- 抖音 / 小红书 / 快手 / 视频号 / B站 / TikTok 等 11 平台支持视频上传。
- 抖音 / 小红书 / 快手 支持图文（upload-note）。
- 抖音 / 小红书 / 快手 / 视频号 / B站 / TikTok 支持定时发布。
- B站：运行时自动下载 `biliup` 封装驱动。
- YouTube：走浏览器自动化（非官方 API）。

## 方向菜单

- **A. 快速上手跑通**（推荐，贴合用户「部署+跑通」意图）：从环境/安装 → conf.py → 账号登录 → 首次上传 的最小闭环。
- **B. 配置详解**：平台账号与 cookie 机制、发布参数（标题/话题/定时/可见性）、conf.example.py 全量键位。
- **C. 部署运维与排错**：Linux/Docker 部署、登录失效、平台风控、代理、headless 被识别等真实坑。
- **D. 全流程综合**：A+B+C 组合，产出一份完整上手+配置+排错指南。

## 候选源清单（去重后）

| # | title | url | tier | date | score | supports |
|---|-------|-----|------|------|-------|----------|
| 1 | GitHub 仓库主页 + README | https://github.com/dreammis/social-auto-upload | 1 | 2026 活跃 | 5 | 平台矩阵; sau CLI; 账号/cookie 机制; conf.py 说明; YouTube/代理 |
| 2 | 官方安装说明 docs/install.md | https://github.com/dreammis/social-auto-upload/blob/main/docs/install.md | 1 | unknown | 5 | uv 安装; patchright install chromium; 镜像加速; conf.example.py→conf.py; LOCAL_CHROME_PATH/HEADLESS/DEBUG; verify_code.txt; biliup 下载 |
| 3 | pyproject.toml | https://github.com/dreammis/social-auto-upload/blob/main/pyproject.toml | 1 | unknown | 4 | Python 3.10–3.12; sau 入口; 依赖 patchright/qrcode/opencv |
| 4 | 官方文档站 sap-doc | https://sap-doc.nasdaddy.com/ （安装页 /docs/installation/） | 1 | unknown | 3 | 旧版安装路径; 注意滞后于 CLI 重构 |
| 5 | DeepWiki 项目解析（聚合） | https://deepwiki.com/dreammis/social-auto-upload | 2 | 2026-08 | 3 | CLI-first 架构; 反检测; uploader 模块化 |
| 6 | DeepWiki Auth & Cookie | https://deepwiki.com/dreammis/social-auto-upload/6-authentication-and-cookie-management | 2 | unknown | 4 | cookie 存储/校验; check 判定信号; storage_state; CDP 导出 |
| 7 | GitHub Issues（登录/失效/上传失败检索） | https://github.com/dreammis/social-auto-upload/issues?q=is%3Aissue+%E7%99%BB%E5%BD%95+OR+%E5%A4%B1%E6%95%88+OR+%E6%89%BE%E4%B8%8D%E5%88%B0+OR+%E4%B8%8A%E4%BC%A0%E5%A4%B1%E8%B4%A5 | 3 | 2026 Q2 | 4 | 登录失败案例(#283/#230/#252); 页面改版; headless 风控; 视频号 qrconnect; B站 21566 |
| 8 | DEV Community 深度解析 | https://dev.to/tenglongai2026/this-11k-tool-auto-publishes-to-7-platforms-tiktok-youtube-bilibili-douyin--34o2 | 2 | unknown | 3 | 第三方上手视角; 平台能力佐证（数据滞后） |
| 9 | CSDN Linux 部署排错 | https://blog.csdn.net/qq_56694800/article/details/161059269 | 3 | unknown | 3 | Python 版本兼容; Chromium 下载镜像; LOCAL_CHROME_PATH; headless 开关 |

## 覆盖缺口

- **conf.example.py 全量键位**：P1 仅确认关键开关，未逐一核对全部配置项（P2 需抓 raw conf.example.py）。
- **发布参数字段**：标题/话题/定时/可见性/合集等主要在 CLI 层（`--tags/--visibility/--playlist/--tid`），README 未细述 → P2 需深挖各平台 uploader 或 CLI 帮助。
- **版本口径冲突**：官方文档站（sap-doc）仍停留在旧版 `pip install -r requirements.txt` + playwright；README 主线是 `uv` + patchright。笔记中必须标注新旧两套，避免误导。
- **YouTube/更多平台的当前状态**：搜索快照与 README 有出入，以 README 一手为准。
- 水印去除、AI 生成标题/话题等**未被列为显式功能**，笔记中不写。

## P2 预估范围

- 抓取核心源：#1 README、#2 docs/install.md、conf.example.py（raw）、#3 pyproject.toml、#6 DeepWiki Auth、#7 精选 Issues。
- 预计 5-6 个源，覆盖：安装部署、conf.py 配置、账号登录与 cookie 维护、CLI 发布命令、常见坑与排错。
- 若用户选 B/C 方向，追加：各平台 uploader 源码页、更多 Issues、Docker/Linux 排错帖。
