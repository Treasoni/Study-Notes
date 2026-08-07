# GHCR 推送镜像权限配置 - 意图文件

## 基本信息

- **主题**: GHCR 推送镜像权限配置
- **项目标识**: ghcr-push-permission
- **创建时间**: 2026-08-08
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: C:\note\Study-Notes
- **笔记目录**: GitHub项目
- **MOC 路径**: 待阶段 7 确认

## 学习目标

### 笔记类型
概念 + 实战

### 学习深度
上手

### 用户基础
有了解

## 研究计划

### 探索方向

1. GHCR 推送权限机制与 `GITHUB_TOKEN` 的限制：为什么 CI 默认凭据不一定能推镜像
2. Fine-grained PAT 的权限配置细节：`Packages: Read and Write`、Resource owner、Repository access
3. Repository Secret + `docker/login-action` 兜底登录的落地配置：`GHCR_TOKEN || GITHUB_TOKEN`

### 重点收集

- **核心概念**: GHCR、GitHub Actions `GITHUB_TOKEN`、PAT（Fine-grained / Classic）、Packages 权限模型、Repository Secret、`docker/login-action`
- **实战代码**: `docker/login-action@v3` 配置、`GHCR_TOKEN || GITHUB_TOKEN` 兜底写法、`docker push ghcr.io/...` 示例
- **常见坑**: Token 过期、Secret 命名不一致（`GHCR_TOKEN` vs Workflow 引用）、组织级 Packages 权限、Package 的 `Manage Actions access`
- **工具链**: GitHub Actions、GHCR、docker/login-action、GitHub Secrets

### 信源偏好

- 官方文档: 是
- 技术博客: 是
- 社区讨论: 否
- 学术论文: 否

## 备注

用户附带了一份完整落地操作指南（阶段一：生成 Fine-grained PAT；阶段二：配置 Repository Secret；阶段三：Workflow 兜底登录）。笔记将以这份指南为主线，补充「为什么要这么配」的原理说明和易错点。
