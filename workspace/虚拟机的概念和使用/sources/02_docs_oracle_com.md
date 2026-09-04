---
url: "https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html"
title: "Working with Virtual Machines"
scraped_at: 2026-09-04T15:57:07+00:00
---

[Previous](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/create-vm.html) [Next](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/cloud-integration.html) JavaScript must be enabled to correctly display this content 
##  5 Working with Virtual Machines 
This chapter provides detailed steps for configuring an Oracle VirtualBox virtual machine (VM). For an introduction to Oracle VirtualBox and steps to get your first virtual machine running, see [About Oracle VirtualBox](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Introduction.html#ct_about-virtualbox). 
You have considerable latitude when deciding what virtual hardware to provide to the guest. Use virtual hardware to communicate with the host system or with other guests. For example, you can use virtual hardware in the following ways: 
  * Have Oracle VirtualBox present an ISO CD-ROM image to a guest system as if it were a physical CD-ROM. 
  * Provide a guest system access to the physical network through its virtual network card. 
  * Provide the host system, other guests, and computers on the Internet access to the guest system. 


### Running a Virtual Machine
To start a virtual machine (VM), you have the following options:
  * Open the Machines list in Oracle VirtualBox Manager, and then double-click the VM's name. 
  * Select the VM's name in the Machines tool in Oracle VirtualBox Manager, and then click Start. 
  * Go to the `VirtualBox VMs` folder in your system user's home directory. Find the subdirectory of the machine you want to start and double-click the machine settings file. This file has a `.vbox` file extension. 


The VM you started appears in a new window and you will see it start to boot up, or prompt you to install an operating system as required. Everything that would normally be seen on the virtual system's monitor is shown in the window.
In general, you can use the virtual machine as you would use a real computer. The following topics describe a few points to note when running a VM.
#### Starting a New VM for the First Time
When you start a VM for the first time the Unattended Installation process is started automatically, using the ISO image file specified. See [Creating a New Virtual Machine](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/create-vm.html#tk_create-vm). 
Follow the onscreen instructions to install your OS.
The installation operation changes the boot device order to boot the virtual hard disk first and then the virtual DVD drive. If the virtual hard disk is empty prior to the automatic installation, the VM boots from the virtual DVD drive and begins the installation.
If the virtual hard disk contains a bootable OS, the installation operation exits. In this case, change the boot device order manually by pressing F12 during the BIOS splash screen.
#### Virtual Machine Status Bar
A status bar is displayed at the bottom of the virtual machine window. The status bar contains icons that enable you to view and change settings for the virtual machine, as follows: 
  * Highlight an icon to show details of the current settings.
  * Right-click an icon to change a setting.
Some settings, such as audio, can be changed directly by right-clicking the status bar icon. For other settings, you select from the displayed menu options.


[Table 5-1](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#vm-status-bar__table-status-bar-icons "Describes icons on the status bar located at the bottom of the virtual machine window") describes the icons on the status bar. 
Table 5-1 Virtual Machine Status Bar Icons  
|  Icon   |  Description   |  
| --- | --- |  
|  Storage (SATA) Settings for attached SATA storage devices, such as hard disk drives. See also [Storage Settings](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ct_settings-storage).   |  
|  Storage (IDE) Settings for attached IDE storage devices, such as optical CD-ROM drives. See also [Storage Settings](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ct_settings-storage).  Right-click to show options for adding and removing IDE devices. See also [The Virtual Media Manager](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/storage.html#ct_virtual-media-manager).   |  
|  Audio Settings for audio output and audio input. Right-click to change a setting. The status bar icon is updated automatically to show which settings are enabled. See also [Audio Settings](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ct_settings-audio).   |  
|  Network Settings for attached network adapters. Right-click to connect or disconnect a network adapter. See also [Network Settings](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ct_settings-network).   |  
|  USB Settings for attached USB devices. Right-click to select from the available USB devices on the host and to specify a USB filter. See also [USB Settings](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#settings-usb).   |  
|  Shared Folders Settings for shared folders. Right-click to change shared folder settings or to add a new shared folder. See also [Shared Folders](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ct_shared-folders).   |  
|  Display Settings for the virtual machine display. Right-click to show options for resizing and scaling the display. See also [Resizing the VM's Window](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#intro-resize-window).   |  
|  Recording Settings for video and audio recording. Right-click to show options to enable and disable recording, or to change recording settings. To enable recording, right-click the status bar icon and select the Recording option. The icon changes to a pulsing red dot to indicate that recording is in progress.  To disable recording, right-click the status bar icon and deselect the Recording option. The icon changes back to the default image.  See also [Recording Tab](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#settings-capture).   |  
|  Processor Settings for the CPU used by the virtual machine. The colored bar in the icon indicates current processor activity. Red indicates high CPU usage, Green indicates low CPU usage. A green turtle icon indicates that a native hypervisor, such as Hyper-V, is running on the host. See also [Processor Tab](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#settings-processor).   |  
|  Mouse Integration Settings for capturing the host mouse pointer. The icon indicates whether mouse integration is on (green arrow) or off (yellow arrow) and whether the pointer is captured (mouse icon colored) or not (mouse icon gray). Right-click to enable or disable mouse integration. See also [Capturing and Releasing Keyboard and Mouse](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#keyb_mouse_normal).   |  
|  Host Key Settings for capturing the host keyboard. The arrow on the icon is green if the keyboard is captured, and black if not. The background is blue if the host key is not pressed, and white when it is pressed. A check icon appears when the VM is waiting for a host key combination to be typed. The current host key is displayed to the right of the icon. Right-click to show options for configuring the host key combination and other keyboard shortcuts. Right-click to insert a special key combination, such as Ctrl-Alt-Del. See also [Typing Special Characters](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#specialcharacters).   |  
Configuring the Status Bar
You can configure the status bar as follows:
  * To hide the status bar, right-click in the status bar area and deselect Show Status Bar. 
  * To show the status bar, select View, Status Bar, Show Status Bar from the virtual machine's menu bar. 
  * To modify the status bar contents, right-click in the status bar area and select Status Bar Settings. You can then do the following: 
    * Select icons that you want to include in the status bar.
    * Deselect icons that you want to remove from the status bar.
    * Drag and drop icons to change their order in the status bar.
Click the check mark button to save your changes to the status bar.
See also [User Interface](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ct_user-interface) for other options to change the status bar. 


#### Capturing and Releasing Keyboard and Mouse
Oracle VirtualBox provides a virtual USB tablet device to new virtual machines through which mouse events are communicated to the guest OS. If you are running a modern guest OS that can handle such devices, mouse support may work out of the box without the mouse being captured as described below. See [Motherboard Tab](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#settings-motherboard). 
Otherwise, if the virtual machine detects only standard PS/2 mouse and keyboard devices, since the OS in the virtual machine does not know that it is not running on a real computer, it expects to have exclusive control over your keyboard and mouse. But unless you are running the VM in full screen mode, your VM needs to share keyboard and mouse with other applications and possibly other VMs on your host. 
After installing a guest OS and before you install the Guest Additions, described in [Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/guestadditions.html#guestadditions), either your VM or the rest of your computer can own the keyboard and the mouse. Both cannot own the keyboard and mouse at the same time. You will see a second mouse pointer which is always confined to the limits of the VM window. You activate the VM by clicking inside it. 
To return ownership of keyboard and mouse to your host OS, Oracle VirtualBox reserves a special key on your keyboard: the Host key. By default, this is the right Ctrl key on your keyboard. On a Mac host, the default Host key is the left Command key. You can change this default using the Preferences window. See [Set Oracle VirtualBox Preferences](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/configuring-virtualbox.html#tk_preferences). The current setting for the Host key is always displayed at the bottom right of your VM window. 
Figure 5-1 Host Key Setting on the Virtual Machine Status Bar
This means the following: 
  * Your keyboard is owned by the VM if the VM window on your host desktop has the keyboard focus. If you have many windows open in your guest OS, the window that has the focus in your VM is used. This means that if you want to enter text within your VM, click the title bar of your VM window first. 
To release keyboard ownership, press the Host key. As explained above, this is typically the right Ctrl key. 
Note that while the VM owns the keyboard, some key sequences, such as Alt+Tab, will no longer be seen by the host, but will go to the guest instead. After you press the Host key to reenable the host keyboard, all key presses will go through the host again, so that sequences such as Alt+Tab will no longer reach the guest. For technical reasons it may not be possible for the VM to get all keyboard input even when it does own the keyboard. Examples of this are the Ctrl+Alt+Del sequence on Windows hosts or single keys grabbed by other applications on X11 hosts such as the GNOME desktop Locate Pointer feature. 
  * Your mouse is owned by the VM only after you have clicked in the VM window. The host mouse pointer will disappear, and your mouse will drive the guest's pointer instead of your normal mouse pointer. 
Note that mouse ownership is independent of that of the keyboard. Even after you have clicked on a titlebar to be able to enter text into the VM window, your mouse is not necessarily owned by the VM yet. 
To release ownership of your mouse by the VM, press the Host key. 


As this behavior is inconvenient, Oracle VirtualBox provides a set of tools and device drivers for guest systems called the Oracle VirtualBox Guest Additions. These tools make VM keyboard and mouse operations much more seamless. Most importantly, the Guest Additions suppress the second "guest" mouse pointer and make your host mouse pointer work directly in the guest. See [Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/guestadditions.html#guestadditions). 
#### Typing Special Characters
Some OSes expect certain key combinations to initiate certain procedures. The key combinations that you type into a VM might target the host OS, the Oracle VirtualBox software, or the guest OS. The recipient of these keypresses depends on a number of factors, including the key combination itself. 
  * Host OSes reserve certain key combinations for themselves. For example, you cannot use the Ctrl+Alt+Delete combination to reboot the guest OS in your VM, because this key combination is reserved by the host OS. Even though both Windows and Linux OSes can intercept this key combination, the host OS is rebooted automatically. 
On Linux and Oracle Solaris hosts, which use the X Window System, the key combination Ctrl+Alt+Backspace normally resets the X server and restarts the entire graphical user interface. As the X server intercepts this combination, pressing it will usually restart your host graphical user interface and kill all running programs, including Oracle VirtualBox, in the process. 
On Linux hosts supporting virtual terminals, the key combination Ctrl+Alt+Fx, where Fx is one of the function keys from F1 to F12, normally enables you to switch between virtual terminals. As with Ctrl+Alt+Delete, these combinations are intercepted by the host OS and therefore always switch terminals on the host. 
If, instead, you want to send these key combinations to the guest OS in the virtual machine, you will need to use one of the following methods: 
    * Use the items in the Input, Keyboard menu of the virtual machine window. This menu includes the settings Insert Ctrl+Alt+Delete and Insert Ctrl+Alt+Backspace. However, the latter setting affects only Linux guests or Oracle Solaris guests. 
This menu also includes an option for inserting the Host key combination. 
    * Use special key combinations with the Host key, which is normally the right Control key. Oracle VirtualBox then translates the following key combinations for the VM: 
      * Host key + Del sends Ctrl+Alt+Del to reboot the guest OS. 
      * Host key + Backspace sends Ctrl+Alt+Backspace to restart the graphical user interface of a Linux or Oracle Solaris guest. 
      * Host key + Function key. For example, use this key combination to simulate Ctrl+Alt+Fx to switch between virtual terminals in a Linux guest. 
  * For some other keyboard combinations such as Alt+Tab to switch between open windows, Oracle VirtualBox enables you to configure whether these combinations will affect the host or the guest, if a virtual machine currently has the focus. This is a global setting for all virtual machines and can be found under File, Preferences, Input. 
  * A soft keyboard can be used to input key combinations in the guest. See [Using the Soft Keyboard](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#soft-keyb-using). 


#### Soft Keyboard
Oracle VirtualBox provides a soft keyboard that enables you to input keyboard characters on the guest. A soft keyboard is an on-screen keyboard that can be used as an alternative to a physical keyboard. See [Using the Soft Keyboard](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#soft-keyb-using) for details of how to use the soft keyboard. 
Caution:
For best results, ensure that the keyboard layout configured on the guest OS matches the keyboard layout used by the soft keyboard. Oracle VirtualBox does not do this automatically. 
The soft keyboard can be used in the following scenarios: 
  * When the physical keyboard on the host is not the same as the keyboard layout configured on the guest. For example, if the guest is configured to use an international keyboard, but the host keyboard is US English. 
  * To send special key combinations to the guest. Note that some common key combinations are also available in the Input, Keyboard menu of the guest VM window. See [Typing Special Characters](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#specialcharacters). 
  * For guests in kiosk mode, where a physical keyboard is not present. 
  * When using nested virtualization, the soft keyboard provides a method of sending key presses to a guest. 


By default, the soft keyboard includes some common international keyboard layouts. You can copy and modify these to meet your own requirements. See [Creating a Custom Keyboard Layout](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#soft-keyb-custom). 
##### Using the Soft Keyboard
  1. Display the soft keyboard. 
In the guest VM window, select Input, Keyboard, Soft Keyboard. 
  2. Select the required keyboard layout. 
The name of the current keyboard layout is displayed in the toolbar of the soft keyboard window. This is the previous keyboard layout that was used. 
Click the Layout List icon in the toolbar of the soft keyboard window. The Layout List window is displayed. 
Select the required keyboard layout from the entries in the Layout List window. 
The keyboard display graphic is updated to show the available input keys. 
  3. Use the soft keyboard to enter keyboard characters on the guest. 
     * Modifier keys such as Shift, Ctrl, and Alt are available on the soft keyboard. Click once to select the modifier key, click twice to lock the modifier key. 
The Reset the Keyboard and Release All Keys icon can be used to release all pressed modifier keys, both on the host and the guest. 
     * To change the look of the soft keyboard, click the Settings icon in the toolbar. You can change colors used in the keyboard graphic, and can hide or show sections of the keyboard, such as the NumPad or multimedia keys. 


##### Creating a Custom Keyboard Layout
You can use one of the supplied default keyboard layouts as the starting point to create a custom keyboard layout. 
Note:
To permanently save a custom keyboard layout, you must save it to a file. Otherwise, any changes you make are discarded when you close down the Soft Keyboard window. 
Custom keyboard layouts that you save are stored as an XML file on the host, in the `keyboardLayouts` folder in the global configuration data directory. For example, in `$HOME/.config/VirtualBox/keyboardLayouts` on a Linux host. 
  1. Display the Layout List. 
Click the Layout List icon in the toolbar of the soft keyboard window. 
  2. Make a copy of an existing keyboard layout. 
Highlight the required layout and click the Copy the Selected Layout icon. 
A new layout entry with a name suffix of `-Copy` is created. 
  3. Edit the new keyboard layout. 
Highlight the new layout in the Layout List and click the Edit the Selected Layout icon. 
Enter a new name for the layout. 
Edit keys in the new layout. Click the key that you want to edit and enter new key captions in the Captions fields. 
The keyboard graphic is updated with the new captions. 
  4. (Optional) Save the layout to a file. This means that your custom keyboard layout will be available for future use. 
Highlight the new layout in the Layout List and click the Save the Selected Layout into File icon. 
Any custom layouts that you create can later be removed from the Layout List, by highlighting and clicking the Delete the Selected Layout icon. 


#### Changing Removable Media
While a virtual machine is running, you can change removable media in the Devices menu of the VM's window. Here you can select in detail what Oracle VirtualBox presents to your VM as a CD, DVD, or floppy drive. 
The settings are the same as those available for the VM in the Settings window of Oracle VirtualBox Manager. But as the Settings window is disabled while the VM is in the Running or Saved state, the Devices menu saves you from having to shut down and restart the VM every time you want to change media. 
Using the Devices menu, you can attach the host drive to the guest or select a floppy or DVD image, as described in [Storage Settings](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ct_settings-storage). 
The Devices menu also includes an option for creating a virtual ISO (VISO) from selected files on the host. 
#### Resizing the VM's Window
You can resize the VM's window while that VM is running. When you do, the window is scaled as follows: 
  * If you have scaled mode enabled, then the virtual machine's screen will be scaled to the size of the window. This can be useful if you have many machines running and want to have a look at one of them while it is running in the background. Alternatively, it might be useful to enlarge a window if the VM's output screen is very small, for example because you are running an old OS in it. 
To enable scaled mode, press Host key + C, or select Scaled Mode from the View menu in the VM window. To leave scaled mode, press Host key + C again. 
The aspect ratio of the guest screen is preserved when resizing the window. To ignore the aspect ratio, press Shift during the resize operation. 
  * If you have the Guest Additions installed and they support automatic resizing, the Guest Additions will automatically adjust the screen resolution of the guest OS. For example, if you are running a Windows guest with a resolution of 1024x768 pixels and you then resize the VM window to make it 100 pixels wider, the Guest Additions will change the Windows display resolution to 1124x768. 
See [Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/guestadditions.html#guestadditions). 
  * Otherwise, if the window is bigger than the VM's screen, the screen will be centered. If it is smaller, then scroll bars will be added to the machine window. 


#### Pausing a VM
Pausing a VM suspends all the processes running on the VM.
To pause a VM: 
  1. Open the Machines tool in Oracle VirtualBox Manager, and select the running VM you want to pause. 
  2. Right-click the VM name, or open the Machine menu, and choose Pause. 

To start a paused VM running again: 
  1. Open the Machines tool in Oracle VirtualBox Manager, and select the paused VM. 
  2. Right-click the VM name, or open the Machine menu, and choose Pause. 
The VM starts running again.


#### Resetting a VM
Resetting a VM is the equivalent of choosing the reset or restart option in the OS. It does not reset to factory settings or other known state, it restarts the guest OS.
To reset a VM 
  1. Open the Machines tool in Oracle VirtualBox Manager, and select the running VM you want to reset. 
  2. Right-click the VM name, or open the Machine menu, and choose Reset. 
  3. Click Reset to confirm. Note that you will lose unsaved data. 


#### Closing or Saving a VM
When you click the Close button of your virtual machine window, at the top right of the window, just like you would close any other window on your system, Oracle VirtualBox asks you whether you want to save or power off the VM. As a shortcut, you can also press Host key + Q. 
The difference between the three options is important. They mean the following: 
  * Save State With this option, Oracle VirtualBox freezes the virtual machine by completely saving its state to your local disk. 
When you start the VM again later, you will find that the VM continues exactly where it was left off. All your programs will still be open, and your computer resumes operation. Saving the state of a virtual machine is thus in some ways similar to suspending a laptop by closing its lid.
  * Shut Down This will send an ACPI shutdown signal to the virtual machine, which has the same effect as if you had pressed the power button on a real computer. This should trigger a proper shutdown mechanism from within the VM. State is not saved. Save any open applications before choosing this option. 
  * Power Off  With this option, Oracle VirtualBox also stops running the virtual machine, but immediately without shutdown procedures or saving its state. 
Caution:
This is equivalent to pulling the power plug on a real computer without shutting it down properly. If you start the machine again after powering it off, your OS will have to reboot completely and may begin a lengthy check of its virtual system disks. As a result, this should not normally be done, since it can potentially cause data loss or an inconsistent state of the guest system on disk. 
As an exception, if your virtual machine has any snapshots, see [Snapshots](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ct_snapshots), you can use this option to quickly restore the current snapshot of the virtual machine. In that case, powering off the machine will discard the current state and any changes made since the previous snapshot was taken will be lost. 


The Discard button discards a virtual machine's saved state. This has the same effect as powering it off, and the same warnings apply. 
### Adding Virtual Machines
  * If you want to create a completely new VM, click New and follow the steps in [Creating a New Virtual Machine](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/create-vm.html#tk_create-vm). 
  * If you already have a VM saved on your machine, you can add it to the machine list by clicking Open. 
  * If you have a VM on a different machine, you can import it by clicking Import. See [Importing an Appliance in OVF Format](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ovf-import-appliance). 
  * If you want to view an OCI instance from within Oracle VirtualBox Manager, see [Adding a Cloud VM](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/cloud-integration.html#cloud-vm-add). 


### Importing and Exporting Virtual Machines
Oracle VirtualBox can import and export virtual machines in the following formats: 
  * Open Virtualization Format (OVF). This is the industry-standard format. See [About the OVF Format](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ovf-about). 
  * Cloud service formats. Export to and import from cloud services such as Oracle Cloud Infrastructure is supported. See [Integrating with Oracle Cloud Infrastructure](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/cloud-integration.html#cloud-integration). 


#### About the OVF Format
OVF is a cross-platform standard supported by many virtualization products which enables the creation of ready-made virtual machines that can then be imported into a hypervisor such as Oracle VirtualBox. Oracle VirtualBox makes OVF import and export easy to do, using Oracle VirtualBox Manager or the command-line interface. 
Using OVF enables packaging of virtual appliances. These are disk images, together with configuration settings that can be distributed easily. This way one can offer complete ready-to-use software packages, including OSes with applications, that need no configuration or installation except for importing into Oracle VirtualBox. 
Note:
The OVF standard is complex, and support in Oracle VirtualBox is an ongoing process. No guarantee is made that Oracle VirtualBox supports all appliances created by other virtualization software. In particular, the following limitations exist: 
  * OVF localization, with multiple languages in a single OVF file, is not yet supported.
  * Some OVF sections like StartupSection, DeploymentOptionSection, and InstallSection are ignored.
  * OVF environment documents, including their property sections are not yet supported.
  * Remote files using HTTP or other mechanisms are not yet supported.


Appliances in OVF format can appear in the following variants: 
  * They can come in several files, as one or several disk images, typically in the widely-used VMDK format. See [Disk Image Files (VDI, VMDK, VHD, HDD)](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/storage.html#vdidetails). They also include a textual description file in an XML dialect with an `.ovf` extension. These files must then reside in the same directory for Oracle VirtualBox to be able to import them. 
  * Alternatively, the above files can be packed together into a single archive file, typically with an `.ova` extension. Such archive files use a variant of the TAR archive format and can therefore be unpacked outside of Oracle VirtualBox with any utility that can unpack standard TAR files. 


Note:
OVF cannot describe snapshots that were taken for a virtual machine. As a result, when you export a virtual machine that has snapshots, only the current state of the machine will be exported. The disk images in the export will have a flattened state identical to the current state of the virtual machine. 
#### Importing an Appliance in OVF Format
The following steps show how to import one or more VMs from OVF format.
  1. In Oracle VirtualBox Manager, click Home, and then click Import. Choose the file you want to import. 
Alternatively, double-click the OVF or OVA file in your file manager. Oracle VirtualBox creates file type associations automatically for any OVF and OVA files on your host OS. 
  2. In Appliance Settings, check the VMs described in the OVF or OVA file and change any of the VM settings you need to. 
  3. By default, membership of VM groups is preserved on import for VMs that were initially exported from Oracle VirtualBox. You can change this behavior by using the Primary Group setting for the VM. 
The following global settings apply to all of the VMs that you import:
     * Base Folder: Specifies the directory on the host in which to store the imported VMs. 
If an appliance has multiple VMs, you can specify a different directory for each VM by editing the Base Folder setting for the VM. 
     * MAC Address Policy: Reinitializes the MAC addresses of network cards in your VMs prior to import, by default. You can override the default behavior and preserve the MAC addresses on import. 
     * Import Hard Drives as VDI: Imports hard drives in the VDI format rather than in the default VMDK format. 
  4. Click Finish to import the appliance. 
Oracle VirtualBox copies the disk images and creates local VMs with the settings described on the Appliance Settings page. The imported VMs are shown in the list of VMs in VirtualBox Manager. 
Because disk images are large, the VMDK images that are included with virtual appliances are shipped in a compressed format that cannot be used directly by VMs. So, the images are first unpacked and copied, which might take several minutes. 


You can use the `VBoxManage import` command to import an appliance. See [VBoxManage import](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage-import "Import a virtual appliance in OVF format or from a cloud service and create virtual machines"). 
#### Exporting an Appliance in OVF Format
The following steps show how to export one or more VMs to OVF format.
  1. Select File,  Export Appliance. 
On the initial Virtual machines page, you can combine several VMs into an OVF appliance. 
Select one or more VMs to export, and click Next. 
  2. The Format Settings page enables you to configure the following settings: 
     * Format: Selects the Open Virtualization Format value for the output files. 
The Oracle Cloud Infrastructure value exports the appliance to Oracle Cloud Infrastructure. See [Exporting an Appliance to Oracle Cloud Infrastructure](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/cloud-integration.html#cloud-export-oci). 
     * File: Selects the location in which to store the exported files. 
     * MAC Address Policy: Specifies whether to retain or reassign network card MAC addresses on export. 
     * Write Manifest File: Enables you to include a manifest file in the exported archive file. 
     * Include ISO Image Files: Enables you to include ISO image files in the exported archive file. 
  3. Click Next to show the Appliance Settings page. 
You can edit settings for the virtual appliance. For example, you can change the name of the virtual appliance or add product information, such as vendor details or license text.
Double-click the appropriate field to change its value.
  4. Click Finish to begin the export process. Note that this operation might take several minutes. 


You can use the `VBoxManage export` command to export an appliance. See [VBoxManage export](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage-export "Export one or more virtual machines to a virtual appliance or to a cloud service"). 
### Removing and Moving Virtual Machines
You can remove a VM from Oracle VirtualBox or move the VM and its associated files, such as disk images, to another location on the host. 
  * Removing a VM. To remove a VM, click Machines in Oracle VirtualBox Manager. Right-click the VM in the machine list and choose Remove. 
The confirmation dialog enables you to specify whether to only remove the VM from the list of machines or to remove the files associated with the VM.
Note that the Remove menu item is disabled while a VM is running. 
  * Moving a VM. To move a VM to a new location on the host, click Machines in Oracle VirtualBox Manager. Right-click the VM in the machine list and choose Move. 
Specify a new location for the VM.
When you move a VM, Oracle VirtualBox configuration files are updated automatically to use the new location on the host. 
Note that the Move menu item is disabled while a VM is running. 
You can also use the `VBoxManage movevm` command to move a VM. See [VBoxManage movevm](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage-movevm "Move a virtual machine to a new location on the host system"). 


For information about removing or moving a disk image file from Oracle VirtualBox, see [The Virtual Media Manager](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/storage.html#ct_virtual-media-manager). 
### Cloning a Virtual Machine
You can create a full copy or a linked copy of an existing VM. This copy is called a clone. You might use a cloned VM to experiment with a VM configuration, to test different guest OS levels, or to back up a VM. 
To clone a VM:
  1. Check the Expert experience level is set. See [Experience Levels for VirtualBox Manager](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/configuring-virtualbox.html#gui-experience-level). 
  2. In Oracle VirtualBox Manager, click Machines. Ensure the VM you want to clone is not running. 
  3. Right-click the VM name in the Machines list, and choose Clone.... 
  4. Enter the following details for the clone. 
     * Name: A name for the cloned machine. 
     * Path: Choose a location for the cloned virtual machine, otherwise Oracle VirtualBox uses the default machines folder. 
     * MAC Address Policy: Specifies whether to retain network card MAC addresses when cloning the VM. 
The Generate New MAC Addresses For All Network Adapters value assigns a new MAC address to each network card during cloning. This is the default setting. This is the best option when both the source VM and the cloned VM must operate on the same network. Other values enable you to retain the existing MAC addresses in the cloned VM. 
     * Keep Disk Names: Retains the disk image names when cloning the VM. 
     * Keep Hardware UUIDs: Retains the hardware universally unique identifiers (UUIDs) when cloning the VM. 
  5. Click Next. The Clone Type page is displayed. 
  6. The Clone Type option specifies whether to create a clone that is linked to the source VM or to create a fully independent clone: 
     * Full Clone: Copies all dependent disk images to the new VM folder. A full clone can operate fully without the source VM. 
     * Linked Clone: Creates new differencing disk images based on the source VM disk images. If you select the current state of the source VM as the clone point, Oracle VirtualBox creates a new snapshot. 
  7. Click Next. If your VM has snapshots and you chose Full Clone, use the Snapshots page to select the parts of the snapshot tree to clone with the VM. 
     * Current Machine State: Clones the current state of the VM. Snapshots are not included. 
     * Everything: Clones the current machine state and all its snapshots. 
  8. Click Finish to start the clone operation. 


The duration of the clone operation depends on the size and number of attached disk images. In addition, the clone operation saves all the differencing disk images of a snapshot. 
You can also use the `VBoxManage clonevm` command to clone a VM. See [VBoxManage clonevm](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage-clonevm "Create a clone of an existing virtual machine"). 
### Managing VMs
As you add, import or create VMs they will appear in the Machines list. 
To change the hardware configuration of a VM. See [Configure the Settings for a VM](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#configbasics)
To use VM Groups, see [Using VM Groups](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#gui-vmgroups). 
Check the Notification Center for tasks in progress and error messages. Click Open notification center to see the list of notifications. Errors are indicated by a warning triangle. 
#### Configure the Settings for a VM
You may need to change the configuration of a Virtual Machine (VM) after it has been created. For example, you may want to add more memory.
Be careful when changing VM settings. It is possible to change all VM settings after installing a guest OS, but certain changes might prevent a guest OS from functioning correctly if done after installation.
To change the settings for a VM: 
  1. Select the VM in the Machines list. 
  2. Ensure the VM is Powered off, not Running or Saved. You can't change fundamental characteristics of the VM if it is running.
  3. Click Settings to see the current configuration for the VM, and change the parameters as required. 


The parameters are described in detail in [Virtual Machine Settings](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ct_settings-window). 
Even more parameters are available when using the `VBoxManage` command line interface. See [VBoxManage Command Reference](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage "Oracle VirtualBox command-line interfaceChange a virtual machine's state based on a saved state fileManage bandwidth groupsCheck encryption password on a DEK-encrypted medium or a disk imageCreate a clone of a mediumCreate a clone of an existing virtual machineRemove a hard disk, DVD, or floppy image from the media registryManage the cloud entitiesManage the cloud profilesChange state and settings for a running virtual machineConvert a raw disk image to a virtual disk imageCreate a new mediumCreate a new virtual machineIntrospection and guest debuggingDHCP server managementDiscard the saved state of a virtual machineManage a DEK-encrypted medium or imageChange encryption and passwords of the VMExport one or more virtual machines to a virtual appliance or to a cloud serviceExtension package managementView keyword values that are associated with a virtual machine or configurationControl a virtual machine from the host systemManage virtual machine guest propertiesManage host-only network interfacesHost Only Network managementImport a virtual appliance in OVF format or from a cloud service and create virtual machinesView system information and VM configuration detailsMedium content accessManage medium propertiesMonitor system resource usageChange the characteristics of an existing disk imageList and modify the NVRAM content of a virtual machineChange settings for a virtual machine that is stoppedMove a virtual machine to a new location on the host systemCreate, modify, and manage a NAT networkManage the tracked objectsRegister a virtual machineSet a keyword value that is associated with a virtual machine or configurationChange global settingsAdd and remove shared folders, configure security policy for shared foldersShow information about a mediumShow configuration information or log file contents for a virtual machineDigitally sign an OVAManage virtual machine snapshotsStart a virtual machineAttach, remove, and modify storage media used by a virtual machineManage a storage controllerUnattended guest OS installationUnregister a virtual machineChecks for a newer version of Oracle VirtualBoxAdd and remove USB device sourcesManage USB filtersFUSE mount a virtual disk image for Mac OS and Linux hosts"). 
#### Using VM Groups
Create VM groups if you want to manage several VMs together, and perform functions on them collectively, as well as individually.
  * Create a group using Oracle VirtualBox Manager. Do one of the following: 
    * Drag a VM on top of another VM.
    * Select multiple VMs and choose Move to Group, New Group from the right-click menu. 
  * A default name is assigned to new groups, following the format New Group <Number>. To rename the new group, right-click on the group's name and choose Rename Group. Type the new name, and then press Enter. 
  * To remove a VM from a group, right-click the VM and choose Move to Group, No Group. 
  * Create and manage a group using the command line. Do one of the following:
    * Create a group and assign a VM. For example:

```
VBoxManage modifyvm "vm01" --groups "/TestGroup"
```

This command creates a group `TestGroup` and attaches the VM `vm01` to that group. 
    * Detach a VM from the group, and delete the group if empty. For example:

```
VBoxManage modifyvm "vm01" --groups ""
```

This command detaches all groups from the VM `vm01` and deletes the empty group. 
  * Create multiple groups. For example: 

```
VBoxManage modifyvm "vm01" --groups "/TestGroup,/TestGroup2"
```

This command creates the groups `TestGroup` and `TestGroup2`, if they do not exist, and attaches the VM `vm01` to both of them. 
  * Create nested groups, having a group hierarchy. For example: 

```
VBoxManage modifyvm "vm01" --groups "/TestGroup/TestGroup2"
```

This command attaches the VM `vm01` to the subgroup `TestGroup2` of the `TestGroup` group. 
  * Use Oracle VirtualBox Manager menu options to control and manage all the VMs in a group. For example: Start, Pause, Reset, Close (save state, send shutdown signal, poweroff), Discard Saved State, Show in Explorer, Sort. 


### Snapshots
With snapshots, you can save a particular state of a virtual machine for later use. At any later time, you can revert to that state, even though you may have changed the VM considerably since then. A snapshot of a virtual machine is thus similar to a machine in Saved state, but there can be many of them, and these saved states are preserved.
To see the snapshots of a virtual machine, click the VM name in the Machines list in Oracle VirtualBox Manager, and then click Snapshots. 
If you select multiple VMs in the machine list, all snapshots are listed for each VM.
Until you take a snapshot of the virtual machine, the list of snapshots will be empty, except for the Current State item. This item represents the current point in the lifetime of the virtual machine. 
The Snapshots toolbar includes the following snapshot operations: 
  * Take. Takes a snapshot of the selected VM. See [Taking, Restoring, and Deleting Snapshots](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#snapshots-take-restore-delete). 
  * Delete. Removes a snapshot from the list of snapshots. See [Taking, Restoring, and Deleting Snapshots](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#snapshots-take-restore-delete). 
  * Restore. Restores the VM state to be the same as the selected snapshot. See [Taking, Restoring, and Deleting Snapshots](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#snapshots-take-restore-delete). 
  * Properties. Displays the properties for the selected snapshot. The Attributes tab is used to specify a Name and Description for the snapshot. The Information tab shows VM settings for the snapshot. 
  * Clone. Displays the Clone Virtual Machine workflow. This enables you to create a clone of the VM, based on the selected snapshot. 
  * Settings. Available for the Current State snapshot only. Displays the Settings window for the VM, enabling you to make configuration changes. 
  * Discard. For a running VM, discards the saved state for the VM and closes it down. 
  * Start. Start the VM. This operation is available for the Current State item. 


#### Taking, Restoring, and Deleting Snapshots
There are three operations related to snapshots, as follows: 
  1. Take a snapshot. This makes a copy of the machine's current state, to which you can go back at any given time later. 
     * If your VM is running: 
In the VM window, select Take Snapshot from the Machine menu. 
The VM is paused while the snapshot is being created. After snapshot creation, the VM continues to run as normal.
     * In Oracle VirtualBox Manager, if your VM is in either the Saved or the Powered Off state, as displayed next to the VM name in the Machines list: 
Click Snapshots and do one of the following: 
       * Click Take in the Snapshots toolbar. 
       * Right-click the Current State item in the snapshots list and select Take. 
A dialog is displayed, prompting you for a snapshot name. This name is purely for reference purposes, to help you remember the state of the snapshot. For example, a useful name would be Fresh installation from scratch, no Guest Additions, or Service Pack 3 just installed. You can also add a longer text description in the Snapshot Description field. 
Your new snapshot will then appear in the snapshots list. Underneath your new snapshot, you will see an item called Current State, signifying that the current state of your VM is a variation based on the snapshot you took earlier. If you later take another snapshot, you will see that they are displayed in sequence, and that each subsequent snapshot is derived from an earlier one. 
Oracle VirtualBox imposes no limits on the number of snapshots you can take. The only practical limitation is disk space on your host. Each snapshot stores the state of the virtual machine and thus occupies some disk space. See [Snapshot Contents](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#snapshots-contents) for details on what is stored in a snapshot. 
  2. Restore a snapshot. In the Snapshots tab, select the snapshot you have taken and click Restore in the toolbar. By restoring a snapshot, you go back or forward in time. The current state of the machine is lost, and the machine is restored to the exact state it was in when the snapshot was taken. 
Note:
Restoring a snapshot will affect the virtual hard drives that are connected to your VM, as the entire state of the virtual hard drive will be reverted as well. This means also that all files that have been created since the snapshot and all other file changes will be lost. In order to prevent such data loss while still making use of the snapshot feature, it is possible to add a second hard drive in write-through mode using the `VBoxManage` interface and use it to store your data. As write-through hard drives are not included in snapshots, they remain unaltered when a machine is reverted. See [Special Image Write Modes](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/storage.html#hdimagewrites). 
To avoid losing the current state when restoring a snapshot, you can create a new snapshot before the restore operation.
By restoring an earlier snapshot and taking more snapshots from there, it is even possible to create a kind of alternate reality and to switch between these different histories of the virtual machine. This can result in a whole tree of virtual machine snapshots.
  3. Delete a snapshot. This does not affect the state of the virtual machine, but only releases the files on disk that Oracle VirtualBox used to store the snapshot data, thus freeing disk space. To delete a snapshot, select the snapshot name in the Snapshots tab and click Delete in the toolbar. Snapshots can be deleted even while a machine is running. 
Note:
Whereas taking and restoring snapshots are fairly quick operations, deleting a snapshot can take a considerable amount of time since large amounts of data may need to be copied between several disk image files. Temporary disk files may also need large amounts of disk space while the operation is in progress.
There are some situations that cannot be handled while a VM is running, and you will get an appropriate message that you need to perform this snapshot deletion when the VM is shut down.


#### Snapshot Contents
Think of a snapshot as a point in time that you have preserved. More formally, a snapshot consists of the following: 
  * The snapshot contains a complete copy of the VM settings, including the hardware configuration, so that when you restore a snapshot, the VM settings are restored as well. For example, if you changed the hard disk configuration or the VM's system settings, that change is undone when you restore the snapshot. 
The copy of the settings is stored in the machine configuration, an XML text file, and thus occupies very little space. 
  * The complete state of all the virtual disks attached to the machine is preserved. Going back to a snapshot means that all changes that had been made to the machine's disks, file by file and bit by bit, will be undone. Files that were since created will disappear, files that were deleted will be restored, changes to files will be reverted. 
Strictly speaking, this is only true for virtual hard disks in "normal" mode. You can configure disks to behave differently with snapshots, see [Special Image Write Modes](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/storage.html#hdimagewrites). In technical terms, it is not the virtual disk itself that is restored when a snapshot is restored. Instead, when a snapshot is taken, Oracle VirtualBox creates differencing images which contain only the changes since the snapshot were taken. When the snapshot is restored, Oracle VirtualBox throws away that differencing image, thus going back to the previous state. This is both faster and uses less disk space. For the details, which can be complex, see [Differencing Images](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/storage.html#diffimages). 
Creating the differencing image as such does not occupy much space on the host disk initially, since the differencing image will initially be empty and grow dynamically later with each write operation to the disk. The longer you use the machine after having created the snapshot, however, the more the differencing image will grow in size. 
  * If you took a snapshot while the machine was running, the memory state of the machine is also saved in the snapshot. This is in the same way that memory can be saved when you close a VM window. When you restore such a snapshot, execution resumes at exactly the point when the snapshot was taken. 
The memory state file can be as large as the memory size of the VM and will therefore occupy considerable disk space. 


### Emulated Hardware
Oracle VirtualBox virtualizes nearly all of the host's hardware. Depending on a VM's configuration, the guest will see the following virtual hardware: 
  * Input devices.Oracle VirtualBox can emulate a standard PS/2 keyboard and mouse. These devices are supported by most guest OSes. 
In addition, Oracle VirtualBox can provide virtual USB input devices to avoid having to capture mouse and keyboard, as described in [Capturing and Releasing Keyboard and Mouse](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#keyb_mouse_normal). 
  * Graphics. The default Oracle VirtualBox graphics device for Windows guests is an SVGA device. For Linux guests, the default graphics device emulates a VMware SVGA graphics device. See [Screen Tab](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#settings-screen). 
For legacy guest OSes, a VGA-compatible graphics device is available. 
  * Storage.Oracle VirtualBox emulates the most common types of hard disk controllers. See [Hard Disk Controllers](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/storage.html#harddiskcontrollers). Whereas supporting only one of these controllers would be enough for Oracle VirtualBox by itself, this multitude of storage adapters is required for compatibility with other hypervisors. Windows is very selective about its boot devices, and migrating VMs between hypervisors is very difficult or impossible if the storage controllers are different. 
  * Networking. See [Virtual Networking Hardware](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/networkingdetails.html#nichardware). 
  * USB.Oracle VirtualBox emulates the most common USB host controllers. See [USB Support](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ct_usb-support). 
The emulated USB controllers do not communicate directly with devices on the host. Instead they communicate with a virtual USB layer that abstracts the USB protocol and enables the use of remote USB devices. 
  * Audio. See [Audio Settings](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#ct_settings-audio). 


### Paravirtualization Providers
Oracle VirtualBox enables the exposure of a paravirtualization interface, to facilitate accurate and efficient execution of software within a virtual machine. These interfaces require the guest operating system to recognize their presence and make use of them in order to leverage the benefits of communicating with the Oracle VirtualBox hypervisor. 
Most modern, mainstream guest operating systems, including Windows and Linux, ship with support for one or more paravirtualization interfaces. Hence, there is typically no need to install additional software in the guest to take advantage of this feature. 
Exposing a paravirtualization provider to the guest operating system does not rely on the choice of host platforms. For example, the Hyper-V paravirtualization provider can be used for VMs to run on any host platform supported by Oracle VirtualBox and not just Windows. 
Oracle VirtualBox provides the following interfaces: 
  * Minimal: Announces the presence of a virtualized environment. Additionally, reports the TSC and APIC frequency to the guest operating system. This provider is mandatory for running any Mac OS X guests. 
  * KVM: Presents a Linux KVM hypervisor interface which is recognized by Linux kernels version 2.6.25 or later. Oracle VirtualBox's implementation currently supports paravirtualized clocks and SMP spinlocks. This provider is recommended for Linux guests. 
  * Hyper-V: Presents a Microsoft Hyper-V hypervisor interface which is recognized by Windows 7 and newer operating systems. Oracle VirtualBox's implementation currently supports paravirtualized clocks, APIC frequency reporting, guest debugging, guest crash reporting and relaxed timer checks. This provider is recommended for Windows guests. 


### Nested Paging and VPIDs
In addition to normal hardware virtualization, your processor may also support the following additional sophisticated techniques:
  * Nested paging implements some memory management in hardware, which can greatly accelerate hardware virtualization since these tasks no longer need to be performed by the virtualization software. 
With nested paging, the hardware provides another level of indirection when translating linear to physical addresses. Page tables function as before, but linear addresses are now translated to "guest physical" addresses first and not physical addresses directly. A new set of paging registers now exists under the traditional paging mechanism and translates from guest physical addresses to host physical addresses, which are used to access memory. 
Nested paging eliminates the overhead caused by VM exits and page table accesses. In essence, with nested page tables the guest can handle paging without intervention from the hypervisor. Nested paging thus significantly improves virtualization performance. 
On AMD processors, nested paging has been available starting with the Barcelona (K10) architecture. They now call it rapid virtualization indexing (RVI). Intel added support for nested paging, which they call extended page tables (EPT), with their Core i7 (Nehalem) processors. 
If nested paging is enabled, the Oracle VirtualBox hypervisor can also use large pages to reduce TLB usage and overhead. This can yield a performance improvement of up to 5%. To enable this feature for a VM, you use the `VBoxManage modifyvm --large-pages` command. See [VBoxManage modifyvm](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage-modifyvm "Change settings for a virtual machine that is stopped"). 
If you have an Intel CPU with EPT, please consult [CVE-2018-3646](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Security.html#sec-rec-cve-2018-3646) for security concerns regarding EPT. 
  * On Intel CPUs, a hardware feature called Virtual Processor Identifiers (VPIDs) can greatly accelerate context switching by reducing the need for expensive flushing of the processor's Translation Lookaside Buffers (TLBs). 
To enable these features for a VM, you use the `VBoxManage modifyvm --vtx-vpid` and `VBoxManage modifyvm --large-pages` commands. See [VBoxManage modifyvm](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage-modifyvm "Change settings for a virtual machine that is stopped"). 


### Virtual Machine Settings
Settings for a virtual machine are configured using the Settings window. 
To display the Settings window, do either of the following: 
  * In the Machines list, right-click the virtual machine name, and click Settings.... 
  * In the Machines list, click the virtual machine name, and then click Settings on the toolbar. 


Note:
The available settings depend on the selected experience level. To display all available settings, ensure the experience level is set to Expert. 
See [Experience Levels for VirtualBox Manager](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/configuring-virtualbox.html#gui-experience-level). 
### General Settings
In the Settings window, under General, you can configure the most fundamental aspects of the virtual machine such as memory and essential hardware. The following tabs are available. 
#### Identity Tab
On the Identity tab of the General settings category, you can find these settings: 
  * VM Name: The name of the the VM, as shown in the list of VMs in the main VirtualBox Manager window. Using this name, Oracle VirtualBox also saves the VM's configuration files. If you change the name, Oracle VirtualBox renames these files as well. As a result, you can only use characters which are allowed for file names on your host OS. 
Note that internally, Oracle VirtualBox uses unique identifiers (UUIDs) to identify virtual machines. You can display these using the `VBoxManage` commands. 
  * OS: The type of guest OS for the VM. Additionally, set the OS Distribution or OS Edition, and OS Version. For example, if the OS is Linux, the OS Distribution might be Oracle Linux and the OS Version might be Oracle Linux 8.x (64-bit). 
These are the same settings that are specified in the New Virtual Machine workflow. See [Creating a New Virtual Machine](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/create-vm.html#tk_create-vm). 
Whereas the default settings of a newly created VM depend on the selected OS, changing the OS later has no effect on VM settings.


#### Features Tab
The following settings are available in the Features tab: 
  * Snapshot Folder: By default, Oracle VirtualBox saves snapshot data together with your other Oracle VirtualBox configuration data. See [Where Oracle VirtualBox Stores its Files](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Troubleshooting.html#vboxconfigdata). With this setting, you can specify any other folder for each VM. 
  * Shared Clipboard: You can select here whether the clipboard of the guest OS should be shared with that of your host. If you select Bidirectional, then Oracle VirtualBox will always make sure that both clipboards contain the same data. If you select Host to Guest or Guest to Host, then Oracle VirtualBox will only ever copy clipboard data in one direction. 
Clipboard sharing requires the Oracle VirtualBox [Guest Additions](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/guestadditions.html#guestadditions). 
For security reasons, the shared clipboard is disabled by default. This setting can be changed at any time using the Shared Clipboard menu item in the Devices menu of the virtual machine. 
  * Drag and Drop: You can select multiple drag and drop modes for a VM to enable or restrict access in either direction. 
For drag and drop to work, the Guest Additions need to be installed on the guest.
Note:
Drag and drop is disabled by default. This setting can be changed at any time using the Drag and Drop menu item in the Devices menu of the virtual machine. 
See [Drag and Drop](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/guestadditions.html#guestadd-dnd). 


#### Description Tab
On the Description tab you can enter a description for your virtual machine. This has no effect on the functionality of the machine, but you may find this space useful to note down things such as the configuration of a virtual machine and the software that has been installed into it. 
To insert a line break into the Description text field, press Shift+Enter. 
#### Disk Encryption Tab
The Disk Encryption tab enables you to encrypt disks that are attached to the virtual machine. 
To enable disk encryption, select the Encrypt Disks check box. 
Settings are available to configure the cipher used for encryption and the encryption password.
Note:
All files related to the virtual machine except disk images are stored unencrypted. To encrypt these files, use the `VBoxManage encryptvm` command as described in [Encryption of VMs](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/AdvancedTopics.html#vmencryption). 
### System Settings
The System category groups various settings that are related to the basic hardware that is presented to the virtual machine. 
Note:
As the activation mechanism of Windows is sensitive to hardware changes, if you are changing hardware settings for a Windows guest, some of these changes may trigger a request for another activation with Microsoft.
The following tabs are available.
#### Motherboard Tab
On the Motherboard tab, you can configure virtual hardware that would normally be on the motherboard of a real computer. 
  * Base Memory: Sets the amount of RAM that is allocated and given to the VM when it is running. The specified amount of memory will be requested from the host OS, so it must be available or made available as free memory on the host when attempting to start the VM and will not be available to the host while the VM is running. This is the same setting that was specified when [Creating a New Virtual Machine](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/create-vm.html#tk_create-vm). 
Generally, it is possible to change the memory size after installing the guest OS. But you must not reduce the memory to an amount where the OS would no longer boot.
  * Boot Device Order (BIOS only): Determines the order in which the guest OS will attempt to boot from the various virtual boot devices. Analogous to a real PC's BIOS setting, Oracle VirtualBox can tell a guest OS to start from the virtual floppy, the virtual CD/DVD drive, the virtual hard drive (each of these as defined by the other VM settings), the network, or none of these. 
If you select Network, the VM will attempt to boot from a network using the PXE mechanism. This needs to be configured in detail on the command line. See [VBoxManage modifyvm](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage-modifyvm "Change settings for a virtual machine that is stopped"). 
  * Chipset: You can select which chipset will be presented to the virtual machine. This can't be changed on VMs with an Arm architecture. PIIX3 is the default chipset for most guests. For some guest OSs, the PIIX3 chipset is not well supported. As a result, Oracle VirtualBox provides an emulation of the ICH9 chipset, which supports PCI express, three PCI buses, PCI-to-PCI bridges and Message Signaled Interrupts (MSI). This enables modern OSs to address more PCI devices and no longer requires IRQ sharing. Using the ICH9 chipset it is also possible to configure up to 36 network cards, compared to a maximum of eight network adapters with PIIX3. 
  * TPM Version: Enables support for a Trusted Platform Module (TPM) security processor. Choose from the available TPM versions. This can't be changed on VMs with an Arm architecture. 
  * Pointing Device: The default virtual pointing device for some guest OSs is the traditional PS/2 mouse. If set to USB Tablet, Oracle VirtualBox reports to the virtual machine that a USB tablet device is present and communicates mouse events to the virtual machine through this device. Another setting is USB Multi-Touch Tablet, which is suitable for guests running Windows 8 or later. 
Using the virtual USB tablet has the advantage that movements are reported in absolute coordinates, instead of as relative position changes. This enables Oracle VirtualBox to translate mouse events over the VM window into tablet events without having to capture the mouse in the guest as described in [Capturing and Releasing Keyboard and Mouse](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#keyb_mouse_normal). This makes using the VM less tedious even if Guest Additions are not installed. 
  * I/O APIC: Advanced Programmable Interrupt Controllers (APICs) are an x86 hardware feature that have replaced Programmable Interrupt Controllers (PICs). With an I/O APIC, OSs can use more than 16 interrupt requests (IRQs) and therefore avoid IRQ sharing for improved reliability. Can't be changed on VMs with an Arm architecture. 
Note:
Enabling the I/O APIC is required for 64-bit Windows guest OSs. It is also required if you want to use more than one virtual CPU in a virtual machine. 
However, software support for I/O APICs has been unreliable with some OSs other than Windows. Also, the use of an I/O APIC slightly increases the overhead of virtualization and therefore slows down the guest OS a little.
Note:
All Windows OSs install different kernels, depending on whether an I/O APIC is available. As with ACPI, the I/O APIC therefore must not be turned off after installation of a Windows guest OS. Turning it on after installation will have no effect however. 
  * Hardware Clock in UTC: If selected, Oracle VirtualBox will report the system time in UTC format to the guest instead of the local (host) time. This affects how the virtual real-time clock (RTC) operates and may be useful for UNIX-like guest OSs, which typically expect the hardware clock to be set to UTC. 
  * UEFI Enables Extensible Firmware Interface (EFI), which replaces the legacy BIOS and may be useful for certain advanced use cases. See [Alternative Firmware (UEFI)](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#efi). Can't be changed on VMs with an Arm architecture. 
  * Secure Boot: Enables Secure Boot, to provide a secure environment for starting the guest OS. 


In addition, you can turn off the Advanced Configuration and Power Interface (ACPI) which Oracle VirtualBox presents to the guest OS by default. 
ACPI is the current industry standard to allow OSs to recognize hardware, configure motherboards and other devices and manage power. As most computers contain this feature and Windows and Linux support ACPI, it is also enabled by default in Oracle VirtualBox. However, no ACPI information, such as battery status or power source, is reported to Oracle Solaris guests. 
ACPI can only be turned off using the command line. See [VBoxManage modifyvm](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage-modifyvm "Change settings for a virtual machine that is stopped"). 
Note:
All Windows OSs install different kernels, depending on whether ACPI is available. This means that ACPI must not be turned off after installation of a Windows guest OS. However, turning it on after installation will have no effect. 
#### Processor Tab
On the Processor tab, you can configure settings for the CPU used by the virtual machine. 
  * Number of CPUs: Sets the number of virtual CPU cores the guest OSes can see. Oracle VirtualBox supports symmetrical multiprocessing (SMP) and can present up to 32 virtual CPU cores to each virtual machine. 
You should not configure virtual machines to use more CPU cores than are available physically. This includes real cores, with no hyperthreads.
  * Processing Cap: Configures the CPU processing cap. This limits the amount of time a host CPU spends to emulate a virtual CPU. The default setting is 100%, meaning that there is no limitation. A setting of 50% implies a single virtual CPU can use up to 50% of a single host CPU. Note that limiting the execution time of the virtual CPUs may cause guest timing problems. 
A warning is displayed at the bottom of the Processor tab if a Processing Cap setting is made that may affect system performance.
  * PAE/NX: Determines whether the PAE (Physical Address Extension) and NX capabilities of the host CPU will be exposed to the virtual machine. Can't be changed on VMs with an Arm architecture. 
Normally, if enabled and supported by the OS, then even a 32-bit x86 CPU can access more than 4 GB of RAM. This is made possible by adding another 4 bits to memory addresses, so that with 36 bits, up to 64 GB can be addressed. Some OSs, such as Ubuntu Server, require PAE support from the CPU and cannot be run in a virtual machine without it.
  * Nested VT-x/AMD-V: Enables nested virtualization, with passthrough of hardware virtualization functions to the guest VM. Can't be changed on VMs with an Arm architecture. 


With virtual machines running modern server OSs, Oracle VirtualBox also supports CPU hot-plugging. For details, see [CPU Hot-Plugging](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/AdvancedTopics.html#cpuhotplug). 
#### Acceleration Tab
On this tab, you can configure Oracle VirtualBox to use hardware virtualization extensions that your host CPU supports. 
  * Paravirtualization Interface: Oracle VirtualBox provides paravirtualization interfaces to improve time-keeping accuracy and performance of guest OSs. The options available are documented under the `--paravirt-provider` option in [VBoxManage Command Reference](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage "Oracle VirtualBox command-line interfaceChange a virtual machine's state based on a saved state fileManage bandwidth groupsCheck encryption password on a DEK-encrypted medium or a disk imageCreate a clone of a mediumCreate a clone of an existing virtual machineRemove a hard disk, DVD, or floppy image from the media registryManage the cloud entitiesManage the cloud profilesChange state and settings for a running virtual machineConvert a raw disk image to a virtual disk imageCreate a new mediumCreate a new virtual machineIntrospection and guest debuggingDHCP server managementDiscard the saved state of a virtual machineManage a DEK-encrypted medium or imageChange encryption and passwords of the VMExport one or more virtual machines to a virtual appliance or to a cloud serviceExtension package managementView keyword values that are associated with a virtual machine or configurationControl a virtual machine from the host systemManage virtual machine guest propertiesManage host-only network interfacesHost Only Network managementImport a virtual appliance in OVF format or from a cloud service and create virtual machinesView system information and VM configuration detailsMedium content accessManage medium propertiesMonitor system resource usageChange the characteristics of an existing disk imageList and modify the NVRAM content of a virtual machineChange settings for a virtual machine that is stoppedMove a virtual machine to a new location on the host systemCreate, modify, and manage a NAT networkManage the tracked objectsRegister a virtual machineSet a keyword value that is associated with a virtual machine or configurationChange global settingsAdd and remove shared folders, configure security policy for shared foldersShow information about a mediumShow configuration information or log file contents for a virtual machineDigitally sign an OVAManage virtual machine snapshotsStart a virtual machineAttach, remove, and modify storage media used by a virtual machineManage a storage controllerUnattended guest OS installationUnregister a virtual machineChecks for a newer version of Oracle VirtualBoxAdd and remove USB device sourcesManage USB filtersFUSE mount a virtual disk image for Mac OS and Linux hosts") `modifyvm`. For further details on the paravirtualization providers, see [Paravirtualization Providers](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#gimproviders). 
  * Hardware Virtualization: 
    * Nested Paging: If the host CPU supports the nested paging (AMD-V) or EPT (Intel VT-x) features, then you can expect a significant performance increase by enabling nested paging in addition to hardware virtualization. For technical details, see [Nested Paging and VPIDs](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#nestedpaging). For Intel EPT security recommendations, see [CVE-2018-3646](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Security.html#sec-rec-cve-2018-3646). 


### Display Settings
The following tabs are available for configuring the display for a virtual machine. 
#### Screen Tab
  * Video Memory: Sets the size of the memory provided by the virtual graphics card available to the guest, in megabytes. As with the main memory, the specified amount will be allocated from the host's resident memory. Based on the amount of video memory, higher resolutions and color depths may be available. 
Oracle VirtualBox Manager will show a warning if the amount of video memory is too small to be able to switch the VM into full screen mode. The minimum value depends on the number of virtual monitors, the screen resolution and the color depth of the host display as well as on the use of 3D acceleration. A rough estimate is (color depth / 8) x vertical pixels x horizontal pixels x number of screens = number of bytes. Extra memory may be required if display acceleration is used. 
  * Number of Virtual Monitors: With this setting, Oracle VirtualBox can provide more than one virtual monitor to a virtual machine. If a guest OS supports multiple attached monitors, Oracle VirtualBox can pretend that multiple virtual monitors are present. Up to eight such virtual monitors are supported. 
The output of the multiple monitors are displayed on the host in multiple VM windows which are running side by side. However, in full screen and seamless mode, they use the available physical monitors attached to the host. As a result, for full screen and seamless modes to work with multiple monitors, you will need at least as many physical monitors as you have virtual monitors configured, or Oracle VirtualBox will report an error. 
You can configure the relationship between guest and host monitors using the View menu by pressing Host key + Home when you are in full screen or seamless mode. 
See also [Known Issues](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Troubleshooting.html#known-issues). 
  * Scale Factor: Enables scaling of the display size. For multiple monitor displays, you can set the scale factor for individual monitors, or globally for all of the monitors. Use the slider to select a scaling factor up to 200%. 
You can set a default scale factor for all VMs. Use the Display tab in the Preferences window. 
  * Graphics Controller: Specifies the graphics adapter type used by the guest VM. Note that you must install the Guest Additions on the guest VM to specify the VBoxSVGA or VMSVGA graphics controller. The following options are available: 
    * VBoxSVGA: The default graphics controller for new VMs that use Windows 7 or later. 
This graphics controller improves performance and 3D support when compared to the legacy VBoxVGA option.
    * VBoxVGA: Use this graphics controller for legacy guest OSes. This is the default graphics controller for Windows versions before Windows 7 and for Oracle Solaris. 
3D acceleration is not supported for this graphics controller. 
    * VMSVGA: Use this graphics controller to emulate a VMware SVGA graphics device. This is the default graphics controller for Linux guests. 
    * None: Does not emulate a graphics adapter type. 
  * 3D Acceleration: If a virtual machine has Guest Additions installed, you can enable accelerated 3D graphics on the VM. With 3D acceleration enabled, the VM also uses video decoding acceleration if the host also supports video decoding acceleration. See [Hardware-Accelerated Graphics](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/guestadditions.html#guestadd-video). 


#### Remote Display Tab
On the Remote Display tab, if the VirtualBox Remote Display Extension (VRDE) is installed, you can enable the VRDP server that is built into Oracle VirtualBox. This enables you to connect to the console of the virtual machine remotely with any standard RDP viewer, such as `mstsc.exe` that comes with Microsoft Windows. On Linux and Oracle Solaris systems you can use the standard open source `rdesktop` program. These features are described in [Remote Display (VRDP Support)](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/remotevm.html#vrde). 
  * Enable Server: Select this check box and configure settings for the remote display connection. 


#### Recording Tab
On the Recording tab you can enable video and audio recording for a virtual machine and change related settings. Note that these features can be enabled and disabled while a VM is running. Settings apply to all selected screens. 
  * Enable Recording: Select this check box and select a Recording Mode option. 
  * Recording Mode: You can choose to record video, audio, or both video and audio. 
Some settings on the Recording tab may be grayed out, depending on the Recording Mode setting. 
  * File Path: The file where the recording is saved. 
  * Frame Size: The video resolution of the recorded video, in pixels. The drop-down list enables you to select from common frame sizes. 
  * Frame Rate: Use the slider to set the maximum number of video frames per second (FPS) to record. Frames that have a higher frequency are skipped. Increasing this value reduces the number of skipped frames and increases the file size. 
  * Video Quality: Use the slider to set the bit rate of the video in kilobits per second. Increasing this value improves the appearance of the video at the cost of an increased file size. 
  * Audio Quality: Use the slider to set the quality of the audio recording. Increasing this value improves the audio quality at the cost of an increased file size. 
  * Screens: For a multiple monitor display, you can select which screens to record video from. 


As you adjust the video and audio recording settings, the approximate output file size for a five minute video is shown.
### Storage Settings
The Storage category in the VM settings enables you to connect virtual hard disk and CD/DVD images and drives to your virtual machine. 
In a real computer, so-called storage controllers connect physical disk drives to the rest of the computer. Similarly, Oracle VirtualBox presents virtual storage controllers to a virtual machine. Under each controller, the virtual devices, such as hard disks and CD/DVD drives, attached to the controller are shown. 
Note:
This section gives a quick introduction to the Oracle VirtualBox storage settings. See [Virtual Storage](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/storage.html#storage) for a full description of the available storage settings in Oracle VirtualBox. 
Depending on the guest OS type that you selected when you created the VM, a new VM includes the following storage devices:
  * IDE controller. A virtual CD/DVD drive is attached to device 0 on the secondary channel of the IDE controller. 
  * SATA controller. This is a modern type of storage controller for higher hard disk data throughput, to which the virtual hard disks are attached. Initially you will normally have one such virtual disk, but as shown in the previous screenshot, you can have more than one. Each is represented by a disk image file, such as a VDI file in this example. 


VMs with an Arm architecture have VirtIO SCSI only.
If you created your VM with an older version of Oracle VirtualBox, the default storage layout may differ. You might then only have an IDE controller to which both the CD/DVD drive and the hard disks have been attached. This might also apply if you selected an older OS type when you created the VM. Since older OSes do not support SATA without additional drivers, Oracle VirtualBox will make sure that no such devices are present initially. See [Hard Disk Controllers](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/storage.html#harddiskcontrollers). 
Oracle VirtualBox also provides a floppy controller. You cannot add devices other than floppy drives to this controller. Virtual floppy drives, like virtual CD/DVD drives, can be connected to either a host floppy drive, if you have one, or a disk image, which in this case must be in RAW format. 
You can modify these media attachments freely. For example, if you want to copy some files from another virtual disk that you created, you can connect that disk as a second hard disk, as in the above screenshot. You could also add a second virtual CD/DVD drive, or change where these items are attached. The following options are available: 
  * To add another virtual hard disk, or a CD/DVD or floppy drive, select the storage controller to which it should be added (such as IDE, SATA, SCSI, SAS, floppy controller) and then click the Add Disk button below the tree. You can then either select Optical Drive or Hard Disk. If you clicked on a floppy controller, you can add a floppy drive instead. Alternatively, right-click the storage controller and select a menu item there. 
A dialog is displayed, enabling you to select an existing disk image file or to create a new disk image file. Depending on the type of disk image, the dialog is called Hard Disk Selector, Optical Disk Selector, or Floppy Disk Selector. 
See [Disk Image Files (VDI, VMDK, VHD, HDD)](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/storage.html#vdidetails) for information on the image file types that are supported by Oracle VirtualBox. 
For virtual CD/DVD drives, the image files will typically be in the standard ISO format instead. Most commonly, you will select this option when installing an OS from an ISO file that you have obtained from the Internet. For example, most Linux distributions are available in this way. 
Depending on the type of disk image, you can set the following Attributes for the disk image in the right part of the Storage settings page: 
    * The device slot of the controller that the virtual disk is connected to. IDE controllers have four slots: primary device 0, primary device 1, secondary device 0, and secondary device 1. By contrast, SATA and SCSI controllers offer you up to 30 slots for attaching virtual devices. 
    * Solid-state Drive presents a virtual disk to the guest as a solid-state device. 
    * Hot-pluggable presents a virtual disk to the guest as a hot-pluggable device. 
    * For virtual CD/DVD drives, you can select Live CD/DVD. This means that the virtual optical disk is not removed from when the guest system ejects it. 
  * To remove an attachment, either select it and click the Remove icon at the bottom, or right-click the attachment and select the menu item. 


Removable media, such as CD/DVDs and floppies, can be changed while the guest is running. Since the Settings window is not available at that time, you can also access these settings from the Devices menu of your virtual machine window. 
### Audio Settings
The Audio section in a virtual machine's Settings window determines whether the VM will detect a connected sound card, and if the audio output should be played on the host system. 
To enable audio for a guest, select the Enable Audio check box. The following settings are available: 
  * Host Audio Driver: The audio driver that Oracle VirtualBox uses on the host. 
The Default option is enabled by default for all new VMs. This option selects the best audio driver for the host platform automatically. This enables you to move VMs between different platforms without having to change the audio driver. 
On a Linux host, depending on your host configuration, you can select between the OSS, ALSA, or the PulseAudio subsystem. On newer Linux distributions, the PulseAudio subsystem is preferred. 
Only OSS is supported on Oracle Solaris hosts. The Oracle Solaris Audio audio backend is no longer supported on Oracle Solaris hosts. 
  * Audio Controller: You can choose between the emulation of an Intel AC'97 controller, an Intel HD Audio controller, or a SoundBlaster 16 card. 
  * Audio Output: Enables audio output only for the VM. 
  * Audio Input: Enables audio input only for the VM. 


### Network Settings
The Network section in a virtual machine's Settings window enables you to configure how Oracle VirtualBox presents virtual network cards to your VM, and how they operate. 
When you first create a virtual machine, Oracle VirtualBox by default enables one virtual network card and selects the Network Address Translation (NAT) mode for it. This way the guest can connect to the outside world using the host's networking and the outside world can connect to services on the guest which you choose to make visible outside of the virtual machine. 
This default setup is good for the majority of Oracle VirtualBox users. However, Oracle VirtualBox is extremely flexible in how it can virtualize networking. It supports many virtual network cards per virtual machine. The first four virtual network cards can be configured in detail in Oracle VirtualBox Manager. Additional network cards can be configured using the `VBoxManage` command. 
Many networking options are available. See [Virtual Networking](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/networkingdetails.html#networkingdetails) for more information. 
### Serial Ports
Oracle VirtualBox supports the use of virtual serial ports in a virtual machine with an x86 architecture. Serial ports are not available on Arm VMs. 
Ever since the original IBM PC, personal computers have been equipped with one or two serial ports, also called COM ports by DOS and Windows. Serial ports were commonly used with modems, and some computer mice used to be connected to serial ports before USB became commonplace. 
While serial ports are no longer as common as they used to be, there are still some important uses left for them. For example, serial ports can be used to set up a primitive network over a null-modem cable, in case Ethernet is not available. Also, serial ports are indispensable for system programmers needing to do kernel debugging, since kernel debugging software usually interacts with developers over a serial port. With virtual serial ports, system programmers can do kernel debugging on a virtual machine instead of needing a real computer to connect to. 
If a virtual serial port is enabled, the guest OS sees a standard 16550A compatible UART device. Other UART types can be configured using the `VBoxManage modifyvm` command. Both receiving and transmitting data is supported. How this virtual serial port is then connected to the host is configurable, and the details depend on your host OS. 
You can use either the Settings tabs or the `VBoxManage` command to set up virtual serial ports. For the latter, see [VBoxManage modifyvm](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/vboxmanage.html#vboxmanage-modifyvm "Change settings for a virtual machine that is stopped") for information on the `--uart`, `--uart-mode` and `--uart-type` options. 
You can configure up to four virtual serial ports per virtual machine. For each device, you must set the following:
  1. Port Number: This determines the serial port that the virtual machine should see. For best results, use the traditional values as follows: 
     * COM1: I/O base 0x3F8, IRQ 4 
     * COM2: I/O base 0x2F8, IRQ 3 
     * COM3: I/O base 0x3E8, IRQ 4 
     * COM4: I/O base 0x2E8, IRQ 3 
You can also configure a user-defined serial port. Enter an I/O base address and interrupt (IRQ).
  2. Port Mode: What the virtual port is connected to. For each virtual serial port, you have the following options: 
     * Disconnected: The guest will see the device, but it will behave as if no cable had been connected to it. 
     * Host Device: Connects the virtual serial port to a physical serial port on your host. On a Windows host, this will be a name like `COM1`. On Linux or Oracle Solaris hosts, it will be a device node like `/dev/ttyS0`. Oracle VirtualBox will then simply redirect all data received from and sent to the virtual serial port to the physical device. 
     * Host Pipe: Configure Oracle VirtualBox to connect the virtual serial port to a software pipe on the host. This depends on your host OS, as follows: 
       * On a Windows host, data will be sent and received through a named pipe. The pipe name must be in the format `\\.\pipe\name ` where name should identify the virtual machine but may be freely chosen. 
       * On a Mac OS, Linux, or Oracle Solaris host, a local domain socket is used instead. The socket filename must be chosen such that the user running Oracle VirtualBox has sufficient privileges to create and write to it. The `/tmp` directory is often a good candidate. 
On Linux there are various tools which can connect to a local domain socket or create one in server mode. The most flexible tool is `socat` and is available as part of many distributions. 
In this case, you can configure whether Oracle VirtualBox should create the named pipe, or the local domain socket on non-Windows hosts, itself or whether Oracle VirtualBox should assume that the pipe or socket exists already. With the `VBoxManage` command-line options, this is referred to as server mode or client mode, respectively. 
For a direct connection between two virtual machines, corresponding to a null-modem cable, simply configure one VM to create a pipe or socket and another to attach to it. 
     * Raw File: Send the virtual serial port output to a file. This option is very useful for capturing diagnostic output from a guest. Any file may be used for this purpose, as long as the user running Oracle VirtualBox has sufficient privileges to create and write to the file. 
     * TCP: Useful for forwarding serial traffic over TCP/IP, acting as a server, or it can act as a TCP client connecting to other servers. This option enables a remote machine to directly connect to the guest's serial port using TCP. 
       * TCP Server: Deselect the Connect to Existing Pipe/Socket check box and specify the port number in the Path/Address field. This is typically 23 or 2023. Note that on UNIX-like systems you will have to use a port a number greater than 1024 for regular users. 
The client can use software such as `PuTTY` or the `telnet` command line tool to access the TCP Server. 
       * TCP Client: To create a virtual null-modem cable over the Internet or LAN, the other side can connect using TCP by specifying `hostname:port` in the Path/Address field. The TCP socket will act in client mode if you select the Connect to Existing Pipe/Socket check box. 


Up to four serial ports can be configured per virtual machine, but you can pick any port numbers out of the above. However, serial ports cannot reliably share interrupts. If both ports are to be used at the same time, they must use different interrupt levels, for example COM1 and COM2, but not COM1 and COM3. 
### USB Support
#### USB Settings
The USB section in a virtual machine's Settings window enables you to configure Oracle VirtualBox's sophisticated USB support. 
Oracle VirtualBox can enable virtual machines to access the USB devices on your host directly. To achieve this, Oracle VirtualBox presents the guest OS with a virtual USB controller. 
Caution:
As soon as the guest system starts using a USB device, it will be disconnected from the host without a proper shutdown. This may cause data loss.
Note:
USB support on Oracle Solaris hosts requires Oracle Solaris 11 FCS or later. Webcams and other isochronous devices are known to have poor performance.
Oracle VirtualBox also enables your guests to connect to remote USB devices by use of the VirtualBox Remote Desktop Extension (VRDE). See [Remote USB](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/remotevm.html#usb-over-rdp). 
Enable USB for a VM
  1. Ensure the VM is not running.
  2. Select the VM in the machine list, and then click Settings. 
  3. On the USB tab, select Enable USB Controller and choose the USB Controller you need for your guest OS. In most cases this will be xHCI. Only use OHCI or EHCI if your guest OS does not support xHCI. For some legacy Windows guests you'll need to install third party drivers for xHCI support. 
     * OHCI supports USB 1.1 
     * EHCI supports USB 2.0. This also enables OHCI.
     * xHCI supports all USB speeds up to USB 3.0
  4. Specify which devices can be attached to the guest by adding USB Device Filters. USB devices with a matching filter will be automatically passed to the guest once they are attached to the host. USB devices without a matching filter can be passed manually to the guest, for example by using the Devices, USB menu. 
     * Click the USB filter button to create a new filter with blank fields, and then complete the fields. 
     * Or, click the Add USB filter button to create a filter with the fields completed for the selected USB device. 
Give the filter a name, for later reference, and specify the filter criteria. The more criteria you specify, the more precisely devices will be selected. For instance, if you specify only a vendor ID of 046d, all devices produced by Logitech will be available to the guest. If you fill in all fields, on the other hand, the filter will only apply to a particular device model from a particular vendor, and not even to other devices of the same type with a different revision and serial number. 
The following criteria are available: 
     * Vendor and Product ID. With USB, each vendor of USB products carries an identification number that is unique world-wide, called the vendor ID. Similarly, each line of products is assigned a product ID number. Both numbers are commonly written in hexadecimal, and a colon separates the vendor from the product ID. For example, `046d:c016` stands for Logitech as a vendor, and the M-UV69a Optical Wheel Mouse product. 
Alternatively, you can also specify Manufacturer and Product by name. 
To list all the USB devices that are connected to your host machine with their respective vendor IDs and product IDs, use the following command: 

```
VBoxManage list usbhost
```

On Windows, you can also see all USB devices that are attached to your system in the Device Manager. On Linux, you can use the `lsusb` command. 
     * Serial Number. While vendor ID and product ID are quite specific to identify USB devices, if you have two identical devices of the same brand and product line, you will also need their serial numbers to filter them out correctly. 
     * Remote. This setting specifies whether the device will be local only, remote only, such as over VRDP, or either. 
As an example, you could create a new USB filter and specify a vendor ID of 046d for Logitech, Inc, a manufacturer index of 1, and not remote. Then any USB devices on the host system produced by Logitech, Inc with a manufacturer index of 1 will be visible to the guest system. 
Several filters can select a single device. For example, a filter which selects all Logitech devices, and one which selects a particular webcam.
  5. On a Windows host, you will need to unplug and reconnect a USB device to use it after creating a filter for it. 
  6. Ensure the filters you need immediately are selected in the list. Selected filters will be attached automatically when the VM starts.


#### Implementation Notes for Windows and Linux Hosts
On Windows hosts, a kernel mode device driver provides USB proxy support. It implements both a USB monitor, which enables Oracle VirtualBox to capture devices when they are plugged in, and a USB device driver to claim USB devices for a particular virtual machine. System reboots are not necessary after installing the driver. Also, you do not need to replug devices for Oracle VirtualBox to claim them. 
On supported Linux hosts, Oracle VirtualBox accesses USB devices through special files in the file system. When Oracle VirtualBox is installed, these are made available to all users in the `vboxusers` system group. In order to be able to access USB from guest systems, make sure that you are a member of this group. 
### Shared Folders
Shared folders enable you to easily exchange data between a virtual machine and your host, or between VMs. This feature requires that the Oracle VirtualBox Guest Additions be installed in a virtual machine and is described in detail in [Shared Folders](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/guestadditions.html#sharedfolders). 
### User Interface
The User Interface section enables you to change certain aspects of the user interface of the selected VM. 
  * Menu Bar: This widget enables you to disable a complete menu, by clicking on the menu name to deselect it. Menu entries can be disabled, by deselecting the check box next to the entry. On Windows and Linux hosts, the complete menu bar can be disabled by deselecting the check box on the right, after the menus. 
  * Mini ToolBar: In full screen or seamless mode, Oracle VirtualBox can display a small toolbar that contains some of the items that are normally available from the virtual machine's menu bar. This toolbar reduces itself to a small gray line unless you move the mouse over it. With the toolbar, you can return from full screen or seamless mode, control machine execution, or enable certain devices. If you do not want to see the toolbar, disable the Show in Full Screen/Seamless setting. 
The Show at Top of Screen setting enables you to show the toolbar at the top of the screen, instead of showing it at the bottom. 
The Mini Toolbar is not available on macOS hosts. 
  * Status Bar: This widget enables you to disable and reorder icons on the status bar. Deselect the check box of an icon to disable it, or rearrange icons by dragging and dropping the icon. To disable the complete status bar deselect the check box on the left, before the icons. 


### Alternative Firmware (UEFI)
Oracle VirtualBox includes support for the Unified Extensible Firmware Interface (UEFI), which is an industry standard intended to replace the legacy BIOS as the primary interface for bootstrapping computers and certain system services later. 
By default, Oracle VirtualBox uses the BIOS firmware for virtual machines. To use UEFI for a given virtual machine, you can enable EFI in the machine's Settings. See [Motherboard Tab](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#settings-motherboard). Alternatively, use the `VBoxManage` command line interface as follows: 

```
VBoxManage modifyvm "VM name" --firmware efi
```

To switch back to using the BIOS:

```
VBoxManage modifyvm "VM name" --firmware bios
```

Most modern macOS and Windows releases require UEFI. All Arm VMs require UEFI.
Another possible use of UEFI in Oracle VirtualBox is development and testing of UEFI applications, without booting any OS. 
#### Video Modes in EFI
EFI provides two distinct video interfaces: GOP (Graphics Output Protocol) and UGA (Universal Graphics Adapter). Modern OSes, such as Mac OS X, generally use GOP, while some older ones still use UGA. Oracle VirtualBox provides a configuration option to control the graphics resolution for both interfaces, making the difference mostly irrelevant for users. 
The default resolution is 1024x768. To select a graphics resolution for EFI, use the following `VBoxManage` command: 

```
VBoxManage setextradata "VM name" VBoxInternal2/EfiGraphicsResolution HxV
```

Find the horizontal resolution H and the vertical resolution V from the following list of default resolutions: 
Table 5-2 Default Resolutions for Display Types  
| Display Type  | Default Horizontal Resolution (px)  | Default Vertical Resolution (px)  | Color Depth (BPP)  | Display Aspect Ratio  |  
| --- | --- | --- | --- | --- |  
| VGA  | 640  | 480  | 32  | 4:3  |  
| SVGA  | 800  | 600  | 32  | 4:3  |  
| XGA  | 1024  | 768  | 32  | 4:3  |  
| XGA+  | 1152  | 864  | 32  | 4:3  |  
| 1280  | 720  | 32  | 16:9  |  
| WXGA  | 1280  | 800  | 32  | 16:10  |  
| SXGA  | 1280  | 1024  | 32  | 5:4  |  
| SXGA+  | 1400  | 1050  | 32  | 4:3  |  
| WXGA+  | 1440  | 900  | 32  | 16:10  |  
| HD+  | 1600  | 900  | 32  | 16:9  |  
| UXGA  | 1600  | 1200  | 32  | 4:3  |  
| WSXGA+  | 1680  | 1050  | 32  | 16:10  |  
| Full HD  | 1920  | 1080  | 32  | 16:9  |  
| WUXGA  | 1920  | 1200  | 32  | 16:10  |  
| DCI 2K  | 2048  | 1080  | 32  | 19:10  |  
| Full HD+  | 2160  | 1440  | 32  | 3:2  |  
| Unnamed  | 2304  | 1440  | 32  | 16:10  |  
| QHD  | 2560  | 1440  | 32  | 16:9  |  
| WQXGA  | 2560  | 1600  | 32  | 16:10  |  
| QWXGA+  | 2880  | 1800  | 32  | 16:10  |  
| QHD+  | 3200  | 1800  | 32  | 16:9  |  
| WQSXGA  | 3200  | 2048  | 32  | 16:10  |  
| 4K UHD  | 3840  | 2160  | 32  | 16:9  |  
| WQUXGA  | 3840  | 2400  | 32  | 16:10  |  
| DCI 4K  | 4096  | 2160  | 32  | 19:10  |  
| HXGA  | 4096  | 3072  | 32  | 4:3  |  
| UHD+  | 5120  | 2880  | 32  | 16:9  |  
| WHXGA  | 5120  | 3200  | 32  | 16:10  |  
| WHSXGA  | 6400  | 4096  | 32  | 16:10  |  
| HUXGA  | 6400  | 4800  | 32  | 4:3  |  
| 8K UHD2  | 7680  | 4320  | 32  | 16:9  |  
If this list of default resolutions does not cover your needs, see [Custom VESA Resolutions](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/AdvancedTopics.html#customvesa). Note that the color depth value specified in a custom video mode must be specified. Color depths of 8, 16, 24, and 32 are accepted. EFI assumes a color depth of 32 by default. 
The EFI default video resolution settings can only be changed when the VM is powered off. 
#### Specifying Boot Arguments
It is currently not possible to manipulate EFI variables from within a running guest. For example, setting the `boot-args` variable by running the `nvram` tool in a Mac OS X guest will not work. As an alternative method, `VBoxInternal2/EfiBootArgs` extradata can be passed to a VM in order to set the `boot-args` variable. To change the `boot-args` EFI variable, use the following command: 

```
VBoxManage setextradata "VM name" VBoxInternal2/EfiBootArgs <value>
```

### Monitoring of Virtual Machines
Oracle VirtualBox Manager includes the following tools for viewing runtime information, configuration details, and performance metrics of virtual machines and cloud VM instances. 
Note:
To monitor a cloud VM, the Compute Instance Monitoring plugin must be enabled and running on the Oracle Cloud Infrastructure instance. See the Oracle Cloud Infrastructure documentation for more details. 
  * Resources. Displays an overview of performance metrics for all running virtual machines and cloud VM instances. 
See [Resources](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#tk_vm-activity-overview). 
  * Session Information Dialog. Displays configuration and runtime information for the selected VM. 
See [Session Information Dialog](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#tk_vm-activity-session-information). 


#### Resources
The Resources tool displays several performance metrics for all running virtual machines and cloud VM instances, and for the host system. This provides an overview of system resources used by individual virtual machines and the host system. 
To display the Resources, in Oracle VirtualBox Manager click Resources. 
  * To show metrics for all virtual machines, including those that are not running, right-click the list of virtual machines and select List All Virtual Machines. 
  * To show metrics for cloud VMs, right-click the list of virtual machines and select Show Cloud Virtual Machines. 
  * To configure the set of metrics to be shown, click Columns in the toolbar. You can then sort the list of virtual machines by a particular metric. 
  * To see more performance information for a virtual machine, select the VM name and click Resource Use in the toolbar. The Resource Use tab of the Session Information dialog is shown, see [Session Information Dialog](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#tk_vm-activity-session-information). 


#### Session Information Dialog
The Session Information dialog includes multiple tabs that show important configuration and runtime information for the guest system. The tabs are as follows: 
  * Configuration Details. Displays the system configuration of the virtual machine in a tabular format. The displayed information includes details such as storage configuration and audio settings. 
  * Runtime Information. Displays runtime information for the guest session in a tabular format similar to the Configuration Details tab. 
  * Resource Use. Includes several time series charts which monitor guest resource usage including CPU, RAM, Disk I/O, and Network. Note that the RAM chart requires the Guest Additions to be running on the guest system. The Resource Use tab can also be accessed directly from the Resources. See [Resources](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html#tk_vm-activity-overview). 
  * Guest Control. Details of processes used by the Guest Control File Manager. See [Guest Control File Manager](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/guestadditions.html#ct_guestadd-gc-file-manager). 


Note:
For cloud VMs, only the Resource Use tab is shown. 
To display session information for a guest VM or a cloud VM, select the VM name in the Machines list and click the Resource Use tab. 
#### The Log Viewer
Every time you start up a VM, Oracle VirtualBox creates a log file that records system configuration and events. The Log Viewer is a Oracle VirtualBox Manager tool that enables you to view and analyze system logs. 
To display the Log Viewer, do either of the following: 
  * Click the VM name in the machine list and select Logs from the machine tools menu. 
  * In the VM, select Machine, Show Log. 


Log messages for the VM are displayed in tabs in the Log Viewer window. See [Collecting Debugging Information](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Troubleshooting.html#collect-debug-info) for details of the various log files generated by Oracle VirtualBox. 
If you select multiple VMs in the machine list, logs are listed for each VM. 
The toolbar of the Log Viewer includes the following options: 
  * Save: Exports the contents of the selected log file to a text file. Specify the destination filename and location in the displayed dialog. 
  * Find: Searches for a text string in the log file. 
  * Filter: Uses filter terms to display specific types of log messages. Common log message terms used by Oracle VirtualBox, such as Audio and NAT, are included by default. Select one or more terms from the drop-down list. To add your own filter term, enter the text string in the text box field. 
  * Bookmark: Saves the location of a log message, enabling you to find it quickly. To create a bookmark, either click the line number, or select some text and then click Bookmark. 
  * Preferences: Configures the text display used in the log message window. 
  * Refresh: Refreshes the log file you are currently viewing. Only log messages in the current tab are updated. 
  * Reload: Refreshes all log files. Log messages in every tab are updated. 
  * Settings: Displays the Settings window for the VM, enabling you to make configuration changes. 
  * Discard: For a running VM, discards the saved state for the VM and closes it down. 
  * Show/Start: For a running VM, Show displays the VM window. For a stopped VM, Start displays options for powering up the VM. 


