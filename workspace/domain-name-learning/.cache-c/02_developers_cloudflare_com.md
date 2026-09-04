---
url: "https://developers.cloudflare.com/tunnel/"
title: "Cloudflare Tunnel · Cloudflare Docs"
scraped_at: 2026-09-04T04:45:09+00:00
---

[Skip to content](https://developers.cloudflare.com/tunnel/#main-content)
> Documentation IndexFetch the complete documentation index at: https://developers.cloudflare.com/tunnel/llms.txtUse this file to discover all available pages before exploring further.
# Cloudflare Tunnel
Last updated May 5, 2026|Copy as Markdown|[View as Markdown](https://developers.cloudflare.com/tunnel/index.md)|[Agent setup](https://developers.cloudflare.com/agent-setup/)
Securely connect your origin servers, APIs, and services to Cloudflare with post-quantum encrypted tunnels — no public IPs required.
Available on all plans
Cloudflare Tunnel connects your infrastructure to Cloudflare through an outbound-only, [post-quantum encrypted](https://developers.cloudflare.com/ssl/post-quantum-cryptography/) connection. Instead of exposing a public IP, you install a lightweight daemon called `cloudflared` on your server. It creates a persistent tunnel to Cloudflare's global network, so all traffic to your origins flows through Cloudflare — where CDN caching, WAF, Bot Management, and DDoS protection are applied automatically.
No open inbound ports. No public IPs. No attack surface.
## How it works
  1. Install `cloudflared` on your server or network.
  2. `cloudflared` establishes outbound, post-quantum encrypted connections to Cloudflare — no inbound ports or firewall changes required.
  3. Map public hostnames to local services (for example, `app.example.com` to `http://localhost:8080`).
  4. Traffic flows through Cloudflare's network to your origin, with full CDN and security applied.


Each tunnel maintains four long-lived connections to two Cloudflare data centers for built-in redundancy. You can run multiple `cloudflared` [replicas](https://developers.cloudflare.com/tunnel/configuration/#replicas-and-high-availability) for additional high availability.
## Use cases
  * **Secure origin connectivity** — Eliminate public origin IPs. All traffic flows through Cloudflare with CDN, WAF, and DDoS protection applied.
  * **Public ingress routing** — Publish internal applications to the internet by mapping public hostnames to local services. Supports HTTP, HTTPS, TCP, SSH, RDP, and [more](https://developers.cloudflare.com/tunnel/routing/#supported-protocols).
  * **Workers VPC** — Enable [Cloudflare Workers](https://developers.cloudflare.com/workers-vpc/) to securely access private databases, APIs, and services through your tunnel.
  * **Load Balancing** — Use tunnels as origin endpoints in [Cloudflare Load Balancer](https://developers.cloudflare.com/load-balancing/) pools for high availability and intelligent traffic steering.


## Get started
### [Create your first tunnel](https://developers.cloudflare.com/tunnel/setup/)
Set up a tunnel in under 5 minutes using the dashboard or API.
DNS records, protocols, and load balancing for published applications.
Cloudflare One, Workers VPC, Load Balancing, Access, and more.
### [Configuration](https://developers.cloudflare.com/tunnel/configuration/)
Replicas, firewall rules, tokens, and runtime parameters.
Was this helpful?
Yes
