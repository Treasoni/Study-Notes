# 如何写 subagent（DeepSeek-Harness） - 意图文件

## 基本信息

- **主题**: 如何写 subagent（DeepSeek-Harness）
- **项目标识**: deepseek-harness-subagent
- **创建时间**: 2026-08-16
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: D:\Study-Notes
- **笔记目录**: AI学习/DeepSeek-Harness 教程/
- **MOC 路径**: AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC.md

## 学习目标

### 笔记类型
概念理解 + 实战笔记

### 学习深度
上手（概念理解 + 动手写 provider 插件，会用现成 provider）

### 用户基础
有了解（已熟悉 Claude Code 扩展体系，已读 dsh 插件开发五章）

## 研究计划

### 探索方向
1. dsh subagent 心智模型：`ctx.subagents` 注册表 / `SubagentProvider` 契约 / 委托工具三层结构
2. 现成 provider 使用：`spawn` / `fork` / `acp` / `codex` / `claude-code` / `dsh-sdk` 的安装、挂载与配置
3. 自己写 provider 插件：`SubagentProvider` 接口、`capabilities`、`start` / `prepareContinuable`、`ctx.subagents.registerProvider`
4. 委托与控制工具：`dsh-tool-subagent`（provider/toolName/backgroundMode/maxDepth/agentOptions/persona/toolFilter）、`dsh-tool-subagent-control`、`dsh-tool-subagent-report`
5. 与 Claude Code subagent 对照迁移（`.claude/agents/*.md` → provider 插件 + 工具实例）

### 重点收集
- **核心概念**: ctx.subagents、SubagentProvider、capabilities、one-shot vs continuable、maxDepth / delegationDepth、inheritsParentContext、subagent/start|end 事件
- **实战代码**: provider 插件最小实现（registerProvider）、cordis.patch.yml 挂载示例、dsh-tool-subagent 配置、control/report 接线
- **常见坑**: spawn 无父对话历史、capability 不支持即响亮失败、one-shot 后台结果走 task 工具、重复 toolName、developer preview 破坏性变更
- **工具链**: @deepseek-ai/dsh-subagent(-spawn-in-process/-fork/-acp/-codex/-claude-code/-dsh-sdk)、dsh-tool-subagent(-control/-report)、dsh-hooks-claude-code 的 SubagentStart/SubagentStop 桥

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 承接上一轮对话：用户已了解 dsh 的 `ctx.subagents` 注册表、`dsh-tool-subagent`、provider 系列，本笔记把「subagent 从概念到能自己写 provider 插件」补齐。
- 归属：补进现有 DeepSeek-Harness 教程系列（新分册），更新 [[AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC|DeepSeek-Harness MOC]]。
- 官方素材已在手：docs/subsystems/subagent.md、tool-subagent(-control/-report) README、spawn-in-process README（2026-08-16 抓取），可作 P2 深度素材基础。
