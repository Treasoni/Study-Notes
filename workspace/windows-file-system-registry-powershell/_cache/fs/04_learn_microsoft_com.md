---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-itemproperty"
title: "Set-ItemProperty (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:26+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-itemproperty?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-itemproperty?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# Set-ItemProperty 

模块:
    [Microsoft.PowerShell.Management Module](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/?view=powershell-7.6)
创建或更改项的属性的值。
## 语法
###  propertyValuePathSet (Default) - All providers 

```
Set-ItemProperty
    [-Path] <string[]>
    [-Name] <string>
    [-Value] <Object>
    [-PassThru]
    [-Force]
    [-Filter <string>]
    [-Include <string[]>]
    [-Exclude <string[]>]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [<CommonParameters>]

```

###  propertyPSObjectPathSet - All providers 

```
Set-ItemProperty
    [-Path] <string[]>
    -InputObject <psobject>
    [-PassThru]
    [-Force]
    [-Filter <string>]
    [-Include <string[]>]
    [-Exclude <string[]>]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [<CommonParameters>]

```

###  propertyValueLiteralPathSet - All providers 

```
Set-ItemProperty
    [-Name] <string>
    [-Value] <Object>
    -LiteralPath <string[]>
    [-PassThru]
    [-Force]
    [-Filter <string>]
    [-Include <string[]>]
    [-Exclude <string[]>]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [<CommonParameters>]

```

###  propertyPSObjectLiteralPathSet - All providers 

```
Set-ItemProperty
    -LiteralPath <string[]>
    -InputObject <psobject>
    [-PassThru]
    [-Force]
    [-Filter <string>]
    [-Include <string[]>]
    [-Exclude <string[]>]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [<CommonParameters>]

```

###  propertyValuePathSet (Default) - Registry provider 

```
Set-ItemProperty
    [-Path] <string[]>
    [-Name] <string>
    [-Value] <Object>
    [-PassThru]
    [-Force]
    [-Filter <string>]
    [-Include <string[]>]
    [-Exclude <string[]>]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [-Type <RegistryValueKind>]
    [<CommonParameters>]

```

###  propertyPSObjectPathSet - Registry provider 

```
Set-ItemProperty
    [-Path] <string[]>
    -InputObject <psobject>
    [-PassThru]
    [-Force]
    [-Filter <string>]
    [-Include <string[]>]
    [-Exclude <string[]>]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [-Type <RegistryValueKind>]
    [<CommonParameters>]

```

###  propertyValueLiteralPathSet - Registry provider 

```
Set-ItemProperty
    [-Name] <string>
    [-Value] <Object>
    -LiteralPath <string[]>
    [-PassThru]
    [-Force]
    [-Filter <string>]
    [-Include <string[]>]
    [-Exclude <string[]>]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [-Type <RegistryValueKind>]
    [<CommonParameters>]

```

###  propertyPSObjectLiteralPathSet - Registry provider 

```
Set-ItemProperty
    -LiteralPath <string[]>
    -InputObject <psobject>
    [-PassThru]
    [-Force]
    [-Filter <string>]
    [-Include <string[]>]
    [-Exclude <string[]>]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [-Type <RegistryValueKind>]
    [<CommonParameters>]

```

## 说明
`Set-ItemProperty` cmdlet 更改指定项的属性的值。 可以使用 cmdlet 来建立或更改项的属性。 例如，可以使用 `Set-ItemProperty` 将文件对象的 **IsReadOnly** 属性的值设置为 `$true`。
还可以使用 `Set-ItemProperty` 创建和更改注册表值和数据。 例如，可以将新的注册表项添加到某个键，并建立或更改其值。
## 示例
### 示例 1：设置文件的属性
此命令将“final.doc”文件的 **IsReadOnly** 属性的值设置为“true”。 它使用 **Path** 来指定文件，**Name** 指定属性的名称，**Value** 参数指定新值。
该文件是 **System.IO.FileInfo** 对象，**IsReadOnly** 只是其属性之一。 若要查看所有属性，请键入 `Get-Item C:\GroupFiles\final.doc | Get-Member -MemberType Property`。
`$true` 自动变量表示值为“TRUE”。 有关详细信息，请参阅 [about_Automatic_Variables](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_automatic_variables?view=powershell-7.6)。

```
Set-ItemProperty -Path C:\GroupFiles\final.doc -Name IsReadOnly -Value $true

```

### 示例 2：创建注册表项和值
此示例演示如何使用 `Set-ItemProperty` 创建新的注册表项，并为该条目分配值。 它在 `HKLM\Software` 键的“ContosoCompany”键中创建“NoOfEmployees”条目，并将其值设置为 823。
由于注册表项被视为注册表项的属性（即项），因此使用 `Set-ItemProperty` 创建注册表项，以及建立和更改其值。

```
Set-ItemProperty -Path "HKLM:\Software\ContosoCompany" -Name "NoOfEmployees" -Value 823
Get-ItemProperty -Path "HKLM:\Software\ContosoCompany"

```

```
PSPath        : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\software\contosocompany
PSParentPath  : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\software
PSChildName   : contosocompany
PSDrive       : HKLM
PSProvider    : Microsoft.PowerShell.Core\Registry
NoOfLocations : 2
NoOfEmployees : 823

```

```
Set-ItemProperty -Path "HKLM:\Software\ContosoCompany" -Name "NoOfEmployees" -Value 824
Get-ItemProperty -Path "HKLM:\Software\ContosoCompany"

```

```
PSPath        : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\software\contosocompany
PSParentPath  : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\software
PSChildName   : contosocompany
PSDrive       : HKLM
PSProvider    : Microsoft.PowerShell.Core\Registry
NoOfLocations : 2
NoOfEmployees : 824

```

第一个命令创建注册表项。 它使用 **Path** 来指定 `HKLM:` 驱动器的路径和 `Software\MyCompany` 键。 该命令使用 **名称** 指定条目名称和 **值** 指定值。
第二个命令使用 `Get-ItemProperty` cmdlet 查看新的注册表项。 如果使用 `Get-Item` 或 `Get-ChildItem` cmdlet，则不会显示这些条目，因为它们是键的属性，而不是项或子项。
第三个命令将 **NoOfEmployees** 条目的值更改为 824。
还可以使用 `New-ItemProperty` cmdlet 创建注册表项及其值，然后使用 `Set-ItemProperty` 更改值。
有关 `HKLM:` 驱动器的详细信息，请键入 `Get-Help Get-PSDrive`。 有关如何使用 PowerShell 管理注册表的详细信息，请键入 `Get-Help Registry`。
### 示例 3：使用管道修改项
该示例使用 `Get-ChildItem` 来获取 `weekly.txt` 文件。 文件对象通过管道传递给 `Set-ItemProperty`。 `Set-ItemProperty` 命令使用 **Name** 和 **Value** 参数来指定属性及其新值。

```
Get-ChildItem weekly.txt | Set-ItemProperty -Name IsReadOnly -Value $true

```

## 参数
### -Confirm
在运行 cmdlet 之前，提示你进行确认。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | False  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | cf  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
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
### -Force
强制 cmdlet 对用户无法访问的项设置属性。 实现因提供程序而异。 有关详细信息，请参阅 [about_Providers](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | False  |  
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
### -Include
指定一个或多个此 cmdlet 在操作中包含的项，这些项以字符串数组形式表示。 此参数的值定义了 **Path** 参数的限定条件。 输入路径元素或模式，例如 `"*.txt"`。 允许使用通配符。 仅当命令包含某项的内容（例如 ，其中通配符指定 `C:\Windows\*` 目录的内容）时，`C:\Windows` 参数才有效。
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
### -InputObject
指定具有此 cmdlet 更改的属性的对象。 输入包含对象或获取对象的命令的变量。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
propertyPSObjectPathSet   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | True  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
propertyPSObjectLiteralPathSet   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | True  |  
| 来自管道的值（按属性名称）:  | True  |  
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
propertyValueLiteralPathSet   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
propertyPSObjectLiteralPathSet   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Name
指定属性的名称。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | PSProperty  |  
#### 参数集
propertyValuePathSet   
| Position:  | 1  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
propertyValueLiteralPathSet   
| Position:  | 1  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -PassThru
返回一个表示项属性的对象。 默认情况下，此 cmdlet 不生成任何输出。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
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
### -Path
指定要修改的属性的项的路径。 允许使用通配符。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
propertyValuePathSet   
| Position:  | 0  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
propertyPSObjectPathSet   
| Position:  | 0  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Type
这是 Registry 提供程序提供的动态参数。 Registry 提供程序和此参数仅在 Windows 上可用。
指定此 cmdlet 添加的属性的类型。 此参数的可接受值为：
  * `String`：指定以 null 结尾的字符串。 用于 REG_SZ 值。
  * `ExpandString`：指定一个以空字符结尾的字符串，该字符串包含尚未展开的环境变量引用，这些引用在检索值时进行展开。 用于 REG_EXPAND_SZ 值。
  * `Binary`：指定任何形式的二进制数据。 用于 REG_BINARY 值。
  * `DWord`：指定 32 位二进制数。 用于 REG_DWORD 值。
  * `MultiString`：指定一个由 null 终止并以两个空字符结尾的字符串数组。 用于 REG_MULTI_SZ 值。
  * `Qword`：指定 64 位二进制数。 用于 REG_QWORD 值。
  * `Unknown`：指示不支持的注册表数据类型，例如 **REG_RESOURCE_LIST** 值。


#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
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
### -Value
指定属性的值。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
propertyValuePathSet   
| Position:  | 2  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
propertyValueLiteralPathSet   
| Position:  | 2  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -WhatIf
显示 cmdlet 运行时会发生什么情况。 命令脚本未运行。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | False  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | 无线  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### CommonParameters
此 cmdlet 支持通用参数：-Debug、-ErrorAction、-ErrorVariable、-InformationAction、-InformationVariable、-OutBuffer、-OutVariable、-PipelineVariable、-ProgressAction、-Verbose、-WarningAction 和 -WarningVariable。 有关详细信息，请参阅 [about_CommonParameters](https://go.microsoft.com/fwlink/?LinkID=113216)。
## 输入
可以通过管道将对象传递给此 cmdlet。
## 输出
###  None
默认情况下，此 cmdlet 不返回任何输出。
###  [PSCustomObject](https://learn.microsoft.com/zh-cn/dotnet/api/system.management.automation.pscustomobject)
使用 **PassThru** 参数时，此 cmdlet 返回一个 **PSCustomObject** 对象，该对象表示已更改的项及其新属性值。
## 备注
PowerShell 包含以下与 `Set-ItemProperty`相关的别名：
  * 所有平台： 


`Set-ItemProperty` 被设计用于处理任何供应商公开的数据。 若要列出会话中可用的提供程序，请键入 `Get-PSProvider`。 有关详细信息，请参阅 [about_Providers](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6)。
## 相关链接
  * [Clear-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/clear-itemproperty?view=powershell-7.6)
  * [Copy-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/copy-itemproperty?view=powershell-7.6)
  * [Move-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/move-itemproperty?view=powershell-7.6)
  * [Remove-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/remove-itemproperty?view=powershell-7.6)
  * [Rename-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/rename-itemproperty?view=powershell-7.6)


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-itemproperty?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
