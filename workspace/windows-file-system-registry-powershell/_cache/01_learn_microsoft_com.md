---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/get-help"
title: "Get-Help (Microsoft.PowerShell.Core) - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:04+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/get-help?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/get-help?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# Get-Help 

模块:
    [Microsoft.PowerShell.Core Module](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/?view=powershell-7.6)
显示有关 PowerShell 命令和概念的信息。
## 语法
###  AllUsersView (默认值) 

```
Get-Help
    [[-Name] <String>]
    [-Path <String>]
    [-Category <String[]>]
    [-Full]
    [-Component <String[]>]
    [-Functionality <String[]>]
    [-Role <String[]>]
    [<CommonParameters>]

```

###  DetailedView 

```
Get-Help
    [[-Name] <String>]
    -Detailed
    [-Path <String>]
    [-Category <String[]>]
    [-Component <String[]>]
    [-Functionality <String[]>]
    [-Role <String[]>]
    [<CommonParameters>]

```

###  EXAMPLES 

```
Get-Help
    [[-Name] <String>]
    -Examples
    [-Path <String>]
    [-Category <String[]>]
    [-Component <String[]>]
    [-Functionality <String[]>]
    [-Role <String[]>]
    [<CommonParameters>]

```

###  PARAMETERS 

```
Get-Help
    [[-Name] <String>]
    -Parameter <String[]>
    [-Path <String>]
    [-Category <String[]>]
    [-Component <String[]>]
    [-Functionality <String[]>]
    [-Role <String[]>]
    [<CommonParameters>]

```

###  Online 

```
Get-Help
    [[-Name] <String>]
    -Online
    [-Path <String>]
    [-Category <String[]>]
    [-Component <String[]>]
    [-Functionality <String[]>]
    [-Role <String[]>]
    [<CommonParameters>]

```

###  ShowWindow 

```
Get-Help
    [[-Name] <String>]
    -ShowWindow
    [-Path <String>]
    [-Category <String[]>]
    [-Component <String[]>]
    [-Functionality <String[]>]
    [-Role <String[]>]
    [<CommonParameters>]

```

## 说明
`Get-Help` cmdlet 显示有关 PowerShell 概念和命令的信息，包括 cmdlet、函数、Common Information Model （CIM） 命令、工作流、提供程序、别名和脚本。
若要获取 PowerShell cmdlet 的帮助，请键入 `Get-Help` 后跟 cmdlet 名称，例如：`Get-Help Get-Process`。
PowerShell 中的概念帮助文章以 **about_** 开头，例如 **about_Comparison_Operators** 。 若要查看所有 about_ 文章，请键入 `Get-Help about_*`。 若要查看特定文章，请键入 `Get-Help about_<article-name>`，例如 `Get-Help about_Comparison_Operators`。
若要获取有关 PowerShell 提供程序的帮助，请键入 `Get-Help`，后跟提供程序名称。 例如，若要获取证书提供程序的帮助，请键入 `Get-Help Certificate`。
还可以键入 `help` 或 `man`，这样会一次显示一个文本屏幕。 或者，`<cmdlet-name> -?`，这与 `Get-Help`相同，但仅适用于 cmdlet。
`Get-Help` 从计算机上的帮助文件中获取其显示的帮助内容。 如果没有帮助文件，`Get-Help` 仅显示有关 cmdlet 的基本信息。 某些 PowerShell 模块包括帮助文件。 从 PowerShell 3.0 开始，Windows操作系统附带的模块不包含帮助文件。 若要在 PowerShell 3.0 中下载或更新模块的帮助文件，请使用 `Update-Help` cmdlet。
还可以联机查看 PowerShell 帮助文档。 若要获取帮助文件的联机版本，请使用 **Online** 参数，例如：`Get-Help Get-Process -Online`。
如果您键入 `Get-Help`，然后输入帮助文章的确切名称或该帮助文章中特有的单词，那么 `Get-Help` 将显示该文章的内容。 如果您指定命令别名的确切名称，`Get-Help` 将显示该原始命令的帮助信息。 如果输入多个帮助文章标题中显示的单词或单词模式，`Get-Help` 显示匹配标题的列表。 如果输入任何未显示在任何帮助文章标题中的文本，`Get-Help` 将显示在其内容中包含该文本的文章列表。
`Get-Help` 可以获取所有支持的语言和区域设置的帮助文章。 `Get-Help`首先查找Windows区域设置中的帮助文件，然后在父区域设置（如 **pt** for **pt-BR** ），然后在回退区域设置中查找帮助文件。 从 PowerShell 3.0 开始，如果 `Get-Help` 在回退区域设置中找不到帮助，则会在返回错误消息或显示自动生成的帮助之前查找英语帮助文章 **en-US** 。
有关 `Get-Help` 命令语法图中显示的符号的信息，请参阅 [about_Command_Syntax](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_command_syntax?view=powershell-7.6)。 有关参数属性（例如 Required 和 Position）的信息，请参阅 **about_Parameters** 。
注释
在 PowerShell 3.0 和 PowerShell 4.0 中，除非将模块导入当前会话，否则 `Get-Help` 无法在模块中找到 About 文章。 若要获取模块中的 About 文章，请使用 cmdlet 或运行该模块中包含的 cmdlet 导入该模块`Import-Module`。
从 **PSReadLine** v2.2.2 开始，该模块附带了两个函数，可在命令行上键入命令时快速访问帮助。 帮助显示在终端的备用屏幕缓冲区中并分页。
按 F1 键时，PSReadLine 函数会调用 以获取最靠近光标左侧的 cmdlet 名称。`ShowCommandHelp``Get-Help -Full` 当光标紧挨着参数左侧时，函数将跳转到该参数的完整帮助主题的说明部分。 点击 `Q` 退出帮助视图时，将返回到位于同一游标位置的命令行，以便可以继续键入命令。
当您使用组合键 `Alt`+`h`时，**PSReadLine**`ShowParameterHelp` 函数会显示位于光标左侧参数的帮助信息。 帮助文本显示在命令行下方。 这允许你查看参数的说明并继续键入命令。
有关详细信息，请参阅[使用动态帮助](https://learn.microsoft.com/zh-cn/powershell/scripting/learn/shell/dynamic-help)。
## 示例
### 示例 1：显示有关 cmdlet 的基本帮助信息
这些示例显示有关 `Format-Table` cmdlet 的基本帮助信息。

```
Get-Help Format-Table
Get-Help -Name Format-Table
Format-Table -?

```

`Get-Help <cmdlet-name>` 是 `Get-Help` cmdlet 的最简单和默认语法。 可以省略 **Name** 参数。
语法 `<cmdlet-name> -?` 仅适用于 cmdlet。
### 示例 2：一次显示一页的基本信息
这些示例显示有关 `Format-Table` cmdlet 的基本帮助信息，一次显示一页。

```
help Format-Table
man Format-Table
Get-Help Format-Table | Out-Host -Paging

```

`help` 是在内部运行 `Get-Help` cmdlet 并一次显示一页结果的函数。
`man` 是 `help` 函数的别名。
`Get-Help Format-Table` 将对象发送到管道。 `Out-Host -Paging` 接收来自管道的输出，并逐页显示。 有关详细信息，请参阅 [Out-Host](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/out-host?view=powershell-7.6)。
### 示例 3：显示更多有关 cmdlet 的信息
这些示例显示有关 `Format-Table` cmdlet 的更详细的帮助信息。

```
Get-Help Format-Table -Detailed
Get-Help Format-Table -Full

```

Detailed 参数显示帮助文章的详细视图，其中包括参数说明和示例。
**Full** 参数显示帮助文章的完整视图，其中包括参数说明、示例、输入和输出对象类型以及其他说明。
Detailed 和 Full 参数仅对计算机上安装了帮助文件的命令有效。 这些参数对于概念性 (about_) 帮助文章无效。
### 示例 4：使用参数显示 cmdlet 的选定部分
这些示例显示 `Format-Table` cmdlet 帮助的选定部分。

```
Get-Help Format-Table -Examples
Get-Help Format-Table -Parameter *
Get-Help Format-Table -Parameter GroupBy

```

**Examples** 参数显示帮助文件的 **NAME** 和 **SYNOPSIS** 部分以及所有示例。 无法指定示例编号，因为 **Examples** 参数是参数 `[switch]` 。
**参数** 参数仅显示指定参数的说明。 如果仅指定星号（`*`）通配符，则会显示所有参数的说明。 当 **参数** 指定参数名称（如 **GroupBy** ）时，将显示有关该参数的信息。
这些参数对于概念性 (about_) 帮助文章无效。
### 示例 5：显示联机版本的帮助
本示例显示默认 Web 浏览器中 `Format-Table` cmdlet 的帮助文章的联机版本。

```
Get-Help Format-Table -Online

```

### 示例 6：显示有关帮助系统的帮助
不带参数的 `Get-Help` cmdlet 显示有关 PowerShell 帮助系统的信息。

```
Get-Help

```

### 示例 7：显示可用的帮助文章
本示例显示计算机上可用的所有帮助文章的列表。

```
Get-Help *

```

### 示例 8：显示概念文章列表
本示例显示 PowerShell 帮助中包含的概念文章列表。 所有这些文章都以字符 **about_** 开头。 若要显示特定的帮助文件，请键入 `Get-Help \<about_article-name\>`，例如 `Get-Help about_Signing`。
仅显示计算机上安装了帮助文件的概念文章。 有关在 PowerShell 3.0 中下载和安装帮助文件的信息，请参阅 [Update-Help](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/update-help?view=powershell-7.6)。

```
Get-Help about_*

```

### 示例 9：在 cmdlet 帮助中搜索单词
此示例演示如何在 cmdlet 帮助文章中搜索单词。

```
Get-Help Add-Member -Full | Out-String -Stream | Select-String -Pattern Clixml

```

```
the Export-Clixml cmdlet to save the instance of the object, including the additional members...
can use the Import-Clixml cmdlet to re-create the instance of the object from the information...
Export-Clixml
Import-Clixml

```

`Get-Help`使用 **Full** 参数获取 `Add-Member` 的帮助信息并返回。 `Out-String` 使用 **Stream** 参数将对象转换为字符串。 `Select-String` 使用 **Pattern** 参数搜索 **Clixml** 的字符串。
### 示例 10：显示包含单词的文章列表
此示例显示包含单词 remoting 的文章列表。
输入任何文章标题中未显示的单词时，`Get-Help` 显示包含该单词的文章列表。

```
Get-Help -Name remoting

```

```
Name                              Category  Module                    Synopsis
----                              --------  ------                    --------
Install-PowerShellRemoting.ps1    External                            Install-PowerShellRemoting.ps1
Disable-PSRemoting                Cmdlet    Microsoft.PowerShell.Core Prevents remote users...
Enable-PSRemoting                 Cmdlet    Microsoft.PowerShell.Core Configures the computer...

```

### 示例 11：显示特定于提供程序的帮助
此示例显示了获取 `Get-Item` 的特定于提供程序的帮助的两种方式。 这些命令获得帮助，说明如何在 PowerShell SQL Server 提供程序的 **DataCollection** 节点中使用 `Get-Item` cmdlet。
第一个示例使用 `Get-Help`**Path** 参数指定SQL Server提供程序的路径。 由于指定了提供程序的路径，因此可以从任何路径位置运行命令。
第二个示例使用 `Set-Location` 导航到SQL Server提供程序的路径。 从该位置开始， 无需使用 Path 参数来获取特定于提供程序的帮助`Get-Help`。

```
Get-Help Get-Item -Path SQLSERVER:\DataCollection

```

```
NAME

    Get-Item

SYNOPSIS

    Gets a collection of Server objects for the local computer and any computers

    to which you have made a SQL Server PowerShell connection.
    ...

```

```
Set-Location SQLSERVER:\DataCollection
SQLSERVER:\DataCollection> Get-Help Get-Item

```

```
NAME

    Get-Item

SYNOPSIS

    Gets a collection of Server objects for the local computer and any computers

    to which you have made a SQL Server PowerShell connection.
    ...

```

### 示例 12：显示脚本的帮助
此示例获取有关 `MyScript.ps1 script` 的帮助。 有关如何为函数和脚本编写帮助的信息，请参阅 [about_Comment_Based_Help](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_comment_based_help?view=powershell-7.6)。

```
Get-Help -Name C:\PS-Test\MyScript.ps1

```

## 参数
### -Category
只显示指定类别及其别名中的项的帮助。 概念文章位于 **HelpFile** 类别中。
此参数的可接受值如下所示：
  * 别名
  * Cmdlet (命令行工具)
  * 提供者
  * 概况
  * FAQ
  * 术语表
  * HelpFile
  * ScriptCommand
  * 功能
  * 过滤器
  * ExternalScript
  * 全部
  * DefaultHelp
  * Workflow
  * DscResource
  * 班级
  * 配置


#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 接受的值:  | Alias, Cmdlet, Provider, General, FAQ, Glossary, HelpFile, ScriptCommand, Function, Filter, ExternalScript, All, DefaultHelp, Workflow, DscResource, Class, Configuration  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Component
显示具有指定组件值的命令，例如 **Exchange** 。 输入组件名称。 允许使用通配符。 此参数对概念性 (About_) 帮助的显示不起作用。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Detailed
向基本帮助显示添加参数说明和示例。 仅当计算机上安装帮助文件时，此参数才有效。 它对概念性 (About_) 帮助的显示不起作用。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | False  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
DetailedView   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Examples
仅显示名称、摘要和示例。 仅当计算机上安装帮助文件时，此参数才有效。 它对概念性 (About_) 帮助的显示不起作用。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | False  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
Examples   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Full
显示 cmdlet 的整个帮助文章。 Full 包括参数说明和属性、示例、输入和输出对象类型以及其他说明。
仅当计算机上安装帮助文件时，此参数才有效。 它对概念性 (About_) 帮助的显示不起作用。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | False  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
AllUsersView   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Functionality
显示具有指定功能的项的帮助。 输入功能。 允许使用通配符。 此参数对概念性 (About_) 帮助的显示不起作用。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Name
获取有关指定命令或概念的帮助。 输入 cmdlet、函数、提供程序、脚本或工作流的名称，例如 `Get-Member`、概念文章名称（如 `about_Objects`）或别名（如 `ls`）。 cmdlet 和提供程序名称中允许使用通配符，但不能使用通配符查找函数帮助和脚本帮助文章的名称。
若要获取未位于 `$Env:PATH` 环境变量中列出的路径中的脚本的帮助，请键入脚本的路径和文件名。
如果输入帮助文章的确切名称，`Get-Help` 显示文章内容。
如果输入多个帮助文章标题中显示的单词或单词模式，`Get-Help` 显示匹配标题的列表。
如果输入与任何帮助文章标题不匹配的任何文本，`Get-Help` 显示在其内容中包含该文本的文章列表。
概念性文章的名称（如 `about_Objects`）必须以英语输入，即使在非英语版本的 PowerShell 中也是如此。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | 0  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Online
在默认浏览器中显示帮助文章的联机版本。 此参数仅适用于 cmdlet、函数、工作流和脚本帮助文章。 不能在远程会话中将 **Online** 参数与 `Get-Help` 一同使用。
有关在编写的帮助文章中支持此功能的信息，请参阅 [about_Comment_Based_Help](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_comment_based_help?view=powershell-7.6)、[支持联机帮助](https://learn.microsoft.com/zh-cn/powershell/scripting/developer/module/supporting-online-help)和[为 PowerShell Cmdlet 编写帮助](https://learn.microsoft.com/zh-cn/powershell/scripting/developer/help/writing-help-for-windows-powershell-cmdlets)。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | False  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
Online   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Parameter
仅显示指定参数的详细说明。 允许使用通配符。 此参数对概念性 (About_) 帮助的显示不起作用。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
Parameters   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Path
获取说明 cmdlet 在指定的提供程序路径中的工作方式的帮助。 输入 PowerShell 提供程序路径。
此参数获取 cmdlet 帮助文章的自定义版本，该文章介绍了 cmdlet 在指定的 PowerShell 提供程序路径中的工作原理。 此参数仅适用于有关提供程序 cmdlet 的帮助，并且仅当提供程序在其帮助文件中包含提供程序 cmdlet 帮助文章的自定义版本时才有效。 若要使用此参数，请安装包含提供程序的模块的帮助文件。
若要查看提供程序路径的自定义 cmdlet 帮助，请转到提供程序路径位置并输入 `Get-Help` 命令，或者从任何路径位置使用 `Get-Help` 参数来指定提供程序路径。 还可以联机查找帮助文章的提供程序帮助部分中的自定义 cmdlet 帮助。
有关 PowerShell 提供程序的详细信息，请参阅 [about_Providers](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6)。
注释
指定路径的提供程序必须安装 PowerShell 提供程序帮助文件。 如果没有提供程序帮助文件可用，则不会返回任何帮助信息。 此版本的 PowerShell 随附的提供程序没有可用的提供程序帮助文件。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Role
显示针对指定用户角色自定义的帮助。 输入角色。 允许使用通配符。
输入用户在组织中扮演的角色。 某些 cmdlet 根据此参数的值在其帮助文件中显示不同的文本。 此参数对核心 cmdlet 的帮助不起作用。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -ShowWindow
在窗口中显示帮助主题，以便更轻松地阅读。 该窗口包括 **“查找** 搜索功能”和“**设置”** 框，用于设置显示选项，包括仅显示帮助主题选定部分的选项。
ShowWindow 参数支持命令（cmdlet、函数、CIM 命令、脚本）的帮助主题和概念性 About 主题。 它不支持提供程序帮助。
此参数在 PowerShell 7.0 中重新引入。 此参数仅在Windows可用。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | False  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
ShowWindow   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### CommonParameters
此 cmdlet 支持通用参数：-Debug、-ErrorAction、-ErrorVariable、-InformationAction、-InformationVariable、-OutBuffer、-OutVariable、-PipelineVariable、-ProgressAction、-Verbose、-WarningAction 和 -WarningVariable。 有关详细信息，请参阅 [about_CommonParameters](https://go.microsoft.com/fwlink/?LinkID=113216)。
## 输入
###  None
不能用管道将对象传送到此 cmdlet。
## 输出
###  ExtendedCmdletHelpInfo
如果在没有帮助文件的命令上运行 `Get-Help`，`Get-Help` 返回表示自动生成帮助的 **ExtendedCmdletHelpInfo** 对象。
如果收到概念帮助文章，`Get-Help` 将其作为字符串返回。
###  MamlCommandHelpInfo
如果接收到带有帮助文件的命令，`Get-Help` 返回 **MamlCommandHelpInfo** 对象。
## 备注
PowerShell 3.0 不包括帮助文件。 若要下载并安装 `Get-Help` 读取的帮助文件，请使用 `Update-Help` cmdlet。 可以使用 `Update-Help` cmdlet 下载和安装 PowerShell 附带的核心命令以及安装的任何模块的帮助文件。 还可以使用它来更新帮助文件，以便计算机上的帮助永远不会过时。
还可以从  PowerShell 入门Windows PowerShell。
可用于 `Get-Help` 按关键字或通配符模式搜索帮助文章。 `Get-Help` 显示匹配项目的列表。 如果搜索词与已批准的谓词匹配， `Get-Help` 则显示使用该谓词的命令列表。 它不包括包含匹配搜索词的其他帮助文章。 如果搜索词与批准的谓词不匹配， `Get-Help` 则显示在其内容中包含该文本的文章列表。 有关已批准的谓词的详细信息，请参阅 [Get-Verb](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.utility/get-verb?view=powershell-7.6)。
`Get-Help`在Windows操作系统的区域设置或该区域设置的回退语言中显示帮助。 如果没有主区域设置或回退区域设置的帮助文件，则 `Get-Help` 的行为将如同计算机上没有帮助文件一样。 若要获取其他区域设置的帮助，请使用 **Region** 和 **Language** 在控制面板中更改设置。 在 Windows 10 或更高版本上，Settings、Time &语言。
帮助的完整视图包括有关参数的信息的表。 该表包含以下字段：
  * **必需** 。 指示参数是必需参数（true）还是可选（false）。
  * **位置** 。 指示参数是命名还是位置（数字）。 位置参数必须出现在命令的指定位置。
  * **命名** 指示参数名称是必需的，但该参数可以在命令中的任何位置显示。
  * **Numeric** 指示参数名称是可选的，但在省略名称时，参数必须位于数字指定的位置。 例如，`2` 指示在省略参数名称时，参数必须是命令中的第二个或仅未命名的参数。 使用参数名称时，该参数可以出现在命令中的任意位置。
  * **默认值** 。 PowerShell 使用的参数值或默认行为（如果命令中不包含参数）。
  * 接受管道输入。 指示是否可以（true）或无法（false）通过管道将对象发送到参数。 “按属性名称”表示通过管道传递的对象必须具有与参数名称相同的属性。
  * **接受通配符** 。 指示参数的值是否可以包含通配符，例如星号（`*`）或问号（`?`）。


## 相关链接
  * [about_Command_Syntax](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_command_syntax?view=powershell-7.6)
  * [about_Comment_Based_Help](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_comment_based_help?view=powershell-7.6)
  * [编写针对 PowerShell Cmdlet 的帮助](https://learn.microsoft.com/zh-cn/powershell/scripting/developer/help/writing-help-for-windows-powershell-cmdlets)


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/get-help?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
