---
url: "https://docs.docker.com/engine/network/packet-filtering-firewalls/"
title: "Packet filtering and firewalls | Docker Docs"
scraped_at: 2026-08-27T19:22:06+00:00
---

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)
✕
Start a new chat
### What can I help you with?
I'm Gordon, your AI assistant for Docker and documentation questions.
Try asking
Get started with Docker
Docker Hardened Images
MCP Toolkit
Create an org
Answers are generated based on the documentation.
Back


# Packet filtering and firewalls
Ask Gordon Copy Markdown View Markdown
Table of contents
On Linux, Docker creates firewall rules to implement network isolation, [port publishing](https://docs.docker.com/engine/network/port-publishing/) and filtering.
Because these rules are required for the correct functioning of Docker bridge networks, you should not modify the rules created by Docker.
This page describes options that control Docker's firewall rules to implement functionality including port publishing, and NAT/masquerading.
> Note
> Docker creates firewall rules for bridge networks.
> No rules are created for `ipvlan`, `macvlan` or `host` networking.
## [Firewall backend](https://docs.docker.com/engine/network/packet-filtering-firewalls/#firewall-backend)
By default, Docker Engine creates its firewall rules using iptables, see [Docker with iptables](https://docs.docker.com/engine/network/firewall-iptables/). It also has support for nftables, see [Docker with nftables](https://docs.docker.com/engine/network/firewall-nftables/).
For bridge networks, iptables and nftables have the same functionality.
Docker Engine option `firewall-backend` can be used to select whether iptables or nftables is used. See [daemon configuration](https://docs.docker.com/reference/cli/dockerd/).
## [Docker on a router](https://docs.docker.com/engine/network/packet-filtering-firewalls/#docker-on-a-router)
On Linux, Docker needs "IP Forwarding" enabled on the host. So, it enables the `sysctl` settings `net.ipv4.ip_forward` and `net.ipv6.conf.all.forwarding` if they are not already enabled when it starts. When it does that, it also configures the firewall to drop forwarded packets unless they are explicitly accepted.
When Docker sets the default forwarding policy to "drop", it will prevent your Docker host from acting as a router. This is the recommended setting when IP Forwarding is enabled, unless router functionality is required.
To stop Docker from setting the forwarding policy to "drop", include `"ip-forward-no-drop": true` in `/etc/docker/daemon.json`, or add option `--ip-forward-no-drop` to the `dockerd` command line.
> Note
> With the experimental nftables backend, Docker does not enable IP forwarding itself, and it will not create a default "drop" nftables policy. See [Migrating from iptables to nftables](https://docs.docker.com/engine/network/firewall-nftables/#migrating-from-iptables-to-nftables).
## [Prevent Docker from manipulating firewall rules](https://docs.docker.com/engine/network/packet-filtering-firewalls/#prevent-docker-from-manipulating-firewall-rules)
Setting the `iptables` or `ip6tables` keys to `false` in [daemon configuration](https://docs.docker.com/reference/cli/dockerd/), will prevent Docker from creating most of its `iptables` or `nftables` rules. But, this option is not appropriate for most users, it is likely to break container networking for the Docker Engine.
For example, with Docker's firewalling disabled and no replacement rules, containers in bridge networks will not be able to access internet hosts by masquerading, but all of their ports will be accessible to hosts on the local network.
It is not possible to completely prevent Docker from creating firewall rules, and creating rules after-the-fact is extremely involved and beyond the scope of these instructions.
## [Integration with firewalld](https://docs.docker.com/engine/network/packet-filtering-firewalls/#integration-with-firewalld)
If you are running Docker with the `iptables` or `ip6tables` options set to `true`, and [firewalld](https://firewalld.org) is enabled on your system, in addition to its usual iptables or nftables rules, Docker creates a `firewalld` zone called `docker`, with target `ACCEPT`.
All bridge network interfaces created by Docker (for example, `docker0`) are inserted into the `docker` zone.
Docker also creates a forwarding policy called `docker-forwarding` that allows forwarding from `ANY` zone to the `docker` zone.
## [Docker and ufw](https://docs.docker.com/engine/network/packet-filtering-firewalls/#docker-and-ufw)
[Uncomplicated Firewall](https://launchpad.net/ufw) (ufw) is a frontend that ships with Debian and Ubuntu, and it lets you manage firewall rules. Docker and ufw use firewall rules in ways that make them incompatible with each other.
When you publish a container's ports using Docker, traffic to and from that container gets diverted before it goes through the ufw firewall settings. Docker routes container traffic in the `nat` table, which means that packets are diverted before it reaches the `INPUT` and `OUTPUT` chains that ufw uses. Packets are routed before the firewall rules can be applied, effectively ignoring your firewall configuration.
Search this siteResults will appear as you typeClear
Start typing to search the documentation 
Give feedback
By clicking “Accept All Cookies”, you agree to the storing of cookies on your device to enhance site navigation, analyze site usage, and assist in our marketing efforts. 
Cookies Settings Reject All Accept All Cookies
## Privacy Preference Center
When you visit any website, it may store or retrieve information on your browser, mostly in the form of cookies. This information might be about you, your preferences or your device and is mostly used to make the site work as you expect it to. The information does not usually directly identify you, but it can give you a more personalized web experience. Because we respect your right to privacy, you can choose not to allow some types of cookies. Click on the different category headings to find out more and change our default settings. However, blocking some types of cookies may impact your experience of the site and the services we are able to offer. [More information](https://cookiepedia.co.uk/giving-consent-to-cookies)
Allow All
###  Manage Consent Preferences
#### Functional Cookies
Functional Cookies
These cookies enable the website to provide enhanced functionality and personalisation. They may be set by us or by third party providers whose services we have added to our pages. If you do not allow these cookies then some or all of these services may not function properly.
#### Strictly Necessary Cookies
Always Active
These cookies are necessary for the website to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the site will not then work. These cookies do not store any personally identifiable information.
#### Performance Cookies
Performance Cookies
These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. They help us to know which pages are the most and least popular and see how visitors move around the site. All information these cookies collect is aggregated and therefore anonymous. If you do not allow these cookies we will not know when you have visited our site, and will not be able to monitor its performance.
#### Targeting Cookies
Targeting Cookies
These cookies may be set through our site by our advertising partners. They may be used by those companies to build a profile of your interests and show you relevant adverts on other sites. They do not store directly personal information, but are based on uniquely identifying your browser and internet device. If you do not allow these cookies, you will experience less targeted advertising.
Back Button
### Cookie List
Search Icon
Filter Icon
Clear
checkbox label label
Apply Cancel
Consent Leg.Interest
checkbox label label
checkbox label label
checkbox label label
Reject All Confirm My Choices
