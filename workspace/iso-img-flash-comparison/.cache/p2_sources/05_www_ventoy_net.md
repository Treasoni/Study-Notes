---
url: "https://www.ventoy.net/cn/doc_openwrt.html"
title: "openwrt . Ventoy"
scraped_at: 2026-09-09T15:13:52+00:00
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


## Ventoy 启动 OpenWrt 说明
  * 背景介绍 


Ventoy 从 1.0.41 版本支持 OpenWrt 的 IMG 镜像的启动。但需要一些特殊处理，在这里进行说明。  注意：使用时首先要确保 OpenWrt 的 IMG 镜像直接烧录到你的 U 盘上在你当前测试的机器上是可以正常启动的。 如果直接烧录启动都有问题，那说明镜像不支持当前的硬件环境，那可能就不是 Ventoy 的问题了。 
  * ventoy_openwrt.xz 插件


由于目前 OpenWrt 镜像中并没有打包 Ventoy 所需的 dm 内核模块，所以需要下载 `ventoy_openwrt.xz` 这个插件放到U盘里才可以正常启动。 这个插件其实就是把 OpenWrt 官网上的内核模块文件打包了一下而已，下载链接如下： <https://github.com/ventoy/OpenWrtPlugin/releases> 注意随着OpenWrt版本更新，这个文件会经常更新，请保持使用最新版本。 在U盘第1个分区（容量大的、保存镜像文件的分区）的根目录下新建一个 `ventoy`（全小写）目录，然后把这个文件下载下来，放在这个目录下。 （如果你熟悉Ventoy的插件，则此文件就是放在和 `ventoy.json` 同一个位置。关于 ventoy.json 的位置以及相关说明，请参考 [ 插件入口 ](https://www.ventoy.net/cn/plugin_entry.html)） 
  * 支持的 IMG 镜像类型


Ventoy 只支持 x86 类型的 `combined-ext4.img` 和 `combined-squashfs.img` 这两种 OpenWrt 镜像。 对于 `combined-ext4.img` 类型，直接从官网下载到 gzip 压缩包解压后即可启动。 对于 `combined-squashfs.img` 类型，从官网下载后需要处理一下才可以，详见本文后面的说明。 
  * combined-squashfs.img 的处理


`combined-squashfs.img` 类型的镜像从官网下载之后，需要使用 `ventoy_openwrt_squashfs.sh` 脚本处理后才可以使用 Ventoy 启动。 此脚本也是从上面那个链接中下载，使用方法如下： 

```
sh ventoy_openwrt_squashfs.sh  openwrt-xxx-combined-squashfs.img.gz

例如：
sh ventoy_openwrt_squashfs.sh  openwrt-19.07.7-x86-64-combined-squashfs.img.gz

```

在上例中，脚本处理完之后会生成 `openwrt-19.07.7-x86-64-combined-squashfs.img` 文件，将此文件拷贝到 Ventoy U盘中即可启动。 
ventoy.net (website) Copyright © 2020-2026 longpanda Mail all comments and suggestions to longpanda admin@ventoy.net
