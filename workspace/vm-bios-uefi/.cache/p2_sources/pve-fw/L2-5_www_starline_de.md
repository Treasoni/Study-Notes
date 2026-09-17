---
url: "https://www.starline.de/en/magazine/technical-articles/best-practice-configurations-for-virtual-machines-on-proxmox-ve"
title: "Best Practice Configurations for Virtual Machines on Proxmox VE - Starline Computer: Storage und Server Lösungen von erfahrenen Experten"
scraped_at: 2026-09-17T16:09:45+00:00
---

[Homepage](https://www.starline.de/en) [Magazine](https://www.starline.de/en/magazine) [Technical Articles](https://www.starline.de/en/magazine/technical-articles) Best Practice Configurations for Virtual Machines on Proxmox VE
26 JUN 2026 
**The information provided here is based on practical experience and is intended to serve as a guide when setting up new VMs.**
##  General Preferences 
### Machine Type/Chipset
We generally recommend “**q35** ” as the machine type. This chipset already offers modern PCIe support and is a prerequisite for certain features, such as TPM 2.0 or PCIe passthrough.
### BIOS
For new VMs, we use**OVMF (UEFI)** provided that the guest operating system supports it. SeaBIOS should only be used for legacy systems or older operating system versions, but it is not strictly necessary.  
| **Setting**  | **Recommendation**  | **Hint**  |  
| --- | --- | --- |  
| Machine Type  | q35  | Modern PCIe Support  |  
| BIOS  | OVMF (UEFI)  | Legacy: SeaBIOS  |  
| SCSI controller  | VirtIO SCSI Single  | Beste Performance  |  
| Network card  | VirtIO (paravirtualized)  | Driver required  |  
### CPU
  * **The number of sockets should not exceed that of the host.**
  * The number of vCPUs should **not** exceed the number of host threads/cores. => In current Proxmox installations, this is no longer possible via the WebUI.
  * For the CPU type, we recommend**x86-64-v2-AES (or newer)** or **host**.
    * **host** : While this offers maximum performance, it limits live migration between different CPU generations. Additionally, this setting may cause issues with some operating systems.
    * **x86-64-v2-AES (or newer)** : This option provides a good balance between performance and migration compatibility. => Unless you need all of the host’s CPU flags, this is the recommended configuration. You should select the lowest common denominator as the type across the cluster. This can be done per node and indicates the maximum CPU type supported on that node:`wget -qO - https://cloud.starline.de/s/QmQt79dpJebtC46/download/checkCPUType.sh | awk -f -`
  * You should enable NUMA topology if the VM or host has more than one CPU socket. This allows Proxmox to keep a VM’s resources on a single NUMA node.


### RAM
  * You should define the size in increments of 1024. For example, 8 GB equals 8 × 1024 = 8192 GB, 16 GB equals 16384 GB, and so on.
  * **Ballooning** should always be enabled, but configured with a reasonable minimum value. <https://en.wikipedia.org/wiki/Memory_ballooning>
  * If you experience performance issues, you could try disabling ballooning, though this depends on the workload.
  * **Huge pages** can improve performance for memory-intensive workloads (host-side configuration required).


### Storage / Hard Drives
  * Controller: **VirtIO SCSI Single**
  * Disk Type: **SCSI**
  * Disk Format: **qcow2**(flexible, e.g., for snapshots, even under LVM (Technology Preview) or raw (maximum performance)
    * The supported format depends on the storage. See <https://pve.proxmox.com/wiki/Storage>
  * Enable **Discard** if the storage backend supports thin provisioning (e.g., ZFS, LVM-Thin, CEPH).
  * Enable **IO Threads** per Disk for better parallel I/O performance.
  * Enable SSD emulation if the underlying storage is an SSD or flash system.
  * Optional; does not provide any performance improvement and is relevant, for example, if the guest OS expects an SSD.


### Network
  * Network model: **VirtIO (paravirtualized)** for optimal performance.
  * Leave the MTU set to **1500** , unless the network supports jumbo frames and is configured accordingly. For high bandwidths, the multiqueue can be set to a maximum equal to the number of vCPUs assigned to the VM. This enables higher bandwidths.


### Sonstiges
  * **QEMU Guest Agent** installieren und in der VM-Konfiguration aktivieren. Ermöglicht sauberere Snapshots, korrekte IP-Anzeige und gesteuerte Shutdowns.
    * Nicht vergessen unter VM > Options aktivieren


### Misc
  * Install the **QEMU Guest Agent** and enable it in the VM configuration. This enables cleaner snapshots, correct IP display, and controlled shutdowns.
    * Don't forget to enable it under VM > Options


##  Special Considerations for Windows VMs 
### CPU Type
Current Windows installations require at least the**x86-64-v3** CPU type.
Alternatively, the host configuration (for the current CPU) is also permitted.
### Host
Many posts in the forum suggest that when using the “**Host** ” CPU type with a current Windows installation, the **“nested-virt** ” flag must be removed.
This disables virtualization-based security, which is currently causing many problems (low performance, high latency, and unexplained freezes).
To do this, go to **CPU > Advanced** (if you haven’t already) > set “–” for **nested-virt** in the **Flag** column > OK
### VirtIO Drivers
Windows does not include VirtIO drivers. They must be installed manually.
  * Mount the VirtIO driver ISO as a second CD drive during installation.
  * Contains drivers for: Network, Storage, Balloon, Serial, Guest Agent.
  * For the latest ISO, please always check the Proxmox article and Known Issues first! => <https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers>


You can download the currently recommended VirtIO version [271](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/virtio-win-0.1.271-1/virtio-win-0.1.271.iso) here.
Occasionally, there are issues with older and newer versions. You can check for them in advance under “**Known Issues** ” [here](https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers#Known_Issues).
### Ballooning on Windows
Ballooning on Windows is a bit more specialized. Unfortunately, the implementation involving the automatic allocation and deallocation of RAM on Windows does not work very reliably. It can lead to performance issues or crashes. However, since ballooning is required for accurate RAM reporting, this service must remain enabled on Windows as well.
Therefore, it is recommended to set the Min and Max values for ballooning to the same value. This prevents any reallocation of RAM for this VM, while ensuring that RAM reporting continues to function reliably.
### TPM 2.0
  * Windows 11 requires **TPM 2.0**. For Windows Server, this is currently optional (<=WS2025).
  * In Proxmox, an **emulated TPM 2.0** (software TPM) can be added (vTPM).
  * Prerequisite: Machine Type **q35** and BIOS **OVMF (UEFI)**.


### Recommended Settings for Windows  
| **Setting**  | **Recommendation**  |  
| --- | --- |  
| Machine Type/Chipset  | q35  |  
| BIOS  | OVMF (UEFI)  |  
| TPM  | v2.0  |  
| SCSI controller  | VirtIO SCSI Single  |  
| Network  | VirtIO (after installing the driver)  |  
| Guest Agent  | QEMU Guest Agent (VirtIO package)  |  
### Notes
  * Windows activation may fail if hardware changes are made (e.g., a change in machine type)—check the license status before making any changes.
  * If you are using VirtIO networking, install the driver before migration; otherwise, there will be no network connection after the migration.


##  Special Considerations for Linux VMs 
### VirtIO Support
Modern Linux kernels (2.6.25 and later) include VirtIO drivers natively. A separate driver installation is generally**not required**.
### QEMU Guest Agent
However, this must be installed separately; it may, however, be installed automatically during a fresh installation of the guest operating system.
  * Package name depending on the distribution:
    * Debian/Ubuntu: `apt install qemu-guest-agent`
    * RHEL/Rocky/AlmaLinux: `dnf install qemu-guest-agent`
  * Enable the service: `systemctl enable --now qemu-guest-agent`


###  Recommended Settings for Linux  
| **Setting**  | **Recommendation**  |  
| --- | --- |  
| Machine Type/Chipset  | q35 or i1440fx  |  
| BIOS  | OVMF (UEFI) or SeaBIOS  |  
| SCSI controller  | VirtIO SCSI Single  |  
| Network  | VirtIO  |  
| Guest Agent  | qemu-guest-agent (package)  |  
| Cloud-Init  | Recommended for template deployments  |  
**Notes**
  * You should configure **Discard/TRIM** within the VM so that the host can reclaim the released storage. Configuring it only on the VM disk is not sufficient. In most cases, however, this is already configured by default in the guest OS, though usually only for SSDs => SSD emulation may be necessary, or manual configuration may be required, for example, in fstab.


### What else should you keep in mind?
**Host CPU Type**
While this CPU type offers the most features and delivers the best performance, it could pose limitations for future live migrations.
In general, a live migration using the Host type between two different host CPUs is not possible or is very unstable. (For example, migrating from a newer to an older CPU usually doesn’t work, but migrating from an older to a newer CPU generation might work) .
This could potentially lead to problems when expanding the cluster. Therefore, we generally recommend choosing one of the **x86-64-vX** CPUs, as these have a fixed CPU feature set that remains consistent across all nodes. You should select the lowest common denominator within the cluster.
Additionally, this CPU type sometimes causes problems under Windows (if necessary, remove the **nested-virt** flag).
Do you have questions about open source solutions?  Our experienced team will be happy to advise you.  Click here! 
##  More Proxmox Topics 
[ Proxmox Virtual Environment  Virtualize servers, networks, and storage in a single environment — with a Proxmox B2B server solution. ](https://www.starline.de/en/solutions/proxmox/proxmox-virtual-environment) [ Project on Proxmox virtualisation  Do you think data security is handled too laxly on the net? Here is an anti-micro-targeting project for this. ](https://www.starline.de/en/magazine/technical-articles/staff-project-proxmox-virtualisation-for-data-protection-at-home) [ How to mount iSCSI storage under Proxmox  In this step-by-step guide, we will show you how to integrate your iSCSI storage under Proxmox VE. ](https://www.starline.de/en/magazine/technical-articles/mounting-iscsi-storage-under-proxmox) [ Proxmox LVM via iSCSI/FC/SAS  Multipath enables redundant access even if one or more components fail. This is how it works. ](https://www.starline.de/en/magazine/technical-articles/proxmox-lvm-on-top-of-iscsi-fc-sas-with-multipathing)
##  Any questions? 
Kevin Fietz 
Technical Support 
Our expert on Ceph, GRAID, PetaSAN, Proxmox, and more
