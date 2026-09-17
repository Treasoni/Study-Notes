---
url: "https://knowledge.broadcom.com/external/article/384912/"
title: "Virtual Machine fails to boot when changing the Firmware from BIOS to EFI"
scraped_at: 2026-09-17T16:08:58+00:00
---

Cookie Settings
Virtual Machine fails to boot when changing the Firmware from BIOS to EFI
search cancel
Search 
### Virtual Machine fails to boot when changing the Firmware from BIOS to EFI
book
#### Article ID: 384912
calendar_today
#### Updated On: 
Feedback Subscribe
#### Products
VMware vSphere ESXi VMware vCenter Server
Show More Show Less
#### Issue/Introduction
  * Virtual Machine will fail to boot after changing the Firmware from BIOS to EFI or from EFI to BIOS. 
  * VM will fail to boot with following error message on the Console : 


#### Environment
VMware vSphere ESXi 7.x VMware vSphere ESXi 8.x 
VMware vCenter Server 7.x VMware vCenter Server 8.x 
#### Cause
This is an expected behavior as changing the firmware is not supported since BIOS uses **MBR (Master Boot Record)** partitioning and EFI requires **GPT (GUID Partition Table)** partitioning on the VM disks. While changing the Firmware, a warning is also displayed that the installed guest operating system might become unbootable. 
#### Resolution
To make it work, we have the following options : 
  * Rebuild the VM by choosing EFI/BIOS as firmware and attach the same hard disks to it to make it bootable.
  * Convert the VM's disks to GPT before switching to EFI. This can be done by tools like **mbr2gpt.exe** in Windows and needs to be supported by Guest OS vendor, refer to the following [article](https://learn.microsoft.com/en-us/windows/deployment/mbr-to-gpt). 


#### Feedback
thumb_up Yes
thumb_down No
Powered by
