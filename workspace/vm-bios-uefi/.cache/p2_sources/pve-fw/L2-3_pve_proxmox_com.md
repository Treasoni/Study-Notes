---
url: "https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries"
title: "OVMF/UEFI Boot Entries - Proxmox VE"
scraped_at: 2026-09-17T16:09:45+00:00
---

# OVMF/UEFI Boot Entries
From Proxmox VE
[Jump to navigation](https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries#mw-head) [Jump to search](https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries#searchInput)
## Contents
  * [1 Introduction](https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries#Introduction)
  * [2 Add a Boot Option](https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries#Add_a_Boot_Option)
    * [2.1 Short How-To](https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries#Short_How-To)
    * [2.2 Detailed How-To](https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries#Detailed_How-To)
  * [3 References](https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries#References)


## Introduction
If a VM boots via OVMF (UEFI), the firmware has to know which bootloader it has to start from the ESP. When no boot entries exist in the EFIVARS store, it tries to load the fallback `$ESP/EFI/BOOT/BOOTX64.efi` loader. Should that also fail, the VM gets booted into the EFI Shell 
## Add a Boot Option
### Short How-To
  1. Start-up the VM and press ESC exactly once when the splash screen appears. 
     * On current versions of Proxmox VE, select the "EFI Firmware Setup" entry to get into the OVMF menu.
     * On older versions of Proxmox VE, you should be in the OVMF menu already.
  2. Then "Boot Maintenance Manager" -> "Boot Options" -> "Add Boot Option" -> choose Disk with the EFI System Partition.
  3. Now find the EFI executable, for example for Debian: `EFI/debian/grubx64.efi` or for Fedora: `EFI/fedora/shimx64-fedora.efi`.
  4. Name it ("Input the description") and "Commit Change"
  5. Use "Change Boot Order" to order the new entry to the top.


### Detailed How-To
To add an entry of an existing bootloader go into the OVMF menu. Press 'ESC' exactly once during boot when the splash screen appears. On current versions of Proxmox VE, select the 'EFI Firmware Setup' entry. On older versions of Proxmox VE, you are already in the OVMF menu after pressing escape. Then select 'Boot Maintenance Manager': 
Select 'Boot Options': 
Select 'Add Boot Option': 
Choose the Hard Drive with the ESP: 
Navigate the folder structure to your bootloader (EFI/debian/shimx64.efi in this example) 
→ → 
After that, enter a name and commit: 
→ → 
To make it the default boot entry, you now have to change the boot order: 
Press enter, select the boot entry with the arrow keys and move it up and down with '+' and '-' respectively. Then press enter again and commit your changes: 
The last step is to reset the VM via OVMF, after that it should boot using the just configured boot entry. 
## References
  1. <https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface>
  2. EFI System Partition. <https://en.wikipedia.org/wiki/EFI_system_partition>


Retrieved from "[https://pve.proxmox.com/mediawiki/index.php?title=OVMF/UEFI_Boot_Entries&oldid=12527](https://pve.proxmox.com/mediawiki/index.php?title=OVMF/UEFI_Boot_Entries&oldid=12527)"
[Category](https://pve.proxmox.com/wiki/Special:Categories "Special:Categories"): 


Cookies help us deliver our services. By using our services, you agree to our use of cookies.
## Navigation menu
### Search
