---
url: "https://tailscale.com/docs/reference/troubleshooting/network-configuration/ip-forwarding-errors-advertise"
title: "Troubleshoot IP forwarding issues when advertising subnet routes or exit nodes · Tailscale Docs"
scraped_at: 2026-08-27T19:22:06+00:00
---

[Aperture is GA! Build a home(lab) with AI.Read the blog ->](http://tailscale.com/blog/aperture-ga)
### Documentation
Close navigation
# Troubleshoot IP forwarding issues when advertising subnet routes or exit nodes
Last validated: Mar 16, 2026|Copy as Markdown|[View as Markdown](https://tailscale.com/docs/reference/troubleshooting/network-configuration/ip-forwarding-errors-advertise.md)
Tailscale's routing features ([subnet routers](https://tailscale.com/docs/features/subnet-routers) and [exit nodes](https://tailscale.com/docs/features/exit-nodes)) require IP forwarding to be enabled. If it is not enabled, you may encounter an error when using `--advertise-routes` or `--advertise-exit-node`.
For information about how to do this for your Linux device, refer to [Enable IP forwarding](https://tailscale.com/docs/features/subnet-routers#enable-ip-forwarding).
