# 动手 · VMware Workstation：给 Windows 11 建一台虚拟机

前面几章用 VirtualBox 建过 Ubuntu，但若想在虚拟机里装 Windows 11，会发现 VBox 建机向导没有 vTPM 这一步，而 Windows 11 对可信平台模块有硬性要求，直接装容易卡在硬件检查。这章换同为 Type 2 的商业选手 VMware Workstation，把「Windows 11 + vTPM」这条 VBox 缺源的路线走通。

## 7.1 VMware Workstation：商业 Type 2，为什么需要它

VMware Workstation 是 VMware 出品的桌面虚拟化软件，与 VirtualBox 一样是 Type 2 托管型 Hypervisor：它作为普通应用装在宿主操作系统之上，而不是直接装在硬件上。[^c7-2]

- **Workstation Player**：免费版，界面精简，够建机、跑系统。
- **Workstation Pro**：付费版，功能更全（快照、克隆、高级网络等）。
- 2023 年 Broadcom 收购 VMware 后，授权与价格常有调整，具体**以官网为准**。

已有 VirtualBox 为何还要单独开这章？VirtualBox 开源免费、适合入门（第 5 章 Ubuntu 就是它装的）；VMware 则在 Windows 11 场景有官方路径——创建 Windows 11 客户机时，Workstation 会自动添加 vTPM（虚拟可信平台模块），让 Win11 通过安装检查。[^c7-1]

> [!tip] 大白话：vTPM 是什么？
> 把 TPM 想成主板上的一把「硬件锁」，系统开机先对暗号，确认机器没被掉包。真电脑装 Win11 需要这把锁；VMware 就在虚拟机里用软件造一把虚拟锁（vTPM），Win11 看见锁在，就肯继续装了。

## 7.2 Typical 向导建机，逐步入

流程和第 5 章大同小异，跟「新建虚拟机」向导的 Typical（典型）配置走即可；它适合大多数情况，只有要改硬件兼容版本、磁盘类型等细节时才选 Custom（自定义）。[^c7-1]

1. **选 ISO**：启动「新建虚拟机」向导，配置类型选「典型」；客户机操作系统来源选「安装程序光盘映像文件 (ISO)」，指向准备好的 Windows 11 镜像。[截图：新建虚拟机向导 - 选择 ISO]
2. **选系统**：客户机操作系统类型选 `Windows 11 x64`，下一步——这正是向导自动添加 vTPM 的触发条件。[^c7-1][截图：客户机操作系统 - Windows 11 x64]
3. **命名与目录**：输入虚拟机名称与存放目录，下一步；所在磁盘留足空间，这个文件夹以后会越变越大。[截图：命名与位置]
4. **加密与 vTPM**：选加密类型、设密码。加密范围二选一：加密全部文件，或「仅加密支持 vTPM 设备所需的最小文件数」——日常学习选最小加密即可，更快也满足要求。[^c7-1][截图：选择加密范围]
5. **磁盘**：设置虚拟磁盘大小（典型配置还会问是否拆成多个文件）。沿用第 5 章铁律：够用即可，别把宿主磁盘塞满。
6. **Customize Hardware（可选）**：想调内存、CPU、固件可以点开改，创建后再改也行，这步可直接跳过。[^c7-1]
7. **创建**：勾选「创建后开启此虚拟机」并完成，向导随即开机进入 Windows 11 安装。[截图：向导完成]

> [!tip] 大白话：为什么加密和 vTPM 绑在一起？
> 加密是给虚拟机文件上「保险箱锁」，没密码谁也打不开；vTPM 是保险箱里那把「硬件锁」。Windows 11 要两者配合才肯干活，所以向导把它俩放在同一步，你只输一次密码。

## 7.3 Windows 11 特例：装完别删加密和 vTPM

- **自动加 vTPM**：选 Windows 11 x64 后，Workstation 会自动把 vTPM 加进虚拟机，这是安装能通过硬件检查的关键。[^c7-1]
- **装后不要移除**：官方手册建议，装完 Windows 11 后，不要为了「更流畅」把加密或 vTPM 从虚拟机中移除，否则会影响 Windows 11 的使用体验。[^c7-1]
- **远程 VM 不支持**：Workstation 不支持在远程虚拟机上创建 Windows 11 客户机，想装 Win11 要在本机建。[^c7-1]

## 7.4 与 VirtualBox 的异同小结

拉回第 3 章那张「虚拟机 = 参数 + 文件」的地图：两者同为 Type 2，都由配置文件加虚拟磁盘镜像描述一台机器，建机都走向导。差异集中在授权、开源和 Windows 11 路径上：

| 对比维度 | VMware Workstation | Oracle VirtualBox |
| --- | --- | --- |
| 许可证 | Player 免费、Pro 付费（商业软件，以官网为准） | 开源免费 |
| 是否开源 | 否（闭源商业） | 是 |
| Win11 + vTPM 路径 | 向导自动加 vTPM 并要求加密（官方手册路径） | 建机向导无 vTPM 步骤，装 Win11 需自行处理（本笔记不展开） |
| 图形化完整度 | 社区认为最完善，克隆/快照/网络配置一键完成 | 社区认为功能完整、操作逻辑简单 |
| 适合人群 | 愿付费、需 Win11 场景与丰富教程的开发者 | 零成本入门、开源爱好者、基础练习 |

表中「图形化完整度」两行转述自博客园的社区对比，属个人经验、无基准测试，以本机实测为准。[^c7-2]

## 本章小结

- VMware Workstation 是商业 Type 2 托管型 Hypervisor：Player 免费、Pro 付费；Broadcom 收购后授权与价格以官网为准。
- 建 Windows 11 客户机时，Workstation 自动添加 vTPM 并要求加密；选「仅加密最小文件」即可满足日常学习。
- Typical 向导路径：选 ISO → Windows 11 x64 → 命名/目录 → 加密/vTPM → 磁盘 →（可选）Customize Hardware → 创建。
- 两条官方红线：装完 Win11 后不要移除加密或 vTPM；远程虚拟机不支持创建 Windows 11 客户机。
- 与 VirtualBox 同为 Type 2，主要差别在许可证、开源性与 Win11 + vTPM 支持路径。

免费与商业工具都试过以后，下一章把镜头拉远：什么时候真的该用虚拟机？Windows 桌面的 WSL2、Hyper-V、VMware、VirtualBox 四套方案怎么选？我们给一张决策地图。

## 参考来源

[^c7-1]: VMware（Broadcom）官方中文手册《在 Workstation 中的虚拟机上安装 Windows 11》：新建虚拟机向导步骤、Windows 11 x64 触发自动添加 vTPM、最小加密范围、装后勿移除加密/vTPM、远程 VM 不支持 Win11 客户机（`sources/09_techdocs_broadcom_com.md`）。
[^c7-2]: 博客园 sunlong88《VMware Workstation，Hyper-V，wsl2，VirtualBox 区别》：VMware/VirtualBox 同为 Type 2 托管型、付费与开源属性、图形化完整度对比（社区经验，以实测为准）（`sources/08_www_cnblogs_com.md`）。
