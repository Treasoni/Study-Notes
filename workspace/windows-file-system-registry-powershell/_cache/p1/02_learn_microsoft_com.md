---
url: "https://learn.microsoft.com/zh-cn/powershell/scripting/discover-powershell"
title: "发现 PowerShell - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:10+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/scripting/discover-powershell?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/scripting/discover-powershell?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# 发现 PowerShell
PowerShell 是一种命令行 shell 和一种脚本语言。 PowerShell 在 Windows 上启动，可帮助自动执行管理任务。 现在，它跨平台运行，可用于各种任务。
使 PowerShell 唯一的是它接受并返回 .NET 对象，而不是文本。 使用此功能可以更轻松地连接 _管道_ 中的不同命令。
## PowerShell可以用来做什么？
最初，PowerShell 是仅限 Windows 的。 现在，它是跨平台的，可用于各种任务，例如：
  * **云管理** 。 PowerShell 可用于管理云资源。 例如，可以检索信息、更新或部署新资源。
  * **CI/CD** 。 它还可用作持续集成/持续部署管道的一部分。
  * **自动执行 Active Directory 和 Exchange 的任务** 。 你可以使用它自动执行 Windows 上几乎任何任务，例如在 Active Directory 中创建用户和 Exchange 中的邮箱。


## 谁使用 PowerShell？
PowerShell 是一种功能强大的工具，可帮助从事多种角色的人员。 传统上，系统管理员使用 PowerShell。 现在，它被自称为 DevOps、Cloud Ops 甚至开发人员的人所使用。
## PowerShell cmdlet
PowerShell 附带数百个预安装的命令。 PowerShell 命令称为 cmdlet（发音为 _命令莱特_ ）。
每个 cmdlet 的名称由 _Verb-Noun_ 对组成。 例如，`Get-Process`。 通过此命名约定，可以更轻松地了解 cmdlet 的作用。 此外，还可以更轻松地查找您寻找的命令。 查找要使用的 cmdlet 时，可以筛选谓词或名词。
### 使用 cmdlet 浏览 PowerShell
当你第一次拿起 PowerShell 时，它可能会感到令人生畏，因为似乎有很多东西要学习。 PowerShell 旨在帮助你按需逐步学习。
PowerShell 包含可帮助探索 PowerShell 的 cmdlet。 使用这四个 cmdlet，您可以发现哪些命令是可用的，它们的作用是什么，以及它们所操作的类型。
  * `Get-Verb`。 运行此命令将返回大多数命令所遵循的谓词列表。 响应包括这些动词执行的描述。 由于大多数命令都遵循此命名约定，因此它会设定命令的作用预期。 此命令可帮助你在创建自己的命令时选择适当的动词和命名方式。
  * `Get-Command`。 此命令检索计算机上安装的所有命令的列表。
  * `Get-Member`。 它基于对象的输出进行作，能够发现哪些对象、属性和方法可用于命令。
  * `Get-Help`。 以命令名称作为参数调用此命令将显示描述命令的各个部分的帮助页。


使用这些命令，几乎可以发现有关 PowerShell 所需的任何内容。
### 动词
_谓词_ 是 PowerShell 中的重要概念。 这是大多数 cmdlet 遵循的命名标准。 这也是编写自己的命令时应遵循的命名标准。 想法是 _动词_ 表示你尝试执行的操作，比如读取或更改数据。 PowerShell 具有标准化的谓词列表。 若要获取所有可能谓词的完整列表，请使用 `Get-Verb` cmdlet：

```
Get-Verb

```

该 cmdlet 返回一长串动词。 **说明** 提供了动词要执行功能的上下文。 下面是前几行输出：

```
Verb    AliasPrefix   Group     Description
----    -----------   -----     -----------
Add     a             Common    Adds a resource to a container, or attaches an item to another item
Clear   cl            Common    Removes all the resources from a container but does not delete the container
Close   cs            Common    Changes the state of a resource to make it inaccessible, unavailable, or unusab…
Copy    cp            Common    Copies a resource to another name or to another container
Enter   et            Common    Specifies an action that allows the user to move into a resource
Exit    ex            Common    Sets the current environment or context to the most recently used context
...

```

## 使用 Get-Command 找到命令
该 `Get-Command` cmdlet 返回系统上安装的所有可用命令的列表。 列表可能很大。 可以使用参数或帮助程序 cmdlet 筛选响应来限制返回的信息量。
### 按名称进行筛选
可以对`Get-Command`的输出使用不同的参数进行筛选。 通过筛选，可以查找具有特定属性的命令。 **Name 参数** 允许按名称查找特定命令。

```
Get-Command -Name Get-Process

```

```
CommandType     Name              Version    Source
-----------     ----              -------    ------
Cmdlet          Get-Process       7.0.0.0    Microsoft.PowerShell.Management

```

如果要查找使用进程的所有命令，该怎么办？ 可以使用通配符 `*` 来匹配其他类型的字符串。 例如：

```
Get-Command -Name *-Process

```

```
CommandType     Name              Version    Source
-----------     ----              -------    ------
Cmdlet          Debug-Process     7.0.0.0    Microsoft.PowerShell.Management
Cmdlet          Get-Process       7.0.0.0    Microsoft.PowerShell.Management
Cmdlet          Start-Process     7.0.0.0    Microsoft.PowerShell.Management
Cmdlet          Stop-Process      7.0.0.0    Microsoft.PowerShell.Management
Cmdlet          Wait-Process      7.0.0.0    Microsoft.PowerShell.Management

```

### 对名词和动词进行筛选
还有其他参数可以筛选谓词和名词值。 命令名称的谓词部分是最左侧的部分。 动词应该是 `Get-Verb` cmdlet 返回的值之一。 命令的最右侧部分是名词部分。 名词可以是任何东西。
  * **根据谓词进行筛选** 。 在命令 `Get-Process`中，谓词部分为 `Get`. 若要筛选谓词部分，请使用 **Verb** 参数。

```
Get-Command -Verb 'Get'

```

此示例列出使用谓词 `Get`的所有命令。
  * **筛选名词** 。 在命令 `Get-Process`中，名词部分为 `Process`。 若要筛选名词，请使用 **名词** 参数。 下面的示例返回以字母 `U`开头具有名词的所有 cmdlet。

```
Get-Command -Noun U*

```



此外，还可以合并参数以缩小搜索范围，例如：

```
Get-Command -Verb Get -Noun U*

```

```
CommandType     Name                         Version    Source
-----------     ----                         -------    ------
Cmdlet          Get-UICulture                7.0.0.0    Microsoft.PowerShell.Utility
Cmdlet          Get-Unique                   7.0.0.0    Microsoft.PowerShell.Utility
Cmdlet          Get-Uptime                   7.0.0.0    Microsoft.PowerShell.Utility

```

### 使用帮助程序 cmdlet 筛选结果
还可以使用其他 cmdlet 筛选结果。
  * `Select-Object`。 此通用命令可帮助你从一个或多个对象中选择特定属性。 还可以限制返回的项目数。 以下示例返回当前会话中前 5 个可用命令**的名称和****源** 属性值。

```
Get-Command | Select-Object -First 5 -Property Name, Source

```

```
Name                      Source
----                      ------
Add-AppPackage            Appx
Add-AppPackageVolume      Appx
Add-AppProvisionedPackage Dism
Add-AssertionOperator     Pester
Add-ProvisionedAppPackage Dism

```

有关详细信息，请参阅 [Select-Object](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.utility/select-object?view=powershell-7.6)。
  * `Where-Object`。 通过此 cmdlet，可以基于属性的值筛选返回的对象。 该命令采用一个表达式，该表达式可以测试属性的值。 以下示例返回所有以 `ProcessName` 开头的 `p` 进程。

```
Get-Process | Where-Object {$_.ProcessName -like "p*"}

```

该 `Get-Process` cmdlet 返回进程对象的集合。 若要筛选响应，请通过管道将输出传递给`Where-Object`。 管道指的是两个或多个命令通过 `|` 管道符号进行连接。 一个命令的输出作为下一命令的输入发送。 筛选器表达式`Where-Object`使用`-like`运算符匹配以字母`p`开头的进程。


## 使用 Get-Member 浏览对象
找到所需的 cmdlet 后，想要详细了解它生成的输出。 该 `Get-Member` cmdlet 显示对象的类型、属性和方法。 通过管道将您要检查的输出传递给 `Get-Member`。

```
Get-Process | Get-Member

```

结果将显示返回的类型 `TypeName` 以及对象的所有属性和方法。 下面是此类结果的摘录：

```
TypeName: System.Diagnostics.Process

Name        MemberType     Definition
----        ----------     ----------
Handles     AliasProperty  Handles = Handlecount
Name        AliasProperty  Name = ProcessName
...

```

使用 **MemberType** 参数可以限制返回的信息。

```
Get-Process | Get-Member -MemberType Method

```

默认情况下，PowerShell 仅显示几个属性。 上一个示例显示了`Name`和`MemberType``Definition`成员。 可用于 `Select-Object` 指定要查看的属性。 例如，你想要仅显示 `Name` 和 `Definition` 属性：

```
Get-Process | Get-Member | Select-Object Name, Definition

```

### 按参数类型搜索
`Get-Member` 向我们展示了 `Get-Process` 返回 **Process** 类型对象。 **ParameterType** 参数`Get-Command`可用于查找将 **Process** 对象作为输入的其他命令。

```
Get-Command -ParameterType Process

```

```
CommandType     Name                         Version    Source
-----------     ----                         -------    ------
Cmdlet          Debug-Process                7.0.0.0    Microsoft.PowerShell.Managem…
Cmdlet          Enter-PSHostProcess          7.1.0.0    Microsoft.PowerShell.Core
Cmdlet          Get-Process                  7.0.0.0    Microsoft.PowerShell.Managem…
Cmdlet          Get-PSHostProcessInfo        7.1.0.0    Microsoft.PowerShell.Core
Cmdlet          Stop-Process                 7.0.0.0    Microsoft.PowerShell.Managem…
Cmdlet          Wait-Process                 7.0.0.0    Microsoft.PowerShell.Managem…

```

了解命令的输出类型有助于缩小搜索相关命令的范围。
### 其他资源


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/scripting/discover-powershell?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/powershell/powershell/issues/new)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2026-04-10 


