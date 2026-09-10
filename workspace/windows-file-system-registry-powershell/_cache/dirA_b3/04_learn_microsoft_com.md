---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/dir"
title: "dir | Microsoft Learn"
scraped_at: 2026-09-10T15:41:26+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/dir) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/dir)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# dir
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


显示目录的文件和子目录的列表。 如果未使用参数，此命令将显示磁盘的卷标签和序列号，后跟磁盘上的目录和文件列表（包括其名称和上次修改日期和时间）。 对于文件，此命令显示名称扩展名和大小（以字节为单位）。 此命令还显示列出的文件和目录总数、其累积大小以及磁盘上剩余的可用空间（以字节为单位）。
**dir** 命令也可以使用不同的参数从 Windows 恢复控制台运行。 有关详细信息，请参阅 [Windows 恢复环境（WinRE）](https://learn.microsoft.com/zh-cn/windows-hardware/manufacture/desktop/windows-recovery-environment--windows-re--technical-reference)。
## Syntax

```
dir [<drive>:][<path>][<filename>] [...] [/p] [/q] [/w] [/d] [/a[[:]<attributes>]][/o[[:]<sortorder>]] [/t[[:]<timefield>]] [/s] [/b] [/l] [/n] [/x] [/c] [/4] [/r]

```

### Parameters  
| Parameter  | Description  |  
| --- | --- |  
| `[<drive>:][<path>]`  | 指定要在其中查看列表的驱动器和目录。  |  
| `[<filename>]`  | 指定要查看其列表的特定文件或文件组。  |  
| /p  | 一次显示一个列表的一个屏幕。 若要查看下一个屏幕，请按任意键。  |  
| /q  | 显示文件所有权信息。  |  
| /w  | 以宽格式显示列表，每行包含多达五个文件名或目录名称。  |  
| /d  | 以与 **/w** 相同的格式显示列表，但文件按列排序。  |  
| /a[[:]`<attributes>`]  | 仅显示具有指定属性的目录和文件的名称。 如果不使用此参数，该命令将显示除隐藏文件和系统文件之外的所有文件的名称。 如果在未指定任何 _属性_ 的情况下使用此参数，则该命令将显示所有文件的名称，包括隐藏文件和系统文件。 可能的 _属性_ 值列表包括：
  * **d** - 目录
  * **h** - 隐藏文件
  * **s** - 系统文件
  * **l** - 重新分析点
  * **r** - 只读文件
  * **a** - 准备存档的文件
  * **i** - 未索引内容的文件

可以使用这些值的任意组合，但不要使用空格分隔值。 （可选）可以使用冒号（:)分隔符），也可以使用连字符（-）作为前缀来表示“not”。 例如，使用 **-s** 属性不会显示系统文件。  |  
| /o[[:]`<sortorder>`]  | 根据 _排序顺序_ 对输出进行排序，排序顺序可以是以下值的任意组合：
  * **n** - 按名称字母顺序排列
  * **e** - 按字母顺序扩展
  * **g** - 首先组目录
  * **s** - 按大小，最小在前
  * **d** - 按日期/时间，最早的在前
  * 使用 **-** 前缀来反转排序顺序

将按照列出这些值的顺序处理多个值。 不要用空格分隔多个值，但可以选择使用冒号（:)）。如果未指定 _sortorder_ ，则 **dir /o** 按字母顺序列出目录，然后列出文件，这些文件也按字母顺序排序。  |  
| /t[[:]`<timefield>`]  | 指定要显示或用于排序的时间字段。 可用的 _时间字段_ 值包括：
  * **c** - 创造
  * **a** - 上次访问时间
  * **w** - 上次写入

 |  
| /s  | 列出指定目录和所有子目录中指定文件名的每个匹配项。  |  
| /b  | 显示目录和文件的裸列表，没有其他信息。 **/b** 参数重写 **/w** 。  |  
| /l  | 使用小写显示未排序的目录名称和文件名。  |  
| /n  | 在屏幕最右侧显示具有文件名的长列表格式。  |  
| /x  | 显示为非 8dot3 文件名生成的短名称。 显示与 **/n** 的显示相同，但短名称插入到长名称之前。  |  
| /c  | 以文件大小显示千位分隔符。 这是默认行为。 使用 **/-c** 隐藏分隔符。  |  
| /4  | 以四位数格式显示年份。 由于默认 **的dir** 输出已经可以显示四位数年份，使用这个参数时你可能不会注意到变化。  |  
| /r  | 显示文件的备用数据流。  |  
| /?  | 在命令提示符下显示帮助。  |  
#### Remarks
  * 要使用多个 _文件名_ 参数，请用空格、逗号或分号分隔每个文件名。
  * 您可以使用通配符（***** 或 **？** ）来表示文件名的一个或多个字符，并显示文件或子目录的子集。
  * 可以使用通配符（***** ）替换任何字符串字符，例如：
    * `dir *.txt` 列出了当前目录中以 .txt开头的所有文件，例如 .txt、.txt1、.txt_old。
    * `dir read *.txt` 列出以读取开头的当前目录中的所有文件，以及以 .txt开头的扩展名，例如 .txt、.txt1 或 .txt_old。
    * `dir read *.*` 列出以任何扩展名读取开头的当前目录中的所有文件。
星号通配符始终使用短文件名映射，因此可能会获得意外的结果。 例如，以下目录包含两个文件（t.txt2 和 t97.txt）：

```
C:\test>dir /x
Volume in drive C has no label.
Volume Serial Number is B86A-EF32

Directory of C:\test

11/30/2004  01:40 PM <DIR>  .
11/30/2004  01:40 PM <DIR> ..
11/30/2004  11:05 AM 0 T97B4~1.TXT t.txt2
11/30/2004  01:16 PM 0 t97.txt

```

你可能希望键入 `dir t97\*` 将返回文件 t97.txt。 但是，键入会 `dir t97\*` 返回这两个文件，因为星号通配符使用其短名称映射 _T97B4~1.TXT_ 将文件 t.txt2 与 t97.txt 匹配。 同样，键入 `del t97\*` 将删除这两个文件。
  * 可以使用问号（？）作为名称中单个字符的替代项。 例如，键入 `dir read???.txt` 会列出当前目录中以读取开头且后跟最多三个字符的 .txt 扩展名的文件。 这包括 Read.txt、Read1.txt、Read12.txt、Read123.txt和 Readme1.txt，但不包括 Readme12.txt。
  * 如果在**属性** 中使用具有多个值的 _/a_ ，则此命令仅显示具有所有指定属性的文件的名称。 例如，如果将 **/a** 与 **r** 和 **-h** 用作属性（通过使用任一 `/a:r-h` 或 `/ar-h`），则此命令将仅显示未隐藏的只读文件的名称。
  * 如果指定多个 _排序顺序_ 值，则此命令将按第一个条件对文件名进行排序，然后按第二个条件对文件名进行排序，依此类推。 例如，如果将 **/o** 与 **sortorder** 的 **e** 和 _-s_ 参数一起使用（通过使用任一`/o:e-s`或 `/oe-s`），则此命令将按扩展名对目录和文件的名称进行排序，首先是最大的，然后显示最终结果。 按扩展名进行字母排序会导致没有扩展名的文件名首先出现，然后是目录名称，然后是扩展名的文件名。
  * 如果使用重定向符号 （） 将此命令的输出发送到文件，或者使用管道 （`|`） 将此命令的输出发送到另一个命令，则必须使用 `/a:-d` 仅列出文件名。 可以将 _filename_ 与 **/b** 和 **/s** 一起使用，以指定此命令在当前目录及其子目录中搜索与 _filename_ 匹配的所有文件名。 此命令仅列出找到的每个文件名的驱动器号、目录名称、文件名和文件扩展名（每行一个路径）。 在使用管道将此命令的输出发送到另一个命令之前，应在 Autoexec.nt 文件中设置 _TEMP_ 环境变量。


## Examples
若要按字母顺序显示所有目录，采用宽格式，并在每个屏幕后暂停，请确保根目录是当前目录，然后键入：

```
dir /s/w/o/p

```

输出列出了根目录、子目录和根目录中的文件，包括扩展。 此命令还会列出树中每个子目录中的子目录名称和文件名。
要更改前面的示例，使 **dir** 显示文件名和扩展名，但省略目录名称，请键入：

```
dir /s/w/o/p/a:-d

```

若要打印目录列表，请键入：

```
dir > prn

```

指定 **prn** 时，目录列表将发送到连接到 LPT1 端口的打印机。 如果您的打印机连接到其他端口，则必须将 **prn** 替换为正确端口的名称。
您还可以通过将 **prn** 替换为文件名来将 **dir** 命令的输出重定向到文件。 还可以键入路径。 例如，要将 **dir** 输出定向到 Records 目录中的文件dir.doc，请键入：

```
dir > \records\dir.doc

```

如果dir.doc不存在，则 **dir** 会创建它，除非 **Records** 目录不存在。 在这种情况下，将显示以下消息：

```
File creation error

```

若要显示驱动器 C 上所有目录中具有 .txt 扩展名的所有文件名的列表，请键入：

```
dir c:\*.txt /w/o/s/p

```

**dir** 命令以宽格式显示每个目录中匹配文件名的字母顺序列表，每次屏幕填满时它都会暂停，直到您按任意键继续。
## Related links


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-08-16 


