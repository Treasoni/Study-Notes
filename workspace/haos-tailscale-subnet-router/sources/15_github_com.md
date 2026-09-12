---
url: "https://github.com/hassio-addons/app-tailscale/issues/415#comments"
title: "Issue #415 comments - Routing traffic from LAN to Tailscale not working"
scraped_at: 2026-09-12T00:00:00+00:00
note: "Full comment thread via GitHub REST API (unauthenticated). Issue body is in 06_github_com.md"
---

## lmagyar (COLLABORATOR) 2024-10-14T09:00:34Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2410510747

This should work, tested several times.

Do you really need `snat_subnet_routes: false`? This requires much more config everywhere. To access other TS devices, or other subnet devices behind other TS devices, from your LAN, you don't need this. With `snat_subnet_routes: true` it just works.

If you really want full blown site-to-site networking (ie. using `snat_subnet_routes: false`), please follow steps from step 3 on [Site-to-site networking](https://tailscale.com/kb/1214/site-to-site/)? - Yeah DOCS.md says steps 2-3, TS changed the docs, DOCS.md will be updated.

## ghost (NONE) 2024-10-15T05:48:25Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2412950163

I changed `snat_subnet_routes` to true. Sadly this doesn't make a change:
```
ping 100.84.130.100
PING 100.84.130.100 (100.84.130.100): 56 data bytes
Request timeout for icmp_seq 0
92 bytes from 192.168.178.1: Redirect Host(New addr: 192.168.178.3)
Vr HL TOS  Len   ID Flg  off TTL Pro  cks      Src      Dst
 4  5  00 0054 da1e   0 0000  3f  01 4795 192.168.178.148  100.84.130.100
```

```
traceroute 100.84.130.100
traceroute to 100.84.130.100 (100.84.130.100), 64 hops max, 40 byte packets
 1  192.168.178.1 (192.168.178.1)  6.683 ms  2.521 ms  2.538 ms
 2  192.168.178.3 (192.168.178.3)  2.686 ms  3.289 ms  2.992 ms
 3  * * *
```

## lmagyar (COLLABORATOR) 2024-10-15T12:30:32Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2413782901

OK, questions:
- what is your installation type?
- did you enable subnet routing on the admin site for the ***source*** lan also?

Because it seems that either the OS is missing some feature (forwarding) or the routing is not configured beetween 192.168.178.3 and tailscale0. Test it first:
- with snat_...: true, and
- without your firewall/router, ie. modify the local route table on the source lan device that it sends packages for 100.x.x.x directly to 192.168.178.3. This way you must be able to access from your source lan any tailscale device.
- then add the other/destination subnet to the routing on your local/source lan device that it send packages for the other lan (not 192.168.178.x) to 192.168.178.3. This way you must be able to access any other subnet.

This must work. If it doesn't work, it is a config error or a TS bug/breaking change. When it works, you can experiment with snat_...: false and firewalls/routers, this is plain old network config from here. 

## ghost (NONE) 2024-10-16T19:10:59Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2417730247

Thanks @lmagyar 


- what is your installation type?
>HASS OS running in VM with TrueNAS SCALE as hypervisor
- did you enable subnet routing on the admin site for the source lan also?
>Yes

After a lot of troubleshooting and trial & error I tried spinning up a Ubuntu VM and installed TS with the same properties as I had in my TS addon on HASS. Edited the static route so it pointed to that Ubuntu VM, still same results as described above.

I ended up adding a NAT rule to the iptables configuration in the Ubuntu VM for traffic to  from `192.168.178.0/24` to interface `tailscale0`.

I guess the last part was not configured / is not configurable in HASS OS.

## lmagyar (COLLABORATOR) 2024-10-17T20:20:47Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2420480206

So you edited the static routes on the non-TS lan devices. What was snat_... (true or false) when you had to add the additional rule for tailscale0? Ie. this extra rule is needed for both snat_...: false and true, or only for false?

## ghost (NONE) 2024-10-18T06:37:48Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2421544517

> So you edited the static routes on the non-TS lan devices. What was snat_... (true or false) when you had to add the additional rule for tailscale0? Ie. this extra rule is needed for both snat_...: false and true, or only for false?

No. I made an NAT-rule on the tailscale enabled device (the Ubuntu VM). Static route is still created to that Ubuntu VM is still at my router/Unifi gateway.
I didn't provide any snat_ flag, and default is true.

## lmagyar (COLLABORATOR) 2024-10-19T12:46:33Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2423825134

Strange. I will repeat my tests (site-to-site with snat=true) in the next weeks, I need some time, my physical test env. is currently used for other stuff. :/

## maxenceleduc92 (NONE) 2024-10-29T10:16:03Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2443802923

Hi,
I've been having the same issue here.
According to[ tailscale's subnet router quick guide](https://tailscale.com/kb/1406/quick-guide-subnets), were's supposed to execute the following commands: 
```
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf
```

However, it doesn't seem to work on HASS OS. I get the following error:
```
[core-ssh ~]$ sysctl -p /etc/sysctl.d/99-tailscale.conf
sysctl: error setting key 'net.ipv4.ip_forward': Read-only file system
sysctl: error setting key 'net.ipv6.conf.all.forwarding': Read-only file system
```

## lmagyar (COLLABORATOR) 2024-10-29T18:15:04Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2445013994

Please read the docs, it says "follow steps from step 3", because what you want to configure, is already set.

## github-actions[bot] (NONE) 2024-11-29T08:29:15Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2507313990

There hasn't been any activity on this issue recently, so we clean up some of the older and inactive issues.
Please make sure to update to the latest version and check if that solves the issue. Let us know if that works for you by leaving a comment 👍
This issue has now been marked as stale and will be closed if no further activity occurs. Thanks!

## ghost (NONE) 2024-12-04T13:59:46Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2517490379

Routing traffic back into Tailscale still doesnt work with the Tailscall Hass container

## github-actions[bot] (NONE) 2025-01-05T08:24:28Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2571544284

There hasn't been any activity on this issue recently, so we clean up some of the older and inactive issues.
Please make sure to update to the latest version and check if that solves the issue. Let us know if that works for you by leaving a comment 👍
This issue has now been marked as stale and will be closed if no further activity occurs. Thanks!

## lmagyar (COLLABORATOR) 2025-01-07T16:33:05Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2575741751

Not stale, needs some investigation and maybe some fix.

## lmagyar (COLLABORATOR) 2025-01-24T00:41:56Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2611304422

OK, I've tested meticuously the site-to-site networking (for another reason), and in short, it works flawlessly, no need for any extra iptables rule.

Test was done with rPIs running HASS OS.

I've tested non-TS clients on the LAN with local ~iptables~ ip route config, no issues, but when I used the router to route toward my TS subnet router, while outgoing (LAN->tailnet) connections worked fine, I lost the returning/reply packets from the LAN back to the tailnet (different path for the returning packets, they go through the router, while the original packages from the tailnet was sent by the TS subnet router directly to the non-TS device), but this was a firewall issue, fixed this, and this config works also flawlessly.

So I think this is not a HASS OS or add-on issue, but a local net/VM config issue.

## lmagyar (COLLABORATOR) 2025-01-24T12:20:35Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2612397933

And tested on a VirtualBox VM running HA-OS: exact same results as with rPI+HA OS: it just works, with userspace enabled/disabled, snat enabled/disabled, local/router routing config.

So I think this issue can be closed.

## ghost (NONE) 2025-01-24T16:12:08Z
Source: https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2612893869

Thanks for all the work @lmagyar! I'll try to troubleshoot this more on my end!
