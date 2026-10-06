# Update Report — 虚拟机/ISO与IMG镜像烧录方法对比.md

更新日期：2026-09-17
更新方式：patch-in-place（直接修订 vault 内原笔记）
更新人：note-updater
触发：用户「`.img/.raw/.qcow2` 更新一下，把这几个的也加入一下」
用户确认范围：**全篇扩写，文件名不变**（三选一里选了推荐项）

## 变更摘要

| 项目 | 变更 |
|---|---|
| frontmatter | `title` → `ISO 与 IMG / raw / qcow2 镜像烧录/写盘方法对比`；tags 增 `raw`、`qcow2`；`updated` → 2026-09-17 |
| H1 | 同步改名；其后新增 `[!note] 标题里的三个后缀`，声明「IMG」在正文中代表磁盘镜像整类 |
| 一句话结论（顶部 + 第一章） | 改为三分法，并在顶部结论新增第 3 条「qcow2 多一道门槛」 |
| **新增小节（第二章）** | `qcow2：同一块盘，被装进了 QEMU 的「容器」`——裸镜像 vs 容器格式 5 行对照表 + `qemu-img info/convert` 三条命令 + 大白话类比 + 官方出处 |
| 章节框架 | 第一 / 三 / 四 / 六章的标题、导语、结论段统一改为「ISO / IMG·raw / qcow2」三分法 |
| 三张速查表 | 第二章「一张表看懂」2 列 → 3 列；第三章「工具层速览」5 列 → 6 列（新增「`.qcow2` 怎么办」）；第六章「第一步判类型」改写 + 新增 `.vhd/.vhdx` 行、「第二步工具速查」新增 2 行 |
| 高频坑清单 | 7 条 → 8 条，新增「把 `.qcow2` 当裸镜像直接写盘（或改后缀蒙混）」 |
| 工具层 | 四类工具表下新增第 4 条要点（qcow2 是四类工具共同盲区）；Etcher / Rufus / Ventoy / dd 四节各补 qcow2 处置方式 |
| 虚拟机章 | PVE 路径 2 新增 `[!tip] 三种后缀在 PVE 里的待遇` + 反向导出命令；virt-install 补 `--disk` 接受三种格式 |
| 物理机章 | 一句话对照新增「手里只有 `.qcow2` → 先转换再走 IMG 流程」 |
| 更新记录 | 文末新增 `## 更新记录`（2026-09-09 初版 / 2026-09-17 本次） |
| MOC | `虚拟机/虚拟机 MOC.md` 索引行改写 + `updated` → 2026-09-17 |
| 篇幅 | 34.5 KB → 47.5 KB（+13.0 KB，+38%） |

## 本次真正新增的知识点（不是只改称呼）

1. **裸镜像 vs 容器格式**：`.img` / `.raw` 是裸的（文件第 0 字节 = 盘的第 0 字节），`.qcow2` 是 QEMU 容器
   （首个簇是文件头，v2 固定 72 字节 / v3 至少 104 字节；按簇分配；支持内部快照 / 压缩 / backing file）。
2. **`qemu-img` 三条命令**：`info` 看格式与占用；`convert -f qcow2 -O raw` 拆成裸盘写物理机；
   `convert -f raw -O qcow2` 收成容器给虚拟机用。
3. **「改后缀 ≠ 转换」**：只改名不改内容，写出来仍是不可引导的盘——已单独做成 `[!warning]` 并进坑清单第 8 条。
4. **工具层把 `.qcow2` 单列**：原来四类工具表里根本没有它的位置，现在明确「四类都不能直接写」。
5. **PVE 的不对称**：`.img` / `.raw` / `.qcow2` 在 PVE 里都能直接 `qm disk import`（PVE 自己按目标存储格式落盘）；
   反过来物理机上只有 `.img` / `.raw` 能直接写。

## 来源

- QEMU qcow2 格式规范：https://www.qemu.org/docs/master/interop/qcow2.html
- qemu-img 手册：https://www.qemu.org/docs/master/tools/qemu-img.html
- QEMU 磁盘镜像文档：https://www.qemu.org/docs/master/system/images.html
- Ventoy 官网首页（可启动类型列表）：https://www.ventoy.net/cn/index.html
- Proxmox qm 手册（沿用 2026-09 缓存）：https://pve.proxmox.com/pve-docs/qm.1.html
- Rufus 官方 Wiki FAQ（沿用 2026-09 缓存）：https://github.com/pbatard/rufus/wiki/FAQ

核实说明：`.raw` ≈ `.img`（QEMU 默认 raw 格式）、qcow2 文件头长度、qcow2 支持内部快照与 backing file、
Ventoy 支持列表不含 qcow2 —— 以上四条均回源逐条比对后再落笔。

## 未处理风险 / 后续建议

1. **vault / workspace 漂移（已存在，本次扩大）**
   - vault 侧（权威稿，已本次更新）：`虚拟机/ISO与IMG镜像烧录方法对比.md`，47,496 B，mtime 2026-09-17 22:20
   - workspace 侧（停在组装阶段）：`workspace/iso-img-flash-comparison/output/final_note.md`，34,562 B，mtime 2026-09-09 23:25；
     同项目 `chapters/*.md` 6 个文件共 33,761 B，同样停在 2026-09-09
   - 本次**只改了 vault 一侧**，两边差距从「美化版 vs 组装版」进一步拉大。
   - 处置建议（需用户选）：**以 vault 为准、弃用 workspace 副本**（推荐，`iso-img-flash-comparison` 工作流 run 已 `current_phase: done`），
     或重跑组装把 vault 稿回灌 workspace。**本次未擅自回写 workspace。**
2. **`iso和img.md`（概念篇）未同步**：它的 §5 有 `.qcow2` / `.raw` 小段，但与本文新增的「裸镜像 vs 容器格式」深度不一致。
   如果要两篇口径对齐，需要另起一次 note-updater（该笔记另有 `workspace/iso-img-update/` 记录，其中「未覆盖内容」一条
   本就写着「未补充 qcow2/raw 的 PVE 命令示例（如 `qemu-img convert`）」）。
3. **`.vhd` / `.vhdx` 只做了轻量纳入**：出现在第三章 Rufus 节与第六章判类型表，没有独立小节。
   如需展开（Rufus 直接写 VHD、虚拟化平台导入），可再来一轮。
4. **工作流 run 未改动**：`workspace/workflow-runs/iso-img-flash-comparison.workflow.md` 仍是 `current_phase: done` /
   `quality_gate: passed`。本次是有确认范围的既有笔记更新，未新建或重开 workflow run。

## 与本次会话无关的改动（提醒，非本会话所改）

- `linux/linux的LVM管理.md` 在本次会话开始前就已是 modified（`git status --short` 初次检查即存在），未触碰。

## 产物

- 修订后笔记：`虚拟机/ISO与IMG镜像烧录方法对比.md`
- 更新计划：`workspace/iso-img-flash-update/update_plan.md`
- 本报告：`workspace/iso-img-flash-update/update_report.md`
