---
url: "https://ventoy.net/cn/doc_disk_layout.html"
title: "disk_layout . Ventoy"
scraped_at: 2026-09-08T14:36:07+00:00
---

新一代多系统启动U盘解决方案
  * [Ventoy Compatible](https://ventoy.net/cn/compatible.html)


  * 最新资讯 
  * 使用说明 
    * [Linux 图形化界面 — GTK/QT](https://ventoy.net/cn/doc_linux_gui.html)
    * [Linux 图形化界面 — WebUI](https://ventoy.net/cn/doc_linux_webui.html)
    * [启动 Ventoy Vlnk 文件](https://ventoy.net/cn/doc_vlnk.html)
    * [Ventoy LiveCD](https://ventoy.net/cn/doc_livecd.html)
    * [Secure Boot (安全启动)说明](https://ventoy.net/cn/doc_secure.html)
    * [ARM64 UEFI 支持](https://ventoy.net/cn/doc_aarch64.html)
    * [MIPS64 UEFI 支持](https://ventoy.net/cn/doc_mips64el.html)
    * [控制 Ventoy 搜索路径方法总结](https://ventoy.net/cn/doc_search_path.html)
    * [Ventoy 启动 OpenWrt 说明](https://ventoy.net/cn/doc_openwrt.html)
    * [Ventoy2Disk.exe 安装失败处理方法](https://ventoy.net/cn/doc_ventoy2disk.html)
    * [Ventoy2Disk.exe 升级失败处理方法](https://ventoy.net/cn/doc_fail_update.html)
    * [FydeOS/CloudReady 说明](https://ventoy.net/cn/doc_chrome_os.html)
    * [如何往 Linux Live 系统中注入文件](https://ventoy.net/cn/doc_live_injection.html)
    * [替换ISO文件启动菜单背景图片](https://ventoy.net/cn/doc_boot_background.html)
    * [关于 VentoyAutoRun.bat](https://ventoy.net/cn/doc_inject_autorun.html)
    * [ISO 文件名中的特殊标识说明](https://ventoy.net/cn/doc_name_identifier.html)
    * [如何删除 Ventoy 安全启动 Key](https://ventoy.net/cn/doc_delete_key.html)
    * [Ventoy 菜单多语言支持](https://ventoy.net/cn/doc_menu_language.html)
    * [Ventoy 启动联想 Recovery 镜像说明](https://ventoy.net/cn/doc_lenovo_recovery.html)
    * [Ventoy Linux Remount](https://ventoy.net/cn/doc_linux_remount.html)
  * Ventoy内部原理 
    * [Ventoy MBR & GPT 格式对比](https://ventoy.net/cn/doc_mbr_vs_gpt.html)
    * [Legacy BIOS 访问范围限制](https://ventoy.net/cn/doc_legacy_limit.html)
    * [Ventoy启动Windows/WinPE时花屏](https://ventoy.net/cn/doc_fuzzy_screen.html)
  * 插件说明 
      * [ Windows VHD 启动插件](https://ventoy.net/cn/plugin_vhdboot.html)
      * [ Linux vDisk 启动插件](https://ventoy.net/cn/plugin_vtoyboot.html)
      * [ Driver Update Disk 插件](https://ventoy.net/cn/plugin_dud.html)
  * Ventoy Compatible 
    * [Ventoy参数如何传递给操作系统](https://ventoy.net/cn/doc_compatible_pass.html)
    * [Ventoy Compatible标志](https://ventoy.net/cn/doc_compatible_mark.html)
  * 其他 


## Ventoy MBR格式U盘分区布局
上面是一个安装了Ventoy的32GB U盘的分区示意图。你可以看到，整个U盘被分成了2个分区（MBR格式）。 
  * 为什么选择MBR格式


为了能支持Legacy BIOS模式，只能选择MBR分区格式
  * 关于分区1


Ventoy 将U盘的第一个分区默认格式化为exFAT文件系统来存放ISO文件。exFAT文件系统有比较好的跨平台特性而且也比较适合U盘。 从 Ventoy-1.0.11 版本开始，你也可以自己手动再把第一个分区重新格式化为其他文件系统。当前支持的文件系统有: exFAT/FAT32/NTFS/UDF/XFS/Ext2/Ext3/Ext4  需要说明的是，如果选择 XFS/Ext2/Ext3/Ext4 文件系统，则U盘正常是无法在Windows上使用的，也无法用来安装Windows系统，这个比较适合纯Linux的场景。 
  * 关于分区2


首先，在UEFI模式下必须要有一个EFI系统分区才可以启动，而且这个分区必须是FAT格式的文件系统。这个是UEFI规范的强制性要求，必须遵守。 所以第二个分区就是这个EFI系统分区，用来保存UEFI模式下的启动文件以及Ventoy的其他文件。这些文件都比较小，所以这个分区只分配了32MB的空间就够了。 其实，这个EFI系统分区可以是第一个分区，也可以是第二个分区。这里把它放在第二个分区，纯粹是因为在某些早期版本的Windows系统中，只有U盘的第一个分区才能挂载使用， 后面的分区是看不到的。当然，第二个分区不可见对于Ventoy来说也是件好事，可以防止用户误操作。 这个分区很小，是用来保存Ventoy的核心文件的，所以用户最好不要对其做改动。 
  * 关于1MB的间隙


这部分空间是用来存放Legacy BIOS模式下的启动文件的 
## 保留空间
从 1.0.14 版本开始，Ventoy支持在安装时在磁盘最后保留一部分空间。下图为一个安装了Ventoy的32GB U盘的分区示意图（2GB的保留空间）。 
在安装时可以在 “选项配置” ---> “分区设置” 中设置要保留的空间大小 (Linux版本是 -r 选项)。注意保留空间只在安装时有效，升级时不关注此项。 
  1. 保留空间只能位于磁盘的最后面，不能是前面或中间位置
  2. 分区1和分区2是Ventoy创建的两个分区，这两个分区不能动，不能修改他们的位置或大小
  3. 可以使用保留空间创建分区3和分区4，这两个分区可以自由使用，不影响Ventoy功能


ventoy.net (website) Copyright © 2020-2026 longpanda Mail all comments and suggestions to longpanda admin@ventoy.net
