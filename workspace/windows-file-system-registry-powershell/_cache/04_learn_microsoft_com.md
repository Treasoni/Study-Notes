---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/update-help"
title: "Update-Help (Microsoft.PowerShell.Core) - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:04+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/update-help?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/update-help?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# Update-Help 

模块:
    [Microsoft.PowerShell.Core Module](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/?view=powershell-7.6)
在计算机上下载并安装最新的帮助文件。
## 语法
###  Path (默认值) 

```
Update-Help
    [[-Module] <String[]>]
    [[-SourcePath] <String[]>]
    [[-UICulture] <CultureInfo[]>]
    [-FullyQualifiedModule <ModuleSpecification[]>]
    [-Recurse]
    [-Credential <PSCredential>]
    [-UseDefaultCredentials]
    [-Force]
    [-Scope <UpdateHelpScope>]
    [-WhatIf]
    [-Confirm]
    [<CommonParameters>]

```

###  LiteralPath 

```
Update-Help
    [[-Module] <String[]>]
    [[-UICulture] <CultureInfo[]>]
    [-FullyQualifiedModule <ModuleSpecification[]>]
    [-LiteralPath <String[]>]
    [-Recurse]
    [-Credential <PSCredential>]
    [-UseDefaultCredentials]
    [-Force]
    [-Scope <UpdateHelpScope>]
    [-WhatIf]
    [-Confirm]
    [<CommonParameters>]

```

## 说明
`Update-Help` cmdlet 下载 PowerShell 模块的最新帮助文件，并将其安装在计算机上。 无需重启 PowerShell 才能使更改生效。 可以使用 `Get-Help` cmdlet 立即查看新的帮助文件。
`Update-Help` 检查计算机上的帮助文件版本。 如果没有模块的帮助文件或帮助文件已过时，`Update-Help` 下载最新的帮助文件。 可以从 Internet 或文件共享下载和安装帮助文件。
如果没有参数，`Update-Help` 更新支持可更新帮助的模块的帮助文件，并将其加载到会话中或安装在 `$Env:PSModulePath`中包含的位置。 有关详细信息，请参阅 [about_Updatable_Help](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_updatable_help?view=powershell-7.6)。
`Update-Help` 检查安装的帮助版本。 如果 `Update-Help` 找不到模块的更新帮助文件，则它将继续以无提示方式继续，而不会显示错误消息。 使用 **Force** 参数跳过版本检查。 使用 **详细** 参数查看状态和进度详细信息。 使用 **Module** 参数更新特定模块的帮助文件。
还可以在未连接到 Internet 的计算机上使用 `Update-Help`。 首先，使用 `Save-Help`cmdlet 从 Internet 下载帮助文件，并将其保存在无法连接到 Internet 的系统可访问的共享文件夹中。 然后使用 的 `Update-Help` 参数从共享文件下载更新的帮助文件，并将其安装在计算机上。
`Update-Help` cmdlet 是在 Windows PowerShell 3.0 中引入的。
重要
`Update-Help` 需要 PowerShell 6.0 及更低版本中的管理权限。 PowerShell 6.1 及更高版本将默认 **范围** 设置为 `CurrentUser`。 在 PowerShell 6.1 之前，**Scope** 参数不可用。
必须是计算机上的 Administrators 组的成员才能更新核心 PowerShell 模块的帮助文件。
若要下载或更新 PowerShell 安装目录中模块（`$PSHOME\Modules`）的帮助文件（包括 PowerShell Core 模块），请使用 **以管理员身份运行** 选项启动 PowerShell。 例如： `Start-Process pwsh.exe -Verb RunAs`。
## 示例
### 示例 1：更新所有模块的帮助文件
`Update-Help` cmdlet 更新支持可更新帮助的已安装模块的帮助文件。 用户界面（UI）区域性语言在操作系统中设置。

```
Update-Help

```

### 示例 2：更新指定模块的帮助文件
`Update-Help` cmdlet 仅针对以 **Microsoft.PowerShell** 开头的模块名称更新帮助文件。

```
Update-Help -Module Microsoft.PowerShell*

```

### 示例 3：更新未设置为 en-US 区域设置的系统上的帮助
`Update-Help` cmdlet 旨在下载多种语言的帮助。 但是，当系统使用的语言没有帮助时，会显示模块和 UI 区域性的错误消息。
在此示例中，`Update-Help` 在设置为 `en-GB` 区域设置的系统上运行。

```
Update-Help Microsoft.PowerShell.Utility -Force

```

```
Update-Help: Failed to update Help for the module(s) 'Microsoft.PowerShell.Utility' with
UI culture(s) {en-GB} : The specified culture is not supported: en-GB. Specify a culture
from the following list: {en-US}..
English-US help content is available and can be installed using: Update-Help -UICulture en-US.

```

始终为 `en-US` 区域设置发布帮助文件。 若要下载英语帮助，请使用 `Update-Help` 参数运行 并指定 `en-US` 区域设置。
### 示例 4：从文件共享更新多个计算机上的帮助文件
在此示例中，已更新的帮助文件将从 Internet 下载并保存在文件共享中。 需要具有访问文件共享和安装更新的权限的用户凭据。 使用文件共享时，可以更新防火墙后或未连接到 Internet 的计算机。

```
Save-Help -DestinationPath \\Server01\Share\PSHelp -Credential Domain01\Admin01
Invoke-Command -ComputerName (Get-Content Servers.txt) -ScriptBlock {
     Update-Help -SourcePath \\Server01\Share\PSHelp -Credential Domain01\Admin01
}

```

`Save-Help` 命令下载支持可更新帮助的所有模块的最新帮助文件。 **DestinationPath** 参数将文件保存在 `\\Server01\Share\PSHelp` 文件共享中。 **Credential** 参数指定有权访问文件共享的用户。
`Invoke-Command` cmdlet 在多台计算机上运行远程 `Update-Help` 命令。 **ComputerName** 参数从 **Servers.txt** 文件中获取远程计算机的列表。 **ScriptBlock** 参数运行 `Update-Help` 命令，并使用 **SourcePath** 参数指定包含更新的帮助文件的文件共享。 **Credential** 参数指定可以访问文件共享并运行远程 `Update-Help` 命令的用户。
### 示例 5：获取更新的帮助文件列表
`Update-Help` cmdlet 更新指定模块的帮助。 该 cmdlet 使用 **Verbose** 常见参数来显示已更新的帮助文件列表。 可以使用 **详细** 查看特定模块的所有帮助文件或帮助文件的输出。
如果没有 **详细** 参数，`Update-Help` 不显示命令的结果。 **详细** 参数输出可用于验证是否已更新帮助文件，或者是否安装了最新版本。

```
Update-Help -Module Microsoft.PowerShell.Utility -Verbose

```

### 示例 6：查找支持可更新帮助的模块
此示例列出了支持可更新帮助的模块。 该命令使用模块的 **HelpInfoUri** 属性来标识支持可更新帮助的模块。 **HelpInfoUri** 属性包含运行 `Update-Help` cmdlet 时重定向的 URL。

```
Get-Module -ListAvailable | Where-Object -Property HelpInfoUri

```

```
   Directory: C:\Program Files\PowerShell\6\Modules

ModuleType Version    Name                                PSEdition ExportedCommands
---------- -------    ----                                --------- ----------------
Manifest   6.1.0.0    CimCmdlets                          Core      {Get-CimAssociatedInstance... }
Manifest   1.2.2.0    Microsoft.PowerShell.Archive        Desk      {Compress-Archive... }
Manifest   6.1.0.0    Microsoft.PowerShell.Diagnostics    Core      {Get-WinEvent, New-WinEvent}

    Directory: C:\WINDOWS\system32\WindowsPowerShell\v1.0\Modules

ModuleType Version    Name                                PSEdition ExportedCommands
---------- -------    ----                                --------- ----------------
Manifest   2.0.1.0    Appx                                Core,Desk {Add-AppxPackage, ... }
Script     1.0.0.0    AssignedAccess                      Core,Desk {Clear-AssignedAccess, ... }
Manifest   1.0.0.0    BitLocker                           Core,Desk {Unlock-BitLocker, ... }

```

### 示例 7：清单更新的帮助文件
在此示例中，脚本 `Get-UpdateHelpVersion.ps1` 为每个模块及其版本号创建可更新帮助文件的清单。
该脚本使用模块的 **HelpInfoUri** 属性标识支持可更新帮助的模块。 对于支持可更新帮助的模块，脚本查找并分析帮助信息文件（*helpinfo.xml）以查找最新的版本号。
该脚本使用 **PSCustomObject** 类和哈希表创建自定义输出对象。

```
# Get-UpdateHelpVersion.ps1
param (
    [Parameter(Mandatory=$false)]
    [string[]]
    $Module
)
$HelpInfoNamespace = @{helpInfo='http://schemas.microsoft.com/powershell/help/2010/05'}

if ($Module) { $Modules = Get-Module $Module -ListAvailable | where {$_.HelpInfoUri} }
else { $Modules = Get-Module -ListAvailable | where {$_.HelpInfoUri} }

foreach ($mModule in $Modules)
{
    $mDir = $mModule.ModuleBase

    if (Test-Path $mDir\*helpinfo.xml)
    {
        $mName=$mModule.Name
        $mNodes = dir $mDir\*helpinfo.xml -ErrorAction SilentlyContinue |
            Select-Xml -Namespace $HelpInfoNamespace -XPath "//helpInfo:UICulture"
        foreach ($mNode in $mNodes)
        {
            $mCulture=$mNode.Node.UICultureName
            $mVer=$mNode.Node.UICultureVersion

            [pscustomobject]@{"ModuleName"=$mName; "Culture"=$mCulture; "Version"=$mVer}
        }
    }
}

```

```
ModuleName                              Culture                                 Version
----------                              -------                                 -------
ActiveDirectory                         en-US                                   3.0.0.0
ADCSAdministration                      en-US                                   3.0.0.0
ADCSDeployment                          en-US                                   3.0.0.0
ADDSDeployment                          en-US                                   3.0.0.0
ADFS                                    en-US                                   3.0.0.0

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
指定有权访问 **SourcePath** 指定的文件系统位置的用户的凭据。 仅当命令中使用 **SourcePath** 或 **LiteralPath** 参数时，此参数才有效。
使用 **Credential** 参数可以在远程计算机上使用 `Update-Help` 参数运行 命令。 通过提供显式凭据，可以在远程计算机上运行该命令，并在第三台计算机上访问文件共享，而不会遇到访问被拒绝错误或使用 CredSSP 身份验证委托凭据。
键入用户名（如 **User01** 或 **Domain01\User01** ），或输入由 cmdlet 生成的 `Get-Credential` 对象。 如果键入用户名，系统会提示输入密码。
凭据存储在 [PSCredential](https://learn.microsoft.com/zh-cn/dotnet/api/system.management.automation.pscredential) 对象中，密码存储为 [SecureString](https://learn.microsoft.com/zh-cn/dotnet/api/system.security.securestring)。
注释
有关 **SecureString** 数据保护的详细信息，请参阅 [SecureString 的安全性如何？](https://learn.microsoft.com/zh-cn/dotnet/fundamentals/runtime-libraries/system-security-securestring#how-secure-is-securestring)。
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
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Force
指示此 cmdlet 不遵循每天一次的限制，跳过版本检查，并下载超过 1 GB 限制的文件。
如果没有此参数，`Update-Help` 每 24 小时仅运行一次。 每个模块的下载内容限制为 1 GB 的未压缩内容，并且仅当下载文件比计算机上的现有文件更新时才安装帮助文件。
每天一次的限制可保护托管帮助文件的服务器，并使你能够将 `Update-Help` 命令添加到 PowerShell 配置文件，而不会产生重复连接或下载的资源成本。
若要在没有 **Force** 参数的情况下更新多个 UI 区域性中的模块的帮助，请将所有 UI 区域性包含在同一命令中，例如：
`Update-Help -Module PSScheduledJobs -UICulture en-US, fr-FR, pt-BR`
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
### -FullyQualifiedModule
该值可以是模块名称、完整模块规范或模块文件的路径。
如果值为路径，则路径可以完全限定或相对。 相对于包含 using 语句的脚本解析相对路径。
当该值为名称或模块规范时，PowerShell 会在 **PSModulePath** 中搜索指定的模块。
模块规范是具有以下键的哈希表。
  * `ModuleName` - **必需** 指定模块名称。
  * `GUID` - **可选** 指定模块的 GUID。
  * 它还 **必需** 指定以下三个键中的至少一个。 
    * `ModuleVersion` - 指定模块的最低可接受版本。
    * `MaximumVersion` - 指定模块的最大可接受版本。
    * `RequiredVersion` - 指定模块的确切所需版本。 这不能与其他版本密钥一起使用。


不能在与 **Module** 参数相同的命令中指定 **FullyQualifiedModule** 参数。
#### 参数属性  
| 类型:  |  [ModuleSpecification](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.powershell.commands.modulespecification)[]  |  
| --- | --- |  
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
### -LiteralPath
指定更新的帮助文件的文件夹，而不是从 Internet 下载它们。 如果使用 cmdlet 将帮助文件下载到目录，请使用此参数或 `Save-Help`。
可以将目录对象（例如从 `Get-Item` 或 `Get-ChildItem` cmdlet）管道到 `Update-Help`。
与 **SourcePath** 的值不同，**LiteralPath** 的值与类型化完全相同。 不会将任何字符解释为通配字符。 如果路径包含转义字符，请将它括在单引号中。 单引号告知 PowerShell 不要将任何字符解释为转义序列。
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
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Module
更新指定模块的帮助。 在逗号分隔的列表中输入一个或多个模块名称或名称模式，或指定一个文件，该文件在每行中列出一个模块名称。 允许使用通配符。 可以将 `Get-Module` cmdlet 中的模块管道到 `Update-Help` cmdlet。
指定的模块必须安装在计算机上，但它们不必导入到当前会话中。 可以在会话中指定任何模块，也可以指定安装在 `$Env:PSModulePath` 环境变量中列出的位置的任何模块。
`*`（所有）的值尝试更新计算机上安装的所有模块的帮助。 包含不支持可更新帮助的模块。 当命令遇到不支持可更新帮助的模块时，此值可能会生成错误。 而是在没有参数的情况下运行 `Update-Help`。
cmdlet 的 `Update-Help` 参数不接受模块文件或模块清单文件的完整路径。 若要更新不在 `$Env:PSModulePath` 位置的模块的帮助，请在运行 `Update-Help` 命令之前将模块导入当前会话。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
| 别名:  | 名称  |  
#### 参数集
(All)   
| Position:  | 0  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Recurse
对指定目录中的帮助文件执行递归搜索。 仅当命令使用 **SourcePath** 参数时，此参数才有效。
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
### -Scope
指定更新帮助的系统范围。 **AllUsers** 范围内的更新需要 Windows 系统上的管理权限。 PowerShell Core 版本 6.1 中引入了 `-Scope` 参数。
**CurrentUser** 是 PowerShell 6.1 及更高版本中帮助文件的默认范围。 **AllUsers** 可以指定为所有用户安装或更新帮助。 在 Unix 系统上，需要 `sudo` 特权来更新所有用户的帮助。 例如：`sudo pwsh -c Update-Help`
可接受的值为：
  * 当前用户
  * 所有用户


#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | CurrentUser  |  
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
### -SourcePath
指定 `Update-Help` 更新帮助文件的文件系统文件夹，而不是从 Internet 下载它们。 输入文件夹的路径。 不要指定文件名或文件扩展名。 可以将文件夹（如 `Get-Item` 或 `Get-ChildItem` cmdlet 中的文件夹）管道到 `Update-Help`。
默认情况下，`Update-Help` 从 Internet 下载更新的帮助文件。 使用 cmdlet 将更新的帮助文件下载到目录时，请使用 `Save-Help`。
若要指定 **SourcePath** 的默认值，请转到 **组策略** 、**计算机配置** ，**设置 Update-Help** 的默认源路径。 此组策略设置可防止用户使用 `Update-Help` 从 Internet 下载帮助文件。 有关详细信息，请参阅 [about_Group_Policy_Settings](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_group_policy_settings?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | 路径  |  
#### 参数集
Path   
| Position:  | 1  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -UICulture
指定此 cmdlet 更新帮助文件的 UI 区域性值。 输入一个或多个语言代码，例如 `es-ES`、包含区域性对象的变量或获取区域性对象的命令，例如 `Get-Culture` 或 `Get-UICulture` 命令。 不允许使用通配符。
默认情况下，`Update-Help` 获取作系统或其回退区域性的 UI 区域性集中的帮助文件。 如果指定 **UICulture** 参数，`Update-Help` 仅查找指定语言的帮助。
从 PowerShell 7.4 开始，可以使用部分语言代码（例如 `en`）为任何区域下载英语帮助。
注释
Ubuntu 18.04 将默认区域设置更改为 `C.UTF.8`，这是无法识别的 UI 区域性。 除非对受支持的区域设置（如 `Update-Help`）使用此参数，否则 `en-US` 无法以无提示方式下载帮助。 这可能发生在使用不受支持的值的任何平台上。
#### 参数属性  
| 类型:  |  [CultureInfo](https://learn.microsoft.com/zh-cn/dotnet/api/system.globalization.cultureinfo)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | 2  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -UseDefaultCredentials
指示 `Update-Help` 使用当前用户的凭据运行命令，包括 Internet 下载。 默认情况下，该命令在没有显式凭据的情况下运行。
仅当 Web 下载使用 NT LAN 管理器（NTLM）、协商或基于 Kerberos 的身份验证时，此参数才有效。
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
### -WhatIf
显示 cmdlet 运行时会发生什么情况。 cmdlet 未能运行。
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
###  [DirectoryInfo](https://learn.microsoft.com/zh-cn/dotnet/api/system.io.directoryinfo)
可以通过管道将目录路径对象传递给此 cmdlet。
###  [PSModuleInfo](https://learn.microsoft.com/zh-cn/dotnet/api/system.management.automation.psmoduleinfo)
可以通过管道将模块对象传递给此 cmdlet。
## 输出
###  None
此 cmdlet 不返回任何输出。
## 备注
若要更新核心 PowerShell 模块的帮助，其中包含随 PowerShell 一起安装的命令或 `$PSHOME\Modules` 目录中的任何模块，请使用 **以管理员身份** 运行的选项启动 PowerShell。
只有计算机上的 Administrators 组成员可以更新核心 PowerShell 模块、与 PowerShell 一起安装的命令以及 `$PSHOME\Modules` 文件夹中的模块的帮助。 如果没有更新帮助文件的权限，则可以联机阅读帮助文件。 例如，`Get-Help Update-Help -Online`。
模块是可更新帮助的最小单元。 无法更新特定 cmdlet 的帮助。 若要查找包含特定 cmdlet 的模块，请使用 cmdlet 的 `Get-Command` 属性，例如 `(Get-Command Update-Help).ModuleName`。
由于帮助文件安装在模块目录中，`Update-Help` cmdlet 只能为计算机上安装的模块安装更新的帮助文件。 但是，`Save-Help` cmdlet 可以为计算机上未安装的模块保存帮助。
`Update-Help` cmdlet 是在 Windows PowerShell 3.0 中引入的。 它在早期版本的 PowerShell 中不起作用。 在同时具有 Windows PowerShell 2.0 和 Windows PowerShell 3.0 的计算机上，使用 Windows PowerShell 3.0 会话中的 `Update-Help` cmdlet 下载和更新帮助文件。 帮助文件适用于 Windows PowerShell 2.0 和 Windows PowerShell 3.0。
`Update-Help` 和 `Save-Help` cmdlet 使用以下端口下载帮助文件：HTTP 端口 80 和 HTTPS 端口 443。
`Update-Help` 支持所有模块和核心 PowerShell 管理单元。它不支持任何其他管理单元。
若要更新 `$Env:PSModulePath` 环境变量中未列出的某个模块的帮助，请将模块导入当前会话，然后运行 `Update-Help` 命令。 在没有参数的情况下运行 `Update-Help` 或使用 **Module** 参数指定模块名称。 和 `Update-Help` cmdlet 的 `Save-Help` 参数不接受模块文件或模块清单文件的完整路径。
任何模块都可以支持可更新的帮助。 有关在创作的模块中支持可更新帮助的说明，请参阅 [支持可更新帮助](https://learn.microsoft.com/zh-cn/powershell/scripting/developer/module/supporting-updatable-help)。
Windows 预安装环境（Windows PE）不支持 `Update-Help` 和 `Save-Help` cmdlet。
## 相关链接


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/update-help?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
