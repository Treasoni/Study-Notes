---
url: "https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains"
title: "Configuring chains - nftables wiki"
scraped_at: 2026-09-23T06:11:59+00:00
---

# Configuring chains
From nftables wiki
[Jump to navigation](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#mw-head) [Jump to search](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#searchInput)
As in _iptables_ , with _nftables_ you attach your [rules](https://wiki.nftables.org/wiki-nftables/index.php/Simple_rule_management "Simple rule management") to chains. Unlike in _iptables_ , there are no predefined chains like INPUT, OUTPUT, etc. Instead, to filter packets at a particular processing step, you explicitly create a **base chain** with name of your choosing, and attach it to the appropriate [ Netfilter hook](https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks "Netfilter hooks"). This allows very flexible configurations without slowing Netfilter down with built-in chains not needed by your ruleset. 
## Contents
  * [1 Syntactic conventions](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Syntactic_conventions)
  * [2 Adding base chains](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Adding_base_chains)
    * [2.1 Base chain types](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Base_chain_types)
    * [2.2 Base chain hooks](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Base_chain_hooks)
    * [2.3 Base chain priority](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Base_chain_priority)
    * [2.4 Base chain policy](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Base_chain_policy)
  * [3 Adding regular chains](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Adding_regular_chains)
  * [4 Deleting chains](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Deleting_chains)
  * [5 Flushing chains](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Flushing_chains)
  * [6 Example configuration: Filtering traffic for your standalone computer](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Example_configuration:_Filtering_traffic_for_your_standalone_computer)


# Syntactic conventions
Naturally, in order to make use of _nftables_ commands and directives, it is necessary to become familiar with them, along with their supported grammar. Even with that knowledge, users sometimes experience difficulties where passing _nftables_ commands as arguments to the nft(8) utility. That's because shells recognise certain characters as metacharacters and treat them in a special way unless they are quoted. 
Throughout this article, examples that begin with the hash character (U+23) can be taken as examples of valid shell code. That is, they are syntactically valid if entered into any implementation of the Shell Command Language, including bash. By contrast, examples that do not begin with the hash character can be interpreted as either synopses of _nftables_ grammar, similar in style to the nft(8) man page, or as examples of complete rulesets, if so indicated. 
As such, examples of shell code shall generally be of the following form. 

```
# nft 'nftables commands go here'
```

Note that enclosing the _nftables_ commands within single quotes is a straightforward way of preventing the shell from interpreting characters as metacharacters, most notably the semicolon. Rather, the shell will consider all that is between the pair of single quotes as a single word before passing it on to the nft(8) utility as a single argument, verbatim. Another way to prevent the shell from attempting to parse metacharacters is to run nft(8) in its interactive mode. 

```
# nft -i
```

In that case, nft(8) will directly interpret any further input given until such time as it is either interrupted, encounters the end-of-file (EOF) condition, or encounters the "quit" command. In most terminal emulators, EOF can be conveyed with the Ctrl+D key combination. 
Examples describing _nftables_ grammar shall employ square brackets (U+5B, U+5D) to denote optional components of syntax, and angle brackets (U+3C, U+3D) to denote user-specified values. 
# Adding base chains
Base chains are those that are registered into the [Netfilter hooks](https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks "Netfilter hooks"), i.e. these chains see packets flowing through your Linux TCP/IP stack. The syntax for adding base chains is as follows. 

```
add chain [<family>] <table_name> <chain_name> { type <type> hook <hook> [device <device>] priority <priority> ; [policy <policy> ;] [comment <comment> ;] }
```

The following example shows how to add a new base chain _input_ to the _filter_ table (which must have been previously created): 

```
# nft 'add chain ip filter input { type filter hook input priority 0; }'
```

The _add chain_ command registers the _input_ chain, that it attached to the _input_ hook so it will see packets that are addressed to the local processes. 
The _priority_ is important since it determines the ordering of the chains, thus, if you have several chains in the _input_ hook, you can decide which one sees packets before another. For example, input chains with priorities -12, -1, 0, 10 would be consulted exactly in that order. It's possible to give two base chains the same priority, but there is no guaranteed evaluation order of base chains with identical priority that are attached to the same hook location. 
If you want to use _nftables_ to filter traffic for desktop Linux computers, i.e. a computer which does not forward traffic, you can also register the output chain: 

```
# nft 'add chain ip filter output { type filter hook output priority 0; }'
```

Now you are ready to filter incoming (directed to local processes) and outgoing (generated by local processes) traffic. 
**Important note** : If you don't include the chain configuration that is specified enclosed in the curly braces, you are creating a regular chain that will not see any packets (similar to _iptables -N chain-name_). 
Since nftables 0.5, you can also specify the default policy for base chains as in _iptables_ : 

```
# nft 'add chain ip filter output { type filter hook output priority 0; policy accept; }'
```

As in _iptables_ , the two possible default policies are _accept_ and _drop_. 
When adding a chain on **ingress** hook, it is mandatory to specify the device where the chain will be attached: 

```
# nft 'add chain netdev filter eth0_filter { type filter hook ingress device eth0 priority 0; }'
```

## Base chain types
The possible chain types are: 
  * **filter** , which is used to filter packets. This is supported by the arp, bridge, ip, ip6 and inet table families.
  * **route** , which is used to reroute packets if any relevant IP header field or the packet mark is modified. If you are familiar with _iptables_ , this chain type provides equivalent semantics to the _mangle_ table but only for the _output_ hook (for other hooks use type _filter_ instead). This is supported by the ip, ip6 and inet table families.
  * **nat** , which is used to perform Networking Address Translation (NAT). Only the first packet of a given flow hits this chain; subsequent packets bypass it. Therefore, never use this chain for filtering. The _nat_ chain type is supported by the ip, ip6 and inet table families.


## Base chain hooks
The possible [ **hooks**](https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks "Netfilter hooks") that you can use when you configure your base chain are: 
  * **ingress** (only in _netdev_ family since Linux kernel 4.2, and _inet_ family since Linux kernel 5.10): sees packets immediately after they are passed up from the NIC driver, before even prerouting. So you have an alternative to _tc_.
  * **prerouting** : sees all incoming packets, before any routing decision has been made. Packets may be addressed to the local or remote systems.
  * **input** : sees incoming packets that are addressed to and have now been routed to the local system and processes running there.
  * **forward** : sees incoming packets that are not addressed to the local system.
  * **output** : sees packets that originated from processes in the local machine.
  * **postrouting** : sees all packets after routing, just before they leave the local system.


## Base chain priority
Each nftables base chain is assigned a [**priority**](https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks#Priority_within_hook "Netfilter hooks") that defines its ordering among other base chains, flowtables, and Netfilter internal operations at the same hook. For example, a chain on the _prerouting_ hook with priority _-300_ will be placed before connection tracking operations. 
**NOTE** : If a packet is accepted and there is another chain, bearing the same hook type and with a later priority, then the packet will subsequently traverse this other chain. Hence, an accept verdict - be it by way of a rule or the default chain policy - isn't necessarily final. However, the same is _not_ true of packets that are subjected to a drop verdict. Instead, drops take immediate effect, with no further rules or chains being evaluated. 
The following ruleset demonstrates this potentially surprising distinction in behaviour: 

```
table ip filter {
        # This chain is evaluated first due to priority
        chain services {
                type filter hook input priority 0; policy accept;

                # If matched, this rule will prevent any further evaluation
                tcp dport http drop

                # If matched, and despite the accept verdict, the packet proceeds to enter the chain below
                tcp dport ssh accept

                # Likewise for any packets that get this far and hit the default policy
        }

        # This chain is evaluated last due to priority
        chain input {
                type filter hook input priority 1; policy drop;
                # All ingress packets end up being dropped here!
        }
}

```

If the priority of the 'input' chain above were to be changed to -1, the only difference would be that no packets have the opportunity to enter the 'services' chain. Either way, this ruleset will result in all ingress packets being dropped. 
In summary, packets will traverse all of the chains within the scope of a given hook until they are either dropped or no more base chains exist. An accept verdict is only guaranteed to be final in the case that there is no later chain bearing the same type of hook as the chain that the packet originally entered. 
Netfilter's hook execution mechanism is described in more detail in [Pablo's paper on connection tracking](http://people.netfilter.org/pablo/docs/login.pdf). 
## Base chain policy
This is the default verdict that will be applied to packets reaching the end of the chain (i.e, no more rules to be evaluated against). 
Currently there are 2 policies: **accept** (default) or **drop**. 
  * The _accept_ verdict means that the packet will keep traversing the network stack (default).
  * The _drop_ verdict means that the packet is discarded if the packet reaches the end of the base chain.


**NOTE** : If no policy is explicitly selected, the default policy **accept** will be used. 
# Adding regular chains
You can also create regular chains, analogous to _iptables_ user-defined chains, the syntax for which is as follows. 

```
add chain [family] <table_name> <chain_name> [comment <comment>]
```

The chain name is an arbitrary string, with arbitrary case. 
Note that no _hook_ keyword is included when adding a regular chain. Because it is not attached to a Netfilter hook, **by itself a regular chain does not see any traffic**. But one or more base chains can include rules that [jump](https://wiki.nftables.org/wiki-nftables/index.php/Jumping_to_chain "Jumping to chain") or goto this chain -- following which, the regular chain processes packets in exactly the same way as the calling base chain. It can be very useful to arrange your ruleset into a tree of base and regular chains by using the [jump](https://wiki.nftables.org/wiki-nftables/index.php/Jumping_to_chain "Jumping to chain") and/or goto actions. (Though we're getting a bit ahead of ourselves, nftables [vmaps](https://wiki.nftables.org/wiki-nftables/index.php/Verdict_Maps_\(vmaps\) "Verdict Maps \(vmaps\)") provide an even more powerful way to construct highly-efficient branched rulesets.) 
# Deleting chains
The syntax for deleting chains is as follows. 

```
delete chain [family] <table_name> <chain_name>
```

The only condition is that the chain you want to delete needs to be empty, otherwise the kernel will complain that the chain is still in use. 

```
# nft 'delete chain ip filter input'
<cmdline>:1:1-28: Error: Could not delete chain: Device or resource busy
delete chain ip filter input
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

You will have to [flush the ruleset](https://wiki.nftables.org/wiki-nftables/index.php/Simple_rule_management "Simple rule management") in that chain before you can remove the chain. 
# Flushing chains
To flush a chain means to delete all of the rules that it contains, if any. The syntax for doing so is as follows. 

```
flush chain [family] <table_name> <chain_name>
```

# Example configuration: Filtering traffic for your standalone computer
You can create a table with two base chains to define rule to filter traffic coming to and leaving from your computer, asumming IPv4 connectivity: 

```
# nft 'add table ip filter'
# nft 'add chain ip filter input { type filter hook input priority 0; }'
# nft 'add chain ip filter output { type filter hook output priority 0; }'
```

Now, you can start attaching [rules](https://wiki.nftables.org/wiki-nftables/index.php/Simple_rule_management "Simple rule management") to these two base chains. Note that you don't need the _forward_ chain in this case since this example assumes that you're configuring nftables to filter traffic for a standalone computer that doesn't behave as router. 
Here is the exact same policy, only shown in the declarative style. That is, in the same format as would be employed upon issuing the "list ruleset" command. Despite the marked difference in style, it constitutes valid _nftables_ syntax and is equivalent to the combination of "add table" and "add chain" commands shown above. 

```
table ip filter {
	chain input {
		type filter hook input priority filter; policy accept;
	}

	chain output {
		type filter hook output priority filter; policy accept;
	}
}
```

Retrieved from "[http://wiki.nftables.org/wiki-nftables/index.php?title=Configuring_chains&oldid=1151](http://wiki.nftables.org/wiki-nftables/index.php?title=Configuring_chains&oldid=1151)"
[Categories](https://wiki.nftables.org/wiki-nftables/index.php/Special:Categories "Special:Categories"): 
  * [Pages using deprecated source tags](https://wiki.nftables.org/wiki-nftables/index.php?title=Category:Pages_using_deprecated_source_tags&action=edit&redlink=1 "Category:Pages using deprecated source tags \(page does not exist\)")
  * [Pages with syntax highlighting errors](https://wiki.nftables.org/wiki-nftables/index.php?title=Category:Pages_with_syntax_highlighting_errors&action=edit&redlink=1 "Category:Pages with syntax highlighting errors \(page does not exist\)")


## Navigation menu
### Search
