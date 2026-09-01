## 学习笔记大纲：《HKUDS DeepTutor —— Agent-Native 终身个性化学习工作区》

> 笔记类型：实战 + 概念（使用为主，兼顾原理）
> 预计总篇幅：长篇（约 7 章）
> 章节数：7
> 素材引用体系：[S1]–[S6]（对应 `02_deep_research.md` 源表）
> 方向配比：部署与上手（B）≈ 65% · 架构与原理（C）≈ 35%
> 目标读者：有基本了解的中文学习者（知道 Docker/LLM，不熟 Agent/RAG）
> 输出目标：Obsidian vault `GitHub项目/` 目录（frontmatter：title/tags/created/updated/status/source_project）
> 版本锚点：以 v1.6.2 为 latest，提示读者以官方文档为准，避免版本漂移

---

## 第 1 章：DeepTutor 是什么 —— Agent-Native 终身个性化学习工作区

- **篇幅**：中篇
- **覆盖要点**：一句话定位、三支柱痛点、功能全景（六合一能力面）、版本里程碑与现状、适用场景与目标用户、设计哲学
- **素材引用**：[S1]、[S2]、[S5]、[S6]
- **代码示例**：无

### 1.1 一句话定位：运行时统一"辅导 / 解题 / 出题 / 研究 / 可视化 / 掌握度练习"
### 1.2 它解决什么问题：知识碎片化、学习缺乏连续性、AI 工具过于被动
### 1.3 功能全景：Chat、Ask Questions、Quiz、Research、Visualize、Solve、Course Study、Mastery Path、Immersive Reading/Watching 共享同一运行时与会话上下文
### 1.4 里程碑与版本现状：正式发布、star 增速、当前 v1.6.2
### 1.5 适用场景与目标用户：自学者、学生、教师、研究者
### 1.6 三支柱设计哲学：持久化记忆 + 统一知识库 + 主动式智能体

---

## 第 2 章：Docker 快速上手 —— 一条命令跑通 DeepTutor

- **篇幅**：长篇
- **覆盖要点**：四种安装路径与选型、Docker 单容器部署命令、端口与持久化 volume、模型与 Embedding 配置（云端 API 为主，本地 Ollama 为可选补充）、首次对话验证、容器生命周期管理
- **素材引用**：[S1]、[S3]、[S4]
- **代码示例**：有（docker run / logs / stop / volume 命令、Ollama host.docker.internal Base URL、CLI deeptutor chat / doctor）

### 2.1 环境准备：Docker Desktop（Windows）与镜像确认（ghcr.io/hkuds/deeptutor:latest）
### 2.2 四种安装路径对比（PyPI / 源码 / Docker / CLI Only），为什么首选 Docker
### 2.3 部署命令逐行拆解
#### 2.3.1 端口映射：为什么只需暴露 3782（前端中转 /api、/ws 到后端 8001）
#### 2.3.2 数据持久化：deeptutor-data volume 与 data/user/settings/ 布局
### 2.4 模型接入：设置 → Models
#### 2.4.1 云端 API 为主：OpenAI / DeepSeek / Anthropic 的 Base URL 与 key 前缀
#### 2.4.2 本地 Ollama 补充：host.docker.internal（Windows/macOS 免加 --add-host，Linux 需 extra_hosts）
#### 2.4.3 Embedding 配置：完整 endpoint 规则（/v1/embeddings、/v2/embed 等）
### 2.5 首次对话验证：Web UI 与 CLI 双路径
### 2.6 容器生命周期：后台运行、日志、停止、升级、彻底重置 volume
### 2.7 本节小结：部署验收清单

---

## 第 3 章：核心玩法 —— 建知识库、出题、可视化与深研

- **篇幅**：长篇
- **覆盖要点**：Knowledge Center 与多引擎 RAG 知识库、带引用问答、Ask Questions/Quiz 出题、Visualize 可视化、Solve 解题、Research 深研
- **素材引用**：[S1]、[S2]、[S4]、[S6]
- **代码示例**：有（deeptutor kb create/add/search、Web UI 建库与提问操作路径）

### 3.1 知识库（Knowledge Center）：上传教材，建立可检索索引
#### 3.1.1 创建 KB：create new 上传建新索引 vs link existing 复用外部索引
#### 3.1.2 引擎与解析器：LlamaIndex 默认、PageIndex/GraphRAG/LightRAG 等；MinerU/Docling/markitdown 等解析器
#### 3.1.3 索引管理：version-N 目录、Re-index now、单文档移除
### 3.2 带引用的问答：让回答可追溯（rag / read_source 工具）
### 3.3 出题：Ask Questions 与 Quiz 的难度校准
### 3.4 可视化（Visualize）与解题（Solve）
### 3.5 深研（Research）：多步检索与综合
### 3.6 本节小结：一个完整学习闭环示例

---

## 第 4 章：掌握度路径（Mastery Path）与 Course Study

- **篇幅**：短篇
- **覆盖要点**：Mastery Path 掌握度路径的机制与用法、Course Study 课程学习、与核心玩法第 3 章的关系
- **素材引用**：[S1]
- **代码示例**：无（以 Web UI 操作与概念说明为主）

### 4.1 Mastery Path 是什么：分级掌握门控与 /learning 仪表盘
### 4.2 Course Study：课程绑定上下文的小班式学习
### 4.3 与第 3 章核心玩法如何串联：从知识库 → 出题 → 掌握度验证

---

## 第 5 章：进阶玩法 —— Living Book、Partners 与 Agent 驱动

- **篇幅**：中篇
- **覆盖要点**：Living Book（Book Engine 14 种块类型）、Partners/TutorBot（SOUL/模型策略/资料库/记忆 + 15+ IM 渠道）、My Agents 调度外部 agent、CLI 与 SDK 驱动、EduHub 技能生态（详写）、术语演进说明
- **素材引用**：[S1]、[S4]；EduHub/My Agents 需补一轮针对性收集（用户已确认补收集后详写）
- **代码示例**：有（deeptutor run 驱动、Partner 创建与渠道接入、Living Book 编译与导出、skill install）

### 5.1 Living Book：把 KB / 笔记 / 题库 / 聊天历史编译成交互"活书"
#### 5.1.1 块类型与页面聊天（Page Chat）
#### 5.1.2 编译、导出 Markdown、健康检查
### 5.2 Partners / TutorBot：持久陪伴体与 15+ IM 渠道
#### 5.2.1 术语演进：TutorBot → Partners（写作时统一并说明）
#### 5.2.2 创建 Partner 并接入一个 IM 渠道（Feishu/Telegram/微信等）
#### 5.2.3 渠道排错：missing SDK、allow_from 显式 opt-in
### 5.3 My Agents：调度外部 agent（Claude Code / Codex 等）与导入历史会话
### 5.4 CLI 与 SDK：单轮 run、给其他 agent 驱动 DeepTutor
### 5.5 EduHub 技能生态：Agent-Skills 格式、搜索/安装/发布、安全门

---

## 第 6 章：架构与原理 —— 它为什么这么设计

- **篇幅**：长篇
- **覆盖要点**：Agent-Native 单 Agent 循环与 ChatOrchestrator、Tools + Capabilities 插件模型、两类上下文、三层持久记忆与 Memory Graph、多引擎 RAG 设计、论文混合个性化引擎与 TutorBench 评测结论、论文设计与当前产品的差异
- **素材引用**：[S1]、[S2]
- **代码示例**：无（以架构示意与概念说明为主）

### 6.1 Agent-Native 架构重写：为什么是"单一 Agent 循环"
#### 6.1.1 ChatOrchestrator：Web / CLI / SDK / Partner 所有入口汇聚
#### 6.1.2 工具模型：可开关工具 vs 上下文相关工具（自动挂载）
#### 6.1.3 两类上下文：sticky session context vs one-time references
### 6.2 三层持久记忆：可读、可审计、可追溯
#### 6.2.1 L1 事件追踪 → L2 单面整理 → L3 跨面综合
#### 6.2.2 Memory Graph：从综合主张回溯原始事件
#### 6.2.3 read_memory / write_memory 的工作机制
### 6.3 多引擎 RAG：为什么不是一套检索打天下
### 6.4 论文设计：混合个性化引擎与 TutorBench
#### 6.4.1 引文锚定问题辅导 + 难度校准题目生成
#### 6.4.2 评测方法与结论（个性化指标 +10.8%、通用 agentic reasoning +29.4%）
### 6.5 论文设计与当前产品的版本差异（术语与功能演进）
### 6.6 开放生态与许可：Agent-Skills 格式、EduHub、Apache-2.0

---

## 第 7 章：避坑与排错速查

- **篇幅**：中篇
- **覆盖要点**：高频问题分类速查（端口占用、401、embedding 维度、容器退出、前端空白页）、Windows 环境专项、知识库/索引问题、Partner 渠道问题、认证安全、排错工具链
- **素材引用**：[S3]、[S4]
- **代码示例**：有（lsof / ss / Get-NetTCPConnection、docker logs、deeptutor doctor --online、tail 日志）

### 7.1 排错工具链：deeptutor doctor、日志 tail、端口检查
### 7.2 启动类问题：端口被占、容器立刻退出、前端空白页
### 7.3 模型接入类问题：provider probe 401、host.docker.internal 解析、embedding endpoint
### 7.4 知识库与索引问题：Embedding dimension mismatch、KB 卡 indexing
### 7.5 Windows 环境专项：VS Build Tools、pip 慢
### 7.6 Partner 渠道与认证：missing SDK、allow_from 显式 opt-in、auth_secret 丢失
### 7.7 高频问题速查表汇总

---

## 素材缺口标记（写作前需补收集）

- **第 5 章（EduHub + My Agents）**：当前仅 [S1] 概述，无实操细节。用户已确认"补收集后详写"→ 在第 5 章写作前补一轮针对性资料收集（EduHub 搜索/安装/发布流程、My Agents 调度与导入的实操）。

---

## 输出约定（给 chapter-writer）

- 每章最终笔记需带 frontmatter：`title` / `tags` / `created` / `updated` / `status` / `source_project`（source_project 填 `deeptutor`）。
- 代码块必须带语言标识；Callout 仅用于结构意义（summary/note/tip/warning/example）。
- 双链只添加高价值概念（如 [[RAG]]、[[Agent]]、[[Docker]]），不逐词链接。
- 引用素材统一用 [S1]–[S6] 标注；版本以 v1.6.2 为锚。

## 学习路径说明

### 前置要求
- 已安装 Docker Desktop（Windows），了解基本 `docker run` / volume 概念。
- 有至少一个可用云端 LLM API key（OpenAI `sk-` / DeepSeek / Anthropic `sk-ant-`），或本地已装 Ollama（可选）。
- 会使用 Windows 终端 / PowerShell 执行简单命令。
- 不需要预先掌握 Agent / RAG 概念 —— 笔记会在使用时同步讲解，原理放在第 6 章集中展开。

### 学完能做什么
- 用一条 `docker run` 命令部署 DeepTutor，并完成 LLM / Embedding 配置（云端为主，本地 Ollama 可备选）。
- 上传教材建立知识库，做带引用、可追溯的问答；生成习题；做可视化与深研；走一遍掌握度路径。
- 创建 Living Book 与 Partners/TutorBot，接入至少一个 IM 渠道；用 CLI / 外部 agent 驱动 DeepTutor。
- 能解释 DeepTutor 的 Agent-Native 单循环、三层持久记忆、多引擎 RAG 与论文中的混合个性化设计。
- 独立排查部署与使用中的 4 类高频问题（端口、401、embedding 维度、容器退出）。

### 建议学习顺序
- 顺序：第 1 章 → 第 2 章 → 第 3 章 → 第 4 章 → 第 5 章 → 第 6 章 → 第 7 章。
- 第 7 章是速查表，建议第一次通读，之后按需查阅；第 6 章可先通读建立整体认知，部署后再精读。
- 时间估计（仅供参考）：第 1 章约 30 分钟；第 2 章部署 + 配置约 1–2 小时；第 3 章核心玩法约 3–4 小时；第 4 章约 30–45 分钟；第 5 章进阶约 2 小时；第 6 章原理约 2–3 小时；第 7 章随用随查。
