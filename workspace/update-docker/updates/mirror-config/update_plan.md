# Update Plan — DockerDesktop镜像加速器配置.md

> 工作流：batch-note-update-flow（update-docker）
> 笔记：`docker/DockerDesktop镜像加速器配置.md`
> 计划时间：2026-08-03
> 模式：project-output-only（原文不动，输出到 `updates/mirror-config/updated_note.md`）

## 目标

把笔记的镜像源清单、版本基线、GUI 配置说明刷新到 2026-08 现状，同时保持原文结构、友好语气、FAQ/验证章节与一键脚本不变（仅替换脚本中的镜像列表）。

## 变更列表

1. **镜像源清单整体替换**（依据 S4/S5）
   - 删除失效源：`docker.mirrors.ustc.edu.cn`、`docker.nju.edu.cn`、`docker.mirrors.sjtug.sjtu.edu.cn`
   - 启用 2025-2026 社区实测可用源：`docker.m.daocloud.io`、`docker.1ms.run`、`docker.xuanyuan.me`
   - 新增可选：个人阿里云 ACR 免费版 `https://<your-id>.mirror.aliyuncs.com`
   - 涉及位置：二·步骤3 JSON、三·3.2/3.3/3.5、四·4.1 预期输出、五·表格与多源 JSON

2. **版本基线更新**（依据 S1/S2）
   - 概述 callout 补充：本文基于 Docker Desktop 4.83 / Docker Engine 29.x（2026-08）
   - 参考资料新增官方 release notes 链接

3. **机制澄清**（依据 S6）
   - 确认 GUI 流程仍是 **Settings → Docker Engine** 编辑 `registry-mirrors` 数组，与 4.83 一致
   - 新增 tip：`registry-mirrors` 数组仍受支持；仅 `dockerd --registry-mirror` flag 自 17.06 起弃用

4. **风险提示**（依据 S4/S5）
   - 五·表格前新增 warning：国内镜像站已大面积关停，社区源不保证长期有效，须配置多个；多数只支持 `docker pull` 不支持 `docker search`

5. **FAQ 修正**（依据 S6/S7/S8）
   - Q1：新增「使用 `docker.io/xxx` 全限定名会绕过镜像源」排查项
   - Q3：新增 daemon 代理（Settings→Resources→Proxies）、云厂商镜像服务、Cmirror 替代方案
   - Q4：说明 GUI 与 CLI 实际编辑同一个 `~/.docker/daemon.json`，正常不冲突

6. **参考资料更新**
   - 移除失效的 USTC 镜像站链接；保留 DaoCloud；补充 2026 社区教程（zachthinking.github.io）

7. **元数据**
   - frontmatter 补 `title`/`status`/`source_project`，`updated=2026-08-03`，保留 `created` 与 tags
   - 文末追加 `## 更新记录`，更新「最后更新」

## 不变内容

一（原理）、二（流程结构与截图框架）、三（配置文件位置/重启方式）、四（测速部分）、六（其余 FAQ）、个人笔记、相关文档双链、原有 `[!info]`/`[!personal]` callout 语气。
