# 第 5 章 在远程客户端上接收路由

第 4 章你在 HAOS 侧 advertise 了 `192.168.1.0/24`、又在管理端勾了授权，但路由要真正进入你手机或笔记本的路由表，客户端这端也得点头。本章三件事：四个条件、Linux 例外、一条自证命令。

## 5.1 路由注入的四个条件

官方文档把「路由什么时候被注入客户端路由表」写得很清楚，必须同时满足四条：

1. **子路由节点 advertise**：节点用 `--advertise-routes` 声明它能到哪些网段，对应第 4 章的 `advertise_routes`。
2. **管理员 approve**：在管理控制台授权，或用 tailnet policy file 里的 `autoApprovers`。
3. **控制面分发**：授权通过后，控制面才把这条路由放进下发给客户端的 network map。
4. **客户端 accept**：客户端必须开启接受子路由。

四条是「与」的关系，缺哪一条，现象都是同一句「配了没生效」。顺带一条：客户端不会 ping 路由器来发现路由，路由是 advertise + approve 后从 network map 收到的。

> [!tip] 大白话
> 把路由想成新开一条公交线：① 车队申报要开，② 交管局（管理端）批，③ 印到站牌（network map）发到各站，④ 乘客（客户端）还得愿意上车。缺一步，你都会觉得「这线路配了等于没有」。

> [!warning] ACL / grants 不会注入路由
> 官方点名的常见误解：grants 和 ACLs **不**控制路由注入，它们只管包过滤。于是两种半吊子状态都不通——**有路由没 ACL**：包进了隧道被过滤器丢掉；**有 ACL 没路由**：包根本没进隧道。两者都要有才端到端通。第 7.3 节会再展开，这里先记住「路由和 ACL 是两套东西」。

## 5.2 各平台默认值不一样，Linux 最容易踩

第 4 条「客户端 accept」的默认值，各平台并不一致：

- Windows、macOS、Android、iOS、tvOS **默认接受**子路由；
- **Linux 默认不接受**，要显式执行 `tailscale set --accept-routes`。

> [!tip] 大白话
> 同一份快递，手机和 Mac 默认放前台，Linux 默认放驿站——不特别交代一声，它不会送上来。

这就解释了一个高频困惑：同一套 HAOS 配置，**手机一配就通、Linux 服务器死活不通**。先别怀疑 HAOS，多半是踩到了 Linux 的默认值。

## 5.3 客户端上怎么打开，以及那条校验命令

图形界面里对应的开关叫 **Use Tailscale subnets**，取消勾选就是「忽略 advertise 过来的路由」，即不接受。命令行等价操作：

```bash
# 接受子路由（Linux 默认关闭，需显式打开）
tailscale set --accept-routes

# 反过来：不接受
tailscale set --accept-routes=false
```

想确认是否生效，用官方校验命令：

```bash
# 看 RouteAll 是否为 true
tailscale debug prefs
```

为 `true` 说明这台客户端确实在接受子路由；为 `false` 就照第一条命令打开。

> [!tip] 大白话
> 第 1 章 1.4 节提醒过你：别背版本号、别信二手教程，要「以你配置页此刻的实际值为准」。`tailscale debug prefs` 的 `RouteAll` 就是这句话的兑现方式——界面显示和文档都不算数，这台机器实际生效的值才算；第 2.4 节说的界面与实际不一致，也靠它判定。

**本章小结**

- 路由注入四条缺一不可：advertise、approve、控制面下发、客户端 accept。
- ACL / grants 不注入路由，只管包过滤；有路由没 ACL、有 ACL 没路由，两种都不通。
- 默认值分平台：Windows / macOS / Android / iOS / tvOS 默认接受，Linux 默认不接受。
- 图形界面看 `Use Tailscale subnets`，命令行用 `tailscale set --accept-routes`（关闭加 `=false`），校验看 `tailscale debug prefs` 的 `RouteAll`。

配置齐了不等于通了。第 6 章把前面环节串成一份六步验收清单，你亲自跑一遍并记下结果。
