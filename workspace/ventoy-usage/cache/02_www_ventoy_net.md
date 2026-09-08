---
url: "https://www.ventoy.net/en/faq.html"
title: "FAQ . Ventoy"
scraped_at: 2026-09-08T14:36:07+00:00
---

A New Bootable USB Solution
  * [Experience Sharing](https://www.ventoy.net/en/experience.html)


##  Collapse All [ - ](javascript:) Expand All [ + ](javascript:)
## . Installation FAQ [ - ](javascript:)
  1. Can I install Ventoy to local disk ? 
Yes ! You can install Ventoy to USB drive, Removable HD, SD Card, SATA HDD, SSD, NVMe ... In Windows, Ventoy2Disk.exe will only list the device removable and in USB interface type by default. If you want you can toggle `Show all devices` option, then all the devices will be in the list. In this case you must take care about the list and make sure to select the right disk. In Linux, you need to specify the device to install Ventoy which can be a USB drive or local disk. It should be specially noted that, no matter USB drive or local disk, all the data will be lost after install Ventoy, please be very careful.
  2. Ventoy2Disk.exe can't enumerate my USB device
In Windows, some processes will occupy the USB drive, and Ventoy2Disk.exe cannot obtain the control right of the USB drive, so that the device cannot be listed. Some known process are as follows: 1. Paragon ExtFS for Windows 2. ParagonMounter 3. DokanMounter 4. ext2fsd 5. extservice 6. DiskGenius 7. DSAService.exe (Intel® Driver & Support Assistant). 
  3. Ventoy2Disk.exe always failed to install ?
Please refer [When Ventoy2Disk.exe Failed to Install](https://www.ventoy.net/en/doc_ventoy2disk.html)
  4. Ventoy2Disk.exe always failed to update ?
Please refer [When Ventoy2Disk.exe Fail to Update](https://www.ventoy.net/en/doc_fail_update.html)
  5. Can I reformat the 1st (bigger) partition ?
Yes. You can reformat it with FAT32/NTFS/UDF/XFS/Ext2/Ext3/Ext4 filesystem, the only request is that Cluster Size must greater than or equal to 2048. You can use these commands to format it: 1. Format NTFS in Windows: format x: /fs:ntfs /q 2. Format UDF in Windows: format x: /fs:udf /q 3. Format Ext4 in Linux: sudo mkfs -t ext4 /dev/sdb1 4. Format XFS in Linux: sudo mkfs -t xfs /dev/sdb1 
  6. How to recover VTOYEFI partition
Sometimes the VTOYEFI partition gets dead and that makes the device completely unbootable. You can recover the VTOYEFI partition with the following 2 steps: 1. Delete the broken VTOYEFI partition with some disk utility (e.g. diskgenius, diskpart ...) 2. Use [Ventoy Non-destructive Install](https://www.ventoy.net/en/doc_non_destructive.html)
  7. The USB partition shows very slow after install Ventoy
It may be related to the motherboard USB 2.0/3.0 port. Please refer [github issue/1975](https://github.com/ventoy/Ventoy/issues/1975)


## . Boot Process FAQ [ - ](javascript:)
  1. What kind of BIOS does Ventoy support ?
x86 Legacy BIOS, IA32 UEFI, x86_64 UEFI, ARM64 UEFI and MIPS64EL UEFI
  2. Can Ventoy select the BIOS mode ?
No! It's the BIOS that decides the boot mode not Ventoy. The BIOS decides to boot Ventoy in Legacy BIOS mode or in UEFI mode. 
  3. How to determine the current boot mode ?
After boot into the Ventoy main menu, pay attention to the lower left corner of the screen:  1.0.84 BIOS www.ventoy.net  ===> This means current is Legacy BIOS mode.  1.0.84 UEFI www.ventoy.net  ===> This means current is UEFI mode.  1.0.84 IA32 www.ventoy.net  ===> This means current is 32bit UEFI mode.  1.0.84 AA64 www.ventoy.net  ===> This means current is ARM64 UEFI mode.  1.0.84 MIPS www.ventoy.net  ===> This means current is MIPS64EL UEFI mode. 
  4. How to mount the ISO partition in Linux after boot ?
Please refer [Linux Remount](https://www.ventoy.net/en/doc_linux_remount.html)
  5. Can't boot in UEFI, some Secure error ?
Secure Boot is supported since Ventoy-1.0.07, please use the latest version and see the [Notes](https://www.ventoy.net/en/doc_secure.html).
  6. Fuzzy screen when booting Windows/WinPE
Please refer: [About Fuzzy Screen When Booting Window/WinPE](https://www.ventoy.net/en/doc_fuzzy_screen.html)
  7. Can't install Windows 7 ISO, no install media found ?
Most likely it was caused by the lack of USB 3.0 driver in the ISO.
  8. Checksum image file
When you run into problem when booting an image file, please make sure that the file is not corrupted. Please follow [About file checksum](https://www.ventoy.net/en/doc_checksum.html) to checksum the file. 
  9. Ventoy boot into grub shell
Ventoy's boot menu is not shown but with the following grub shell. 

```
                             GNU GRUB  version 2.04

   Minimal BASH-like line editing is supported. For the first word, TAB
   lists possible command completions. Anywhere else TAB lists possible
   device or file completions. ESC at any time exits.

grub>

```
The following situations may cause this phenomenon, please check one by one: 1. You have a fake/faulty USB stick. You can use some tools to test it. 2. Your computer's BIOS has a access range limitation. Please refer: [About Legacy BIOS Limitation](https://www.ventoy.net/en/doc_legacy_limit.html)
  10. Ventoy hang with the following message 

```
    Ventoy scanning files, please wait...

```
That's because there are too many files in the disk. Please refer: [Ventoy Search Configuration](https://www.ventoy.net/en/doc_search_path.html)
  11. Fuzzy Screen When Booting Window/WinPE
Please refer: [About Fuzzy Screen When Booting Window/WinPE](https://www.ventoy.net/en/doc_search_path.html)


## . Boot Menu FAQ [ - ](javascript:)
  1. Where can iso files be placed ?
You can put the iso file any where of the first partition. Ventoy will search all the directories and sub directories recursively to find all the iso files and list them in the boot menu.
  2. How to suppress iso files under specific directory ?
You can put a file with name `.ventoyignore` in the specific directory. When ventoy detects this file, it will not search the directory and all the subdirectories for iso files. 
  3. $xxx.iso was shown in boot menu
Probably you didn't delete the file completely but to the recycle bin. 
  4. ISO file name not displayed completely
If the ISO file name is too long to displayed completely. You can press left or right arrow keys ← → to scroll the menu. 


## . Plugin FAQ [ - ](javascript:)
  1. Where should ventoy.json be placed
ventoy.json should be placed at the 1st partition which has the larger capacity (The partition to store ISO files). Do NOT put the file to the 32MB VTOYEFI partition. After install, the 1st larger partition is empty, and no files or directories in it. You need to create a directory with name `ventoy` and put ventoy.json in this directory(that is \ventoy\ventoy.json). 


ventoy.net (website) Copyright © 2020-2026 longpanda Mail all comments and suggestions to longpanda admin@ventoy.net
