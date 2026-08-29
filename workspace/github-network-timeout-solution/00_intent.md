# GitHub 国内网络连接超时解决方案 - 意图文件

## 基本信息

- **主题**: GitHub 国内网络连接超时解决方案
- **项目标识**: github-network-timeout-solution
- **创建时间**: 2026-08-29
- **当前阶段**: 阶段 0
- **输出目标**: project-output
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
实战笔记（可落地的解决方案 + 原理）

### 学习深度
上手

### 用户基础
有了解（会用 git / 命令行、懂基本网络概念）

## 研究计划

### 探索方向
1. 诊断：如何确认 GitHub 连接超时发生在哪个环节（DNS 解析 / TCP 连接 / TLS 握手 / 具体服务）
2. 代理方案：git、npm、pip、docker、go module 等工具的代理配置
3. 国内镜像加速：GitHub 仓库克隆加速前缀、各大包管理器镜像源
4. hosts / CDN 工具方案：github520、FastGithub 等
5. Agent 拉包场景：如何给 agent 配置代理（环境变量 / git 全局配置）

### 重点收集
- **核心概念**: 连接超时、DNS 污染、TCP 阻断、TLS 握手、HTTP(S) 代理、透明代理、镜像源、ghproxy
- **实战代码**: git config 代理、环境变量代理（`http_proxy`/`https_proxy`）、镜像前缀替换、镜像加速器配置
- **常见坑**: 代理只对 HTTPS 生效、npm/pip 缓存旧包、混合源导致依赖锁问题、docker daemon 不读 shell 环境变量、代理端口不一致
- **工具链**: git、curl、npm、pip、go、docker、Clash/v2ray 类代理、ghproxy、github520

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 用户场景具体：agent 拉取 GitHub 的一个包时连接超时（国内网络）。需要覆盖「git 仓库克隆」与「常见包管理器」两个层面。
- 阶段 2 结束需确认执行模式（大纲模式 / 随性模式）。
