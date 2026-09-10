---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_psmodulepath"
title: "about_PSModulePath - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:42:33+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_psmodulepath?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_psmodulepath?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# about_PSModulePath
## 简短说明
本文介绍 `$Env:PSModulePath` 环境变量的用途和用法。
## 详细说明
`$Env:PSModulePath` 环境变量包含文件夹位置的列表。 PowerShell 以递归方式搜索每个文件夹的模块（`.psd1` 或 `.psm1`）文件。
默认情况下，分配给 `$Env:PSModulePath` 的有效位置为：
  * **CurrentUser** 范围内安装的模块：
    * 在 Windows 上，这些模块存储在 `$HOME\Documents\PowerShell\Modules`中。 `Documents` 文件夹的特定位置因 Windows 版本和使用文件夹重定向而异。 此外，Microsoft OneDrive 可以更改 `Documents` 文件夹的位置。 若要验证 `Documents` 文件夹的位置，请运行以下命令：`[Environment]::GetFolderPath('MyDocuments')`。
    * 在非 Windows 系统上，这些模块存储在 `$HOME/.local/share/powershell/Modules` 文件夹中。
  * 安装在 **AllUsers** 范围内的模块：
    * 在 Windows 上，这些模块存储在 `$Env:ProgramFiles\PowerShell\Modules`中。
    * 在非 Windows 系统上，这些模块存储在 `/usr/local/share/powershell/Modules`中。
  * 随 PowerShell 一起随附的模块存储在 `$PSHOME\Modules`中。


注意
包含 PowerShell 模块的应用程序可以在 Windows 的其他目录中安装模块，例如 `Program Files` 文件夹。 安装程序包可能不会将位置追加到 `$Env:PSModulePath`。
Windows PowerShell 5.1 的默认位置不同于 PowerShell 7。
  * **CurrentUser** 范围中安装的模块存储在 `$HOME\Documents\WindowsPowerShell\Modules`中。
  * 安装在 AllUsers 范围内的模块存储在 `$Env:ProgramFiles\WindowsPowerShell\Modules` 中。
  * Windows PowerShell 附带的模块存储在 `$PSHOME\Modules` 中，即 `$Env:SystemRoot\System32\WindowsPowerShell\1.0\Modules`。


## PowerShell PSModulePath 构造
每次启动 PowerShell 时，都会构造 `$Env:PSModulePath` 的值。 该值因 PowerShell 版本及其启动方式而异。
### Windows PowerShell 启动
在启动时，Windows PowerShell 使用以下逻辑构造 `PSModulePath`：
  * 如果 `PSModulePath` 不存在，请合并 **CurrentUser** 、**AllUsers** 和 `$PSHOME` 模块路径
  * 如果 `PSModulePath` 存在：
    * 如果 `PSModulePath` 包含 `$PSHOME` 模块路径：
      * **AllUsers** 模块路径插入到 `$PSHOME` 模块路径之前
    * 否则：
      * 按照定义，只需使用`PSModulePath`，因为用户故意删除了`$PSHOME`位置。


仅当用户范围 不存在时，`$Env:PSModulePath` 模块路径才具有前缀。 否则，将按定义使用 User 范围 `$Env:PSModulePath`。
### PowerShell 7 启动
在 Windows 中，对于大多数环境变量，如果存在用户范围的变量，则新进程仅使用该值，即使存在同名的计算机范围的变量也是如此。 _路径_ 环境变量的处理方式不同。
在 Windows 上，`PSModulePath` 与处理 `Path` 环境变量的方式类似。 `Path` 与其他环境变量的处理方式不同。 当启动进程时，Windows 会将用户范围的 `Path` 与计算机范围的 `Path`组合在一起。
  * 检索用户范围的 `PSModulePath`
  * 与进程继承的 `PSModulePath` 环境变量进行比较
    * 如果相同：
      * 请根据 环境变量的语义，将 `PSModulePath``PATH` 追加到末尾。
      * Windows `System32` 路径来源于由计算机定义的 `PSModulePath`，因此无需显式添加。
    * 如果两者不同，则可以认为用户显式修改了它，不要追加 **AllUsers**`PSModulePath`
  * 按该顺序以 PS7 用户、系统和 `$PSHOME` 路径为前缀 
    * 如果 `powershell.config.json` 包含用户范围的 `PSModulePath`，请使用该路径，而不是用户的默认路径
    * 如果 `powershell.config.json` 包含系统范围的 `PSModulePath`，请使用该路径，而不是系统的默认路径


非 Windows 系统没有用户和系统环境变量的分离。 `PSModulePath` 是继承的，如果尚未定义，则特定于 PS7 的路径会带有前缀。
### 从 PowerShell 7 启动 Windows PowerShell
对于此讨论，Windows PowerShell 意味着 `powershell.exe` 和 `powershell_ise.exe`。
将 `$Env:PSModulePath` 的值复制到 `WinPSModulePath`，并进行以下修改：
  * 删除 PS7 用户模块路径
  * 删除 PS7 系统模块路径
  * 删除 PS7 的 `$PSHOME` 模块路径


删除 PS7 路径，以便 PS7 模块不会在 Windows PowerShell 中加载。 启动 Windows PowerShell 时，将使用 `WinPSModulePath` 值。
此修改仅适用于 PowerShell 7 直接启动的 Windows PowerShell 进程。 当Windows PowerShell 通过中间进程（例如 `cmd.exe` PowerShell 7 启动的或Python进程）启动时，中间进程将继承 PowerShell 7 的未修改`$Env:PSModulePath`，并将其传递给其自己的子进程。 Windows PowerShell 以这种方式启动，保留继承的 PowerShell 7 模块路径。 由于这些路径位于Windows PowerShell 系统模块路径之前，Windows PowerShell 可以将共享模块名称（例如`Microsoft.PowerShell.Utility`）解析为无法加载的 PowerShell 7 模块版本。 这会中断模块自动加载，并且这些模块中的 cmdlet 失败并出现 `CommandNotFoundException` 错误。
若要从具有正确模块路径的中间进程开始Windows PowerShell，请从子进程的环境中删除`PSModulePath`。 Windows PowerShell 然后在启动时构造其默认值。 例如：
  * 在 PowerShell 7.4 及更高版本中，使用 **Environment** 参数 `Start-Process` 从中间进程的环境中删除变量：

```
Start-Process python harness.py -Environment @{ PSModulePath = $null }

```

  * 在`cmd.exe`开始Windows PowerShell 之前清除变量：

```
cmd /c "set PSModulePath=&& powershell.exe -File script.ps1"

```

  * 在Python中，从传递给子进程的环境中删除变量：

```
import os
import subprocess

env = {k: v for k, v in os.environ.items() if k.upper() != "PSMODULEPATH"}
subprocess.run(["powershell.exe", "-File", "script.ps1"], env=env)

```



### 从 Windows PowerShell 启动 PowerShell 7
PowerShell 7 启动按原样继续，添加了 Windows PowerShell 所添加的继承路径。 由于 PS7 特定的路径具有前缀，因此没有功能问题。
## 模块搜索行为
PowerShell 以递归方式在 **PSModulePath** 中搜索模块（`.psd1` 或 `.psm1`）文件中的每个文件夹。 此搜索模式允许将同一模块的多个版本安装在不同的文件夹中。 例如：

```
    Directory: C:\Program Files\WindowsPowerShell\Modules\PowerShellGet

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----           8/14/2020  5:56 PM                1.0.0.1
d----           9/13/2019  3:53 PM                2.1.2

```

默认情况下，当找到多个版本时，PowerShell 会加载模块的最高版本号。 若要加载特定版本，请将 `Import-Module` 与 FullyQualifiedName 参数结合使用。 有关详细信息，请参阅 [Import-Module](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/import-module?view=powershell-7.6)。
## 修改 PSModulePath
在大多数情况下，应在默认模块位置安装模块。 但是，可能需要更改 `PSModulePath` 环境变量的值。
例如，若要在当前会话中暂时将 `C:\Program Files\Fabrikam\Modules` 目录添加到 `$Env:PSModulePath`，请键入：

```
$Env:PSModulePath = $Env:PSModulePath+";C:\Program Files\Fabrikam\Modules"

```

命令中的分号（`;`）将新路径与列表中前面的路径分隔开来。 在非 Windows 平台上，冒号（`:`）分隔环境变量中的路径位置。
### 在非 Windows 中修改 PSModulePath
若要更改非 Windows 环境中每个会话 `PSModulePath` 的值，请将上一个命令添加到 PowerShell 配置文件。
### 在 Windows 中修改 PSModulePath
若要更改每个会话中 `PSModulePath` 的值，请编辑存储 `PSModulePath` 值的注册表项。 `PSModulePath` 值作为 _未展开_ 字符串存储在注册表中。 若要避免将 `PSModulePath` 值永久保存为 _扩展_ 字符串，请使用子项上的 `GetValue()` 方法并直接编辑值。
示例将 `C:\Program Files\Fabrikam\Modules` 路径添加到 `PSModulePath` 环境变量值中，而不会对字符串进行展开。

```
$key = (Get-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment')
$path = $key.GetValue('PSModulePath','','DoNotExpandEnvironmentNames')
$path += ';%ProgramFiles%\Fabrikam\Modules'
$key.SetValue('PSModulePath',$path,[Microsoft.Win32.RegistryValueKind]::ExpandString)

```

若要将路径添加到用户设置，请使用以下代码：

```
$key = (Get-Item 'HKCU:\Environment')
$path = $key.GetValue('PSModulePath','','DoNotExpandEnvironmentNames')
$path += ';%ProgramFiles%\Fabrikam\Modules'
$key.SetValue('PSModulePath',$path,[Microsoft.Win32.RegistryValueKind]::ExpandString)

```

## 另请参阅
  * [about_Windows_PowerShell_Compatibility](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_windows_powershell_compatibility)


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_psmodulepath?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2026-08-25 


