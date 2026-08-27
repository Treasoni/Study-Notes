---
url: "https://github.com/tailscale/tailscale/issues/9605"
title: "The document of Docker Image is incorrect in the description of the 'TS_ROUTES' parameter! · Issue #9605 · tailscale/tailscale"
scraped_at: 2026-08-27T19:22:06+00:00
---

[Skip to content](https://github.com/tailscale/tailscale/issues/9605#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/tailscale/tailscale/issues/9605) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/tailscale/tailscale/issues/9605) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/tailscale/tailscale/issues/9605) to refresh your session. Dismiss alert
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/tailscale/tailscale/issues/9605).
/ Public
  * [ Notifications ](https://github.com/login?return_to=%2Ftailscale%2Ftailscale) You must be signed in to change notification settings
  * [ Fork 3.1k ](https://github.com/login?return_to=%2Ftailscale%2Ftailscale)
  * [ Star  35.7k ](https://github.com/login?return_to=%2Ftailscale%2Ftailscale)


#  The document of Docker Image is incorrect in the description of the 'TS_ROUTES' parameter!
Copy link
Copy link
Closed
Closed
[The document of Docker Image is incorrect in the description of the 'TS_ROUTES' parameter!](https://github.com/tailscale/tailscale/issues/9605#top)#9605
Copy link
Assignees
Labels
[Likelihood](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22L2%20Few%22)Likelihood[P1 NuisancePriority level](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22P1%20Nuisance%22)Priority level[T4 DocsIssue type](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22T4%20Docs%22)Issue type[Bug](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22bug%22)Bug
## Description
opened [on Sep 30, 2023](https://github.com/tailscale/tailscale/issues/9605#issue-1920133484)
Issue body actions
### What is the issue?
Description of "TS_ROUTES" in <https://hub.docker.com/r/tailscale/tailscale>:
> "TS_ROUTES: Accept [subnet routes](https://tailscale.com/kb/1019/subnets/) that other nodes advertise. Linux devices default to not accepting routes."
In <https://tailscale.com/kb/1282/docker/#ts_routes>:
> "Accept [subnet routes](https://tailscale.com/kb/1019/subnets/) that other nodes advertise. Linux devices default to not accepting routes. This is equivalent to [tailscale set --accept-routes=](https://tailscale.com/kb/1080/cli/#set)."
Actrally, in code 
[tailscale/cmd/containerboot/main.go](https://github.com/tailscale/tailscale/blob/ab810f1f6d6fcb57068738b2212ff101cc3ac1c5/cmd/containerboot/main.go#L551-L575)
Lines 551 to 575 in [ab810f1](https://github.com/tailscale/tailscale/commit/ab810f1f6d6fcb57068738b2212ff101cc3ac1c5)  
|  // tailscaleSet uses cfg to run 'tailscale set' to set any known configuration  |  
| --- |  
|  // options that are passed in via environment variables. This is run after the  |  
|  // node is in Running state.  |  
|  func tailscaleSet(ctx context.Context, cfg *settings) error {   |  
|  args := []string{"--socket=" + cfg.Socket, "set"}   |  
|  if cfg.AcceptDNS {   |  
|  args = append(args, "--accept-dns=true")   |  
|  } else {   |  
|  args = append(args, "--accept-dns=false")   |  
|  if cfg.Routes != "" {   |  
|  args = append(args, "--advertise-routes="+cfg.Routes)   |  
|  if cfg.Hostname != "" {   |  
|  args = append(args, "--hostname="+cfg.Hostname)   |  
|  log.Printf("Running 'tailscale set'")   |  
|  cmd := exec.CommandContext(ctx, "tailscale", args...)   |  
|  cmd.Stdout = os.Stdout  |  
|  cmd.Stderr = os.Stderr  |  
|  if err := cmd.Run(); err != nil {   |  
|  return fmt.Errorf("tailscale set failed: %v", err)   |  
|  return nil  |  
On line 562, it is obvious that "TS_ROUTES" is used to set "--advertise-routes", not "--accept-route"
This has caused me a lot of trouble. When I set 'TS_ROUTES' to true, I got an error in the log saying "'true' is not a valid IP address or CIDR prefix", and I don't know what I did wrong.
Hope to be corrected.
### Steps to reproduce
_No response_
### Are there any recent changes that introduced the issue?
_No response_
### OS
Linux
### OS version
Ubuntu Server 23
### Tailscale version
1.50.0
### Other software
_No response_
### Bug report
_No response_
👍React with 👍1Reacted by pravardhanreddy
## Activity
[OneLostCat](https://github.com/OneLostCat)
added 
[Bug](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22bug%22)Bug
[on Sep 30, 2023](https://github.com/tailscale/tailscale/issues/9605#event-10516736278)
[knyar](https://github.com/knyar)
added 
[Likelihood](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22L2%20Few%22)Likelihood
[P1 NuisancePriority level](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22P1%20Nuisance%22)Priority level
[T4 DocsIssue type](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22T4%20Docs%22)Issue type
and removed [on Sep 30, 2023](https://github.com/tailscale/tailscale/issues/9605#event-10516952126)
### OneLostCat commented on Oct 5, 2023 
[on Oct 5, 2023](https://github.com/tailscale/tailscale/issues/9605#issuecomment-1748042353) via email
Author
More actions
Because Outlook treated this email as spam, I apologize for taking so long to reply. It's not like this. Because the comment at the top of this code<<https://github.com/tailscale/tailscale/blob/ab810f1f6d6fcb57068738b2212ff101cc3ac1c5/cmd/containerboot/main.go#L16C7-L16C46>> is written: TS_ROUTES: subnet routes to advertise. that means there's no problem with the code. The code works according to the designer's expectations. The problem lies in the document. Just like this<<https://hub.docker.com/r/tailscale/tailscale>> TS_ROUTES: Accept subnet routes that other nodes advertise. Linux devices default to not accepting routes. The description of the code in the document is incorrect. This is an error made by the person who wrote this document. So I said it was a "document error". The code actually has no issues.
________________________________ 发件人: Kianda ***@***.***> 发送时间: 2023年10月1日 3:13 收件人: tailscale/tailscale ***@***.***> 抄送: OneLostCat ***@***.***>; Author ***@***.***> 主题: Re: [tailscale/tailscale] The document of Docker Image is incorrect in the description of the 'TS_ROUTES' parameter! (Issue [#9605](https://github.com/tailscale/tailscale/issues/9605)) I think this is why I'm getting "Some peers are advertising routes but --accept-routes is false" on the health check. (Ubuntu 22.04 with Docker Tailscale 1.50.0) cfg.Routes should set also --accept-routes ? From this: if cfg.Routes != "" { args = append(args, "--advertise-routes="+cfg.Routes) } To this: if cfg.Routes != "" { args = append(args, "--advertise-routes="+cfg.Routes, "--accept-routes") } ― Reply to this email directly, view it on GitHub<[#9605 (comment)](https://github.com/tailscale/tailscale/issues/9605#issuecomment-1741840111)>, or unsubscribe<<https://github.com/notifications/unsubscribe-auth/AS2SFG5TB36SH532WSV7KFDX5BVPPANCNFSM6AAAAAA5NKMPNM>>. You are receiving this because you authored the thread.Message ID: ***@***.***>
[clairew](https://github.com/clairew)
self-assigned this
[on Nov 4, 2023](https://github.com/tailscale/tailscale/issues/9605#event-10858008183)
### clairew commented on Nov 4, 2023 
Contributor
More actions
Thanks! Updated documentation.
[clairew](https://github.com/clairew)
closed this as [completed](https://github.com/tailscale/tailscale/issues?q=is%3Aissue%20state%3Aclosed%20archived%3Afalse%20reason%3Acompleted)[on Nov 4, 2023](https://github.com/tailscale/tailscale/issues/9605#event-10860682845)
[Sign up for free](https://github.com/signup?return_to=https://github.com/tailscale/tailscale/issues/9605)**to join this conversation on GitHub.** Already have an account? [Sign in to comment](https://github.com/login?return_to=https://github.com/tailscale/tailscale/issues/9605)
## Metadata
## Metadata
### Assignees
  * [clairew](https://github.com/clairew)


### Labels
[Likelihood](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22L2%20Few%22)Likelihood[P1 NuisancePriority level](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22P1%20Nuisance%22)Priority level[T4 DocsIssue type](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22T4%20Docs%22)Issue type[Bug](https://github.com/tailscale/tailscale/issues?q=state%3Aopen%20label%3A%22bug%22)Bug
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
