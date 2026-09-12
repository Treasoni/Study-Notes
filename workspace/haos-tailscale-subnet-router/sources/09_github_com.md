---
url: "https://github.com/hassio-addons/app-tailscale/issues/462"
title: "userspace_networking needs to be enabled and disabled to allow for peer to peer connections · Issue #462 · hassio-addons/app-tailscale"
scraped_at: 2026-09-12T14:20:57+00:00
---

[Skip to content](https://github.com/hassio-addons/app-tailscale/issues/462#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/462) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/462) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/462) to refresh your session. Dismiss alert
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/issues/462).
/ Public
  * [ Notifications ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale) You must be signed in to change notification settings
  * [ Fork 134 ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale)
  * [ Star  546 ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale)


#  userspace_networking needs to be enabled and disabled to allow for peer to peer connections
Copy link
Copy link
Closed as not planned
Closed as not planned
[userspace_networking needs to be enabled and disabled to allow for peer to peer connections](https://github.com/hassio-addons/app-tailscale/issues/462#top)#462
Copy link
Labels
[There has not been activity on this issue or PR for quite some time.](https://github.com/hassio-addons/app-tailscale/issues?q=state%3Aopen%20label%3A%22stale%22)There has not been activity on this issue or PR for quite some time.
## Description
opened [on Feb 4, 2025](https://github.com/hassio-addons/app-tailscale/issues/462#issue-2829207968)
Issue body actions
# Desc
I setup tailscale for a peer to peer connection between to HA devices to be able to use Remote HomeAssistant.
Even when seeing both instance connected in the tailscale dashboard, I was not able to ping the internal IPs from within the HA terminal. I needed to enable and then disable the `userspace_networking`.
See post where I found this: <https://community.home-assistant.io/t/remote-access-to-two-ha-instances/424162/19>
After I've done this, I can ping the other instance directly. Final configuration:
I also think the documentation would benefit from a section on how to connect two different HA instance with the settings from above.
# State
Tailscale version: 0.24.0
## Activity
[Sign up for free](https://github.com/signup?return_to=https://github.com/hassio-addons/app-tailscale/issues/462)**to join this conversation on GitHub.** Already have an account? [Sign in to comment](https://github.com/login?return_to=https://github.com/hassio-addons/app-tailscale/issues/462)
## Metadata
## Metadata
### Assignees
No one assigned
### Labels
[There has not been activity on this issue or PR for quite some time.](https://github.com/hassio-addons/app-tailscale/issues?q=state%3Aopen%20label%3A%22stale%22)There has not been activity on this issue or PR for quite some time.
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
