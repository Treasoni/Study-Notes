# 批量更新报告

> 工作流：batch-note-update-flow
> 运行标识：update-docker
> 阶段：P5 汇总与 MOC 同步
> 生成时间：2026-08-04

## 一、总览

| 指标 | 数量 |
|------|------|
| 扫描总数 | 12 |
| 正文更新 | 6 |
| 仅补 frontmatter | 2 |
| **更新总数** | **8** |
| 跳过 | 4 |
| 失败 | 0 |
| 需复核 | 0 |

- **源路径**：`docker/`
- **更新目标**：全面刷新 Docker / Docker Desktop / WSL2 到 2026 最新版本与最佳实践
- **输出模式**：project-output-only（原文件零改动）
- **共享资料**：`shared_research/source_bank.md`（12 条来源）

## 二、逐篇更新摘要

### 正文更新（6 篇）

| 笔记 | 输出路径 | 摘要 |
|------|---------|------|
| mirror-config | updates/mirror-config/updated_note.md | 替换 6 处失效镜像源（USTC/南大/SJTU → DaoCloud/1ms.run/轩辕 + 阿里云 ACR）；版本基线 → Desktop 4.83 / Engine 29.x；澄清 registry-mirrors 仍受支持；加社区源失效警告 |
| windows-install | updates/windows-install/updated_note.md | WSL2 主流程改 `wsl --install`/`--update`；镜像源替换；下载链接标注待验证；补充 WSL 常见错误 |
| proxy | updates/proxy/updated_note.md | 补 frontmatter；关键修正：Docker Desktop 忽略 daemon.json 代理，须用 Settings→Resources→Proxies；容器代理 config.json |
| compare | updates/compare/updated_note.md | 镜像源现状同步；代理配置路径修正；版本基线；修复 1 处 ASCII 损坏字符 |
| network | updates/network/updated_note.md | 仅 5 处外科手术修改（97% 逐字节一致）；Docker 25.0 → 29.x；补 nftables/IPv6 现状 callout |
| container-update | updates/container-update/updated_note.md | 补 frontmatter 字段；版本基线 callout；`docker compose` v2 为标准的说明 |

### 仅补 frontmatter（2 篇）

| 笔记 | 输出路径 | 摘要 |
|------|---------|------|
| gid-uid | updates/gid-uid/updated_note.md | 补 title/created/updated/status/source_project；正文未动 |
| build-errors | updates/build-errors/updated_note.md | 同上 |

### MOC（P5 同步）

| 笔记 | 输出路径 | 摘要 |
|------|---------|------|
| Docker MOC | updates/docker-moc/updated_note.md | 更新 frontmatter `updated` + 更新日志条目；索引链接未变（标题均保留）。**vault 原 MOC 未改动**，发布待确认 |

## 三、共享资料来源清单

见 [[workspace/update-docker/shared_research/source_bank.md]]：

- 官方/一手：S1 Engine 29 release notes、S2 Desktop release notes、S6 dockerd 文档、S8-S10 Docker daemon proxy 官方文档、S11 WSL 官方
- 社区汇总：S3 endoflife.date、S4-S5 国内镜像源现状、S7 替代方案、S12 WSL 版本
- ⚠️ S5 社区镜像源清单时效波动，须实测

## 四、跳过清单

| 笔记 | 原因 |
|------|------|
| comic-library（如何搭建漫画库） | 用户确认跳过（与全面刷新 Docker 相关性低） |
| github-raw（github文件直链方式） | 非 Docker 主题 |
| sortspec | Obsidian 排序插件内部文件 |
| Docker MOC（正文） | 索引，由 P5 单独同步 |

## 五、未处理风险与建议

| 风险/问题 | 建议 |
|-----------|------|
| 社区镜像源（DaoCloud/1ms.run 等）随时可能失效 | 使用前 `docker pull alpine:latest` 实测；多配置几个；阿里云 ACR 占位符 `https://<your-id>.mirror.aliyuncs.com` 待填 |
| network 原笔记 4 处 ASCII 图 mojibake（`��`，原有） | 后续单独修复 |
| network 示例 `compose version: '3.8'` 已过时（Compose v2 忽略） | 可选清理 |
| `source_project` 字段值不一致（Study-Notes/study-notes/docker/update-docker） | 后续统一为 `study-notes` |
| gid-uid 正文「UID / GID>」疑似损坏行 | 后续修复渲染 |
| created 字段为近似值（用 vault 时间戳 2026-07-28） | 如知真实创作日期可修正 |
| 原文件全部未发布到 vault | 需用户确认发布位置后再 copy/patch |

## 六、下一批建议

- 本次 8 篇已全部完成，无后续批次。
- 若后续需要发布到 Obsidian vault：确认 `publish_mode`（copy/overwrite/patch）与目标目录，可将 `updates/*/updated_note.md` 应用到 `docker/` 目录。
