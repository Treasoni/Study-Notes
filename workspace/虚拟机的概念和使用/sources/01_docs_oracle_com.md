---
url: "https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/create-vm.html"
title: "Creating a New Virtual Machine"
scraped_at: 2026-09-04T15:57:07+00:00
---

[Previous](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/configuring-virtualbox.html) [Next](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html) JavaScript must be enabled to correctly display this content 
##  4 Creating a New Virtual Machine 
To create a Virtual Machine (VM) using the GUI, follow the steps below. To use VBoxManage, see [Creating a New Virtual Machine Using VBoxManage](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/create-vm.html#unattended-guest-install-example). 
  * In Oracle VirtualBox Manager window, click Home, then click New and follow the workflow. 
If you don't see the New Virtual Machine workflow, change the experience level to Basic. See [Experience Levels for VirtualBox Manager](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/configuring-virtualbox.html#gui-experience-level). In Expert mode you see all the options on one page. 
The exact settings available depend on the architecture of the host platform.


Once created, the virtual machine is displayed in the Machines list in Oracle VirtualBox Manager, with the name that you specify. You can make changes later, in the Settings for the VM. 
You must supply an operating system image, in ISO format, for the operating system you intend to install on the VM. Oracle VirtualBox does not supply the OS or any license required to use it. 
### Specify Name and Operating System
  1. Give the virtual machine (VM) a name. The name you enter is shown in the Machines tool in Oracle VirtualBox Manager and is also used for the VM's files on disk. Be sure to assign each VM an informative name that describes the OS and software running on the VM. For example, `Windows 10 with Visio`. The name is also used to help Oracle VirtualBox suggest the appropriate OS and related field contents automatically, unless you have selected the OS Type. 
  2. Select the location where VMs are stored on your computer, called the VM Folder. Ensure that the folder location has enough free space, especially if you intend to use the snapshots feature. See also [The VM Folder](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Troubleshooting.html#vboxconfigdata-machine-folder). 
  3. Select the ISO image file for the operating system you intend to install on the new VM. The image file can be used directly to install an OS on the new VM as part of an unattended installation, or it can be attached to a DVD drive on the new VM. If the image contains more than one edition or variant, select the one you want to use.
  4. Oracle VirtualBox completes the OS and related fields if it can detect the operating system in the ISO. If it cannot detect the OS, then set these according to your OS. For example, if the OS is Linux, the OS Distribution might be Oracle Linux and the OS Version might be Oracle Linux 8.x (64-bit). The options available for the guest OS are also limited by the host architecture. See [Guest Operating Systems](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Introduction.html#guestossupport) for more information. 
The supported OSs are grouped into types. If you want to install something very unusual that is not listed, select Other as the OS. 
Depending on your selection, Oracle VirtualBox will enable or disable certain VM settings that your guest OS may require. This is particularly important for 64-bit guests (see [64-bit Guests](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Introduction.html#intro-64bitguests)). 
  5. By default, Oracle VirtualBox will install the chosen OS using the ISO image provided, if the image supports unattended installation. See also [Configure Unattended Installation of Guest OS](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/create-vm.html#tk_create-vm-unattended-install). 
If you prefer to install the OS manually, deselect Install OS Using Unattended Installation. The selected ISO image is attached to the new VM and you must install the OS from there. 


### Configure Unattended Installation of Guest OS
If you chose Unattended Installation, Oracle VirtualBox you must supply certain configuration options to be used in the installation. 
See also [Creating a New Virtual Machine Using VBoxManage](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/create-vm.html#unattended-guest-install-example) for details of how to configure unattended installation from the command line. 
  1. Enter the User Name and Password for a default user on the guest OS. On Windows, this will be an administrator. On Linux, the `root` user will also be created with the same password. 
  2. For Windows guests, enter the Product Key supplied with Windows. 
  3. Enter the Host Name for the VM. By default, this is the same as the VM name. 
  4. Enter the Domain Name for the VM. 
  5. Select Install in Background if you want to create the VM without a GUI. 
  6. Unattended Guest Additions installation is available for some guests. Select Install Guest Additions if you would like Oracle VirtualBox to install the Guest Additions after the OS. Specify the ISO to use, usually the default file that is part of the VirtualBox installation on the host machine. 


### Specify Virtual Hardware
  1. Based on the OS you have chosen, Oracle VirtualBox suggests a suitable default size for Base Memory. This is the amount of RAM that Oracle VirtualBox should allocate to the virtual machine (VM) every time it is started. The guest OS will report this size as the VM's installed RAM. 
Caution:
Choose this setting carefully. The memory you give to the VM will not be available to your host OS while the VM is running.
Do not specify more than you can spare, whilst ensuring you allocate enough for your guest OS and applications to run properly. For example, if your host machine has 4 GB of RAM and you enter 2048 MB as the base memory for a VM, you will have 2 GB left for all the other software on your host while that VM is running.
A guest OS may require at least 1 or 2 GB of memory to install and boot up. If you intend to run more than one VM at a time, plan accordingly. A VM will not start if it does not have enough RAM to boot.
Always ensure that the host OS has enough RAM remaining. If insufficient RAM remains, the system might excessively swap memory to the hard disk, which will effectively bring the host system to a standstill.
  2. For Processors, select the number of virtual processors to assign to the VM. Do not assign more than half of the total processor threads from the host machine. 
  3. Choose the Disk Size for a new, dynamically allocated, virtual hard disk image to be created in the VM folder. 
For other options when allocating virtual storage, see [Virtual Storage](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/storage.html#storage). 
  4. Select Use EFI to boot the guest OS using Extended Firmware Interface (EFI). 


### Creating a New Virtual Machine Using VBoxManage
You can create a VM on the command line using VBoxManage. See also [VBoxManage createvm](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage-createvm "Create a new virtual machine"). 
The following example uses various `VBoxManage` commands to specify the VM and configure an unattended guest installation for an Oracle Linux VM on a Linux host. 
It then shows the use of the `VBoxManage unattended install` command to install and configure the guest OS. 
  1. Set a variable for the name of the OS.
```
# VM="ol8-autoinstall"

```

  2. List the available guest OS types and note the exact name of the one you need. This is required in `VBoxManage` commands.
```
# VBoxManage list ostypes
```

  3. Create the virtual machine.
```
# VBoxManage createvm --name $VM --ostype "Oracle_64" --register
```

The VM has a unique UUID.
An XML settings file is generated.
  4. Create a 32768 MB virtual hard disk for the VM.
```
# VBoxManage createhd --filename /VirtualBox/$VM/$VM.vdi --size 32768
```

  5. Create storage devices for the VM.
     * Create a SATA storage controller and attach the virtual hard disk. 
```
# VBoxManage storagectl $VM --name "SATA Controller" --add sata --controller IntelAHCI
# VBoxManage storageattach $VM --storagectl "SATA Controller" --port 0 --device 0 \
--type hdd --medium /VirtualBox/$VM/$VM.vdi
```

     * Create an IDE storage controller for a virtual DVD drive and attach an Oracle Linux installation ISO. 
```
# VBoxManage storagectl $VM --name "IDE Controller" --add ide
# VBoxManage storageattach $VM --storagectl "IDE Controller" --port 0 --device 0 \
--type dvddrive --medium /u01/Software/OL/OracleLinux-R7-U6-Server-x86_64-dvd.iso
```

  6. (Optional) Configure some settings for the VM. 
     * Enable I/O APIC for the motherboard of the VM. 
```
# VBoxManage modifyvm $VM --ioapic on
```

     * Configure the boot device order for the VM. 
```
# VBoxManage modifyvm $VM --boot1 dvd --boot2 disk --boot3 none --boot4 none
```

     * Allocate 8192 MB of RAM and 128 MB of video RAM to the VM. 
```
# VBoxManage modifyvm $VM --memory 8192 --vram 128
```

  7. Specify the Unattended Installation parameters, and then install the OS.
     * Specify an Oracle Linux ISO as the installation ISO.
```
# VBoxManage unattended install $VM \
--iso=/u01/Software/OL/OracleLinux-R7-U6-Server-x86_64-dvd.iso \
```

     * Specifiy a user name, full name, and password for a default user on the guest OS.
```
--user=login --full-user-name=name --user-password password \
```

Note that the specified password is also used for the root user account on the guest.
     * Specify that you want to install the VirtualBox Guest Additions on the VM.
```
--install-additions \
```

     * Sets the time zone for the guest OS to Central European Time (CET). 
```
--time-zone=CET
```

  8. Start the virtual machine.

```
# VBoxManage startvm $VM --type headless
```

The VM starts in headless mode, which means that it does not have a GUI.


