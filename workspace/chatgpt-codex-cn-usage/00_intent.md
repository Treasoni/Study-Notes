# 如何在国内网络情况下使用 ChatGPT 云端 Codex - 意图文件

## 基本信息

- **主题**: 如何在国内网络情况下使用 ChatGPT 云端 Codex（实战教程）
- **项目标识**: chatgpt-codex-cn-usage
- **创建时间**: 2026-09-04
- **当前阶段**: 阶段 0
- **输出目标**: project-output（先存 `workspace/output/`，Obsidian 发布待定）
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
实战教程（教程类：入口形态 + 网络方案 + 订阅鉴权 + 使用流程 + 常见坑）

### 学习深度
上手

### 用户基础
有了解：已用过 Claude Code / opencode 等 AI 编程工具，只关心「云端 Codex」在国内的联网与鉴权差异，不须科普基础 AI 概念

## 研究计划

### 探索方向
1. 形态与门槛：ChatGPT 云端 Codex（云任务）是什么，入口在哪（网页 / App / 桌面），需要哪种订阅（Plus / Pro / Team / Enterprise），支持地区
2. 国内网络可达性：访问 chatgpt.com / 云端 Codex 需要的网络条件；哪些节点/出口常被 OpenAI 风控；如何选择稳定方案
3. 账号与订阅：注册与登录的地区限制、付费方式（海外卡 / App Store / 其他）、锁号与风控的常见原因及规避
4. 实际使用流程：新建 Codex 会话 → 指派任务 → 连接 GitHub / 执行环境 → 审查并采纳变更
5. 常见坑与替代：IP 风控、地区不支持、订阅失败；团队/企业方案、API 中转、国内平替（如直接用国产 Coding Agent）

### 重点收集
- **核心概念**: Codex 云任务（cloud tasks）、ChatGPT 订阅层级与配额、支持地区清单、出口 IP 风控、权限/审计
- **实战代码**: 少量；主要是操作步骤、网络/账号配置、风险规避清单
- **常见坑**: 节点 IP 被 OpenAI 屏蔽、订阅支付被拒、账号被标记风控、任务执行区网络限制
- **工具链**: ChatGPT 官方入口（web / iOS/Android App / macOS 桌面端）、代理工具与节点选择

### 信源偏好
- 官方文档（OpenAI Help Center / openai.com/codex）: 是
- 技术博客: 是
- 社区讨论（V2EX / Reddit r/ChatGPT / 即刻）: 是

## 备注

- 教程类笔记「一章一节一文件」：每个顶级小节对应一个产物/文件，字段细节收进 `####` 子节。
- 关键处补 `[!tip] 大白话` + 打比方。
- 涉及 GitHub / 官方 API 时，用 `curl api.github.com` / 官方源核验后再写入，不凭印象写 URL。
