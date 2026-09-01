# 第 5 章：方案三 — hosts 与 gh-proxy 工具

前两章讲的代理和镜像，分别需要「一台可用代理」或「可信镜像源」。这一章给出两个零依赖、零成本的临时手段：改 hosts 把 GitHub 域名直接指向较快 IP，以及给 GitHub URL 加反代前缀的 gh-proxy。它们适合应急救急，但各有明确的时效与安全边界——读完这一章，你会知道什么时候能用、什么时候千万别用。

## 5.1 hosts 方案：GitHub520 原理与使用

### 原理：电话簿手动改号码

hosts 是操作系统自带的「域名 → IP」静态映射表，优先级高于 DNS 查询。GitHub520 的思路很简单：当域名解析被污染、或解析出的 IP 跨境链路差时，它提前测好一批「大陆直连速度较好」的 GitHub IP 写进 hosts，让本机跳过污染 DNS 直接连过去。[GitHub520](https://github.com/521xueweihan/GitHub520)（S14）

[!tip] 大白话
把 hosts 想成「电话簿手动改号码」：你按原电话号码（DNS 解析的 IP）拨过去总打不通或很卡，GitHub520 直接给你一本实测通畅的号码簿，把 GitHub 的号码手抄进去，以后拨号就不经过那个爱捣乱的查号台。所以改 hosts 只绕过了「查号」环节，并不能绕过线路本身的阻断。

### 数据源与 hosts 位置

GitHub520 的 hosts 内容托管在非 GitHub 域名上，**不依赖访问 GitHub 本身**：

```
数据源：https://raw.hellogithub.com/hosts
```

三种主流系统的 hosts 位置（S14）：

| 系统 | hosts 文件路径 |
|------|--------------|
| Windows | `C:\Windows\System32\drivers\etc\hosts` |
| Linux | `/etc/hosts` |
| macOS | `/etc/hosts` |

### 刷新 DNS 缓存

改完 hosts 后无需重启系统，但要让新映射立即生效，需刷新 DNS 缓存（S14）。

Windows（以管理员身份运行 cmd / PowerShell）：

```bash
ipconfig /flushdns
```

macOS：

```bash
sudo killall -HUP mDNSResponder
```

### macOS 一键命令与 SwitchHosts 自动更新

GitHub520 官方 README 提供 macOS 一键脚本（S14）。运行前建议先用 `curl` 预览 hosts 内容再执行：

```bash
curl https://raw.hellogithub.com/hosts   # 先预览，确认内容后再执行下方命令
sudo sh -c 'cd /etc; curl -L https://raw.hellogithub.com/hosts -o hosts; killall -HUP mDNSResponder'
```

手动改 hosts 的痛点是「GitHub 的 IP 会变」。GitHub520 推荐用跨平台工具 **SwitchHosts**：把 `https://raw.hellogithub.com/hosts` 配成远程源，客户端每小时自动拉取刷新，省去手工维护成本（S14）。

## 5.2 反代前缀：gh-proxy 用法与自部署

### 前缀用法：给 URL 加一段即可

gh-proxy 是反向代理项目：把 GitHub 的克隆/下载 URL 前面加一个代理前缀，流量先到代理服务器，由它替你访问 GitHub 再转回来。[gh-proxy](https://github.com/suiyueqingqian/gh-proxy)（S15）

克隆公开仓库时，把 `https://github.com/user/repo.git` 换成「前缀 + 原 URL」：

```bash
git clone https://gh.api.99988866.xyz/https://github.com/user/repo.git
```

### 公共实例的局限

公共代理实例免费开放，但有两个现实问题（S15）：

- **域名频繁变动**：公共实例域名随时可能更换，写进脚本很快失效；
- **演示站不堪重负**：免费实例被大量用户共用，速度和稳定性没保证。

结论：**偶尔手动用一次可以；大量使用或写进自动化脚本，建议自部署**。

### 自部署选项

gh-proxy 官方提供两个版本（S15）：

1. **CF Worker 版**：把项目里的 `worker.js` 粘到自己的 Cloudflare Workers，无需服务器；CF 免费版每天 10 万次请求，对个人使用通常足够。
2. **Python 版**：基于 Python，可用 Docker 一键部署到自己的服务器/VPS；Docker 镜像与启动命令以项目 README 的 `docker run` 说明为准，按其执行即可。

## 5.3 时效与安全风险

这一节是本章重点，**用前必读**。

**风险清单（S14、S15、[ipdodo](https://www.ipdodo.com/news/16580/) 的 S5）：**

1. **Token 泄露（最高危）**：私有仓库若用 `git clone https://user:TOKEN@gh-proxy...` 的方式，Token 会以明文经过第三方代理服务器传输，等于把仓库钥匙交给陌生人，**有泄露风险——绝对不要用公共 gh-proxy 实例克隆私有仓库**（S15）。
2. **hosts 服务器到期**：GitHub520 的数据服务器将于 **2026-12-31 到期**（续费靠赞助），该数据源可能在到期后停更（S14）。
3. **社区 IP 时效**：hosts 内容是社区实测 IP，可能随 GitHub 变更/更换 CDN 失效；失效时表现为「hosts 里明明写着这个 IP，连接却超时」（S5）。
4. **不适合自动化构建**：在服务器或 CI 里硬编码 hosts 后，IP 动态轮换会让配置几天内失效，维护成本高；gh-proxy 公共前缀同理会因域名变动而失效。**两者都不适合自动化构建**（S5、S15）。
5. **只绕 DNS，不绕线路**：hosts 只解决「解析到好 IP」；若该 IP 线路本身被限速或阻断，依然会超时（回顾第 2 章的 SNI 过滤机制）。

[!tip] 大白话
这两个方案本质是「熟人带路」：GitHub520 帮你抄好电话号码，gh-proxy 帮你去柜台代取快递。熟人靠谱时很快，但「代取快递」的中间人只要经手一次你的钥匙（Token），保险柜就再也不安全了——所以私有仓库的钥匙永远别交给代取的人。

## 本章小结

- hosts 方案（GitHub520）把 GitHub 域名手动解析到社区实测的较快 IP，数据源 `https://raw.hellogithub.com/hosts`，不依赖访问 GitHub；改完需刷新 DNS（Win `ipconfig /flushdns` / Mac `sudo killall -HUP mDNSResponder`），可用 SwitchHosts 远程源自动更新。
- gh-proxy 反代前缀把 `https://github.com/...` 换成 `https://gh.api.99988866.xyz/https://github.com/...`，公开仓库偶尔用可以；公共实例域名变动频繁、人多易慢，大量使用建议自部署 CF Worker 或 Python Docker 版。
- 高风险事项：私有仓库 Token 经第三方代理传输会泄露；hosts 服务器 2026-12-31 到期；社区 IP 会随 GitHub 变更失效；两者都不适合写进自动化构建。
- 下一章把这些手段放进 agent 场景：如何给拉包工具（含 docker daemon）统一配好网络。
