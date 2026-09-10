---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers"
title: "about_Providers - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:10+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# about_Providers
## 简短说明
介绍 PowerShell 提供程序如何提供对不可在命令行轻松访问的数据和组件的访问权限。 数据以与文件系统驱动器类似的一致格式显示。
## 详细说明
PowerShell 提供程序是 .NET 程序，提供对专用数据存储的访问权限，以便更轻松地查看和管理。 数据显示在驱动器中，并且访问路径中的数据，就像在硬盘驱动器上一样。 可以使用提供程序支持的任何内置 cmdlet 来管理提供程序驱动器中的数据。 此外，可以使用专为数据设计的自定义 cmdlet。
提供程序还可以将动态参数添加到内置 cmdlet。 仅当将 cmdlet 与提供程序数据一起使用时，这些参数才可用。
## 内置提供程序
PowerShell 包括一组内置提供程序，这些提供程序提供对不同类型的对象的访问。
  * **别名** 提供程序
    * 驱动器 - `Alias:`
    * 对象类型 - **System.Management.Automation.AliasInfo**
  * **证书** 提供程序
    * 驱动器 - `Cert:`
    * 对象类型 - **Microsoft.PowerShell.Commands.X509StoreLocation** ，**System.Security.Cryptography.X509Certificates.X509Certificate2**
  * **环境** 提供程序
    * 驱动器 - `Env:`
    * 对象类型 - **System.Collections.DictionaryEntry**
  * **FileSystem** 提供程序
    * 驱动器 - `C:` 和其他取决于硬件
    * 对象类型 - **System.IO.FileInfo** 、**System.IO.DirectoryInfo**
  * **函数** 提供程序
    * 驱动器 - `Function:`
    * 对象类型 - **System.Management.Automation.FunctionInfo**
  * **注册表** 提供程序
    * 驱动器 - `HKLM:`，`HKCU:`
    * 对象类型 - **Microsoft.Win32.RegistryKey**
  * **变量** 提供程序
    * 驱动器 - `Variable:`
    * 对象类型 - **System.Management.Automation.PSVariable**
  * **WSMan** 提供程序
    * 驱动器 - `WSMan:`
    * 对象类型 - **Microsoft.WSMan.Management.WSManConfigContainerElement**


还可以创建自己的 PowerShell 提供程序，还可以安装其他人开发的提供程序。 若要列出会话中可用的提供程序，请键入：

```
Get-PSProvider

```

注意
**证书** 、**注册表** 和 **WSMan** 提供程序仅在 Windows 平台上可用。
## 安装和删除提供程序
提供程序通常通过 PowerShell 模块安装。 将模块导入到会话中。 无法卸载内置提供程序。 可以卸载其他模块加载的提供程序。
可以使用 `Remove-Module` cmdlet 从当前会话中卸载提供程序。 此 cmdlet 不会卸载提供程序，但它使提供程序在会话中不可用。
还可以使用 `Remove-PSDrive` cmdlet 从当前会话中删除任何驱动器。 驱动器上的此数据不受影响，但该驱动器在该会话中不再可用。
## 查看提供程序
若要查看计算机上的 PowerShell 提供程序，请键入：

```
Get-PSProvider

```

输出列出了已添加到会话的内置提供程序和提供程序。
## 提供程序 cmdlet
以下 cmdlet 旨在处理任何提供程序公开的数据。 可以采用相同的方式使用相同的 cmdlet 来管理提供程序公开的不同类型的数据。 了解如何管理一个提供程序的数据后，可以将相同的过程与来自任何提供程序的数据一起使用。
例如，`New-Item` cmdlet 会创建新项。 在 `C:` 提供程序支持的 驱动器中，可以使用 `New-Item` 创建新的文件或文件夹。 在 **注册表** 提供程序支持的驱动器中，可以使用 `New-Item` 创建新的注册表项。 在 `Alias:` 驱动器中，可以使用 `New-Item` 创建新的别名。
有关以下任一 cmdlet 的详细信息，请键入：

```
Get-Help <cmdlet-name> -Detailed

```

### ChildItem cmdlet


### 内容 Cmdlet


### Item Cmdlet


### ItemProperty cmdlet


### 位置 cmdlet


### 路径 cmdlet


### PSDrive cmdlet


### PSProvider Cmdlet


## 查看提供程序数据
提供程序的主要好处是，它以熟悉且一致的方式公开其数据。 数据呈现的模型是文件系统驱动器。
提供程序允许查看、导航和更改数据存储中的项，就像它们是文件系统中的数据一样。 数据存储通过它支持的驱动器的名称进行访问。
驱动器在 `Get-PSProvider` cmdlet 的默认显示中列出，但你可以使用 `Get-PSDrive` cmdlet 获取有关提供程序驱动器的信息。 例如，若要获取 Function： drive 的所有属性，请键入：

```
Get-PSDrive Function | Format-List *

```

可以像在文件系统驱动器上一样查看和移动提供程序驱动器中的数据。
若要查看提供程序驱动器的内容，请使用 `Get-Item` 或 `Get-ChildItem` cmdlet。 键入驱动器名称后跟冒号（`:`）。 例如，若要查看 `Alias:` 驱动器的内容，请键入：

```
Get-Item Alias:

```

可以通过在路径中包含驱动器名称，从另一个驱动器查看和管理任何驱动器中的数据。 例如，若要从另一个驱动器查看 `HKLM\Software` 驱动器中的 `HKLM:` 注册表项，请键入：

```
Get-ChildItem HKLM:\SOFTWARE\

```

若要打开驱动器，请使用 `Set-Location` cmdlet。 指定驱动器路径时，请记住冒号。 例如，若要将位置更改为 `Cert:` 驱动器的根目录，请键入：

```
Set-Location Cert:

```

然后，若要查看 `Cert:` 驱动器的内容，请键入：

```
Get-ChildItem

```

## 在分层数据中移动
可以像硬盘驱动器一样在提供程序驱动器中移动。 如果数据在项内的项层次结构中排列，请使用反斜杠（`\`）来指示子项。 使用以下格式：

```
drive:\location\child-location\...

```

例如，若要将位置更改为 `HKLM\Software` 注册表项，请键入 `Set-Location` 命令，例如：

```
Set-Location HKLM:\SOFTWARE\

```

如果完全限定名称中的任何元素包含空格，则必须用双引号（`"`）将名称括起来。 以下示例演示包含空格的完全限定路径。

```
"C:\Program Files\Internet Explorer\iexplore.exe"

```

还可以使用对位置的相对引用。 点（`.`）表示当前位置。 例如，如果位于 `HKLM:\Software\Microsoft` 注册表项中，并且想要在 `HKLM:\Software\Microsoft\PowerShell` 项中列出注册表子项，请键入以下命令：

```
Get-ChildItem .\PowerShell

```

此外，双点（`..`）指目录或容器，直接指当前位置上方的目录或容器。 可以使用双点（`..`）在提供程序层次结构中导航。

```
PS HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters\> cd ..\..\LanmanWorkstation\Parameters
PS HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters>

```

## 提供商主页
提供商还有一个 **主页** 位置。 此位置由提供程序支持的所有 `PSDrives` 共享。 可以通过查看提供程序的 **Home** 属性来检索它。

```
Get-PSProvider | Format-Table Name, Home

```

```
Name        Home
----        ----
Registry
Alias
Environment
FileSystem  C:\Users\username
Function
Variable
Certificate

```

**FileSystem** 提供程序是唯一具有 **主页** 默认值的提供程序。 它的值与 `$HOME`相同。 有关详细信息，请参阅 [about_Automatic_Variables](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_automatic_variables?view=powershell-7.6)。
可以使用提供程序的属性为提供程序设置 **Home** 目录。

```
(Get-PSProvider FileSystem).Home = "C:\"

```

`~` 字符可用于表示提供程序的主目录。 如果提供商没有 **主页** 位置集，则会看到错误。

```
Cert:\> Set-Location ~

```

```
Set-Location : Home location for this provider isn't set. To set the home
location, call "(Get-PSProvider 'Certificate').Home = 'path'".
At line:1 char:1
+ Set-Location ~
+ ~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [Set-Location],
                              PSInvalidOperationException
...

```

## 查找动态参数
动态参数是提供程序添加到 cmdlet 中的 cmdlet 参数。 仅当 cmdlet 与添加它们的提供程序一起使用时，这些参数才可用。
例如，`Cert:` 驱动器将 **CodeSigningCert** 参数添加到 `Get-Item` 和 `Get-ChildItem` cmdlet。 只有在 `Get-Item` 驱动器中使用 `Get-ChildItem` 或 `Cert:` 时，才能使用此参数。
有关提供程序支持的动态参数的列表，请参阅提供程序的帮助文件。 类型：

```
Get-Help <provider-name>

```

例如：

```
Get-Help Certificate

```

## 了解提供程序
尽管所有提供程序数据都显示在驱动器中，并且你使用相同的方法来移动它们，但相似性会停止在那里。 提供程序公开的数据存储可以随 Active Directory 位置和Microsoft Exchange Server 邮箱而异。
有关单个 PowerShell 提供程序的信息，请键入：

```
Get-Help <ProviderName>

```

例如：

```
Get-Help Registry

```

有关提供程序的帮助主题列表，请键入：

```
Get-Help * -Category Provider

```

## 另请参阅
  * [about_Path_Syntax](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_path_syntax?view=powershell-7.6)


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-02-05 


