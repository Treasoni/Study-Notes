---
url: "https://god.ad/learn/how-tailscale-works"
title: "How Tailscale Works: Building a Mesh VPN on WireGuard — God Mode"
scraped_at: 2026-08-27T19:22:06+00:00
---

Share
# How Tailscale Works: Building a Mesh VPN on WireGuard
2026-04-24 · 26 min read
**Tailscale** is a mesh VPN built on top of [WireGuard](https://god.ad/learn/how-wireguard-works) that connects devices into a secure private network without requiring any infrastructure changes, port forwarding, or complex configuration. Unlike [traditional VPNs](https://god.ad/learn/how-vpns-work) that route all traffic through a central gateway, Tailscale creates **direct, peer-to-peer encrypted tunnels** between every pair of devices in your network. The result is a flat network where your laptop in a coffee shop, your server in AWS, and your Raspberry Pi at home can all reach each other directly as if they were on the same LAN.
What makes Tailscale remarkable from a networking perspective is that it solves one of the hardest problems in distributed systems: establishing direct connections between devices that are almost always behind [NAT](https://god.ad/learn/how-nat-works). Most of your devices do not have public [IP addresses](https://god.ad/learn/what-is-an-ip-address). They sit behind home routers, corporate firewalls, and carrier-grade NAT. Tailscale navigates all of this automatically, using a combination of STUN, relay servers, and aggressive NAT traversal techniques to punch through network boundaries.
To understand how Tailscale works, we need to separate it into two distinct planes: the **control plane** (coordination) and the **data plane** (actual traffic). This separation is the key architectural insight that makes Tailscale both secure and efficient.
Contents
  * [Architecture: Control Plane vs Data Plane](https://god.ad/learn/how-tailscale-works#architecture-control-plane-vs-data-plane)
  * [WireGuard: The Cryptographic Foundation](https://god.ad/learn/how-tailscale-works#wireguard-the-cryptographic-foundation)
  * [NAT Traversal: The Hard Problem](https://god.ad/learn/how-tailscale-works#nat-traversal-the-hard-problem)
  * [DERP: Detoured Encrypted Routing Protocol](https://god.ad/learn/how-tailscale-works#derp-detoured-encrypted-routing-protocol)
  * [Mesh Topology vs Hub-and-Spoke](https://god.ad/learn/how-tailscale-works#mesh-topology-vs-hub-and-spoke)
  * [ACL Policy Engine](https://god.ad/learn/how-tailscale-works#acl-policy-engine)
  * [Key Distribution and Rotation](https://god.ad/learn/how-tailscale-works#key-distribution-and-rotation)
  * [Subnet Routers](https://god.ad/learn/how-tailscale-works#subnet-routers)
  * [Tailscale vs Traditional VPN: A Comparison](https://god.ad/learn/how-tailscale-works#tailscale-vs-traditional-vpn-a-comparison)
  * [How Connection Establishment Works End-to-End](https://god.ad/learn/how-tailscale-works#how-connection-establishment-works-end-to-end)
  * [Tailscale IP Addressing](https://god.ad/learn/how-tailscale-works#tailscale-ip-addressing)
  * [Headscale: The Open-Source Coordination Server](https://god.ad/learn/how-tailscale-works#headscale-the-open-source-coordination-server)
  * [Advanced Features](https://god.ad/learn/how-tailscale-works#advanced-features)
  * [The BGP Connection](https://god.ad/learn/how-tailscale-works#the-bgp-connection)
  * [Security Model](https://god.ad/learn/how-tailscale-works#security-model)
  * [Limitations and Trade-offs](https://god.ad/learn/how-tailscale-works#limitations-and-trade-offs)
  * [How Tailscale Differs from Plain WireGuard](https://god.ad/learn/how-tailscale-works#how-tailscale-differs-from-plain-wireguard)
  * [Under the Hood: The Tailscale Client](https://god.ad/learn/how-tailscale-works#under-the-hood-the-tailscale-client)


## Architecture: Control Plane vs Data Plane
Tailscale's architecture is built on a fundamental separation between coordination and data transfer. This split is what allows it to be both centrally managed and fully peer-to-peer at the same time.
### The Control Plane (Coordination Server)
The **coordination server** is Tailscale's centrally operated service (at `controlplane.tailscale.com`). It never sees your actual network traffic. Instead, it performs three critical functions:
  * **Identity and authentication** — verifying who you are via your identity provider (Google, Microsoft, GitHub, Okta, etc.)
  * **Key distribution** — collecting each node's WireGuard public key and distributing them to authorized peers
  * **Network configuration** — assigning stable IP addresses (from the `100.64.0.0/10` CGNAT range), pushing ACL policies, and telling each node about the endpoints where its peers can be reached


When a device joins a Tailscale network (called a **tailnet**), the client generates a WireGuard keypair locally. The private key never leaves the device. The public key, along with the device's discovered network endpoints, is registered with the coordination server. The server then distributes a **network map** (netmap) to every authorized node, containing the public keys and known endpoints of all peers it is allowed to communicate with.
This is conceptually similar to how [DNS](https://god.ad/learn/what-is-dns) works: a centralized directory maps names to addresses, but the actual communication happens directly between endpoints. The coordination server is the phone book, not the phone line.
### The Data Plane (WireGuard Tunnels)
Once nodes have each other's public keys and endpoint information, they establish **direct WireGuard tunnels** between themselves. All actual data travels through these peer-to-peer encrypted tunnels. The coordination server is not in the data path at all. If Tailscale's coordination servers went down entirely, existing connections between nodes that already have each other's keys would continue to work. You just would not be able to add new devices or update configurations.
Each device in the tailnet runs a userspace WireGuard implementation (or, on Linux, can use the kernel WireGuard module). The Tailscale client manages the WireGuard configuration automatically, adding and removing peers, rotating keys, and updating endpoints as network conditions change.
Tailscale Architecture: Control Plane vs Data Plane Coordination Server Auth, key distribution, ACLs controlplane.tailscale.com CONTROL PLANE Laptop 100.64.0.1 (NAT) Cloud Server 100.64.0.2 (public) Phone 100.64.0.3 (4G NAT) Home Server 100.64.0.4 (NAT) Raspberry Pi 100.64.0.5 (NAT) Control plane (keys, config, auth) Data plane (WireGuard tunnels, direct P2P) DATA PLANE
This separation has a profound security benefit: even if Tailscale's coordination servers are compromised, an attacker cannot decrypt any existing traffic. The coordination server distributes public keys, not private keys. The worst an attacker could do is inject a rogue node into the network. And even that is mitigated by the fact that new devices require authentication through your identity provider.
## WireGuard: The Cryptographic Foundation
At its core, every Tailscale connection is a [WireGuard](https://god.ad/learn/how-wireguard-works) tunnel. WireGuard is a modern VPN protocol that is dramatically simpler than its predecessors (IPsec, OpenVPN). Its entire codebase is roughly 4,000 lines of code, compared to hundreds of thousands for OpenVPN or IPsec. This simplicity translates directly to security — less code means a smaller attack surface and easier auditability.
WireGuard uses a fixed set of modern cryptographic primitives:
  * **Curve25519** for Diffie-Hellman key exchange
  * **ChaCha20-Poly1305** for authenticated encryption
  * **BLAKE2s** for hashing
  * **SipHash24** for hashtable keys
  * **HKDF** for key derivation


There is no cipher negotiation, no version selection, and no protocol options. If a vulnerability is found in one of these primitives, the entire protocol version is updated. This eliminates an entire class of downgrade attacks that plague older VPN protocols.
WireGuard operates at Layer 3, encapsulating IP packets inside encrypted UDP datagrams. Each peer is identified by its **Curve25519 public key** — this serves as the peer's identity. The protocol performs a one-round-trip handshake (Noise IK pattern) to establish a session, after which data flows with minimal overhead (just 32 bytes of header per packet, plus 16 bytes of authentication tag).
Tailscale adds its own key management layer on top of WireGuard's raw key exchange. Instead of manually configuring each device with every other device's public key, the coordination server automates this distribution. But the underlying cryptographic guarantees remain those of WireGuard.
## NAT Traversal: The Hard Problem
The most technically challenging thing Tailscale does is establishing direct connections between devices that are behind [NAT](https://god.ad/learn/how-nat-works). In today's internet, the vast majority of devices do not have publicly routable IP addresses. They sit behind one or more layers of NAT: home routers, corporate firewalls, and carrier-grade NAT (CGNAT). Two devices behind separate NAT gateways cannot simply connect to each other, because neither has a public address the other can reach.
Tailscale solves this through a multi-step process that tries increasingly aggressive techniques until a direct connection is established.
### Step 1: Endpoint Discovery with STUN
The first step is for each node to discover its own public-facing IP address and port — the address other hosts on the internet would see when receiving packets from this device. Tailscale does this using **STUN** (Session Traversal Utilities for NAT), which is a simple protocol where a device sends a UDP packet to a known STUN server, and the server replies with the source IP and port it observed.
Tailscale operates its own STUN servers, co-located with its DERP relay servers. When a Tailscale client starts up, it sends STUN requests to multiple DERP regions to discover its public endpoint. This endpoint information is then reported to the coordination server, which distributes it to the device's authorized peers.
STUN also reveals what _type_ of NAT the device is behind, which is critical for determining what traversal technique will work:
  * **Full cone NAT** — once a mapping is created, any external host can send packets to the mapped address. Direct connections are trivial.
  * **Address-restricted cone NAT** — the mapped port only accepts packets from the same IP address the internal host has sent to. Requires coordination.
  * **Port-restricted cone NAT** — even more restrictive: the mapped port only accepts packets from the exact IP:port pair the internal host has sent to.
  * **Symmetric NAT** — a different mapping is created for every destination. STUN-based traversal fails; relay is often required.


### Step 2: NAT Hole Punching
Once two nodes know each other's public endpoints (via the coordination server), they attempt **UDP hole punching**. This technique exploits the way most NAT implementations work: when a device behind NAT sends a UDP packet to an external address, the NAT router creates a temporary mapping that allows return traffic from that address. If both sides simultaneously send packets to each other's discovered endpoints, both NAT devices create mappings, and a bidirectional UDP channel is established.
The process works as follows:
  1. Node A learns (via the coordination server) that Node B's public endpoint is `203.0.113.50:39281`.
  2. Node B learns that Node A's public endpoint is `198.51.100.22:50123`.
  3. Both nodes simultaneously send UDP packets to each other's endpoints.
  4. Node A's NAT router sees outbound traffic to `203.0.113.50:39281` and creates a mapping allowing return traffic from that address.
  5. Node B's NAT router does the same for `198.51.100.22:50123`.
  6. The packets cross in transit. Each NAT now has a mapping that accepts traffic from the other. A direct UDP channel is established.


This works reliably with cone NATs but fails with symmetric NATs, where the port changes for each new destination. Tailscale handles this by trying multiple port candidates and using heuristics to predict the NAT's port allocation behavior. When all else fails, it falls back to relay.
### Step 3: Direct Connection or DERP Relay
If hole punching succeeds, the two nodes have a direct, low-latency UDP path between them, and WireGuard traffic flows over that path. If it fails — as happens with some particularly restrictive NATs and firewalls — traffic falls back to a **DERP** relay.
## DERP: Detoured Encrypted Routing Protocol
DERP (Detoured Encrypted Routing Protocol) is Tailscale's custom relay protocol. It is **not** a traditional VPN relay — traffic through DERP remains fully end-to-end encrypted by WireGuard. The DERP server cannot read the traffic it relays. It simply forwards opaque encrypted blobs between peers.
DERP servers serve two functions:
  * **Relay** — forwarding WireGuard-encrypted packets between peers that cannot establish a direct connection
  * **STUN** — helping peers discover their public endpoints for NAT traversal


DERP relays operate over HTTPS (TCP port 443), which means they work even in environments where UDP is entirely blocked — restrictive corporate networks, airports, hotel Wi-Fi, and other hostile network environments. The DERP protocol uses a simple framing protocol over an HTTP connection upgrade, similar to WebSockets.
Tailscale operates DERP relay servers in over 20 regions worldwide. Each region has multiple servers for redundancy. When a node cannot establish a direct connection, it routes traffic through the nearest DERP server. The critical point is that this is always a fallback: Tailscale continuously attempts to upgrade DERP-relayed connections to direct connections in the background. In practice, Tailscale reports that over 92% of connections eventually establish a direct path.
The DERP protocol is open source and documented, and anyone can run their own DERP servers. This is particularly useful for organizations that want to ensure their relay traffic stays on infrastructure they control, even though the relay server cannot decrypt it.
## Mesh Topology vs Hub-and-Spoke
Understanding the difference between Tailscale's mesh topology and traditional VPN architectures is key to understanding why Tailscale exists.
### Traditional VPN: Hub-and-Spoke
A [traditional VPN](https://god.ad/learn/how-vpns-work) uses a **hub-and-spoke** model. There is a central VPN concentrator (the hub), and all client devices (the spokes) connect to it. All traffic between clients must travel through the hub, even if the clients are in the same building. This creates several problems:
  * **Bandwidth bottleneck** — the hub must handle all traffic, creating a single point of congestion
  * **Latency penalty** — traffic between two clients must travel to the hub and back, even if a direct path would be shorter. Two devices on the same LAN would route traffic through a VPN server possibly on another continent.
  * **Single point of failure** — if the hub goes down, all VPN connectivity is lost
  * **Infrastructure burden** — someone must provision, maintain, patch, and scale the VPN concentrator
  * **Configuration complexity** — certificates, firewall rules, split tunneling, and routing tables must all be managed manually


### Tailscale: Full Mesh
Tailscale creates a **full mesh** network where every device can connect directly to every other device. There is no hub. Traffic between Node A and Node B travels directly from A to B, regardless of where they are located. This means:
  * **No bottleneck** — bandwidth scales with the number of peers, not with central infrastructure
  * **Minimal latency** — traffic takes the shortest possible path between devices
  * **No single point of failure** in the data plane — each connection is independent
  * **Zero infrastructure to manage** — Tailscale handles coordination; you just install the client


The full mesh approach does require each device to maintain a WireGuard configuration for every peer it might communicate with. For N devices, that is N-1 peer entries per device, and N*(N-1)/2 potential tunnels across the network. Tailscale manages this automatically, and WireGuard's efficient implementation means that even hundreds of peer entries consume minimal resources. WireGuard does not maintain state for idle peers — the peer configuration exists, but no handshake occurs until traffic is actually sent.
## MagicDNS
Tailscale assigns each device a stable IP address from the `100.64.0.0/10` CGNAT range (specifically the `100.x.y.z` space). These addresses are stable across reboots and network changes. But memorizing IP addresses is impractical, so Tailscale provides **MagicDNS** — an integrated [DNS](https://god.ad/learn/what-is-dns) system that gives each device a human-readable hostname.
With MagicDNS enabled, every device in your tailnet is reachable by its hostname. If you name your home server `nas`, you can simply `ssh nas` from any device in your tailnet. No DNS configuration, no editing `/etc/hosts`, no separate DNS server.
MagicDNS works by intercepting DNS queries on each device (Tailscale runs a local DNS resolver at `100.100.100.100`) and resolving tailnet hostnames to their Tailscale IPs. Queries for non-tailnet names are forwarded to upstream DNS servers. The DNS records are distributed as part of the netmap from the coordination server.
MagicDNS also supports **HTTPS certificates** via a partnership with Let's Encrypt. Tailscale can provision valid TLS certificates for your tailnet hostnames (under a `.ts.net` domain), enabling HTTPS for internal services without self-signed certificates. This is notable because it provides valid public CA-backed certificates for private network services — something traditionally very difficult to achieve.
## ACL Policy Engine
In a traditional network, access control is enforced by firewalls sitting at network boundaries. In a mesh network with no central gateway, this approach does not work. Tailscale replaces perimeter-based security with a **centralized policy engine** based on Access Control Lists (ACLs).
Tailscale ACLs are defined in a JSON or HuJSON (human-friendly JSON with comments and trailing commas) policy file. The policy is evaluated by the coordination server and the resulting rules are pushed to each node as part of the netmap. Each node's Tailscale client then enforces the policy locally by configuring its WireGuard peer list and local packet filter.
A basic ACL policy looks like this:

```
{
  "acls": [
    // Engineering can access all servers
    {"action": "accept",
     "src": ["group:engineering"],
     "dst": ["tag:server:*"]},

    // Everyone can access the wiki
    {"action": "accept",
     "src": ["*"],
     "dst": ["wiki:80,443"]},

    // Contractors only get SSH to staging
    {"action": "accept",
     "src": ["group:contractors"],
     "dst": ["tag:staging:22"]}
  ],
  "groups": {
    "group:engineering": ["alice@example.com", "bob@example.com"],
    "group:contractors": ["carol@contractor.co"]
  },
  "tagOwners": {
    "tag:server": ["group:engineering"],
    "tag:staging": ["group:engineering"]
  }
}
```

Key features of the ACL system include:
  * **Default deny** — nothing is allowed unless explicitly permitted
  * **Identity-based** — rules reference users and groups from your identity provider, not IP addresses
  * **Tag-based device grouping** — servers can be tagged (e.g., `tag:production`, `tag:database`) and policies written against tags
  * **Port-level granularity** — rules can specify specific ports or port ranges
  * **Test infrastructure** — ACLs can be tested before deployment with `tailscale debug acl` and the ACL test syntax
  * **Git-managed** — the policy file can be version-controlled via GitOps integration


The enforcement happens at the node level, not at a central point. When the coordination server evaluates the policy, it determines which peers each node is allowed to communicate with and on which ports. Peers that a node has no permission to reach are simply not included in its WireGuard configuration. This means unauthorized traffic is not just blocked — the connection cannot even be attempted because the WireGuard tunnel does not exist.
## Key Distribution and Rotation
Key management is one of the most critical aspects of any VPN system, and it is where Tailscale differs most significantly from raw WireGuard. In a basic WireGuard setup, you must manually generate keys and distribute public keys to every peer. For N devices, this means managing N keypairs and distributing N*(N-1) public key entries. This does not scale.
Tailscale automates this entirely. The lifecycle of a node's key works as follows:
  1. When the Tailscale client is installed and first authenticated, it generates a **node key** (Curve25519 keypair). The private key is stored locally in a protected file.
  2. The public key is uploaded to the coordination server as part of the registration process.
  3. The coordination server verifies the user's identity (via the identity provider) and, if authorized, includes the new node's public key in the netmap distributed to all peers that are permitted to communicate with it.
  4. Keys are **rotated automatically**. By default, node keys expire and are rotated periodically. The client generates a new keypair and re-registers with the coordination server.
  5. If a device is deauthorized (removed from the tailnet, user account disabled), its public key is removed from all peers' netmaps in the next sync, immediately revoking its access.


Tailscale also supports **pre-authentication keys** (auth keys) for headless devices, CI/CD systems, and automated deployments. These are tokens generated from the admin console that allow a device to join the tailnet without interactive login. Auth keys can be configured as single-use or reusable, and can automatically apply tags to the devices that use them.
## Subnet Routers
Not every device can run the Tailscale client. Network printers, IoT devices, legacy servers, and entire on-premise networks need to be reachable without installing software on each device. Tailscale solves this with **subnet routers**.
A subnet router is a Tailscale node that advertises access to an entire [subnet](https://god.ad/learn/what-is-a-subnet) (e.g., `192.168.1.0/24` or `10.0.0.0/8`). Other nodes in the tailnet can then route traffic to that subnet through the subnet router. The subnet router performs NAT and forwards traffic between the tailnet and the physical subnet.
For example, if you have a home network at `192.168.1.0/24` and you run a Tailscale subnet router on a Linux box in that network, all your tailnet devices can access anything on `192.168.1.0/24` as if they were physically present. Your laptop at a coffee shop can reach your network printer at `192.168.1.50`.
Subnet routes must be explicitly approved in the admin console (or via ACL auto-approvers), providing a security gate. Multiple subnet routers can advertise the same route for high availability — if one goes down, traffic automatically fails over to another. This functions similarly to [anycast](https://god.ad/learn/what-is-anycast) in concept, though the implementation is different.
## Exit Nodes
An **exit node** is a Tailscale node that acts as a network gateway, routing all of another device's internet traffic through it. This is the one case where Tailscale behaves like a traditional [VPN](https://god.ad/learn/how-vpns-work): traffic exits from the exit node's IP address, not from the originating device's.
Exit nodes are useful for several scenarios:
  * **Security on untrusted networks** — route all traffic through a trusted server when on public Wi-Fi
  * **Location-specific access** — access services that are restricted to certain IP ranges or geographic regions
  * **Consistent egress IP** — present a stable source IP to services that use IP-based allow lists


Any Tailscale node can be configured as an exit node. When enabled, it advertises a `0.0.0.0/0` and `::/0` route, indicating it can handle all traffic. Other nodes can then select it as their exit node, either through the UI, CLI, or MDM policy.
The important distinction from a traditional VPN is that exit node usage is _optional and selective_. By default, Tailscale only routes tailnet traffic (100.64.0.0/10 and subnet routes) through the VPN tunnels. Internet traffic goes directly to the internet via the device's normal network connection. Exit nodes override this for devices that opt in.
## Tailscale vs Traditional VPN: A Comparison
Tailscale (Mesh) vs Traditional VPN (Hub-and-Spoke) Property Tailscale Traditional VPN Topology Full mesh (P2P) Hub-and-spoke Data path Direct peer-to-peer Through central gateway NAT traversal Automatic (STUN + DERP) Manual port forwarding Key management Automatic distribution Manual or PKI-based Protocol WireGuard IPsec / OpenVPN / SSL Authentication SSO / Identity provider Certificates / passwords Access control Identity-based ACLs Network-based firewall rules Infrastructure Zero (SaaS coordination) Self-hosted gateway server DNS MagicDNS (automatic) Manual / split DNS config SPOF (data plane) None (distributed mesh) VPN concentrator Scaling O(N) nodes, O(N^2) tunnels O(N) at hub bottleneck
## How Connection Establishment Works End-to-End
Let's walk through the complete sequence when Device A wants to reach Device B for the first time.
  1. **Registration** — Both Device A and Device B have already registered with the coordination server. Each has uploaded its WireGuard public key and discovered endpoints. The coordination server has evaluated the ACL policy and determined that A and B are allowed to communicate.
  2. **Netmap distribution** — The coordination server pushes a netmap to both devices. A's netmap includes B's public key and known endpoints, and vice versa.
  3. **STUN discovery** — Both devices have already performed STUN queries against multiple DERP servers to discover their public-facing endpoints (IP:port pairs). These endpoints are included in the netmap.
  4. **Connection attempt** — When A sends traffic to B's Tailscale IP (e.g., `100.64.0.5`), the Tailscale client initiates a connection. It tries multiple strategies in parallel: 
     * Direct connection to B's known public endpoints via UDP hole punching
     * Direct connection to B's local network address (if both are on the same LAN)
     * Connection via the nearest DERP relay as an immediate fallback
  5. **DERP relay (immediate)** — The first packets almost always travel via DERP, because direct connection establishment takes time. DERP provides **instant connectivity** while the more optimal direct path is negotiated in the background.
  6. **Hole punching (background)** — Both nodes send probes to each other's public endpoints. If any probe gets through, both sides detect the successful direct path.
  7. **Path upgrade** — Once a direct path is confirmed, traffic seamlessly migrates from DERP to the direct connection. The WireGuard session is maintained throughout; only the underlying UDP transport changes. The user experiences no interruption.
  8. **Ongoing maintenance** — Tailscale continuously monitors path quality and re-evaluates whether the direct path is still the best option. If a device moves to a different network, endpoint discovery is re-triggered and a new direct path is established.


This entire process typically completes in under a second. The user sees instant connectivity (via DERP) with optimal direct connectivity following within a few hundred milliseconds.
## Tailscale IP Addressing
Tailscale assigns each device a stable [IP address](https://god.ad/learn/what-is-an-ip-address) from the `100.64.0.0/10` range. This range is the IANA-assigned Carrier-Grade NAT (CGNAT) space, defined in RFC 6598. Tailscale chose this range because it is almost never used for end-user addressing, minimizing the chance of conflicts with existing private networks (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`).
Each device also receives a unique IPv6 address from the `fd7a:115c:a1e0::/48` ULA (Unique Local Address) prefix. This Tailscale-specific IPv6 prefix is deterministically derived from the device's identity, providing stable dual-stack connectivity within the tailnet.
These addresses are **stable across reboots, network changes, and location changes**. Your laptop has the same Tailscale IP whether it is on your home Wi-Fi, a hotel network, or a cellular connection. This stability is what makes MagicDNS and ACL policies work: the identity-to-IP mapping is permanent.
## Headscale: The Open-Source Coordination Server
While Tailscale's client software is open source, the coordination server is a proprietary SaaS service. For organizations that need (or prefer) full control over their coordination infrastructure, **Headscale** is an open-source, self-hosted implementation of the Tailscale coordination server.
Headscale implements the Tailscale coordination protocol, allowing standard Tailscale clients to connect to a self-hosted coordination server instead of Tailscale's SaaS. It supports:
  * Node registration and key distribution
  * ACL policy enforcement
  * MagicDNS
  * OIDC-based authentication
  * Pre-authentication keys
  * Subnet route management
  * Exit node configuration


Headscale stores its state in a SQLite or PostgreSQL database and runs as a single binary. It does not implement DERP relay functionality directly, but you can point it at Tailscale's public DERP servers or run your own.
The main trade-offs of running Headscale instead of Tailscale's SaaS are:
  * **Full sovereignty** — your coordination data never touches third-party servers
  * **Self-managed** — you are responsible for availability, backups, and updates
  * **Feature lag** — new Tailscale features (like Tailscale SSH, Funnel, etc.) may take time to appear in Headscale, and some may not be implemented at all
  * **No official support** — Headscale is a community project, not supported by Tailscale Inc.


Headscale is a significant project because it demonstrates the clean separation in Tailscale's architecture: because the coordination protocol is well-defined and the data plane is standard WireGuard, it is possible to replace the coordination server without modifying any clients.
## Advanced Features
### Tailscale SSH
Tailscale SSH allows nodes to accept SSH connections authenticated by Tailscale identity, without managing SSH keys or certificates. Instead of checking `~/.ssh/authorized_keys`, the SSH server verifies the connecting user's Tailscale identity against the ACL policy. This eliminates the need to distribute and manage SSH public keys across your fleet.
### Tailscale Funnel
Funnel exposes a service running on your tailnet to the public internet. Tailscale provisions a public DNS name (under `.ts.net`) and routes incoming HTTPS traffic through Tailscale's infrastructure to your device. This is essentially the reverse of a traditional VPN: instead of reaching into your private network, it lets the public internet reach into it, in a controlled way.
### Taildrop
Taildrop is a file-sharing feature that uses the Tailscale mesh to transfer files directly between devices. Files are sent peer-to-peer over the same WireGuard tunnels used for all other traffic, with no size limits and no intermediary storage.
### App Connectors
App connectors allow Tailscale to route traffic to specific SaaS applications through designated nodes in your tailnet. This enables IP-based access control for SaaS services: the SaaS provider sees traffic coming from your app connector's fixed IP, and you can restrict which tailnet users can reach the app connector.
## The BGP Connection
Tailscale's architecture intersects with [BGP](https://god.ad/learn/what-is-bgp) and internet routing in several ways:
  * **DERP server placement** — Tailscale's DERP relay servers are distributed globally, announced via [BGP](https://god.ad/learn/what-is-bgp) by the [autonomous systems](https://god.ad/learn/what-is-an-autonomous-system) of their hosting providers. The geographic distribution of DERP servers directly affects relay latency for connections that cannot be established directly.
  * **Exit node egress** — when using an exit node, your traffic exits from the exit node's IP address. The [BGP route](https://god.ad/learn/what-is-bgp) for that IP determines how return traffic reaches it. The exit node's [AS](https://god.ad/learn/what-is-an-autonomous-system) and its peering relationships affect latency and routing efficiency.
  * **Subnet routing and BGP** — in enterprise deployments, Tailscale subnet routers often sit alongside traditional routers that participate in [BGP](https://god.ad/learn/what-is-bgp). The subnet router bridges the Tailscale overlay network with the underlay network that BGP routes.
  * **CGNAT address space** — Tailscale's use of `100.64.0.0/10` means these addresses must never leak into the public [BGP](https://god.ad/learn/what-is-bgp) routing table. ISPs that use this range for their own CGNAT deployments could potentially conflict with Tailscale addressing, though this is rare in practice since Tailscale traffic is encapsulated inside WireGuard tunnels.


## Security Model
Tailscale's security model rests on several layers:
  1. **Authentication** — users authenticate through established identity providers (Google Workspace, Microsoft Entra ID, Okta, GitHub). Tailscale delegates authentication entirely, inheriting the IdP's security properties including MFA.
  2. **Authorization** — the ACL policy engine determines which devices can communicate with which other devices, on which ports. Policies are evaluated centrally and enforced at every node.
  3. **Encryption** — all traffic is encrypted end-to-end by WireGuard. Not even Tailscale's own servers can decrypt traffic between your devices. DERP relay servers see only opaque encrypted packets.
  4. **Key management** — keys are generated locally, rotated automatically, and distributed through the coordination server. Revoking a device is instant: remove it from the tailnet, and its key is removed from all peers' configurations.
  5. **Zero trust posture** — Tailscale enables a zero-trust architecture by making every connection authenticated and authorized, regardless of network location. Being "on the corporate network" grants no implicit access.


One subtlety worth noting: the coordination server is a trust anchor. You trust Tailscale (or your Headscale instance) to correctly distribute keys and enforce policies. If the coordination server were compromised, a sophisticated attacker could potentially insert a rogue node's key into your netmap. This is mitigated by the fact that adding a node requires authentication through your identity provider, and by Tailscale's operational security practices. For organizations where this trust model is unacceptable, Headscale provides the option of self-hosting the coordination server.
## Limitations and Trade-offs
Tailscale makes deliberate trade-offs that are worth understanding:
  * **Coordination server dependency** — while existing connections survive a coordination server outage, new device registration, key rotation, and policy updates require the server to be available.
  * **O(N^2) scaling** — the full mesh model means the number of potential tunnels grows quadratically with the number of devices. At very large scales (thousands of devices), the netmap distribution and WireGuard peer configuration can become a concern, though Tailscale actively optimizes for this.
  * **Userspace WireGuard overhead** — on most platforms, Tailscale uses a userspace WireGuard implementation, which has slightly higher CPU overhead and latency compared to the Linux kernel WireGuard module. On Linux, the kernel module can be used for better performance.
  * **CGNAT conflicts** — the use of `100.64.0.0/10` for Tailscale addresses can conflict with ISPs that use the same CGNAT range. This is uncommon but can occur.
  * **UDP dependency** — WireGuard requires UDP. While DERP provides a TCP fallback, relayed connections have higher latency. Environments that block all UDP traffic will always use DERP.


## How Tailscale Differs from Plain WireGuard
Since Tailscale is built on [WireGuard](https://god.ad/learn/how-wireguard-works), it is natural to ask: why not just use WireGuard directly? The answer lies in everything above the encryption layer:
  * **Key management** — WireGuard has no built-in key distribution. You must manually copy public keys between every pair of devices. Tailscale automates this entirely.
  * **NAT traversal** — WireGuard has no mechanism for punching through [NAT](https://god.ad/learn/how-nat-works). It requires at least one side to have a publicly reachable endpoint. Tailscale handles NAT traversal transparently.
  * **Relay fallback** — WireGuard has no relay mechanism. If a direct connection is not possible, WireGuard simply does not work. Tailscale's DERP servers ensure connectivity is always possible.
  * **Dynamic configuration** — WireGuard peers are statically configured. If a device's IP changes, you must update every peer's configuration. Tailscale tracks endpoint changes automatically.
  * **Identity integration** — WireGuard identifies peers only by public key. Tailscale maps keys to user identities from your identity provider.
  * **Access control** — WireGuard has no concept of policies or ACLs. If a peer is configured, it can send any traffic. Tailscale provides fine-grained, identity-based access control.
  * **DNS** — WireGuard has no [DNS](https://god.ad/learn/what-is-dns) integration. You must use IP addresses or manage DNS separately. Tailscale provides MagicDNS automatically.


In essence, WireGuard provides the cryptographic tunnel, and Tailscale provides everything needed to make that tunnel useful in a real-world, multi-device, multi-network environment. WireGuard is the engine; Tailscale is the car.
## Under the Hood: The Tailscale Client
The Tailscale client (open source, written in Go) runs as a daemon on each device. It consists of several components:
  * **Control client** — maintains a persistent connection to the coordination server (via HTTPS long-polling or WebSocket), receiving netmap updates and pushing endpoint changes
  * **WireGuard engine** — manages the WireGuard tunnels, either via the userspace `wireguard-go` implementation or the Linux kernel module
  * **Magicsock** — a custom socket implementation that handles NAT traversal, STUN, DERP relay, and path selection. This is the most complex component of the client. It multiplexes all peer traffic over a single UDP socket and dynamically switches between direct and relayed paths.
  * **DNS resolver** — the local DNS proxy that implements MagicDNS
  * **Packet filter** — enforces ACL rules on incoming and outgoing packets
  * **Network monitor** — watches for changes in the device's network configuration (new Wi-Fi, cellular handoff) and triggers endpoint re-discovery


The `magicsock` component deserves special mention. It implements a single UDP socket that speaks both WireGuard and STUN. When a packet arrives, magicsock examines it to determine whether it is a STUN response, a DERP frame, or a direct WireGuard packet, and routes it accordingly. This unified approach means Tailscale needs only one open UDP port, and all NAT traversal state is managed in a single place.
## Summary
Tailscale transforms WireGuard from a point-to-point tunneling protocol into a full mesh network platform. The key architectural decisions that make this possible are:
  * Separating the control plane (coordination server) from the data plane (WireGuard tunnels) so that centralized management does not mean centralized traffic
  * Aggressive, multi-strategy NAT traversal that establishes direct connections even through multiple layers of NAT
  * DERP relays that guarantee connectivity as a fallback while maintaining end-to-end encryption
  * Automatic key distribution and rotation that eliminates the manual key management burden of raw WireGuard
  * Identity-based ACLs that bring zero-trust access control to a flat network
  * MagicDNS that makes devices discoverable without infrastructure


The result is a VPN that does not feel like a VPN. There is no gateway to connect to, no split tunneling to configure, no certificates to manage. You install Tailscale, log in, and every authorized device is reachable. The complexity of NAT traversal, key management, and access control is handled automatically, letting you focus on the devices and services you actually care about.
Want to see how your network's IP addresses route across the global internet? [Try the BGP Looking Glass](https://god.ad/) to look up the BGP origin, AS path, and geolocation for any IP address or prefix.
See BGP routing data in real time
[Open Looking Glass](https://god.ad/)
Related Articles
[How the Tor Network Works: Onion Routing and Internet Anonymity](https://god.ad/learn/how-tor-works) [How Tor Onion Services Work: .onion Addresses and the Rendezvous Protocol](https://god.ad/learn/how-tor-onion-services-work)
[ ← Previous How VPNs Work: Tunneling Protocols and Encryption ](https://god.ad/learn/how-vpns-work) [ Next → How WireGuard Works: Modern VPN Protocol Explained ](https://god.ad/learn/how-wireguard-works)
More Articles
[How the Tor Network Works: Onion Routing and Internet Anonymity](https://god.ad/learn/how-tor-works) [How Tor Onion Services Work: .onion Addresses and the Rendezvous Protocol](https://god.ad/learn/how-tor-onion-services-work) [How VPNs Work: Tunneling Protocols and Encryption](https://god.ad/learn/how-vpns-work) [How WireGuard Works: Modern VPN Protocol Explained](https://god.ad/learn/how-wireguard-works) [What is BGP? The Internet's Routing Protocol Explained](https://god.ad/learn/what-is-bgp) [What is an Autonomous System (AS)?](https://god.ad/learn/what-is-an-autonomous-system)
Share
×
Copy Link  [ Text Message ](https://god.ad/learn/how-tailscale-works) [ Telegram ](https://god.ad/learn/how-tailscale-works) [ Facebook ](https://god.ad/learn/how-tailscale-works) [ Messenger ](https://god.ad/learn/how-tailscale-works) Instagram  Snapchat  [ Share on X ](https://god.ad/learn/how-tailscale-works) [ LinkedIn ](https://god.ad/learn/how-tailscale-works) [ Email ](https://god.ad/learn/how-tailscale-works) More... 
