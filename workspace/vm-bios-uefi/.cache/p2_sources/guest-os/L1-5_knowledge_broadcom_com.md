---
url: "https://knowledge.broadcom.com/external/article/408976/windows-11-installation-fails-on-esxi-70.html"
title: "Windows 11 Installation Fails on ESXi 7.0U3 – \"This PC Doesn't Currently Meet Windows 11 System Requirements\""
scraped_at: 2026-09-17T16:08:58+00:00
---

Cookie Settings
Windows 11 Installation Fails on ESXi 7.0U3 – "This PC Doesn't Currently Meet Windows 11 System Requirements"
search cancel
Search 
### Windows 11 Installation Fails on ESXi 7.0U3 – "This PC Doesn't Currently Meet Windows 11 System Requirements"
book
#### Article ID: 408976
calendar_today
#### Updated On: 
Feedback Subscribe
#### Products
VMware vSphere ESXi
Show More Show Less
#### Issue/Introduction
When deploying a Windows 11 virtual machine (VM) from a template on ESXi 7.0U3q, the installation fails during boot with the following error:
"This PC doesn't currently meet Windows 11 system requirements."
#### Environment
ESXi 7.x
#### Cause
Windows 11 enforces strict hardware requirements that must be met by the virtual machine. If any of these prerequisites are missing or misconfigured, the installation will fail.
#### Resolution
Ensure the following minimum requirements are met when deploying a Windows 11 VM on ESXi 7.0U3:
1) **VM Hardware Compatibility** : Use hardware version 14 or later.
2) **Firmware Type** : Set to EFI (this is VMware’s term for UEFI).
3) **Secure Boot** : Must be enabled in VM settings.
4) **vTPM (Virtual TPM)** : Required for Windows 11. This needs VM encryption, which in turn requires a Key Management Server (KMS).
5) **RAM** : Minimum 4 GB (8 GB+ recommended).
6) **Storage** : Minimum 64 GB virtual disk.
7) **ISO** : Use the official Windows 11 ISO from Microsoft.
#### Additional Information
If vTPM cannot be added due to missing encryption support, configure a Key Management Server (KMS) in vCenter to enable VM encryption.
Refer to VMware by Broadcom's official documentation for [Windows 11 support on vSphere](https://www.vmware.com/docs/windows-11-support-on-vsphere).
#### Feedback
thumb_up Yes
thumb_down No
Powered by
