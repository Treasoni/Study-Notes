---
url: "https://learn.microsoft.com/zh-cn/windows/win32/fileio/maximum-file-path-limitation"
title: "最大路径长度限制 - Win32 apps | Microsoft Learn"
scraped_at: 2026-09-10T15:41:08+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows/win32/fileio/maximum-file-path-limitation) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows/win32/fileio/maximum-file-path-limitation)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# 最大路径长度限制
在 Windows API 中（以下段落中讨论了一些例外情况），路径的最大长度为 **MAX_PATH** ，此项被定义为 260 个字符。 系统按以下顺序构建本地路径：驱动器号、冒号、反斜杠、用反斜杠分隔的名称组件和终止 null 字符。 例如，驱动器 D 上的最大路径为“D:\_某个 256 个字符的路径字符串_ <NUL>”，其中“<NUL>”表示当前系统代码页的不可见终止 null 字符。 （<> 字符在此用于醒目用途，不能作为有效路径字符串的一部分。）
例如，如果要将具有长文件名的 Git 存储库克隆到本身具有长名称的文件夹中，则可能会遇到此限制。
注意
Windows API 中的文件 I/O 函数在将名称转换为 NT 样式名称的过程中会将“/”转换为“\”，但使用“\\\?\”前缀时除外，如以下小节中所述。
Windows API 的许多函数还具有 Unicode 版本，以允许最大总路径长度为 32,767 个字符的扩展长度路径。 此类型的路径由反斜杠分隔的组件组成，每个组件都取决于 _GetVolumeInformation_ 函数的 [lpMaximumComponentLength](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-getvolumeinformationa) 参数中返回的值（此值通常为 255 个字符）。 要指定扩展长度路径，请使用“\\\?\”前缀。 例如，“\\\?\D:\_非常长的路径_ ”。
注意
32,767 个字符的最大路径是近似值，因为系统可能会在运行时将“\\\?\”前缀扩展为更长的字符串，并且此扩展适用于总长度。
“\\\?\”前缀还可以用于根据通用命名约定 (UNC) 构建的路径。 要使用 UNC 指定此类路径，请使用“\\\?\UNC\”前缀。 例如，“\\\?\UNC\server\share”，其中“server”是计算机的名称，“share”是共享文件夹的名称。 这些前缀并不用作路径本身的一部分。 它们指示将路径传递给系统时修改量应最少，这意味着您不能用正斜杠来表示路径分隔符，不能用句点来表示当前目录，也不能用双点来表示父目录。 由于“\\\?\”前缀不能与相对路径一起使用，因此相对路径总字符数始终不能超过 **MAX_PATH** 个字符。
不需要对路径和文件名字符串执行任何 Unicode 规范化以供 Windows 文件 I/O API 函数使用，因为文件系统会将路径和文件名视为 **WCHAR** 的不透明序列。 在对相关 Windows 文件 I/O API 函数的任何调用的外部执行应用程序所需的任何规范化时，都应考虑到这一点。
使用 API 创建目录时，指定的路径不能太长以致于无法附加 8.3 文件名（即目录名不能超过 **MAX_PATH** 减 12）。
Shell 和文件系统有不同的要求。 可以使用 Shell 用户界面无法正确解释的 Windows API 来创建路径。
## 在 Windows 10 版本 1607 及更高版本中启用长路径
从 Windows 10 版本 1607 开始，许多常见的 Win32 文件和目录函数中删除了 **MAX_PATH** 限制。 但是，你的应用必须选择支持新行为。
要为每个应用程序启用新的长路径行为，必须满足两个条件。 必须设置注册表值，应用程序清单必须包含 `longPathAware` 元素。
### 用于启用长路径的注册表设置
重要
了解启用此注册表设置将只影响为利用新功能而修改的应用程序。 开发人员必须将其应用声明为可感知长路径，如[以下](https://learn.microsoft.com/zh-cn/windows/win32/fileio/maximum-file-path-limitation#application-manifest-updates-to-declare-long-path-capability)应用程序清单设置中所述。 这不是将影响所有应用程序的更改。
注册表值 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem LongPathsEnabled (Type: REG_DWORD)` 必须存在并设置为 `1`。 在首次调用受影响的 Win32 文件或目录函数后，系统（每个进程）将缓存此注册表值（请参见下面的函数列表）。 在进程的生存期内，将不会重新加载注册表值。 为了使系统上的所有应用都能识别该值，可能需要重新启动，因为某些进程可能在设置密钥之前已经启动。
你还可以将此代码复制到一个可以为你设置此项的 `.reg` 文件中，或者通过提升的特权在终端窗口中使用 PowerShell 命令：


```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem]
"LongPathsEnabled"=dword:00000001

```

```
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
-Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

```

注意
还可以在 `Computer Configuration > Administrative Templates > System > Filesystem > Enable Win32 long paths` 中通过组策略控制此注册表设置。 还可以使用 [策略配置服务提供程序（CSP）](https://learn.microsoft.com/zh-cn/windows/client-management/mdm/policy-configuration-service-provider)通过 Microsoft Intune 应用策略。
### 应用程序清单会更新以声明长路径功能
[应用程序清单](https://learn.microsoft.com/zh-cn/windows/win32/sbscs/application-manifests)还必须包含 `longPathAware` 元素。

```
<application xmlns="urn:schemas-microsoft-com:asm.v3">
    <windowsSettings xmlns:ws2="http://schemas.microsoft.com/SMI/2016/WindowsSettings">
        <ws2:longPathAware>true</ws2:longPathAware>
    </windowsSettings>
</application>

```

## 没有 MAX_PATH 限制的函数
如果你选择支持长路径行为，那么以下目录管理函数不再具有 **MAX_PATH** 限制：CreateDirectoryW、CreateDirectoryExW GetCurrentDirectoryW RemoveDirectoryW SetCurrentDirectoryW。
如果你选择支持长路径行为，那么以下文件管理函数不再具有 **MAX_PATH** 限制：CopyFileW、CopyFile2、CopyFileExW、CreateFileW、CreateFile2、CreateHardLinkW、CreateSymbolicLinkW、DeleteFileW、 FindFirstFileW、FindFirstFileExW、FindNextFileW、GetFileAttributesW、GetFileAttributesExW、SetFileAttributesW、GetFullPathNameW、GetLongPathNameW、MoveFileW、MoveFileExW、MoveFileWithProgressW、ReplaceFileW、SearchPathW、FindFirstFileNameW、FindNextFileNameW、FindFirstStreamW、FindNextStreamW、GetCompressedFileSizeW、GetFinalPathNameByHandleW。
## 另请参阅
[GetVolumeInformation](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-getvolumeinformationa)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2024-11-21 


