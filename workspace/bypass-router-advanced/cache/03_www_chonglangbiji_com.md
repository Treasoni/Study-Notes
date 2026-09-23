---
url: "https://www.chonglangbiji.com/guide/openwrt-bypass-router-gateway-dns-transparent-proxy-2026/"
title: "OpenWrt 旁路由新手教程：网关、DNS、DHCP 和透明代理 2026 | 排查清单 | 冲浪笔记"
scraped_at: 2026-09-23T06:05:30+00:00
---

OpenWrt 旁路由的核心是让客户端把网关或 DNS 指向旁路由，同时保持主路由负责拨号和上网。新手建议先固定旁路由 LAN IP，关闭旁路由 DHCP；再在主路由 DHCP 中下发网关和 DNS；确认普通上网正常后，最后开启透明代理插件。
## 适用场景与不适用场景
适用：
  * 主路由已经能正常上网，想加一台 OpenWrt / iStoreOS 做旁路由。
  * 电视、游戏主机、NAS 等设备不方便单独装客户端。
  * 想理解网关、DNS、DHCP 与透明代理的关系。


不适用：
  * OpenWrt 作为主路由拨号，这篇只讲旁路由。
  * 你要做复杂多 VLAN、企业网络或多出口负载。
  * 你的主路由无法修改 DHCP 选项，可能需要手动给设备设置网关/DNS。


## 拓扑先画清楚  
| 角色  | 示例地址  | 职责  | 新手建议  |  
| --- | --- | --- | --- |  
| 主路由  | `192.168.1.1`  | 拨号、NAT、DHCP  | 保持不变  |  
| OpenWrt 旁路由  | `192.168.1.2`  | DNS、透明代理、规则分流  | 固定 LAN IP  |  
| 客户端  | `192.168.1.x`  | 手机、电脑、电视、NAS  | 先挑一台测试  |  
旁路由最容易错在 DHCP。网络里同时出现两个 DHCP 服务时，客户端可能拿到随机网关，表现为有时能上网、有时不行。
## 第 1 步：固定旁路由 LAN IP
进入 OpenWrt 的 LAN 接口设置：
  1. 设置旁路由 IP 为主路由同网段未占用地址，例如 `192.168.1.2`。
  2. 子网掩码与主路由一致。
  3. 默认网关填主路由地址，例如 `192.168.1.1`。
  4. DNS 可以先填主路由或可信公共 DNS，后续再交给插件。
  5. 保存后重新用新地址登录 LuCI。


## 第 2 步：关闭旁路由 DHCP
在 OpenWrt LAN 的 DHCP 设置中勾选忽略接口，或明确关闭 DHCP 服务。主路由继续分配地址，避免客户端随机拿到旁路由地址池。
如果你必须让旁路由接管 DHCP，要确保主路由 DHCP 关闭，并且旁路由下发的网关、DNS、租期都正确。新手不建议一开始就这样做。
## 第 3 步：选择网关方案还是 DNS 方案  
| 方案  | 客户端网关  | 客户端 DNS  | 适合场景  | 注意点  |  
| --- | --- | --- | --- | --- |  
| 网关指向旁路由  | 旁路由 IP  | 旁路由 IP 或指定 DNS  | 想让设备流量统一经过旁路由  | 旁路由故障会影响测试设备上网  |  
| 只改 DNS  | 主路由 IP  | 旁路由 IP  | 只想先验证 DNS 分流  | 不是所有流量都会进旁路由  |  
| 手动单设备  | 单台设备手动设置  | 单台设备手动设置  | 小范围测试  | 不影响全家设备  |  
建议先只改一台电脑或手机，确认没有问题后，再通过主路由 DHCP 下发给更多设备。
## 第 4 步：开启透明代理前的检查
在安装或开启 OpenClash、PassWall、luci-app-mihomo 前，先验证：
  1. 测试设备能打开主路由管理页。
  2. 测试设备能打开旁路由 LuCI。
  3. NAS、打印机、电视投屏等内网服务可访问。
  4. 普通网页可打开。
  5. 旁路由重启后，测试设备不会丢网关或 DNS。


需要多端共用订阅时，可以准备多格式测试订阅源，但插件导入前确认 OpenWrt 基础网络是通的。
## 验证是否成功
  * 客户端 IP、网关、DNS 与预期一致。
  * `192.168.1.1` 和 `192.168.1.2` 都能打开。
  * OpenWrt 系统日志没有 DHCP 冲突提示。
  * 开启插件后，日志能看到测试设备请求。
  * 关闭插件后，内网访问仍正常，说明基础网络没有被破坏。


## 相关阅读
  * [OpenWrt dnsmasq 与 Mihomo 顺序](https://www.chonglangbiji.com/guide/openwrt-dnsmasq-mihomo-order-2026/)
  * [OpenWrt Mihomo DNS 泄漏排查](https://www.chonglangbiji.com/guide/openwrt-mihomo-dns-leak-fix-2026/)
  * [OpenWrt / iStoreOS 订阅导入失败排查](https://www.chonglangbiji.com/guide/openwrt-passwall-openclash-subscription-import-checklist-2026/)
  * [路由器 VPN 全屋流媒体配置](https://www.taojichang.com/devices/router-vpn-full-home-streaming/)


## 旁路由常见故障速查
记一个排查原则：不要把订阅、DNS、规则分流和系统代理混在一起排查。先固定变量，只看一层。  
| 现象  | 优先检查  | 验证方式  |  
| --- | --- | --- |  
| 订阅导入失败  | URL、User-Agent、证书、订阅格式  | 浏览器打开订阅地址，看客户端日志  |  
| 节点全红  | 订阅是否过期、DNS、时间、出口端口  | 换同订阅另一个客户端对照  |  
| 开了代理没网  | 系统代理、TUN、路由表、DNS  | 先测 IP，再测域名  |  
| 电视和 NAS 不走代理  | 网关、旁路由、DHCP、分流规则  | 用同一域名做设备对照  |  
## 常见问题 旁路由一定要关闭 DHCP 吗？
    新手建议关闭旁路由 DHCP，让主路由统一分配地址。只有明确知道两台设备如何分工时，才考虑旁路由接管 DHCP。 网关和 DNS 都要指向旁路由吗？
    取决于方案。全流量经过旁路由通常会下发旁路由网关；只做 DNS 分流时可能只改 DNS。新手不要两种方案混着改。 旁路由配置后内网 NAS 打不开怎么办？
    检查客户端网关、子网掩码和防火墙区域，确认私有网段没有被透明代理或规则错误接管。 透明代理插件应该什么时候开？
    等 DHCP、网关、DNS 和普通上网都验证通过后再开。否则很难分清是基础网络问题还是插件问题。
## 参考来源
最后查看：2026-05-21
  * [OpenWrt Network User Guide](https://openwrt.org/docs/guide-user/network/start)
  * [OpenWrt DHCP Configuration](https://openwrt.org/docs/guide-user/base-system/dhcp)
  * [OpenWrt dnsmasq and DHCP Documentation](https://openwrt.org/docs/guide-user/base-system/dhcp.dnsmasq)
  * [OpenWrt Firewall Configuration](https://openwrt.org/docs/guide-user/firewall/firewall_configuration)


