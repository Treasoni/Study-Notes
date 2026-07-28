---
title: "Linux 日志管理"
created: 2026-07-29
updated: 2026-07-29
tags: [linux, 日志, journald, rsyslog, logrotate]
status: completed
source_project: linux-commands
---

> [!note]
> 日志是系统排障的"黑匣子"。从 journald 的二进制日志到 rsyslog 的灵活路由，从 logrotate 的自动轮转到集中式日志收集，本章帮你建立完整的日志管理知识体系，让排查问题时不再大海捞针。

---

## 1. systemd-journald — 现代日志系统

现代 Linux 发行版默认使用 systemd-journald 集中管理日志。它收集内核日志、系统服务日志、用户应用程序日志，统一存储在二进制文件中。

### 1.1 journalctl 基本用法

```bash
# 查看所有日志（默认按时间倒序，底部是最新的）
journalctl

# 查看最新 20 条（类似 tail -20）
journalctl -n 20

# 持续追踪新日志（类似 tail -f）
journalctl -f

# 查看指定服务的日志
journalctl -u nginx.service
journalctl -u ssh.service

# 查看多个服务的日志（合并输出）
journalctl -u nginx.service -u php8.1-fpm.service

# 查看内核日志（等价于 dmesg）
journalctl -k

# 查看本次启动以来的日志
journalctl -b

# 查看上一次启动的日志
journalctl -b -1

# 列出所有启动记录（用于 -b 参数）
journalctl --list-boots
```

> [!tip]
> `journalctl --list-boots` 输出格式：
> ```
>  -3 5b8a...  Mon 2026-07-14 07:15:01 CST—Tue 2026-07-14 10:30:01 CST
>  -2 1a2b...  Wed 2026-07-15 07:15:01 CST—Thu 2026-07-16 18:00:01 CST
>  -1 e3f4...  Fri 2026-07-17 07:15:01 CST—Sun 2026-07-19 23:45:01 CST
>   0 9a8b...  Mon 2026-07-20 07:15:01 CST—still running
> ```
> 第一列的数字就是 `-b` 的参数，`0` 表示当前启动，负数为之前的启动。

### 1.2 日志筛选与搜索

```bash
# 按时间范围筛选
journalctl --since "2026-07-28 09:00:00" --until "2026-07-28 18:00:00"

# 相对时间
journalctl --since "1 hour ago"
journalctl --since yesterday
journalctl --since "2 days ago" --until "1 day ago"
journalctl --since "2026-07-01" --until "2026-07-31"

# 按优先级筛选
journalctl -p err                # 仅错误及以上
journalctl -p warning            # 警告及以上
journalctl -p info               # 信息及以上（默认）

# 优先级等级
# 0: emerg（紧急）  1: alert（警报）
# 2: crit（严重）   3: err（错误）
# 4: warning（警告） 5: notice（通知）
# 6: info（信息）    7: debug（调试）

# 按可执行文件路径筛选
journalctl /usr/sbin/nginx
journalctl /usr/bin/python3

# 按用户筛选
journalctl _UID=1000

# 按 PID 筛选
journalctl _PID=1234

# 组合条件（AND 关系）
journalctl -u nginx.service -p err --since "1 hour ago"

# 使用 grep 进一步过滤
journalctl -u nginx.service | grep "502 Bad Gateway"
```

### 1.3 日志格式与输出控制

```bash
# 输出格式控制
journalctl -o short           # 默认格式，一行一条
journalctl -o short-full      # 带完整时间戳
journalctl -o verbose         # 显示所有字段（最详细）
journalctl -o json            # JSON 格式
journalctl -o json-pretty     # 格式化 JSON
journalctl -o cat             # 仅输出消息本身（无前缀信息）

# 显示最近 10 条，只输出消息内容
journalctl -n 10 -o cat

# 输出到分页器（默认）
journalctl | less

# 不分页直接输出（重定向文件时用）
journalctl --no-pager > /tmp/all_logs.txt

# 导出日志
journalctl -o export > system_logs.journal
```

### 1.4 journald 配置与维护

```bash
# 查看日志占用的磁盘空间
journalctl --disk-usage
# Archived and active journals take up 1.2G in the file system

# 限制日志大小（修改配置）
sudo vim /etc/systemd/journald.conf

# /etc/systemd/journald.conf 关键配置
SystemMaxUse=1G               # 日志最大占用 1GB
SystemMaxFileSize=200M        # 单个日志文件最大 200MB
MaxRetentionSec=1month        # 日志保留 1 个月
ForwardToSyslog=yes           # 转发到 rsyslog（如已安装 rsyslog）
Compress=yes                  # 压缩旧日志

# 修改后重启
sudo systemctl restart systemd-journald

# 手动清理日志（保留 500MB）
sudo journalctl --vacuum-size=500M

# 保留最近 7 天
sudo journalctl --vacuum-time=7d

# 保留最近 2 次启动
sudo journalctl --vacuum-files=2
```

> [!warning]
> `journalctl --vacuum-*` 是**立即清理**，不是设置限制。要设置上限，需要修改 `/etc/systemd/journald.conf` 然后重启服务。

---

## 2. rsyslog — 灵活的日志路由

rsyslog 是传统的系统日志守护进程，可以从各类程序、内核、远程主机收集日志，并按规则路由到不同的文件或目的地。

### 2.1 基本概念

**常见日志文件位置：**

| 日志文件 | 用途 |
|----------|------|
| `/var/log/syslog` | 系统综合日志（Ubuntu/Debian） |
| `/var/log/messages` | 系统综合日志（RHEL/CentOS） |
| `/var/log/auth.log` | 认证日志（登录、sudo） |
| `/var/log/kern.log` | 内核日志 |
| `/var/log/dmesg` | 内核环形缓冲区日志 |
| `/var/log/nginx/access.log` | Nginx 访问日志 |
| `/var/log/nginx/error.log` | Nginx 错误日志 |
| `/var/log/mysql/error.log` | MySQL 错误日志 |
| `/var/log/mail.log` | 邮件服务器日志 |

### 2.2 查看日志

```bash
# 查看认证日志（登录、sudo 操作）
sudo tail -f /var/log/auth.log

# 查看最近的 sudo 执行记录
sudo grep sudo /var/log/auth.log | tail -20

# 查看 SSH 登录记录
sudo grep sshd /var/log/auth.log | tail -20

# 查看系统综合日志
sudo tail -f /var/log/syslog

# 查看内核日志
sudo tail -f /var/log/kern.log
```

### 2.3 rsyslog 配置基础

```bash
# /etc/rsyslog.conf 或 /etc/rsyslog.d/ 下的自定义配置

# 配置语法：facility.priority    action
auth.*                          /var/log/auth.log
*.info;auth,authpriv.none       /var/log/syslog
kern.*                          /var/log/kern.log

# 将 nginx 访问日志转发到特定文件
# 前提：nginx 配置了 syslog 输出
```

**常见的 facility 和 priority：**

| Facility | 含义 | Priority | 含义 |
|----------|------|----------|------|
| `auth` | 认证系统 | `emerg` | 紧急 |
| `authpriv` | 私有认证 | `alert` | 警报 |
| `cron` | 定时任务 | `crit` | 严重 |
| `daemon` | 守护进程 | `err` | 错误 |
| `kern` | 内核 | `warning` | 警告 |
| `mail` | 邮件系统 | `notice` | 通知 |
| `syslog` | syslog 自身 | `info` | 信息 |
| `user` | 用户程序 | `debug` | 调试 |
| `local0-local7` | 自定义使用 | — | — |

### 2.4 配置 rsyslog 收集远程日志

```bash
# 服务端配置（接收远程日志）
# /etc/rsyslog.d/remote-server.conf
module(load="imtcp")
input(type="imtcp" port="514")

# 按主机名分类存储
$template RemoteLogs,"/var/log/remote/%HOSTNAME%/%$YEAR%-%$MONTH%-%$DAY%.log"
*.* ?RemoteLogs
```

```bash
# 客户端配置（发送日志到中心服务器）
# /etc/rsyslog.d/remote-client.conf
*.* @@192.168.1.100:514
# @    = UDP
# @@   = TCP（更可靠）
```

```bash
# 重启 rsyslog
sudo systemctl restart rsyslog

# 确认端口监听
sudo ss -tlnp | grep 514
```

> [!tip]
> 生产环境建议用 **TCP** 传输日志（`@@`），避免 UDP 丢包。大量日志场景可启用压缩或使用专用的日志收集工具。如果只是简单查看日志，journald 已经足够，不一定要部署 rsyslog 远程收集。

---

## 3. logrotate — 日志轮转

日志文件如果不加控制，终将撑满磁盘。logrotate 负责自动轮转、压缩、删除旧日志。

### 3.1 基本配置

```bash
# /etc/logrotate.conf 全局配置
weekly                    # 每周轮转一次
rotate 4                  # 保留 4 份轮转后的日志
create                    # 轮转后创建新日志文件
dateext                   # 文件名带日期后缀
compress                  # 轮转后压缩旧日志（gzip）
include /etc/logrotate.d  # 包含应用自定义配置
```

### 3.2 应用日志配置示例

```nginx
# /etc/logrotate.d/nginx
/var/log/nginx/*.log {
    daily                    # 每天轮转
    missingok                # 日志文件不存在时不报错
    rotate 14                # 保留 14 天
    compress                 # 压缩旧日志
    delaycompress            # 延迟压缩（保留一份未压缩的）
    notifempty               # 空文件不轮转
    create 0640 www-data adm  # 新日志文件的权限和所有者
    sharedscripts            # 所有日志轮转完后执行一次脚本
    postrotate               # 轮转后通知 nginx 重新打开日志文件
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

```bash
# /etc/logrotate.d/rsyslog
/var/log/syslog
/var/log/auth.log
/var/log/kern.log
/var/log/mail.log
/var/log/debug
{
    rotate 7
    daily
    missingok
    notifempty
    compress
    delaycompress
    sharedscripts
    postrotate
        /usr/lib/rsyslog/rsyslog-rotate
    endscript
}
```

### 3.3 logrotate 常用配置指令

| 指令 | 含义 | 示例 |
|------|------|------|
| `daily` / `weekly` / `monthly` | 轮转频率 | `daily` |
| `rotate N` | 保留 N 份旧日志 | `rotate 30` |
| `compress` | gzip 压缩旧日志 | `compress` |
| `delaycompress` | 延迟一次轮转后再压缩 | `delaycompress` |
| `missingok` | 日志缺失不报错 | `missingok` |
| `notifempty` | 空文件不轮转 | `notifempty` |
| `create [mode] [owner] [group]` | 创建新日志文件 | `create 0640 www-data adm` |
| `dateext` | 日期后缀而非数字后缀 | `dateext` |
| `maxsize SIZE` | 日志超过此大小即触发轮转 | `maxsize 100M` |
| `minsize SIZE` | 必须同时满足时间和大小条件 | `minsize 50M` |
| `postrotate` / `endscript` | 轮转后执行脚本 | 通知应用重开文件 |
| `prerotate` / `endscript` | 轮转前执行脚本 | 备份前操作 |
| `sharedscripts` | 所有匹配文件只执行一次脚本 | `sharedscripts` |
| `size SIZE` | 按日志大小轮转（替代时间） | `size 100M` |

### 3.4 管理 logrotate

```bash
# 手动触发 logrotate（调试配置）
sudo logrotate -f /etc/logrotate.d/nginx

# 调试模式（显示会做什么但不执行）
sudo logrotate -d /etc/logrotate.conf

# 查看 logrotate 状态（上次轮转时间）
cat /var/lib/logrotate/status | head -20

# 强制轮转并查看详细信息
sudo logrotate -vf /etc/logrotate.d/nginx
```

> [!warning]
> **logrotate 常见坑：**
> 1. 应用必须在 `postrotate` 中重新打开日志文件（发送 `USR1` 信号），否则日志会写入已删除的文件句柄
> 2. 配置修改后用 `-d` 先调试确认语法正确
> 3. 如果应用不响应 `USR1` 信号，可配置 `copytruncate`（先复制再截断，但可能有少量丢日志）
> 4. `copytruncate` 与 `create` 互斥，二选一

---

## 4. 实践场景

### 场景 1：排查 502 Bad Gateway

```bash
# 1. 检查 Nginx 错误日志
sudo tail -f /var/log/nginx/error.log

# 2. 同时跟踪 Nginx 和 PHP-FPM 日志
journalctl -u nginx.service -u php8.1-fpm.service -f

# 3. 看 journald 中 PHP-FPM 的最近错误
journalctl -u php8.1-fpm.service -p err --since "30 min ago" --no-pager

# 4. 检查系统资源
free -h              # 内存
df -h                # 磁盘
```

### 场景 2：排查 SSH 登录失败

```bash
# 1. 查看认证日志
sudo tail -f /var/log/auth.log | grep sshd

# 2. 查看暴力破解尝试
sudo grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -10

# 3. 查看 journald
journalctl -u ssh.service -p err --since "today"

# 4. 查看登录失败记录
sudo lastb | head -20
```

### 场景 3：配置日志轮转防止磁盘写满

```bash
# /etc/logrotate.d/custom-apps
/var/log/myapp/*.log
/var/log/myapp/*.json {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    maxsize 100M    # 即使未到每天，超过 100M 也轮转
    sharedscripts
    postrotate
        systemctl reload myapp  # 应用重新加载
    endscript
}
```

### 场景 4：集中式日志收集

```bash
# 小型架构方案
# 1. 所有服务器配置 rsyslog 发送日志到中心服务器
# 2. 中心服务器上 journald 接收并存储
# 3. 运维人员只需 ssh 到中心服务器查看日志

# 服务端（192.168.1.100）—— /etc/rsyslog.d/server.conf
module(load="imtcp")
input(type="imtcp" port="514")
$template RemoteLogs,"/var/log/remote/%HOSTNAME%/%programname%/%$YEAR%-%$MONTH%-%$DAY%.log"
*.* ?RemoteLogs

# 客户端—— /etc/rsyslog.d/client.conf
*.* @@192.168.1.100:514

# 验证
sudo logger -t test "Test message from $(hostname)"
sudo tail -f /var/log/remote/*/test/*
```

> [!tip]
> 生产环境日志量大的话，rsyslog 远程收集可能成为瓶颈，可以考虑 Elastic Stack（ELK）、Loki 或专门的日志 SaaS 服务。本节的配置适合中小规模（几十台服务器以下）的场景。

---

## 5. 常见问题

### 5.1 journald 日志占用空间太大

```bash
# 查看当前占用
journalctl --disk-usage

# 紧急清理
sudo journalctl --vacuum-size=500M

# 长期限制：修改配置文件
sudo sed -i 's/^#SystemMaxUse=/SystemMaxUse=/; s/^SystemMaxUse=.*/SystemMaxUse=500M/' /etc/systemd/journald.conf
sudo systemctl restart systemd-journald
```

### 5.2 logrotate 未按预期工作

```bash
# 调试模式运行
sudo logrotate -d /etc/logrotate.conf

# 检查状态文件
cat /var/lib/logrotate/status | grep nginx

# 常见问题：
# - 文件路径写错（如 /var/log 写成 /var/logs）
# - 权限不足（create 指定的用户/组不存在）
# - postrotate 脚本执行失败（脚本错误）
# - 轮转后没有通知应用重开文件句柄
```

### 5.3 日志文件被删除但空间未释放

应用打开日志文件后，`rm` 删除只删除了目录项，文件实际由该应用的文件句柄持有，空间不会释放。

```bash
# 找到持有已删除文件句柄的进程
lsof | grep deleted

# 找到具体是哪个应用
lsof /var/log/nginx/access.log

# 解决方法：正确重启应用或发送 USR1 信号让其重开
kill -USR1 $(cat /var/run/nginx.pid)
```

---

> [!summary]
> **核心命令速查：**
>
> | 操作 | 命令 |
> |------|------|
> | 查看所有日志 | `journalctl` |
> | 查看服务日志 | `journalctl -u nginx.service` |
> | 跟踪实时日志 | `journalctl -f` |
> | 按时间筛选 | `journalctl --since "1 hour ago"` |
> | 按错误级别 | `journalctl -p err` |
> | 查看认证日志 | `sudo tail -f /var/log/auth.log` |
> | 查看系统日志 | `sudo tail -f /var/log/syslog` |
> | 清理 journald | `sudo journalctl --vacuum-size=500M` |
> | 手动轮转日志 | `sudo logrotate -f /etc/logrotate.d/nginx` |
> | 调试轮转 | `sudo logrotate -d /etc/logrotate.conf` |
