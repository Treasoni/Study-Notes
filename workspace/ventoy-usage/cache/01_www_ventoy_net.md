---
url: "https://www.ventoy.net/en/doc_secure.html"
title: "secure . Ventoy"
scraped_at: 2026-09-08T14:36:07+00:00
---

A New Bootable USB Solution
  * [Experience Sharing](https://www.ventoy.net/en/experience.html)


  * News 
  * How to use 
    * [Windows Command Line](https://www.ventoy.net/en/doc_windows_cli.html)
    * [Linux GUI -- GTK/QT](https://www.ventoy.net/en/doc_linux_gui.html)
    * [Linux GUI -- WebUI](https://www.ventoy.net/en/doc_linux_webui.html)
    * [Ventoy LiveCD](https://www.ventoy.net/en/doc_livecd.html)
    * [Secondary boot menu](https://www.ventoy.net/en/doc_secondary_boot_menu.html)
    * [Browse/Boot Files In Local Disk](https://www.ventoy.net/en/doc_browser.html)
    * [Boot Ventoy Vlnk File](https://www.ventoy.net/en/doc_vlnk.html)
    * [About Secure Boot](https://www.ventoy.net/en/doc_secure.html)
    * [IA32 UEFI Support](https://www.ventoy.net/en/doc_ia32.html)
    * [ARM64 UEFI Support](https://www.ventoy.net/en/doc_aarch64.html)
    * [MIPS64 UEFI Support](https://www.ventoy.net/en/doc_mips64el.html)
    * [Ventoy Search Configuration](https://www.ventoy.net/en/doc_search_path.html)
    * [About OpenWrt](https://www.ventoy.net/en/doc_openwrt.html)
    * [About WIMBOOT Mode](https://www.ventoy.net/en/doc_wimboot.html)
    * [About GRUB2 Mode](https://www.ventoy.net/en/doc_grub2boot.html)
    * [When Ventoy2Disk.exe Failed To Install](https://www.ventoy.net/en/doc_ventoy2disk.html)
    * [When Ventoy2Disk.exe Failed To Update](https://www.ventoy.net/en/doc_fail_update.html)
    * [About the Github CI release](https://www.ventoy.net/en/doc_github_ci.html)
    * [About FydeOS/CloudReady](https://www.ventoy.net/en/doc_chrome_os.html)
    * [Inject files to Linux Live OS](https://www.ventoy.net/en/doc_live_injection.html)
    * [Replace ISO boot menu background](https://www.ventoy.net/en/doc_boot_background.html)
    * [About VentoyAutoRun.bat](https://www.ventoy.net/en/doc_inject_autorun.html)
    * [About file checksum](https://www.ventoy.net/en/doc_checksum.html)
    * [Non-destructive Installation](https://www.ventoy.net/en/doc_non_destructive.html)
    * [About USB hardware problem](https://www.ventoy.net/en/doc_fake_usb.html)
    * [Special identifier in ISO name](https://www.ventoy.net/en/doc_name_identifier.html)
    * [Delete Ventoy Secure Boot Key](https://www.ventoy.net/en/doc_delete_key.html)
    * [Ventoy Menu Multi-Language](https://www.ventoy.net/en/doc_menu_language.html)
    * [Ventoy Ctrl Settings Menu](https://www.ventoy.net/en/doc_ctrl_settings.html)
    * [Ventoy Linux Remount](https://www.ventoy.net/en/doc_linux_remount.html)
  * How Ventoy works 
    * [Ventoy Composition](https://www.ventoy.net/en/doc_composition.html)
    * [Disk Layout In MBR](https://www.ventoy.net/en/doc_disk_layout.html)
    * [Disk Layout In GPT](https://www.ventoy.net/en/doc_disk_layout_gpt.html)
    * [Ventoy MBR & GPT](https://www.ventoy.net/en/doc_mbr_vs_gpt.html)
    * [About Legacy BIOS Limitation](https://www.ventoy.net/en/doc_legacy_limit.html)
    * [About Fuzzy Screen for WinPE](https://www.ventoy.net/en/doc_fuzzy_screen.html)
  * Ventoy Plugin 
    * [Plugin Entrypoint](https://www.ventoy.net/en/plugin_entry.html)
    * [Multi-Mode Option](https://www.ventoy.net/en/plugin_dual_option.html)
    * [About Path Matching](https://www.ventoy.net/en/plugin_path_match.html)
      * [ Global Control Plugin](https://www.ventoy.net/en/plugin_control.html)
      * [ Image List Plugin](https://www.ventoy.net/en/plugin_imagelist.html)
      * [ Menu Class Plugin](https://www.ventoy.net/en/plugin_menuclass.html)
      * [ Menu Alias Plugin](https://www.ventoy.net/en/plugin_menualias.html)
      * [ Menu Tip Plugin](https://www.ventoy.net/en/plugin_menutip.html)
      * [ Menu Extension Plugin](https://www.ventoy.net/en/plugin_grubmenu.html)
      * [ Auto Installation Plugin](https://www.ventoy.net/en/plugin_autoinstall.html)
      * [ Injection Plugin](https://www.ventoy.net/en/plugin_injection.html)
      * [ Persistence Plugin](https://www.ventoy.net/en/plugin_persistence.html)
      * [ Wimboot Plugin](https://www.ventoy.net/en/plugin_wimboot.html)
      * [ Windows Vhdboot Plugin](https://www.ventoy.net/en/plugin_vhdboot.html)
      * [ Linux vDisk boot Plugin](https://www.ventoy.net/en/plugin_vtoyboot.html)
      * [ Auto Memdisk Plugin](https://www.ventoy.net/en/plugin_automemdisk.html)
      * [ Boot Conf Replace Plugin](https://www.ventoy.net/en/plugin_bootconf_replace.html)
      * [ Driver Update Disk Plugin](https://www.ventoy.net/en/plugin_dud.html)
      * [ Password Plugin](https://www.ventoy.net/en/plugin_password.html)
  * Ventoy Compatible 
    * [Ventoy information format](https://www.ventoy.net/en/doc_compatible_format.html)
    * [How information passed to OS](https://www.ventoy.net/en/doc_compatible_pass.html)
    * [How to mount the iso file](https://www.ventoy.net/en/doc_compatible_mount.html)
    * [How to mark as Ventoy Compatible](https://www.ventoy.net/en/doc_compatible_mark.html)
  * Miscellaneous 
    * [Ventoy License](https://www.ventoy.net/en/doc_license.html)


## About Secure Boot in UEFI mode
Attention: For some computers you must enable `Allow Microsoft 3rd Part UEFI CA` option in the UEFI firmware to make Ventoy boot. 
Secure Boot was supported by default from Ventoy 1.0.76, an option for secure boot is added in Ventoy2Disk.exe/Ventoy2Disk.sh. Menu `Option-->Secure Boot Support` for Ventoy2Disk.exe and `-s` option for Ventoy2Disk.sh  Attention: Ventoy default policy is fully bypass secure boot which means all EFI files can be booted without any check. If you still want to follow the UEFI secure boot policy, you can set Ventoy Global Control Plugin Option. For details please refer [Ventoy Secure Boot Policy](https://github.com/ventoy/Ventoy/blob/master/SecureBoot.md) In theory, Ventoy can boot fine no matter whether the secure boot in the BIOS is enabled or disabled. If the secure boot is enabled in the BIOS, the following screen should be displayed when boot Ventoy at thte first time. Please follow the guid bellow.
However the solution is not perfect enough. If you get some error screen instead of the above blue screen (for example, Linpus lite xxxx). It means that the secure boot solution doesn't work with your machine, so you need to turn off the option, and disable secure boot in the BIOS. 
Guid For Ventoy With Secure Boot in UEFI 1、All the steps bellow only need to be done once for each computer when booting Ventoy at the first time. 2、Since Ventoy 1.1.13+ you need to enroll a new key for the UEFI CA 2023 issue. 
## Enroll Key
ventoy.net (website) Copyright © 2020-2026 longpanda Mail all comments and suggestions to longpanda admin@ventoy.net
