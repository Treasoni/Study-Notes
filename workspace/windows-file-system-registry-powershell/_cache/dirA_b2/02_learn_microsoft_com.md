---
url: "https://learn.microsoft.com/zh-cn/windows/deployment/usmt/usmt-recognized-environment-variables"
title: "识别的环境变量 | Microsoft Learn"
scraped_at: 2026-09-10T15:41:14+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows/deployment/usmt/usmt-recognized-environment-variables) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows/deployment/usmt/usmt-recognized-environment-variables)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# 识别的环境变量
  * 适用于: ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client)


使用 XML 文件 `MigDocs.xml`、 `MigApp.xml`和 `MigUser.xml` 时，环境变量可用于标识不同计算机上可能不同的文件夹。 CSIDL) 值 (常量特殊项 ID 列表提供了一种标识应用程序经常使用但在任何给定计算机上可能具有不同名称或位置的文件夹的方法。 例如， **Documents** 文件夹可能位于 `C:\Users\<Username>\Documents` 一台计算机和 `C:\Users\<Username>\My Documents` 另一台计算机上。 星号 (*) 通配符可以在 和 `MigApp.xml``MigDoc.xml` 文件中使用`MigUser.xml`。 但是，不能在文件中使用 `Config.xml` 星号 (*) 通配符。
## 在作系统和每个用户的上下文中处理的变量
这些变量可以在具有 `context=UserAndSystem`、 `context=User`和 `context=System`**的.xml** 文件中的节内使用。  
| 变量  | 说明  |  
| --- | --- |  
|  _ALLUSERSAPPDATA_  | 与 **CSIDL_COMMON_APPDATA** 相同。  |  
|  _ALLUSERSPROFILE_  | 引用 `%PROFILESFOLDER%\Public` 或 `%PROFILESFOLDER%\all users`。  |  
|  _COMMONPROGRAMFILES_  | 与 **CSIDL_PROGRAM_FILES_COMMON** 相同。  |  
|  _COMMONPROGRAMFILES_ (X86)   | 指 `C:\Program Files (x86)\Common Files` 64 位系统上的文件夹。  |  
|  _CSIDL_COMMON_ADMINTOOLS_  | 版本 10.0。 包含计算机所有用户的管理工具的文件系统目录。  |  
|  _CSIDL_COMMON_ALTSTARTUP_  | 与所有用户的非本地化启动程序组对应的文件系统目录。  |  
|  _CSIDL_COMMON_APPDATA_  | 包含所有用户的应用程序数据的文件系统目录。 Windows 的典型路径是 `C:\ProgramData`。  |  
|  _CSIDL_COMMON_DESKTOPDIRECTORY_  | 文件系统目录，其中包含所有用户在桌面上显示的文件和文件夹。 典型路径为 `C:\Users\Public\Desktop`。  |  
|  _CSIDL_COMMON_DOCUMENTS_  | 包含所有用户通用文档的文件系统目录。 典型路径为 `C:\Users\Public\Documents`。  |  
|  _CSIDL_COMMON_FAVORITES_  | 文件系统目录，用作所有用户共有的收藏夹的通用存储库。 典型路径为 C：\Users\Public\Favorites。  |  
|  _CSIDL_COMMON_MUSIC_  | 文件系统目录，用作所有用户通用的音乐文件的存储库。 典型路径为 `C:\Users\Public\Music`。  |  
|  _CSIDL_COMMON_PICTURES_  | 文件系统目录，用作所有用户通用的映像文件的存储库。 典型路径为 `C:\Users\Public\Pictures`。  |  
|  _CSIDL_COMMON_PROGRAMS_  | 文件系统目录，其中包含所有用户在 **“开始”** 菜单上显示的常见程序组的目录。 典型路径为 `C:\ProgramData\Microsoft\Windows\Start Menu\Programs`。  |  
|  _CSIDL_COMMON_STARTMENU_  | 文件系统目录，其中包含所有用户显示在 **“开始** ”菜单上的程序和文件夹。 Windows 中的一个典型路径是 `C:\ProgramData\Microsoft\Windows\Start Menu`。  |  
|  _CSIDL_COMMON_STARTUP_  | 文件系统目录，其中包含所有用户的“启动”文件夹中显示的程序。 典型路径为 `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup`。  |  
|  _CSIDL_COMMON_TEMPLATES_  | 包含可供所有用户使用的模板的文件系统目录。 典型路径为 `C:\ProgramData\Microsoft\Windows\Templates`。  |  
|  _CSIDL_COMMON_VIDEO_  | 用作所有用户通用视频文件的存储库的文件系统目录。 典型路径为 `C:\Users\Public\Videos`。  |  
|  _CSIDL_DEFAULT_APPDATA_  | 引用 中的`Appdata``%DEFAULTUSERPROFILE%`文件夹。  |  
| C _SIDL_DEFAULT_LOCAL_APPDATA_  | 引用 中的`%DEFAULTUSERPROFILE%`本地`Appdata`文件夹。  |  
|  _CSIDL_DEFAULT_COOKIES_  | 引用 中的 `%DEFAULTUSERPROFILE%`Cookies 文件夹。  |  
|  _CSIDL_DEFAULT_CONTACTS_  | 引用 中的 `%DEFAULTUSERPROFILE%`“联系人”文件夹。  |  
|  _CSIDL_DEFAULT_DESKTOP_  | 引用 中的 `%DEFAULTUSERPROFILE%`Desktop 文件夹。  |  
|  _CSIDL_DEFAULT_DOWNLOADS_  | 引用 中的 `%DEFAULTUSERPROFILE%`Downloads 文件夹。  |  
|  _CSIDL_DEFAULT_FAVORITES_  | 引用 中的 `%DEFAULTUSERPROFILE%`“收藏夹”文件夹。  |  
|  _CSIDL_DEFAULT_HISTORY_  | 引用 中的 `%DEFAULTUSERPROFILE%`“历史记录”文件夹。  |  
|  _CSIDL_DEFAULT_INTERNET_CACHE_  | 指 中的 `%DEFAULTUSERPROFILE%`Internet 缓存文件夹。  |  
|  _CSIDL_DEFAULT_PERSONAL_  | 指 中的 `%DEFAULTUSERPROFILE%`“个人”文件夹。  |  
|  _CSIDL_DEFAULT_MYDOCUMENTS_  | 引用 中的 `%DEFAULTUSERPROFILE%`Documents 文件夹。  |  
|  _CSIDL_DEFAULT_MYPICTURES_  | 引用 中的 `%DEFAULTUSERPROFILE%`“图片”文件夹。  |  
|  _CSIDL_DEFAULT_MYMUSIC_  | 引用 中的 `%DEFAULTUSERPROFILE%`“音乐”文件夹。  |  
|  _CSIDL_DEFAULT_MYVIDEO_  | 引用 中的 `%DEFAULTUSERPROFILE%`“视频”文件夹。  |  
|  _CSIDL_DEFAULT_RECENT_  | 引用 中的 `%DEFAULTUSERPROFILE%`“最近”文件夹。  |  
|  _CSIDL_DEFAULT_SENDTO_  | 引用 中的 `%DEFAULTUSERPROFILE%`“发送到”文件夹。  |  
|  _CSIDL_DEFAULT_STARTMENU_  | 引用 中的 `%DEFAULTUSERPROFILE%`“开始菜单”文件夹。  |  
|  _CSIDL_DEFAULT_PROGRAMS_  | 引用 中的 `%DEFAULTUSERPROFILE%`“程序”文件夹。  |  
|  _CSIDL_DEFAULT_STARTUP_  | 指 中的 `%DEFAULTUSERPROFILE%`Startup 文件夹。  |  
|  _CSIDL_DEFAULT_TEMPLATES_  | 引用 中的 `%DEFAULTUSERPROFILE%`Templates 文件夹。  |  
|  _CSIDL_DEFAULT_QUICKLAUNCH_  | 引用 中的 `%DEFAULTUSERPROFILE%`“快速启动”文件夹。  |  
|  _CSIDL_FONTS_  | 包含字体的虚拟文件夹。 典型路径为 `C:\Windows\Fonts`。  |  
|  _CSIDL_PROGRAM_FILESX86_  | 64 位系统上的 Program Files 文件夹。 典型路径为 `C:\Program Files (x86)`。  |  
|  _CSIDL_PROGRAM_FILES_COMMONX86_  | 跨 64 位系统上的应用程序共享的组件的文件夹。 典型路径为 `C:\Program Files (x86)\Common`。  |  
|  _CSIDL_PROGRAM_FILES_  | Program Files 文件夹。 典型路径为 `C:\Program Files`。  |  
|  _CSIDL_PROGRAM_FILES_COMMON_  | 跨应用程序共享的组件的文件夹。 典型路径为 `C:\Program Files\Common`。  |  
|  _CSIDL_RESOURCES_  | 包含资源数据的文件系统目录。 典型路径为 `C:\Windows\Resources`。  |  
|  _CSIDL_SYSTEM_  | Windows 系统文件夹。 典型路径为 `C:\Windows\System32`。  |  
|  _CSIDL_WINDOWS_  | Windows 目录或系统根路径。 此值对应于 `%WINDIR%` 或 `%SYSTEMROOT%` 环境变量。 典型路径为 `C:\Windows`。  |  
|  _DEFAULTUSERPROFILE_  | 引用 中的 `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList [DefaultUserProfile]`值。  |  
|  _PROFILESFOLDER_  | 引用 中的 `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList [ProfilesDirectory]`值。  |  
|  _PROGRAMFILES_  | 与 **CSIDL_PROGRAM_FILES** 相同。  |  
|  _PROGRAMFILES (X86)_  | 指 `C:\Program Files (x86)` 64 位系统上的文件夹。  |  
| 引用 `%WINDIR%\system32`。  |  
|  _SYSTEM16_  | 引用 `%WINDIR%\system`。  |  
|  _SYSTEM32_  | 引用 `%WINDIR%\system32`。  |  
|  _SYSTEMDRIVE_  | 保存 Windows 文件夹的驱动器。 此值是驱动器名称，而不是文件夹名称 (`C:` 不 `C:\`) 。  |  
|  _SYSTEMPROFILE_  | 引用 中的 `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\S-1-5-18 [ProfileImagePath]`值。  |  
|  _SYSTEMROOT_  | 与 **WINDIR** 相同。  |  
|  _WINDIR_  | 指位于系统驱动器上的 Windows 文件夹。  |  
## 仅在用户上下文中识别的变量
这些变量可以在具有 `context=User` 和 `context=UserAndSystem`的节中的 **.xml** 文件中使用。  
| 变量  | 说明  |  
| --- | --- |  
|  _APPDATA_  | 与 **CSIDL_APPDATA** 相同。  |  
|  _CSIDL_ADMINTOOLS_  | 用于存储单个用户的管理工具的文件系统目录。 Microsoft管理控制台 (MMC) 将自定义主机保存到此目录，该目录随用户配置文件漫游。  |  
|  _CSIDL_ALTSTARTUP_  | 与用户的未本地化启动程序组对应的文件系统目录。  |  
|  _CSIDL_APPDATA_  | 用作应用程序特定数据的通用存储库的文件系统目录。 典型路径为 `C:\Users\<username>\AppData\Roaming`。  |  
|  _CSIDL_BITBUCKET_  | 包含用户回收站中的对象的虚拟文件夹。  |  
|  _CSIDL_CDBURN_AREA_  | 充当等待写入 CD 的文件的暂存区域的文件系统目录。 典型路径为 `C:\Users\<username>\AppData\Local\Microsoft\Windows\MasteredBurning\Disc Burning`。  |  
|  _CSIDL_CONNECTIONS_  | 表示包含网络和拨号连接的网络Connections的虚拟文件夹。  |  
|  _CSIDL_CONTACTS_  | 此值引用 **%CSIDL_PROFILE%** 中的“联系人”文件夹。  |  
|  _CSIDL_CONTROLS_  | 包含控制面板项图标的虚拟文件夹。  |  
|  _CSIDL_COOKIES_  | 用作 Internet Cookie 通用存储库的文件系统目录。 典型路径为 `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Cookies`。  |  
|  _CSIDL_DESKTOP_  | 表示 Windows 桌面的虚拟文件夹。  |  
|  _CSIDL_DESKTOPDIRECTORY_  | 用于在桌面上物理存储文件对象的文件系统目录，不应将其与桌面文件夹本身混淆。 典型路径为 `C:\Users\<username>\Desktop`。  |  
|  _CSIDL_DRIVES_  | 表示**此电脑** 的虚拟文件夹，其中包含本地计算机上的一切内容：存储设备、打印机和控制面板。 该文件夹还可以包含映射的网络驱动器。  |  
|  _CSIDL_FAVORITES_  | 用作用户收藏夹的通用存储库的文件系统目录。 典型路径为 `C:\Users\<username>\Favorites`。  |  
|  _CSIDL_HISTORY_  | 用作 Internet 历史记录项的通用存储库的文件系统目录。  |  
|  _CSIDL_INTERNET_  | Internet Explorer 的虚拟文件夹。  |  
|  _CSIDL_INTERNET_CACHE_  | 用作临时 Internet 文件的通用存储库的文件系统目录。 典型路径为 `C:\Users\<username>\AppData\Local\Microsoft\Windows\Temporary Internet Files`  |  
|  _CSIDL_LOCAL_APPDATA_  | 充当本地非漫游应用程序的数据存储库的文件系统目录。 典型路径为 `C:\Users\<username>\AppData\Local`。  |  
|  _CSIDL_MYDOCUMENTS_  | 表示 **Documents** 文件夹的虚拟文件夹。典型路径为 `C:\Users\<username>\Documents`。  |  
|  _CSIDL_MYMUSIC_  | 用作音乐文件的通用存储库的文件系统目录。 典型路径为 `C:\Users\<username>\Music`。  |  
|  _CSIDL_MYPICTURES_  | 用作映像文件的通用存储库的文件系统目录。 典型路径为 `C:\Users\<username>\Pictures`。  |  
|  _CSIDL_MYVIDEO_  | 用作视频文件的通用存储库的文件系统目录。 典型路径为 `C:\Users\<username>\Videos`。  |  
|  _CSIDL_NETHOOD_  | 一个文件系统目录，其中包含可能存在于 **网络** 虚拟文件夹中的链接对象。 它与表示网络命名空间根目录 _的 CSIDL_NETWORK_ 不同。 典型路径为 `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Network Shortcuts`。  |  
|  _CSIDL_NETWORK_  | 表示网络桌面项（ **网络** 命名空间层次结构的根目录）的虚拟文件夹。  |  
|  _CSIDL_PERSONAL_  | 表示**用户 >桌面项的<**虚拟文件夹。 此值等效于 **CSIDL_MYDOCUMENTS** 。 典型路径为 `C:\User\<username>\Documents`。  |  
|  _CSIDL_PLAYLISTS_  | 用于存储播放专辑的虚拟文件夹，通常 `C:\Users\<username>\Music\Playlists`为 。  |  
|  _CSIDL_PRINTERS_  | 包含已安装打印机的虚拟文件夹。  |  
|  _CSIDL_PRINTHOOD_  | 文件系统目录，其中包含可存在于打印机虚拟文件夹中的链接对象。 典型路径为 `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Printer Shortcuts`。  |  
|  _CSIDL_PROFILE_  | 用户的配置文件文件夹。 典型路径为 `C:\Users\<username>`。  |  
|  _CSIDL_PROGRAMS_  | 包含用户程序组（即文件系统目录）的文件系统目录。 典型路径为 `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs`。  |  
|  _CSIDL_RECENT_  | 包含用户最近使用的文档的快捷方式的文件系统目录。 典型路径为 `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Recent`。  |  
|  _CSIDL_SENDTO_  | 包含 **“发送到”** 菜单项的文件系统目录。 典型路径为 `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\SendTo`。  |  
|  _CSIDL_STARTMENU_  | 包含 **“开始”** 菜单项的文件系统目录。 典型路径为 `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu`。  |  
|  _CSIDL_STARTUP_  | 与用户的启动程序组对应的文件系统目录。 典型路径为 `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`。  |  
|  _CSIDL_TEMPLATES_  | 用作文档模板的通用存储库的文件系统目录。 典型路径为 `C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Templates`。  |  
|  _HOMEPATH_  | 与标准环境变量相同。  |  
| 计算机上的临时文件夹。 典型路径为 `%USERPROFILE%\AppData\Local\Temp`。  |  
|  _TMP_  | 计算机上的临时文件夹。 典型路径为 `%USERPROFILE%\AppData\Local\Temp`。  |  
|  _USERPROFILE_  | 与 **CSIDL_PROFILE** 相同。  |  
|  _USERSID_  | 表示当前用户帐户安全标识符 (SID) 。 例如，`S-1-5-21-1714567821-1326601894-715345443-1026`。  |  
## 相关文章
[USMT XML 参考](https://learn.microsoft.com/zh-cn/windows/deployment/usmt/usmt-xml-reference)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-01-29 


