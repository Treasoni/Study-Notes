# 共享资料研究计划

> 阶段：P3 共享资料收集
> 运行标识：update-docker
> 生成时间：2026-08-03

## 适用笔记范围

- **组 A**：mirror-config, windows-install, proxy, compare
- **组 B**：network, container-update（部分主题）

## 研究主题

| # | 主题 | 适用笔记 | 目标结论 |
|---|------|----------|---------|
| T1 | Docker Engine / Docker Desktop 2026 版本现状 | mirror-config, windows-install, network | 当前版本号、主要变化、下载方式 |
| T2 | 国内镜像加速器 2026 可用方案 | mirror-config, windows-install, compare | registry-mirrors 是否仍可用、可用镜像源清单、替代方案 |
| T3 | Docker daemon / 容器代理 2026 现状 | proxy, compare, windows-install | daemon proxy、容器 proxy 推荐做法 |
| T4 | WSL2 2026 现状 | windows-install | 当前 WSL 版本、安装命令 |

## 资料规则

- 每条资料保留：URL、日期、适用主题、100-200 字摘要
- 优先官方文档（docs.docker.com、learn.microsoft.com、GitHub release）与一手来源
- 镜像源可用性标注验证日期与可信度
- 不保存网页全文

## 验证标准

- [ ] T1：确认 2026 年 Docker Engine 最新版本号
- [ ] T2：确认 registry-mirrors 存废状态 + 至少 2 个 2026 可用镜像源/替代方案
- [ ] T3：确认 daemon/容器代理推荐做法无重大变化
- [ ] T4：确认 WSL 当前版本与 `wsl --update` 状态
