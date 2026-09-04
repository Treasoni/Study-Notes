---
url: "https://knowledge.broadcom.com/external/article?legacyId=2019649"
title: "Defragmenting and shrinking VMware Workstation virtual machine disks"
scraped_at: 2026-09-04T15:57:07+00:00
---

Cookie Settings
Defragmenting and shrinking VMware Workstation virtual machine disks
search cancel
Search 
### Defragmenting and shrinking VMware Workstation virtual machine disks
book
#### Article ID: 315631
calendar_today
#### Updated On: 
Feedback Subscribe
#### Products
VMware Desktop Hypervisor VMware Workstation 16.x Pro (for Windows) VMware Workstation 7 (for Linux) VMware Workstation Pro VMware Workstation Pro 15.x (for Windows)
Show More Show Less
#### Issue/Introduction
This article provides steps to reduce the size of a virtual disk (.vmdk) file so that it reflects the actual usage of the virtual machine.
#### Symptoms:
  * The virtual disk (.vmdk) file size on the host machine is larger than the actual space used on the non-preallocated virtual disk for a virtual machine.


#### Environment  
| 
  * VMware Workstation 10.x (Windows)
  * VMware Workstation 11.x (for Windows)
  * VMware Workstation Pro 16.x (Windows)
  * VMware Workstation 9.x (Windows)
  * VMware Workstation Pro 16.x (Linux)
  * VMware Workstation 8.x (Windows)
  * VMware Workstation Pro 15.x (Windows)
  * VMware Workstation 7.x (Windows)

 | 
  * VMware Workstation Pro 14.x (for Windows)
  * VMware Workstation Pro 12.x (Windows)
  * VMware Workstation Pro 15.x (Linux)
  * VMware Workstation Pro 12.x (Linux)
  * VMware Workstation Pro 14.x (for Linux)
  * VMware Workstation 7.x (Linux)
  * VMware Workstation 8.x (Linux)

 |  
| --- | --- |  
#### Resolution
Workstation virtual machines can be pre-allocated or sparse.
  * In a pre-allocated virtual machine, the size of the virtual disk file (or files, if you have chosen to split the virtual machine into 2GB files) is equal to the size of the virtual machine.
  * In a sparse virtual machine, the size of the virtual disk file (or files) is equal to the total used space of the virtual machine.


Your virtual machine bundle is always larger than the size of your virtual disks because the bundle contains snapshots, suspend state files (if the virtual machine is suspended), settings files, and logs. However, if the size of your virtual disks is significantly larger than the used space shown in the virtual machine's operating system, it is possible to reduce this size.
To reduce the size of the disk:
  1. Defragment the disk from Windows.
  2. Shrink the virtual disk using VMware Tools.
  3. Clean up the virtual disk from the host OS using the built-in Workstation utility.


**Note:** This process does not apply to pre-allocated disks.
To determine if your disk is sparse or pre-allocated, check the virtual disk settings:
  1. Launch Workstation.
  2. From the menu bar, click Virtual Machine > Settings.
  3. Click Hard Disk.
  4. View the details in Disk information.
  5. If your disk has snapshots, you must delete the snapshots before trying to reduce the size of the disk.


### Defragmenting within Windows
In a Windows virtual machine, you must first run a disk defragment from Windows. Defragmenting within Windows ensures that all of the used spaces are contiguous. You can then reduce the size of the virtual disk.
To run a disk defragment within Windows, follow the instructions from Microsoft:
  * Windows XP: [How to Defragment Your Disk Drive Volumes in Windows XP](http://support.microsoft.com/kb/314848)
  * Windows Vista: [Improve performance by defragmenting your hard disk](https://support.microsoft.com/en-us/windows/ways-to-improve-your-computer-s-performance-c6018c78-0edd-a71a-7040-02267d68ea90)
  * Windows 7: [Improve performance by defragmenting your hard disk](https://support.microsoft.com/en-us/windows/ways-to-improve-your-computer-s-performance-c6018c78-0edd-a71a-7040-02267d68ea90)
  * Windows 8: [Improve performance by defragmenting your hard disk](https://support.microsoft.com/en-us/windows/ways-to-improve-your-computer-s-performance-c6018c78-0edd-a71a-7040-02267d68ea90)
  * Windows 10: [Improve performance by defragmenting your hard disk](https://support.microsoft.com/en-us/windows/ways-to-improve-your-computer-s-performance-c6018c78-0edd-a71a-7040-02267d68ea90)


### Shrinking the virtual disk
After defragmenting the virtual disk, use VMware Tools to erase empty disk sectors at the end of the disk to free the unused space.
To shrink the virtual disk:
  1. Open the VMware Tools Control Panel / Toolbox: 
     * In Windows:Double-click the VMware Tools icon in the system tray, or click **Start > Control Panel > VMware Tools**. 
     * In Linux:Open the terminal and run this command:vmware-toolbox**Note:** In Workstation 9.x (Windows) and later, shrinking is automatically done while cleaning up the disk. Therefore, this option is removed from VMware Tools Panel. Go to **VM > Manage > Clean up Disks. **This is not available in Linux version of VMware Workstation 9.x and later. 
  2. Click the Shrink tab.
  3. Select the drive you want to shrink.
  4. Click **Prepare to Shrink** , then follow the onscreen instructions.


**Caution:** Do not shut down your virtual machine or the host machine while the disk is shrinking. In addition, do not try to cancel the process. Interrupting this process can cause irreparable damage to your virtual disk and you may not be able to start your virtual machine again.
#### Feedback
thumb_up Yes
thumb_down No
Powered by
