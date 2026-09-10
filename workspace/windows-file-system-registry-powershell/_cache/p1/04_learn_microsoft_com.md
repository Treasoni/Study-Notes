---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_execution_policies"
title: "about_Execution_Policies - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:10+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# about_Execution_Policies
## 简短说明
介绍 PowerShell 执行策略，并说明如何管理它们。
## 详细说明
PowerShell 的执行策略是一项安全功能，用于控制 PowerShell 加载配置文件和运行脚本的条件。 此功能有助于防止执行恶意脚本。
在 Windows 计算机上，可以为本地计算机、当前用户或特定会话设置执行策略。 还可以使用组策略设置为计算机和用户设置执行策略。
本地计算机和当前用户的执行策略存储在 PowerShell 配置文件中。 无需在 PowerShell 配置文件中设置执行策略。 特定会话的执行策略仅存储在内存中，并在会话关闭时丢失。
执行策略不是安全边界，它是深层防御。 例如，当用户无法运行脚本时，可以在命令行中键入脚本内容，从而轻松绕过策略。 相反，执行策略可帮助用户设置基本规则，并防止他们无意中违反这些规则。
有关安全边界的详细信息，请参阅 [PowerShell 安全功能](https://learn.microsoft.com/zh-cn/powershell/scripting/security/security-features#security-servicing-criteria)的安全 _服务条件_ 部分。
在非Windows计算机上，默认执行策略是**Unrestricted** 无法更改的。 `Set-ExecutionPolicy` cmdlet 可用，但 PowerShell 会显示不支持的控制台消息。 虽然`Get-ExecutionPolicy`在非Windows平台上返回**Unrestricted** ，但行为确实匹配**Bypass** ，因为这些平台不实现Windows 安全中心区域。
## PowerShell 执行策略
这些策略的执行仅在 Windows 平台上发生。 PowerShell 执行策略如下所示：
  * `AllSigned`
    * 脚本可以运行。
    * 要求受信任的发布者对所有脚本和配置文件进行签名，包括在本地计算机上编写的脚本。
    * 在运行来自尚未分类为可信或不可信的发布者的脚本之前会提示你。
    * 存在运行已签名的恶意脚本的风险。
  * `Bypass`
    * 没有阻止任何内容，也没有警告或提示。
    * 此执行策略旨在用于将 PowerShell 脚本内置到更大的应用程序或 PowerShell 是具有其安全模型的程序的基础的配置。
  * `Default`
    * 设置默认执行策略。
    * 为 Windows 客户端和服务器 **RemoteSigned** 。
  * `RemoteSigned`
    * Windows 计算机的默认执行策略。
    * 脚本可以运行。
    * 需要受信任的发布者对从 Internet 下载的脚本和配置文件（包括电子邮件和即时消息程序）的数字签名。
    * 不需要在本地计算机上编写的脚本（而不是从 Internet 下载）上的数字签名。
    * 如果脚本被取消阻止（例如通过使用 `Unblock-File` cmdlet），则会运行从 Internet 下载且未签名的脚本。
    * 从 Internet 以外的源运行未签名的脚本以及可能是恶意的签名脚本的风险。
  * `Restricted`
    * 允许单个命令，但不允许脚本。
    * 防止运行所有脚本文件，包括格式化和配置文件（`.ps1xml`）、模块脚本文件（`.psm1`）和 PowerShell 配置文件（`.ps1`）。
  * `Undefined`
    * 当前范围内没有设置执行策略。
    * 如果所有范围内的执行策略都是 **Undefined** ，那么 Windows 客户端的有效执行策略是 **Restricted** ，而 Windows Server 的有效执行策略是 **RemoteSigned** 。
  * `Unrestricted`
    * 非Windows计算机的默认执行策略，无法更改。
    * 未签名的脚本可以运行。 存在运行恶意脚本的风险。
    * 在运行不是来自本地 Intranet 区域的脚本和配置文件之前，警告用户。
注意
在无法将通用命名约定 （UNC） 路径与 Internet 路径区分开来的系统上，不允许使用 **RemoteSigned** 执行策略运行 UNC 路径标识的脚本。


## 执行策略范围和优先级
可以设置仅在特定范围内有效的执行策略。 该参数接受以下值：
  * `MachinePolicy` - 由计算机的所有用户的组策略设置
  * `UserPolicy` - 由计算机的当前用户的组策略设置
  * `Process` - 仅影响当前 PowerShell 会话
  * `CurrentUser` - 仅影响当前用户
  * `LocalMachine` - Default 影响计算机所有用户的范围


注意
`MachinePolicy` 并 `UserPolicy` 按组策略设置。 如果尝试将范围设置为这些值之一，PowerShell 会显示一条错误消息，指出该作用域由组策略设置，并且无法更改。
如果组策略未定义执行策略，则有效的执行策略由优先级顺序确定，如下所示：
  * `Process` - 最高优先级。 `Process` 范围仅影响当前的 PowerShell 会话。 执行策略保存在 environment variable `$Env:PSExecutionPolicyPreference`中，而不是注册表中。 关闭 PowerShell 会话后，将删除变量和值。
  * `CurrentUser` - 第二高优先级。 此设置存储在用户特定的 `powershell.config.json` 文件中。
  * `LocalMachine` - 最低优先级。 该设置存储在 `$PSHOME/powershell.config.json` 文件中。


有关该文件的详细信息 `powershell.config.json` ，请参阅 [about_PowerShell_Config](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_powershell_config?view=powershell-7.6)。
## 使用 PowerShell 管理执行策略
若要获取当前 PowerShell 会话的有效执行策略，请使用 `Get-ExecutionPolicy` cmdlet。
以下命令可获取有效的执行策略：

```
Get-ExecutionPolicy

```

若要获取影响当前会话的所有执行策略，并按优先级顺序显示它们：

```
Get-ExecutionPolicy -List

```

结果类似于以下示例输出：

```
        Scope ExecutionPolicy
        ----- ---------------
MachinePolicy       Undefined
   UserPolicy       Undefined
      Process       Undefined
  CurrentUser    RemoteSigned
 LocalMachine       AllSigned

```

在这种情况下，有效执行策略 **RemoteSigned** ，因为当前用户的执行策略优先于为本地计算机设置的执行策略。
若要为特定范围设置执行策略，请使用 **Scope** 的 `Get-ExecutionPolicy` 参数。
例如，以下命令获取 **CurrentUser** 范围的执行策略：

```
Get-ExecutionPolicy -Scope CurrentUser

```

### 更改执行策略
若要更改 Windows 计算机上的 PowerShell 执行策略，请使用 `Set-ExecutionPolicy` cmdlet。 更改立即生效。 无需重启 PowerShell。
如果您为范围 **LocalMachine** 或 **CurrentUser** 设置执行策略，则更改将保存在配置文件中，并在您再次更改之前保持有效。
如果为 **Process** 范围设置执行策略，则不会将其保存在配置文件中。 执行策略将一直保留，直到当前进程和任何子进程关闭。
注意
在 Windows Vista 和更高版本的 Windows 中，若要运行更改本地计算机的执行策略的命令（**LocalMachine** 范围），请使用 **以管理员身份运行** 选项启动 PowerShell。
若要更改执行策略，请执行以下操作：

```
Set-ExecutionPolicy -ExecutionPolicy <PolicyName>

```

例如：

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned

```

若要在特定范围内设置执行策略，请执行以下操作：

```
Set-ExecutionPolicy -ExecutionPolicy <PolicyName> -Scope <scope>

```

例如：

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

```

更改执行策略的命令可以成功，但仍不能更改有效的执行策略。
例如，设置本地计算机的执行策略的命令可能会成功，但会被当前用户的执行策略覆盖。
### 删除执行策略
若要删除特定范围的执行策略，请将执行策略设置为 **Undefined** 。
例如，若要删除本地计算机的所有用户的执行策略：

```
Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope LocalMachine

```

若要删除 **Scope** 的执行策略，请执行以下操作：

```
Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser

```

如果未在任何范围内设置执行策略，则有效执行策略 **Restricted** ，这是 Windows 客户端的默认值。
### 为一个会话设置不同的策略
可以使用 的 `pwsh.exe` 参数为新的 PowerShell 会话设置执行策略。 该策略仅影响当前会话和子会话。
若要为新会话设置执行策略，请在命令行（如 `cmd.exe` 或 PowerShell 中）启动 PowerShell，然后使用 `pwsh.exe` 参数设置执行策略。
例如：

```
pwsh.exe -ExecutionPolicy AllSigned

```

设置的执行策略不会存储在配置文件中。 而是存储在 `$Env:PSExecutionPolicyPreference` 环境变量中。 关闭设置策略的会话时，将删除该变量。 无法通过编辑变量值来更改策略。
在会话期间，为会话设置的执行策略优先于在本地计算机或当前用户的配置文件中设置的执行策略。 但是，它不优先于使用组策略设置的执行策略。
## 使用组策略管理执行策略
可以使用“**打开脚本执行组策略** ”设置来管理企业中计算机的执行策略。 组策略设置会覆盖 PowerShell 中在所有范围内设置的执行策略。
“**启用脚本执行** ”策略设置如下所示：
  * 如果禁用“启用脚本执行”，则脚本不会运行。 这相当于 **Restricted** 执行策略。
  * 如果启用“**启用脚本执行** ”，则可以选择一个执行策略。 组策略设置等效于以下执行策略设置：  
| 组策略  | 执行策略  |  
| --- | --- |  
| 允许所有脚本  | Unrestricted  |  
| 允许本地脚本和远程签名脚本  | 远程签名  |  
| 仅允许已签名的脚本  | AllSigned  |  
  * 如果未配置“启用脚本执行”，则不起作用。 PowerShell 中的执行策略已生效。


和`PowerShellCoreExecutionPolicy.adm``PowerShellCoreExecutionPolicy.admx`文件将**打开脚本执行** 策略添加到组策略编辑器中的“计算机配置”和“用户配置”节点，路径如下：
`Administrative Templates\Windows Components\Windows PowerShell`
计算机配置节点中设置的策略优先于用户配置节点中设置的策略。
有关详细信息，请参阅 [about_Group_Policy_Settings](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_group_policy_settings?view=powershell-7.6)。
## 管理已签名和未签名的脚本
在 Windows 中，Internet Explorer 和 Microsoft Edge 等程序向下载的文件添加备用数据流。 这会将文件标记为“来自 Internet”。 如果 PowerShell 执行策略 **RemoteSigned** ，PowerShell 将不会运行从 Internet 下载的未签名脚本，其中包括电子邮件和即时消息程序。
可以对脚本进行签名，或选择在不更改执行策略的情况下运行未签名的脚本。
从 PowerShell 3.0 开始，可以使用 cmdlet 的 `Get-Item` 参数来检测因从 Internet 下载而阻止的文件。 使用 `Unblock-File` cmdlet 取消阻止脚本，以便可以在 PowerShell 中运行这些脚本。
有关详细信息，请参阅 [about_Signing](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_signing?view=powershell-7.6)、[Get-Item](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-item?view=powershell-7.6) 以及 [Unblock-File](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.utility/unblock-file?view=powershell-7.6)。
注意
下载文件的其他方法可能不会将文件标记为来自 Internet 区域。 一些示例包括：
  * `curl.exe`
  * `Invoke-RestMethod`
  * `Invoke-WebRequest`


## Windows Server Core 和 Windows Nano Server 上的执行策略
在某些情况下，在 Windows Server Core 或 Windows Nano Server 上运行 PowerShell 6 时，执行策略可能会失败，并出现以下错误：

```
AuthorizationManager check failed.
At line:1 char:1
+ C:\scriptpath\scriptname.ps1
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess

```

PowerShell 使用 Windows 桌面外壳（`explorer.exe`）中的 API 来验证脚本文件的区域。 Windows Server Core 和 Windows Nano Server 上不提供 Windows Shell。
如果 Windows 桌面 Shell 不可用或无响应，则还可以在任何 Windows 系统上收到此错误。 例如，在登录期间，PowerShell 登录脚本可以在 Windows 桌面准备就绪之前启动执行，从而导致失败。
使用 **ByPass** 或 **AllSigned** 的执行策略不需要区域检查以避免问题。
## 另请参阅
  * [about_Environment_Variables](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.6)
  * [about_Group_Policy_Settings](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_group_policy_settings?view=powershell-7.6)


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2026-08-31 


