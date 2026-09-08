---
url: "https://www.ventoy.net/cn/doc_start.html"
title: "Get start . Ventoy"
scraped_at: 2026-09-08T14:36:07+00:00
---

新一代多系统启动U盘解决方案
  * [Ventoy Compatible](https://www.ventoy.net/cn/compatible.html)


  * 最新资讯 
  * 使用说明 
    * [Linux 图形化界面 — GTK/QT](https://www.ventoy.net/cn/doc_linux_gui.html)
    * [Linux 图形化界面 — WebUI](https://www.ventoy.net/cn/doc_linux_webui.html)
    * [启动 Ventoy Vlnk 文件](https://www.ventoy.net/cn/doc_vlnk.html)
    * [Ventoy LiveCD](https://www.ventoy.net/cn/doc_livecd.html)
    * [Secure Boot (安全启动)说明](https://www.ventoy.net/cn/doc_secure.html)
    * [ARM64 UEFI 支持](https://www.ventoy.net/cn/doc_aarch64.html)
    * [MIPS64 UEFI 支持](https://www.ventoy.net/cn/doc_mips64el.html)
    * [控制 Ventoy 搜索路径方法总结](https://www.ventoy.net/cn/doc_search_path.html)
    * [Ventoy 启动 OpenWrt 说明](https://www.ventoy.net/cn/doc_openwrt.html)
    * [Ventoy2Disk.exe 安装失败处理方法](https://www.ventoy.net/cn/doc_ventoy2disk.html)
    * [Ventoy2Disk.exe 升级失败处理方法](https://www.ventoy.net/cn/doc_fail_update.html)
    * [FydeOS/CloudReady 说明](https://www.ventoy.net/cn/doc_chrome_os.html)
    * [如何往 Linux Live 系统中注入文件](https://www.ventoy.net/cn/doc_live_injection.html)
    * [替换ISO文件启动菜单背景图片](https://www.ventoy.net/cn/doc_boot_background.html)
    * [关于 VentoyAutoRun.bat](https://www.ventoy.net/cn/doc_inject_autorun.html)
    * [ISO 文件名中的特殊标识说明](https://www.ventoy.net/cn/doc_name_identifier.html)
    * [如何删除 Ventoy 安全启动 Key](https://www.ventoy.net/cn/doc_delete_key.html)
    * [Ventoy 菜单多语言支持](https://www.ventoy.net/cn/doc_menu_language.html)
    * [Ventoy 启动联想 Recovery 镜像说明](https://www.ventoy.net/cn/doc_lenovo_recovery.html)
    * [Ventoy Linux Remount](https://www.ventoy.net/cn/doc_linux_remount.html)
  * Ventoy内部原理 
    * [Ventoy MBR & GPT 格式对比](https://www.ventoy.net/cn/doc_mbr_vs_gpt.html)
    * [Legacy BIOS 访问范围限制](https://www.ventoy.net/cn/doc_legacy_limit.html)
    * [Ventoy启动Windows/WinPE时花屏](https://www.ventoy.net/cn/doc_fuzzy_screen.html)
  * 插件说明 
      * [ Windows VHD 启动插件](https://www.ventoy.net/cn/plugin_vhdboot.html)
      * [ Linux vDisk 启动插件](https://www.ventoy.net/cn/plugin_vtoyboot.html)
      * [ Driver Update Disk 插件](https://www.ventoy.net/cn/plugin_dud.html)
  * Ventoy Compatible 
    * [Ventoy参数如何传递给操作系统](https://www.ventoy.net/cn/doc_compatible_pass.html)
    * [Ventoy Compatible标志](https://www.ventoy.net/cn/doc_compatible_mark.html)
  * 其他 


## Ventoy使用说明
下载安装包，例如 ventoy-1.0.00-windows.zip 然后解压开。 直接执行 `Ventoy2Disk.exe` 如下图所示，选择磁盘设备，然后点击 `安装` 按钮即可。  说明：默认的 `Ventoy2Disk.exe` 是32位x86程序，同时支持最常见的32位和64位Windows系统，绝大部分情况下使用它就可以。 从1.0.58版本开始，Ventoy还同时提供了 `Ventoy2Disk_X64.exe/Ventoy2Disk_ARM.exe/Ventoy2Disk_ARM64.exe` 可以根据需要使用。 这些文件位于安装包内的`altexe`目录下，使用时需要将其拷贝到上一层目录（即和 `Ventoy2Disk.exe` 同一位置）。 
安装包内 Ventoy 版本：当前安装包中的Ventoy版本号  设备内部 Ventoy 版本：U盘中已安装的Ventoy版本号，如果为空则表示U盘内没有安装Ventoy  左侧显示的 MBR/GPT：用户当前选择的分区格式，可以在选项中修改，只对安装过程有效。  右侧显示的 MBR/GPT：设备当前使用的分区格式 （也就是当初安装Ventoy时选择的分区格式），如果U盘内没有安装Ventoy，则会显示空。  左侧显示的 exFAT/NTFS/FAT32：用户当前选择的Ventoy分区文件系统类型，可以在选项中修改，只对安装过程有效。  右侧显示的 exFAT/NTFS/FAT32：当前设备中Ventoy分区的文件系统类型。如果当前设备中没有安装Ventoy，则显示为空。  安装：把Ventoy安装到U盘，只有第一次的时候需要，其他情况就只需要升级即可  升级：升级U盘中的Ventoy版本，升级不会影响已有的ISO文件 
  1. 如果Ventoy2Disk.exe安装或升级一直提示失败，请参考 [说明](https://www.ventoy.net/cn/doc_ventoy2disk.html)
  2. Ventoy可以安装在U盘上，也可以安装在本地硬盘上。为防止误操作，默认只会列出U盘，你可以勾选 `配置选项-->显示所有设备` 这个选项。 此时会列出包括系统盘在内的所有磁盘，但此时你自己务必要小心操作，不要选错盘。 
  3. MBR/GPT 分区格式选项只在安装时会用，升级的时候是不管的，也就是说升级是不会改变现有分区格式的，必须重新安装才可以。
  4. 安装完之后，U盘存放镜像文件的Ventoy分区也可以再次手动格式化。支持 exFAT/FAT32/NTFS/UDF/XFS/Ext2/3/4 系统。对于普通U盘建议使用exFAT文件系统，对于大容量的移动硬盘、本地硬盘、SSD等建议使用NTFS文件系统。


  * 2. Windows 系统安装 Ventoy —— 命令行界面


从 Ventoy 1.0.86 版本开始，也支持在命令行模式下执行安装、升级。请参考 [Windows 命令行](https://www.ventoy.net/cn/doc_windows_cli.html)
  * 3. Linux系统安装 Ventoy —— 图形化界面


方式1，请参考 [Linux 图形化界面 — GTK/QT](https://www.ventoy.net/cn/doc_linux_gui.html) 方式2，请参考 [Linux 图形化界面 — WebUI](https://www.ventoy.net/cn/doc_linux_webui.html)
  * 4. Linux系统安装 Ventoy —— 命令行界面


下载安装包，例如 ventoy-1.0.00-linux.tar.gz, 然后解压开. 在终端以root权限执行 ` sudo sh Ventoy2Disk.sh -i /dev/XXX ` 其中 /dev/XXX 是U盘对应的设备名，比如 /dev/sdb 

```
Ventoy2Disk.sh  命令  [选项]  /dev/XXX
  命令含义:
    -i   安装ventoy到磁盘中 (如果对应磁盘已经安装了ventoy则会返回失败)
    -I   强制安装ventoy到磁盘中，(不管原来有没有安装过)
    -u   升级磁盘中的ventoy版本
    -l   显示磁盘中的ventoy相关信息
    
  选项含义: (可选)
    -r SIZE_MB  在磁盘最后保留部分空间，单位 MB (只在安装时有效)
    -s          启用安全启动支持 (默认是关闭的)
    -g          使用GPT分区格式，默认是MBR格式 (只在安装时有效)
    -L          主分区（镜像分区）的卷标 (默认是 Ventoy)

```

针对Linux系统有几点需要特殊说明一下： 1. 执行脚本时需要有root权限, 对一些系统比如ubuntu/deepin 执行的时候需要在前面加 sudo 比如 ` sudo sh Ventoy2Disk.sh -i /dev/sdb` 2. 必须cd到ventoy解压之后的目录下执行此脚本 3. 请务必输入正确的设备名称，ventoy不会检查你输入的设备是U盘还是本地硬盘，如果输错了有可能会把你的系统盘格式化掉哦！ 
请注意：选择安装的时候，磁盘将会被格式化，里面所有的数据都会丢失！ 你只需要安装一次Ventoy即可，剩下的就只需要把各种ISO/WIM/VHD(x)/EFI文件拷贝到U盘中就可以了. 你也可以把它当成普通U盘使用，保存普通文件、图片或视频等，不会影响Ventoy的功能。 
  * 5. 拷贝镜像文件


安装完成之后，U盘会被分成两个分区（参考 [说明](https://www.ventoy.net/cn/doc_disk_layout.html)）。 其中第1个分区（就是容量大的那个分区，也可以称之为 镜像分区）将会被格式化为exFAT文件系统（你也可以再手动重新格式化成其他支持的文件系统，比如 NTFS/FAT32/UDF/XFS/Ext2/3/4 等，参考 [说明](https://www.ventoy.net/cn/doc_disk_layout.html)）， 你只需要把ISO/WIM等文件拷贝到这里面即可。你可以把文件放在任意目录以及子目录下。 Ventoy默认会遍历所有的目录和子目录，找出所有的镜像文件，并按照字母排序之后显示在菜单中。 你可以通过插件配置让Ventoy只搜索某一个固定的目录，或是跳过某些特殊目录等。 详细的控制 Ventoy 搜索路径的方法请参考 [控制 Ventoy 搜索路径方法总结](https://www.ventoy.net/cn/doc_search_path.html)
  * 6. 升级 Ventoy


如果Ventoy发布了新版本之后，你可以点击 `升级` 按钮进行升级，或者Linux系统中使用 -u 选项进行升级。 需要说明的是，升级操作是安全的，不会影响现有的镜像文件，也不会重新把镜像分区改成exFAT格式。 你可以认为升级只是把第二个分区（32MB的VTOYEFI分区）内的Ventoy启动文件覆盖了，不会动到镜像分区，因此镜像文件不会丢失。 即使你当初安装完成之后，把镜像分区重新格式化为了NTFS，升级的时候也不会再改回exFAT。 
ventoy.net (website) Copyright © 2020-2026 longpanda Mail all comments and suggestions to longpanda admin@ventoy.net
