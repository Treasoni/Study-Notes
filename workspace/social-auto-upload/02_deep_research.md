# social-auto-upload 深度研究素材（P2）

> 主题：如何配置使用 social-auto-upload（dreammis/social-auto-upload）
> 阶段：P2 深度收集 · 方向 D（全流程综合）
> 日期：2026-09-05
> 用途：供 outline-generator / chapter-writer 直接引用，无需回读原始源

---

## 0. 源清单与可信度

| # | 源 | 类型 | 关键内容 | 滞后/注意 |
|---|-----|------|---------|-----------|
| S1 | GitHub README（缓存 04） | Tier1 官方 | 平台矩阵、CLI 快速开始、重构说明、YouTube/代理机制 | 作者自述「详细文档已落后于重构」 |
| S2 | docs/install.md（缓存 03） | Tier1 官方 | uv 安装主线、conf.py、各平台 login/check/upload、短信验证码 | 当前推荐主线 |
| S3 | conf.example.py（缓存 02） | Tier1 官方 | 6 个顶层配置键 | 极精简，无 DB/日志/cookie 路径键 |
| S4 | pyproject.toml（缓存 01） | Tier1 官方 | Python 3.10–3.12、依赖、sau 入口 | — |
| S5 | docs/CLI.md（缓存 02_raw…实为 CLI.md） | Tier1 官方 | CLI 参数语义、--schedule 定时支持矩阵、平台限制 | — |
| S6 | DeepWiki Auth & Cookie | Tier2 社区镜像 | cookie 存储布局、check 失效信号、CDP 9222 导出 | 内容基于旧 Playwright 布局，需与 install.md 交叉印证 |
| S7 | GitHub Issues 检索 | Tier3 真实运维 | #224/#230/#252/#226/#210/#283 等真实坑 | 多数 Open，部分 PR 未确认合并 |
| S8 | CSDN Linux 部署排错 | Tier3 实操 | Chromium 镜像、ensurepip、f-string、LOCAL_CHROME_PATH | 建议 Python3.8 与现主线冲突，仅取通用坑 |

---

## 1. 项目是什么（面向笔记开头/总览章）

- **定位**：把「AI agent 每次临时解析网页做多平台分发」的高频重复劳动，固化成 Python 脚本 + 浏览器自动化的自动上传工具，支持视频/图文上传与定时发布。
- **现状**：约 14.8k star / 2.5k fork / MIT；2026-03 作者宣布回归并做大重构：统一 **CLI（`sau`）+ skills**、驱动从 playwright 迁移到 **patchright**、主线优先 **headless**。
- **当前权威口径 = README（S1）+ install.md（S2）+ CLI.md（S5）**。官方外部文档站 sap-doc.nasdaddy.com 内容可能滞后于 CLI 重构，引用需交叉核对。
- **旧 Web 版**（Flask+Vue）已保留在 `docs/legacy-web.md`，非当前主线、不保证可运行；`requirements.txt` 仅历史兼容。

---

## 2. 环境要求与安装（快速上手章 A 的核心）

### 2.1 环境硬性要求
- **Python**: `>=3.10,<3.13`（3.10/3.11/3.12 可用；**3.13 不可用**，见 S4）。
- **包管理**: 官方推荐 `uv`；主线依赖用 `uv pip install -e .`（S2/S4）。
- **浏览器驱动**: 需执行 `patchright install chromium`；国内加速设 `PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright"`。注意：环境变量名仍带 `PLAYWRIGHT_` 前缀（patchright 兼容 playwright 下载设施），照原样使用即可。
- **biliup**: 不需手动装，首次运行自动下载并自动查上游更新（可配 gh-proxy 加速）。
- 系统：Windows/Linux/macOS 均覆盖；教程命令分 PowerShell 与 bash 两种写法。

### 2.2 安装命令（当前推荐主线，S2 1-6 节）
```bash
git clone https://github.com/dreammis/social-auto-upload.git
cd social-auto-upload
# 虚拟环境
uv venv
# Windows PowerShell: .venv\Scripts\activate   /  Linux·macOS: source .venv/bin/activate
uv pip install -e .          # 注册 sau 命令
# patchright Chromium（国内先设镜像）
# PowerShell: $env:PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright"; patchright install chromium
# bash: PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright" patchright install chromium
cp conf.example.py conf.py   # 生成个人配置
sau --help                   # 验证
```

### 2.3 新旧安装路径差异（笔记要写清，避免读者走错）
| 维度 | 新主线（推荐） | 旧路径（历史） |
|------|---------------|---------------|
| 依赖 | pyproject.toml + `uv pip install -e .` | requirements.txt + pip |
| 浏览器驱动 | patchright + `patchright install chromium` | playwright |
| Chrome | 默认 patchright chromium | 依赖 `LOCAL_CHROME_PATH` 指向本机 Chrome |
| 入口 | `sau` CLI | Web 版 / examples |

---

## 3. conf.py 配置详解（配置章 B 的核心）

conf.example.py 仅 6 个顶层键（S3）：

| 配置键 | 默认 | 含义 | 备注 |
|--------|------|------|------|
| `BASE_DIR` | `Path(__file__).parent.resolve()` | 项目根基准，自动解析 | 不硬编码路径 |
| `XHS_SERVER` | `"http://127.0.0.1:11901"` | **仅小红书旧流程用** | 新 CLI 主线不用 |
| `LOCAL_CHROME_PATH` | `""` | 可选，复用本机 Chrome | 如 `C:/Program Files/Google/Chrome/Application/chrome.exe`；留空用 patchright chromium |
| `LOCAL_CHROME_HEADLESS` | `True` | 默认无头 | 登录被风控时可临时 False |
| `DEBUG_MODE` | `True` | 调试开关 | 服务器无头排错建议与 HEADLESS 搭配 |
| `YT_PROXY` | `None` | **仅 YouTube** 代理 | 如 `"http://127.0.0.1:7890"`；chromium 不吃系统代理 |

**边界提醒**：官方 conf.example.py **没有** DB/日志/各平台 cookie 路径键。账号模型是「一个 `account_name` = 一个账号文件」，cookie 落在 `cookies/[平台名]/{platform}_{account}.json`（S6，但以 `sau --help`/实测为准）。不要臆造 conf 键名。

---

## 4. 平台能力矩阵与 CLI 命令（能力章 + 发布命令）

### 4.1 平台能力总表（以 S1 README 矩阵为准）
| 平台 | CLI 前缀 | 视频 | 图文 | 定时发布 | CLI 接入 | 说明 |
|------|---------|:--:|:--:|:--:|:--:|------|
| 抖音 | `douyin` | ✅ | ✅ | ✅ | ✅ | 主线最完整；图文支持 BGM/notef |
| Bilibili | `bilibili` | ✅ | ❌ | ✅ | ✅ | 自动下载 biliup；`--tid` 分区必填(示例249) |
| 小红书 | `xiaohongshu` | ✅ | ✅ | ✅ | ✅ | 浏览器版；旧流程需 XHS_SERVER |
| 快手 | `kuaishou` | ✅ | ✅ | ✅ | ✅ | — |
| 视频号 | `tencent` | ✅ | ❌ | ✅ | ✅ | `--collection`/`--draft` |
| 百家号 | `baijiahao` | ✅ | ❌ | ❌ | ✅ | `--collection` |
| 支付宝生活号 | `alipay` | ✅ | ❌ | ❌ | ✅ | 需开通生活号创作 |
| 微博 | `weibo` | ✅ | ❌ | ❌ | ✅ | 标题≤30字 |
| 虎扑 | `hupu` | ✅ | ❌ | ❌ | ✅ | 标题4–40字 |
| YouTube | `youtube` | ✅ | ❌ | ❌ | ✅ | 浏览器自动化 Studio；`--playlist`/`--visibility`；被墙需 YT_PROXY |
| TikTok | （无 CLI） | ✅ | ❌ | ✅(矩阵) | ❌ | 走历史 Chrome example，非 CLI |

> 注意行文矛盾（S1 内部）：快速开始段「已接入 CLI」句未列 YouTube，但同段给了 `sau youtube` 示例、CLI.md 也含 youtube → 判定 **YouTube 实际有 CLI**，README 行文漏写（推断）。
> TikTok 定时发布✅但无 CLI → 与 CLI.md `--schedule` 支持表（不含 TikTok）存在张力，成稿建议写「矩阵列为支持，但当前 CLI 未接入」。

### 4.2 CLI 命令语义
- 结构：`sau <platform> <action> --account <account_name> [参数]`；`--account` 为通用必选，一个 name 对应一个账号文件，可多账号并发。
- 子命令：`login`（准备登录态）→ `check`（校验登录态）→ `upload-video` / `upload-note`（发布）。
- 运行参数：`--headless`（默认）/`--headed`/`--debug`。

### 4.3 发布参数
- 视频通用：`--file --title --desc [--tags 'a,b' --thumbnail*]`；元数据约定视频=title+desc+tags、图文=title+note+tags。
- 图文（仅 douyin/kuaishou/xhs）：`upload-note --images a.png b.png --title "…" --note "…"`；抖音可 `--notef 文件`、`--bgm '音乐'`。
- 平台扩展：B站 `--tid`；YouTube `--playlist`/`--visibility`；视频号/百家号/支付宝 `--collection`、视频号 `--draft`；抖音 `--product-link/--product-title`。
- **定时发布**：参数为 `--schedule "2026-03-24 21:30"`（绝对时间，传了就切定时策略，不传立即发布）。CLI.md 支持表：抖音(视频+图文)/快手(视频+图文)/小红书(视频+图文)/B站(视频)/视频号(视频)；**不支持**：百家号/支付宝/微博/虎扑。作者背景：「基于第二天」时间计算是默认策略。

### 4.4 成功/失败判定
- **文档缺口**：README/install/CLI 均未说明命令输出格式、退出码或成功标志。上传成功与否需看 `sau_cli.py` 或实测。成稿应写「以 CLI 输出/实测为准」，不臆造 JSON 返回约定。

---

## 5. 登录 / Cookie / 平台风控机制（排错章 C 核心）

### 5.1 登录态怎么存与怎么判
- 存储：新主线 `cookies/[平台]/[平台]_[account].json`；登录态本质是 patchright/playwright 的 `storage_state` JSON（抖音导出脚本还带 localStorage）。
- `check` 判定：导航到平台上传/发布页，若出现登录 UI 即判失效。失效信号参考：抖音=出现「扫码登录」文字、快手=「机构服务」选择器、视频号=「微信小店」、小红书=「手机号/扫码登录」。⚠️ 该判定有竞态缺陷（见坑 #230）。
- **CDP 9222 逃生通道（抖音，高风控/服务器）**：VNC 打开真实浏览器登录 `creator.douyin.com` → `bash export_douyin_cookie.sh --account <name>` → `sau douyin check`。脚本原理：连 Remote Debugging Port 9222，`Network.getAllCookies` + JS 抽 localStorage，写成 uploader 兼容 JSON。
- 抖音短信验证码：项目根目录 `verify_code.txt` 喂验证码，验证后自动删除；agent 场景把二维码图片直接展示给用户扫。

### 5.2 真实坑速查表（S7，成稿标「案例」勿写成通用结论）
| 坑 | 影响 | 症状 | 状态/方案 |
|----|------|------|----------|
| headless 登录被识别 | 抖音/快手 | 扫码后「二维码异常」作废、超时 | #224 Open；CDP 复用真实 Chrome / headed 登录 |
| 创作者中心改版选择器失效 | 抖音 | login 等「扫码登录」/扫码后超时、check 误判 | #230 Open；PR#229 提议多级选择器回退+networkidle+200s |
| 登录判定竞态 | 抖音 | 有效 cookie 被判 invalid | #224/#230；改判 `sessionid` 类 cookie |
| 二维码 iframe 切 qrconnect | 视频号 | 「未获取到视频号登录二维码地址」 | #252 → PR#253（Closed）：识别 qrconnect + 相对路径转 data URL |
| 非 ASCII 路径读不了二维码 | Windows 部署 | OpenCV `imread` 静默失败 | PR#253：`np.fromfile+cv2.imdecode` |
| 海外登录被 ban | 小红书 | 「暂不支持海外用户登录」 | #226 → PR#233：creator 域名可配置(rednote.com) |
| B站投稿过于频繁 21566 | B站 | 冷却/重登无效 | #210 Open；疑 APP 端风控，未解决 |
| Google 登录风控 | TikTok/YouTube | 密码登录被拦/「浏览器不安全」 | #220 Open；建议真实浏览器复用登录态 |

### 5.3 部署环境坑（S8+CSDN，仅取通用坑）
| 坑 | 解决 |
|----|------|
| f-string 反斜杠 SyntaxError（Python<3.12） | 先赋值再进 f-string |
| venv ensurepip 缺失（Linux） | 装 `python3.x-venv` + distutils |
| pip 装 setuptools 卡住 | 先 `pip install --upgrade pip` |
| Chromium 下载 404/ECONNRESET | `PLAYWRIGHT_DOWNLOAD_HOST=npmmirror` 或手动下载解压 + `LOCAL_CHROME_PATH` |
| 无头行为不对 | `LOCAL_CHROME_HEADLESS=True` 且 `DEBUG_MODE=False` |
| YouTube 连不上（被墙） | `YT_PROXY` 显式代理 |

---

## 6. 矛盾与不确定（写稿必须处理）

1. **版本口径**：README/install 主线=uv+patchright+CLI；sap-doc 文档站与多数第三方教程=旧 pip+playwright+Web。笔记需明确「以 README 当前主线为准，旧教程仅作对照」。
2. **YouTube 是否 CLI**：README 行文矛盾，判定有 CLI（推断）。
3. **TikTok 定时发布**：矩阵✅但 CLI 未接入，实现路径存疑。
4. **CSDN 建议 Python3.8** 与现主线 `>=3.10` 冲突，判断该文针对旧 commit。
5. **deepwiki/PR 合并状态**：#229/#233 合入与否未确认；引用时写「提出/建议」。
6. **CLI 成功判定、`--tid` 是否仍必填**：文档未明，需实测。
7. **rednote / 各平台代理**：P2 官方源未见「rednote 大陆版」或「抖音代理项」；只确认 YT_PROXY。

---

## 7. 给下游的一句话导读

**安装**：Python 3.10–3.12 + `uv venv` + `uv pip install -e .` + `patchright install chromium`（国内 npmmirror 镜像）→ `cp conf.example.py conf.py`。
**配置**：conf.py 只需关心 `LOCAL_CHROME_PATH`（可选复本机 Chrome）、`LOCAL_CHROME_HEADLESS`、`DEBUG_MODE`；`YT_PROXY` 仅 YouTube 被墙用。
**跑通闭环**：`sau douyin login --account <name>` → `sau douyin check --account <name>` → `sau douyin upload-video --account <name> --file demo.mp4 --title "…" --desc "…"`；短信验证码写根目录 `verify_code.txt`。
**平台能力**：11 平台，其中 10 个（抖音/快手/小红书/B站/视频号/百家号/支付宝/微博/虎扑/YouTube）已接 CLI，TikTok 未接；图文仅抖音/快手/小红书；定时发布 CLI 支持抖音/快手/小红书/B站/视频号。
**排错心法**：登录被风控优先「复用真实浏览器登录态」（CDP 9222/headed），不要硬刚自动化；平台改版导致元素失效很常见，升到最新代码再看 Issues。
