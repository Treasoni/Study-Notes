## 第 4 章 初始化 iStoreOS 并访问后台

虚拟机创建完成只是第一步——iStoreOS 此时还只是一张未启动的系统盘。本章接通最后一段：开机、通过 VNC 看到命令行、用 `quickstart` 初始化到你的局域网，最后用浏览器进入后台。

### 4.1 开机与 VNC 连接

在飞牛 fnOS 虚拟机列表里选中刚创建的 iStoreOS 虚拟机，启动后用 **VNC** 连接访问控制台 [飞牛虚拟机部署 iStoreOS 做旁路由教程（S8）](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481)。首次启动需等待自动安装镜像，看到提示后敲一次回车即可。

> [!tip] 大白话：VNC 黑屏
> 把 VNC 想成「给虚拟机插了一块屏幕」。屏幕黑着不代表机器没开机——只要系统能通过 IP 提供服务，就说明它活着。VNC 黑屏但 IP 可访问时，直接改用浏览器访问，属正常现象 [S8 回帖]。

### 4.2 quickstart 初始化并修改 LAN IP

进入命令行后输入 `quickstart` 回车，或输入 `qu` 再按 Tab 自动补全 [飞牛虚拟机部署 iStoreOS 做旁路由教程（S8）](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481) [x86 物理机安装 iStoreOS（S3）](https://doc.istoreos.com/zh/guide/istoreos/install_x86.html)：

```bash
quickstart
```

按键盘下键选择 **Change LAN IP** 回车，然后依次输入：
1. 局域网里未被占用的静态 IP，回车；
2. 子网掩码，回车。

设置完成即可正常访问后台 [S8]。

> [!tip] 大白话：Change LAN IP
> 默认 LAN IP 相当于出厂门牌号，和你家小区（网段）对不上。Change LAN IP 就是「换一个自家小区里没人占用的门牌号」，换完邻居设备才找得到它。

### 4.3 浏览器访问后台与默认账号

浏览器输入刚设置的静态 IP 即可进入后台 [S8]。默认账号 `root`、密码 `password` [飞牛虚拟机部署 iStoreOS 做旁路由教程（S8）](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481) [x86 物理机安装 iStoreOS（S3）](https://doc.istoreos.com/zh/guide/istoreos/install_x86.html)。

> [!warning] 默认密码跨版本有差异
> 部分固件初始未设密码，首次登录时直接设置管理员密码 [飞牛 fnOS 安装 iStoreOS（S9）](https://blog.csdn.net/u013262414/article/details/155347617)。默认密码、固件文件名等一律「以官方最新页面为准」。

> [!tip] 大白话：root/password
> 把它想成新设备出厂配的「万能钥匙」。多数固件统一发 root/password 这把钥匙；个别版本换了锁（未设密码等）。开不了门就先查官方最新说明。

### 4.4 中文化设置

后台显示英文、没有中文选项时，在终端执行三条命令修复 [S8 回帖]：

```bash
uci set luci.languages.zh_cn='中文 (Chinese)'
uci set luci.main.lang='zh_cn'
uci commit luci
```

> [!tip] 大白话：uci
> uci 是 iStoreOS/OpenWrt 的「配置记事本」。三条命令等于写下「启用中文、默认中文」并保存，最后一行 `uci commit luci` 是「落笔生效」，漏了它配置不会保存。

### 本章小结

- 启动虚拟机后用 VNC 连接，首次启动等待自动安装、按提示敲回车。
- VNC 黑屏但 IP 可访问属正常现象，改用浏览器访问。
- 用 `quickstart`（或 `qu` + Tab）选 Change LAN IP，设置未被占用的静态 IP 与子网掩码。
- 浏览器访问该 IP，默认账号 `root` / 密码 `password`，跨版本差异以官方最新为准。
- 界面为英文时，用三条 `uci` 命令启用并切换到中文。
