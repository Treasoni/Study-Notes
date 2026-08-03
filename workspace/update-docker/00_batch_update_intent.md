# 批量更新意图

> 工作流：batch-note-update-flow
> 运行标识：update-docker
> 创建时间：2026-08-03

## 意图参数

```yaml
source_path: "docker/"
source_scope: directory
source_glob: "*.md"
update_goal: "全面刷新到最新：核对 Docker / Docker Desktop / WSL2 在 2026 年的最新版本与最佳实践，刷新过时命令和配置"
destination_mode: project-output-only
batch_size: 3
shared_research: auto
moc_path: "docker/Docker MOC.md"
stale_threshold: ""
```

## 目标范围

`docker/` 目录下 12 篇 Markdown 笔记（含 MOC 和 sortspec）：

| 文件 | 大小 | 最后修改 |
|------|------|----------|
| Docker MOC.md | 6.4KB | 2026-07-28 |
| DockerDesktop镜像加速器配置.md | 14.6KB | 2026-07-28 |
| Docker网络结构详解.md | 44.6KB | 2026-07-28 |
| Windows-DockerDesktop安装指南-国内网络版.md | 23.7KB | 2026-07-28 |
| docker容器如何更新.md | 11.4KB | 2026-07-28 |
| docker容器搭建错误的知识讲解.md | 1.8KB | 2026-07-28 |
| docker进行代理.md | 5.5KB | 2026-07-28 |
| docker里的GID和UID.md | 2.2KB | 2026-07-28 |
| github文件直链方式.md | 1.7KB | 2026-07-28 |
| sortspec.md | 0.4KB | 2026-07-28 |
| 如何搭建漫画库.md | 1.0KB | 2026-07-28 |
| 镜像加速器vs代理-概念对比.md | 15.5KB | 2026-07-28 |

## 确认状态

- [x] source_path / source_scope / source_glob：`docker/` 全目录 `*.md`
- [x] update_goal：全面刷新到最新（用户确认，2026-08-03）
- [x] destination_mode：project-output-only（用户确认，2026-08-03）
- [x] batch_size：3（用户确认，2026-08-03）
- [x] shared_research：auto（待 P2 判定是否需要）
- [ ] MOC 同步范围待 P5 确认
