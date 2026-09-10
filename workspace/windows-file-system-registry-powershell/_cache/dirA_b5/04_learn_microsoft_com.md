---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-sparse"
title: "fsutil sparse | Microsoft Learn"
scraped_at: 2026-09-10T15:42:00+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-sparse) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-sparse)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# fsutil sparse
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


管理稀疏文件。 稀疏文件是其中包含一个或多个未分配数据区域的文件。
程序将这些未分配区域视为包含零值字节的区域，并且认为没有任何磁盘空间来表示这些零。 读取稀疏文件时，已分配的数据按存储方式返回，未分配的数据作为零返回（默认情况，遵循 C2 安全需求规范）。 稀疏文件支持允许从文件中的任何位置释放数据。
## Syntax

```
fsutil sparse [queryflag] <filename>
fsutil sparse [queryrange] <filename>
fsutil sparse [setflag] <filename>
fsutil sparse [setrange] <filename> <beginningoffset> <length>

```

### Parameters  
| Parameter  | Description  |  
| --- | --- |  
| queryflag  | Queries sparse.  |  
| queryrange  | 扫描文件并搜索可能包含非零数据的范围。  |  
| setflag  | 将指示的文件标记为稀疏。  |  
| setrange  | 用零填充文件的指定范围。  |  
| `<filename>`  | 指定文件的完整路径，包括文件名和扩展名，例如 _C:\documents\filename.txt_ 。  |  
| `<beginningoffset>`  | 指定文件中要标记为稀疏的偏移量。  |  
| `<length>`  | 指定文件中要标记为稀疏的区域的长度（以字节为单位）。  |  
#### Remarks
  * 所有有意义或非零的数据都会被分配，而所有无意义的数据（由零组成的大型数据串）都不会被分配。
  * 在稀疏文件中，大范围的零可能不需要磁盘分配。 写入文件时，会根据需要为非零数据分配空间。
  * 只有压缩文件或稀疏文件才能具有操作系统已知的清零范围。
  * 如果文件是稀疏或压缩，NTFS 可能会取消分配文件中的磁盘空间。 这会将字节范围设置为零，而不会扩展文件大小。


### Examples
要将 _c：\temp_ 目录中名为 _sample.txt_ 的文件标记为稀疏文件，请键入：

```
fsutil sparse setflag c:\temp\sample.txt

```

## Related links
  *   * [fsutil](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil)


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-08-16 


