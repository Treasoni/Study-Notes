---
url: "https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/efi.html"
title: "3.14. Alternative Firmware (EFI)"
scraped_at: 2026-09-17T16:08:55+00:00
---

[Skip to Main Content](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/efi.html#main_content)
Oracle® VM VirtualBox
User Manual for Release 6.0  
| [Previous User Interface ](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/user-interface.html "Go To Previous Page \[access key: p\]")  | [Home Oracle® VM VirtualBox User Manual for Release 6.0 ](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/index.html "Go To Home Page \[access key: h\]")  | [Up Configuring Virtual Machines ](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/BasicConcepts.html "Go Up A Level In The Navigation \[access key: u\]")  | [Next Guest Additions ](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadditions.html "Go To Next Page \[access key: n\]")  |  
| --- | --- | --- | --- |  


  *   *     * [Why is Virtualization Useful?](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/virt-why-useful.html)
    * [Some Terminology](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/virtintro.html)
    *     * [Supported Host Operating Systems](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/hostossupport.html)
      * [Host CPU Requirements](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/hostossupport.html#hostcpurequirements)
    * [Installing Oracle VM VirtualBox and Extension Packs](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/intro-installing.html)
    * [Starting Oracle VM VirtualBox](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/intro-starting.html)
    * [Creating Your First Virtual Machine](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/gui-createvm.html)
    * [Running Your Virtual Machine](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/intro-running.html)
      * [Starting a New VM for the First Time](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/intro-running.html#intro-starting-vm-first-time)
      * [Capturing and Releasing Keyboard and Mouse](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/intro-running.html#keyb_mouse_normal)
      * [Typing Special Characters](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/intro-running.html#specialcharacters)
      * [Changing Removable Media](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/intro-running.html#intro-removable-media-changing)
      * [Resizing the Machine's Window](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/intro-running.html#intro-resize-window)
      * [Saving the State of the Machine](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/intro-running.html#intro-save-machine-state)
    *     *       * [Taking, Restoring, and Deleting Snapshots](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/snapshots.html#snapshots-take-restore-delete)
      *     * [Virtual Machine Configuration](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/configbasics.html)
    * [Removing and Moving Virtual Machines](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/intro-removing.html)
    * [Cloning Virtual Machines](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/clone.html)
    * [Importing and Exporting Virtual Machines](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/ovf.html)
      * [About the OVF Format](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/ovf.html#ovf-about)
      * [Importing an Appliance in OVF Format](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/ovf.html#ovf-import-appliance)
      * [Exporting an Appliance in OVF Format](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/ovf.html#ovf-export-appliance)
      * [Exporting an Appliance to Oracle Cloud Infrastructure](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/ovf.html#cloud-export-oci)
      * [Importing an Instance from Oracle Cloud Infrastructure](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/ovf.html#cloud-import-oci)
      * [The Cloud Profile Manager](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/ovf.html#ovf-cloud-profile-manager)
    *     * [Alternative Front-Ends](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/frontends.html)
    *       * [Using the Soft Keyboard](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/soft-keyb.html#soft-keyb-using)
      * [Creating a Custom Keyboard Layout](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/soft-keyb.html#soft-keyb-custom)
  * [Installation Details](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/installation.html)
    * [Installing on Windows Hosts](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/installation_windows.html)
      *       * [Performing the Installation](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/installation_windows.html#install-win-performing)
      *       * [Unattended Installation](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/installation_windows.html#install-win-unattended)
      *     * [Installing on Mac OS X Hosts](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/installation-mac.html)
      * [Performing the Installation](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/installation-mac.html#install-mac-performing)
      *       * [Unattended Installation](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/installation-mac.html#install-mac-unattended)
    * [Installing on Linux Hosts](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html)
      *       * [The Oracle VM VirtualBox Kernel Modules](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html#externalkernelmodules)
        * [Kernel Modules and UEFI Secure Boot](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html#kernel-modules-efi-secure-boot)
      * [Performing the Installation](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html#install-linux-performing)
        * [Installing Oracle VM VirtualBox from a Debian or Ubuntu Package](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html#install-linux-debian-ubuntu)
        * [Using the Alternative Generic Installer (VirtualBox.run)](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html#install-linux-alt-installer)
        * [Performing a Manual Installation](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html#install-linux-manual)
        * [Updating and Uninstalling Oracle VM VirtualBox](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html#install-linux-update-uninstall)
        * [Automatic Installation of Debian Packages](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html#install-linux-debian-automatic)
        * [Automatic Installation of RPM Packages](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html#install-linux-rpm-automatic)
        * [Automatic Installation Options](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html#linux_install_opts)
      *       * [Starting Oracle VM VirtualBox on Linux](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-linux-host.html#startingvboxonlinux)
    * [Installing on Oracle Solaris Hosts](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-solaris-host.html)
      * [Performing the Installation](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-solaris-host.html#install-solaris-performing)
      *       * [Starting Oracle VM VirtualBox on Oracle Solaris](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-solaris-host.html#install-solaris-starting)
      *       * [Unattended Installation](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-solaris-host.html#install-solaris-unattended)
      * [Configuring a Zone for Running Oracle VM VirtualBox](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/install-solaris-host.html#solaris-zones)
  * [Configuring Virtual Machines](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/BasicConcepts.html)
    * [Supported Guest Operating Systems](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestossupport.html)
      *       *     * [Unattended Guest Installation](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/basic-unattended.html)
      * [An Example of Unattended Guest Installation](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/basic-unattended.html#unattended-guest-install-example)
    * [Emulated Hardware](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/emul-hardware.html)
    *       *       *       *       *     *       *       *       *     *       *       *       *     *     *     *     *     *       *       * [Implementation Notes for Windows and Linux Hosts](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/usb-support.html#usb-implementation-notes)
    *     *     * [Alternative Firmware (EFI)](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/efi.html)
      * [Video Modes in EFI](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/efi.html#efividmode)
      * [Specifying Boot Arguments](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/efi.html#efibootargs)
  *     * [Introduction to Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-intro.html)
    * [Installing and Maintaining Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html)
      * [Guest Additions for Windows](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-windows)
        * [Installing the Windows Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#mountingadditionsiso)
        * [Updating the Windows Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-windows-updating)
        *         *       * [Guest Additions for Linux](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-linux)
        * [Installing the Linux Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-linux-install)
        * [Graphics and Mouse Integration](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-linux-graphics-mouse)
        * [Updating the Linux Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-linux-updating)
        * [Uninstalling the Linux Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-linux-uninstall)
      * [Guest Additions for Oracle Solaris](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-solaris)
        * [Installing the Oracle Solaris Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-solaris-install)
        * [Uninstalling the Oracle Solaris Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-solaris-uninstall)
        * [Updating the Oracle Solaris Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-solaris-updating)
      * [Guest Additions for OS/2](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-install.html#additions-os2)
    *       *       *     *       *       *     * [Hardware-Accelerated Graphics](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-video.html)
      * [Hardware 3D Acceleration (OpenGL and Direct3D 8/9)](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-video.html#guestadd-3d)
      * [Hardware 2D Video Acceleration for Windows Guests](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-video.html#guestadd-2d)
    *     *       * [Using Guest Properties to Wait on VM Events](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-guestprops.html#guestadd-guestprops-waits)
    * [Guest Control File Manager](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-gc-file-manager.html)
      * [Using the Guest Control File Manager](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-gc-file-manager.html#guestadd-gc-file-manager-using)
    * [Guest Control of Applications](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-guestcontrol.html)
    * [Memory Overcommitment](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/guestadd-memory-usage.html)
      *       *   * [Virtual Storage](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/storage.html)
    * [Hard Disk Controllers](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/harddiskcontrollers.html)
    * [Disk Image Files (VDI, VMDK, VHD, HDD)](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vdidetails.html)
    * [The Virtual Media Manager](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vdis.html)
    * [Special Image Write Modes](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/hdimagewrites.html)
    * [Differencing Images](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/diffimages.html)
    * [Cloning Disk Images](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/cloningvdis.html)
    * [Host Input/Output Caching](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/iocaching.html)
    * [Limiting Bandwidth for Disk Images](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/storage-bandwidth-limit.html)
    *     *     * [vboximg-mount: A Utility for FUSE Mounting a Virtual Disk Image](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboximg-mount.html)
      * [Viewing Detailed Information About a Virtual Disk Image](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboximg-mount.html#vboximg-mount-display)
      * [Mounting a Virtual Disk Image](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboximg-mount.html#vboximg-mount-steps)
  * [Virtual Networking](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/networkingdetails.html)
    * [Virtual Networking Hardware](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/nichardware.html)
    * [Introduction to Networking Modes](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/networkingmodes.html)
    * [Network Address Translation (NAT)](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/network_nat.html)
      * [Configuring Port Forwarding with NAT](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/network_nat.html#natforward)
      * [PXE Booting with NAT](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/network_nat.html#nat-tftp)
      *     * [Network Address Translation Service](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/network_nat_service.html)
    * [Bridged Networking](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/network_bridged.html)
    * [Internal Networking](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/network_internal.html)
    * [Host-Only Networking](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/network_hostonly.html)
    * [UDP Tunnel Networking](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/network_udp_tunnel.html)
    *     * [Limiting Bandwidth for Network Input/Output](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/network_bandwidth_limit.html)
    * [Improving Network Performance](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/network_performance.html)
  *     *     *     *     *     * [VBoxManage showvminfo](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-showvminfo.html)
    * [VBoxManage registervm/unregistervm](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-registervm.html)
    * [VBoxManage createvm](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-createvm.html)
    * [VBoxManage modifyvm](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-modifyvm.html)
      *       *         *       *       *       * [Remote Machine Settings](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-modifyvm.html#vboxmanage-modifyvm-vrde)
      *       *       * [USB Card Reader Settings](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-modifyvm.html#vboxmanage-usbcardreader)
      * [Autostarting VMs During Host System Boot](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-modifyvm.html#vboxmanage-autostart)
    *     *       *       * [Import from Oracle Cloud Infrastructure](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-import.html#vboxmanage-import-cloud)
    *       *       * [Export to Oracle Cloud Infrastructure](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-export.html#vboxmanage-export-cloud)
    * [VBoxManage startvm](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-startvm.html)
    * [VBoxManage controlvm](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-controlvm.html)
    * [VBoxManage discardstate](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-discardstate.html)
    * [VBoxManage adoptstate](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-adoptstate.html)
    * [VBoxManage closemedium](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-closemedium.html)
    * [VBoxManage storageattach](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-storageattach.html)
    * [VBoxManage storagectl](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-storagectl.html)
    * [VBoxManage bandwidthctl](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-bandwidthctl.html)
    * [VBoxManage showmediuminfo](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-showmediuminfo.html)
    * [VBoxManage createmedium](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-createmedium.html)
    * [VBoxManage modifymedium](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-modifymedium.html)
    * [VBoxManage clonemedium](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-clonemedium.html)
    * [VBoxManage mediumproperty](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-mediumproperty.html)
    * [VBoxManage encryptmedium](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-encryptmedium.html)
    * [VBoxManage checkmediumpwd](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-checkmediumpwd.html)
    * [VBoxManage convertfromraw](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-convertfromraw.html)
    * [VBoxManage getextradata/setextradata](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-extradata.html)
    * [VBoxManage setproperty](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-setproperty.html)
    * [VBoxManage usbfilter add/modify/remove](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-usbfilter.html)
    * [VBoxManage sharedfolder add/remove](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-sharedfolder.html)
    * [VBoxManage guestproperty](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-guestproperty.html)
    * [VBoxManage guestcontrol](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-guestcontrol.html)
    * [VBoxManage metrics](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-metrics.html)
    * [VBoxManage natnetwork](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-natnetwork.html)
    * [VBoxManage hostonlyif](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-hostonlyif.html)
    * [VBoxManage usbdevsource](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-usbdevsource.html)
    * [VBoxManage unattended](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-unattended.html)
      *       *         *         *     * [VBoxManage snapshot](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html)
      *       *         * [General Command Operand](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html#idm44990829124112)
        * [Take a Snapshot of a Virtual Machine](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html#idm44990829120352)
        *         *         * [Restore the Current Snapshot](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html#idm44990829079936)
        * [Change the Name or Description of an Existing Snapshot](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html#idm44990829072848)
        *         * [Show Information About a Snapshot's Settings](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-snapshot.html#idm44990829035056)
      *     * [VBoxManage clonevm](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-clonevm.html)
      *       *       * [Command Operand and Options](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-clonevm.html#idm44990828990928)
      *       *     * [VBoxManage extpack](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-extpack.html)
      *       *         *         *         *       *     * [VBoxManage dhcpserver](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-dhcpserver.html)
      *       *         *         *         *         *         *         *         *     * [VBoxManage debugvm](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-debugvm.html)
      *       *         *         *         *         *         *         *         *         *         *         *         *         *         *         *         *     * [VBoxManage cloudprofile](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-cloudprofile.html)
      *       *         *         *         *         *         *     * [VBoxManage cloud list](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-cloudlist.html)
      *       *         *         *         *     * [VBoxManage cloud instance](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-cloudinstance.html)
      *       *         *         *         *         * [cloud instance termination](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-cloudinstance.html#idm44990827619168)
        *         *     * [VBoxManage cloud image](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-cloudimage.html)
      *       *         *         *         *         *         *         *   * 

[Search Highlighter (On/Off)](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/efi.html)
##  3.14. Alternative Firmware (EFI)
Oracle VM VirtualBox includes experimental support for the Extensible Firmware Interface (EFI), which is an industry standard intended to replace the legacy BIOS as the primary interface for bootstrapping computers and certain system services later. 
By default, Oracle VM VirtualBox uses the BIOS firmware for virtual machines. To use EFI for a given virtual machine, you can enable EFI in the machine's **Settings** dialog. See [Section 3.5.1, “Motherboard Tab”](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/settings-system.html#settings-motherboard "3.5.1. Motherboard Tab"). Alternatively, use the **VBoxManage** command line interface as follows: 

```
VBoxManage modifyvm "VM name" --firmware efi
```

To switch back to using the BIOS: 

```
VBoxManage modifyvm "VM name" --firmware bios
```

One notable user of EFI is Apple Mac OS X. More recent Linux versions and Windows releases, starting with Vista, also offer special versions that can be booted using EFI. 
Another possible use of EFI in Oracle VM VirtualBox is development and testing of EFI applications, without booting any OS. 
Note that the Oracle VM VirtualBox EFI support is experimental and will be enhanced as EFI matures and becomes more widespread. Mac OS X, Linux, and newer Windows guests are known to work fine. Windows 7 guests are unable to boot with the Oracle VM VirtualBox EFI implementation. 
###  3.14.1. Video Modes in EFI
EFI provides two distinct video interfaces: GOP (Graphics Output Protocol) and UGA (Universal Graphics Adapter). Modern OSes, such as Mac OS X, generally use GOP, while some older ones still use UGA. Oracle VM VirtualBox provides a configuration option to control the graphics resolution for both interfaces, making the difference mostly irrelevant for users. 
The default resolution is 1024x768. To select a graphics resolution for EFI, use the following **VBoxManage** command: 

```
VBoxManage setextradata "VM name" VBoxInternal2/EfiGraphicsResolution HxV
```

Determine the horizontal resolution H and the vertical resolution V from the following list of default resolutions:      
640x480, 32bpp, 4:3  


    
800x600, 32bpp, 4:3      
1024x768, 32bpp, 4:3  


    
1152x864, 32bpp, 4:3      
1280x720, 32bpp, 16:9  


    
1280x800, 32bpp, 16:10  


    
1280x1024, 32bpp, 5:4  

SXGA+ 
    
1400x1050, 32bpp, 4:3  

WXGA+ 
    
1440x900, 32bpp, 16:10      
1600x900, 32bpp, 16:9  


    
1600x1200, 32bpp, 4:3  

WSXGA+ 
    
1680x1050, 32bpp, 16:10  

Full HD 
    
1920x1080, 32bpp, 16:9  

WUXGA 
    
1920x1200, 32bpp, 16:10  

DCI 2K 
    
2048x1080, 32bpp, 19:10  

Full HD+ 
    
2160x1440, 32bpp, 3:2  

Unnamed 
    
2304x1440, 32bpp, 16:10      
2560x1440, 32bpp, 16:9  

WQXGA 
    
2560x1600, 32bpp, 16:10  

QWXGA+ 
    
2880x1800, 32bpp, 16:10  


    
3200x1800, 32bpp, 16:9  

WQSXGA 
    
3200x2048, 32bpp, 16:10  

4K UHD 
    
3840x2160, 32bpp, 16:9  

WQUXGA 
    
3840x2400, 32bpp, 16:10  

DCI 4K 
    
4096x2160, 32bpp, 19:10  


    
4096x3072, 32bpp, 4:3  


    
5120x2880, 32bpp, 16:9  

WHXGA 
    
5120x3200, 32bpp, 16:10  

WHSXGA 
    
6400x4096, 32bpp, 16:10  

HUXGA 
    
6400x4800, 32bpp, 4:3  

8K UHD2 
    
7680x4320, 32bpp, 16:9 
If this list of default resolution does not cover your needs, see [Custom VESA Resolutions](https://docs.oracle.com/en/virtualization/virtualbox/6.0/admin/adv-display-config.html#customvesa). Note that the color depth value specified in a custom video mode must be specified. Color depths of 8, 16, 24, and 32 are accepted. EFI assumes a color depth of 32 by default. 
The EFI default video resolution settings can only be changed when the VM is powered off. 
###  3.14.2. Specifying Boot Arguments
It is currently not possible to manipulate EFI variables from within a running guest. For example, setting the `boot-args` variable by running the **nvram** tool in a Mac OS X guest will not work. As an alternative method, `VBoxInternal2/EfiBootArgs` extradata can be passed to a VM in order to set the `boot-args` variable. To change the `boot-args` EFI variable, use the following command: 

```
VBoxManage setextradata "VM name" VBoxInternal2/EfiBootArgs <value>
```

Copyright © 2004, 2020 Oracle and/or its affiliates. All rights reserved. [Legal Notices](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/cpyr.htm)
