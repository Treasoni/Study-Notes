---
url: "https://www.mankier.com/8/conntrack"
title: "conntrack: command line interface for netfilter connection tracking | Man Page | System Administration | conntrack-tools | ManKier"
scraped_at: 2026-09-23T06:11:32+00:00
---


[conntrack](https://www.mankier.com/8/conntrack)
## [Examples (TL;DR)](https://www.mankier.com/8/conntrack#Examples_\(TL;DR\))
  * List all currently tracked connections: `conntrack [-L[](https://www.mankier.com/8/conntrack#-L)|--dump[](https://www.mankier.com/8/conntrack#--dump)]`
  * Display a real-time event log of connection changes: `conntrack [-E[](https://www.mankier.com/8/conntrack#-E)|--event[](https://www.mankier.com/8/conntrack#--event)]`
  * Display a real-time event log of connection changes and associated timestamps: `conntrack [-E[](https://www.mankier.com/8/conntrack#-E)|--event[](https://www.mankier.com/8/conntrack#--event)] [-o[](https://www.mankier.com/8/conntrack#-o)|--output[](https://www.mankier.com/8/conntrack#--output)] timestamp`
  * Display a real-time event log of connection changes for a specific IP address: `conntrack [-E[](https://www.mankier.com/8/conntrack#-E)|--event[](https://www.mankier.com/8/conntrack#--event)] [-s[](https://www.mankier.com/8/conntrack#-s)|--orig-src[](https://www.mankier.com/8/conntrack#--orig-src)] ip_address`
  * Delete all flows for a specific source IP address: `conntrack [-D[](https://www.mankier.com/8/conntrack#-D)|--delete[](https://www.mankier.com/8/conntrack#--delete)] [-s[](https://www.mankier.com/8/conntrack#-s)|--orig-src[](https://www.mankier.com/8/conntrack#--orig-src)] ip_address`


[tldr.sh](https://tldr.sh/)
## [Synopsis](https://www.mankier.com/8/conntrack#Synopsis)
`**conntrack -L[](https://www.mankier.com/8/conntrack#-L) [table] [options] [-z[](https://www.mankier.com/8/conntrack#-z)]****conntrack -G[](https://www.mankier.com/8/conntrack#-G) [table] parameters****conntrack -D[](https://www.mankier.com/8/conntrack#-D) [table] parameters****conntrack -I[](https://www.mankier.com/8/conntrack#-I) [table] parameters****conntrack -A[](https://www.mankier.com/8/conntrack#-A) [table] parameters****conntrack -U[](https://www.mankier.com/8/conntrack#-U) [table] parameters****conntrack -E[](https://www.mankier.com/8/conntrack#-E) [table] [options]****conntrack -F[](https://www.mankier.com/8/conntrack#-F) [table]****conntrack -C[](https://www.mankier.com/8/conntrack#-C) [table]****conntrack -S[](https://www.mankier.com/8/conntrack#-S)** **conntrack -R[](https://www.mankier.com/8/conntrack#-R) file**`
## [Description](https://www.mankier.com/8/conntrack#Description)
The **conntrack** utility provides a full-featured userspace interface to the Netfilter connection tracking system that is intended to replace the old /proc/net/ip_conntrack interface. This tool can be used to search, list, inspect and maintain the connection tracking subsystem of the Linux kernel.
Using **conntrack** , you can dump a list of all (or a filtered selection of) currently tracked connections, delete connections from the state table, and even add new ones.
In addition, you can also monitor connection tracking events, e.g. show an event message (one line) per newly established connection.
## [Tables](https://www.mankier.com/8/conntrack#Tables)
The connection tracking subsystem maintains several internal tables:     
This is the default table. It contains a list of all currently tracked connections through the system. If you don't use connection tracking exemptions (NOTRACK iptables target), this means all connections that go through the system.     
This is the table of expectations. Connection tracking expectations are the mechanism used to "expect" **RELATED** connections to existing ones. Expectations are generally used by "connection tracking helpers" (sometimes called application level gateways [ALGs]) for more complex protocols such as FTP, SIP or H.323.     
This table shows the conntrack entries, that have expired and that have been destroyed by the connection tracking system itself, or via the **conntrack** utility.     
This table shows new entries, that are not yet inserted into the conntrack table. These entries are attached to packets that are traversing the stack, but did not reach the confirmation point at the postrouting hook.
The tables "dying" and "unconfirmed" are basically only useful for debugging purposes. Under normal operation, it is hard to see entries in any of them. There are corner cases, where it is valid to see entries in the unconfirmed table, eg. when packets that are enqueued via nfqueue, and the dying table, eg. when [conntrackd(8)](https://www.mankier.com/8/conntrackd) runs in event reliable mode. ## [Options](https://www.mankier.com/8/conntrack#Options)
The options recognized by **conntrack** can be divided into several different groups.
### [Commands](https://www.mankier.com/8/conntrack#Options-Commands)
These options specify the particular operation to perform. Only one of them can be specified at any given time.     
List connection tracking or expectation table     
Search for and show a particular (matching) entry in the given table.     
Delete an entry from the given table.     
Create a new entry from the given table, it fails if it already exists.     
Add a new entry from the given table.     
Update an entry from the given table.     
Display a real-time event log.     
Flush the whole given table     
Show the table counter.     
Show the in-kernel connection tracking system statistics.     
Load entries from a given file. To read from stdin, "-" should be specified. ### [Parameters](https://www.mankier.com/8/conntrack#Options-Parameters)     
Atomically zero counters after reading them. This option is only valid in combination with the "[-L](https://www.mankier.com/8/conntrack#-L), [--dump](https://www.mankier.com/8/conntrack#--dump)" command options. 

**[-o](https://www.mankier.com/8/conntrack#-o), [--output](https://www.mankier.com/8/conntrack#--output) [extended,xml,save,timestamp,id,ktimestamp,labels]**
    
Display output in a certain format. With the extended output option, this tool displays the layer 3 information. With ktimestamp, it displays the in-kernel timestamp available since 2.6.38 (you can enable it via the [sysctl(8)](https://www.mankier.com/8/sysctl) key **net.netfilter.nf_conntrack_timestamp**). The labels output option tells **conntrack** to show the names of connection tracking labels that might be present. The userspace output option tells if the event has been triggered by a process. 

[-e](https://www.mankier.com/8/conntrack#-e), [--event-mask](https://www.mankier.com/8/conntrack#--event-mask) _[ALL|NEW|UPDATES|DESTROY][,...]_ 
    
Set the bitmask of events that are to be generated by the in-kernel ctnetlink event code. Using this parameter, you can reduce the event messages generated by the kernel to the types that you are actually interested in. This option can only be used in conjunction with "[-E](https://www.mankier.com/8/conntrack#-E), [--event](https://www.mankier.com/8/conntrack#--event)". 

[-b](https://www.mankier.com/8/conntrack#-b), [--buffer-size](https://www.mankier.com/8/conntrack#--buffer-size) _value_ 
    
Set the Netlink socket buffer size in bytes. This option is useful if the command line tool reports ENOBUFS errors. If you do not pass this option, the default value available at [sysctl(8)](https://www.mankier.com/8/sysctl) key **net.core.rmem_default** is used. The tool reports this problem if your process is too slow to handle all the event messages or, in other words, if the amount of events is big enough to overrun the socket buffer. Note that using a big buffer reduces the chances to hit ENOBUFS, however, this results in more memory consumption. This option can only be used in conjunction with "[-E](https://www.mankier.com/8/conntrack#-E), [--event](https://www.mankier.com/8/conntrack#--event)". ### [Filter Parameters](https://www.mankier.com/8/conntrack#Options-Filter_Parameters) 

[-s](https://www.mankier.com/8/conntrack#-s), [--src](https://www.mankier.com/8/conntrack#--src), [--orig-src](https://www.mankier.com/8/conntrack#--orig-src) _IP_ADDRESS_ 
    
Match only entries whose source address in the original direction equals the one specified as argument. Implies "[--mask-src](https://www.mankier.com/8/conntrack#--mask-src)" when CIDR notation is used. 

[-d](https://www.mankier.com/8/conntrack#-d), [--dst](https://www.mankier.com/8/conntrack#--dst), [--orig-dst](https://www.mankier.com/8/conntrack#--orig-dst) _IP_ADDRESS_ 
    
Match only entries whose destination address in the original direction equals the one specified as argument. Implies "[--mask-dst](https://www.mankier.com/8/conntrack#--mask-dst)" when CIDR notation is used. 

[-r](https://www.mankier.com/8/conntrack#-r), [--reply-src](https://www.mankier.com/8/conntrack#--reply-src) _IP_ADDRESS_ 
    
Match only entries whose source address in the reply direction equals the one specified as argument. 

[-q](https://www.mankier.com/8/conntrack#-q), [--reply-dst](https://www.mankier.com/8/conntrack#--reply-dst) _IP_ADDRESS_ 
    
Match only entries whose destination address in the reply direction equals the one specified as argument. 

[-p](https://www.mankier.com/8/conntrack#-p), [--proto](https://www.mankier.com/8/conntrack#--proto) _PROTO_ 
    
Specify layer four (TCP, UDP, ...) protocol. 

[-f](https://www.mankier.com/8/conntrack#-f), [--family](https://www.mankier.com/8/conntrack#--family) _PROTO_ 
    
Specify layer three (ipv4, ipv6) protocol. This option is only required in conjunction with "[-L](https://www.mankier.com/8/conntrack#-L), [--dump](https://www.mankier.com/8/conntrack#--dump)". If this option is not passed, the default layer 3 protocol will be IPv4. 

[-t](https://www.mankier.com/8/conntrack#-t), [--timeout](https://www.mankier.com/8/conntrack#--timeout) _TIMEOUT_ 
    
Specify the timeout. 

[-m](https://www.mankier.com/8/conntrack#-m), [--mark](https://www.mankier.com/8/conntrack#--mark) _MARK[/MASK]_ 
    
Specify the conntrack mark. Optionally, a mask value can be specified. In "[--update](https://www.mankier.com/8/conntrack#--update)" mode, this mask specifies the bits that should be zeroed before XORing the MARK value into the ctmark. Otherwise, the mask is logically ANDed with the existing mark before the comparison. In "[--create](https://www.mankier.com/8/conntrack#--create)" mode, the mask is ignored. 

[-l](https://www.mankier.com/8/conntrack#-l), [--label](https://www.mankier.com/8/conntrack#--label) _LABEL_ 
    
Specify a conntrack label. This option is only available in conjunction with "[-L](https://www.mankier.com/8/conntrack#-L), [--dump](https://www.mankier.com/8/conntrack#--dump)", "[-E](https://www.mankier.com/8/conntrack#-E), [--event](https://www.mankier.com/8/conntrack#--event)", "[-U](https://www.mankier.com/8/conntrack#-U) [--update](https://www.mankier.com/8/conntrack#--update)" or "[-D](https://www.mankier.com/8/conntrack#-D) [--delete](https://www.mankier.com/8/conntrack#--delete)". Match entries whose labels include those specified as arguments. Use multiple [-l](https://www.mankier.com/8/conntrack#-l) options to specify multiple labels that need to be set. 

[--labelmap](https://www.mankier.com/8/conntrack#--labelmap) _PATH_ 
    
Specify the path to a connlabel.conf file to load instead of the default one. This option is only available in conjunction with "[-L](https://www.mankier.com/8/conntrack#-L), [--dump](https://www.mankier.com/8/conntrack#--dump)", "[-E](https://www.mankier.com/8/conntrack#-E), [--event](https://www.mankier.com/8/conntrack#--event)", "[-U](https://www.mankier.com/8/conntrack#-U) [--update](https://www.mankier.com/8/conntrack#--update)" or "[-D](https://www.mankier.com/8/conntrack#-D) [--delete](https://www.mankier.com/8/conntrack#--delete)". 

[--label-add](https://www.mankier.com/8/conntrack#--label-add) _LABEL_ 
    
Specify the conntrack label to add to the selected conntracks. This option is only available in conjunction with "[-I](https://www.mankier.com/8/conntrack#-I), [--create](https://www.mankier.com/8/conntrack#--create)", "[-A](https://www.mankier.com/8/conntrack#-A), [--add](https://www.mankier.com/8/conntrack#--add)" or "[-U](https://www.mankier.com/8/conntrack#-U), [--update](https://www.mankier.com/8/conntrack#--update)". As a rule of thumb, you must use either the 'connlabel' match in your iptables ruleset or the 'ct label' statement in your nftables ruleset, this turns on the ct label support in the kernel and it allows you to update labels via "[-U](https://www.mankier.com/8/conntrack#-U), [--update](https://www.mankier.com/8/conntrack#--update)", otherwise label updates are ignored. 

[--label-del](https://www.mankier.com/8/conntrack#--label-del) _[LABEL]_ 
    
Specify the conntrack label to delete from the selected conntracks. If no label is given, all labels are deleted. This option is only available in conjunction with "[-U](https://www.mankier.com/8/conntrack#-U), [--update](https://www.mankier.com/8/conntrack#--update)". 

[-c](https://www.mankier.com/8/conntrack#-c), [--secmark](https://www.mankier.com/8/conntrack#--secmark) _SECMARK_ 
    
Specify the conntrack selinux security mark. 

[-u](https://www.mankier.com/8/conntrack#-u), [--status](https://www.mankier.com/8/conntrack#--status) _[ASSURED|SEEN_REPLY|FIXED_TIMEOUT|EXPECTED|OFFLOAD|UNSET][,...]_ 
    
Specify the conntrack status.     
Filter source NAT connections.     
Filter destination NAT connections.     
Filter any NAT connections.     
Filter by conntrack zone. See iptables CT target for more information.     
Filter by conntrack zone in original direction. See iptables CT target for more information.     
Filter by conntrack zone in reply direction. See iptables CT target for more information. 

[--tuple-src](https://www.mankier.com/8/conntrack#--tuple-src) _IP_ADDRESS_ 
    
Specify the tuple source address of an expectation. Implies "[--mask-src](https://www.mankier.com/8/conntrack#--mask-src)" when CIDR notation is used. 

[--tuple-dst](https://www.mankier.com/8/conntrack#--tuple-dst) _IP_ADDRESS_ 
    
Specify the tuple destination address of an expectation. Implies "[--mask-dst](https://www.mankier.com/8/conntrack#--mask-dst)" when CIDR notation is used. 

[--mask-src](https://www.mankier.com/8/conntrack#--mask-src) _IP_ADDRESS_ 
    
Specify the source address mask. For conntracks this option is only available in conjunction with "[-L](https://www.mankier.com/8/conntrack#-L), [--dump](https://www.mankier.com/8/conntrack#--dump)", "[-E](https://www.mankier.com/8/conntrack#-E), [--event](https://www.mankier.com/8/conntrack#--event)", "[-U](https://www.mankier.com/8/conntrack#-U) [--update](https://www.mankier.com/8/conntrack#--update)" or "[-D](https://www.mankier.com/8/conntrack#-D) [--delete](https://www.mankier.com/8/conntrack#--delete)". For expectations this option is only available in conjunction with "[-I](https://www.mankier.com/8/conntrack#-I), [--create](https://www.mankier.com/8/conntrack#--create)". 

[--mask-dst](https://www.mankier.com/8/conntrack#--mask-dst) _IP_ADDRESS_ 
    
Specify the destination address mask. Same limitations as for "[--mask-src](https://www.mankier.com/8/conntrack#--mask-src)". ### [Protocol Filter Parameters](https://www.mankier.com/8/conntrack#Options-Protocol_Filter_Parameters) 

TCP-specific fields:


**--sport, --orig-port-src** _PORT_ 
    
Source port in original direction 

**--dport, --orig-port-dst** _PORT_ 
    
Destination port in original direction 

**--reply-port-src** _PORT_ 
    
Source port in reply direction 

**--reply-port-dst** _PORT_ 
    
Destination port in reply direction 

**--state** _state_ 
    
TCP state, one of NONE, SYN_SENT, SYN_RECV, ESTABLISHED, FIN_WAIT, CLOSE_WAIT, LAST_ACK, TIME_WAIT, CLOSE or LISTEN. 

UDP-specific fields:


**--sport, --orig-port-src** _PORT_ 
    
Source port in original direction 

**--dport, --orig-port-dst** _PORT_ 
    
Destination port in original direction 

**--reply-port-src** _PORT_ 
    
Source port in reply direction 

**--reply-port-dst** _PORT_ 
    
Destination port in reply direction 

ICMP-specific fields:


**--icmp-type** _TYPE_ 
    
ICMP Type. Has to be specified numerically. 

**--icmp-code** _CODE_ 
    
ICMP Code. Has to be specified numerically. 

**--icmp-id** _ID_ 
    
ICMP Id. Has to be specified numerically (non-mandatory) 

UDPlite-specific fields:


**--sport, --orig-port-src** _PORT_ 
    
Source port in original direction 

**--dport, --orig-port-dst** _PORT_ 
    
Destination port in original direction 

**--reply-port-src** _PORT_ 
    
Source port in reply direction 

**--reply-port-dst** _PORT_ 
    
Destination port in reply direction 

SCTP-specific fields:


**--sport, --orig-port-src** _PORT_ 
    
Source port in original direction 

**--dport, --orig-port-dst** _PORT_ 
    
Destination port in original direction 

**--reply-port-src** _PORT_ 
    
Source port in reply direction 

**--reply-port-dst** _PORT_ 
    
Destination port in reply direction 

**--state** _state_ 
    
SCTP state, one of NONE, CLOSED, COOKIE_WAIT, COOKIE_ECHOED, ESTABLISHED, SHUTDOWN_SENT, SHUTDOWN_RECD, SHUTDOWN_ACK_SENT. 

**--orig-vtag** _value_ 
    
Verification tag (32-bits value) in the original direction 

**--reply-vtag** _value_ 
    
Verification tag (32-bits value) in the reply direction 

DCCP-specific fields (needs Linux >= 2.6.30):


**--sport, --orig-port-src** _PORT_ 
    
Source port in original direction 

**--dport, --orig-port-dst** _PORT_ 
    
Destination port in original direction 

**--reply-port-src** _PORT_ 
    
Source port in reply direction 

**--reply-port-dst** _PORT_ 
    
Destination port in reply direction 

**--state** _state_ 
    
DCCP state, one of NONE, REQUEST, RESPOND, PARTOPEN, OPEN, CLOSEREQ, CLOSING, TIMEWAIT. 

**--role** _[client|server]_ 
    
Role that the original conntrack tuple is tracking 

GRE-specific fields:


**--srckey, --orig-key-src** _KEY_ 
    
Source key in original direction (in hexadecimal or decimal) 

**--dstkey, --orig-key-dst** _KEY_ 
    
Destination key in original direction (in hexadecimal or decimal) 

**--reply-key-src** _KEY_ 
    
Source key in reply direction (in hexadecimal or decimal) 

**--reply-key-dst** _KEY_ 
    
Destination key in reply direction (in hexadecimal or decimal) ## [Diagnostics](https://www.mankier.com/8/conntrack#Diagnostics)
The exit code is 0 for correct function. Errors which appear to be caused by invalid command line parameters cause an exit code of 2. Any other errors cause an exit code of 1.
## [Examples](https://www.mankier.com/8/conntrack#Examples) 

**conntrack[-L](https://www.mankier.com/8/conntrack#-L)**
    
Show the connection tracking table in /proc/net/ip_conntrack format 

**conntrack[-L](https://www.mankier.com/8/conntrack#-L) [-o](https://www.mankier.com/8/conntrack#-o) extended**
    
Show the connection tracking table in /proc/net/nf_conntrack format, with additional information. 

**conntrack[-L](https://www.mankier.com/8/conntrack#-L) [-o](https://www.mankier.com/8/conntrack#-o) xml**
    
Show the connection tracking table in XML 

**conntrack[-L](https://www.mankier.com/8/conntrack#-L) [-o](https://www.mankier.com/8/conntrack#-o) save**
    
Show the connection tracking table in conntrack syntax format 

**conntrack[-L](https://www.mankier.com/8/conntrack#-L) [-f](https://www.mankier.com/8/conntrack#-f) ipv6 [-o](https://www.mankier.com/8/conntrack#-o) extended**
    
Only dump IPv6 connections in /proc/net/nf_conntrack format, with additional information. 

**conntrack[-L](https://www.mankier.com/8/conntrack#-L) [--src-nat](https://www.mankier.com/8/conntrack#--src-nat)**
    
Show source NAT connections 

**conntrack[-E](https://www.mankier.com/8/conntrack#-E) [-o](https://www.mankier.com/8/conntrack#-o) timestamp**
    
Show connection events together with the timestamp 

**conntrack[-D](https://www.mankier.com/8/conntrack#-D) [-s](https://www.mankier.com/8/conntrack#-s) 1.2.3.4**
    
Delete all flows whose source address is 1.2.3.4 

**conntrack[-U](https://www.mankier.com/8/conntrack#-U) [-s](https://www.mankier.com/8/conntrack#-s) 1.2.3.4 [-m](https://www.mankier.com/8/conntrack#-m) 1**
    
Set connmark to 1 of all the flows whose source address is 1.2.3.4 

**conntrack[-L](https://www.mankier.com/8/conntrack#-L) [-w](https://www.mankier.com/8/conntrack#-w) 11 [-o](https://www.mankier.com/8/conntrack#-o) save | sed s/[-w](https://www.mankier.com/8/conntrack#-w) 11/[-w](https://www.mankier.com/8/conntrack#-w) 12/g | conntrack [--load-file](https://www.mankier.com/8/conntrack#--load-file) -**
    
Copy all entries from ct zone 11 to ct zone 12 ## [Bugs](https://www.mankier.com/8/conntrack#Bugs)
Please, report them to netfilter-devel@vger.kernel.org or file a bug in Netfilter's bugzilla (<https://bugzilla.netfilter.org>).
## [See Also](https://www.mankier.com/8/conntrack#See_Also)
**nftables**(8),[iptables(8)](https://www.mankier.com/8/iptables),[conntrackd(8)](https://www.mankier.com/8/conntrackd)See <http://conntrack-tools.netfilter.org>
## [Authors](https://www.mankier.com/8/conntrack#Authors)
Jay Schulist, Patrick McHardy, Harald Welte and Pablo Neira Ayuso wrote the kernel-level "ctnetlink" interface that is used by the conntrack tool.
Pablo Neira Ayuso wrote and maintains the conntrack tool, Harald Welte added support for conntrack-based accounting counters.
Man page written by Harald Welte <laforge@netfilter.org> and Pablo Neira Ayuso <pablo@netfilter.org>.
## [Referenced By](https://www.mankier.com/8/conntrack#Referenced_By)
[conntrackd(8)](https://www.mankier.com/8/conntrackd), [conntrackd.conf(5)](https://www.mankier.com/5/conntrackd.conf), [flowtop(8)](https://www.mankier.com/8/flowtop), [nfct(8)](https://www.mankier.com/8/nfct), [shorewall(8)](https://www.mankier.com/8/shorewall).
Aug 9, 2019
