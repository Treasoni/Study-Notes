---
url: "https://tailscale.com/docs/features/client/manage-preferences"
title: "Manage client preferences · Tailscale Docs"
scraped_at: 2026-09-12T14:20:57+00:00
---

[See everything you missed at TailscaleUp.Read the recap →](https://tailscale.com/tailscaleup-date-week-26)
### Documentation
Close navigation
# Manage client preferences
Last validated: Jan 5, 2026|Copy as Markdown|[View as Markdown](https://tailscale.com/docs/features/client/manage-preferences.md)
[Admins](https://tailscale.com/docs/reference/user-roles) can manage devices on a network, and restrict which devices can connect using access control policies.
Individual users still have control over their own devices, to block incoming connections from Tailscale or to ignore Tailscale's DNS settings and advertised routes.
## [Default configuration](https://tailscale.com/docs/features/client/manage-preferences#default-configuration)
By default, a Tailscale client will:
  * Allow incoming connections
  * Use Tailscale DNS settings


macOS, Windows, and other non-Linux devices use Tailscale subnets by default. Linux devices do not use Tailscale by default.
## [Allow incoming connections](https://tailscale.com/docs/features/client/manage-preferences#allow-incoming-connections)
If other devices in your tailnet are allowed to connect to your device based on access control policies, then the connection will be created. Access control policies are directional, so that an access rule allowing your laptop to connect to a web server does not allow the web server to establish connections to your laptop.
If you want to block all incoming connections, you can do so. This is also known as "shields up". In the menu bar of your device, uncheck **Allow incoming connections**. When unchecked, your device will still be visible and allowed to _send_ traffic, but won't _accept_ any connections over Tailscale, including pings.
### [Toggling incoming connections](https://tailscale.com/docs/features/client/manage-preferences#toggling-incoming-connections)
This can be configured in the client menu bar or the CLI.
### [In the client menu bar](https://tailscale.com/docs/features/client/manage-preferences#in-the-client-menu-bar)
If you are running Tailscale v1.60.0 or later, from the menu bar, select Tailscale, select **Settings** , and then check/uncheck **Allow incoming connections**.
If you are running a version of Tailscale earlier than v1.60.0, from the menu bar, select Tailscale and check/uncheck **Allow incoming connections**.
To block incoming connections:

```
tailscale set --shields-up

```

To allow incoming connections (default):

```
tailscale set --shields-up=false

```

## [Use Tailscale DNS settings](https://tailscale.com/docs/features/client/manage-preferences#use-tailscale-dns-settings)
If an Admin has configured [DNS settings for your tailnet, including MagicDNS or split DNS](https://tailscale.com/docs/reference/dns-in-tailscale), then DNS queries for devices in your Tailscale network will respect those settings.
If you are using an [exit node](https://tailscale.com/docs/features/exit-nodes), your local DNS is the DNS for the exit node, not your device.
This can be configured in the client menu bar or the CLI.
### [In the client menu bar](https://tailscale.com/docs/features/client/manage-preferences#in-the-client-menu-bar-1)
If you want to only use local DNS, in the menu bar of your device, uncheck **Use Tailscale DNS settings**.
To use Tailscale DNS settings (default):

```
tailscale set --accept-dns=true

```

To not use Tailscale DNS settings:

```
tailscale set --accept-dns=false

```

## [Use Tailscale subnets](https://tailscale.com/docs/features/client/manage-preferences#use-tailscale-subnets)
If an Admin has created [subnet routes](https://tailscale.com/docs/features/subnet-routers) for your tailnet, then Tailscale will route your device's traffic for the advertised subnets to the appropriate subnet router.
This can be configured in the client menu bar or the CLI.
### [In the client menu bar](https://tailscale.com/docs/features/client/manage-preferences#in-the-client-menu-bar-2)
If you want to ignore the advertised routes, in the menu bar of your device, uncheck **Use Tailscale subnets**.
To use Tailscale subnets (default, except for Linux):

```
tailscale set --accept-routes=true

```

To not use Tailscale subnets (default on Linux):

```
tailscale set --accept-routes=false

```

