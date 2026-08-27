---
url: "https://github.com/tailscale/tailscale/issues/13754"
title: "Iptables FORWARD chain wrong order · Issue #13754 · tailscale/tailscale"
scraped_at: 2026-08-27T19:22:06+00:00
---

[Skip to content](https://github.com/tailscale/tailscale/issues/13754#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/tailscale/tailscale/issues/13754) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/tailscale/tailscale/issues/13754) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/tailscale/tailscale/issues/13754) to refresh your session. Dismiss alert
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/tailscale/tailscale/issues/13754).
/ Public
  * [ Notifications ](https://github.com/login?return_to=%2Ftailscale%2Ftailscale) You must be signed in to change notification settings
  * [ Fork 3.1k ](https://github.com/login?return_to=%2Ftailscale%2Ftailscale)
  * [ Star  35.7k ](https://github.com/login?return_to=%2Ftailscale%2Ftailscale)


#  Iptables FORWARD chain wrong order #13754
Copy link
Copy link
[Iptables FORWARD chain wrong order](https://github.com/tailscale/tailscale/issues/13754#top)#13754
Copy link
Labels
[Bug](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22bug%22)Bug[containers](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22containers%22)[needs-triage](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22needs-triage%22)
## Description
opened [on Oct 9, 2024](https://github.com/tailscale/tailscale/issues/13754#issue-2576820422)
Last edited by samthesamman
Issue body actions
### What is the issue?
When you have Docker containers running and Tailscale on the same machine, the order that each is brought up is critical. Traffic into Docker containers from the LAN should originate from the Docker container's gateway IP, not the Tailscale IP. This works if `tailscale up` is called after the Docker containers are started, but not if the `tailscale up` is called before the Docker containers are started.
This all has to do with the order of the `ts-forward` chain in iptables `FORWARD` chain. `ts-forward` needs to come before the Docker rules for everything to work correctly.
### Steps to reproduce
**PRODUCES ERROR** Run Tailscale on `server 1` and `server 2`. `server 1` runs a reverse proxy (nginx) and `server 2` runs an application inside a Docker container.
`$ tailscale up` (on both servers)
Then on `server 2` go to your app folder and:
`$ docker compose up`
Now when traffic comes into the container via the Tailscale network (from `server 1` to `server 2`), the traffic IP will be the tailscale IP of Tailscale node running in `server 1`.
**FIX**
On `server 2` run `$ tailscale down` and then `$ tailscale up` after the `$ docker compose up`, and the LAN traffic coming into the docker app container will be the correct IP (the container's gateway IP).
### Are there any recent changes that introduced the issue?
_No response_
### OS
Linux
### OS version
Ubuntu 24.04
### Tailscale version
1.74.1
### Other software
tailscale installed directly on Ubuntu OS (not via Docker)
### Bug report
_No response_
👍React with 👍5Reacted by Dmitry Shulgachik, Logan Pairman, Henrique Sousa, guzlewski and Evan Duong
## Activity
[samthesamman](https://github.com/samthesamman)
added 
[Bug](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22bug%22)Bug
[on Oct 10, 2024](https://github.com/tailscale/tailscale/issues/13754#event-14578778573)
[irbekrm](https://github.com/irbekrm)
added and removed [on Oct 10, 2024](https://github.com/tailscale/tailscale/issues/13754#event-14583944011)
### irbekrm commented on Oct 10, 2024 
Contributor
More actions
I can reproduce this if I install docker on the host _after_ installing tailscale.
What is the actual issue that the source IP being host's Tailscale IP is causing you?
### samthesamman commented on Oct 11, 2024 
Author
More actions
Ideally when using Tailscale the network bahavior is consistent. In my specific case, I run Plex on my server and for whatever reason if the incoming request IP is a Tailscale IP, it doesn't show the true user IP whereas if the incoming request is the docker gateway IP, it pulls the correct request headers to set the user IP correctly. You may say that this is a Plex issue, and it may be, but ultimately the network behaviour should be consistent whether you bring a Docker container up first, or a Tailscale node. I also run an SMTP server where I need to whitelist the incoming IP so it's not ideal to not know which IP the incoming request will see.
### aofei commented on Oct 20, 2024 
More actions
I'm experiencing a similar issue in my K3s cluster environment. My setup uses Flannel as the CNI, with [the entire cluster running over the Tailscale network](https://docs.k3s.io/networking/distributed-multicloud#integration-with-the-tailscale-vpn-provider-experimental).
In my case, the impact is quite significant. Any upgrade to Tailscale, or even a simple `systemctl restart tailscale.service`, causes the entire cluster to go down. This appears to be due to the same root cause described in the original post: the order of iptables rules, specifically the position of Tailscale rules (`ts-input` and `ts-forward`) relative to other networking rules.
As a workaround, I've added the following script to the `ExecStartPost` directive of the `tailscale.service`:

```
#!/bin/bash
set -e
move_rule() {
	while ! iptables -C $1 -j $2 2> /dev/null; do sleep 1; done
	iptables -D $1 -j $2
	iptables -A $1 -j $2
}
move_rule INPUT ts-input
move_rule FORWARD ts-forward
```

This script ensures that the Tailscale iptables rules are moved to the end of their respective chains after Tailscale starts, effectively resolving the issue for my setup.
### guzlewski commented on Apr 26, 2025 
More actions
> I can reproduce this if I install docker on the host _after_ installing tailscale.
> What is the actual issue that the source IP being host's Tailscale IP is causing you?
I have the same issue, I have Tailscale installed as system package and have Docker containers running various software. Having incorrect IPs (Docker gateway instead of Tailscale client) negatively affects traceability as all Tailscale clients appers as single IP in service logs, and even poses security risk as I had to disable some IP based limiting protections as it would restrict access for all Tailscale clients. So there are some real implications of this issue, I hope it would get fixed. Thanks
### hensou commented on May 21, 2025 
More actions
I'm having a somewhat similar issue in my NixOS setup, but in a single machine, where after running `tailscale up` my containers are not reachable via `localhost:<port>`.
However, even after ordering the operations, it does work for me.
Moreover, if I try to access the container with its internal IP, then it works.
### hensou commented on May 21, 2025 
More actions
> I'm having a somewhat similar issue in my NixOS setup, but in a single machine, where after running `tailscale up` my containers are not reachable via `localhost:<port>`.
> However, even after ordering the operations, it does work for me.
> Moreover, if I try to access the container with its internal IP, then it works.
Well, I just discovered that the issue for me was the lack of this flag:
> `--exit-node-allow-lan-access` Allow the client node access to its own LAN while connected to an exit node. Defaults to not allowing access while connected to an exit node.
[Sign up for free](https://github.com/signup?return_to=https://github.com/tailscale/tailscale/issues/13754)**to join this conversation on GitHub.** Already have an account? [Sign in to comment](https://github.com/login?return_to=https://github.com/tailscale/tailscale/issues/13754)
## Metadata
## Metadata
### Assignees
No one assigned
### Labels
[Bug](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22bug%22)Bug[containers](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22containers%22)[needs-triage](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22needs-triage%22)
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
