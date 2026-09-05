# 第三章 AI 内容生产（一）：MoneyPrinterTurbo 文字一键成片

> 本章定位：内容生产环节的头号工具。第 1 章把经营拆成五个环节，「内容生产」是决定产能的一环——批量起号缺的不是创意，是把选题快速变成初稿的速度。MoneyPrinterTurbo 恰好补上这一环：给一句话，它把文案、配音、字幕、素材、剪辑整条流水线替你跑完，产出的成片可直接投喂第 2 章的发布通道。

## 3.1 一条流水线：从一句话到一条可发布成片

MoneyPrinterTurbo（`harry0703/MoneyPrinterTurbo`，MIT）约 120.7k★，v1.3.6（2026-09-02），提交活跃，是内容生产环节星标最高、维护最勤的项目 [MPT-R](https://github.com/harry0703/MoneyPrinterTurbo)。它把「文字一键成片」做成了全自动链路：

| 环节 | 做什么 | 默认谁来干 |
|---|---|---|
| 输入 | 只需一个主题或几个关键词 | 你 |
| 文案 | 扩写成口播脚本 + 画面关键词 | LLM |
| 配音 | 脚本转语音 | TTS（默认免费 Edge TTS） |
| 字幕 | 生成时间轴并渲染进画面 | edge 时间戳 / whisper 转写 |
| 素材 | 按关键词取画面片段 | Pexels / Pixabay / Coverr 在线素材 |
| 剪辑 | 拼接、转场、配乐、合成导出 | 本地 ffmpeg |
| 输出 | 一条带字幕的 mp4 | — |

输出画幅三档可选：**9:16 竖屏**（1080×1920，抖音 / 小红书信息流）、**16:9 横屏**（1920×1080，西瓜 / B 站向）、**1:1 方形**（1080×1080）。一次可生成多条（`video_count`）、文案段落数、字幕开关等都可调 [MPT-R]。

[!tip] 大白话
把 MoneyPrinterTurbo 想成一家「文字进、成片出」的内容中央厨房：主笔（LLM）写稿、主播（TTS）念稿、采买（素材源）找画面、剪辑师（ffmpeg）合成装盒。你不需要亲自掌勺，只要下订单时写清主题、选好规格（竖屏 / 横屏 / 方形），出锅后负责试吃把关。所以它的上手门槛很低，真正的功夫全在「下订单」和「验收」这两端。

## 3.2 四种用法：Agent / WebUI / API / CLI

官方明示四种使用方式，「既能快速上手，也能接入自动化流程」[MPT-R]：

| 用法 | 入口 | 适合谁 |
|---|---|---|
| Agent | 把官方 Skill 文档交给能读文档并操作终端的 AI Agent（如 Claude Code 类），一句话让它自动安装、配置、生成 | 不想手动配置；想把成片编进 Agent 工作流 |
| WebUI | http://127.0.0.1:8501（Streamlit 界面） | 第一次体验、单条生成、在界面里挑音色与参数 |
| API | http://127.0.0.1:8080/docs（FastAPI OpenAPI），`POST /api/v1/videos` | 程序批量调用、n8n 等编排、Agent 编程式调用 |
| CLI | `uv run python cli.py --video-subject "..."` | 无浏览器 / SSH 环境、批量清单（`--batch-file`，上限 100 条） |

Agent 用法的意义在于它把「成片能力」变成可编排的一环：AI Agent 写完选题后直接调本地 MPT 出片，再转给第 2 章的 social-auto-upload 发布通道，就是一套「选题 → 成片 → 发布」的串链雏形；第 5 章会拿它和一体化平台 AiToEarn 做整体对比。

## 3.3 部署与依赖边界：GPU 非必需，重点是 Python ≥ 3.11

部署门槛在同级工具里算低：

- **语言**：Python 3.11+；本地跑推荐用 `uv sync` 或 Windows 一键启动包 [MPT-R]。
- **硬件**：官方给的最低配置是 4 核 CPU / 4 GB 内存，**GPU 非必须**。若主要依赖云端 LLM、在线素材和默认 Edge TTS，CPU 与内存比 GPU 更重要；只有启用本地 whisper 字幕、批量生成等更重的本地链路时，GPU 才明显提速 [MPT-R]。
- **镜像**：官方推荐 `docker-compose.release.yml`，直接拉取 GHCR 预编译镜像 `ghcr.io/harry0703/moneyprinterturbo:latest`；WebUI 服务映射 127.0.0.1:8501，API 服务映射 127.0.0.1:8080。仓库同时提供 **.gpu 版**（`docker-compose.gpu.yml` + `Dockerfile.gpu`，本地构建，需本机 NVIDIA 驱动 + NVIDIA Container Toolkit），用于 GPU 跑 Whisper 字幕 [MPT-R]。

起服务：

```bash
# 方式一：拉 GHCR 预编译镜像（推荐，无需本地构建）
cd MoneyPrinterTurbo
cp config.example.toml config.toml     # 先复制出配置文件，填好 Key 再启动
docker compose -f docker-compose.release.yml up -d
# 随后打开 WebUI  http://127.0.0.1:8501
#        API 文档  http://127.0.0.1:8080/docs

# 方式二：需要 GPU 跑本地 Whisper 字幕时才本地构建 GPU 版
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build
```

字幕默认走 **edge**（用 TTS 时间戳生成，速度快、免 GPU）；只有要更准字幕时间轴时才切 **whisper**（本地 faster-whisper 转写，首次需下载模型）[MPT-R]。

[!tip] 大白话
把容器跑在自己机器上，想成「把中央厨房开在自己家」——但食材仍由第三方供应：文案要调云端 LLM，配音默认走微软 Edge TTS（在线、免费），素材从 Pexels 等在线图库拉取。真正离线的是本地 whisper 字幕与最后的 ffmpeg 合成。这再次印证第 1 章的提醒：**自部署 ≠ 离线**，这条生产链路是「自托管」，不是「断网可跑」。

## 3.4 可选服务清单与配置

整条链路除了剪辑，几乎每步都可换供应商，配置统一收敛在 `config.toml`（Docker 以卷挂载进容器；首次运行也会自动从 `config.example.toml` 生成）。常用可选服务：

| 类别 | 可选服务 | 要点 |
|---|---|---|
| LLM（文案） | Kimi / OpenAI / Claude / Gemini / DeepSeek / Qwen / 火山方舟 Ark / MiniMax / OpenRouter / Ollama | 决定文案质量的核心；Ollama 是唯一真·本地选项 |
| TTS（配音） | 默认 Edge TTS（免费免 Key）；扩展 Azure V2 / SiliconFlow / Gemini / MiMo / ElevenLabs 等 | 中文短视频默认 Edge TTS 音色通常够用 |
| 字幕 | edge（默认）/ whisper | whisper 首次从 Hugging Face 下模型：large-v3 约 3 GB，turbo 约 1.6 GB |
| 素材画面 | Pexels / Pixabay / Coverr | 各需注册免费 API Key；支持多 Key 逗号分隔轮换 |
| 文生视频 | MiniMax H3、火山方舟 Seedance 等（按片计费） | 素材库搜不到合适画面时用 AI 直接生成片段 |
| 背景乐 | 内置 `resource/songs` | README 声明部分默认曲目来自 YouTube，商用前应替换 |

`config.toml` 最小改法（只填你实际用到的段落）：

```toml
[app]
llm_provider = "deepseek"              # 文案引擎：moonshot/openai/anthropic/gemini/deepseek/qwen/.../ollama
subtitle_provider = "edge"             # edge = 免 GPU 时间轴字幕；whisper = 本地转写（见下方 [whisper]）
video_source = "pexels"                # 素材源：pexels / pixabay / coverr，或文生视频源

# 例：DeepSeek
deepseek_api_key = "sk-..."
deepseek_model_name = "deepseek-chat"

# 素材源 Key（可填多个做轮换）
pexels_api_keys = ["你的PexelsKey"]

# 仅当 subtitle_provider = "whisper" 时需要
[whisper]
model_size = "large-v3-turbo"          # 更省资源；追求精度可换 large-v3
device = "cuda"                        # 无 NVIDIA GPU 时改回 "cpu"
compute_type = "int8"
```

若你的前端页面需要跨域直连 API，才需设环境变量 `CORS_ALLOWED_ORIGINS`；curl / Postman / n8n 等服务端调用不受 CORS 限制 [MPT-R]。

## 3.5 一条命令/一次请求出片

先看一眼成片效果最直接的方式是 WebUI；要接入程序则用 API 或 CLI。字段清单以 `http://127.0.0.1:8080/docs` 的 OpenAPI 为准：

```bash
# API：提交一条竖屏视频任务，返回 task_id，再用 GET /api/v1/tasks/{task_id} 轮询结果
curl -X POST http://127.0.0.1:8080/api/v1/videos \
  -H "Content-Type: application/json" \
  -d '{"video_subject":"人工智能如何改变普通人的日常生活","video_aspect":"9:16","video_count":1}'

# CLI：等价命令；--batch-file tasks.json 可一次排队多条（上限 100 条）
uv run python cli.py --video-subject "人工智能如何改变普通人的日常生活" --video-aspect 9:16
```

## 3.6 质量与版权提醒：它产的是「初稿」，不是「成品」

三点必须心里有数：

1. **生成质量的天花板是 LLM**。文案写得像水稿，后面配音、素材再好也救不回来；选更强模型、写更具体的主题、多生成几条挑最优，比调剪辑参数更值钱。若为「纯离线」选 Ollama 本地模型，文案质量通常弱于头部云模型——这是「离线」与「质量」的取舍。
2. **素材版权要自己把关**。Pexels / Pixabay / Coverr 各有授权条款，商用前逐一核对（通常允许商用，但普遍禁止「转售素材本身」之类用法）；文生视频片段按次计费，适合补空镜而非全片铺量。
3. **平台治理风险在前方**。用工具批量产出的同质内容直接铺量，可能撞上平台「自动化批量同质内容」的治理红线，合规细则在第 8 章收口。建议定位是「MPT 出初稿，人工改调性」——标题、封面、开头三秒钩子、素材取舍仍要人把一遍再进发布通道。

[!warning] 版权与调性提示
项目自带的默认背景乐中部分来自 YouTube，官方 README 已声明「如侵权请删除」[MPT-R]，商用前务必替换为自有或正版授权音乐。素材库与 AI 生成片段同样需按各自授权条款商用。别把 AI 初稿未经人工调整就批量铺号——这既影响账号调性，也可能触碰平台对批量同质内容的治理红线（详见第 8 章）。

## 本章小结

- MoneyPrinterTurbo 把「主题 → 文案 → 配音 → 字幕 → 素材 → 剪辑 → 成片」做成全自动链路，输出 9:16 / 16:9 / 1:1 三档画幅，MIT 协议、约 120.7k★、维护活跃。
- 四种用法覆盖从体验到自动化：Agent（一句话交给 AI Agent 干）、WebUI（8501）、API（8080，`POST /api/v1/videos`）、CLI（`cli.py`）。
- 部署门槛低：Python ≥ 3.11，GPU 非必需——只有本地 whisper 字幕/大批量处理才需要；Docker 直接拉 `ghcr.io/harry0703/moneyprinterturbo:latest`，.gpu 版需本地构建。
- 所有第三方服务（LLM / TTS / 素材 / 文生视频）在 `config.toml` 一处配置；默认 Edge TTS 免费免 Key。自托管但非离线，Ollama 是唯一本地 LLM 选项。
- 它擅长「批量出初稿」，不擅长「精」。素材与默认 BGM 的版权、AI 文案的调性都要人工把关后再发布。

下一章进入内容生产的另一半：当一条片子需要「人为精细控制」——按句子、按说话人切段、本地重剪时，MoneyPrinterTurbo 帮不上忙，轮到 FunClip（并顺带看一眼已停更的 ShortGPT 能留给我们什么架构参考）。
