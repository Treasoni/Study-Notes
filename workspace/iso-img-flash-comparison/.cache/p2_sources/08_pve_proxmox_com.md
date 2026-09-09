---
url: "https://pve.proxmox.com/pve-docs/qm.1.html"
title: "qm(1)"
scraped_at: 2026-09-09T15:13:52+00:00
---

☰
# qm(1)
Proxmox Server Solutions GmbH <support@proxmox.com> version 9.2.10, Tue Sep 8 21:32:09 CEST 2026
[↑](https://pve.proxmox.com/pve-docs/qm.1.html)
##  NAME 
qm - QEMU/KVM Virtual Machine Manager
##  SYNOPSIS 
**qm** <COMMAND> [ARGS] [OPTIONS]
**qm agent**
An alias for _qm guest cmd_.
**qm cleanup** <vmid> <clean-shutdown> <guest-requested>
Cleans up resources like tap devices, vgpus, etc. Called after a vm shuts down, crashes, etc. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<clean-shutdown>: <boolean> 
    
Indicates if qemu shutdown cleanly.  

<guest-requested>: <boolean> 
    
Indicates if the shutdown was requested by the guest or via qmp. 
**qm clone** <vmid> <newid> [OPTIONS]
Create a copy of virtual machine/template. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<newid>: <integer> (100 - 999999999) 
    
VMID for the clone.  

--bwlimit <integer> (0 - N) (_default =_ clone limit from datacenter or storage config) 
    
Override I/O bandwidth limit (in KiB/s).  

--description <string> 
    
Description for the new VM.  

--format <qcow2 | raw | vmdk> 
    
Target disk format. Only valid for full clone. If the target storage does not support the format, the storage’s default format is used instead.  

--full <boolean> 
    
Create a full copy of all disks. This is always done when you clone a normal VM. For VM templates, we try to create a linked clone by default.  

--name <string> 
    
Set a name for the new VM.  

--pool <string> 
    
Add the new VM to the specified pool.  

--snapname <string> 
    
The name of the snapshot.  

--storage <storage ID> 
    
Target storage for full clone.  

--target <string> 
    
Target node. Only allowed if the original VM is on shared storage. 
**qm cloudinit dump** <vmid> <type>
Get automatically generated cloudinit config. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<type>: <meta | network | user> 
    
Config type. 
**qm cloudinit pending** <vmid>
Get the cloudinit configuration with both current and pending values. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM. 
**qm cloudinit update** <vmid>
Regenerate and change cloudinit config drive. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM. 
**qm config** <vmid> [OPTIONS]
Get the virtual machine configuration with pending configuration changes applied. Set the _current_ parameter to get the current configuration instead. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--current <boolean> (_default =_ 0) 
    
Get current values (instead of pending values).  

--snapshot <string> 
    
Fetch config values from given snapshot. 
**qm create** <vmid> [OPTIONS]
Create or restore a virtual machine. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--acpi <boolean> (_default =_ 1) 
    
Enable/disable ACPI.  

--affinity <string> 
    
List of host cores used to execute guest processes, for example: 0,5,8-11  

--agent [enabled=]<1|0> [,freeze-fs=<1|0>] [,fstrim_cloned_disks=<1|0>] [,type=<virtio|isa>] 
    
Enable/disable communication with the QEMU Guest Agent and its properties.  

--allow-ksm <boolean> (_default =_ 1) 
    
Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).  

--amd-sev [type=]<sev-type> [,allow-smt=<1|0>] [,kernel-hashes=<1|0>] [,no-debug=<1|0>] [,no-key-sharing=<1|0>] 
    
Secure Encrypted Virtualization (SEV) features by AMD CPUs  

--arch <aarch64 | x86_64> 
    
Virtual processor architecture. Defaults to the host architecture.  

--archive <string> 
    
The backup archive. Either the file system path to a .tar or .vma file (use _-_ to pipe data from stdin) or a proxmox storage backup volume identifier.  

--args <string> 
    
Arbitrary arguments passed to kvm.  

--audio0 device=<ich9-intel-hda|intel-hda|AC97> [,driver=<spice|none>] 
    
Configure a audio device, useful in combination with QXL/Spice.  

--autostart <boolean> (_default =_ 0) 
    
Automatic restart after crash (currently ignored).  

--balloon <integer> (0 - N) 
    
Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.  

--bios <ovmf | seabios> (_default =_ seabios) 
    
Select BIOS implementation.  

--boot [[legacy=]<[acdn]{1,4}>] [,order=<device[;device...]>] 
    
Specify guest boot order. Use the _order=_ sub-property as usage with no key or _legacy=_ is deprecated.  

--bootdisk (ide|sata|scsi|virtio)\d+ 
    
Enable booting from specified disk. Deprecated: Use _boot: order=foo;bar_ instead.  

--bwlimit <integer> (0 - N) (_default =_ restore limit from datacenter or storage config) 
    
Override I/O bandwidth limit (in KiB/s).  

--cdrom <volume> 
    
This is an alias for option -ide2  

--cicustom [meta=<volume>] [,network=<volume>] [,user=<volume>] [,vendor=<volume>] 
    
cloud-init: Specify custom files to replace the automatically generated ones at start.  

--cipassword <password> 
    
cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.  

--citype <configdrive2 | nocloud | opennebula> 
    
Specifies the cloud-init configuration format. The default depends on the configured operating system type (ostype. We use the nocloud format for Linux, and configdrive2 for windows.  

--ciupgrade <boolean> (_default =_ 1) 
    
cloud-init: do an automatic package upgrade after the first boot.  

--ciuser <string> 
    
cloud-init: User name to change ssh keys and password for instead of the image’s configured default user.  

--cores <integer> (1 - N) (_default =_ 1) 
    
The number of cores per socket.  

--cpu [[cputype=]<string>] [,flags=<+FLAG[;-FLAG...]>] [,guest-phys-bits=<integer>] [,hidden=<1|0>] [,hv-vendor-id=<vendor-id>] [,level=<integer>] [,phys-bits=<8-64|host>] [,reported-model=<enum>] 
    
Emulated CPU type.  

--cpulimit <number> (0 - 128) (_default =_ 0) 
    
Limit of CPU usage.  

--cpuunits <integer> (1 - 262144) (_default =_ cgroup v1: 1024, cgroup v2: 100) 
    
CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.  

--description <string> 
    
Description for the VM. Shown in the web-interface VM’s summary. This is saved as comment inside the configuration file.  

--efidisk0 [file=]<volume> [,efitype=<2m|4m>] [,format=<enum>] [,import-from=<source volume>] [,ms-cert=<enum>] [,pre-enrolled-keys=<1|0>] [,size=<DiskSize>] 
    
Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--force <boolean> 
    
Allow to overwrite existing VM.   
| Requires option(s): archive  |  
| --- | 

--freeze <boolean> 
      
Freeze CPU at startup (use _c_ monitor command to start execution).  

--ha-managed <boolean> (_default =_ 0) 
    
Add the VM as a HA resource after it was created.  

--hookscript <string> 
    
Script that will be executed during various steps in the vms lifetime.  

--hostpci[n] [[host=]<HOSTPCIID[;HOSTPCIID2...]>] [,device-id=<hex id>] [,driver=<vfio|keep>] [,legacy-igd=<1|0>] [,mapping=<mapping-id>] [,mdev=<string>] [,pcie=<1|0>] [,rombar=<1|0>] [,romfile=<string>] [,sub-device-id=<hex id>] [,sub-vendor-id=<hex id>] [,vendor-id=<hex id>] [,x-vga=<1|0>] 
    
Map host PCI devices into guest.  

--hotplug <string> (_default =_ network,disk,usb) 
    
Selectively enable hotplug features. This is a comma separated list of hotplug features: _network_ , _disk_ , _cpu_ , _memory_ , _usb_ and _cloudinit_. Use _0_ to disable hotplug completely. Using _1_ as value is an alias for the default network,disk,usb. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.  

--hugepages <1024 | 2 | any> 
    
Enables hugepages memory. 
Sets the size of hugepages in MiB. If the value is set to _any_ then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB. 

--ide[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,model=<model>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--import-working-storage <storage ID> 
    
A file-based storage with _images_ content-type enabled, which is used as an intermediary extraction storage during import. Defaults to the source storage.  

--intel-tdx [type=]<tdx-type> ,attestation=<1|0> [,vsock-cid=<integer>] [,vsock-port=<integer>] 
    
Trusted Domain Extension (TDX) features by Intel CPUs  

--ipconfig[n] [gw=<GatewayIPv4>] [,gw6=<GatewayIPv6>] [,ip=<IPv4Format/CIDR>] [,ip6=<IPv6Format/CIDR>] 
    
cloud-init: Specify IP addresses and gateways for the corresponding interface. 
IP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.
The special string _dhcp_ can be used for IP addresses to use DHCP, in which case no explicit gateway should be provided. For IPv6 the special string _auto_ can be used to use stateless autoconfiguration. This requires cloud-init 19.4 or newer.
If cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using dhcp on IPv4. 

--ivshmem size=<integer> [,name=<string>] 
    
Inter-VM shared memory. Useful for direct communication between VMs, or to the host.  

--keephugepages <boolean> (_default =_ 0) 
    
Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.  

--keyboard <da | de | de-ch | en-gb | en-us | es | fi | fr | fr-be | fr-ca | fr-ch | hu | is | it | ja | lt | mk | nl | no | pl | pt | pt-br | sl | sv | tr> 
    
Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.  

--kvm <boolean> (_default =_ 1) 
    
Enable/disable KVM hardware virtualization.  

--live-restore <boolean> 
    
Start the VM immediately while importing or restoring in the background.  

--localtime <boolean> 
    
Set the real time clock (RTC) to local time. This is enabled by default if the ostype indicates a Microsoft Windows OS.  

--lock <backup | clone | create | migrate | rollback | snapshot | snapshot-delete | suspended | suspending> 
    
Lock/unlock the VM.  

--machine [[type=]<machine type>] [,aw-bits=<number>] [,enable-s3=<1|0>] [,enable-s4=<1|0>] [,viommu=<intel|virtio>] 
    
Specify the QEMU machine.  

--memory [current=]<integer> 
    
Memory properties.  

--migrate_downtime <number> (0 - N) (_default =_ 0.1) 
    
Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).  

--migrate_speed <integer> (0 - N) (_default =_ 0) 
    
Set maximum speed (in MB/s) for migrations. Value 0 is no limit.  

--name <string> 
    
Set a name for the VM. Only used on the configuration web interface.  

--nameserver <string> 
    
cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.  

--net[n] [model=]<enum> [,bridge=<bridge>] [,firewall=<1|0>] [,host-tunnel=<1|0>] [,link_down=<1|0>] [,macaddr=<XX:XX:XX:XX:XX:XX>] [,mtu=<integer>] [,queues=<integer>] [,rate=<number>] [,tag=<integer>] [,trunks=<vlanid[;vlanid...]>] [,<model>=<macaddr>] 
    
Specify network devices.  

--numa <boolean> (_default =_ 0) 
    
Enable/disable NUMA.  

--numa[n] cpus=<id[-id];...> [,hostnodes=<id[-id];...>] [,memory=<number>] [,policy=<preferred|bind|interleave>] 
    
NUMA topology.  

--onboot <boolean> (_default =_ 0) 
    
Specifies whether a VM will be started during system bootup.  

--ostype <l24 | l26 | other | solaris | w2k | w2k3 | w2k8 | win10 | win11 | win7 | win8 | wvista | wxp> (_default =_ other) 
    
Specify guest operating system.  

--parallel[n] /dev/parport\d+|/dev/usb/lp\d+ 
    
Map host parallel devices (n is 0 to 2).  

--pool <string> 
    
Add the VM to the specified pool.  

--protection <boolean> (_default =_ 0) 
    
Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.  

--reboot <boolean> (_default =_ 1) 
    
Allow reboot. If set to _0_ the VM exit on reboot.  

--rng0 [source=]</dev/urandom|/dev/random|/dev/hwrng> [,max_bytes=<integer>] [,period=<integer>] 
    
Configure a VirtIO-based Random Number Generator.  

--sata[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--scsi[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,iothread=<1|0>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,product=<product>] [,queues=<integer>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,ro=<1|0>] [,scsiblock=<1|0>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,vendor=<vendor>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--scsihw <lsi | lsi53c810 | megasas | pvscsi | virtio-scsi-pci | virtio-scsi-single> (_default =_ lsi) 
    
SCSI controller model  

--searchdomain <string> 
    
cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.  

--serial[n] (/dev/[^,]+|socket) 
    
Create a serial device inside the VM (n is 0 to 3)  

--shares <integer> (0 - 50000) (_default =_ 1000) 
    
Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.  

--smbios1 [base64=<1|0>] [,family=<Base64 encoded string>] [,manufacturer=<Base64 encoded string>] [,product=<Base64 encoded string>] [,serial=<Base64 encoded string>] [,sku=<Base64 encoded string>] [,uuid=<UUID>] [,version=<Base64 encoded string>] 
    
Specify SMBIOS type 1 fields.  

--smp <integer> (1 - N) (_default =_ 1) 
    
The number of CPUs. Please use option -sockets instead.  

--sockets <integer> (1 - N) (_default =_ 1) 
    
The number of CPU sockets.  

--spice_enhancements [foldersharing=<1|0>] [,videostreaming=<off|all|filter>] 
    
Configure additional enhancements for SPICE.  

--sshkeys <filepath> 
    
cloud-init: Setup public SSH keys (one key per line, OpenSSH format).  

--start <boolean> (_default =_ 0) 
    
Start VM after it was created successfully.  

--startdate (now | YYYY-MM-DD | YYYY-MM-DDTHH:MM:SS) (_default =_ now) 
    
Set the initial date of the real time clock. Valid format for date are:'now' or _2006-06-17T16:01:21_ or _2006-06-17_.  

--startup `[[order=]\d+] [,up=\d+] [,down=\d+] ` 
    
Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the _up_ or _down_ delay in seconds, which specifies a delay to wait before the next VM is started or stopped.  

--storage <storage ID> 
    
Default storage.  

--tablet <boolean> (_default =_ 1) 
    
Enable/disable the USB tablet device.  

--tags <string> 
    
Tags of the VM. This is only meta information.  

--tdf <boolean> (_default =_ 0) 
    
Enable/disable time drift fix.  

--template <boolean> (_default =_ 0) 
    
Enable/disable Template.  

--tpmstate0 [file=]<volume> [,format=<raw|qcow2|vmdk>] [,import-from=<source volume>] [,size=<DiskSize>] [,version=<v1.2|v2.0>] 
    
Configure a Disk for storing TPM state. The format is fixed to _raw_. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--unique <boolean> 
    
Assign a unique random ethernet address.   
| Requires option(s): archive  |  
| --- | 

--unused[n] [file=]<volume> 
      
Reference to unused volumes. This is used internally, and should not be modified manually.  

--usb[n] [[host=]<HOSTUSBDEVICE|spice>] [,mapping=<mapping-id>] [,usb3=<1|0>] 
    
Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).  

--vcpus <integer> (1 - N) (_default =_ 0) 
    
Number of hotplugged vcpus.  

--vga [[type=]<enum>] [,clipboard=<vnc>] [,memory=<integer>] 
    
Configure the VGA hardware.  

--virtio[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,iothread=<1|0>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,ro=<1|0>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,werror=<enum>] 
    
Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--virtiofs[n] [dirid=]<mapping-id> [,cache=<enum>] [,direct-io=<1|0>] [,expose-acl=<1|0>] [,expose-xattr=<1|0>] 
    
Configuration for sharing a directory between host and guest using Virtio-fs.  

--vmgenid <UUID> (_default =_ 1 (autogenerated)) 
    
Set VM Generation ID. Use _1_ to autogenerate on create or update, pass _0_ to disable explicitly.  

--vmstatestorage <storage ID> 
    
Default storage for VM state volumes/files.  

--watchdog [[model=]<i6300esb|ib700>] [,action=<enum>] 
    
Create a virtual hardware watchdog device. 
**qm delsnapshot** <vmid> <snapname> [OPTIONS]
Delete a VM snapshot. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<snapname>: <string> 
    
The name of the snapshot.  

--force <boolean> 
    
For removal from config file, even if removing disk snapshots fails. 
**qm destroy** <vmid> [OPTIONS]
Destroy the VM and all used/owned volumes. Removes any VM specific permissions and firewall rules 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--destroy-unreferenced-disks <boolean> (_default =_ 0) 
    
If set, destroy additionally all disks not referenced in the config but with a matching VMID from all enabled storages.  

--purge <boolean> 
    
Remove VMID from configurations, like backup & replication jobs and HA.  

--skiplock <boolean> 
    
Ignore locks - only root is allowed to use this option. 
**qm disk import** <vmid> <source> <storage> [OPTIONS]
Import an external disk image as an unused disk in a VM. The image format has to be supported by qemu-img(1). 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<source>: <string> 
    
Path to the disk image to import  

<storage>: <storage ID> 
    
Target storage ID  

--format <qcow2 | raw | vmdk> 
    
Target format  

--target-disk <efidisk0 | ide0 | ide1 | ide2 | ide3 | sata0 | sata1 | sata2 | sata3 | sata4 | sata5 | scsi0 | scsi1 | scsi10 | scsi11 | scsi12 | scsi13 | scsi14 | scsi15 | scsi16 | scsi17 | scsi18 | scsi19 | scsi2 | scsi20 | scsi21 | scsi22 | scsi23 | scsi24 | scsi25 | scsi26 | scsi27 | scsi28 | scsi29 | scsi3 | scsi30 | scsi4 | scsi5 | scsi6 | scsi7 | scsi8 | scsi9 | tpmstate0 | unused0 | unused1 | unused10 | unused100 | unused101 | unused102 | unused103 | unused104 | unused105 | unused106 | unused107 | unused108 | unused109 | unused11 | unused110 | unused111 | unused112 | unused113 | unused114 | unused115 | unused116 | unused117 | unused118 | unused119 | unused12 | unused120 | unused121 | unused122 | unused123 | unused124 | unused125 | unused126 | unused127 | unused128 | unused129 | unused13 | unused130 | unused131 | unused132 | unused133 | unused134 | unused135 | unused136 | unused137 | unused138 | unused139 | unused14 | unused140 | unused141 | unused142 | unused143 | unused144 | unused145 | unused146 | unused147 | unused148 | unused149 | unused15 | unused150 | unused151 | unused152 | unused153 | unused154 | unused155 | unused156 | unused157 | unused158 | unused159 | unused16 | unused160 | unused161 | unused162 | unused163 | unused164 | unused165 | unused166 | unused167 | unused168 | unused169 | unused17 | unused170 | unused171 | unused172 | unused173 | unused174 | unused175 | unused176 | unused177 | unused178 | unused179 | unused18 | unused180 | unused181 | unused182 | unused183 | unused184 | unused185 | unused186 | unused187 | unused188 | unused189 | unused19 | unused190 | unused191 | unused192 | unused193 | unused194 | unused195 | unused196 | unused197 | unused198 | unused199 | unused2 | unused20 | unused200 | unused201 | unused202 | unused203 | unused204 | unused205 | unused206 | unused207 | unused208 | unused209 | unused21 | unused210 | unused211 | unused212 | unused213 | unused214 | unused215 | unused216 | unused217 | unused218 | unused219 | unused22 | unused220 | unused221 | unused222 | unused223 | unused224 | unused225 | unused226 | unused227 | unused228 | unused229 | unused23 | unused230 | unused231 | unused232 | unused233 | unused234 | unused235 | unused236 | unused237 | unused238 | unused239 | unused24 | unused240 | unused241 | unused242 | unused243 | unused244 | unused245 | unused246 | unused247 | unused248 | unused249 | unused25 | unused250 | unused251 | unused252 | unused253 | unused254 | unused255 | unused26 | unused27 | unused28 | unused29 | unused3 | unused30 | unused31 | unused32 | unused33 | unused34 | unused35 | unused36 | unused37 | unused38 | unused39 | unused4 | unused40 | unused41 | unused42 | unused43 | unused44 | unused45 | unused46 | unused47 | unused48 | unused49 | unused5 | unused50 | unused51 | unused52 | unused53 | unused54 | unused55 | unused56 | unused57 | unused58 | unused59 | unused6 | unused60 | unused61 | unused62 | unused63 | unused64 | unused65 | unused66 | unused67 | unused68 | unused69 | unused7 | unused70 | unused71 | unused72 | unused73 | unused74 | unused75 | unused76 | unused77 | unused78 | unused79 | unused8 | unused80 | unused81 | unused82 | unused83 | unused84 | unused85 | unused86 | unused87 | unused88 | unused89 | unused9 | unused90 | unused91 | unused92 | unused93 | unused94 | unused95 | unused96 | unused97 | unused98 | unused99 | virtio0 | virtio1 | virtio10 | virtio11 | virtio12 | virtio13 | virtio14 | virtio15 | virtio2 | virtio3 | virtio4 | virtio5 | virtio6 | virtio7 | virtio8 | virtio9> 
    
The disk name where the volume will be imported to (e.g. scsi1). 
**qm disk move** <vmid> <disk> [<storage>] [OPTIONS]
Move volume to different storage or to a different VM. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<disk>: <efidisk0 | ide0 | ide1 | ide2 | ide3 | sata0 | sata1 | sata2 | sata3 | sata4 | sata5 | scsi0 | scsi1 | scsi10 | scsi11 | scsi12 | scsi13 | scsi14 | scsi15 | scsi16 | scsi17 | scsi18 | scsi19 | scsi2 | scsi20 | scsi21 | scsi22 | scsi23 | scsi24 | scsi25 | scsi26 | scsi27 | scsi28 | scsi29 | scsi3 | scsi30 | scsi4 | scsi5 | scsi6 | scsi7 | scsi8 | scsi9 | tpmstate0 | unused0 | unused1 | unused10 | unused100 | unused101 | unused102 | unused103 | unused104 | unused105 | unused106 | unused107 | unused108 | unused109 | unused11 | unused110 | unused111 | unused112 | unused113 | unused114 | unused115 | unused116 | unused117 | unused118 | unused119 | unused12 | unused120 | unused121 | unused122 | unused123 | unused124 | unused125 | unused126 | unused127 | unused128 | unused129 | unused13 | unused130 | unused131 | unused132 | unused133 | unused134 | unused135 | unused136 | unused137 | unused138 | unused139 | unused14 | unused140 | unused141 | unused142 | unused143 | unused144 | unused145 | unused146 | unused147 | unused148 | unused149 | unused15 | unused150 | unused151 | unused152 | unused153 | unused154 | unused155 | unused156 | unused157 | unused158 | unused159 | unused16 | unused160 | unused161 | unused162 | unused163 | unused164 | unused165 | unused166 | unused167 | unused168 | unused169 | unused17 | unused170 | unused171 | unused172 | unused173 | unused174 | unused175 | unused176 | unused177 | unused178 | unused179 | unused18 | unused180 | unused181 | unused182 | unused183 | unused184 | unused185 | unused186 | unused187 | unused188 | unused189 | unused19 | unused190 | unused191 | unused192 | unused193 | unused194 | unused195 | unused196 | unused197 | unused198 | unused199 | unused2 | unused20 | unused200 | unused201 | unused202 | unused203 | unused204 | unused205 | unused206 | unused207 | unused208 | unused209 | unused21 | unused210 | unused211 | unused212 | unused213 | unused214 | unused215 | unused216 | unused217 | unused218 | unused219 | unused22 | unused220 | unused221 | unused222 | unused223 | unused224 | unused225 | unused226 | unused227 | unused228 | unused229 | unused23 | unused230 | unused231 | unused232 | unused233 | unused234 | unused235 | unused236 | unused237 | unused238 | unused239 | unused24 | unused240 | unused241 | unused242 | unused243 | unused244 | unused245 | unused246 | unused247 | unused248 | unused249 | unused25 | unused250 | unused251 | unused252 | unused253 | unused254 | unused255 | unused26 | unused27 | unused28 | unused29 | unused3 | unused30 | unused31 | unused32 | unused33 | unused34 | unused35 | unused36 | unused37 | unused38 | unused39 | unused4 | unused40 | unused41 | unused42 | unused43 | unused44 | unused45 | unused46 | unused47 | unused48 | unused49 | unused5 | unused50 | unused51 | unused52 | unused53 | unused54 | unused55 | unused56 | unused57 | unused58 | unused59 | unused6 | unused60 | unused61 | unused62 | unused63 | unused64 | unused65 | unused66 | unused67 | unused68 | unused69 | unused7 | unused70 | unused71 | unused72 | unused73 | unused74 | unused75 | unused76 | unused77 | unused78 | unused79 | unused8 | unused80 | unused81 | unused82 | unused83 | unused84 | unused85 | unused86 | unused87 | unused88 | unused89 | unused9 | unused90 | unused91 | unused92 | unused93 | unused94 | unused95 | unused96 | unused97 | unused98 | unused99 | virtio0 | virtio1 | virtio10 | virtio11 | virtio12 | virtio13 | virtio14 | virtio15 | virtio2 | virtio3 | virtio4 | virtio5 | virtio6 | virtio7 | virtio8 | virtio9> 
    
The disk you want to move.  

<storage>: <storage ID> 
    
Target storage.  

--bwlimit <integer> (0 - N) (_default =_ move limit from datacenter or storage config) 
    
Override I/O bandwidth limit (in KiB/s).  

--delete <boolean> (_default =_ 0) 
    
Delete the original disk after successful copy. By default the original disk is kept as unused disk.  

--digest <string> 
    
Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.  

--format <qcow2 | raw | vmdk> 
    
Target disk format. Only used when moving to a different storage. If the target storage does not support the format, the storage’s default format is used instead.  

--target-digest <string> 
    
Prevent changes if the current config file of the target VM has a different SHA1 digest. This can be used to detect concurrent modifications.  

--target-disk <efidisk0 | ide0 | ide1 | ide2 | ide3 | sata0 | sata1 | sata2 | sata3 | sata4 | sata5 | scsi0 | scsi1 | scsi10 | scsi11 | scsi12 | scsi13 | scsi14 | scsi15 | scsi16 | scsi17 | scsi18 | scsi19 | scsi2 | scsi20 | scsi21 | scsi22 | scsi23 | scsi24 | scsi25 | scsi26 | scsi27 | scsi28 | scsi29 | scsi3 | scsi30 | scsi4 | scsi5 | scsi6 | scsi7 | scsi8 | scsi9 | tpmstate0 | unused0 | unused1 | unused10 | unused100 | unused101 | unused102 | unused103 | unused104 | unused105 | unused106 | unused107 | unused108 | unused109 | unused11 | unused110 | unused111 | unused112 | unused113 | unused114 | unused115 | unused116 | unused117 | unused118 | unused119 | unused12 | unused120 | unused121 | unused122 | unused123 | unused124 | unused125 | unused126 | unused127 | unused128 | unused129 | unused13 | unused130 | unused131 | unused132 | unused133 | unused134 | unused135 | unused136 | unused137 | unused138 | unused139 | unused14 | unused140 | unused141 | unused142 | unused143 | unused144 | unused145 | unused146 | unused147 | unused148 | unused149 | unused15 | unused150 | unused151 | unused152 | unused153 | unused154 | unused155 | unused156 | unused157 | unused158 | unused159 | unused16 | unused160 | unused161 | unused162 | unused163 | unused164 | unused165 | unused166 | unused167 | unused168 | unused169 | unused17 | unused170 | unused171 | unused172 | unused173 | unused174 | unused175 | unused176 | unused177 | unused178 | unused179 | unused18 | unused180 | unused181 | unused182 | unused183 | unused184 | unused185 | unused186 | unused187 | unused188 | unused189 | unused19 | unused190 | unused191 | unused192 | unused193 | unused194 | unused195 | unused196 | unused197 | unused198 | unused199 | unused2 | unused20 | unused200 | unused201 | unused202 | unused203 | unused204 | unused205 | unused206 | unused207 | unused208 | unused209 | unused21 | unused210 | unused211 | unused212 | unused213 | unused214 | unused215 | unused216 | unused217 | unused218 | unused219 | unused22 | unused220 | unused221 | unused222 | unused223 | unused224 | unused225 | unused226 | unused227 | unused228 | unused229 | unused23 | unused230 | unused231 | unused232 | unused233 | unused234 | unused235 | unused236 | unused237 | unused238 | unused239 | unused24 | unused240 | unused241 | unused242 | unused243 | unused244 | unused245 | unused246 | unused247 | unused248 | unused249 | unused25 | unused250 | unused251 | unused252 | unused253 | unused254 | unused255 | unused26 | unused27 | unused28 | unused29 | unused3 | unused30 | unused31 | unused32 | unused33 | unused34 | unused35 | unused36 | unused37 | unused38 | unused39 | unused4 | unused40 | unused41 | unused42 | unused43 | unused44 | unused45 | unused46 | unused47 | unused48 | unused49 | unused5 | unused50 | unused51 | unused52 | unused53 | unused54 | unused55 | unused56 | unused57 | unused58 | unused59 | unused6 | unused60 | unused61 | unused62 | unused63 | unused64 | unused65 | unused66 | unused67 | unused68 | unused69 | unused7 | unused70 | unused71 | unused72 | unused73 | unused74 | unused75 | unused76 | unused77 | unused78 | unused79 | unused8 | unused80 | unused81 | unused82 | unused83 | unused84 | unused85 | unused86 | unused87 | unused88 | unused89 | unused9 | unused90 | unused91 | unused92 | unused93 | unused94 | unused95 | unused96 | unused97 | unused98 | unused99 | virtio0 | virtio1 | virtio10 | virtio11 | virtio12 | virtio13 | virtio14 | virtio15 | virtio2 | virtio3 | virtio4 | virtio5 | virtio6 | virtio7 | virtio8 | virtio9> 
    
The config key the disk will be moved to on the target VM (for example, ide0 or scsi1). Default is the source disk key.  

--target-vmid <integer> (100 - 999999999) 
    
The (unique) ID of the VM. 
**qm disk rescan** [OPTIONS]
Rescan all storages and update disk sizes and unused disk images. 

--dryrun <boolean> (_default =_ 0) 
    
Do not actually write changes out to VM config(s).  

--vmid <integer> (100 - 999999999) 
    
The (unique) ID of the VM. 
**qm disk resize** <vmid> <disk> <size> [OPTIONS]
Extend volume size. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<disk>: <efidisk0 | ide0 | ide1 | ide2 | ide3 | sata0 | sata1 | sata2 | sata3 | sata4 | sata5 | scsi0 | scsi1 | scsi10 | scsi11 | scsi12 | scsi13 | scsi14 | scsi15 | scsi16 | scsi17 | scsi18 | scsi19 | scsi2 | scsi20 | scsi21 | scsi22 | scsi23 | scsi24 | scsi25 | scsi26 | scsi27 | scsi28 | scsi29 | scsi3 | scsi30 | scsi4 | scsi5 | scsi6 | scsi7 | scsi8 | scsi9 | tpmstate0 | virtio0 | virtio1 | virtio10 | virtio11 | virtio12 | virtio13 | virtio14 | virtio15 | virtio2 | virtio3 | virtio4 | virtio5 | virtio6 | virtio7 | virtio8 | virtio9> 
    
The disk you want to resize.  

<size>: \\+?\d+(\\.\d+)?[KMGT]? 
    
The new size. With the + sign the value is added to the actual size of the volume and without it, the value is taken as an absolute one. Shrinking disk size is not supported.  

--digest <string> 
    
Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.  

--skiplock <boolean> 
    
Ignore locks - only root is allowed to use this option. 
**qm disk unlink** <vmid> --idlist <string> [OPTIONS]
Unlink/delete disk images. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--force <boolean> 
    
Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called _unused[n]_ , which contains the volume ID. Unlink of unused[n] always cause physical removal.  

--idlist <string> 
    
A list of disk IDs you want to delete. 
**qm enroll-efi-keys** <vmid>
Enroll important updated certificates to the EFI disk with pre-enrolled-keys. Currently, these are UEFI 2023 certificates from Microsoft. Must be called while the VM is shut down. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM. 
**qm guest cmd** <vmid> <command>
Execute QEMU Guest Agent commands. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<command>: <fsfreeze-freeze | fsfreeze-status | fsfreeze-thaw | fstrim | get-fsinfo | get-host-name | get-memory-block-info | get-memory-blocks | get-osinfo | get-time | get-timezone | get-users | get-vcpus | info | network-get-interfaces | ping | shutdown | suspend-disk | suspend-hybrid | suspend-ram> 
    
The QGA command. 
**qm guest exec** <vmid> [<extra-args>] [OPTIONS]
Executes the given command via the guest agent 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<extra-args>: <array> 
    
Extra arguments as array  

--pass-stdin <boolean> (_default =_ 0) 
    
When set, read STDIN until EOF and forward to guest agent via _input-data_ (usually treated as STDIN to process launched by guest agent). Allows maximal 1 MiB.  

--synchronous <boolean> (_default =_ 1) 
    
If set to off, returns the pid immediately instead of waiting for the command to finish or the timeout.  

--timeout <integer> (0 - N) (_default =_ 30) 
    
The maximum time to wait synchronously for the command to finish. If reached, the pid gets returned. Set to 0 to deactivate 
**qm guest exec-status** <vmid> <pid>
Gets the status of the given pid started by the guest-agent 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<pid>: <integer> 
    
The PID to query 
**qm guest passwd** <vmid> <username> [OPTIONS]
Sets the password for the given user to the given password 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<username>: <string> 
    
The user to set the password for.  

--crypted <boolean> (_default =_ 0) 
    
set to 1 if the password has already been passed through crypt() 
**qm help** [OPTIONS]
Get help about specified command. 

--extra-args <array> 
    
Shows help for a specific command  

--verbose <boolean> 
    
Verbose output format. 
**qm import** <vmid> <source> --storage <string> [OPTIONS]
Import a foreign virtual guest from a supported import source, such as an ESXi storage. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<source>: <string> 
    
The import source volume id.  

--acpi <boolean> (_default =_ 1) 
    
Enable/disable ACPI.  

--affinity <string> 
    
List of host cores used to execute guest processes, for example: 0,5,8-11  

--agent [enabled=]<1|0> [,freeze-fs=<1|0>] [,fstrim_cloned_disks=<1|0>] [,type=<virtio|isa>] 
    
Enable/disable communication with the QEMU Guest Agent and its properties.  

--allow-ksm <boolean> (_default =_ 1) 
    
Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).  

--amd-sev [type=]<sev-type> [,allow-smt=<1|0>] [,kernel-hashes=<1|0>] [,no-debug=<1|0>] [,no-key-sharing=<1|0>] 
    
Secure Encrypted Virtualization (SEV) features by AMD CPUs  

--arch <aarch64 | x86_64> 
    
Virtual processor architecture. Defaults to the host architecture.  

--args <string> 
    
Arbitrary arguments passed to kvm.  

--audio0 device=<ich9-intel-hda|intel-hda|AC97> [,driver=<spice|none>] 
    
Configure a audio device, useful in combination with QXL/Spice.  

--autostart <boolean> (_default =_ 0) 
    
Automatic restart after crash (currently ignored).  

--balloon <integer> (0 - N) 
    
Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.  

--bios <ovmf | seabios> (_default =_ seabios) 
    
Select BIOS implementation.  

--boot [[legacy=]<[acdn]{1,4}>] [,order=<device[;device...]>] 
    
Specify guest boot order. Use the _order=_ sub-property as usage with no key or _legacy=_ is deprecated.  

--bootdisk (ide|sata|scsi|virtio)\d+ 
    
Enable booting from specified disk. Deprecated: Use _boot: order=foo;bar_ instead.  

--cdrom <volume> 
    
This is an alias for option -ide2  

--cicustom [meta=<volume>] [,network=<volume>] [,user=<volume>] [,vendor=<volume>] 
    
cloud-init: Specify custom files to replace the automatically generated ones at start.  

--cipassword <string> 
    
cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.  

--citype <configdrive2 | nocloud | opennebula> 
    
Specifies the cloud-init configuration format. The default depends on the configured operating system type (ostype. We use the nocloud format for Linux, and configdrive2 for windows.  

--ciupgrade <boolean> (_default =_ 1) 
    
cloud-init: do an automatic package upgrade after the first boot.  

--ciuser <string> 
    
cloud-init: User name to change ssh keys and password for instead of the image’s configured default user.  

--cores <integer> (1 - N) (_default =_ 1) 
    
The number of cores per socket.  

--cpu [[cputype=]<string>] [,flags=<+FLAG[;-FLAG...]>] [,guest-phys-bits=<integer>] [,hidden=<1|0>] [,hv-vendor-id=<vendor-id>] [,level=<integer>] [,phys-bits=<8-64|host>] [,reported-model=<enum>] 
    
Emulated CPU type.  

--cpulimit <number> (0 - 128) (_default =_ 0) 
    
Limit of CPU usage.  

--cpuunits <integer> (1 - 262144) (_default =_ cgroup v1: 1024, cgroup v2: 100) 
    
CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.  

--delete <string> 
    
A list of settings you want to delete.  

--description <string> 
    
Description for the VM. Shown in the web-interface VM’s summary. This is saved as comment inside the configuration file.  

--dryrun <boolean> (_default =_ 0) 
    
Show the create command and exit without doing anything.  

--efidisk0 [file=]<volume> [,efitype=<2m|4m>] [,format=<enum>] [,import-from=<source volume>] [,ms-cert=<enum>] [,pre-enrolled-keys=<1|0>] [,size=<DiskSize>] 
    
Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--format <qcow2 | raw | vmdk> 
    
Target format  

--freeze <boolean> 
    
Freeze CPU at startup (use _c_ monitor command to start execution).  

--hookscript <string> 
    
Script that will be executed during various steps in the vms lifetime.  

--hostpci[n] [[host=]<HOSTPCIID[;HOSTPCIID2...]>] [,device-id=<hex id>] [,driver=<vfio|keep>] [,legacy-igd=<1|0>] [,mapping=<mapping-id>] [,mdev=<string>] [,pcie=<1|0>] [,rombar=<1|0>] [,romfile=<string>] [,sub-device-id=<hex id>] [,sub-vendor-id=<hex id>] [,vendor-id=<hex id>] [,x-vga=<1|0>] 
    
Map host PCI devices into guest.  

--hotplug <string> (_default =_ network,disk,usb) 
    
Selectively enable hotplug features. This is a comma separated list of hotplug features: _network_ , _disk_ , _cpu_ , _memory_ , _usb_ and _cloudinit_. Use _0_ to disable hotplug completely. Using _1_ as value is an alias for the default network,disk,usb. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.  

--hugepages <1024 | 2 | any> 
    
Enables hugepages memory. 
Sets the size of hugepages in MiB. If the value is set to _any_ then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB. 

--ide[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,model=<model>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--intel-tdx [type=]<tdx-type> ,attestation=<1|0> [,vsock-cid=<integer>] [,vsock-port=<integer>] 
    
Trusted Domain Extension (TDX) features by Intel CPUs  

--ipconfig[n] [gw=<GatewayIPv4>] [,gw6=<GatewayIPv6>] [,ip=<IPv4Format/CIDR>] [,ip6=<IPv6Format/CIDR>] 
    
cloud-init: Specify IP addresses and gateways for the corresponding interface. 
IP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.
The special string _dhcp_ can be used for IP addresses to use DHCP, in which case no explicit gateway should be provided. For IPv6 the special string _auto_ can be used to use stateless autoconfiguration. This requires cloud-init 19.4 or newer.
If cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using dhcp on IPv4. 

--ivshmem size=<integer> [,name=<string>] 
    
Inter-VM shared memory. Useful for direct communication between VMs, or to the host.  

--keephugepages <boolean> (_default =_ 0) 
    
Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.  

--keyboard <da | de | de-ch | en-gb | en-us | es | fi | fr | fr-be | fr-ca | fr-ch | hu | is | it | ja | lt | mk | nl | no | pl | pt | pt-br | sl | sv | tr> 
    
Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.  

--kvm <boolean> (_default =_ 1) 
    
Enable/disable KVM hardware virtualization.  

--live-import <boolean> (_default =_ 0) 
    
Immediately start the VM and copy the data in the background.  

--localtime <boolean> 
    
Set the real time clock (RTC) to local time. This is enabled by default if the ostype indicates a Microsoft Windows OS.  

--lock <backup | clone | create | migrate | rollback | snapshot | snapshot-delete | suspended | suspending> 
    
Lock/unlock the VM.  

--machine [[type=]<machine type>] [,aw-bits=<number>] [,enable-s3=<1|0>] [,enable-s4=<1|0>] [,viommu=<intel|virtio>] 
    
Specify the QEMU machine.  

--memory [current=]<integer> 
    
Memory properties.  

--migrate_downtime <number> (0 - N) (_default =_ 0.1) 
    
Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).  

--migrate_speed <integer> (0 - N) (_default =_ 0) 
    
Set maximum speed (in MB/s) for migrations. Value 0 is no limit.  

--name <string> 
    
Set a name for the VM. Only used on the configuration web interface.  

--nameserver <string> 
    
cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.  

--net[n] [model=]<enum> [,bridge=<bridge>] [,firewall=<1|0>] [,host-tunnel=<1|0>] [,link_down=<1|0>] [,macaddr=<XX:XX:XX:XX:XX:XX>] [,mtu=<integer>] [,queues=<integer>] [,rate=<number>] [,tag=<integer>] [,trunks=<vlanid[;vlanid...]>] [,<model>=<macaddr>] 
    
Specify network devices.  

--numa <boolean> (_default =_ 0) 
    
Enable/disable NUMA.  

--numa[n] cpus=<id[-id];...> [,hostnodes=<id[-id];...>] [,memory=<number>] [,policy=<preferred|bind|interleave>] 
    
NUMA topology.  

--onboot <boolean> (_default =_ 0) 
    
Specifies whether a VM will be started during system bootup.  

--ostype <l24 | l26 | other | solaris | w2k | w2k3 | w2k8 | win10 | win11 | win7 | win8 | wvista | wxp> (_default =_ other) 
    
Specify guest operating system.  

--parallel[n] /dev/parport\d+|/dev/usb/lp\d+ 
    
Map host parallel devices (n is 0 to 2).  

--protection <boolean> (_default =_ 0) 
    
Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.  

--reboot <boolean> (_default =_ 1) 
    
Allow reboot. If set to _0_ the VM exit on reboot.  

--rng0 [source=]</dev/urandom|/dev/random|/dev/hwrng> [,max_bytes=<integer>] [,period=<integer>] 
    
Configure a VirtIO-based Random Number Generator.  

--sata[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--scsi[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,iothread=<1|0>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,product=<product>] [,queues=<integer>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,ro=<1|0>] [,scsiblock=<1|0>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,vendor=<vendor>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--scsihw <lsi | lsi53c810 | megasas | pvscsi | virtio-scsi-pci | virtio-scsi-single> (_default =_ lsi) 
    
SCSI controller model  

--searchdomain <string> 
    
cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.  

--serial[n] (/dev/[^,]+|socket) 
    
Create a serial device inside the VM (n is 0 to 3)  

--shares <integer> (0 - 50000) (_default =_ 1000) 
    
Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.  

--smbios1 [base64=<1|0>] [,family=<Base64 encoded string>] [,manufacturer=<Base64 encoded string>] [,product=<Base64 encoded string>] [,serial=<Base64 encoded string>] [,sku=<Base64 encoded string>] [,uuid=<UUID>] [,version=<Base64 encoded string>] 
    
Specify SMBIOS type 1 fields.  

--smp <integer> (1 - N) (_default =_ 1) 
    
The number of CPUs. Please use option -sockets instead.  

--sockets <integer> (1 - N) (_default =_ 1) 
    
The number of CPU sockets.  

--spice_enhancements [foldersharing=<1|0>] [,videostreaming=<off|all|filter>] 
    
Configure additional enhancements for SPICE.  

--sshkeys <string> 
    
cloud-init: Setup public SSH keys (one key per line, OpenSSH format).  

--startdate (now | YYYY-MM-DD | YYYY-MM-DDTHH:MM:SS) (_default =_ now) 
    
Set the initial date of the real time clock. Valid format for date are:'now' or _2006-06-17T16:01:21_ or _2006-06-17_.  

--startup `[[order=]\d+] [,up=\d+] [,down=\d+] ` 
    
Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the _up_ or _down_ delay in seconds, which specifies a delay to wait before the next VM is started or stopped.  

--storage <storage ID> 
    
Default storage.  

--tablet <boolean> (_default =_ 1) 
    
Enable/disable the USB tablet device.  

--tags <string> 
    
Tags of the VM. This is only meta information.  

--tdf <boolean> (_default =_ 0) 
    
Enable/disable time drift fix.  

--template <boolean> (_default =_ 0) 
    
Enable/disable Template.  

--tpmstate0 [file=]<volume> [,format=<raw|qcow2|vmdk>] [,import-from=<source volume>] [,size=<DiskSize>] [,version=<v1.2|v2.0>] 
    
Configure a Disk for storing TPM state. The format is fixed to _raw_. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--unused[n] [file=]<volume> 
    
Reference to unused volumes. This is used internally, and should not be modified manually.  

--usb[n] [[host=]<HOSTUSBDEVICE|spice>] [,mapping=<mapping-id>] [,usb3=<1|0>] 
    
Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).  

--vcpus <integer> (1 - N) (_default =_ 0) 
    
Number of hotplugged vcpus.  

--vga [[type=]<enum>] [,clipboard=<vnc>] [,memory=<integer>] 
    
Configure the VGA hardware.  

--virtio[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,iothread=<1|0>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,ro=<1|0>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,werror=<enum>] 
    
Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--virtiofs[n] [dirid=]<mapping-id> [,cache=<enum>] [,direct-io=<1|0>] [,expose-acl=<1|0>] [,expose-xattr=<1|0>] 
    
Configuration for sharing a directory between host and guest using Virtio-fs.  

--vmgenid <UUID> (_default =_ 1 (autogenerated)) 
    
Set VM Generation ID. Use _1_ to autogenerate on create or update, pass _0_ to disable explicitly.  

--vmstatestorage <storage ID> 
    
Default storage for VM state volumes/files.  

--watchdog [[model=]<i6300esb|ib700>] [,action=<enum>] 
    
Create a virtual hardware watchdog device. 
**qm importdisk**
An alias for _qm disk import_.
**qm importovf** <vmid> <manifest> <storage> [OPTIONS]
Create a new VM using parameters read from an OVF manifest 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<manifest>: <string> 
    
path to the ovf file  

<storage>: <storage ID> 
    
Target storage ID  

--dryrun <boolean> 
    
Print a parsed representation of the extracted OVF parameters, but do not create a VM  

--format <qcow2 | raw | vmdk> 
    
Target format 
**qm list** [OPTIONS]
Virtual machine index (per node). 

--full <boolean> 
    
Determine the full status of active VMs. 
**qm listsnapshot** <vmid>
List all snapshots. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM. 
**qm migrate** <vmid> <target> [OPTIONS]
Migrate virtual machine. Creates a new migration task. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<target>: <string> 
    
Target node.  

--bwlimit <integer> (0 - N) (_default =_ migrate limit from datacenter or storage config) 
    
Override I/O bandwidth limit (in KiB/s).  

--force <boolean> 
    
Allow to migrate VMs which use local devices. Only root may use this option.  

--migration_network <string> 
    
CIDR of the (sub) network that is used for migration.  

--migration_type <insecure | secure> 
    
Migration traffic is encrypted using an SSH tunnel by default. On secure, completely private networks this can be disabled to increase performance.  

--online <boolean> 
    
Use online/live migration if VM is running. Ignored if VM is stopped.  

--targetstorage <string> 
    
Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value _1_ will map each source storage to itself.  

--with-conntrack-state <boolean> (_default =_ 0) 
    
Whether to migrate conntrack entries for running VMs.  

--with-local-disks <boolean> 
    
Enable live storage migration for local disk 
**qm monitor** <vmid>
Enter QEMU Monitor interface. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM. 
**qm move-disk**
An alias for _qm disk move_.
**qm move_disk**
An alias for _qm disk move_.
**qm mtunnel**
Used by qmigrate - do not use manually.
**qm nbdstop** <vmid>
Stop embedded nbd server. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM. 
**qm pending** <vmid>
Get the virtual machine configuration with both current and pending values. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM. 
**qm reboot** <vmid> [OPTIONS]
Reboot the VM by shutting it down, and starting it again. Applies pending changes. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--timeout <integer> (0 - N) 
    
Wait maximal timeout seconds for the shutdown. 
**qm remote-migrate** <vmid> [<target-vmid>] <target-endpoint> --target-bridge <string> --target-storage <string> [OPTIONS]
Migrate virtual machine to a remote cluster. Creates a new migration task. EXPERIMENTAL feature! 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<target-vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<target-endpoint>: apitoken=<PVEAPIToken=user@realm!token=SECRET> ,host=<ADDRESS> [,fingerprint=<FINGERPRINT>] [,port=<PORT>] 
    
Remote target endpoint  

--bwlimit <integer> (0 - N) (_default =_ migrate limit from datacenter or storage config) 
    
Override I/O bandwidth limit (in KiB/s).  

--delete <boolean> (_default =_ 0) 
    
Delete the original VM and related data after successful migration. By default the original VM is kept on the source cluster in a stopped state.  

--online <boolean> 
    
Use online/live migration if VM is running. Ignored if VM is stopped.  

--target-bridge <string> 
    
Mapping from source to target bridges. Providing only a single bridge ID maps all source bridges to that bridge. Providing the special value _1_ will map each source bridge to itself.  

--target-storage <string> 
    
Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value _1_ will map each source storage to itself. 
**qm rescan**
An alias for _qm disk rescan_.
**qm reset** <vmid> [OPTIONS]
Reset virtual machine. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--skiplock <boolean> 
    
Ignore locks - only root is allowed to use this option. 
**qm resize**
An alias for _qm disk resize_.
**qm resume** <vmid> [OPTIONS]
Resume virtual machine. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--nocheck <boolean> 
    
Do not check whether the VM is running, used internally during migration. Only root may use this option.  

--skiplock <boolean> 
    
Ignore locks - only root is allowed to use this option. 
**qm rollback** <vmid> <snapname> [OPTIONS]
Rollback VM state to specified snapshot. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<snapname>: <string> 
    
The name of the snapshot.  

--start <boolean> (_default =_ 0) 
    
Whether the VM should get started after rolling back successfully. (Note: VMs will be automatically started if the snapshot includes RAM.) 
**qm sendkey** <vmid> <key> [OPTIONS]
Send key event to virtual machine. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<key>: <string> 
    
The key (qemu monitor encoding).  

--skiplock <boolean> 
    
Ignore locks - only root is allowed to use this option. 
**qm set** <vmid> [OPTIONS]
Set virtual machine options (synchronous API) - You should consider using the POST method instead for any actions involving hotplug or storage allocation. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--acpi <boolean> (_default =_ 1) 
    
Enable/disable ACPI.  

--affinity <string> 
    
List of host cores used to execute guest processes, for example: 0,5,8-11  

--agent [enabled=]<1|0> [,freeze-fs=<1|0>] [,fstrim_cloned_disks=<1|0>] [,type=<virtio|isa>] 
    
Enable/disable communication with the QEMU Guest Agent and its properties.  

--allow-ksm <boolean> (_default =_ 1) 
    
Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).  

--amd-sev [type=]<sev-type> [,allow-smt=<1|0>] [,kernel-hashes=<1|0>] [,no-debug=<1|0>] [,no-key-sharing=<1|0>] 
    
Secure Encrypted Virtualization (SEV) features by AMD CPUs  

--arch <aarch64 | x86_64> 
    
Virtual processor architecture. Defaults to the host architecture.  

--args <string> 
    
Arbitrary arguments passed to kvm.  

--audio0 device=<ich9-intel-hda|intel-hda|AC97> [,driver=<spice|none>] 
    
Configure a audio device, useful in combination with QXL/Spice.  

--autostart <boolean> (_default =_ 0) 
    
Automatic restart after crash (currently ignored).  

--balloon <integer> (0 - N) 
    
Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.  

--bios <ovmf | seabios> (_default =_ seabios) 
    
Select BIOS implementation.  

--boot [[legacy=]<[acdn]{1,4}>] [,order=<device[;device...]>] 
    
Specify guest boot order. Use the _order=_ sub-property as usage with no key or _legacy=_ is deprecated.  

--bootdisk (ide|sata|scsi|virtio)\d+ 
    
Enable booting from specified disk. Deprecated: Use _boot: order=foo;bar_ instead.  

--cdrom <volume> 
    
This is an alias for option -ide2  

--cicustom [meta=<volume>] [,network=<volume>] [,user=<volume>] [,vendor=<volume>] 
    
cloud-init: Specify custom files to replace the automatically generated ones at start.  

--cipassword <password> 
    
cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.  

--citype <configdrive2 | nocloud | opennebula> 
    
Specifies the cloud-init configuration format. The default depends on the configured operating system type (ostype. We use the nocloud format for Linux, and configdrive2 for windows.  

--ciupgrade <boolean> (_default =_ 1) 
    
cloud-init: do an automatic package upgrade after the first boot.  

--ciuser <string> 
    
cloud-init: User name to change ssh keys and password for instead of the image’s configured default user.  

--cores <integer> (1 - N) (_default =_ 1) 
    
The number of cores per socket.  

--cpu [[cputype=]<string>] [,flags=<+FLAG[;-FLAG...]>] [,guest-phys-bits=<integer>] [,hidden=<1|0>] [,hv-vendor-id=<vendor-id>] [,level=<integer>] [,phys-bits=<8-64|host>] [,reported-model=<enum>] 
    
Emulated CPU type.  

--cpulimit <number> (0 - 128) (_default =_ 0) 
    
Limit of CPU usage.  

--cpuunits <integer> (1 - 262144) (_default =_ cgroup v1: 1024, cgroup v2: 100) 
    
CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.  

--delete <string> 
    
A list of settings you want to delete.  

--description <string> 
    
Description for the VM. Shown in the web-interface VM’s summary. This is saved as comment inside the configuration file.  

--digest <string> 
    
Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.  

--efidisk0 [file=]<volume> [,efitype=<2m|4m>] [,format=<enum>] [,import-from=<source volume>] [,ms-cert=<enum>] [,pre-enrolled-keys=<1|0>] [,size=<DiskSize>] 
    
Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--force <boolean> 
    
Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called _unused[n]_ , which contains the volume ID. Unlink of unused[n] always cause physical removal.   
| Requires option(s): delete  |  
| --- | 

--freeze <boolean> 
      
Freeze CPU at startup (use _c_ monitor command to start execution).  

--hookscript <string> 
    
Script that will be executed during various steps in the vms lifetime.  

--hostpci[n] [[host=]<HOSTPCIID[;HOSTPCIID2...]>] [,device-id=<hex id>] [,driver=<vfio|keep>] [,legacy-igd=<1|0>] [,mapping=<mapping-id>] [,mdev=<string>] [,pcie=<1|0>] [,rombar=<1|0>] [,romfile=<string>] [,sub-device-id=<hex id>] [,sub-vendor-id=<hex id>] [,vendor-id=<hex id>] [,x-vga=<1|0>] 
    
Map host PCI devices into guest.  

--hotplug <string> (_default =_ network,disk,usb) 
    
Selectively enable hotplug features. This is a comma separated list of hotplug features: _network_ , _disk_ , _cpu_ , _memory_ , _usb_ and _cloudinit_. Use _0_ to disable hotplug completely. Using _1_ as value is an alias for the default network,disk,usb. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.  

--hugepages <1024 | 2 | any> 
    
Enables hugepages memory. 
Sets the size of hugepages in MiB. If the value is set to _any_ then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB. 

--ide[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,model=<model>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--intel-tdx [type=]<tdx-type> ,attestation=<1|0> [,vsock-cid=<integer>] [,vsock-port=<integer>] 
    
Trusted Domain Extension (TDX) features by Intel CPUs  

--ipconfig[n] [gw=<GatewayIPv4>] [,gw6=<GatewayIPv6>] [,ip=<IPv4Format/CIDR>] [,ip6=<IPv6Format/CIDR>] 
    
cloud-init: Specify IP addresses and gateways for the corresponding interface. 
IP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.
The special string _dhcp_ can be used for IP addresses to use DHCP, in which case no explicit gateway should be provided. For IPv6 the special string _auto_ can be used to use stateless autoconfiguration. This requires cloud-init 19.4 or newer.
If cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using dhcp on IPv4. 

--ivshmem size=<integer> [,name=<string>] 
    
Inter-VM shared memory. Useful for direct communication between VMs, or to the host.  

--keephugepages <boolean> (_default =_ 0) 
    
Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.  

--keyboard <da | de | de-ch | en-gb | en-us | es | fi | fr | fr-be | fr-ca | fr-ch | hu | is | it | ja | lt | mk | nl | no | pl | pt | pt-br | sl | sv | tr> 
    
Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.  

--kvm <boolean> (_default =_ 1) 
    
Enable/disable KVM hardware virtualization.  

--localtime <boolean> 
    
Set the real time clock (RTC) to local time. This is enabled by default if the ostype indicates a Microsoft Windows OS.  

--lock <backup | clone | create | migrate | rollback | snapshot | snapshot-delete | suspended | suspending> 
    
Lock/unlock the VM.  

--machine [[type=]<machine type>] [,aw-bits=<number>] [,enable-s3=<1|0>] [,enable-s4=<1|0>] [,viommu=<intel|virtio>] 
    
Specify the QEMU machine.  

--memory [current=]<integer> 
    
Memory properties.  

--migrate_downtime <number> (0 - N) (_default =_ 0.1) 
    
Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).  

--migrate_speed <integer> (0 - N) (_default =_ 0) 
    
Set maximum speed (in MB/s) for migrations. Value 0 is no limit.  

--name <string> 
    
Set a name for the VM. Only used on the configuration web interface.  

--nameserver <string> 
    
cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.  

--net[n] [model=]<enum> [,bridge=<bridge>] [,firewall=<1|0>] [,host-tunnel=<1|0>] [,link_down=<1|0>] [,macaddr=<XX:XX:XX:XX:XX:XX>] [,mtu=<integer>] [,queues=<integer>] [,rate=<number>] [,tag=<integer>] [,trunks=<vlanid[;vlanid...]>] [,<model>=<macaddr>] 
    
Specify network devices.  

--numa <boolean> (_default =_ 0) 
    
Enable/disable NUMA.  

--numa[n] cpus=<id[-id];...> [,hostnodes=<id[-id];...>] [,memory=<number>] [,policy=<preferred|bind|interleave>] 
    
NUMA topology.  

--onboot <boolean> (_default =_ 0) 
    
Specifies whether a VM will be started during system bootup.  

--ostype <l24 | l26 | other | solaris | w2k | w2k3 | w2k8 | win10 | win11 | win7 | win8 | wvista | wxp> (_default =_ other) 
    
Specify guest operating system.  

--parallel[n] /dev/parport\d+|/dev/usb/lp\d+ 
    
Map host parallel devices (n is 0 to 2).  

--protection <boolean> (_default =_ 0) 
    
Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.  

--reboot <boolean> (_default =_ 1) 
    
Allow reboot. If set to _0_ the VM exit on reboot.  

--revert <string> 
    
Revert a pending change.  

--rng0 [source=]</dev/urandom|/dev/random|/dev/hwrng> [,max_bytes=<integer>] [,period=<integer>] 
    
Configure a VirtIO-based Random Number Generator.  

--sata[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--scsi[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,iothread=<1|0>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,product=<product>] [,queues=<integer>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,ro=<1|0>] [,scsiblock=<1|0>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,vendor=<vendor>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--scsihw <lsi | lsi53c810 | megasas | pvscsi | virtio-scsi-pci | virtio-scsi-single> (_default =_ lsi) 
    
SCSI controller model  

--searchdomain <string> 
    
cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.  

--serial[n] (/dev/[^,]+|socket) 
    
Create a serial device inside the VM (n is 0 to 3)  

--shares <integer> (0 - 50000) (_default =_ 1000) 
    
Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.  

--skiplock <boolean> 
    
Ignore locks - only root is allowed to use this option.  

--smbios1 [base64=<1|0>] [,family=<Base64 encoded string>] [,manufacturer=<Base64 encoded string>] [,product=<Base64 encoded string>] [,serial=<Base64 encoded string>] [,sku=<Base64 encoded string>] [,uuid=<UUID>] [,version=<Base64 encoded string>] 
    
Specify SMBIOS type 1 fields.  

--smp <integer> (1 - N) (_default =_ 1) 
    
The number of CPUs. Please use option -sockets instead.  

--sockets <integer> (1 - N) (_default =_ 1) 
    
The number of CPU sockets.  

--spice_enhancements [foldersharing=<1|0>] [,videostreaming=<off|all|filter>] 
    
Configure additional enhancements for SPICE.  

--sshkeys <filepath> 
    
cloud-init: Setup public SSH keys (one key per line, OpenSSH format).  

--startdate (now | YYYY-MM-DD | YYYY-MM-DDTHH:MM:SS) (_default =_ now) 
    
Set the initial date of the real time clock. Valid format for date are:'now' or _2006-06-17T16:01:21_ or _2006-06-17_.  

--startup `[[order=]\d+] [,up=\d+] [,down=\d+] ` 
    
Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the _up_ or _down_ delay in seconds, which specifies a delay to wait before the next VM is started or stopped.  

--tablet <boolean> (_default =_ 1) 
    
Enable/disable the USB tablet device.  

--tags <string> 
    
Tags of the VM. This is only meta information.  

--tdf <boolean> (_default =_ 0) 
    
Enable/disable time drift fix.  

--template <boolean> (_default =_ 0) 
    
Enable/disable Template.  

--tpmstate0 [file=]<volume> [,format=<raw|qcow2|vmdk>] [,import-from=<source volume>] [,size=<DiskSize>] [,version=<v1.2|v2.0>] 
    
Configure a Disk for storing TPM state. The format is fixed to _raw_. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--unused[n] [file=]<volume> 
    
Reference to unused volumes. This is used internally, and should not be modified manually.  

--usb[n] [[host=]<HOSTUSBDEVICE|spice>] [,mapping=<mapping-id>] [,usb3=<1|0>] 
    
Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).  

--vcpus <integer> (1 - N) (_default =_ 0) 
    
Number of hotplugged vcpus.  

--vga [[type=]<enum>] [,clipboard=<vnc>] [,memory=<integer>] 
    
Configure the VGA hardware.  

--virtio[n] [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,import-from=<source volume>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,iothread=<1|0>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,ro=<1|0>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,werror=<enum>] 
    
Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the _import-from_ parameter to import from an existing volume.  

--virtiofs[n] [dirid=]<mapping-id> [,cache=<enum>] [,direct-io=<1|0>] [,expose-acl=<1|0>] [,expose-xattr=<1|0>] 
    
Configuration for sharing a directory between host and guest using Virtio-fs.  

--vmgenid <UUID> (_default =_ 1 (autogenerated)) 
    
Set VM Generation ID. Use _1_ to autogenerate on create or update, pass _0_ to disable explicitly.  

--vmstatestorage <storage ID> 
    
Default storage for VM state volumes/files.  

--watchdog [[model=]<i6300esb|ib700>] [,action=<enum>] 
    
Create a virtual hardware watchdog device. 
**qm showcmd** <vmid> [OPTIONS]
Show command line which is used to start the VM (debug info). 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--pretty <boolean> (_default =_ 0) 
    
Puts each option on a new line to enhance human readability  

--snapshot <string> 
    
Fetch config values from given snapshot. 
**qm shutdown** <vmid> [OPTIONS]
Shutdown virtual machine. This is similar to pressing the power button on a physical machine. This will send an ACPI event for the guest OS, which should then proceed to a clean shutdown. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--forceStop <boolean> (_default =_ 0) 
    
Make sure the VM stops.  

--keepActive <boolean> (_default =_ 0) 
    
Do not deactivate storage volumes.  

--skiplock <boolean> 
    
Ignore locks - only root is allowed to use this option.  

--timeout <integer> (0 - N) 
    
Wait maximal timeout seconds. 
**qm snapshot** <vmid> <snapname> [OPTIONS]
Snapshot a VM. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

<snapname>: <string> 
    
The name of the snapshot.  

--description <string> 
    
A textual description or comment.  

--vmstate <boolean> 
    
Save the vmstate 
**qm start** <vmid> [OPTIONS]
Start virtual machine. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--force-cpu <string> 
    
Override QEMU’s -cpu argument with the given string.  

--machine [[type=]<machine type>] [,aw-bits=<number>] [,enable-s3=<1|0>] [,enable-s4=<1|0>] [,viommu=<intel|virtio>] 
    
Specify the QEMU machine.  

--migratedfrom <string> 
    
The cluster node name.  

--migration_network <string> 
    
CIDR of the (sub) network that is used for migration.  

--migration_type <insecure | secure> 
    
Migration traffic is encrypted using an SSH tunnel by default. On secure, completely private networks this can be disabled to increase performance.  

--nets-host-mtu net\d+=\d+(,net\d+=\d+)* 
    
Used for migration compat. List of VirtIO network devices and their effective host_mtu setting according to the QEMU object model on the source side of the migration. A value of 0 means that the host_mtu parameter is to be avoided for the corresponding device.  

--skiplock <boolean> 
    
Ignore locks - only root is allowed to use this option.  

--stateuri <string> 
    
Some command save/restore state from this location.  

--targetstorage <string> 
    
Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value _1_ will map each source storage to itself.  

--timeout <integer> (0 - N) (_default =_ max(30, vm memory in GiB)) 
    
Wait maximal timeout seconds.  

--with-conntrack-state <boolean> (_default =_ 0) 
    
Whether to migrate conntrack entries for running VMs. 
**qm status** <vmid> [OPTIONS]
Show VM status. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--verbose <boolean> 
    
Verbose output format 
**qm stop** <vmid> [OPTIONS]
Stop virtual machine. The qemu process will exit immediately. This is akin to pulling the power plug of a running computer and may damage the VM data. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--keepActive <boolean> (_default =_ 0) 
    
Do not deactivate storage volumes.  

--migratedfrom <string> 
    
The cluster node name.  

--overrule-shutdown <boolean> (_default =_ 0) 
    
Try to abort active _qmshutdown_ tasks before stopping.  

--skiplock <boolean> 
    
Ignore locks - only root is allowed to use this option.  

--timeout <integer> (0 - N) 
    
Wait maximal timeout seconds. 
**qm suspend** <vmid> [OPTIONS]
Suspend virtual machine. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--skiplock <boolean> 
    
Ignore locks - only root is allowed to use this option.  

--statestorage <storage ID> 
    
The storage for the VM state   
| Requires option(s): todisk  |  
| --- | 

--todisk <boolean> (_default =_ 0) 
      
If set, suspends the VM to disk. Will be resumed on next VM start. 
**qm template** <vmid> [OPTIONS]
Create a Template. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--disk <efidisk0 | ide0 | ide1 | ide2 | ide3 | sata0 | sata1 | sata2 | sata3 | sata4 | sata5 | scsi0 | scsi1 | scsi10 | scsi11 | scsi12 | scsi13 | scsi14 | scsi15 | scsi16 | scsi17 | scsi18 | scsi19 | scsi2 | scsi20 | scsi21 | scsi22 | scsi23 | scsi24 | scsi25 | scsi26 | scsi27 | scsi28 | scsi29 | scsi3 | scsi30 | scsi4 | scsi5 | scsi6 | scsi7 | scsi8 | scsi9 | tpmstate0 | virtio0 | virtio1 | virtio10 | virtio11 | virtio12 | virtio13 | virtio14 | virtio15 | virtio2 | virtio3 | virtio4 | virtio5 | virtio6 | virtio7 | virtio8 | virtio9> 
    
If you want to convert only 1 disk to base image. 
**qm terminal** <vmid> [OPTIONS]
Open a terminal using a serial device (The VM need to have a serial device configured, for example _serial0: socket_) 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--escape <string> (_default =_ ^O) 
    
Escape character.  

--iface <serial0 | serial1 | serial2 | serial3> 
    
Select the serial device. By default we simply use the first suitable device. 
**qm unlink**
An alias for _qm disk unlink_.
**qm unlock** <vmid>
Unlock the VM. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM. 
**qm vncproxy** <vmid>
Proxy VM VNC traffic to stdin/stdout 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM. 
**qm wait** <vmid> [OPTIONS]
Wait until the VM is stopped. 

<vmid>: <integer> (100 - 999999999) 
    
The (unique) ID of the VM.  

--timeout <integer> (1 - N) 
    
Timeout in seconds. Default is to wait forever. 
##  DESCRIPTION 
QEMU (short form for Quick Emulator) is an open source hypervisor that emulates a physical computer. From the perspective of the host system where QEMU is running, QEMU is a user program which has access to a number of local resources like partitions, files, network cards which are then passed to an emulated computer which sees them as if they were real devices.
A guest operating system running in the emulated computer accesses these devices, and runs as if it were running on real hardware. For instance, you can pass an ISO image as a parameter to QEMU, and the OS running in the emulated computer will see a real CD-ROM inserted into a CD drive.
QEMU can emulate a great variety of hardware, from ARM to Sparc. On x86 hosts, Proxmox VE is concerned with 32-bit and 64-bit PC clone emulation, since it represents the overwhelming majority of server hardware. On arm64 hosts, Proxmox VE emulates 64-bit ARM (aarch64) machines instead. Emulating the same architecture as the host is also one of the fastest options, due to the availability of processor extensions which greatly speed up QEMU when the emulated architecture matches the host architecture.  
| You may sometimes encounter the term _KVM_ (Kernel-based Virtual Machine). It means that QEMU is running with the support of the virtualization processor extensions, via the Linux KVM module. In the context of Proxmox VE _QEMU_ and _KVM_ can be used interchangeably, as QEMU in Proxmox VE will always try to load the KVM module.  |  
| --- |  
QEMU inside Proxmox VE runs as a root process, since this is required to access block and PCI devices.
##  Emulated devices and paravirtualized devices 
The PC hardware emulated by QEMU includes a motherboard, network controllers, SCSI, IDE and SATA controllers, serial ports (the complete list can be seen in the kvm(1) man page) all of them emulated in software. All these devices are the exact software equivalent of existing hardware devices, and if the OS running in the guest has the proper drivers it will use the devices as if it were running on real hardware. This allows QEMU to run _unmodified_ operating systems.
This however has a performance cost, as running in software what was meant to run in hardware involves a lot of extra work for the host CPU. To mitigate this, QEMU can present to the guest operating system _paravirtualized devices_ , where the guest OS recognizes it is running inside QEMU and cooperates with the hypervisor.
QEMU relies on the virtio virtualization standard, and is thus able to present paravirtualized virtio devices, which includes a paravirtualized generic disk controller, a paravirtualized network card, a paravirtualized serial port, a paravirtualized SCSI controller, etc …  
| It is **highly recommended** to use the virtio devices whenever you can, as they provide a big performance improvement and are generally better maintained. Using the virtio generic disk controller versus an emulated IDE controller will double the sequential write throughput, as measured with bonnie++(8). Using the virtio network interface can deliver up to three times the throughput of an emulated Intel E1000 network card, as measured with iperf(1). [See this benchmark on the KVM wiki <https://www.linux-kvm.org/page/Using_VirtIO_NIC>]  |  
| --- |  
##  Virtual Machines Settings 
Generally speaking Proxmox VE tries to choose sane defaults for virtual machines (VM). Make sure you understand the meaning of the settings you change, as it could incur a performance slowdown, or putting your data at risk.
###  General Settings
General settings of a VM include
  * the **Node** : the physical server on which the VM will run 
  * the **VM ID** : a unique number in this Proxmox VE installation used to identify your VM 
  * **Name** : a free form text string you can use to describe the VM 
  * **Resource Pool** : a logical group of VMs 


###  OS Settings
When creating a virtual machine (VM), setting the proper Operating System(OS) allows Proxmox VE to optimize some low level parameters. For instance Windows OS expect the BIOS clock to use the local time, while Unix based OS expect the BIOS clock to have the UTC time.
###  System Settings
On VM creation you can change some basic system components of the new VM. You can specify which [display type](https://pve.proxmox.com/pve-docs/qm.1.html#qm_display) you want to use.
Additionally, the [SCSI controller](https://pve.proxmox.com/pve-docs/qm.1.html#qm_hard_disk) can be changed. If you plan to install the QEMU Guest Agent, or if your selected ISO image already ships and installs it automatically, you may want to tick the _QEMU Agent_ box, which lets Proxmox VE know that it can use its features to show some more information, and complete some actions (for example, shutdown or snapshots) more intelligently.
Proxmox VE allows to boot VMs with different firmware and machine types, namely [SeaBIOS and OVMF](https://pve.proxmox.com/pve-docs/qm.1.html#qm_bios_and_uefi). In most cases you want to switch from the default SeaBIOS to OVMF only if you plan to use [PCIe passthrough](https://pve.proxmox.com/pve-docs/qm.1.html#qm_pci_passthrough). On arm64 hosts OVMF is the default and only option, as SeaBIOS is x86-only.
#### Machine Type 
A VM’s _Machine Type_ defines the hardware layout of the VM’s virtual motherboard. You can choose between the default [Intel 440FX](https://en.wikipedia.org/wiki/Intel_440FX) or the [Q35](https://ark.intel.com/content/www/us/en/ark/products/31918/intel-82q35-graphics-and-memory-controller.html) chipset, which also provides a virtual PCIe bus, and thus may be desired if you want to pass through PCIe hardware. Additionally, you can select a [vIOMMU](https://pve.proxmox.com/pve-docs/qm.1.html#qm_pci_viommu) implementation.  
| The Intel 440FX and Q35 chipsets are specific to x86 guests. On arm64 hosts, virtual machines use the virt machine type, which models a generic, UEFI-based ARM machine.  |  
| --- |  
##### Machine Version 
Each machine type is versioned in QEMU and a given QEMU binary supports many machine versions. New versions might bring support for new features, fixes or general improvements. However, they also change properties of the virtual hardware. To avoid sudden changes from the guest’s perspective and ensure compatibility of the VM state, live-migration and snapshots with RAM will keep using the same machine version in the new QEMU instance.
For Windows guests, the machine version is pinned during creation, because Windows is sensitive to changes in the virtual hardware - even between cold boots. For example, the enumeration of network devices might be different with different machine versions. Other OSes like Linux can usually deal with such changes just fine. For those, the _Latest_ machine version is used by default. This means that after a fresh start, the newest machine version supported by the QEMU binary is used (e.g. the newest machine version QEMU 8.1 supports is version 8.1 for each machine type).
The machine version is also used as a safeguard when implementing new features or fixes that would change the hardware layout to ensure backward compatibility. For operations on a running VM, such as live migrations, the running machine version is saved to ensure that the VM can be recovered exactly as it was, not only from a QEMU virtualization perspective, but also in terms of how Proxmox VE will create the QEMU virtual machine instance.
PVE Machine Revision
Sometimes Proxmox VE needs to make changes to the hardware layout or modify options without waiting for a new QEMU release. For this, Proxmox VE has added an extra downstream revision in the form of +pveX. In these revisions, X is 0 for each new QEMU machine version and is omitted in this case, e.g. machine version pc-q35-9.2 would be the same as machine version pc-q35-9.2+pve0.
If Proxmox VE wants to change the hardware layout or a default option, the revision is incremented and used for newly created guests or on reboot for VMs that always use the latest machine version.
##### QEMU Machine Version Deprecation 
Starting with QEMU 10.1, machine versions are removed from upstream QEMU after 6 years. In Proxmox VE, major releases happen approximately every 2 years, so a major Proxmox VE release will support machine versions from approximately two previous major Proxmox VE releases.
Before upgrading to a new major Proxmox VE release, you should update VM configurations to avoid all machine versions that will be dropped during the next major Proxmox VE release. This ensures that the guests can still be used throughout that release. See the section [Update to a Newer Machine Version](https://pve.proxmox.com/pve-docs/qm.1.html#qm_machine_update).
The removal policy is not yet in effect for Proxmox VE 8, so the baseline for supported machine versions is 2.4. The last QEMU binary version released for Proxmox VE 9 is expected to be QEMU 11.2. This QEMU binary will remove support for machine versions older than 6.0, so 6.0 is the baseline for the Proxmox VE 9 release life cycle. The baseline is expected to increase by 2 major versions for each major Proxmox VE release, for example 8.0 for Proxmox VE 10.
##### Update to a Newer Machine Version 
If you see a deprecation warning, you should change the machine version to a newer one. Be sure to have a working backup first and be prepared for changes to how the guest sees hardware. In some scenarios, re-installing certain drivers might be required. You should also check for snapshots with RAM that were taken with these machine versions (i.e. the runningmachine configuration entry). Unfortunately, there is no way to change the machine version of a snapshot, so you’d need to load the snapshot to salvage any data from it.
###  Hard Disk
#### Bus/Controller 
QEMU can emulate a number of storage controllers:  
| It is highly recommended to use the **VirtIO SCSI** or **VirtIO Block** controller for performance reasons and because they are better maintained.  |  
| --- |  
  * the **IDE** controller, has a design which goes back to the 1984 PC/AT disk controller. Even if this controller has been superseded by recent designs, each and every OS you can think of has support for it, making it a great choice if you want to run an OS released before 2003. You can connect up to 4 devices on this controller. 
  * the **SATA** (Serial ATA) controller, dating from 2003, has a more modern design, allowing higher throughput and a greater number of devices to be connected. You can connect up to 6 devices on this controller. 
  * the **SCSI** controller, designed in 1985, is commonly found on server grade hardware, and can connect up to 14 storage devices. Proxmox VE emulates by default a LSI 53C895A controller. 
A SCSI controller of type _VirtIO SCSI single_ and enabling the [IO Thread](https://pve.proxmox.com/pve-docs/qm.1.html#qm_hard_disk_iothread) setting for the attached disks is recommended if you aim for performance. This is the default for newly created Linux VMs since Proxmox VE 7.3. Each disk will have its own _VirtIO SCSI_ controller, and QEMU will handle the disks IO in a dedicated thread. Linux distributions have support for this controller since 2012, and FreeBSD since 2014. For Windows OSes, you need to provide an extra ISO containing the drivers during the installation.
  * The **VirtIO Block** controller, often just called VirtIO or virtio-blk, is an older type of paravirtualized controller. It has been superseded by the VirtIO SCSI Controller, in terms of features. 


#### Image Format 
On each controller you attach a number of emulated hard disks, which are backed by a file or a block device residing in the configured storage. The choice of a storage type will determine the format of the hard disk image. Storages which present block devices (LVM, ZFS, Ceph) will require the **raw disk image format** , whereas files based storages (like Ext4, XFS, NFS, or CIFS) will let you to choose either the **raw disk image format** or the **QEMU image format**.
  * the **QEMU image format** is a copy on write format which allows snapshots, and thin provisioning of the disk image. 
  * the **raw disk image** is a bit-to-bit image of a hard disk, similar to what you would get when executing the dd command on a block device in Linux. This format does not support thin provisioning or snapshots by itself, requiring cooperation from the storage layer for these tasks. It may, however, be up to 10% faster than the **QEMU image format**. [See this benchmark for details <https://events.static.linuxfound.org/sites/events/files/slides/CloudOpen2013_Khoa_Huynh_v3.pdf>]
  * the **VMware image format** only makes sense if you intend to import/export the disk image to other hypervisors. 


#### Cache Mode 
Setting the **Cache** mode of the hard drive will impact how the host system will notify the guest systems of block write completions. The **No cache** default means that the guest system will be notified that a write is complete when each block reaches the physical storage write queue, ignoring the host page cache. This provides a good balance between safety and speed.
If you want the Proxmox VE backup manager to skip a disk when doing a backup of a VM, you can set the **No backup** option on that disk.
If you want the Proxmox VE storage replication mechanism to skip a disk when starting a replication job, you can set the **Skip replication** option on that disk. As of Proxmox VE 5.0, replication requires the disk images to be on a storage of type zfspool, so adding a disk image to other storages when the VM has replication configured requires to skip replication for this disk image.
#### Trim/Discard 
If your storage supports _thin provisioning_ (see the storage chapter in the Proxmox VE guide), you can activate the **Discard** option on a drive. With **Discard** set and a _TRIM_ -enabled guest OS [TRIM, UNMAP, and discard <https://en.wikipedia.org/wiki/Trim_%28computing%29>], when the VM’s filesystem marks blocks as unused after deleting files, the controller will relay this information to the storage, which will then shrink the disk image accordingly. For the guest to be able to issue _TRIM_ commands, you must enable the **Discard** option on the drive. Some guest operating systems may also require the **SSD Emulation** flag to be set. Note that **Discard** on **VirtIO Block** drives is only supported on guests using Linux Kernel 5.0 or higher.
If you would like a drive to be presented to the guest as a solid-state drive rather than a rotational hard disk, you can set the **SSD emulation** option on that drive. There is no requirement that the underlying storage actually be backed by SSDs; this feature can be used with physical media of any type. Note that **SSD emulation** is not supported on **VirtIO Block** drives.
#### IO Thread 
The **IO thread** option can only be used when using a disk with one of the following bus/device controllers:
  * **SCSI** , if the emulated SCSI controller type is **VirtIO SCSI single** , or 
  * **VirtIO Block**


With **IO thread** enabled, QEMU creates one I/O thread per storage controller rather than handling all I/O in the main event loop or vCPU threads. One benefit is better work distribution and utilization of the underlying storage. Another benefit is reduced latency (hangs) in the guest for very I/O-intensive host workloads, since neither the main thread nor a vCPU thread can be blocked by disk I/O.
###  CPU
A **CPU socket** is a physical slot on a PC motherboard where you can plug a CPU. This CPU can then contain one or many **cores** , which are independent processing units. Whether you have a single CPU socket with 4 cores, or two CPU sockets with two cores is mostly irrelevant from a performance point of view. However some software licenses depend on the number of sockets a machine has, in that case it makes sense to set the number of sockets to what the license allows you.
Increasing the number of virtual CPUs (cores and sockets) will usually provide a performance improvement though that is heavily dependent on the use of the VM. Multi-threaded applications will of course benefit from a large number of virtual CPUs, as for each virtual cpu you add, QEMU will create a new thread of execution on the host system. If you’re not sure about the workload of your VM, it is usually a safe bet to set the number of **Total cores** to 2.  
| It is perfectly safe if the _overall_ number of cores of all your VMs is greater than the number of cores on the server (for example, 4 VMs each with 4 cores (= total 16) on a machine with only 8 cores). In that case the host system will balance the QEMU execution threads between your server cores, just like if you were running a standard multi-threaded application. However, Proxmox VE will prevent you from starting VMs with more virtual CPU cores than physically available, as this will only bring the performance down due to the cost of context switches.  |  
| --- |  
#### Resource Limits 
**cpulimit**
In addition to the number of virtual cores, the total available “Host CPU Time” for the VM can be set with the **cpulimit** option. It is a floating point value representing CPU time in percent, so 1.0 is equal to 100%, 2.5 to 250% and so on. If a single process would fully use one single core it would have 100% CPU Time usage. If a VM with four cores utilizes all its cores fully it would theoretically use 400%. In reality the usage may be even a bit higher as QEMU can have additional threads for VM peripherals besides the vCPU core ones.
This setting can be useful when a VM should have multiple vCPUs because it is running some processes in parallel, but the VM as a whole should not be able to run all vCPUs at 100% at the same time.
For example, suppose you have a virtual machine that would benefit from having 8 virtual CPUs, but you don’t want the VM to be able to max out all 8 cores running at full load - because that would overload the server and leave other virtual machines and containers with too little CPU time. To solve this, you could set **cpulimit** to 4.0 (=400%). This means that if the VM fully utilizes all 8 virtual CPUs by running 8 processes simultaneously, each vCPU will receive a maximum of 50% CPU time from the physical cores. However, if the VM workload only fully utilizes 4 virtual CPUs, it could still receive up to 100% CPU time from a physical core, for a total of 400%.  
| VMs can, depending on their configuration, use additional threads, such as for networking or IO operations but also live migration. Thus a VM can show up to use more CPU time than just its virtual CPUs could use. To ensure that a VM never uses more CPU time than vCPUs assigned, set the **cpulimit** to the same value as the total core count.  |  
| --- |  
**cpuunits**
With the **cpuunits** option, nowadays often called CPU shares or CPU weight, you can control how much CPU time a VM gets compared to other running VMs. It is a relative weight which defaults to 100 (or 1024 if the host uses legacy cgroup v1). If you increase this for a VM it will be prioritized by the scheduler in comparison to other VMs with lower weight.
For example, if VM 100 has set the default 100 and VM 200 was changed to 200, the latter VM 200 would receive twice the CPU bandwidth than the first VM 100.
For more information see man systemd.resource-control, here CPUQuota corresponds to cpulimit and CPUWeight to our cpuunits setting. Visit its Notes section for references and implementation details.
**affinity**
With the **affinity** option, you can specify the physical CPU cores that are used to run the VM’s vCPUs. Peripheral VM processes, such as those for I/O, are not affected by this setting. Note that the **CPU affinity is not a security feature**.
Forcing a CPU **affinity** can make sense in certain cases but is accompanied by an increase in complexity and maintenance effort. For example, if you want to add more VMs later or migrate VMs to nodes with fewer CPU cores. It can also easily lead to asynchronous and therefore limited system performance if some CPUs are fully utilized while others are almost idle.
The **affinity** is set through the taskset CLI tool. It accepts the host CPU numbers (see lscpu) in the List Format from man cpuset. This ASCII decimal list can contain numbers but also number ranges. For example, the **affinity** 0-1,8-11 (expanded 0, 1, 8, 9, 10, 11) would allow the VM to run on only these six specific host cores.
#### CPU Type 
QEMU can emulate a number different of **CPU types** from 486 to the latest Xeon processors. Each new processor generation adds new features, like hardware assisted 3d rendering, random number generation, memory protection, etc. Also, a current generation can be upgraded through microcode update with bug or security fixes.
Usually you should select for your VM a processor type which closely matches the CPU of the host system, as it means that the host CPU features (also called _CPU flags_ ) will be available in your VMs. If you want an exact match, you can set the CPU type to **host** in which case the VM will have exactly the same CPU flags as your host system.
This has a downside though. If you want to do a live migration of VMs between different hosts, your VM might end up on a new system with a different CPU type or a different microcode version. If the CPU flags passed to the guest are missing, the QEMU process will stop. To remedy this QEMU has also its own virtual CPU types, that Proxmox VE uses by default.
The backend default is _kvm64_ which works on essentially all x86_64 host CPUs and the UI default when creating a new VM is _x86-64-v2-AES_ , which requires a host CPU starting from Westmere for Intel or at least a fourth generation Opteron for AMD.  
| The _kvm64_ and _x86-64-v*_ CPU models described here are x86-only. On arm64 hosts, guests use ARM CPU models: _host_ to expose the physical CPU (recommended on the supported hardware), or a generic model such as _max_ , together with the virt machine type.  |  
| --- |  
In short:
If you don’t care about live migration or have a homogeneous cluster where all nodes have the same CPU and same microcode version, set the CPU type to host, as in theory this will give your guests maximum performance.
If you care about live migration and security, and you have only Intel CPUs or only AMD CPUs, choose the lowest generation CPU model of your cluster.
If you care about live migration without security, or have mixed Intel/AMD cluster, choose the lowest compatible virtual QEMU CPU type.  
| Live migrations between Intel and AMD host CPUs have no guarantee to work.  |  
| --- |  
See also List of AMD and Intel CPU Types as Defined in QEMU.
#### QEMU CPU Types 
QEMU also provide virtual CPU types, compatible with both Intel and AMD host CPUs.  
| To mitigate the Spectre vulnerability for virtual CPU types, you need to add the relevant CPU flags, see [Meltdown / Spectre related CPU flags](https://pve.proxmox.com/pve-docs/qm.1.html#qm_meltdown_spectre).  |  
| --- |  
Historically, Proxmox VE had the _kvm64_ CPU model, with CPU flags at the level of Pentium 4 enabled, so performance was not great for certain workloads.
In the summer of 2020, AMD, Intel, Red Hat, and SUSE collaborated to define three x86-64 microarchitecture levels on top of the x86-64 baseline, with modern flags enabled. For details, see the [x86-64-ABI specification](https://gitlab.com/x86-psABIs/x86-64-ABI).  
| Some newer distributions like CentOS 9 are now built with _x86-64-v2_ flags as a minimum requirement.  |  
| --- |  
  * _kvm64 (x86-64-v1)_ : Compatible with Intel CPU >= Pentium 4, AMD CPU >= Phenom. 
  * _x86-64-v2_ : Compatible with Intel CPU >= Nehalem, AMD CPU >= Opteron_G3. Added CPU flags compared to _x86-64-v1_ : _+cx16_ , _+lahf-lm_ , _+popcnt_ , _+pni_ , _+sse4.1_ , _+sse4.2_ , _+ssse3_. 
  * _x86-64-v2-AES_ : Compatible with Intel CPU >= Westmere, AMD CPU >= Opteron_G4. Added CPU flags compared to _x86-64-v2_ : _+aes_. 
  * _x86-64-v3_ : Compatible with Intel CPU >= Haswell, AMD CPU >= EPYC. Added CPU flags compared to _x86-64-v2-AES_ : _+avx_ , _+avx2_ , _+bmi1_ , _+bmi2_ , _+f16c_ , _+fma_ , _+movbe_ , _+xsave_. 
  * _x86-64-v4_ : Compatible with Intel CPU >= Skylake, AMD CPU >= EPYC v4 Genoa. Added CPU flags compared to _x86-64-v3_ : _+avx512f_ , _+avx512bw_ , _+avx512cd_ , _+avx512dq_ , _+avx512vl_. 


#### Custom CPU Types 
You can define custom CPU types with a configurable set of base model, vendor, physical address bits, and per-flag toggles, then assign them to VMs like a built-in type. Custom types are referenced from a VM configuration as custom-<name>.
Manage them under Datacenter -> Custom CPU Models in the web UI. The model dialog embeds a flag editor grid with free-text search over flag name and description, an accelerator (kvm/tcg) selector, and a per-node multi-select that highlights the flags each selected cluster node currently reports as supported - useful to spot which flags would actually be available on the target hosts before committing to a model. The same grid is reused in the per-VM Processor edit dialog, restricted there to the flags settable per VM; configured flags unknown to the API or unsupported on the selected accelerator surface at the top with a warning.
Custom CPU types are still backed by the configuration file /etc/pve/virtual-guest/cpu-models.conf and can be maintained from the CLI as well, see man cpu-models.conf for the format.
Access to a custom model is controlled per model via the ACL path /mapping/cpu/<name>. Mapping.Audit lets a user see the model in listings, Mapping.Modify gates create/update/delete in the panel, and Mapping.Use is required to assign the model to a VM. The latter is enforced on VM create, VM update, and VM clone, so a user who can clone a VM that uses a custom model still needs Mapping.Use on that model’s ACL path.
#### Meltdown / Spectre related CPU flags 
There are several CPU flags related to the Meltdown and Spectre vulnerabilities [Meltdown Attack <https://meltdownattack.com/>] which need to be set manually unless the selected CPU type of your VM already enables them by default.
There are two requirements that need to be fulfilled in order to use these CPU flags:
  * The host CPU(s) must support the feature and propagate it to the guest’s virtual CPU(s) 
  * The guest operating system must be updated to a version which mitigates the attacks and is able to utilize the CPU feature 


Otherwise you need to set the desired CPU flag of the virtual CPU, either by editing the CPU options in the web UI, or by setting the _flags_ property of the _cpu_ option in the VM configuration file.
For Spectre v1,v2,v4 fixes, your CPU or system vendor also needs to provide a so-called “microcode update” for your CPU, see chapter Firmware Updates. Note that not all affected CPUs can be updated to support spec-ctrl.
To check if the Proxmox VE host is vulnerable, execute the following command as root:

```
for f in /sys/devices/system/cpu/vulnerabilities/*; do echo "${f##*/} -" $(cat "$f"); done
```

A community script is also available to detect if the host is still vulnerable. [spectre-meltdown-checker <https://meltdown.ovh/>]
#### Intel processors 
  * _pcid_
This reduces the performance impact of the Meltdown (CVE-2017-5754) mitigation called _Kernel Page-Table Isolation (KPTI)_ , which effectively hides the Kernel memory from the user space. Without PCID, KPTI is quite an expensive mechanism [PCID is now a critical performance/security feature on x86 <https://groups.google.com/forum/m/#!topic/mechanical-sympathy/L9mHTbeQLNU>].
To check if the Proxmox VE host supports PCID, execute the following command as root:

```
# grep ' pcid ' /proc/cpuinfo
```

If this does not return empty your host’s CPU has support for _pcid_.
  * _spec-ctrl_
Required to enable the Spectre v1 (CVE-2017-5753) and Spectre v2 (CVE-2017-5715) fix, in cases where retpolines are not sufficient. Included by default in Intel CPU models with -IBRS suffix. Must be explicitly turned on for Intel CPU models without -IBRS suffix. Requires an updated host CPU microcode (intel-microcode >= 20180425).
  * _ssbd_
Required to enable the Spectre V4 (CVE-2018-3639) fix. Not included by default in any Intel CPU model. Must be explicitly turned on for all Intel CPU models. Requires an updated host CPU microcode(intel-microcode >= 20180703).


#### AMD processors 
  * _ibpb_
Required to enable the Spectre v1 (CVE-2017-5753) and Spectre v2 (CVE-2017-5715) fix, in cases where retpolines are not sufficient. Included by default in AMD CPU models with -IBPB suffix. Must be explicitly turned on for AMD CPU models without -IBPB suffix. Requires the host CPU microcode to support this feature before it can be used for guest CPUs.
  * _virt-ssbd_
Required to enable the Spectre v4 (CVE-2018-3639) fix. Not included by default in any AMD CPU model. Must be explicitly turned on for all AMD CPU models. This should be provided to guests, even if amd-ssbd is also provided, for maximum guest compatibility. Note that this must be explicitly enabled when when using the "host" cpu model, because this is a virtual feature which does not exist in the physical CPUs.
  * _amd-ssbd_
Required to enable the Spectre v4 (CVE-2018-3639) fix. Not included by default in any AMD CPU model. Must be explicitly turned on for all AMD CPU models. This provides higher performance than virt-ssbd, therefore a host supporting this should always expose this to guests if possible. virt-ssbd should none the less also be exposed for maximum guest compatibility as some kernels only know about virt-ssbd.
  * _amd-no-ssb_
Recommended to indicate the host is not vulnerable to Spectre V4 (CVE-2018-3639). Not included by default in any AMD CPU model. Future hardware generations of CPU will not be vulnerable to CVE-2018-3639, and thus the guest should be told not to enable its mitigations, by exposing amd-no-ssb. This is mutually exclusive with virt-ssbd and amd-ssbd.


#### Windows-related CPU settings 
A couple of CPU defaults and properties are tuned specifically for Windows guests on recent Intel hardware:
  * cet-ibt and cet-ss (Control-flow Enforcement Technology: indirect branch tracking and shadow stack) are disabled by default for Windows 11 machine types, as they currently break boot for Windows guests with virtualization-based security enabled. Workloads that explicitly rely on the flags can re-enable them per VM via the Processor flag editor. 
  * The QEMU level CPU property is exposed so it can be set per VM (or in a custom CPU model) without resorting to custom args. Setting level=30 is a known workaround for Hyper-V boot failures of Windows guests on recent Intel hosts when the CPU type is host or max. The property only applies for x86_64 vCPUs; it is silently ignored on other architectures. 


#### NUMA 
You can also optionally emulate a **NUMA** [<https://en.wikipedia.org/wiki/Non-uniform_memory_access>] architecture in your VMs. The basics of the NUMA architecture mean that instead of having a global memory pool available to all your cores, the memory is spread into local banks close to each socket. This can bring speed improvements as the memory bus is not a bottleneck anymore. If your system has a NUMA architecture [if the command numactl --hardware | grep available returns more than one node, then your host system has a NUMA architecture] we recommend to activate the option, as this will allow proper distribution of the VM resources on the host system. This option is also required to hot-plug cores or RAM in a VM.
If the NUMA option is used, it is recommended to set the number of sockets to the number of nodes of the host system.
#### vCPU hot-plug 
Modern operating systems introduced the capability to hot-plug and, to a certain extent, hot-unplug CPUs in a running system. Virtualization allows us to avoid a lot of the (physical) problems real hardware can cause in such scenarios. Still, this is a rather new and complicated feature, so its use should be restricted to cases where its absolutely needed. Most of the functionality can be replicated with other, well tested and less complicated, features, see [Resource Limits](https://pve.proxmox.com/pve-docs/qm.1.html#qm_cpu_resource_limits).
In Proxmox VE the maximal number of plugged CPUs is always cores * sockets. To start a VM with less than this total core count of CPUs you may use the **vcpus** setting, it denotes how many vCPUs should be plugged in at VM start.
Currently this feature is only supported on Linux, a kernel newer than 3.10 is needed, a kernel newer than 4.7 is recommended.
You can use a udev rule as follow to automatically set new CPUs as online in the guest:

```
SUBSYSTEM=="cpu", ACTION=="add", TEST=="online", ATTR{online}=="0", ATTR{online}="1"
```

Save this under /etc/udev/rules.d/ as a file ending in .rules.
Note: CPU hot-remove is machine dependent and requires guest cooperation. The deletion command does not guarantee CPU removal to actually happen, typically it’s a request forwarded to guest OS using target dependent mechanism, such as ACPI on x86/amd64.
###  Memory
For each VM you have the option to set a fixed size memory or asking Proxmox VE to dynamically allocate memory based on the current RAM usage of the host.
Fixed Memory Allocation
When setting memory and minimum memory to the same amount Proxmox VE will simply allocate what you specify to your VM.
Even when using a fixed memory size, the ballooning device gets added to the VM, because it delivers useful information such as how much memory the guest really uses. In general, you should leave **ballooning** enabled, but if you want to disable it (like for debugging purposes), simply uncheck **Ballooning Device** or set

```
balloon: 0
```

in the configuration.
Automatic Memory Allocation
When setting the minimum memory lower than memory, Proxmox VE will make sure that the minimum amount you specified is always available to the VM, and if RAM usage on the host is below a certain target percentage, will dynamically add memory to the guest up to the maximum memory specified. The target percentage defaults to 80% and can be configured in the node options. 
When the host is running low on RAM, the VM will then release some memory back to the host, swapping running processes if needed and starting the oom killer in last resort. The passing around of memory between host and guest is done via a special balloon kernel driver running inside the guest, which will grab or release memory pages from the host. [A good explanation of the inner workings of the balloon driver can be found here <https://rwmj.wordpress.com/2010/07/17/virtio-balloon/>]
When multiple VMs use the autoallocate facility, it is possible to set a **Shares** coefficient which indicates the relative amount of the free host memory that each VM should take. Suppose for instance you have four VMs, three of them running an HTTP server and the last one is a database server. The host is configured to target 80% RAM usage. To cache more database blocks in the database server RAM, you would like to prioritize the database VM when spare RAM is available. For this you assign a Shares property of 3000 to the database VM, leaving the other VMs to the Shares default setting of 1000. The host server has 32GB of RAM, and is currently using 16GB, leaving 32 * 80/100 - 16 = 9GB RAM to be allocated to the VMs on top of their configured minimum memory amount. The database VM will benefit from 9 * 3000 / (3000 + 1000 + 1000 + 1000) = 4.5 GB extra RAM and each HTTP server from 1.5 GB.
All Linux distributions released after 2010 have the balloon kernel driver included. For Windows OSes, the balloon driver needs to be added manually and can incur a slowdown of the guest, so we don’t recommend using it on critical systems.
When allocating RAM to your VMs, a good rule of thumb is always to leave 1GB of RAM available to the host.
###  Memory Encryption
#### AMD SEV 
SEV (Secure Encrypted Virtualization) enables memory encryption per VM using AES-128 encryption and the AMD Secure Processor.
SEV-ES (Secure Encrypted Virtualization - Encrypted State) in addition encrypts all CPU register contents, to prevent leakage of information to the hypervisor.
SEV-SNP (Secure Encrypted Virtualization - Secure Nested Paging) also attempts to prevent software-based integrity attacks. See the [ AMD SEV SNP white paper](https://www.amd.com/content/dam/amd/en/documents/epyc-business-docs/white-papers/SEV-SNP-strengthening-vm-isolation-with-integrity-protection-and-more.pdf) for more information.
**Host Requirements:**
  * AMD EPYC CPU 
  * SEV-ES is only supported on AMD EPYC 7002 series and newer EPYC CPUs 
  * SEV-SNP is only supported on AMD EPYC 7003 series and newer EPYC CPUs 
  * SEV-SNP requires host kernel version 6.11 or higher. 
  * configure AMD memory encryption in the BIOS settings of the host machine 
  * add "kvm_amd.sev=1" to kernel parameters if not enabled by default 
  * add "mem_encrypt=on" to kernel parameters if you want to encrypt memory on the host (SME) see <https://www.kernel.org/doc/Documentation/x86/amd-memory-encryption.txt>
  * maybe increase SWIOTLB see <https://github.com/AMDESE/AMDSEV#faq-4>


To check if SEV is enabled on the host search for sev in dmesg and print out the SEV kernel parameter of kvm_amd:

```
# dmesg | grep -i sev
[...] ccp 0000:45:00.1: sev enabled
[...] ccp 0000:45:00.1: SEV API: <buildversion>
[...] SEV supported: <number> ASIDs
[...] SEV-ES supported: <number> ASIDs
# cat /sys/module/kvm_amd/parameters/sev
Y
```

**Guest Requirements:**
  * edk2-OVMF 
  * advisable to use Q35 
  * The guest operating system must contain SEV-support. 


**Limitations:**
  * Because the memory is encrypted the memory usage on host is always wrong. 
  * Operations that involve saving or restoring memory like snapshots & live migration do not work yet or are [attackable](https://github.com/PSPReverse/amd-sev-migration-attack). 
  * PCI passthrough is not supported. 
  * SEV-ES & SEV-SNP are very experimental. 
  * EFI disks are not supported with SEV-SNP. 
  * With SEV-SNP, the reboot command inside a VM simply shuts down the VM. 


**Example Configuration (SEV):**

```
# qm set <vmid> -amd-sev type=std,no-debug=1,no-key-sharing=1,kernel-hashes=1
```

The **type** defines the encryption technology ("type=" is not necessary). Available options are std, es & snp.
The QEMU **policy** parameter gets calculated with the **no-debug** and **no-key-sharing** parameters. These parameters correspond to policy-bit 0 and 1. If **type** is **es** the policy-bit 2 is set to 1 so that SEV-ES is enabled. Policy-bit 3 (nosend) is always set to 1 to prevent migration-attacks. For more information on how to calculate the policy see: [AMD SEV API Specification Chapter 3](https://www.amd.com/system/files/TechDocs/55766_SEV-KM_API_Specification.pdf)
The **kernel-hashes** option is off per default for backward compatibility with older OVMF images and guests that do not measure the kernel/initrd. See <https://lists.gnu.org/archive/html/qemu-devel/2021-11/msg02598.html>
**Check if SEV is working in the VM**
Method 1 - dmesg:
Output should look like this.

```
# dmesg | grep -i sev
AMD Memory Encryption Features active: SEV
```

Method 2 - MSR 0xc0010131 (MSR_AMD64_SEV):
Output should be 1.

```
# apt install msr-tools
# modprobe msr
# rdmsr -a 0xc0010131
1
```

**Example Configuration (SEV-SNP):**

```
# qm set <vmid> -amd-sev type=snp,allow-smt=1,no-debug=1,kernel-hashes=1
```

The allow-smt policy-bit is set by default. If you disable it by setting allow-smt to 0, SMT must be disabled on the host in order for the VM to run.
**Check if SEV-SNP is working in the VM**

```
# dmesg | grep -i snp
Memory Encryption Features active: AMD SEV SEV-ES SEV-SNP
SEV: Using SNP CPUID table, 29 entries present.
SEV: SNP guest platform device initialized.
```

Links:
  * <https://developer.amd.com/sev/>
  * <https://github.com/AMDESE/AMDSEV>
  * <https://www.qemu.org/docs/master/system/i386/amd-memory-encryption.html>
  * <https://www.amd.com/system/files/TechDocs/55766_SEV-KM_API_Specification.pdf>
  * <https://documentation.suse.com/sles/15-SP1/html/SLES-amd-sev/index.html>
  * [ SEV Secure Nested Paging Firmware ABI Specification](https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/specifications/56860.pdf)


###  Network Device
Each VM can have many _Network interface controllers_ (NIC), of four different types:
  * **Intel E1000** is the default, and emulates an Intel Gigabit network card. 
  * the **VirtIO** paravirtualized NIC should be used if you aim for maximum performance. Like all VirtIO devices, the guest OS should have the proper driver installed. 
  * the **Realtek 8139** emulates an older 100 MB/s network card, and should only be used when emulating older operating systems ( released before 2002 ) 
  * the **vmxnet3** is another paravirtualized device, which should only be used when importing a VM from another hypervisor. 


Proxmox VE will generate for each NIC a random **MAC address** , so that your VM is addressable on Ethernet networks.
The NIC you added to the VM can follow one of two different models:
  * in the default **Bridged mode** each virtual NIC is backed on the host by a _tap device_ , ( a software loopback device simulating an Ethernet NIC ). This tap device is added to a bridge, by default vmbr0 in Proxmox VE. In this mode, VMs have direct access to the Ethernet LAN on which the host is located. 
  * in the alternative **NAT mode** , each virtual NIC will only communicate with the QEMU user networking stack, where a built-in router and DHCP server can provide network access. This built-in DHCP will serve addresses in the private 10.0.2.0/24 range. The NAT mode is much slower than the bridged mode, and should only be used for testing. This mode is only available via CLI or the API, but not via the web UI. 


You can also skip adding a network device when creating a VM by selecting **No network device**.
You can overwrite the **MTU** setting for each VM network device manually. Leaving the field empty or setting mtu=1 will inherit the MTU from the underlying bridge. This option is only available for **VirtIO** network devices.
Multiqueue
If you are using the VirtIO driver, you can optionally activate the **Multiqueue** option. This option allows the guest OS to process networking packets using multiple virtual CPUs, providing an increase in the total number of packets transferred.
When using the VirtIO driver with Proxmox VE, each NIC network queue is passed to the host kernel, where the queue will be processed by a kernel thread spawned by the vhost driver. With this option activated, it is possible to pass _multiple_ network queues to the host kernel for each NIC.
When using Multiqueue, it is recommended to set it to a value equal to the number of vCPUs of your guest. Remember that the number of vCPUs is the number of sockets times the number of cores configured for the VM. You also need to set the number of multi-purpose channels on each VirtIO NIC in the VM with this ethtool command:
ethtool -L ens1 combined X
where X is the number of the number of vCPUs of the VM.
To configure a Windows guest for Multiqueue install the [Redhat VirtIO Ethernet Adapter drivers](https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers), then adapt the NIC’s configuration as follows. Open the device manager, right click the NIC under "Network adapters", and select "Properties". Then open the "Advanced" tab and select "Receive Side Scaling" from the list on the left. Make sure it is set to "Enabled". Next, navigate to "Maximum number of RSS Queues" in the list and set it to the number of vCPUs of your VM. Once you verified that the settings are correct, click "OK" to confirm them.
You should note that setting the Multiqueue parameter to a value greater than one will increase the CPU load on the host and guest systems as the traffic increases. We recommend to set this option only when the VM has to process a great number of incoming connections, such as when the VM is running as a router, reverse proxy or a busy HTTP server doing long polling.
###  Display
QEMU can virtualize a few types of VGA hardware. Some examples are:
  * **std** , the default, emulates a card with Bochs VBE extensions. 
  * **cirrus** , this was once the default, it emulates a very old hardware module with all its problems. This display type should only be used if really necessary [<https://www.kraxel.org/blog/2014/10/qemu-using-cirrus-considered-harmful/> qemu: using cirrus considered harmful], for example, if using Windows XP or earlier 
  * **vmware** , is a VMWare SVGA-II compatible adapter. 
  * **qxl** , is the QXL paravirtualized graphics card. Selecting this also enables [SPICE](https://www.spice-space.org/) (a remote viewer protocol) for the VM. 
  * **virtio-gl** , often named VirGL is a virtual 3D GPU for use inside VMs that can offload workloads to the host GPU without requiring special (expensive) models and drivers and neither binding the host GPU completely, allowing reuse between multiple guests and or the host.   
| VirGL support needs some extra libraries that aren’t installed by default due to being relatively big and also not available as open source for all GPU models/vendors. For most setups you’ll just need to do: apt install libgl1 libegl1  |  
| --- |  


You can edit the amount of memory given to the virtual GPU, by setting the _memory_ option. This can enable higher resolutions inside the VM, especially with SPICE/QXL.
As the memory is reserved by display device, selecting Multi-Monitor mode for SPICE (such as qxl2 for dual monitors) has some implications:
  * Windows needs a device for each monitor, so if your _ostype_ is some version of Windows, Proxmox VE gives the VM an extra device per monitor. Each device gets the specified amount of memory. 
  * Linux VMs, can always enable more virtual monitors, but selecting a Multi-Monitor mode multiplies the memory given to the device with the number of monitors. 


Selecting serialX as display _type_ disables the VGA output, and redirects the Web Console to the selected serial port. A configured display _memory_ setting will be ignored in that case.
VNC clipboard
You can enable the VNC clipboard by setting clipboard to vnc.

```
# qm set <vmid> -vga <displaytype>,clipboard=vnc
```

In order to use the clipboard feature, you must first install the SPICE guest tools. On Debian-based distributions, this can be achieved by installing spice-vdagent. For other Operating Systems search for it in the official repositories or see: <https://www.spice-space.org/download.html>
Once you have installed the spice guest tools, you can use the VNC clipboard function (e.g. in the noVNC console panel). However, if you’re using SPICE, virtio or virgl, you’ll need to choose which clipboard to use. This is because the default **SPICE** clipboard will be replaced by the **VNC** clipboard, if clipboard is set to vnc.  
| In order to enable the VNC clipboard, QEMU is configured to use the qemu-vdagent device. Live migration support for this device was added with QEMU version 10.1. VMs running on a QEMU or machine version below 10.1 with an enabled VNC clipboard cannot be live-migrated.  |  
| --- |  
###  USB Passthrough
There are two different types of USB passthrough devices:
  * Host USB passthrough 
  * SPICE USB passthrough 


Host USB passthrough works by giving a VM a USB device of the host. This can either be done via the vendor- and product-id, or via the host bus and port.
The vendor/product-id looks like this: **0123:abcd** , where **0123** is the id of the vendor, and **abcd** is the id of the product, meaning two pieces of the same usb device have the same id.
The bus/port looks like this: **1-2.3.4** , where **1** is the bus and **2.3.4** is the port path. This represents the physical ports of your host (depending of the internal order of the usb controllers).
If a device is present in a VM configuration when the VM starts up, but the device is not present in the host, the VM can boot without problems. As soon as the device/port is available in the host, it gets passed through.  
| Using this kind of USB passthrough means that you cannot move a VM online to another host, since the hardware is only available on the host the VM is currently residing.  |  
| --- |  
The second type of passthrough is SPICE USB passthrough. If you add one or more SPICE USB ports to your VM, you can dynamically pass a local USB device from your SPICE client through to the VM. This can be useful to redirect an input device or hardware dongle temporarily.
It is also possible to map devices on a cluster level, so that they can be properly used with HA and hardware changes are detected and non root users can configure them. See [Resource Mapping](https://pve.proxmox.com/pve-docs/qm.1.html#resource_mapping) for details on that.
###  BIOS and UEFI
In order to properly emulate a computer, QEMU needs to use a firmware. Which, on common PCs often known as BIOS or (U)EFI, is executed as one of the first steps when booting a VM. It is responsible for doing basic hardware initialization and for providing an interface to the firmware and hardware for the operating system. By default QEMU uses **SeaBIOS** for this, which is an open-source, x86 BIOS implementation. SeaBIOS is a good choice for most standard setups.  
| SeaBIOS, and thus bios=seabios, is available for x86 guests only. On arm64 hosts, virtual machines always boot through UEFI, using the ARM build of OVMF (AAVMF), so bios=ovmf is the only supported setting there.  |  
| --- |  
Some operating systems (such as Windows 11) may require use of an UEFI compatible implementation. In such cases, you must use **OVMF** instead, which is an open-source UEFI implementation. [See the OVMF Project <https://github.com/tianocore/tianocore.github.io/wiki/OVMF>]
There are other scenarios in which the SeaBIOS may not be the ideal firmware to boot from, for example if you want to do VGA passthrough. [Alex Williamson has a good blog entry about this <https://vfio.blogspot.co.at/2014/08/primary-graphics-assignment-without-vga.html>]
If you want to use OVMF, there are several things to consider:
In order to save things like the **boot order** , there needs to be an EFI Disk. This disk will be included in backups and snapshots, and there can only be one.
You can create such a disk with the following command:

```
# qm set <vmid> -efidisk0 <storage>:1,format=<format>,efitype=4m,pre-enrolled-keys=1
```

Where **< storage>** is the storage where you want to have the disk, and **< format>** is a format which the storage supports. Alternatively, you can create such a disk through the web interface with _Add_ → _EFI Disk_ in the hardware section of a VM.
The **efitype** option specifies which version of the OVMF firmware should be used. For new VMs, this should always be _4m_ , as it supports Secure Boot and has more space allocated to support future development (this is the default in the GUI).
**pre-enroll-keys** specifies if the efidisk should come pre-loaded with distribution-specific and Microsoft Standard Secure Boot keys. It also enables Secure Boot by default (though it can still be disabled in the OVMF menu within the VM). See also [Secure Boot Certificate Expiration](https://pve.proxmox.com/pve-docs/qm.1.html#qm_secure_boot_ca_expiration).  
| If you want to start using Secure Boot in an existing VM (that still uses a _2m_ efidisk), you need to recreate the efidisk. To do so, delete the old one (qm set <vmid> -delete efidisk0) and add a new one as described above. This will reset any custom configurations you have made in the OVMF menu!  |  
| --- |  
When using OVMF with a virtual display (without VGA passthrough), you need to set the client resolution in the OVMF menu (which you can reach with a press of the ESC button during boot), or you have to choose SPICE as the display type.
When using OVMF with PXE boot, you have to add an [RNG device](https://pve.proxmox.com/pve-docs/qm.1.html#qm_virtio_rng) to the VM. For security reasons, the OVMF firmware disables PXE boot for guests without a random number generator.
#### Secure Boot Certificate Expiration 
The original set of Microsoft certificates from 2011, which Windows and common Linux distributions use for secure boot, expires in June 2026. Microsoft created replacement certificates in 2023 [Microsoft support article about the issue <https://support.microsoft.com/en-us/topic/windows-secure-boot-certificate-expiration-and-ca-updates-7ff40d33-95dc-4c3c-8725-a9b95457578e>].
The firmware only allows bootloaders signed with certificates present on the EFI disk. In particular, an EFI disk with only the 2011 certificates will reject bootloaders signed with the 2023 certificates. The ms-cert=2023k marker in the VM configuration for an EFI disk indicates that the new certificates are enrolled.
If the pve-edk2-firmware package version is at least 4.2025.05-1, newly created EFI disks contain both the 2011 and 2023 certificates and will have the ms-cert=2023k marker. For EFI disks created before that, you need to enroll the certificates:
For Windows with BitLocker, run the following command inside PowerShell:

```
manage-bde -protectors -disable <drive>
```

For example, <drive> could be C:. This is required for each drive with BitLocker before proceeding. Otherwise, you will be prompted for the BitLocker recovery key on the next boot!
Select the EFI disk in the _Hardware_ view in the UI and use _Disk Action > Enroll Updated Certificates_. Alternatively, enroll the certificates via the /nodes/{node}/qemu/{vmid}/config API endpoint. The enrollment takes effect when the VM is next started. The

```
qm enroll-efi-keys <vmid>
```

CLI command achieves the same, but requires the VM to be shut down.
For further steps on updating secure boot within Windows and signing the bootloader with the new 2023 certificates, refer to the Microsoft support articles about [enterprise deployment guidance for CVE-2023-24932](https://support.microsoft.com/en-us/topic/enterprise-deployment-guidance-for-cve-2023-24932-88b8f034-20b7-4a45-80cb-c6049b0f9967) and the [related security update](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-24932) which needs to be installed first.  
| The markers ms-cert=2023 and ms-cert=2023w may indicate partial enrollment. The VM start task log will warn about this. You should apply the enrollment procedure for such EFI disks too.  |  
| --- |  
###  Trusted Platform Module (TPM)
A **Trusted Platform Module** is a device which stores secret data - such as encryption keys - securely and provides tamper-resistance functions for validating system boot.
Certain operating systems (such as Windows 11) require such a device to be attached to a machine (be it physical or virtual).
A TPM is added by specifying a **tpmstate** volume. This works similar to an efidisk, in that it cannot be changed (only removed) once created. You can add one via the following command:

```
# qm set <vmid> -tpmstate0 <storage>:1,version=<version>
```

Where **< storage>** is the storage you want to put the state on, and **< version>** is either _v1.2_ or _v2.0_. You can also add one via the web interface, by choosing _Add_ → _TPM State_ in the hardware section of a VM.
The _v2.0_ TPM spec is newer and better supported, so unless you have a specific implementation that requires a _v1.2_ TPM, it should be preferred.  
| Compared to a physical TPM, an emulated one does **not** provide any real security benefits. The point of a TPM is that the data on it cannot be modified easily, except via commands specified as part of the TPM spec. Since with an emulated device the data storage happens on a regular volume, it can potentially be edited by anyone with access to it.  |  
| --- |  
###  Inter-VM shared memory
You can add an Inter-VM shared memory device (ivshmem), which allows one to share memory between the host and a guest, or also between multiple guests.
To add such a device, you can use qm:

```
# qm set <vmid> -ivshmem size=32,name=foo
```

Where the size is in MiB. The file will be located under /dev/shm/pve-shm-$name (the default name is the vmid).  
| Currently the device will get deleted as soon as any VM using it got shutdown or stopped. Open connections will still persist, but new connections to the exact same device cannot be made anymore.  |  
| --- |  
A use case for such a device is the Looking Glass [Looking Glass: <https://looking-glass.io/>] project, which enables high performance, low-latency display mirroring between host and guest.
###  Audio Device
To add an audio device run the following command:

```
qm set <vmid> -audio0 device=<device>
```

Supported audio devices are:
  * ich9-intel-hda: Intel HD Audio Controller, emulates ICH9 
  * intel-hda: Intel HD Audio Controller, emulates ICH6 
  * AC97: Audio Codec '97, useful for older operating systems like Windows XP 


There are two backends available:
  * _spice_
  * _none_


The _spice_ backend can be used in combination with [SPICE](https://pve.proxmox.com/pve-docs/qm.1.html#qm_display) while the _none_ backend can be useful if an audio device is needed in the VM for some software to work. To use the physical audio device of the host use device passthrough (see [PCI Passthrough](https://pve.proxmox.com/pve-docs/qm.1.html#qm_pci_passthrough) and [USB Passthrough](https://pve.proxmox.com/pve-docs/qm.1.html#qm_usb_passthrough)). Remote protocols like Microsoft’s RDP have options to play sound.
###  VirtIO RNG
A RNG (Random Number Generator) is a device providing entropy (_randomness_) to a system. A virtual hardware-RNG can be used to provide such entropy from the host system to a guest VM. This helps to avoid entropy starvation problems in the guest (a situation where not enough entropy is available and the system may slow down or run into problems), especially during the guests boot process.
To add a VirtIO-based emulated RNG, run the following command:

```
qm set <vmid> -rng0 source=<source>[,max_bytes=X,period=Y]
```

source specifies where entropy is read from on the host and has to be one of the following:
  * /dev/urandom: Non-blocking kernel entropy pool (preferred) 
  * /dev/random: Blocking kernel pool (not recommended, can lead to entropy starvation on the host system) 
  * /dev/hwrng: To pass through a hardware RNG attached to the host (if multiple are available, the one selected in /sys/devices/virtual/misc/hw_random/rng_current will be used) 


A limit can be specified via the max_bytes and period parameters, they are read as max_bytes per period in milliseconds. However, it does not represent a linear relationship: 1024B/1000ms would mean that up to 1 KiB of data becomes available on a 1 second timer, not that 1 KiB is streamed to the guest over the course of one second. Reducing the period can thus be used to inject entropy into the guest at a faster rate.
By default, the limit is set to 1024 bytes per 1000 ms (1 KiB/s). It is recommended to always use a limiter to avoid guests using too many host resources. If desired, a value of _0_ for max_bytes can be used to disable all limits.
###  Virtiofs
Virtiofs is a shared filesystem designed for virtual environments. It allows to share a directory tree available on the host by mounting it within VMs. It does not use the network stack and aims to offer similar performance and semantics as the source filesystem.
To use virtiofs, the [virtiofsd](https://gitlab.com/virtio-fs/virtiofsd) daemon needs to run in the background. This happens automatically in Proxmox VE when starting a VM using a virtiofs mount.
Linux VMs with kernel >=5.4 support virtiofs by default ([virtiofs kernel module](https://www.kernelconfig.io/CONFIG_VIRTIO_FS)), but some features require a newer kernel.
To use virtiofs, ensure that virtiofsd is installed on the Proxmox VE host:

```
apt install virtiofsd
```

There is a [guide](https://github.com/virtio-win/kvm-guest-drivers-windows/wiki/Virtiofs:-Shared-file-system) available on how to utilize virtiofs in Windows VMs.
#### Known Limitations 
  * If virtiofsd crashes, its mount point will hang in the VM until the VM is completely stopped. 
  * virtiofsd not responding may result in a hanging mount in the VM, similar to an unreachable NFS. 
  * Memory hotplug does not work in combination with virtiofs (also results in hanging access). 
  * Memory related features such as live migration, snapshots, and hibernate are not available with virtiofs devices. 
  * Windows cannot understand ACLs in the context of virtiofs. Therefore, do not expose ACLs for Windows VMs, otherwise the virtiofs device will not be visible within the VM. 


#### Add Mapping for Shared Directories 
To add a mapping for a shared directory, you can use the API directly with pvesh as described in the [Resource Mapping](https://pve.proxmox.com/pve-docs/qm.1.html#resource_mapping) section:

```
pvesh create /cluster/mapping/dir --id dir1 \
    --map node=node1,path=/path/to/share1 \
    --map node=node2,path=/path/to/share2 \
```

#### Add virtiofs to a VM 
To share a directory using virtiofs, add the parameter virtiofs<N> (N can be anything between 0 and 9) to the VM config and use a directory ID (dirid) that has been configured in the resource mapping. Additionally, you can set the cache option to either always, never, metadata, or auto (default: auto), depending on your requirements. How the different caching modes behave can be read [here under the "Caching Modes" section](https://lwn.net/Articles/774495/).
The virtiofsd supports ACL and xattr passthrough (can be enabled with the expose-acl and expose-xattr options), allowing the guest to access ACLs and xattrs if the underlying host filesystem supports them, but they must also be compatible with the guest filesystem (for example most Linux filesystems support ACLs, while Windows filesystems do not).
The expose-acl option automatically implies expose-xattr, that is, it makes no difference if you set expose-xattr to 0 if expose-acl is set to 1.
If you want virtiofs to honor the O_DIRECT flag, you can set the direct-io parameter to 1 (default: 0). This will degrade performance, but is useful if applications do their own caching.

```
qm set <vmid> -virtiofs0 dirid=<dirid>,cache=always,direct-io=1
qm set <vmid> -virtiofs1 <dirid>,cache=never,expose-xattr=1
qm set <vmid> -virtiofs2 <dirid>,expose-acl=1
```

To temporarily mount virtiofs in a guest VM with the Linux kernel virtiofs driver, run the following command inside the guest:

```
mount -t virtiofs <dirid> <mount point>
```

To have a persistent virtiofs mount, you can create an fstab entry:

```
<dirid> <mount point> virtiofs rw,relatime 0 0
```

The dirid associated with the path on the current node is also used as the mount tag (name used to mount the device on the guest).
For more information on available virtiofsd parameters, see the [GitLab virtiofsd project page](https://gitlab.com/virtio-fs/virtiofsd).
###  Device Boot Order
QEMU can tell the guest which devices it should boot from, and in which order. This can be specified in the config via the boot property, for example:

```
boot: order=scsi0;net0;hostpci0
```

This way, the guest would first attempt to boot from the disk scsi0, if that fails, it would go on to attempt network boot from net0, and in case that fails too, finally attempt to boot from a passed through PCIe device (seen as disk in case of NVMe, otherwise tries to launch into an option ROM).
On the GUI you can use a drag-and-drop editor to specify the boot order, and use the checkbox to enable or disable certain devices for booting altogether.  
| If your guest uses multiple disks to boot the OS or load the bootloader, all of them must be marked as _bootable_ (that is, they must have the checkbox enabled or appear in the list in the config) for the guest to be able to boot. This is because recent SeaBIOS and OVMF versions only initialize disks if they are marked _bootable_.  |  
| --- |  
In any case, even devices not appearing in the list or having the checkmark disabled will still be available to the guest, once it’s operating system has booted and initialized them. The _bootable_ flag only affects the guest BIOS and bootloader.
###  Automatic Start and Shutdown of Virtual Machines
After creating your VMs, you probably want them to start automatically when the host system boots. For this you need to select the option _Start at boot_ from the _Options_ Tab of your VM in the web interface, or set it with the following command:

```
# qm set <vmid> -onboot 1
```

Start and Shutdown Order
In some case you want to be able to fine tune the boot order of your VMs, for instance if one of your VM is providing firewalling or DHCP to other guest systems. For this you can use the following parameters:
  * **Start/Shutdown order** : Defines the start order priority. For example, set it to 1 if you want the VM to be the first to be started. (We use the reverse startup order for shutdown, so a machine with a start order of 1 would be the last to be shut down). If multiple VMs have the same order defined on a host, they will additionally be ordered by _VMID_ in ascending order. 
  * **Startup delay** : Defines the interval between this VM start and subsequent VMs starts. For example, set it to 240 if you want to wait 240 seconds before starting other VMs. 
  * **Shutdown timeout** : Defines the duration in seconds Proxmox VE should wait for the VM to be offline after issuing a shutdown command. By default this value is set to 180, which means that Proxmox VE will issue a shutdown request and wait 180 seconds for the machine to be offline. If the machine is still online after the timeout it will be stopped forcefully. 

  
| VMs managed by the HA stack do not follow the _start on boot_ and _boot order_ options currently. Those VMs will be skipped by the startup and shutdown algorithm as the HA manager itself ensures that VMs get started and stopped.  |  
| --- |  
Please note that machines without a Start/Shutdown order parameter will always start after those where the parameter is set. Further, this parameter can only be enforced between virtual machines running on the same host, not cluster-wide.
If you require a delay between the host boot and the booting of the first VM, see the section on Proxmox VE Node Management.
###  QEMU Guest Agent
The QEMU Guest Agent is a service which runs inside the VM, providing a communication channel between the host and the guest. It is used to exchange information and allows the host to issue commands to the guest.
For example, the IP addresses in the VM summary panel are fetched via the guest agent.
Or when starting a backup, the guest is told via the guest agent to sync outstanding writes via the guest-fsfreeze-freeze and guest-fsfreeze-thaw commands.
For the guest agent to work properly the following steps must be taken:
  * install the agent in the guest and make sure it is running 
  * enable the communication via the agent in Proxmox VE 


#### Install Guest Agent 
For most Linux distributions, the guest agent is available. The package is usually named qemu-guest-agent.
For Windows, see our [Windows VirtIO Drivers](https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers) article for more information on how to acquire and install the drivers.
#### Enable Guest Agent Communication 
Communication from Proxmox VE with the guest agent can be enabled in the VM’s **Options** panel. A fresh start of the VM is necessary for the changes to take effect.
#### Automatic TRIM Using QGA 
It is possible to enable the _Run guest-trim_ option. With this enabled, Proxmox VE will issue a trim command to the guest after the following operations that have the potential to write out zeros to the storage:
  * moving a disk to another storage 
  * live migrating a VM to another node with local storage 


On a thin provisioned storage, this can help to free up unused space.  
| There is a caveat with ext4 on Linux, because it uses an in-memory optimization to avoid issuing duplicate TRIM requests. Since the guest doesn’t know about the change in the underlying storage, only the first guest-trim will run as expected. Subsequent ones, until the next reboot, will only consider parts of the filesystem that changed since then.  |  
| --- |  
#### Filesystem Freeze & Thaw 
By default, if the QEMU Guest Agent is enabled in the guest’s config and if the agent is available inside of the guest, then the virtual machine’s filesystems are synced via the guest-fsfreeze-freeze QEMU Guest Agent command when certain operations are performed. This is done to provide data consistency.
See the [QEMU Guest Agent Protocol Reference](https://www.qemu.org/docs/master/interop/qemu-ga-ref.html) for more details.
A freeze will be issued for any of the following operations on a VM:
  * Performing a backup in snapshot mode 
  * Creating a clone of a VM while it is running 
  * Replicating a VM while it is running 
  * Taking a snapshot without RAM of a running VM 
  * Importing a disk image from a running guest will issue a freeze for that running guest 


On Windows guests, some applications might handle consistent backups themselves by hooking into the Windows VSS (Volume Shadow Copy Service) layer, a freeze then might interfere with that. For example, it has been observed that calling guest-fsfreeze-freeze with some SQL Servers triggers VSS to call the SQL Writer VSS module in a mode that breaks the SQL Server backup chain for differential backups.
There are two options on how to handle such a situation.
  1. Configure the QEMU Guest Agent to use a different VSS variant that does not interfere with other VSS users. The [Proxmox VE wiki](https://pve.proxmox.com/wiki/VM_Backup_Consistency) has more details. 
  2. Alternatively, you can configure Proxmox VE to not issue a freeze-and-thaw cycle by disabling the freeze-fs guest agent option. This can also be done in the GUI: open the _Options_ panel of the virtual machine, then the _QEMU Guest Agent_ dialog, and disable the _Freeze/thaw guest filesystems during certain operations for consistency_ option.   
| Disabling this option can potentially lead to backups with inconsistent filesystems. Therefore, adapting the QEMU Guest Agent configuration in the guest is the preferred option.  |  
| --- |  


#### Troubleshooting 
VM does not shut down
Make sure the guest agent is installed and running.
Once the guest agent is enabled, Proxmox VE will send power commands like _shutdown_ via the guest agent. If the guest agent is not running, commands cannot get executed properly and the shutdown command will run into a timeout.
###  SPICE Enhancements
SPICE Enhancements are optional features that can improve the remote viewer experience.
To enable them via the GUI go to the **Options** panel of the virtual machine. Run the following command to enable them via the CLI:

```
qm set <vmid> -spice_enhancements foldersharing=1,videostreaming=all
```
  
| To use these features the [**Display**](https://pve.proxmox.com/pve-docs/qm.1.html#qm_display) of the virtual machine must be set to SPICE (qxl).  |  
| --- |  
#### Folder Sharing 
Share a local folder with the guest. The spice-webdavd daemon needs to be installed in the guest. It makes the shared folder available through a local WebDAV server located at <http://localhost:9843>.
For Windows guests the installer for the _Spice WebDAV daemon_ can be downloaded from the [official SPICE website](https://www.spice-space.org/download.html#windows-binaries).
Most Linux distributions have a package called spice-webdavd that can be installed.
To share a folder in Virt-Viewer (Remote Viewer) go to _File → Preferences_. Select the folder to share and then enable the checkbox.  
| Folder sharing currently only works in the Linux version of Virt-Viewer.  |  
| --- |  
| Experimental! Currently this feature does not work reliably.  |  
| --- |  
#### Video Streaming 
Fast refreshing areas are encoded into a video stream. Two options exist:
  * **all** : Any fast refreshing area will be encoded into a video stream. 
  * **filter** : Additional filters are used to decide if video streaming should be used (currently only small window surfaces are skipped). 


A general recommendation if video streaming should be enabled and which option to choose from cannot be given. Your mileage may vary depending on the specific circumstances.
#### Troubleshooting 
Shared folder does not show up
Make sure the WebDAV service is enabled and running in the guest. On Windows it is called _Spice webdav proxy_. In Linux the name is _spice-webdavd_ but can be different depending on the distribution.
If the service is running, check the WebDAV server by opening <http://localhost:9843> in a browser in the guest.
It can help to restart the SPICE session.
##  Migration 
If you have a cluster, you can migrate your VM to another host with

```
# qm migrate <vmid> <target>
```

There are generally two mechanisms for this
  * Online Migration (aka Live Migration) 
  * Offline Migration 


###  Online Migration
If your VM is running and no locally bound resources are configured (such as devices that are passed through), you can initiate a live migration with the --online flag in the qm migration command evocation. The web interface defaults to live migration when the VM is running.  
| Live migration is only possible between hosts of the same CPU architecture. A running guest’s CPU state cannot be transferred between an x86 and an arm64 host.  |  
| --- |  
#### How it works 
Online migration first starts a new QEMU process on the target host with the _incoming_ flag, which performs only basic initialization with the guest vCPUs still paused and then waits for the guest memory and device state data streams of the source Virtual Machine. All other resources, such as disks, are either shared or got already sent before runtime state migration of the VMs begins; so only the memory content and device state remain to be transferred.
Once this connection is established, the source begins asynchronously sending the memory content to the target. If the guest memory on the source changes, those sections are marked dirty and another pass is made to send the guest memory data. This loop is repeated until the data difference between running source VM and incoming target VM is small enough to be sent in a few milliseconds, because then the source VM can be paused completely, without a user or program noticing the pause, so that the remaining data can be sent to the target, and then unpause the targets VM’s CPU to make it the new running VM in well under a second.
#### Requirements 
For Live Migration to work, there are some things required:
  * The VM has no local resources that cannot be migrated. For example, PCI or USB devices that are passed through currently block live-migration. Local Disks, on the other hand, can be migrated by sending them to the target just fine. 
  * The hosts are located in the same Proxmox VE cluster. 
  * The hosts have a working (and reliable) network connection between them. 
  * The target host must have the same, or higher versions of the Proxmox VE packages. Although it can sometimes work the other way around, this cannot be guaranteed. 
  * The hosts have CPUs from the same vendor with similar capabilities. Different vendor **might** work depending on the actual models and VMs CPU type configured, but it cannot be guaranteed - so please test before deploying such a setup in production. 


#### Conntrack State Migration   
| Conntrack state migration is considered best-effort only and might not work, as it heavily depends on the network setup. For example, setups using source address masquerading (SNAT) on the host will most likely **not** work.  |  
| --- |  
Conntrack is a Linux kernel mechanism to enable a stateful firewall by tracking individual connection. When live migrating running VMs, active in- and/or outbound connections **might** get interrupted as soon as the VM starts running on the target host, as the new host node does not have the same conntrack entries and thus the firewall can drop packets.
Conntrack state migration copies all conntrack entries on the host for the live-migrated VM to the target node and afterwards flushes the migrated entries from the conntrack table on the source node.
###  Offline Migration
If you have local resources, you can still migrate your VMs offline as long as all disk are on storage defined on both hosts. Migration then copies the disks to the target host over the network, as with online migration. Note that any hardware passthrough configuration may need to be adapted to the device location on the target host.
##  Copies and Clones 
VM installation is usually done using an installation media (CD-ROM) from the operating system vendor. Depending on the OS, this can be a time consuming task one might want to avoid.
An easy way to deploy many VMs of the same type is to copy an existing VM. We use the term _clone_ for such copies, and distinguish between _linked_ and _full_ clones. 

Full Clone 
    
The result of such copy is an independent VM. The new VM does not share any storage resources with the original. 
It is possible to select a **Target Storage** , so one can use this to migrate a VM to a totally different storage. You can also change the disk image **Format** if the storage driver supports several formats.  
| A full clone needs to read and copy all VM image data. This is usually much slower than creating a linked clone.  |  
| --- |  
Some storage types allows to copy a specific **Snapshot** , which defaults to the _current_ VM data. This also means that the final copy never includes any additional snapshots from the original VM. 

Linked Clone 
    
Modern storage drivers support a way to generate fast linked clones. Such a clone is a writable copy whose initial contents are the same as the original data. Creating a linked clone is nearly instantaneous, and initially consumes no additional space. 
They are called _linked_ because the new image still refers to the original. Unmodified data blocks are read from the original image, but modification are written (and afterwards read) from a new location. This technique is called _Copy-on-write_.
This requires that the original volume is read-only. With Proxmox VE one can convert any VM into a read-only [ Template](https://pve.proxmox.com/pve-docs/qm.1.html#qm_templates)). Such templates can later be used to create linked clones efficiently.  
| You cannot delete an original template while linked clones exist.  |  
| --- |  
It is not possible to change the **Target storage** for linked clones, because this is a storage internal feature.
The **Target node** option allows you to create the new VM on a different node. The only restriction is that the VM is on shared storage, and that storage is also available on the target node.
To avoid resource conflicts, all network interface MAC addresses get randomized, and we generate a new _UUID_ for the VM BIOS (smbios1) setting.
##  Virtual Machine Templates 
One can convert a VM into a Template. Such templates are read-only, and you can use them to create linked clones.  
| It is not possible to start templates, because this would modify the disk images. If you want to change the template, create a linked clone and modify that.  |  
| --- |  
##  VM Generation ID 
Proxmox VE supports Virtual Machine Generation ID (_vmgenid_) [Official _vmgenid_ Specification <https://docs.microsoft.com/en-us/windows/desktop/hyperv_v2/virtual-machine-generation-identifier>] for virtual machines. This can be used by the guest operating system to detect any event resulting in a time shift event, for example, restoring a backup or a snapshot rollback.
When creating new VMs, a _vmgenid_ will be automatically generated and saved in its configuration file.
To create and add a _vmgenid_ to an already existing VM one can pass the special value ‘1’ to let Proxmox VE autogenerate one or manually set the _UUID_ [Online GUID generator <http://guid.one/>] by using it as value, for example:

```
# qm set VMID -vmgenid 1
# qm set VMID -vmgenid 00000000-0000-0000-0000-000000000000
```
  
| The initial addition of a _vmgenid_ device to an existing VM, may result in the same effects as a change on snapshot rollback, backup restore, etc., has as the VM can interpret this as generation change.  |  
| --- |  
In the rare case the _vmgenid_ mechanism is not wanted one can pass ‘0’ for its value on VM creation, or retroactively delete the property in the configuration with:

```
# qm set VMID -delete vmgenid
```

The most prominent use case for _vmgenid_ are newer Microsoft Windows operating systems, which use it to avoid problems in time sensitive or replicate services (such as databases or domain controller [<https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/virtualized-domain-controller-architecture>]) on snapshot rollback, backup restore or a whole VM clone operation.
##  Importing Virtual Machines 
Importing existing virtual machines from foreign hypervisors or other Proxmox VE clusters can be achieved through various methods, the most common ones are:
  * Using the native import wizard, which utilizes the _import_ content type, such as provided by the ESXi special storage. 
  * Performing a backup on the source and then restoring on the target. This method works best when migrating from another Proxmox VE instance. 
  * using the OVF-specific import command of the qm command-line tool. 


If you import VMs to Proxmox VE from other hypervisors, it’s recommended to familiarize yourself with the [concepts of Proxmox VE](https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE#Concepts).
###  Import Wizard
Proxmox VE provides an integrated VM importer using the storage plugin system for native integration into the API and web-based user interface. You can use this to import the VM as a whole, with most of its config mapped to Proxmox VE’s config model and reduced downtime.  
| The import wizard was added during the Proxmox VE 8.2 development cycle and is in tech preview state. While it’s already promising and working stable, it’s still under active development.  |  
| --- |  
To use the import wizard you have to first set up a new storage for an import source, you can do so on the web-interface under _Datacenter → Storage → Add_.
Then you can select the new storage in the resource tree and use the _Virtual Guests_ content tab to see all available guests that can be imported.
Select one and use the _Import_ button (or double-click) to open the import wizard. You can modify a subset of the available options here and then start the import. Please note that you can do more advanced modifications after the import finished.  
| The ESXi import wizard has been tested with ESXi versions 6.5 through 8.0. Note that guests using vSAN storage cannot be directly imported directly; their disks must first be moved to another storage. While it is possible to use a vCenter as the import source, performance is dramatically degraded (5 to 10 times slower).  |  
| --- |  
For a step-by-step guide and tips for how to adapt the virtual guest to the new hyper-visor see our [migrate to Proxmox VE wiki article](https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE#Migration).
#### OVA/OVF Import 
To import OVA/OVF files, you first need a File-based storage with the _import_ content type. On this storage, there will be an _import_ folder where you can put OVA files or OVF files with the corresponding images in a flat structure. Alternatively you can use the web UI to upload or download OVA files directly. You can then use the web UI to select those and use the import wizard to import the guests.
For OVA files, there is additional space needed to temporarily extract the image. This needs a file-based storage that has the _images_ content type configured. By default the source storage is selected for this, but you can specify a _Import Working Storage_ on which the images will be extracted before importing to the actual target storage.  
| Since OVA/OVF file structure and content are not always well maintained or defined, it might be necessary to adapt some guest settings manually. For example the SCSI controller type is almost never defined in OVA/OVF files, but the default is unbootable with OVMF (UEFI), so you should select _Virtio SCSI_ or _VMware PVSCSI_ for these cases.  |  
| --- |  
###  Import OVF/OVA Through CLI
A VM export from a foreign hypervisor takes usually the form of one or more disk images, with a configuration file describing the settings of the VM (RAM, number of cores). The disk images can be in the vmdk format, if the disks come from VMware or VirtualBox, or qcow2 if the disks come from a KVM hypervisor. The most popular configuration format for VM exports is the OVF standard, but in practice interoperation is limited because many settings are not implemented in the standard itself, and hypervisors export the supplementary information in non-standard extensions.
Besides the problem of format, importing disk images from other hypervisors may fail if the emulated hardware changes too much from one hypervisor to another. Windows VMs are particularly concerned by this, as the OS is very picky about any changes of hardware. This problem may be solved by installing the MergeIDE.zip utility available from the Internet before exporting and choosing a hard disk type of **IDE** before booting the imported Windows VM.
Finally there is the question of paravirtualized drivers, which improve the speed of the emulated system and are specific to the hypervisor. GNU/Linux and other free Unix OSes have all the necessary drivers installed by default and you can switch to the paravirtualized drivers right after importing the VM. For Windows VMs, you need to install the Windows paravirtualized drivers by yourself.
GNU/Linux and other free Unix can usually be imported without hassle. Note that we cannot guarantee a successful import/export of Windows VMs in all cases due to the problems above.
#### Step-by-step example of a Windows OVF import 
Microsoft provides [Virtual Machines downloads](https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/) to get started with Windows development.We are going to use one of these to demonstrate the OVF import feature.
##### Download the Virtual Machine zip 
After getting informed about the user agreement, choose the _Windows 10 Enterprise (Evaluation - Build)_ for the VMware platform, and download the zip.
##### Extract the disk image from the zip 
Using the unzip utility or any archiver of your choice, unpack the zip, and copy via ssh/scp the ovf and vmdk files to your Proxmox VE host.
##### Import the Virtual Machine 
This will create a new virtual machine, using cores, memory and VM name as read from the OVF manifest, and import the disks to the local-lvm storage. You have to configure the network manually.

```
# qm importovf 999 WinDev1709Eval.ovf local-lvm
```

The VM is ready to be started.
##### Adding an external disk image to a Virtual Machine 
You can also add an existing disk image to a VM, either coming from a foreign hypervisor, or one that you created yourself.
Suppose you created a Debian/Ubuntu disk image with the _vmdebootstrap_ tool:

```
vmdebootstrap --verbose \
 --size 10GiB --serial-console \
 --grub --no-extlinux \
 --package openssh-server \
 --package avahi-daemon \
 --package qemu-guest-agent \
 --hostname vm600 --enable-dhcp \
 --customize=./copy_pub_ssh.sh \
 --sparse --image vm600.raw
```

You can now create a new target VM, importing the image to the storage pvedir and attaching it to the VM’s SCSI controller:

```
# qm create 600 --net0 virtio,bridge=vmbr0 --name vm600 --serial0 socket \
   --boot order=scsi0 --scsihw virtio-scsi-pci --ostype l26 \
   --scsi0 pvedir:0,import-from=/path/to/dir/vm600.raw
```

The VM is ready to be started.
##  Cloud-Init Support 
[Cloud-Init](https://cloudinit.readthedocs.io) is the de facto multi-distribution package that handles early initialization of a virtual machine instance. Using Cloud-Init, configuration of network devices and ssh keys on the hypervisor side is possible. When the VM starts for the first time, the Cloud-Init software inside the VM will apply those settings.
Many Linux distributions provide ready-to-use Cloud-Init images, mostly designed for _OpenStack_. These images will also work with Proxmox VE. While it may seem convenient to get such ready-to-use images, we usually recommended to prepare the images by yourself. The advantage is that you will know exactly what you have installed, and this helps you later to easily customize the image for your needs.
Once you have created such a Cloud-Init image we recommend to convert it into a VM template. From a VM template you can quickly create linked clones, so this is a fast method to roll out new VM instances. You just need to configure the network (and maybe the ssh keys) before you start the new VM.
We recommend using SSH key-based authentication to login to the VMs provisioned by Cloud-Init. It is also possible to set a password, but this is not as safe as using SSH key-based authentication because Proxmox VE needs to store an encrypted version of that password inside the Cloud-Init data.
Proxmox VE generates an ISO image to pass the Cloud-Init data to the VM. For that purpose, all Cloud-Init VMs need to have an assigned CD-ROM drive. Usually, a serial console should be added and used as a display. Many Cloud-Init images rely on this, it is a requirement for OpenStack. However, other images might have problems with this configuration. Switch back to the default display configuration if using a serial console doesn’t work.
###  Preparing Cloud-Init Templates
The first step is to prepare your VM. Basically you can use any VM. Simply install the Cloud-Init packages **inside the VM** that you want to prepare. On Debian/Ubuntu based systems this is as simple as:

```
apt-get install cloud-init
```
  
| This command is **not** intended to be executed on the Proxmox VE host, but only inside the VM.  |  
| --- |  
Already many distributions provide ready-to-use Cloud-Init images (provided as .qcow2 files), so alternatively you can simply download and import such images. For the following example, we will use the cloud image provided by Ubuntu at <https://cloud-images.ubuntu.com>.

```
# download the image
wget https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img

# create a new VM with VirtIO SCSI controller
qm create 9000 --memory 2048 --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-pci

# import the downloaded disk to the local-lvm storage, attaching it as a SCSI drive
qm set 9000 --scsi0 local-lvm:0,import-from=/path/to/bionic-server-cloudimg-amd64.img
```
  
| Ubuntu Cloud-Init images require the virtio-scsi-pci controller type for SCSI drives.  |  
| --- |  
Add Cloud-Init CD-ROM drive
The next step is to configure a CD-ROM drive, which will be used to pass the Cloud-Init data to the VM.

```
qm set 9000 --ide2 local-lvm:cloudinit
```

To be able to boot directly from the Cloud-Init image, set the boot parameter to order=scsi0 to restrict BIOS to boot from this disk only. This will speed up booting, because VM BIOS skips the testing for a bootable CD-ROM.

```
qm set 9000 --boot order=scsi0
```

For many Cloud-Init images, it is required to configure a serial console and use it as a display. If the configuration doesn’t work for a given image however, switch back to the default display instead.

```
qm set 9000 --serial0 socket --vga serial0
```

In a last step, it is helpful to convert the VM into a template. From this template you can then quickly create linked clones. The deployment from VM templates is much faster than creating a full clone (copy).

```
qm template 9000
```

###  Deploying Cloud-Init Templates
You can easily deploy such a template by cloning:

```
qm clone 9000 123 --name ubuntu2
```

Then configure the SSH public key used for authentication, and configure the IP setup:

```
qm set 123 --sshkey ~/.ssh/id_rsa.pub
qm set 123 --ipconfig0 ip=10.0.10.123/24,gw=10.0.10.1
```

You can also configure all the Cloud-Init options using a single command only. We have simply split the above example to separate the commands for reducing the line length. Also make sure to adopt the IP setup for your specific environment.
###  Custom Cloud-Init Configuration
The Cloud-Init integration also allows custom config files to be used instead of the automatically generated configs. This is done via the cicustom option on the command line:

```
qm set 9000 --cicustom "user=<volume>,network=<volume>,meta=<volume>"
```

The custom config files have to be on a storage that supports snippets and have to be available on all nodes the VM is going to be migrated to. Otherwise the VM won’t be able to start. For example:

```
qm set 9000 --cicustom "user=local:snippets/userconfig.yaml"
```

There are three kinds of configs for Cloud-Init. The first one is the user config as seen in the example above. The second is the network config and the third the meta config. They can all be specified together or mixed and matched however needed. The automatically generated config will be used for any that don’t have a custom config file specified.
The generated config can be dumped to serve as a base for custom configs:

```
qm cloudinit dump 9000 user
```

The same command exists for network and meta.
###  Cloud-Init on Windows
There is a reimplementation of Cloud-Init available for Windows called [cloudbase-init](https://cloudbase.it/). Not every feature of Cloud-Init is available with Cloudbase-Init, and some features differ compared to Cloud-Init.
Cloudbase-Init requires both ostype set to any Windows version and the citype set to configdrive2, which is the default with any Windows ostype.
There are no ready-made cloud images for Windows available for free. Using Cloudbase-Init requires manually installing and configuring a Windows guest.
###  Preparing Cloudbase-Init Templates
The first step is to install Windows in a VM. Download and install Cloudbase-Init in the guest. It may be necessary to install the Beta version. Don’t run Sysprep at the end of the installation. Instead configure Cloudbase-Init first.
A few common options to set would be:
  * _username_ : This sets the username of the administrator 
  * _groups_ : This allows one to add the user to the Administrators group 
  * _inject_user_password_ : Set this to true to allow setting the password in the VM config 
  * _first_logon_behaviour_ : Set this to no to not require a new password on login 
  * _rename_admin_user_ : Set this to true to allow renaming the default Administrator user to the username specified with username
  * _metadata_services_ : Set this to cloudbaseinit.metadata.services.configdrive.ConfigDriveService for Cloudbase-Init to first check this service. Otherwise it may take a few minutes for Cloudbase-Init to configure the system after boot. 


Some plugins, for example the SetHostnamePlugin, require reboots and will do so automatically. To disable automatic reboots by Cloudbase-Init, you can set allow_reboot to false.
A full set of configuration options can be found in the [official cloudbase-init documentation](https://cloudbase-init.readthedocs.io/en/latest/config.html).
It can make sense to make a snapshot after configuring in case some parts of the config still need adjustments. After configuring Cloudbase-Init you can start creating the template. Shutdown the Windows guest, add a Cloud-Init disk and make it into a template.

```
qm set 9000 --ide2 local-lvm:cloudinit
qm template 9000
```

Clone the template into a new VM:

```
qm clone 9000 123 --name windows123
```

Then set the password, network config and SSH key:

```
qm set 123 --cipassword <password>
qm set 123 --ipconfig0 ip=10.0.10.123/24,gw=10.0.10.1
qm set 123 --sshkey ~/.ssh/id_rsa.pub
```

Make sure that the ostype is set to any Windows version before setting the password. Otherwise the password will be encrypted and Cloudbase-Init will use the encrypted password as plaintext password.
When everything is set, start the cloned guest. On the first boot the login won’t work and it will reboot automatically for the changed hostname. After the reboot the new password should be set and login should work.
###  Cloudbase-Init and Sysprep
Sysprep is a feature to reset the configuration of Windows and provide a new system. This can be used in conjunction with Cloudbase-Init to create a clean template.
When using Sysprep there are 2 configuration files that need to be adapted. The first one is the normal configuration file, the second one is the one ending in -unattend.conf.
Cloudbase-Init runs in 2 steps, first the Sysprep step using the -unattend.conf and then the regular step using the primary config file.
For Windows Server running Sysprep with the provided Unattend.xml file should work out of the box. Normal Windows versions however require additional steps:
  1. Open a PowerShell instance 
  2. Enable the Administrator user: 

```
net user Administrator /active:yes`
```

  3. Install Cloudbase-Init using the Administrator user 
  4. Modify Unattend.xml to include the command to enable the Administrator user on the first boot after sysprepping: 

```
<RunSynchronousCommand wcm:action="add">
  <Path>net user administrator /active:yes</Path>
  <Order>1</Order>
  <Description>Enable Administrator User</Description>
</RunSynchronousCommand>
```

Make sure the <Order> does not conflict with other synchronous commands. Modify <Order> of the Cloudbase-Init command to run after this one by increasing the number to a higher value: <Order>2</Order>
  5. (Windows 11 only) Remove the conflicting Microsoft.OneDriveSync package: 

```
Get-AppxPackage -AllUsers Microsoft.OneDriveSync | Remove-AppxPackage -AllUsers
```

  6. cd into the Cloudbase-Init config directory: 

```
cd 'C:\Program Files\Cloudbase Solutions\Cloudbase-Init\conf'
```

  7. (optional) Create a snapshot of the VM before Sysprep in case of a misconfiguration 
  8. Run Sysprep: 

```
C:\Windows\System32\Sysprep\sysprep.exe /generalize /oobe /unattend:Unattend.xml
```



After following the above steps the VM should be in shut down state due to the Sysprep. Now you can make it into a template, clone it and configure it as needed.
###  Cloud-Init specific Options 

cicustom: [meta=<volume>] [,network=<volume>] [,user=<volume>] [,vendor=<volume>] 
    
Specify custom files to replace the automatically generated ones at start.  

meta=<volume> 
    
Specify a custom file containing all meta data passed to the VM via cloud-init. This is provider specific meaning configdrive2 and nocloud differ.  

network=<volume> 
    
To pass a custom file containing all network data to the VM via cloud-init.  

user=<volume> 
    
To pass a custom file containing all user data to the VM via cloud-init.  

vendor=<volume> 
    
To pass a custom file containing all vendor data to the VM via cloud-init.  

cipassword: <string> 
    
Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.  

citype: <configdrive2 | nocloud | opennebula> 
    
Specifies the cloud-init configuration format. The default depends on the configured operating system type (ostype. We use the nocloud format for Linux, and configdrive2 for windows.  

ciupgrade: <boolean> (_default =_ 1) 
    
do an automatic package upgrade after the first boot.  

ciuser: <string> 
    
User name to change ssh keys and password for instead of the image’s configured default user.  

ipconfig[n]: [gw=<GatewayIPv4>] [,gw6=<GatewayIPv6>] [,ip=<IPv4Format/CIDR>] [,ip6=<IPv6Format/CIDR>] 
    
Specify IP addresses and gateways for the corresponding interface. 
IP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.
The special string _dhcp_ can be used for IP addresses to use DHCP, in which case no explicit gateway should be provided. For IPv6 the special string _auto_ can be used to use stateless autoconfiguration. This requires cloud-init 19.4 or newer.
If cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using dhcp on IPv4. 

gw=<GatewayIPv4> 
    
Default gateway for IPv4 traffic.   
| Requires option(s): ip  |  
| --- | 

gw6=<GatewayIPv6> 
      
Default gateway for IPv6 traffic.   
| Requires option(s): ip6  |  
| --- | 

ip=<IPv4Format/CIDR> (_default =_ dhcp) 
      
IPv4 address in CIDR format.  

ip6=<IPv6Format/CIDR> (_default =_ dhcp) 
    
IPv6 address in CIDR format.  

nameserver: <string> 
    
Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.  

searchdomain: <string> 
    
Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.  

sshkeys: <string> 
    
Setup public SSH keys (one key per line, OpenSSH format). 
##  PCI(e) Passthrough 
PCI(e) passthrough is a mechanism to give a virtual machine control over a PCI device from the host. This can have some advantages over using virtualized hardware, for example lower latency, higher performance, or more features (e.g., offloading).
But, if you pass through a device to a virtual machine, you cannot use that device anymore on the host or in any other VM.
Note that, while PCI passthrough is available for i440fx and q35 machines, PCIe passthrough is only available on q35 machines. This does not mean that PCIe-capable devices that are passed through as PCI devices will only run at PCI speeds. Passing through devices as PCIe just sets a flag for the guest to tell it that the device is a PCIe device instead of a "really fast legacy PCI device". Some guest applications benefit from this.
###  General Requirements
Since passthrough is performed on real hardware, it needs to fulfill some requirements. A brief overview of these requirements is given below, for more information on specific devices, see [PCI Passthrough Examples](https://pve.proxmox.com/wiki/PCI_Passthrough).
#### Hardware 
Your hardware needs to support IOMMU (**I** /**O** **M** emory **M** anagement **U** nit) interrupt remapping, this includes the CPU and the motherboard.
Generally, Intel systems with VT-d and AMD systems with AMD-Vi support this. On arm64, the equivalent is the System Memory Management Unit (SMMU), provided by supported platforms. It is not guaranteed that everything will work out of the box, due to bad hardware implementation and missing or low quality drivers.
Further, server grade hardware has often better support than consumer grade hardware, but even then, many modern systems can support this.
Please refer to your hardware vendor to check if they support this feature under Linux for your specific setup.
#### Determining PCI Card Address 
The easiest way is to use the GUI to add a device of type "Host PCI" in the VM’s hardware tab. Alternatively, you can use the command line.
You can locate your card using

```
 lspci
```

#### Configuration 
Once you ensured that your hardware supports passthrough, you will need to do some configuration to enable PCI(e) passthrough.
IOMMU
You will have to enable IOMMU support in your BIOS/UEFI. Usually the corresponding setting is called IOMMU or VT-d, but you should find the exact option name in the manual of your motherboard.
With AMD CPUs IOMMU is enabled by default. With recent kernels (6.8 or newer), this is also true for Intel CPUs. On older kernels, it is necessary to enable it on Intel CPUs via the kernel command line by adding:

```
 intel_iommu=on
```
  
| The intel_iommu=on parameter applies to x86 hosts. On arm64, the SMMU is enabled through firmware and ACPI, so no such kernel command line parameter is needed.  |  
| --- |  
IOMMU Passthrough Mode
If your hardware supports IOMMU passthrough mode, enabling this mode might increase performance. This is because VMs then bypass the (default) DMA translation normally performed by the hypervisor and instead pass DMA requests directly to the hardware IOMMU. To enable these options, add:

```
 iommu=pt
```

to the kernel commandline.
Kernel Modules
Make sure the following modules are loaded by adding them to a file under '/etc/modules-load.d/', for example '/etc/modules-load.d/vfio.conf':  
|  Mediated devices passthrough If passing through mediated devices (e.g. vGPUs), the following is not needed. In these cases, the device will be owned by the appropriate host driver directly.  |  
| --- |  

```
 vfio
 vfio_iommu_type1
 vfio_pci
```

After changing anything modules related, you need to refresh your initramfs. On Proxmox VE this can be done by executing: 

```
# update-initramfs -u -k all
```

To check if the modules are being loaded, the output of

```
# lsmod | grep vfio
```

should include the three modules from above.
Finish Configuration
Finally, reboot to bring the changes into effect and check that IOMMU is indeed enabled.

```
# dmesg | grep -e DMAR -e IOMMU -e AMD-Vi
```

should display that IOMMU, Directed I/O or Interrupt Remapping is enabled, depending on hardware and kernel the exact message can vary.
For notes on how to troubleshoot or verify if IOMMU is working as intended, please see the [Verifying IOMMU Parameters](https://pve.proxmox.com/wiki/PCI_Passthrough#Verifying_IOMMU_parameters) section in our wiki.
It is also important that the device(s) you want to pass through are in a **separate** IOMMU group. This can be checked with a call to the Proxmox VE API:

```
# pvesh get /nodes/{nodename}/hardware/pci --pci-class-blacklist ""
```

It is okay if the device is in an IOMMU group together with its functions (e.g. a GPU with the HDMI Audio device) or with its root port or PCI(e) bridge.  
|  PCI(e) slots Some platforms handle their physical PCI(e) slots differently. Sometimes it can help to put the card in another PCI(e) slot, if you do not get the desired IOMMU group separation.  |  
| --- |  
|  Unsafe interrupts For some platforms, it may be necessary to allow unsafe interrupts. To do so, add the following line to a file ending in .conf under **/etc/modprobe.d/** : 
```
 options vfio_iommu_type1 allow_unsafe_interrupts=1
```
Please be aware that this option can make your system unstable.  |  
| --- |  
#### GPU Passthrough Notes 
It is not possible to display the frame buffer of the GPU via NoVNC or SPICE on the Proxmox VE web interface.
When passing through a whole GPU or a vGPU and graphic output is wanted, one has to either physically connect a monitor to the card, or configure a remote desktop software (for example, VNC or RDP) inside the guest.
If you only want to use the GPU as a hardware accelerator — for example, with programs using OpenCL or CUDA — this isn’t necessary.
###  Host Device Passthrough
The most used variant of PCI(e) passthrough is to pass through a whole PCI(e) card, for example a GPU or a network card.
#### Host Configuration 
Proxmox VE tries to automatically make the PCI(e) device unavailable for the host. However, if this doesn’t work, there are two things that can be done:
  * pass the device IDs to the options of the _vfio-pci_ modules by adding 

```
 options vfio-pci ids=1234:5678,4321:8765
```

to a .conf file in **/etc/modprobe.d/** where 1234:5678 and 4321:8765 are the vendor and device IDs obtained by:

```
# lspci -nn
```

  * blacklist the driver on the host completely, ensuring it is free to bind for passthrough instead, by adding 

```
 blacklist DRIVERNAME
```

to a .conf file in **/etc/modprobe.d/**.
To find the driver name, execute

```
# lspci -k
```

for example:

```
# lspci -k | grep -A 3 "VGA"
```

will output something similar to

```
01:00.0 VGA compatible controller: NVIDIA Corporation GP108 [GeForce GT 1030] (rev a1)
        Subsystem: Micro-Star International Co., Ltd. [MSI] GP108 [GeForce GT 1030]
        Kernel driver in use: <some-module>
        Kernel modules: <some-module>
```

Now we can blacklist the drivers by writing them into a .conf file:

```
echo "blacklist <some-module>" >> /etc/modprobe.d/blacklist.conf
```



For both methods you need to [update the initramfs](https://pve.proxmox.com/pve-docs/qm.1.html#qm_pci_passthrough_update_initramfs) and reboot after that.
Should this not work, you might need to set a soft dependency to load _vfio-pci_ before loading the GPU modules. This can be done with the _softdep_ flag, see also the manpages on _modprobe.d_ for more information.
For example, if you are using drivers named <some-module>:

```
# echo "softdep <some-module> pre: vfio-pci" >> /etc/modprobe.d/<some-module>.conf
```

Verify Configuration
To check if your changes were successful, you can use

```
# lspci -nnk
```

and check your device entry. If it says

```
Kernel driver in use: vfio-pci
```

or the _in use_ line is missing entirely, the device is ready to be used for passthrough.  
|  Mediated devices For mediated devices this line will differ as the device will be owned by the host driver directly, not _vfio-pci_.  |  
| --- |  
#### VM Configuration 
When passing through a GPU, the best compatibility is reached when using _q35_ as machine type, _OVMF_ (_UEFI_ for VMs) instead of SeaBIOS and PCIe instead of PCI. Note that if you want to use _OVMF_ for GPU passthrough, the GPU needs to have a UEFI-capable ROM, otherwise use SeaBIOS instead. To check if the ROM is UEFI capable, see the [PCI Passthrough Examples](https://pve.proxmox.com/wiki/PCI_Passthrough#How_to_know_if_a_graphics_card_is_UEFI_.28OVMF.29_compatible) wiki.
Furthermore, when using OVMF, VGA arbitration can potentially be disabled, which reduces the amount of legacy code that needs to run at boot. To disable VGA arbitration:

```
 echo "options vfio-pci ids=<vendor-id>,<device-id> disable_vga=1" > /etc/modprobe.d/vfio.conf
```

replacing the <vendor-id> and <device-id> with the ones obtained from:

```
# lspci -nn
```

PCI devices can be added in the web interface in the hardware section of the VM. Alternatively, you can use the command line; set the **hostpciX** option in the VM configuration, for example by executing:

```
# qm set VMID -hostpci0 00:02.0
```

or by adding a line to the VM configuration file:

```
 hostpci0: 00:02.0
```

If your device has multiple functions (e.g., ‘00:02.0’ and ‘00:02.1’ ), you can pass them through all together with the shortened syntax ``00:02`_. This is equivalent to checking the ``All Functions`_ checkbox in the web interface.
There are some options which may be necessary, depending on the device and guest OS:
  * **x-vga=on|off** marks the PCI(e) device as the primary GPU of the VM. With this enabled the **vga** configuration option will be ignored. 
  * **pcie=on|off** tells Proxmox VE to use a PCIe or PCI port. Some guests/device combinations require PCIe rather than PCI. PCIe is only available for _q35_ machine types. 
  * **rombar=on|off** makes the firmware ROM visible for the guest. Default is on. Some PCI(e) devices need this disabled. 
  * **romfile= <path>**, is an optional path to a ROM file for the device to use. This is a relative path under **/usr/share/kvm/**. 


Example
An example of PCIe passthrough with a GPU set to primary:

```
# qm set VMID -hostpci0 02:00,pcie=on,x-vga=on
```

PCI ID overrides
You can override the PCI vendor ID, device ID, and subsystem IDs that will be seen by the guest. This is useful if your device is a variant with an ID that your guest’s drivers don’t recognize, but you want to force those drivers to be loaded anyway (e.g. if you know your device shares the same chipset as a supported variant).
The available options are vendor-id, device-id, sub-vendor-id, and sub-device-id. You can set any or all of these to override your device’s default IDs.
For example:

```
# qm set VMID -hostpci0 02:00,device-id=0x10f6,sub-vendor-id=0x0000
```

###  SR-IOV
Another variant for passing through PCI(e) devices is to use the hardware virtualization features of your devices, if available.  
|  Enabling SR-IOV To use SR-IOV, platform support is especially important. It may be necessary to enable this feature in the BIOS/UEFI first, or to use a specific PCI(e) port for it to work. If in doubt, consult the manual of the platform or contact its vendor.  |  
| --- |  
_SR-IOV_ (**S** ingle-**R** oot **I** nput/**O** utput **V** irtualization) enables a single device to provide multiple _VFs_ (**V** irtual **F** unctions) to the system. Each of those _VFs_ can be used in a different VM, with full hardware features and also better performance and lower latency than software-virtualized devices.
Currently, the most common use case for this is with NICs (**N** etwork **I** nterface **C** ard) with SR-IOV support, which can provide multiple VFs per physical port. This allows features such as checksum offloading to be used inside a VM, reducing the (host) CPU overhead.
#### Host Configuration 
Generally, there are two methods for enabling virtual functions on a device.
  * sometimes there is an option for the driver module e.g. for some Intel drivers 

```
 max_vfs=4
```

which can be placed in a file with a _.conf_ ending under **/etc/modprobe.d/**. (Do not forget to update your initramfs after that)
Please refer to your driver module documentation for the exact parameters and options.
  * The second, more generic, approach is using the sysfs. If a device and driver support this, you can change the number of VFs on the fly. For example, to set up 4 VFs on device 0000:01:00.0 execute: 

```
# echo 4 > /sys/bus/pci/devices/0000:01:00.0/sriov_numvfs
```

To make this change persistent, you can use the ‘sysfsutils` Debian package. After installation, configure it via **/etc/sysfs.conf** or a `FILE.conf’ in **/etc/sysfs.d/**.


#### VM Configuration 
After creating VFs, you should see them as separate PCI(e) devices when outputting them with lspci. Get their ID and pass them through like a [normal PCI(e) device](https://pve.proxmox.com/pve-docs/qm.1.html#qm_pci_passthrough_vm_config).
###  Mediated Devices (vGPU, GVT-g)
Mediated devices are another method to reuse features and performance from physical hardware for virtualized hardware. These are most commonly found in virtualized GPU setups such as Intel’s GVT-g and NVIDIA’s vGPUs used in their GRID technology.
With this, a physical card is able to create virtual cards, similar to SR-IOV. The difference is that mediated devices do not appear as PCI(e) devices on the host, and are thus only suited for use in virtual machines.
#### Host Configuration 
In general, your card’s driver must support that feature, otherwise it will not work. So please refer to your vendor for compatible drivers and how to configure them.
Intel’s drivers for GVT-g are integrated in the kernel and should work with 5th, 6th and 7th generation Intel Core Processors, as well as E3 v4, E3 v5 and E3 v6 Xeon Processors.
To enable it for Intel Graphics, you have to make sure to load the module _kvmgt_ (for example via /etc/modules-load.d/) and to enable it on the kernel commandline and add the following parameter:

```
 i915.enable_gvt=1
```

After that remember to [update the initramfs](https://pve.proxmox.com/pve-docs/qm.1.html#qm_pci_passthrough_update_initramfs), and reboot your host.
#### VM Configuration 
To use a mediated device, simply specify the mdev property on a hostpciX VM configuration option.
You can get the supported devices via the _sysfs_. For example, to list the supported types for the device _0000:00:02.0_ you would simply execute:

```
# ls /sys/bus/pci/devices/0000:00:02.0/mdev_supported_types
```

Each entry is a directory which contains the following important files:
  * _available_instances_ contains the amount of still available instances of this type; each _mdev_ used in a VM reduces this. 
  * _description_ contains a short description about the capabilities of the type 
  * _create_ is the endpoint to create such a device — Proxmox VE does this automatically for you if a _hostpciX_ option with mdev is configured. 


Example configuration with an Intel GVT-g vGPU (Intel Skylake 6700k):

```
# qm set VMID -hostpci0 00:02.0,mdev=i915-GVTg_V5_4
```

With this set, Proxmox VE automatically creates such a device on VM start, and cleans it up again when the VM stops.
###  Usage in Clusters
It is also possible to map devices at a cluster level, so that they can be properly used with HA and hardware changes are detected and non-root users can configure them. See [Resource Mapping](https://pve.proxmox.com/pve-docs/qm.1.html#resource_mapping) for details on that.
###  vIOMMU (emulated IOMMU)
vIOMMU is the emulation of a hardware IOMMU within a virtual machine, providing improved memory access control and security for virtualized I/O devices. Using the vIOMMU option also allows you to pass through PCI(e) devices to level-2 VMs in level-1 VMs via [Nested Virtualization](https://pve.proxmox.com/wiki/Nested_Virtualization). To pass through physical PCI(e) devices from the host to nested VMs, follow the PCI(e) passthrough instructions.
There are currently two vIOMMU implementations available: Intel and VirtIO.
#### Intel vIOMMU 
Intel vIOMMU-specific VM requirements:
  * Whether you are using an Intel or AMD CPU on your host, it is important to set intel_iommu=on in the VM’s kernel parameters. 
  * To use Intel vIOMMU you need to set **q35** as the machine type. 


If all requirements are met, you can add viommu=intel to the machine parameter in the configuration of the VM that should be able to pass through PCI devices.

```
# qm set VMID -machine q35,viommu=intel
```

[QEMU documentation for VT-d](https://wiki.qemu.org/Features/VT-d)
#### VirtIO vIOMMU 
This vIOMMU implementation is more recent and does not have as many limitations as Intel vIOMMU but is currently less used in production and less documented.
With VirtIO vIOMMU there is **no** need to set any kernel parameters. It is also **not** necessary to use q35 as the machine type, but it is advisable if you want to use PCIe.

```
# qm set VMID -machine q35,viommu=virtio
```

[Blog-Post by Michael Zhao explaining virtio-iommu](https://web.archive.org/web/20230804075844/https://michael2012z.medium.com/virtio-iommu-789369049443)
##  Hookscripts 
You can add a hook script to VMs with the config property hookscript.

```
# qm set 100 --hookscript local:snippets/hookscript.pl
```

It will be called during various phases of the guests lifetime. For an example and documentation see the example script under /usr/share/pve-docs/examples/guest-example-hookscript.pl.
##  Hibernation 
You can suspend a VM to disk with the GUI option Hibernate or with

```
# qm suspend ID --todisk
```

That means that the current content of the memory will be saved onto disk and the VM gets stopped. On the next start, the memory content will be loaded and the VM can continue where it was left off.
State storage selection
If no target storage for the memory is given, it will be automatically chosen, the first of: 
  1. The storage vmstatestorage from the VM config. 
  2. The first shared storage from any VM disk. 
  3. The first non-shared storage from any VM disk. 
  4. The storage local as a fallback. 


##  Resource Mapping 
When using or referencing local resources (e.g. address of a pci device), using the raw address or id is sometimes problematic, for example:
  * when using HA, a different device with the same id or path may exist on the target node, and if one is not careful when assigning such guests to HA groups, the wrong device could be used, breaking configurations. 
  * changing hardware can change ids and paths, so one would have to check all assigned devices and see if the path or id is still correct. 


To handle this better, one can define cluster wide resource mappings, such that a resource has a cluster unique, user selected identifier which can correspond to different devices on different hosts. With this, HA won’t start a guest with a wrong device, and hardware changes can be detected.
Creating such a mapping can be done with the Proxmox VE web GUI under Datacenter in the relevant tab in the Resource Mappings category, or on the cli with

```
# pvesh create /cluster/mapping/<type> <options>
```

Where <type> is the hardware type (currently either pci, usb or [dir](https://pve.proxmox.com/pve-docs/qm.1.html#qm_virtiofs)) and <options> are the device mappings and other configuration parameters.
Note that the options must include a map property with all identifying properties of that hardware, so that it’s possible to verify the hardware did not change and the correct device is passed through.
For example to add a PCI device as device1 with the path 0000:01:00.0 that has the device id 0001 and the vendor id 0002 on the node node1, and 0000:02:00.0 on node2 you can add it with:

```
# pvesh create /cluster/mapping/pci --id device1 \
 --map node=node1,path=0000:01:00.0,id=0002:0001 \
 --map node=node2,path=0000:02:00.0,id=0002:0001
```

You must repeat the map parameter for each node where that device should have a mapping (note that you can currently only map one USB device per node per mapping).
Using the GUI makes this much easier, as the correct properties are automatically picked up and sent to the API.
It’s also possible for PCI devices to provide multiple devices per node with multiple map properties for the nodes. If such a device is assigned to a guest, the first free one will be used when the guest is started. The order of the paths given is also the order in which they are tried, so arbitrary allocation policies can be implemented.
This is useful for devices with SR-IOV, since some times it is not important which exact virtual function is passed through.
You can assign such a device to a guest either with the GUI or with

```
# qm set ID -hostpci0 <name>
```

for PCI devices, or

```
# qm set <vmid> -usb0 <name>
```

for USB devices.
Where <vmid> is the guests id and <name> is the chosen name for the created mapping. All usual options for passing through the devices are allowed, such as mdev.
To create mappings Mapping.Modify on /mapping/<type>/<name> is necessary (where <type> is the device type and <name> is the name of the mapping).
To use these mappings, Mapping.Use on /mapping/<type>/<name> is necessary (in addition to the normal guest privileges to edit the configuration).
Additional Options
There are additional options when defining a cluster wide resource mapping. Currently there are the following options:
  * mdev (PCI): This marks the PCI device as being capable of providing mediated devices. When this is enabled, you can select a type when configuring it on the guest. If multiple PCI devices are selected for the mapping, the mediated device will be created on the first one where there are any available instances of the selected type. 
  * live-migration-capable (PCI): This marks the PCI device as being capable of being live migrated between nodes. This requires driver and hardware support. Only NVIDIA GPUs with recent kernel are known to support this. Note that live migrating passed through devices is an experimental feature and may not work or cause issues. 


##  Managing Virtual Machines with qm
qm is the tool to manage QEMU/KVM virtual machines on Proxmox VE. You can create and destroy virtual machines, and control execution (start/stop/suspend/resume). Besides that, you can use qm to set parameters in the associated config file. It is also possible to create and delete virtual disks.
###  CLI Usage Examples
Using an iso file uploaded on the _local_ storage, create a VM with a 4 GB IDE disk on the _local-lvm_ storage

```
# qm create 300 -ide0 local-lvm:4 -net0 e1000 -cdrom local:iso/proxmox-mailgateway_2.1.iso
```

Start the new VM

```
# qm start 300
```

Send a shutdown request, then wait until the VM is stopped.

```
# qm shutdown 300 && qm wait 300
```

Same as above, but only wait for 40 seconds.

```
# qm shutdown 300 && qm wait 300 -timeout 40
```

If the VM does not shut down, force-stop it and overrule any running shutdown tasks. As stopping VMs may incur data loss, use it with caution.

```
# qm stop 300 -overrule-shutdown 1
```

Destroying a VM always removes it from Access Control Lists and it always removes the firewall configuration of the VM. You have to activate _--purge_ , if you want to additionally remove the VM from replication jobs, backup jobs and HA resource configurations.  
| Activating purge will also remove the HA resource from any affinity rules referencing it and will remove rules that have only this one remaining resource.  |  
| --- |  

```
# qm destroy 300 --purge
```

Move a disk image to a different storage.

```
# qm move-disk 300 scsi0 other-storage
```

Reassign a disk image to a different VM. This will remove the disk scsi1 from the source VM and attaches it as scsi3 to the target VM. In the background the disk image is being renamed so that the name matches the new owner.

```
# qm move-disk 300 scsi1 --target-vmid 400 --target-disk scsi3
```

##  Configuration 
VM configuration files are stored inside the Proxmox cluster file system, and can be accessed at /etc/pve/qemu-server/<VMID>.conf. Like other files stored inside /etc/pve/, they get automatically replicated to all other cluster nodes.  
| VMIDs < 100 are reserved for internal purposes, and VMIDs need to be unique cluster wide.  |  
| --- |  
Example VM Configuration

```
boot: order=virtio0;net0
cores: 1
sockets: 1
memory: 512
name: webmail
ostype: l26
net0: e1000=EE:D2:28:5F:B6:3E,bridge=vmbr0
virtio0: local:vm-100-disk-1,size=32G
```

Those configuration files are simple text files, and you can edit them using a normal text editor (vi, nano, …). This is sometimes useful to do small corrections, but keep in mind that you need to restart the VM to apply such changes.
For that reason, it is usually better to use the qm command to generate and modify those files, or do the whole thing using the GUI. Our toolkit is smart enough to instantaneously apply most changes to running VM. This feature is called "hot plug", and there is no need to restart the VM in that case.
###  File Format
VM configuration files use a simple colon separated key/value format. Each line has the following format:

```
# this is a comment
OPTION: value
```

Blank lines in those files are ignored, and lines starting with a # character are treated as comments and are also ignored.
###  Snapshots
When you create a snapshot, qm stores the configuration at snapshot time into a separate snapshot section within the same configuration file. For example, after creating a snapshot called “testsnapshot”, your configuration file will look like this:
VM configuration with snapshot

```
memory: 512
swap: 512
parent: testsnaphot
...

[testsnaphot]
memory: 512
swap: 512
snaptime: 1457170803
...
```

There are a few snapshot related properties like parent and snaptime. The parent property is used to store the parent/child relationship between snapshots. snaptime is the snapshot creation time stamp (Unix epoch).
You can optionally save the memory of a running VM with the option vmstate. For details about how the target storage gets chosen for the VM state, see [State storage selection](https://pve.proxmox.com/pve-docs/qm.1.html#qm_vmstatestorage) in the chapter [Hibernation](https://pve.proxmox.com/pve-docs/qm.1.html#qm_hibernate).
###  Options 

acpi: <boolean> (_default =_ 1) 
    
Enable/disable ACPI.  

affinity: <string> 
    
List of host cores used to execute guest processes, for example: 0,5,8-11  

agent: [enabled=]<1|0> [,freeze-fs=<1|0>] [,fstrim_cloned_disks=<1|0>] [,type=<virtio|isa>] 
    
Enable/disable communication with the QEMU Guest Agent and its properties.  

enabled=<boolean> (_default =_ 0) 
    
Enable/disable communication with a QEMU Guest Agent (QGA) running in the VM.  

freeze-fs=<boolean> (_default =_ 1) 
    
Whether to issue the guest-fsfreeze-freeze and guest-fsfreeze-thaw QEMU guest agent commands. Backups in snapshot mode, clones, snapshots without RAM, importing disks from a running guest, and replications normally issue a guest-fsfreeze-freeze and a respective thaw command when the QEMU Guest agent option is enabled in the guest’s configuration and the agent is running inside of the guest. 
The deprecated _freeze-fs-on-backup_ setting is treated as an alias for this setting. 

fstrim_cloned_disks=<boolean> (_default =_ 0) 
    
Run fstrim after moving a disk or migrating the VM.  

type=<isa | virtio> (_default =_ virtio) 
    
Select the agent type  

allow-ksm: <boolean> (_default =_ 1) 
    
Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).  

amd-sev: [type=]<sev-type> [,allow-smt=<1|0>] [,kernel-hashes=<1|0>] [,no-debug=<1|0>] [,no-key-sharing=<1|0>] 
    
Secure Encrypted Virtualization (SEV) features by AMD CPUs  

allow-smt=<boolean> (_default =_ 1) 
    
Sets policy bit to allow Simultaneous Multi Threading (SMT) (Ignored unless for SEV-SNP)  

kernel-hashes=<boolean> (_default =_ 0) 
    
Add kernel hashes to guest firmware for measured linux kernel launch  

no-debug=<boolean> (_default =_ 0) 
    
Sets policy bit to disallow debugging of guest  

no-key-sharing=<boolean> (_default =_ 0) 
    
Sets policy bit to disallow key sharing with other guests (Ignored for SEV-SNP)  

type=<sev-type> 
    
Enable standard SEV with type=_std_ or enable experimental SEV-ES with the _es_ option or enable experimental SEV-SNP with the _snp_ option.  

arch: <aarch64 | x86_64> 
    
Virtual processor architecture. Defaults to the host architecture.  

args: <string> 
    
Arbitrary arguments passed to kvm, for example: 
args: -no-reboot -smbios _type=0,vendor=FOO_  
| this option is for experts only.  |  
| --- | 

audio0: device=<ich9-intel-hda|intel-hda|AC97> [,driver=<spice|none>] 
      
Configure a audio device, useful in combination with QXL/Spice.  

device=<AC97 | ich9-intel-hda | intel-hda> 
    
Configure an audio device.  

driver=<none | spice> (_default =_ spice) 
    
Driver backend for the audio device.  

autostart: <boolean> (_default =_ 0) 
    
Automatic restart after crash (currently ignored).  

balloon: <integer> (0 - N) 
    
Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.  

bios: <ovmf | seabios> (_default =_ seabios) 
    
Select BIOS implementation.  

boot: [[legacy=]<[acdn]{1,4}>] [,order=<device[;device...]>] 
    
Specify guest boot order. Use the _order=_ sub-property as usage with no key or _legacy=_ is deprecated.  

legacy=<[acdn]{1,4}> (_default =_ cdn) 
    
Boot on floppy (a), hard disk (c), CD-ROM (d), or network (n). Deprecated, use _order=_ instead.  

order=<device[;device...]> 
    
The guest will attempt to boot from devices in the order they appear here. 
Disks, optical drives and passed-through storage USB devices will be directly booted from, NICs will load PXE, and PCIe devices will either behave like disks (e.g. NVMe) or load an option ROM (e.g. RAID controller, hardware NIC).
Note that only devices in this list will be marked as bootable and thus loaded by the guest firmware (BIOS/UEFI). If you require multiple disks for booting (e.g. software-raid), you need to specify all of them here.
Overrides the deprecated _legacy=[acdn]*_ value when given. 

bootdisk: (ide|sata|scsi|virtio)\d+ 
    
Enable booting from specified disk. Deprecated: Use _boot: order=foo;bar_ instead.  

cdrom: <volume> 
    
This is an alias for option -ide2  

cicustom: [meta=<volume>] [,network=<volume>] [,user=<volume>] [,vendor=<volume>] 
    
cloud-init: Specify custom files to replace the automatically generated ones at start.  

meta=<volume> 
    
Specify a custom file containing all meta data passed to the VM via cloud-init. This is provider specific meaning configdrive2 and nocloud differ.  

network=<volume> 
    
To pass a custom file containing all network data to the VM via cloud-init.  

user=<volume> 
    
To pass a custom file containing all user data to the VM via cloud-init.  

vendor=<volume> 
    
To pass a custom file containing all vendor data to the VM via cloud-init.  

cipassword: <string> 
    
cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.  

citype: <configdrive2 | nocloud | opennebula> 
    
Specifies the cloud-init configuration format. The default depends on the configured operating system type (ostype. We use the nocloud format for Linux, and configdrive2 for windows.  

ciupgrade: <boolean> (_default =_ 1) 
    
cloud-init: do an automatic package upgrade after the first boot.  

ciuser: <string> 
    
cloud-init: User name to change ssh keys and password for instead of the image’s configured default user.  

cores: <integer> (1 - N) (_default =_ 1) 
    
The number of cores per socket.  

cpu: [[cputype=]<string>] [,flags=<+FLAG[;-FLAG...]>] [,guest-phys-bits=<integer>] [,hidden=<1|0>] [,hv-vendor-id=<vendor-id>] [,level=<integer>] [,phys-bits=<8-64|host>] [,reported-model=<enum>] 
    
Emulated CPU type.  

cputype=<string> (_default =_ kvm64) 
    
Emulated CPU type. Can be default or custom name (custom model names must be prefixed with _custom-_).  

flags=<+FLAG[;-FLAG...]> 
    
List of additional CPU flags separated by _;_. Use _+FLAG_ to enable, _-FLAG_ to disable a flag. There is a special _nested-virt_ shorthand which controls nested virtualization for the current CPU (_svm_ for AMD and _vmx_ for Intel). Custom CPU models can specify any flag supported by QEMU/KVM, VM-specific flags must be from the following set for security reasons: aes, amd-no-ssb, amd-ssbd, hv-evmcs, hv-tlbflush, ibpb, md-clear, nested-virt, pcid, pdpe1gb, spec-ctrl, ssbd, virt-ssbd  

guest-phys-bits=<integer> (32 - 64) 
    
Number of physical address bits available to the guest.  

hidden=<boolean> (_default =_ 0) 
    
Do not identify as a KVM virtual machine. Only affects vCPUs with x86-64 architecture.  

hv-vendor-id=<vendor-id> 
    
The Hyper-V vendor ID. Some drivers or programs inside Windows guests need a specific ID.  

level=<integer> (0 - 4294967295) 
    
Maximum input value for the basic CPUID leaves the guest can query - that is the vendor (leaf 0), family/model/stepping and feature bits (leaf 1), cache and topology info (leaves 4 and B), and so on. Higher-numbered leaves are hidden. Setting _30_ is a common workaround for Hyper-V boot failures on Windows guests running on recent Intel hosts. Only applies when the vCPU architecture is x86_64.  

phys-bits=<8-64|host> 
    
The physical memory address bits that are reported to the guest OS. Should be smaller or equal to the host’s. Set to _host_ to use value from host CPU, but note that doing so will break live migration to CPUs with other values.  

reported-model=<486 | Broadwell | Broadwell-IBRS | Broadwell-noTSX | Broadwell-noTSX-IBRS | Cascadelake-Server | Cascadelake-Server-noTSX | Cascadelake-Server-v2 | Cascadelake-Server-v4 | Cascadelake-Server-v5 | ClearwaterForest | ClearwaterForest-v2 | ClearwaterForest-v3 | Conroe | Cooperlake | Cooperlake-v2 | DiamondRapids | EPYC | EPYC-Genoa | EPYC-Genoa-v2 | EPYC-IBPB | EPYC-Milan | EPYC-Milan-v2 | EPYC-Milan-v3 | EPYC-Rome | EPYC-Rome-v2 | EPYC-Rome-v3 | EPYC-Rome-v4 | EPYC-Rome-v5 | EPYC-Turin | EPYC-v3 | EPYC-v4 | EPYC-v5 | GraniteRapids | GraniteRapids-v2 | GraniteRapids-v3 | GraniteRapids-v4 | GraniteRapids-v5 | Haswell | Haswell-IBRS | Haswell-noTSX | Haswell-noTSX-IBRS | Icelake-Client | Icelake-Client-noTSX | Icelake-Server | Icelake-Server-noTSX | Icelake-Server-v3 | Icelake-Server-v4 | Icelake-Server-v5 | Icelake-Server-v6 | Icelake-Server-v7 | IvyBridge | IvyBridge-IBRS | KnightsMill | Nehalem | Nehalem-IBRS | Opteron_G1 | Opteron_G2 | Opteron_G3 | Opteron_G4 | Opteron_G5 | Penryn | SandyBridge | SandyBridge-IBRS | SapphireRapids | SapphireRapids-v2 | SapphireRapids-v3 | SapphireRapids-v4 | SapphireRapids-v5 | SapphireRapids-v6 | SierraForest | SierraForest-v2 | SierraForest-v3 | SierraForest-v4 | SierraForest-v5 | Skylake-Client | Skylake-Client-IBRS | Skylake-Client-noTSX-IBRS | Skylake-Client-v4 | Skylake-Server | Skylake-Server-IBRS | Skylake-Server-noTSX-IBRS | Skylake-Server-v4 | Skylake-Server-v5 | Westmere | Westmere-IBRS | a64fx | athlon | core2duo | coreduo | cortex-a35 | cortex-a53 | cortex-a55 | cortex-a57 | cortex-a710 | cortex-a72 | cortex-a76 | cortex-a78ae | host | kvm32 | kvm64 | max | neoverse-n1 | neoverse-n2 | neoverse-v1 | pentium | pentium2 | pentium3 | phenom | qemu32 | qemu64> (_default =_ kvm64) 
    
CPU model and vendor to report to the guest. Must be a QEMU/KVM supported model. Only valid for custom CPU model definitions, default models will always report themselves to the guest OS.  

cpulimit: <number> (0 - 128) (_default =_ 0) 
    
Limit of CPU usage.   
| If the computer has 2 CPUs, it has total of _2_ CPU time. Value _0_ indicates no CPU limit.  |  
| --- | 

cpuunits: <integer> (1 - 262144) (_default =_ cgroup v1: 1024, cgroup v2: 100) 
      
CPU weight for a VM. Argument is used in the kernel fair scheduler. The larger the number is, the more CPU time this VM gets. Number is relative to weights of all the other running VMs.  

description: <string> 
    
Description for the VM. Shown in the web-interface VM’s summary. This is saved as comment inside the configuration file.  

efidisk0: [file=]<volume> [,efitype=<2m|4m>] [,format=<enum>] [,ms-cert=<enum>] [,pre-enrolled-keys=<1|0>] [,size=<DiskSize>] 
    
Configure a disk for storing EFI vars.  

efitype=<2m | 4m> (_default =_ 2m) 
    
Size and type of the OVMF EFI vars. _4m_ is newer and recommended, and required for Secure Boot. For backwards compatibility, _2m_ is used if not otherwise specified. Ignored for VMs with arch=aarch64 (ARM).  

file=<volume> 
    
The drive’s backing volume.  

format=<cloop | qcow | qcow2 | qed | raw | vmdk> 
    
The drive’s backing file’s data format.  

ms-cert=<2011 | 2023 | 2023k | 2023w> (_default =_ 2011) 
    
Informational marker indicating the version of the latest Microsoft UEFI certificates that have been enrolled by Proxmox VE. The value _2023k_ means that the _Microsoft UEFI CA 2023_ , the _Windows UEFI CA 2023_ and the _Microsoft Corporation KEK 2K CA 2023_ certificates are included. The values _2023_ and _2023w_ are deprecated and for compatibility only.  

pre-enrolled-keys=<boolean> (_default =_ 0) 
    
Use am EFI vars template with distribution-specific and Microsoft Standard keys enrolled, if used with _efitype=4m_. Note that this will enable Secure Boot by default, though it can still be turned off from within the VM.  

size=<DiskSize> 
    
Disk size. This is purely informational and has no effect.  

freeze: <boolean> 
    
Freeze CPU at startup (use _c_ monitor command to start execution).  

hookscript: <string> 
    
Script that will be executed during various steps in the vms lifetime.  

hostpci[n]: [[host=]<HOSTPCIID[;HOSTPCIID2...]>] [,device-id=<hex id>] [,driver=<vfio|keep>] [,legacy-igd=<1|0>] [,mapping=<mapping-id>] [,mdev=<string>] [,pcie=<1|0>] [,rombar=<1|0>] [,romfile=<string>] [,sub-device-id=<hex id>] [,sub-vendor-id=<hex id>] [,vendor-id=<hex id>] [,x-vga=<1|0>] 
    
Map host PCI devices into guest.   
| This option allows direct access to host hardware. So it is no longer possible to migrate such machines - use with special care.  |  
| --- |  
| Experimental! User reported problems with this option.  |  
| --- | 

device-id=<hex id> 
      
Override PCI device ID visible to guest  

driver=<keep | vfio> (_default =_ vfio) 
    
If set to _keep_ the device will neither be reset nor bound to the _vfio-pci_ driver. Useful for devices that already have the correct driver loaded.  

host=<HOSTPCIID[;HOSTPCIID2...]> 
    
Host PCI device pass through. The PCI ID of a host’s PCI device or a list of PCI virtual functions of the host. HOSTPCIID syntax is: 
_bus:dev.func_ (hexadecimal numbers)
You can use the _lspci_ command to list existing PCI devices.
Either this or the _mapping_ key must be set. 

legacy-igd=<boolean> (_default =_ 0) 
    
Pass this device in legacy IGD mode, making it the primary and exclusive graphics device in the VM. Requires _pc-i440fx_ machine type and VGA set to _none_.  

mapping=<mapping-id> 
    
The ID of a cluster wide mapping. Either this or the default-key _host_ must be set.  

mdev=<string> 
    
The type of mediated device to use. An instance of this type will be created on startup of the VM and will be cleaned up when the VM stops.  

pcie=<boolean> (_default =_ 0) 
    
Choose the PCI-express bus (needs the _q35_ machine model).  

rombar=<boolean> (_default =_ 1) 
    
Specify whether or not the device’s ROM will be visible in the guest’s memory map.  

romfile=<string> 
    
Custom pci device rom filename (must be located in /usr/share/kvm/).  

sub-device-id=<hex id> 
    
Override PCI subsystem device ID visible to guest  

sub-vendor-id=<hex id> 
    
Override PCI subsystem vendor ID visible to guest  

vendor-id=<hex id> 
    
Override PCI vendor ID visible to guest  

x-vga=<boolean> (_default =_ 0) 
    
Enable vfio-vga device support.  

hotplug: <string> (_default =_ network,disk,usb) 
    
Selectively enable hotplug features. This is a comma separated list of hotplug features: _network_ , _disk_ , _cpu_ , _memory_ , _usb_ and _cloudinit_. Use _0_ to disable hotplug completely. Using _1_ as value is an alias for the default network,disk,usb. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.  

hugepages: <1024 | 2 | any> 
    
Enables hugepages memory. 
Sets the size of hugepages in MiB. If the value is set to _any_ then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB. 

ide[n]: [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,model=<model>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as IDE hard disk or CD-ROM (n is 0 to 3).  

aio=<io_uring | native | threads> 
    
AIO type to use.  

backup=<boolean> 
    
Whether the drive should be included when making backups.  

bps=<bps> 
    
Maximum r/w speed in bytes per second.  

bps_max_length=<seconds> 
    
Maximum length of I/O bursts in seconds.  

bps_rd=<bps> 
    
Maximum read speed in bytes per second.  

bps_rd_max_length=<seconds> 
    
Maximum length of read I/O bursts in seconds.  

bps_wr=<bps> 
    
Maximum write speed in bytes per second.  

bps_wr_max_length=<seconds> 
    
Maximum length of write I/O bursts in seconds.  

cache=<directsync | none | unsafe | writeback | writethrough> 
    
The drive’s cache mode  

detect_zeroes=<boolean> 
    
Controls whether to detect and try to optimize writes of zeroes.  

discard=<ignore | on> 
    
Controls whether to pass discard/trim requests to the underlying storage.  

file=<volume> 
    
The drive’s backing volume.  

format=<cloop | qcow | qcow2 | qed | raw | vmdk> 
    
The drive’s backing file’s data format.  

iops=<iops> 
    
Maximum r/w I/O in operations per second.  

iops_max=<iops> 
    
Maximum unthrottled r/w I/O pool in operations per second.  

iops_max_length=<seconds> 
    
Maximum length of I/O bursts in seconds.  

iops_rd=<iops> 
    
Maximum read I/O in operations per second.  

iops_rd_max=<iops> 
    
Maximum unthrottled read I/O pool in operations per second.  

iops_rd_max_length=<seconds> 
    
Maximum length of read I/O bursts in seconds.  

iops_wr=<iops> 
    
Maximum write I/O in operations per second.  

iops_wr_max=<iops> 
    
Maximum unthrottled write I/O pool in operations per second.  

iops_wr_max_length=<seconds> 
    
Maximum length of write I/O bursts in seconds.  

mbps=<mbps> 
    
Maximum r/w speed in megabytes per second.  

mbps_max=<mbps> 
    
Maximum unthrottled r/w pool in megabytes per second.  

mbps_rd=<mbps> 
    
Maximum read speed in megabytes per second.  

mbps_rd_max=<mbps> 
    
Maximum unthrottled read pool in megabytes per second.  

mbps_wr=<mbps> 
    
Maximum write speed in megabytes per second.  

mbps_wr_max=<mbps> 
    
Maximum unthrottled write pool in megabytes per second.  

media=<cdrom | disk> (_default =_ disk) 
    
The drive’s media type.  

model=<model> 
    
The drive’s reported model name, url-encoded, up to 40 bytes long.  

replicate=<boolean> (_default =_ 1) 
    
Whether the drive should considered for replication jobs.  

rerror=<ignore | report | stop> 
    
Read error action.  

serial=<serial> 
    
The drive’s reported serial number, url-encoded, up to 20 bytes long.  

shared=<boolean> (_default =_ 0) 
    
Mark this locally-managed volume as available on all nodes.   
| This option does not share the volume automatically, it assumes it is shared already!  |  
| --- | 

size=<DiskSize> 
      
Disk size. This is purely informational and has no effect.  

snapshot=<boolean> 
    
Controls qemu’s snapshot mode feature. If activated, changes made to the disk are temporary and will be discarded when the VM is shutdown.  

ssd=<boolean> 
    
Whether to expose this drive as an SSD, rather than a rotational hard disk.  

werror=<enospc | ignore | report | stop> 
    
Write error action.  

wwn=<wwn> 
    
The drive’s worldwide name, encoded as 16 bytes hex string, prefixed by _0x_.  

intel-tdx: [type=]<tdx-type> ,attestation=<1|0> [,vsock-cid=<integer>] [,vsock-port=<integer>] 
    
Trusted Domain Extension (TDX) features by Intel CPUs  

attestation=<boolean> (_default =_ 1) 
    
Enable TDX attestation by including quote-generation-socket  

type=<tdx-type> 
    
Enable TDX  

vsock-cid=<integer> (2 - N) (_default =_ 2) 
    
CID for vsock of Quote Generation Service  

vsock-port=<integer> (0 - N) (_default =_ 4050) 
    
Port for vsock of Quote Generation Service  

ipconfig[n]: [gw=<GatewayIPv4>] [,gw6=<GatewayIPv6>] [,ip=<IPv4Format/CIDR>] [,ip6=<IPv6Format/CIDR>] 
    
cloud-init: Specify IP addresses and gateways for the corresponding interface. 
IP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.
The special string _dhcp_ can be used for IP addresses to use DHCP, in which case no explicit gateway should be provided. For IPv6 the special string _auto_ can be used to use stateless autoconfiguration. This requires cloud-init 19.4 or newer.
If cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using dhcp on IPv4. 

gw=<GatewayIPv4> 
    
Default gateway for IPv4 traffic.   
| Requires option(s): ip  |  
| --- | 

gw6=<GatewayIPv6> 
      
Default gateway for IPv6 traffic.   
| Requires option(s): ip6  |  
| --- | 

ip=<IPv4Format/CIDR> (_default =_ dhcp) 
      
IPv4 address in CIDR format.  

ip6=<IPv6Format/CIDR> (_default =_ dhcp) 
    
IPv6 address in CIDR format.  

ivshmem: size=<integer> [,name=<string>] 
    
Inter-VM shared memory. Useful for direct communication between VMs, or to the host.  

name=<string> 
    
The name of the file. Will be prefixed with _pve-shm-_. Default is the VMID. Will be deleted when the VM is stopped.  

size=<integer> (1 - N) 
    
The size of the file in MB.  

keephugepages: <boolean> (_default =_ 0) 
    
Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.  

keyboard: <da | de | de-ch | en-gb | en-us | es | fi | fr | fr-be | fr-ca | fr-ch | hu | is | it | ja | lt | mk | nl | no | pl | pt | pt-br | sl | sv | tr> 
    
Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.  

kvm: <boolean> (_default =_ 1) 
    
Enable/disable KVM hardware virtualization.  

localtime: <boolean> 
    
Set the real time clock (RTC) to local time. This is enabled by default if the ostype indicates a Microsoft Windows OS.  

lock: <backup | clone | create | migrate | rollback | snapshot | snapshot-delete | suspended | suspending> 
    
Lock/unlock the VM.  

machine: [[type=]<machine type>] [,aw-bits=<number>] [,enable-s3=<1|0>] [,enable-s4=<1|0>] [,viommu=<intel|virtio>] 
    
Specify the QEMU machine.  

aw-bits=<number> (32 - 64) 
    
Specifies the vIOMMU address space bit width. 
Intel vIOMMU supports a bit width of either 39 or 48 bits and VirtIO vIOMMU supports any bit width between 32 and 64 bits. 

enable-s3=<boolean> 
    
Enables S3 power state. Defaults to false beginning with machine types 9.2+pve1, true before.  

enable-s4=<boolean> 
    
Enables S4 power state. Defaults to false beginning with machine types 9.2+pve1, true before.  

type=<machine type> 
    
Specifies the QEMU machine type.  

viommu=<intel | virtio> 
    
Enable and set guest vIOMMU variant (Intel vIOMMU needs q35 to be set as machine type).  

memory: [current=]<integer> 
    
Memory properties.  

current=<integer> (16 - N) (_default =_ 512) 
    
Current amount of online RAM for the VM in MiB. This is the maximum available memory when you use the balloon device.  

migrate_downtime: <number> (0 - N) (_default =_ 0.1) 
    
Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).  

migrate_speed: <integer> (0 - N) (_default =_ 0) 
    
Set maximum speed (in MB/s) for migrations. Value 0 is no limit.  

name: <string> 
    
Set a name for the VM. Only used on the configuration web interface.  

nameserver: <string> 
    
cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.  

net[n]: [model=]<enum> [,bridge=<bridge>] [,firewall=<1|0>] [,host-tunnel=<1|0>] [,link_down=<1|0>] [,macaddr=<XX:XX:XX:XX:XX:XX>] [,mtu=<integer>] [,queues=<integer>] [,rate=<number>] [,tag=<integer>] [,trunks=<vlanid[;vlanid...]>] [,<model>=<macaddr>] 
    
Specify network devices.  

bridge=<bridge> 
    
Bridge to attach the network device to. The Proxmox VE standard bridge is called _vmbr0_. 
If you do not specify a bridge, we create a kvm user (NATed) network device, which provides DHCP and DNS services. The following addresses are used:

```
10.0.2.2   Gateway
10.0.2.3   DNS Server
10.0.2.4   SMB Server
```

The DHCP server assign addresses to the guest starting from 10.0.2.15. 

firewall=<boolean> 
    
Whether this interface should be protected by the firewall.  

host-tunnel=<boolean> 
    
Enable host GSO over UDP tunnel offload (VirtIO only). Requires QEMU > 10.2 and guest and host kernel support. Disabled by default starting with machine version 11.0+pve1 to work around an issue with the virtio-net driver in guest kernels. With machine versions 10.2 and 11.0, this is enabled by default.  

link_down=<boolean> 
    
Whether this interface should be disconnected (like pulling the plug).  

macaddr=<XX:XX:XX:XX:XX:XX> 
    
A common MAC address with the I/G (Individual/Group) bit not set.  

model=<e1000 | e1000-82540em | e1000-82544gc | e1000-82545em | e1000e | i82551 | i82557b | i82559er | ne2k_isa | ne2k_pci | pcnet | rtl8139 | virtio | vmxnet3> 
    
Network Card Model. The _virtio_ model provides the best performance with very low CPU overhead. If your guest does not support this driver, it is usually best to use _e1000_.  

mtu=<integer> (1 - 65520) 
    
Force MTU of network device (VirtIO only). Setting to _1_ or empty will use the bridge MTU  

queues=<integer> (0 - 64) 
    
Number of packet queues to be used on the device.  

rate=<number> (0 - N) 
    
Rate limit in mbps (megabytes per second) as floating point number.  

tag=<integer> (1 - 4094) 
    
VLAN tag to apply to packets on this interface.  

trunks=<vlanid[;vlanid...]> 
    
VLAN trunks to pass through this interface.  

numa: <boolean> (_default =_ 0) 
    
Enable/disable NUMA.  

numa[n]: cpus=<id[-id];...> [,hostnodes=<id[-id];...>] [,memory=<number>] [,policy=<preferred|bind|interleave>] 
    
NUMA topology.  

cpus=<id[-id];...> 
    
CPUs accessing this NUMA node.  

hostnodes=<id[-id];...> 
    
Host NUMA nodes to use.  

memory=<number> 
    
Amount of memory this NUMA node provides.  

policy=<bind | interleave | preferred> 
    
NUMA allocation policy.  

onboot: <boolean> (_default =_ 0) 
    
Specifies whether a VM will be started during system bootup.  

ostype: <l24 | l26 | other | solaris | w2k | w2k3 | w2k8 | win10 | win11 | win7 | win8 | wvista | wxp> (_default =_ other) 
    
Specify guest operating system. This is used to enable special optimization/features for specific operating systems:   
|  other   |  unspecified OS   |  
| --- | --- |  
|  wxp   |  Microsoft Windows XP   |  
|  w2k   |  Microsoft Windows 2000   |  
|  w2k3   |  Microsoft Windows 2003   |  
|  w2k8   |  Microsoft Windows 2008   |  
|  wvista   |  Microsoft Windows Vista   |  
|  win7   |  Microsoft Windows 7   |  
|  win8   |  Microsoft Windows 8/2012/2012r2   |  
|  win10   |  Microsoft Windows 10/2016/2019   |  
|  win11   |  Microsoft Windows 11/2022/2025   |  
|  l24   |  Linux 2.4 Kernel   |  
|  l26   |  Linux 2.6 - 7.X Kernel   |  
|  solaris   |  Solaris/OpenSolaris/OpenIndiania kernel   | 

parallel[n]: /dev/parport\d+|/dev/usb/lp\d+ 
      
Map host parallel devices (n is 0 to 2).   
| This option allows direct access to host hardware. So it is no longer possible to migrate such machines - use with special care.  |  
| --- |  
| Experimental! User reported problems with this option.  |  
| --- | 

protection: <boolean> (_default =_ 0) 
      
Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.  

reboot: <boolean> (_default =_ 1) 
    
Allow reboot. If set to _0_ the VM exit on reboot.  

rng0: [source=]</dev/urandom|/dev/random|/dev/hwrng> [,max_bytes=<integer>] [,period=<integer>] 
    
Configure a VirtIO-based Random Number Generator.  

max_bytes=<integer> (_default =_ 1024) 
    
Maximum bytes of entropy allowed to get injected into the guest every _period_ milliseconds. Use 0 to disable limiting (potentially dangerous!).  

period=<integer> (_default =_ 1000) 
    
Every _period_ milliseconds the entropy-injection quota is reset, allowing the guest to retrieve another _max_bytes_ of entropy.  

source=</dev/hwrng | /dev/random | /dev/urandom> 
    
The file on the host to gather entropy from. Using urandom does **not** decrease security in any meaningful way, as it’s still seeded from real entropy, and the bytes provided will most likely be mixed with real entropy on the guest as well. _/dev/hwrng_ can be used to pass through a hardware RNG from the host.  

sata[n]: [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as SATA hard disk or CD-ROM (n is 0 to 5).  

aio=<io_uring | native | threads> 
    
AIO type to use.  

backup=<boolean> 
    
Whether the drive should be included when making backups.  

bps=<bps> 
    
Maximum r/w speed in bytes per second.  

bps_max_length=<seconds> 
    
Maximum length of I/O bursts in seconds.  

bps_rd=<bps> 
    
Maximum read speed in bytes per second.  

bps_rd_max_length=<seconds> 
    
Maximum length of read I/O bursts in seconds.  

bps_wr=<bps> 
    
Maximum write speed in bytes per second.  

bps_wr_max_length=<seconds> 
    
Maximum length of write I/O bursts in seconds.  

cache=<directsync | none | unsafe | writeback | writethrough> 
    
The drive’s cache mode  

detect_zeroes=<boolean> 
    
Controls whether to detect and try to optimize writes of zeroes.  

discard=<ignore | on> 
    
Controls whether to pass discard/trim requests to the underlying storage.  

file=<volume> 
    
The drive’s backing volume.  

format=<cloop | qcow | qcow2 | qed | raw | vmdk> 
    
The drive’s backing file’s data format.  

iops=<iops> 
    
Maximum r/w I/O in operations per second.  

iops_max=<iops> 
    
Maximum unthrottled r/w I/O pool in operations per second.  

iops_max_length=<seconds> 
    
Maximum length of I/O bursts in seconds.  

iops_rd=<iops> 
    
Maximum read I/O in operations per second.  

iops_rd_max=<iops> 
    
Maximum unthrottled read I/O pool in operations per second.  

iops_rd_max_length=<seconds> 
    
Maximum length of read I/O bursts in seconds.  

iops_wr=<iops> 
    
Maximum write I/O in operations per second.  

iops_wr_max=<iops> 
    
Maximum unthrottled write I/O pool in operations per second.  

iops_wr_max_length=<seconds> 
    
Maximum length of write I/O bursts in seconds.  

mbps=<mbps> 
    
Maximum r/w speed in megabytes per second.  

mbps_max=<mbps> 
    
Maximum unthrottled r/w pool in megabytes per second.  

mbps_rd=<mbps> 
    
Maximum read speed in megabytes per second.  

mbps_rd_max=<mbps> 
    
Maximum unthrottled read pool in megabytes per second.  

mbps_wr=<mbps> 
    
Maximum write speed in megabytes per second.  

mbps_wr_max=<mbps> 
    
Maximum unthrottled write pool in megabytes per second.  

media=<cdrom | disk> (_default =_ disk) 
    
The drive’s media type.  

replicate=<boolean> (_default =_ 1) 
    
Whether the drive should considered for replication jobs.  

rerror=<ignore | report | stop> 
    
Read error action.  

serial=<serial> 
    
The drive’s reported serial number, url-encoded, up to 20 bytes long.  

shared=<boolean> (_default =_ 0) 
    
Mark this locally-managed volume as available on all nodes.   
| This option does not share the volume automatically, it assumes it is shared already!  |  
| --- | 

size=<DiskSize> 
      
Disk size. This is purely informational and has no effect.  

snapshot=<boolean> 
    
Controls qemu’s snapshot mode feature. If activated, changes made to the disk are temporary and will be discarded when the VM is shutdown.  

ssd=<boolean> 
    
Whether to expose this drive as an SSD, rather than a rotational hard disk.  

werror=<enospc | ignore | report | stop> 
    
Write error action.  

wwn=<wwn> 
    
The drive’s worldwide name, encoded as 16 bytes hex string, prefixed by _0x_.  

scsi[n]: [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,iothread=<1|0>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,product=<product>] [,queues=<integer>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,ro=<1|0>] [,scsiblock=<1|0>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,ssd=<1|0>] [,vendor=<vendor>] [,werror=<enum>] [,wwn=<wwn>] 
    
Use volume as SCSI hard disk or CD-ROM (n is 0 to 30).  

aio=<io_uring | native | threads> 
    
AIO type to use.  

backup=<boolean> 
    
Whether the drive should be included when making backups.  

bps=<bps> 
    
Maximum r/w speed in bytes per second.  

bps_max_length=<seconds> 
    
Maximum length of I/O bursts in seconds.  

bps_rd=<bps> 
    
Maximum read speed in bytes per second.  

bps_rd_max_length=<seconds> 
    
Maximum length of read I/O bursts in seconds.  

bps_wr=<bps> 
    
Maximum write speed in bytes per second.  

bps_wr_max_length=<seconds> 
    
Maximum length of write I/O bursts in seconds.  

cache=<directsync | none | unsafe | writeback | writethrough> 
    
The drive’s cache mode  

detect_zeroes=<boolean> 
    
Controls whether to detect and try to optimize writes of zeroes.  

discard=<ignore | on> 
    
Controls whether to pass discard/trim requests to the underlying storage.  

file=<volume> 
    
The drive’s backing volume.  

format=<cloop | qcow | qcow2 | qed | raw | vmdk> 
    
The drive’s backing file’s data format.  

iops=<iops> 
    
Maximum r/w I/O in operations per second.  

iops_max=<iops> 
    
Maximum unthrottled r/w I/O pool in operations per second.  

iops_max_length=<seconds> 
    
Maximum length of I/O bursts in seconds.  

iops_rd=<iops> 
    
Maximum read I/O in operations per second.  

iops_rd_max=<iops> 
    
Maximum unthrottled read I/O pool in operations per second.  

iops_rd_max_length=<seconds> 
    
Maximum length of read I/O bursts in seconds.  

iops_wr=<iops> 
    
Maximum write I/O in operations per second.  

iops_wr_max=<iops> 
    
Maximum unthrottled write I/O pool in operations per second.  

iops_wr_max_length=<seconds> 
    
Maximum length of write I/O bursts in seconds.  

iothread=<boolean> 
    
Whether to use iothreads for this drive  

mbps=<mbps> 
    
Maximum r/w speed in megabytes per second.  

mbps_max=<mbps> 
    
Maximum unthrottled r/w pool in megabytes per second.  

mbps_rd=<mbps> 
    
Maximum read speed in megabytes per second.  

mbps_rd_max=<mbps> 
    
Maximum unthrottled read pool in megabytes per second.  

mbps_wr=<mbps> 
    
Maximum write speed in megabytes per second.  

mbps_wr_max=<mbps> 
    
Maximum unthrottled write pool in megabytes per second.  

media=<cdrom | disk> (_default =_ disk) 
    
The drive’s media type.  

product=<product> 
    
The drive’s product name, up to 16 bytes long.  

queues=<integer> (2 - N) 
    
Number of queues.  

replicate=<boolean> (_default =_ 1) 
    
Whether the drive should considered for replication jobs.  

rerror=<ignore | report | stop> 
    
Read error action.  

ro=<boolean> 
    
Whether the drive is read-only.  

scsiblock=<boolean> (_default =_ 0) 
    
whether to use scsi-block for full passthrough of host block device   
| can lead to I/O errors in combination with low memory or high memory fragmentation on host  |  
| --- | 

serial=<serial> 
      
The drive’s reported serial number, url-encoded, up to 20 bytes long.  

shared=<boolean> (_default =_ 0) 
    
Mark this locally-managed volume as available on all nodes.   
| This option does not share the volume automatically, it assumes it is shared already!  |  
| --- | 

size=<DiskSize> 
      
Disk size. This is purely informational and has no effect.  

snapshot=<boolean> 
    
Controls qemu’s snapshot mode feature. If activated, changes made to the disk are temporary and will be discarded when the VM is shutdown.  

ssd=<boolean> 
    
Whether to expose this drive as an SSD, rather than a rotational hard disk.  

vendor=<vendor> 
    
The drive’s vendor name, up to 8 bytes long.  

werror=<enospc | ignore | report | stop> 
    
Write error action.  

wwn=<wwn> 
    
The drive’s worldwide name, encoded as 16 bytes hex string, prefixed by _0x_.  

scsihw: <lsi | lsi53c810 | megasas | pvscsi | virtio-scsi-pci | virtio-scsi-single> (_default =_ lsi) 
    
SCSI controller model  

searchdomain: <string> 
    
cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.  

serial[n]: (/dev/[^,]+|socket) 
    
Create a serial device inside the VM (n is 0 to 3), and pass through a host serial device (i.e. /dev/ttyS0), or create a unix socket on the host side (use _qm terminal_ to open a terminal connection).   
| If you pass through a host serial device, it is no longer possible to migrate such machines - use with special care.  |  
| --- |  
| Experimental! User reported problems with this option.  |  
| --- | 

shares: <integer> (0 - 50000) (_default =_ 1000) 
      
Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.  

smbios1: [base64=<1|0>] [,family=<Base64 encoded string>] [,manufacturer=<Base64 encoded string>] [,product=<Base64 encoded string>] [,serial=<Base64 encoded string>] [,sku=<Base64 encoded string>] [,uuid=<UUID>] [,version=<Base64 encoded string>] 
    
Specify SMBIOS type 1 fields.  

base64=<boolean> 
    
Flag to indicate that the SMBIOS values are base64 encoded  

family=<Base64 encoded string> 
    
Set SMBIOS1 family string.  

manufacturer=<Base64 encoded string> 
    
Set SMBIOS1 manufacturer.  

product=<Base64 encoded string> 
    
Set SMBIOS1 product ID.  

serial=<Base64 encoded string> 
    
Set SMBIOS1 serial number.  

sku=<Base64 encoded string> 
    
Set SMBIOS1 SKU string.  

uuid=<UUID> 
    
Set SMBIOS1 UUID.  

version=<Base64 encoded string> 
    
Set SMBIOS1 version.  

smp: <integer> (1 - N) (_default =_ 1) 
    
The number of CPUs. Please use option -sockets instead.  

sockets: <integer> (1 - N) (_default =_ 1) 
    
The number of CPU sockets.  

spice_enhancements: [foldersharing=<1|0>] [,videostreaming=<off|all|filter>] 
    
Configure additional enhancements for SPICE.  

foldersharing=<boolean> (_default =_ 0) 
    
Enable folder sharing via SPICE. Needs Spice-WebDAV daemon installed in the VM.  

videostreaming=<all | filter | off> (_default =_ off) 
    
Enable video streaming. Uses compression for detected video streams.  

sshkeys: <string> 
    
cloud-init: Setup public SSH keys (one key per line, OpenSSH format).  

startdate: (now | YYYY-MM-DD | YYYY-MM-DDTHH:MM:SS) (_default =_ now) 
    
Set the initial date of the real time clock. Valid format for date are:'now' or _2006-06-17T16:01:21_ or _2006-06-17_.  

startup: `[[order=]\d+] [,up=\d+] [,down=\d+] ` 
    
Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the _up_ or _down_ delay in seconds, which specifies a delay to wait before the next VM is started or stopped.  

tablet: <boolean> (_default =_ 1) 
    
Enable/disable the USB tablet device. This device is usually needed to allow absolute mouse positioning with VNC. Else the mouse runs out of sync with normal VNC clients. If you’re running lots of console-only guests on one host, you may consider disabling this to save some context switches. This is turned off by default if you use spice (qm set <vmid> --vga qxl).  

tags: <string> 
    
Tags of the VM. This is only meta information.  

tdf: <boolean> (_default =_ 0) 
    
Enable/disable time drift fix.  

template: <boolean> (_default =_ 0) 
    
Enable/disable Template.  

tpmstate0: [file=]<volume> [,format=<raw|qcow2|vmdk>] [,size=<DiskSize>] [,version=<v1.2|v2.0>] 
    
Configure a Disk for storing TPM state. The format is fixed to _raw_.  

file=<volume> 
    
The drive’s backing volume.  

format=<qcow2 | raw | vmdk> 
    
Format of the image.  

size=<DiskSize> 
    
Disk size. This is purely informational and has no effect.  

version=<v1.2 | v2.0> (_default =_ v1.2) 
    
The TPM interface version. v2.0 is newer and should be preferred. Note that this cannot be changed later on.  

unused[n]: [file=]<volume> 
    
Reference to unused volumes. This is used internally, and should not be modified manually.  

file=<volume> 
    
The drive’s backing volume.  

usb[n]: [[host=]<HOSTUSBDEVICE|spice>] [,mapping=<mapping-id>] [,usb3=<1|0>] 
    
Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).  

host=<HOSTUSBDEVICE|spice> 
    
The Host USB device or port or the value _spice_. HOSTUSBDEVICE syntax is: 

```
'bus-port(.port)*' (decimal numbers) or
'vendor_id:product_id' (hexadecimal numbers) or
'spice'
```

You can use the _lsusb -t_ command to list existing usb devices.  
| This option allows direct access to host hardware. So it is no longer possible to migrate such machines - use with special care.  |  
| --- |  
The value _spice_ can be used to add a usb redirection devices for spice.
Either this or the _mapping_ key must be set. 

mapping=<mapping-id> 
    
The ID of a cluster wide mapping. Either this or the default-key _host_ must be set.  

usb3=<boolean> (_default =_ 0) 
    
Specifies whether if given host option is a USB3 device or port. For modern guests (machine version >= 7.1 and ostype l26 and windows > 7), this flag is irrelevant (all devices are plugged into a xhci controller).  

vcpus: <integer> (1 - N) (_default =_ 0) 
    
Number of hotplugged vcpus.  

vga: [[type=]<enum>] [,clipboard=<vnc>] [,memory=<integer>] 
    
Configure the VGA Hardware. If you want to use high resolution modes (>= 1280x1024x16) you may need to increase the vga memory option. Since QEMU 2.9 the default VGA display type is _std_ for all OS types besides some Windows versions (XP and older) which use _cirrus_. The _qxl_ option enables the SPICE display server. For win* OS you can select how many independent displays you want, Linux guests can add displays them self. You can also run without any graphic card, using a serial device as terminal.  

clipboard=<vnc> 
    
Enable a specific clipboard. If not set, depending on the display type the SPICE one will be added. Live migration with a VNC clipboard is not possible with QEMU machine version < 10.1.  

memory=<integer> (4 - 512) 
    
Sets the VGA memory (in MiB). Has no effect with serial display.  

type=<cirrus | none | qxl | qxl2 | qxl3 | qxl4 | serial0 | serial1 | serial2 | serial3 | std | virtio | virtio-gl | vmware> (_default =_ std) 
    
Select the VGA type. Using type _cirrus_ is not recommended.  

virtio[n]: [file=]<volume> [,aio=<native|threads|io_uring>] [,backup=<1|0>] [,bps=<bps>] [,bps_max_length=<seconds>] [,bps_rd=<bps>] [,bps_rd_max_length=<seconds>] [,bps_wr=<bps>] [,bps_wr_max_length=<seconds>] [,cache=<enum>] [,detect_zeroes=<1|0>] [,discard=<ignore|on>] [,format=<enum>] [,iops=<iops>] [,iops_max=<iops>] [,iops_max_length=<seconds>] [,iops_rd=<iops>] [,iops_rd_max=<iops>] [,iops_rd_max_length=<seconds>] [,iops_wr=<iops>] [,iops_wr_max=<iops>] [,iops_wr_max_length=<seconds>] [,iothread=<1|0>] [,mbps=<mbps>] [,mbps_max=<mbps>] [,mbps_rd=<mbps>] [,mbps_rd_max=<mbps>] [,mbps_wr=<mbps>] [,mbps_wr_max=<mbps>] [,media=<cdrom|disk>] [,replicate=<1|0>] [,rerror=<ignore|report|stop>] [,ro=<1|0>] [,serial=<serial>] [,shared=<1|0>] [,size=<DiskSize>] [,snapshot=<1|0>] [,werror=<enum>] 
    
Use volume as VIRTIO hard disk (n is 0 to 15).  

aio=<io_uring | native | threads> 
    
AIO type to use.  

backup=<boolean> 
    
Whether the drive should be included when making backups.  

bps=<bps> 
    
Maximum r/w speed in bytes per second.  

bps_max_length=<seconds> 
    
Maximum length of I/O bursts in seconds.  

bps_rd=<bps> 
    
Maximum read speed in bytes per second.  

bps_rd_max_length=<seconds> 
    
Maximum length of read I/O bursts in seconds.  

bps_wr=<bps> 
    
Maximum write speed in bytes per second.  

bps_wr_max_length=<seconds> 
    
Maximum length of write I/O bursts in seconds.  

cache=<directsync | none | unsafe | writeback | writethrough> 
    
The drive’s cache mode  

detect_zeroes=<boolean> 
    
Controls whether to detect and try to optimize writes of zeroes.  

discard=<ignore | on> 
    
Controls whether to pass discard/trim requests to the underlying storage.  

file=<volume> 
    
The drive’s backing volume.  

format=<cloop | qcow | qcow2 | qed | raw | vmdk> 
    
The drive’s backing file’s data format.  

iops=<iops> 
    
Maximum r/w I/O in operations per second.  

iops_max=<iops> 
    
Maximum unthrottled r/w I/O pool in operations per second.  

iops_max_length=<seconds> 
    
Maximum length of I/O bursts in seconds.  

iops_rd=<iops> 
    
Maximum read I/O in operations per second.  

iops_rd_max=<iops> 
    
Maximum unthrottled read I/O pool in operations per second.  

iops_rd_max_length=<seconds> 
    
Maximum length of read I/O bursts in seconds.  

iops_wr=<iops> 
    
Maximum write I/O in operations per second.  

iops_wr_max=<iops> 
    
Maximum unthrottled write I/O pool in operations per second.  

iops_wr_max_length=<seconds> 
    
Maximum length of write I/O bursts in seconds.  

iothread=<boolean> 
    
Whether to use iothreads for this drive  

mbps=<mbps> 
    
Maximum r/w speed in megabytes per second.  

mbps_max=<mbps> 
    
Maximum unthrottled r/w pool in megabytes per second.  

mbps_rd=<mbps> 
    
Maximum read speed in megabytes per second.  

mbps_rd_max=<mbps> 
    
Maximum unthrottled read pool in megabytes per second.  

mbps_wr=<mbps> 
    
Maximum write speed in megabytes per second.  

mbps_wr_max=<mbps> 
    
Maximum unthrottled write pool in megabytes per second.  

media=<cdrom | disk> (_default =_ disk) 
    
The drive’s media type.  

replicate=<boolean> (_default =_ 1) 
    
Whether the drive should considered for replication jobs.  

rerror=<ignore | report | stop> 
    
Read error action.  

ro=<boolean> 
    
Whether the drive is read-only.  

serial=<serial> 
    
The drive’s reported serial number, url-encoded, up to 20 bytes long.  

shared=<boolean> (_default =_ 0) 
    
Mark this locally-managed volume as available on all nodes.   
| This option does not share the volume automatically, it assumes it is shared already!  |  
| --- | 

size=<DiskSize> 
      
Disk size. This is purely informational and has no effect.  

snapshot=<boolean> 
    
Controls qemu’s snapshot mode feature. If activated, changes made to the disk are temporary and will be discarded when the VM is shutdown.  

werror=<enospc | ignore | report | stop> 
    
Write error action.  

virtiofs[n]: [dirid=]<mapping-id> [,cache=<enum>] [,direct-io=<1|0>] [,expose-acl=<1|0>] [,expose-xattr=<1|0>] 
    
Configuration for sharing a directory between host and guest using Virtio-fs.  

cache=<always | auto | metadata | never> (_default =_ auto) 
    
The caching policy the file system should use (auto, always, metadata, never).  

direct-io=<boolean> (_default =_ 0) 
    
Honor the O_DIRECT flag passed down by guest applications.  

dirid=<mapping-id> 
    
Mapping identifier of the directory mapping to be shared with the guest. Also used as a mount tag inside the VM.  

expose-acl=<boolean> (_default =_ 0) 
    
Enable support for POSIX ACLs (enabled ACL implies xattr) for this mount.  

expose-xattr=<boolean> (_default =_ 0) 
    
Enable support for extended attributes for this mount.  

vmgenid: <UUID> (_default =_ 1 (autogenerated)) 
    
The VM generation ID (vmgenid) device exposes a 128-bit integer value identifier to the guest OS. This allows to notify the guest operating system when the virtual machine is executed with a different configuration (e.g. snapshot execution or creation from a template). The guest operating system notices the change, and is then able to react as appropriate by marking its copies of distributed databases as dirty, re-initializing its random number generator, etc. Note that auto-creation only works when done through API/CLI create or update methods, but not when manually editing the config file.  

vmstatestorage: <storage ID> 
    
Default storage for VM state volumes/files.  

watchdog: [[model=]<i6300esb|ib700>] [,action=<enum>] 
    
Create a virtual hardware watchdog device. Once enabled (by a guest action), the watchdog must be periodically polled by an agent inside the guest or else the watchdog will reset the guest (or execute the respective action specified)  

action=<debug | none | pause | poweroff | reset | shutdown> 
    
The action to perform if after activation the guest fails to poll the watchdog in time.  

model=<i6300esb | ib700> (_default =_ i6300esb) 
    
Watchdog type to emulate. 
##  Locks 
Online migrations, snapshots and backups (vzdump) set a lock to prevent incompatible concurrent actions on the affected VMs. Sometimes you need to remove such a lock manually (for example after a power failure).

```
# qm unlock <vmid>
```
  
| Only do that if you are sure the action which set the lock is no longer running.  |  
| --- |  
##  Files  

/etc/pve/qemu-server/<VMID>.conf 
    
Configuration file for the VM _< VMID>_. 
##  Copyright and Disclaimer 
Copyright © 2007-2022 Proxmox Server Solutions GmbH
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>
Version 9.2.10 Last updated Tue Sep 8 21:32:09 CEST 2026 
