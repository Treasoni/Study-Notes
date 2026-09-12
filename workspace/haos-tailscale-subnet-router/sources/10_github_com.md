---
url: "https://github.com/hassio-addons/app-tailscale/issues/96"
title: "Only one of two subnets is advertised · Issue #96 · hassio-addons/app-tailscale"
scraped_at: 2026-09-12T14:20:57+00:00
---

[Skip to content](https://github.com/hassio-addons/app-tailscale/issues/96#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/96) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/96) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/hassio-addons/app-tailscale/issues/96) to refresh your session. Dismiss alert
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/hassio-addons/app-tailscale/issues/96).
/ Public
  * [ Notifications ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale) You must be signed in to change notification settings
  * [ Fork 134 ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale)
  * [ Star  546 ](https://github.com/login?return_to=%2Fhassio-addons%2Fapp-tailscale)


#  Only one of two subnets is advertised
Copy link
Copy link
Closed
Closed
[Only one of two subnets is advertised](https://github.com/hassio-addons/app-tailscale/issues/96#top)#96
Copy link
## Description
opened [on May 18, 2022](https://github.com/hassio-addons/app-tailscale/issues/96#issue-1239382704)
Issue body actions
# Problem/Motivation
I have two subnets on my HA host, on two NICs. `ha net info` shows as much.
They are 192.168.X.0/24 and 192.168.Y.0/24
## Expected behavior
In tailscale, that both subnets appear under "Subnet routes"
## Actual behavior
only the first subnet shows up under Subnet routes
## Steps to reproduce
Use two subnets on two NICs?
## Proposed changes
Either a way to detect both subnets, or a way to configure the `advertise-routes` option
👍React with 👍2Reacted by Deniz Koellhofer and Dima K.
## Activity
### github-actions commented on Jun 17, 2022 
More actions
There hasn't been any activity on this issue recently, so we clean up some of the older and inactive issues. Please make sure to update to the latest version and check if that solves the issue. Let us know if that works for you by leaving a comment 👍 This issue has now been marked as stale and will be closed if no further activity occurs. Thanks!
[github-actions](https://github.com/apps/github-actions)
added 
[There has not been activity on this issue or PR for quite some time.](https://github.com/hassio-addons/app-tailscale/issues?q=state%3Aopen%20label%3A%22stale%22)There has not been activity on this issue or PR for quite some time.
[on Jun 17, 2022](https://github.com/hassio-addons/app-tailscale/issues/96#event-6827158603)
[github-actions](https://github.com/apps/github-actions)
closed this as [completed](https://github.com/hassio-addons/app-tailscale/issues?q=is%3Aissue%20state%3Aclosed%20archived%3Afalse%20reason%3Acompleted)[on Jun 24, 2022](https://github.com/hassio-addons/app-tailscale/issues/96#event-6872484915)
### andorardo commented on Jun 25, 2022 
Last edited by andorardo
Author
More actions
Please don't close this as "completed", since it is still very much an issue! Saying it is "completed" is inaccurate.
[frenck](https://github.com/frenck)
reopened this [on Jun 25, 2022](https://github.com/hassio-addons/app-tailscale/issues/96#event-6877534873)
[frenck](https://github.com/frenck)
removed 
[There has not been activity on this issue or PR for quite some time.](https://github.com/hassio-addons/app-tailscale/issues?q=state%3Aopen%20label%3A%22stale%22)There has not been activity on this issue or PR for quite some time.
[on Jun 25, 2022](https://github.com/hassio-addons/app-tailscale/issues/96#event-6877534999)
### BlackCatPeanut commented on Jul 5, 2022 
More actions
Adding a comment to this thread so I can follow updates. Definitely a capability which Tailscale supports and useful for those who have numerous subnets on their local network. Keen to see it supported in the HA add on.
### DirschedlF commented on Jul 11, 2022 
More actions
I'm interest in this feature too. I have several subnet to separate devices (open, protect, guest iot ...) via firewall rules in an pfsense router. In the tailscale cli you can specifify several routes via "--advertise-routes=192.168.xxx.0/24,192.168.yyyy.0/24". I use this approach in another tailscale docker container on unraid. It enables the access to targets in the specified subnets. Perhaps you could add an option to specify a list of subnets. in the syntax used by -"-advertise-routes". if this option is empty just use the current subnet of homeassistant as it works today.
### dalkain commented on Jul 29, 2022 
More actions
Also interested in this being implemented
### arunoruto commented on Aug 13, 2022 
More actions
It would be nice to have the possibility to enter further subnets in the config as an array. If I have time in the upcoming days, maybe I can try to configure it, since it should be just an array joined with a comma and slapped onto the `--advertise-routers` flag.
### github-actions commented on Sep 12, 2022 
More actions
There hasn't been any activity on this issue recently, so we clean up some of the older and inactive issues. Please make sure to update to the latest version and check if that solves the issue. Let us know if that works for you by leaving a comment 👍 This issue has now been marked as stale and will be closed if no further activity occurs. Thanks!
[github-actions](https://github.com/apps/github-actions)
added 
[There has not been activity on this issue or PR for quite some time.](https://github.com/hassio-addons/app-tailscale/issues?q=state%3Aopen%20label%3A%22stale%22)There has not been activity on this issue or PR for quite some time.
[on Sep 12, 2022](https://github.com/hassio-addons/app-tailscale/issues/96#event-7365245153)
### DirschedlF commented on Sep 13, 2022 
More actions
I'm still interested to specify more than one subnet. See my comment regarding "--advertise-routes= ..." above.
[github-actions](https://github.com/apps/github-actions)
removed 
[There has not been activity on this issue or PR for quite some time.](https://github.com/hassio-addons/app-tailscale/issues?q=state%3Aopen%20label%3A%22stale%22)There has not been activity on this issue or PR for quite some time.
[on Sep 13, 2022](https://github.com/hassio-addons/app-tailscale/issues/96#event-7374317142)
### github-actions commented on Oct 13, 2022 
More actions
There hasn't been any activity on this issue recently, so we clean up some of the older and inactive issues. Please make sure to update to the latest version and check if that solves the issue. Let us know if that works for you by leaving a comment 👍 This issue has now been marked as stale and will be closed if no further activity occurs. Thanks!
###  22 remaining items
Load more
Loading
[Sign up for free](https://github.com/signup?return_to=https://github.com/hassio-addons/app-tailscale/issues/96)**to join this conversation on GitHub.** Already have an account? [Sign in to comment](https://github.com/login?return_to=https://github.com/hassio-addons/app-tailscale/issues/96)
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
