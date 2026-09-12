---
url: "https://github.com/hassio-addons/app-tailscale/discussions/449"
title: "How to make Home Assistant resolve MagicDNS endpoints without losing the ability to resolve anything non-MagicDNS? · hassio-addons/app-tailscale · Discussion #449 · GitHub"
scraped_at: 2026-09-12T14:20:57+00:00
---

[Skip to content](https://github.com/hassio-addons/app-tailscale/discussions/449#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/discussions/449) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/discussions/449) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/discussions/449) to refresh your session. Dismiss alert
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).
/ Public
  * [ Notifications ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale) You must be signed in to change notification settings
  * [ Fork 134 ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale)
  * [ Star  546 ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale)


#  How to make Home Assistant resolve MagicDNS endpoints without losing the ability to resolve anything non-MagicDNS?  #449
[ xxczaki  ](https://github.com/xxczaki) started this conversation in [Show and tell](https://github.com/hassio-addons/app-tailscale/discussions/categories/show-and-tell)
[ How to make Home Assistant resolve MagicDNS endpoints without losing the ability to resolve anything non-MagicDNS? ](https://github.com/hassio-addons/app-tailscale/discussions/449#top) #449
[ xxczaki  ](https://github.com/xxczaki)
Jan 11, 2025 · 5 comments · 7 replies 
Discussion options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
edited
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


## 
[ xxczaki ](https://github.com/xxczaki) [ Jan 11, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussion-7809093)  
| 
## Related to
  * [Failure with Tailscale integration and DNS resolving #376](https://github.com/hassio-addons/app-tailscale/issues/376)
  * [Home Assistant OS cannot resolve Tailscale hostnames #310](https://github.com/hassio-addons/app-tailscale/issues/310)
  * [Update docs with DNS settings #428](https://github.com/hassio-addons/app-tailscale/pull/428)
  * <https://community.home-assistant.io/t/cannot-access-other-tailnet-device-from-ha-using-magicdns-name-tailscale/825664>


## How to make Home Assistant resolve MagicDNS endpoints without losing the ability to resolve anything non-MagicDNS?
  1. Make sure you have the "Accept DNS" option turned on in the add-on's configuration: 
  2. Go to `https://login.tailscale.com/admin/dns` and configure your default DNS resolver (I used my Pi-hole, but if you don't have one, then consider using one of the options available after clicking the "Add nameserver" button – then, check the "Override local DNS" option): 
  3. SSH to your Home Assistant instance and run `ha dns info` – make sure that you see `servers: []` in the output – if not, run `ha dns reset`
  4. Go to Settings -> System -> Network -> IPv4 and make the first DNS server `100.100.100.100`: 
  5. (optional) If using IPv6, set the first DNS server to `fd7a:115c:a1e0::53`: 
  6. Go back to SSH and run `ha dns restart`
  7. Confirm that everything is working by running `ping google.com` and `ping XXX.XXX.ts.net` in the SSH console – both addresses should resolve correctly


## Why does this work?
It seems like the second DNS server specified in Settings -> System -> Network -> IPv4 doesn't really work if the first one (`100.100.100.100` in our case) isn't. By modifying the DNS settings in Tailscale's dashboard, we are effectively forcing `100.100.100.100` to use a different DNS server (Pi-hole in my case) if the specified address is not MagicDNS. See <https://tailscale.com/kb/1381/what-is-quad100>.  |  
| --- |  
You must be logged in to vote
All reactions
##  Replies:  5 comments  · 7 replies 
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
### 
[ lmagyar ](https://github.com/lmagyar) [ Jan 13, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11822577)
Collaborator   
|  First of all, thank you for this post, based on your steps I was able to configure TS DNS the first time ever! Then everything crashed, and spent hours to figure out the root cause... TLDR: Turn off MagicDNS, and then everything will work fine, without any tricks. Based on my experiments, I will make a PR to update the add-on docs about DNS. Comments:
>   1. Make sure you have the "Accept DNS" option turned on in the add-on's configuration:
> 

This is enabled by default. So you don't need to modify this.
> Go to <https://login.tailscale.com/admin/dns> and configure your default DNS resolver (I used my Pi-hole, but if you don't have one, then consider using one of the options available after clicking the "Add nameserver" button – then, check the "Override local DNS" option):
What will happen on other TS devices in your tailnet that has no access to your local 192.168.1.15? Does this subnet routed to other devices? Why not use the tailnet IP of this Pi-hole here on the admin page? Just for reference, what I did:
  1. Based on your guide 
     * TS: MagicDNS is enabled, override local DNS is enabled, global nameservers: 1.1.1.1
     * HA: DNS 100.100.100.100 and 1.1.1.1
     * ha dns restart (it seems to be unnecessary, based on docker ps, hassio_dns container is restarted after DNS UI config change)
     * It works, first ever
  2. experiment, revert TS changes, HA unchanged 
     * TS: override local DNS is **disabled** , global nameservers: **-**
     * HA: DNS no change (100.100.100.100 and 1.1.1.1)
     * ha dns restart
     * still works, though with a noticable delay for resolution eg. ping google.com, a bit strange, but hmmm, it works...
  3. experiment, HA uses only TS DNS 
     * TS: no change
     * HA: DNS 100.100.100.100
     * ha dns restart
     * still works, though with a noticable delay...
     * nslookup google.com 100.100.100.100 -> works, wow... :/

Then hassio_dns crashed and can't be restarted, supervisor crashed and restarted, nginx add-on restarted, nothing can be pinged... hassio_dns says: 
```
[FATAL] plugin/loop: Loop (172.30.32.1:51675 -> :53) detected for zone ".", see https://coredns.io/plugins/loop#troubleshooting. Query: "HINFO 3773484566690024990.644798792321423444."
[01:09:56] WARNING: Halt DNS plug-in with exit code 1

```
This is the state, I think, where I always ended previously, without noticing, that hassio_dns is crashed!!! I've spent several hours to really reset HA DNS (ha dns reset, ha dns restart, ha host reboot, configuring HA DNS 1.1.1.1, several times), finally everything is back to it's normal state. **My diagnosis is: MagicDNS after some time somehow managed to use the local configured DNS (to resolve addresses like google.com?), that is redirected to itself, loop, crash.**
  1. experiment, **disable MagicDNS** , lets configure eg. as if HA DNS works normally, ie. calls the second DNS if the first fails 
     * TS: MagicDNS is disabled globally, override local DNS is disabled, global nameservers: -
     * HA: DNS 100.100.100.100 and 1.1.1.1
     * ha dns restart
     * and everything works as expected
     * ha host reboot
     * HA, SU, DNS logs are "green"
     * still works 
       * nslookup tailnet-device.xxxx.ts.net 100.100.100.100 -> works, 100.x.x.x is resolved
       * nslookup tailnet-device 100.100.100.100 ->SERVFAIL, as expected, no MagicDNS
       * nslookup google.com 100.100.100.100 ->SERVFAIL, as expected
       * ping tailnet-device.xxxx.ts.net -> works, 100.x.x.x is resolved, not it's external funnel IP
       * ping google.com -> works

**Verdict: disable MagicDNS globally, and TS DNS + any other DNS configured in HA starts to work as expected, though you lose the ability to access TS devices without the fully qualified domain name.**  |  
| --- |  
You must be logged in to vote
All reactions
0 replies 
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
### 
[ lmagyar ](https://github.com/lmagyar) [ Jan 13, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11822807)
Collaborator   
|  cc [#310](https://github.com/hassio-addons/app-tailscale/issues/310) and [#376](https://github.com/hassio-addons/app-tailscale/issues/376) participants [@david-kalbermatten](https://github.com/david-kalbermatten) [@lwis](https://github.com/lwis) [@codyc1515](https://github.com/codyc1515) [@2manyvcos](https://github.com/2manyvcos) [@kernelb00t](https://github.com/kernelb00t) [@bhovig](https://github.com/bhovig) [@sinclairpaul](https://github.com/sinclairpaul) [@bjeanes](https://github.com/bjeanes) [@shaver](https://github.com/shaver) I've experimented with HA + TS DNS, and based on my results I plan to update the add-on docs with a DNS section. See PR [#450](https://github.com/hassio-addons/app-tailscale/pull/450)
  * Please check/test/comment/review this draft PR.
  * **I didn't test the AdGuard/Pi-hole configuration, please really review that part.**

Based on my experiments and TS docs digging, these are the facts I used writing the PR:
  * HA DNS works correctly when there are multiple DNSs configured, it will call them sequentially 
    * when it fails to call the second configured, it is caused by the faulty MagicDNS behind the first configured 100.100.100.100, when I disabled MagicDNS, all my problems disappeared (see previous comment above)
    * this is tested by me back and forth several times, even the hassio_dns config template looks correct to me (<https://github.com/home-assistant/plugin-dns/blob/master/rootfs/usr/share/tempio/corefile#L18>)
  * `ha dns restart` is not needed 
    * when the HA networking is configured through the UI, the hassio_dns container is always restarted automatically
  * MagicDNS is to resolve device-name without the full domain eg. device-name.xxxx.ts.net, **nothing more!** , it's like a multicast DNS without service discovery 
    * MagicDNS is not the whole TS DNS (even though lot of comments, docs suggest it)
    * MagicDNS is not the resolvers configured on the TS admin page (even though `tailscale dns status` suggest otherwise)
    * MagicDNS has no role in serve or funnel
    * this is tested by me back and forth several times, and finally all my test configs were done with MagicDNS disabled, and only the resolution of device-name without the full domain was not working, everything else worked perfectly without MagicDNS
  * `--accept-dns=false` means not accepting the global DNS settings from the TS admin page (global nameservers, etc.) 
    * this is not to turn off MagicDNS locally (even though lot of comments, docs suggest it)
    * this is not to turn of TS DNS locally (even though `tailscale dns status` says the exact opposite)
    * this is tested by me back and forth several times, nslookup on 100.100.100.100 is always accessible; when 1.1.1.1 is configured as resolver on the admin page, it resolvs google.com, when `--accept-dns=false` specified, it stops resolving google.com, but continue to resolve device-name.xxxx.ts.net (even when MagicDNS is also disabled)
  * We could add with Supervisor API the TS DNS 100.100.100.100 to the servers config option of the DNS, but I agree, that it is better done by the docs + user who knows it's config.

Questionable things:
  * I couldn't find any use case for this: some global nameserver (eg. 1.1.1.1) is configured on the TS admin page, but **"Override local DNS" is not enabled**. I had to enable "Override local DNS" to (the configured global nameservers on the TS admin page) have any effect on 100.100.100.100.
  * What about exit nodes? I haven't used/tested it. Yeah, there is no add-on config for it yet, but any info on it related to DNS?

 |  
| --- |  
You must be logged in to vote
All reactions
0 replies 
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
### 
[ xxczaki ](https://github.com/xxczaki) [ Jan 13, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11823546)
Author   
| 
> What will happen on other TS devices in your tailnet that has no access to your local 192.168.1.15? Why not use the tailnet IP of this Pi-hole here on the admin page?
Using the Tailnet IP could work, didn't test that – you could also add a backup DNS entry in the admin panel, although that would mean that your traffic wouldn't be filtered when you are away from home.
> disable MagicDNS globally, and TS DNS + any other DNS configured in HA starts to work as expected, though you lose the ability to access TS devices without the fully qualified domain name.
This is fascinating – wouldn't disabling MagicDNS make the domain names disappear from the admin panel? Even if not, what about automatic SSL certificates? Would Tailscale renew them when the MagicDNS is off?
> I couldn't find any use case for this: some global nameserver (eg. 1.1.1.1) is configured on the TS admin page, but "Override local DNS" is not enabled. I had to enable "Override local DNS" to (the configured global nameservers on the TS admin page) have any effect on 100.100.100.100.
I think the "Override local DNS" feature is ultimately only intended as a way to force the devices in the Tailnet to use a custom DNS resolver – like when you specify the DNS servers in your home router's config and all of the network devices get it.  |  
| --- |  
You must be logged in to vote
All reactions
1 reply 
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
#### 
[lmagyar](https://github.com/lmagyar) [ Jan 13, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11825777)
Collaborator   
|  **TLDR: disabling MagicDNS is fine for HA (or other "linux" servers with manual net configs), but bad for general (even DHCP based) win/linux clients - > better figure out how MagicDNS interferes with hassio_dns than to disable it completely**, pffff..... If MagicDNS is disabled:
  * Ubuntu: 
    * 100.100.100.100 stops resolving device names without domain, but resolves it with domain
    * configuring DNS for the host stops completely, so 100.100.100.100 will not be asked at all
    * so we lose resolution even for the fully specified names...
  * Win11: 
    * 100.100.100.100 never resolves device names without domain, but resolves it with domain (it's behaviour is independent of MagicDNS config, and differs from the linux version, it's not an issue, it's never used)
    * modifying the hosts file stops completely, so nothing resolved
    * so we lose resolution even for the fully specified names...


> wouldn't disabling MagicDNS make the domain names disappear from the admin panel? Even if not, what about automatic SSL certificates? Would Tailscale renew them when the MagicDNS is off?
I turned off MagicDNS approx. 2 days ago, and didn't notice any change, other than resolving devices names (without the full domain) stopped working. Serve, funnel works, ie. public TCP forwarders are working, so my assumption is that the certs will be renewed, though I can't say it for sure. The HTTPS TS docs says (<https://tailscale.com/kb/1153/enabling-https>), we have to enable MagicDNS. But in the middle it says it will be used to resolve <http://machine-name> requests. One of my devices has a cert that expires within 2 days, another within approx. 30 days. I will check the renewal, but it is strange, that it is not renewed 4 days before expiration (2 days ago MagicDNS was enabled). There is no info on when TS renews the cert, I see 14 days, 2/3rd of lifetime, this didn't happen in this case. OK, checked on the device in /data/state/certs/ the cert is not renewed in the add-on's file-system. Based on TS issues/PRs, renewal is just simply broken, it will happen only when the cert is expired... [tailscale/tailscale#8204](https://github.com/tailscale/tailscale/issues/8204) [tailscale/tailscale#8258](https://github.com/tailscale/tailscale/pull/8258) [tailscale/tailscale#8599](https://github.com/tailscale/tailscale/pull/8599) [tailscale/tailscale#8725](https://github.com/tailscale/tailscale/issues/8725) [tailscale/tailscale@`24f322b`](https://github.com/tailscale/tailscale/commit/24f322bc43cd0aa6f9492c2d03b3c0d330b0cc3b) I will check it 2 days from now.
> I think the "Override local DNS" feature is ultimately only intended as a way to force the devices in the Tailnet to use a custom DNS resolver – like when you specify the DNS servers in your home router's config and all of the network devices get it.
Yes, I have to enable it to make the 100.100.100.100 DNS use the configured global nameservers. But what is the effect, if I configure global nameservers, but did not enable "Override local DNS"??? I didn't notice any effect of this configuration. In the disabled state, 100.100.100.100 DNS will not use the configured global nameservers, so why it is there? The disabled state has no effect. Maybe this is a quick way to "disable" the configured global nameserver list temporarily without deleting it one-by-one????????  |  
| --- |  
All reactions
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
### 
[ lmagyar ](https://github.com/lmagyar) [ Jan 15, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11843267)
Collaborator   
|  I've found the root cause and have a fix!!! PR will follow, currently is under testing. Problem:
  * MagicDNS (TS DNS on 100.100.100.100 + magical modification of any system's DNS settings) when can't resolve something, **doesn't return REFUSED, SERVFAIL or NXDOMAIN** , but calls the original DNS server (based on the DNS config existed before TS started, in our case /etc/resolv.conf)
  * on HA, this is hassio_dns, where we configure to first call 100.100.100.100
  * loop, crash...

Not solutions:
  * there is no way, to modify this TS DNS behavior
  * permanent accept_dns=false disables the DNS config's magical modification, but also disables accepting configured global nameservers by 100.100.100.100 from TS admin page, they won't be called, it would break things

Solution:
  * **mount an empty resolv.conf for tailscaled** (for any other process, there is the default add-on resolv.conf pointing to hassio_dns) 
    * if a resolution is requested by any process (in the TS add-on or in any other container), it first goes to hassio_dns, then hassio_dns calls 100.100.100.100 (if configured), if 100.100.100.100 returns an error, hassio_dns calls the next server, this is the normal HA way to do DNS queries
    * but TS fills the log with warnings for every non-resolved DNS request: `dns: resolver: forward: no upstream resolvers set, returning SERVFAIL`
  * **start a dummy dnsmasq, that answers REFUSED for everything, and use it in the fake resolv.conf for tailscaled**
    * it runs on 127.52.52.52:53, only port 53 is allowed in resolv.conf
    * **I've tried to hide it with a network namespace, but my Linux (apparmor?) experience wasn't enough to achieve this**

Positive side effects:
  * name resolution works the same in the TS add-on as in any other container in HA
  * if TS add-on (and DNS) is down, HA will work normally, though will resolve funnel-ed devices with their external public address, but even this is correct

Negative side effects:
  * we must configure 100.100.100.100 in HA net settings, tailnet resolution even inside the TS add-on won't work without this, a bit strange for TS users, but correct for HA
  * `ping tailnet-device-name` doesn't work, only `ping tailnet-device-name.tailxxxx.ts.net`, so without domain, only local.hass.io domain works, but this is the default HA behavior, so I think it is fine

 |  
| --- |  
You must be logged in to vote
All reactions
5 replies 
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
#### 
[2manyvcos](https://github.com/2manyvcos) [ Jan 15, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11843555)  
|  What happens if the Tailscale plugin is stopped / crashes when 100.100.100.100 is configured in the HA network settings? Will HA simply skip the server and try the next one in the list or will DNS resolution stop working completely?  |  
| --- |  
All reactions
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
#### 
[lmagyar](https://github.com/lmagyar) [ Jan 15, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11846915)
Collaborator   
|  Yes, will skip it. Tested.  |  
| --- |  
All reactions
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
#### 
[lmagyar](https://github.com/lmagyar) [ Jan 15, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11846936)
Collaborator   
|  I've tested all combination of userspace_networking: true/false, accept_dns: true/false, MagicDNS enabled/disabled, Global nameservers configured/not configured, Override local DNS enabled/disabled. It survived everything.  |  
| --- |  
All reactions
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
#### 
[2manyvcos](https://github.com/2manyvcos) [ Jan 15, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11847128)  
|  Perfect, thanks for testing!  |  
| --- |  
All reactions
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
#### 
[bjeanes](https://github.com/bjeanes) [ Jan 15, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11848745)  
|  This is promising!  |  
| --- |  
All reactions
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
### 
[ lmagyar ](https://github.com/lmagyar) [ Jan 20, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11889751)
Collaborator   
|  There are 2 new draft PR-s relate to this conversation, [#454](https://github.com/hassio-addons/app-tailscale/pull/454) and [#455](https://github.com/hassio-addons/app-tailscale/pull/455). Tested with AdGuard, no issues. Though I will test it with subnet routing, because [#454](https://github.com/hassio-addons/app-tailscale/pull/454) is still too general in my opinion, so I think it can break subnet routing on some level, better to test it before releasing it even on my forked repo users.  |  
| --- |  
You must be logged in to vote
All reactions
1 reply 
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/discussions/449).


Quote reply
#### 
[lmagyar](https://github.com/lmagyar) [ Jan 26, 2025 ](https://github.com/hassio-addons/app-tailscale/discussions/449#discussioncomment-11962028)
Collaborator   
|  Tested these changes, all is fine, PRs are ready for review. If you want to test them, you can install my fork from: <https://github.com/lmagyar/homeassistant-addon-tailscale>
  * stop official add-on, turn off auto-start
  * copy-paste the yaml configuration from the official to the forked add-on
  * start the forked version
  * authenticate the forked verison through the WEB UI
  * check the logs

Follow the steps in the add-on's documenttion at the DNS chapter: <https://github.com/lmagyar/homeassistant-addon-tailscale/blob/main/tailscale/DOCS.md#dns>  |  
| --- |  
All reactions
[Sign up for free](https://github.com/join?source=comment-repo) **to join this conversation on GitHub**. Already have an account? [Sign in to comment](https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fhassio-addons%2Fapp-tailscale%2Fdiscussions%2F449)
Category 
[ Show and tell ](https://github.com/hassio-addons/app-tailscale/discussions/categories/show-and-tell)
Labels 
None yet 
4 participants 
You can’t perform that action at this time. 
