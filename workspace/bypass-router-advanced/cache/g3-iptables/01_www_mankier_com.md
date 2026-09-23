---
url: "https://www.mankier.com/8/iptables"
title: "iptables: administration tool for IPv4/IPv6 packet filtering and NAT | Man Page | System Administration | iptables-libs | ManKier"
scraped_at: 2026-09-23T06:11:42+00:00
---


[iptables](https://www.mankier.com/8/iptables)
## [Examples (TL;DR)](https://www.mankier.com/8/iptables#Examples_\(TL;DR\))
  * View chains, rules, packet/byte counters, and line numbers for the filter table: `sudo iptables [-vnL --line-numbers[](https://www.mankier.com/8/iptables#--line-numbers)|--verbose[](https://www.mankier.com/8/iptables#--verbose) --numeric[](https://www.mankier.com/8/iptables#--numeric) --list[](https://www.mankier.com/8/iptables#--list) --line-numbers[](https://www.mankier.com/8/iptables#--line-numbers)]`
  * Set chain policy rule: `sudo iptables [-P[](https://www.mankier.com/8/iptables#-P)|--policy[](https://www.mankier.com/8/iptables#--policy)] chain rule`
  * Append rule to chain policy for IP: `sudo iptables [-A[](https://www.mankier.com/8/iptables#-A)|--append[](https://www.mankier.com/8/iptables#--append)] chain [-s|--source] ip_address [-j|--jump] rule`
  * Append rule to chain policy for IP considering protocol and port: `sudo iptables [-A[](https://www.mankier.com/8/iptables#-A)|--append[](https://www.mankier.com/8/iptables#--append)] chain [-s|--source] ip_address [-p|--protocol] tcp|udp|icmp|... --dport port [-j|--jump] rule`
  * Add a NAT rule to translate all traffic from the `192.168.0.0/24` subnet to the host's public IP: `sudo iptables [-t[](https://www.mankier.com/8/iptables#-t)|--table[](https://www.mankier.com/8/iptables#--table)] nat [-A[](https://www.mankier.com/8/iptables#-A)|--append[](https://www.mankier.com/8/iptables#--append)] POSTROUTING [-s|--source] 192.168.0.0/24 [-j|--jump] MASQUERADE`
  * Delete chain rule: `sudo iptables [-D[](https://www.mankier.com/8/iptables#-D)|--delete[](https://www.mankier.com/8/iptables#--delete)] chain rule_line_number`


[tldr.sh](https://tldr.sh/)
## [Synopsis](https://www.mankier.com/8/iptables#Synopsis)
`**iptables** [  _table_] {|||} _chain rule-specification_`
`**ip6tables** [ _table_] {|||} _chain rule-specification_`
`**iptables** [ _table_]  _chain_ [_rulenum_] _rule-specification_`
`**iptables** [ _table_]  _chain rulenum rule-specification_`
`**iptables** [ _table_]  _chain rulenum_`
`**iptables** [ _table_]  [_chain_ [_rulenum_]]`
`**iptables** [ _table_] {||} [_chain_ [_rulenum_]] [_options..._]`
`**iptables** [ _table_]  _chain_`
`**iptables** [ _table_]  [_chain_]`
`**iptables** [ _table_]  _chain policy_`
`**iptables** [ _table_]  _old-chain-name new-chain-name_`
`rule-specification := [matches...] [target]`
`match := **-m** _matchname_ [per-match-options]`
`target := **-j** _targetname_ [per-target-options]`
## [Description](https://www.mankier.com/8/iptables#Description)
**Iptables** and **ip6tables** are used to set up, maintain, and inspect the tables of IPv4 and IPv6 packet filter rules in the Linux kernel. Several different tables may be defined. Each table contains a number of built-in chains and may also contain user-defined chains.
Each chain is a list of rules which can match a set of packets. Each rule specifies what to do with a packet that matches. This is called a `target', which may be a jump to a user-defined chain in the same table.
## [Targets](https://www.mankier.com/8/iptables#Targets)
A firewall rule specifies criteria for a packet and a target. If the packet does not match, the next rule in the chain is examined; if it does match, then the next rule is specified by the value of the target, which can be the name of a user-defined chain, one of the targets described in [iptables-extensions(8)](https://www.mankier.com/8/iptables-extensions), or one of the special values **ACCEPT** , **DROP** or **RETURN**.
**ACCEPT** means to let the packet through. **DROP** means to drop the packet on the floor. **RETURN** means stop traversing this chain and resume at the next rule in the previous (calling) chain. If the end of a built-in chain is reached or a rule in a built-in chain with target **RETURN** is matched, the target specified by the chain policy determines the fate of the packet.
## [Tables](https://www.mankier.com/8/iptables#Tables)
There are currently five independent tables (which tables are present at any time depends on the kernel configuration options and which modules are present). 

[-t](https://www.mankier.com/8/iptables#-t), [--table](https://www.mankier.com/8/iptables#--table) _table_ 
    
This option specifies the packet matching table which the command should operate on. If the kernel is configured with automatic module loading, an attempt will be made to load the appropriate module for that table if it is not already there.
The tables are as follows: 

**filter** :
    
This is the default table (if no [-t](https://www.mankier.com/8/iptables#-t) option is passed). It contains the built-in chains **INPUT** (for packets destined to local sockets), **FORWARD** (for packets being routed through the box), and **OUTPUT** (for locally-generated packets). 

**nat** :
    
This table is consulted when a packet that creates a new connection is encountered. It consists of four built-ins: **PREROUTING** (for altering packets as soon as they come in), **INPUT** (for altering packets destined for local sockets), **OUTPUT** (for altering locally-generated packets before routing), and **POSTROUTING** (for altering packets as they are about to go out). IPv6 NAT support is available since kernel 3.7. 

**mangle** :
    
This table is used for specialized packet alteration. Until kernel 2.4.17 it had two built-in chains: **PREROUTING** (for altering incoming packets before routing) and **OUTPUT** (for altering locally-generated packets before routing). Since kernel 2.4.18, three other built-in chains are also supported: **INPUT** (for packets coming into the box itself), **FORWARD** (for altering packets being routed through the box), and **POSTROUTING** (for altering packets as they are about to go out). 

**raw** :
    
This table is used mainly for configuring exemptions from connection tracking in combination with the NOTRACK target. It registers at the netfilter hooks with higher priority and is thus called before ip_conntrack, or any other IP tables. It provides the following built-in chains: **PREROUTING** (for packets arriving via any network interface) and **OUTPUT** (for packets generated by local processes). 

**security** :
    
This table is used for Mandatory Access Control (MAC) networking rules, such as those enabled by the **SECMARK** and **CONNSECMARK** targets. Mandatory Access Control is implemented by Linux Security Modules such as SELinux. The security table is called after the filter table, allowing any Discretionary Access Control (DAC) rules in the filter table to take effect before MAC rules. This table provides the following built-in chains: **INPUT** (for packets coming into the box itself), **OUTPUT** (for altering locally-generated packets before routing), and **FORWARD** (for altering packets being routed through the box). ## [Options](https://www.mankier.com/8/iptables#Options)
The options that are recognized by **iptables** and **ip6tables** can be divided into several different groups.
### [Commands](https://www.mankier.com/8/iptables#Options-Commands)
These options specify the desired action to perform. Only one of them can be specified on the command line unless otherwise stated below. For long versions of the command and option names, you need to use only enough letters to ensure that **iptables** can differentiate it from all other options. 

[-A](https://www.mankier.com/8/iptables#-A), [--append](https://www.mankier.com/8/iptables#--append) _chain rule-specification_ 
    
Append one or more rules to the end of the selected chain. When the source and/or destination names resolve to more than one address, a rule will be added for each possible address combination. 

[-C](https://www.mankier.com/8/iptables#-C), [--check](https://www.mankier.com/8/iptables#--check) _chain rule-specification_ 
    
Check whether a rule matching the specification does exist in the selected chain. This command uses the same logic as to find a matching entry, but does not alter the existing iptables configuration and uses its exit code to indicate success or failure. 

[-D](https://www.mankier.com/8/iptables#-D), [--delete](https://www.mankier.com/8/iptables#--delete) _chain rule-specification_ 


, _chain rulenum_ 
    
Delete one or more rules from the selected chain. There are two versions of this command: the rule can be specified as a number in the chain (starting at 1 for the first rule) or a rule to match. 

[-I](https://www.mankier.com/8/iptables#-I), [--insert](https://www.mankier.com/8/iptables#--insert) _chain_ [_rulenum_] _rule-specification_ 
    
Insert one or more rules in the selected chain as the given rule number. So, if the rule number is 1, the rule or rules are inserted at the head of the chain. This is also the default if no rule number is specified. 

[-R](https://www.mankier.com/8/iptables#-R), [--replace](https://www.mankier.com/8/iptables#--replace) _chain rulenum rule-specification_ 
    
Replace a rule in the selected chain. If the source and/or destination names resolve to multiple addresses, the command will fail. Rules are numbered starting at 1. 

[-L](https://www.mankier.com/8/iptables#-L), [--list](https://www.mankier.com/8/iptables#--list) [_chain_]
    
List all rules in the selected chain. If no chain is selected, all chains are listed. Like every other iptables command, it applies to the specified table (filter is the default), so NAT rules get listed by

```
 iptables -t[](https://www.mankier.com/8/iptables#-t) nat -n[](https://www.mankier.com/8/iptables#-n) -L[](https://www.mankier.com/8/iptables#-L)
```

Please note that it is often used with the option, in order to avoid long reverse DNS lookups. It is legal to specify the (zero) option as well, in which case the chain(s) will be atomically listed and zeroed. The exact output is affected by the other arguments given. The exact rules are suppressed until you use

```
 iptables -L[](https://www.mankier.com/8/iptables#-L) -v[](https://www.mankier.com/8/iptables#-v)
```

or [iptables-save(8)](https://www.mankier.com/8/iptables-save). 

[-S](https://www.mankier.com/8/iptables#-S), [--list-rules](https://www.mankier.com/8/iptables#--list-rules) [_chain_]
    
Print all rules in the selected chain. If no chain is selected, all chains are printed like iptables-save. Like every other iptables command, it applies to the specified table (filter is the default). 

[-F](https://www.mankier.com/8/iptables#-F), [--flush](https://www.mankier.com/8/iptables#--flush) [_chain_]
    
Flush the selected chain (all the chains in the table if none is given). This is equivalent to deleting all the rules one by one. 

[-Z](https://www.mankier.com/8/iptables#-Z), [--zero](https://www.mankier.com/8/iptables#--zero) [_chain_ [_rulenum_]]
    
Zero the packet and byte counters in all chains, or only the given chain, or only the given rule in a chain. It is legal to specify the , (list) option as well, to see the counters immediately before they are cleared. (See above.) 

[-N](https://www.mankier.com/8/iptables#-N), [--new-chain](https://www.mankier.com/8/iptables#--new-chain) _chain_ 
    
Create a new user-defined chain by the given name. There must be no target of that name already. 

[-X](https://www.mankier.com/8/iptables#-X), [--delete-chain](https://www.mankier.com/8/iptables#--delete-chain) [_chain_]
    
Delete the chain specified. There must be no references to the chain. If there are, you must delete or replace the referring rules before the chain can be deleted. The chain must be empty, i.e. not contain any rules. If no argument is given, it will delete all empty chains in the table. Empty builtin chains can only be deleted with **iptables-nft**. 

[-P](https://www.mankier.com/8/iptables#-P), [--policy](https://www.mankier.com/8/iptables#--policy) _chain target_ 
    
Set the policy for the built-in (non-user-defined) chain to the given target. The policy target must be either **ACCEPT** or **DROP**. 

[-E](https://www.mankier.com/8/iptables#-E), [--rename-chain](https://www.mankier.com/8/iptables#--rename-chain) _old-chain new-chain_ 
    
Rename the user specified chain to the user supplied name. This is cosmetic, and has no effect on the structure of the table.     
Help. Give a (currently very brief) description of the command syntax. ### [Parameters](https://www.mankier.com/8/iptables#Options-Parameters)
The following parameters make up a rule specification (as used in the add, delete, insert, replace and append commands). 

**-4** , **--ipv4** 
    
This option has no effect in iptables and iptables-restore. If a rule using the **-4** option is inserted with (and only with) **ip6tables-restore** , it will be silently ignored. Any other uses will throw an error. This option allows IPv4 and IPv6 rules in a single rule file for use with both iptables-restore and ip6tables-restore. 

**-6** , **--ipv6** 
    
If a rule using the **-6** option is inserted with (and only with) **iptables-restore** , it will be silently ignored. Any other uses will throw an error. This option allows IPv4 and IPv6 rules in a single rule file for use with both iptables-restore and ip6tables-restore. This option has no effect in ip6tables and ip6tables-restore. 

[**!**] **-p** , **--protocol** _protocol_ 
    
The protocol of the rule or of the packet to check. The specified protocol can be one of **tcp** , **udp** , **udplite** , **icmp** , **icmpv6** , **esp** , **ah** , **sctp** , **mh** or the special keyword "**all** ", or it can be a numeric value, representing one of these protocols or a different one. A protocol name from _/etc/protocols_ is also allowed. A "!" argument before the protocol inverts the test. The number zero is equivalent to **all**. "**all** " will match with all protocols and is taken as default when this option is omitted. Note that, in ip6tables, IPv6 extension headers except **esp** are not allowed. **esp** and **ipv6-nonext** can be used with Kernel version 2.6.11 or later. The number zero is equivalent to **all** , which means that you cannot test the protocol field for the value 0 directly. To match on a HBH header, even if it were the last, you cannot use **-p 0** , but always need **-m hbh**. 

[**!**] **-s** , **--source** _address_[**/**_mask_][**,**_..._]
    
Source specification. _Address_ can be either a network name, a hostname, a network IP address (with **/**_mask_), or a plain IP address. Hostnames will be resolved once only, before the rule is submitted to the kernel. Please note that specifying any name to be resolved with a remote query such as DNS is a really bad idea. The _mask_ can be either an ipv4 network mask (for iptables) or a plain number, specifying the number of 1's at the left side of the network mask. Thus, an iptables mask of _24_ is equivalent to _255.255.255.0_. A "!" argument before the address specification inverts the sense of the address. The flag **--src** is an alias for this option. Multiple addresses can be specified, but this will **expand to multiple rules** (when adding with [-A](https://www.mankier.com/8/iptables#-A)), or will cause multiple rules to be deleted (with [-D](https://www.mankier.com/8/iptables#-D)). 

[**!**] **-d** , **--destination** _address_[**/**_mask_][**,**_..._]
    
Destination specification. See the description of the **-s** (source) flag for a detailed description of the syntax. The flag **--dst** is an alias for this option. 

**-m** , **--match** _match_ 
    
Specifies a match to use, that is, an extension module that tests for a specific property. The set of matches make up the condition under which a target is invoked. Matches are evaluated first to last as specified on the command line and work in short-circuit fashion, i.e. if one extension yields false, evaluation will stop. 

**-j** , **--jump** _target_ 
    
This specifies the target of the rule; i.e., what to do if the packet matches it. The target can be a user-defined chain (other than the one this rule is in), one of the special builtin targets which decide the fate of the packet immediately, or an extension (see [Match and Target Extensions](https://www.mankier.com/8/iptables#Match_and_Target_Extensions) below). If this option is omitted in a rule (and **-g** is not used), then matching the rule will have no effect on the packet's fate, but the counters on the rule will be incremented. 

**-g** , **--goto** _chain_ 
    
This specifies that the processing should continue in a user specified chain. Unlike with the --jump option, **RETURN** will not continue processing in this chain but instead in the chain that called us via --jump. 

[**!**] **-i** , **--in-interface** _name_ 
    
Name of an interface via which a packet was received (only for packets entering the **INPUT** , **FORWARD** and **PREROUTING** chains). When the "!" argument is used before the interface name, the sense is inverted. If the interface name ends in a "+", then any interface which begins with this name will match. If this option is omitted, any interface name will match. 

[**!**] **-o** , **--out-interface** _name_ 
    
Name of an interface via which a packet is going to be sent (for packets entering the **FORWARD** , **OUTPUT** and **POSTROUTING** chains). When the "!" argument is used before the interface name, the sense is inverted. If the interface name ends in a "+", then any interface which begins with this name will match. If this option is omitted, any interface name will match. 

[**!**] **-f** , **--fragment** 
    
This means that the rule only refers to second and further IPv4 fragments of fragmented packets. Since there is no way to tell the source or destination ports of such a packet (or ICMP type), such a packet will not match any rules which specify them. When the "!" argument precedes the "-f" flag, the rule will only match head fragments, or unfragmented packets. This option is IPv4 specific, it is not available in ip6tables. 

**-c** , **--set-counters** _packets bytes_ 
    
This enables the administrator to initialize the packet and byte counters of a rule (during **INSERT** , **APPEND** , **REPLACE** operations). ### [Other Options](https://www.mankier.com/8/iptables#Options-Other_Options)
The following additional options can be specified:     
Verbose output. This option makes the list command show the interface name, the rule options (if any), and the TOS masks. The packet and byte counters are also listed, with the suffix 'K', 'M' or 'G' for 1000, 1,000,000 and 1,000,000,000 multipliers respectively (but see the flag to change this). For appending, insertion, deletion and replacement, this causes detailed information on the rule or rules to be printed. may be specified multiple times to possibly emit more detailed debug statements: Specified twice, **iptables-legacy** will dump table info and entries in libiptc, **iptables-nft** dumps rules in netlink (VM code) presentation. Specified three times, **iptables-nft** will also dump any netlink messages sent to kernel.     
Show program version and the kernel API used. 

[-w](https://www.mankier.com/8/iptables#-w), [--wait](https://www.mankier.com/8/iptables#--wait) [_seconds_]
    
Wait for the xtables lock. To prevent multiple instances of the program from running concurrently, an attempt will be made to obtain an exclusive lock at launch. By default, the program will exit if the lock cannot be obtained. This option will make the program wait (indefinitely or for optional _seconds_) until the exclusive lock can be obtained.     
Numeric output. IP addresses and port numbers will be printed in numeric format. By default, the program will try to display them as host names, network names, or services (whenever applicable).     
Expand numbers. Display the exact value of the packet and byte counters, instead of only the rounded number in K's (multiples of 1000), M's (multiples of 1000K) or G's (multiples of 1000M). This option is only relevant for the command.     
When listing rules, add line numbers to the beginning of each rule, corresponding to that rule's position in the chain. 

[--modprobe](https://www.mankier.com/8/iptables#--modprobe)=_command_ 
    
When adding or inserting rules into a chain, use _command_ to load any necessary modules (targets, match extensions, etc). ## [Lock File](https://www.mankier.com/8/iptables#Lock_File)
iptables uses the _/run/xtables.lock_ file to take an exclusive lock at launch.
The **XTABLES_LOCKFILE** environment variable can be used to override the default setting.
## [Match and Target Extensions](https://www.mankier.com/8/iptables#Match_and_Target_Extensions)
iptables can use extended packet matching and target modules. A list of these is available in the [iptables-extensions(8)](https://www.mankier.com/8/iptables-extensions) manpage.
## [Diagnostics](https://www.mankier.com/8/iptables#Diagnostics)
Various error messages are printed to standard error. The exit code is 0 for correct functioning. Errors which appear to be caused by invalid or abused command line parameters cause an exit code of 2. Errors which indicate an incompatibility between kernel and user space cause an exit code of 3. Errors which indicate a resource problem, such as a busy lock, failing memory allocation or error messages from kernel cause an exit code of 4. Finally, other errors cause an exit code of 1.
## [Bugs](https://www.mankier.com/8/iptables#Bugs)
Bugs? What's this? ;-) Well, you might want to have a look at <https://bugzilla.netfilter.org/> **iptables** will exit immediately with an error code of 111 if it finds that it was called as a setuid-to-root program. iptables cannot be used safely in this manner because it trusts the shared libraries (matches, targets) loaded at run time, the search path can be set using environment variables.
## [Compatibility with Ipchains](https://www.mankier.com/8/iptables#Compatibility_with_Ipchains)
This **iptables** is very similar to ipchains by Rusty Russell. The main difference is that the chains **INPUT** and **OUTPUT** are only traversed for packets coming into the local host and originating from the local host respectively. Hence every packet only passes through one of the three chains (except loopback traffic, which involves both INPUT and OUTPUT chains); previously a forwarded packet would pass through all three.
The other main difference is that **-i** refers to the input interface; **-o** refers to the output interface, and both are available for packets entering the **FORWARD** chain.
The various forms of NAT have been separated out; **iptables** is a pure packet filter when using the default `filter' table, with optional extension modules. This should avoid much of the confusion over the combination of IP masquerading and packet filtering seen previously. So the following options are handled differently:

```
 -j MASQ
 -M -S[](https://www.mankier.com/8/iptables#-S)
 -M -L[](https://www.mankier.com/8/iptables#-L)
```

There are several other changes in iptables.
## [See Also](https://www.mankier.com/8/iptables#See_Also)
[iptables-apply(8)](https://www.mankier.com/8/iptables-apply), [iptables-save(8)](https://www.mankier.com/8/iptables-save), [iptables-restore(8)](https://www.mankier.com/8/iptables-restore), [iptables-extensions(8)](https://www.mankier.com/8/iptables-extensions),
The packet-filtering-HOWTO details iptables usage for packet filtering, the NAT-HOWTO details NAT, the netfilter-extensions-HOWTO details the extensions that are not in the standard distribution, and the netfilter-hacking-HOWTO details the netfilter internals.See <https://www.netfilter.org/>.
## [Authors](https://www.mankier.com/8/iptables#Authors)
Rusty Russell originally wrote iptables, in early consultation with Michael Neuling.
Marc Boucher made Rusty abandon ipnatctl by lobbying for a generic packet selection framework in iptables, then wrote the mangle table, the owner match, the mark stuff, and ran around doing cool stuff everywhere.
James Morris wrote the TOS target, and tos match.
Jozsef Kadlecsik wrote the REJECT target.
Harald Welte wrote the ULOG and NFQUEUE target, the new libiptc, as well as the TTL, DSCP, ECN matches and targets.
The Netfilter Core Team is: Jozsef Kadlecsik, Pablo Neira Ayuso, Eric Leblond, Florian Westphal and Arturo Borrero Gonzalez. Emeritus Core Team members are: Marc Boucher, Martin Josefsson, Yasuyuki Kozakai, James Morris, Harald Welte and Rusty Russell.
Man page originally written by Herve Eychenne <rv@wallfire.org>.
## [Version](https://www.mankier.com/8/iptables#Version)
This manual page applies to iptables/ip6tables 1.8.13.
## [Referenced By](https://www.mankier.com/8/iptables#Referenced_By)
[arptables-legacy(8)](https://www.mankier.com/8/arptables-legacy), [arptables-nft(8)](https://www.mankier.com/8/arptables-nft), [bpfmon(8)](https://www.mankier.com/8/bpfmon), [brctl(8)](https://www.mankier.com/8/brctl), [cdist-type__iptables_apply(7)](https://www.mankier.com/7/cdist-type__iptables_apply), [cdist-type__iptables_rule(7)](https://www.mankier.com/7/cdist-type__iptables_rule), [cgroups(7)](https://www.mankier.com/7/cgroups), [collectd.conf(5)](https://www.mankier.com/5/collectd.conf), [conntrack(8)](https://www.mankier.com/8/conntrack), [conntrackd(8)](https://www.mankier.com/8/conntrackd), [ebtables-legacy(8)](https://www.mankier.com/8/ebtables-legacy), [ebtables-nft(8)](https://www.mankier.com/8/ebtables-nft), [firewall-cmd(1)](https://www.mankier.com/1/firewall-cmd), [firewalld.service(5)](https://www.mankier.com/5/firewalld.service), [firewall-offline-cmd(1)](https://www.mankier.com/1/firewall-offline-cmd), [flowtop(8)](https://www.mankier.com/8/flowtop), [fwcheck_psad(8)](https://www.mankier.com/8/fwcheck_psad), [fwknop(8)](https://www.mankier.com/8/fwknop), [fwknopd(8)](https://www.mankier.com/8/fwknopd), [herbstluftwm(1)](https://www.mankier.com/1/herbstluftwm), [ifconfig(8)](https://www.mankier.com/8/ifconfig), [ip-link(8)](https://www.mankier.com/8/ip-link), [ipset(8)](https://www.mankier.com/8/ipset), [iptables-apply(8)](https://www.mankier.com/8/iptables-apply), [iptables-restore(8)](https://www.mankier.com/8/iptables-restore), [iptables-save(8)](https://www.mankier.com/8/iptables-save), [iptables_selinux(8)](https://www.mankier.com/8/iptables_selinux), [iptables-xml(1)](https://www.mankier.com/1/iptables-xml), [iptstate(8)](https://www.mankier.com/8/iptstate), [ipvsadm(8)](https://www.mankier.com/8/ipvsadm), [monitorix.conf(5)](https://www.mankier.com/5/monitorix.conf), [mountd(8)](https://www.mankier.com/8/mountd), [nbdkit-rate-filter(1)](https://www.mankier.com/1/nbdkit-rate-filter), [netstat(8)](https://www.mankier.com/8/netstat), [network_namespaces(7)](https://www.mankier.com/7/network_namespaces), [nfct(8)](https://www.mankier.com/8/nfct), [nft(8)](https://www.mankier.com/8/nft), [oping(8)](https://www.mankier.com/8/oping), [ovs-ctl(8)](https://www.mankier.com/8/ovs-ctl), [pptpd.conf(5)](https://www.mankier.com/5/pptpd.conf), [proc_pid_net(5)](https://www.mankier.com/5/proc_pid_net), [psad(8)](https://www.mankier.com/8/psad), [redsocks(8)](https://www.mankier.com/8/redsocks), [shorewall(8)](https://www.mankier.com/8/shorewall), [sslsplit(1)](https://www.mankier.com/1/sslsplit), [statd(8)](https://www.mankier.com/8/statd), [systemd.dns-delegate(5)](https://www.mankier.com/5/systemd.dns-delegate), [systemd.socket(5)](https://www.mankier.com/5/systemd.socket), [tayga(8)](https://www.mankier.com/8/tayga), [tc-bpf(8)](https://www.mankier.com/8/tc-bpf), [tc-fw(8)](https://www.mankier.com/8/tc-fw), [tc-mqprio(8)](https://www.mankier.com/8/tc-mqprio), [ufw(8)](https://www.mankier.com/8/ufw), [ufw-framework(8)](https://www.mankier.com/8/ufw-framework), [wg-quick(8)](https://www.mankier.com/8/wg-quick), [xtables-addons(8)](https://www.mankier.com/8/xtables-addons), [xtables-monitor(8)](https://www.mankier.com/8/xtables-monitor), [xtables-nft(8)](https://www.mankier.com/8/xtables-nft), [xtables-translate(8)](https://www.mankier.com/8/xtables-translate).
The man page ip6tables(8) is an alias of iptables(8).
iptables 1.8.13
