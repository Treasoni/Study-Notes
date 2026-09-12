---
url: "https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/3"
title: "How to announce routes with Tailscale add-on in Home Assistant - Raspberry Pi - Tailscale"
scraped_at: 2026-09-12T14:20:57+00:00
---

[ Skip to where you left off (post 3) ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/3) [ Skip to last reply ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/4) [ Skip to top ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/1)  
[ Skip to main content ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/3#main-container)
This site is in staff only mode. Please continue to browse, but signing up is unavailable and only staff members can log in.
#  [ How to announce routes with Tailscale add-on in Home Assistant ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374)
You have selected **0** posts.
[ select all ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/3)
[ cancel selecting ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/3)
6.5k views  1 link 
[ Jan 2023  ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/1 "Jump to the first post")
3 / 4 
Feb 2023 
[ Feb 2023 ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/4)
##  post by BenZoFly on Jan 29, 2023 
##  post by BenZoFly on Jan 31, 2023 
[ BenZoFly ](https://forum.tailscale.com/u/benzofly)
[ Jan 2023 ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/2 "Post date")
Hi again,
For info I found out that the official Tailscale addon was deprecated, although not specified as such, while there’s another one that does the job instead, including a configuration option to announce routes from the add-on.
Alternate add-on is here:
For devices on the announced routes to be reachable from the container running Tailscale, the following configuration needs to be set in the addon (in addition to auth_key and hostname):
advertise_routes: the routes to be anounced userspace_networking: needs to be enabled (important or the route will be announced but routing will not exit the container!)
12 days later 
##  post by OH1MAC on Feb 13, 2023 
[ OH1MAC ](https://forum.tailscale.com/u/oh1mac)
[ Feb 2023 ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/3 "Post date")
Hi BenZoFly!
It seems I have had similar problems with my HA & Tailscale, or at least so I have understood. I do have generic understanding of the network, HA configuration and such, but after I read you post I must admit I may have lost my path 
Could you please elaborate what I may need to do in my case, based on your findings.
The case:
My local network (192.168.1.0/24), HAOS installed with tsujamin’s Tailscale addon. Remote network (192.168.2.0/24) and lots of IoT devices. Between is fully working Tailscale network.
The HAOS does not seem to “see” the remote subnet, at the remote side there is a Tailscale node with published subnets. and all other clients in the same Tailscale network can see all the devices from all the available networks (192.168.1.0/24, 192.168.2.0/24, Tailnet).
As I read your post I realised that the problem indeed must be in the way networking has been handled inside HAOS containers - and If I have now understood correctly the “Internal routing” between HAOS containers needs to be activated.
From this point I need some help to understand how the configuration on the tsujamin’s Tailscale add-nn need to be for such routing to happen.
The ultimate goal would be that the HAOS core and all add-ons (containers) are able to see, ping and communicate to all networks locally and all the published sub networks Tailscale is advertising from the remote side.
The needed extra configuration should then include “advertise_routes” and “userspace_networking”. The actual format of these configurations in the add-on’s YAML is something I am not that familiar with, nor understand the correct format of the parameters.
I read the Tailscale documentation about these, but as there were options not used in the YAML configuration format I got totally lost about how to do this.
I tried following but was not able to get the routes to work as planned:
advertise_routes: 192.168.2.0/24 userspace_networking: true <— I think that is fundamentally wrong!?
Any chance to have few thoughts from you for this? Much appreciated!
Br: Mac (OH1MAC)
##  post by BenZoFly on Feb 14, 2023 
[ BenZoFly ](https://forum.tailscale.com/u/benzofly)
[ Feb 2023 ](https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/4 "Post date")
Hi,
I think I was trying to solve another problem.
In my case I am using a client (e.g. my mobile) to access remotely Home Assistant, which is located in a vlan 192.168.2.x and itself talks to IoT devices in the vlans 192.168.3.x and 192.168.68.x.
I wanted to lock the IoT networks from the internet but still access the devices remotely via their local ip. So I am using HA as a jump server to the local network, after having crossed the Tailscale network so to say.
But I understand that you’re trying to do something different, the two vlans are at different exit points of the Tailscale network, right?
If that’s the case, then you need 2 routing nodes, one locally for routing 192.168.1.x and another one in the other location to announce the route 192.168.2.x. A Tailscale node only announces local vlans.
But I may have not grasped what you try to achieve?
Regards, B
Edit: re-reading your post, if HA is the only node on the one side, then HA is a single client, not a routing node. No need to announce routes if the devices on the « other side » only look for HA. You need a routing node on the other side to bridge Tailscale with you local lan though. This one will announce 2.x network. Then HA will know where to bounce to access the other nodes on the other side.
My addon configuration to reach other vlans locally to the HA instance 
[ image1328×981 30.5 KB ](https://canada1.discourse-cdn.com/flex030/uploads/tailscale/original/2X/9/9381c9278fbe1bb283c9e33dbfa9c655bd12ef10.png "image")
Reply
###  Related topics   
Topic list, column headers with buttons are sortable.  
|  Topic   |  Replies   |  Views   |  Activity   |  
| --- | --- | --- | --- |  
|  [Issue with avahi advertising when tailscale is running](https://forum.tailscale.com/t/issue-with-avahi-advertising-when-tailscale-is-running/2008)  |  
|  [Remote Home Assistant with tailscale](https://forum.tailscale.com/t/remote-home-assistant-with-tailscale/1961)  |  1.0k  |  
|  [Tailscale can’t access subnet devices in subnet router mode](https://forum.tailscale.com/t/tailscale-cant-access-subnet-devices-in-subnet-router-mode/3632)  |  1.8k  |  
|  [Am I misunderstanding subnet routing?](https://forum.tailscale.com/t/am-i-misunderstanding-subnet-routing/2622)  |  1.2k  |  
|  [Connect two house on network level via tailscale](https://forum.tailscale.com/t/connect-two-house-on-network-level-via-tailscale/2824)  |
