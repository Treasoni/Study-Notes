---
url: "https://blog.openyq.top/posts/23739/"
title: "Mihomo Magisk 模块使用心得 - YQ's Toy Box"
scraped_at: 2026-09-23T06:08:26+00:00
---

# Mihomo Magisk 模块使用心得
本文最后更新于 6 个月前
##  1. 现有 Magisk 代理方案对比
目前，实现 Magisk 模块运行原生 Clash 内核的项目主要有两个：Box4Magisk 和 Box for Root，两者各有优劣。前者作者是 singbox 的协作者，技术能力强；后者在前者项目的基础上进一步完善，添加了订阅等功能，目录结构更加清晰。
两个模块都支持多种模式的透明代理，包括 TProxy、Redirect、TUN 以及一些混合模式如 TProxy+TUN 等（用于分开处理 TCP/UDP）
  * TProxy 是最佳选择，拥有 Linux 内核支持，性能优异，协议支持全面，可以考虑优先使用
  * Redirect 是以类似 NAT 的方式转发数据包，且不支持 UDP，个人不倾向于使用
  * TUN 则是 mihomo 内核原生支持的机制，和 TProxy 类似，不过其工作在第三层。在配置文件中开启 gso 后性能应该与 TProxy 差异不大。


两个模块都支持应用的黑 / 白名单机制，可以在模块设置中填写黑 / 白名单包名。
相较于官方的 CMFA 安卓客户端，Box 模块有一定的优势，主要是在性能方面略优、耗电相对较低，且配置自由度高。客户端的优势是服务启停、切换节点和看日志相对方便，配置起来也不用花什么心思。
##  2. 模块配置经验
模块的黑 / 白名单机制只能配合梯子的 `redir-host` 模式使用，在 `fake-ip` 下不支持。原因如下：
> 安卓应用的 DNS 最终由 netd 负责，tproxy 模式的黑白名单由 iptables uid 扩展匹配进行黑名单应用的 DNS 仍会被 box 核心劫持返回 fakeip，所以黑名单无法上网，使用 singbox 的 dns rule 控制黑名单应用域名返回非 fakeip dns 可以缓解上述问题，mihomo 可以考虑使用 fake-ip-filter，目前该字段已支持 规则集合而不止单域名写法
> —— [Issue #74 · CHIZI-0618/box4magisk (github.com)](https://github.com/CHIZI-0618/box4magisk/issues/74)
笔者由于倾向于使用 `fake-ip` 模式，因此采用 TUN 模式运行内核，启用 `fake-ip`，并通过在 Mihomo 配置文件中添加 `include-package` 条目来实现原生的包名白名单。
示例配置：

```
find-process-mode: always
...
tun:
  enable: true
  stack: system
  device: tun1
  dns-hijack:
    - "0.0.0.0:53"
    - "tcp://0.0.0.0:53"
  auto-detect-interface: true   # 自动识别出口网卡
  strict-route: true            # 严格路由模式
  gso: true                     # 启用通用分段卸载（仅Linux）
  auto-route: true              # 自动配置路由表
  # 安卓代理包名白名单
  include-package:
    - "com.microsoft.office.outlook"
    - "com.android.vending"
    - "com.openai.chatgpt"
    - "com.github.android"
    - ......

YAML

```

这样在同步配置文件的时候，安卓包名白名单也可以被一起同步过去。
Mihomo Magisk 模块使用心得
https://blog.openyq.top/posts/23739/
作者
yqs112358
[ Tailscale Taildrop 部分源码阅读记录 上一篇](https://blog.openyq.top/posts/22700/ "Tailscale Taildrop 部分源码阅读记录")[docker-compose 快速禁用特定 service 下一篇 ](https://blog.openyq.top/posts/25925/ "docker-compose 快速禁用特定 service")
