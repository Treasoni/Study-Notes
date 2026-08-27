---
url: "https://tailscale.com/docs/concepts/tailscale-ip-addresses.md"
scraped_at: 2026-08-27T19:22:06+00:00
---


```
# What are these 100.x.y.z addresses?

Last validated Jan 12, 2026

Tailscale automatically assigns a unique IP address to each device in your Tailscale network (known as a [tailnet][docs-tailnet]). This IP address is known as a Tailscale IP address and comes from the shared address space defined in [RFC6598][xt-rfc-6598-cgnat], known as Carrier-Grade NAT (CGNAT).

Tailscale IP addresses remain constant regardless of the device's physical location. Even if a device switches network connections, such as from Wi-Fi to a cellular network, its Tailscale IP address remains the same. Additionally, every tailnet device has local access to a private service IP address called [Quad100 (`100.100.100.100`)][docs-what-is-quad100]. Tailscale also reserves specific address ranges for internal services. Refer to [reserved IP addresses][docs-reserved-ip-addresses] for details.

IP addresses from the CGNAT range are [special-use][xt-rfc-5735-special-use] IPv4 addresses from the `100.64.0.0/10` subnet (`100.64.0.0` through `100.127.255.255`). They're similar to other special-use IP addresses (such as private IP addresses); they differ from private IP addresses in that they're reserved for Internet Service Provider (ISP) networks and routing equipment rather than private networks.

Tailscale uses IP addresses from the CGNAT range for the following reasons:

* They don't conflict with IP addresses from subnets commonly used for private networks (such as `10.0.0.0/8` and `192.168.0.0/16`). However, conflicts might occur when using Tailscale with [other VPNs that use the same address space][docs-other-vpns].

* They're for intermediate traffic that requires additional NAT before reaching the public internet, which is precisely [how Tailscale uses these addresses][bl-how-tailscale-works].

* They're for Internet Service Providers (ISPs) rather than private networks. Philosophically, [Tailscale][docs-what-is-tailscale] is a service provider creating a shared network on top of the regular internet. Tailscale IP addresses aren't exposed to the public internet.

[bl-how-tailscale-works]: /blog/how-nat-traversal-works

[docs-other-vpns]: /docs/reference/faq/other-vpns

[docs-tailnet]: /docs/concepts/tailnet

[docs-what-is-quad100]: /docs/reference/quad100

[docs-what-is-tailscale]: /docs/concepts/what-is-tailscale

[xt-rfc-5735-special-use]: https://www.rfc-editor.org/rfc/rfc5735.html

[docs-reserved-ip-addresses]: /docs/reference/reserved-ip-addresses

[xt-rfc-6598-cgnat]: https://www.rfc-editor.org/rfc/rfc6598.html

```

