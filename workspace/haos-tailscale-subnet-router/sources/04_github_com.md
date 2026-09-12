---
url: "https://github.com/hassio-addons/app-tailscale/issues/216"
title: "Using Tailscale addon for site-to-site networking with 2 HA instances do not work · Issue #216 · hassio-addons/app-tailscale"
scraped_at: 2026-09-12T14:20:57+00:00
---

[Skip to content](https://github.com/hassio-addons/app-tailscale/issues/216#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/216) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/216) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/216) to refresh your session. Dismiss alert
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/issues/216).
/ Public
  * [ Notifications ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale) You must be signed in to change notification settings
  * [ Fork 134 ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale)
  * [ Star  546 ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale)


#  Using Tailscale addon for site-to-site networking with 2 HA instances do not work
Copy link
Copy link
Closed
Closed
[Using Tailscale addon for site-to-site networking with 2 HA instances do not work](https://github.com/hassio-addons/app-tailscale/issues/216#top)#216
Copy link
## Description
opened [on Jun 18, 2023](https://github.com/hassio-addons/app-tailscale/issues/216#issue-1762252345)
Issue body actions
# Problem/Motivation
Hi, I have 2 Home Assistant (HA) running in 2 distant locations on 2 Raspberry Pis. Both run Tailscale as addon in a docker container. When the purpose is to only access HA itself, it works out of the box.
I initially extended the usage to accessing whole VLAN subnets from "outside" to "inside" via Taiscale and a subnet router node. In this case the conf of the Tailscale addon needs to include the activation of "userspace_networking" so that the traffic reaching the subnet router node can be bounced from the docker container to the host network interface (ethernet or wifi interfaces) and from there to the target subnet. This works if and only if the source client runs Tailscale itself.
In a new usage, I'm trying to access the distant network from a device in the source network, which does not run Tailscale. Following the documentation, I have configured both subnet routers on each side to announce routes, accept routes, etc.
The problem I am facing is the following: As required, the local router in the source network has a static route to send traffic to the distant subnet via the local Tailscale node. This works as intended. However, when the traffic reaches the ethernet interface (called "Supervisor eth0") of the host (the Raspberry) the default route for this interface is sending back the traffic to the local router (as default gateway). There is no route to any tailscale interface for the outbound traffic. When "userspace_networking" is activated, there is not even a network interface for tailscale. In comparison, when I run tailscale on a laptop there is a tailscale network interface and there are routes for the distant LANs that are set to bounce traffic from the laptop to the distant LAN via the Tailscale gateway IP instead of the physical network interface, and it works.
If I disable "userspace_networking" in the Addon, I see appearing a new network interface called "tailscale0" with many routes to 100.x IPs, very similar to what I see on my laptop. I am therefore wondering if the usage of "userspace_networking" for subnet routing is not just a bad workaround to a deeper routing issue.
## Expected behavior
I would expect to run the Tailscale addon without "userspace_networking" enabled, and instead to have automatically added outbound routes from tailscale0 to the local subnets via eth0 for the routes that the node announces, as well as automatically added inbound routes from eth0 to the distant subnets via tailscale0 for the routes that the node accepts from other router nodes.
## Actual behavior
routes are not added and traffic from subnet to subnet is not routed correctly.
## Steps to reproduce
1/ Run Home assistant on a Raspberry Pi. 2/ Install Tailscale as addon to HA 3/ configure Tailscale addon to announce local routes and approve routes in the admin console. this is the target subnet router node that will serve distant VLAN IPs. 4/ run Tailscale in the addon docker container. -> at this stage, IPs from the distant VLAN are reachable if "userspace_networking" is enabled 5/ do the same for another HA instance that is the source subnet router that will serve local VLAN IPs. 6/ configure the local router to route distant VLANS via HA local IP (eth0) -> routing stops at eth0 and is not passed to Tailscale container network interface 7/ disable "userspace_networking" on the source Tailscale subnet router. 8/ a tailscale0 device appears when using nmcli on the HA host
-> there is no route from eth0 to tailscale0 for next hop to distant VLANs
## Proposed changes
see expected behaviour
## Activity
### lmagyar commented on Jun 18, 2023 
Collaborator
More actions
See [#181](https://github.com/hassio-addons/app-tailscale/pull/181), I think it will solve this problem when released. Blocking issue (the reason it is not released): two nodes advertising the same eg. 192.168.x.x subnet and turning on subnet routing makes HA unable to reach local network ("soft bricking" it). [#201](https://github.com/hassio-addons/app-tailscale/pull/201) is a possible workaround for this blocking issue. (note: I'm just another user)
### Gyosa3 commented on Jun 20, 2023 
Author
More actions
hi thanks for the answer, I had previously looked at these PR but I'm not sure it really solves the issue.
I have opened an issue with Tailscale support and I got an interesting answer, now I have a better idea where it all fits: [tailscale/tailscale#8370](https://github.com/tailscale/tailscale/issues/8370)
**My understanding is:**
  * if `userspace-networking` is enabled, there is a soft routing in Tailscale that allows a packet coming from the Tailscale network to reach external machines on the local lan (if the lan is announced by the tailscale node)
  * if `userspace-networking` is disabled, Tailscale creates an interface `tailscale0` and it should work the same as above but it does not. The traffic seems to be prevented to route out of the host. That may be because `tailscale0 `has no route to the internal network? Or should the host know that to reach the internal network it needs to use `eth0 `but there is no "bridge" (whatever it means) between `tailscale0 `and `eth0`? I can't say what happens here, I'm not a specialist of the Linux network stack. Maybe it's firewalled or nginx is in the middle? I'd like to have a sound explanation one day... And I suppose that PR [Drop userspace networking #181](https://github.com/hassio-addons/app-tailscale/pull/181) will break subnet routing on the way, right? Or is it THE fix to the above problem?


**What I know:**
This scenario works with userspace-networking enabled and fails when it is disabled.

```
remote device  <---> tailscale client  <--|--> Tailscale addon  <----> HomeAssistant host <---> Local LAN
    any IP             100.100.1.1        |      100.100.1.2              192.168.2.2          192.168.2.0/24

```

So I have extended it and the new scenario fails, and seems to require that userspace-networking is disabled, but then some bridges seem to be missing.

```
local device  <--> homeAssistant host <--> tailscale addon  <--|--> Tailscale addon  <----> HomeAssistant host <---> Local LAN
192.168.5.10          192.168.5.2            100.100.1.1       |      100.100.1.2              192.168.2.2          192.168.2.0/24
                         eth0                 tailscale0

```

You can see that the local route announced on the left and the one on the right are not similar and there is no conflict of routing between local routes and distant routes. So PR [#201](https://github.com/hassio-addons/app-tailscale/pull/201) do not apply here I'm affraid.
A traceroute shows that the traffic from the source client reaches the home assistant host at interface `eth0 `but do not reach `tailscale0`. Or maybe it does, but maybe then `tailscale0 `to not reach the network within the docker container?
What I find weird is that for a simple usage, installing the addon without userspace-networking gives access to HA core. So this means that traffic coming "from tailscale" is capable to exit the container and access other containers. For example when I reach the AdGuard addon from a remote tailscale client, AdGuard sees the request coming from either 127.0.0.1 or from 192.168.5.2 (so the eth0 IP address). This proves that when there is no userspace-networking, the tailscale0 interface should do the same, that is to reach out to eth0 as next hop.
that's my view but I'm rather lost here...
### Gyosa3 commented on Jun 20, 2023 
Author
More actions
> See [#181](https://github.com/hassio-addons/app-tailscale/pull/181), I think it will solve this problem when released. Blocking issue (the reason it is not released): two nodes advertising the same eg. 192.168.x.x subnet and turning on subnet routing makes HA unable to reach local network ("soft bricking" it). [#201](https://github.com/hassio-addons/app-tailscale/pull/201) is a possible workaround for this blocking issue. (note: I'm just another user)
Hi again,
I'm bouncing back again on your previous reply, tying to dig into the matter as much as I can. In the documentation of this addon there is this sentence:
> The add-on exposes "Exit Node" capabilities that you can enable from your Tailscale account. Additionally, if the Supervisor managed your network ( which is the default), the add-on will also advertise routes to your subnets on all supported interfaces to Tailscale.
I am not sure what it says here. I would understand
> if the Supervisor manages your network
would mean that `userspace-networking` is disabled and `tailscale0` interface exists and is managed by the Supervisor in the host
> (which is the default)
apparently not, this seems to be the opposite, right? `userspace-networking` is enabled by default, right? (so confusing...)
> the addon will also advertise routes to your subnets on all supported interfaces to Tailscale
This is ambiguous to me in the context of subnet routing vs. site-to-site tunneling. I suppose that it means that the addon finds the local lan where the `eth0 `or wifi interfaces are attached to and "auto-announces" it as subnet router in Tailscale. This would work:
  * if `userspace-networking` is enabled (that's probably why [Drop userspace networking #181](https://github.com/hassio-addons/app-tailscale/pull/181) fails in certain situations)
  * if the same lan definition is not announced by another tailscale node (that's your change [Protect local subnets from being routed toward Tailscale subnets if they collide #201](https://github.com/hassio-addons/app-tailscale/pull/201) indeed)
  * if the user has only one local LAN and does not wish to announce others (like, many users like me are now creating a separate vlan for iot devices that they only/also wish to announce on Tailscale)


For me the first step towards a working site-to-site tunnel using Tailscale addon on 2 HA instances would be to have the above working also when `userspace-networking` is disabled.
I'd like to have your view on this, if that makes sense in view of the pull requests that you're trying to push forward?
### lmagyar commented on Jun 20, 2023 
Collaborator
More actions
Subnet routing is independent of whether userspace networking is enabled or not, you will be always able to reach from your tailnet devices the local LANs of other tailnet devices. The add-on advertises the local LANs as subnets, but you also have to enable subnet routing on tailscale's [admin page](https://login.tailscale.com/admin/machines) device by device.
Userspace networking enabled means you don't have tailscale0. Userspace networking diasabled means you have tailscale0. Current last released official add-on runs with userspace networking enabled, no tailscale0.
When Userspace networking is diasabled (ie. you have tailscale0)(the last released official add-on doesn't do this), not only the tailscale add-on (inside a docker container) can access devices on other LANs, but other docker containers also, ie. HA core itself, because there is a tailscale0 interface, and it is configured properly (as seen by `ip route show table 52`).
In case of site-to-site networking, not only the device (who has eth0 and tailscale0), but other devices on it's local LAN also can access LANs of other devices. As I understand [Site-to-site networking](https://tailscale.com/kb/1214/site-to-site/) requires:
  1. enable subnet routes in tailscale admin console (I think you did this)
  2. enable IP forwarding (as I know it is enabled)
  3. `--tun=userspace-networking` option is _**not**_ used (the last released official add-on doesn't do this, it uses this option)
  4. `--snat-subnet-routes=false` (the last released official add-on doesn't do this)
  5. configure local LAN non-tailscale devices' routing toward local tailscaled's (inside HA add-on) eth0 (you did this)


So I made a quick modification in my beta fork of the official tailscale add-on to handle point 4. (it already handles point 3.), please test it (you already have the test setup, I don't), you can find it at: <https://github.com/lmagyar/homeassistant-addon-tailscale-beta>.
Add to the add-on configuration:

```
userspace_networking = false
snat_subnet_routes = false

```

It will create a tailscale2 interface, just to not mess up with tailscale0 if it is already set up, but please stop the official add-on before you start this fork!
Please continue at [lmagyar/homeassistant-addon-tailscale-beta#4](https://github.com/lmagyar/homeassistant-addon-tailscale-beta/issues/4), just to not pollute this official repo.
### Gyosa3 commented on Jun 21, 2023 
Author
More actions
OK thanks, I'll reply on the other repo on the site-to-site aspects.
> Subnet routing is independent of whether userspace networking is enabled or not, you will be always able to reach from your tailnet devices the local LANs of other tailnet devices. The add-on advertises the local LANs as subnets, but you also have to enable subnet routing on tailscale's [admin page](https://login.tailscale.com/admin/machines) device by device.
Regarding `userspace-networking` I have to slightly disagree with you on this, at least in my setup, which I believe is very standard: Raslberry Pi4 + HAOS latest versions + tailscale addon.
Here is my observation:
  * the tailscale node is well registered in the admin console, the subnet (`192.168.5.0/24`) is well advertised and **approved**.
  * the source is a tailscale client on my mobile phone not in the local network (obviously) with Tailscale IP `100.104.70.102`.
  * the target is my router's local IP `192.168.5.1`.


Here is what I get in the node logs when userspace-networking is disabled: the connection times out and I get nowhere.
and here is the log when it's enabled: the connection works immediately and the web interface is shown without any issue.
**Please note** that HA core UI is accessible in both cases so this parameter do not seem to affect the routing in-between containers, it seem to affect only the egress traffic from the HA host to the local LAN. So I'm not even sure if the argument that exposing the `tailscale0` poses so much a threat to the other containers, as they seem to be reachable regardless of its existence. But I may be wrong on this one of course, I just see it from the surface.
So as far as I'm concerned, userspace-networking is a key element in subnet routing working or not. Actually I don't say it should be the case, I would want to believe that what you say is what should happen, you should be able to reach the local vlan regardless of this parameter, but it is not the case in practice and that's what I'd like to see corrected in the first place, before talking about s-2-s networking.
You seem to be the best and only person who has an opinion on this matter so please tell me how I can help, it's very important to me to get this setup working properly.
cheers!
### Gyosa3 commented on Jun 26, 2023 
Author
More actions
Thanks for solving this issue, seems to work already with beta version. Cheers!
[Gyosa3](https://github.com/Gyosa3)
closed this as [completed](https://github.com/hassio-addons/app-tailscale/issues?q=is%3Aissue%20state%3Aclosed%20archived%3Afalse%20reason%3Acompleted)[on Jun 26, 2023](https://github.com/hassio-addons/app-tailscale/issues/216#event-9635545610)
[github-actions](https://github.com/apps/github-actions)
locked and limited conversation to collaborators [on Jul 26, 2023](https://github.com/hassio-addons/app-tailscale/issues/216#event-9921204854)
[Sign up for free](https://github.com/signup?return_to=https://github.com/hassio-addons/app-tailscale/issues/216)**to join this conversation on GitHub.** Already have an account? [Sign in to comment](https://github.com/login?return_to=https://github.com/hassio-addons/app-tailscale/issues/216)
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
