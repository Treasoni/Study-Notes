---
url: "https://www.virtualbox.org/ticket/18282"
title: "#18282 (EFI shell not shown when VMSVGA or VBoxSVGA is chosen. No installation is possible. => fixed in svn)\n          – Oracle VirtualBox"
scraped_at: 2026-09-17T16:09:07+00:00
---



Opened [8 years ago](https://www.virtualbox.org/timeline?from=2019-01-04T14%3A56%3A57Z&precision=second "See timeline at 01/04/2019 02:56:57 PM")
Closed [7 years ago](https://www.virtualbox.org/timeline?from=2019-04-17T10%3A23%3A47Z&precision=second "See timeline at 04/17/2019 10:23:47 AM")
##  [#18282](https://www.virtualbox.org/ticket/18282)
#  EFI shell not shown when VMSVGA or VBoxSVGA is chosen. No installation is possible. => fixed in svn  
| Reported by:  | Owned by:  |  
| --- | --- |  
|  Component:   |  Version:   |  
|  Keywords:   |  Cc:   |  
|  Guest type:   |  Host type:   |  
## Description [ ¶](https://www.virtualbox.org/ticket/18282#comment:description "Link to this section")
If the Graphics Controller is not set as a VBoxVGA, and a bootable medium is not provided, then the EFI shell never comes up. 
On top of that, none of the following ExtraData are honored if VMSVGA is chosen, the resolution comes up with the "default" 640x480 : 

```
<ExtraDataItem name="VBoxInternal2/EfiGopMode" value="3"/>
<ExtraDataItem name="VBoxInternal2/EfiGraphicsResolution" value="1280x1024"/>
<ExtraDataItem name="VBoxInternal2/EfiHorizontalResolution" value="1280"/>
<ExtraDataItem name="VBoxInternal2/EfiVerticalResolution" value="1024"/>

```

### [ Change History (17)](https://www.virtualbox.org/ticket/18282#no1)
###  by Socratis, [8 years ago](https://www.virtualbox.org/timeline?from=2019-01-04T15%3A18%3A52Z&precision=second "See timeline at 01/04/2019 03:18:52 PM")
**UPDATE** Actually it's worse than simply not having the shell showing; no booting happens. I tried a Win10-Oct1809 and an OSX 10.8.5 guests. No booting, no go, no matter the vGPU option, unless it's the old VBoxVGA... 
**UPDATE 2** I _hate_ that I can't edit my ticket, but if a gentle soul could amend the "No installation is possible." to the end of the ticket description, I'd appreciate it! 
Last edited [8 years ago](https://www.virtualbox.org/timeline?from=2019-01-04T15%3A58%3A08Z&precision=second "See timeline at 01/04/2019 03:58:08 PM") by Socratis ([previous](https://www.virtualbox.org/ticket/18282?cversion=0&cnum_hist=1#comment:1)) ([diff](https://www.virtualbox.org/ticket/18282?action=comment-diff&cnum=1&version=1)) 
###  by gombara, [8 years ago](https://www.virtualbox.org/timeline?from=2019-01-04T16%3A00%3A54Z&precision=second "See timeline at 01/04/2019 04:00:54 PM")  
| Summary:  |  EFI shell not shown when VMSVGA or VBoxSVGA is chosen. → EFI shell not shown when VMSVGA or VBoxSVGA is chosen. No installation is possible.  |  
| --- | --- |  
###  by Socratis, [8 years ago](https://www.virtualbox.org/timeline?from=2019-01-04T16%3A01%3A31Z&precision=second "See timeline at 01/04/2019 04:01:31 PM")
Thanks @gombara! 
###  by Klaus Espenlaub, [8 years ago](https://www.virtualbox.org/timeline?from=2019-01-07T18%3A28%3A58Z&precision=second "See timeline at 01/07/2019 06:28:58 PM")
The cause is quite simple: as of today there's no graphics driver in the EFI firmware which handles VMSVGA or VBoxSVGA. For VBoxSVGA it should be a limited effort (since it's mostly compatible with VBoxVGA), and for VMSVGA it's more work. All open source, see the EFI firmware directory. 
###  by Akemi Yagi, [8 years ago](https://www.virtualbox.org/timeline?from=2019-01-07T18%3A38%3A05Z&precision=second "See timeline at 01/07/2019 06:38:05 PM")
CC: me 
###  by Socratis, [8 years ago](https://www.virtualbox.org/timeline?from=2019-01-07T20%3A43%3A05Z&precision=second "See timeline at 01/07/2019 08:43:05 PM")
I understand the part about the EFI and the "age"/maturity of the VBoxSVGA/VMSVGA; they both need some work. I just wanted to have a placeholder so that the developers won't forget. ;) 
But mainly so that I can point people to something tangible... 
###  by Fake4d, [8 years ago](https://www.virtualbox.org/timeline?from=2019-02-11T07%3A31%3A42Z&precision=second "See timeline at 02/11/2019 07:31:42 AM")
CC: me 
###  by rjcuk, [8 years ago](https://www.virtualbox.org/timeline?from=2019-02-12T23%3A44%3A05Z&precision=second "See timeline at 02/12/2019 11:44:05 PM")
CC: me on [VirtualBox](https://www.virtualbox.org/wiki/VirtualBox) 6.0.4 
###  by Klaus Espenlaub, [8 years ago](https://www.virtualbox.org/timeline?from=2019-02-15T16%3A21%3A36Z&precision=second "See timeline at 02/15/2019 04:21:36 PM")
Latest 6.0 [Testbuilds](https://www.virtualbox.org/wiki/Testbuilds) should have this issue fixed. Both for VBoxSVGA and VMSVGA. Please confirm, feedback is much appreciated. 
###  by Socratis, [8 years ago](https://www.virtualbox.org/timeline?from=2019-02-15T17%3A11%3A58Z&precision=second "See timeline at 02/15/2019 05:11:58 PM")
Confirmed as fixed with version 6.0.5 r128870 (Qt5.6.3). 
Tested with a Win10-64 (VBoxSVGA), and Ubuntu 18.10 (VMSVGA) guests on an OSX 10.11.6 host. 
Thanks @klaus! 
###  by Klaus Espenlaub, [8 years ago](https://www.virtualbox.org/timeline?from=2019-02-15T21%3A28%3A52Z&precision=second "See timeline at 02/15/2019 09:28:52 PM")  
| Summary:  |  EFI shell not shown when VMSVGA or VBoxSVGA is chosen. No installation is possible. → EFI shell not shown when VMSVGA or VBoxSVGA is chosen. No installation is possible. => fixed in svn  |  
| --- | --- |  
###  by Mike Vastola, [8 years ago](https://www.virtualbox.org/timeline?from=2019-02-21T02%3A10%3A21Z&precision=second "See timeline at 02/21/2019 02:10:21 AM")
CC: me 
###  by 林博仁(Buo-Ren, Lin), [8 years ago](https://www.virtualbox.org/timeline?from=2019-02-21T07%3A12%3A45Z&precision=second "See timeline at 02/21/2019 07:12:45 AM")
CC: me 
###  by Socratis, [8 years ago](https://www.virtualbox.org/timeline?from=2019-02-21T09%3A24%3A09Z&precision=second "See timeline at 02/21/2019 09:24:09 AM")
@ALL 
It would be more beneficial if you could give your some feedback with regards to the [test builds](https://www.virtualbox.org/wiki/Testbuilds), instead of simply Cc:ing yourselves to the ticket... ;) 
Anything over r128870 would do... 
###  by Fake4d, [8 years ago](https://www.virtualbox.org/timeline?from=2019-02-22T06%3A25%3A10Z&precision=second "See timeline at 02/22/2019 06:25:10 AM")
@socratis : You are right :) Had to smile a little bit! 
I tried the built 6.0.x revision 128914 on Linux 64bit (Ubuntu 18.04.2) and Windows 10 (1809). Both working for me - your new built seems fine in my setup. 
###  by Socratis, [8 years ago](https://www.virtualbox.org/timeline?from=2019-02-22T09%3A33%3A28Z&precision=second "See timeline at 02/22/2019 09:33:28 AM")
I'm sure a developer _"just got their wings"_... :) 
Thanks @Fake4d for confirming... 
###  by Michael Thayer, [7 years ago](https://www.virtualbox.org/timeline?from=2019-04-17T10%3A23%3A47Z&precision=second "See timeline at 04/17/2019 10:23:47 AM")  
| Resolution:  |  → fixed  |  
| --- | --- |  
| Status:  |  new → closed  |  
**Note:** See [TracTickets](https://www.virtualbox.org/wiki/TracTickets) for help on using tickets. 
### Download in other formats:
  * [ Comma-delimited Text](https://www.virtualbox.org/ticket/18282?format=csv)
  * [ Tab-delimited Text](https://www.virtualbox.org/ticket/18282?format=tab)


Powered by [**Trac 1.4.3.2**](https://www.virtualbox.org/about) By [Edgewall Software](http://www.edgewall.org/) . 
[ © 2025 Oracle](https://www.oracle.com) [Support](https://www.oracle.com/virtualization/virtualbox/#rc30category-support-services) [Privacy ](https://www.oracle.com/html/privacy.html) / [ Do Not Sell My Info](https://www.oracle.com/legal/privacy/privacy-choices.html) [Terms of Use](https://www.oracle.com/html/terms.html) [Trademark Policy](https://www.oracle.com/legal/trademarks.html) [Automated Access Etiquette](https://www.virtualbox.org/wiki/AutomatedAccessEtiquette)
