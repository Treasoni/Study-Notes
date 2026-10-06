---
url: "https://lists.freedesktop.org/archives/systemd-devel/2024-June/050463.html"
title: "[systemd-devel] mounts with \"nofail\" can be unmounted on shutdown before \"After=*-fs.target\" units"
scraped_at: 2026-09-18T07:25:37+00:00
---

# [systemd-devel] mounts with "nofail" can be unmounted on shutdown before "After=*-fs.target" units
**MichaIng**
micha at dietpi.com 
_Sat Jun 29 17:26:03 UTC 2024_
  * Previous message (by thread): [[systemd-devel] Default run0 background colors not working ](https://lists.freedesktop.org/archives/systemd-devel/2024-June/050462.html)
  * Next message (by thread): [[systemd-devel] systemd --user managers after systemd upgrade ](https://lists.freedesktop.org/archives/systemd-devel/2024-June/050464.html)
  * **Messages sorted by:** [[ date ]](https://lists.freedesktop.org/archives/systemd-devel/2024-June/date.html#50463) [[ thread ]](https://lists.freedesktop.org/archives/systemd-devel/2024-June/thread.html#50463) [[ subject ]](https://lists.freedesktop.org/archives/systemd-devel/2024-June/subject.html#50463) [[ author ]](https://lists.freedesktop.org/archives/systemd-devel/2024-June/author.html#50463)



```
Hey guys, I have question regarding a certain behaviour of the systemd 
mount generator.

Mounts do not have `Before=*-fs.target` if the `nofail` mount option is 
added to their `/etc/fstab` entry.

 From the man page I see that this is intended behaviour:
- 
https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html#Default%20Dependencies[](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html#Default%20Dependencies)
- 
https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html#noauto[](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html#noauto)

First of all, I see the reason why it seems to be not important for 
mounts to start before certain targets, if one explicitly declares that 
it is okay for them to fail. But I do not see a downside of adding 
`Before=*-fs.target` either. There are use cases where one still wants 
other services to wait for at least the attempt to have all network 
shares mounted, even when not wanting some of them to cause failure in 
the boot sequence.

The more problematic implication however is indeed, that those mounts 
can be attempted to be unmounted on shutdown, before services with 
`After=*-fs.target` are stopped. This can lead to hanging services and 
potential data loss. It has been observed with qBittorrent and a CIFS 
network share in particular, where the CIFS mount was tried to be 
unmounted first, failed, since it was accessed by qBittorrent, and for 
some reason was hanging the shutdown sequence, so that the system needed 
to be power cycled. Doing the unmount manually before shutdown, solves 
the issue. This was when I found the missing `Before=remote-fs.target` 
entry.

Is there a particular reason `nofail` mounts do not have 
`Before=*-fs.target` defined, respectively is there any downside when 
defining it as well with `nofail`? One thing I have in mind, is that 
hanging mount attempts delay `remote-fs.target` and hence 
`getty at .service[](https://lists.freedesktop.org/mailman/listinfo/systemd-devel)` units, i.e. the local login prompt. However, if I want 
to avoid this, because I am expecting the share to be offline regularly, 
then I would would use `noauto`, in case with `x-systemd.automount`. But 
I did not expect the `nofail` option to be a "mount at any later time on 
boot" + "unmount at any earlier time on shutdown".

Best regards,

Micha

```

  * Previous message (by thread): [[systemd-devel] Default run0 background colors not working ](https://lists.freedesktop.org/archives/systemd-devel/2024-June/050462.html)
  * Next message (by thread): [[systemd-devel] systemd --user managers after systemd upgrade ](https://lists.freedesktop.org/archives/systemd-devel/2024-June/050464.html)
  * **Messages sorted by:** [[ date ]](https://lists.freedesktop.org/archives/systemd-devel/2024-June/date.html#50463) [[ thread ]](https://lists.freedesktop.org/archives/systemd-devel/2024-June/thread.html#50463) [[ subject ]](https://lists.freedesktop.org/archives/systemd-devel/2024-June/subject.html#50463) [[ author ]](https://lists.freedesktop.org/archives/systemd-devel/2024-June/author.html#50463)


[More information about the systemd-devel mailing list](https://lists.freedesktop.org/mailman/listinfo/systemd-devel)
