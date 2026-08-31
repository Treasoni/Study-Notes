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
| §3.1.2 / §4.2 | 新增**方案 C**：iStore 手动安装 `.run` 包，作为 iStoreOS 推荐方式（原方案 A/B 保留） |
| §3.1.2 / §4.2 方案 C | `.run` 包来源修正为 **bcseputetto/Are-u-ok 的 iStoreOS_24.10 Release**（原 AUK9527 主仓库仅维护 22.03 的 aarch64 包）；示例文件名修正为真实命名（PassWall2 26.8.27 / OpenClash 0.47.156，`_sdk_24.10` 后缀，OpenClash 为 `+x86_64_core` 内置内核格式） |
| §4.2 方案 A | **修正 OpenClash 安装错误**：删除「从 Passwall SourceForge 源 `opkg install luci-app-openclash`」错误步骤（该源不含 OpenClash），替换为社区一键安装脚本（slobys/openclash-auto-installer，已核实仓库与 `main` 分支） |
| §3.1.2 / §4.2 / §6 | 方案 A/B 补充依赖步骤：`kmod-nft-tproxy` / `kmod-nft-socket`（24.10 nftables 透明代理）与可选 `dnsmasq-full`；OpenClash 方案 B 依赖更新为 24.10 适用集合（`kmod-tun`、`kmod-inet-diag`、`luci-compat` 等） |
| §3.1.2 方案 A | 新增注意：`opkg-key` 为 24.10 专用、SourceForge 源不含 OpenClash、存储空间与 SSR-Plus 冲突提示 |
| §6 Q1 方案一 | 修正固件来源表述：AUK9527 仓库不提供固件（仅插件 `.run` 包），官方固件下载为 fw.koolcenter.com |
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
- [AUK9527/Are-u-ok 插件库（22.03，aarch64）](https://github.com/AUK9527/Are-u-ok)
- [bcseputetto/Are-u-ok — iStoreOS_24.10 Release（.run 包，含 x86_64）](https://github.com/bcseputetto/Are-u-ok/releases/tag/iStoreOS_24.10)
- [slobys/openclash-auto-installer（OpenClash 一键安装脚本）](https://github.com/slobys/openclash-auto-installer)

## 未处理风险

- **OpenClash 自启 Bug**：v0.47.055 的「无法随系统启动」问题是否已在 v0.47.156 彻底修复，无法从远端直接确认，报告采用「升级观察」的保守表述。
- **OpenClash 一键脚本**：slobys/openclash-auto-installer 仓库与 `main` 分支已核实，但脚本本身未逐行审查；安装时菜单选项以脚本实际为准。
- **链接有效性**：未逐一验证全部外部链接是否失效，仅补充了 naiyous 新版文章链接。
- **HomeProxy 标准 OpenWrt 兼容性**：官方主要面向 ImmortalWrt / OpenWrt 23.05+，实际使用仍需用户实测。
- **`.run` 包来源**：bcseputetto/Are-u-ok 为社区维护（原 AUK9527 24.10 维护者接手），文件版本会随上游更新，示例文件名（PassWall2 26.8.27 / OpenClash 0.47.156）为核实时的版本，安装时以 Release 页最新为准。
- **25.12 生态**：25.12 仍为测试版，apk 软件源下的 Passwall 自定义源方案尚在社区磨合，未写入具体命令。

## 下次更新关注点

- iStoreOS 25.12 正式版发布与稳定化情况（包管理器 apk 适配）
- OpenClash 自启 Bug 的社区确认状态
- Passwall2 / sing-box / xray-core 版本发布节奏
- 25.12 下 Passwall 自定义软件源（`/etc/apk/repositories.d/`）的成熟方案
