# 动手 · VirtualBox（下）：增强功能、关机、快照与网络

上一章用 VirtualBox 建好了虚拟机并装好 Ubuntu。这一章把日常使用要补的四件事讲完：装增强功能、分清三种关闭方式、亲手做一次「拍快照→玩坏→回滚」、搞懂网络模式。

## 6.1 装 Guest Additions：把「遥控器」递给虚拟机

没装增强功能的虚拟机像隔着玻璃操作：鼠标一进窗口就被「困」住、窗口拉大分辨率不变、剪贴板不互通。Guest Additions 是 VirtualBox 附送、但要装进客户机**内部**的驱动工具包，专治这些毛病。[^c6-1]

安装步骤：

1. 启动第 5 章建好的 Ubuntu 虚拟机，登录桌面。
2. 在 VM 窗口菜单栏点 **Devices → Insert Guest Additions CD image…**。VirtualBox 会把自带的驱动镜像像「塞光盘」一样挂载进虚拟机。[截图：Devices 菜单的 Insert Guest Additions CD image]
3. 回到客户机：一般会自动弹出安装提示，Ubuntu 要你输密码授权，一路确认；没弹窗就手动打开挂载的光盘（形如 `VBOXADDITIONS_…`）运行安装程序。
4. 装完按提示**重启虚拟机**。

重启后改善明显：第二个鼠标指针消失，鼠标能自由滑出窗口；窗口拉多大分辨率自动跟着变；剪贴板、拖放、共享文件夹等宿主 ↔ 客户机互传功能也解锁（都以 Guest Additions 为前提，且前两者默认关闭，可在 Devices 菜单打开）。[^c6-1]

> [!tip] 大白话：Guest Additions 是什么？
> 把虚拟机想成刚搬来的邻居，Guest Additions 就是你去送的那把「万能遥控器」。之前调他家电视（分辨率）、给他送东西（剪贴板/文件）都得敲门喊话；有了遥控器，两边直接互通。所以装完系统第一件事就是装它。

## 6.2 三种关闭方式：先别急着点那个 ×

点 VM 窗口右上角的关闭按钮，VirtualBox 不会直接关掉虚拟机，而是弹窗问你想怎么处理（也可按 Host key + Q）。三个选项区别很大：[^c6-2]

| 选项 | 行为 | 何时用 |
| --- | --- | --- |
| **Save State**（保存状态） | 整机「冻结」并把完整状态写入宿主磁盘；下次启动原地续跑，打开的程序和窗口都还在 | 临时走开、想留现场又不占内存，类似笔记本「合盖休眠」 |
| **Shut Down**（关机） | 发 ACPI 关机信号，等同按真实电脑电源键，触发客户机正常关机流程；不保存状态 | 日常真正用完收尾——最接近物理机关机 |
| **Power Off**（断电） | 立刻停止虚拟机，不关机、不保存状态 | 正常情况别用；唯一例外是下节快照回滚场景 |

两句红线：**Save State 不是关机**——只是把状态「冻住存盘」，客户机没走关机流程，下次启动直接回到刚才的桌面，但此时不能改那些要求机器关闭的设置。**Power Off 等于拔电源**，没有关机保护，可能损坏系统盘或触发长时间自检。[^c6-2]

> [!tip] 大白话：Save State、关机、断电差在哪？
> 把没做完的工作想成一桌菜：Save State 是连火候拍照存档、关火走人，回来原样接着炒；Shut Down 是正常关火收拾，下次重来；Power Off 是一脚踹翻灶台——菜没了还可能砸锅。

## 6.3 快照实操：拍一张「后悔药」，然后真的吃一次

第 4 章说过快照是时光机，这里动手验证：拍快照 → 危险操作 → 回滚。

1. **拍快照**：让虚拟机处于「干净可用」状态（如刚装完系统）。点菜单 **Machine → Take Snapshot…**，起名如「刚装好，干净」，点 OK；拍摄瞬间会暂停一两秒。[^c6-3][截图：Take Snapshot 对话框]
2. **做危险操作**：故意在客户机里折腾——删几个文件、乱改系统设置或装个可疑软件，制造「后悔了」的场景。
3. **回滚**，两种走法殊途同归：
   - 走法 A：正常关掉虚拟机，在管理器选中该 VM → 点右侧 **Snapshots** → 选中刚才的快照 → 点工具栏 **Restore** → 确认后重启。[截图：Snapshots 列表点 Restore]
   - 走法 B：虚拟机还在运行就直接关窗口选 **Power Off**。只要这台 VM 有快照，Power Off 就会丢弃自最近快照以来的改动、回到快照状态——这正是 6.2 里 Power Off 那个「唯一例外」的正确用法。[^c6-2][^c6-3]

回滚后，删掉的文件回来了、改坏的设置复原，与拍快照那一刻分毫不差——但快照之后的新改动会**永久丢失**，有不想丢的东西就先再拍一张。不需要的快照选中点 **Delete** 即可，不影响当前状态，只释放磁盘空间。[^c6-3]

## 6.4 网络：默认 NAT 够用，什么时候换模式

新建虚拟机时，VirtualBox 默认启用一张虚拟网卡并设为 **NAT** 模式。对多数人这已足够：客户机想上网浏览、下载、收邮件，无需任何设置。[^c6-4][^c6-5]

> [!tip] 大白话：NAT 是什么？
> 把宿主机想成小区门卫。虚拟机出门上网都走门卫这道，外面看到的只是门卫的地址。好处是安全省事、不用管 IP；坏处是外人想主动进楼找你（访问虚拟机里的服务），门卫默认不放行，除非你专门开一条「访客通道」（端口转发）。

那什么时候改模式？要诀一句话：**只上网用 NAT；给局域网/外网提供服务改 Bridged；只要宿主↔虚拟机互通选 Host-only；只想让几台虚拟机自己互通选 Internal。** 改网络先关机——设置窗口在虚拟机运行或保存（Saved）状态时是禁用的。[^c6-4] 步骤：

1. 用 Shut Down 正常关闭虚拟机。
2. 在管理器选中该 VM，点 **Settings → Network**。
3. 把 Adapter 1 的 **Attached to** 从 NAT 改成目标模式，点 OK。
4. 重启虚拟机生效。[截图：Network 设置页的 Attached to 下拉框]

四种模式（外加 NAT 家族的 NAT Network）怎么记，看速记表：[^c6-5]

| 模式 | 通信范围 | 能否上网 | 用途 |
| --- | --- | --- | --- |
| **NAT**（默认） | 虚拟机单向发起出网；外部/宿主默认连不进虚拟机 | 能（借宿主网络） | 虚拟机只当「上网客户端」，零配置 |
| **NAT Network** | 同一 NAT 网络的多台虚拟机可互访，且都能出外网 | 能（经宿主） | 多台虚拟机既要互访又要一起上网的实验环境 |
| **Bridged**（桥接） | 虚拟机直接挂到宿主所在局域网，相当于局域网内一台独立主机，双向可达 | 能（用局域网真实 IP） | 在虚拟机里跑服务、给局域网/外部设备访问 |
| **Host-only**（仅主机） | 仅宿主机 ↔ 虚拟机及同网虚拟机之间 | 否（默认不通外网） | 只要宿主和虚拟机私密互通，不需要外网 |
| **Internal**（内部网络） | 仅选中的虚拟机之间；宿主和外部都看不见 | 否 | 纯虚拟机之间的私密通信演练 |

> NAT 默认形态下外部连不进虚拟机内的服务；想让宿主机或外网访问 VM 内某端口（如 Web 服务）需配置 **NAT 端口转发（port forwarding）**——进阶操作，本章不展开。

## 本章小结

- Guest Additions 装进客户机内部：消除第二鼠标指针、窗口自适应、解锁剪贴板/拖放/共享文件夹，装完重启。[02][03]
- Save State = 冻结续跑（不是关机）；Shut Down = ACPI 正常关机（首选）；Power Off = 拔电源，仅在要回滚快照时用。[02]
- 快照「拍→玩坏→回滚」：Restore 丢快照后的改动；Delete 只释放磁盘；有快照时 Power Off 会回到快照状态。[02]
- 默认 NAT 上网零配置；对外服务换 Bridged；Host-only 仅宿主↔VM；Internal 仅 VM 间；改网络先关机。[02][04]

下一章换到另一款主流桌面虚拟化软件 VMware Workstation，用同一套思路给 Windows 11 建虚拟机——顺便看看它和 VirtualBox 的关键差异。

## 参考来源

[^c6-1]: Oracle VirtualBox User Manual：Guest Additions 定义「随软件附送但需装进客户机内部」（`sources/03_docs_oracle_com.md`）；消除第二鼠标指针、窗口自适应分辨率、共享文件夹需 Guest Additions、剪贴板/拖放默认关闭（`sources/02_docs_oracle_com.md`）。
[^c6-2]: Oracle VirtualBox 7.2 User Guide《Closing or Saving a VM》：Save State / Shut Down / Power Off 行为，及「有快照时 Power Off 可快速回到快照」的例外（`sources/02_docs_oracle_com.md`）。
[^c6-3]: Oracle VirtualBox 7.2 User Guide《Snapshots》：Take Snapshot（Machine 菜单）、Restore 整机回滚且快照后改动丢失、Delete 只释放磁盘（`sources/02_docs_oracle_com.md`）。
[^c6-4]: Oracle VirtualBox 7.2 User Guide：新建 VM 默认启用一张网卡并选 NAT；Settings 窗口在 VM 运行或 Saved 状态禁用（`sources/02_docs_oracle_com.md`）。
[^c6-5]: Oracle VirtualBox 6.0 User Guide《Introduction to Networking Modes》：NAT / NAT Network / Bridged / Internal / Host-only 各模式正文定义（`sources/04_docs_oracle_com.md`）。
