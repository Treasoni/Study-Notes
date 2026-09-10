---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/diskpart"
title: "diskpart | Microsoft Learn"
scraped_at: 2026-09-10T15:41:37+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/diskpart) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/diskpart)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# diskpart
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


> 适用于：Windows Server 2022、Windows 10、Windows 8.1、Windows 8、Windows 7、Windows Server 2019、Windows Server 2016、Windows Server 2012 R2、Windows Server 2012 和 Windows Server 2008 R2、Windows Server 2008
diskpart 命令解释器可帮助你管理计算机的驱动器（磁盘、分区、卷或虚拟硬盘）。
在使用 **diskpart** 命令之前，必须先列出一个对象，然后选择一个对象以使其处于焦点状态。 对象具有焦点后，键入的任何 diskpart 命令都将对该对象执行作。
## Determine focus
选择对象时，焦点将保留在该对象上，直到选择其他对象。 例如，如果在磁盘 0 上设置了焦点，并且选择磁盘 2 上的卷 8，则焦点将从磁盘 0 转移到磁盘 2，卷 8。
某些命令会自动更改焦点。 例如，创建新分区时，焦点会自动切换到新分区。
只能将焦点放在所选磁盘上的分区上。 分区具有焦点后，相关卷（如果有）也具有焦点。 卷具有焦点后，如果卷映射到单个特定分区，则相关磁盘和分区也具有焦点。 如果情况并非如此，则焦点位于磁盘和分区上会丢失。
## Syntax
若要启动 diskpart 命令解释器，请在命令提示符处键入：

```
diskpart <parameter>

```

Important
您必须在本地 **管理员** 组或具有类似权限的组中才能运行 diskpart。
### Parameters
可以从 Diskpart 命令解释器运行以下命令：  
| Command  | Description  |  
| --- | --- |  
| 将磁盘的分区标记为活动状态。  |  
| 将具有焦点的简单卷镜像到指定的磁盘。  |  
| 给选中的卷分配一个驱动器号或装入点。  |  
| 附加（有时称为装载或显露 (surface)）虚拟硬盘 (VHD)，使其在主机计算机上显示为本地硬盘驱动器。  |  
| 显示、设置或清除磁盘或卷的属性。  |  
| 启用或禁用自动装载功能。  |  
| 将具有焦点的镜像卷拆分为两个简单的卷。  |  
| 从具有焦点的磁盘中删除任何分区或卷格式。  |  
|  [compact vdisk](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/compact-vdisk)  | 减小动态扩展虚拟硬盘 (VHD) 文件的物理大小。  |  
| 将文件分配表（FAT）和 FAT32 卷转换为 NTFS 文件系统，使现有文件和目录保持不变。  |  
| 在磁盘、一个或多个磁盘上的卷或虚拟硬盘（VHD）上创建分区。  |  
| 删除分区或卷。  |  
| 阻止所选虚拟硬盘 (VHD) 在主计算机上显示为本地硬盘驱动器。  |  
| 显示有关所选磁盘、分区、卷或虚拟硬盘（VHD）的信息。  |  
| 退出 diskpart 命令解释器。  |  
| 将虚拟硬盘（VHD）扩展到指定的大小。  |  
| 将具有焦点的卷或分区及其文件系统扩展到磁盘上的可用（未分配）空间。  |  
| 显示有关具有焦点的卷的当前文件系统的信息，并列出支持格式化卷的文件系统。  |  
| 格式化磁盘以接受文件。  |  
| 将 gpt 属性（s）分配给分区，并将焦点集中在基本 GUID 分区表 （gpt） 磁盘上。  |  
| 显示可用命令的列表或有关指定命令的详细帮助信息。  |  
| 将外部磁盘组导入到本地计算机的磁盘组中。  |  
| 将具有焦点的系统分区或启动分区标记为基本主启动记录（MBR）磁盘上处于非活动状态。  |  
| 显示磁盘中的磁盘、磁盘中的分区、磁盘中的卷或虚拟硬盘（VHD）的列表。  |  
| 将差异虚拟硬盘 (VHD) 与其对应的父 VHD 合并。  |  
| 将联机磁盘或卷设置为脱机状态。  |  
| 使脱机磁盘或卷处于联机状态。  |  
| 刷新磁盘组中所有磁盘的状态，尝试恢复无效磁盘组中的磁盘，并重新同步具有过时数据的镜像卷和 RAID-5 卷。  |  
| 提供向脚本添加注释的方法。  |  
| 从卷中删除驱动器号或装入点。  |  
| 通过用指定的动态磁盘替换失效的磁盘区域来修复选中的 RAID-5 卷。  |  
| 找到可能已添加到计算机的新磁盘。  |  
| 准备要用作启动卷或系统卷的现有动态简单卷。  |  
| 显示或设置操作系统的存储区域网络 (san) 策略。  |  
| 将焦点转移到磁盘、分区、卷或虚拟硬盘（VHD）。  |  
| 更改具有焦点的分区的“分区类型”字段。  |  
| 按指定的量减小所选卷的大小。  |  
| 显示或设置具有焦点的磁盘的 GUID 分区表（GPT）标识符或主启动记录（MBR）签名。  |  
## 列出可用对象
可以通过运行主命令后跟该特定命令可用的选项来查看与每个命令关联的选项列表。 运行 **列表** 本身将显示以下四个参数：
Note
运行 **列表** 命令后，焦点对象旁边会出现一个星号 （***** ）。
### Examples
若要查看可用磁盘，请运行 **列表磁盘** ：

```
list disk

```

若要选择磁盘，请运行 **select disk** ，然后运行磁盘号。 For example:

```
select disk 1

```

在使用磁盘 1 之前，需要通过运行 **创建分区主数据库来创建分区** ：

```
create partition primary

```

最后，通过运行 **格式 fs=ntfs label=Backup=Backup quick** ，我们可以使用标签“Backup”执行磁盘 1 到 NTFS 的快速格式，如下所示：

```
format fs=ntfs label=Backup quick

```

## Related links
  *   *   * [Windows PowerShell 中的存储 Cmdlet](https://learn.microsoft.com/zh-cn/powershell/module/storage/)


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-08-16 


