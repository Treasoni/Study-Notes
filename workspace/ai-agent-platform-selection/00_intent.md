# 自托管 AI Agent 平台选型（Octop / OpenClaw / Hermes） - 意图文件

## 基本信息

- **主题**: 自托管 AI Agent 平台选型（Octop / OpenClaw / Hermes）
- **项目标识**: ai-agent-platform-selection
- **创建时间**: 2026-09-29
- **当前阶段**: 阶段 0
- **输出目标**: project-output（阶段 6 再确认 Obsidian 位置）
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
对比笔记（选型决策型），辅以能落地的实战锚点

### 学习深度
上手 —— 读到「各自跑起来是什么样」的关键配置与目录结构，同类能力给出可比的具体证据；不读源码级剖析，默认不实际部署三个平台

### 用户基础
有了解（已实际使用过 OpenClaw、Hermes 类 agent）

### 待解问题（本篇笔记要回答的核心）
能力面高度重叠的多个 self-hosted agent，在什么场景下该选哪一个？判断依据是什么？

## 研究计划

### 探索方向
1. 三个平台各自的设计理念与架构分层：多用户模型、多 agent 编排粒度、记忆机制、工具体系
2. 「自托管平台」阵营 vs 「本地 CLI」阵营（Claude Code / Codex CLI 等）的能力边界与适用场景差异
3. 抽取通用选型判断框架：按运行形态 / 编排粒度 / 扩展点 / 记忆与上下文 / 多用户与权限几个轴做决策树，使新出现的 agent 也能自行归位

### 重点收集
- **核心概念**: self-hosted agent、agent harness、multi-agent 编排、long-term memory、tool / MCP 扩展模型、多用户与权限、会话与上下文管理
- **实战代码**: 三者各自的部署方式（Docker / compose）、配置文件与目录结构、最小可用启动示例；同类能力（记忆、工具注册、权限）在三者中的具体写法对照
- **常见坑**: 功能清单叠影导致「看起来都一样」的误判；自托管运维成本；数据落盘位置与隐私边界；扩展生态成熟度差异
- **工具链**: 各自的插件 / Skill / MCP 体系、模型接入方式、与本地文件系统及 Obsidian 的集成路径

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是（选型结论必须有真实使用反馈支撑，不能只靠官方自述）
- 学术论文: 否

## 用户实际使用场景（第一手锚点）

用户在 2026-09-29 阶段 0 澄清时提供，权重高于官方自述：

| 平台 | 用户实际用途 | 来源 |
| --- | --- | --- |
| Hermes | 个人助手；也用于一部分企业工作 | 用户原话（阶段 0） |
| OpenClaw | **待用户确认**（用户原话主语缺失，见「待确认事项」） | 待补 |
| Octop | **推断**：尚未使用，作为「是否值得引入」的新选项提出 | 推断（用户只给了仓库地址 + 提问，未声明已用它） |

### 由用户自述推出的诊断假设（需在阶段 1-2 验证）
用户的**现有用法本身就是重叠的**（个人助手 / 企业工作这一类「通用助理」场景同时落在 Hermes 上，而 OpenClaw 的角色他自己也说不清）。这可能正是「感觉这些 agent 干的事都一样」的根源：不是产品真的同质，而是**使用者的场景划分先于工具划分**。笔记要专门处理这一层——先按场景切分，再谈工具归位；否则容易退化成功能清单叠影。

## 待确认事项

- OpenClaw 在用户手上的实际角色未确认，暂不写入任何结论。可选解释见阶段 0 对话记录，需用户指定后再补入上表。

## 备注

- 用户核心诉求是**选型判断依据**，不是单个产品的入门教程；避免写成「A 有什么功能、B 有什么功能」的平铺清单
- 已用 GitHub API 核实三个仓库存在（2026-09-29）：
  - `TencentCloud/Octop` — 5,695★，MIT，Python，定位 "self-hosted AI assistant — multi-user, multi-agent"，homepage: octop.cloud
  - `openclaw/openclaw` — 390,772★，定位 "The AI that really does things. Any OS. Any Platform."
  - `NousResearch/hermes-agent` — 249,977★，定位 "The agent that grows with you"
- 待用户补充：三个平台各自的实际使用场景（若有），其权重高于官方自述
- 项目内同类历史运行可复用、不重复收集：`hermes-agent`、`hermes-docker-deploy`、`hermes-tool-config`、`hermes-rules-config`、`hermes-home-assistant`、`deepseek-harness-agent-preset`
