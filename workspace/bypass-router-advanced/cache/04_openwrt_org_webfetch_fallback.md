---
retrieved_at: 2026-09-23
method: WebFetch fallback (crawler blocked by Anubis proof-of-work challenge)
urls:
  - S5  https://openwrt.org/docs/guide-user/base-system/dhcp
  - S5a https://openwrt.org/docs/guide-user/base-system/dhcp_configuration
note: |
  crawl.sh 对 openwrt.org 返回 Anubis 反爬页面（见 01_openwrt_org.md / 02_openwrt_org.md，
  title="Testing to determine if you are a bot!"）。curl 直取与 DokuWiki _export/raw 端点同样被拦。
  因此改用 WebFetch 分两次独立检索，下列引号内文本为两次检索一致返回的内容。
  未取得页面完整快照，也未取得页面更新日期。
---

## S5 (dhcp) 返回内容

- dhcp_option 与 dnsmasq 的关系：
  - "The ID dhcp_option here must be with written with an underscore."
  - "OpenWrt will translate this to --dhcp-option, with a hyphen, as ultimately used by dnsmasq."
- dhcp_option_force 定义：
  - "Exactly the same as dhcp_option (note the underscores), but it will be translated to --dhcp-option-force"
  - "meaning that the DHCP option will be sent regardless on whether the client requested it."
  - "dhcp_option_force available since 18.06"
  - 该条目位于 "DHCP pools" 选项表中，类型 "list of strings"，非必填，默认 "_(none)_"。
- 选项号示例：'\"3,192.168.1.1 6,192.168.1.1\" to give out gateway and DNS server addresses'；
  另有 '26,1470' / 'option:mtu, 1470'。
- tag 机制：tag list 为 "List of tags that dnsmasq needs to match to use with --dhcp-range."；
  "you can use the dhcp_option list to add DHCP options to be sent to hosts with this tag (or networkid)."；
  "tag classifying sections have one configuration option: values of DHCP options to assign to this tag."
- IPv6/DNS：odhcpd 的 dns 选项 "Only IPv6 addresses are accepted. To configure IPv4 DNS servers, use dhcp_option."；
  dns_service 为 "Announce the IPv6 address of interface as DNS service if the list of dns option is empty."；
  dhcpv6 为 "Specifies whether DHCPv6 server should be enabled (server), relayed (relay) or disabled (disabled)."
- 页面未出现针对「IPv6 DNS 不能用 dhcp_option 下发」的明确表述。

## S5a (dhcp_configuration) 返回内容

- 示例（uci add_list 形式）：dhcp_option="3,192.168.1.2"；dhcp_option="6,172.16.60.64,172.16.60.65"；
  dhcp_option="42,172.16.60.64"；dhcp_option="44"。
- tag classifier："Use the tag classifier to create a tagged group."；
  "Assign individual DHCP options to hosts tagged with tag1."；
  uci set dhcp.tag1="tag"；uci set dhcp.tag1.dhcp_option="6,8.8.8.8,8.8.4.4"；uci set dhcp.@host[-1].tag="tag1"。
- MAC classifier：dhcp.mac1.dhcp_option="3"（"Disable default gateway"）与 dhcp.mac1.dhcp_option="6,192.168.1.3"。
- 两次检索均确认：该页不含 dhcp_option_force 一词；相近的只有 "Race conditions with netifd" 下的 dhcp.lan.force="1"，
  用于 "skip check for competing DHCP servers"（与 dhcp_option_force 不是同一机制）。
- IPv6 DNS 走 odhcpd：uci add_list dhcp.lan.dns="2001:4860:4860::8888"；
  uci set dhcp.lan.dns_service="0"；uci set dhcp.lan.ra_dns="0"。

## 交叉核对：OpenWrt dnsmasq init 脚本（一手源码）

来源：https://raw.githubusercontent.com/openwrt/openwrt/master/package/network/services/dnsmasq/files/dnsmasq.init
（openwrt/openwrt master，2026-09-23 取回，本地副本 /tmp/dnsmasq.init，1404 行）

行 688-694（dhcp_option_append）：
    xappend "--dhcp-option${force:+-force}=${networkid:+$networkid,}$option"

行 696-721（dhcp_option_add）：
    local opt="dhcp_option"
    [ "$force" = "0" ] && force=
    [ "$force" = "2" ] && opt="dhcp_option_force"

行 471-486（dhcp_tag_add，tag 段只读 dhcp_option + 布尔 force）：
    config_get_bool force "$cfg" force 0
    [ "$force" = "0" ] && force=
    config_get option "$cfg" dhcp_option
    for o in $option; do
        xappend "--dhcp-option${force:+-force}=tag:$tag,$o"
    done

行 667-674（IPv6 DNS 走 option6，不走 dhcp_option）：
    if [ -n "$dns" ]; then ... for d in $dns; do append dnss "[$d]" ","; done
    else dnss="[::]" fi
    dhcp_option_append "option6:dns-server,$dnss" "$networkid"
