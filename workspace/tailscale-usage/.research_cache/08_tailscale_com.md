---
url: "https://tailscale.com/docs/reference/derp-servers/custom-derp-servers"
title: "Custom DERP servers · Tailscale Docs"
scraped_at: 2026-08-27T16:20:42+00:00
---

[Aperture is GA! Build a home(lab) with AI.Read the blog ->](http://tailscale.com/blog/aperture-ga)
### Documentation
Close navigation
# Custom DERP servers
Last validated: Jan 5, 2026|Copy as Markdown|[View as Markdown](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers.md)
Custom DERP servers are currently [in alpha](https://tailscale.com/docs/reference/tailscale-release-stages#alpha).
A custom DERP server is a designated [DERP server](https://tailscale.com/docs/reference/derp-servers) set up and managed by an organization or individual other than Tailscale for specific networking needs. By default, all Tailscale networks (known as tailnets) use Tailscale-operated DERP servers. DERP servers primarily play a supporting role in facilitating connectivity between devices in a Tailscale network (known as a [tailnet](https://tailscale.com/docs/concepts/tailnet)). But they also function as a fallback mechanism when [direct connections](https://tailscale.com/docs/reference/connection-types) aren't possible and [peer relays](https://tailscale.com/docs/features/peer-relay) aren't available.
In most cases, there's no need to run a custom DERP server. DERP servers typically only serve as the connective tissue between devices in your tailnet (with no visibility into the data exchanged between devices).
However, in some restrictive network environments, it's more likely for devices to use a DERP server because they can't establish direct connections to other devices. Because DERP relayed connections are slower than direct connections, you might experience poor performance. If you frequently encounter DERP relayed connections, and want to avoid performance issues, it's usually better to [find out why you can't establish a direct connection](https://tailscale.com/docs/reference/troubleshooting/connectivity) or set up peer relays instead of a custom DERP server.
[Tailscale Peer Relays](https://tailscale.com/docs/features/peer-relay):
  * Offer lower latency and better performance than DERP servers because they run within your own network or infrastructure.
  * Don't incur additional costs associated with egress data transfer through DERP servers (for cloud environments).
  * Avoid the overhead and limitations of maintaining custom DERP servers.


That said, there are some rare cases in which it might make sense to run a custom DERP server. For example, you might run a custom DERP server to [restrict where encrypted traffic routes to comply with a corporate policy](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#policy-compliance).
## [Limitations](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#limitations)
In most cases, there's no need to run a custom DERP server. However, there are some rare cases in which it makes sense to run a custom DERP server. To do so, you must build, deploy, and update the `cmd/derper` binary.
Running custom DERP servers is an advanced operation that requires significant resources on your part to set up and maintain. Additionally, running a custom DERP servers have the following caveats:
  * Custom DERP servers don't support device sharing or other cross-tailnet features.
  * Custom DERP servers, just like normal DERP servers, have no visibility of the data exchanged between devices because they're encrypted. As a result, DERP servers aren't helpful for network-level debugging.
  * Custom DERP servers won't benefit from some optimizations from the Tailscale control plane.
  * Custom DERP servers won't work [from behind a firewall or a load balancer](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#direct-internet-access).
  * [Mullvad exit nodes](https://tailscale.com/docs/features/exit-nodes/mullvad-exit-nodes) don't work with custom DERP servers.
  * Custom DERP servers are not used for [regional routing](https://tailscale.com/docs/how-to/set-up-high-availability#regional-routing). Refer to [issue #12993](https://github.com/tailscale/tailscale/issues/12993) for updates.


## [Requirements](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#requirements)
Custom DERP servers must have [direct access to the internet](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#direct-internet-access), [allow ICMP traffic](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#icmp-traffic), and [open ports for HTTP, HTTPS, and STUN](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#required-ports).
### [Direct internet access](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#direct-internet-access)
DERP servers require direct internet connectivity and must not be behind NAT devices (such as firewalls) or load balancers. This direct connection requirement exists for two critical reasons: [device identification](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#device-identification) and [protocol compatibility](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#protocol-compatibility).
#### [Device identification](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#device-identification)
DERP servers identify tailnet devices by inspecting the source addresses of incoming traffic. This crucial functionality fails when traffic passes through NAT or load balancers, as they modify the original source addresses.
#### [Protocol compatibility](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#protocol-compatibility)
Tailscale clients use the HTTP upgrade protocol to establish bidirectional data channels. Most cloud load balancer systems don't support this protocol, making them incompatible with DERP server operations.
Running your own DERP servers is an advanced operation that requires significant resources on your part to set up and maintain.
### [Required ports](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#required-ports)
DERP servers must have the following ports open to run an HTTP server, an HTTPS server, and a [STUN](https://en.wikipedia.org/wiki/STUN) server. The ports for those three services need to be open for traffic from the internet so users in your tailnet can access them from places such as their homes or coffee shops.  
| **Server**  | **Port**  |  
| --- | --- |  
| HTTP  |  
| HTTPS  | `443`  |  
| STUN  | `3478`  |  
To use other port numbers for HTTPS and STUN, set [`DERPNode.DERPPort`](https://pkg.go.dev/tailscale.com/tailcfg#DERPNode.DERPPort) or [`DERPNode.STUNPort`](https://pkg.go.dev/tailscale.com/tailcfg#DERPNode.STUNPort), respectively. You cannot use a custom port number for HTTP.
### [ICMP traffic](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#icmp-traffic)
DERP servers must allow inbound and outbound ICMP (Internet Control Message Protocol) traffic.
Tailscale runs [DERP relay servers](https://tailscale.com/docs/reference/derp-servers) to help connect your nodes. Generally, you don't need to customize Tailscale DERP servers. However, it is possible to do it.
## [Get started with a custom DERP server](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#get-started-with-a-custom-derp-server)
Running your own DERP servers is an advanced operation that requires significant resources on your part to set up and maintain. Consider the [requirements](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#requirements) and [limitations](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#limitations) before proceeding.
To set up a custom DERP server, you'll need to:
  1. Run a DERP server from source.
  2. Add the DERP server to your tailnet.


The following additional steps are optional:
  1. Restrict tailnet device access to your custom DERP server.
  2. Remove Tailscale's default DERP servers from your tailnet.


### [Run a DERP server from source](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#run-a-derp-server-from-source)
To run your own DERP server, you must build the DERP server from source. Using the [latest version of Go](https://golang.org/doc/install), run:

```
go install tailscale.com/cmd/derper@latest

```

... to install the latest DERP server to `$HOME/go/bin`.
Before running the binary, you'll need a domain name pointing at your server. With both the domain name and the binary, to start the DERP server on your domain name run:

```
sudo derper --hostname=example.com

```

This will start the DERP server exposed on port 443, reachable at your domain. Then, you can add the DERP server to your tailnet as specified in Step 2.
To stay compatible with Tailscale client updates, you might need to update DERP servers periodically by rebuilding from source with `go install tailscale.com/cmd/derper@latest`.
### [Add the custom DERP servers to your tailnet](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#add-the-custom-derp-servers-to-your-tailnet)
If you find that Tailscale does not provide a DERP server within your region, or you are otherwise unable to use the provided DERPs, you can augment or edit the set of DERP servers by specifying them in your tailnet's [policy JSON](https://tailscale.com/docs/reference/syntax/policy-file) by setting the `derpMap` key to a value of type [`DERPMap`](https://pkg.go.dev/tailscale.com/tailcfg#DERPMap).
Each region has a unique region ID. The region ID values `900` to `999` are reserved for use as custom, user-specified regions and will not be used by Tailscale.
For example, the following configuration enables a custom DERP server with the hostname `example.com`. For more options, refer to the definitions of [`DERPRegion`](https://pkg.go.dev/tailscale.com/tailcfg#DERPRegion) and [`DERPNode`](https://pkg.go.dev/tailscale.com/tailcfg#DERPNode).

```
{
  // ... other parts of tailnet policy file
  "derpMap": {
    "Regions": {
      "900": {
        "RegionID": 900,
        "RegionCode": "myderp",
        "Nodes": [
          {
            "Name": "1",
            "RegionID": 900,
            "HostName": "example.com",
            // IPv4 and IPv6 are optional, but recommended, to reduce
            // potential DERP connectivity issues if DNS is unavailable
            // or having issues. Addresses must be publicly routable
            // and not in private IP ranges.
            "IPv4": "203.0.113.15",
            "IPv6": "2001:db8::1"
          }
        ]
      }
    }
  }
}

```

There can be only one DERP server per region. If you want DERP redundancy, use multiple regions with only one DERP server in each region.
### [(Optional) Remove Tailscale's DERP servers](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#optional-remove-tailscales-derp-servers)
For various reasons, such as [compliance](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#policy-compliance), you might not want to route traffic through a specific DERP region. You can remove DERP regions available to the devices in your tailnet by creating a custom DERP map in the tailnet policy file. To exclude a region, set its value to `null`. When set to `null`, devices in your tailnet cannot connect to DERP servers in that region.
For example, the following DERP map configuration disables routing traffic through the New York Tailscale DERP region, which has the region ID `1`:

```
{
  // ... other parts of tailnet policy file
  "derpMap": { "Regions": { "1": null } }
}

```

You can access Tailscale's default DERP map from `https://controlplane.tailscale.com/derpmap/default`:

```
curl https://controlplane.tailscale.com/derpmap/default

```

If you have `jq` installed, use this to list Tailscale's default DERP regions and their IDs:

```
curl --silent https://controlplane.tailscale.com/derpmap/default | jq -r '.Regions[] | "\(.RegionID) \(.RegionName)"'

```

To guarantee that your traffic only flows through your custom DERP servers, remove all Tailscale's default DERP regions by setting the `OmitDefaultRegions` flag to `true` in the DERP map:

```
{
  // ... other parts of tailnet policy file
  "derpMap": {
    "OmitDefaultRegions": true,
    "Regions": {
      "900": {
        "RegionID": 900,
        "RegionCode": "myderp",
        "Nodes": [
          {
            "Name": "1",
            "RegionID": 900,
            "HostName": "example.com",
            // IPv4 and IPv6 are optional, but recommended, to reduce
            // potential DERP connectivity issues if DNS is unavailable
            // or having issues. Addresses must be publicly routable
            // and not in private IP ranges.
            "IPv4": "203.0.113.15",
            "IPv6": "2001:db8::1"
          }
        ]
      }
    }
  }
}

```

You can access the full set of options for DERP maps the source code's [`DERPMap` definition](https://pkg.go.dev/tailscale.com/tailcfg#DERPMap).
### [(Optional) Verify client traffic to the custom DERP server](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#optional-verify-client-traffic-to-the-custom-derp-server)
Anyone that knows the IP address of your DERP server could add it to their DERP map and route their tailnet traffic through your DERP server. To allow only your tailnet traffic through your DERP server, run `tailscaled` on the same device as your DERP server, and start `derper` with the `--verify-clients` flag:

```
sudo derper --hostname=example.com --verify-clients

```

## [Monitor custom DERP servers](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#monitor-custom-derp-servers)
Use the [`cmd/derpprobe`](https://github.com/tailscale/tailscale/tree/main/cmd/derpprobe) binary to monitor your custom DERP servers and to verify they are working correctly. You'll need to specify a `--derp-map=file://` URL that is a JSON document with your DERP map to monitor.
## [Policy compliance](https://tailscale.com/docs/reference/derp-servers/custom-derp-servers#policy-compliance)
One reason to host a custom DERP server is to ensure policy compliance. For example, you might have a strict policy requirement that prevents traffic from going through public servers, even if the traffic is encrypted.
DERP servers only forward encrypted traffic, and they have no access to plain text traffic. Additionally, Tailscale's DERP servers are shared resources across all Tailscale customers. You may have a strict routing policy, such as preventing encrypted traffic from traversing servers outside of your control.
To comply with such a policy, you can run one or more custom DERP servers and remove the default Tailscale DERP servers from the list of DERP servers your tailnet can use.
