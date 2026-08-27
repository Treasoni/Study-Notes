---
url: "https://github.com/tailscale/tailscale/issues/12407"
title: "Tailscale does not forward traffic when output interface is on the same host · Issue #12407 · tailscale/tailscale"
scraped_at: 2026-08-27T19:22:06+00:00
---

[Skip to content](https://github.com/tailscale/tailscale/issues/12407#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/tailscale/tailscale/issues/12407) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/tailscale/tailscale/issues/12407) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/tailscale/tailscale/issues/12407) to refresh your session. Dismiss alert
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/tailscale/tailscale/issues/12407).
/ Public
  * [ Notifications ](https://github.com/login?return_to=%2Ftailscale%2Ftailscale) You must be signed in to change notification settings
  * [ Fork 3.1k ](https://github.com/login?return_to=%2Ftailscale%2Ftailscale)
  * [ Star  35.7k ](https://github.com/login?return_to=%2Ftailscale%2Ftailscale)


#  Tailscale does not forward traffic when output interface is on the same host #12407
Copy link
Copy link
[Tailscale does not forward traffic when output interface is on the same host](https://github.com/tailscale/tailscale/issues/12407#top)#12407
Copy link
Labels
[OS-linux](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22OS-linux%22)[Bug](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22bug%22)Bug[pod/network-features](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22pod%2Fnetwork-features%22)[Issues relating to subnet routes, 4via6](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22subnet%22)Issues relating to subnet routes, 4via6
## Description
opened [on Jun 8, 2024](https://github.com/tailscale/tailscale/issues/12407#issue-2341602772)
Issue body actions
### What is the issue?
**CONTEXT:** I have a Proxmox server with a few LXC containers. Tailscale is installed on the host node, advertising itself as a subnet route.
This is done so that I can access my services on all the LXC containers without the need to install an instance of Tailscale per container.
The subnet route, in this case, does not work as intended. When accessing an HTTP service on those LXCs, the page keeps loading until timeout.
**BUG:** After some troubleshooting, this is what I found. In order to forward traffic, Tailscale uses the `ts-forward` chain in the FILTER table, which marks the packet with `0x40000/0xff0000`; then it perform MASQUERADE in the `ts-postrouting` NAT table. And this is expected.
But since the traffic is being forwarded to a LXC container (which resides on the same host), when the packet reenters from a different interface, it will go through the same process (ts-forward --> ts-postrouting), even though it has already been masqueraded and it's "ready" to proceed. That happens because it retains the "mark" assigned in the `ts-forward` chain. When it is masqueraded the second time, I guess the kernel drops it (by reading the TRACE, that is the last time I see that packet id)
What should happen is that when the packet reenters, since now it's not a "Tailscale packet" anymore (the source has been correctly masqueraded) it should skip the ts-* chains.
**NOTEs:**
  1. Tailscale subnet route works as intended when accessing services not on the same machine, eg I can access my router home page from any Tailscale node
  2. Tailscale is using iptables


**PROPOSED SOLUTIONs:** Add one of the following rules to iptables. I'm not an expert by any means, I learned to use `iptables` just to try fixing this annoyance. So please carefully review the rules
  1. `iptables -t raw -A PREROUTING -m mark --mark 0x40000/0xff0000 -j MARK --set-mark 0` or
  2. `iptables -D FORWARD 1; iptables -I FORWARD 1 -m mark ! --mark 0x40000/0xff0000 -j ts-forward` Right know I'm using the second approach which I think is cleaner and it works as intended.


**DEBUG files:** Those are the traces before and after adding proposed solution n. 1. [TRACE-before-rule](https://github.com/user-attachments/files/15747599/only-TRACE-dest-ip-port.txt): packet does not arrive to destination [TRACE-after-rule](https://github.com/user-attachments/files/15747600/removing-mark-v2.txt): packet arrives to destination
### Steps to reproduce
  1. Install Proxmox
  2. Install Tailscale and adversite subnet route `tailscale up --adversite-routes=192.168.159.0/24`
  3. Deploy some LXC container
  4. Deploy some services on those LXC container
  5. Try accessing those servers from any other Tailscale nodes


### Are there any recent changes that introduced the issue?
I think the problem is there before v1.66 and is unrelated to the `stateful-filtering` issue I've been reading about docker.
### OS
Linux
### OS version
Proxmox Virtual Environment 8.2.2
### Tailscale version
1.66.4
### Other software
_No response_
### Bug report
BUG-8b6786c395b8074d21607dea19cb147ae9d5f58ae3b04d8fffb7fc4260c283ed-20240608102505Z-577d8722201567fe
👍React with 👍1Reacted by jon r
## Activity
[luigir-it](https://github.com/luigir-it)
added 
[Bug](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22bug%22)Bug
[on Jun 8, 2024](https://github.com/tailscale/tailscale/issues/12407#event-13087997142)
[timtailscale](https://github.com/timtailscale)
added 
[Issues relating to subnet routes, 4via6](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22subnet%22)Issues relating to subnet routes, 4via6
and removed [on Aug 13, 2024](https://github.com/tailscale/tailscale/issues/12407#event-13852773223)
### numboDumbo commented on Oct 13, 2024 
More actions
Facing the same issue for site to site vpn.
mentioned this [on Jul 16, 2025](https://github.com/tailscale/tailscale/issues/12407#event-2771229922)
  * [Cannot ping deivces on subnet after creating subnet router #16158](https://github.com/tailscale/tailscale/issues/16158)


[bcreane](https://github.com/bcreane)
added [on Jan 9, 2026](https://github.com/tailscale/tailscale/issues/12407#event-21936524404)
[Logvin](https://github.com/Logvin)
mentioned this [on May 22, 2026](https://github.com/tailscale/tailscale/issues/12407#event-6797810879)
  * [Docker 28 and Tailscale subnet routing moby/moby#51015](https://github.com/moby/moby/issues/51015)


[Sign up for free](https://github.com/signup?return_to=https://github.com/tailscale/tailscale/issues/12407)**to join this conversation on GitHub.** Already have an account? [Sign in to comment](https://github.com/login?return_to=https://github.com/tailscale/tailscale/issues/12407)
## Metadata
## Metadata
### Assignees
No one assigned
### Labels
[OS-linux](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22OS-linux%22)[Bug](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22bug%22)Bug[pod/network-features](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22pod%2Fnetwork-features%22)[Issues relating to subnet routes, 4via6](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22subnet%22)Issues relating to subnet routes, 4via6
No type
### Projects
No projects
### Milestone
No milestone
### Relationships
None yet
### Development
No branches or pull requests
### Participants
## Issue actions
  * Open in GitHub Copilot app


You can’t perform that action at this time. 
