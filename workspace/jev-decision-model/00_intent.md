# Jev 决策模型 - 意图文件

## 基本信息

- **主题**: Jev 决策模型（TypeSafe AI）
- **项目标识**: jev-decision-model
- **创建时间**: 2026-09-20
- **当前阶段**: 阶段 0
- **输出目标**: project-output（阶段 6 前再确认是否发布到 Obsidian）
- **Vault 路径**: 待确认（本 vault，阶段 6 由用户指定）
- **笔记目录**: `AI学习/Jev 决策模型/`（候选，待确认）
- **MOC 路径**: `AI学习/00-索引/AI学习 MOC.md`（候选，待确认）

## 学习目标

### 笔记类型
concept + practice 混合（概念打底 + 接入/速查实战）

### 学习深度
上手 —— 目标是读懂三原语语义，并能跑通一次真实调用

### 用户基础
有 LLM / Agent 基础，零 Jev 基础

### 用户原始诉求
1. 这个模型的概念
2. 如何使用这个模型

## 研究计划

### 探索方向

1. **概念与定位**：决策模型 vs LLM、System One、Jevons 命名由来、在 agent 分层架构中的位置
2. **使用方式**：API 调用流程、Schema 定义、置信度阈值处理
3. **实战集成**：agent judge / 模型路由 / 分类 / 上下文压缩，外加 Vercel AI Gateway、LangChain、Claude Code 插件三个生态接入点
4. **开源复现**：APUS `fast-browser-use`、本地 Qwen3.5-9B 离线路线
5. **局限与实测**：第三方实测边界、算术/日期/否定弱点、与 frontier 模型的互补分工

### 重点收集

- **核心概念**
  - 决策模型与 LLM 的本质差异：输出空间从「词表」换成「预定义类型」
  - System One / System Two 对照（卡尼曼），Jev 在 agent 分层架构中的位置
  - 三原语：Choice（≤255 选项）/ Score（数值区间）/ Noul（yes-no + 概率）
  - 校准（calibration）与置信概率的含义：概率可信 ≠ 判断正确
  - RLCD（Reinforcement Learning for Calibrated Decisions）
  - 「零幻觉」的确切边界：不越出 Schema ≠ 判断正确
  - 命名来源：Jevons / 杰文斯悖论（成本下降 → 用量爆炸）

- **实战代码**
  - API 最小调用示例：state + 预定义问题 → 结构化判断
  - Schema 定义方式（Choice 选项集、Score 区间、Noul 判定）
  - 置信度阈值处理：低置信度如何回退到大模型
  - Vercel AI Gateway 接入方式
  - LangChain「Jev-as-a-Judge」用法
  - Claude Code `fast-jev-compaction` 插件（上下文压缩实例）
  - APUS `fast-browser-use` 本地离线复现（Qwen3.5-9B）

- **常见坑**
  - 官方性能数字（最高 193.6x 快 / 444.6x 便宜）为官方自测，非第三方基准
  - 实测弱点：算术、日期比较、否定与模糊表述
  - 不适合长文本生成、聊天、复杂推理
  - 误读「零幻觉」为「判断不会错」
  - 发布初期未向中国大陆开放
  - 架构与权重未公开，无法自行训练

- **工具链**
  - TypeSafe AI 官方 API / SDK 与定价
  - Vercel AI Gateway
  - LangChain 集成
  - Claude Code 插件生态
  - APUS `fast-browser-use`（MIT，本地 Qwen3.5-9B）
  - Agent 分层架构：frontier 慢思考 + Flash + Jev 快判断 + 确定性代码 + Harness 调度

### 信源偏好

- **官方文档**: 是（优先级最高）—— TypeSafe 官方站点、API 文档、定价页
- **技术博客**: 是 —— 独立评测与上手文章
- **社区讨论**: 是 —— Vercel、LangChain、开发者实测
- **学术论文**: 视情况 —— RLCD 若发布技术报告/论文则收入，否则不收

## 备注

- 主题 2026-09-15 发布，上线仅 5 天，官方文档可能不完整。
- **阶段 1/2 强制区分「官方口径」与「第三方独立验证」**，笔记正文须标注来源性质。
- 性能与定价声明必须挂来源，并标注为官方自测口径。
- 实测类结论优先引用独立评测，不用官方宣传材料替代。
- 开源复现路线（APUS）与官方闭源模型必须分开表述，不得混为一谈。
