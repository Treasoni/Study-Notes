---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-psdrive"
title: "Get-PSDrive (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:26+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-psdrive?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-psdrive?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# Get-PSDrive 

模块:
    [Microsoft.PowerShell.Management Module](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/?view=powershell-7.6)
获取当前会话中的驱动器。
## 语法
###  Name (默认值) 

```
Get-PSDrive
    [[-Name] <String[]>]
    [-Scope <String>]
    [-PSProvider <String[]>]
    [<CommonParameters>]

```

###  LiteralName 

```
Get-PSDrive
    [-LiteralName] <String[]>
    [-Scope <String>]
    [-PSProvider <String[]>]
    [<CommonParameters>]

```

## 说明
`Get-PSDrive` cmdlet 获取当前会话中的驱动器。 可以在会话中获取特定驱动器或所有驱动器。
此 cmdlet 获取以下类型的驱动器：
  * 计算机上的 Windows 逻辑驱动器，包括映射到网络共享的驱动器。
  * PowerShell 提供程序公开的驱动器（如 Certificate：、Function：和 Alias： 驱动器）和 HKLM：和 HKCU：由 Windows PowerShell 注册表提供程序公开的驱动器。
  * 使用 New-PSDrive cmdlet 创建的会话指定的临时驱动器和持久性映射网络驱动器。


从 Windows PowerShell 3.0 开始，**persist** 参数 `New-PSDrive` cmdlet 可以创建在本地计算机上保存的映射网络驱动器，并在其他会话中可用。 有关详细信息，请参阅 New-PSDrive。
此外，从 Windows PowerShell 3.0 开始，当外部驱动器连接到计算机时，Windows PowerShell 会自动将 PSDrive 添加到表示新驱动器的文件系统。 无需重启 Windows PowerShell。 同样，当外部驱动器与计算机断开连接时，Windows PowerShell 会自动删除表示已删除驱动器的 PSDrive。
## 示例
### 示例 1：获取当前会话中的驱动器

```
PS C:\> Get-PSDrive

Name           Used (GB)     Free (GB) Provider      Root
----           ---------     --------- --------      ----
Alias                                  Alias
C                 202.06      23718.91 FileSystem    C:\
Cert                                   Certificate   \
D                1211.06     123642.32 FileSystem    D:\
Env                                    Environment
Function                               Function
HKCU                                   Registry      HKEY_CURRENT_USER
HKLM                                   Registry      HKEY_LOCAL_MACHINE
Variable                               Variable

```

此命令获取当前会话中的驱动器。
输出显示硬盘驱动器（C：）、CD-ROM 驱动器（D：）以及 Windows PowerShell 提供程序公开的驱动器（别名：、Cert：、Env：、Function：、HKCU：、HKLM：和 Variable：）。
### 示例 2：在计算机上获取驱动器

```
PS C:\foo> Get-PSDrive D

Name           Used (GB)     Free (GB) Provider      Root
----           ---------     --------- --------      ----
D                1211.06     123642.32 FileSystem    D:\

```

此命令获取计算机上的 D： 驱动器。 请注意，命令中的驱动器号后跟冒号。
### 示例 3：获取 Windows PowerShell FileSystem 提供程序支持的所有驱动器

```
PS C:\> Get-PSDrive -PSProvider FileSystem
Name           Used (GB)     Free (GB) Provider      Root
----           ---------     --------- --------      ----
A                                                    A:\
C                 202.06      23718.91 FileSystem    C:\
D                1211.06     123642.32 FileSystem    D:\
G                 202.06        710.91 FileSystem    \\Music\GratefulDead

```

此命令获取 Windows PowerShell FileSystem 提供程序支持的所有驱动器。 这包括固定驱动器、逻辑分区、映射的网络驱动器以及使用 New-PSDrive cmdlet 创建的临时驱动器。
### 示例 4：检查驱动器是否用作 Windows PowerShell 驱动器名称

```
if (Get-PSDrive X -ErrorAction SilentlyContinue) {
    Write-Host 'The X: drive is already in use.'
} else {
    New-PSDrive -Name X -PSProvider Registry -Root HKLM:\SOFTWARE
}

```

此命令检查 X 驱动器是否已用作 Windows PowerShell 驱动器名称。 否则，该命令使用 `New-PSDrive` cmdlet 创建映射到 HKLM：\SOFTWARE 注册表项的临时驱动器。
### 示例 5：比较文件系统驱动器的类型

```
PS C:\> Get-PSDrive -PSProvider FileSystem
Name           Used (GB)     Free (GB) Provider      Root
----           ---------     --------- --------      ----
A                                                    A:\
C                 202.06      23718.91 FileSystem    C:\
D                1211.06     123642.32 FileSystem    D:\
G                 202.06        710.91 FileSystem    \\Music\GratefulDead
X                                      Registry      HKLM:\Network

PS C:\> net use
New connections will be remembered.
Status       Local     Remote                    Network
-------------------------------------------------------------------------------
OK           G:        \\Server01\Public         Microsoft Windows Network

PS C:\> [System.IO.DriveInfo]::GetDrives() | Format-Table
Name DriveType DriveFormat IsReady AvailableFreeSpace TotalFreeSpace TotalSize     RootDirectory VolumeLabel
---- --------- ----------- ------- ------------------ -------------- ---------     ------------- -----------
A:\    Network               False                                                 A:\
C:\      Fixed NTFS          True  771920580608       771920580608   988877418496  C:\           Windows
D:\      Fixed NTFS          True  689684144128       689684144128   1990045179904 D:\           Big Drive
E:\      CDRom               False                                                 E:\
G:\    Network NTFS          True      69120000           69120000       104853504 G:\           GratefulDead

PS N:\> Get-CimInstance -Class Win32_LogicalDisk

DeviceID DriveType ProviderName   VolumeName         Size          FreeSpace
-------- --------- ------------   ----------         ----          ---------
A:       4
C:       3                        Windows            988877418496  771926069248
D:       3                        Big!              1990045179904  689684144128
E:       5
G:       4         \\Music\GratefulDead              988877418496  771926069248


PS C:\> Get-CimInstance -Class Win32_NetworkConnection
LocalName RemoteName            ConnectionState Status
--------- ----------            --------------- ------
G:        \\Music\GratefulDead  Connected       OK

```

此示例将 `Get-PSDrive` 显示的文件系统驱动器类型与其他方法进行比较。 此示例演示了在 Windows PowerShell 中显示驱动器的不同方式，并显示仅可在 Windows PowerShell 中访问使用 New-PSDrive cmdlet 创建的特定于会话的驱动器。
第一个命令使用 `Get-PSDrive` 获取会话中的所有文件系统驱动器。 这包括固定驱动器（C： 和 D：）、使用 的 `New-PSDrive` 参数创建的映射网络驱动器 （G：），以及使用 `New-PSDrive` 创建的 PowerShell 驱动器 （T：），而不使用 **Persist** 参数创建。
**net use** 命令显示 Windows 映射的网络驱动器，在本例中，它仅显示 G 驱动器。 它不显示由 `New-PSDrive`创建的 X： 驱动器。 它显示 G： 驱动器也映射到 \\\Music\GratefulDead。
第三个命令使用 Microsoft .NET Framework **System.IO.DriveInfo** 类的 **GetDrives** 方法。 此命令获取 Windows 文件系统驱动器，包括驱动器 G：，但它不会获取由 `New-PSDrive`创建的驱动器。
第四个命令使用 `Get-CimInstance` cmdlet 来获取 **Win32_LogicalDisk** 类的实例。 它返回 A：、C：、D：、E：和 G： 驱动器，但返回由 `New-PSDrive`创建的驱动器。
最后一个命令使用 `Get-CimInstance` cmdlet 来显示 **Win32_NetworkConnection** 类的实例。 与 **net use** 一样，它仅返回由 `New-PSDrive`创建的持久 G： 驱动器。
## 参数
### -LiteralName
指定驱动器的名称。
**LiteralName** 的值与键入时完全相同。 不会将任何字符解释为通配符。 如果名称包含转义字符，请将其括在单引号中。 单引号告知 Windows PowerShell 不要将任何字符解释为转义序列。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
LiteralName   
| Position:  | 0  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Name
指定此 cmdlet 在操作中获取的驱动器的名称或名称作为字符串数组。 键入没有冒号的驱动器名称或字母（`:`）。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
#### 参数集
Name   
| Position:  | 0  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -PSProvider
以字符串数组的形式指定 Windows PowerShell 提供程序。 此 cmdlet 仅获取此提供程序支持的驱动器。 键入提供程序的名称，例如 FileSystem、注册表或证书。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
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
### -Scope
指定此 cmdlet 获取驱动器的范围。
此参数的可接受值为：
  * 全球
  * 本地
  * 剧本
  * 一个相对于当前范围的数字（0 到范围的数目，其中 0 是当前范围，1 是它的父范围）。 “Local”是默认值。


有关详细信息，请参阅 [about_Scopes](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_scopes?view=powershell-7.6)。
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
### CommonParameters
此 cmdlet 支持通用参数：-Debug、-ErrorAction、-ErrorVariable、-InformationAction、-InformationVariable、-OutBuffer、-OutVariable、-PipelineVariable、-ProgressAction、-Verbose、-WarningAction 和 -WarningVariable。 有关详细信息，请参阅 [about_CommonParameters](https://go.microsoft.com/fwlink/?LinkID=113216)。
## 输入
###  None
不能用管道将对象传送到此 cmdlet。
## 输出
###  [PSDriveInfo](https://learn.microsoft.com/zh-cn/dotnet/api/system.management.automation.psdriveinfo)
此 cmdlet 返回表示会话中的驱动器的对象。
## 备注
PowerShell 包含以下与 `Get-PSDrive`相关的别名：
  * 所有平台：
    * `gdr`
  * 此 cmdlet 的设计目的是与任何供应商公开的数据进行协作。 若要列出会话中可用的提供程序，请使用 `Get-PSProvider` cmdlet。 有关详细信息，请参阅 [about_Providers](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6)。
  * 使用 New-PSDrive cmdlet **Persist** 参数创建的映射网络驱动器特定于用户帐户。 在以管理员身份运行选项或其他用户凭据开头的会话中创建的映射网络驱动器在会话中不可见，这些会话在没有显式凭据或当前用户的凭据的情况下启动。


## 相关链接


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-psdrive?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
