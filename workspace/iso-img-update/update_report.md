# Update Report — iso和img.md

更新日期：2026-08-27
更新方式：patch-in-place（直接修订 [[iso和img.md]]）
更新人：note-updater

## 变更摘要

| 项目 | 变更 |
|------|------|
| frontmatter | 新增 `title / tags / created / updated / status` |
| 标题结构 | 新增 H1 `# ISO 和 IMG 的区别`；章节 `#`→`##`、小节 `##`→`###`；修 `## 1.4PVE` → `### 1.4 PVE` 等标题空格 |
| 顶部引言 | 原两行 blockquote 包装为 `[!info] 一句话总结`，保留"刻进脑子里"原句 |
| 失效链接 | 原 `PVE的学习/安装和使用PVE教程/PVE存储库.md#4.…`（目录不存在 + 锚点不存在）→ `[[PVE的学习/01-安装配置/PVE存储库#PVE 里的"两种存储库"]]` |
| Callout 修复 | 2.4 末尾 `[!warning]` 原格式损坏（`>` 空行中断）→ 补全语法；标题修正 |
| 大白话 tip | §1.1 ISO、§2.1 IMG 各补 `[!tip] 大白话`；§3 补 `[!tip] 记忆口诀` |
| §2.4 步骤完善 | 4 步 → 5 步：补 `.img.gz` 先解压提示、`/var/lib/vz/template/iso/` 上传说明、"未使用磁盘 → 引导顺序"细节 |
| 更新记录 | 新增 `## 更新记录` 段 |
| 内容保留 | §1.2/§1.3/§2.2/§2.3/§3 对比表/§4 类比/§5 qcow2/raw 原样保留 |

## 来源

- OpenWRT 官方 Wiki「虚拟 iStoreOS 旁路由」：https://wiki.openwrt.xyz/guide/vm/pve/a/istoreos/
- cnblogs「PVE 安装 iStore OS」：https://www.cnblogs.com/txqdm/p/18518395
- 什么值得买「PVE 安装 iStore 手把手图文教程」（2022-12）
- 本地：[[PVE的学习/01-安装配置/PVE存储库]]（`## PVE 里的"两种存储库"` 锚点）

核实结论：笔记中 `qm importdisk 100 istoreos.img local-lvm` 与 `/var/lib/vz/template/iso/` 上传路径均与 2025-2026 年通行做法一致，无需修改命令本身。

## 未处理风险 / 后续建议

1. **MOC 归属未定**：该笔记目前位于 vault 根目录，未加入任何 MOC。它被 [[虚拟机/VMware Workstation Player 安装 Windows 虚拟机.md]] 的"下一步学习"引用为"镜像文件格式介绍"，内容又偏 PVE 场景。
   - 建议 1：在 `虚拟机/虚拟机 MOC.md` 增补 `- [[iso和img.md]] - 镜像文件格式介绍（ISO/IMG/qcow2/raw 区别）`；
   - 建议 2：或迁入 `PVE的学习/` 并在 PVE MOC 登记。**需用户确认后再执行，本次未改动任何 MOC。**
2. **文件位置**：未移动笔记（避免破坏 VMware 笔记现有 `[[iso和img.md]]` 链接）；如日后决定迁移，需同步更新该反链。
3. **未覆盖内容**：未补充 qcow2/raw 的 PVE 命令示例（如 `qemu-img convert`），如需可在下次扩展。

## 产物

- 修订后笔记：`iso和img.md`
- 更新计划：`workspace/iso-img-update/update_plan.md`
- 本报告：`workspace/iso-img-update/update_report.md`
