# 更新报告：iStoreOS爬梯配置指南

## 基本信息

| 项目 | 内容 |
|------|------|
| 笔记路径 | `软路由教程/iStoreOS爬梯配置指南.md` |
| 原更新日期 | 2026-03-07 |
| 本次更新 | 2026-07-11 |
| 更新方式 | patch-in-place |

## 变更摘要

### 已更新（5处）

| 位置 | 变更内容 |
|------|---------|
| Frontmatter | `updated` 日期更新为 2026-07-11 |
| §1 iStoreOS 简介 | 新增「最新版本 24.10.7」特性行 |
| §2.1 插件对比表 | 新增「当前版本」列（Passwall2 26.6.16-1, OpenClash v0.47.096-dev） |
| §2.3 Passwall2 说明 | 补充新版本格式 YY.M.DD-N、仓库迁移、核心组件版本、sing-box DNS 与 xray-core 变更提醒 |
| §4.1 OpenClash 说明 | 补充当前版本号 + v0.47.x 新特性（界面重构、覆写设置、多订阅合并、内核管理） |
| §4.2 OpenClash IPK 示例 | 版本从 `v0.46.033-beta` 更新为 `v0.47.096-beta` |
| §3.1.3 Passwall2 IPK 示例 | 仓库从 `xiaorouji` → `Openwrt-Passwall`，版本从 `v1.28` 更新为 `26.6.16-1` |
| §6 Q1 IPK 示例 | 同上更新 |
| §6 Q1 IPK 下载地址 | 同上更新仓库链接 |
| 参考资料 | Passwall2 Releases 链接更新为 `Openwrt-Passwall` 组织 |
| §4.7 核心模式 | 补充 v0.47.x 已知 Bug（无法自启）+ iStoreOS 24.10.7 升级冲突提醒 |
| 末尾 | 新增「更新记录」章节 |
| 最后更新行 | 日期更新 |

### 未变动

- Passwall 主配置流程和分流规则（基本操作未变）
- 旁路由网络拓扑和配置（网络原理未变）
- 常见问题 Q2-Q6（通用排查方法未变）
- 最佳实践和建议
- 大部分外部参考资料（交叉验证仍有效）

### 资料收集来源

- [iStoreOS 24.10.7 更新日志](https://github.com/istoreos/istoreos/discussions/2971)
- [Passwall2 Releases](https://github.com/Openwrt-Passwall/openwrt-passwall2/releases)
- [OpenClash 更新 v0.47.055-beta](https://openclash.net/openclash-beta-update-release-v0-47-055)
- [HomeProxy DeepWiki](https://deepwiki.com/immortalwrt/homeproxy/1-overview)
- [openwrt-passwall-build SourceForge](https://sourceforge.net/projects/openwrt-passwall-build/)
- [2026年最新PassWall安装教程](https://naiyous.com/10535.html)

## 下次更新关注点

- iStoreOS 后续大版本（如 25.x）是否使用 APK 包格式
- OpenClash v0.47.x 的 auto-start Bug 是否修复
- Passwall2 的新版本发布节奏
