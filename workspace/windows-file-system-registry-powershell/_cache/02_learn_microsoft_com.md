---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_character_encoding"
title: "about_Character_Encoding - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:04+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# about_Character_Encoding
## 简短说明
介绍 PowerShell 如何对字符串数据的输入和输出使用字符编码。
## 详细说明
Unicode 是一种全球字符编码标准。 系统专门使用 Unicode 进行字符和字符串操作。 有关 Unicode 的各个方面的详细说明，请参阅 [Unicode 标准](https://www.unicode.org/standard/standard.html)。
Windows 支持 Unicode 和传统字符集。 传统字符集（如 Windows 代码页）使用 8 位值或 8 位值的组合来表示特定语言或地理区域设置中使用的字符。
PowerShell 默认使用 Unicode 字符集。 但是，多个 cmdlet 具有 **编码** 参数，可以指定不同字符集的编码。 此参数允许你选择与其他系统和应用程序互操作性所需的特定字符编码。
以下 cmdlet 具有 **Encoding** 参数：
  * Microsoft.PowerShell.Management
    * Add-Content
    * Get-Content
    * Set-Content
  * Microsoft.PowerShell.Utility
    * Export-Clixml
    * Export-Csv
    * Export-PSSession
    * Format-Hex
    * Import-Csv
    * Out-File
    * Select-String
    * Send-MailMessage


## 字节顺序标记
字节顺序标记（BOM）是位于文件或文本流的前几个字节中的 _Unicode 签名_ ，用于指示数据采用的 Unicode 编码。 有关详细信息，请参阅 [字节顺序标记](https://learn.microsoft.com/zh-cn/globalization/encoding/byte-order-mark) 文档。
在 Windows PowerShell 中，除 `UTF7`之外的任何 Unicode 编码始终创建 BOM。 PowerShell（v6 及更高版本）默认为所有文本输出 `utf8NoBOM`。
为获得最佳整体兼容性，请避免在 UTF-8 文件中使用 BOM。 Unix 平台和 Windows 平台上使用的 Unix 继承实用程序不支持 BOM。
同样，应避免使用 `UTF7` 编码。 UTF-7 不是标准的 Unicode 编码，并且在所有版本的 PowerShell 中都未编写 BOM。
在类似 Unix 的平台上或使用 Windows 上的跨平台编辑器（如 Visual Studio Code）创建 PowerShell 脚本会导致使用 `UTF8NoBOM`编码的文件。 这些文件在 PowerShell 中正常工作，但如果文件包含非 Ascii 字符，则可能会在 Windows PowerShell 中中断。
如果需要在脚本中使用非 Ascii 字符，请使用 BOM 将它们另存为 UTF-8。 如果没有 BOM，Windows PowerShell 会将脚本误解为使用过时的“ANSI”代码页进行编码。 相反，在类似 Unix 的平台上，具有 UTF-8 BOM 的文件可能会出现问题。 许多 Unix 工具（如 `cat`、`sed`、`awk`）和某些编辑器（如 `gedit`）不知道如何处理 BOM。
## Windows PowerShell 中的字符编码
在 PowerShell 5.1 中，**Encoding** 参数支持以下值：
  * `Ascii` 使用 Ascii （7 位） 字符集。
  * `BigEndianUnicode` 将 UTF-16 与 big-endian 字节顺序配合使用。
  * `BigEndianUTF32` 将 UTF-32 与 big-endian 字节顺序配合使用。
  * `Byte` 将一组字符编码为字节序列。
  * `Default` 使用与系统的活动代码页（通常是 ANSI）对应的编码。
  * `Oem` 使用与系统的当前 OEM 代码页对应的编码。
  * `String` 与 `Unicode`相同。
  * `Unicode` 使用 UTF-16 和小端字节序。
  * `Unknown` 与 `Unicode`相同。
  * `UTF32` 将 UTF-32 与 little-endian 字节顺序配合使用。
  * `UTF7` 使用 UTF-7。
  * `UTF8` 使用 UTF-8（带 BOM）。


通常，Windows PowerShell 默认使用 Unicode [UTF-16LE](https://wikipedia.org/wiki/UTF-16) 编码。 但是，Windows PowerShell 中 cmdlet 使用的默认编码不一致。
注意
使用任何 Unicode 编码（除 `UTF7`以外）总是会创建 BOM。
对于将输出写入文件的 cmdlet：
  * `Out-File` 和重定向运算符 和 `>>` 创建 UTF-16LE，这明显不同于 `Set-Content` 和 `Add-Content`。
  * `New-ModuleManifest` 和 `Export-Clixml` 还创建 UTF-16LE 文件。
  * 当目标文件为空或不存在时，`Set-Content``Add-Content` 使用 `Default` 编码。 `Default` 是由当前系统语言环境的 ANSI 旧代码页指定的编码。
  * `Export-Csv` 创建 `Ascii` 文件，但在使用 **Append** 参数时使用不同的编码（请参阅下文）。
  * 默认情况下，`Export-PSSession` 使用 BOM 创建 UTF-8 文件。
  * `New-Item -Type File -Value` 会创建不带 BOM 的 UTF-8 文件。
  * 默认情况下，`Send-MailMessage` 使用 `Ascii` 编码。
  * `Start-Transcript` 创建 `Utf8` 带有 BOM 的文件。 使用 **Append** 参数时，编码可能有所不同（请参阅下文）。


对于在现有文件中追加的命令：
  * `Out-File -Append` 和 `>>` 重定向运算符不会尝试匹配现有目标文件内容的编码。 而是使用默认编码，除非使用 **Encoding** 参数。 在追加内容时，必须使用文件原始编码。
  * 如果没有显式 **编码** 参数，`Add-Content` 会检测现有编码，并自动将其应用于新内容。 如果现有内容没有 BOM，则使用 `Default` ANSI 编码。 在 PowerShell（v6 及更高版本）中，`Add-Content` 的行为相同，但默认编码为 `Utf8`。
  * 当目标文件包含 BOM 时，`Export-Csv -Append` 与现有编码匹配。 如果没有 BOM，则使用 `Utf8` 编码。
  * `Start-Transcript -Append` 与包含 BOM 的文件的现有编码匹配。 如果没有 BOM，则默认为 `Ascii` 编码。 当脚本中的数据包含多字节字符时，此编码可能会导致数据丢失或字符损坏。


对于在没有 BOM 的情况下读取字符串数据的 cmdlet：
  * `Get-Content` 和 `Import-PowerShellDataFile` 使用 `Default` ANSI 编码。 ANSI 也是 PowerShell 引擎从文件读取源代码时使用的内容。
  * 在没有 BOM 的情况下，`Import-Csv`、`Import-Clixml`和 `Select-String` 假定 `Utf8`。


## PowerShell 中的字符编码
在 PowerShell（v7.1 及更高版本）中，**Encoding** 参数支持以下值：
  * `ascii`：对 ASCII（7 位）字符集使用编码。
  * `ansi`：对当前区域性的 ANSI 代码页使用编码。 此选项已在 PowerShell 7.4 中添加。
  * `bigendianunicode`：使用大端字节序以 UTF-16 格式进行编码。
  * `bigendianutf32`：使用大端字节顺序以 UTF-32 格式编码。
  * `oem`：对 MS-DOS 和控制台程序使用默认编码。
  * `unicode`：使用小端字节序以 UTF-16 格式进行编码。
  * `utf7`：采用 UTF-7 格式编码。
  * `utf8`：采用 UTF-8 格式（无 BOM）进行编码。
  * `utf8BOM`：使用字节序标记 (BOM) 以 UTF-8 格式进行编码
  * `utf8NoBOM`：采用不带字节顺序标记（BOM）的 UTF-8 格式进行编码。
  * `utf32`：使用小端字节序以 UTF-32 格式进行编码。


PowerShell 默认将所有输出设置为 `utf8NoBOM`。
从 PowerShell 6.2 开始，**编码参数** 还允许使用注册代码页的数字 ID（如 `-Encoding 1251`）或注册代码页的字符串名称（如 `-Encoding "windows-1251"`）。 有关详细信息，请参阅 [Encoding.CodePage](https://learn.microsoft.com/zh-cn/dotnet/api/system.text.encoding.codepage).NET 文档。
从 PowerShell 7.4 开始，可以使用 `ANSI` 参数的 值来传递当前区域性 ANSI 代码页的数字 ID，而无需手动指定它。
## 更改默认编码
PowerShell 有两个可用于更改默认编码行为的默认变量。
  * `$PSDefaultParameterValues`
  * `$OutputEncoding`


有关详细信息，请参阅 [about_Preference_Variables](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_preference_variables?view=powershell-7.6)。
从 PowerShell 5.1 开始，重定向运算符（ 和 `>>`）调用 `Out-File` cmdlet。 因此，可以使用 `$PSDefaultParameterValues` 首选项变量设置默认编码，如以下示例所示：

```
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

```

使用以下语句更改具有 **Encoding** 参数的所有 cmdlet 的默认编码。

```
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

```

重要
将此命令放在 PowerShell 配置文件中会使首选项成为影响未显式指定编码的所有命令和脚本的会话全局设置。
同样，应该在你希望行为方式与此相同的脚本或模块中包含这样的命令。 使用这些命令可确保 cmdlet 的行为方式相同，即使其他用户、在另一台计算机或不同版本的 PowerShell 中运行也是如此。
自动变量 `$OutputEncoding` 影响 PowerShell 用来与外部程序通信的编码。 它不会影响输出重定向运算符和 PowerShell cmdlet 用于保存到文件的编码。
## 另请参阅
  * [about_Preference_Variables](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_preference_variables?view=powershell-7.6)
  * [.NET](https://learn.microsoft.com/zh-cn/dotnet/standard/base-types/character-encoding-introduction) 中的字符编码简介


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-01-30 


