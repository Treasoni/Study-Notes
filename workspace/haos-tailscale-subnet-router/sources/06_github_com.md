---
url: "https://github.com/hassio-addons/app-tailscale/issues/415"
title: "Routing traffic from LAN to Tailscale not working · Issue #415 · hassio-addons/app-tailscale"
scraped_at: 2026-09-12T14:20:57+00:00
---

[Skip to content](https://github.com/hassio-addons/app-tailscale/issues/415#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/415) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/415) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/415) to refresh your session. Dismiss alert
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/issues/415).
/ Public
  * [ Notifications ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale) You must be signed in to change notification settings
  * [ Fork 134 ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale)
  * [ Star  546 ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale)


#  Routing traffic from LAN to Tailscale not working
Copy link
Copy link
Closed
Closed
[Routing traffic from LAN to Tailscale not working](https://github.com/hassio-addons/app-tailscale/issues/415#top)#415
Copy link
## Description
opened [on Oct 14, 2024](https://github.com/hassio-addons/app-tailscale/issues/415#issue-2584869813)
# Problem/Motivation
> Tailscale addon not routing traffic from LAN to Tailscale
## Expected behavior
> Since my tailscale on HASS is acting as a subnetrouter, it's routing traffic from Tailscale to my LAN, the other way around should also be possible.
## Actual behavior
> traceroute 100.84.130.100 traceroute to 100.84.130.100 (100.84.130.100), 64 hops max, 40 byte packets 1 192.168.178.1 (192.168.178.1) 5.353 ms 2.572 ms 2.309 ms 2 192.168.178.3 (192.168.178.3) 4.191 ms 2.893 ms 3.061 ms 3 * * *
## Steps to reproduce
I configured my hass-tailscale-addon as follows:

```
advertise_exit_node: true
accept_routes: true
accept_dns: true
userspace_networking: false
snat_subnet_routes: false
advertise_routes:
  - 192.168.178.0/24

```

I created a static route on my firewall for destination: `100.0.0.0/10` to `192.168.178.3` (my HASS IP)
When I ping `100.84.130.100` (IP from another client in my Tailscale) from HASS I get a instant connection. When I ping / traceroute that same IP from any other device without Tailscale installed it hangs at `192.168.178.3`. (see above for the traceroute)
## Proposed changes
> N/A
## Activity
### lmagyar commented on Oct 14, 2024 
Last edited by lmagyar
Collaborator
More actions
This should work, tested several times.
Do you really need `snat_subnet_routes: false`? This requires much more config everywhere. To access other TS devices, or other subnet devices behind other TS devices, from your LAN, you don't need this. With `snat_subnet_routes: true` it just works.
If you really want full blown site-to-site networking (ie. using `snat_subnet_routes: false`), please follow steps from step 3 on [Site-to-site networking](https://tailscale.com/kb/1214/site-to-site/)? - Yeah DOCS.md says steps 2-3, TS changed the docs, DOCS.md will be updated.
### lmagyar commented on Oct 15, 2024 
Collaborator
More actions
OK, questions:
  * what is your installation type?
  * did you enable subnet routing on the admin site for the _**source**_ lan also?


Because it seems that either the OS is missing some feature (forwarding) or the routing is not configured beetween 192.168.178.3 and tailscale0. Test it first:
  * with snat_...: true, and
  * without your firewall/router, ie. modify the local route table on the source lan device that it sends packages for 100.x.x.x directly to 192.168.178.3. This way you must be able to access from your source lan any tailscale device.
  * then add the other/destination subnet to the routing on your local/source lan device that it send packages for the other lan (not 192.168.178.x) to 192.168.178.3. This way you must be able to access any other subnet.


This must work. If it doesn't work, it is a config error or a TS bug/breaking change. When it works, you can experiment with snat_...: false and firewalls/routers, this is plain old network config from here.
### lmagyar commented on Oct 18, 2024 
Collaborator
More actions
So you edited the static routes on the non-TS lan devices. What was snat_... (true or false) when you had to add the additional rule for tailscale0? Ie. this extra rule is needed for both snat_...: false and true, or only for false?
### lmagyar commented on Oct 19, 2024 
Collaborator
More actions
Strange. I will repeat my tests (site-to-site with snat=true) in the next weeks, I need some time, my physical test env. is currently used for other stuff. :/
### maxenceleduc92 commented on Oct 29, 2024 
Last edited by maxenceleduc92
More actions
Hi, I've been having the same issue here. According to[ tailscale's subnet router quick guide](https://tailscale.com/kb/1406/quick-guide-subnets), were's supposed to execute the following commands:

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

### lmagyar commented on Oct 30, 2024 
Collaborator
More actions
Please read the docs, it says "follow steps from step 3", because what you want to configure, is already set.
### github-actions commented on Nov 29, 2024 
[on Nov 29, 2024](https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2507313990) – with [GitHub Actions](https://help.github.com/en/actions)
More actions
There hasn't been any activity on this issue recently, so we clean up some of the older and inactive issues. Please make sure to update to the latest version and check if that solves the issue. Let us know if that works for you by leaving a comment 👍 This issue has now been marked as stale and will be closed if no further activity occurs. Thanks!
[github-actions](https://github.com/apps/github-actions)
added 
[There has not been activity on this issue or PR for quite some time.](https://github.com/hassio-addons/app-tailscale/issues?q=state%3Aopen%20label%3A%22stale%22)There has not been activity on this issue or PR for quite some time.
[on Nov 29, 2024](https://github.com/hassio-addons/app-tailscale/issues/415#event-15472624762)
[github-actions](https://github.com/apps/github-actions)
removed 
[There has not been activity on this issue or PR for quite some time.](https://github.com/hassio-addons/app-tailscale/issues?q=state%3Aopen%20label%3A%22stale%22)There has not been activity on this issue or PR for quite some time.
[on Dec 5, 2024](https://github.com/hassio-addons/app-tailscale/issues/415#event-15540163304)
### github-actions commented on Jan 5, 2025 
[on Jan 5, 2025](https://github.com/hassio-addons/app-tailscale/issues/415#issuecomment-2571544284) – with [GitHub Actions](https://help.github.com/en/actions)
More actions
There hasn't been any activity on this issue recently, so we clean up some of the older and inactive issues. Please make sure to update to the latest version and check if that solves the issue. Let us know if that works for you by leaving a comment 👍 This issue has now been marked as stale and will be closed if no further activity occurs. Thanks!
[github-actions](https://github.com/apps/github-actions)
added 
[There has not been activity on this issue or PR for quite some time.](https://github.com/hassio-addons/app-tailscale/issues?q=state%3Aopen%20label%3A%22stale%22)There has not been activity on this issue or PR for quite some time.
[on Jan 5, 2025](https://github.com/hassio-addons/app-tailscale/issues/415#event-15816950136)
###  7 remaining items
Load more
Loading
[Sign up for free](https://github.com/signup?return_to=https://github.com/hassio-addons/app-tailscale/issues/415)**to join this conversation on GitHub.** Already have an account? [Sign in to comment](https://github.com/login?return_to=https://github.com/hassio-addons/app-tailscale/issues/415)
## Metadata
## Metadata
### Assignees
No one assigned
### Labels
No labels
No labels
No type
### Projects
No projects
### Milestone
No milestone
### Relationships
None yet
### Development
No branches or pull requests
## Issue actions
  * Open in GitHub Copilot app


You can’t perform that action at this time. 
