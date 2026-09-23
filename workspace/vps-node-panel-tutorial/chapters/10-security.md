## 第 10 章 安全事项与最小加固

前面几章里，你已经把节点跑通、导进客户端，甚至处理过一次被墙换 IP。但"能连"不等于"安全"：面板默认口令、SSH 密码登录、无限制的爆破尝试，任意一处没收尾都可能让你在不觉察时被人接管。本章按「面板侧 → SSH 侧 → 封禁侧」三层，每层只给最小必要动作，深度加固不在这里展开。

### 面板侧：先堵默认凭据这道口子

面板是整台机器上最值钱的入口——拿到它等于拿到全部入站配置。它的凭据长什么样，取决于你在第 5 章选的安装方式：

- **一键脚本安装**：安装时会随机生成用户名、密码与访问路径（来源：B-1 | Install in one-line；A-3 | Quick Start）。这里没有"默认值"需要改，要做的是把随机凭据保存好。
- **Docker Compose / Docker CLI 安装**：默认凭据固定为 `admin` / `admin`（来源：B-1 | Using Docker Compose）。登录后必须**立刻**在 `Panel Settings > Authentication` 改掉（来源：B-1 | Using Docker Compose）。

除改口令外，B-1 的安装页还建议两项（来源：B-1 | Using Docker Compose）：

- 开启两步验证（2FA）；
- 配置自定义面板访问路径，让面板不落在可猜的 URL 上。

随机凭据弄丢时，登录服务器执行 `x-ui` 可重开管理菜单，查看或重置凭据（来源：B-1 | Install in one-line；A-3 | Quick Start）。

> [!warning] 面板层没有独立的安全文档
> 3x-ui 官方仓库与安装 wiki 都不提供专门的安全加固章节（来源：A-3 全页 / B-1 全页）。上面这些动作都出自**产品配置说明**（安装页的 Caution 提示与仓库 Features 清单），不是一份"官方安全指南"，请按此层级理解，勿当作官方安全标准。

> [!note] 合规提醒
> 项目自述"仅供个人使用，请勿用于非法用途或生产环境"（来源：A-3 | Important）。这是一句项目方的定位声明，不是安全能力承诺。

> [!tip] 大白话
> 把面板默认口令想成"开发商交付的同一把钥匙"——每一间毛坯房都是这把。你不换锁，别人手里的钥匙就能开你的门。Docker 安装默认 admin/admin，等于门锁上贴着"钥匙就是 1234"；一键安装给的是每户不同的随机钥匙，别弄丢。

### SSH 侧：`sshd_config` 里三条最小改动

SSH 是你唯一的管理通道，攻击面也最直接。下面这张表是**OpenSSH `sshd_config(5)` 手册页标注的默认值**，以及建议值（来源：C-4 | KEYWORDS）：

| 配置项 | 官方手册默认值 | 建议值 | 作用 |
|---|---|---|---|
| `PasswordAuthentication` | `yes` | `no` | 关闭密码登录，只认公钥 |
| `PermitRootLogin` | `prohibit-password` | `prohibit-password` 或 `no` | root 不许用密码登录 |
| `PermitEmptyPasswords` | `no` | 保持 `no` | 拒绝空密码账户 |
| `MaxAuthTries` | `6` | 按需调小 | 单连接最大认证尝试次数 |
| `LoginGraceTime` | `120` 秒 | 按需调小 | 未登录成功即断开的等待时间 |

改动落在 `/etc/ssh/sshd_config`，让改动生效：

```bash
systemctl restart ssh
```

> [!warning] 关掉密码登录之前，先把公钥配好
> 把 `PasswordAuthentication` 改成 `no` 后，如果公钥还没生效，你会把自己锁在门外。务必**先用另一条 SSH 连接验证公钥能登入**（新开一个终端试连、成功后再退出当前会话），最后才重启服务。

> [!tip] 大白话
> `prohibit-password` 想成"root 这间办公室不许刷工牌（密码）进，只许用专用钥匙（公钥）进"。`MaxAuthTries=6` 是"连错 6 次就请你出去"，`LoginGraceTime=120` 秒是"给你两分钟站门口，超时不进就关门"。

### 封禁侧：fail2ban 的覆盖机制与三个参数

即使关了密码登录，公钥握手失败、无效用户名探测仍会刷屏。fail2ban 做的是"读日志里的失败记录，临时封掉来源 IP"。

**先理解它怎么读配置**（来源：C-3 | CONFIGURATION FILES FORMAT）：官方建议 `*.conf` 保持不动以便升级，你的改动写进 `*.local`。解析顺序为 `jail.conf` → `jail.d/*.conf` → `jail.local` → `jail.d/*.local`，**后解析的覆盖先解析的**。所以在 `.local` 里只写你要改的那几行即可。

三个核心参数（来源：C-3 | jail.conf [DEFAULT]）：

- `bantime`：封禁持续时长；
- `findtime`：统计失败次数的时间窗口；
- `maxretry`：在最近 `findtime` 内累计失败达到多少次就封。

> [!warning] C-3 未给发行版默认数值
> fail2ban 手册页**没有列出** `bantime` / `findtime` / `maxretry` 在各发行版的具体默认秒数（来源：C-3 | jail.conf [DEFAULT]）。本章因此只写参数语义，不写"默认封 10 分钟"这类数字——具体默认值请以你机器上 `/etc/fail2ban/jail.conf` 的实际内容为准。

时间写法支持缩写，`600` 等价 `10m`（来源：C-3 | TIME ABBREVIATION FORMAT）。用自带的工具校验，再重启服务：

```bash
# 校验时间缩写是否合法（10m = 600 秒）
fail2ban-client --str2sec 10m
# 让改动生效
systemctl restart fail2ban
```

另外两个有用的键：`ignoreip` 列出永不封禁的 IP/CIDR（来源：C-3 | jail.conf [DEFAULT]）；封禁与解封动作分别由 `actionban`（达到 `maxretry` 且落在最近 `findtime` 内时触发）和 `actionunban`（`bantime` 之后）定义（来源：C-3 | ACTION CONFIGURATION FILES）。

> [!tip] 大白话
> `.conf` 想成"产品说明书原件"，`.local` 想成"你在说明书上贴的便签"：只贴便签、不涂原件，下次升级换说明书，你的便签还在。`maxretry` 是"容忍几次"，`findtime` 是"在多长时间内数"，`bantime` 是"关小黑屋关多久"。

### 什么必须做，什么超出本篇范围

必须做的收尾动作就是本章三节：面板改默认凭据（Docker 安装必做）、SSH 收紧登录方式、fail2ban 按参数语义配置。

**超出本篇范围的深度加固**：`nftables` / `suricata` 级别的防火墙与入侵检测、内核直配、传输层前沿方案的原理，请在既有笔记中展开，本篇只做指引与双链：[[自建代理节点搭建实战]]。

### 本章小结

- 面板侧最小加固 = 改默认凭据 + 2FA + 自定义路径；此层无官方安全文档，属产品配置说明。
- SSH 侧三条核心：`PasswordAuthentication no`、`PermitRootLogin prohibit-password`、保持 `PermitEmptyPasswords no`，其余为按需可调项。
- fail2ban 只改 `.local`，后解析者覆盖先解析者；三个参数只按语义写，不套默认秒数。
- 关闭密码登录前务必先验证公钥可用，否则会把自锁在门外。
- 深度加固（nftables / suricata / 内核直配）不在本篇展开，指向既有笔记。

接下来是附录：一张端口与命令速查表，以及本篇与既有笔记的分工与互链说明。

---

### 参考来源

- [3x-ui 官方 Installation 文档（B-1）](https://github.com/MHSanaei/3x-ui/wiki/Installation)
- [MHSanaei/3x-ui 官方仓库（A-3）](https://github.com/MHSanaei/3x-ui)
- [OpenSSH sshd_config(5) 手册页（C-4）](https://man.openbsd.org/sshd_config)
- [fail2ban jail.conf(5) 手册页（C-3）](https://manpages.debian.org/bookworm/fail2ban/jail.conf.5.en.html)
