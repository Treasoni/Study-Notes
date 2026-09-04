---
url: "https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0/creating-virtual-machines-in-workstation-player-help-win/install-windows-11-on-a-virtual-machine-in-workstation-win.html"
title: "在 Workstation 中的虚拟机上安装 Windows 11"
scraped_at: 2026-09-04T15:57:07+00:00
---

VMware Workstation Pro 17.0
切换版本
17.0 
English  日本語  简体中文 
  * [使用 VMware Workstation Pro](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-pro.html)
  * [使用适用于 Windows 的 VMware Workstation Player](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0.html)
    *     * [安装和使用 适用于 Windows 的 VMware Workstation Player](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0/installing-and-using-workstation-player-win.html)
    * [更改 适用于 Windows 的 VMware Workstation Player 首选项设置](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0/changing-workstation-player-preference-settings-win.html)
    * [在 适用于 Windows 的 VMware Workstation Player 中创建虚拟机](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0/creating-virtual-machines-in-workstation-player-help-win.html)
      *       *       *       *       *       * [在 Workstation 中的虚拟机上安装 Windows 11](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0/creating-virtual-machines-in-workstation-player-help-win/install-windows-11-on-a-virtual-machine-in-workstation-win.html)
      *     * [在启用了 Hyper-V 的主机上运行 Workstation](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0/running-workstation-on-a-hyper-v-enabled-host-win.html)
    *     * [在 适用于 Windows 的 VMware Workstation Player 中启动和停止虚拟机](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0/starting-and-stopping-virtual-machines-win.html)
    *     *     *     *     *     *     *     *     * [使用 vctl 命令管理容器和运行 Kubernetes 集群](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0/using-vctl-command-to-manage-containers-and-run-kubernetes-cluster-win.html)
    *     * [使用 VMware 适用于 Windows 的 VMware Workstation Player REST API](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0/using-vmware-workstation-player-rest-api-win.html)
  * [使用适用于 Linux 的 VMware Workstation Player](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-linux-17-0.html)
  * [Documentation Legal Notice](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/documentation-legal-notice-english-public.html)


# 在 Workstation 中的虚拟机上安装 Windows 11
在虚拟机上安装 Windows 11 与在物理计算机中安装 Windows 11 十分相似。创建以 Windows 11 作为客户机操作系统的虚拟机时，
Workstation Pro
Workstation Player
会将 vTPM（虚拟可信平台模块）添加到虚拟机。 
[ 下载 PDF ](https://techdocs.broadcom.com/content/dam/broadcom/techdocs/us/zh_cn/pdf/vmware/desktop-hypervisors/workstation/vmware-workstation-pro-17-0.pdf)
# 
在 Workstation 中的虚拟机上安装 Windows 11
在虚拟机上安装 Windows 11 与在物理计算机中安装 Windows 11 十分相似。创建以 Windows 11 作为客户机操作系统的虚拟机时，
Workstation Pro
Workstation Player
会将 vTPM（虚拟可信平台模块）添加到虚拟机。 
  * 确认您具有
“新建虚拟机”
向导创建虚拟机所需的信息。
  * 有关您打算安装的客户机操作系统的信息，请参见
《VMware 客户机操作系统安装指南》
。 
  * 如果从安装程序光盘中安装客户机操作系统，请将安装程序光盘插入主机系统的 CD-ROM 驱动器中。 
  * 如果要通过 ISO 映像文件安装客户机操作系统，请确认该 ISO 映像文件位于主机系统可访问的目录中。 
  * 如果虚拟机将会使用主机系统中的物理磁盘或未使用的分区，请执行适当的准备任务。


您可以通过运行
新建虚拟机
向导在本地主机系统中创建新虚拟机。 
在完成 Windows 11 操作系统的安装后，我们建议您不要为了使用 Windows 11 时的无缝体验而从虚拟机中移除加密或 vTPM 设备。
Workstation 不支持在远程虚拟机上创建 Windows 11 客户机操作系统。
  1. 启动
“新建虚拟机”
向导。   
| Windows 主机  | 选择。   |  
| --- | --- |  
| Linux 主机  |  选择。  |  
  2. 选择配置类型，然后单击
下一步
。   
| 向导将提示您指定或接受基本虚拟机设置的默认设置。典型配置类型适用于大多数情况。  |  
| --- |  
| 自定义模式  | 您必须选择自定义配置类型以执行以下操作：创建与默认硬件兼容性设置不同的虚拟机版本，指定 SCSI 适配器的 I/O 适配器类型，指定是创建 IDE、SCSI、SATA 还是 NVMe 虚拟磁盘，使用物理磁盘而不是虚拟磁盘，使用现有的虚拟磁盘，或者分配所有虚拟磁盘空间而不是允许磁盘空间逐渐增大到最大磁盘容量。  |  
  3. 如果选择
自定义
选项，则需要选择硬件兼容性设置。 
硬件兼容性设置决定了虚拟机的硬件功能。 
  4. 选择客户机操作系统的来源。   
| 安装程序光盘  | 选择插入了安装光盘的物理驱动器。  |  
| --- | --- |  
| 安装程序光盘映像文件 (ISO)  | 请键入或浏览到客户机操作系统 ISO 映像文件所在的位置。  |  
| 稍后再安装客户机操作系统  | 创建一个具有空白磁盘的虚拟机。您必须在完成虚拟机的创建后手动安装客户机操作系统。  |  
  5. 选择 
Windows 11 x64
作为客户机操作系统，然后单击
下一步
。
  6. 键入虚拟机名称，指定虚拟机文件目录位置，然后单击
下一步
。 
  7. 选择加密类型，输入加密密码，然后单击
下一步
。
您可以选择加密所有文件，或者仅加密支持 vTPM 设备所需的最小文件数。
您可以指定选择的密码，也可以选择选项来自动生成一个密码。要将密码复制到剪贴板，请单击。您还可以选择记住加密密码的选项。对于 Windows 主机操作系统，Microsoft 凭据管理器会存储密码。对于 Linux 主机操作系统，GNOME libsecret 库会存储密码。
  8. 按照提示配置虚拟机。 
如果您选择典型配置，向导会提示您配置虚拟磁盘的大小并指定是否将磁盘拆分为多个文件。如果您选择自定义配置，向导会提示您配置固件类型、虚拟机处理器、内存分配、网络连接配置、I/O 控制器类型、虚拟磁盘类型和模式以及虚拟磁盘。 
对于固件类型，如果选择 UEFI 并且客户机操作系统支持 UEFI 安全引导，您可以选择相应的选项以启用 UEFI 安全引导。 
  9. 单击
自定义硬件
以自定义硬件配置。 
也可以在创建完虚拟机后修改虚拟硬件设置。 
  10. 选择
创建后开启此虚拟机
以在创建完后立即开启虚拟机。 
如果手动安装客户机操作系统，则该选项不可用。 
  11. 单击以创建虚拟机。 


虚拟机将出现在库中。 
Workstation Pro
Workstation Player
会创建新虚拟机，并且用户可以按照安装说明安装操作系统。
[在 适用于 Windows 的 VMware Workstation Player 中创建虚拟机](https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0/creating-virtual-machines-in-workstation-player-help-win.html "您可以使用新建虚拟机向导创建虚拟机。新建虚拟机向导可引导您设置新的虚拟机，帮助您设置相应选项和参数。  ")
本页对您有帮助吗？
上次更新时间 July 15, 2025
Other Product Support Resources 
Support
[Support Portal](https://support.broadcom.com) [Product Communities](https://community.broadcom.com) [Knowledge Base](https://www.broadcom.com/support/knowledgebase)
Learning
[Brocade Education](https://www.broadcom.com/support/education/brocade) [Mainframe Software Education](https://www.broadcom.com/support/education/mainframe/education-program) [Software Education](https://www.broadcom.com/support/education/software) [VMware Learning](https://www.broadcom.com/support/education/vmware)
Need more help?
[Virtual Agent](https://support.broadcom.com) [Advanced Support](https://www.broadcom.com/support/services-support/ca-support/support-programs) [Contact Us](https://support.broadcom.com/web/ecx/contact-support)
本页对您有帮助吗？
上次更新时间 July 15, 2025
