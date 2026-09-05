# 02 - 深度研究（P2 Deep Research）

> run_id: `xiaohongshu-douyin-tools` ｜ learning-note-flow P2
> 方向：A 全景盘点（按场景组织：自动发布 / 内容生产 / 一体化 / 数据运营 / 合规与选型）
> 检索日期：2026-09-05
> 说明：本文件是下游大纲/写作的唯一素材交接，所有结论均带源 ID；「推」= 推断，与源区分。

---

## 1. Scope

覆盖 7 个核心候选 + 4 个边缘候选 + 2 个显性缺口（官方开放平台数据分析、合规/风控边界）：

- 核心：social-auto-upload、AiToEarn、MoneyPrinterTurbo、FunClip、MediaCrawler、CreatorHub、xhs_douyin_content
- 边缘：MediaPublishPlatform、ShortGPT（确认停更）、Visual_MediaCrawler、omnipost
- 缺口：抖音/小红书官方数据接口能力与自建分析路径；自动化发布/采集的协议与司法边界

---

## 2. 源表（Source Table）

| 源ID | 对象 | URL | 发布方 | 层级 | 日期/版本 |
|---|---|---|---|---|---|
| SAU-R | social-auto-upload README | github.com/dreammis/social-auto-upload | dreammis | 官方GitHub | 末提交 2026-09-02 |
| SAU-I | social-auto-upload install 文档 | github.com/dreammis/social-auto-upload (docs/install.md) | dreammis | 官方文档子页 | main |
| ATE-R | AiToEarn README | github.com/yikart/AiToEarn | yikart | 官方GitHub | v2.5.0 / 末提交 2026-08-15 |
| MPT-R | MoneyPrinterTurbo | github.com/harry0703/MoneyPrinterTurbo | harry0703 | 官方GitHub | v1.3.6 (2026-09-02), ~120.7k★ |
| FC-R | FunClip | github.com/modelscope/FunClip | ModelScope | 官方GitHub | v2.2.1 (2026-09-01), ~6.2k★ |
| SG-R | ShortGPT | github.com/RayVentura/ShortGPT | RayVentura | 官方GitHub | 最后 push 2025-02-10（停更） |
| M-R | MediaCrawler | github.com/NanmiCoder/MediaCrawler | NanmiCoder | 官方GitHub | ~64.4k★，语义版本 unknown |
| C-R | CreatorHub | github.com/3441293738/creatorhub | 3441293738 | 官方GitHub | ~1.9k★，license=null |
| X-R | xhs_douyin_content | github.com/cwjcw/xhs_douyin_content | cwjcw | 官方GitHub | ~303★，GPL-3.0 |
| S1 | 抖音开放平台-视频数据 | developer.open-douyin.com docs | 抖音开放平台 | 官方文档 | 近30天数据 |
| S2 | 抖音开放平台-能力申请 | developer.open-douyin.com capacity-center | 抖音开放平台 | 官方文档 | — |
| S3 | 抖音用户协议 | douyin.com/agreement | 抖音 | 官方规则 | 2026-02-20 生效 |
| S4 | 抖音社区自律公约/矩阵号治理 | douyin.com/rule/main | 抖音 | 官方规则 | 矩阵号 2023-12-01 |
| S5 | 抖音开放平台公约 | developer.open-douyin.com/forum | 抖音开放平台 | 官方规则 | — |
| S6 | 小红书开放平台入口 | open.xiaohongshu.com | 小红书 | 官方文档 | 登录后能力未核 |
| S7 | 蒲公英数据 API 门槛（第三方综述） | xiao-ad.com/zx/1613.html | 第三方服务商 | 知名博客 | 2025 |
| S8 | 小红书治理公告（媒体转载） | finance.sina.com.cn | 小红书公告 | 官方规则（转载） | 2026-06-10 |
| S9 | 小红书数据合规路径综述 | jizhil.com/xhsdata/14587.html | 站长博客 | 知名博客 | — |
| S10 | 最高法数据权益指导性案例 | pkulaw.com/news/... | 最高人民法院 | 法律 | 2025-08 |
| S11 | 抖音诉轻抖（刷量）案 | iprchn.com/...NewsId=141019 | 法院/知产媒体 | 法律/判例 | 2023 终审 |

---

## 3. 工具 Claim / 源映射

### 3.1 social-auto-upload（自动发布标杆）★5 · MIT
- 11 平台视频上传；图文仅抖音/小红书/快手；定时发布覆盖抖音/B站/小红书/快手/视频号/TikTok；多账号并发；入口为 `sau` CLI + 抖音/小红书/快手/B站 Skill [SAU-R]
- 主推 `uv` + **patchright** 驱动 Chromium（README 措辞滞后，install 文档以 patchright 为主线）；每账号一个 cookie 账号文件，`sau <平台> login/check` 校验 [SAU-I][SAU-R §近况]
- 抖音短信验证读 `verify_code.txt`；B站建议本地扫码；**无自动失效刷新机制**（推：登录态需人工维护）[SAU-R/I]
- 2026-03 声明进入密集重构；~14.8k★；MIT 可商用（含闭源）；B站功能封装自 biliup [SAU-R]
- 无数据看板与 REST API；定位是供 AI Agent 调用的发布通道（Claude Code/OpenClaw/Codex）[SAU-R]
- 矛盾：README「重构计划」把 patchright 写成待更换，install 文档称当前主线用 patchright —— 措辞滞后 [SAU]

### 3.2 AiToEarn（AI 内容营销一体化）★4 · MIT
- OPC 定位，四大 Agent：Monetize（CPS/CPE/CPM 变现）、Publish（日历排期+一键分发）、Engage（浏览器插件自动互动/AI 回复/高意向评论挖掘）、Create（Grok/Veo/Seedance/Nano Banana 批量生成）[ATE-R]
- 14 平台（含抖音/小红书/快手/B站/视频号/公众号/TikTok/YT/FB/IG 等）[ATE-R]
- 5 种入口：Web SaaS、OpenClaw 插件、MCP/SSE（Claude/Cursor）、Docker compose 自部署（localhost:8080、免装 DB）、源码 Node 20.18.x [ATE-R]
- **官方 API Key 硬依赖**（环境不匹配即 401）；社交 OAuth 可走官方 Relay 借用官方凭据，否则自备各平台开发者凭据；AI 模型可自填各厂 Key 或经 Relay [ATE-R]
- 结论：即便 Docker 自部署也**强依赖官方 Relay/Key**，非纯离线；风险形态与自托管 cookie 类不同 [推]

### 3.3 MoneyPrinterTurbo（文字一键成片）★5 · MIT
- 主题/关键词 → 文案→配音→字幕→素材→剪辑全自动；输出 9:16(1080×1920)/16:9/1:1；Agent/WebUI/API/CLI 四用法 [MPT-R]
- **GPU 非必需**（仅本地 whisper 字幕推荐），Python≥3.11，Docker compose 镜像（含 .gpu 版）[MPT-R]
- LLM 支持 Kimi/OpenAI/Claude/Gemini/DeepSeek/Qwen/火山Ark/MiniMax/OpenRouter/Ollama；TTS 默认免费 Edge TTS；素材 Pexels/Pixabay/Coverr；文生视频 MiniMax H3/Seedance [MPT-R]
- v1.3.6 (2026-09-02)，末 push 2026-09-04，~120.7k★，维护活跃 [MPT]

### 3.4 FunClip（ASR 字幕驱动剪辑）★4 · MIT
- 基于 FunASR(Paraformer/SeACo/CAM++) 本地自动剪辑：ASR 后按文本/说话人切段；v2.2.1 起内置 Pillow 字幕渲染 [FC-R]
- pip 安装，`python funclip/launch.py` 起 Gradio；基础功能仅需 Python，Whisper 时间戳需大显存 [FC-R]
- 可选 LLM 剪辑（TwelveLabs Pegasus 结合画面+音频）[FC-R]
- v2.2.1 (2026-09-01)，~6.2k★，活跃；源码 MIT（模型权重各自授权）[FC-R]

### 3.5 ShortGPT（边缘/参考）★3 · MIT —— 停更
- AI 短视频自动化框架（YT/TikTok 向）；MIT；~7.9k★；**最后 push 2025-02-10**，约 19 个月无提交 → 判停更 [SG-R]

### 3.6 MediaCrawler（数据采集事实标准）★5 · 自定义非商用许可
- 7 平台（小红书笔记、抖音/快手/B站视频、微博、贴吧、知乎）+ 关键词搜索/指定ID/二级评论/指定主页/IP代理池/评论词云 [M-R]
- **自定义「非商业学习使用许可证 1.1」**：仅学习研究，禁商用/大规模爬虫 [M-R §LICENSE]
- Playwright 默认 CDP 连用户 Chrome 复用登录态降风控；扫码登录+缓存；uv/pip；需 Node≥16；无 Docker [M-R]
- 输出 CSV/JSON/JSONL/Excel/SQLite/MySQL；另有付费 MediaCrawlerPro [M-R]

### 3.7 CreatorHub（评论/私信/多账号面板）★4 · license=null
- 本地多平台面板：抖音/小红书/快手/视频号；同步作品/关注/粉丝/私信；视频号仅本账号 [C-R]
- 关键词采集仅抖音（小红书规划中）；作品/评论/弹幕监控、断点续传、抖音↔小红书转发 [C-R]
- 自动评论/回复、私信自动回复（关键词/排除词/模板/冷却，默认生成待审核草稿）[C-R]
- **GitHub API license=null，未声明标准开源协议** → 商用/分发受限（推）[C-R]
- Python3.10+，每账号独立 Chrome CDP Profile；默认 conservative 模式，403/429/461/471 阶梯冷却 [C-R]

### 3.8 xhs_douyin_content（自账号创作者中心数据）★4 · GPL-3.0
- 抓抖音/小红书**创作者中心自账号**每作品数据：播放/完播/点击/2s跳出/播放时长/点赞/分享/评论/收藏/主页访问/粉丝增量 [X-R]
- 依赖创作者中心登录态（扫码登录→pkl 缓存）；输出 `data.xlsx`/`yesterday.xlsx`；GPL-3.0 [X-R]
- 合规风险相对最低（自账号、自家数据），但创作者中心接口变动会致失效 [推]

### 3.9 边缘候选简况
- MediaPublishPlatform：MIT ~153★，Flask+Vue3+Playwright 可视化批量/定时发布 9 平台，star 少需自测 [P1]
- Visual_MediaCrawler：~69★，非商用许可（继承上游），采集+展示一体 [P1]
- omnipost：MIT ~46★，social-auto-upload 衍生（+头条/搜狐/知乎），仅 1 commit，质量依赖上游 [P1]

---

## 4. 合规与开放平台（Claim / 源映射）

- 抖音开放平台授权后可取**近30天**主页数据（赞/粉/评/分享/访问）与指定视频近30天数据；但仅限粉丝≥1000 账号、授权次日约十点刷新、无聚合需分页自算，且须遵守个保法 [S1]
- 普通抖音号能力需在控制台逐项申请；经营号（品牌/员工/合作号）默认授权 [S2]
- 抖音用户协议：禁爬虫/镜像（2.4）、禁自动化程序或第三方工具接入收集信息（5.1）、禁爬虫抓取/模拟下载盗取内容（5.3）[S3]
- 抖音开放平台公约：禁非正常手段造假数据、批量注册虚拟账号、未授权第三方工具 [S5]
- 抖音矩阵号治理规则（2023-12-01）[S4]
- 小红书：无个人/专业号自账号批量导出 API；合规取数仅创作者中心导出 Excel、企业专业号后台导出 CSV [S9]；蒲公英数据 API 门槛高（品牌近一年消耗>500万或白名单），个人/普通专业号无法接入 [S7]
- 小红书 2026-06-10 公告：禁刷量/伪造、禁自动化批量生产同质内容、禁干预搜索与 AI 问答，违者降权/封禁 [S8]
- 司法：最高法指导案例——数据分层保护，未获许可爬取并「实质性替代」平台服务可依反不正当竞争法判赔 [S10]；抖音诉轻抖——组织刷量干扰推荐算法构成不正当竞争，判赔 400 万 [S11]

**对选型的红线（推）**：
1. **官方授权渠道优先**：自账号官方取数（抖音 OpenAPI / 创作者中心导出）风险最低；爬他人公开数据涉及个保法与反法，不宜写进「推荐」而只作「学习研究」标注。
2. 抖音自动化发布/采集条款明令禁止，所有 cookie/Playwright 类工具都违约风险自担 → 笔记必须给「风控提示」callout。
3. 小红书无开放数据 API + 明令禁止自动化批量同质内容 → 工具盘点聚焦「官方后台导出 + 企业商业 API + 公开数据对标监测（商业）」。

---

## 5. 相互矛盾点 / 需注意

1. social-auto-upload README 与 install 文档关于 patchright 表述不一致（措辞滞后）[SAU]
2. AiToEarn 官方 Key/Relay 硬依赖 vs「自部署开源」印象 —— 自部署 ≠ 离线 [ATE-R]
3. MediaCrawler / CreatorHub 无标准 OSI 许可（自定义禁商用 / license=null）—— 商用场景下法律状态不明 [M-R][C-R]
4. 抖音官方 OpenAPI 存在但条件苛刻（≥1000粉/T+1/需审批），「官方数据分析工具」在实际中小账号场景仍近乎空白 [S1][S2][S12]

---

## 6. 实践指引（Practical Guidance）

- **发布通道首选** social-auto-upload（MIT、生态完整、零云依赖）；登录态人工维护；想可视化后台可试 MediaPublishPlatform。
- **想「AI 生产→发布」一体**：AiToEarn 开箱快但强依赖官方 Relay；偏好纯离线则自行组合 MoneyPrinterTurbo（生产）+ social-auto-upload（发布）。
- **剪辑提效**：FunClip 本地 ASR 按句/说话人切段；MoneyPrinterTurbo 负责批量「文字成片」。
- **数据**：合规优先 = 抖音官方 OpenAPI（≥1000粉）或 xhs_douyin_content（自账号创作者中心）；研究/对标 = MediaCrawler（仅学习、禁商用）；互动管理 = CreatorHub（无开源协议 + 自动互动踩线，慎用）。
- **选型红线**：是否官方授权 / 是否标准开源协议 / 是否纯离线 / 维护活跃度 四个维度打分。

---

## 7. 开放问题（Open Questions）

- AiToEarn 开源版与云端版功能裁剪边界、模型供应商完整清单未核（需 DOCKER_DEPLOYMENT_CN.md）[ATE]
- social-auto-upload 最低 Python 版本与 Docker 用法未从 pyproject.toml/Dockerfile 核实 [SAU]
- CreatorHub 小红书关键词采集仍在「规划中」，数据表结构未知 [C-R]
- FunClip 官方未给 CPU/显存硬指标 [FC-R]
- 小红书《用户协议/社区规范》禁爬虫/外挂具体条号未取得一手原文 [S9 gap]
- 抖音经营号（品牌/员工/合作号）能力范围与 scope 需登录后台核实 [S2]

---

## 8. 下游交接（Handoff to outline-generator）

建议章节骨架（≤3 级，方向 A）：
1. 总览：经营小红书/抖音的工具全景与选型维度（官方/开源/自部署/风控）
2. 自动发布与多平台分发：social-auto-upload 深讲 + MPP/omnipost 简评
3. AI 内容生产：MoneyPrinterTurbo（成片）、FunClip（剪辑）、ShortGPT（停更参考）；素材管理开源空白
4. 一体化平台：AiToEarn（能力/云依赖/边界）
5. 数据与运营：MediaCrawler（研究用）、xhs_douyin_content（自账号）、CreatorHub（互动管理）、开放平台数据路径
6. 合规与风控红线 + 选型矩阵（工具 × 协议 × 部署 × 风控 × 场景）

每章引用源 ID：见上文映射；写作时保留 source tier 语气（官方 vs 社区）。
