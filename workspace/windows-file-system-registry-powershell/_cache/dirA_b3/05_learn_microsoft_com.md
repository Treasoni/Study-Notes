---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/compact"
title: "compact | Microsoft Learn"
scraped_at: 2026-09-10T15:41:26+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/compact) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/compact)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# compact
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


显示或更改 NTFS 分区上的文件或目录的压缩。 如果不带参数使用， **compact** 将显示当前目录及其包含的任何文件的压缩状态。
## Syntax

```
compact [/C | /U] [/S[:dir]] [/A] [/I] [/F] [/Q] [/EXE[:algorithm]] [/CompactOs[:option] [/windir:dir]] [filename [...]]

```

### Parameters  
| Parameter  | Description  |  
| --- | --- |  
| /c  | 压缩指定的目录或文件。 目录将被标记，以便压缩之后添加的任何文件，除非指定了 /EXE 参数。  |  
| /u  | 取消压缩指定的目录或文件。 将目录标记为以后添加的任何文件不会压缩。 如果指定了 /EXE 参数，则仅压缩为可执行文件的文件;如果未指定 /EXE 参数，则仅取消压缩 NTFS 压缩文件。  |  
| /s`[:<dir>]`  | 对指定目录和所有子目录中的文件执行所选作。 默认情况下，当前目录用作 `<dir>` 值。  |  
| /a  | 显示隐藏文件或系统文件。 默认情况下，不包括这些文件。  |  
| /i  | 继续执行指定的作，忽略错误。 默认情况下，此命令在遇到错误时停止。  |  
| /f  | 强制压缩或取消压缩指定的目录或文件。 默认情况下会跳过已压缩的文件。 **/f** 参数用于在作因系统崩溃而中断时部分压缩的文件。 若要强制整个压缩文件，请使用 **/c** 和 **/f** 参数并指定部分压缩的文件。  |  
| /q  | 仅报告最重要的信息。  |  
| /EXE  | 对经常读取但未修改的可执行文件使用经过优化的压缩。 支持的算法包括：
  * **XPRESS4K** （最快和默认值）
  * **XPRESS8K**
  * **XPRESS16K**
  * **LZX** （最紧凑）

 |  
| /CompactOs  | 设置或查询系统的压缩状态。 支持的选项包括：
  * **查询** - 查询系统的 **Compact** 状态。
  * **always** - 压缩所有作系统二进制文件并将系统状态设置为 Compact，除非管理员更改它，否则该状态将保持不变。
  * **never** - 解压缩所有作系统二进制文件并将系统状态设置为非压缩，除非管理员更改它，否则该状态将保留。

 |  
| /windir  | 在查询脱机作系统时与 **/CompactOs：query** 参数一起使用。 指定安装 Windows 的目录。  |  
| `<filename>`  | 指定模式、文件或目录。 可以使用多个文件名， ***** 以及 **和 ？** 通配符。  |  
| /?  | 在命令提示符下显示帮助。  |  
#### Remarks
  * 此命令是 NTFS 文件系统压缩功能的命令行版本。 目录的压缩状态指示将文件添加到目录时是否自动压缩。 设置目录的压缩状态不一定更改目录中已存在文件的压缩状态。
  * 不能使用此命令读取、写入或装载使用 DriveSpace 或 DoubleSpace 压缩的卷。 也不能使用此命令压缩文件分配表（FAT）或 FAT32 分区。


## Examples
若要设置当前目录的压缩状态、其子目录和现有文件，请键入：

```
compact /c /s

```

若要在当前目录中设置文件和子目录的压缩状态，而不更改当前目录本身的压缩状态，请键入：

```
compact /c /s *.*

```

若要压缩卷，请从卷的根目录中键入：

```
compact /c /i /s:\

```

Note
此示例设置所有目录（包括卷上的根目录）的压缩状态，并压缩卷上的每个文件。 **/i** 参数可防止错误消息中断压缩过程。
若要在 \tmp 目录和 \tmp 的所有子目录中使用 .bmp 文件扩展名压缩所有文件，而不修改目录的压缩属性，请键入：

```
compact /c /s:\tmp *.bmp

```

要强制完全压缩文件 _zebra.bmp_ ，该文件在系统崩溃期间被部分压缩，请键入：

```
compact /c /f zebra.bmp

```

若要从目录 c：\tmp 中删除压缩属性，而不更改该目录中任何文件的压缩状态，请键入：

```
compact /u c:\tmp

```

## Related links


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-08-16 


