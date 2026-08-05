# 基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统 - 意图文件

## 基本信息

- **主题**: 基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统（实战构建）
- **项目标识**: ai-smart-home-system
- **创建时间**: 2026-08-05
- **当前阶段**: 阶段 0
- **输出目标**: Obsidian vault
- **Vault 路径**: `C:\note\Study-Notes`
- **笔记目录**: `homeassistant/ai-smart-home-system/`
- **MOC 路径**: `homeassistant/Home Assistant MOC.md`

## 学习目标

### 笔记类型
实战构建指南（practice 为主，附方案/决策背景）

### 学习深度
精通（能独立搭建、改造、扩展、排错）

### 用户基础
熟悉（已用过或了解 Home Assistant，正在编写 HA 部署方式对比笔记）

## 研究计划

### 探索方向
1. 系统架构与四层设计：用户交互层（微信 / Web / 语音）→ 智能体层（Python Agent + DeepSeek Function Calling）→ 核心平台层（Home Assistant）→ 基础设施层（Docker Compose）
2. 环境搭建与国内适配：Docker Container 部署（HA Core + Agent 容器化编排）、阿里云 ACR 镜像、Gitee 镜像、Xiaomi Miot Auto 预置集成（不依赖 HACS）；说明为何不选已弃用的 Supervised，以及 HAOS 作为"专机专用"替代的取舍
3. 智能体实现：轻量 Python + FastAPI + DeepSeek API 的 Function Calling，实现自然语言 → 设备控制
4. HA 自动化与场景模板：Blueprint、packages 场景（回家/离家/睡眠）、模板化复制（三层分离 + entity_map 映射）
5. 产品化与复制策略：git clone + install.sh / HA Blueprint 导入 / Docker 预打包镜像

### 重点收集
- **核心概念**: Home Assistant Supervised、Docker Compose 编排、Xiaomi Miot Auto、LLM Function Calling、HA Blueprint、custom_components
- **实战代码**: install.sh 一键部署脚本、docker-compose.yml、Agent main.py（FastAPI + DeepSeek tool calling）、场景 YAML（packages/blueprints）、entity_map.yaml 映射
- **常见坑**: Supervised 宿主系统检测、Docker Hub / GitHub 国内网络卡点、米家 API 变更、DeepSeek API 稳定性、非技术用户安装卡点
- **工具链**: Docker CLI/compose、阿里云 ACR、Gitee、DeepSeek API、FastAPI、HA Blueprint、Xiaomi Miot Auto

### 信源偏好
- 官方文档: 是（home-assistant.io、DeepSeek API 文档、Xiaomi Miot Auto 仓库）
- 技术博客: 是
- 社区讨论: 是（瀚思彼岸论坛、HA 社区）
- 学术论文: 否

## 备注

- **参考报告**: `C:\Users\zhqzn\Desktop\智能家居系统报告.html`（实施方案 / 决策方案 / 市场调研 / 竞争优势 4 部分）
- **部署方式修正**: 报告决策二选 **HA Supervised**，但官方已于 **2025.12 弃用** Supervised（公告 2025-05-22）。本笔记改用 **Docker Container 部署**（官方正式路径之一，HA Core + Agent 由 docker-compose 一起编排，最贴合本项目架构）；HAOS 作为"专机专用"场景的替代。详见 [[Home Assistant 三种部署方式对比与选型.md]]
- **素材策略**: 以报告为基础 + research-collector 深度收集，补充官方文档、最新代码示例与踩坑经验
- **与已有笔记关系**: 部署方式选型（Supervised）与 `homeassistant/Home Assistant 三种部署方式对比与选型.md` 直接相关，成稿后互相双链
- **Obsidian 规则**: 表格不嵌套在列表内；YAML frontmatter 中含特殊字符（`[]`、`:`）的值必须正确引用
