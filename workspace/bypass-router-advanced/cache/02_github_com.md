---
url: "https://github.com/istoreos/istoreos/issues/2066"
title: "最新版istoreos系统的几个问题。 · Issue #2066 · istoreos/istoreos"
scraped_at: 2026-09-23T06:05:30+00:00
---

[Skip to content](https://github.com/istoreos/istoreos/issues/2066#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/istoreos/istoreos/issues/2066) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/istoreos/istoreos/issues/2066) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/istoreos/istoreos/issues/2066) to refresh your session. Dismiss alert
/ Public
  * [ Notifications ](https://github.com/login?return_to=%2Fistoreos%2Fistoreos) You must be signed in to change notification settings
  * [ Fork 921 ](https://github.com/login?return_to=%2Fistoreos%2Fistoreos)
  * [ Star  8.1k ](https://github.com/login?return_to=%2Fistoreos%2Fistoreos)


#  最新版istoreos系统的几个问题。
New issue
Copy link
New issue
Copy link
[最新版istoreos系统的几个问题。](https://github.com/istoreos/istoreos/issues/2066#top)#2066
Copy link
## Description
opened [on Jan 17, 2025](https://github.com/istoreos/istoreos/issues/2066#issue-2794318869)
Last edited by kygsmsc
Issue body actions
这两天升级办公室的网络设备，实体X86小主机安装istoreOS作为旁路由，爱快路由器做主路由，发现几个问题如下： 1.istoreos利用自带的设置向导设置为旁路由时，不会自动关闭DHCP，需要手动勾选忽略此接口。 2.即便你手动在DHCP勾选忽略此接口，但是当电脑网卡设置成自动获取IP后，IP是不会获取了，但网关会获取成istoreOS旁路由的IP。 3.istoreOS系统商店中安装PVE提示失败，但已安装中会出现PVE，打卡PVE菜单，选择右下方的安装还是提示安装失败。安装KVM没有这样的问题。
## Activity
### jjm2473 commented on Jan 17, 2025 
Contributor
More actions
这个你取消勾选了吗？ 
### kygsmsc commented on Jan 18, 2025 
Author
More actions
问题1解决了，问题2再次测试，发现有的电脑会获取到网关，有的不会。问题3问题依旧存在。
### jjm2473 commented on Jan 19, 2025 
Last edited by jjm2473
Contributor
More actions
如果istoreos的dhcp服务都关了，那你的电脑获取不到网关跟istoreos有什么关系？应该要去检查dhcp服务啊。
PVE插件的问题到这里反馈 <https://github.com/linkease/openwrt-app-actions/issues> ，带上配置截图，更重要的是带上报错信息，我才好转给插件作者看。
### kc-bao commented on Oct 8, 2025 
Collaborator
More actions
此问题已在 **酷友社** 上被提及。那里可能有相关详细信息：
<https://www.koolcenter.com/t/topic/1886/1>
[Sign up for free](https://github.com/signup?return_to=https://github.com/istoreos/istoreos/issues/2066)**to join this conversation on GitHub.** Already have an account? [Sign in to comment](https://github.com/login?return_to=https://github.com/istoreos/istoreos/issues/2066)
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
### Participants
## Issue actions
  * Open in GitHub Copilot app


You can’t perform that action at this time. 
