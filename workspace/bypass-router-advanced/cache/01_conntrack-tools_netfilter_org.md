---
url: "https://conntrack-tools.netfilter.org/manual.html"
title: "The conntrack-tools user manual"
scraped_at: 2026-09-23T06:10:59+00:00
---

#  The conntrack-tools user manual
###  Pablo Neira Ayuso
`<pablo@netfilter.org>`
This document details how to install and to configure the [conntrack-tools](http://conntrack-tools.netfilter.org). 
Copyright © 2008-2020 Pablo Neira Ayuso
Permission is granted to copy, distribute and/or modify this document under the terms of the GNU Free Documentation License, Version 1.2 or any later version published by the Free Software Foundation; with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts. A copy of the license is included in the section entitled "GNU Free Documentation License". 
**Table of Contents** 




[2. What are the conntrack-tools?](https://conntrack-tools.netfilter.org/manual.html#what)








[5. Using conntrack: the command line interface](https://conntrack-tools.netfilter.org/manual.html#conntrack)


[6. Setting up conntrackd: the daemon](https://conntrack-tools.netfilter.org/manual.html#settingup)
     

[State table synchronization](https://conntrack-tools.netfilter.org/manual.html#sync)
     




[Configuring the daemon](https://conntrack-tools.netfilter.org/manual.html#sync-configure)


[Active-Backup setups](https://conntrack-tools.netfilter.org/manual.html#sync-pb)


[Active-Active setups](https://conntrack-tools.netfilter.org/manual.html#sync-aa)


[Launching conntrackd](https://conntrack-tools.netfilter.org/manual.html#sync-launch)


[Other configuration options](https://conntrack-tools.netfilter.org/manual.html#sync-options)


[User-space helpers](https://conntrack-tools.netfilter.org/manual.html#helpers)





[7. System integration](https://conntrack-tools.netfilter.org/manual.html#system-integration)

#  Chapter 1. Introduction
This documentation provides a description on how to install and to configure the [conntrack-tools](http://conntrack-tools.netfilter.org).
This documentation assumes that the reader is familiar with basic firewalling and Netfilter concepts. You also must understand the difference between _stateless_ and _stateful_ firewalls. Otherwise, please read [Netfilter's Connection Tracking System](http://people.netfilter.org/pablo/docs/login.pdf) published in _:login; the USENIX magazine_ for a quick reference.
#  Chapter 2. What are the conntrack-tools?
The [conntrack-tools](http://conntrack-tools.netfilter.org) package contains two programs:
  * _conntrack_ provides a full featured command line utility to interact with the connection tracking system. The _conntrack_ utility provides a replacement for the limited /proc/net/nf_conntrack interface. With _conntrack_ , you can list, update and delete the existing flow entries; you can also listen to flow events.
  * _conntrackd_ is the user-space connection tracking daemon. This daemon can be used to deploy fault-tolerant GNU/Linux firewalls but you can also use it to collect flow-based statistics of the firewall use.


Mind the trailing that refers to either the command line utility or the daemon.
#  Chapter 3. Requirements
If you are using the Linux kernel that your distribution provides, then you most likely can skip this.
If you compile your own Linux kernel, then please make sure the following options are enabled.
You require a [Linux kernel](http://www.kernel.org) version >= 2.6.18.
  * Connection Tracking System.
    * CONFIG_NF_CONNTRACK=m
    * CONFIG_NF_CONNTRACK_IPV4=m
    * CONFIG_NF_CONNTRACK_IPV6=m (if your setup supports IPv6)
  * nfnetlink: the generic messaging interface for Netfilter.
    * CONFIG_NETFILTER_NETLINK=m
  * nf_conntrack_netlink: the messaging interface for the Connection Tracking System.
    * CONFIG_NF_CT_NETLINK=m
  * connection tracking event notification API: the flow-based event notification interface.
    * CONFIG_NF_CONNTRACK_EVENTS=y

  
| Validating Linux kernel support  |  
| --- |  
|  You can validate that your Linux kernel support for the _conntrack-tools_ through _modinfo_. 
```
 # modinfo nf_conntrack
filename:       /lib/modules/5.2.0/kernel/net/netfilter/nf_conntrack.ko
license:        GPL
alias:          nf_conntrack-10
alias:          nf_conntrack-2
alias:          ip_conntrack
depends:        nf_defrag_ipv6,libcrc32c,nf_defrag_ipv4
retpoline:      Y
intree:         Y
name:           nf_conntrack
vermagic:       5.7.0+ SMP preempt mod_unload modversions 
parm:           tstamp:Enable connection tracking flow timestamping. (bool)
parm:           acct:Enable connection tracking flow accounting. (bool)
parm:           nf_conntrack_helper:Enable automatic conntrack helper assignment (default 0) (bool)
parm:           expect_hashsize:uint
parm:           enable_hooks:Always enable conntrack hooks (bool)

```
Make sure _nf_conntrack_netlink_ is also available.  |  
You also need to install the following library dependencies:
  * libnfnetlink: the netfilter netlink library use the official release available in [netfilter.org](http://www.netfilter.org/projects/libnfnetlink)
  * libnetfilter_conntrack: the netfilter netlink library use the official release available in [netfilter.org](http://www.netfilter.org/projects/libnetfilter_conntrack)

  
| Installing library dependencies  |  
| --- |  
| Your distribution most likely also provides packages for this software, so you do not have to compile it yourself. |  
#  Chapter 4. Installation
To compile and install the _conntrack-tools_ run the following commands:

```
	(non-root)$ tar xvjf conntrack-tools-x.x.x.tar.bz2
	(non-root)$ cd conntrack-tools-x.x.x
	(non-root)$ ./configure --prefix=/usr
	(non-root)$ make
	(root)    # make install
```
  
| Installing conntrack and conntrackd  |  
| --- |  
| Your distribution most likely also provides packages for this software, so you do not have to compile it yourself. |  
#  Chapter 5. Using conntrack: the command line interface
The _/proc/net/nf_conntrack_ interface is very limited as it only allows you to display the existing flows, their state and metadata such the flow mark:

```
 # cat /proc/net/nf_conntrack
 tcp      6 431982 ESTABLISHED src=192.168.2.100 dst=123.59.27.117 sport=34846 dport=993 packets=169 bytes=14322 src=123.59.27.117 dst=192.168.2.100 sport=993 dport=34846 packets=113 bytes=34787 [ASSURED] mark=0 use=1
 tcp      6 431698 ESTABLISHED src=192.168.2.100 dst=123.59.27.117 sport=34849 dport=993 packets=244 bytes=18723 src=123.59.27.117 dst=192.168.2.100 sport=993 dport=34849 packets=203 bytes=144731 [ASSURED] mark=0 use=1
 
```

You can list the existing flows using the _conntrack_ utility via command:

```
 # conntrack -L
 tcp      6 431982 ESTABLISHED src=192.168.2.100 dst=123.59.27.117 sport=34846 dport=993 packets=169 bytes=14322 src=123.59.27.117 dst=192.168.2.100 sport=993 dport=34846 packets=113 bytes=34787 [ASSURED] mark=0 use=1
 tcp      6 431698 ESTABLISHED src=192.168.2.100 dst=123.59.27.117 sport=34849 dport=993 packets=244 bytes=18723 src=123.59.27.117 dst=192.168.2.100 sport=993 dport=34849 packets=203 bytes=144731 [ASSURED] mark=0 use=1
conntrack v1.4.6 (conntrack-tools): 2 flow entries have been shown.
 
```

The _conntrack_ syntax is similar to _iptables_.
You can filter out the listing without using _grep_ :

```
 # conntrack -L -p tcp --dport 993
 tcp      6 431982 ESTABLISHED src=192.168.2.100 dst=123.59.27.117 sport=34846 dport=993 packets=169 bytes=14322 src=123.59.27.117 dst=192.168.2.100 sport=993 dport=34846 packets=113 bytes=34787 [ASSURED] mark=0 use=1
conntrack v1.4.6 (conntrack-tools): 1 flow entries have been shown.
 
```

You can update the ct mark, extending the previous example:

```
 # conntrack -U -p tcp --dport 993 --mark 10
 tcp      6 431982 ESTABLISHED src=192.168.2.100 dst=123.59.27.117 sport=34846 dport=993 packets=169 bytes=14322 src=123.59.27.117 dst=192.168.2.100 sport=993 dport=34846 packets=113 bytes=34787 [ASSURED] mark=10 use=1
conntrack v1.4.6 (conntrack-tools): 1 flow entries have been updated.
 
```

You can also delete entries

```
 # conntrack -D -p tcp --dport 993
 tcp      6 431982 ESTABLISHED src=192.168.2.100 dst=123.59.27.117 sport=34846 dport=993 packets=169 bytes=14322 src=123.59.27.117 dst=192.168.2.100 sport=993 dport=34846 packets=113 bytes=34787 [ASSURED] mark=10 use=1
conntrack v1.4.6 (conntrack-tools): 1 flow entries have been deleted.
 
```

This allows you to block TCP traffic if:
  * You have a stateful rule-set that drops traffic in INVALID state.
  * You set _/proc/sys/net/netfilter/nf_conntrack_tcp_loose_ to zero.


You can also listen to the connection tracking events:

```
 # conntrack -E
     [NEW] udp      17 30 src=192.168.2.100 dst=192.168.2.1 sport=57767 dport=53 [UNREPLIED] src=192.168.2.1 dst=192.168.2.100 sport=53 dport=57767
  [UPDATE] udp      17 29 src=192.168.2.100 dst=192.168.2.1 sport=57767 dport=53 src=192.168.2.1 dst=192.168.2.100 sport=53 dport=57767
     [NEW] tcp      6 120 SYN_SENT src=192.168.2.100 dst=66.102.9.104 sport=33379 dport=80 [UNREPLIED] src=66.102.9.104 dst=192.168.2.100 sport=80 dport=33379
  [UPDATE] tcp      6 60 SYN_RECV src=192.168.2.100 dst=66.102.9.104 sport=33379 dport=80 src=66.102.9.104 dst=192.168.2.100 sport=80 dport=33379
  [UPDATE] tcp      6 432000 ESTABLISHED src=192.168.2.100 dst=66.102.9.104 sport=33379 dport=80 src=66.102.9.104 dst=192.168.2.100 sport=80 dport=33379 [ASSURED]

```

There are many options, including support for XML output, more advanced filters, and so on. Please check the manpage for more information.
#  Chapter 6. Setting up conntrackd: the daemon
**Table of Contents** 

[State table synchronization](https://conntrack-tools.netfilter.org/manual.html#sync)
     




[Configuring the daemon](https://conntrack-tools.netfilter.org/manual.html#sync-configure)


[Active-Backup setups](https://conntrack-tools.netfilter.org/manual.html#sync-pb)


[Active-Active setups](https://conntrack-tools.netfilter.org/manual.html#sync-aa)


[Launching conntrackd](https://conntrack-tools.netfilter.org/manual.html#sync-launch)


[Other configuration options](https://conntrack-tools.netfilter.org/manual.html#sync-options)


[User-space helpers](https://conntrack-tools.netfilter.org/manual.html#helpers)




The _conntrackd_ daemon supports three modes:
  * _State table synchronization_ , to synchronize the connection tracking state table between several firewalls in High Availability (HA) scenarios.
  * _Userspace connection tracking helpers_ , for layer 7 Application Layer Gateway (ALG) such as DHCPv6, MDNS, RPC, SLP and Oracle TNS. As an alternative to the in-kernel connection tracking helpers that are available in the Linux kernel.
  * _Flow-based statistics collection_ , to collect flow-based statistics as an alternative to [ulogd2](http://www.netfilter.org/projects/ulogd/), although _ulogd2_ allows for more flexible statistics collection.


##  State table synchronization
###  Requirements
If you would like to configure _conntrackd_ to work in state synchronization mode, then you require:
  1. A working installation of [keepalived](http://www.keepalived.org), preferibly a recent version. Check if your distribution comes with a recent packaged version. Otherwise, you may compile it from the sources. 
There is a very simple example file in the _conntrackd_ sources to setup a simple HA cluster with keepalived (see the file keepalived.conf under the doc/sync/ directory). This file can be used to set up a simple VRRP cluster composed of two machines that hold the virtual IPs 192.168.0.100 on eth0 and 192.168.1.100 on eth1.
If you are not familiar with _keepalived_ , please read the official documentation available at the keepalived website (<http://www.keepalived.org>).
If you use a different high availability manager, make sure it works correctly before going ahead.
  2. A dedicated link. The dedicated link between the firewalls is used to transmit and receive the state information. The use of a dedicated link is mandatory for security reasons as someone may pick the state information that is transfered between the firewalls.
  3. A well-formed stateful rule-set. Otherwise you are likely to experience problems during the fail-over. An example of a well-formed stateful iptables rule-set is available in the [conntrack-tools website](http://conntrack-tools.netfilter.org/testcase.html).
  4. If your Linux kernel is < 2.6.22, you have to disable TCP window tracking: 

```
    # echo 1 > /proc/sys/net/netfilter/nf_conntrack_tcp_be_liberal
   
```



###  Configuring the daemon
The daemon _conntrackd_ in synchronization mode supports up to three replication approaches:
  * _notrack_ : this approach is the most simple as it is based on a best effort replication protocol, ie. unreliable protocol. This protocol sends and receives the state information without performing any specific checking. 
  * _ft-fw_ : this approach is based on a reliable protocol that performs message tracking. Thus, the protocol can recover from message loss, re-ordering and corruption.
  * _alarm_ : this approach is spamming. It is based on a alarm-based protocol that periodically re-sends the flow state to the backup firewall replicas. This protocol consumes a lot of bandwidth but it resolves synchronization problems fast.


The three existing approaches are soft real-time asynchronous replication protocols that are aimed to have negligible impact in terms of latency and bandwidth throughput in the stateful firewall filtering.
To configure _conntrackd_ in any of the existing synchronization modes, you have to copy the example configuration file to the directory /etc/conntrackd/ on every firewall replica. Note that __type__ is the synchronization type selected.

```
 (conntrack-tools-x.x.x)# cp doc/_type_/conntrackd.conf /etc/conntrackd/conntrackd.conf

```

Do not forget to edit the files before going ahead. There are several parameters that you have to tune to adapt the example configuration file to your setup.   
| Configuration file location  |  
| --- |  
| If you don't want to put the config file under /etc/conntrackd/, just tell conntrackd where to find it passing the option -C. |  
###  Active-Backup setups  
| Stateful firewall architectures  |  
| --- |  
| A good reading to extend the information about firewall architectures is [Demystifying cluster-based fault-tolerant firewalls](http://1984.lsi.us.es/~pablo/docs/intcomp09.pdf) published in IEEE Internet Computing magazine.  |  
In the Active-Backup setup, one of the stateful firewall replicas filters traffic and the other acts as backup. If you use this approach, you have to copy the script _primary-backup.sh_ to: 

```
 (conntrack-tools-x.x.x)# cp doc/sync/primary-backup.sh /etc/conntrackd/

```

The HA manager invokes this script when a transition happens, ie. If a stateful firewall replica:
  * becomes active to recover the filtering.
  * becomes backup.
  * hits failure (this is available if the HA manager has a failure state, which is true for [keepalived](http://www.keepalived.org).


The script is simple, and it contains the different actions that _conntrackd_ performs to recover the filtering or purge obsolete entries from the state table, among others. The script is commented, you can have a look at it if you need further information.
###  Active-Active setups
The Active-Active setup consists of having more than one stateful firewall actively filtering traffic. Thus, we reduce the resource waste that implies to have a backup firewall which is spare.
We can classify the type of Active-Active setups in several families:
  * _Symmetric path routing_ : The stateful firewalls share the workload in terms of flows, ie. the packets that are part of a flow are always filtered by the same firewall.
  * _Asymmetric multi-path routing_ : The packets that are part of a flow can be filtered by whatever stateful firewall in the cluster. Thus, every flow-states have to be propagated to all the firewalls in the cluster as we do not know which one would be the next to filter a packet. This setup goes against the design of stateful firewalls as we define the filtering policy based on flows, not in packets anymore. 


_conntrackd_ allows you to deploy an symmetric Active-Active setup based on a static approach. For example, assume that you have two virtual IPs, vIP1 and vIP2, and two firewall replicas, FW1 and FW2. You can give the virtual vIP1 to the firewall FW1 and the vIP2 to the FW2. 
The asymmetric path scenario is hard: races might occurs between state synchronization and packet forwarding. If you would like to deploy an Active-Active setup with an assymmetic multi-path routing configuration, then, make sure the same firewall _forwards_ packets coming in the original and the reply directions. If you cannot guarantee this and you still would like to deply an Active-Active setup, then you might have to consider downgrading your firewall ruleset policy to stateless filtering.
###  Launching conntrackd
Once you have configured _conntrackd_ , you can run in _console mode_ which is an interactive mode, in that case type 'conntrackd' as root.

```
(root)# conntrackd
```

If you want to run _conntrackd_ in _daemon mode_ , then type:

```
(root)# conntrackd -d
```

You can verify that conntrackd is running by checking the log messages via . Moreover, if _conntrackd_ is running fine, you can dump the current status of the daemon:

```
 # conntrackd -s
 cache internal:
 current active connections:                4
 connections created:                       4    failed:            0
 connections updated:                       0    failed:            0
 connections destroyed:                     0    failed:            0

 cache external:
 current active connections:                0
 connections created:                       0    failed:            0
 connections updated:                       0    failed:            0
 connections destroyed:                     0    failed:            0

 traffic processed:
                    0 Bytes                         0 Pckts

 multicast traffic:
                  352 Bytes sent                    0 Bytes recv
                   22 Pckts sent                    0 Pckts recv
                    0 Error send                    0 Error recv

 multicast sequence tracking:
                    0 Pckts mfrm                    0 Pckts lost
 
```

This command displays the number of entries in the internal and external cache:
  * The internal cache contains the states that this firewall replica is filtering, ie. this is a cache of the kernel state table. 
  * The external cache contains the states that the other firewall replica is filtering. 


You can dump the internal cache with the following command:

```
 # conntrackd -i
 tcp      6 ESTABLISHED src=192.168.2.100 dst=139.174.175.20 sport=58491 dport=993 src=139.174.175.20 dst=192.168.2.100 sport=993 dport=58491 [ASSURED] mark=0 secmark=0 [active since 536s]
 tcp      6 ESTABLISHED src=192.168.2.100 dst=123.59.27.117 sport=38211 dport=993 src=123.59.27.117 dst=192.168.2.100 sport=993 dport=38211 [ASSURED] mark=0 secmark=0 [active since 536s]
 tcp      6 ESTABLISHED src=192.168.2.100 dst=123.59.27.117 sport=38209 dport=993 src=123.59.27.117 dst=192.168.2.100 sport=993 dport=38209 [ASSURED] mark=0 secmark=0 [active since 536s]
 tcp      6 TIME_WAIT src=192.168.2.100 dst=74.125.45.166 sport=42593 dport=80 src=74.125.45.166 dst=192.168.2.100 sport=80 dport=42593 [ASSURED] [active since 165s]
 tcp      6 ESTABLISHED src=192.168.2.100 dst=139.174.175.20 sport=37962 dport=993 src=139.174.175.20 dst=192.168.2.100 sport=993 dport=37962 [ASSURED] mark=0 secmark=0 [active since 536s]
 
```

You can dump the external cache with the following command:

```
# conntrackd -e
```

If the replication works fine, _conntrackd -s_ displays the active's internal cache should display the same number of entries than the backup's external cache and vice-versa.
To verify that the recovery works fine, if you trigger a fail-over, the log files should display the following information:

```
 [Thu Sep 18 18:03:02 2008] (pid=9759) [notice] committing external cache
 [Thu Sep 18 18:03:02 2008] (pid=9759) [notice] Committed 1545 new entries
```

This means that the state entries have been injected into the kernel correctly.
###  Other configuration options
The daemon allows several configuration options that you may want to enable. This section contains some information about them.
####  Disabling external cache
It is possible to disable the external cache. Thus, _conntrackd_ directly injects the flow-states into the in-kernel Connection Tracking System of the backup firewall. You can do it by enabling the _DisableExternalCache_ option in the _conntrackd.conf_ configuration file: 

```
Sync {
	Mode FTFW {
		 [...]
		 DisableExternalCache Off
	}
}
 
```

You can also use this option with the NOTRACK and ALARM modes. This increases CPU consumption in the backup firewall but now you do not need to commit the flow-states during the master failures since they are already in the in-kernel Connection Tracking table. Moreover, you save memory in the backup firewall since you do not need to store the foreign flow-states anymore. 
####  Disabling internal cache
You can also disable the internal cache by means of the _DisableInternalCache_ option in the _conntrackd.conf_ configuration file: 

```
Sync {
	Mode NOTRACK {
		 [...]
		 DisableInternalCache Off
	}
}
 
```

However, this option is only available for the NOTRACK mode. This mode provides unreliable flow-state synchronization between firewalls. Thus, if flow-states are lost during the synchronization, the protocol provides no way to recover them.
####  Using UDP, TCP or multicast for flow-state synchronization
You can use up to three different transport layer protocols to synchronize flow-state changes between the firewalls: UDP, TCP and Multicast. UDP and multicast are unreliable but together with the FT-FW mode provide partial reliable flow-state synchronization. 
The preferred choice is FT-FW over UDP, or multicast alternatively. TCP introduces latency in the flow-state synchronization due to the congestion control. Under flow-state message are lost, the FIFO delivery becomes also a problem since the backup firewall quickly gets out of sync. For that reason, its use is discouraged. Note that using TCP only makes sense with the NOTRACK mode. 
####  Redundant dedicated links
You can set redundant dedicated links without using bonding, you have to configure as many redundant links as you want in the configuration file. In case of failure of the master dedicated link, conntrackd failovers to one of the backups. An example of this configuration is the following: 

```
Sync {
	Mode FTFW {
		 [...]
	}
	# default master dedicated link
        UDP Default {
                IPv4_address 192.168.2.1
                IPv4_Destination_Address 192.168.2.2
                Port 3780
                Interface eth3
                SndSocketBuffer 24985600
                RcvSocketBuffer 24985600
                Checksum on
        }
	# backup dedicated link
        UDP {
               IPv4_address 192.168.1.3
               IPv4_Destination_Address 192.168.1.4
               Port 3780
               Interface eth2
               SndSocketBuffer 24985600
               RcvSocketBuffer 24985600
               Checksum on
        }
	[...]
}
 
```

####  Filtering Connection tracking events with iptables
Since Linux kernel >= 2.6.34, iptables provides the iptables target that allows to reduce the amount of Connection Tracking events that are delivered to user-space. However, you will have to use a Linux kernel >= 2.6.38 to profit from this feature, since several aspects of the event filtering were broken.
The following example shows how to only generate the _assured_ and _destroy_ events:

```
 # iptables -I PREROUTING -t raw -j CT --ctevents assured,destroy
 
```
  
| Assured flows  |  
| --- |  
| One flow is assured if the firewall has seen traffic for it in both directions. |  
Reducing the amount of events generated helps to reduce CPU consumption in the active firewall.
####  Synchronization of expectations  
| Check your Linux kernel version first  |  
| --- |  
|  The synchronization of expectations require a Linux kernel >= 3.5 to work appropriately.  |  
The connection tracking system provides helpers that allows you to filter multi-flow application protocols like FTP, H.323 and SIP among many others. These protocols usually split the control and data traffic in different flows. Moreover, the control flow usually announces layer 3 and 4 information to let the other peer know where the data flows will be open. This sort of protocols require that the firewall inspects the content of the packet, otherwise filtering by layer 3 and 4 selectors like addresses and ports become a real nightmare. Netfilter already provides the so-called _helpers_ that track this protocol aspects to allow deploying appropriate filtering. These helpers create _expectation_ entries that represent expected traffic that will arrive to the firewall according to the inspected packets.
In case that you have enabled tracking of these protocols, you may want to enable the state-synchronization of expectation as well. Thus, established flows for this specific protocols will not suffer any disruption.
To enable the expectation support in the configuration file, you have to use the following option:

```
Sync {
       ...
       Options {
               ExpectationSync {
                       ftp
                       sip
                       ras    # for H.323
                       q.931  # for H.323
                       h.245  # for H.323
               }
       }
}
```

The example above enables the synchronization of the expectations for the FTP, SIP and H.323 helpers.
In my testbed, there are two firewalls in a primary-backup configuration running keepalived. They use a couple of floating cluster IP address (192.168.0.100 and 192.168.1.100) that are used by the client. These firewalls protect one FTP server (192.168.1.2) that will be accessed by one client.
In ASCII art, it looks like this:

```
         192.168.0.100      192.168.1.100
                  eth1      eth2
                       fw-1
                     /      \       FTP
        client ------       ------ server
      192.168.0.2    \      /   192.168.1.2
                       fw-2
 
```

This is the rule-set for the firewalls:

```
    -A FORWARD -m state --state RELATED -j ACCEPT
    -A FORWARD -i eth2 -m state --state ESTABLISHED -j ACCEPT
    -A FORWARD -i eth1 -p tcp -m tcp --dport 21 --tcp-flags FIN,SYN,RST,ACK SYN -m state --state NEW -j ACCEPT
    -A FORWARD -i eth1 -p tcp -m state --state ESTABLISHED -j ACCEPT
    -A FORWARD -m state --state INVALID -j LOG --log-prefix "invalid: "
```

Before going ahead, make sure _nf_conntrack_ftp_ is loaded.
The following steps detail how to check that the expectation support works fine with FTP traffic:
  1. Switch to the client. Start one FTP control connection to one server that is protected by the firewalls, enter passive mode:

```
  (term-1) user@client$ nc 192.168.1.2 21
   220 dummy FTP server
   USER anonymous
   331 Please specify the password.
   PASS nothing
   230 Login successful.
   PASV
   227 Entering Passive Mode (192,168,1,2,163,11).
```

This means that port 163*256+11=41739 will be used for the data traffic. I suggest you to read [djb's FTP protocol description](http://www.freefire.org/articles/ftpexample.php) in case that you don't understand how this calculation is done.
  2. Switch to fw-1 (primary) to check that the expectation is in the internal cache.

```
 root@fw1# conntrackd -i exp
 proto=6 src=192.168.0.2 dst=192.168.1.2 sport=0 dport=41739 mask-src=255.255.255.255 mask-dst=255.255.255.255 sport=0 dport=65535 master-src=192.168.0.2 master-dst=192.168.1.2 sport=36390 dport=21 helper=ftp [active since 5s]
 
```

  3. Switch to fw-2 (backup) to check that the expectation has been successfully replicated.

```
 root@fw2# conntrackd -e exp
 proto=6 src=192.168.0.2 dst=192.168.1.2 sport=0 dport=41739 mask-src=255.255.255.255 mask-dst=255.255.255.255 sport=0 dport=65535 master-src=192.168.0.2 master-dst=192.168.1.2 sport=36390 dport=21 [active since 8s]
 
```

  4. Make the primary firewall fw-1 fail. Now fw-2 becomes primary.
  5. Switch to fw-2 (primary) to commit the external cache into the kernel. The logs should display that the commit was successful:

```
 root@fw2# tail -100f /var/log/conntrackd.log
 [Wed Dec  7 22:16:31 2011] (pid=19195) [notice] committing external cache: expectations
 [Wed Dec  7 22:16:31 2011] (pid=19195) [notice] Committed 1 new entries
 [Wed Dec  7 22:16:31 2011] (pid=19195) [notice] commit has taken 0.000366 seconds
```

  6. Switch to the client. Open a new terminal and connect to the port that has been announced by the server:

```
 (term-2) user@client$ nc -vvv 192.168.1.2 41739
 (UNKNOWN) [192.168.1.2] 41739 (?) open
```

  7. Switch to term-1 and ask for the file listing:

```
 [...]
 227 Entering Passive Mode (192,168,1,2,163,11).
 LIST
```

  8. Switch to term-2, it should display the listing. That means everything has worked fine.


You may want to try disabling the expectation support and repeating the steps to check that _it does not work_ without the state-synchronization.
##  User-space helpers  
| Check your Linux kernel version first  |  
| --- |  
|  The user-space helper infrastructure requires a Linux kernel >= 3.6 to work appropriately.  |  
Connection tracking helpers allows you to filter multi-flow protocols that usually separate control and data traffic into different flows. These protocols usually violate network layering by including layer 3/4 details, eg. IP address and TCP/UDP ports, in their application protocol (which resides in layer 7). This is problematic for gateways since they operate at packet-level, ie. layers 3/4, and therefore they miss this important information to filter these protocols appropriately.
Helpers inspect packet content (at layer 7) and create the so-called expectations. These expectations are added to one internal table that resides in the gateway. For each new packet arriving to the gateway, the gateway first looks up for matching expectations. If there is any, then this flow is accepted since it's been expected. Note this lookup only occurs for the first packet that is part of one newly established flow, not for all packets.
Since 1.4.0, conntrackd provides the infrastructure to develop helpers in user-space. The main features of the user-space infrastructure for helpers are:
  * Rapid connection tracking helper development, as developing code in user-space is usually faster.
  * Reliability: A buggy helper does not crash the kernel. If the helper fails, ie. the conntrackd crashes, Moreover, we can monitor the helper process and restart it in case of problems.
  * Security: Avoid complex string matching and mangling in kernel-space running in privileged mode. Going further, we can even think about running user-space helper as a non-root process.
  * It allows the development of very specific helpers for proprietary protocols that are not standard. This is the case of the SQL*net helper. Implementing this in kernel-space may be problematic, since this may not be accepted for ainline inclusion in the Linux kernel. As an alternative, we can still distribute this support as separate patches. However, my personal experience is that, given that the kernel API/ABI is not stable, changes in the interface lead to the breakage of the patch. This highly increase the overhead in the maintainance.


Currently, the infrastructure supports the following user-space helpers: 
  * Oracle*TNS, to support its special _Redirect_ message.
  * NFSv3, mind that version 4 does not require this helper.
  * FTP (this helper is also available in kernel-space).
  * SSDP.


The following steps describe how to enable the RPC portmapper helper for NFSv3 (this is similar for other helpers):
  1. Add configuration to conntrackd.conf: 

```
Helper {
        Setup yes

        Type rpc inet udp {
                QueueNum 1
		QueueLen 10240
                Policy rpc {
                        ExpectMax 1
                        ExpectTimeout 300
                }
        }
        Type rpc inet tcp {
                QueueNum 2
		QueueLen 10240
                Policy rpc {
                        ExpectMax 1
                        ExpectTimeout 300
                }
        }
}

```

This configures conntrackd to use NFQUEUE queue numbers 1 and 2 to send traffic for inspection to user-space  
| If you have some custom libnetfilter_queue application  |  
| --- |  
|  Make sure your queue numbers do not collide with those used in your conntrackd.conf file.  |  
  2. Run conntrackd: 

```
# conntrackd -d -C /path/to/conntrackd.conf

```

  3. Add iptables rule using the CT target: 

```
# iptables -I OUTPUT -t raw -p udp --dport 111 -j CT --helper rpc
# iptables -I OUTPUT -t raw -p tcp --dport 111 -j CT --helper rpc

```

With this, packets matching port TCP/UDP/111 are passed to user-space for inspection. If there is no instance of conntrackd configured to support user-space helpers, no inspection happens and packets are not sent to user-space.


Now you can test this (assuming you have some working NFSv3 setup) with: 

```
mount -t nfs -onfsvers=3 mynfs.server.info:/srv/cvs /mnt/

```

You should see new expectations being added via: 

```
# conntrack -E expect
    [NEW] 300 proto=17 src=1.2.3.4 dst=1.2.3.4 sport=0 dport=54834 mask-src=255.255.255.255 mask-dst=255.255.255.255 sport=0 dport=65535 master-src=1.2.3.4 master-dst=1.2.3.4 sport=58190 dport=111 PERMANENT class=0 helper=rpc
    [NEW] 300 proto=6 src=1.2.3.4 dst=1.2.3.4 sport=0 dport=2049 mask-src=255.255.255.255 mask-dst=255.255.255.255 sport=0 dport=65535 master-src=1.2.3.4 master-dst=1.2.3.4 sport=55450 dport=111 PERMANENT class=0 helper=rpc
    [NEW] 300 proto=17 src=1.2.3.4 dst=1.2.3.4 sport=0 dport=58031 mask-src=255.255.255.255 mask-dst=255.255.255.255 sport=0 dport=65535 master-src=1.2.3.4 master-dst=1.2.3.4 sport=56309 dport=111 PERMANENT class=0 helper=rpc

```

##  Troubleshooting
Problems with _conntrackd_? The following list of questions should help for troubleshooting: 

1. [ I see packets lost in conntrackd -s ](https://conntrack-tools.netfilter.org/manual.html#idm393) 


2. [ The log messages report that the maximum netlink socket buffer has been reached. ](https://conntrack-tools.netfilter.org/manual.html#idm402) 


3. [ I see can't open multicast server in the log messages ](https://conntrack-tools.netfilter.org/manual.html#idm410) 


4. [ Can I use wackamole, heartattack or any other HA manager? ](https://conntrack-tools.netfilter.org/manual.html#idm417) 


5. [ Does conntrackd support TCP flow-recovery with window tracking enabled? ](https://conntrack-tools.netfilter.org/manual.html#idm423) 


6. [ Does conntrackd support the H.323 and SIP connection tracking helpers? ](https://conntrack-tools.netfilter.org/manual.html#idm428) 


7. [ Is there any way to set up a more verbose mode in the log message for debugging? ](https://conntrack-tools.netfilter.org/manual.html#idm433) 
  
|  I see _packets lost_ in _conntrackd -s_  |  
| --- |  
|  You can rise the value of _McastRcvSocketBuffer_ and _McastRcvSocketBuffer_ , if the problem is due to buffer overruns in the multicast sender or the receiver, the problem should disapear.   |  
|  The log messages report that the _maximum netlink socket buffer has been reached_.   |  
|  You can increase the values of _SocketBufferSize_ and _SocketBufferSizeMaxGrown_.   |  
|  I see _can't open multicast server_ in the log messages   |  
|  Make sure that the _IPv4_interface_ clause has the IP of the dedicated link.   |  
|  Can I use [wackamole](http://www.backhand.org/wackamole/), heartattack or any other HA manager?   |  
|  Absolutely, you can. But before reporting issues, make sure that your HA manager is not the source of the problems.   |  
|  Does conntrackd support TCP flow-recovery with window tracking enabled?   |  
|  Yes, but you require a Linux kernel >= 2.6.36 and the conntrack-tools >= 0.9.15. To enable it, check the TCPWindowTracking clause in the example configuration files.   |  
|  Does conntrackd support the H.323 and SIP connection tracking helpers?   |  
|  Yes, conntrackd includes expectation support since version 1.2.0.   |  
|  Is there any way to set up a more verbose mode in the log message for debugging?   |  
|  No, but conntrackd provides lots of information that you can look up in runtime via -s option. You can check network statistics to find anomalies: 
```
# conntrackd -s network
    network statistics:
        recv:
                Malformed messages:                        0
                Wrong protocol version:                    0
                Malformed header:                          0
                Malformed payload:                         0
                Bad message type:                          0
                Truncated message:                         0
                Bad message size:                          0
        send:
                Malformed messages:                        0

sequence tracking statistics:
        recv:
                Packets lost:                          42726
                Packets before:                            0

UDP traffic (active device=eth3):
              564232 Bytes sent              1979844 Bytes recv
                2844 Pckts sent                 8029 Pckts recv
                   0 Error send                    0 Error recv
    
```
You can check cache statistics: 
```
# conntrackd -s cache
cache:internal  active objects:                    0
        active/total entries:                      0/           0
        creation OK/failed:                    11068/           0
                no memory available:               0
                no space left in cache:            0
        update OK/failed:                       4128/           0
                entry not found:                   0
        deletion created/failed:               11068/           0
                entry not found:                   0

cache:external  active objects:                    0
        active/total entries:                      0/           0
        creation OK/failed:                    10521/           0
                no memory available:               0
                no space left in cache:            0
        update OK/failed:                       8832/           0
                entry not found:                   0
        deletion created/failed:               10521/           0
                entry not found:                   0
    
```
You can check runtime miscelaneous statistics: 
```
# conntrackd -s runtime
daemon uptime: 14 min

netlink stats:
        events received:                       24736
        events filtered:                           0
        events unknown type:                       0
        catch event failed:                        0
        dump unknown type:                         0
        netlink overrun:                           0
        flush kernel table:                        1
        resync with kernel table:                  0
        current buffer size (in bytes):      8000000

runtime stats:
        child process failed:                      0
                child process segfault:            0
                child process termsig:             0
        select failed:                             0
        wait failed:                               0
        local read failed:                         0
        local unknown request:                     0
    
```
You can check dedicated link statistics: 
```
# conntrackd -s link
UDP traffic device=eth3 status=RUNNING role=ACTIVE:
              566848 Bytes sent              1982612 Bytes recv
                3018 Pckts sent                 8203 Pckts recv
                   0 Error send                    0 Error recv
    
```
You can check network queue statistics: 
```
# conntrackd -s queue
allocated queue nodes:                     1

queue txqueue:
current elements:                          0
maximum elements:                 2147483647
not enough space errors:                   0

queue errorq:
current elements:                          0
maximum elements:                        128
not enough space errors:                   0

queue rsqueue:
current elements:                          1
maximum elements:                     131072
not enough space errors:                   0
    
```
 |  
#  Chapter 7. System integration
You may want to integrate conntrackd into your system in order to build a robust firewall cluster. You should take a look at how the linux distro of your choice does this, as there are some interesting things to take into account. 
Depending on the architecture of the firewall cluster, you may want to sync each node after a fallback operation, so the new node inmediately knows the connection of the other. This is specially interesting in _Active-Active_ mode. 
This can be done using _conntrackd -n_ just after the new node has joined the conntrackd cluster, for example at boot time. These operations require the main conntrackd daemon to open the UNIX socket to receive the order from the _conntrackd -n_ call. 
Care must be taken that no race conditions happens (i.e, the UNIX socket is actually opened before _conntrackd -n_ is launched). Otherwise, you may end with a new node (after fallback) which doesn't know any connection states from the other node. 
Since _conntrack-tools 1.4.4_ , the conntrackd daemon includes integration with _libsystemd_. If conntrackd is configured at build time with this support (using _--enable-systemd_), then you can use _Systemd on_ in the _conntrackd.conf_ main configuration file. To benefit from this integration, you should use a systemd service file of _Type=notify_ , which also includes support for the systemd watchdog. 
Using systemd and conntrackd with libsystemd support and a service file of Type=notify means that conntrackd will notify of its readiness to systemd, so you can launch _conntrackd -n_ safely, avoiding such race conditions. 
