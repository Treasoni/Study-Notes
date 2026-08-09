# 第五章：HACS 首次配置与常用仓库实战

第四章我们成功把 HACS 装进了 Docker 版 HA，重启后它就在后台静静等待。这一章我们把它「唤醒」：走通 HACS 3.x 首次配置全流程，完成 GitHub 授权，装上一批高频使用的卡片和集成，并学会快速定位最常见的报错。

## 5.1 先确认 HACS 真的加载了

重启 HA 后，打开「设置 → 设备与服务」，点右上角「+ 添加集成」，在搜索框输入 `HACS`。能搜到就直接进入 5.2；搜不到，多半是浏览器缓存了旧页面——按 `Ctrl+F5` 强制刷新（Mac 用 `Cmd+Shift+R`）再试一次。[Source: HACS 3.x 首次配置流程](https://www.hacs.xyz/)

[!tip] 大白话：清缓存
把浏览器想成一位「记性太好的前台」。你换了房间号（HACS 装好了），它还按老房间指路。`Ctrl+F5` 就是拍它一下：「忘掉旧记忆，重新看」。所以新装集成后搜不到，先强刷，再排查其他问题。

## 5.2 HACS 3.x 首次配置完整流程

确认能搜到 HACS 后，按下面的顺序走（全程约 5 分钟）：

1. **添加集成**：点「+ 添加集成」→ 搜 `HACS` → 点击进入。
2. **勾选声明**：HACS 会弹出使用条款与免责声明，**全部勾选**后点 `Submit`。不勾全无法继续。
3. **Device flow 授权**：页面显示一个**设备代码**（形如 `ABCD-1234`）。复制它，另开标签页访问 `https://github.com/login/device`，粘贴代码，点 Authorize 授权 HACS 读取你的 GitHub 账号。**注意：代码 15 分钟有效**，超时需重新生成。[Source: HACS 首次配置 Device flow](https://www.hacs.xyz/)
4. **回到 HA**：授权完成后回到 HA 页面，点 `Submit`，等待几秒验证。
5. **分配区域**：选一个区域（如「家庭」）或不分配，点 `Finish`。

完成后左侧边栏会出现 HACS 入口。「搜索」就是社区仓库的入口，后面装卡片和集成都靠它。

[!tip] 大白话：Device flow
Device flow 就像「扫码登录」：GitHub 不给你账号密码，而是给一张一次性的「验证码」（设备代码），你去 GitHub 官网输入验证码，确认「我同意这台设备读我的仓库」。15 分钟有效，就像验证码短信会过期。好处是你全程不把密码交给 HA；只有你亲自授权，HACS 才能替你下载社区仓库。

## 5.3 国内「两段论」：下载可加速，授权必须直连

国内环境用 HACS 有一条铁律，记住它排障快一半：

- **下载/更新阶段可以加速**：第四章配置的 gh-proxy 前缀、hacs-china 极速版、HACS 3.x「选项」里填的 GitHub API 代理，都作用在这一段。
- **首次授权必须直连 GitHub**：Device flow 走的是 `github.com/login/device`，没有任何代理能替你做授权。这是账号安全边界，绕不开。所以先决条件就一条：首次授权时网络必须能直连 GitHub（开全局代理，或临时切到可直连网络）。授权完成后，日常下载、更新走代理即可，不必常开。

[!tip] 大白话：两段论
把 HACS 想成「让你在 GitHub 商店自助提货」。提货（下载文件）可以找快递代理帮你拿；但「验明正身」（授权）必须你本人到场。所以下载失败可以怪网络，授权转圈只能怪自己没直连。

## 5.4 高频报错定位

授权和首次加载最容易踩的坑，集中在下表：

| 报错现象 | 原因 | 处理 |
|---|---|---|
| `Timeout of 20 reached while waiting for...` | 网络/DNS 不通 GitHub | 检查科学上网或 DNS，重试 |
| 列表加载失败 / token 失败 | `api.github.com` 被墙 | HACS「选项」里填 GitHub API 代理（如 `ghapi.hacs.vip/api`）|
| 授权一直转圈 | 未直连 github.com | 开启全局直连，再走一遍 Device flow |
| 搜不到 HACS | 浏览器缓存旧页面 | `Ctrl+F5` 强刷缓存 |
| 下载/更新失败 | 下载源被墙或代理失效 | 换 gh-proxy 前缀（ghproxy.com 已死，改用 gh-proxy.com）|

> 来源：方向 B4 报错说明与 B6 国内高频坑。[Source: HACS 国内环境高频问题](https://www.hacs.xyz/)

## 5.5 常用仓库清单

生态就绪后，下面这些是社区口碑最好、最值得先装的仓库。装法统一：HACS → 搜索仓库名 → 下载 → 重启 HA（集成类）或刷新页面（前端卡片类）。

| 类别 | 名称 | GitHub 仓库 | 用途 |
|---|---|---|---|
| 前端卡片 | Mushroom Cards | `piitaya/lovelace-mushroom` | 现代化仪表盘卡片，触控友好，替代默认卡片 |
| 前端卡片 | Mini Media Player | `piitaya/mini-media-player` | 紧凑型媒体播放器卡片 |
| 前端卡片 | Card Mod | `thomasloven/lovelace-card-mod` | 用 CSS 微调任意卡片样式 |
| 集成 | Xiaomi Miot Auto | `al-one/hass-xiaomi-miot` | 米家设备接入（走 MIoT 协议）|
| 集成 | browser_mod | `thomasloven/hass-browser_mod` | 让浏览器页面变成可控制实体 |
| 集成 | Xiaomi Gateway3 | `AlexxIT/XiaomiGateway3` | 小米多模网关接入（Zigbee/蓝牙）|
| 主题 | Glassmorphism | `reputasyon/glassmorphism-ha` | 毛玻璃质感主题 |
| 主题 | Mushroom Themes | `piitaya/lovelace-mushroom-themes` | 与 Mushroom 卡片配套的主题 |

> 来源：方向 B5 常用仓库清单。

以安装 Mushroom Cards 为例：HACS → 搜索 `Mushroom` → 结果里选 `Mushroom Cards` → 点「下载」确认版本 → 回到仪表盘编辑模式，点「添加卡片」，搜索 `Mushroom` 就能看到一整套新卡片。注意两类仓库的生效时机不同：**前端卡片无需重启**，下载完刷新页面即用；**集成类（如 Xiaomi Miot Auto）需要重启 HA**，之后才会出现在「设置 → 设备与服务 → 添加集成」的搜索结果里。

若某仓库下载后找不到实体，先回 HACS 确认它是否属于「前端卡片 / 主题 / 集成」哪一类，再按对应路径去配置——多数「装不上」其实是找错了入口。

## 本章小结

- HACS 首次配置五步走：加集成 → 勾声明 → Device flow 授权 → 回 HA 确认 → 分配区域。
- Device flow 是安全设计：验证码 15 分钟有效，全程不把 GitHub 密码交给 HA。
- 国内铁律「两段论」：下载/更新可加速，首次授权必须直连 GitHub。
- 报错先看现象定位：超时查网络、列表失败换 API 代理、转圈查直连。
- 常用仓库按需装：卡片类刷新即用，集成类需重启后配置。

生态已经就绪，接下来进入「稳定运行」主题。第六章先解决最基础也最关键的一环：版本锁定与镜像加速策略——让 HA 别再在 `stable` 浮动标签上「随波逐流」。
