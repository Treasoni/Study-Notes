---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/new-item"
title: "New-Item (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:26+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/new-item?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/new-item?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# New-Item 

模块:
    [Microsoft.PowerShell.Management Module](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/?view=powershell-7.6)
创建新项。
## 语法
###  pathSet (Default) - All providers 

```
New-Item
    [-Path] <String[]>
    [-ItemType <String>]
    [-Value <Object>]
    [-Force]
    [-Credential <PSCredential>]
    [-WhatIf]
    [-Confirm]
    [<CommonParameters>]

```

###  nameSet - All providers 

```
New-Item
    [[-Path] <String[]>]
    -Name <String>
    [-ItemType <String>]
    [-Value <Object>]
    [-Force]
    [-Credential <PSCredential>]
    [-WhatIf]
    [-Confirm]
    [<CommonParameters>]

```

###  pathSet (Default) - WSMan provider 

```
New-Item
    [-Path] <string[]>
    -ConnectionURI <uri>
    [-ItemType <string>]
    [-Value <Object>]
    [-Force]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [-OptionSet <hashtable>]
    [-Authentication <AuthenticationMechanism>]
    [-CertificateThumbprint <string>]
    [-SessionOption <SessionOption>]
    [-Port <int>]
    [<CommonParameters>]

```

###  nameSet - WSMan provider 

```
New-Item
    [[-Path] <string[]>]
    -Name <string>
    [-ItemType <string>]
    [-Value <Object>]
    [-Force]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [-OptionSet <hashtable>]
    [-Authentication <AuthenticationMechanism>]
    [-CertificateThumbprint <string>]
    [-SessionOption <SessionOption>]
    [-ApplicationName <string>]
    [-Port <int>]
    [-UseSSL]
    [<CommonParameters>]

```

###  pathSet (Default) - Alias provider 

```
New-Item
    [-Path] <string[]>
    [-ItemType <string>]
    [-Value <Object>]
    [-Force]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [-Options <ScopedItemOptions>]
    [<CommonParameters>]

```

###  nameSet - Alias provider 

```
New-Item
    [[-Path] <string[]>]
    -Name <string>
    [-ItemType <string>]
    [-Value <Object>]
    [-Force]
    [-Credential <pscredential>]
    [-WhatIf]
    [-Confirm]
    [-Options <ScopedItemOptions>]
    [<CommonParameters>]

```

## 说明
`New-Item` cmdlet 将创建新项并设置其值。 可以创建的项的类型取决于项的位置。 例如，在文件系统中，`New-Item` 创建文件和文件夹。 在注册表中，`New-Item` 创建注册表项和条目。
`New-Item` 还可以设置其创建的项的值。 例如，创建新文件时，`New-Item` 可以将初始内容添加到该文件。
## 示例
### 示例 1：在当前目录中创建文件
此命令在当前目录中创建名为“testfile1.txt”的文本文件。 **Path** 参数的值中的点 （'.'） 指示当前目录。 **Value** 参数后面的带引号的文本作为内容添加到文件中。

```
New-Item -Path . -Name "testfile1.txt" -ItemType "File" -Value "This is a text string."

```

### 示例 2：创建目录
此命令在 `C:` 驱动器中创建名为“Logfiles”的目录。 **ItemType** 参数指定新项是目录，而不是文件或其他文件系统对象。

```
New-Item -Path "C:\" -Name "Logfiles" -ItemType "Directory"

```

### 示例 3：创建配置文件
此命令在 `$PROFILE` 变量指定的路径中创建 PowerShell 配置文件。
可以使用配置文件自定义 PowerShell。 `$PROFILE` 是一个自动（内置）变量，用于存储“CurrentUser/CurrentHost”配置文件的路径和文件名。 默认情况下，即使 PowerShell 存储路径和文件名，配置文件也不存在。
在此命令中，`$PROFILE` 变量表示文件的路径。 **ItemType** 参数指定命令创建文件。 **Force** 参数允许在配置文件路径中创建文件，即使路径中的目录不存在也是如此。
创建配置文件后，可以在配置文件中输入别名、函数和脚本来自定义 shell。
有关详细信息，请参阅 [about_Automatic_Variables](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_automatic_variables?view=powershell-7.6) 和 [about_Profiles](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-7.6)。

```
New-Item -Path $PROFILE -ItemType "File" -Force

```

### 示例 4：在不同的目录中创建目录
此示例在“C：\PS-Test”目录中创建新的脚本目录。
新目录项“Scripts”的名称包含在 **Path** 参数的值中，而不是在 **Name** 的值中指定。 如语法所示，任一命令形式都有效。

```
New-Item -ItemType "Directory" -Path "C:\ps-test\scripts"

```

### 示例 5：创建多个文件
此示例在两个不同的目录中创建文件。 由于 **Path** 需要多个字符串，因此可以使用它来创建多个项。

```
New-Item -ItemType "File" -Path "C:\ps-test\test.txt", "C:\ps-test\Logs\test.log"

```

### 示例 6：使用通配符在多个目录中创建文件
`New-Item` cmdlet 支持 **Path** 参数中的通配符。 以下命令在 `temp.txt` 参数中通配符指定的所有目录中创建 文件。

```
Get-ChildItem -Path C:\Temp\

```

```
    Directory:  C:\Temp

Mode                LastWriteTime     Length Name
----                -------------     ------ ----
d-----        5/15/2019   6:45 AM        1   One
d-----        5/15/2019   6:45 AM        1   Two
d-----        5/15/2019   6:45 AM        1   Three

```

```
New-Item -Path C:\Temp\* -Name temp.txt -ItemType File | Select-Object FullName

```

```
FullName
--------
C:\Temp\One\temp.txt
C:\Temp\Three\temp.txt
C:\Temp\Two\temp.txt

```

`Get-ChildItem` cmdlet 显示 `C:\Temp` 目录下的三个目录。 使用通配符，`New-Item` cmdlet 会在当前目录下的所有目录中创建 `temp.txt` 文件。 `New-Item` cmdlet 输出所创建的项，这些项通过管道传递给 `Select-Object` 来验证新创建文件的路径。
### 示例 7：创建指向文件或文件夹的符号链接
此示例创建指向 `Notice.txt` 当前文件夹中文件的符号链接。

```
$link = New-Item -ItemType SymbolicLink -Path .\link -Target .\Notice.txt
$link | Select-Object LinkType, Target

```

```
LinkType     Target
--------     ------
SymbolicLink {.\Notice.txt}

```

在此示例中， **Target** 是 **Value** 参数的别名。 符号链接的目标可以是相对路径。 在 PowerShell v6.2 之前，目标必须是完全限定的路径。
从 PowerShell 7.1 开始，现在可以使用相对路径创建到 Windows 上的文件夹 **SymbolicLink** 。
### 示例 8：使用 -Force 参数尝试重新创建文件夹
此示例创建一个文件夹，其中包含一个文件。 然后，尝试使用 `-Force`创建同一文件夹。 它不会覆盖该文件夹，而只是返回现有文件夹对象，该文件创建完好无损。

```
PS> New-Item -Path .\TestFolder -ItemType Directory
PS> New-Item -Path .\TestFolder\TestFile.txt -ItemType File

PS> New-Item -Path .\TestFolder -ItemType Directory -Force

    Directory: C:\
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         5/1/2020   8:03 AM                TestFolder

PS> Get-ChildItem .\TestFolder\

    Directory: C:\TestFolder
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         5/1/2020   8:03 AM              0 TestFile.txt

```

### 示例 9：使用 -Force 参数覆盖现有文件
此示例使用值创建一个文件，然后使用 `-Force`重新创建该文件。 这会覆盖现有文件，如 **Length** 属性所示。

```
PS> New-Item ./TestFile.txt -ItemType File -Value 'This is just a test file'

    Directory: C:\Source\Test
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         5/1/2020   8:32 AM             24 TestFile.txt

New-Item ./TestFile.txt -ItemType File -Force

    Directory: C:\Source\Test
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         5/1/2020   8:32 AM              0 TestFile.txt

```

注释
将 `New-Item` 与 **Force** 参数一起使用以创建注册表项时，该命令的行为与覆盖文件时的行为相同。 如果注册表项已存在，则密钥和所有属性和值都会被空注册表项覆盖。
## 参数
### -ApplicationName
这是由 **WSMan** 提供程序提供的动态参数。 **WSMan** 提供程序，此参数仅在 Windows 上可用。
指定连接中的应用程序名称。 **ApplicationName** 参数的默认值 **WSMAN** 。
有关详细信息，请参阅 [New-WSManInstance](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.wsman.management/new-wsmaninstance?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
nameSet   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Authentication
这是由 **WSMan** 提供程序提供的动态参数。 **WSMan** 提供程序，此参数仅在 Windows 上可用。
指定要在服务器上使用的身份验证机制。
有关详细信息，请参阅 [New-WSManInstance](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.wsman.management/new-wsmaninstance?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  [AuthenticationMechanism](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.wsman.management.authenticationmechanism)  |  
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
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -CertificateThumbprint
这是由 **WSMan** 提供程序提供的动态参数。 **WSMan** 提供程序，此参数仅在 Windows 上可用。
指定有权执行此 WSMan作的用户帐户的数字公钥证书（X509）。 输入证书的证书指纹。
有关详细信息，请参阅 [New-WSManInstance](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.wsman.management/new-wsmaninstance?view=powershell-7.6)。
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
### -ConnectionURI
这是由 **WSMan** 提供程序提供的动态参数。 **WSMan** 提供程序，此参数仅在 Windows 上可用。
指定 WSMan 的连接终结点。
有关详细信息，请参阅 [New-WSManInstance](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.wsman.management/new-wsmaninstance?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
pathSet   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Credential
注释
任何随 PowerShell 一起安装的提供程序都不支持此参数。 若要模拟其他用户或在运行此 cmdlet 时提升凭据，请使用 `Invoke-Command`。
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
### -Force
强制此 cmdlet 创建写入现有只读项的项。 实现因服务提供商而异。 即使使用 **Force** 参数，cmdlet 也不能替代安全限制。
从 PowerShell 7.4 开始，此参数还允许覆盖现有交接点。 以前，此作会失败，出现“无法删除，因为它不为空”错误。
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
### -ItemType
指定新项的提供程序指定类型。 此参数的可用值取决于所使用的当前提供程序。
如果位置位于 `FileSystem` 驱动器中，则允许以下值：
  * `File`
  * `Directory`
  * `SymbolicLink`
  * `Junction`
  * `HardLink`


注释
在 Windows 上创建 `SymbolicLink` 类型需要以管理员身份提升。 但是，启用了开发人员模式的 Windows 10（内部版本 14972 或更高版本）不再需要提升创建符号链接。
在 `Certificate` 驱动器中，可以指定以下值：
  * `Certificate Provider`
  * `Certificate`
  * `Store`
  * `StoreLocation`


有关详细信息，请参阅 [about_Providers](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | 类型  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Name
指定新项的名称。 可以在 **名称** 或 **Path** 参数值中指定新项的名称，并且可以在 **Name** 或 **Path** 值中指定新项的路径。 使用 **Name** 参数传递的项名称相对于 **Path** 参数的值创建。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
nameSet   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Options
这是 **别名** 提供程序提供的动态参数。 有关详细信息，请参阅 [New-Alias](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.utility/new-alias?view=powershell-7.6)。
指定别名的 **Options** 属性的值。
有效值为：
  * `None`：别名没有约束（默认值）
  * `ReadOnly`：别名可以删除，但除非使用 **Force** 参数，否则无法更改。
  * `Constant`：无法删除或更改别名
  * `Private`：别名仅在当前范围内可用
  * `AllScope`：别名复制到任何创建的新作用域。
  * `Unspecified`：未指定选项


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
### -OptionSet
这是由 **WSMan** 提供程序提供的动态参数。 **WSMan** 提供程序，此参数仅在 Windows 上可用。
将一组开关传递给服务，以修改或优化请求的性质。
有关详细信息，请参阅 [New-WSManInstance](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.wsman.management/new-wsmaninstance?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | 操作系统  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Path
指定新项的位置的路径。 当省略 **路径** 时，默认值为当前位置。 可以在 **名称** 中指定新项的名称，或将其包含在 **Path** 中。 使用 **Name** 参数传递的项名称相对于 **Path** 参数的值创建。
对于此 cmdlet，**Path** 参数的工作方式类似于其他 cmdlet 的 **LiteralPath** 参数。 不解释通配符。 所有字符都传递给位置的提供程序。 提供程序可能不支持所有字符。 例如，无法创建包含星号（`*`）字符的文件名。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | Current location  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
pathSet   
| Position:  | 0  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
nameSet   
| Position:  | 0  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Port
这是由 **WSMan** 提供程序提供的动态参数。 **WSMan** 提供程序，此参数仅在 Windows 上可用。
指定客户端连接到 WinRM 服务时要使用的端口。
有关详细信息，请参阅 [New-WSManInstance](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.wsman.management/new-wsmaninstance?view=powershell-7.6)。
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
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -SessionOption
这是由 **WSMan** 提供程序提供的动态参数。 **WSMan** 提供程序，此参数仅在 Windows 上可用。
定义 WS-Management 会话的一组扩展选项。
有关详细信息，请参阅 [New-WSManInstance](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.wsman.management/new-wsmaninstance?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | 所以  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -UseSSL
这是由 **WSMan** 提供程序提供的动态参数。 **WSMan** 提供程序，此参数仅在 Windows 上可用。
指定应使用安全套接字层 （SSL） 协议建立与远程计算机的连接。 默认情况下，不使用 SSL。
有关详细信息，请参阅 [New-WSManInstance](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.wsman.management/new-wsmaninstance?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
nameSet   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Value
指定新项的值。 还可以通过管道将值传递给 `New-Item`。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | Target  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | True  |  
| 来自管道的值（按属性名称）:  | True  |  
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
可以将新项的值通过管道传递给此 cmdlet。
## 输出
###  [DictionaryEntry](https://learn.microsoft.com/zh-cn/dotnet/api/system.collections.dictionaryentry)
该 cmdlet 在创建新环境变量时返回 **DictionaryEntry** 对象。
###  [DirectoryInfo](https://learn.microsoft.com/zh-cn/dotnet/api/system.io.directoryinfo)
该 cmdlet 在文件系统中创建新目录时返回 **DirectoryInfo** 对象。
该 cmdlet 在文件系统中创建新文件时返回 **FileInfo** 对象。
该 cmdlet 在创建新别名时返回 **AliasInfo** 对象。
###  [FunctionInfo](https://learn.microsoft.com/zh-cn/dotnet/api/system.management.automation.functioninfo)
该 cmdlet 在创建新函数时返回 **FunctionInfo** 对象。
###  [PSVariable](https://learn.microsoft.com/zh-cn/dotnet/api/system.management.automation.psvariable)
该 cmdlet 在创建新变量时返回 **PSVariable** 对象。
## 备注
PowerShell 包含以下与 `New-Item`相关的别名：
  * 所有平台： 


`New-Item` 被设计用于处理任何供应商公开的数据。 若要列出会话中可用的提供程序，请键入 `Get-PSProvider`。 有关详细信息，请参阅 [about_Providers](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6)。
## 相关链接


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/new-item?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
