# Update Plan — 镜像加速器vs代理-概念对比.md

> 工作流：batch-note-update-flow（update-docker）
> 笔记：`docker/镜像加速器vs代理-概念对比.md`
> 计划时间：2026-08-04
> 模式：project-output-only（原文不动，输出到 `updates/compare/updated_note.md`）

## 目标

把笔记中「镜像加速器」与「代理」的时效性现状刷新到 2026-08（国内镜像站关停、Docker Desktop 代理配置入口、版本基线），同时保留核心概念对比、表格与决策流程图不变。

## 变更列表

1. **frontmatter 补齐**（项目规范）
   - 补 `title` / `status` / `source_project`，`updated=2026-08-04`，保留 `created=2026-03-28` 与 tags。

2. **镜像加速器现状**（依据 S4/S5/S6）
   - 2.1 示例配置后新增 [!warning]：2024-06 起国内公共 Docker Hub 镜像站大面积关停（USTC/NJU/SJTU/阿里云/腾讯云）；社区源只支持 `docker pull` 不支持 `docker search`、不保证长期有效；个人可用阿里云 ACR 免费版。
   - 6.1 速查表删除失效源 `docker.mirrors.ustc.edu.cn`，替换为 `docker.xuanyuan.me`（保留 daoCloud / 1ms.run）。
   - 3.3 / 6.1 补 tip：`registry-mirrors` 机制仍受 Docker Engine 支持；仅 `dockerd --registry-mirror` CLI flag 弃用。

3. **代理配置现状**（依据 S8/S9/S10）
   - 3.3 与 6.2 明确：**Docker Desktop 忽略 daemon.json 代理**，必须用 Settings → Resources → Proxies；systemd drop-in 只适用于非 Desktop Linux daemon。
   - 3.3 / 6.3 / 误区 2 补充 `~/.docker/config.json` 的 `proxies.default` 统一注入容器/构建代理。

4. **版本基线**（依据 S1/S2）
   - 概述 callout 补充：本文基于 Docker Desktop 4.83 / Docker Engine 29.x（2026-08 现状）核对。

5. **误区章节（保持准确性）**
   - 误区 1：补充社区源只支持 pull 的说明，强化「加速器 ≠ 翻墙」。
   - 误区 2：补例外说明——Docker Desktop 的 Settings → Resources → Proxies 配置会自动把代理传播给容器（区别于 daemon.json / systemd 代理只影响 pull/build）。
   - 误区 3：保留。

6. **格式合规**
   - 为全部 ASCII 示意图补 `text` 语言标识；修复 2.1 原理图中一处乱码箭头字符。

7. **元数据**
   - 文末追加 `## 更新记录`（2026-08-04），「最后更新」改 2026-08-04；参考资料补充 2026 社区来源。

## 不变内容

核心区别表（一）、作用范围图（3.1）、功能对比表（3.2）、决策流程图（4.1）、典型场景推荐表（4.2）、误区 1/3、一张图总结（七）、个人笔记、相关文档双链、官方参考资料链接。
