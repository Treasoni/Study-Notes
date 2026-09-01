# DeepTutor 深度研究素材（P2）

> 阶段：P2 深度收集（learning-note-flow / run_id: deeptutor）
> 收集日期：2026-09-01
> 范围：方向 B（部署与上手使用）+ 方向 C（架构与原理）
> 抓取：`crawl4ai` 本地爬虫（6 个源），原始抓取见 `sources/*.md`

---

## 一、范围与源表

| ID | 源 | 类型 | Tier | 抓取内容 |
|----|----|------|------|----------|
| S1 | [GitHub README](https://github.com/HKUDS/DeepTutor) | 官方仓库 | 1 | 完整 README：功能、4 种安装路径、CLI 命令、架构、Partner/记忆/多引擎 RAG 详解 |
| S2 | [arXiv:2604.26962 摘要](https://arxiv.org/abs/2604.26962) | 学术论文 | 1 | 摘要：混合个性化引擎、TutorBench、评测结论（2026-04-10 提交，v3 2026-07-09） |
| S3 | [官方文档·Docker 部署](https://docs.deeptutor.info/zh-cn/get-started/docker/) | 官方文档 | 1 | 单容器部署、端口映射、本地 LLM 接入、升级与常见错误 |
| S4 | [官方文档·故障排查](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/) | 官方文档 | 1 | 端口/进程、LLM/Embedding 401、知识库、Docker、Python 安装、前端、Partner、记忆/RAG 精度 |
| S5 | [CSDN·部署与实战](https://blog.csdn.net/weixin_27230891/article/details/160874436) | 技术博客 | 2 | 产品定位与设计哲学（中段付费截断，只取有效部分） |
| S6 | [BAAI 智源·在线教程](https://hub.baai.ac.cn/view/53930) | 社区平台 | 2 | 功能概览、RAG/多智能体定位、HyperAI 在线体验教程 |

去重后共 6 源（Tier 1 ×4，Tier 2 ×2）。

---

## 二、产品定位与核心功能（claim → 源）

| # | 核心 claim | 源 |
|---|-----------|-----|
| 1 | DeepTutor 是 **Agent-Native 终身个性化辅导**学习工作区，一个运行时统一"辅导/解题/出题/研究/可视化/掌握度练习" | S1, S2 |
| 2 | 核心功能面：Chat、Ask Questions、Quiz、Research（深研）、Visualize、Solve、Course Study、Mastery Path、Immersive Reading/Watching 共享同一能力运行时与会话上下文 | S1 |
| 3 | **多引擎知识库**：LlamaIndex（默认，本地向量+BM25）、PageIndex（推理检索）、GraphRAG、LightRAG、LightRAG Server、腾讯 IMA、MarginNote 4、链接的 Obsidian vault；每个 KB 绑定一个引擎 | S1 |
| 4 | **三层可审计记忆**：L1 工作区镜像+事件追踪、L2 单面整理事实、L3 跨面综合；Memory Graph 可把每条综合主张追溯回原始事件 | S1 |
| 5 | **Partners/TutorBot**：带独立 SOUL、模型策略、资料库、记忆与渠道的持久陪伴体，支持 Feishu/Telegram/Slack/Discord/微信/企业微信/Zulip/Mattermost/Matrix 等 15+ IM 渠道 | S1 |
| 6 | **My Agents**：可现场调度 Claude Code/Codex/Antigravity/Kimi/opencode/MiMo/Hermes/OpenClaw/DeepSeek 等外部 agent，或导入历史会话作为上下文 | S1 |
| 7 | **Book Engine（Living Book）**：把 KB/笔记/题库/聊天历史编译成可交互"活书"，含 14 种块类型（文本/callout/测验/闪卡/时间线/代码/图表/交互 HTML/动画/概念图等），可导出 Markdown | S1 |
| 8 | **EduHub 技能生态**：Agent-Skills 开放格式（SKILL.md），内置教育技能市场，兼容 ClawHub，可发布自有技能 | S1 |
| 9 | 里程碑：2025-12-29 正式发布；39 天 10k stars；111 天 20k stars；当前 v1.6.2（2026-08-31）、38.2k stars、4.8k forks | S1, S6 |
| 10 | 定位与痛点：解决知识碎片化、学习缺乏连续性、AI 工具过于被动（"持久化记忆+统一知识库+主动式智能体"三支柱） | S5 |

---

## 三、部署与上手（方向 B 核心）

### 3.1 四种安装路径

| 路径 | 命令要点 | 前置要求 | 适用 |
|------|----------|----------|------|
| PyPI 安装 | `pip install -U deeptutor` → `deeptutor init` → `deeptutor start` | Python 3.11–3.13 + Node.js 20+（Web 前端由 start 拉起） | 完整 Web + CLI，不用 clone |
| 源码安装 | `git clone` → venv → `pip install -e .` → `(cd web && npm ci --legacy-peer-deps)` → `deeptutor start --dev` | Python 3.11–3.13 + Node.js 22 LTS | 开发/改源码 |
| **Docker（推荐上手）** | `docker run --rm --name deeptutor -p 127.0.0.1:3782:3782 -v deeptutor-data:/app/data ghcr.io/hkuds/deeptutor:latest` | Docker（Desktop 可满足） | 一条命令跑通，推荐 |
| CLI Only | 源码 `pip install -e ./packaging/deeptutor-cli` → `deeptutor init --cli` → `deeptutor chat` | Python 3.11+ | 只要终端/给其他 agent 驱动 |

统一工作区布局：设置存于 `data/user/settings/`（可用 `DEEPTUTOR_HOME` / `deeptutor start --home` 指定）。端口默认：前端 `3782`、后端 `8001`。

### 3.2 Docker 部署关键细节

- **只映射 `3782` 即可**：浏览器只跟前端 origin 通信；容器内 Next.js 中间件（`web/proxy.ts`）把 `/api/*` 和 `/ws/*` 在容器内部转发给 FastAPI 后端。`8001` 仅当要 curl 调 API 时才需要暴露。
- 首次启动自动创建 `/app/data/user/settings/*.json`；配置/API key/日志/工作区/记忆/知识库全部持久化在 `deeptutor-data` volume。
- 可选依赖通过 `DEEPTUTOR_EXTRAS`（系统库用 `DEEPTUTOR_APT_PACKAGES`）在部署层声明，别 `docker exec pip install`。
- 后台运行：加 `-d`；跟踪 `docker logs -f deeptutor`；停止 `docker stop deeptutor`；删除容器 volume 保留；彻底重置 `docker volume rm deeptutor-data`。
- 升级：`docker pull` 新镜像 → `docker rm -f deeptutor` → 重新 `docker run`；volume 保留设置/KB/记忆。
- 反向代理：单容器场景无需配 API base，直接指向发布出的 `:3782`。拆分部署才需在 `system.json` 设 `next_public_api_base`。
- 改端口：改 `-p` 左侧宿主机端口即可；若改容器侧端口需同步右侧。

### 3.3 接入本地 LLM（Docker + 宿主机 Ollama 等）

- 容器内 `localhost` 指容器本身；用 host gateway 访问宿主机模型服务：
  `docker run … --add-host=host.docker.internal:host-gateway …`
- 设置 → Models 里 Base URL 指到 `host.docker.internal`：
  - Ollama LLM：`http://host.docker.internal:11434/v1`
  - Ollama embedding：`http://host.docker.internal:11434/api/embed`
  - LM Studio：`http://host.docker.internal:1234/v1`；llama.cpp：`http://host.docker.internal:8080/v1`
- **Windows/macOS Docker Desktop 通常无需 `--add-host`**；Linux 需要该 flag 或改用 `--network=host`。
- Linux 也可用 `172.17.0.1`（docker0 网桥）作为宿主机地址。

### 3.4 初始化与基本使用流程

1. `deeptutor init`：交互式询问端口 + LLM provider/base URL/API key/model + 可选 embedding（知识库用）+ 可选搜索 provider。跳过也可启动，之后在 设置→Models 补。
2. `deeptutor start`：同时拉起后端+前端，打印前端 URL（默认 http://127.0.0.1:3782），`Ctrl+C` 停止两者。
3. 浏览器打开后用 设置→Models 添加 LLM profile（Base URL / API key / model），保存；用知识库功能再加 embedding profile。
4. 常用 CLI：`deeptutor chat`（REPL）、`deeptutor run <capability> "…"`（单轮）、`deeptutor kb create/add/search`、`deeptutor memory show`、`deeptutor config show`、`deeptutor doctor`（健康检查，`--online` 探测模型 provider）。
5. Web 主要界面：Chat、Ask Questions、Quiz、Visualize、Research、Solve、Mastery Path、Immersive Reading、Knowledge Center、Learning Space、Memory、Settings。

### 3.5 常见坑速查（排错）

| 症状 | 解法 | 源 |
|------|------|-----|
| 端口被占 `Address already in use :3782/:8001` | `lsof -i:3782` / `ss -ltnp \| grep :3782` / PowerShell `Get-NetTCPConnection` 找到并处理；或改 `system.json` 端口 / 环境变量 `BACKEND_PORT`、`FRONTEND_PORT` | S3, S4 |
| provider probe 401 | API key 前缀不符：OpenAI `sk-`/`sk-proj-`、Anthropic `sk-ant-`、Gemini `AIza`；Ollama 本地留空或 `none` | S4 |
| `host.docker.internal` 解析不了 | Linux 用 `172.17.0.1` 或加 `extra_hosts: "host.docker.internal:host-gateway"` | S4 |
| KB 查询 `Embedding dimension mismatch` | 换过 embedding 模型 → Web UI Knowledge → KB → Index versions → **Re-index now** | S4 |
| Embedding endpoint 报错 | 必须填完整 endpoint：OpenAI `…/v1/embeddings`、Cohere `…/v2/embed`、Jina `…/v1/embeddings` | S4 |
| KB 卡 `indexing` | 看日志 `tail -f data/user/logs/deeptutor.jsonl \| grep -i kb`；常见 429 限流/embedding host 不可达/PDF 有密码 | S4 |
| 容器立刻退出 | `docker logs deeptutor \| tail -30`；无效 LLM 凭据只记 warning 不致命 | S3, S4 |
| 前端空白页 | Console 看 CORS（加 `cors_origins`）/ `/_next/...` 404（`cd web && npm run build`）/ 后端未起（`curl http://localhost:8001/`） | S4 |
| Windows `Microsoft Visual C++ 14.0 is required` | 装 VS Build Tools，勾 "Desktop development with C++" | S4 |
| pip 慢 | `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple` | S4 |
| Partner channel 置灰/`missing SDK` | `pip install -e ".[partners]"`；channel 的 `allow_from: []` 默认拒绝全部，需显式 opt-in | S4 |
| 重启后所有 API 401 | `data/system/auth/auth_secret` 丢失 → 从备份恢复或接受新 secret 全员重登 | S4 |

---

## 四、架构与原理（方向 C 核心）

### 4.1 Agent-Native 架构（claim → S1）

- v1.0.0-beta.1（2026-04-04）为 **agent-native 架构重写（~20 万行）**：Tools + Capabilities 插件模型，CLI & SDK，TutorBot、Co-Writer、Guided Learning、持久记忆。
- **单一 Agent 循环**：Chat 是默认能力，模型"思考多轮 → 必要时调用工具 → 观察结果 → 以无工具消息收尾"。`ask_user` 可暂停回合做结构化澄清。
- **用户可开关工具**：`brainstorm`、`web_search`、`paper_search`、`reason`、`geogebra_analysis`、`imagegen`、`videogen`。
- **上下文相关工具**（自动挂载）：`rag`、`kb_files`、`read_source`、`read_memory`、`write_memory`、`read_skill`、`load_tools`、`exec`、`web_fetch`、`ask_user`、`list_notebook`、`write_note`、`question_bank`、`github`、`consult_subagent`。
- **两种上下文**：sticky session context（subagent/KB/persona/model/voice，跨轮持久）；one-time references（文件/聊天历史/书/笔记/题库/导入 agent，单轮）。
- 所有入口（Web/CLI/SDK）汇聚到同一个 `ChatOrchestrator`，事件驱动流式输出；Partner 的每条消息也是一次普通 ChatOrchestrator 回合（partner-scoped workspace）。

### 4.2 三层记忆系统

| 层 | 内容 | 说明 |
|----|------|------|
| L1 | 工作区镜像 + append-only 事件追踪 `trace/<surface>/<date>.jsonl` | 原始事实记录 |
| L2 | 每面整理事实 `L2/<surface>.md` | 引用 L1 |
| L3 | 跨面综合 `L3/<profile\|recent\|scope\|preferences>.md` | 引用 L2 |

- 刻意**不是隐藏向量库**，而是文件背书、可读可审计；Memory Graph 呈现金字塔（L3 中心、L2 中环、L1 外环），任何综合主张可追溯回原始事件。
- 追踪面：chat、notebook、quiz、kb、book、partner、cowriter。
- `read_memory` 拼接四份 L3 文档（preferences 由 write_memory 直写；recent/profile/scope 需在 Memory Workbench 手动整合，**没有自动每 N 轮整合**）。
- `write_memory` 接受 1–240 字符偏好文本。

### 4.3 论文设计（claim → S2）

- **混合个性化引擎（hybrid personalization engine）**：静态知识锚定 + 动态学习者记忆，持续适应学习者演变需求。
- 框架统一：**引文锚定的问题辅导 + 难度校准的题目生成**（citation-grounded problem tutoring + difficulty-calibrated question generation）。
- 同一个性化基底扩展到：自适应学习工作流、交互式书籍、主动多通道辅导 agent。
- **TutorBench**：交互式评测基准，含 5 个大学课程领域的定制学习者画像。
- **LLM 首人称交互评测协议**：用画像驱动的学生模拟器做评估。
- 结果：个性化指标平均提升 **10.8%**；5 个 backbone 模型的通用 agentic reasoning 提升 **29.4%**。

### 4.4 多引擎 RAG 与知识库（claim → S1）

- 每种 KB 绑定一个检索引擎：LlamaIndex（默认，本地向量+BM25）、PageIndex（页面级引用+推理检索）、GraphRAG、LightRAG、LightRAG Server（HTTP 外连）、Tencent IMA、MarginNote 4、链接的 Obsidian vault。
- 创建 KB 两种方式：create new（上传建新索引）或 link existing（复用外部索引，原地读取不重建）。
- 支持跟踪 GitHub 仓库（repo/branch/glob）与文档站 URL（有界抓取深度）；按需 sync 增量 diff。
- 重建索引写新 `version-N` 目录并保留旧版；单文档可从 error 状态 KB 移除（不必整库重建）。
- 文档解析引擎可选：Text-only、MinerU、Docling、Tika、markitdown、PyMuPDF4LLM、LiteParse；本地模型下载默认关闭；Docling 支持远程 Docling Serve 模式。

### 4.5 生态与设计原则（claim → S1）

- Skills 用开放 Agent-Skills 格式（SKILL.md + YAML frontmatter + 可选参考文件），非 DeepTutor 专属；EduHub 为默认 hub，兼容 ClawHub；导入有安全门（安全判定→zip 防护→suffix 白名单→剥离 `always:`→写入 `.hub-lock.json`）。
- 社区/上游启发：RAGLAB、MoT（超轻量 agent 引擎，原 TutorBot）、LightRAG、OpenAGI（零代码 agent 框架）、Auto-DeepResearch、ClawHub、OpenCode、Codex、Manim（Math Animator）。
- 许可协议：**Apache-2.0**（README 尾部 + LICENSE 文件明确标注）。

---

## 五、矛盾与待核实

1. **许可协议（已解决）**：P1 探测时任务参数记为 AGPL-3.0；README 与 LICENSE 均为 **Apache-2.0**。以 Apache-2.0 为准。
2. **版本节奏极快**：2026-08 内连发 v1.5.7→v1.6.2；教程写作时应以"当前 latest=v1.6.2"为锚，并提示读者以官方文档为准，避免版本漂移。
3. **star 数动态**：S6（2026-04-14）称 17.8k；S1（2026-08-31）38.2k。属正常增长，非冲突。
4. **CSDN 文章付费截断**：架构深度部分不可用，仅采用其产品定位与设计哲学；架构细节以 S1/S2 为准。
5. 论文 v3 修订（2026-07-09）与 README 功能（v1.6.x）时间上有先后，部分术语（如 Partner vs TutorBot、LightRAG 演进）存在版本演化，写作时注意区分"论文设计"与"当前产品"。

---

## 六、实战指南（面向本用户：有基本了解，Obsidian 输出，Windows 环境）

1. **首选 Docker 路径**：用户机器为 Windows（vault D:\Study-Notes）。Docker Desktop 下：
   `docker run --rm --name deeptutor -p 127.0.0.1:3782:3782 -v deeptutor-data:/app/data ghcr.io/hkuds/deeptutor:latest`
   打开 http://127.0.0.1:3782 → 设置→Models 配 LLM（可连本地 Ollama 或云端 OpenAI/DeepSeek）。
2. **本地模型接入（Windows）**：Docker Desktop 自动解析 `host.docker.internal`，无需 `--add-host`；Base URL 见 3.3。
3. **API 直连可选**：需要 curl 调 API 时再加 `-p 127.0.0.1:8001:8001`。
4. **数据持久化**：设置/KB/记忆都在 `deeptutor-data` volume；升级/删容器不丢数据。
5. **进阶验证路径**：部署后按 4 个场景验证：① 上传 PDF 建 KB → 提问看引用；② 让 Quiz 生成习题；③ 创建 Partner/TutorBot 并连一个 IM 渠道；④ 用 Memory 查看 L1/L2/L3 与 Memory Graph。
6. **排错入口**：`deeptutor doctor`；遇到 4 类高频问题（端口、401、embedding 维度、容器退出）用 3.5 速查表。

---

## 七、未决问题（写作时需用户确认或标注）

1. 用户的实际部署方式：Docker（推荐）还是本地 Python？是否已有可用 LLM API（OpenAI/DeepSeek）或本地 Ollama？
2. 笔记深度配比："使用"与"原理"各占多少篇幅？建议 6:4（先跑通，再讲原理）。
3. 是否覆盖多用户/团队部署、MCP 服务、EduHub 技能发布等进阶话题，还是聚焦单人核心玩法？

---

## 八、下游交接（给 outline-generator / chapter-writer）

- **素材定位**：`workspace/deeptutor/sources/*.md`（6 个原始抓取）+ 本文档。写章节时引用 claim 用 `[S1]`–`[S6]` 标注。
- **建议大纲方向（草案）**：
  1. DeepTutor 是什么：定位、功能全景、适用场景
  2. 快速上手：Docker 部署 + 模型配置 + 首次对话
  3. 核心玩法：知识库（RAG）、出题、可视化、深研
  4. 进阶玩法：Living Book、Partner/TutorBot、CLI 与 agent 驱动
  5. 原理：Agent-Native 单循环架构、三层记忆、多引擎 RAG、论文设计
  6. 避坑与排错：常见问题速查
- **写作注意**：版本以 v1.6.2 为锚；术语"TutorBot"已演进为"Partners"，写作时统一并说明演进。
