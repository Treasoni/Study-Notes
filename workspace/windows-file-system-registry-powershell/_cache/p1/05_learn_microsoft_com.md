---
url: "https://learn.microsoft.com/zh-cn/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7"
title: "从 Windows PowerShell 5.1 迁移到 PowerShell 7 - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:10+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# 从 Windows PowerShell 5.1 迁移到 PowerShell 7
PowerShell 7 专为云、本地和混合环境而设计，包含增强功能和 [新功能](https://learn.microsoft.com/zh-cn/powershell/scripting/whats-new/what-s-new-in-powershell-70?view=powershell-7.6)。
  * 与 Windows PowerShell 并行安装和运行
  * 改进了与现有 Windows PowerShell 模块的兼容性
  * 新的语言功能，如三元运算符和 `ForEach-Object -Parallel`
  * 性能更强
  * 基于 SSH 的远程处理
  * 跨平台互作性
  * 支持 Docker 容器


PowerShell 7 与 Windows PowerShell 并行工作，使你可以在部署前轻松测试和比较版本。 迁移简单、快速且安全。
以下 Windows作系统支持 PowerShell 7：
  * Windows 10 和 11
  * Windows Server 2016、2019 和 2022


PowerShell 7 还在 macOS 和多个 Linux 分发版上运行。 有关支持的作系统的列表以及有关支持生命周期的信息，请参阅 [PowerShell 支持生命周期](https://learn.microsoft.com/zh-cn/powershell/scripting/install/powershell-support-lifecycle?view=powershell-7.6)。
## 安装 PowerShell 7
为了灵活和支持 IT、DevOps 工程师和开发人员的需求，可以使用多种选项来安装 PowerShell 7。 在大多数情况下，安装选项可以减少到以下方法：
  * 使用 [MSI 包](https://learn.microsoft.com/zh-cn/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.6#msi)部署 PowerShell
  * 使用 [ZIP 包](https://learn.microsoft.com/zh-cn/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.6#zip)部署 PowerShell


注释
可以使用管理产品（如 [Microsoft Configuration Manager](https://learn.microsoft.com/zh-cn/configmgr/apps/)）部署和更新 MSI 包。 从 [GitHub 发布页](https://github.com/PowerShell/PowerShell/releases)下载包。
部署 MSI 包需要管理员权限。 ZIP 包可由任何用户部署。 在提交完整安装之前，ZIP 包是安装 PowerShell 7 以进行测试的最简单方法。
您还可以通过 Windows 应用商店或 `winget` 安装 PowerShell 7。 有关这两种方法的详细信息，请参阅在 [Windows 上安装 PowerShell](https://learn.microsoft.com/zh-cn/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.6#winget) 中的详细说明。
## 将 PowerShell 7 与 Windows PowerShell 5.1 并行使用
PowerShell 7 旨在与 Windows PowerShell 5.1 共存。 以下功能可确保对 PowerShell 的投资得到保护，并且迁移到 PowerShell 7 非常简单。
  * 单独的安装路径和可执行文件名称
  * 单独的 PSModulePath
  * 每个版本的单独配置文件
  * 改进了模块兼容性
  * 新的远程处理终结点
  * 组策略支持
  * 单独的事件日志


### .NET 版本的差异
PowerShell 7.4 基于 .NET 8.0 构建。 Windows PowerShell 5.1 基于 .NET Framework 4.x 构建。 .NET 版本之间的差异可能会影响脚本的行为，尤其是在直接调用 .NET 方法时。 有关详细信息，请参阅 [Windows PowerShell 5.1 和 PowerShell 7.x 之间的差异](https://learn.microsoft.com/zh-cn/powershell/scripting/whats-new/differences-from-windows-powershell?view=powershell-7.6)。
### 单独的安装路径和可执行文件名称
PowerShell 7 安装到一个新的目录中，使其能够与 Windows PowerShell 5.1 并行运行。
按版本安装位置：
  * Windows PowerShell 5.1：`$Env:windir\System32\WindowsPowerShell\v1.0`
  * PowerShell 6.x： `$Env:ProgramFiles\PowerShell\6`
  * PowerShell 7： `$Env:ProgramFiles\PowerShell\7`


新位置将添加到 PATH，使你能够同时运行 Windows PowerShell 5.1 和 PowerShell 7。 如果要从 PowerShell 6.x 迁移到 PowerShell 7，则会删除 PowerShell 6 并替换 PATH。
在 Windows PowerShell 中，PowerShell 可执行文件名为 `powershell.exe`。 在版本 6 及更高版本中，可执行文件命名 `pwsh.exe`。 使用新名称，可以轻松支持两个版本的并行执行。
### 单独的 PSModulePath
默认情况下，Windows PowerShell 和 PowerShell 7 将模块存储在不同的位置。 PowerShell 7 将这些位置合并到 `$Env:PSModulePath` 环境变量中。 按名称导入模块时，PowerShell 会检查指定 `$Env:PSModulePath`的位置。 这允许 PowerShell 7 同时加载 Core 和 Desktop 模块。  
| 安装范围  | Windows PowerShell 5.1  | PowerShell 7.0  |  
| --- | --- | --- |  
| PowerShell 模块  | `$Env:windir\system32\WindowsPowerShell\v1.0\Modules`  | `$Env:ProgramFiles\PowerShell\7\Modules`  |  
| 用户安装AllUsers 范围  | `$Env:ProgramFiles\WindowsPowerShell\Modules`  | `$Env:ProgramFiles\PowerShell\Modules`  |  
| 用户安装CurrentUser 范围  | `$HOME\Documents\WindowsPowerShell\Modules`  | `$HOME\Documents\PowerShell\Modules`  |  
以下示例显示了每个版本的默认值 `$Env:PSModulePath` 。
  * 对于 Windows PowerShell 5.1：

```
$Env:PSModulePath -split (';')

```

```
C:\Users\<user>\Documents\WindowsPowerShell\Modules
C:\Program Files\WindowsPowerShell\Modules
C:\WINDOWS\System32\WindowsPowerShell\v1.0\Modules

```

  * 对于 PowerShell 7：

```
$Env:PSModulePath -split (';')

```

```
C:\Users\<user>\Documents\PowerShell\Modules
C:\Program Files\PowerShell\Modules
C:\Program Files\PowerShell\7\Modules
C:\Program Files\WindowsPowerShell\Modules
C:\WINDOWS\System32\WindowsPowerShell\v1.0\Modules

```



请注意，PowerShell 7 包括 Windows PowerShell 路径和 PowerShell 7 路径，用于提供模块的自动加载。
注释
如果更改了 PSModulePath 环境变量或已安装的自定义模块或应用程序，则可能存在其他路径。
有关详细信息，请参阅 [about_PSModulePath](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_psmodulepath)。
有关模块的详细信息，请参阅 [about_Modules](https://learn.microsoft.com/zh-cn/powershell/module/Microsoft.PowerShell.Core/About/about_Modules)。
### 单独的配置文件
PowerShell 配置文件是在 PowerShell 启动时执行的脚本。 此脚本通过添加命令、别名、函数、变量、模块和 PowerShell 驱动器来自定义环境。 配置文件脚本使这些自定义项在每个会话中都可用，而无需手动重新创建它们。
在 PowerShell 7 中，配置文件的位置路径发生了更改。
  * 在 Windows PowerShell 5.1 中，配置文件的位置为 `$HOME\Documents\WindowsPowerShell`。
  * 在 PowerShell 7 中，配置文件的位置为 `$HOME\Documents\PowerShell`。


配置文件的文件名也发生了更改：

```
$PROFILE | Select-Object *Host* | Format-List

```

```
 AllUsersAllHosts       : C:\Program Files\PowerShell\7\profile.ps1
 AllUsersCurrentHost    : C:\Program Files\PowerShell\7\Microsoft.PowerShell_profile.ps1
 CurrentUserAllHosts    : C:\Users\<user>\Documents\PowerShell\profile.ps1
 CurrentUserCurrentHost : C:\Users\<user>\Documents\PowerShell\Microsoft.PowerShell_profile.ps1

```

如需了解更多信息[ about_Profiles](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_profiles)。
### PowerShell 7 与 Windows PowerShell 5.1 模块的兼容性
在 Windows PowerShell 5.1 中使用的大多数模块已经适用于 PowerShell 7，包括 Azure PowerShell 和 Active Directory。 我们将继续与其他团队合作，为更多模块添加本机 PowerShell 7 支持，包括 Microsoft Graph、Office 365 和其他模块。 有关支持的模块的当前列表，请参阅 [PowerShell 7 模块兼容性](https://learn.microsoft.com/zh-cn/powershell/scripting/whats-new/module-compatibility?view=powershell-7.6)。
注释
在 Windows 上，我们还向 添加了 UseWindowsPowerShell`Import-Module` 开关，以便使用不兼容模块的用户轻松转换到 PowerShell 7。 有关此功能的详细信息，请参阅 [about_Windows_PowerShell_Compatibility](https://learn.microsoft.com/zh-cn/powershell/module/Microsoft.PowerShell.Core/About/about_windows_powershell_compatibility)。
## PowerShell 远程处理
借助 PowerShell 远程处理，可以在一台或多台远程计算机上运行任何 PowerShell 命令。 可以建立持久连接、启动交互式会话，并在远程计算机上运行脚本。
### WS-Management 远程处理
Windows PowerShell 5.1 及更低版本使用 WS-Management （WSMAN） 协议进行连接协商和数据传输。 Windows 远程管理（WinRM）使用 WSMAN 协议。 如果 WinRM 已启用，PowerShell 7 将使用名为 `Microsoft.PowerShell` 的现有 Windows PowerShell 5.1 终结点建立远程连接。 若要更新 PowerShell 7 以增加它自己独立的终结点，请运行 `Enable-PSRemoting` cmdlet。 要了解有关连接到特定终结点的信息，请参阅 [PowerShell 中的 WS-Management 远程处理](https://learn.microsoft.com/zh-cn/powershell/scripting/security/remoting/wsman-remoting-in-powershell?view=powershell-7.6)
若要使用 Windows PowerShell 远程处理，必须将远程计算机配置为进行远程管理。 有关详细信息，包括说明，请参阅 [“关于远程要求](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_remote_requirements)”。
要详细了解如何使用远程处理，请参阅[关于远程](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_remote)
### 基于 SSH 的远程处理
PowerShell 6.x 中添加了基于 SSH 的远程处理，以支持无法使用 Windows 本机组件（如 **WinRM** ）的其他作系统。 SSH 远程处理会在目标计算机上创建一个 PowerShell 托管进程作为 SSH 子系统。 有关在 Windows 或 Linux 上设置基于 SSH 的远程处理的详细信息和示例，请参阅： [通过 SSH 进行 PowerShell 远程处理](https://learn.microsoft.com/zh-cn/powershell/scripting/security/remoting/ssh-remoting-in-powershell?view=powershell-7.6)。
注释
PowerShell 库（PSGallery）包含一个模块和 cmdlet，用于自动配置基于 SSH 的远程控制。 从 `Microsoft.PowerShell.RemotingTools` 安装 模块，然后运行 `Enable-SSH` cmdlet。
`New-PSSession`、`Enter-PSSession`和`Invoke-Command` cmdlet有新的参数集以支持SSH连接。

```
[-HostName <string>]  [-UserName <string>]  [-KeyFilePath <string>]

```

若要创建远程会话，请使用 **HostName** 参数指定目标计算机，并使用 **UserName** 提供用户名。 以交互方式运行 cmdlet 时，系统会提示输入密码。

```
Enter-PSSession -HostName <Computer> -UserName <Username>

```

或者，使用 **HostName** 参数时，请提供用户名信息，后跟符号@（`@`），然后是计算机名称。

```
Enter-PSSession -HostName <Username>@<Computer>

```

可以使用具有 **KeyFilePath** 参数的私钥文件设置 SSH 密钥身份验证。 有关详细信息，请参阅 [OpenSSH 密钥管理](https://learn.microsoft.com/zh-cn/windows-server/administration/openssh/openssh_keymanagement)。
## 支持的组策略
PowerShell 包括组策略设置，可帮助你为企业环境中的服务器定义一致的选项值。 这些设置包括：
  * 控制台会话配置：设置运行 PowerShell 的配置终结点。
  * 启用模块日志记录：设置模块的 LogPipelineExecutionDetails 属性。
  * 启用 PowerShell 脚本块日志记录：启用所有 PowerShell 脚本的详细日志记录。
  * 启用脚本执行：设置 PowerShell 执行策略。
  * 启用 PowerShell 听录：允许将 PowerShell 命令的输入和输出捕获到基于文本的脚本中。
  * 设置 Update-Help 的默认源路径：将可更新帮助的源设置为目录，而不是 Internet。


有关详细信息，请参阅 [about_Group_Policy_Settings](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_group_policy_settings)。
PowerShell 7 包括组策略模板和 `$PSHOME`中的安装脚本。
组策略工具使用管理模板文件（`.admx`，`.adml`）在用户界面中填充策略设置。 这允许管理员管理基于注册表的策略设置。 该 `InstallPSCorePolicyDefinitions.ps1` 脚本在本地计算机上安装 PowerShell 管理模板。

```
Get-ChildItem -Path $PSHOME -Filter *Core*Policy*

```

```
    Directory: C:\Program Files\PowerShell\7

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---           2/27/2020 12:38 AM          15861 InstallPSCorePolicyDefinitions.ps1
-a---           2/27/2020 12:28 AM           9675 PowerShellCoreExecutionPolicy.adml
-a---           2/27/2020 12:28 AM           6201 PowerShellCoreExecutionPolicy.admx

```

## 单独的事件日志
Windows PowerShell 和 PowerShell 7 将事件记录到单独的事件日志。 使用以下命令获取 PowerShell 日志的列表。

```
Get-WinEvent -ListLog *PowerShell*

```

有关详细信息，请参阅 [about_Logging_Windows](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_logging_windows)。
## 改进了 Visual Studio Code 的编辑体验
具有 [PowerShell 扩展](https://code.visualstudio.com/)的 [Visual Studio Code （VS Code）](https://code.visualstudio.com/docs/languages/powershell)是 PowerShell 7 支持的脚本环境。 Windows PowerShell 集成脚本环境（ISE）仅支持 Windows PowerShell。
更新后的 PowerShell 扩展包括：
  * 新的 ISE 兼容性模式
  * 集成控制台中的 PSReadLine，包括语法突出显示、多行编辑和反向搜索
  * 稳定性和性能改进
  * 新的 CodeLens 集成
  * 改进了路径自动完成


若要简化到 Visual Studio Code 的转换，请使用**命令面板中** 提供的**“启用 ISE 模式”** 函数。 此函数将 VS Code 切换到 ISE 样式布局。 借助 ISE 样式布局，可以通过熟悉的用户体验来使用 PowerShell 的所有新特性和功能。
若要切换到新的 ISE 布局，请按 `Ctrl`+`Shift`+`P` 打开 **命令面板** ，键入 `PowerShell` 并选择 **PowerShell：启用 ISE 模式** 。
若要将布局设置为原始布局，请打开**命令面板** ，选择 **PowerShell：禁用 ISE 模式（还原为默认值）。**
有关将 VS Code 布局自定义到 ISE 的详细信息，请参阅 [如何在 Visual Studio Code 中复制 ISE 体验](https://learn.microsoft.com/zh-cn/powershell/scripting/dev-cross-plat/vscode/how-to-replicate-the-ise-experience-in-vscode?view=powershell-7.6)
注释
目前没有使用新功能更新 ISE 的计划。 在最新版本的 Windows 10 或 Windows Server 2019 及更高版本中，ISE 现在是用户可卸载的功能。 没有永久删除 ISE 的计划。 PowerShell 团队及其合作伙伴专注于改进 Visual Studio Code 的 PowerShell 扩展中的脚本体验。
## 后续步骤
掌握有效迁移的知识，立即 [安装 PowerShell 7](https://learn.microsoft.com/zh-cn/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.6) ！
在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/powershell/powershell/issues/new)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2026-04-10 


