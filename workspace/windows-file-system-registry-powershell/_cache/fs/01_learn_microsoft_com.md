---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-itemproperty"
title: "Get-ItemProperty (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:26+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-itemproperty?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-itemproperty?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# Get-ItemProperty 

模块:
    [Microsoft.PowerShell.Management Module](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/?view=powershell-7.6)
获取指定项的属性。
## 语法
###  Path (默认值) 

```
Get-ItemProperty
    [-Path] <String[]>
    [[-Name] <String[]>]
    [-Filter <String>]
    [-Include <String[]>]
    [-Exclude <String[]>]
    [-Credential <PSCredential>]
    [<CommonParameters>]

```

###  LiteralPath 

```
Get-ItemProperty
    [[-Name] <String[]>]
    -LiteralPath <String[]>
    [-Filter <String>]
    [-Include <String[]>]
    [-Exclude <String[]>]
    [-Credential <PSCredential>]
    [<CommonParameters>]

```

## 说明
`Get-ItemProperty` cmdlet 获取指定项的属性。 例如，可以使用此 cmdlet 获取文件对象的 **LastAccessTime** 属性的值。 还可以使用此 cmdlet 查看注册表项及其值。
## 示例
### 示例 1：获取有关特定目录的信息
此命令获取有关 `C:\Windows` 目录的信息。

```
Get-ItemProperty C:\Windows

```

### 示例 2：获取特定文件的属性
此命令获取 `C:\Test\Weather.xls` 文件的属性。 结果通过管道传递给 `Format-List` cmdlet，以将输出显示为列表。

```
Get-ItemProperty C:\Test\Weather.xls | Format-List

```

### 示例 3：获取注册表子项中注册表项的值名称和数据
此命令获取 `ProgramFilesDir` 注册表子项中 `CurrentVersion` 注册表项的值名称和数据。 **Path** 指定子项，**Name** 参数指定项的值名称。

```
Get-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion -Name "ProgramFilesDir"

```

注释
此命令要求有一个名为 `HKLM:` 的 PowerShell 驱动器映射到注册表 `HKEY_LOCAL_MACHINE` 配置单元。
默认情况下，具有该名称和映射的驱动器在 PowerShell 中可用。 或者，可以使用以下替代路径来指定此注册表子项的路径，该路径以提供程序名称开头，后跟两个冒号：
`Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion`。
### 示例 4：获取注册表项中注册表项的值名称和数据
此命令获取 `PowerShellEngine` 注册表项中注册表项的值名称和数据。 结果显示在以下示例输出中。

```
Get-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\PowerShell\1\PowerShellEngine

```

```
ApplicationBase         : C:\Windows\system32\WindowsPowerShell\v1.0\
ConsoleHostAssemblyName : Microsoft.PowerShell.ConsoleHost, Version=1.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, ProcessorArchitecture=msil
PowerShellVersion       : 2.0
RuntimeVersion          : v2.0.50727
CTPVersion              : 5
PSCompatibleVersion     : 1.0,2.0

```

## 参数
### -Credential
注释
任何随 PowerShell 一起安装的提供程序都不支持此参数。 要模拟其他用户，或在运行此 cmdlet 时提升凭据，请使用 [Invoke-Command](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/invoke-command?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | Current user  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Exclude
指定一个或多个在操作中被此 cmdlet 排除的项目，以字符串数组的形式表示。 此参数的值定义了 **Path** 参数的限定条件。 输入路径元素或模式，例如 `*.txt`。 允许使用通配符。 仅当命令包含项（如 ）的内容（其中通配符指定 `C:\Windows\*` 目录的内容）时，`C:\Windows` 参数才有效。
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
### -Filter
指定筛选器以限定 **Path** 参数。 唯一支持使用筛选器的 PowerShell 提供程序是已安装的 [FileSystem](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6) 提供程序。 可以在 **about_Wildcards** 中找到 [FileSystem](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_wildcards?view=powershell-7.6) 筛选器语言的语法。 筛选器比其他参数更有效，因为提供程序在 cmdlet 获取对象时应用它们，而不是在检索对象后让 PowerShell 筛选对象。
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
### -Include
指定一个或多个此 cmdlet 在操作中包含的项，这些项以字符串数组形式表示。 此参数的值定义了 **Path** 参数的限定条件。 输入路径元素或模式，例如 `*.txt`。 允许使用通配符。 仅当命令包含某项的内容（例如 ，其中通配符指定 `C:\Windows\*` 目录的内容）时，`C:\Windows` 参数才有效。
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
### -LiteralPath
指定通向一个或多个位置的路径。 **LiteralPath** 的值严格按照所键入的形式使用。 不会将任何字符解释为通配符。 如果路径包含转义字符，请将它括在单引号中。 单引号告知 PowerShell 不要将任何字符解释为转义序列。
有关详细信息，请参阅 [about_Quoting_Rules](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | PSPath, LP  |  
#### 参数集
LiteralPath   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Name
指定要检索的属性的名称。 允许使用通配符。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
| 别名:  | PSProperty  |  
#### 参数集
(All)   
| Position:  | 1  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Path
指定一个或多个项的路径。 允许使用通配符。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
Path   
| Position:  | 0  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | True  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### CommonParameters
此 cmdlet 支持通用参数：-Debug、-ErrorAction、-ErrorVariable、-InformationAction、-InformationVariable、-OutBuffer、-OutVariable、-PipelineVariable、-ProgressAction、-Verbose、-WarningAction 和 -WarningVariable。 有关详细信息，请参阅 [about_CommonParameters](https://go.microsoft.com/fwlink/?LinkID=113216)。
## 输入
可以通过管道将包含路径的字符串传递给此 cmdlet。
## 输出
###  [DirectoryInfo](https://learn.microsoft.com/zh-cn/dotnet/api/system.io.directoryinfo)
此 cmdlet 返回它获取的每个项属性的对象。 对象类型取决于检索的对象。 例如，在文件系统驱动器中，它可能会返回文件或文件夹。
## 备注
PowerShell 包含以下与 `Get-ItemProperty`相关的别名：
  * 所有平台： 


`Get-ItemProperty` cmdlet 用于处理由任何提供程序公开的数据。 若要列出会话中可用的提供程序，请键入 `Get-PSProvider`。 有关详细信息，请参阅 [about_Providers](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6)。
## 相关链接
  * [Clear-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/clear-itemproperty?view=powershell-7.6)
  * [Copy-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/copy-itemproperty?view=powershell-7.6)
  * [Move-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/move-itemproperty?view=powershell-7.6)
  * [Remove-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/remove-itemproperty?view=powershell-7.6)
  * [Rename-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/rename-itemproperty?view=powershell-7.6)


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-itemproperty?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
