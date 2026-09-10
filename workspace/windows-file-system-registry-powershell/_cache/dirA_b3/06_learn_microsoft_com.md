---
url: "https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-streams"
title: "文件流（本地文件系统） - Win32 apps | Microsoft Learn"
scraped_at: 2026-09-10T15:41:26+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-streams) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-streams)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# 文件流（本地文件系统）
流是字节序列。 在 NTFS 文件系统中，流包含写入文件的数据，并提供有关文件的详细信息，而不是属性。 例如，可以创建包含搜索关键字的流，也可以创建创建文件的用户帐户的标识。
与文件关联的每个流都有自己的分配大小、实际大小和有效数据长度：
  * 分配大小是为流保留的磁盘空间量。
  * 实际大小是调用方使用的字节数。
  * 有效数据长度（VDL）是从流的分配大小初始化的字节数。


每个流还维护自己的压缩、加密和稀疏状态。 如果任何流曾经是稀疏的，则文件上的 **FILE_ATTRIBUTE_SPARSE_FILE** 属性在从 [FindFirstFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-findfirstfilea)、[FindFirstFileEx](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-findfirstfileexa) 和 [FindNextFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-findnextfilea) 函数返回的 [WIN32_FIND_DATA](https://learn.microsoft.com/zh-cn/windows/win32/api/MinWinBase/ns-minwinbase-win32_find_dataa) 结构的 **dwFileAttributes** 成员中被设置。 [GetFileAttributes](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-getfileattributesa)、 [GetFileAttributesEx](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-getfileattributesexa)、 [GetFileAttributesTransacted](https://learn.microsoft.com/zh-cn/windows/win32/api/WinBase/nf-winbase-getfileattributestransacteda)、 [GetFileInformationByHandle](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-getfileinformationbyhandle) 和 [GetFileInformationByHandleEx](https://learn.microsoft.com/zh-cn/windows/win32/api/WinBase/nf-winbase-getfileinformationbyhandleex) 如果未指定任何流，则返回默认数据流的稀疏状态。
没有与流关联的文件时间。 更新文件中的任何流时，文件的文件时间将更新。
每个流维护机会锁。 每个流也维护共享模式。 在文件上请求删除访问权限时，作系统会检查文件中所有打开的流上的删除访问权限。 如果另一个进程打开了没有 **FILE_SHARE_DELETE** 权限的流，则无法打开文件以删除访问权限。
如果复制的文件具有数据流和使用网络重定向程序，则仅当客户端同时具有读取权限和读取属性权限时，才能复制该文件。
## 流的命名约定
从 Windows shell 命令行指定时，流的全名为“ _文件名_ ： _流名称_ ： _流类型_ ”，如以下示例所示：“myfile.dat：stream1：$DATA”。
对于文件名合法的任何字符，对于流名称（包括空格）也是合法的。 有关详细信息，请参阅 [命名文件](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file)。 流类型（也称为属性类型代码）是 NTFS 文件系统的内部类型。 因此，用户无法创建新的流类型，但可以打开现有的 NTFS 文件系统类型。 流类型说明符值始终以美元符号 （$） 符号开头。 有关流类型的列表，请参阅下文。
默认情况下，默认数据流未命名。 若要完全指定默认数据流，请使用“ _文件名_ ：：$DATA”，其中$DATA是流类型。 这相当于“ _文件名_ ”。 可以使用 [文件命名约定](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file)在文件中创建命名流。 请注意，“$DATA”是合法的流名称。 例如，名为“ _示例_ ”的文件中名为“$DATA”的流的完整名称将是“ _示例_ ：$DATA：$DATA”。 如果在同一文件上创建了名为“bar”的流，其全名将为“ _示例_ ：bar：$DATA”。
创建和使用具有一个字符名称的文件时，请为文件名加上句点后跟反斜杠（.），或使用完全限定的路径名称。 这样做的原因是 Windows 将单个字符文件名视为驱动器号。 使用相对路径指定驱动器号时，冒号会将驱动器号与路径分开。 如果单字符名称是驱动器号还是文件名存在歧义，则 Windows 假定如果冒号后面的字符串是有效路径，则 Windows 假定它是驱动器号，即使驱动器号无效。
## 流类型
下面是 NTFS 流类型的列表，也称为属性类型代码。 某些流类型是 NTFS 的内部类型，其格式是未记录的。  
| 流类型  | 描述  |  
| --- | --- |  
| ：：$ATTRIBUTE_LIST  | 包含构成文件的所有属性的列表，并标识每个属性的位置。  |  
| ：：$BITMAP  | 索引用于管理目录的 b 树可用空间的位图。 b 树以 4 KB 区块（而不考虑群集大小）进行管理，这用于管理这些区块的分配。 每个目录中都存在此流类型。  |  
| ：：$DATA  | 数据流。 默认数据流没有名称。 可以使用 [FindFirstStreamW](https://learn.microsoft.com/zh-cn/windows/win32/api/fileapi/nf-fileapi-findfirststreamw) 和 [FindNextStreamW](https://learn.microsoft.com/zh-cn/windows/win32/api/fileapi/nf-fileapi-findnextstreamw) 函数枚举数据流。  |  
| ：：$EA  | 包含扩展属性数据。  |  
| ：：$EA_INFORMATION  | 包含有关扩展属性的支持信息。  |  
| ：：$FILE_NAME  | 文件的名称（以 Unicode 字符为单位）。 这包括文件的短名称以及任何硬链接。  |  
| ：：$INDEX_ALLOCATION  | 目录的流类型。 用于实现大型目录的文件名分配。 此流表示目录本身，并包含目录的所有数据。 此类型的流更改记录到 NTFS 更改日志。 $INDEX_ALLOCATION 流类型的默认流名称为 $I 30，因此“ _DirName_ ”、“ _DirName_ ：：$INDEX_ALLOCATION”和“ _DirName_ ：$I 30：$INDEX_ALLOCATION”都是等效的。  |  
| ：：$INDEX_ROOT  | 此流表示索引的 b 树的根。 每个目录中都存在此流类型。  |  
| ：：$LOGGED_UTILITY_STREAM  | 类似于 ：：$DATA，但作记录到 NTFS 更改日志。 EFS 和 [事务性 NTFS （TxF）](https://learn.microsoft.com/zh-cn/windows/win32/fileio/transactional-ntfs-portal)使用。 EFS 的“： _StreamName_ ：$_StreamType_ ”对为“：$EFS：$LOGGED_UTILITY_STREAM”，TxF 的“：$TXF_DATA：$LOGGED_UTILITY_STREAM”。  |  
| ：：$OBJECT_ID  | 用于标识链接跟踪服务的文件的 16 字节 ID。  |  
| ：：$REPARSE_POINT  |  
## 相关内容
使用流 
[事务性 NTFS （TxF）](https://learn.microsoft.com/zh-cn/windows/win32/fileio/transactional-ntfs-portal)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-07-10 


