---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_pipelines"
title: "about_Pipelines - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:10+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_pipelines?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_pipelines?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# about_Pipelines
## 简短说明
将命令在 PowerShell 中合并为管道
## 详细说明
管道是由管道操作员（`|`） (ASCII 124) 连接的一系列命令。 每个管道运算符将上述命令的结果发送到下一个命令。
可以将第一个命令的输出作为输入发送到第二个命令进行处理。 该输出可以发送到另一个命令。 结果是一个由一系列简单命令组成的复杂命令链或管道。
例如

```
Command-1 | Command-2 | Command-3

```

在此示例中，`Command-1` 发出的对象将发送到 `Command-2`。 `Command-2` 处理对象并将其发送到 `Command-3`。 `Command-3` 处理对象并将其发送到管道。 由于管道中没有更多命令，因此结果将显示在控制台中。
在管道中，命令按从左到右的顺序进行处理。 处理将作为单个操作进行处理，并且输出在生成时显示。
下面是一个简单的示例。 以下命令获取记事本进程，然后停止它。
例如

```
Get-Process notepad | Stop-Process

```

第一个命令使用 `Get-Process` cmdlet 获取表示记事本进程的对象。 它使用管道运算符（`|`）将进程对象发送到停止记事本进程的 `Stop-Process` cmdlet。 请注意，`Stop-Process` 命令没有 **名称** 或 **ID** 参数来指定进程，因为指定的进程是通过管道提交的。
此管道示例获取当前目录中的文本文件，仅选择长度超过 10,000 字节的文件，按长度对这些文件进行排序，并在表中显示每个文件的名称和长度。

```
Get-ChildItem -Path *.txt |
  Where-Object {$_.Length -gt 10000} |
    Sort-Object -Property Length |
      Format-Table -Property Name, Length

```

此管道按指定顺序包含四个命令。 下图展示了每个命令的输出如何传递到管道中的下一个命令。

```
Get-ChildItem -Path *.txt
| (FileInfo objects for *.txt)
V
Where-Object {$_.Length -gt 10000}
| (FileInfo objects for *.txt)
| (      Length > 10000      )
V
Sort-Object -Property Length
| (FileInfo objects for *.txt)
| (      Length > 10000      )
| (     Sorted by length     )
V
Format-Table -Property Name, Length
| (FileInfo objects for *.txt)
| (      Length > 10000      )
| (     Sorted by length     )
| (   Formatted in a table   )
V

Name                       Length
----                       ------
tmp1.txt                    82920
tmp2.txt                   114000
tmp3.txt                   114000

```

## 使用管道
大多数 PowerShell cmdlet 旨在支持管道。 在大多数情况下，可以将 _Get_ cmdlet 的结果**通过管道** 传递给同一名词的另一个 cmdlet。 例如，可以通过管道将 `Get-Service` cmdlet 的输出传递给 `Start-Service` 或 `Stop-Service` cmdlet。
此示例管道在计算机上启动 WMI 服务：

```
Get-Service wmi | Start-Service

```

例如，可以将 PowerShell 注册表提供程序中 `Get-Item` 或 `Get-ChildItem` 的输出传递给 `New-ItemProperty` cmdlet。 此示例向 **MyCompany** 注册表键中添加了一个新的注册表项 **NoOfEmployees** ，其值为 **8124** 。

```
Get-Item -Path HKLM:\Software\MyCompany |
  New-ItemProperty -Name NoOfEmployees -Value 8124

```

许多实用工具 cmdlet（例如 `Get-Member`、`Where-Object`、`Sort-Object`、`Group-Object`和 `Measure-Object`）几乎完全用于管道中。 可以通过管道将任何对象类型传递给这些 cmdlet。 此示例演示如何按每个进程中打开的句柄数对计算机上的所有进程进行排序。

```
Get-Process | Sort-Object -Property Handles

```

可以通过管道将对象传递给格式化、导出和输出 cmdlet，例如 `Format-List`、`Format-Table`、`Export-Clixml`、`Export-Csv` 和 `Out-File`。
此示例演示如何使用 `Format-List` cmdlet 显示进程对象的属性列表。

```
Get-Process winlogon | Format-List -Property *

```

还可以通过管道将本机命令的输出传递给 PowerShell cmdlet。 例如：

```
PS> ipconfig.exe | Select-String -Pattern 'IPv4'

   IPv4 Address. . . . . . . . . . . : 172.24.80.1
   IPv4 Address. . . . . . . . . . . : 192.168.1.45
   IPv4 Address. . . . . . . . . . . : 100.64.108.37

```

重要
“成功”流和“错误”流类似于其他 shell 的 stdout 和 stderr 流。 但是，stdin 并未与 PowerShell 管道相连以进行输入。 有关重定向的详细信息，请参阅 [about_Redirection](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_redirection?view=powershell-7.6)。
通过一些实践，你会发现将简单的命令合并到管道中可以节省时间和键入，并使脚本更高效。
## 管道的工作原理
本部分介绍如何将输入对象绑定到 cmdlet 参数，并在管道执行期间进行处理。
### 接受管道输入
若要支持管道传送，接收 cmdlet 必须具有接受管道输入的参数。 将 `Get-Help` 命令与 **Full** 或 **Parameter** 选项一起使用，以确定 cmdlet 接受管道输入的参数。
例如，若要确定 `Start-Service` cmdlet 的哪些参数接受管道输入，请键入：

```
Get-Help Start-Service -Full

```

或

```
Get-Help Start-Service -Parameter *

```

`Start-Service` cmdlet 的帮助显示，只有 **InputObject** 和 **Name** 参数接受管道输入。

```
-InputObject <ServiceController[]>
Specifies ServiceController objects representing the services to be started.
Enter a variable that contains the objects, or type a command or expression
that gets the objects.

Required?                    true
Position?                    0
Default value                None
Accept pipeline input?       True (ByValue)
Accept wildcard characters?  false

-Name <String[]>
Specifies the service names for the service to be started.

The parameter name is optional. You can use Name or its alias, ServiceName,
or you can omit the parameter name.

Required?                    true
Position?                    0
Default value                None
Accept pipeline input?       True (ByPropertyName, ByValue)
Accept wildcard characters?  false

```

将对象通过管道发送到 `Start-Service`时，PowerShell 会尝试将对象与 **InputObject** 和 **Name** 参数相关联。
### 接受管道输入的方法
Cmdlet 参数可以通过以下两种不同的方式之一接受管道输入：
  * **ByValue** ：参数接受与预期的 .NET 类型匹配的值或可转换为该类型的值。
例如， 的`Start-Service`参数接受按值输入的管道。 它可以接受可转换为字符串的字符串对象或对象。
  * **ByPropertyName** ：仅当输入对象具有与参数同名的属性时，参数才接受输入。
例如，`Start-Service` 的 Name 参数可以接受具有 **Name** 属性的对象。 若要列出对象的属性，请通过管道将其传递给 `Get-Member`。


某些参数可以通过值或属性名称接受对象，以便更轻松地从管道获取输入。
### 参数绑定
将对象从一个命令传递给另一个命令时，PowerShell 会尝试将管道对象与接收 cmdlet 的参数相关联。
PowerShell 的参数绑定组件根据以下条件将输入对象与 cmdlet 参数相关联：
  * 参数必须接受来自管道的输入。
  * 该参数必须接受要发送的对象的类型或可转换为预期类型的类型。
  * 该参数未在命令中使用。


例如，`Start-Service` cmdlet 具有许多参数，但其中只有两个参数，**Name** ，**InputObject** 接受管道输入。 **Name** 参数采用字符串，**InputObject** 参数采用服务对象。 因此，你可以通过管道传递字符串、服务对象，以及具有可以转换为字符串或服务对象的属性的对象。
PowerShell 尽可能高效地管理参数绑定。 无法建议或强制 PowerShell 绑定到特定参数。 如果 PowerShell 无法绑定管道对象，该命令将失败。
有关排查绑定错误的详细信息，请参阅本文后面的[调查管道错误](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_pipelines?view=powershell-7.6#investigating-pipeline-errors)。
### 一次性处理
将对象管道传递给命令非常类似于使用命令的参数来提交对象。 让我们看看一个管道示例。 在此示例中，我们使用管道来显示服务对象的表。

```
Get-Service | Format-Table -Property Name, DependentServices

```

在功能上，这类似于使用 `Format-Table` 参数来提交对象集合。
例如，我们可以将服务的集合保存到使用 **InputObject** 参数传递的变量。

```
$services = Get-Service
Format-Table -InputObject $services -Property Name, DependentServices

```

或者，我们可以在 **InputObject** 参数中嵌入命令。

```
Format-Table -InputObject (Get-Service) -Property Name, DependentServices

```

但是，有一个重要区别。 将多个对象通过管道传递给命令时，PowerShell 一次将对象发送到一个命令。 使用命令参数时，对象将作为单个数组对象发送。 这种细微差异具有重大后果。
执行管道时，PowerShell 会自动枚举实现 `IEnumerable` 接口或其泛型对等接口的任何类型。 枚举项会逐一通过管道发送。 PowerShell 还通过 属性枚举 `Rows` 类型。
自动枚举存在一些例外情况。
  * 对于哈希表、实现 `GetEnumerator()` 接口或其泛型接口的类型以及 System.Xml.XmlNode 类型，必须调用 `IDictionary` 方法。
  * **System.String** 类实现 `IEnumerable`，但 PowerShell 不枚举字符串对象。


在以下示例中，数组和哈希表通过管道传递给 `Measure-Object` cmdlet，以计算从管道接收的对象数。 该数组具有多个成员，哈希表具有多个键值对。 一次只枚举一个数组。

```
@(1,2,3) | Measure-Object

```

```
Count    : 3
Average  :
Sum      :
Maximum  :
Minimum  :
Property :

```

```
@{"One"=1;"Two"=2} | Measure-Object

```

```
Count    : 1
Average  :
Sum      :
Maximum  :
Minimum  :
Property :

```

同样，如果将多个进程对象从 `Get-Process` cmdlet 传递给 `Get-Member` cmdlet，PowerShell 将每个进程对象逐个发送到 `Get-Member`。 `Get-Member` 显示进程对象的 .NET 类（类型），以及它们的属性和方法。

```
Get-Process | Get-Member

```

```
TypeName: System.Diagnostics.Process

Name      MemberType     Definition
----      ----------     ----------
Handles   AliasProperty  Handles = Handlecount
Name      AliasProperty  Name = ProcessName
NPM       AliasProperty  NPM = NonpagedSystemMemorySize
...

```

注意
`Get-Member` 消除重复项，因此，如果对象都是同一类型，则它只显示一种对象类型。
但是，如果使用 的 `Get-Member` 参数，则 `Get-Member` 接收 **System.Diagnostics.Process** 对象的数组作为单个单元。 它显示对象的数组的属性。 （请注意 `[]` 类型名称之后的数组符号（）。
例如

```
Get-Member -InputObject (Get-Process)

```

```
TypeName: System.Object[]

Name               MemberType    Definition
----               ----------    ----------
Count              AliasProperty Count = Length
Address            Method        System.Object& Address(Int32 )
Clone              Method        System.Object Clone()
...

```

此结果可能不是预期的结果。 但了解后，可以使用它。 例如，所有数组对象都有一个 **Count** 属性。 可以使用该函数对计算机上运行的进程数进行计数。
例如

```
(Get-Process).Count

```

记住，通过管道传递的对象是一个接一个地进行传递的。
## 在管道中使用本机命令
PowerShell 允许在管道中包含系统自带的外部命令。
在 PowerShell 7.4 之前，从输出原始字节数据的本机程序管道或重定向输出将输出转换为 .NET 字符串。 此转换导致原始数据输出损坏。
在 PowerShell 7.4 或更高版本中 `PSNativeCommandPreserveBytePipe` ，实验性功能是主流功能。 当将本机命令的 **stdout** 流重定向到文件时，或者将字节流数据管道传输到本机命令的 **stdin** 流时，此功能将保留字节流数据。
例如，使用本机命令 `curl` 可以下载二进制文件，并使用重定向将其保存到磁盘。

```
$uri = 'https://github.com/PowerShell/PowerShell/releases/download/v7.3.4/powershell-7.3.4-linux-arm64.tar.gz'

# native command redirected to a file
curl -s -L $uri > powershell.tar.gz

```

你还可以通过管道将字节流数据传递给另一原生命令的 stdin 流。 以下示例使用 `curl`下载压缩的 TAR 文件。 下载的文件数据流式传输到 `tar` 命令，以提取存档的内容。

```
# native command output piped to a native command
curl -s -L $uri | tar -xzvf - -C .

```

还可以通过管道将 PowerShell 命令的字节流输出传递给本机命令的输入。 以下示例使用 `Invoke-WebRequest` 下载与前面的示例相同的 TAR 文件。

```
# byte stream piped to a native command
(Invoke-WebRequest $uri).Content | tar -xzvf - -C .

# bytes piped to a native command (all at once as byte[])
,(Invoke-WebRequest $uri).Content | tar -xzvf - -C .

```

将 **stderr** 输出重定向到 **stdout** 时，此功能不支持字节流数据。 合并 **stderr** 和 **stdout** 流时，合并的流将被视为字符串数据。
## 调查管道错误
当 PowerShell 无法将管道对象与接收 cmdlet 的参数相关联时，命令将失败。
在以下示例中，我们尝试将注册表项从一个注册表项移动到另一个注册表项。 `Get-Item` cmdlet 获取目标路径，然后通过管道传递给 `Move-ItemProperty` cmdlet。 `Move-ItemProperty` 命令指定要移动的注册表项的当前路径和名称。

```
Get-Item -Path HKLM:\Software\MyCompany\sales |
Move-ItemProperty -Path HKLM:\Software\MyCompany\design -Name product

```

该命令失败，PowerShell 会显示以下错误消息：

```
Move-ItemProperty : The input object can't be bound to any parameters for
the command either because the command doesn't take pipeline input or the
input and its properties do not match any of the parameters that take
pipeline input.
At line:1 char:23
+ $a | Move-ItemProperty <<<<  -Path HKLM:\Software\MyCompany\design -Name p

```

若要调查，请使用 `Trace-Command` cmdlet 跟踪 PowerShell 的参数绑定组件。 以下示例在执行管道时跟踪参数绑定。 **PSHost** 参数在控制台中显示跟踪结果，**FilePath** 参数将跟踪结果发送到 `debug.txt` 文件以供以后参考。

```
Trace-Command -Name ParameterBinding -PSHost -FilePath debug.txt -Expression {
  Get-Item -Path HKLM:\Software\MyCompany\sales |
    Move-ItemProperty -Path HKLM:\Software\MyCompany\design -Name product
}

```

跟踪的结果很长，但它们显示绑定到 `Get-Item` cmdlet 的值，然后显示绑定到 `Move-ItemProperty` cmdlet 的命名值。

```
...
BIND NAMED cmd line args [`Move-ItemProperty`]
BIND arg [HKLM:\Software\MyCompany\design] to parameter [Path]
...
BIND arg [product] to parameter [Name]
...
BIND POSITIONAL cmd line args [`Move-ItemProperty`]
...

```

最后，它显示尝试将路径与 **目标的** 参数 `Move-ItemProperty` 绑定失败。

```
...
BIND PIPELINE object to parameters: [`Move-ItemProperty`]
PIPELINE object TYPE = [Microsoft.Win32.RegistryKey]
RESTORING pipeline parameter's original values
Parameter [Destination] PIPELINE INPUT ValueFromPipelineByPropertyName NO
COERCION
Parameter [Credential] PIPELINE INPUT ValueFromPipelineByPropertyName NO
COERCION
...

```

使用 `Get-Help` cmdlet 查看 **Destination** 参数的属性。

```
Get-Help Move-ItemProperty -Parameter Destination

-Destination <String>
    Specifies the path to the destination location.

    Required?                    true
    Position?                    1
    Default value                None
    Accept pipeline input?       True (ByPropertyName)
    Accept wildcard characters?  false

```

结果显示，**目标** 仅“按属性名称”接受管道输入。 因此，管道对象必须具有名为 **Destination** 的属性。
使用 `Get-Member` 查看来自 `Get-Item`的对象的属性。

```
Get-Item -Path HKLM:\Software\MyCompany\sales | Get-Member

```

输出显示该项是 **Microsoft.Win32.RegistryKey** 对象，该对象没有 **Destination** 属性。 这解释了命令失败的原因。
**路径** 参数按名称或值接受管道输入。

```
Get-Help Move-ItemProperty -Parameter Path

-Path <String[]>
    Specifies the path to the current location of the property. Wildcard
    characters are permitted.

    Required?                    true
    Position?                    0
    Default value                None
    Accept pipeline input?       True (ByPropertyName, ByValue)
    Accept wildcard characters?  true

```

若要修复命令，必须在 `Move-ItemProperty` cmdlet 中指定目标，并使用 `Get-Item` 获取要移动的项 **路径** 。
例如

```
Get-Item -Path HKLM:\Software\MyCompany\design |
Move-ItemProperty -Destination HKLM:\Software\MyCompany\sales -Name product

```

## 内部行延续
如前所述，管道是由管道操作员（`|`）连接的一系列命令，通常用单行编写。 但是，为了便于阅读，PowerShell 允许跨多行拆分管道。 当管道运算符是行上的最后一个标记时，PowerShell 分析器会将下一行联接到当前命令，以继续构造管道。
例如，以下单行管道：

```
Command-1 | Command-2 | Command-3

```

可以编写为：

```
Command-1 |
    Command-2 |
    Command-3

```

后续行中的前导空格并不重要。 缩进增强了可读性。
PowerShell 7 添加了对管道延续的支持，并在行的开头加上管道字符。 以下示例演示如何使用此新功能。

```
# Wrapping with a pipe at the beginning of a line (no backtick required)
Get-Process | Where-Object CPU | Where-Object Path
    | Get-Item | Where-Object FullName -Match "AppData"
    | Sort-Object FullName -Unique

# Wrapping with a pipe on a line by itself
Get-Process | Where-Object CPU | Where-Object Path
    |
    Get-Item | Where-Object FullName -Match "AppData"
    |
    Sort-Object FullName -Unique

```

重要
在 shell 中以交互方式工作时，仅当使用 `Ctrl`+`V` 进行粘贴时，才会在行开头粘贴管道的代码。 右键单击粘贴操作一次插入一行。 由于该行不以管道字符结尾，因此 PowerShell 会将输入视为完成并按输入执行该行。
## 另请参阅
  * [about_Command_Syntax](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_command_syntax?view=powershell-7.6)


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_pipelines?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-12-28 


