---
title: Docker 快速上手 —— 一条命令跑通 DeepTutor
tags:
  - obsidian/学习笔记
  - github项目
  - ai/agent
  - docker
created: 2026-09-01
updated: 2026-09-01
status: 完成
source_project: deeptutor
---

# Docker 快速上手 —— 一条命令跑通 DeepTutor

第 1 章我们把 DeepTutor 定义为"有记忆、有知识库、会主动辅导"的 Agent-Native 学习工作区，但那还是概念。这一章彻底落地：借助 [[Docker]]，用一条 `docker run` 命令把完整应用跑起来，再配上模型，完成第一次对话。路线是"准备环境 → 选对安装路径 → 逐行看懂部署命令 → 接入模型（云端为主，本地 [[Ollama]] 可选）→ 验证首聊 → 学会管理容器"。全书以 Windows + Docker Desktop 为主线，看完整章，你的浏览器里会有一个真正能对话的 DeepTutor。写作时以 v1.6.2 为锚，新版本请以官方文档为准。

## 2.1 环境准备：Docker Desktop（Windows）与镜像确认（ghcr.io/hkuds/deeptutor:latest）

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

## 2.2 四种安装路径对比（PyPI / 源码 / Docker / CLI Only），为什么首选 Docker

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

## 2.3 部署命令逐行拆解

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

### 2.3.1 端口映射：为什么只需暴露 3782（前端中转 /api、/ws 到后端 8001）

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

### 2.3.2 数据持久化：deeptutor-data volume 与 data/user/settings/ 布局

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

## 2.4 模型接入：设置 → Models

浏览器打开 <http://127.0.0.1:3782>，进入 **设置 → Models**。给 DeepTutor 配模型，核心就一个 LLM profile：**Base URL / API key / model 名称**，保存后 DeepTutor 会做一次 provider probe（连通性探测）[S1][S4]。这个页面有点像手机的"输入法设置"——不是配一次就完事，而是可以存多套 profile 随时切换，比如日常用云端 DeepSeek 省钱、推理难题切到 Anthropic、断网时切到本地 Ollama。

- 只配 **LLM** 就能聊天、解题、出题。
- 想用知识库 / [[RAG]]（第 3 章）再配一个 **Embedding** profile。
- v1.6.x 里可以用 **Connections** 一次性录入某厂商凭证，自动镜像到该厂商能服务的所有服务（LLM、Embedding 等），不用重复粘贴 [S1]。

> [!note] 核心概念
> provider probe 是"保存即探测"：DeepTutor 拿着你填的 Base URL 和 key 去厂商打一个测试请求。它通过，说明配置大概率没问题；报 `401`，多半不是网络问题，而是 **key 前缀不对** [S4]。

### 2.4.1 云端 API 为主：OpenAI / DeepSeek / Anthropic 的 Base URL 与 key 前缀

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

### 2.4.2 本地 Ollama 补充：host.docker.internal（Windows/macOS 免加 --add-host，Linux 需 extra_hosts）

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

### 2.4.3 Embedding 配置：完整 endpoint 规则（/v1/embeddings、/v2/embed 等）

Embedding 是知识库 / [[RAG]] 的基石，第 3 章建知识库时必需。它的坑和 LLM 不同：**Embedding adapter 会原样使用 profile 里的 Base URL，所以必须填完整 endpoint，而不是只填 API root** [S4]。

| Provider | 错误（只填 API root） | 正确（完整 endpoint） |
|----------|------------------------|------------------------|
| OpenAI | `https://api.openai.com/v1` | `https://api.openai.com/v1/embeddings` |
| Cohere | `https://api.cohere.com` | `https://api.cohere.com/v2/embed` |
| Jina | `https://api.jina.ai/v1` | `https://api.jina.ai/v1/embeddings` |
| Ollama（容器内访问宿主机） | `http://host.docker.internal:11434` | `http://host.docker.internal:11434/api/embed` |

> [!warning] 易错点
> 记住规则：OpenAI 兼容系一般是 `/v1/embeddings`，Cohere 是 `/v2/embed` [S4]。填错 endpoint 会一直报 Embedding 错误；如果之后换了 embedding 模型再建库还报 `Embedding dimension mismatch`，那是索引维度缓存对不上，需要在第 3 章的知识库界面做 **Re-index now** 重建索引（第 7 章也会讲到）。

## 2.5 首次对话验证：Web UI 与 CLI 双路径

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

## 2.6 容器生命周期：后台运行、日志、停止、升级、彻底重置 volume

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

## 2.7 本节小结：部署验收清单

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
