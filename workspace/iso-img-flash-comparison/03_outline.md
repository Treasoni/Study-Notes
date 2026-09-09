## 学习笔记大纲：《ISO 与 IMG 镜像烧录/写盘方法对比》

> 笔记类型：对比 + 实战操作（结论先行 → 结构原因 → 分工具/场景逐项对比 → 速查与避坑，对比中内嵌实操步骤）
> 预计总篇幅：约 20-24 页（短 1 + 中 3 + 长 2）
> 章节数：6 章
> 关联笔记：[[iso和img.md]]（vault 根目录「概念篇」，本文为「操作篇」，全文互链）
> 核心结论（供速览）：不能一概而论——工具层「是否相同」视工具而定（Etcher/dd 几乎一致，Rufus/Ventoy 区分处理）；流程层「是否相同」视场景而定（物理机与虚拟机的 ISO 路径都要先进安装器，IMG 路径「导入/写入即启动」）。

---

### 第一章：一句话结论 —— ISO 与 IMG 烧录方法「分两层看」
> 开篇直接回答「方法/操作是否相同」，给出两分法结论框架与全文导航。

- **篇幅**：短
- **覆盖要点**：工具层结论（逐字节写盘 vs 双模式工具）、流程层结论（安装器式 vs 成品盘式）、本笔记读法
- **素材引用**：S1, S3, S5, S7
- **代码示例**：无

### 第二章：镜像结构差异 —— 为什么处理方式会不一样
> 讲清 ISO=光盘文件系统镜像/安装介质、IMG=整盘扇区镜像（自带分区表+引导+系统），以及 isohybrid 混血特性如何成为分界点。

- **篇幅**：中
- **覆盖要点**：ISO9660/光盘介质本质、isohybrid 尾部附加分区表与引导、IMG/raw 整盘扇区镜像（GPT/MBR+引导+文件系统）、结构差异如何决定「能否当磁盘镜像直写」
- **素材引用**：S1, S3, S5, S7, S8
- **代码示例**：无（可用表格对比两者结构）

### 第三章：工具层对比 —— Etcher / Rufus / Ventoy / dd 对 ISO 与 IMG 的处理
> 逐工具拆解：每个工具对 ISO 与 IMG 是「一视同仁」还是「区分模式」。

- **篇幅**：长
- **覆盖要点**：balenaEtcher 逐字节写入、无模式之分、Windows ISO 例外；Rufus ISO Image mode vs DD Image mode、.img 自动走 DD、isohybrid 用 DD 的坑；Ventoy 不烧录只拷贝 + OpenWrt IMG 需 ventoy_openwrt.xz 插件及支持范围；dd 块级「转换并拷贝」对 iso/img 本身无差别（目标须是整盘）
- **素材引用**：S1, S2, S3, S4（dd 细节为通用知识，见研究文件 gap #5）
- **代码示例**：有（`dd if=x.img of=/dev/sdX bs=4M status=progress conv=fsync` 及「目标整盘非分区」说明）

### 第四章：物理机两种刷机流程 —— IMG 成品盘式 vs ISO 安装器式
> 以 iStoreOS（IMG 范式）与 Ubuntu（ISO 范式）两个官方流程作对照，点出「写盘之后是否还有安装阶段」这一本质差异。

- **篇幅**：中
- **覆盖要点**：iStoreOS 固件 .img.gz 下载后「不解压」→ Rufus 写 U 盘 → U 盘引导 → quickstart → Install X86 → 写内置盘拔盘直启；Ubuntu ISO → Rufus「保留 ISO Image mode」→ U 盘引导 → Try/Install 安装向导；两种范式的本质对照
- **素材引用**：S5, S7, S3
- **代码示例**：无（实操以 Rufus 界面选项 + quickstart 步骤描述为主）

### 第五章：虚拟机两种用法 —— ISO 虚拟光驱安装 vs IMG/raw/qcow2 磁盘导入直启
> 覆盖 PVE 与 libvirt/virt-install 两套入口，分别对应「挂光驱 + 空盘走安装器」与「导入既有磁盘即启动」。

- **篇幅**：长
- **覆盖要点**：PVE 侧 ISO 路径（镜像传至 iso 区 → `-cdrom` 挂只读光驱 + 空盘 → 安装器落盘）；PVE 侧磁盘直启路径（`qm disk import` 导入 unused 磁盘 → attach → boot order，及新写法 `import-from=` 导入即挂盘、virtio-scsi + boot 顺序建议）；virt-install 侧对应（`--cdrom` vs `--location` vs `--import`、`--disk device=cdrom|disk`）
- **素材引用**：S8, S9
- **代码示例**：有（`qm create -cdrom`/`qm disk import`/`import-from=`、`virt-install --cdrom`/`--location`/`--import` 命令片段）

### 第六章：速查表、常见坑与延伸 —— 实操前必看
> 收束为可执行清单：先判镜像类型再选工具，列出高频坑，并与「概念篇」互链收尾。

- **篇幅**：中
- **覆盖要点**：先判类型（.iso=安装介质 / .img .raw=磁盘镜像）；工具×镜像类型速查表（Rufus/Etcher/Ventoy/dd）；常见坑——.img.gz 未解压或未整盘写入、选错目标盘、isohybrid 误用 DD 模式、刷完不引导（Secure Boot/引导顺序/GPT 备份）、Ventoy 不能通吃任意 IMG、Windows ISO 用 Etcher 不适用；延伸——引导 iso 与系统盘区分、互链 [[iso和img.md]]
- **素材引用**：S1, S3, S4, S5, S8
- **代码示例**：无（速查表 + 检查清单为主）

---

## 学习路径说明

### 前置要求
- 已理解 ISO（安装介质）与 IMG（成品盘）的基本定义 —— 由 [[iso和img.md]] 打底
- 具备 Rufus/balenaEtcher、或 PVE/虚拟机基础中的任意一项即可，其余在文中补齐
- 实操需准备：一块 U 盘（物理机刷机）或一台 PVE/libvirt 宿主机（虚拟机练习）

### 学完能做什么
- 面对任意 .iso / .img / .img.gz / .raw / .qcow2，能先判断类型再选择正确工具与模式
- 能独立把 iStoreOS/OpenWrt 系成品固件写入 U 盘并完成物理机直启安装
- 能在 PVE 或 virt-install 中给虚拟机挂 ISO 走安装器，或用 `qm disk import`/`--import` 直启既有磁盘镜像
- 能识别并避开 .img.gz 未解压、目标盘写错、isohybrid 误用 DD、Ventoy 兼容性等高频坑

### 建议学习顺序
- 顺序通读（约 60-90 分钟）：第一章定框架 → 第二章补结构 → 第三至五章按需精读工具/物理机/虚拟机 → 第六章对照速查与避坑
- 跳读方案：只刷软路由固件 → 重点第四、六章；只玩虚拟机 → 重点第五、六章；只纠结工具选择 → 重点第三、六章
- 每章写作完成后建议先核对「素材引用」对应官方源，再进入下一章
