---
url: "https://tailscale.com/docs/features/subnet-routers/how-to/setup"
title: "Configure a subnet router · Tailscale Docs"
scraped_at: 2026-08-27T16:20:42+00:00
---

[Aperture is GA! Build a home(lab) with AI.Read the blog ->](http://tailscale.com/blog/aperture-ga)
### Documentation
Close navigation
# Configure a subnet router
Last validated: Jan 5, 2026|Copy as Markdown|[View as Markdown](https://tailscale.com/docs/features/subnet-routers/how-to/setup.md)
This topic is a quick guide for configuring subnet routers in a tailnet. For more detailed information, see [Subnet routers](https://tailscale.com/docs/features/subnet-routers).
To use a tailnet device as a subnet router, select your platform and complete the steps.
  1. [Download and install](https://tailscale.com/docs/install/linux) the Tailscale client.
  2. Open a terminal session on the device and enable IP forwarding.
If your Linux system has a `/etc/sysctl.d` directory, use:

```
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf

```

Otherwise, use:

```
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p /etc/sysctl.conf

```

  3. In the terminal session, advertise subnet routes for the device. Replace the subnets in the example below with the subnets for your network.

```
sudo tailscale set --advertise-routes=192.0.2.0/24,198.51.100.0/24

```

  4. Go to the [Machines](https://console.tailscale.com/admin/machines) page of the admin console and locate the device in the list. It should display the **Subnets** badge.
  5. Select the menu, then select **Edit route settings**.
  6. Check the IP range boxes that correspond to the subnet routes you want to advertise, then select **Save**.


For more information about subnet router configuration with Tailscale, review [Subnet routers](https://tailscale.com/docs/features/subnet-routers).
