## 笔记概览

实战笔记（部署 + 跑通 + 配置），深度「快速上手」，读者定位为零基础～有了解的配置使用者。全文以「uv + patchright + `sau` CLI」当前主线为准，核心目标是让读者独立安装、配置并把第一条视频发布到抖音，再按需扩展到其余平台。

### 第 1 章 项目简介与能做什么

> 篇幅：短 ｜ 素材：§1(S1)、§4.1(S1)、§6.1(S1/S2) ｜ 代码：无 ｜ 表格：无

#### 1.1 项目定位与工作原理
- social-auto-upload 是什么：把「AI 人工逐个平台分发」的高频重复劳动，固化为 Python 脚本 + 浏览器自动化的多平台自动上传工具
- 核心能力：视频/图文上传、定时发布
- 运行架构关键点：基于 patchright 浏览器自动化 + Cookie 登录态，而非公开 API 直传
- 现状与代号：约 14.8k star / 2.5k fork / MIT；2026-03 作者回归后大重构，统一 CLI（`sau`）+ headless 主线

#### 1.2 支持平台一览与版本口径提醒
- 支持 11 个平台；其中 10 个已接入 CLI，TikTok 走历史 Chrome example（未接入 CLI）
- 版本口径提醒：以 README + docs/install.md + docs/CLI.md 当前主线为准；旧 Web 版（legacy-web）、requirements.txt 与多数第三方教程已滞后于 CLI 重构，仅作对照

### 第 2 章 环境要求与安装（新 CLI 主线）

> 篇幅：中 ｜ 素材：§2.1(S4)、§2.2(S2)、§2.3(S1/S2)、§6.4(S8) ｜ 代码：完整安装命令序列（PowerShell/bash 双写法） ｜ 表格：新旧安装路径差异表

#### 2.1 环境硬性要求
- Python `>=3.10,<3.13`（3.13 不可用）；包管理推荐 uv
- 浏览器驱动：patchright chromium（`patchright install chromium`）；国内加速设 `PLAYWRIGHT_DOWNLOAD_HOST=npmmirror` 镜像（变量名仍带 PLAYWRIGHT 前缀）
- biliup 无需手动装，首次运行自动下载；Windows/Linux/macOS 均覆盖

#### 2.2 安装步骤（uv 主线）
- 步骤序列：git clone → `uv venv` → 激活虚拟环境 → `uv pip install -e .`（注册 sau）→ `patchright install chromium` → `cp conf.example.py conf.py` → `sau --help` 验证
- 命令按 PowerShell / bash 双写法给出

#### 2.3 新旧安装路径差异（避免走错教程）
- 表格对照：依赖（pyproject+uv vs requirements+pip）、浏览器驱动（patchright vs playwright）、Chrome（默认 patchright chromium vs 依赖 LOCAL_CHROME_PATH）、入口（sau CLI vs Web 版/examples）
- 提醒：旧教程的 pip/playwright/强制 LOCAL_CHROME_PATH 用法已非当前主线

### 第 3 章 快速跑通：配置 conf.py 并发布第一条抖音视频

> 篇幅：长 ｜ 素材：§3(S3/S6)、§4.2(S5)、§4.3(S5)、§5.1(S6)、§7 ｜ 代码：conf.py 最小配置 + login/check/upload-video 全流程命令 ｜ 表格：conf.py 六个顶层键速查表

#### 3.1 conf.py 需要关心什么
- conf.example.py 仅 6 个顶层键：BASE_DIR、XHS_SERVER、LOCAL_CHROME_PATH、LOCAL_CHROME_HEADLESS、DEBUG_MODE、YT_PROXY；给出 6 键速查表（默认值 / 含义 / 何时改）
- 快速上手实际只需关注 3 个：LOCAL_CHROME_PATH（可选复用本机 Chrome）、LOCAL_CHROME_HEADLESS（登录被风控时临时设 False）、DEBUG_MODE
- 边界提醒：官方 conf 无 DB/日志/cookie 路径键；账号模型是「一个 account_name = 一个账号文件」，cookie 落在 `cookies/[平台]/[平台]_[account].json`；不要臆造 conf 键名

#### 3.2 发布第一条抖音（跑通闭环）
- 三步命令：`sau douyin login --account demo` → `sau douyin check --account demo` → `sau douyin upload-video --account demo --file demo.mp4 --title "…" --desc "…"`
- 预期行为：login 准备登录态、check 校验、upload 立即发布（不传 --schedule）；成功判定以 CLI 输出/实测为准

#### 3.3 登录验证的最小闭环
- 短信验证码：写入项目根目录 `verify_code.txt`，验证后自动删除
- 二维码/扫码场景：直接把二维码图片展示给用户扫
- headless 登录被风控时的临时对策（改 headed，机制详见第 5、6 章）

### 第 4 章 平台能力矩阵与 CLI 命令参考

> 篇幅：中 ｜ 素材：§4.1(S1)、§4.2(S5)、§4.3(S5)、§4.4(S1/S5)、§6.2/§6.3/§6.6 ｜ 代码：各平台上传/图文/定时命令示例 ｜ 表格：平台能力总表 + 定时发布支持矩阵

#### 4.1 平台能力总表（11 平台）
- 表格列：平台 / CLI 前缀 / 视频 / 图文 / 定时发布 / CLI 接入 / 说明（含 B站 --tid 必填示例、视频号 --collection/--draft、YouTube --playlist/--visibility 等注记）
- 行文矛盾处理：YouTube 判定实际有 CLI（README 漏写）；TikTok 定时在矩阵列支持但当前 CLI 未接入

#### 4.2 CLI 通用结构
- 结构：`sau <platform> <action> --account <account_name> [参数]`；--account 通用必选，一个 name 对应一个账号文件
- 子命令三件套：login → check → upload-video / upload-note
- 运行参数：--headless（默认）/ --headed / --debug；支持多账号并发

#### 4.3 发布参数速查
- 视频通用：--file --title --desc [--tags 'a,b']
- 图文（仅 douyin/kuaishou/xhs）：upload-note --images；抖音另支持 --notef、--bgm
- 平台扩展：B站 --tid；YouTube --playlist/--visibility；视频号/百家号/支付宝 --collection、视频号 --draft；抖音 --product-link/--product-title
- 定时发布：`--schedule "YYYY-MM-DD HH:MM"`（绝对时间，传了切定时策略、不传立即发布）；附 CLI 支持表（抖音/快手/小红书/B站/视频号支持；百家号/支付宝/微博/虎扑不支持）

#### 4.4 成功/失败判定缺口
- README/install/CLI 均未说明输出格式、退出码或成功标志；成稿提示「以 CLI 输出或实测为准」，不臆造返回约定

### 第 5 章 登录态与 Cookie 机制

> 篇幅：中 ｜ 素材：§5.1(S6)、§5.2(S7)、§3(S3)、§6.5/§6.7 ｜ 代码：export_douyin_cookie.sh 与 CDP 9222 流程命令 ｜ 表格：各平台 check 失效信号对照

#### 5.1 登录态存储与账号模型
- Cookie 落在 `cookies/[平台]/[平台]_[account].json`，本质是 patchright/playwright 的 storage_state JSON（抖音导出还带 localStorage）
- 与 conf.py「一个 account_name = 一个账号文件」的模型呼应

#### 5.2 check 怎么判失效
- 判定机制：导航到上传/发布页，出现登录 UI 即判失效
- 各平台失效信号对照（抖音「扫码登录」/ 快手「机构服务」/ 视频号「微信小店」/ 小红书「手机号/扫码登录」）—— 以最新代码为准
- 竞态缺陷提醒：有效 cookie 也可能被判 invalid（#224/#230）

#### 5.3 高风控逃生通道：CDP 9222 导出真实浏览器登录态（抖音）
- 场景：高风控/服务器无头登录失败
- 流程：VNC 开真实 Chrome 登录 creator.douyin.com → `bash export_douyin_cookie.sh --account <name>` → `sau douyin check`
- 原理：连接 Remote Debugging Port 9222，用 Network.getAllCookies + JS 抽 localStorage 写成兼容 JSON

#### 5.4 短信验证码与扫码
- verify_code.txt 喂码机制与自动删除行为
- 二维码直接展示给用户扫的 agent 场景
- 心法：登录被风控优先复用真实浏览器登录态，不要硬刚自动化

### 第 6 章 常见坑与排错

> 篇幅：长 ｜ 素材：§5.2(S7)、§5.3(S8)、§2.1(S2/S4)、§6.4(S8) ｜ 代码：少量修复命令片段（pip 升级 / 镜像下载 / 导出脚本） ｜ 表格：真实案例坑速查表 + 部署环境坑速查表

#### 6.1 排错心法（先定策略再动手）
- 登录被风控 → 优先复用真实浏览器登录态（CDP 9222 / headed），不要硬刚自动化
- 平台改版导致元素失效 → 先升到最新代码，再查 Issues/PR

#### 6.2 真实用户案例坑（GitHub Issues，标「案例」勿当通论）
- 表格逐行给出「坑 / 影响 / 症状 / 状态或方案」：
  - headless 登录被识别（抖音/快手 #224）
  - 创作者中心改版选择器失效 + 登录判定竞态（抖音 #230，PR#229 建议）
  - 视频号 qrconnect 二维码 iframe（#252，PR#253 已 Closed）
  - 非 ASCII 路径读不了二维码（Windows 部署）
  - 小红书海外登录被 ban（#226，PR#233 rednote 域名可配置）
  - B 站投稿过于频繁 21566（#210 Open）
  - Google 登录风控（TikTok/YouTube #220）

#### 6.3 部署环境坑（S8/CSDN，仅取通用项）
- 表格：f-string 反斜杠 SyntaxError（Python<3.12）、venv ensurepip 缺失、pip 装 setuptools 卡住、Chromium 下载 404/ECONNRESET（镜像或 LOCAL_CHROME_PATH）、无头行为不对（LOCAL_CHROME_HEADLESS + DEBUG_MODE 组合）、YouTube 连不上（YT_PROXY 显式代理）
- 提醒：CSDN 文建议 Python3.8 针对旧 commit，与现主线 >=3.10 冲突，勿照搬

### 第 7 章 结语：版本口径与下一步

> 篇幅：短 ｜ 素材：§0(S1/S2/S5)、§6.1–§6.7、§7 ｜ 代码：无 ｜ 表格：无

#### 7.1 版本口径与待实测清单
- 再次提醒：以 README + install.md + CLI.md 当前主线为准；sap-doc 文档站与第三方教程可能停留在旧 pip+playwright+Web 时代
- 存疑清单：YouTube 有 CLI（推断）、TikTok 定时未接入 CLI、--tid 是否仍必填、CLI 成功判定格式 —— 标注需实测/升最新代码确认

#### 7.2 下一步方向
- 多平台/多账号扩展、定时发布组合、无头服务器与 Docker 化部署、跟进上游 Issues/PR
- 进一步资源：GitHub README、docs/install.md、docs/CLI.md、GitHub Issues

## 写作顺序与依赖

- 章节依赖：1（概念铺垫）→ 2（安装，是 3 的前提）→ 3（抖音样例跑通「配置-登录-发布」闭环）→ 5（登录机制，解释第 3 章的登录行为并引出排错）→ 4（将单平台命令推广为全平台系统参考，可在 3 之后按需查阅）→ 6（依赖第 5 章机制知识）→ 7（收尾）。建议实际写作顺序为 1 → 2 → 3 → 5 → 4 → 6 → 7。
- 横向约束：第 2、3、6、7 章都需贯穿「以当前 CLI 主线为准、旧教程仅对照」的版本口径提醒，避免读者混用新旧安装路径与命令。
- 成稿口径约束：第 4 章 YouTube 有 CLI 与第 5 章 check 失效信号属推断/易变信息，需标「以最新代码/实测为准」；第 6 章 Issues 案例一律标「案例」，不写成通用结论。
