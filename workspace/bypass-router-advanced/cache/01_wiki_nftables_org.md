---
url: "https://wiki.nftables.org/wiki-nftables/index.php/Flowtables"
title: "Flowtables - nftables wiki"
scraped_at: 2026-09-23T06:11:11+00:00
---

# Flowtables
From nftables wiki
[Jump to navigation](https://wiki.nftables.org/wiki-nftables/index.php/Flowtables#mw-head) [Jump to search](https://wiki.nftables.org/wiki-nftables/index.php/Flowtables#searchInput)
Flowtables allow you to accelerate packet forwarding in software (and in hardware if your NIC supports it) by using a conntrack-based network stack bypass. 
Entries are represented through a tuple that is composed of the input interface, source and destination address, source and destination port; and layer 3/4 protocols. Each entry also caches the destination interface and the gateway address (to update the destination link-layer address) to forward packets. 
The TTL and hoplimit fields are also decremented. Hence, flowtables provides an alternative path that allow packets to bypass the classic forwarding path. 

```
                                         userspace process
                                          ^              |
                                          |              |
                                     _____|____     ____\/___
                                    /          \   /         \
                                    |   input  |   |  output |
                                    \__________/   \_________/
                                         ^               |
                                         |               |
      _________      __________      ---------     _____\/_____
     /         \    /          \     |Routing |   /            \
  -->  ingress  ---> prerouting ---> |decision|   | postrouting|--> neigh_xmit
     \_________/    \__________/     ----------   \____________/          ^
       |      ^                          |               ^                |
   flowtable  |                     ____\/___            |                |
       |      |                    /         \           |                |
    __\/___   |                    | forward |------------                |
    |-----|   |                    \_________/                            |
    |-----|   |                 'flow add' rule                           |
    |-----|   |                   adds entry to                           |
    |_____|   |                     flowtable                             |
       |      |                                                           |
      / \     |                                                           |
     /hit\_no_|                                                           |
     \ ? /                                                                |
      \ /                                                                 |
       |__yes_________________fastpath bypass ____________________________|

               Fig.1 Netfilter hooks and flowtable interactions

```

Flowtables reside in the ingress hook that is located before the prerouting hook. You can select which flows you want to offload through the flow expression from the forward chain. Flowtables are identified by their address [family](https://wiki.nftables.org/wiki-nftables/index.php/Nftables_families "Nftables families") and their name. The address family must be one of ip, ip6, or inet. When no address family is specified, ip is used by default. 
Flows are offloaded after the state is created. That means that usually the first reply packet will create the flowtable entry. A firewall rule to accept the initial traffic is required. The flow expression on the forward chain must match the return traffic of the initial connection. Be aware that the return route is deducted from the packet, that creates the flowtable entry. This also means if you are using special ip rules, you need to make sure that they match the reply packet traffic as well as the original traffic. 
The *priority* can be a signed integer or *filter* which stands for 0. Addition and subtraction can be used to set relative priority, e.g. filter + 5 equals to 5. 
The *devices* are specified as [iifname](https://wiki.nftables.org/wiki-nftables/index.php/Data_types "Data types")(s) of the input interface(s) of the traffic that should be offloaded. Devices are required for both traffic directions. 
An Example to offload HTTP traffic for a router: 

```
define DEV_PRIVATE=eth0
define DEV_INTERNET=eth1

table inet x {

    flowtable f {
        hook ingress priority 0
        devices = { $DEV_PRIVATE, $DEV_INTERNET }
    }

    chain forward {
        type filter hook forward priority 0; policy drop;

        # offload established HTTP connections
        tcp dport { 80, 443 } flow add @f counter packets 0 bytes 0

        # Allow traffic from established and related packets, drop invalid
        ct state vmap { established : accept, related : accept, invalid : drop }

        # connections from the internal net to the internet or to other
        # internal nets are allowed
        iifname $DEV_PRIVATE counter accept
    }
}

```

Note that: 
  1. The rule that uses the _flow add_ statement determines what flows are added to the flowtable. This ruleset above adds entries to the flowtable for established HTTP connections.
  2. The devices you specify in the flowtable declaration determine where the flowtable hooks in the pipeline for lookups, in the example above, it registers a hook for devices eth0 and eth1 in the ingress hook at priority 0.


## See also
  * [Linux kernel documentation on Netfilter flowtable](https://www.kernel.org/doc/html/latest/networking/nf_flowtable.html)
  * [Netfilter Mini-Workshop, Netdev 0x13, 2019-03](https://netdevconf.info/0x13/session.html?workshop-netfilter-mini)
  * [Mellanox flowtable hardware offload](https://lwn.net/Articles/804384/)
  * [Some Mellanox flowtable hardware offload performance measurements by Wen Xu of UCloud](https://www.programmersought.com/article/11833283913/)
  * [Netfilter hardware offloads, Pablo Neira Ayuso, Linux Plumbers Conference, 2019-09](https://linuxplumbersconf.org/event/4/contributions/463/)


Retrieved from "[http://wiki.nftables.org/wiki-nftables/index.php?title=Flowtables&oldid=1162](http://wiki.nftables.org/wiki-nftables/index.php?title=Flowtables&oldid=1162)"
## Navigation menu
### Search
