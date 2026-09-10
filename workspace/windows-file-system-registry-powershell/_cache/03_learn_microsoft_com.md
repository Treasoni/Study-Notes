---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-location"
title: "Set-Location (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:04+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# Set-Location 

模块:
    [Microsoft.PowerShell.Management Module](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/?view=powershell-7.6)
将当前工作位置设置为指定位置。
## 语法
###  Path (默认值) 

```
Set-Location
    [[-Path] <String>]
    [-PassThru]
    [<CommonParameters>]

```

###  LiteralPath 

```
Set-Location
    -LiteralPath <String>
    [-PassThru]
    [<CommonParameters>]

```

###  Stack 

```
Set-Location
    [-PassThru]
    [-StackName <String>]
    [<CommonParameters>]

```

## 说明
`Set-Location` cmdlet 将工作位置设置为指定位置。 该位置可以是目录、子目录、注册表位置或任何提供程序路径。
PowerShell 6.2 添加了对 `-` 和 `+` 的支持，作为 **Path** 参数的值。 PowerShell 维护可以使用 `-` 和 `+`访问的最后 20 个位置的历史记录。 此列表独立于使用 **StackName** 参数访问的位置堆栈。
## 示例
### 示例 1：设置当前位置

```
PS C:\> Set-Location -Path "HKLM:\"
PS HKLM:\>

```

此命令将当前位置设置为 `HKLM:` 驱动器的根目录。
### 示例 2：设置当前位置并显示该位置

```
PS C:\> Set-Location -Path "Env:\" -PassThru

```

```
Path
----
Env:\

PS Env:\>

```

此命令将当前位置设置为 `Env:` 驱动器的根目录。 它使用 **PassThru** 参数指示 PowerShell 返回表示 位置的 `Env:\` 对象。
### 示例 3：将位置设置为 C： 驱动器中的当前位置

```
PS C:\Windows\> Set-Location HKLM:\
PS HKLM:\> Set-Location C:
PS C:\Windows\>

```

第一个命令将位置设置为注册表提供程序中 `HKLM:` 驱动器的根目录。 第二个命令将位置设置为 FileSystem 提供程序中 `C:` 驱动器的当前位置。 当驱动器名称在窗体 `<DriveName>:`（没有反斜杠）中指定时，cmdlet 会将位置设置为 PSDrive 中的当前位置。 若要获取 PSDrive 中的当前位置，请使用 `Get-Location -PSDrive <DriveName>` 命令。
### 示例 4：将当前位置设置为命名堆栈

```
PS C:\> Push-Location -Path 'C:\Program Files\PowerShell\' -StackName "Paths"
PS C:\Program Files\PowerShell\> Set-Location -StackName "Paths"
PS C:\Program Files\PowerShell\> Get-Location -Stack

```

```
Path
----
C:\

```

第一个命令将当前位置添加到“路径”堆栈。 第二个命令使路径位置堆栈成为当前位置堆栈。 第三个命令显示当前位置堆栈中的位置。
`*-Location` cmdlet 使用当前位置堆栈，除非命令中指定了其他位置堆栈。 有关位置堆栈的信息，请参阅 [备注](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.6#notes)。
### 示例 5：使用“+”或“-”导航位置历史记录

```
PS C:\> Set-Location -Path $Env:SystemRoot
PS C:\Windows> Set-Location -Path Cert:\
PS Cert:\> Set-Location -Path HKLM:\
PS HKLM:\>

# Navigate back through the history using "-"
PS HKLM:\> Set-Location -Path -
PS Cert:\> Set-Location -Path -
PS C:\Windows>

# Navigate using the Set-Location alias "cd" and the implicit positional Path parameter
PS C:\Windows> cd -
PS C:\> cd +
PS C:\Windows> cd +
PS Cert:\>

```

使用别名、`cd -` 或 `cd +` 是一种在终端中浏览位置历史记录的简单方法。 有关使用 `-`/`+`导航的详细信息，请参阅 **Path** 参数。
## 参数
### -LiteralPath
指定位置的路径。 **LiteralPath** 参数的值与类型完全相同。 不会将任何字符解释为通配字符。 如果路径包含转义字符，请将它括在单引号中。 单引号告知 PowerShell 不要将任何字符解释为转义序列。
#### 参数属性  
| 类型:  |  
| --- |  
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
### -PassThru
返回一个 **PathInfo** 对象，该对象代表位置。 默认情况下，此 cmdlet 不生成任何输出。
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
### -Path
指定新工作位置的路径。 如果未提供路径，`Set-Location` 默认为当前用户的主目录。 使用通配符时，cmdlet 会选择与通配符模式匹配的容器（目录、注册表项、证书存储）。 如果通配符模式与多个容器匹配，则 cmdlet 将返回错误。
PowerShell 保留你设置的最后 20 个位置的历史记录。 如果 **Path** 参数值是 `-` 字符，则新工作位置将是历史记录中以前的工作位置（如果存在）。 同样，如果值为 `+` 字符，则新的工作位置将是历史记录中的下一个工作位置（如果存在）。 这类似于使用 `Pop-Location` 和 `Push-Location`，只是历史记录是列表，而不是堆栈，并且是隐式跟踪的，而不是手动控制的。 无法查看历史记录列表。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
Path   
| Position:  | 0  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | True  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -StackName
指定此 cmdlet 生成当前位置堆栈的现有位置堆栈名称。 输入位置堆栈名称。 若要指示未命名的默认位置堆栈，请键入 `$null` 或空字符串（`""`）。
使用此参数不会更改当前位置。 它仅更改 `*-Location` cmdlet 使用的堆栈。 除非使用 `*-Location` 参数来指定其他堆栈，否则 cmdlet 在当前堆栈上执行操作。 有关位置堆栈的详细信息，请参阅 [备注](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.6#notes)。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
Stack   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### CommonParameters
此 cmdlet 支持通用参数：-Debug、-ErrorAction、-ErrorVariable、-InformationAction、-InformationVariable、-OutBuffer、-OutVariable、-PipelineVariable、-ProgressAction、-Verbose、-WarningAction 和 -WarningVariable。 有关详细信息，请参阅 [about_CommonParameters](https://go.microsoft.com/fwlink/?LinkID=113216)。
## 输入
可以通过管道将包含路径（但不是文本路径）的字符串传递给此 cmdlet。
## 输出
###  None
默认情况下，此 cmdlet 不返回任何输出。
将 **PassThru** 参数与 **Path** 或 **LiteralPath** 配合使用时，此 cmdlet 将返回表示新位置的 **PathInfo** 对象。
###  [PathInfoStack](https://learn.microsoft.com/zh-cn/dotnet/api/system.management.automation.pathinfostack)
将 **PassThru** 参数用于 **StackName** 时，此 cmdlet 将返回表示新堆栈上下文的 **PathInfoStack** 对象。
## 备注
PowerShell 包含以下与 `Set-Location`相关的别名：
  * 所有平台：
    * `chdir`


PowerShell 支持每个进程的多个运行空间。 每个 runspace 都有其独立的 _当前目录_ 。 这与 `[System.Environment]::CurrentDirectory`不同。 调用 .NET API 或运行本机应用程序而不提供显式目录路径时，此行为可能是一个问题。
即使位置 cmdlet 确实设置了进程范围的当前目录，也不能依赖它，因为其他运行空间可能会随时更改它。 应使用位置 cmdlet 使用特定于当前运行空间的当前工作目录执行基于路径的作。
`Set-Location` cmdlet 用于处理由任何提供程序公开的数据。 若要列出会话中可用的提供程序，请键入 `Get-PSProvider`。 有关详细信息，请参阅 [about_Providers](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6)。
堆栈是最后一个先出列表，其中只能访问最近添加的项。 按使用项的顺序将项添加到堆栈中，然后检索它们以反向顺序使用。 PowerShell 允许将提供程序位置存储在位置堆栈中。 PowerShell 创建未命名的默认位置堆栈。 可以创建多个命名位置堆栈。 如果未指定堆栈名称，PowerShell 将使用当前位置堆栈。 默认情况下，未命名的默认位置是当前位置堆栈，但你可以使用 `Set-Location` cmdlet 更改当前位置堆栈。
若要管理位置堆栈，请使用 `*-Location` cmdlet，如下所示：
  * 若要将位置添加到位置堆栈，请使用 `Push-Location` cmdlet。
  * 若要从位置堆栈获取位置，请使用 `Pop-Location` cmdlet。
  * 若要显示当前位置堆栈中的位置，请使用 cmdlet 的 `Get-Location` 参数。 若要在命名位置堆栈中显示位置，请使用 的 `Get-Location` 参数。
  * 若要创建新的位置堆栈，请使用 `Push-Location` 参数。 如果指定不存在的堆栈，`Push-Location` 创建堆栈。
  * 若要使位置堆栈成为当前位置堆栈，请使用 的 `Set-Location` 参数。


仅当默认位置堆栈是当前位置堆栈时，才完全可访问未命名的默认位置堆栈。 如果将命名位置堆栈设为当前位置堆栈，则不能再使用 `Push-Location` 或 `Pop-Location` cmdlet 从默认堆栈添加或获取项，或使用 `Get-Location` cmdlet 显示未命名堆栈中的位置。 若要使未命名的堆栈成为当前堆栈，请使用 cmdlet 的 `Set-Location` 参数，其值为 `$null` 或空字符串（`""`）。
## 相关链接


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
