---
url: "https://tailscale.com/docs/how-to/quickstart"
title: "Tailscale quickstart · Tailscale Docs"
scraped_at: 2026-08-27T16:20:42+00:00
---

[Aperture is GA! Build a home(lab) with AI.Read the blog ->](http://tailscale.com/blog/aperture-ga)
### Documentation
Close navigation
# Tailscale quickstart
Last validated: Jan 5, 2026|Copy as Markdown|[View as Markdown](https://tailscale.com/docs/how-to/quickstart.md)
Welcome! Follow the steps in this topic to create your own private Tailscale network (known as a tailnet), or watch the following video to get started with Tailscale and set up some useful features.
## [Create a tailnet](https://tailscale.com/docs/how-to/quickstart#create-a-tailnet)
  1. Go to [`tailscale.com`](https://tailscale.com/) and select **Get Started**. Alternatively, you can [download and install](https://tailscale.com/docs/install) the Tailscale client on your device, then [sign up](https://login.tailscale.com/start).
  2. On the **Sign up with your identity provider** page, log in using a [single sign-on (SSO) identity provider](https://tailscale.com/docs/integrations/identity) account.
If you sign up using a custom-owned domain, you are automatically enrolled in the [Enterprise](https://tailscale.com/pricing) plan for a 14-day trial. If you sign up using a public domain email account such as `@gmail.com`, you are automatically enrolled in the [Personal](https://tailscale.com/pricing) plan, which entitles you to six free users and many of the features offered in the Enterprise plan. You can always change your plan. For more information, refer to [Manage your plan](https://tailscale.com/docs/account/manage-plans).
  3. On the **Welcome to Tailscale** page, select either **Business use** or **Personal use**.
  4. On the **Let's add your first device** page, select the OS that corresponds to the device you are using to download and install the client. Authenticate the client using the same credentials that you used to create the tailnet in step 2.
Once you are authenticated, the device will appear in the browser window.
  5. On the **Next, add a second device** page, select the OS for another machine to add to the tailnet. Copy the link and send it to the second device. After the second device is authenticated, both devices will display.
  6. Select **Take me home**. You will be redirected to the Tailscale [admin console](https://console.tailscale.com/admin). This interface lets you control most aspects of your tailnet including users, devices, DNS, permissions, authentication keys, and more.


## [Rename devices](https://tailscale.com/docs/how-to/quickstart#rename-devices)
Every device added to a tailnet, including servers, nodes, phones, and personal computers is assigned a unique name generated from the device's OS hostname. This name is displayed in the [Machines](https://console.tailscale.com/admin/machines) page of the admin console. You can also [rename a device](https://tailscale.com/docs/concepts/machine-names#renaming-a-machine) to help you locate and organize devices in the **Machines** page list.
## [Use MagicDNS](https://tailscale.com/docs/how-to/quickstart#use-magicdns)
[MagicDNS](https://tailscale.com/docs/features/magicdns) makes communicating with devices across your tailnet easier by allowing you to use the name listed in the **Machines** page of the admin console instead of an IP address. This works using automatically assigned OS hostnames or renamed device names. MagicDNS is enabled by default, and we recommend you keep it enabled.
## [Invite users](https://tailscale.com/docs/how-to/quickstart#invite-users)
There are two types of tailnet user invites.
Team member invites are for users who will authenticate using the same identity provider you used when creating the tailnet.
External invites are for users who are not part of your custom domain, such as contractors, friends, and family.
### [Team members](https://tailscale.com/docs/how-to/quickstart#team-members)
If your tailnet uses a custom domain (`example.com`), users with email addresses with the same domain can log in without needing an invite. Alternatively, you can send [team member invites](https://tailscale.com/docs/features/sharing/how-to/invite-team-members) to notify them to join.
### [External users](https://tailscale.com/docs/how-to/quickstart#external-users)
To invite external users to a tailnet, open the [Users](https://console.tailscale.com/admin/users) page of the admin console, select **Invite external users** , and choose one of the following options:
  * **Invite via email** to send one or more invites.
  * **Copy invite link** to share the invite link with others.


When users select the link, they will be directed to the Tailscale login page, where they can authenticate using a [supported single sign-on (SSO) identity provider](https://tailscale.com/docs/integrations/identity) account. Once they are authenticated, users are added on the **Users** page of the admin console.
For more information, refer to [Invite any user to your tailnet](https://tailscale.com/docs/features/sharing/how-to/invite-any-user).
## [Add devices](https://tailscale.com/docs/how-to/quickstart#add-devices)
You can add more devices to your tailnet using one of the following methods:
  * [Login](https://login.tailscale.com/login) to the tailnet from other devices using an existing user account.
  * Add servers to a tailnet using a [tag](https://tailscale.com/docs/features/tags) as the identity of the server, and provision the server using an [authentication key](https://tailscale.com/docs/features/access-control/auth-keys). For more information, refer to [Setting up a server on your Tailscale network](https://tailscale.com/docs/how-to/set-up-servers).
  * Incorporate your existing system policies such as mobile device management (MDM) to control device management. For more information, refer to [Integrate with an MDM solution](https://tailscale.com/docs/mdm).


Tailscale automatically assigns each device on your network a [unique 100.x.y.z IP address](https://tailscale.com/docs/concepts/ip-and-dns-addresses), to establish stable connections between machines no matter where they are in the world, even when they switch networks or are [behind a firewall](https://tailscale.com/blog/how-nat-traversal-works).
For more about adding devices, refer to [Add a device](https://tailscale.com/docs/features/access-control/device-management/how-to/set-up).
## [Secure traffic using exit nodes](https://tailscale.com/docs/how-to/quickstart#secure-traffic-using-exit-nodes)
Keep your internet activity private on an untrusted network by designating devices in your tailnet as exit nodes, then configure your tailnet devices to use those exit nodes.
  * For details on how to quickly configure and use exit nodes, refer to [Use exit nodes](https://tailscale.com/docs/features/exit-nodes/how-to/setup).
  * For more in-depth information about exit nodes, refer to the main [Exit nodes](https://tailscale.com/docs/features/exit-nodes) topic.


## [Route traffic using subnets](https://tailscale.com/docs/how-to/quickstart#route-traffic-using-subnets)
You can provide tailnet access to existing resources in your network using a subnet router. This can be useful if you need to access devices on which the Tailscale client cannot be installed, such as printers.
  * For details on how to quickly configure and use a subnet router, refer to [Configure a subnet router](https://tailscale.com/docs/features/subnet-routers/how-to/setup).
  * For more in-depth information about subnet routers, refer to the main [Subnet routers](https://tailscale.com/docs/features/subnet-routers) topic.


## [Manage permissions with access control policies](https://tailscale.com/docs/how-to/quickstart#manage-permissions-with-access-control-policies)
You can define your own custom permission for the users and devices in your tailnet, using [access control policies](https://tailscale.com/docs/features/access-control) (such as [ACLs](https://tailscale.com/docs/features/access-control/acls) or [grants](https://tailscale.com/docs/features/access-control/grants)). These permissions are configured in the tailnet policy file, which is located on the [Access controls](https://console.tailscale.com/admin/acls) page of the admin console.
## [Monitor and log traffic](https://tailscale.com/docs/how-to/quickstart#monitor-and-log-traffic)
You can monitor and log tailnet activity such as network traffic, client activity, tailnet configuration changes, and SSH session recordings.
For more information, refer to [Logging, auditing, and streaming](https://tailscale.com/docs/features/logging).
## [Use cases](https://tailscale.com/docs/how-to/quickstart#use-cases)
Need some inspiration? Tailscale can be used for a wide variety of users and environments. This section provides guidance for some common scenarios that you may want to use in your tailnet.
  * Interact with tailnet resources from Visual Studio Code using our [Visual Studio Code extension](https://tailscale.com/docs/integrations/vscode-extension).
  * Deploy, scale, and manage containerized applications such as [Kubernetes](https://tailscale.com/docs/kubernetes), [Docker](https://tailscale.com/docs/features/containers/docker), and [Proxmox](https://tailscale.com/docs/integrations/proxmox).
  * [Connect to serverless apps](https://tailscale.com/docs/integration-serverless-apps) such as AWS App Runner, AWS Lambda, Google Cloud Run, and Heroku.
  * [Connect to cloud services](https://tailscale.com/docs/cloud-server) such as AWS, Azure, Google Compute Engine, Hetzner, and Oracle Cloud.
  * Share local services on your machine such as web applications, accessible only from your tailnet using [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve) or share publicly over the internet using [Tailscale Funnel](https://tailscale.com/docs/features/tailscale-funnel).
  * [Share prototype servers](https://tailscale.com/docs/concepts/local-team-server) with other colleagues without needing to modify firewall settings.


  * Manage the authentication and authorization of SSH connections in your tailnet using [Tailscale SSH](https://tailscale.com/docs/features/tailscale-ssh).
  * Integrate Tailscale deployments on [AWS](https://tailscale.com/docs/reference/reference-architectures/aws) and [Azure](https://tailscale.com/docs/reference/reference-architectures/azure).
  * Control device and user access to your third-party applications without requiring any end-user configuration using [app connectors](https://tailscale.com/docs/features/app-connectors).
  * Control what users can access in their Tailscale client using [system policies](https://tailscale.com/docs/features/tailscale-system-policies).
  * Use [Tailscale SSH session recording](https://tailscale.com/docs/features/tailscale-ssh/tailscale-ssh-session-recording) to stream recordings of Tailscale SSH sessions from the destination node to a recorder node in your tailnet.
  * Automate aspects of your Tailscale network using the [Tailscale API](https://tailscale.com/docs/reference/tailscale-api).
  * Share an existing service with your peers outside your domain with [node sharing](https://tailscale.com/docs/features/sharing).
  * Administer a computer remotely and lock down your [connections to a Microsoft Remote Desktop Protocol (RDP) server](https://tailscale.com/docs/solutions/access-remote-desktops-using-windows-rdp).


### [Personal users](https://tailscale.com/docs/how-to/quickstart#personal-users)
  * Connect an [Apple TV](https://tailscale.com/docs/install/appletv) to your tailnet for viewing your media server files, use your Apple TV as an [exit node](https://tailscale.com/docs/features/exit-nodes) to route traffic through your home internet connection when you're away, or choose an exit node to route your Apple TV's traffic through.
  * Receive files from a [network attached storage](https://tailscale.com/docs/integrations/nas) (NAS) server using FTP, and access media files from players such as VLC, Plex, and JellyFin.
  * Implement DNS-based ad blocking for your tailnet using [Control D](https://tailscale.com/docs/integrations/control-d), [NextDNS](https://tailscale.com/docs/integrations/nextdns) or a [Pi-hole](https://tailscale.com/docs/solutions/block-ads-all-devices-anywhere-using-raspberry-pi) server.
  * Share files between your own devices, even across operating systems, with [Taildrop](https://tailscale.com/docs/features/taildrop).
  * Host a private server for you and your peers to play [Minecraft](https://tailscale.com/docs/solutions/set-up-minecraft) or chat on IRC.


## [Troubleshooting and support](https://tailscale.com/docs/how-to/quickstart#troubleshooting-and-support)
Visit our [Support](https://tailscale.com/contact/support) page to read common questions and answers, file bugs, request new features, observe Tailscale's operational status, or engage directly with our Support team.
Here are some links that provide assistance for common inquiries:
  * [Troubleshooting guide](https://tailscale.com/docs/reference/troubleshooting)
  * [Production best practices](https://tailscale.com/docs/reference/best-practices/production)
  * [Security best practices](https://tailscale.com/docs/reference/best-practices/security)
  * [Using Tailscale with your firewall](https://tailscale.com/docs/integrations/firewalls)


