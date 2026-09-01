---
title: HKUDS DeepTutor —— Agent-Native 终身个性化学习工作区
tags:
  - obsidian/学习笔记
  - github项目
  - ai/agent
  - ai/rag
  - docker
created: 2026-09-01
updated: 2026-09-01
status: 完成
source_project: deeptutor
---

# HKUDS DeepTutor —— Agent-Native 终身个性化学习工作区

这份笔记把 HKUDS DeepTutor 从认识、部署、核心玩法、掌握度路径、进阶玩法、架构原理到排错速查完整串成一条学习路径，共 7 章。第 1 章先回答"它是什么、解决什么问题、为谁而做"；第 2 章用 Docker 一条命令把应用跑起来并接入模型；第 3 章上手建知识库、带引用问答、出题、可视化与深研；第 4 章进入掌握度路径（Mastery Path）与 Course Study；第 5 章进阶到 Living Book、Partners 与 Agent 驱动；第 6 章拆开引擎盖讲"为什么这么设计"；第 7 章收拢一张随用随查的避坑与排错速查表。笔记写作时以 v1.6.2 为锚，命令与配置项以官方文档为准。

## 目录

1. [DeepTutor 是什么 —— Agent-Native 终身个性化学习工作区](#DeepTutor-是什么--Agent-Native-终身个性化学习工作区)
2. [Docker 快速上手 —— 一条命令跑通 DeepTutor](#Docker-快速上手--一条命令跑通-DeepTutor)
3. [第 3 章 核心玩法 —— 建知识库、出题、可视化与深研](#第-3-章-核心玩法--建知识库出题可视化与深研)
4. [掌握度路径（Mastery Path）与 Course Study](#掌握度路径Mastery-Path与-Course-Study)
5. [进阶玩法 —— Living Book、Partners 与 Agent 驱动](#进阶玩法--Living-BookPartners-与-Agent-驱动)
6. [架构与原理 —— 它为什么这么设计](#架构与原理--它为什么这么设计)
7. [避坑与排错速查](#避坑与排错速查)

---

## DeepTutor 是什么 —— Agent-Native 终身个性化学习工作区

如果你已经用过 ChatGPT、DeepSeek 这类通用聊天助手，多半撞见过同一个尴尬：问一道题它能答，但答完就忘；你换个角度再问，它又从头讲一遍；它既不记得你上次学到哪儿，也不会主动甩几道题考考你。DeepTutor（HKUDS DeepTutor）正是冲着这个痛点来的。它不是又一个聊天框，而是一个"有记忆、有知识库、会主动辅导"的终身个性化学习工作区。本章先回答三个问题：它是什么、解决什么问题、为谁而做，给你搭一个整体认知框架。

### 1.1 一句话定位：运行时统一"辅导 / 解题 / 出题 / 研究 / 可视化 / 掌握度练习"

DeepTutor 对自己的定位是：**Agent-Native 终身个性化辅导学习工作区**，用一个统一运行时把"辅导、解题、出题、研究、可视化、掌握度练习"六类能力收在一起 [S1][S2]。拆开看三个关键词：

- **终身（Lifelong）**：不是一次性的问答工具，而是能长期陪着你学一个领域、一门课的学习伴侣，跨会话保持你的进度与偏好。
- **个性化（Personalized）**：回答和出题会结合你的知识库与学习档案，而不是给所有人同一套标准答案。
- **Agent-Native**：系统以 [[Agent|智能体]] 为原生形态工作——它会自己规划、调用工具、查阅资料，再给出结果，而不是只会"你问我答"。

> [!tip] 大白话
> 把 Agent-Native 想成一位"会主动动手的家教"，而不是一台"你按键它才出声的复读机"。家教看到你卡壳，会自己翻教材、画图、出题；复读机只会等你输入问题。所以 DeepTutor 的每个能力（辅导、解题、出题……）背后都是一个会"思考 → 查资料 → 行动"的智能体在干活。这正是它与普通聊天助手的本质区别，底层机制留到第 6 章展开。

### 1.2 它解决什么问题：知识碎片化、学习缺乏连续性、AI 工具过于被动

DeepTutor 的设计起点是三组被反复验证的学习痛点 [S5]：

**知识碎片化**。资料通常散落在 PDF、网页、笔记、视频里，学的时候东一榔头西一棒槌，用的时候找不到、对不上。普通 AI 随手给的是片段答案，且与你的资料毫无关联，反而加剧碎片化。

**学习缺乏连续性**。通用聊天助手没有"进度"概念。昨天学到第 5 章，今天再问它不知道；你在哪里卡过壳、哪些题做错过，它更不记得。学习因此变成一次次从零开始，而不是一层层往上垒。

**AI 工具过于被动**。多数 AI 工具只能等你提问。它不会在你学完一章后主动说"来做几道题检验一下"，也不会发现你反复混淆某个概念时提醒你回头补。工具是"被动应答"，而学习需要"主动引导"。

把三组痛点浓缩成一句话：**普通 AI 工具没有"上下文"**。DeepTutor 的整套设计——记忆、知识库、主动式智能体——都是在给 AI 补上学习所需的上下文，后续章节会看到这三支柱如何落地成具体功能。

### 1.3 功能全景：Chat、Ask Questions、Quiz、Research、Visualize、Solve、Course Study、Mastery Path、Immersive Reading/Watching 共享同一运行时与会话上下文

DeepTutor 的功能面不是一堆互相孤立的按钮，而是**九个能力共享同一个能力运行时与同一份会话上下文** [S1]：

| 能力 | 一句话说明 |
|------|-----------|
| Chat | 默认对话能力，也是所有能力的底座 |
| Ask Questions | 主动向你提问（追问、澄清、测试） |
| Quiz | 根据知识库生成习题 |
| Research | 多步检索与综合的"深研" |
| Visualize | 把概念画成图或动画 |
| Solve | 逐步解题 |
| Course Study | 绑定课程上下文的小班式学习 |
| Mastery Path | 掌握度路径，分级检验进度 |
| Immersive Reading/Watching | 沉浸式阅读与观看 |

"共享同一运行时与会话上下文"是本章最值得记住的一句话：你在 Chat 里讨论"微积分中值定理"，转到 Quiz 生成习题、再转 Visualize 画图，系统始终记得刚才聊的是同一个话题。能力之间是"同一次学习中的不同动作"，而不是九个独立的 App。这些功能的具体操作，会在第 3、4、5 章逐个上手。

> [!tip] 大白话
> 把"运行时与上下文"想成同一张书桌。你在书桌上读书、做题、画图、写笔记，桌上的书和笔记始终放着，不会因为你从"做题"换到"画图"就全部收走。DeepTutor 的九个能力，就是同一张书桌上的九种动作。

### 1.4 里程碑与版本现状：正式发布、star 增速、当前 v1.6.2

DeepTutor 由 HKUDS（港大数据科学实验室）开源，成长速度相当惊人 [S1]：

- **2025-12-29** 正式发布；
- 发布后 **39 天**突破 10k stars；
- **111 天**突破 20k stars；
- 截至研究素材抓取时（2026-08-31），仓库为 **v1.6.2**，约 **38.2k stars、4.8k forks** [S1][S6]。

它不只是工程热点，还有配套学术论文支撑：提出"混合个性化引擎"，把静态知识锚定与动态学习者记忆结合，并设计了 TutorBench 交互式评测基准 [S2]。论文细节与评测结论放到第 6 章讲。

> [!warning] 易错点
> 这个项目迭代极快——仅 2026 年 8 月就连发 v1.5.7 → v1.6.2 多个版本 [S1]。本笔记以写作时的 **v1.6.2** 为锚，你读到它时可能已有更新版本；具体命令与配置项请以官方文档与 GitHub README 为准，避免版本漂移。

### 1.5 适用场景与目标用户：自学者、学生、教师、研究者

从功能面看，DeepTutor 主要面向四类人：

**自学者**。上传教材建知识库 → 带引用问答 → 生成习题 → 走掌握度路径，形成"学—测—补"闭环。这是最典型的用法，也是本笔记第 2–4 章的主线。

**学生**。用 Course Study 做课程学习、用 Quiz 与 Mastery Path 检验掌握度，适合系统性啃一门课，而不只是零散问问题。

**教师**。用 Ask Questions / Quiz 出题、用知识库沉淀讲义；进阶玩法里还能把资料编译成交互式"活书"（Living Book）分享给学生 [S1]。

**研究者**。用 Research 做多步深研；学术视角上，论文中的 TutorBench 评测协议本身就是面向教学研究场景设计的 [S2]。

判断是否值得换用 DeepTutor 而不是普通聊天助手，关键看一点：**你是否需要一个长期的、围绕自己资料的、能主动引导的学习系统**。四类人的需求本质相同，只是动作不同——同一个统一运行时既服务自学，也服务教学与研究。

### 1.6 三支柱设计哲学：持久化记忆 + 统一知识库 + 主动式智能体

DeepTutor 的架构设计围绕三根支柱展开 [S5]：

**支柱一：持久化记忆**。系统把学习过程沉淀为三层可审计记忆：L1 记录原始事件、L2 按面整理事实、L3 跨面综合成学习画像，并可用 Memory Graph 把任何一条结论追溯回最初事件 [S1]。说白了，它"记得住你"。

**支柱二：统一知识库**。你上传的教材、笔记、网页会进入一个多引擎检索知识库（默认 LlamaIndex，还可选 GraphRAG、LightRAG 等），问答、出题、深研都从同一份资料里取据 [S1]。这本质是 [[RAG]]（检索增强生成）的工程化落地——先检索、再回答，回答可追溯回原文。

**支柱三：主动式智能体**。基于 Agent-Native 运行时，系统不只是被动等提问，还能主动引导：主动提问、主动出题、通过 IM 渠道持续陪练 [S1][S2]。

> [!tip] 大白话
> 把三支柱想成"教材 + 学习档案 + 家教"：统一知识库是摆在桌上的教材（资料）；持久化记忆是你的学习档案（学过哪、卡在哪）；主动式智能体是那位会翻教材、翻档案、再带你走一步的家教（行动）。三者缺一，就退化成普通的问答工具。

三根支柱的底层实现——单 Agent 循环、三层记忆、多引擎 RAG——都留到第 6 章深入讲解。

### 本章小结

> [!summary] 本章小结
> - DeepTutor 是一个 **Agent-Native 终身个性化学习工作区**，用统一运行时收拢"辅导 / 解题 / 出题 / 研究 / 可视化 / 掌握度练习"六类能力 [S1][S2]。
> - 它针对三组痛点设计：**知识碎片化、学习缺乏连续性、AI 工具过于被动** [S5]。
> - 九个功能面（Chat、Quiz、Research、Mastery Path 等）**共享同一运行时与会话上下文**，是同一场学习中的不同动作 [S1]。
> - 项目 2025-12-29 正式发布，增速极快；写作时锚定 **v1.6.2**（约 38.2k stars）[S1][S6]，使用前记得核对官方文档。
> - 设计哲学是**持久化记忆 + 统一知识库 + 主动式智能体**三支柱 [S5]，对应"记得住你、查得到资料、会主动带你学"。

下一章我们不再纸上谈兵——用一条 `docker run` 命令（借助 [[Docker]]）把 DeepTutor 跑起来，配置好模型，完成第一次对话。

---

## Docker 快速上手 —— 一条命令跑通 DeepTutor

第 1 章我们把 DeepTutor 定义为"有记忆、有知识库、会主动辅导"的 Agent-Native 学习工作区，但那还是概念。这一章彻底落地：借助 [[Docker]]，用一条 `docker run` 命令把完整应用跑起来，再配上模型，完成第一次对话。路线是"准备环境 → 选对安装路径 → 逐行看懂部署命令 → 接入模型（云端为主，本地 [[Ollama]] 可选）→ 验证首聊 → 学会管理容器"。全书以 Windows + Docker Desktop 为主线，看完整章，你的浏览器里会有一个真正能对话的 DeepTutor。写作时以 v1.6.2 为锚，新版本请以官方文档为准。

### 2.1 环境准备：Docker Desktop（Windows）与镜像确认（ghcr.io/hkuds/deeptutor:latest）

动手前先确认两件事：Docker 是否可用、要拉哪个镜像 tag。本笔记针对 Windows 用户，默认你已经装好 Docker Desktop（WSL2 后端）——这是本书唯一的环境依赖，后面你会看到它为什么如此划算。

打开 PowerShell，先验证 Docker 可用：

```powershell
# 确认 docker 命令可用
docker --version

# 确认 Docker 引擎在运行（能打出 Server 信息即正常）
docker info
```

> [!tip] 实践建议
> 如果 PowerShell 提示"无法识别 docker"，先看两处：Docker Desktop 是否已经启动（系统托盘有小鲸鱼图标）、是否已启用 WSL2 后端。都正常后重开一个 PowerShell 再试。第一次冷启动 Docker Desktop 可能要等十几秒，`docker info` 会告诉你引擎到底就绪没有，别急着以为装坏了。

镜像在 GitHub Container Registry（GHCR）上，官方维护的 tag 有三个 [S3][S1]：

| tag | 含义 |
|-----|------|
| `ghcr.io/hkuds/deeptutor:latest` | 当前稳定版（写作时即 v1.6.2） |
| `ghcr.io/hkuds/deeptutor:<version>` | 精确版本，如 `ghcr.io/hkuds/deeptutor:v1.6.2` |
| `ghcr.io/hkuds/deeptutor:pre` | 预发布版（只发版本 tag，不更新 `latest`） |

可以手动先拉一遍（不拉也行，第一条 `docker run` 会自动拉取）：

```bash
docker pull ghcr.io/hkuds/deeptutor:latest
```

> [!tip] 大白话
> 把镜像 tag 想成"版本标签"。`latest` 是"当前推荐版"，`pre` 是"尝鲜版"，`v1.6.2` 是"精确锁定的那一版"。日常用 `latest` 就行；想复现某个版本再锁定具体 tag。

### 2.2 四种安装路径对比（PyPI / 源码 / Docker / CLI Only），为什么首选 Docker

DeepTutor 官方提供四条安装路径 [S1]，它们共享同一套工作区布局（设置在 `data/user/settings/`，默认前端端口 `3782`、后端端口 `8001`）：

| 路径 | 核心命令 | 前置要求 | 适用 |
|------|----------|----------|------|
| PyPI | `pip install -U deeptutor` → `deeptutor init` → `deeptutor start` | Python 3.11–3.13 + Node.js 20+ | 本机跑完整 Web+CLI，不想 clone 源码 |
| 源码 | `git clone` → venv → `pip install -e .` → `(cd web && npm ci --legacy-peer-deps)` → `deeptutor start --dev` | Python 3.11–3.13 + Node.js 22 LTS | 开发 / 改源码 |
| **Docker（推荐）** | `docker run … ghcr.io/hkuds/deeptutor:latest` | Docker Desktop | 一条命令跑通，环境零冲突 |
| CLI Only | 源码 `pip install -e ./packaging/deeptutor-cli` → `deeptutor init --cli` → `deeptutor chat` | Python 3.11+ | 只要终端 / 给其他 agent 驱动 |

为什么本笔记首选 Docker，而不是更"原生"的 PyPI：

- **零环境冲突**：镜像把 Python、Node.js 和全部依赖打包好了，宿主机不用装 Python/Node，也不会跟机器上已有的版本打架。
- **Windows 最友好**：PyPI/源码路径在 Windows 上可能触发 `Microsoft Visual C++ 14.0 is required` 这类源码编译问题（见第 7 章）；Docker 完全绕开。
- **数据进 volume**：设置、知识库、记忆都写在独立数据卷里，升级、删容器都不丢，见 2.3.2。
- **可复现**：换机器、交给别人，都是同一条命令。

> [!tip] 大白话
> 把 Docker 镜像想成"一份打包好的外卖套餐"：米饭、菜、筷子都在盒子里，你拆开就能吃，不用自己买菜做饭，也不会把厨房搞乱。PyPI/源码路径相当于"给你菜谱和食材，自己做"，对 Windows 用户来说更容易踩坑。

其他三条路径并非没用：想要本机 CLI 且愿意装 Python 依赖时选 PyPI；要改源码选源码安装；第 5 章讲"用外部 agent 驱动 DeepTutor"时会用到 CLI Only 的 `deeptutor run`。本章其余部分全部围绕 Docker。

一句话选型建议：**你只是想把它用起来、跑通一个学习场景，就用 Docker**；等哪天真要改 DeepTutor 源码、或者想在无 Docker 的服务器上跑，再考虑其他三条路径。后者的细节在第 7 章排错里会顺带提到（比如 Windows 下 pip 源码编译需要 VS Build Tools）。

### 2.3 部署命令逐行拆解

这是全章最核心的一条命令，把它完整抄进 PowerShell 回车即可：

```bash
docker run --rm --name deeptutor \
  -p 127.0.0.1:3782:3782 \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
```

逐行解释它做了什么：

| 片段 | 作用 |
|------|------|
| `docker run` | 创建并启动一个容器 |
| `--rm` | 容器退出时自动删除容器本体（数据不受影响），重跑前省去手动 `docker rm` |
| `--name deeptutor` | 给容器命名，后面的 `docker logs` / `docker stop` 都靠这个名字引用 |
| `-p 127.0.0.1:3782:3782` | 端口映射：把宿主机 `127.0.0.1:3782` 接到容器内 `3782`（前端端口） |
| `-v deeptutor-data:/app/data` | 数据持久化：把命名卷 `deeptutor-data` 挂载到容器内 `/app/data` |
| `ghcr.io/hkuds/deeptutor:latest` | 使用的镜像 |

首次启动需要拉镜像、初始化，等一两分钟。看到终端持续输出日志、不再快速报错时，浏览器打开 <http://127.0.0.1:3782>，就能看到 DeepTutor 的 Web 界面 [S3]。这一步只要"前端能开出来"就算成功——此时还没配模型，聊天会提示你缺 provider，这是正常的，2.4 节补上即可。

> [!warning] 易错点
> 这条命令用了 `--rm`，所以容器一退出就没了——但你的数据都在 volume 里，所以删容器不可怕。真正需要警惕的是 `docker volume rm`（见 2.6），那才会删数据。

##### 2.3.1 端口映射：为什么只需暴露 3782（前端中转 /api、/ws 到后端 8001）

DeepTutor 内部其实有两个端口：前端（Next.js，`3782`）和后端（FastAPI，`8001`）。但**只需要把 3782 暴露到宿主机** [S1][S3]：

- 浏览器只跟**前端 origin**（`3782`）通信，不直接访问后端。
- 容器内的 Next.js 中间件（`web/proxy.ts`）会把每个 `/api/*` 和 `/ws/*` 请求**在容器内部**转发给 FastAPI 后端（`localhost:8001`）。对浏览器来说，前后端是"同一个地址"。
- 因此单容器场景下你完全不需要配置任何 API base——反向代理 / TLS 终结器直接指向 `:3782` 即可 [S3]。

`8001` 要不要暴露？可选的。只有你想用 curl 或脚本**直接调 API** 时才需要加一条映射 [S3]：

```bash
# 可选：想把后端 API 也暴露到宿主机时再加这条
-p 127.0.0.1:8001:8001
```

`127.0.0.1` 前缀意味着只绑定本机回环地址，局域网其他机器访问不到，本地学习更安全。想换端口只改 `-p` 左侧即可，例如 `-p 127.0.0.1:8088:3782` 就从 8088 访问 [S3]。

对初学者来说，把"前端"和"后端"先简化理解即可：前端是你在浏览器里看到的界面（Chat 输入框、按钮），后端是真正调用模型、查知识库、存记忆的引擎。DeepTutor 把它们装进同一个容器，再用内部代理串起来，所以你只看到一扇门（3782）。第 6 章讲架构时会看到这条内部链路的完整样子。

> [!tip] 大白话
> 把 3782 想成"前台接待"，8001 是"后面的办公室"。你进大楼只跟接待说话，接待再通过**内部走廊**（容器内的 `/api`、`/ws` 转发）帮你找办公室。所以对外只需要开前台这一扇门，办公室的门不必对外开。

##### 2.3.2 数据持久化：deeptutor-data volume 与 data/user/settings/ 布局

`-v deeptutor-data:/app/data` 里的 `deeptutor-data` 是一个 Docker 命名卷（named volume），它把容器里的数据目录 `/app/data` 持久化到 Docker 管理的宿主机存储中 [S3]。

首次启动时，容器会自动在 `/app/data` 下创建 `data/user/settings/*.json` [S3]。**配置、API key、日志、工作区文件、记忆、知识库、Partner 工作区（`data/partners/<id>/`）全部持久化在这个 volume 里**——这意味着你升级镜像、删掉容器，这些东西都还在 [S1][S3]。

`data/user/settings/` 下是普通 JSON/YAML 配置文件，推荐用浏览器里的"设置"页编辑，不推荐手改 [S1]：

| 文件 | 用途 |
|------|------|
| `model_catalog.json` | LLM / Embedding / 搜索 provider 的 profile、API key、激活模型 |
| `system.json` | 前后端端口、API base、CORS、SSL 校验、附件目录等 |
| `auth.json` | 可选的多用户认证开关、用户名、密码哈希 |
| `interface.json` | UI 语言 / 主题 / 侧边栏偏好 |
| `main.yaml` | 运行时行为默认值 |
| `agents.yaml` | 各能力 / 工具的温度与 token 设置 |

一个容易踩的坑：**可选依赖要声明在部署层，而不是钻进容器里安装**。想加 RAG 引擎之类的额外 Python 包，设好 `DEEPTUTOR_EXTRAS`（系统库用 `DEEPTUTOR_APT_PACKAGES`），每个容器启动时自动补齐；用 `docker exec … pip install` 装的东西，下次重建容器就没了 [S3]。

> [!tip] 大白话
> 把 volume 想成"插在容器上的一块移动硬盘"。容器本身是一次性纸杯，扔了不可惜；你的资料、设置、API key 都在移动硬盘里，拔下来换新杯子再插上，东西一样不少。所以"删容器"不可怕，"格式化硬盘"（`docker volume rm`）才可怕。

### 2.4 模型接入：设置 → Models

浏览器打开 <http://127.0.0.1:3782>，进入 **设置 → Models**。给 DeepTutor 配模型，核心就一个 LLM profile：**Base URL / API key / model 名称**，保存后 DeepTutor 会做一次 provider probe（连通性探测）[S1][S4]。这个页面有点像手机的"输入法设置"——不是配一次就完事，而是可以存多套 profile 随时切换，比如日常用云端 DeepSeek 省钱、推理难题切到 Anthropic、断网时切到本地 Ollama。

- 只配 **LLM** 就能聊天、解题、出题。
- 想用知识库 / [[RAG]]（第 3 章）再配一个 **Embedding** profile。
- v1.6.x 里可以用 **Connections** 一次性录入某厂商凭证，自动镜像到该厂商能服务的所有服务（LLM、Embedding 等），不用重复粘贴 [S1]。

> [!note] 核心概念
> provider probe 是"保存即探测"：DeepTutor 拿着你填的 Base URL 和 key 去厂商打一个测试请求。它通过，说明配置大概率没问题；报 `401`，多半不是网络问题，而是 **key 前缀不对** [S4]。

##### 2.4.1 云端 API 为主：OpenAI / DeepSeek / Anthropic 的 Base URL 与 key 前缀

日常最省事的是接云端 API。下表给出研究素材中明确记录的信息 [S4]，Base URL 未在素材中出现的厂商，请以其官方文档为准：

| Provider | Base URL | API key 前缀 | 备注 |
|----------|----------|--------------|------|
| OpenAI | `https://api.openai.com/v1` | `sk-` / `sk-proj-` | project key 用 `sk-proj-` [S4] |
| Anthropic | 以官方文档为准 | `sk-ant-` | 401 时先核对前缀 [S4] |
| DeepSeek | 以官方文档为准（OpenAI 兼容端点） | `sk-` 开头 | 走 OpenAI 兼容协议 |
| Gemini | 以官方文档为准 | `AIza` | Google 系 [S4] |
| Ollama（宿主机直连场景） | `http://localhost:11434/v1` | 留空或 `none` | 非 Docker 部署时用 [S4] |

> [!warning] 易错点
> provider probe 报 `HTTPError 401 Unauthorized`，九成是 key 前缀不对：OpenAI 必须是 `sk-`/`sk-proj-`、Anthropic 必须是 `sk-ant-`、Gemini 必须是 `AIza`；Ollama 这类本地 OpenAI 兼容服务 key 留空或填 `none` [S4]。另外，`Failed to fetch /models`（模型列表拉取失败）是**非致命**的，向导会回退到内置模型列表继续 [S4]。

##### 2.4.2 本地 Ollama 补充：host.docker.internal（Windows/macOS 免加 --add-host，Linux 需 extra_hosts）

如果你偏好本地模型，在宿主机装好 [[Ollama]] 后，关键认知是：**容器内的 `localhost` 指容器自己，不是宿主机** [S3]。要让容器访问宿主机上跑的模型服务，需要走 host gateway（`host.docker.internal`）。

Base URL 在设置 → Models 里指到 `host.docker.internal` [S3][S1]：

| 本地服务 | Base URL |
|----------|----------|
| Ollama LLM | `http://host.docker.internal:11434/v1` |
| Ollama embedding | `http://host.docker.internal:11434/api/embed` |
| LM Studio | `http://host.docker.internal:1234/v1` |
| llama.cpp | `http://host.docker.internal:8080/v1` |

运行容器时的差别：

- **Windows / macOS 的 Docker Desktop 通常不需要 `--add-host`**，`host.docker.internal` 会被原生解析 [S3][S4]。
- **Linux 上**需要显式把这个 hostname 指到宿主网关，推荐在 `docker run` 里加 `--add-host=host.docker.internal:host-gateway` [S3]；用 docker-compose 则写 `extra_hosts`：

```yaml
# docker-compose 的 Linux 场景（Windows/macOS 可忽略）
services:
  deeptutor:
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

综合起来，Windows 上想连本地 Ollama 的完整命令是：

```bash
docker run --rm --name deeptutor \
  -p 127.0.0.1:3782:3782 \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
```

（Windows/macOS 不加 `--add-host`；Linux 用户在上面命令里插入 `--add-host=host.docker.internal:host-gateway` 一行即可 [S3]。）

> [!tip] 大白话
> 把 `host.docker.internal` 想成"回老家的秘密通道"。你在外面上大学（容器里），`localhost` 指你自己的宿舍；想找家里（宿主机）的打印机，得走一条叫 `host.docker.internal` 的通道回去。Windows/macOS 的宿舍管理员（Docker Desktop）默认修好了这条通道，Linux 需要你自己打通。

##### 2.4.3 Embedding 配置：完整 endpoint 规则（/v1/embeddings、/v2/embed 等）

Embedding 是知识库 / [[RAG]] 的基石，第 3 章建知识库时必需。它的坑和 LLM 不同：**Embedding adapter 会原样使用 profile 里的 Base URL，所以必须填完整 endpoint，而不是只填 API root** [S4]。

| Provider | 错误（只填 API root） | 正确（完整 endpoint） |
|----------|------------------------|------------------------|
| OpenAI | `https://api.openai.com/v1` | `https://api.openai.com/v1/embeddings` |
| Cohere | `https://api.cohere.com` | `https://api.cohere.com/v2/embed` |
| Jina | `https://api.jina.ai/v1` | `https://api.jina.ai/v1/embeddings` |
| Ollama（容器内访问宿主机） | `http://host.docker.internal:11434` | `http://host.docker.internal:11434/api/embed` |

> [!warning] 易错点
> 记住规则：OpenAI 兼容系一般是 `/v1/embeddings`，Cohere 是 `/v2/embed` [S4]。填错 endpoint 会一直报 Embedding 错误；如果之后换了 embedding 模型再建库还报 `Embedding dimension mismatch`，那是索引维度缓存对不上，需要在第 3 章的知识库界面做 **Re-index now** 重建索引（第 7 章也会讲到）。

### 2.5 首次对话验证：Web UI 与 CLI 双路径

配置完模型，来做第一次对话验收，有 Web 和 CLI 两条路。

**路径一：Web UI**

1. 打开 <http://127.0.0.1:3782>，进入 Chat 页面。
2. 确认右上/设置里已配置好 LLM profile（probe 通过）。
3. 输入一句测试，比如"你好，请用一句话解释什么是 RAG"，观察回复是否流式输出。

看到正常回复，说明部署 + 模型链路已通。如果回复卡住或报错，先看右下/设置里 provider 是否 probe 通过，再回看 2.4.1 的 key 前缀表。顺带可以在设置 → Models 里把 Embedding 也配好，给第 3 章建知识库做准备——现在配好，第 3 章上传教材就不用回头补了。

**路径二：CLI**

DeepTutor 自带 CLI：`deeptutor chat` 进入交互式聊天 REPL，`deeptutor doctor` 做健康检查（`--online` 额外探测已配置的模型 provider）[S1]。在 Docker 部署下，这两条命令在**容器内**执行，作用于同一个 `/app/data` 工作区：

```bash
# 容器内健康检查：工作区是否就绪
docker exec deeptutor deeptutor doctor

# --online 会额外探测模型 provider 是否可连（401/网络问题一目了然）
docker exec deeptutor deeptutor doctor --online

# 进入容器内交互式聊天
docker exec -it deeptutor deeptutor chat
```

> [!tip] 实践建议
> `deeptutor doctor --online` 是后面排错的好帮手，第 7 章会反复用到。它的输出会明确告诉你是工作区没就绪、还是模型 provider 连不上，比自己瞎猜快得多。如果你不想每次 `docker exec`，也可以在本机按 2.2 的 CLI Only 路径单独装一个 CLI 包，在宿主机直接敲 `deeptutor chat`——两条路用的是同一套 `data/user/settings/` 布局，理解成本很低。

### 2.6 容器生命周期：后台运行、日志、停止、升级、彻底重置 volume

掌握这组命令，就能把容器"养"起来：

```bash
# 后台运行（加 -d，不再占住当前终端）
docker run -d --name deeptutor \
  -p 127.0.0.1:3782:3782 \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest

# 跟踪日志（Ctrl+C 退出跟踪，不影响容器）
docker logs -f deeptutor

# 停止 / 删除容器（volume 保留，设置和知识库都还在）
docker stop deeptutor
docker rm deeptutor

# 彻底重置：连设置、知识库、记忆一起清空
docker volume rm deeptutor-data
```

后台运行时想看容器在不在、状态如何，用 `docker ps`（`-a` 连已退出的也显示）。容器正常应该是 `Up` 状态。如果它反复重启或立刻退出，`docker logs deeptutor | tail -30` 是最快的排查入口——无效的 LLM 凭据只记 warning、不会让启动失败，所以真退出时去日志里找别的致命错误 [S3][S4]。

**升级**是"拉新镜像 → 删旧容器 → 重建"，volume 会撑过升级，设置、知识库、记忆都保留 [S3]：

```bash
docker pull ghcr.io/hkuds/deeptutor:latest
docker rm -f deeptutor
docker run --rm --name deeptutor \
  -p 127.0.0.1:3782:3782 \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
```

设置 → 关于 会识别 Docker 镜像并提示是否有新版本，但**替换容器属于部署操作**——DeepTutor 不会在运行中的容器里原地升级包 [S3]。所以看到新版本提示，按上面三步走即可。

> [!warning] 易错点
> `docker volume rm deeptutor-data` 是破坏性操作，会清掉所有设置、API key、知识库和记忆，且不可撤销。执行前先确认不再需要这些数据。端口被占、容器立刻退出等问题属于排错范畴，统一放第 7 章。

### 2.7 本节小结：部署验收清单

> [!summary] 本章小结
> - 四条安装路径中 **Docker 最适合上手**：一条命令、零环境冲突、Windows 友好、数据进 volume [S1][S3]。
> - 单容器部署**只需暴露 3782**：容器内 Next.js 中间件把 `/api/*`、`/ws/*` 转发给后端 8001，浏览器不用直连后端 [S1][S3]。
> - `deeptutor-data` 命名卷挂到 `/app/data`，**设置 / API key / 日志 / 工作区 / 记忆 / 知识库 / Partner 工作区全部持久化**，删容器不丢数据 [S3]。
> - 模型配置 401 先查 **key 前缀**（OpenAI `sk-`、Anthropic `sk-ant-`、Gemini `AIza`）[S4]；Embedding 必须填**完整 endpoint**（OpenAI `/v1/embeddings`、Cohere `/v2/embed`）[S4]。
> - 本地 [[Ollama]] 走 `host.docker.internal`，Windows/macOS 免 `--add-host`，Linux 需 `extra_hosts` 或 `--add-host=host.docker.internal:host-gateway` [S3][S4]。
> - 生命周期口诀：`docker logs -f` 看日志、`docker stop` 停、`docker rm` 删容器、`docker volume rm` 才清数据；升级是 `pull → rm -f → run` [S3]。

**部署验收清单**：

- [ ] Docker Desktop 运行中，`docker --version` 正常
- [ ] 一条 `docker run` 启动成功，<http://127.0.0.1:3782> 能打开 Web 界面
- [ ] 设置 → Models 配好 LLM，provider probe 通过（无 401）
- [ ] （可选）配好 Embedding 完整 endpoint，供第 3 章建知识库用
- [ ] （可选）本地 Ollama 场景，`host.docker.internal` 能解析、能连
- [ ] 会用 `docker logs` / `docker stop` / `docker rm`，并理解 volume 里存了什么

至此，DeepTutor 已经在你机器上跑起来并完成首次对话。下一章进入它的主战场——建知识库、出题、可视化与深研，那才是一套学习闭环真正展开的地方。

---

## 第 3 章 核心玩法 —— 建知识库、出题、可视化与深研

> 适用版本：v1.6.2。DeepTutor 迭代很快，文中命令与界面路径以当前版本为准，如有出入请以官方文档为准。

部署完成（第 2 章）之后，你已经能打开 http://127.0.0.1:3782 和 DeepTutor 聊天了。但"聊天"只是入口——真正让它区别于普通聊天工具的是 **Knowledge Center（知识中心）**：把教材上传成可检索的知识库，再让同一个运行时去出题、解题、可视化、深研。这一章就围绕这个核心玩法展开：先建知识库，再做带引用的问答，然后依次玩转出题、可视化、解题与深研。Chat、Ask Questions、Quiz、Visualize、Solve、Research 这些能力共享同一套运行时与会话上下文，这正是它的设计特点 [S1][S6]。

> [!tip] 大白话
> 把 DeepTutor 想成一个"带图书馆的私教"。Chat 是私教本人，知识库就是他的图书馆。没有图书馆，私教只能凭记忆（LLM 预训练知识）回答；有了图书馆，他回答前会先翻书，还能告诉你"这句话出自哪一页"。本章教你如何把书放上架，以及让私教用这些书做各种事 [S1]。

### 3.1 知识库（Knowledge Center）：上传教材，建立可检索索引

先讲一个贯穿全书的概念——[[RAG]]。RAG（Retrieval-Augmented Generation，检索增强生成）就是"先检索、再生成"：模型回答前先从知识库里把相关片段检索出来，再依据这些片段组织答案。它解决的是 LLM 只靠预训练记忆、回答"过期或编造"的问题。DeepTutor 的知识库就是 RAG 的"检索源"，它会去承接 Chat、Co-Writer、Book 生成、Partner 对话等多个能力的提问（原理细节放在第 6 章展开）[S1]。

在 Web UI 里，入口是侧边栏的 **Knowledge Center**（知识中心）；在终端里，入口是 `deeptutor kb` 命令族。两种入口操作的是同一批知识库。

#### 3.1.1 创建 KB：create new 上传建新索引 vs link existing 复用外部索引

进入 Knowledge Center 后新建一个知识库（KB），第一步要选创建方式，两种方式差别很大 [S1]：

| 方式 | 含义 | 典型场景 |
| --- | --- | --- |
| **create new** | 上传文档，DeepTutor 解析后**新建一份索引** | 上传教材 PDF、课程 PPT、笔记文档，从零建库 |
| **link existing** | **原地复用**外部已有索引，不重建 | 链接自己的 Obsidian vault、外部 LightRAG Server、腾讯 IMA、MarginNote 4 等 |

`create new` 是上手最常用的：点击后上传教材文件（PDF/DOCX/PPTX/XLSX 等），DeepTutor 会按你选的解析器抽取正文、切分、向量化，最终形成一份本地索引。`link existing` 则适合你已经有数据的地方——比如你的 Obsidian 笔记库，链接后 DeepTutor 直接原地读写，**不会重复建一份**。每个 KB 只绑定一种引擎（见 3.1.2），所以"新建 vs 链接"其实是"本地建索引 vs 引用外部索引"的分叉口。

用 CLI 建库更直接，比如用一份教材 PDF 新建一个名为 `my-kb` 的知识库：

```bash
# 新建知识库并上传一份教材
deeptutor kb create my-kb --doc textbook.pdf

# 追加另一份文档到已有 KB
deeptutor kb add my-kb --doc notes.md

# 在 KB 里检索一个查询
deeptutor kb search my-kb "傅里叶变换"

# 查看所有 KB / 查看某个 KB 的详情
deeptutor kb list
deeptutor kb info my-kb
```

> [!tip] 大白话
> 把 `create new` 想成"在图书馆里**新进一批书并编好目录**"；把 `link existing` 想成"把你家书房**整个并入**图书馆，直接用原书，不再抄一遍"。所以前者要花时间建索引，后者基本秒开，但前提是你得先有那份"外部索引"。

#### 3.1.2 引擎与解析器：LlamaIndex 默认、PageIndex/GraphRAG/LightRAG 等；MinerU/Docling/markitdown 等解析器

每个 KB 创建时都要选一个**检索引擎**（retrieval engine）。默认是 [[LlamaIndex]]，但 DeepTutor 特意做成"多引擎"，因为不同资料形态适合不同检索方式 [S1]：

| 引擎 | 检索方式 | 适合 |
| --- | --- | --- |
| **LlamaIndex**（默认） | 本地向量 + BM25 混合 | 大多数教材/文档，开箱即用 |
| **PageIndex** | 页面级引用 + 推理式检索（可自托管 OSS） | 需要"逐页引用"的阅读场景 |
| **GraphRAG** | 知识图谱检索 | 需要跨实体关系、归纳性提问的资料 |
| **LightRAG** | 轻量知识图谱检索（也可用 LightRAG Server 外连） | 同上，偏好更轻量/自托管 |
| **Tencent IMA / MarginNote 4 / 链接的 Obsidian vault** | 外部资料库原地读写 | 你已经把资料整理在这些工具里 |

选好引擎后，文档怎么"读"进去由**解析器**（document parsing engine）决定。可选的有 Text-only、MinerU、Docling、Tika、markitdown、PyMuPDF4LLM、LiteParse，在 **Settings → Knowledge Base**（文档解析引擎）里统一配置 [S1]。其中 MinerU 支持 PDF、常见图片、DOCX/PPTX/XLSX，适合公式/表格多的教材；Docling 还支持"远程 Docling Serve"模式，不装本地模型就能解析。注意本地模型默认关闭下载，需要时再开。

> [!tip] 大白话
> 引擎和解析器是两回事：引擎决定"**怎么查**"（按关键词？按语义？按知识图谱？），解析器决定"**怎么读**"（PDF 里的表格和公式能不能被正确抽出来）。先用默认的 LlamaIndex + Text-only 跑通，遇到 PDF 解析质量差再换 MinerU/Docling，不必一步到位。

#### 3.1.3 索引管理：version-N 目录、Re-index now、单文档移除

知识库用久了会碰到三种管理场景，DeepTutor 的设计都考虑了 [S1][S4]：

1. **重建索引不破坏旧版**：重新索引时，新结果写入一个新的 `version-N` 目录（如 `version-1`、`version-2`），旧的保留，正在服务的索引不会被中途毁掉。Web UI 里在 **Knowledge → KB → Index versions** 查看版本历史。
2. **换过 embedding 模型后要手动重建**：如果配置之后更换了 Embedding 模型，旧向量和新向量维度不一致，检索会报 `Embedding dimension mismatch`。此时去 **Knowledge → KB → Index versions → Re-index now** 一键重建即可，不用删库重来 [S4]。
3. **单文档移除**：某份文档解析失败、卡在 error 状态，不必"删库重建"，可以**只移除这一份**失败文档 [S1][S4]。KB 卡在 indexing 时，可看日志定位原因：

```bash
tail -f data/user/logs/deeptutor.jsonl | grep -i kb
```

常见诱因包括 Embedding 限流（429）、embedding host 不可达、PDF 带密码等 [S4]。

> [!warning] 易错点
> 上传 PDF 后提问得到"答非所问"，先别怀疑模型——九成是解析/索引环节的问题：检查解析器是否抽到了乱码、embedding 配置是否完整、有没有重建索引。排错顺序：看日志 → 换解析器 → Re-index now。

### 3.2 带引用的问答：让回答可追溯（rag / read_source 工具）

知识库建好后，最核心的用法是**带引用的问答**。回到 Chat（默认能力），在输入框上方的工具栏里选中所绑定的知识库（这是"粘性会话上下文"，跨轮保持），然后提问。模型回答时，会根据需要自动挂载上下文相关工具 [S1]：

- **`rag`**：从当前 KB 检索相关片段；
- **`read_source`**：读取命中片段的**源文档/源页面**，把完整上下文带回对话；
- **`kb_files`**：浏览 KB 里的文件清单。

因为这套工具链的存在，DeepTutor 的答案是**可追溯**的——回答里的每个结论都能指向它引用的来源，你可以点开引用看原文，而不是对着一个黑箱输出猜来源 [S1]。这也是论文里强调的"引文锚定的问题辅导"（citation-grounded problem tutoring）落地的样子 [S2]。

CLI 里同样可以指定 KB 再提问：

```bash
# 用 textbook 这个 KB 做底，走单轮 chat
deeptutor run chat "Explain the Fourier transform" --tool rag --kb textbook

# 进入交互式 REPL，随时切换 KB
deeptutor chat --capability chat --tool rag --kb my-kb
```

> [!tip] 大白话
> 把 `rag` 想成"去图书馆查资料"，`read_source` 想成"把查到的那本书**翻到那一页**读原文"。所以 DeepTutor 的回答像写论文：每个观点后面都跟着参考文献，你可以点进去核对，而不是听它空口白话。

### 3.3 出题：Ask Questions 与 Quiz 的难度校准

读懂了教材，怎么检验自己？用 **Ask Questions（提问）** 和 **Quiz（测验）** 两个能力 [S1]。

- **Ask Questions**：基于当前上下文（知识库、笔记、聊天记录）生成开放式问题，适合自测理解、引导思考。Web UI 首页即可一键进入。
- **Quiz**：生成带选项的测验题，可以绑定知识库出题。生成的题目会进入**题库（Question Bank）**，之后可复用。

这两个能力背后的关键设计是**难度校准（difficulty-calibrated）**。论文把整个引擎概括为"引文锚定的问题辅导 + 难度校准的题目生成"，并配套了一个叫 TutorBench 的评测基准来验证"个性化出题"的效果——简单说，它不只是"生成一些题"，而是**贴合你的掌握水平**去出题 [S2]。深层的个性化机制在第 6 章讲，这里你先记住：出题时会结合你的学习档案（记忆）调整难度，而不是每次随机。

CLI 对应能力名：

```bash
# 基于深研结果，继续出题考自己（用上一轮的 session 延续上下文）
deeptutor run deep_question "Quiz me on that survey" --session "$SID" --format json
```

> [!tip] 大白话
> 难度校准想成"私教先摸你的底，再给你**够得着但不白给**的题"。全是太简单的题你会无聊，全是大难题你会劝退；好私教知道你现在能跳多高，题目就卡在"踮踮脚能碰到"的位置。

### 3.4 可视化（Visualize）与解题（Solve）

- **Visualize（可视化）**：把概念/数据画成图，底层用 Chart.js/SVG/Mermaid 等渲染，v1.6.2 起是插件式目录（plugin-driven catalog），所以能画的图会越来越多 [S1]。适合把抽象的数学、算法、数据结构变成看得见的图。
- **Solve（解题）**：走完整推理过程，不只给答案，给"怎么一步步想出来"。在 v1.6.2 中叫 `deep_solve`，可以配合 `--tool reason` 或挂载知识库来解 [S1]。

Web 入口：首页直接有 Visualize；Solve 在 **More Capabilities**（更多能力）里。CLI：

```bash
# 可视化：让 DeepTutor 生成图表
deeptutor run visualize "画一下傅里叶级数逼近方波的过程"

# 解题：带知识库和推理工具解一道题
deeptutor run deep_solve "Solve x^2 = 4" --tool rag --kb my-kb
deeptutor run deep_solve "Find d/dx[sin(x^2)]" --tool reason --format json
```

> [!tip] 大白话
> Visualize 想成"私教在草稿纸上画图给你看"，Solve 想成"私教把每一步演算过程写在黑板上"。两者都是**把黑盒答案变成可见过程**，帮你从"知道答案"走向"理解过程"。

### 3.5 深研（Research）：多步检索与综合

**Research（深研）**是功能面里"最强检索"的一档：给定一个主题，它会**多步检索、反复迭代**，最后输出带引用的综合报告 [S1]。和普通问答的"问一句答一句"不同，深研更像"给你一个课题，先查资料、再交叉验证、最后写一篇带出处的小综述"。能力名是 `deep_research`，Web 入口在 **More Capabilities → Research**。

CLI 示例（输出模式可设 report、深度可调）：

```bash
deeptutor run deep_research "Survey 2026 papers on RAG" \
  --config mode=report --config depth=standard
```

深研的结果天然适合接上 3.3 的出题——查完一个主题，让它基于这份调研给你出题，就是一个完整的"输入 → 研究 → 检验"链条。

> [!tip] 大白话
> 普通问答是"查一个词条"，深研是"**写一篇综述**"：它会自己拆解子问题、反复搜索、判断哪些资料靠谱，最后拼成一篇带引用的报告。你只给方向，跑腿的事交给它，但你依然能点开每条引用核对来源。

### 3.6 本节小结：一个完整学习闭环示例

把 3.1–3.5 串起来，就是一个可重复的**学习闭环**：

> [!example] 学习闭环示例
> 1. **建库**：在 Knowledge Center 用 `create new` 上传教材 PDF（引擎默认 [[LlamaIndex]]，解析器用 MinerU 处理公式表格），建好 `textbook` 知识库。
> 2. **带引用问答**：在 Chat 选中 `textbook`，问"什么是傅里叶变换"，看回答里的引用并点进 `read_source` 核对原文。
> 3. **出题**：用 Ask Questions / Quiz 基于该知识库生成习题，检验是否真的读懂。
> 4. **可视化 + 解题**：对没想明白的推导，让 Visualize 画图、让 Solve 展开步骤。
> 5. **深研**：写报告或深入研究时，让 Research 多步检索产出带引用的综述。
> 6. **沉淀**：把有价值的问答、报告、习题整理进笔记/题库，供后续复用。

> [!summary] 本章要点
> - 知识库是 DeepTutor 一切玩法的基础：`create new` 新建索引、`link existing` 复用外部索引（Obsidian/IMA/MarginNote/LightRAG Server 等）。
> - 每个 KB 绑定一个检索引擎（默认 [[LlamaIndex]]，可选 [[GraphRAG]]/LightRAG/PageIndex 等）；解析器在 Settings → Knowledge Base 配置（Text-only/MinerU/Docling/markitdown 等）。
> - 索引管理三件事：`version-N` 版本目录保留旧版、换 embedding 后 **Re-index now**、坏文档可单文档移除。
> - 带引用问答靠 `rag` + `read_source` 工具实现可追溯回答；出题有难度校准（论文核心之一）；Visualize/Solve/Research 分别对应画图、展开步骤、多步检索综合。
> - 所有能力共享同一运行时与上下文：建好库后，出题/解题/可视化/深研都围绕它运转。

下一章进入 **第 4 章：掌握度路径（Mastery Path）与 Course Study**——看看 DeepTutor 如何把第 3 章的"出题"升级成"分级的掌握度门控"，把零散练习变成一条可追踪的学习路径。

---

## 掌握度路径（Mastery Path）与 Course Study

第 3 章我们把教材喂进知识库、让 DeepTutor 出题和深研，解决了"学什么、怎么练"的供给问题。但学习不能只靠"练得多"，还得回答"到底学会了没有"。本章讲 DeepTutor 给出的答案：用 **Mastery Path** 做分级掌握度验证，用 **Course Study** 把学习固定在某个课程上下文里（版本锚点 v1.6.2，具体功能以官方文档为准 [S1]）。

### 4.1 Mastery Path 是什么：分级掌握门控与 /learning 仪表盘

Mastery Path 是 DeepTutor 的功能面之一，与 Chat、Quiz、Solve 等共享同一个能力运行时与会话上下文，只是它的循环专门为"掌握度练习"设计 [S1]。在界面里，它和 Immersive Reading 一样是**独立的侧边栏工作区**，而不是首页上的一个按钮 [S1]。

它的核心机制叫**分级掌握门控**（progressive mastery gating）。自 v1.4.5 起，Guided Learning 重建在 chat agent loop 之上，为每种类型设置了硬性门控（hard per-type mastery gate），并配上 `/learning` 仪表盘统一展示进度 [S1]。可以把路径理解成被切成多个知识点关卡，每个关卡按类型（概念、计算、推理等）出题，**达标了才放行到下一级，没达标就卡住、回到对应材料重练**。这种"按类型卡进度"的设计，让掌握度验证不是笼统打一个分，而是能明确指出你的短板落在哪个类型上。

> [!tip] 大白话
> 把 Mastery Path 想成"闯关游戏"：每一关没打满血条就不让你进下一关。所以它先暴露你在哪些类型上薄弱，再用题目验证你到底补上没有，而不是一路闷头往下学。

用法上，进入 Mastery Path 工作区后选一个学习目标，系统会在 `/learning` 仪表盘上显示各类型的掌握状态，逐级练习直到门控通过 [S1]。批改过的掌握度题目还会自动流入 **Question Bank**，成为后续可复用的题目资产 [S1]；这些已过关的题之后也能被第 5 章的 Book 等场景引用，作为生成材料的一部分。CLI 层同样保留了 mastery_path、course_study 两个能力入口，方便用脚本单轮触发 [S1]。

### 4.2 Course Study：课程绑定上下文的小班式学习

如果说 Mastery Path 是按"知识点"组织，Course Study 就是按"课程"组织。它与 Chat、Quiz 共享同一能力运行时，但**保持课程绑定的上下文**（course-bound context）[S1]。在 v1.6.0 中，课程自带 **Little Tutor** 与 **Ask Questions** 两个能力，由 [[Agent]] 在该课程的上下文内讲解和提问 [S1]。

> [!tip] 大白话
> 把 Course Study 想成"小班教室"：一个班有自己的教材、聊天记录和作业。你在这个班里提问、被讲解，上下文不会串到别的科目，老师（Agent）记得你在这门课学到哪了。

支撑它的还有 Learning Space 里的 **My courses**：把每个科目的会话归组，tutor 线程嵌套在父课程之下，聊天历史可按课程或线程类型过滤 [S1]。所以课程不是一次性的聊天会话，而是有归属、可归档、可过滤的长期上下文。Course Study 因此适合按"一门课"推进：一门课一个上下文，学习材料、对话、出题都留在这个封闭范围内，不会互相串味。

### 4.3 与第 3 章核心玩法如何串联：从知识库 → 出题 → 掌握度验证

第 3 章和第 4 章其实是同一个闭环的两半。第 3 章在 Knowledge Center 建好知识库（[[RAG]] 可检索索引），用 Ask Questions / Quiz 生成习题；第 4 章的 Mastery Path 把这些内容变成"验证关卡"。

1. **知识库**（第 3 章）：上传教材，建立可检索索引，为回答和出题提供依据。
2. **出题**（第 3 章）：Ask Questions 针对某个知识点提问，Quiz 生成习题。
3. **掌握度验证**（本章）：Mastery Path 用分级门控逐级测你，通过后把批改过的题沉淀进 Question Bank [S1]，反过来再供第 3 章的场景（问答、习题、Living Book）复用。

> [!tip] 实践建议
> 一个顺手的循环：进 Course Study 选定课程 → 用第 3 章的知识库问答和 Quiz 出题 → 到 Mastery Path 逐级验证 → 没通过的回到 Ask Questions 精讲该知识点 → 全部通过后题目进 Question Bank 成为资产。

> [!summary] 本章小结
> - Mastery Path 用分级掌握门控验证"是否真的学会"，`/learning` 仪表盘统一展示进度 [S1]。
> - 掌握度题批改后自动流入 Question Bank，沉淀为可复用的题目资产 [S1]。
> - Course Study 保持课程绑定上下文，课程自带 Little Tutor 与 Ask Questions，适合按门课推进 [S1]。
> - 与第 3 章串联成"知识库 → 出题 → 掌握度验证"的闭环，即"学—练—验"。

下一章进入进阶玩法：把知识库、题库与聊天历史编译成交互式 **Living Book**，并让 **Partners/TutorBot** 在 IM 渠道上陪你学。

---

## 进阶玩法 —— Living Book、Partners 与 Agent 驱动

前三章我们把 DeepTutor 当成"高级搜索引擎 + 出题机"用：建知识库、做带引用问答、生成习题、走掌握度路径。这一章换一个思路——把学习材料编译成可以交互阅读的"活书"、让一个拥有自己性格和 IM 号码的伙伴常驻陪伴、把其他 [[Agent]] 变成自己的一部分，最后反过来让外部 agent 来驱动 DeepTutor。这些都是"进阶玩法"：不改变核心运行时（第 6 章才讲架构），但它们决定了一个学习工作区能"活"到什么程度。本文以 v1.6.2 为锚，新版以官方文档为准 [S1]。

### 5.1 Living Book：把 KB / 笔记 / 题库 / 聊天历史编译成交互式"活书"

Book Engine 是 DeepTutor 里的"活书"编译器。它把静态材料——知识库、笔记、题库、聊天历史——编译成一本可交互阅读的书，而不是一份死板的 PDF [S1]。和普通电子书最大的区别是：书由"类型化块"（typed blocks）拼成，每个块可以单独插入、移动、重新生成、改写或切换类型；每一页还挂着自己的聊天（Page Chat），读者可以就地提问。

> [!tip] 大白话
> 把 Living Book 想成"把一本教材做成带弹窗练习、可展开代码、能画动画的交互式网页"，而且每一页底下都有"评论区"可以和 AI 对话。所以阅读不再是被动翻页，而是随时可以停下来提问、做题、记笔记。

##### 5.1.1 块类型与页面聊天（Page Chat）

Book Engine 内置 **14 种块类型**，覆盖了从"读"到"练"到"展示"的大部分场景 [S1]。常见的有：文本、callout、测验（quiz）、闪卡（flash card）、时间线、代码、图（figure）、交互式 HTML、动画、概念图（concept graph）、深挖（deep dive）和用户笔记（user note）等。

- 同一章可以混排多种块：一段概念讲解后面紧跟一个测验块，再跟一张概念图，读者可以边读边自测。
- 每个块都可单独操作：插入、移动、重新生成、改写、或直接切换块类型，不需要整章重写。
- **Page Chat** 是每页自带的对话：读者对当前页内容提问，AI 在"这一页"的上下文里回答，而不是拉进整本书 [S1]。

创建时 DeepTutor 会先**提议章节大纲**，你确认结构后才生成内容，而不是一次性盲写 [S1]。进度、书签、测验作答、捕获（capture）和 Page Chat 都按读者私有保存——即使这本书是共享的只读或协作编辑，每个读者的阅读状态也互不干扰 [S1]。

##### 5.1.2 编译、导出 Markdown、健康检查

创建一本书可以基于四种材料之一：知识库、笔记、题库或聊天历史 [S1]——这正是第 3 章和第 4 章攒下的东西。流程上是：

1. 在 Book 工作区选来源（KB / notebook / question bank / chat history）；
2. 确认 DeepTutor 提议的章节大纲；
3. 开始编译：长书编译支持暂停和续跑，编译过程中可以边生成边阅读（v1.5.13 起）[S1]；
4. 阅读、加块、Page Chat、导出。

任何书都可以**导出为 Markdown**，方便带走或在其他工具里继续编辑。命令行提供配套的健康检查命令 [S1]：

```bash
# 列出本地所有书
deeptutor book list

# 健康检查：对比源指纹，标记源材料是否漂移（源文件被改/删）
deeptutor book health

# 手动刷新源指纹
deeptutor book refresh-fingerprints
```

如果源材料（比如 KB 里的文档、题库）在你编完书之后变了，`book health` 会标记"源漂移"，提醒你决定要不要重新编译——这正是"活书"和静态导出文件的差别：它和源头保持可追踪的关系 [S1]。

### 5.2 Partners / TutorBot：持久陪伴体与 15+ IM 渠道

如果说 Living Book 把"材料"做活了，那么 Partner 就是把"AI 老师"做活了。Partner 是一个**持久陪伴体**：有独立的 SOUL（人设）、模型策略、资料库、记忆和渠道，可以常驻在微信、飞书、Telegram 等 IM 里 [S1]。

> [!tip] 大白话
> 把 Partner 想成"一个自带电话号码的 AI 好友"——你把它加进微信/飞书通讯录，它就一直在线，用自己固定的人设、自己的知识库、自己的记忆回答你。所以 Partner 的本质是"一只有性格、有电话号码的 Chat"。

##### 5.2.1 术语演进：TutorBot → Partners

在 v1.4.3（2026-06-12）之前，这个功能叫 **TutorBot**；v1.4.3 起官方把它重命名为 **Partners**，同时把 IM 管道升级为生产级（15 个渠道、实时流式输出）[S1]。早期文档、论文和社区文章里仍会出现"TutorBot"字样，本书统一用 **Partners**，读到"TutorBot"时可以按同一概念理解 [S1]。

##### 5.2.2 创建 Partner 并接入一个 IM 渠道（Feishu/Telegram/微信等）

Partner 不是独立的 bot 引擎——每条进来的 IM 消息在内部都是一次普通的 Chat 回合，跑在 partner 专属的工作区里 [S1]。每个 Partner 包含：`SOUL.md`（人设）、模型选择、渠道、工具策略和指定资料库；知识库、技能和笔记会被复制进 `data/partners/<id>/workspace/`，所以 [[RAG]]、技能、笔记、记忆这些工具在 Partner 身上照常工作。它**读取主人（你）的记忆，但只写自己的记忆** [S1]。

创建路径（Web UI 为主）[S1]：

1. 进入 **Partners** 面板 → 新建 Partner，填 SOUL.md（人设）、选模型与工具策略、指定资料库；
2. 添加渠道：渠道层是 schema 驱动的，支持 Feishu、Telegram、Slack、Discord、DingTalk、QQ/NapCat、WeCom、WhatsApp、Zulip、Mattermost、Matrix、Mochat、Microsoft Teams 等 15+ 个 [S1]；
3. 快速接入：飞书/Lark 应用、企业微信 AI 机器人可直接在浏览器里扫码创建；个人微信号也支持扫码登录 [S1]。

命令行同样可以管理 Partner 的生命周期 [S1]：

```bash
deeptutor partner list
deeptutor partner create
deeptutor partner start
deeptutor partner stop
```

> [!warning] 易错点
> 接 IM 渠道前先确认装了 Partner 渠道 SDK 依赖（`pip install -e ".[partners]"`），否则渠道会置灰或报 `missing SDK` [S4]。

##### 5.2.3 渠道排错：missing SDK、allow_from 显式 opt-in

接入渠道时最常碰到的两个坑，这里先标记，完整排错清单在第 7 章：

- **missing SDK**：某个渠道的 SDK 没装。用 `pip install -e ".[partners]"` 一次性补齐 Partner 相关渠道依赖 [S4]。
- **allow_from 显式 opt-in**：渠道的 `allow_from: []` 默认拒绝所有发送者。也就是说，即使渠道连上了，也不会接收任何人的消息，必须显式把自己（或允许的账号）加进 allowlist [S4]。

> [!tip] 大白话
> 把 `allow_from` 想成"门禁卡名单"——渠道接通只是"门修好了"，名单为空等于"谁都不放进来"。所以新配渠道后消息不进来，先查这一项，而不是怀疑 bot 挂了。

### 5.3 My Agents：调度外部 agent（Claude Code / Codex 等）与导入历史会话

My Agents 把"别的 agent"变成 DeepTutor 的上下文，做的是**两件不同的事** [S1][S10]：

1. **连接 live agent**：把本机上的 [[Claude Code]]、Codex、Antigravity CLI、Kimi CLI、opencode、MiMo Code、Hermes Agent、OpenClaw、DeepSeek Harness 这 9 种 harness（或你自己的 Partner）之一连进来，在聊天回合中途**实时咨询**它；
2. **导入历史会话**：把你过去的 Claude Code / Codex 对话按天导入，变成可搜索、可续聊、可在聊天里引用的"记忆资产"。

**实时咨询**这一块最值得玩：DeepTutor 不是把对话记录粘贴给那个 agent，而是**真的去运行它**，并把它的工作过程流式回传到 Activity 面板，底层由聊天循环里的 `consult_subagent` 工具多轮驱动 [S1][S10]。在聊天输入框用 **Agent 胶囊**（机器人图标）选中 agent，并设置"Max rounds DeepTutor may ask"（本轮咨询的往返上限）；或者直接输入 `@` 做单轮就地引用 [S1][S10]。

- 咨询 **Claude Code**：它在自己的工作目录里跑（读文件、grep、对真实仓库推理），工具调用流式进活动面板，DeepTutor 最后收拢结论 [S10]。
- 咨询 **Partner**：问题送进伙伴自己的会话，它用自己的人设、资料库和私有记忆工具（`partner_search`、`partner_read`）、技能（`read_skill`）作答；一个聊天线程绑定一个伙伴会话，追问延续同一段对话 [S10]。

**导入历史会话**：在 My Agents 里 `Add agent` → 起名 → **按天选择**要导入的日期；之后 `Refresh` 会重新同步所选天数并拉进当天新对话 [S1][S10]。引用时，DeepTutor 把导入会话当作**第三方对话记录**来读——"仍是他们的对话，DeepTutor 不会第一人称代入" [S1][S10]。

> [!tip] 大白话
> 把"consult_subagent"想成"给客户公司打电话咨询，而不是抄他们 PPT"。DeepTutor 是现场拨号、让对方真的干活、再把过程直播回来；导入历史会话则像"翻旧聊天记录当参考资料"——可以参考，但那不是你自己的话。

### 5.4 CLI 与 SDK：单轮 run、给其他 agent 驱动 DeepTutor

DeepTutor 的 CLI 有两副面孔：`deeptutor chat` 是给人用的交互式 REPL；`deeptutor run <capability> "<msg>"` 是给脚本和 agent 用的**单轮执行**。两者共享 `--capability` / `--tool` / `--kb` / `--config` 参数 [S1]。

```bash
# 单轮：让 deep_solve 能力解一道题，并挂上 reason 工具
deeptutor run deep_solve "Find d/dx[sin(x^2)]" --tool reason --format json

# 多轮串联：从 done 事件抓 session_id，后续 --session 复用同一会话上下文
SID=$(deeptutor run deep_research "Survey 2026 papers on RAG" \
  --config mode=report --config depth=standard --format json \
  | jq -r 'select(.type=="done").session_id')
deeptutor run deep_question "Quiz me on that survey" --session "$SID" --format json
```

加 `--format json` 后，每次 `run` 输出 **NDJSON——一行一个事件**（`content` / `tool_call` / `tool_result` / `done` 等），每一行都带 `session_id` 标签 [S1][S9]。这对"让 agent 驱动 DeepTutor"很关键：

- **headless 安全**：没有 TTY 时 `ask_user` 暂停会自动以空回复继续，不会挂起 [S1]；
- **多轮上下文**：从 `done` 事件抓出 `session_id`，再用 `--session "$SID"` 延续对话历史与分支 [S1][S9]；
- **被其他 agent 读取**：仓库根目录有一份约 200 行的 `SKILL.md` 交接文档，Claude Code / Codex / OpenCode 在项目根看到会自动读取；不认 `SKILL.md` 的框架（LangChain / AutoGen / 自定义循环），把 `deeptutor run --format json` 包成一个 tool 定义即可 [S1][S9]。

> [!tip] 大白话
> 把 `--format json` + `--session` 想成"给 agent 看的标准化对讲机协议"——每条消息一个固定格式、每个会话一个编号。所以外部 agent 能像打电话一样稳定地和 DeepTutor 连续对话，而不是靠人眼读终端输出。

### 5.5 EduHub 技能生态：Agent-Skills 格式、搜索/安装/发布、安全门

最后一块拼图是技能生态。DeepTutor 的技能用开放的 **Agent-Skills 格式**：一个技能 = 一个文件夹，根目录放 `SKILL.md`（YAML frontmatter + Markdown playbook），可选带支持文件 [S1][S7]。这个格式不是 DeepTutor 专属，任何说该格式的 registry 都能成为技能源；默认 hub 是官方教育技能社区 **EduHub**，裸 slug 或 `eduhub:` 前缀都解析到它 [S1][S7]。截至 2026-09-01 的快照，EduHub 有 72 个技能、4 大 track（Academics / Companions / Skills & Interests / For Educators），示例技能如 `socratic-tutor`、`flashcard-deck`、`essay-feedback`——数字以官网为准 [S8]。

**搜索与安装（免登录）**[S1]：

```bash
deeptutor skill search "socratic tutor"               # 搜默认 hub EduHub
deeptutor skill install socratic-tutor                # fetch → verify → register
deeptutor skill install eduhub:socratic-tutor@1.2.0   # 钉 hub + 版本
deeptutor skill list                                  # 本地技能及 hub 来源
```

浏览器里也能装：**Learning Space → Skills → Import from EduHub**，浏览目录直接下载进技能库 [S1]。EduHub 说 ClawHub 协议，所以同样支持 `clawhub:<owner>/<slug>` 全限定引用走 ClawHub；同名 slug 多个发布者时用全限定引用来区分 [S1]。自定义 registry 可在 `data/user/settings/skill_hubs.json` 里加 `type:"clawhub"` 或 `type:"command"`，并指定 `"default"` 给裸 slug 用哪个 hub [S1]。

**发布自有技能（需登录）**[S1][S12]：

```bash
deeptutor skill login                                 # 浏览器登录 EduHub
deeptutor skill publish ./my-skill                    # 交互：选 track + tags，然后上传
deeptutor skill update                                # 回滚或发布新版本
```

> [!warning] 易错点
> 不同文档里这个子命令存在单复数混用：README 官方命令表用单数 `deeptutor skill`，部分文档（EduHub 侧）会写 `deeptutor skills`。写作统一以 README 的**单数 `deeptutor skill`** 为准，遇到复数写法按同一命令理解即可 [S1][S7][S12]。

**导入安全门**：无论来源，每次导入在触碰工作区之前都过**同一道安全门** [S1]：

1. 先查 registry 的 **security verdict**，被标记的包拒绝，除非显式 `--allow-unverified`；
2. 归档做防御性解压（zip-slip / zip-bomb 防护）+ **文本/脚本后缀白名单**，二进制永不落进工作区；
3. frontmatter 规范化为 DeepTutor schema，并**剥离 `always:`**，下载的技能不能强制注入每个 system prompt；
4. 来源（hub、版本、verdict、安装时间）写入 **`.hub-lock.json`** 供审计与更新 [S1]。

> [!tip] 大白话
> 把安全门想成"机场海关"——每个技能包裹过同一套安检：查来源黑名单 → 防恶意解压、只放行文本类文件 → 卸掉危险插件 → 留一张安检记录单。所以装社区技能不用慌，但要理解装的是"陌生人寄来的包"。

**版本与代理发布**：版本按 semver 并存，安装用 `@version` 钉版，默认取 latest；rollback 把 latest 指针移到旧版本（不新建版本）[S12]。一旦 slug 存在，只有所有者（或 admin）能发新版或回滚；每次上传还会过静态扫描（可疑模式如 pipe-to-shell、env 外泄、原生可执行文件会被标记）[S12]。想让 Codex / Claude Code 代发技能，可以走"给 agent 在线指南 + `--dry-run` 前置验证"的流程，先 dry-run 通过再正式发布，再用 `inspect` / `search` / `install` 到临时目录验证 [S11][S13]。非 DeepTutor 的 agent 也能直接消费 EduHub：`npx eduhub install socratic-tutor` [S1][S8]。

### 本章小结

> [!summary] 总结
> - **Living Book** 用 Book Engine 把知识库 / 笔记 / 题库 / 聊天历史编译成 14 种块类型的"活书"，每页有 Page Chat；创建时先确认章节大纲，可导出 Markdown，`deeptutor book health` 跟踪源漂移 [S1]。
> - **Partners**（v1.4.3 前叫 TutorBot）是带 SOUL / 模型策略 / 资料库 / 私有记忆的持久陪伴体，本质是"有性格和电话号码的 Chat"；渠道层支持 15+ IM；接渠道先装 `.[partners]`，并显式配置 `allow_from` [S1][S4]。
> - **My Agents** 做两件事：连接 9 种 live harness（或自己的 Partner）在聊天中途实时咨询（`consult_subagent` / Agent 胶囊 / `@`）；以及按天导入 Claude Code / Codex 历史会话作为第三方对话记录引用 [S1][S10]。
> - **CLI / SDK**：`deeptutor run <capability> "<msg>"` 单轮执行，`--format json` 输出带 `session_id` 的 NDJSON 事件流，`--session "$SID"` 串联多轮；仓库根 `SKILL.md` 让 Claude Code / Codex / OpenCode 自动读取 [S1][S9]。
> - **EduHub** 用开放的 Agent-Skills 格式，搜索/安装免登录、发布需登录；每次导入过同一道安全门（verdict → 防御解压 + 后缀白名单 → 剥离 `always:` → `.hub-lock.json`）[S1][S7][S13]。

下一章进入"为什么"。我们把视角从"怎么玩"切到"它为什么这么设计"：Agent-Native 单循环、三层持久记忆、多引擎 RAG 与论文里的混合个性化引擎——理解这些，前面的进阶玩法就都有了底层依据。

---

## 架构与原理 —— 它为什么这么设计

前五章我们已经把 DeepTutor 部署起来，建了知识库、出过题、做过深研，还玩过 Living Book 和 Partners。但"能用"和"懂它为什么能这么用"是两回事。这一章把引擎盖打开，回答一个问题：DeepTutor 凭什么能让"辅导、解题、出题、研究、可视化、掌握度练习"这六类完全不同的功能，共享同一套运行时和记忆？答案是它做了一次彻底的重写——把一切收敛到"单一 Agent 循环"之上。

### 6.1 Agent-Native 架构重写：为什么是"单一 Agent 循环"

DeepTutor 在 v1.0.0-beta.1（2026-04-04）做了一次约 20 万行的 agent-native 架构重写：Tools + Capabilities 插件模型、CLI 与 SDK、TutorBot、Co-Writer、Guided Learning、持久记忆全部在同一套骨架上重建 [S1]。这不是为了炫技，而是解决一个很现实的问题：如果 Chat、Quiz、Research、Solve 各自写一套独立程序，那么每加一个功能就要复制一遍"怎么调模型、怎么挂知识库、怎么读写记忆"的逻辑，功能越多，系统越乱。

「单一 [[Agent]] 循环」的答案是：**不管表面上是哪种功能，底层都是同一条循环在跑**。这条循环刻意保持简单——模型先思考多轮，需要时调用工具，观察工具结果，最后以一条不带工具调用的消息收尾 [S1]。Chat 只是这条循环的默认能力；Quiz、Research、Solve 等不过是给同一条循环换了一套工具和提示词。

> [!tip] 大白话：Agent 循环
> 把这条循环想成一个"边想边查"的人：先动脑（思考多轮）→ 不确定就翻书查资料（调用工具）→ 看到结果接着想（观察结果）→ 想清楚了才开口说话（无工具消息收尾）。所以无论你点的是"提问"还是"出题"，背后都是同一个人在干活，只是他这次带上了"出题"的工具包。

##### 6.1.1 ChatOrchestrator：Web / CLI / SDK / Partner 所有入口汇聚

既然只有一条循环，就需要一个统一的"入口调度器"来承接所有请求。这个角色叫 ChatOrchestrator。Web 界面、CLI 终端、SDK 调用，甚至是 Partner 在 IM 渠道（飞书 / Telegram / 微信等）里收到的每条消息，最终都汇聚成一次普通的 ChatOrchestrator 回合，以事件驱动的方式流式输出结果 [S1]。

这里有个容易被忽视的设计：Partner 不是一套独立的机器人引擎。它是"一个有性格和电话号码的 Chat"——每条进来的消息都只是在 partner-scoped 的独立工作区里跑一次普通回合 [S1]。这样知识库、技能、笔记本、记忆这些工具在 Partner 里不需要任何特判就能工作，因为底层就是同一个 Agent 循环。

> [!note] 核心概念：一条循环，多个入口
> 用餐厅打比方：Web、CLI、SDK、Partner 是不同柜台，但点完单后都进同一个厨房（ChatOrchestrator）出菜。好处是——任何入口学会的能力，其他入口天然也会。

##### 6.1.2 工具模型：可开关工具 vs 上下文相关工具（自动挂载）

工具（Tools）是模型伸出去的"手"。DeepTutor 把工具分成两类 [S1]：

- **可开关工具（用户显式决定）**：`brainstorm`、`web_search`、`paper_search`、`reason`、`geogebra_analysis`，以及配好生成模型后才会出现的 `imagegen`、`videogen`。这些工具不是每轮都需要，由你在界面里决定开还是关。
- **上下文相关工具（自动挂载）**：`rag`、`kb_files`、`read_source`、`read_memory`、`write_memory`、`read_skill`、`load_tools`、`exec`、`web_fetch`、`ask_user`、`list_notebook`、`write_note`、`question_bank`、`github`、`consult_subagent`。只要当前回合具备相应上下文（比如你挂了知识库，`rag` 和 `read_source` 就会自动出现在工具列表里），它们就会自动装上，不需要你手动配置。

> [!tip] 大白话：可开关工具 vs 自动挂载工具
> 可开关工具像你自选的工具箱：你想带计算器就带上，不想带就不带。自动挂载工具像装修队：你一说要铺瓷砖，工头自动给你递上瓷砖刀，不用你开口。所以"自动挂载"的妙处是——模型自己判断这轮要不要用，你只决定大方向。

##### 6.1.3 两类上下文：sticky session context vs one-time references

工具知道了"能干什么"，还得知道"这次带着什么上下文"。DeepTutor 把上下文也分成两类 [S1]：

- **sticky session context（常驻会话上下文）**：子代理（subagent）、知识库、persona、模型、语音。这些挂在创作栏（composer toolbar）上，跨轮次持续生效——你这次选了某个知识库，下一轮它还在。
- **one-time references（一次性引用）**：文件、聊天历史、书、笔记本、题库、导入的 agent。这些从 `+` 菜单里选，只在当前这一轮生效，用完即走。

> [!tip] 大白话：两类上下文
> sticky 上下文是你固定的"工位"：桌上永远放着参考书、身份牌和选好的工具。one-time 引用是你临时从资料室借来的一本书：只看这一页，还完就放回去。这样既不会每轮重复挂载，也不会让临时材料污染后面的对话。

### 6.2 三层持久记忆：可读、可审计、可追溯

如果说单 Agent 循环解决了"能力怎么组织"，三层记忆解决的是"这个人怎么记得住你"。第 1 章讲过 DeepTutor 的三大支柱：持久化记忆、统一知识库、主动式智能体——本节拆解的是第一根支柱。

DeepTutor 的记忆系统刻意**不是**一个隐藏的向量库，而是文件背书、可读、可审计的三层结构 [S1]。为什么？因为向量库虽然检索快，但"里面存了什么、为什么记住了这句"你根本看不见。学习工具的记忆如果不可审计，就谈不上信任。

##### 6.2.1 L1 事件追踪 → L2 单面整理 → L3 跨面综合

三层记忆分别回答三个问题 [S1]：

| 层 | 存什么 | 文件形态 | 职责 |
|----|--------|----------|------|
| L1 | 原始事件 | 工作区镜像 + append-only 事件追踪 `trace/<surface>/<date>.jsonl` | 记流水账，只追加不改写 |
| L2 | 单面整理的事实 | `L2/<surface>.md`，引用 L1 | 把某一面（如 chat）的原始事件整理成事实 |
| L3 | 跨面综合 | `L3/<profile\|recent\|scope\|preferences>.md`，引用 L2 | 把多个面的 L2 综合成对你的画像 |

L2 引用 L1、L3 引用 L2，所以画像里没有任何一条是"无凭无据"的。追踪面覆盖 `chat`、`notebook`、`quiz`、`kb`、`book`、`partner`、`cowriter` [S1]。

> [!tip] 大白话：三层记忆
> L1 是监控录像（只记录不解释），L2 是值班日志（把录像里发生的事整理成"他今天问了三次傅里叶"），L3 是学期评语（综合所有日志得出"他可能在复习信号与系统"）。每一层评语都能翻回录像查证。

##### 6.2.2 Memory Graph：从综合主张回溯原始事件

L3 的"综合主张"凭什么可信？凭 Memory Graph。它以金字塔形式呈现：L3 综合在中心、L2 整理在中环、L1 原始事件在最外环 [S1]：

```
        ● L3 综合画像（中心）
       ● ● L2 单面事实（中环）
      ● ● ● L1 原始事件（外环）
```

任何一条综合主张，点下去都能一路回溯到产生它的那条原始事件 [S1]。这意味着当系统"记错了"你时，你不是面对一个黑盒，而是能顺着证据链找到是哪条对话或哪个知识点导致了误判。

> [!note] 核心概念：Memory Graph
> 它本质上是一条可追溯的证据链：主张 → 支撑它的 L2 事实 → 这些事实背后的 L1 事件。设计目的不是炫技，而是把"个性化"变成可纠错、可辩护的东西。

##### 6.2.3 read_memory / write_memory 的工作机制

记忆不光是后台攒数据，还作为工具暴露给 Agent 循环：

- **`read_memory`**：把四份 L3 文档拼起来喂给模型——`preferences`（偏好）由 `write_memory` 直接写入；`recent`、`profile`、`scope` 需要在 Memory Workbench 里手动整合，**没有"每 N 轮自动整合"** [S1]。
- **`write_memory`**：接受 1–240 字符的偏好文本，写入 L3 的 preferences [S1]。

> [!warning] 易错点：记忆不会自动整理成画像
> 很多人以为 DeepTutor 会像电影里的 AI 一样自动给你建档。实际上，只有"偏好"（preferences）是系统直写的，真正跨面的画像（recent / profile / scope）需要你在 Memory Workbench 手动确认整合。这是刻意为之——防止系统把你随口说的话无限放大成"你这个人"。

### 6.3 多引擎 RAG：为什么不是一套检索打天下

第 3 章我们已经亲手建过知识库，这一节回答"为什么 DeepTutor 不干脆只用一套检索"。

每种知识库（KB）都绑定一个检索引擎 [S1]：

- **LlamaIndex**（默认）：本地向量 + BM25，适合大多数教材、论文的常规语义检索。
- **PageIndex**：页面级引用 + 推理检索，回答需要跨文档推理的问题时更准。
- **GraphRAG / LightRAG**：基于知识图谱的检索，适合关系密集的材料，比如概念之间互相引用的学科。
- **LightRAG Server**：把检索外接到一个远程 LightRAG 实例（HTTP），适合已有独立检索服务的部署。
- **腾讯 IMA / MarginNote 4 / 链接的 Obsidian vault**：直接对接你在别的工具里已经整理好的资料，原地读取，不重建索引。

为什么不是一套打天下？因为"教材"和"概念网"、"单篇论文"和"整库关联"的检索需求不一样。用向量检索去找"第 3 章第 2 节讲过什么"很合适，但要回答"A 理论和 B 理论有什么关系"，知识图谱更擅长。把引擎做成 KB 的可选项，等于让材料决定检索方式，而不是让一套检索方式迁就所有材料。

> [!tip] 大白话：多引擎 [[RAG]]
> 把检索引擎想成图书馆的查书方式：按页码翻（向量检索）适合找一句话，顺着"相关推荐"走（[[GraphRAG]] 知识图谱）适合搞清概念关系。你手里的资料是教材还是概念地图，就该用对应的查法。DeepTutor 让你给每本书选查法，而不是逼你用同一种方式查所有的书。

### 6.4 论文设计：混合个性化引擎与 TutorBench

这一节回到论文本身。DeepTutor 的论文《DeepTutor: Towards Agentic Personalized Tutoring》（arXiv:2604.26962）给出了学术侧的设计骨架：一个**混合个性化引擎（hybrid personalization engine）**，把静态知识锚定与动态学习者记忆耦合起来，持续适应学习者的演变需求 [S2]。

##### 6.4.1 引文锚定问题辅导 + 难度校准题目生成

论文把整个框架统一成两件事 [S2]：

- **引文锚定的问题辅导（citation-grounded problem tutoring）**：给学习者的讲解必须锚定在可引用的材料上，而不是模型凭空发挥。这与产品里 `rag` / `read_source` 工具保证的"带引用回答"是同一个设计意图。
- **难度校准的题目生成（difficulty-calibrated question generation）**：出的题要贴合学习者当前水平，而不是一刀切。这与第 3 章 Ask Questions / Quiz 的难度校准一脉相承。

同一个性化基底还被论文扩展到了自适应学习工作流、交互式书籍、主动式多通道辅导 agent——也就是产品里 Guided Learning / Mastery Path、Living Book、Partners 这些功能在论文里的抽象原型 [S2]。

##### 6.4.2 评测方法与结论（个性化指标 +10.8%、通用 agentic reasoning +29.4%）

论文还提出了 **TutorBench**：一个交互式评测基准，包含基于五个大学课程领域定制出来的学习者画像 [S2]。配套的是一套 **LLM 首人称交互评测协议**——用画像驱动的学生模拟器来扮演真实学生，与系统交互打分，从而在"个性化辅导"这种难以自动评分的任务上得到可复现的评测。

结论是两组数字 [S2]：

- **个性化指标平均提升 10.8%**。
- 在五个 backbone 模型上的**通用 agentic reasoning 提升 29.4%**。

> [!note] 核心概念：为什么用"学生模拟器"来评测
> 个性化辅导没有标准答案，难以用选择题判分。用画像驱动的学生模拟器，等于让"一个符合画像的虚拟学生"去体验系统，再用协议化指标打分。这样既能量化"对这个人够不够个性化"，又不依赖真人付费评测。

### 6.5 论文设计与当前产品的版本差异（术语与功能演进）

论文（v3 修订于 2026-07-09）和当前 README（v1.6.x）在时间上不是同一刻，功能演进带来了一些术语变化 [S1][S2]。最典型的是：

- **TutorBot → Partners**：早期产品里叫 TutorBot，v1.4.3 起演进为 Partners，底层也换成生产级 IM 管线 [S1]。论文里的"主动式多通道辅导 agent"对应到今天就是带 SOUL、模型策略、资料库、记忆与 15+ IM 渠道的 Partners。
- **论文的"抽象设计" vs 产品的"具体落地"**：论文把个性化表达成一个通用框架（自适应学习工作流、交互式书籍、多通道辅导 agent），产品则把这些抽象分别落成 Mastery Path / Guided Learning、Living Book、Partners 等具体可操作的功能。
- **架构沿革**：v1.0.0-beta.1 是一次约 20 万行的 agent-native 重写，v1.4.3 又把 Chat 收敛到单一 agent loop [S1]。所以你现在看到的一切，都建立在"单循环 + 工具 + 记忆"这条主线上。

> [!warning] 版本漂移提示
> 本文以 v1.6.2 为锚点。DeepTutor 迭代极快（2026-08 一个月内连发 v1.5.7 → v1.6.2），术语和功能随时可能再演进。阅读时以官方文档（deeptutor.info / GitHub README）为准。

### 6.6 开放生态与许可：Agent-Skills 格式、EduHub、Apache-2.0

最后看设计哲学的外围：DeepTutor 不想做一座孤岛。

技能（Skills）采用开放的 **Agent-Skills 格式**——一个带 `SKILL.md`（YAML frontmatter + Markdown）和可选参考文件的文件夹，格式本身与 DeepTutor 无关，任何说这个格式的注册中心都能成为技能来源 [S1]。默认中心是教育向的 **EduHub**，同时兼容 ClawHub。导入有安全门：先查注册中心安全判定 → 防御式解压（zip-slip / zip-bomb 防护）→ 后缀白名单剥离二进制 → 剔除 `always:` 防止技能强制进入系统提示 → 把来源信息写进 `.hub-lock.json` 供审计 [S1]。

许可协议是 **Apache-2.0**（README 与 LICENSE 文件明确标注）[S1]。项目也明确站在一堆上游开源项目肩膀上：RAGLAB、MoT（原 TutorBot 的超轻量 agent 引擎）、LightRAG、OpenAGI、Auto-DeepResearch、ClawHub、OpenCode、Codex、Manim 等 [S1]——这和"单一循环 + 开放技能格式 + 可审计记忆"是同一个哲学：尽量少造私有轮子，把能力开放出去。

> [!tip] 大白话：为什么在乎开放格式
> 技能格式开放，就像插座接口统一——任何一个符合标准的插头都能插进 DeepTutor 的插座，反之 DeepTutor 的技能也能被 Claude Code、Codex 等别的工具用。协议开放 + Apache-2.0，等于告诉社区：这个系统不是围墙花园，你的技能、你的数据、你的贡献都属于你。

### 本章小结

- DeepTutor 在 v1.0.0-beta.1 做了约 20 万行的 agent-native 重写，把 Chat、Quiz、Research、Solve 等全部功能收敛到同一条"思考 → 调工具 → 观察 → 收尾"的单一 Agent 循环上，ChatOrchestrator 是所有入口（Web / CLI / SDK / Partner）的统一调度器 [S1]。
- 工具分两类：可开关工具由你决定，上下文相关工具在具备条件时自动挂载；上下文分两种：sticky session context 跨轮常驻，one-time references 单轮即用 [S1]。
- 三层记忆（L1 事件 → L2 单面 → L3 综合）是文件背书而非隐藏向量库，Memory Graph 让每条综合主张都能回溯到原始事件；`read_memory` 拼装 L3，`write_memory` 直写 1–240 字符偏好 [S1]。
- 多引擎 RAG 让每种知识库绑定最合适的检索引擎（LlamaIndex / PageIndex / GraphRAG / LightRAG / Obsidian 等），不搞一刀切 [S1]。
- 论文（arXiv:2604.26962）提出混合个性化引擎、引文锚定问题辅导 + 难度校准题目生成，用 TutorBench 与学生模拟器评测，个性化指标 +10.8%、通用 agentic reasoning +29.4% [S2]。
- 当前产品比论文走得更远：TutorBot 已演进为 Partners，开放 Agent-Skills 格式 + EduHub 生态 + Apache-2.0 许可 [S1]。

下一章把视角从原理拉回实战，整理一份随用随查的避坑与排错速查表——部署、模型接入、知识库索引、Partner 渠道的高频问题一次性收拢。

---

## 避坑与排错速查

第 2 章带你用一条 `docker run` 命令把 DeepTutor 跑通了；本章反过来，专治"部署之后踩到的坑"。如果你已经顺利跑起来，这一章可以先跳过，遇到报错时再回来按症状查。整体思路遵循官方文档的排错流程 [S4]：**先跑健康检查，再看日志，最后针对症状修**。7.1 先给一套通用的排查工具，7.2–7.6 按问题类别给方案，7.7 是一张可直接照做的速查表。内容以写作时的 **v1.6.2** 为锚，命令与配置项以官方文档为准。

### 7.1 排错工具链：deeptutor doctor、日志 tail、端口检查

官方文档给的第一条建议是：安装行为不对，先跑一次 `deeptutor doctor`，看缺了什么 [S4]。

```bash
deeptutor doctor          # 本机健康检查：配置、依赖、端口、各服务状态
deeptutor doctor --online # 额外联网探测模型 provider，验证 API key 是否有效
```

> [!tip] 大白话
> 把 `deeptutor doctor` 想成去医院做体检——它不负责治病，但会告诉你"哪项指标异常、缺哪个零件"。`--online` 相当于多查一项"联网验血"，能确认模型 API key 到底通不通。所以排错第一步永远是先体检，而不是瞎猜。

日志是第二件法宝。运行日志统一写在 `data/user/logs/deeptutor.jsonl`（持久化在 `deeptutor-data` volume 里），可以按关键字过滤 [S4]：

```bash
tail -f data/user/logs/deeptutor.jsonl                 # 看全部日志并持续跟踪
tail -f data/user/logs/deeptutor.jsonl | grep -i kb    # 只看知识库相关
```

用 [[Docker]] 部署时，日志直接用 docker 命令看 [S3]：

```bash
docker logs -f deeptutor           # 跟踪容器日志
docker logs deeptutor | tail -30   # 只看最后 30 行（排错最常用）
```

第三件是端口检查。报"端口被占"时，需要找出到底是谁占用了 3782/8001 [S4]：

```bash
# macOS
lsof -i:3782
# Linux
ss -ltnp | grep :3782
```

```powershell
# Windows PowerShell
Get-NetTCPConnection -LocalPort 3782
```

> [!tip] 实践建议
> 需要去社区求助时，官方建议附上三样东西 [S4]：安装路径（Docker / PyPI / 源码 / 纯 CLI）、`deeptutor config show` 的输出、`data/user/logs/deeptutor.jsonl` 的最后 40 行（Docker 则附 `docker logs deeptutor | tail -40`）。贴日志而不是复述症状，别人才能帮你定位。

### 7.2 启动类问题：端口被占、容器立刻退出、前端空白页

**端口被占**。典型报错有两个 [S3][S4]：

- 本地 Python 启动：`Address already in use :3782`（或 `:8001`）；
- Docker 启动：`Bind for 0.0.0.0:3782 failed: port is already allocated`。

用 7.1 的端口检查命令找出占用进程，干掉它，或者换端口。换端口有几种改法 [S3][S4]：

```bash
# 1) Docker：只改 -p 左侧的宿主机端口
docker run --rm -p 127.0.0.1:8088:3782 -v deeptutor-data:/app/data ghcr.io/hkuds/deeptutor:latest
# 2) Docker 专用端口变量
DEEPTUTOR_DOCKER_FRONTEND_PORT=4000 DEEPTUTOR_DOCKER_BACKEND_PORT=18001
# 3) 非 Docker 启动时用环境变量
BACKEND_PORT=18001 FRONTEND_PORT=4000 deeptutor start
```

也可以编辑 `data/user/settings/system.json` 里的 `backend_port` / `frontend_port` [S4]。

**容器立刻退出**。第一反应是看日志 [S3]：

```bash
docker logs deeptutor | tail -30
```

一个反直觉的常识：**无效的 LLM 凭据只会在日志里记 warning，不会让后端启动失败** [S3]。如果容器退了，说明日志里另有致命错误，照着最后 30 行排查。源码树 Compose 部署时，先确认 `./data:/app/data` 的 bind mount 和宿主机目录权限（`mkdir -p data`）再重试 [S4]。另外容器可能显示 `Running` 但 `unhealthy`——健康检查从容器内探测后端并设了 60 秒 start period，启动偏慢会被标记；此时直接运行镜像内置健康检查 `docker exec deeptutor python /app/healthcheck.py`，再配 `docker logs deeptutor | tail -40` [S4]。

**前端空白页**。打开浏览器开发者工具（Windows 上按 F12）看 Console 标签，三种常见原因 [S4]：

- **CORS 报错**：前端一个 origin、后端另一个 origin，后端没把前端加进允许列表。编辑 `data/user/settings/system.json` 把前端 origin 加进 `cors_origins`。
- **`/_next/...` 404**：静态 bundle 没构建。源码方式运行的话：`cd web && npm run build`。
- **后端连不上**：用 `curl http://localhost:8001/` 验证是否返回 JSON。单容器部署默认由容器内代理把 `/api/*` 转发给后端，出现这个一般先确认容器还活着。

> [!warning] 易错点
> Windows + Docker Desktop 下，容器处于异常状态（端口反复被占、前端打不开）时，先**重启 Docker Desktop** 再重试 `docker run`，不要急着删 volume。很多"怪问题"是 Docker 引擎的残留状态导致的，重开引擎往往就好了。

### 7.3 模型接入类问题：provider probe 401、host.docker.internal 解析、embedding endpoint

**provider probe 401**。配置模型时 probe 报 `HTTPError 401 Unauthorized`，几乎都是 API key 前缀不对 [S4]：

| Provider | key 前缀 / 注意点 |
|---|---|
| OpenAI | `sk-`；project key 是 `sk-proj-` |
| Anthropic | `sk-ant-` |
| Azure OpenAI | 在 设置 → Models → LLM 当前 profile 里填 **API Version** |
| Google Gemini | `AIza` |
| Ollama / 本地 OpenAI 兼容 | **key 留空或用 `none`**，Base URL 指本地，如 `http://localhost:11434/v1` |

修好后重跑 `deeptutor init` 重新输入 key，或直接编辑 `data/user/settings/model_catalog.json` [S4]。另外，配置时若提示 `Failed to fetch /models`，那是 DeepTutor 拉取 provider 的模型列表被网络挡了——这是**非致命**警告，向导会 fallback 到内置常见模型列表继续 [S4]。

> [!tip] 大白话
> 把 API key 想成临时工牌，`sk-`、`sk-ant-`、`AIza` 就是不同公司的工牌颜色。你把 A 公司的工牌刷到 B 公司的门禁（provider），门禁当然回 401——不是工牌坏了，是发错工牌了。检查前缀等于对一下工牌颜色。

**`host.docker.internal` 解析不了**（[[Docker]] 连本地 [[Ollama]] 时）。容器里的 `localhost` 指容器本身，要访问宿主机得用 host gateway [S3][S4]：

| 宿主系统 | Base URL |
|---|---|
| macOS / Windows（Docker Desktop） | `http://host.docker.internal:11434/v1`，通常**无需** `--add-host` |
| Linux | `http://172.17.0.1:11434/v1`（docker0 网桥）或宿主机 LAN IP；也可在 compose 里加 `extra_hosts: "host.docker.internal:host-gateway"` |

**Embedding endpoint 报错**。Embedding 适配器会**原样使用** profile 里的 Base URL，所以必须填完整 endpoint，而不是只填 API root [S4]：

| Provider | 错误（缺路径） | 正确 |
|---|---|---|
| OpenAI | `https://api.openai.com/v1` | `https://api.openai.com/v1/embeddings` |
| Cohere | `https://api.cohere.com` | `https://api.cohere.com/v2/embed` |
| Jina | `https://api.jina.ai/v1` | `https://api.jina.ai/v1/embeddings` |
| Ollama（本地） | — | `http://host.docker.internal:11434/api/embed` |

> [!warning] 易错点
> LLM 的 Base URL 填到 `/v1` 就够，Embedding 却要填到 `/embeddings` 或 `/embed`。两者的完整程度不一样，别把 LLM 的填法照搬到 Embedding——这是维度报错之外第二高频的 embedding 配置失误。

### 7.4 知识库与索引问题：Embedding dimension mismatch、KB 卡 indexing

**`Embedding dimension mismatch`**。你在建库之后换过 embedding 模型，缓存里的向量维度对不上新模型的维度 [S4]。修复：Web UI 里 **Knowledge → 选 KB → Index versions → Re-index now**。注意重建索引**没有暴露成 CLI 命令**，只能走 Web UI [S4]。

> [!tip] 大白话
> 把向量维度想成"格子的大小"。第一次建库用的模型每个向量塞 384 格，后来换了个塞 1536 格的模型，老索引的格子对不上新格子——查询时自然报 dimension mismatch。Re-index now 等于按新格子把书重新抄一遍，索引就统一了。

如果重建索引后维度不匹配**仍然存在**，说明 KB store 里有过期的配置文件，需要删库重建 [S4]：

```bash
deeptutor kb delete physics --force
deeptutor kb create physics --doc chapter1.pdf
```

**KB 卡在 `indexing` 状态**。索引是后台任务跑的，先看日志定位 [S4]：

```bash
tail -f data/user/logs/deeptutor.jsonl | grep -i kb
```

常见三个原因 [S4]：embedding provider 返回 **429 限流**（用更小的 batch 重试）；**embedding host 不可达**（查网络）；**PDF parser 失败**（确认文件没有密码保护）。

### 7.5 Windows 环境专项：VS Build Tools、pip 慢

本章主线是 Docker 路径，这两个坑主要出现在 PyPI / 源码安装路径上——先记着，以后走 Python 安装时会遇到 [S4]。

**`Microsoft Visual C++ 14.0 is required`**。某个依赖在 Windows 上回退到了源码构建。安装 [Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/)，勾选 "Desktop development with C++" workload，然后重试安装 [S4]。

**`pip install` 慢到爆**。网络慢的话换本地 PyPI 镜像。中国大陆用户直接配清华源 [S4]：

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 7.6 Partner 渠道与认证：missing SDK、allow_from 显式 opt-in、auth_secret 丢失

**Partner channel 置灰 / 报 "missing SDK"**。某个渠道的 SDK 导入不进来（比如 `No module named 'lark_oapi'`），Channels 面板会把该渠道置灰，从 CLI 启动 partner 也会报同样的错 [S4]。装齐依赖集并重启 DeepTutor：

```bash
# 源码安装：全部内置 channel SDK
pip install -e ".[partners]"
# PyPI 安装用这条
pip install -U "deeptutor[partners]"
# 只补 Matrix 渠道（加密房间用 ".[matrix-e2e]"，需要 libolm）
pip install -e ".[matrix]"
```

注意：纯 CLI 包（`packaging/deeptutor-cli`）不定义任何 extras，要从源码 checkout 装 requirements 镜像：`python -m pip install -r requirements/partners.txt` [S4]。

**Partner 连上了但不响应**。检查 channel card 里的 `allow_from` [S4]：

```yaml
weixin:
  enabled: true
  allow_from:   # 空 = 全部拒绝
    - "*"       # 允许所有人（测试期先这样，稳定后换成具体 user/chat ids）
```

默认 `allow_from: []` **拒绝所有人**——你必须显式 opt in [S4]。这是"连上了却没反应"最常见的根因。

> [!warning] 易错点
> `allow_from` 想成小区门卫手里的**访客名单**。默认名单是空的，意味着谁按门铃都不放行（虽然门铃本身是通的）。"渠道 `enabled: true`"只代表门铃通电，不代表名单里有你。一定要在 `allow_from` 里显式写 `"*"` 或具体 ID，否则渠道永远"已连接但不干活"。

**重启后所有 API 调用都 401**。`data/system/auth/auth_secret` 丢失或被重新生成了，所有 JWT 都失效 [S4]。从备份恢复该文件，或接受新 secret 让所有用户重新登录。注意项目根目录的 `.env` **不会被运行时自动加载**，别指望在那里配 secret [S4]。

> [!tip] 大白话
> 把 `auth_secret` 想成签发临时工牌（JWT）的**母卡印章**。印章丢了重新刻一个，所有旧工牌（登录态）就全部作废——于是每个 API 调用都变 401。要么找回旧印章（从备份恢复），要么接受换新章后全员重新领工牌（重新登录）。

顺带两个认证小坑（都来自官方文档 [S4]）：第一个用户没被提升为 admin，编辑 `data/system/auth/users.json` 把该用户设成 `"role": "admin"` 再重启；登录成功又跳回 `/login`，多半是 auth cookie 没设置成功——检查 `cookie_secure` 是否与环境（本地 HTTP vs HTTPS）匹配，或浏览器拦了第三方 cookie 而你在子域上部署。

### 7.7 高频问题速查表汇总

下表把本章全部症状收拢成一张速查表，遇到问题先在这里定位，再回对应小节看展开：

| 症状 | 可能原因 | 快速排查 | 修复 |
|---|---|---|---|
| `Address already in use :3782/:8001` / `Bind for 0.0.0.0:3782 failed` | 端口被其他进程占用 | `Get-NetTCPConnection -LocalPort 3782` / `lsof -i:3782` / `ss -ltnp \| grep :3782` | 杀掉占用进程，或改端口（`-p` 左侧 / `system.json` / `DEEPTUTOR_DOCKER_*_PORT`） |
| 容器立刻退出 | 日志里有致命错误（LLM 凭据无效只 warning，不致命） | `docker logs deeptutor \| tail -30` | 按日志定位；Compose 部署先确认 `./data` bind mount 与权限 |
| 前端空白页 | CORS / `/_next` 404 / 后端没起 | 浏览器 Console 看报错；`curl http://localhost:8001/` | 加 `cors_origins`；`npm run build`；确认后端存活 |
| provider probe 401 | API key 前缀不符 | 核对 key 前缀（`sk-` / `sk-ant-` / `AIza`，Ollama 留空或 `none`） | 重跑 `deeptutor init` 或编辑 `model_catalog.json` |
| `host.docker.internal` 解析不了 | Linux 缺 host gateway | 确认宿主系统 | Windows/macOS 直接用；Linux 用 `172.17.0.1` 或 `extra_hosts` |
| Embedding endpoint 报错 | Base URL 没填完整路径 | 对照完整 endpoint 表 | 填到 `/v1/embeddings`、`/v2/embed`、`/api/embed` |
| `Embedding dimension mismatch` | 建库后换过 embedding 模型 | 检查是否重建过索引 | Web UI → KB → Index versions → **Re-index now** |
| 重建索引后仍 dimension mismatch | KB store 有过期配置 | 无 | `deeptutor kb delete <kb> --force` 后 `kb create` 重建 |
| KB 卡 `indexing` | 429 限流 / embedding host 不可达 / PDF 有密码 | `tail -f data/user/logs/deeptutor.jsonl \| grep -i kb` | 减小 batch；查网络；换无密码 PDF |
| `Microsoft Visual C++ 14.0 is required` | 依赖回退源码构建（Windows） | 看安装报错 | 装 VS Build Tools，勾 "Desktop development with C++" |
| `pip install` 慢 | 网络慢 | 无 | `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple` |
| Partner channel 置灰 / "missing SDK" | 渠道 SDK 未安装 | Channels 面板看 import 错误 | `pip install -e ".[partners]"` 后重启 |
| Partner 连上但不响应 | `allow_from: []` 默认拒绝全部 | 检查 channel card 的 `allow_from` | 显式写 `"*"` 或具体 ID |
| 重启后全 API 401 | `auth_secret` 丢失 / 重建 | 检查 `data/system/auth/auth_secret` | 从备份恢复，或接受新 secret 全员重登 |

### 本章小结

> [!summary] 本章小结
> - 排错先走工具链：`deeptutor doctor`（`--online` 验 provider）→ `docker logs deeptutor \| tail -30` → 端口检查（Windows 用 `Get-NetTCPConnection`）[S3][S4]。
> - 三类启动问题各有套路：端口被占改映射或改端口；容器退出看日志（LLM 凭据无效不致命）；前端空白页看浏览器 Console 定位 CORS / `/_next` 404 / 后端存活 [S3][S4]。
> - 模型接入三大坑：401 查 key 前缀；`host.docker.internal` 只在 Linux 需要处理；Embedding endpoint 必须填完整路径 [S4]。
> - 知识库问题记住"换模型→重建索引"：`Re-index now` 只能走 Web UI；重建无效就 `kb delete --force` 后重建；卡 indexing 去日志里查 429 / host 可达性 / PDF 密码 [S4]。
> - Partner 与认证：渠道置灰装 `[partners]` extras；不响应检查 `allow_from` 显式 opt-in；全员 401 查 `auth_secret` 是否丢失 [S4]。

到这里，从第 1 章的认识、第 2 章的上手、第 3–5 章的玩法、第 6 章的原理，到本章的排错，你已经拿到 DeepTutor 的完整使用地图。本章不需要通读——把它当成"随用随查"的工具页，遇到报错先翻 7.7 速查表定位，再回对应小节看展开即可。
