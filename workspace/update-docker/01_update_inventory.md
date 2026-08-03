# 更新清单

> 工作流：batch-note-update-flow
> 运行标识：update-docker
> 阶段：P1 更新清单
> 生成时间：2026-08-03

## 扫描范围

- 路径：`docker/`
- 范围：目录全量 `*.md`
- 数量：12 篇
- 更新目标：全面刷新 Docker / Docker Desktop / WSL2 到 2026 最新版本与最佳实践

## 清单总览

| id | 文件 | 状态 | 优先级 | 大小 | frontmatter | 最后更新 |
|----|------|------|--------|------|-------------|----------|
| mirror-config | DockerDesktop镜像加速器配置.md | **ready** | **高** | 14.6KB | ✅ (2026-03-04) | 2026-03-04 |
| windows-install | Windows-DockerDesktop安装指南-国内网络版.md | **ready** | **高** | 23.7KB | ✅ (2026-03-29) | 2026-03-29 |
| proxy | docker进行代理.md | **ready** | **中高** | 5.5KB | ❌ 缺失 | — |
| compare | 镜像加速器vs代理-概念对比.md | candidate | 中 | 15.5KB | ✅ (2026-03-28) | 2026-03-28 |
| network | Docker网络结构详解.md | candidate | 中 | 44.6KB | ✅ (2026-03-29) | 2026-03-29 |
| container-update | docker容器如何更新.md | candidate | 中 | 11.4KB | ⚠️ 缺日期 | 2026-02-09 |
| gid-uid | docker里的GID和UID.md | candidate | 低 | 2.2KB | ⚠️ 缺日期 | — |
| build-errors | docker容器搭建错误的知识讲解.md | candidate | 低 | 1.8KB | ⚠️ 缺日期 | — |
| comic-library | 如何搭建漫画库.md | needs-review | 低 | 1.0KB | ❌ 缺失 | — |
| github-raw | github文件直链方式.md | skip | — | 1.7KB | ❌ 缺失 | — |
| docker-moc | Docker MOC.md | skip | — | 6.4KB | ✅ (2026-05-14) | 2026-05-14 |
| sortspec | sortspec.md | skip | — | 0.4KB | ⚠️ 插件格式 | — |

## 逐篇判定依据

### ready（可直接进入更新计划）

1. **DockerDesktop镜像加速器配置.md** — 高优先
   - 引用的多个国内镜像源已失效：`docker.mirrors.ustc.edu.cn`（中科大，2024 年中已停 Docker 服务）、`docker.nju.edu.cn`（南大，已停）、SJTU 镜像
   - `registry-mirrors` 机制本身自 2025 年起被 Docker 逐步弃用（Docker Hub 直连策略变化、部分版本移除该配置）
   - 需核对 2026 年当前可用镜像源/替代方案

2. **Windows-DockerDesktop安装指南-国内网络版.md** — 高优先
   - 国内下载方案（解决方案 A/B/C）链接时效性强，可能失效
   - WSL2 安装流程与 `wsl --update` 版本、Docker Desktop 当前版本要求需核对
   - `registry-mirrors` 配置部分同上，需同步更新

3. **docker进行代理.md** — 中高优先
   - 无 frontmatter，需补
   - 代理配置涉及 daemon proxy、容器 proxy，需核对 2026 当前推荐做法（Docker Desktop 代理设置 UI、compose `network_mode`/proxy env 现状）

### candidate（视内容逐篇决定是否更新）

4. **镜像加速器vs代理-概念对比.md** — 中
   - 概念性内容为主，但「镜像加速器」的现状描述需随 mirror-config 更新同步修正
5. **Docker网络结构详解.md** — 中
   - 44.6KB 大笔记，网络原理（bridge/host/overlay/iptables）本身稳定
   - 引用「Docker 25.0」可能过时（2026 已到 27/28.x），命令输出示例需核对
6. **docker容器如何更新.md** — 中
   - compose/run 更新流程基本稳定；缺 frontmatter 日期
   - 可补充 2026 现状（如 `docker compose` 已是默认、watch/rollout 新特性）
7. **docker里的GID和UID.md** — 低
   - UID/GID 概念稳定；缺 frontmatter 日期
8. **docker容器搭建错误的知识讲解.md** — 低
   - compose 错误行为说明基本稳定；缺 frontmatter 日期

### needs-review（范围不清，待确认）

9. **如何搭建漫画库.md** — 低
   - 无 frontmatter、无日期；主题是「用 Docker 搭漫画库」（Tachiyomi 系），与全面刷新 Docker 目标相关度低
   - 待用户确认是否纳入本次更新，还是仅补 frontmatter/跳过

### skip（不纳入正文更新）

10. **github文件直链方式.md** — 与 Docker 更新目标无关（GitHub raw 链接技巧）
11. **Docker MOC.md** — MOC 索引，正文更新交给 P5 MOC 同步阶段
12. **sortspec.md** — Obsidian 排序插件内部文件（sorting-spec 格式），非学习笔记

## 统计

- 扫描总数：12
- **ready**：3
- **candidate**：5
- **needs-review**：1
- **skip**：3

## 待确认项

- [ ] `如何搭建漫画库.md` 是否纳入更新（默认 needs-review，仅补 frontmatter）
- [ ] 3 篇 ready 笔记确认进入更新计划
- [ ] 5 篇 candidate 的优先级和是否纳入第一批
