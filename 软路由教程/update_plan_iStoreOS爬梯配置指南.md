# 更新计划：iStoreOS爬梯配置指南

## 基本信息

| 项目 | 内容 |
|------|------|
| 笔记路径 | `软路由教程/iStoreOS爬梯配置指南.md` |
| 原更新日期 | 2026-07-11 |
| 计划更新 | 2026-08-31 |
| 更新方式 | patch-in-place |
| 触发原因 | 版本信息过时（iStoreOS / OpenClash / Passwall / Passwall2 / 核心组件） |

## Stale Map

### 保留

- §3 Passwall 主配置流程、分流规则（基础操作未变）
- §5 旁路由网络拓扑和配置（网络原理未变）
- §6 常见问题 Q2-Q6（通用排查方法未变）
- 最佳实践、安全建议
- 大部分外部参考资料（交叉验证仍有效）

### 需要更新

| 位置 | 旧内容 | 新内容 | 来源 |
|------|--------|--------|------|
| frontmatter `updated` | 2026-07-11 | 2026-08-31 | — |
| §1 特性表「最新版本」 | 24.10.7（2026-06-05） | 24.10.8（2026-07-31，稳定版） | istoreos discussion #3000 |
| §2.1 对比表「当前版本」 | OpenClash v0.47.096-dev / Passwall 26.6.16-1 / Passwall2 26.6.16-1 | v0.47.156 / 26.8.11-1 / 26.8.27-1 | GitHub releases |
| §2.1 对比表「适配系统」 | HomeProxy 仅 ImmortalWrt | ImmortalWrt / OpenWrt 23.05+ | DeepWiki / kenzok8 |
| §2.3 Passwall2 版本说明 | xray-core 26.6.1 / sing-box 1.13.13 | 26.7.28 / 1.13.19 | passwall2 26.8.20-1 打包信息 |
| §3.1.3 / §6 方案 B IPK 下载 | Passwall2 26.6.16-1 | 26.8.27-1 | passwall2 releases |
| §4.1 OpenClash 版本 | v0.47.096-dev（2026-05） | v0.47.156（2026-08-10） | releasealert.dev |
| §4.2 OpenClash IPK 下载 | v0.47.096-beta | v0.47.156 | releasealert.dev |
| §4.7 已知问题 | iStoreOS 24.10.7 升级冲突 | 24.10.8 升级冲突；自启 Bug 改为「升级观察」表述 | 更新日志 |

### 需要删除

- 无（无失效或重复内容需要删除）

### 需要新增

| 位置 | 内容 |
|------|------|
| §1 | 25.12 测试版说明 callout（opkg→apk、不支持保留配置升级、升级路径、稳定版建议） |
| §2.3 | Passwall v1 与 Passwall2 为独立仓库、版本各自推进 |
| §3.1.3 / §6 方案 A | 25.12（apk）用户注意（软件源配置位置与命令差异） |
| §6 排查脚本 | 25.12（apk）命令对照提示 |
| 参考资料 | 补充 naiyous 10947 新版链接、Passwall v1 Releases |

## 执行清单

- [x] 局部 patch 原笔记（不重写未过时段落）
- [x] 更新 `updated` frontmatter
- [x] 追加 `## 更新记录` 条目
- [x] 检查双链 / MOC（章节结构未变化，MOC 锚点有效，无需更新）
