---
url: "https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html"
title: "systemd.mount(5) — systemd — Debian trixie — Debian Manpages"
scraped_at: 2026-09-18T07:26:29+00:00
---

[MANPAGES](https://manpages.debian.org/)
[Skip Quicknav](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#content)
  * [About Manpages](https://manpages.debian.org/about.html)
  * [Service Information](https://wiki.debian.org/manpages.debian.org)


/ [trixie](https://manpages.debian.org/contents-trixie.html) / [systemd](https://manpages.debian.org/trixie/systemd/index.html) / systemd.mount(5) 
links 
  * [language-indep link](https://manpages.debian.org/trixie/systemd/systemd.mount.5)


table of contents 
  * [AUTOMATIC DEPENDENCIES](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#AUTOMATIC_DEPENDENCIES "AUTOMATIC DEPENDENCIES")


other versions 
  * [trixie](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html) 257.13-1~deb13u1
  * [testing](https://manpages.debian.org/testing/systemd/systemd.mount.5.en.html) 261.2-1
  * [unstable](https://manpages.debian.org/unstable/systemd/systemd.mount.5.en.html) 262~rc3-1


other languages 


[Scroll to navigation](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#panels)  
| SYSTEMD.MOUNT(5)  | systemd.mount  | SYSTEMD.MOUNT(5)  |  
| --- | --- | --- |  
# NAME[¶](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#NAME)
systemd.mount - Mount unit configuration
# SYNOPSIS[¶](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#SYNOPSIS)
_mount_.mount
# DESCRIPTION[¶](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#DESCRIPTION)
A unit configuration file whose name ends in ".mount" encodes information about a file system mount point controlled and supervised by systemd.
This man page lists the configuration options specific to this unit type. See [systemd.unit(5)](https://manpages.debian.org/trixie/systemd/systemd.unit.5.en.html) for the common options of all unit configuration files. The common configuration items are configured in the generic [Unit] and [Install] sections. The mount specific configuration options are configured in the [Mount] section.
Additional options are listed in [systemd.exec(5)](https://manpages.debian.org/trixie/systemd/systemd.exec.5.en.html), which define the execution environment the [mount(8)](https://manpages.debian.org/trixie/mount/mount.8.en.html) program is executed in, and in [systemd.kill(5)](https://manpages.debian.org/trixie/systemd/systemd.kill.5.en.html), which define the way the processes are terminated, and in [systemd.resource-control(5)](https://manpages.debian.org/trixie/systemd/systemd.resource-control.5.en.html), which configure resource control settings for the processes of the service.
Note that the options _User=_ and _Group=_ are not useful for mount units. systemd passes two parameters to [mount(8)](https://manpages.debian.org/trixie/mount/mount.8.en.html); the values of _What=_ and _Where=_. When invoked in this way, [mount(8)](https://manpages.debian.org/trixie/mount/mount.8.en.html) does not read any options from /etc/fstab, and must be run as UID 0.
Mount units must be named after the mount point directories they control. Example: the mount point /home/lennart must be configured in a unit file home-lennart.mount. For details about the escaping logic used to convert a file system path to a unit name, see [systemd.unit(5)](https://manpages.debian.org/trixie/systemd/systemd.unit.5.en.html). Note that mount units cannot be templated, nor is possible to add multiple names to a mount unit by creating symlinks to its unit file.
Optionally, a mount unit may be accompanied by an automount unit, to allow on-demand or parallelized mounting. See [systemd.automount(5)](https://manpages.debian.org/trixie/systemd/systemd.automount.5.en.html).
Mount points created at runtime (independently of unit files or /etc/fstab) will be monitored by systemd and appear like any other mount unit in systemd. See /proc/self/mountinfo description in [proc(5)](https://manpages.debian.org/trixie/manpages/proc.5.en.html).
Some file systems have special semantics as API file systems for kernel-to-userspace and userspace-to-userspace interfaces. Some of them may not be changed via mount units, and cannot be disabled. For a longer discussion see **API File Systems**[1].
The [systemd-mount(1)](https://manpages.debian.org/trixie/systemd/systemd-mount.1.en.html) command allows creating .mount and .automount units dynamically and transiently from the command line.
# AUTOMATIC DEPENDENCIES[¶](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#AUTOMATIC_DEPENDENCIES)
## Implicit Dependencies[¶](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#Implicit_Dependencies)
The following dependencies are implicitly added:
•If a mount unit is beneath another mount unit in the file system hierarchy, both a requirement dependency and an ordering dependency between both units are created automatically.
•Block device backed file systems automatically gain _Requires=_ , _StopPropagatedFrom=_ , and _After=_ type dependencies on the device unit encapsulating the block device (see _x-systemd.device-bound=_ for details).
•If traditional file system quota is enabled for a mount unit, automatic _Wants=_ and _Before=_ dependencies on systemd-quotacheck.service and quotaon.service are added.
•Additional implicit dependencies may be added as result of execution and resource control parameters as documented in [systemd.exec(5)](https://manpages.debian.org/trixie/systemd/systemd.exec.5.en.html) and [systemd.resource-control(5)](https://manpages.debian.org/trixie/systemd/systemd.resource-control.5.en.html).
## Default Dependencies[¶](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#Default_Dependencies)
The following dependencies are added unless _DefaultDependencies=no_ is set:
•All mount units acquire automatic _Before=_ and _Conflicts=_ on umount.target in order to be stopped during shutdown.
•Mount units referring to local file systems automatically gain an _After=_ dependency on local-fs-pre.target, and a _Before=_ dependency on local-fs.target unless one or more mount options among **nofail** , **x-systemd.wanted-by=** , and **x-systemd.required-by=** is set. See below for detailed information. 
Additionally, an _After=_ dependency on swap.target is added when the file system type is "tmpfs".
•Network mount units automatically acquire _After=_ dependencies on remote-fs-pre.target, network.target, plus _After=_ and _Wants=_ dependencies on network-online.target, and a _Before=_ dependency on remote-fs.target, unless one or more mount options among **nofail** , **x-systemd.wanted-by=** , and **x-systemd.required-by=** is set.
Mount units referring to local and network file systems are distinguished by their file system type specification. In some cases this is not sufficient (for example network block device based mounts, such as iSCSI), in which case **_netdev** may be added to the mount option string of the unit, which forces systemd to consider the mount unit a network mount.
# FSTAB[¶](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#FSTAB)
Mount units may either be configured via unit files, or via /etc/fstab (see [fstab(5)](https://manpages.debian.org/trixie/mount/fstab.5.en.html) for details). Mounts listed in /etc/fstab will be converted into native units dynamically at boot and when the configuration of the system manager is reloaded. In general, configuring mount points through /etc/fstab is the preferred approach to manage mounts for humans. For tooling, writing mount units should be preferred over editing /etc/fstab. See [systemd-fstab-generator(8)](https://manpages.debian.org/trixie/systemd/systemd-fstab-generator.8.en.html) for details about the conversion from /etc/fstab to mount units.
The NFS mount option **bg** for NFS background mounts as documented in [nfs(5)](https://manpages.debian.org/trixie/nfs-common/nfs.5.en.html) is detected by **systemd-fstab-generator** and the options are transformed so that systemd fulfills the job-control implications of that option. Specifically **systemd-fstab-generator** acts as though "x-systemd.mount-timeout=infinity,retry=10000" was prepended to the option list, and "fg,nofail" was appended. Depending on specific requirements, it may be appropriate to provide some of these options explicitly, or to make use of the "x-systemd.automount" option described below instead of using "bg".
When reading /etc/fstab a few special mount options are understood by systemd which influence how dependencies are created for mount points. systemd will create a dependency of type _Wants=_ or **Requires=** (see option **nofail** below), from either local-fs.target or remote-fs.target, depending whether the file system is local or remote.
**x-systemd.requires=**
Configures a _Requires=_ and an _After=_ dependency between the created mount unit and another systemd unit, such as a device or mount unit. The argument should be a unit name, or an absolute path to a device node or mount point. This option may be specified more than once. This option is particularly useful for mount point declarations that need an additional device to be around (such as an external journal device for journal file systems) or an additional mount to be in place (such as an overlay file system that merges multiple mount points). See _After=_ and _Requires=_ in [systemd.unit(5)](https://manpages.debian.org/trixie/systemd/systemd.unit.5.en.html) for details. 
Note that this option always applies to the created mount unit only regardless whether **x-systemd.automount** has been specified.
Added in version 220.
**x-systemd.wants=**
Configures a _Wants=_ and an _After=_ dependency between the created mount unit and another systemd unit, similar to the _x-systemd.requires=_ option. 
Added in version 257.
**x-systemd.before=** , **x-systemd.after=**
In the created mount unit, configures a _Before=_ or _After=_ dependency on another systemd unit, such as a mount unit. The argument should be a unit name or an absolute path to a mount point. This option may be specified more than once. This option is particularly useful for mount point declarations with **nofail** option that are mounted asynchronously but need to be mounted before or after some unit start, for example, before local-fs.target unit. See _Before=_ and _After=_ in [systemd.unit(5)](https://manpages.debian.org/trixie/systemd/systemd.unit.5.en.html) for details. 
Note that these options always apply to the created mount unit only regardless whether **x-systemd.automount** has been specified.
Added in version 233.
**x-systemd.wanted-by=** , **x-systemd.required-by=**
In the created mount unit, configures a _WantedBy=_ or _RequiredBy=_ dependency on another unit. This option may be specified more than once. If this is specified, the default dependencies (see above) other than umount.target on the created mount unit, e.g. local-fs.target, are not automatically created. Hence it is likely that some ordering dependencies need to be set up manually through **x-systemd.before=** and **x-systemd.after=**. See _WantedBy=_ and _RequiredBy=_ in [systemd.unit(5)](https://manpages.debian.org/trixie/systemd/systemd.unit.5.en.html) for details. 
Added in version 245.
**x-systemd.wants-mounts-for=** , **x-systemd.requires-mounts-for=**
Configures a _RequiresMountsFor=_ or _WantsMountsFor=_ dependency between the created mount unit and other mount units. The argument must be an absolute path. This option may be specified more than once. See _RequiresMountsFor=_ or _WantsMountsFor=_ in [systemd.unit(5)](https://manpages.debian.org/trixie/systemd/systemd.unit.5.en.html) for details. 
Added in version 220.
**x-systemd.device-bound=**
Takes a boolean argument. If true or no argument, a _BindsTo=_ dependency on the backing device is set. If false, the mount unit is not stopped no matter whether the backing device is still present. This is useful when the file system is backed by volume managers. If not set, and the mount comes from unit fragments, i.e. generated from /etc/fstab by [systemd-fstab-generator(8)](https://manpages.debian.org/trixie/systemd/systemd-fstab-generator.8.en.html) or loaded from a manually configured mount unit, a combination of _Requires=_ and _StopPropagatedFrom=_ dependencies is set on the backing device, otherwise only _Requires=_ is used. 
Added in version 233.
**x-systemd.automount**
An automount unit will be created for the file system. See [systemd.automount(5)](https://manpages.debian.org/trixie/systemd/systemd.automount.5.en.html) for details. 
Added in version 215.
**x-systemd.idle-timeout=**
Configures the idle timeout of the automount unit. See _TimeoutIdleSec=_ in [systemd.automount(5)](https://manpages.debian.org/trixie/systemd/systemd.automount.5.en.html) for details. 
Added in version 220.
**x-systemd.device-timeout=**
Configure how long systemd should wait for a device to show up before giving up on an entry from /etc/fstab. Specify a time in seconds or explicitly append a unit such as "s", "min", "h", "ms". 
Note that this option can only be used in /etc/fstab, and will be ignored when part of the _Options=_ setting in a unit file.
Added in version 215.
**x-systemd.mount-timeout=**
Configure how long systemd should wait for the mount command to finish before giving up on an entry from /etc/fstab. Specify a time in seconds or explicitly append a unit such as "s", "min", "h", "ms". 
Note that this option can only be used in /etc/fstab, and will be ignored when part of the _Options=_ setting in a unit file.
See _TimeoutSec=_ below for details.
Added in version 233.
**x-systemd.makefs**
The file system will be initialized on the device. If the device is not "empty", i.e. it contains any signature, the operation will be skipped. It is hence expected that this option remains set even after the device has been initialized. 
Note that this option can only be used in /etc/fstab, and will be ignored when part of the _Options=_ setting in a unit file.
See **systemd-makefs@.service**(8).
[wipefs(8)](https://manpages.debian.org/trixie/util-linux/wipefs.8.en.html) may be used to remove any signatures from a block device to force **x-systemd.makefs** to reinitialize the device.
Added in version 236.
**x-systemd.growfs**
The file system will be grown to occupy the full block device. If the file system is already at maximum size, no action will be performed. It is hence expected that this option remains set even after the file system has been grown. Only certain file system types are supported, see **systemd-makefs@.service**(8) for details. 
Note that this option can only be used in /etc/fstab, and will be ignored when part of the _Options=_ setting in a unit file.
Added in version 236.
**x-systemd.pcrfs**
Measures file system identity information (mount point, type, label, UUID, partition label, partition UUID) into PCR 15 after the file system has been mounted. This ensures the **systemd-pcrfs@.service**(8) or systemd-pcrfs-root.service services are pulled in by the mount unit. 
Note that this option can only be used in /etc/fstab, and will be ignored when part of the _Options=_ setting in a unit file. It is also implied for the root and /usr/ partitions discovered by [systemd-gpt-auto-generator(8)](https://manpages.debian.org/trixie/systemd/systemd-gpt-auto-generator.8.en.html).
Added in version 253.
**x-systemd.rw-only**
If a mount operation fails to mount the file system read-write, it normally tries mounting the file system read-only instead. This option disables that behaviour, and causes the mount to fail immediately instead. This option is translated into the _ReadWriteOnly=_ setting in a unit file. 
Added in version 246.
**_netdev**
Normally the file system type is used to determine if a mount is a "network mount", i.e. if it should only be started after the network is available. Using this option overrides this detection and specifies that the mount requires network. 
Network mount units are ordered between remote-fs-pre.target and remote-fs.target, instead of local-fs-pre.target and local-fs.target. They also pull in network-online.target and are ordered after it and network.target.
Added in version 235.
**noauto** , **auto**
With **noauto** , the mount unit will not be added as a dependency for local-fs.target or remote-fs.target. This means that it will not be mounted automatically during boot, unless it is pulled in by some other unit. The **auto** option has the opposite meaning and is the default. 
Note that if **x-systemd.automount** (see above) is used, neither **auto** nor **noauto** have any effect. The matching automount unit will be added as a dependency to the appropriate target.
Added in version 215.
**nofail**
With **nofail** , this mount will be only wanted, not required, by local-fs.target or remote-fs.target. Moreover, the mount unit is not ordered before these target units. This means that the boot will continue without waiting for the mount unit and regardless whether the mount point can be mounted successfully. 
Added in version 215.
**x-initrd.mount**
An additional filesystem to be mounted in the initrd. See initrd-fs.target description in [systemd.special(7)](https://manpages.debian.org/trixie/systemd/systemd.special.7.en.html). This is both an indicator to the initrd to mount this partition early and an indicator to the host to leave the partition mounted until final shutdown. Or in other words, if this flag is set it is assumed the mount shall be active during the entire regular runtime of the system, i.e. established before the initrd transitions into the host all the way until the host transitions to the final shutdown phase. 
Added in version 215.
If a mount point is configured in both /etc/fstab and a unit file that is stored below /usr/, the former will take precedence. If the unit file is stored below /etc/, it will take precedence. This means: native unit files take precedence over traditional configuration files, but this is superseded by the rule that configuration in /etc/ will always take precedence over configuration in /usr/.
# OPTIONS[¶](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#OPTIONS)
Mount unit files may include [Unit] and [Install] sections, which are described in [systemd.unit(5)](https://manpages.debian.org/trixie/systemd/systemd.unit.5.en.html).
Mount unit files must include a [Mount] section, which carries information about the file system mount points it supervises. A number of options that may be used in this section are shared with other unit types. These options are documented in [systemd.exec(5)](https://manpages.debian.org/trixie/systemd/systemd.exec.5.en.html), [systemd.kill(5)](https://manpages.debian.org/trixie/systemd/systemd.kill.5.en.html) and [systemd.resource-control(5)](https://manpages.debian.org/trixie/systemd/systemd.resource-control.5.en.html). The options specific to the [Mount] section of mount units are the following:
_What=_
Takes an absolute path or a fstab-style identifier of a device node, file or other resource to mount. See [mount(8)](https://manpages.debian.org/trixie/mount/mount.8.en.html) for details. If this refers to a device node, a dependency on the respective device unit is automatically created. (See [systemd.device(5)](https://manpages.debian.org/trixie/systemd/systemd.device.5.en.html) for more information.) This option is mandatory. Note that the usual specifier expansion is applied to this setting, literal percent characters should hence be written as "%%". If this mount is a bind mount and the specified path does not exist yet it is created as directory.
_Where=_
Takes an absolute path of a file or directory for the mount point; in particular, the destination cannot be a symbolic link. If the mount point does not exist at the time of mounting, it is created as either a directory or a file. The former is the usual case; the latter is done only if this mount is a bind mount and the source (_What=_) is not a directory. This string must be reflected in the unit filename. (See above.) This option is mandatory.
_Type=_
Takes a string for the file system type. See [mount(8)](https://manpages.debian.org/trixie/mount/mount.8.en.html) for details. This setting is optional. 
If the type is "overlay", and "upperdir=" or "workdir=" are specified as options and the directories do not exist, they will be created.
_Options=_
Mount options to use when mounting. This takes a comma-separated list of options. This setting is optional. Note that the usual specifier expansion is applied to this setting, literal percent characters should hence be written as "%%".
_SloppyOptions=_
Takes a boolean argument. If true, parsing of the options specified in _Options=_ is relaxed, and unknown mount options are tolerated. This corresponds with [mount(8)](https://manpages.debian.org/trixie/mount/mount.8.en.html)'s _-s_ switch. Defaults to off. 
Added in version 215.
_LazyUnmount=_
Takes a boolean argument. If true, detach the filesystem from the filesystem hierarchy at time of the unmount operation, and clean up all references to the filesystem as soon as they are not busy anymore. This corresponds with [umount(8)](https://manpages.debian.org/trixie/mount/umount.8.en.html)'s _-l_ switch. Defaults to off. 
Added in version 232.
_ReadWriteOnly=_
Takes a boolean argument. If false, a mount point that shall be mounted read-write but cannot be mounted so is retried to be mounted read-only. If true the operation will fail immediately after the read-write mount attempt did not succeed. This corresponds with [mount(8)](https://manpages.debian.org/trixie/mount/mount.8.en.html)'s _-w_ switch. Defaults to off. 
Added in version 246.
_ForceUnmount=_
Takes a boolean argument. If true, force an unmount (in case of an unreachable NFS system). This corresponds with [umount(8)](https://manpages.debian.org/trixie/mount/umount.8.en.html)'s _-f_ switch. Defaults to off. 
Added in version 232.
_DirectoryMode=_
Directories of mount points (and any parent directories) are automatically created if needed. This option specifies the file system access mode used when creating these directories. Takes an access mode in octal notation. Defaults to 0755.
_TimeoutSec=_
Configures the time to wait for the mount command to finish. If a command does not exit within the configured time, the mount will be considered failed and be shut down again. All commands still running will be terminated forcibly via **SIGTERM** , and after another delay of this time with **SIGKILL**. (See **KillMode=** in [systemd.kill(5)](https://manpages.debian.org/trixie/systemd/systemd.kill.5.en.html).) Takes a unit-less value in seconds, or a time span value such as "5min 20s". Pass 0 to disable the timeout logic. The default value is set from _DefaultTimeoutStartSec=_ option in [systemd-system.conf(5)](https://manpages.debian.org/trixie/systemd/systemd-system.conf.5.en.html).
Check [systemd.unit(5)](https://manpages.debian.org/trixie/systemd/systemd.unit.5.en.html), [systemd.exec(5)](https://manpages.debian.org/trixie/systemd/systemd.exec.5.en.html), and [systemd.kill(5)](https://manpages.debian.org/trixie/systemd/systemd.kill.5.en.html) for more settings.
# SEE ALSO[¶](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#SEE_ALSO)
[systemd(1)](https://manpages.debian.org/trixie/systemd/systemd.1.en.html), [systemctl(1)](https://manpages.debian.org/trixie/systemd/systemctl.1.en.html), [systemd-system.conf(5)](https://manpages.debian.org/trixie/systemd/systemd-system.conf.5.en.html), [systemd.unit(5)](https://manpages.debian.org/trixie/systemd/systemd.unit.5.en.html), [systemd.exec(5)](https://manpages.debian.org/trixie/systemd/systemd.exec.5.en.html), [systemd.kill(5)](https://manpages.debian.org/trixie/systemd/systemd.kill.5.en.html), [systemd.resource-control(5)](https://manpages.debian.org/trixie/systemd/systemd.resource-control.5.en.html), [systemd.service(5)](https://manpages.debian.org/trixie/systemd/systemd.service.5.en.html), [systemd.device(5)](https://manpages.debian.org/trixie/systemd/systemd.device.5.en.html), [proc(5)](https://manpages.debian.org/trixie/manpages/proc.5.en.html), [mount(8)](https://manpages.debian.org/trixie/mount/mount.8.en.html), [systemd-fstab-generator(8)](https://manpages.debian.org/trixie/systemd/systemd-fstab-generator.8.en.html), [systemd.directives(7)](https://manpages.debian.org/trixie/systemd/systemd.directives.7.en.html), [systemd-mount(1)](https://manpages.debian.org/trixie/systemd/systemd-mount.1.en.html)
# NOTES[¶](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html#NOTES) 

1.
    API File Systems
<https://systemd.io/API_FILE_SYSTEMS>  
| systemd 257.13  |  
| --- |  
|  Source file:   |  systemd.mount.5.en.gz (from [systemd 257.13-1~deb13u1](http://snapshot.debian.org/package/systemd/257.13-1~deb13u1/))   |  
| --- | --- |  
|  Source last updated:   |  2026-04-13T19:38:05Z   |  
|  Converted to HTML:   |  2026-09-15T20:47:56Z   |  
debiman df2f1b6, see [github.com/Debian/debiman](https://github.com/Debian/debiman/). Found a problem? See the [FAQ](https://manpages.debian.org/faq.html).
