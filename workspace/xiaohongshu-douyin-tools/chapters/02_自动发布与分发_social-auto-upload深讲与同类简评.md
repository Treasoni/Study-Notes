# 第二章 自动发布与多平台分发：social-auto-upload 深讲与同类简评

> 本章定位：内容做出来之后，怎么高效地铺到多个平台？这是「自动发布」环节的深讲章。我们以自动发布标杆 [[social-auto-upload]] 为主线，讲清它的能力边界、部署与登录态维护、已知的坑，再简评两个同类边缘工具。本文是**盘点视角**：完整安装与排错教程见既有笔记 [[social-auto-upload]]，本章不重复教程正文，只回答「它在全景里值不值得用、坑在哪、同类里怎么选」。

## 2.1 一句话定位与四维打分

在第 1 章拆出的五个环节里，自动发布负责把成品从本地搬到各平台账号上。social-auto-upload（仓库 `dreammis/social-auto-upload`）是这个环节的事实标杆：它不调用任何平台官方上传 API，而是用浏览器自动化**像真人一样登录并操作上传页**，把「逐个网页手工分发」固化成一条条 `sau` 命令。

沿用全文统一标尺做四维打分 [SAU-R](https://github.com/dreammis/social-auto-upload)：

| 维度 | 结论 | 说明 |
|---|---|---|
| 是否官方授权 | ❌ | 非开放平台 API，靠 patchright 驱动 Chromium + cookie 登录态模拟真人 |
| 是否标准开源协议 | ✅ MIT | 标准 OSI 协议，可商用（含闭源场景）；约 14.8k★ |
| 是否纯离线 | ✅ | 零云依赖：全部逻辑在本地 Python + chromium，不需要任何厂商 Key/Relay |
| 维护活跃度 | ✅ | 末提交 2026-09-02；2026-03 作者回归后进入密集重构，迭代快 |

[!tip] 大白话
把「官方授权 vs cookie 自动化」想成进商场两种方式：官方 API 是商场发的正规入场券（合规但门槛高）；social-auto-upload 是让一个替你干活的店员拿着你自己的会员卡去柜台办业务——卡是你本人的，但「店员代办」这件事商场未必允许。所以它能用，但存在违约风险（见本章风控 Callout）。

## 2.2 能力边界：能发什么、不能发什么

先看它能做什么，再看它**刻意不做什么**，边界比功能更重要。一张表看清 [SAU-R](https://github.com/dreammis/social-auto-upload)：

| 能力 | 覆盖范围 | 关键备注 |
|---|---|---|
| 视频上传 | 11 平台 | 抖音/B站/小红书/快手/视频号/百家号/支付宝生活号/微博/虎扑/YouTube/TikTok |
| 图文上传 | 仅抖音/小红书/快手 | 只有这 3 家支持 `upload-note`，其余平台找图文参数是浪费时间 |
| 定时发布 | README 矩阵列 6 平台 | 抖音/B站/小红书/快手/视频号/TikTok；CLI 实际可排期 **5 平台**（TikTok 尚未接入 CLI，见 2.5） |
| 多账号并发 | 每账号独立登录态 | 一个账号名 = 一个 cookie 文件，互不串号，可并行跑多条命令 |
| B站能力 | 封装自 biliup | B站上传内核复用 biliup，首次运行自动下载 |
| 数据看板 | ❌ 无 | 发完即走，不负责播放/涨粉复盘（那是第 6 章的事） |
| REST API | ❌ 无 | 不是常驻服务，是命令；供人/AI Agent 调用的进程入口 |

读这张表最该记住两条结论：**图文能力极稀缺，只有抖音/小红书/快手三行是 ✅**；**它只做「发」，不做「看」**——没有看板、没有 API，别拿它当运营管理平台。

## 2.3 定位真相：它是给 AI Agent 用的「发布通道」

为什么一个没有看板、没有 API 的工具会被当作标杆？因为它的设计定位根本不是「人类后台」，而是**供 AI Agent 调用的发布通道**：把「登录态维护好」之后，Agent 只需拼一条 `sau` 命令，就能把成品发到指定账号。仓库为此直接提供了抖音/小红书/快手/B站的 Skill，适配 Claude Code / OpenClaw / Codex 这类 Agent 环境 [SAU-R](https://github.com/dreammis/social-auto-upload)。

统一命令骨架只有一句话：

```bash
# 统一骨架：sau <平台> <动作> --account <账号名>
sau douyin upload-video --account demo \
  --file demo.mp4 --title "标题" --desc "描述"
```

对照第 5 章可知：AiToEarn 走的是「SaaS + 云 Relay」通道，而 social-auto-upload 走的是「本地 cookie」通道——正是这条差异，让它成了「纯离线 AI 生产 → 发布」组合里发布侧的首选（第 5 章细比）。

[!tip] 大白话
把 Agent 调 `sau` 想成你雇了个实习生：你把各平台的门禁卡（cookie 文件）都办好放在抽屉里，实习生只需要知道「拿哪张卡、去哪个平台、交哪份材料」（一条命令），就能替你跑腿。它不需要理解每个平台网页怎么点——那是 social-auto-upload 替它做的事。

## 2.4 部署与登录态维护（盘点视角，不重复教程）

部署主线一句话：**`uv` + patchright 驱动 Chromium**，Python 要求 `>=3.10,<3.13`。完整分步安装见 [[social-auto-upload]] 第 2 章，这里只给「先睹为快」的提醒片段 [SAU-I](https://github.com/dreammis/social-auto-upload/blob/main/docs/install.md)：

```bash
# 安装主线（完整教程见既有笔记 [[social-auto-upload]]，勿照抄第三方 pip+playwright 旧教程）
uv venv && uv pip install -e .          # 建环境 + 装依赖 + 注册 sau
patchright install chromium             # 下载浏览器内核；国内慢先设 PLAYWRIGHT_DOWNLOAD_HOST 镜像
cp conf.example.py conf.py              # 生成个人配置
```

登录态维护是这套工具最核心的日常操作，模型很固定：**一个 `account_name` = 一个账号文件**，落在 `cookies/[平台]/[平台]_[账号].json`。新平台首次用要人工登录一次，之后 `login` / `check` 就是唯一需要关心的命令：

```bash
# 首次登录（人工扫码或短信码）→ 之后发布前校验
sau douyin login --account demo     # 触发登录：抖音短信码写项目根目录 verify_code.txt（用完自动删除）
sau douyin check --account demo     # 校验登录态：出现登录 UI 即判失效
```

两个登录细节值得单独记：**抖音短信验证码**不是直接喂给命令，而是写进项目根目录 `verify_code.txt`，工具读到后自动提交并删除该文件；**B站建议本地扫码**完成登录，而不是短信。

[!tip] 大白话
把 `verify_code.txt` 想成递给门卫的一次性字条：你收到短信验证码后把它写在字条上塞进门缝，门卫看完当场撕掉（自动删除）。这个设计天生适合 Agent 场景——程序只负责「要码、写文件」，人只负责「看手机、报码」，登录就能自动化走完且不留残余。

[!warning] 文档口径提醒
README 与 install 文档对浏览器驱动的表述**互相矛盾**：README 的「重构计划」把 patchright 写成待更换项，install 文档却把 patchright 当作当前主线。实践判定：`sau` CLI + uv + patchright 即当前主线，一切以最新代码 + [docs/install.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/install.md) 为准；看到第三方教程教你 `pip install playwright` 或强依赖 `LOCAL_CHROME_PATH`，先默认它已过时（详见既有笔记 [[social-auto-upload]] 第 2.3 节）。

## 2.5 已知的坑与能力缺口

工具不是没有代价。盘点视角下最值得知道的三个坑 + 一个缺口：

| # | 坑 / 缺口 | 影响 | 应对 |
|---|---|---|---|
| 1 | **登录态人工维护，无自动失效刷新** | cookie 过期后不会自愈，命令会「发到一半才发现失效」 | 养成发布前 `check` 的习惯；失效就重登一次，把登录态固化进文件后再无头跑 |
| 2 | **README 与 install 对 patchright 表述矛盾** | 只读 README 的用户会以为驱动要换，部署时被旧教程带偏 | 认准 install 文档 + 最新代码；见 2.4 的文档口径提醒 |
| 3 | **无数据看板、无 REST API** | 发完即走：看不到发布结果数据，也无法作为常驻服务被业务系统调用 | 接受它「发布通道」的定位；要复盘数据走第 6 章合规路径 |
| 4 | 平台改版致元素失效、headless 登录被风控 | login/check 卡住、超时或误判（真实案例见 GitHub Issues #224/#230） | 先 `git pull` 升最新代码再排查；高风控场景复用真实浏览器登录态——完整排错表见 [[social-auto-upload]] 第 6 章 |

缺口 3 是最容易被低估的：很多人以为装了它就有「多平台运营后台」，实际上它连「这条视频发出去有没有播放」都不负责。它的边界就是「发出去」，发出去之后的事请交给第 6、7 章的数据工具。

[!tip] 大白话
把「登录态无自动刷新」想成门禁卡到期不提醒：卡还能用时一切正常，某天突然刷不开门你才知道到期了。所以靠谱的做法不是等它失效，而是每次出门前先刷一下闸机（`check`）——确认卡还能用再办事。

## 2.6 同类简评：可视化面板与衍生分支

自动发布方向并非只有它一个。第 1 章列的 4 个边缘候选里，有两个与它同属发布环节，都进不了正章，这里一并简评（据深度研究 §3.9）：

| 工具 | 定位 | 与 social-auto-upload 的差异 | 一句话结论 |
|---|---|---|---|
| **MediaPublishPlatform** | Flask + Vue3 + Playwright 的**可视化**批量/定时发布面板，约 9 平台 | 有 Web 界面，不要求命令行；但约 153★、star 少 | 想要可视化后台可试，但需自测稳定性，别当生产级依赖 |
| **omnipost** | social-auto-upload 的**衍生分支**，另加头条/搜狐/知乎 | 在别人地基上盖楼；仅 1 commit | 增量太小、质量依赖上游，除非正好缺那 3 个平台否则不推荐 |

选型含义很清楚：如果你能接受命令行/Agent 调用，social-auto-upload 是发布侧更稳的选择；如果你「非要可视化界面不可」，MediaPublishPlatform 是唯一可试的同类，但要对它的成熟度有心理准备。

## 2.7 与既有笔记的关系及风险提示

本节收口两点。

**与既有笔记的分工**：[[social-auto-upload]] 是「配置与使用指南」——零基础上手、逐条命令、完整排错，解决「怎么装怎么用」；本章是「盘点评估」——解决「在全景里它值不值得选、坑在哪、同类里怎么比」。两者互链，阅读时教程细节请跳转既有笔记，本文不再展开。

**风险定级**：按第 1 章的三层框架，social-auto-upload 属**第二层风险**——发的是自家账号的自家内容，不是爬取他人数据，但「cookie + 浏览器自动化」本身已踩平台用户协议里「禁止第三方自动化工具接入」的条款。

[!warning] 风控与合规提示
用 cookie/自动化方式发布，无论发的是不是自己的内容，都可能违反抖音/小红书等平台的用户协议：平台明令禁止自动化程序或第三方工具批量接入，违规轻则限流、重则封号。social-auto-upload 属第二层风险（自账号、自内容，风险中等），但一旦升级为「矩阵批量发布」「搬运他人内容」或「刷量」用途，就跨入第三层高风险，还叠加不正当竞争与版权风险。自动化发布前请先评估账号价值与合规底线，完整红线与判例见第 8 章。

## 本章小结

- social-auto-upload 是自动发布环节标杆：四维打分「非官方授权 + MIT 可商用 + 纯离线 + 高活跃」，赢在生态完整与零云依赖。
- 能力边界：视频 11 平台、图文仅抖音/小红书/快手、定时发布 CLI 实际覆盖 5 平台；**没有数据看板、没有 REST API**，定位是供 AI Agent 调用的发布通道（Claude Code / OpenClaw / Codex）。
- 部署主线 = `uv` + patchright + Python `>=3.10,<3.13`；登录态模型是「一个账号名 = 一个 cookie 文件」，日常靠 `login` / `check` 维护；抖音短信码走 `verify_code.txt`。
- 三个坑要认清：登录态人工维护无自动失效刷新、README 与 install 对 patchright 表述矛盾、无看板无 API 导致「只发不看」。
- 同类简评：MediaPublishPlatform（可视化面板、star 少需自测）、omnipost（仅 1 commit 的衍生分支）；发布侧首选仍是 social-auto-upload。
- 与既有笔记 [[social-auto-upload]] 分工：那边讲教程、本章讲评估；cookie 自动化发布属第二层风控风险，升级用途即跨入第三层，详见第 8 章。

下一章转向内容生产的另一半：既然发布通道已经铺好，就该问「发什么」。第 3 章讲 AI 文字一键成片 MoneyPrinterTurbo——如何把一句主题词变成一条可直接发布的成片，与本章的发布通道正好前后衔接。
