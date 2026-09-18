---
url: "https://wiki.ubuntu.com/MountWindowsSharesPermanently"
title: "MountWindowsSharesPermanently - Ubuntu Wiki"
scraped_at: 2026-09-18T07:25:37+00:00
---



#  [Ubuntu Wiki](https://wiki.ubuntu.com/ "Ubuntu Wiki")
  * Immutable Page


  * [Ubuntu Wiki](https://wiki.ubuntu.com/Home)


##  [MountWindowsSharesPermanently](https://wiki.ubuntu.com/MountWindowsSharesPermanently)  
|  Contents
  1. [Prerequisites](https://wiki.ubuntu.com/MountWindowsSharesPermanently#Prerequisites)
  2. [CIFS installation](https://wiki.ubuntu.com/MountWindowsSharesPermanently#CIFS_installation)
  3. [Mounting unprotected (guest) network folders](https://wiki.ubuntu.com/MountWindowsSharesPermanently#Mounting_unprotected_.28guest.29_network_folders)
  4. [Mount password protected network folders](https://wiki.ubuntu.com/MountWindowsSharesPermanently#Mount_password_protected_network_folders)
    1. [Special permissions](https://wiki.ubuntu.com/MountWindowsSharesPermanently#Special_permissions)
    2. [Mount password protected shares using libpam_mount (Ubuntu 9.04)](https://wiki.ubuntu.com/MountWindowsSharesPermanently#Mount_password_protected_shares_using_libpam_mount_.28Ubuntu_9.04.29)
  5. [Troubleshooting](https://wiki.ubuntu.com/MountWindowsSharesPermanently#Troubleshooting)
    1. [Unprotected network folder won't automount](https://wiki.ubuntu.com/MountWindowsSharesPermanently#Unprotected_network_folder_won.27t_automount)
    2. [Mount during login instead of boot](https://wiki.ubuntu.com/MountWindowsSharesPermanently#Mount_during_login_instead_of_boot)
    3. [Slow shutdown due to a CIFS/Network Manager bug](https://wiki.ubuntu.com/MountWindowsSharesPermanently#Slow_shutdown_due_to_a_CIFS.2FNetwork_Manager_bug)
    4. [CIFS Options Deprecated](https://wiki.ubuntu.com/MountWindowsSharesPermanently#CIFS_Options_Deprecated)
    5. [Use of tilde in pathnames such as "credentials=~/.smbcredentials"](https://wiki.ubuntu.com/MountWindowsSharesPermanently#Use_of_tilde_in_pathnames_such_as_.22credentials.3D.2BAH4-.2F.smbcredentials.22)

 |  
| --- |  
This document describes how to mount CIFS shares permanently. The shares might be hosted on a Windows computer/server, or on a Linux/UNIX server running [Samba](https://help.ubuntu.com/community/Samba). This document also applies to SMBFS shares, which are similar to CIFS but are deprecated and should be avoided if possible ([link](https://bugzilla.samba.org/show_bug.cgi?id=1920#c0)). 
(This document does _not_ describe how to host the shares yourself, only how to access shares that are hosted somewhere else. For hosting shares, use [Samba](https://help.ubuntu.com/community/Samba).) 
# Prerequisites
We're assuming that: 
  * Network connections have been configured properly. 
  * Your local (Ubuntu) username is _ubuntuusername_. 
  * Share username on Windows computer is _msusername_. 
  * Share password on Windows computer is _mspassword_. 
  * The Windows computer's name is _servername_ (this can be either an IP address or an assigned name). 
  * The name of the share is _sharename_. 
  * You want to mount the share in _/media/windowsshare_. 


# CIFS installation

```
sudo apt-get install cifs-utils
```

On older systems: 

```
sudo apt-get install smbfs
```

# Mounting unprotected (guest) network folders
First, let's create the mount directory. You will need a separate directory for each mount. 

```
sudo mkdir /media/windowsshare
```

Then edit your /etc/fstab file (with root privileges) to add this line: 

```
//servername/sharename  /media/windowsshare  cifs  guest,uid=1000,iocharset=utf8  0  0
```

Where 
  * **guest** indicates you don't need a password to access the share, 
  * **uid=1000** makes the Linux user specified by the id the owner of the mounted share, allowing them to rename files, 
  * **iocharset=utf8** allows access to files with names in non-English languages. This doesn't work with shares of devices like the Buffalo Tera Station, or Windows machines that export their shares using ISO8895-15. 
  * If there is any **space in the server path** , you need to replace it by \040, for example //servername/My\040Documents 


After you add the entry to /etc/fstab type: 

```
sudo mount -a
```

This will (re)mount all entries listed in /etc/fstab. 
# Mount password protected network folders
The quickest way to auto-mounting a password-protected share is to edit /etc/fstab (with root privileges), to add this line: 

```
//servername/sharename  /media/windowsshare  cifs  username=msusername,password=mspassword,iocharset=utf8  0  0
```

This is not a good idea however: /etc/fstab is readable by everyone and so is your Windows password in it. The way around this is to use a credentials file. This is a file that contains just the username and password. 
Using a text editor, create a file for your remote servers logon credential: 

```
gedit ~/.smbcredentials
```

Enter your Windows username and password in the file: 

```
username=msusername
password=mspassword
```

Save the file, exit the editor. 
Change the permissions of the file to prevent unwanted access to your credentials: 

```
chmod 600 ~/.smbcredentials
```

Then edit your /etc/fstab file (with root privileges) to add this line (replacing the insecure line in the example above, if you added it): 

```
//servername/sharename /media/windowsshare cifs credentials=/home/ubuntuusername/.smbcredentials,iocharset=utf8 0 0 
```

Save the file, exit the editor. 
Finally, test the fstab entry by issuing: 

```
sudo mount -a
```

If there are no errors, you should test how it works after a reboot. Your remote share should mount automatically. 
## Special permissions
If you need special permission (like chmod etc.), you'll need to add a _uid_ (short for 'user id') or _gid_ (for 'group id') parameter to the share's mount options. 

```
//servername/sharename  /media/windowsshare  cifs   uid=ubuntuuser,credentials=/home/ubuntuuser/.smbcredentials,iocharset=utf8   0       0
```

## Mount password protected shares using libpam_mount (Ubuntu 9.04)
In addition to the initial assumptions, we're assuming that 
  * **Your username and password are the same on the Ubuntu machine and on the network drive.**


Install libpam-mount: 

```
sudo apt-get install libpam-mount
```

Edit /etc/security/pam_mount.conf.xml using your preferred text editor. 

```
gksudo gedit /etc/security/pam_mount.conf.xml
```

First, we're moving the user specific config bits to a file which users can actually edit themselves: remove the commenting tags (<!-- and -->) surrounding the section called <luserconf name=".pam_mount.conf.xml" />. Save the file when done. With this in place, users can create their own ~/.pam_mount.conf.xml. 

```
gedit ~/.pam_mount.conf.xml
```

Add the following: 

```
<?xml version="1.0" encoding="utf-8" ?>

<pam_mount>

<volume options="uid=%(USER),gid=100,dmask=0700" user="*" mountpoint="/media/windowsshare" path="sharename" server="servername" fstype="cifs" />

</pam_mount>
```

# Troubleshooting
## Login errors
If you get the error "mount error(13) permission denied", then the server denied your access. Here are the first things to check: 
  * Are you using a valid username and password? Does that account really have access to this folder? 
  * Do you have whitespace in your credentials file? It should be `password=mspassword`, not `password = mspassword`. 
  * Do you need a domain? For example, if you are told that your username is `SALES\sally`, then actually your username is `sally` and your domain is `SALES`. The fstab entry should read: `...username=sally,password=pass,domain=SALES,...` Or: `...credentials=/path/to/file,domain=SALES,...`
  * The security and version settings are interrelated. SMB1 is insecure and no longer supported by default. At first, try to not specify either security or version: do not specify `sec=` or `vers=`. If you still have authentication errors then you may need to specify either `sec=` or `vers=` or both. You can try the options listed at the [mount.cifs man page](http://manpages.ubuntu.com/manpages/raring/en/man8/mount.cifs.8.html). The man page list leaves out the option `sec=lanman` for some reason, but you should try that one as well ([see discussion](https://bugs.launchpad.net/ubuntu/+source/cifs-utils/+bug/1113395)). 


## Unprotected network folder won't automount
I've had a situation where an unprotected network folder wouldn't automount during bootup, but after manually entering "sudo mount -a" was mounted correctly. I solved this by replacing the "guest" option by "username=guest,password=". If anyone has an explanation for this, please leave a comment. 

```
//servername/sharename  /media/windowsshare  smbfs  username=guest,password=,uid=1000,iocharset=utf8,codepage=unicode,unicode  0  0
```

## Mount during login instead of boot
If for some reason/etc/rc0.d/S31umountnfs.sh (networking problems for example) the automatic mounting during boot doesn't work, you can add the "noauto" parameter to your smbfs fstab entry and then have the share mounted at login. 
In /etc/fstab: 

```
//servername/sharename  /media/windowsshare  cifs  noauto,credentials=/home/ubuntuusername/.smbpasswd  0  0
```

In /etc/rc.local: 

```
mount /media/windowsshare
exit 0
```

## Slow shutdown due to a CIFS/Network Manager bug
If you use Network Manager, and are getting really slow shutdowns, it's probably because NM shuts down before unmounting the network shares. That will cause CIFS to hang and wait for 60 seconds or so. Here's how to fix it:/etc/rc0.d/S31umountnfs.sh 

```
sudo ln -s /etc/init.d/umountnfs.sh /etc/rc0.d/K14umountnfs.sh
sudo ln -s /etc/init.d/umountnfs.sh /etc/rc6.d/K14umountnfs.sh
```

Ubuntu 12.04 already runs **umountnfs.sh** at reboot and shutdown by default (/etc/rc0.d/S31umountnfs.sh and /etc/rc6.d/S31umountnfs.sh) so this is no longer necessary. 
## CIFS Options Deprecated
20 Feb 2008 TW 
Using dmask or fmask in the fstab file produces the following warnings: WARNING: CIFS mount option 'dmask' is deprecated. Use 'dir_mode' instead. WARNING: CIFS mount option 'fmask' is deprecated. Use 'file_mode' instead. 
Instead use this format: file_mode=0777,dir_mode=0777 . Or in some cases you might need to use file_mode=0777,dir_mode=0777,nounix ([see discussion](http://superuser.com/a/410561)) 
## Use of tilde in pathnames such as "credentials=~/.smbcredentials"
20 Feb 2008 TW 
Curiously, using credentials=~/.smbcredentials in fstab didn't work. I had to use the full path, i.e. /home/username/.smbcredentials 
(This is likely because the tilde "~" is only a shell short-hand alias for "$HOME"; it isn't something recognized system-wide by all programs, especially not in a system file table where the concept of "HOME" doesn't really exist. -Ian!) 
[CategoryDocumentation](https://wiki.ubuntu.com/CategoryDocumentation)
MountWindowsSharesPermanently (last edited 2024-04-18 09:12:09 by )
The material on this wiki is available under a free license, see [Copyright / License](https://help.ubuntu.com/community/License) for details. 
