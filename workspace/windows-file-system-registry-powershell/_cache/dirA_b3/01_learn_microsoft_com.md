---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/attrib"
title: "attrib | Microsoft Learn"
scraped_at: 2026-09-10T15:41:26+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/attrib) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/attrib)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# attrib
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


显示、设置或删除分配给文件或目录的属性。 如果不带参数使用， **attrib** 会显示当前目录中所有文件的属性。
## Syntax

```
attrib [{+|-}r] [{+|-}a] [{+|-}s] [{+|-}h] [{+|-}o] [{+|-}i] [{+|-}x] [{+|-}p] [{+|-}u] [{+|-}b] [<drive>:][<path>][<filename>] [/s [/d] [/l]]

```

### Parameters  
| Parameter  | Description  |  
| --- | --- |  
| `{+\|-}r`  | 设置 （**+** ） 或清除 （**-** ） 只读文件属性。  |  
| `{+\|-}a`  | 设置 （**+** ） 或清除 （**-** ） 存档文件属性。 此属性集标记自上次备份以来已更改的文件。 **xcopy** 命令使用归档属性。  |  
| `{+\|-}s`  | 设置 （**+** ） 或清除系统**-** 文件属性。 如果文件使用此属性集，则必须清除该属性，然后才能更改文件的任何其他属性。  |  
| `{+\|-}h`  | 设置 （**+** ） 或清除 （**-** ） 隐藏文件属性。 如果文件使用此属性集，则必须清除该属性，然后才能更改文件的任何其他属性。  |  
| `{+\|-}o`  | 设置 （**+** ） 或清除 （**-** ） 脱机文件属性。  |  
| `{+\|-}i`  | 设置 （**+** ） 或清除 （**-** ） 非内容索引文件属性。  |  
| `{+\|-}x`  | 设置 （**+** ） 或清除 （**-** ） 清理文件属性。  |  
| `{+\|-}p`  | 设置 （**+** ） 或清除固定**-** 文件属性。  |  
| `{+\|-}u`  | 设置 （**+** ） 或清除 （**-** ） 未固定的文件属性。  |  
| `{+\|-}b`  | 设置 （**+** ） 或清除 （**-** ） SMR Blob 文件属性。  |  
| `[<drive>:][<path>][<filename>]`  | 指定要查看或更改属性的目录、文件或文件组的位置和名称。可以在 _filename_ 参数中使用 **？** 和***** 通配符来显示或更改一组文件的属性。  |  
| /s  | 将 **attrib** 和任何命令行选项应用于当前目录及其所有子目录中的匹配文件。  |  
| /d  | 将 **attrib** 和任何命令行选项应用于目录。  |  
| /l  | 将 **属性** 和任何命令行选项应用于符号链接，而不是符号链接的目标。  |  
| /?  | 在命令提示符下显示帮助。  |  
## Examples
若要显示位于当前目录中的名为 News86 的文件的属性，请键入：

```
attrib news86

```

若要将只读属性分配给名为 report.txt的文件，请键入：

```
attrib +r report.txt

```

若要从公共目录中的文件及其驱动器 b：中的磁盘上的子目录中删除只读属性，请键入：

```
attrib -r b:\public\*.* /s

```

若要为驱动器 a：上的所有文件设置 Archive 属性，然后清除具有.bak扩展名的文件的 Archive 属性，请键入：

```
attrib +a a:*.* & attrib -a a:*.bak

```

## Related links
  * [xcopy command](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/xcopy)


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-08-16 


