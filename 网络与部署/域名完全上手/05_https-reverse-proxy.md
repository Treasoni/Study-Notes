---
title: "第5章 把域名接上 HTTPS——Caddy 与 Nginx+certbot 反向代理实战"
tags:
  - 学习
  - 网络
  - HTTPS
  - 反向代理
created: 2026-09-04
updated: 2026-09-04
status: 已完成
source_project: domain-name-learning
---

> [!abstract] 本章导航
> [[04_dns-hosting-security|← 第4章 解析托管与域名安全]]  ·  [[域名完全上手|📖 返回目录]]  ·  [[06_no-public-ip|第6章 无公网 IP 接入 →]]

# 第5章 把域名接上 HTTPS——Caddy 与 Nginx+certbot 反向代理实战

域名已经解析到服务器（第 4 章收尾的地方），但浏览器地址栏还挂着「不安全」。本章解决最后一公里：让自有域名以 HTTPS 提供服务，并让证书自己续期，不再手动折腾。按「场景判断 → 证书签发原理 → Caddy 极简落地 → 通配与测试 → Nginx+certbot → 续期」推进；前提是你有一台**有公网 IP** 的服务器、一个 A 记录已指向它的域名，以及一点 Nginx/Docker 反向代理基础。

## 5.1 场景判断：你的条件适合走哪条路

本方案要两样东西：**有公网 IP** + **自有域名**。因为 HTTPS 证书的签发前提是「CA 能通过公网访问到你、证明你控制这个域名」；Caddy/certbot 官方文档对自动 HTTPS 给出的触发条件也建立在这两点上。[^c5-1]

- **有公网 IP、80/443 可直连**：走本章，Caddy 或 Nginx+certbot 二选一，最省心。
- **没有公网 IP，或运营商封了 80/443、不方便开入站端口**：先读 5.2/5.3 建立证书心智模型，再跳到第 6 章。Cloudflare Tunnel、frp+Caddy、Tailscale Funnel 都是「出站连接换入站端口」的思路，不依赖公网 IP。[^c5-1]

> [!tip] 大白话：CA 就是一位「线上验房师」
> 把证书颁发机构（CA）想成一位线上验房师。它不关心你房子的装修（业务代码），只验证一件事——**这间房确实登记在你名下**。验证通过，它发一张写着你名字的门牌（证书）。浏览器看到门牌才肯亮绿锁。所以本章所有操作的本质，都是「怎么向验房师证明域名是你的」。

## 5.2 HTTPS 与证书签发：ACME 三种「控域证明」

HTTPS = HTTP 跑在 TLS 加密通道上，服务器还要出示一张 CA 签发的证书，证明「我是 example.com」。Let's Encrypt（LE）是最常用的免费 CA，ACME 是它和客户端（Caddy/certbot）对话的自动签发协议。签发全程的难点不是加密算法，而是**域控制验证（challenge）**——CA 得先确认你确实控制这个域名。验证方式分三种，区别只在「CA 去哪里查证据」：[^c5-1]

- **HTTP-01（走 80 端口）**：CA 访问 `http://你的域名/.well-known/acme-challenge/<token>`，能读到约定内容，就证明你控制该域、且该域指向这台服务器。前提是 80 公网可达。
- **TLS-ALPN（走 443 端口）**：同一思路，把验证放进 TLS 握手阶段完成，前提是 443 公网可达。
- **DNS-01（走 DNS，不开端口）**：你到 DNS 托管商给 `_acme-challenge.你的域名` 加一条指定 TXT 记录，CA 去公共 DNS 查询核对。它不需要任何入站端口，因此是**通配符证书唯一可行的验证方式**。

Caddy 把这些封装成「自动 HTTPS」：遇到公网域名自动向 LE/ZeroSSL 签证书、到期前自动续期、默认把 80 端口的访问 301 到 443；遇到 `localhost`、内网 IP 这类本地名，则用自建本地 CA，不去打扰公网 CA。[^c5-1]

> [!tip] 大白话：HTTP-01 = 往你家门口信箱投一封验证信
> 验房师要确认「这台服务器归你管」，就往 80 端口这扇「信箱」投一封信（token），谁能取出来回信，谁就控制这个域名对应的机器。所以**信箱（80 端口）必须能被外面投递到**，这就是「HTTP-01 要求 80 公网可达」的原因。

> [!tip] 大白话：DNS-01 = 在单位公告栏贴一张指定告示
> 验房师不进你办公室，只去「DNS 公告栏」看：你在托管商后台的 `_acme-challenge` 记录上贴了指定内容的 TXT 告示，他就认。因为公告栏管着整个域，**不用开任何服务器端口**——代价是你要能登录 DNS 托管商后台、或给它 API 凭据让程序替你贴。

## 5.3 Caddy 最小反向代理

假设服务已跑在 `127.0.0.1:8080`（Docker 容器 `-p 127.0.0.1:8080:8080` 映射到本机同理）。先看完整的 Caddyfile，只有几行：

```caddyfile
# /etc/caddy/Caddyfile
example.com {
	reverse_proxy 127.0.0.1:8080
}
```

拆开讲：

- `example.com` 是**站点地址**，换成你自己的域名。Caddy 看到配置里出现域名，就会启动自动 HTTPS。
- `reverse_proxy 127.0.0.1:8080` 把收到的请求反代给本机 8080 端口——你已有的 Nginx/Docker 反代经验在这里直接平移。想再加一个服务，就再写一个站点块（换域名、换端口）。

保存后 `systemctl reload caddy`（或容器编排里的 reload）即可。Caddy 自动完成：申请证书 → 监听 443 → 80 跳 443 → 到期续期，全程无需你碰证书文件。

但自动 HTTPS 不是魔法。Caddy 官方文档明确给了三个触发条件，缺一个就签不下来：[^c5-1]

1. 域名的 A/AAAA 记录已指向本机（第 4 章用 `dig` 验证过的那步）；
2. 80 与 443 公网可达（HTTP-01/TLS-ALPN 要访问得到）；
3. 配置里确实写了这个域名，而不是裸 IP。

> [!warning] HTTP-01 要求 80 公网可达
> CA 是从公网访问你的 80 端口完成验证的。若 80 被运营商封锁、被防火墙挡掉，或已被别的进程占用，Caddy 就拿不到证书。排错前先 `curl -I http://你的域名` 自测端口通不通，再查 Caddy 日志。

## 5.4 通配符与 staging：两个进阶必知

**通配符证书** `*.example.com` 用一张证书覆盖所有子域，省去逐个子域签发的管理成本。它有两个关键约束：[^c5-1]

1. **LE 对通配符强制 DNS-01**：你要证明的是「整个 example.com 域的控制权」，CA 不接受只证明「某一台服务器可达」的 HTTP-01。Caddy 要签/续通配证书，必须配置 DNS 托管商的 API 凭据（Caddy 的 DNS 模块靠它自动加删 TXT 记录）。
2. **测试务必切 LE staging**：LE 生产端点对同一域名有签发频率限制，反复测试或试续期把配额耗尽，会被封禁最长一周。Caddy 和 certbot 都提供把 ACME 端点切到 LE staging（测试端点）的开关；certbot 是命令行加 `--staging`。**先在 staging 把流程跑通，再切回生产**。

另外，Caddy 2.10+ 在配置里出现多个子域时，会自动改用通配证书服务这些子域。[^c5-1]

> [!tip] 大白话：通配证书 = 整栋楼的万能门卡
> 单域证书是一间房的钥匙，通配证书是能开 `*.example.com` 所有房间的万能门卡。正因为权限太大，发卡机构不认「你在某一间房门口收到信」这种单点证明，而要求你证明「整栋楼都是你的」——所以只能走 DNS-01 的公告栏验证，不能走 HTTP-01。

> [!warning] 通配证书没有 DNS 凭据就签不了
> LE 强制 DNS-01，意味着你必须能操作 DNS 托管商后台、或提供它的 API 凭据（token）给签发工具。只把服务器 80/443 暴露出去是不够的。

> [!warning] 反复测试先切 staging，否则封禁最长一周
> LE 生产端点对同一域名有签发频率限制。拿生产端点反复试错/试续期，配额耗尽会被封禁（最长一周），期间该域签不了新证书。凡是练手、调试、反复续期，一律先切 LE staging，跑通再回生产。[^c5-1]

## 5.5 Nginx + certbot：三条签发路径

已有 Nginx 想继续用，就用 certbot。它把签发拆成两个角色：**authenticator** 负责证明控域，**installer** 负责把证书写进 Web 服务器配置。[^c5-2] 你系统对应的精确安装命令以 certbot.eff.org 指令页为准（选操作系统 + Nginx，它会生成步骤）。[^c5-3] 下面是三种最常用的签发方式：

**① `--nginx`：签发并自动装入 Nginx**

```bash
sudo certbot --nginx -d example.com
```

自动完成「验证 → 签证书 → 改 Nginx 配置 → reload」，全程可回滚（`certbot rollback` 撤销改动）。适合 Nginx 配置本来就由 certbot 托管的情况。[^c5-2]

**② `certonly --webroot`：只签证书、免停机、不动配置**

```bash
sudo certbot certonly --webroot -w /var/www/html -d example.com
```

`-w` 指向现有站点根目录，certbot 在它下面放 HTTP-01 验证文件，Nginx 照常服务即可完成验证。只产出证书文件，不碰 Nginx 配置，适合你想手动管理配置的情况。[^c5-2]

**③ `--standalone`：certbot 自己当临时服务器**

```bash
sudo certbot certonly --standalone -d example.com
```

certbot 临时起一个服务响应 HTTP-01，因此要求 **80 端口空闲且由它独占**。Nginx/Caddy 正听着 80 时不能用这条，需要先停掉它们，或改用 webroot 方式。[^c5-2]

证书统一落在 `/etc/letsencrypt/live/<证书名>/`：`fullchain.pem`（证书链）+ `privkey.pem`（私钥）。目录默认权限 0700、仅 root 可读——这也是 Nginx 主进程要以 root 启动才能读私钥的原因。[^c5-2]

## 5.6 续期机制：让证书自己续

LE 证书寿命短，设计上就要求「频繁、自动、无人值守地续期」。certbot 的续期命令是幂等的，可以放心反复跑：

```bash
# 只续「临期」证书；本次真的续了才重载 Nginx
sudo certbot renew --deploy-hook "nginx -s reload"
```

拆开讲：

- **`certbot renew` 只续临期证书**：阈值是剩余寿命 < 总寿命的 1/3；若证书总寿命 ≤10 天，则剩余 <1/2 才续。平时跑它基本是空转、不产生新证书，所以可以放心放进定时任务（发行版装的 certbot 通常自带每天跑两次的 systemd timer）。[^c5-2]
- **判断「真续期」看 `--deploy-hook`**：`renew` 默认只替换证书文件，**不会自动重载 Web 服务器**。`--deploy-hook` 里的命令只在「本次确实续了证」之后才执行——把重载（`nginx -s reload` / `systemctl reload nginx`）放进去，既让新证书生效，也给你一个「到底续没续」的明确信号。[^c5-2]

两个容易踩的续期坑：

> [!warning] `--manual` 签的证书不会自动续期
> `certbot certonly --manual` 每次验证都要你手动交互（贴文件/TXT），续期自然无法无人值守。它只适合一次性试验；长期站点务必走 `--nginx` 或 `--webroot` 这类能自动完成验证的路径。[^c5-2]

> [!warning] 通配证书的自动续期只能靠 DNS 插件
> `certbot-dns-<厂商>` 插件是通配证书自动续期的唯一途径：它持有 DNS 托管商 API 凭据，续期时自动加删 `_acme-challenge` TXT。手搓 DNS-01 记录或用 `--manual`，到期不会自己更新，证书会静默过期。[^c5-2]

## 本章小结

- 本章面向「有公网 IP + 自有域名」；缺公网 IP 的读者掌握 5.2/5.3 的心智模型后直接去第 6 章。
- 证书自动化的核心是 ACME 控域验证：HTTP-01（80）/TLS-ALPN（443）验证单台服务器可达，DNS-01 验证整个域、是通配符证书的唯一途径。
- Caddy 最小反代 = 一个站点块 + `reverse_proxy`；满足 A/AAAA 指向本机、80/443 公网可达、配置含域名，即自动完成 HTTPS 与续期。
- Nginx 用户按需选 certbot 三路径：`--nginx` 自动装入、`certonly --webroot` 免停机不动配置、`--standalone` 需独占 80。
- 续期自动化：`certbot renew` 只续临期证书，用 `--deploy-hook` 重载服务并判断真续期；`--manual` 不自动续期，通配证书必须走 DNS 插件。

下一章，把「没有公网 IP」的场景补上：Cloudflare Tunnel、frp+Caddy、Tailscale Funnel 三条不依赖入站端口的路线，把本章的证书心智模型直接搬过去。

[^c5-1]: Caddy — Automatic HTTPS（官方文档）：https://caddyserver.com/docs/automatic-https
[^c5-2]: Certbot User Guide（官方文档）：https://eff-certbot.readthedocs.io/en/stable/using.html
[^c5-3]: certbot.eff.org 指令页（官方）：https://certbot.eff.org/instructions
---

[[04_dns-hosting-security|← 第4章 解析托管与域名安全]]  ·  [[域名完全上手|返回目录]]  ·  [[06_no-public-ip|第6章 无公网 IP 接入 →]]
