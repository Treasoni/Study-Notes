---
url: "https://access.redhat.com/solutions/450913"
title: "Diagnosing CIFS Permission denied or \"cifs_mount failed w/return code = -13\" errors             - Red Hat Customer Portal"
scraped_at: 2026-09-18T07:26:00+00:00
---

## Issue
  * Attempted to mount CIFS share manually, for example:

```
[root@flandre-examplebox ~]# mount -t cifs -o credentials=/etc/user-file //remilia-examplebox/  pachiouli /knowledge
mount error(13): Permission denied

```

  * Mounting using `/etc/fstab` with `mount -a` also fails:

```
[root@flandre-examplebox ~]# mount -a
mount error(13): Permission denied

```

  * The following messages are present in `/var/log/messages` from mount attempts:

```
Aug  9 22:39:39 flandre-examplebox kernel: Status code returned 0xc000006d  NT_STATUS_LOGON_FAILURE
Aug  9 22:39:39 flandre-examplebox kernel: CIFS VFS: Send error in SessSetup = -13
Aug  9 22:39:39 flandre-examplebox kernel: CIFS VFS: cifs_mount failed w/return code = -13

```

  * The error `Credential formatted incorrectly: (null)` appears in verbose mount command output:

```
[root@flandre-examplebox ~]# mount -vvv -t cifs -o credentials=/etc/user-file //remilia-  examplebox/pachiouli /knowledge
----8<---- (output trimmed)
Credential formatted incorrectly: (null)
mount.cifs kernel mount options: ip=123.123.123.123,unc=\\remilia-  examplebox\pachiouli,credentials=/etc/user- file,ver=1,user=USER,domain=DOMAIN,prefixpath=DOMAIN/USER,pass=********
mount error(13): Permission denied
Refer to the mount.cifs(8) manual page (e.g. man mount.cifs)

```



## Environment
  * Red Hat Enterprise Linux (RHEL)
  * Various types of CIFS servers


## Subscriber exclusive content
A Red Hat subscription provides unlimited access to our knowledgebase, tools, and much more.
### Current Customers and Partners
Log in for full access
[Log In](https://access.redhat.com/login?redirectTo=https://access.redhat.com/solutions/450913)
### New to Red Hat?
[Learn more about Red Hat subscriptions](https://access.redhat.com/transitioning-rhsm-to-hybrid-cloud-console)
### Using a Red Hat product through a public cloud?
[How to access this content](https://access.redhat.com/articles/public-cloud-marketplace-access)
[ LinkedIn ](https://www.linkedin.com/company/red-hat) [ YouTube ](https://www.youtube.com/user/RedHatVideos) [ Facebook ](https://www.facebook.com/RedHat) [ X, formerly Twitter ](https://twitter.com/RedHat)
### Quick Links
  * [Product Documentation](https://docs.redhat.com)


### Help
  * [Contact Customer Portal](https://access.redhat.com/support/contact/)
  * [Customer Portal FAQ](https://access.redhat.com/articles/33844)


### Site Info
  * [Browser Support Policy](https://www.redhat.com/en/about/browser-support)
  * [Awards and Recognition](https://access.redhat.com/recognition/)


### Related Sites
  * [developers.redhat.com](http://developers.redhat.com/)
  * [connect.redhat.com](https://connect.redhat.com/)


### Systems Status
### About
  * [Red Hat Subscription Value](https://access.redhat.com/subscription-value)


### Red Hat legal and privacy links
  * [Inclusion at Red Hat](https://www.redhat.com/en/about/our-culture/inclusion)
  * [Cool Stuff Store](https://coolstuff.redhat.com/)

Copyright © 2026 Red Hat
### Red Hat legal and privacy links
  * [Privacy statement](https://redhat.com/en/about/privacy-policy)
  * [All policies and guidelines](https://redhat.com/en/about/all-policies-guidelines)
  * [Digital accessibility](https://redhat.com/en/about/digital-accessibility)
  * 

## How we use cookies
We use cookies on our websites to deliver our online services. Details about how we use cookies and how you may disable them are set out in our [Privacy Statement](http://www.redhat.com/en/about/privacy-policy#cookies). By using this website you agree to our use of cookies. 
Accept All More Options
×
### Formatting Tips
Here are the common uses of Markdown. 

Code blocks
    

```
~~~
Code surrounded in tildes is easier to read
~~~
```


Links/URLs
    `[Red Hat Customer Portal](https://access.redhat.com)`
[Learn more](https://access.redhat.com/help/markdown) Close
#### Request a English Translation
Are you sure you want to update a translation? It seems an existing [English Translation](https://access.redhat.com/solutions/@url) exists already. We appreciate your interest in having Red Hat content localized to your language. Please note that excessive use of this feature could cause delays in getting specific content you are interested in translated. 
Close
[Request Japanese Translation](https://access.redhat.com/solutions/450913?rate=jRowOKiWJst6c4Xqiuqr2t3G2IetTBYQ_Bf6DBuDkdE "Request Japanese Translation") [Request Chinese Translation](https://access.redhat.com/solutions/450913?rate=pFXQhvLhCR5wq9VA-RDzKvEeaLaLGIgzMXFIUROKlmg "Request Chinese Translation") [Request Korean Translation](https://access.redhat.com/solutions/450913?rate=MbJn59Gcat3s1wTt3XBgTqDbTODuWD_Ecbi9Biiifto "Request Korean Translation")
#### Generating Machine Translation
Loading…
We are generating a machine translation for this content. Depending on the length of the content, this process could take a while. 
Cancel
