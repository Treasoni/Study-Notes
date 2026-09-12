# 第 2 章 装插件并完成登录授权

这一章只做一件事：把 Tailscale 插件装进 HAOS，让你的 Home Assistant 出现在自己的 tailnet 里。全程在 HA 界面和 Tailscale 控制台点鼠标，不碰配置文件。装完它，第 3 章的远程访问才有前提。

### 2.1 开工前的准备

先注册 Tailscale 账号。官方文档写明它对个人与爱好项目免费，单用户账号最多 100 台客户端/设备，用 Google / Microsoft / GitHub 账号在 `tailscale.com/start` 注册即可 [^c2-1]。注册完你就有了一个 tailnet。

第二件事：装完记得去关掉这台设备的 key 过期。官方建议关闭它，避免和 Home Assistant 失联 [^c2-2]。等设备出现在控制台后就去关。不做的话，key 一到期设备会失联、路由随之失效，fail-close 现场见第 7 章 7.4.1 节。

第三件事：顺手把 tailnet 名改好。默认名字长这样 `tail6e5bf.ts.net`，难记也难打；在控制台点 DNS → Rename tailnet，重摇到顺眼为止，同时确认 MagicDNS 与 HTTPS Certificates 已开启 [^c2-3]。第 3 章的 Serve 要用到这个域名和证书。

> [!tip] 大白话
> 把 tailnet 想成你自己的小区：只有被你拉进来的设备才能进院子串门，外面看不到院里的门牌。「登录授权」就是给 Home Assistant 发一张门禁卡；关掉 key 过期，是让这张卡不要到期作废。

### 2.2 在 HA 应用商店里安装

在 HA 里点左下角 Settings → Apps（旧版本叫 Add-ons，HA 2026.8 起更名），再点右下角 Install app，搜索 Tailscale，选中后点 Install [^c2-4]。

这里必须确认你装的是哪一个——这个主题的教程互相矛盾，多半是因为存在两套插件。本笔记操作的是插件 ID `a0d7b954_tailscale`，来自仓库 `hassio-addons/repository`，维护者是 Home Assistant 核心开发者 Franck Nijhof（frenck）[^c2-1]。它的文档自称 Home Assistant Community App: Tailscale。

> [!warning] 别装错，也别照抄
> 另有一套 `hass-tailscale/hass-addons`（要你填 `auth_key` 的那套）已经废弃。这里只作背景说明，**不构成操作指引、你不需要照它做**：认识它长什么样就够了，看到 `auth_key` 字样的教程直接跳过。

### 2.3 启动并完成登录授权

回到 Apps 菜单，点 Tailscale → Info → Start [^c2-4]。官方步骤是先 Start、再看日志确认没报错，然后才授权 [^c2-1]。接着点 Open Web UI 完成登录授权，把 Home Assistant 挂到你的 tailnet 上；这一步会弹出登录页，需要允许弹窗并确认接入 [^c2-4]。

> [!warning] 不是所有浏览器都能完成这一步
> 官方原文：Some browsers don't work with this step. It is recommended to complete this step on a desktop or laptop computer using the Chrome browser.
> 照做就是：找一台桌面或笔记本，用 Chrome。在手机浏览器上卡住，不是你的问题。

顺手可以打开 Watchdog、Auto update；Show in sidebar 可选，官方说它没那么必要 [^c2-4]。

### 2.4 确认上线，以及一个会浪费你半天的坑

回到控制台 Machines 页，应该能看到一台名为 `homeassistant` 的设备，旁边绿点表示已连接 [^c2-4]。看到绿点，这一章就过关。

那个坑在这里。插件后台 Web UI 里也能看到一部分配置项，但官方文档明确写着：这些选项在 Web UI 里是只读的，你改不动，因为所有在 Web UI 上做的改动都会在插件重启后丢失 [^c2-1]。所以**要改配置，只能改插件自己的 YAML**。记住这一点——它直接决定了第 4 章的配置方式，别指望在后台界面上把 `advertise_routes` 点出来。

> [!warning] 界面上显示的值，不等于实际生效的值
> 还有一类已知现象：有人在插件界面看到的值和实际生效的行为对不上。这不是错觉——插件的部分默认值在历史上发生过翻转，网上 2023–2024 年的教程大量基于旧默认值，与当前文档写的不一致 [^c2-1]。所以别背版本号、别信旧教程：以你装完那一刻配置页显示的值，加上第 5.3 节那条校验命令来判断。

**本章小结**

- 三件准备：注册 Tailscale 账号、装完关掉该节点 key 过期（见 7.4.1）、把 tailnet 改成好记的名字（第 3 章 Serve 要用）。
- 认准插件：ID `a0d7b954_tailscale`、仓库 `hassio-addons/repository`、维护者 frenck；`hass-tailscale/hass-addons` 已废弃，别照它做。
- 顺序是 Install → Start → Open Web UI 授权；授权用桌面 Chrome。
- 后台 Web UI 的配置项只读、重启即丢，改配置只能改插件 YAML。
- 控制台 Machines 里出现 `homeassistant` 加绿点，才算授权成功。

下一章不再碰安装界面：直接用刚挂上 tailnet 的这台 HAOS，从外网打开 Home Assistant。

[^c2-1]: [hassio-addons/app-tailscale DOCS.md](https://github.com/hassio-addons/app-tailscale)（本地缓存 `sources/08_raw_githubusercontent_com.md`）
[^c2-2]: 同 [^c2-1]，`## Configuration` 首段
[^c2-3]: [Remotely access Home Assistant via Tailscale for free](https://tailscale.com/blog/remotely-access-home-assistant)（本地缓存 `sources/11_tailscale_com.md`）
[^c2-4]: 同 [^c2-3]
