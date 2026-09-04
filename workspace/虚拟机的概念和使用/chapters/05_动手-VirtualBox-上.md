# 动手 · VirtualBox（上）：安装、建机、装第一个系统

前四章我们把「虚拟机是什么、磁盘文件、快照」这些概念地图铺好了。这一章开始真正动手：用开源的 VirtualBox 从零建一台虚拟机，装一个 Ubuntu Linux 系统。看完概念却不会建机，等于没学；而建机这第一步里藏着两个新手最容易踩的坑——内存给太多会卡死宿主机、ISO 得自己准备。我们把这两件事一次讲透。

## 5.1 动手前准备：三样东西缺一不可

建机前先备好三样：VirtualBox 软件本身、一份 Ubuntu 系统镜像（ISO 文件）、一台支持硬件虚拟化的电脑。

1. **下载并安装 VirtualBox**
   1. 打开 VirtualBox 官网的 Downloads（下载）页面，选对应你电脑系统的安装包（Windows 用户选 `Windows hosts`）。
   2. 双击安装包，一路 Next / Install。若 Windows 弹出「是否安装此设备软件」的询问，选择安装——VirtualBox 需要装一些驱动程序才能工作。
   3. 完成后打开 VirtualBox Manager（VirtualBox 管理器主界面），你会看到左侧空的「Machines 列表」和上方一排按钮。[截图：VirtualBox 官网下载页] [截图：安装完成后的 VirtualBox Manager 主界面]

2. **备一份 Ubuntu 的 ISO 镜像**
   到 Ubuntu 官网的 Download 页面下载桌面版（Desktop），建议选 LTS（长期支持版），得到一个 `.iso` 文件，记下它存放的路径。[截图：Ubuntu 官网下载页，注意选 LTS]
   VirtualBox 只提供「造电脑」的软件，**不附带任何操作系统，也不提供使用系统所需的许可**——系统镜像必须你自己去各系统官方渠道获取。[^c5-1]

> [!tip] 大白话：ISO 是什么？
> 把 ISO 想成一张「虚拟安装光盘」。真实的系统装机会用光盘/U盘引导，VirtualBox 没有光驱，就直接把这个 `.iso` 文件当成光盘塞给虚拟机。所以你下载的是「一张光盘的完整映像」，不是要双击安装的程序。

3. **检查 VT-x / AMD-V（硬件虚拟化开关）**
   Ubuntu 是 64 位系统，跑得动它需要 CPU 的硬件虚拟化扩展帮忙加速：Intel 的扩展叫 VT-x，AMD 的叫 AMD-V（主板上常写作 SVM Mode）。今天的服务器默认都有，但台式机可能要在 BIOS 里手动打开。[^c5-4]
   在 Windows 上快速看一眼：按 `Ctrl+Shift+Esc` 打开任务管理器 → 性能 → CPU，看右下角「虚拟化」是否为「已启用」。如果是「已禁用」，需要重启电脑，开机时按 `Del`/`F2`（不同主板按键不同）进 BIOS，找到 `Intel Virtualization Technology` 或 `SVM Mode` 设为 Enabled，保存重启。找不到开关也别急，第 9 章会专门讲这个坑怎么排。

## 5.2 New 向导：给这台「电脑」命名、选位置、挂 ISO

在 VirtualBox Manager 主界面点「新建」（New），弹出 New Virtual Machine（新建虚拟机）向导。如果没看到向导而是一整页表单，是「体验级别」被设成了 Expert（专家）模式，切回 Basic（基本）模式即可。[^c5-1]

向导通常有四步，跟着做：

1. **名称和操作系统（Name and Operating System）**
   - **Name（名称）**：给虚拟机起个能看懂的名字，比如 `Ubuntu-学习用`。这个名字既是列表里显示的名字，也会用作磁盘文件的文件名；VirtualBox 还会根据名字自动猜操作系统。[^c5-1]
   - **VM Folder（文件夹）**：虚拟机文件存放的位置。默认在你的用户目录下，建议放到**空间充足**的磁盘分区——尤其你后面要用快照功能时，这个文件夹会越长越大。[^c5-1]
   - **ISO Image（镜像）**：点下拉框，选 5.1 下载好的 Ubuntu ISO。选完后 VirtualBox 一般能自动识别出操作系统类型和版本（Ubuntu 64-bit）。[截图：New 向导的名称/操作系统页]
2. **无人值守，还是手动装？（关键选择）**
   向导里默认勾着「使用无人值守安装」（Install OS Using Unattended Installation）之类的一项。两个方向二选一：
   - **自动（默认）**：勾着它，向导会让你填一个**用户名和密码**，作为系统里的日常账号；官方手册说明，在 Linux 客户机上还会用同一密码创建 root 账号。[^c5-1] 之后 VirtualBox 会替你走完整个安装流程，装完直接进桌面。适合想省事的新手。
   - **手动**：取消勾选。VirtualBox 只把 ISO「塞进虚拟光驱」，剩下点「安装 Ubuntu」、选分区、设账号全由你自己点，更接近真实装机的体验。[截图：无人值守配置页，用户名/密码输入框]
   > 顺带记住：无论自动还是手动，你在系统里建的都是**这台虚拟机的管理员账号**，只管得到虚拟机内部，碰不到宿主机。

3. **虚拟硬件（Virtual Hardware）**：这一步分配内存和 CPU，铁律见 5.3。
4. **虚拟硬盘（Virtual Hard Disk）**：设一个磁盘大小上限（Ubuntu 日常用建议 25–50 GB），保持默认的**动态分配（dynamically allocated）**即可。动态分配意味着这个上限先不真占满，虚拟机实际用多少，磁盘文件才长多少。[^c5-1]

## 5.3 资源分配铁律：内存是借来的

向导会让你填 Base Memory（内存）和 Processors（处理器）。记住两条官方铁律：[^c5-1]

1. **内存是「借」的，不是「分」的。** 你填给虚拟机的内存，在虚拟机运行期间会从宿主机里划走，宿主机自己就少这么多内存可用。VirtualBox 官方特别警告：如果宿主剩余内存不足，系统会拼命把内存换到硬盘（swap），**可能把宿主机拖到近乎死机的程度**。这就是「内存给太多反而卡死真电脑」的真相。[^c5-1]
2. **给多少合适？** 听向导的默认建议值最稳（Ubuntu 一般建议 2048 MB），同时保证给宿主留足余量。举例：宿主机 8 GB 内存，给虚拟机 4 GB，那虚拟机开着时宿主机只剩 4 GB 给其他所有软件。**同时开的虚拟机越多，加起来越要克制。** 处理器同理：官方建议**不要超过宿主机总线程数的一半**。[^c5-1]

> [!tip] 大白话：内存是借来的
> 把宿主内存想成一张工资卡，虚拟机是向你借钱的室友。他借 4000 你只剩 4000，月底他还不上了你还得替他倒贴（系统开始用硬盘硬撑 swap），结果你俩一起卡死。所以别当老好人——按建议值借，给自己留够生活费。

## 5.4 首次启动与 Host key：鼠标「卡」在窗口里了怎么办

向导完成后，虚拟机出现在左侧列表里。选中它，点顶部绿色的「启动」（Start）。[^c5-2]

- 选了**无人值守**：首次启动会自动用之前选好的 ISO 开始安装，全程基本不用管，跟着屏幕提示即可。[^c5-2]
- 选了**手动**：虚拟机会像一台光驱里放着安装盘的真电脑那样启动，你按屏幕提示自己装 Ubuntu。[截图：首次启动、Ubuntu 安装画面]

装的过程里你可能遇到第一个「惊吓」：**鼠标点进虚拟机窗口后「出不来了」，键盘打字也都进了虚拟机。** 这不是坏了，而是虚拟机还没装 Guest Additions（增强功能）时，键盘和鼠标同一时刻只能归一方所有——归了虚拟机，宿主机就抢不回来。[^c5-2]

解决办法是记住一个键：**Host key（宿主键）**。默认是键盘右侧的 `Ctrl`（右 Ctrl），按一下，键盘鼠标的控制权就交还给宿主机。当前 Host key 是什么，永远显示在虚拟机窗口**右下角的状态栏**上，随时可查。[^c5-2]

- 想在虚拟机里按 `Ctrl+Alt+Del`？用 `Host key + Del` 代替。[^c5-2]
- 看到「第二个鼠标指针」？也是正常的——没装 Guest Additions 前的典型现象，第 6 章装完增强功能就消失了。[^c5-2][^c5-3]

等 Ubuntu 装完自动重启进入桌面，你就在 VirtualBox 里拥有了一台真正跑起来的 Linux 电脑。

## 选学：用 VBoxManage 命令行建机（入门可跳过）

向导点按钮的每一步，其实都对应一条命令。想对「建机到底做了什么」有感觉的读者可以看看，完全不想碰命令行的可以直接跳过，不影响后续章节。

```bash
# 创建一台名为 Ubuntu-CLI 的 64 位 Ubuntu 空虚拟机并注册
VBoxManage createvm --name "Ubuntu-CLI" --ostype "Ubuntu_64" --register
# 分配 2048MB 内存、2 个虚拟 CPU
VBoxManage modifyvm "Ubuntu-CLI" --memory 2048 --cpus 2
# 建一块 30GB（30720MB）的动态虚拟硬盘
VBoxManage createhd --filename "Ubuntu-CLI.vdi" --size 30720
```

命令执行后，VirtualBox 会生成一个 XML 配置文件来记录这台虚拟机的硬件参数——这正是第 3 章说的「虚拟机 = 一组参数 + 状态」在文件层面的体现。[^c5-1][^c5-3]

## 本章小结

- 建机前备三样：VirtualBox、Ubuntu ISO、开启 VT-x/AMD-V 的电脑；VirtualBox 不提供操作系统和许可，系统镜像要自己下载。[^c5-1]
- New 向导四步：命名（同时是文件名）、选存放文件夹（快照会占空间）、挂 ISO、选无人值守或手动安装。[^c5-1]
- 无人值守会替你建一个管理员账号并自动装完（Linux 下还用同密码建 root）；手动装则取消勾选、自己点安装器。[^c5-1]
- 资源铁律：内存是「借」的，给太多会把宿主机拖到近死机；按向导建议并给宿主留余量，CPU 不超过宿主线程数一半。[^c5-1]
- 首次启动后鼠标键盘「被抢」是正常现象，按 Host key（默认右 Ctrl）交还；`Host key + Del` = 虚拟机内 `Ctrl+Alt+Del`。[^c5-2]

机器已经跑起来了，但这只是开始：窗口里的鼠标还是双份的、分辨率不跟手、想和宿主机互传文件也还没戏。下一章装 Guest Additions（增强功能），再学三种关机方式、打第一个快照，把网络从 NAT 讲到桥接——一台「好用」的虚拟机才算完工。

## 参考来源

[^c5-1]: Oracle VirtualBox 7.2 用户手册《Creating a New Virtual Machine》：New 向导步骤、VM 名称/文件夹、ISO 自备与许可声明、无人值守建管理员账号、内存借用的 Caution 原文、CPU 不超过宿主线程一半、磁盘默认动态分配；VBoxManage createvm/modifyvm/createhd 示例（`sources/01_docs_oracle_com.md`）。
[^c5-2]: Oracle VirtualBox 7.2 用户手册《Working with Virtual Machines》：启动方式、首次启动无人值守自动开始、安装后引导顺序变更、Host key（默认右 Ctrl）与键盘鼠标所有权、状态栏右下角显示当前 Host key、Host key + Del（`sources/02_docs_oracle_com.md`）。
[^c5-3]: Oracle VirtualBox 6.0 用户手册《Some Terminology》：Host OS/Guest OS/VM/Guest Additions 术语定义（`sources/03_docs_oracle_com.md`）。
[^c5-4]: Baeldung 中文《虚拟机与容器对比》：Intel VT / AMD-V（SVM）扩展是服务器标准功能、台式机可能需在 BIOS 启用（`sources/12_baeldung_cn.md`）。
