---
url: "https://learn.microsoft.com/zh-cn/windows-server/storage/file-server/ntfs-overview"
title: "NTFS 概述 | Microsoft Learn"
scraped_at: 2026-09-10T15:41:37+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/storage/file-server/ntfs-overview) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/storage/file-server/ntfs-overview)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# NTFS 概述
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client)


新技术文件系统（NTFS）是新式基于 Windows 的作系统（OS）的默认文件系统。 它提供高级功能，包括安全描述符、加密、磁盘配额和支持丰富的元数据，从而增强安全性和数据管理。 此外，NTFS 与群集共享卷（CSV）无缝集成，提供可供故障转移群集中的多个节点同时访问的高可用性存储。 此集成可确保持续数据可用性和复原能力。
## 提高可靠性
NTFS 通过维护基于事务的日志文件和检查点信息来提高可靠性。 如果发生系统故障，NTFS 使用此日志在下一次启动期间自动还原文件系统一致性，从而最大程度地降低数据丢失的风险。 检测到坏扇区时，NTFS 会动态将受影响的群集重新映射到正常的群集，将原始群集标记为不可用，并确保数据保留。 例如，在系统崩溃后，NTFS 可以通过重播事务日志来恢复更改，从而帮助维护数据完整性并减少停机时间。
NTFS 包括一项称为 [自我修复 NTFS](https://learn.microsoft.com/zh-cn/previous-versions/windows/it-pro/windows-server-2008-r2-and-2008/cc771388\(v=ws.10\)) 的功能，该功能可自动检测和修复后台的次要文件系统损坏，而无需使卷脱机。 这种主动方法有助于维护数据完整性，并最大程度地减少对用户和应用程序的中断。
对于更重要的文件系统损坏， `chkdsk` 该实用工具可以在保持联机状态的同时扫描和修复 NTFS 卷，最大限度地减少停机时间。 卷可能不可用的唯一时间段是在恢复数据一致性所需的阶段。 将 NTFS 与 CSV 一起使用时，无需停机即可执行修复，确保持续可用性。 若要了解详细信息，请参阅 [NTFS Health 和 Chkdsk](https://learn.microsoft.com/zh-cn/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/hh831536\(v%3dws.11\))。
## 提高安全性
  * **使用 ACL 进行精细访问控制** ：NTFS 允许使用访问控制列表（ACL）向文件和文件夹分配详细权限。 可以指定哪些用户和组有权访问，定义读取、写入或修改等访问权限类型，并定制安全性以满足组织要求。
  * **集成的 BitLocker 驱动器加密支持：NTFS 与 BitLocker 驱动器加密** 无缝配合工作，以保护卷上的敏感数据。 BitLocker 应用基于硬件的安全功能（如受信任的平台模块（TPM）），以提供设备加密，确保即使驱动器被卸载并安装到另一个系统中，也能保护数据。 这有助于防止未经授权的访问用户数据和关键系统文件。 若要了解详细信息，请参阅 [BitLocker 概述](https://learn.microsoft.com/zh-cn/windows/security/operating-system-security/data-protection/bitlocker)。


## 支持大型卷
NTFS 支持大卷，其最大大小由 Windows 版本和所选群集大小决定。 在 Windows Server 2019 及更高版本以及 Windows 10 版本 1709 及更高版本上，NTFS 卷的大小可以高达 8 PB。 早期版本的 Windows 支持高达 256 TB 的卷。 实际的最大卷和文件大小取决于簇大小和 NTFS 支持的簇总数（最多 232 - 1 个簇）。 下表汇总了每个群集大小支持的最大卷和文件大小：  
| 群集大小  | 最大的卷和文件  |  
| --- | --- |  
| 4 KB（默认大小）  | 16 TB  |  
| 8 KB  | 32 TB  |  
| 16 KB  | 64 TB  |  
| 32 KB  | 128 TB  |  
| 64 KB（早期最大值）  | 256 TB  |  
| 128 KB  | 512 TB  |  
| 256 KB  | 1 PB  |  
| 512 KB  | 2 PB  |  
| 1024 KB  | 4 PB  |  
| 2048 KB（最大大小）  | 8 PB  |  
如果尝试装载群集大小大于所使用 Windows 版本支持的最大值的卷，则会出现错误 **STATUS_UNRECOGNIZED_VOLUME** 。
Important
某些服务和应用程序可能会对文件和卷大小强制实施自己的限制。 例如，当使用依赖于卷影复制服务（VSS）快照（没有 SAN 或 RAID 机箱）的“以前版本”功能或备份应用程序时，最大支持的卷大小为 64 TB。 根据工作负荷和存储性能，您可能需要考虑使用较小的存储卷。
## 大型文件的格式要求
若要允许对大型 `.vhdx` 文件进行适当的扩展，有新的建议用于格式化卷。 当格式化用于重复数据删除的卷或托管大型文件（如 `.vhdx` 大于 1 TB 的文件）时，请使用带以下参数的 [Format-Volume](https://learn.microsoft.com/zh-cn/powershell/module/storage/format-volume) cmdlet：

```
Format-Volume -DriveLetter <DriveLetter> -FileSystem NTFS -AllocationUnitSize 65536 -UseLargeFRS

```

在此示例中， **AllocationUnitSize** 参数将分配单元大小设置为 64 KB（65,536 字节）， **UseLargeFRS** 支持大型文件记录段。
你还可以在提升的命令提示符下运行 `format` 命令，其中使用 `/L` 格式化大型文件记录段 (FRS) 卷，并使用 `/A:64k` 设置 64 KB 分配单元大小。

```
format <DriveLetter> /l /a:64k

```

## 最大文件名称和路径
NTFS 支持长文件名和扩展长度路径，并且具有以下最大值：
  * **支持长文件名，具有后向兼容性** ：NTFS 支持长文件名，在磁盘上存储 8.3 别名（采用 Unicode 编码），以提供与文件系统的兼容性。该文件系统可对文件名称和扩展施加 8.3 限制。 如果需要（出于性能方面的原因），可以在 Windows Server 2008 R2、Windows 8 和更新版本的 Windows OS 中有选择地禁用各个 NTFS 卷上的 8.3 别名。 在 Windows Server 2008 R2 及更高版本系统中，如果使用 OS 格式化卷，则默认禁用短名称。 为了实现应用程序兼容性，系统卷上仍启用了短名称。
  * **支持扩展长度路径** ：许多 Windows API 函数的 Unicode 版本允许长度约为 32,767 个字符的扩展长度路径。 该总数超出了MAX_PATH设置定义的 260 个字符的路径限制。 有关详细的文件名和路径格式要求，以及实现扩展长度路径的指南，请参阅 [命名文件、路径和命名空间](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file)。
  * **群集存储** ：在故障转移群集中使用时，NTFS 支持连续可用的卷，当与 CSV 文件系统一起使用时，多个群集节点可以同时访问这些卷。 若要了解更多信息，请参阅[在故障转移群集中使用群集共享卷](https://learn.microsoft.com/zh-cn/windows-server/failover-clustering/failover-cluster-csvs)。


## 灵活分配容量
如果卷上的空间有限，NTFS 提供以下方法来处理服务器的存储容量：
  * 使用磁盘配额跟踪和控制各个用户的 NTFS 卷上的磁盘空间使用情况。
  * 使用文件系统压缩来最大程度地提高可存储的数据量。
  * 通过从同一磁盘或其他磁盘添加未分配的空间来增加 NTFS 卷的大小。
  * 如果用完了驱动器号，或者需要创建可从现有文件夹访问的额外空间，请在本地 NTFS 卷上的任何空文件夹中装载卷。


## 另请参阅
  * [Windows Server 存储文档](https://learn.microsoft.com/zh-cn/windows-server/storage/storage)
  * [弹性文件系统 （ReFS） 概述](https://learn.microsoft.com/zh-cn/windows-server/storage/refs/refs-overview)
  * [适用于 Windows Server 的 NTFS 中的新增](https://learn.microsoft.com/zh-cn/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/dn466520\(v%3dws.11\)) 功能（Windows Server 2012 R2）
  * [NTFS 中的新增功能](https://learn.microsoft.com/zh-cn/previous-versions/windows/it-pro/windows-server-2008-r2-and-2008/ff383236\(v=ws.10\)) （Windows Server 2008 R2、Windows 7）


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-08-16 


