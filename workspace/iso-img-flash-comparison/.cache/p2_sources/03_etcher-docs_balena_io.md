---
url: "https://etcher-docs.balena.io/USER-DOCUMENTATION/"
title: "Etcher User Documentation | Etcher"
scraped_at: 2026-09-09T15:13:52+00:00
---

[Skip to main content](https://etcher-docs.balena.io/USER-DOCUMENTATION/#__docusaurus_skipToContent_fallback)
On this page
This document contains how-tos and FAQs oriented to Etcher users.
## Config[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#config "Direct link to Config")
Etcher's configuration is saved to the `config.json` file in the apps folder. Not all the options are surfaced to the UI. You may edit this file to tweak settings even before launching the app.
## Why is my drive not bootable?[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#why-is-my-drive-not-bootable "Direct link to Why is my drive not bootable?")
Etcher copies images to drives byte by byte, without doing any transformation to the final device, which means images that require special treatment to be made bootable, like Windows images, will not work out of the box. In these cases, the general advice is to use software specific to those kind of images, usually available from the image publishers themselves.
Images known to require special treatment:
  * Microsoft Windows (use [Windows USB/DVD Download Tool](https://www.microsoft.com/en-us/download/windows-usb-dvd-download-tool), [Rufus](https://rufus.akeo.ie), or [WoeUSB](https://github.com/slacka/WoeUSB)).
  * Windows 10 IoT (use the [Windows 10 IoT Core Dashboard](https://developer.microsoft.com/en-us/windows/iot/downloads))


## How can I configure persistent storage?[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#how-can-i-configure-persistent-storage "Direct link to How can I configure persistent storage?")
Some programs, usually oriented at making GNU/Linux live USB drives, include an option to set persistent storage. This is currently not supported by Etcher, so if you require this functionality, we advise to fallback to [UNetbootin](https://unetbootin.github.io).
## Deactivate desktop shortcut prompt on GNU/Linux[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#deactivate-desktop-shortcut-prompt-on-gnulinux "Direct link to Deactivate desktop shortcut prompt on GNU/Linux")
This is a feature provided by [AppImages](http://appimage.org), where the applications prompts the user to automatically register a desktop shortcut to easily access the application.
To deactivate this feature, `touch` any of the files listed below:
  * `$HOME/.local/share/appimagekit/no_desktopintegration`
  * `/usr/share/appimagekit/no_desktopintegration`
  * `/etc/appimagekit/no_desktopintegration`


Alternatively, set the `SKIP` environment variable before executing the AppImage:

```
SKIP=1 ./Etcher-linux-<arch>.AppImage
```

## Flashing Ubuntu ISOs[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#flashing-ubuntu-isos "Direct link to Flashing Ubuntu ISOs")
Ubuntu images (and potentially some other related GNU/Linux distributions) have a peculiar format that allows the image to boot without any further modification from both CDs and USB drives.
A consequence of this enhancement is that some programs, like `parted` get confused about the drive's format and partition table, printing warnings such as:
> /dev/xxx contains GPT signatures, indicating that it has a GPT table. However, it does not have a valid fake msdos partition table, as it should. Perhaps it was corrupted -- possibly by a program that doesn't understand GPT partition tables. Or perhaps you deleted the GPT table, and are now using an msdos partition table. Is this a GPT partition table? Both the primary and backup GPT tables are corrupt. Try making a fresh table, and using Parted's rescue feature to recover partitions.
> Warning: The driver descriptor says the physical block size is 2048 bytes, but Linux says it is 512 bytes.
All these warnings are **safe to ignore** , and your drive should be able to boot without any problems.
Refer to [the following message from Ubuntu's mailing list](https://lists.ubuntu.com/archives/ubuntu-devel/2011-June/033495.html) if you want to learn more.
## Running on Wayland[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#running-on-wayland "Direct link to Running on Wayland")
Electron is based on Gtk2, which can't run natively on Wayland. Fortunately, the [XWayland Server](https://wayland.freedesktop.org/xserver.html) provides backwards compatibility to run _any_ X client on Wayland, including Etcher.
This usually works out of the box on mainstream GNU/Linux distributions that properly support Wayland. If it doesn't, make sure the `xwayland.so` module is being loaded by declaring it in your [weston.ini](http://manpages.ubuntu.com/manpages/wily/man5/weston.ini.5.html):

```
[core]modules=xwayland.so
```

## Runtime GNU/Linux dependencies[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#runtime-gnulinux-dependencies "Direct link to Runtime GNU/Linux dependencies")
This entry aims to provide an up to date list of runtime dependencies needed to run Etcher on a GNU/Linux system.
### Electron specific[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#electron-specific "Direct link to Electron specific")
> See [brightray's gyp file](https://github.com/electron/brightray/blob/master/brightray.gyp#L4)
  * gtk+-2.0
  * dbus-1
  * x11
  * xi
  * xcursor
  * xdamage
  * xrandr
  * xcomposite
  * xext
  * xfixes
  * xrender
  * xtst
  * xscrnsaver
  * gmodule-2.0
  * nss


### Optional dependencies:[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#optional-dependencies "Direct link to Optional dependencies:")
  * libnotify (for notifications)
  * libspeechd (for text-to-speech)


### Etcher specific:[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#etcher-specific "Direct link to Etcher specific:")
  * liblzma (for xz decompression)


## Recovering broken drives[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#recovering-broken-drives "Direct link to Recovering broken drives")
Sometimes, things might go wrong, and you end up with a half-flashed drive that is unusable by your operating systems, and common graphical tools might even refuse to get it back to a normal state.
To solve these kinds of problems, we've collected a list of fail-proof methods to completely erase your drive in major operating systems.
### Windows[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#windows "Direct link to Windows")
In Windows, we'll use [diskpart](https://technet.microsoft.com/en-us/library/cc770877\(v=ws.11\).aspx), a command line utility tool that comes pre-installed in all modern Windows versions.
  * Open `cmd.exe` from either the list of all installed applications, or from the "Run..." dialog usually accessible by pressing Ctrl+X.
  * Type `diskpart.exe` and press "Enter". You'll be asked to provide administrator permissions, and a new prompt window will appear. The following commands should be run **in the new window**.
  * Run `list disk` to list the available drives. Take note of the number id that identifies the drive you want to clean.
  * Run `select disk N`, where `N` corresponds to the id from the previous step.
  * Run `clean`. This command will completely clean your drive by erasing any existent filesystem.
  * Run `create partition primary`. This command will create a new partition.
  * Run `active`. This command will active the partition.
  * Run `list partition`. This command will show available partition.
  * Run `select partition N`, where `N` corresponds to the id of the newly available partition.
  * Run `format override quick`. This command will format the partition. You can choose a specific formatting by adding `FS=xx` where `xx` could be `NTFS or FAT or FAT32` after `format`. Example : `format FS=NTFS override quick`
  * Run `exit` to quit diskpart.


### OS X[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#os-x "Direct link to OS X")
Run the following command in `Terminal.app`, replacing `N` by the corresponding disk number, which you can find by running `diskutil list`:

```
diskutil eraseDisk FAT32 UNTITLED MBRFormat /dev/diskN
```

### GNU/Linux[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#gnulinux "Direct link to GNU/Linux")
Make sure the drive is unmounted (`umount /dev/xxx`), and run the following command as `root`, replacing `xxx` by your actual device path:

```
dd if=/dev/zero of=/dev/xxx bs=512 count=1 conv=notrunc
```

## "No polkit authentication agent found" error in GNU/Linux[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#no-polkit-authentication-agent-found-error-in-gnulinux "Direct link to "No polkit authentication agent found" error in GNU/Linux")
Etcher requires an available [polkit authentication agent](https://wiki.archlinux.org/index.php/Polkit#Authentication_agents) in your system in order to show a secure password prompt dialog to perform elevation. Make sure you have one installed for the desktop environment of your choice.
## Running in older macOS versions[​](https://etcher-docs.balena.io/USER-DOCUMENTATION/#running-in-older-macos-versions "Direct link to Running in older macOS versions")
Etcher GUI is based on the [Electron](https://electronjs.org/) framework, [which only supports macOS 10.10 (Yosemite) and newer versions](https://electronjs.org/docs/tutorial/support#supported-platforms).
See [PUBLISHING](https://etcher-docs.balena.io/PUBLISHING) for more details about release types.
  * [Why is my drive not bootable?](https://etcher-docs.balena.io/USER-DOCUMENTATION/#why-is-my-drive-not-bootable)
  * [How can I configure persistent storage?](https://etcher-docs.balena.io/USER-DOCUMENTATION/#how-can-i-configure-persistent-storage)
  * [Deactivate desktop shortcut prompt on GNU/Linux](https://etcher-docs.balena.io/USER-DOCUMENTATION/#deactivate-desktop-shortcut-prompt-on-gnulinux)
  * [Flashing Ubuntu ISOs](https://etcher-docs.balena.io/USER-DOCUMENTATION/#flashing-ubuntu-isos)
  * [Runtime GNU/Linux dependencies](https://etcher-docs.balena.io/USER-DOCUMENTATION/#runtime-gnulinux-dependencies)
    * [Optional dependencies:](https://etcher-docs.balena.io/USER-DOCUMENTATION/#optional-dependencies)
  * [Recovering broken drives](https://etcher-docs.balena.io/USER-DOCUMENTATION/#recovering-broken-drives)
  * ["No polkit authentication agent found" error in GNU/Linux](https://etcher-docs.balena.io/USER-DOCUMENTATION/#no-polkit-authentication-agent-found-error-in-gnulinux)
  * [Running in older macOS versions](https://etcher-docs.balena.io/USER-DOCUMENTATION/#running-in-older-macos-versions)


