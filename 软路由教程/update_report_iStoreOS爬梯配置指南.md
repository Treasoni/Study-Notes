# 更新报告：iStoreOS爬梯配置指南

## 基本信息

| 项目 | 内容 |
|------|------|
| 笔记路径 | `软路由教程/iStoreOS爬梯配置指南.md` |
| 原更新日期 | 2026-07-11 |
| 本次更新 | 2026-08-31 |
| 更新方式 | patch-in-place |

## 变更摘要

### 已更新

| 位置 | 变更内容 |
|------|---------|
| Frontmatter | `updated` 更新为 2026-08-31 |
| §1 特性表 | 最新版本 24.10.7 → 24.10.8；新增 25.12 测试版说明 callout（opkg→apk、不支持保留配置升级） |
| §2.1 插件对比表 | 当前版本更新：OpenClash v0.47.156、Passwall 26.8.11-1、Passwall2 26.8.27-1、HomeProxy v0.0.11；HomeProxy 适配系统补充 OpenWrt 23.05+ |
| §2.3 Passwall2 版本说明 | 核心组件更新：xray-core 26.7.28、sing-box 1.13.19；明确 v1/v2 为独立仓库 |
| §2.3 HomeProxy 注意 | 系统要求补充依赖（firewall4 / kmod-nft-tproxy / ucode-mod-digest），说明不支持 XHTTP 节点 |
| §3.1.3 / §6 方案 B | Passwall2 IPK 下载版本 26.6.16-1 → 26.8.27-1 |
| §3.1.3 / §6 方案 A | 新增 25.12（apk）用户注意 |
| §4.1 OpenClash 说明 | 当前版本 v0.47.096-dev → v0.47.156（2026-08-10） |
| §4.2 OpenClash IPK | 下载版本 v0.47.096-beta → v0.47.156 |
| §4.6 已知问题 | 自启 Bug 改为「升级到最新版观察」表述；24.10.7 → 24.10.8 升级冲突 |
| §6 排查脚本 | 新增 25.12（apk）命令提示 |
| 更新记录 | 新增 2026-08-31 条目 |
| 最后更新行 | 更新为 2026-08-31 |
| 参考资料 | 补充 naiyous 10947、Passwall（v1）Releases |
| §3.1.2 / §4.2 | **删除**「通过 iStore 搜索安装」的无效步骤；备选安装方案章节重排为 §3.1.2 / §4.2「安装 Passwall / OpenClash」 |
| §3.1.2 / §4.2 | 新增**方案 C**：iStore 手动安装 `.run` 包（AUK9527/Are-u-ok），作为 iStoreOS 推荐方式（原方案 A/B 保留） |
| §6 Q1 建议顺序 | 加入「iStore 手动安装 `.run` 包（推荐）」 |

### 未变动

- Passwall 主配置流程和分流规则（基础操作未变）
- 旁路由网络拓扑和配置（网络原理未变）
- 常见问题 Q2-Q6（通用排查方法未变）
- 最佳实践和安全建议
- MOC 章节锚点（章节结构未变化，`[[软路由教程MOC]]` 链接仍有效，未修改 MOC）

### 资料收集来源

- [iStoreOS 24.10.8 更新日志](https://github.com/istoreos/istoreos/discussions/3000)
- [iStoreOS 25.12 测试和反馈](https://github.com/istoreos/istoreos/discussions/3008)
- [iStoreOS 25.12 尝鲜版上线一周社区反馈](https://post.smzdm.com/p/a70d283g/)
- [OpenClash Releases（Release Alert）](https://releasealert.dev/github/vernesong/OpenClash)
- [Passwall2 Releases](https://github.com/Openwrt-Passwall/openwrt-passwall2/releases)
- [Passwall Releases](https://github.com/Openwrt-Passwall/openwrt-passwall/releases)
- [HomeProxy 安装与设置（DeepWiki）](https://deepwiki.com/immortalwrt/homeproxy/2-installation-and-setup)
- [iStoreOS 通过 iStore .run 安装 passwall、OpenClash 插件](https://www.zoio.net/2026/01/istoreos-passwall.html)
- [AUK9527/Are-u-ok 插件库（.run 包）](https://github.com/AUK9527/Are-u-ok)

## 未处理风险

- **OpenClash 自启 Bug**：v0.47.055 的「无法随系统启动」问题是否已在 v0.47.156 彻底修复，无法从远端直接确认，报告采用「升级观察」的保守表述。
- **OpenClash IPK URL 格式**：示例中的 tag（`v0.47.156`）以 releases 页实际标签为准，可能需要微调。
- **链接有效性**：未逐一验证全部外部链接是否失效，仅补充了 naiyous 新版文章链接。
- **HomeProxy 标准 OpenWrt 兼容性**：官方主要面向 ImmortalWrt / OpenWrt 23.05+，实际使用仍需用户实测。
- **`.run` 包下载**：方案 C 中 AUK9527 插件库的具体文件路径/命名以仓库实际为准，示例仅作演示。
- **25.12 生态**：25.12 仍为测试版，apk 软件源下的 Passwall 自定义源方案尚在社区磨合，未写入具体命令。

## 下次更新关注点

- iStoreOS 25.12 正式版发布与稳定化情况（包管理器 apk 适配）
- OpenClash 自启 Bug 的社区确认状态
- Passwall2 / sing-box / xray-core 版本发布节奏
- 25.12 下 Passwall 自定义软件源（`/etc/apk/repositories.d/`）的成熟方案
