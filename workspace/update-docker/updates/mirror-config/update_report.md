# Update Report — DockerDesktop镜像加速器配置.md

> 工作流：batch-note-update-flow（update-docker）
> 笔记：`docker/DockerDesktop镜像加速器配置.md`
> 输出：`updates/mirror-config/updated_note.md`（原文未改动）
> 报告时间：2026-08-03

## 一、变更摘要

1. **镜像源清单整体替换**：删除已失效的 `docker.mirrors.ustc.edu.cn`（中科大）、`docker.nju.edu.cn`（南大）、`docker.mirrors.sjtug.sjtu.edu.cn`（上海交大），替换为 2025-2026 社区实测可用源 `docker.m.daocloud.io`、`docker.1ms.run`、`docker.xuanyuan.me`，并新增个人阿里云 ACR 免费版作为可选。涉及 GUI JSON、命令行配置、一键脚本、验证预期输出、镜像源表与多源 JSON 共 6 处。
2. **版本基线更新**：概述 callout 明确本文基于 Docker Desktop 4.83 / Docker Engine 29.x（2026-08）；参考资料补充官方 release notes 链接。
3. **机制澄清**：确认 `registry-mirrors` 数组仍受 Docker Engine 支持（S6），新增 tip 说明仅 `dockerd --registry-mirror` flag 弃用；GUI 流程确认仍为 Settings → Docker Engine，与 4.83 一致。
4. **风险提示**：新增 warning，说明国内镜像站 2024-06 起大面积关停、社区源不保证长期有效、须配置多个、多数只支持 pull 不支持 search。
5. **FAQ 修正**：Q1 增加全限定名绕过镜像源排查项；Q3 增加代理/云镜像服务/Cmirror 替代方案；Q4 澄清 GUI 与 CLI 编辑同一 daemon.json。
6. **元数据**：frontmatter 补 `title`/`status`/`source_project`，`updated=2026-08-03`；文末追加 `## 更新记录`。

## 二、使用来源

| 条目 | 内容 | 可信度 |
|------|------|--------|
| S1/S2 | Docker Engine 29.x / Desktop 4.83 版本现状 | ✅ 官方 |
| S3 | Engine 28 已 EOL | ✅ 社区汇总 |
| S4 | 国内镜像站大面积关停（USTC/NJU/SJTU 失效） | 🟡 社区汇总 |
| S5 | 2025-2026 社区可用源清单 + 阿里云 ACR | ⚠️ 时效波动 |
| S6 | registry-mirrors 仍受支持、仅 CLI flag 弃用、常见不生效原因 | ✅ 官方 |
| S7 | 替代方案（代理/云镜像服务/Cmirror） | 🟡 社区汇总 |
| S8 | Docker Desktop 代理需用 Settings→Resources→Proxies | ✅ 官方 |

来源库：`workspace/update-docker/shared_research/source_bank.md`

## 三、未解决风险

- **镜像源可用性波动**：社区源（DaoCloud/1ms.run/轩辕）按 source bank 2026-08 验证结论填写，本 agent 未逐一实拉测试。落地后建议按「四、验证配置」执行 `docker pull alpine:latest` 实测。
- **阿里云 ACR 占位**：`https://<your-id>.mirror.aliyuncs.com` 需用户登录阿里云 ACR 控制台替换为自己的加速地址。
- **白名单模式**：DaoCloud 需测试账号，未配置前可能拉取失败，已标注「需测试」。
- **范围说明**：`docker/` 目录其他 5 篇正文更新（windows-install、proxy、compare、network、container-update）不在本 agent 范围内，由 batch 后续批次处理。

## 四、结论

更新完成，符合 project-output-only 模式：原文 `docker/DockerDesktop镜像加速器配置.md` 未做任何改动，产出 4 个文件至 `updates/mirror-config/`。
