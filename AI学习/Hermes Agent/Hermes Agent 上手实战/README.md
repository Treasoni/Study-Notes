---
title: "Hermes Agent（Nous Research）上手实战"
tags:
  - I学习
  - gent
  - ermes
  - 手实战
created: 2026-08-28
updated: 2026-08-28
status: 已完成
source_project: hermes-agent
---

# Hermes Agent（Nous Research）上手实战

# Hermes Agent（Nous Research）上手实战
这份笔记围绕 Nous Research 出品的开源 AI agent——Hermes Agent 整理而成。与"装好即定型"的传统 agent 不同，Hermes 的核心卖点是内置学习回路：越用越懂你、越用越能干活。全篇按 定位 → 安装 → 模型配置 → 记忆闭环 → 技能体系 → 多平台自动化 → 委派并行 → 部署进阶 → 常见坑 → 身份定制与多 Agent → 命令速查 的顺序展开，十章正文加一个附录，帮助你从零跑通 Hermes，并理解它"用着用着自己变强"的机制。

## 目录

1. [[01-定位与核心理念|定位与核心理念：一个会自我改进的 agent]]
2. [[02-安装与第一跑|安装与第一跑：从命令到首次对话]]
3. [[03-模型 Provider 配置|模型 Provider 配置：打破模型锁定]]
4. [[04-记忆与学习闭环|记忆与学习闭环：跨会话成长]]
5. [[05-技能体系|技能体系：把经验沉淀为可复用资产]]
6. [[06-多平台接入与定时任务|多平台接入与定时任务：从"你找它"到"它找你"]]
7. [[07-委派与并行|委派与并行：子代理与 execute_code]]
8. [[08-部署进阶|部署进阶：Docker、多后端与安全基线]]
9. [[09-常见坑与最佳实践|常见坑与最佳实践]]
10. [[10-身份定制与多 Agent|身份定制与多 Agent：SOUL.md、Profiles 与 Bot Mode]]
11. [[11-附录-命令速查|附录：Hermes Agent 常用命令速查]]

## 快速上手

\`\`\`bash
# 一键安装（Linux/macOS/WSL2/Termux）
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.bashrc
hermes setup --portal    # 最快打通：OAuth + Nous Provider + Tool Gateway

# 已有 Python 环境
pip install hermes-agent

# Docker 部署
mkdir -p ~/.hermes
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent setup
\`\`\`

## 更新记录

- **2026-08-28**：单文件拆分重组为「10 章 + 附录」独立笔记，新增 README 入口与章节间导航；同步修正两处 MOC 的章节数描述。
