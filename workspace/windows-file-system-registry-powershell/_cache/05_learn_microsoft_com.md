---
url: "https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-childitem"
title: "Get-ChildItem (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn"
scraped_at: 2026-09-10T15:41:04+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# Get-ChildItem 

模块:
    [Microsoft.PowerShell.Management Module](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/?view=powershell-7.6)
获取一个或多个指定位置中的项和子项。
## 语法
###  Items (默认值) 

```
Get-ChildItem
    [[-Path] <string[]>]
    [[-Filter] <string>]
    [-Include <string[]>]
    [-Exclude <string[]>]
    [-Recurse]
    [-Depth <uint>]
    [-Force]
    [-Name]
    [<CommonParameters>]

```

###  LiteralItems 

```
Get-ChildItem
    [[-Filter] <string>]
    -LiteralPath <string[]>
    [-Include <string[]>]
    [-Exclude <string[]>]
    [-Recurse]
    [-Depth <uint>]
    [-Force]
    [-Name]
    [<CommonParameters>]

```

## 说明
`Get-ChildItem` cmdlet 获取一个或多个指定位置中的项。 如果该项为容器，则此命令将获取容器内的各项（称为子项）。 可以使用 **Recurse** 参数获取所有子容器中的项，并使用 **Depth** 参数来限制递归级别数。
`Get-ChildItem` cmdlet 旨在处理任何提供程序公开的项目。 例如，项可以是文件系统文件或目录、注册表配置单元或证书存储。 若要列出会话中可用的提供程序，请使用 `Get-PSProvider` 命令。 某些参数仅适用于特定提供程序。 有关详细信息，请参阅 [about_Providers](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6)。
## 示例
### 示例 1：从文件系统目录获取子项
此示例从文件系统目录中获取子项。 将显示文件名和子目录名称。 对于空位置（目录或文件夹），该命令不返回任何输出并返回到 PowerShell 提示符。
`Get-ChildItem` cmdlet 使用 **Path** 参数来指定目录 `C:\Test`。 `Get-ChildItem` PowerShell 控制台中显示文件和目录。

```
Get-ChildItem -Path C:\Test

```

```
   Directory: C:\Test

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2/15/2019     08:29                Logs
-a----        2/13/2019     08:55             26 anotherfile.txt
-a----        2/12/2019     15:40         118014 Command.txt
-a----         2/1/2019     08:43            183 CreateTestFile.ps1
-ar---        2/12/2019     14:31             27 ReadOnlyFile.txt

```

默认情况下，`Get-ChildItem` 列出模式（**属性** ）、**LastWriteTime** 、文件大小（**长度** ），以及项 **名称** 。 **Mode** 属性中的字母可以解释为：
  * `l`（链接）
  * `d`（目录）
  * `a`（存档）
  * `r`（只读）
  * `h`（隐藏）
  * `s`（系统）


有关模式标志的详细信息，请参阅 [about_FileSystem_Provider](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6#attributes-flagsexpression)。
### 示例 2：获取目录中的子项名称
此示例仅列出目录中项的名称。
`Get-ChildItem` cmdlet 使用 **Path** 参数来指定目录 `C:\Test`。 **Name** 参数仅返回指定路径中的文件或目录名称。 返回的名称与 **Path** 参数的值相对。

```
Get-ChildItem -Path C:\Test -Name

```

```
Logs
anotherfile.txt
Command.txt
CreateTestFile.ps1
ReadOnlyFile.txt

```

### 示例 3：获取当前目录和子目录中的子项
此示例显示位于当前目录及其子目录中的 `.txt` 文件。

```
Get-ChildItem -Path .\*.txt -Recurse -Force

```

```
    Directory: C:\Test\Logs\Adirectory

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        2/12/2019     16:16             20 Afile4.txt
-a-h--        2/12/2019     15:52             22 hiddenfile.txt
-a----        2/13/2019     13:26             20 LogFile4.txt

    Directory: C:\Test\Logs\Backup

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        2/12/2019     16:16             20 ATextFile.txt
-a----        2/12/2019     15:50             20 LogFile3.txt

    Directory: C:\Test\Logs

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        2/12/2019     16:16             20 Afile.txt
-a-h--        2/12/2019     15:52             22 hiddenfile.txt
-a----        2/13/2019     13:26             20 LogFile1.txt

    Directory: C:\Test

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        2/13/2019     08:55             26 anotherfile.txt
-a----        2/12/2019     15:40         118014 Command.txt
-a-h--        2/12/2019     15:52             22 hiddenfile.txt
-ar---        2/12/2019     14:31             27 ReadOnlyFile.txt

```

`Get-ChildItem` cmdlet 使用 **Path** 参数来指定 `C:\Test\*.txt`。 **路径** 使用星号（`*`）通配符指定文件扩展名为 `.txt`的所有文件。 **Recurse** 参数搜索 **Path** 目录及其子目录，如 **Directory:** 标题所示。 **Force** 参数显示具有 `hiddenfile.txt` 模式的隐藏文件，例如 。
### 示例 4：使用 Include 参数获取子项
在此示例中，`Get-ChildItem` 使用 **Include** 参数从 **Path** 参数指定的目录中查找特定项。

```
# When using the -Include parameter, if you don't include an asterisk in the path
# the command returns no output.
Get-ChildItem -Path C:\Test\ -Include *.txt

```

```
Get-ChildItem -Path C:\Test\* -Include *.txt

```

```
    Directory: C:\Test

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        2/13/2019     08:55             26 anotherfile.txt
-a----        2/12/2019     15:40         118014 Command.txt
-ar---        2/12/2019     14:31             27 ReadOnlyFile.txt

```

`Get-ChildItem` cmdlet 使用 **Path** 参数来指定目录 `C:\Test`。 **Path** 参数包括尾随星号（`*`）通配符，用于指定目录的内容。 **Include** 参数使用星号（`*`）通配符指定文件扩展名为 `.txt`的所有文件。
使用 **Include** 参数时，**Path** 参数需要尾随星号（`*`）通配符来指定目录的内容。 例如，`-Path C:\Test\*`。
  * 如果将 **Recurse** 参数添加到命令，`*` 参数中的尾随星号 （） 是可选的。 **Recurse** 参数从 **Path** 目录及其子目录中获取项。 例如： `-Path C:\Test\ -Recurse -Include *.txt`
  * 如果 `*` 参数中不包含尾随星号（），该命令不会返回任何输出并返回到 PowerShell 提示符。 例如，`-Path C:\Test\`。


### 示例 5：使用 Exclude 参数获取子项
该示例的输出显示目录 `C:\Test\Logs`的内容。 使用**排除** 和**递归** 参数的其他命令会参考此输出。

```
Get-ChildItem -Path C:\Test\Logs

```

```
    Directory: C:\Test\Logs

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2/15/2019     13:21                Adirectory
d-----        2/15/2019     08:28                AnEmptyDirectory
d-----        2/15/2019     13:21                Backup
-a----        2/12/2019     16:16             20 Afile.txt
-a----        2/13/2019     13:26             20 LogFile1.txt
-a----        2/12/2019     16:24             23 systemlog1.log

```

```
Get-ChildItem -Path C:\Test\Logs\* -Exclude A*

```

```
    Directory: C:\Test\Logs

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2/15/2019     13:21                Backup
-a----        2/13/2019     13:26             20 LogFile1.txt
-a----        2/12/2019     16:24             23 systemlog1.log

```

`Get-ChildItem` cmdlet 使用 **Path** 参数来指定目录 `C:\Test\Logs`。 **Exclude** 参数使用星号（`*`）通配符来指定从输出中排除以 `A` 或 `a` 开头的任何文件或目录。
使用 **Exclude** 参数时，`*` 参数中的尾随星号 （） 是可选的。 例如，`-Path C:\Test\Logs` 或 `-Path C:\Test\Logs\*`。
  * 如果 `*` 参数中不包含尾随星号（），将显示 **Path** 参数的内容。 例外情况是与 **排除** 参数值匹配的文件名或子目录名称。
  * 如果 `*` 参数中包含尾随星号（），该命令将递归到 **Path** 参数的子目录中。 例外情况是与 **排除** 参数值匹配的文件名或子目录名称。
  * 如果将 **Recurse** 参数添加到命令，则递归输出与 **Path** 参数是否包含尾随星号（`*`）相同。


### 示例 6：从注册表配置单元中获取注册表项
此示例从 `HKEY_LOCAL_MACHINE\HARDWARE`获取所有注册表键。
`Get-ChildItem` 使用 **Path** 参数指定注册表项 `HKLM:\HARDWARE`。 Hive 的路径和顶级注册表键显示在 PowerShell 控制台中。
有关详细信息，请参阅 [about_Registry_Provider](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_registry_provider?view=powershell-7.6)。

```
Get-ChildItem -Path HKLM:\HARDWARE

```

```
    Hive: HKEY_LOCAL_MACHINE\HARDWARE

Name             Property
----             --------
ACPI
DESCRIPTION
DEVICEMAP
RESOURCEMAP
UEFI

```

```
Get-ChildItem -Path HKLM:\HARDWARE -Exclude D*

```

```
   Hive: HKEY_LOCAL_MACHINE\HARDWARE

Name                           Property
----                           --------
ACPI
RESOURCEMAP

```

第一个命令显示 `HKLM:\HARDWARE` 注册表项的内容。 **Exclude** 参数指示 `Get-ChildItem` 不返回以 `D*`开头的任何子项。 目前，**Exclude** 参数仅适用于子项，不适用于项属性。
### 示例 7：获取具有代码签名机构的所有证书
此示例获取 PowerShell `Cert:` 驱动器中具有代码签名权限的每个证书。
`Get-ChildItem` cmdlet 使用 **Path** 参数指定带有 `Cert:` 驱动器的证书提供程序。 **Recurse** 参数会搜索由 **Path** 指定的目录及其子目录。 **CodeSigningCert** 参数只获取具有代码签名授权的证书。

```
Get-ChildItem -Path Cert:\* -Recurse -CodeSigningCert

```

有关证书提供程序和 `Cert:` 驱动器的详细信息，请参阅 [about_Certificate_Provider](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.security/about/about_certificate_provider?view=powershell-7.6)。
### 示例 8：使用 Depth 参数获取项
本示例显示目录中的项及其子目录中的项。 **Depth** 参数确定递归过程中要包括的子目录层级数。 从输出中排除空目录。

```
Get-ChildItem -Path C:\Parent -Depth 2

```

```
    Directory: C:\Parent

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2/14/2019     10:24                SubDir_Level1
-a----        2/13/2019     08:55             26 file.txt

    Directory: C:\Parent\SubDir_Level1

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2/14/2019     10:24                SubDir_Level2
-a----        2/13/2019     08:55             26 file.txt

    Directory: C:\Parent\SubDir_Level1\SubDir_Level2

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2/14/2019     10:22                SubDir_Level3
-a----        2/13/2019     08:55             26 file.txt

```

`Get-ChildItem` cmdlet 使用 **Path** 参数来指定 `C:\Parent`。 **Depth** 参数指定两个递归级别。 `Get-ChildItem` 显示由 **Path** 参数和子目录的两个级别指定的目录的内容。
### 示例 9：获取硬链接信息
在 PowerShell 6.2 中，添加了备用视图以获取硬链接信息。

```
Get-ChildItem -Path C:\PathContainingHardLink | Format-Table -View childrenWithHardLink

```

### 示例 10：非 Windows 操作系统的输出
在 Unix 系统上的 PowerShell 7.1 中，`Get-ChildItem` 提供类似于 Unix 的输出：

```
PS> Get-ChildItem /etc/r*

```

```
    Directory: /etc

UnixMode   User Group    LastWriteTime Size Name
--------   ---- -----    ------------- ---- ----
drwxr-xr-x root wheel  9/30/2019 19:19  128 racoon
-rw-r--r-- root wheel  9/26/2019 18:20 1560 rc.common
-rw-r--r-- root wheel  7/31/2017 17:30 1560 rc.common~previous
-rw-r--r-- root wheel  9/27/2019 20:34 5264 rc.netboot
lrwxr-xr-x root wheel  11/8/2019 15:35   22 resolv.conf -> /private/var/run/resolv.conf
-rw-r--r-- root wheel 10/23/2019 17:41    0 rmtab
-rw-r--r-- root wheel 10/23/2019 17:41 1735 rpc
-rw-r--r-- root wheel  7/25/2017 18:37 1735 rpc~previous
-rw-r--r-- root wheel 10/23/2019 18:42  891 rtadvd.conf
-rw-r--r-- root wheel  8/24/2017 21:54  891 rtadvd.conf~previous

```

现在属于输出的一部分的新属性包括：
  * **UnixMode** 是 Unix 系统上表示的文件权限
  * **用户** 是文件所有者
  * **Group** 是组所有者
  * **大小** 是 Unix 系统上表示的文件或目录的大小


注释
此功能已从实验性迁移到 PowerShell 7.1 中的主流。
### 示例 11：获取交接点的链接目标
Windows Command Shell 中的 `dir` 命令显示文件系统连接点的目标位置。 在 PowerShell 中，此信息可从 返回的文件系统对象的 `Get-ChildItem` 属性中获取，并显示在默认输出中。

```
PS D:\> New-Item -ItemType Junction -Name tmp -Target $Env:TEMP
PS D:\> Get-ChildItem | Select-Object Name, LinkTarget

Name     LinkTarget
----     ----------
tmp      C:\Users\user1\AppData\Local\Temp

PS D:\> Get-ChildItem

    Directory: D:\

Mode          LastWriteTime    Length Name
----          -------------    ------ ----
l----   12/16/2021  9:29 AM           tmp -> C:\Users\user1\AppData\Local\Temp

```

### 示例 12：获取 AppX 重新分析点的链接目标
此示例尝试获取 AppX 重新分析点的目标信息。 Microsoft Store 应用程序会在用户的 AppData 目录中创建 AppX 重新分析点。

```
Get-ChildItem ~\AppData\Local\Microsoft\WindowsApps\MicrosoftEdge.exe |
    Select-Object Mode, LinkTarget, LinkType, Name

```

```
Mode  LinkTarget LinkType Name
----  ---------- -------- ----
la---                     MicrosoftEdge.exe

```

目前，Windows 不提供用于获取 AppX 重新分析点的目标信息的方法。 **LinkTarget** 和 **LinkType** 文件系统对象的属性为空。
### 示例 13：使用筛选器仅获取目录中的日志文件

```
# Returns only .log files in C:\Test (filtering is performed by the FileSystem provider)
Get-ChildItem -Path C:\Test -Filter '*.log'

# Returns only .log files in C:\Test (filtering is performed by Get-ChildItem after the
# FileSystem provider enumerates all files)
Get-ChildItem -Path C:\Test -Include '*.log'

```

## 参数
### -Attributes
注释
此参数仅在 [FileSystem](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6) 提供程序中可用。
获取具有指定属性的文件和文件夹。 此参数支持所有属性，并允许指定属性的复杂组合。
例如，若要获取加密或压缩的非系统文件（而不是目录），请键入：
`Get-ChildItem -Attributes !Directory+!System+Encrypted, !Directory+!System+Compressed`
若要查找具有常用属性的文件和文件夹，请使用 **Attributes** 参数。 或者，**Directory** 、**File** 、**Hidden** 、**ReadOnly** 和 **System** 的参数。
**Attributes** 参数支持以下值：
  * `Archive`
  * `Compressed`
  * `Device`
  * `Directory`
  * `Encrypted`
  * `Hidden`
  * `IntegrityStream`
  * `Normal`
  * `NoScrubData`
  * `NotContentIndexed`
  * `Offline`
  * `ReadOnly`
  * `ReparsePoint`
  * `SparseFile`
  * `System`
  * `Temporary`


有关这些属性的说明，请参阅 [FileAttributes](https://learn.microsoft.com/zh-cn/dotnet/api/system.io.fileattributes) 枚举。
若要组合属性，请使用以下运算符：
  * `!` （不）
  * `+`（和）
  * `,`（或）


请勿在运算符及其属性之间使用空格。 逗号后可以使用空格。
对于常见属性，请使用以下缩写：
  * `D`（目录）
  * `H`（隐藏）
  * `R`（只读）
  * `S`（系统）


#### 参数属性  
| 类型:  |  [FlagsExpression<T>](https://learn.microsoft.com/zh-cn/dotnet/api/system.management.automation.flagsexpression-1)[[FileAttributes](https://learn.microsoft.com/zh-cn/dotnet/api/system.io.fileattributes)]  |  
| --- | --- |  
| 默认值:  | None  |  
| 接受的值:  | Archive, Compressed, Device, Directory, Encrypted, Hidden, IntegrityStream, Normal, NoScrubData, NotContentIndexed, Offline, ReadOnly, ReparsePoint, SparseFile, System, Temporary  |  
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
### -CodeSigningCert
注释
此参数仅在 [证书](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.security/about/about_certificate_provider?view=powershell-7.6) 提供程序中可用。
若要获取 `Code Signing` 属性值中具有 的证书列表，请使用 **CodeSigningCert** 参数。
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
### -Depth
此参数已添加到 PowerShell 5.0 中，使你能够控制递归深度。 默认情况下，`Get-ChildItem` 显示父目录的内容。 **Depth** 参数确定递归中包含的子目录级别数，并显示内容。
例如，`-Depth 2` 包括 **Path** 参数的目录、第一级子目录和第二级子目录。 默认情况下，输出中包含目录名称和文件名。
注释
在 Windows 计算机的 PowerShell 或 **cmd.exe** 中，可以使用 **tree.com** 命令显示目录结构的图形视图。
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
### -Directory
注释
此参数仅在 [FileSystem](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6) 提供程序中可用。
若要获取目录列表，请使用 **Directory** 参数或具有 **Directory** 属性的 **Attributes** 参数。 可以将 **Recurse** 参数与 **Directory** 配合使用。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | 广告  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -DnsName
注释
此参数仅在 [证书](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.security/about/about_certificate_provider?view=powershell-7.6) 提供程序中可用。
指定与 cmdlet 获取的证书 **DNSNameList** 属性匹配的域名或名称模式。 此参数的值可以是 `Unicode` 或 `ASCII`。 Punycode 值将转换为 Unicode。 允许使用通配符字符（`*`）。
此参数在 PowerShell 7.1 中重新引入
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -DocumentEncryptionCert
注释
此参数仅在 [证书](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.security/about/about_certificate_provider?view=powershell-7.6) 提供程序中可用。
若要获取 `Document Encryption` 属性值中具有 的证书列表，请使用 **DocumentEncryptionCert** 参数。
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
### -Eku
注释
此参数仅在 [证书](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.security/about/about_certificate_provider?view=powershell-7.6) 提供程序中可用。
指定与 cmdlet 所获取证书的 **EnhancedKeyUsageList** 属性相匹配的文本或文本模式。 允许使用通配符字符（`*`）。 **EnhancedKeyUsageList** 属性包含 EKU 的易记名称和 OID 字段。
此参数在 PowerShell 7.1 中重新引入
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Exclude
指定一个或多个字符串模式的数组，用于在 cmdlet 获取子项时匹配。 输出中排除了任何匹配项。 输入路径元素或模式，例如 `*.txt` 或 `A*`。 允许使用通配符。
`*` 参数中的尾随星号（）是可选的。 例如，`-Path C:\Test\Logs` 或 `-Path C:\Test\Logs\*`。 如果包含尾随星号（`*`），该命令将递归到 **Path** 参数的子目录中。 如果没有星号（`*`），将显示 **Path** 参数的内容。 示例 5 和 Notes 部分包含更多详细信息。
**包含** 和**排除** 参数在文件枚举后由 PowerShell 应用。 这两个参数可以一起使用。 但是，排除是在包含之后应用的，这可能会影响最终输出。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -ExpiringInDays
注释
此参数仅在 [证书](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.security/about/about_certificate_provider?view=powershell-7.6) 提供程序中可用。
指定该 cmdlet 只返回将在指定天数内或之前过期的证书。 值为零（`0`）获取已过期的证书。
此参数在 PowerShell 7.1 中重新引入
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
### -File
注释
此参数仅在 [FileSystem](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6) 提供程序中可用。
若要获取文件列表，请使用 **File** 参数。 可以将 **Recurse** 参数与 **File** 一起使用。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | af  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Filter
指定筛选器以限定 **Path** 参数。 FileSystem 提供程序是唯一支持筛选器的已安装 PowerShell 提供程序。 筛选器比其他参数更高效。 提供程序在 cmdlet 获取对象时应用筛选器，而不是在检索对象后让 PowerShell 筛选对象。
筛选器字符串将传递给 .NET API 以枚举文件。 该参数仅接受单个字符串。 **Filter** 参数的值可以包含通配符，但 API 仅支持`*`和`?`通配符。
**Include** 和 **Exclude** 参数支持`*`和`?`通配符模式，`[]`并且可以接受字符串数组。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | 1  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -FollowSymlink
注释
此参数仅在 [FileSystem](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6) 提供程序中可用。
默认情况下，`Get-ChildItem` cmdlet 显示递归期间发现的目录的符号链接，但不会递归到这些目录。 使用 **FollowSymlink** 参数搜索由这些符号链接指向的目录。 **FollowSymlink** 是动态参数，仅在 **FileSystem** 提供程序中受支持。
此参数是在 PowerShell 6.0 中引入的。
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
### -Force
允许该 cmdlet 获取用户无法访问的项，例如隐藏文件或系统文件。 **Force** 参数不会替代安全限制。 实现因提供程序而异。 有关详细信息，请参阅 [about_Providers](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.6)。
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
### -Hidden
注释
此参数仅在 [FileSystem](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6) 提供程序中可用。
若要仅获取隐藏的项，请使用 **Hidden** 参数或具有 **Hidden** 属性的 **Attributes** 参数。 默认情况下，`Get-ChildItem` 不显示隐藏的项。 使用 **Force** 参数获取隐藏项。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | ah, h  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Include
指定一个或多个字符串模式的数组，用于在 cmdlet 获取子项时匹配。 输出中包含所有匹配的项目。 输入路径元素或模式，例如 `"*.txt"`。 允许使用通配符。 仅当命令包含某项的内容（例如 ，其中通配符指定 `C:\Windows\*` 目录的内容）时，`C:\Windows` 参数才有效。
**包含** 和**排除** 在文件枚举后由 PowerShell 应用。 这两个参数可以一起使用。 但是，排除是在包含之后应用的，这可能会影响最终输出。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -LiteralPath
指定要搜索的一个或多个位置或目标路径的路径。 **LiteralPath** 的值严格按照所键入的形式使用。 不会将任何字符解释为通配符。 如果路径包含转义字符，请将它括在单引号中。 单引号指示 PowerShell 不要将任何字符解释为转义序列。
有关详细信息，请参阅 [about_Quoting_Rules](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-7.6)。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | PSPath, LP  |  
#### 参数集
LiteralItems   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | True  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -Name
仅获取位置中的项的名称。 输出是一个字符串对象，可以将管道向下发送到其他命令。 返回的名称与 **Path** 参数的值相对。
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
### -Path
指定要搜索的一个或多个位置或目标路径的路径。 如果未指定，则目标路径为当前目录（`.`）。 可以使用通配符。 将 **Path** 参数与 **Recurse** 参数一起使用时，请使用谨慎。 有关详细信息，请参阅本文的 [NOTES](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6#notes) 部分。
#### 参数属性  
| 类型:  |  [String](https://learn.microsoft.com/zh-cn/dotnet/api/system.string)[]  |  
| --- | --- |  
| 默认值:  | Current directory  |  
| 支持通配符:  | True  |  
| 不显示:  | False  |  
#### 参数集
Items   
| Position:  | 0  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | True  |  
| 来自管道的值（按属性名称）:  | True  |  
| 来自剩余参数的值:  | False  |  
### -ReadOnly
注释
此参数仅在 [FileSystem](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6) 提供程序中可用。
若要仅获取只读项，请使用 **ReadOnly** 参数或 **Attributes** 参数 **ReadOnly** 属性。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | ar  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -Recurse
获取指定位置及其所有子项中的项。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | False  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | s, r  |  
#### 参数集
(All)   
| Position:  | Named  |  
| --- | --- |  
| 必需:  | False  |  
| 来自管道的值:  | False  |  
| 来自管道的值（按属性名称）:  | False  |  
| 来自剩余参数的值:  | False  |  
### -SSLServerAuthentication
注释
此参数仅在 [证书](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.security/about/about_certificate_provider?view=powershell-7.6) 提供程序中可用。
若要获取 `Server Authentication` 属性值中具有 的证书列表，请使用 **SSLServerAuthentication** 参数。
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
### -System
注释
此参数仅在 [FileSystem](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_filesystem_provider?view=powershell-7.6) 提供程序中可用。
仅获取系统文件和目录。 若要仅获取系统文件和文件夹，请使用 **System** 参数或 **Attributes** 参数中的 **System** 属性。
#### 参数属性  
| 类型:  |  
| --- |  
| 默认值:  | None  |  
| 支持通配符:  | False  |  
| 不显示:  | False  |  
| 别名:  | as  |  
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
可以通过管道将包含路径的字符串传递给此 cmdlet。
## 输出
cmdlet 在访问 `Alias:` 驱动器时输出此类型。
###  [X509StoreLocation](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.powershell.commands.x509storelocation)
###  [X509Certificate2](https://learn.microsoft.com/zh-cn/dotnet/api/system.security.cryptography.x509certificates.x509certificate2)
cmdlet 在访问 `Cert:` 驱动器时输出这些类型。
###  [DictionaryEntry](https://learn.microsoft.com/zh-cn/dotnet/api/system.collections.dictionaryentry)
cmdlet 在访问 `Env:` 驱动器时输出此类型。
###  [DirectoryInfo](https://learn.microsoft.com/zh-cn/dotnet/api/system.io.directoryinfo)
cmdlet 在访问 FileSystem 驱动器时输出这些类型。
###  [FunctionInfo](https://learn.microsoft.com/zh-cn/dotnet/api/system.management.automation.functioninfo)
###  [FilterInfo](https://learn.microsoft.com/zh-cn/dotnet/api/system.management.automation.filterinfo)
该 cmdlet 在访问 `Function:` 驱动器时输出这些类型。
###  [RegistryKey](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.win32.registrykey)
该 cmdlet 在访问注册表驱动器时输出此类型。
###  [PSVariable](https://learn.microsoft.com/zh-cn/dotnet/api/system.management.automation.psvariable)
cmdlet 在访问 `Variable:` 驱动器时输出此类型。
###  [WSManConfigContainerElement](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.wsman.management.wsmanconfigcontainerelement)
###  [WSManConfigLeafElement](https://learn.microsoft.com/zh-cn/dotnet/api/microsoft.wsman.management.wsmanconfigleafelement)
该 cmdlet 在访问 `WSMan:` 驱动器时输出这些类型。
使用 **Name** 参数时，此 cmdlet 将对象名称作为字符串返回。
## 备注
PowerShell 包含以下与 `Get-ChildItem`相关的别名：
  * 所有平台：
    * `dir`、`gci`
  * 窗户： 


**带参数的`-Path` 递归行为：**
将 `Get-ChildItem -Recurse` 与 **Path** 参数一起使用时，cmdlet 将搜索最后一个路径组件，无论它是通配符模式还是文本名称。
  * 如果最后一个路径组件与目标目录的现有直接子目录匹配，则 cmdlet 对匹配目录执行递归枚举。
  * 如果最后一个路径组件与目标目录的现有直接子目录不匹配，则 cmdlet 以递归方式搜索目标目录层次结构中与最后一个路径组件匹配的项


将 `Get-ChildItem -Recurse` 与 **Path** 和 **Name** 参数一起使用时，行为会发生变化。 该命令在目标目录的直接子项中搜索最后一个路径组件。
  * 如果直接子项之间存在匹配项，则 cmdlet 对匹配项执行递归枚举。 通配符匹配仅在目标目录的顶层发生一次。 结果将像单独传递到 **LiteralPath** 参数一样进行处理。
  * 如果最后一个路径组件与顶层的任何项不匹配，则会发生错误。


应避免将 **Path** 参数与 **Recurse** 参数一起使用。 为了获得最佳结果：
  * 使用 **LiteralPath** 指定目标目录，以避免触发对最后一个路径组件的递归搜索。
  * 使用 **筛选器** 或 **包括** 参数来指定应在目标目录层次结构的每个级别中搜索的通配符或文本模式。


## 相关链接
  * [about_Certificate_Provider](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.security/about/about_certificate_provider?view=powershell-7.6)
  * [about_Registry_Provider](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_registry_provider?view=powershell-7.6)


在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/powershell/scripting/community/contributing/powershell-style-guide)。 
PowerShell 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.6) [ 提供产品反馈 ](https://github.com/PowerShell/PowerShell/issues/new/choose)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
