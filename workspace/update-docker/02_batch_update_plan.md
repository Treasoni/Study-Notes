# 批量更新计划

> 工作流：batch-note-update-flow
> 运行标识：update-docker
> 阶段：P2 批量更新计划
> 生成时间：2026-08-03

## 一、更新目标与判断依据

**目标**：全面刷新 Docker / Docker Desktop / WSL2 到 2026 年最新版本与最佳实践，刷新过时命令和配置。

**判断依据**：
- 笔记引用内容 vs 2026-08 已知现状比对（版本号、镜像源可用性、配置机制存废）
- 已知失效项：`docker.mirrors.ustc.edu.cn`、`docker.nju.edu.cn`、SJTU 镜像停服；`registry-mirrors` 机制弃用
- 已知过时项：`Docker 25.0`（当前 27/28.x）；国内下载方案链接
- 结构问题：4 篇缺 frontmatter 或日期

## 二、笔记分组

| 组 | 主题 | 笔记 | 说明 |
|----|------|------|------|
| A | 镜像源/代理（时效性最高） | mirror-config, windows-install, proxy, compare | 共享资料核心，2026 镜像源与代理现状 |
| B | 网络/运维 | network, container-update | 概念稳定，核对版本引用与推荐流程 |
| C | frontmatter 补齐 | gid-uid, build-errors | 仅补元数据，不动正文 |

## 三、逐篇动作

| id | 文件 | 动作 | 说明 |
|----|------|------|------|
| mirror-config | DockerDesktop镜像加速器配置.md | **update** | 替换失效镜像源清单；核对 registry-mirrors 弃用现状；补充 2026 替代方案（如直连/代理/新镜像服务） |
| windows-install | Windows-DockerDesktop安装指南-国内网络版.md | **update** | 核对国内下载方案链接；WSL2 安装流程与版本；镜像源配置同步 |
| proxy | docker进行代理.md | **update** | 补 frontmatter；核对 daemon/容器代理 2026 推荐做法 |
| compare | 镜像加速器vs代理-概念对比.md | **update** | 同步镜像源现状描述（组 A 结论） |
| network | Docker网络结构详解.md | **update** | Docker 25.0 → 当前版本；核对命令与输出示例；补充 2026 网络现状（如 nftables 后端） |
| container-update | docker容器如何更新.md | **update** | 补日期；核对 2026 推荐更新流程（compose watch/rollout 等） |
| gid-uid | docker里的GID和UID.md | **update（仅 frontmatter）** | 补 created/updated/tags，不动正文 |
| build-errors | docker容器搭建错误的知识讲解.md | **update（仅 frontmatter）** | 补 created/updated，不动正文 |
| comic-library | 如何搭建漫画库.md | skip | 用户确认跳过 |
| github-raw | github文件直链方式.md | skip | 非 Docker 主题 |
| docker-moc | Docker MOC.md | skip | P5 MOC 同步 |
| sortspec | sortspec.md | skip | 插件内部文件 |

## 四、共享资料包

**判定：需要（auto → yes）**。组 A + network 共享同一批 2026 现状主题，避免逐篇重复收集。

范围与主题：
1. **Docker Engine / Docker Desktop 2026 版本现状**（适用 mirror-config、windows-install、network）
2. **国内镜像加速器 2026 可用方案**：registry-mirrors 弃用现状、替代镜像服务、直连方案（适用 mirror-config、windows-install、compare）
3. **Docker daemon / 容器代理 2026 现状**（适用 proxy、compare、windows-install）
4. **WSL2 2026 现状**（适用 windows-install）

资料规则：优先官方文档与一手来源；每条保留 URL、日期、适用范围、100-200 字摘要；不保存网页全文。

## 五、批次安排（batch_size = 3）

| 批次 | 笔记 | 依赖 |
|------|------|------|
| **Batch 1** | mirror-config, windows-install, proxy | 组 A 高优先，需共享资料先行 |
| **Batch 2** | compare, network, container-update | 组 A 剩余 + 组 B |
| **Batch 3** | gid-uid, build-errors | 组 C frontmatter 补齐 |

## 六、输出模式与覆盖风险

- **destination_mode**：`project-output-only`
- 每篇输出：`updates/{note_id}/updated_note.md`（原文件不动，零覆盖风险）
- 每篇附：`stale_map.md`、`update_plan.md`、`update_report.md`
- **资料风险**：镜像源方案 2025-2026 变化频繁，须以官方/一手来源为准，社区转载信息标注可信度
- **待复核风险**：network 是 44.6KB 大笔记，patch 时若结构异常则标记 needs-review 不强行改

## 七、待用户确认项

- [x] 更新范围（6 正文 + 2 frontmatter + 4 skip）
- [x] 分组方式
- [x] 共享资料策略（需要）
- [ ] **Batch 1 处理列表**（mirror-config, windows-install, proxy）
- [ ] 批次推进节奏：每批完成后是否立即进入下一批

> 确认后进入 P3 共享资料收集。
