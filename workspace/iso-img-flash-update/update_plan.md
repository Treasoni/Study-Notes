# Update Plan — 虚拟机/ISO与IMG镜像烧录方法对比.md

更新日期：2026-09-17
更新方式：patch-in-place（直接修订 vault 内原笔记，文件名不变）
更新目标：把 `.img` / `.raw` / `.qcow2` 三种磁盘镜像格式统一纳入全篇框架
更新触发：用户请求「`.img/.raw/.qcow2` 更新一下，把这几个的也加入一下」
用户确认范围：**全篇扩写，文件名保持 `ISO与IMG镜像烧录方法对比.md` 不变**

## 更新前的状态诊断

正文里 `.raw` / `.qcow2` 其实已经零散出现（第二章「常见后缀」、第五章标题、第六章判类型表），
但**标题、frontmatter tags、第一章框架、第三章工具层、第四章流程层**都只写「IMG」，
读起来像是「只讲 ISO 和 IMG 两种」；且 `.qcow2` 与 `.img` / `.raw` 的**本质差异（容器格式 vs 裸镜像）全文没有交代过**，
导致「qcow2 能不能直接写 U 盘」这个高频问题没有落点。

## Stale Map

| 现有内容 | 处理 | 去向 |
|---|---|---|
| frontmatter `title` / `tags` | 更新 | 标题加 `raw` / `qcow2`；tags 增 `raw`、`qcow2`；`updated` → 2026-09-17 |
| H1 标题 | 更新 | `ISO 与 IMG / raw / qcow2 镜像烧录/写盘方法对比` |
| 位置：H1 之后 | 新增 | `[!note] 标题里的三个后缀`——声明正文中「IMG」= 磁盘镜像整类 |
| 顶部 `[!info] 一句话结论` | 更新 | 主语改「IMG / raw / qcow2」，新增第 3 条「qcow2 多一道门槛」 |
| 目录 6 条 | 更新 | 1/3/4 条同步框架用词；2/4 条补括注 |
| 第一章 H2 + 配套关系 + 一句话结论 | 更新 | 同步三分法；结论里点明 qcow2 只在虚拟机享受「导入即启动」 |
| 第一章「第一层：工具层」表 + 4 条要点 + 大白话 | 更新 + 新增 | 表头改「是否区分 ISO / 磁盘镜像」；新增第 4 条要点（qcow2 四类工具都不能直接写）与一条 `[!warning] 一个高频误解`（改后缀≠转换） |
| 第一章「第二层：流程层」表 + 要点 + 大白话 | 更新 + 新增 | 表头改「IMG / raw（成品盘式）」；新增 qcow2 要点与大白话收尾句 |
| 第一章「为什么会有这两层」 | 更新 | 补 qcow2 的容器格式定位 |
| 第一章 本章小结 | 更新 | 四条全部改为三分法 |
| 第二章「IMG / raw：一整块硬盘的克隆」 | 更新 | 标题加「（裸镜像）」；`[!note] 常见后缀` → `同一类里的几个后缀`（补 `.raw` 官方出处、`.qcow2` 指引） |
| 位置：第二章该节之后 | 新增 | `### qcow2：同一块盘，被装进了 QEMU 的「容器」`——裸镜像 vs 容器格式 5 行对照表、`[!summary] 结论`、`qemu-img info` / `convert` 三条命令、`[!tip] 大白话`、出处段 |
| 第二章「一张表看懂」 | 更新 | 2 列 → 3 列（ISO / IMG·raw 裸镜像 / qcow2 容器），7 行全部重写 |
| 第二章 小结 | 更新 | 加 qcow2 一条，改四条 |
| 第三章 H2 + 引言 | 更新 | 说明 qcow2 是四类工具的共同盲区 |
| 第三章 Etcher 节 | 更新 | 标题、`.raw` 同为一串字节、新增「qcow2 不能喂给 Etcher」 |
| 第三章 Rufus 节 | 更新 | DD 模式适用对象补 `.vhd/.vhdx`；新增 Rufus 面向线性镜像（附 FAQ 原文出处）；新增 qcow2 先转换 |
| 第三章 Ventoy 节 | 更新 | 新增官方支持列表「ISO/WIM/IMG/VHD(x)/EFI 等」+ Linux vDisk 覆盖 vhd/vdi/raw，**不含 qcow2** |
| 第三章 dd 节 | 更新 | 新增 qcow2 先转换的两行命令；错误点 2 条 → 3 条 |
| 第三章 工具层速览 | 更新 | 5 列表扩为 6 列（新增 `.qcow2` 怎么办）；小结补第四种哲学 |
| 第四章 H2 + 引言 | 更新 | 标题改「IMG / raw 成品盘式」；引言点明 qcow2 在物理机没有自己的流程 |
| 第四章 流程 A 标题 / 步骤 3 / warning 表头 | 更新 | 同步用词 |
| 第四章 一句话对照 | 更新 | 新增第 3 条「手里只有 .qcow2 → 先转换再走 IMG 流程」 |
| 第五章 PVE 路径 2 | 更新 | 新增 `[!tip] 三种后缀在 PVE 里的待遇` + 反向导出命令 |
| 第五章 virt-install 路径 2 | 更新 | 新增 `--disk` 接受 `.img` / `.raw` / `.qcow2` |
| 第五章 小结 | 更新 | 补「虚拟机是 qcow2 唯一能直接当盘用的地方」 |
| 第六章 第一步表 | 更新 | `.qcow2` 行改写；新增 `.vhd/.vhdx` 行；`[!tip] 记忆` 改三分法 |
| 第六章 第二步表 | 更新 | 刷固件行补 `.raw`；新增「把 .qcow2 用到物理机」「查看/转换镜像格式」两行 |
| 第六章 坑清单 | 新增 | 新增第 8 条「把 `.qcow2` 当裸镜像直接写盘（或改后缀蒙混）」 |
| 第六章 最终版回答 / 本章小结 | 更新 | 三分法；「七个坑」→「八个坑」 |
| 位置：文末 | 新增 | `## 更新记录` |
| `虚拟机/虚拟机 MOC.md` | 更新 | 索引行改写 + `updated` → 2026-09-17 |
| `iso和img.md`（概念篇） | **不动** | 其 §5 已有 `.qcow2` / `.raw` 小节，本次不越界修改 |

## 新增的实质内容（不只是改称呼）

1. **裸镜像 vs 容器格式**——qcow2 文件第 0 字节是文件头（v2 72 字节 / v3 ≥104 字节）而不是 MBR/GPT；
   按簇分配所以文件小；支持内部快照 / zlib 压缩 / backing file。
2. **`qemu-img` 三个频率最高的命令**——`info`、`convert -f qcow2 -O raw`（拆）、`convert -f raw -O qcow2`（装）。
3. **「改后缀 ≠ 转换」**——放进出错率最高的一类，同时进坑清单。
4. **工具层把 qcow2 单列**——原来四类工具表里没有它的位置。
5. **PVE 的不对称待遇**——`.img` / `.raw` / `.qcow2` 在 PVE 里都能直接 `qm disk import`，不用手动转换；
   反过来物理机只有 `.img` / `.raw` 能直接写。

## 资料收集（2026-09）

| 来源 | 用途 | URL |
|---|---|---|
| QEMU qcow2 格式规范 | 文件头位置与长度、簇分配、内部快照、backing file | https://www.qemu.org/docs/master/interop/qcow2.html |
| qemu-img 手册 | `convert` 语义、`-f` / `-O`、raw 为默认格式 | https://www.qemu.org/docs/master/tools/qemu-img.html |
| QEMU 磁盘镜像文档 | raw vs qcow2 定位（simple / most versatile / 快照 / backing） | https://www.qemu.org/docs/master/system/images.html |
| Ventoy 官网首页 | 可启动类型列表「ISO/WIM/IMG/VHD(x)/EFI 等」；Linux vDisk 覆盖 vhd/vdi/raw | https://www.ventoy.net/cn/index.html |
| Proxmox qm 手册（沿用缓存） | `qm disk import` 要求「镜像格式必须被 qemu-img 支持」 | https://pve.proxmox.com/pve-docs/qm.1.html |
| Rufus 官方 Wiki FAQ（沿用缓存） | 可像打开 `.iso` 一样直接打开并写入 `.vhd`/`.vhdx` | https://github.com/pbatard/rufus/wiki/FAQ |

## 不做的事

- 不改文件名、不移动笔记（避免破坏 MOC 与其它反链）
- 不重写未受影响的小节（ISO 结构、isohybrid、物理机/虚拟机分步流程正文均保持原样）
- 不修改 `iso和img.md`（概念篇）
- 不回写 `workspace/iso-img-flash-comparison/output/final_note.md`（见 update_report 的漂移登记）
