---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil"
title: "fsutil | Microsoft Learn"
scraped_at: 2026-09-10T15:41:37+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# fsutil
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


> 适用于：Windows Server 2022、Windows Server 2019、Windows Server 2016、Windows 10、Windows 2012 R2、Windows 8.1、Windows 2012、Windows 8、Windows 2008 R2、Windows 7
执行与 FAT 和 NTFS 文件系统相关的任务，例如管理重分析点、处理稀疏文件或卸载卷。 在没有参数的情况下使用时，`fsutil` 显示支持的子命令的列表。
> 你必须以管理员或管理员组的成员身份登录才能使用 `fsutil`。 只有对 Windows作系统有全面了解的高级用户才能使用此强大的命令。
## Parameters  
| Subcommand  | Description  |  
| --- | --- |  
|  [fsutil 8dot3name](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-8dot3name)  | 查询或更改系统上短名称行为的设置，例如，生成长度为 8.3 个字符的文件名。 删除目录中所有文件的短名称。 扫描目录，并识别如果从目录中的文件中删除短名称可能会受到影响的注册表项。  |  
| 为通用日志文件系统（CLFS）日志文件创建或更正身份验证代码。  |  
|  [fsutil devdrv](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-devdrv)  | 管理开发人员驱动器，这是一个针对开发人员方案性能进行调整的卷。 开发人员驱动器还允许设备管理员控制附加到卷的文件系统微筛选器。  |  
| 查询是否设置了卷的脏位，或者设置卷的脏位。 设置卷的脏位后， **autochk** 会在下次重新启动计算机时自动检查卷是否存在错误。  |  
| 按用户名查找文件（如果启用了磁盘配额）、查询文件的分配范围、设置文件的短名称、设置文件的有效数据长度、为文件设置零数据、创建指定大小的新文件、查找文件 ID（如果给定了名称），或者查找指定文件 ID 的文件链接名称。  |  
|  [fsutil fsinfo](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-fsinfo)  | 列出所有驱动器并查询驱动器类型、卷信息、特定于 NTFS 的卷信息或文件系统统计信息。  |  
|  [fsutil hardlink](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-hardlink)  | 列出文件的硬链接，或创建硬链接（文件的目录条目）。 每个文件可视为至少有一个硬链接。 在 NTFS 卷上，每个文件都可以有多个硬链接，因此单个文件可以出现在多个目录中（甚至可以出现在同一目录中，但名称不同）。 由于所有链接都引用同一文件，因此程序可以打开任何链接并修改文件。 只有在删除了指向某一文件的所有链接之后，才会从文件系统中删除该文件。 创建硬链接后，程序可以像使用任何其他文件名一样使用硬链接。  |  
|  [fsutil objectid](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-objectid)  | 管理对象标识符，Windows 操作系统使用这些标识符来跟踪文件和目录等对象。  |  
| 管理 NTFS 卷上的磁盘配额，以便更精确地控制基于网络的存储。 磁盘配额按卷实现，并按用户实现硬存储和软存储限制。  |  
|  [fsutil repair](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-repair)  | 查询或设置卷的自我修复状态。 自我修复 NTFS 尝试联机更正 NTFS 文件系统的损坏，而无需运行 `chkdsk.exe`。 包括启动磁盘验证和等待修复完成。  |  
|  [fsutil reparsepoint](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-reparsepoint)  | 查询或删除重分析点（具有包含用户控制数据的可定义属性的 NTFS 文件系统对象）。 重分析点用于扩展输入/输出 (I/O) 子系统中的功能。 它们用于目录交接点和卷装入点。 文件系统筛选器驱动程序也使用这些驱动程序将某些文件标记为该驱动程序的特殊文件。  |  
|  [fsutil resource](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-resource)  | 创建辅助事务资源管理器，启动或停止事务资源管理器，显示有关事务资源管理器的信息，或修改其行为。  |  
|  [fsutil sparse](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-sparse)  | 管理稀疏文件。 稀疏文件是其中包含一个或多个未分配数据区域的文件。 程序将这些未分配的区域视为包含值为零的字节，但没有使用磁盘空间来表示这些零。 分配所有有意义的或非零数据，而不分配所有非有意义的数据（由零组成的大型数据字符串）。 读取稀疏文件时，已分配的数据按存储方式返回，未分配的数据作为零返回（默认情况，遵循 C2 安全需求规范）。 稀疏文件支持允许从文件中的任何位置释放数据。  |  
|  [fsutil tiering](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-tiering)  | 启用存储层功能管理，例如设置和禁用标志和层列表。  |  
|  [fsutil transaction](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-transaction)  | 提交指定的事务、回滚指定的事务或显示有关该事务的信息。  |  
| 管理更新序列号 (USN) 更改日志，该日志提供对卷上的文件所做的所有更改的永久日志。  |  
|  [fsutil volume](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-volume)  | 管理卷。 卸载卷、查询以查看磁盘上有多少可用空间，或查找使用指定群集的文件。  |  
| 提供发现和管理 WIM 支持的文件的功能。  |  
## Related links


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-03-05 


