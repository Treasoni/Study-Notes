# 如何写 DeepSeek-Harness hook 扩展点插件 - 意图文件

## 基本信息

- **主题**: 如何写 DeepSeek-Harness hook 扩展点插件
- **项目标识**: deepseek-harness-hook-plugin
- **创建时间**: 2026-08-16
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: 本项目即 vault（不硬编码绝对路径）
- **笔记目录**: AI学习/DeepSeek-Harness 教程/DeepSeek-Harness 插件开发教程/
- **MOC 路径**: AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC.md

## 学习目标

### 笔记类型
实战笔记（以代码实现为主线）

### 学习深度
上手（会写、会挂、会用，够日常插件用）

### 用户基础
有了解（已读《插件开发核心》01 章 3.5 速览 + 系列实战分册）

## 研究计划

### 探索方向
1. hook 扩展点语义模型：pre-execute / guard / execute / post-execute / result 各自职责与 `next()` 瀑布语义
2. 实战代码：权限门（allow/deny/ask）、改汇报（post-execute 替换）、只读观察（result）、guard 单调否决，完整插件 + 验证命令链
3. 与 Claude Code hook 迁移对照：PreToolUse ≈ pre-execute，`dsh-hooks-claude-code` 桥如何映射现有 hook 配置

### 重点收集
- **核心概念**: `tools/pre-execute`、`ctx.tools.guard()`、`tools/execute`、`tools/post-execute`、`tools/result`、`ctx.on` + `next()` 瀑布、`PreToolDecision`
- **实战代码**: 权限门 hook 插件、guard 插件、post-execute 改写展示、result 观察、`apply(ctx)` 挂载写法
- **常见坑**: guard 与 pre-execute 叠加语义、post-execute 替换 vs result 只读的取舍、监听器顺序、卸载自动清理
- **工具链**: `dsh-hooks-claude-code` 桥、`defineTool` output.render 与 post-execute 关系

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 否
- 学术论文: 否

## 备注

- 与《插件开发核心》3.5 互补：3.5 是目录速览，本篇是教学落地。
- 与《配置实战》03 章区分：03 章讲「接入已有 Claude Code hooks 配置」，本篇讲「在 dsh 代码里实现 hook 扩展点插件」。
- 篇幅目标：中量 12,000–15,000 字。
- 发布时同步更新系列 README（插件开发教程分册新增章节）与 MOC。
