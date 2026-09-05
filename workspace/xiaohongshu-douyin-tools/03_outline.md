## 学习笔记大纲：《经营小红书和抖音的开源项目与工具盘点》

> 笔记类型：对比/选型盘点笔记（方向 A：全景盘点）
> 预计总篇幅：中长篇（8 章，正文合计约 24-30 页）
> 章节数：8
> 素材基准：`02_deep_research.md`（源 ID 与 §小节编号沿用该文件）

---

### 第一章：总览 —— 经营场景拆解与开源工具全景地图
- **篇幅**：短
- **覆盖要点**：
  - 把「经营小红书/抖音」拆成可工具化的五个环节：自动发布 / 内容生产 / 一体化编排 / 数据运营 / 合规选型
  - 候选工具清单：7 核心（social-auto-upload、AiToEarn、MoneyPrinterTurbo、FunClip、MediaCrawler、CreatorHub、xhs_douyin_content）+ 4 边缘（MediaPublishPlatform、ShortGPT、Visual_MediaCrawler、omnipost）+ 2 显性缺口（官方数据分析能力、合规/风控边界）
  - 全文选型统一使用四维打分：是否官方授权 / 是否标准开源协议 / 是否纯离线 / 维护活跃度
  - 阅读导览：每章对应哪类经营场景，风险分级预览
- **素材引用**：§1、§2、§3、§5、§6
- **代码示例**：无

### 第二章：自动发布与多平台分发 —— social-auto-upload 深讲与同类简评
- **篇幅**：长
- **覆盖要点**：
  - social-auto-upload 定位：11 平台视频上传、图文仅抖音/小红书/快手、定时发布覆盖抖音/B站/小红书/快手/视频号/TikTok、多账号并发；作为 AI Agent 发布通道（Claude Code / OpenClaw / Codex）
  - 部署与登录态管理：`uv` + patchright 驱动 Chromium；每账号一个 cookie 文件；`sau <平台> login/check` 校验；抖音短信验证码落 `verify_code.txt`、B站建议本地扫码
  - 已知坑：无自动失效刷新机制、登录态需人工维护；README 与 install 文档对 patchright 表述不一致
  - 能力边界：无数据看板、无 REST API（仅发布通道）
  - 同类简评：MediaPublishPlatform（可视化批量/定时发布，star 少需自测）、omnipost（衍生分支 +头条/搜狐/知乎，仅 1 commit）
  - 与既有笔记 [[social-auto-upload]] 的关系：引用其配置教程结论，不重复教程正文
- **素材引用**：SAU-R、SAU-I、§3.1、§3.9、§5（矛盾 1）、§6
- **代码示例**：有 —— `sau` CLI 环境搭建、`uv`+patchright 安装、login/check 与定时发布配置片段

### 第三章：AI 内容生产（一）—— MoneyPrinterTurbo 文字一键成片
- **篇幅**：中
- **覆盖要点**：
  - 工作链路：主题/关键词 → 文案 → 配音 → 字幕 → 素材 → 剪辑全自动；输出 9:16 / 16:9 / 1:1
  - 四种用法：Agent / WebUI / API / CLI
  - 依赖配置边界：Python≥3.11、GPU 非必需（仅本地 whisper 字幕推荐）；LLM 可选 Kimi/OpenAI/Claude/Gemini/DeepSeek/Qwen/火山 Ark/MiniMax/OpenRouter/Ollama；TTS 默认免费 Edge TTS；素材源 Pexels/Pixabay/Coverr；文生视频 MiniMax H3/Seedance
  - 维护状态：~120.7k★、v1.3.6（2026-09-02）、提交活跃
- **素材引用**：MPT-R、§3.3
- **代码示例**：有 —— docker compose 起服务（含 .gpu 版）、WebUI/API 调用、常用 LLM/TTS/素材源环境变量

### 第四章：AI 内容生产（二）—— FunClip 本地智能剪辑与 ShortGPT 停更参考
- **篇幅**：短
- **覆盖要点**：
  - FunClip：基于 FunASR 的本地剪辑，ASR 后按文本/说话人切段；v2.2.1 内置 Pillow 字幕渲染；可选 LLM 剪辑（TwelveLabs Pegasus）
  - 资源边界：基础功能仅需 Python，Whisper 时间戳需大显存；模型权重授权独立于源码 MIT
  - ShortGPT：AI 短视频自动化框架但已停更（2025-02 后无提交，约 19 个月），仅作历史/架构参考
  - 素材管理：指出开源空白，衔接 AiToEarn 的 Create Agent 与商业素材方案
- **素材引用**：FC-R、SG-R、§3.4、§3.5
- **代码示例**：有 —— pip 安装与 `python funclip/launch.py` 启动 Gradio

### 第五章：一体化平台 —— AiToEarn 与「AI 生产 → 发布」组合方案对比
- **篇幅**：中
- **覆盖要点**：
  - AiToEarn 定位：AI 内容营销一体化（OPC），四大 Agent：Monetize（变现）/ Publish（排期分发）/ Engage（自动互动）/ Create（批量生成）；14 平台
  - 五种入口：Web SaaS、OpenClaw 插件、MCP/SSE、Docker compose 自部署（localhost:8080、免装 DB）、源码 Node 20.18.x
  - 云依赖边界（关键结论）：官方 API Key / Relay 硬依赖，环境不匹配即 401 → **自部署 ≠ 离线**；社交 OAuth 可走官方 Relay 借用凭据或自备平台开发者凭据
  - 对比选型：AiToEarn 一体开箱 vs「MoneyPrinterTurbo 生产 + social-auto-upload 发布」纯离线组合
- **素材引用**：ATE-R、§3.2、§5（矛盾 2）、§6、§7
- **代码示例**：有 —— docker compose 自部署与 .env 配置骨架（标注官方 Key/Relay 依赖项）

### 第六章：数据与运营（合规向）—— 官方开放平台 API 与自账号取数
- **篇幅**：中
- **覆盖要点**：
  - 抖音开放平台：授权后可取主页/指定视频近 30 天数据；门槛 = 粉丝≥1000、T+1 刷新、逐项申请（经营号默认授权）；无现成聚合需自行分页
  - 小红书数据现状：无个人/专业号批量导出 API；合规取数仅创作者中心导出 Excel、企业专业号后台导出 CSV；蒲公英数据 API 门槛高（品牌年消耗>500 万或白名单）
  - xhs_douyin_content：抓抖音/小红书创作者中心**自账号**每作品数据（播放/完播/点赞/分享/评论/收藏/主页访问/粉丝增量），扫码登录→pkl 缓存，输出 `data.xlsx`；GPL-3.0；合规风险相对最低，但创作者中心接口变动会失效
- **素材引用**：S1、S2、S6、S7、S9、X-R、§3.8、§4
- **代码示例**：有 —— xhs_douyin_content 扫码登录、运行与导出 Excel

### 第七章：数据与运营（研究/对标向）—— 采集器与互动管理
- **篇幅**：长
- **覆盖要点**：
  - MediaCrawler：数据采集事实标准，7 平台（小红书笔记、抖音/快手/B站视频、微博、贴吧、知乎）、关键词/指定 ID/二级评论/主页/IP 代理池/词云；Playwright CDP 复用用户 Chrome 登录态降风控、扫码+缓存；输出 CSV/JSON/JSONL/Excel/SQLite/MySQL；**自定义「非商业学习使用许可证 1.1」→ 仅学习研究、禁商用**；无 Docker
  - Visual_MediaCrawler：采集 + 展示一体，继承非商用许可，star 少（简评）
  - CreatorHub：本地多平台面板（抖音/小红书/快手/视频号），作品/评论/弹幕监控、断点续传、关键词采集仅抖音（小红书规划中）；自动评论/私信回复默认生成待审核草稿 + 阶梯冷却（403/429/461/471）；**license=null 未声明标准开源协议 + 自动互动踩线 → 慎用/仅参考**
  - 选型小结：研究/对标 vs 商用场景的法律分界（结合 §4 红线 2/3）
- **素材引用**：M-R、C-R、§3.6、§3.7、§3.9、§4、§5（矛盾 3）
- **代码示例**：有 —— MediaCrawler uv/pip 安装、CDP 扫码登录与采集运行；CreatorHub 冷却/保守模式配置

### 第八章：合规红线与选型矩阵 —— 怎么选、怎么用不踩线
- **篇幅**：中
- **覆盖要点**：
  - 风险分层框架（[!warning] Callout 统一出口）：
    - 第一层·官方授权渠道：抖音 OpenAPI / 创作者中心导出 → 低风险
    - 第二层·自账号 cookie/Playwright 取数（xhs_douyin_content 类）→ 自家数据违约风险中等
    - 第三层·爬他人公开数据 / 自动化发布 / 刷量互动（MediaCrawler 商用、AiToEarn Engage、CreatorHub 自动互动类）→ 违平台条款 + 个保法 / 反不正当竞争法高风险
  - 平台条款红线：抖音用户协议禁爬虫/第三方自动化接入、开放平台公约禁造假与批量虚拟账号、矩阵号治理规则（2023-12-01）；小红书 2026-06 治理公告禁自动化批量同质内容与刷量、蒲公英门槛
  - 司法判例提示：最高法数据权益指导案例（实质性替代可判赔）、抖音诉轻抖刷量案（判赔 400 万）
  - 选型矩阵：场景 × 工具 × 开源协议 × 部署成本 × 风控等级（表格）
  - 推荐组合：合规发布路径、纯离线 AI 生产路径、合规数据路径三条落地建议
- **素材引用**：S3、S4、S5、S8、S10、S11、§4、§5、§6
- **代码示例**：无（以矩阵表格 + Callout 为主）

---

## 学习路径说明

### 前置要求
- 会用 Docker / docker compose 或命令行跑 Python（uv/pip）项目
- 对小红书/抖音平台后台（创作者中心、专业号）有基本操作经验
- 了解「cookie 登录态」「浏览器自动化」的基本概念即可，不需精通
- 认同合规前提：先分清「官方授权」与「自建 cookie/爬虫」的风险差异再选型

### 学完能做什么
- 能按经营场景从全景清单中挑出候选工具，并用「授权 / 协议 / 离线 / 活跃度」四维快速打分
- 能自部署一套「AI 成片（MoneyPrinterTurbo）+ 多平台发布（social-auto-upload）」的纯离线内容流水线
- 能为自账号搭起合规的数据复盘路径（抖音 OpenAPI / 创作者中心导出 / xhs_douyin_content），知道何时可用 MediaCrawler 做研究性采集
- 能避开三个典型坑：登录态失效需人工维护、自部署 ≠ 离线（AiToEarn 云依赖）、无标准开源协议与自动互动工具的商用/风控风险

### 建议学习顺序
- 第一章 → 建立全景与选型标尺（约 15 分钟）
- 第二、三、四章 → 按「先发布、再生产」或「先生产、再发布」皆可，建议先读第二章自动发布（约 1 小时）
- 第五章 → 在看懂单品后对比一体化方案（约 30 分钟）
- 第六、七章 → 数据运营，注意第六章是合规底座、第七章是研究/对标扩展（约 1 小时）
- 第八章 → 最后读，作为全书红线总结与选型收口（约 30 分钟）
- 每章可独立查阅；若只想要一套能跑的最小组合，按「二 + 三 + 六」阅读即可

---

## 写作注意事项（meta，供 chapter-writer）

- **语气分层**：素材分「官方文档 / 官方规则 / 社区 GitHub / 第三方博客 / 法律判例」多层信源，写作时保留 tier 语气差异（官方禁令类用规则表述，社区项目注明维护者视角）。
- **待核实/开放问题**：写作时以「?」或脚注标注，不当作定论 —— AiToEarn 开源版与云端版功能裁剪边界及模型清单未核；social-auto-upload 最低 Python 版本与 Docker 用法未从 pyproject/Dockerfile 核实；CreatorHub 小红书关键词采集仍在规划中；FunClip 无官方 CPU/显存硬指标；小红书《用户协议》具体禁爬虫条号未取得一手原文。
- **合规措辞**：凡涉及 cookie/Playwright/自动互动的工具，一律配 [!warning] 风控提示 Callout；不把「爬他人数据」写进推荐，只标「学习研究」。
- **双链**：与既有笔记 [[social-auto-upload]] 互链，正文不重复其配置教程。
