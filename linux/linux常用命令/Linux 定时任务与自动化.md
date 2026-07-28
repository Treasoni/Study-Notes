---
title: "Linux 定时任务与自动化"
created: 2026-07-29
updated: 2026-07-29
tags: [linux, 定时任务, crontab, systemd]
status: completed
source_project: linux-commands
---

> [!note]
> 定时任务是 Linux 运维的核心技能之一。从传统的 cron 到现代的 systemd-timer，从一次性任务到周期性调度，本章覆盖 Linux 下所有主流定时任务方案，帮你实现系统自动化运维。

---

## 1. cron / crontab — 周期性任务调度

### 1.1 基本概念

cron 是 Linux 上最经典的定时任务工具，由 `crond` 守护进程管理。用户通过 `crontab` 命令管理自己的任务列表。

### crontab 命令

```bash
# 编辑当前用户的 crontab
crontab -e

# 查看当前用户的定时任务
crontab -l

# 查看其他用户的定时任务（仅 root）
sudo crontab -l -u bob

# 清空定时任务
crontab -r

# 从文件导入任务
crontab tasks.txt
```

### 1.2 时间表达式

cron 表达式共 5 个字段，用空格分隔：

```
* * * * * command
─ ─ ─ ─ ─
│ │ │ │ │
│ │ │ │ └── 星期 (0-7, 0/7=周日)
│ │ │ └──── 月份 (1-12)
│ │ └────── 日期 (1-31)
│ └──────── 小时 (0-23)
└────────── 分钟 (0-59)
```

**常用示例：**

```bash
# 每分钟执行（调试用）
* * * * * /path/to/script.sh

# 每天凌晨 2:30 执行
30 2 * * * /path/to/script.sh

# 每小时的 15 分执行
15 * * * * /path/to/script.sh

# 工作日（周一至周五）早 9 点执行
0 9 * * 1-5 /path/to/script.sh

# 每隔 5 分钟执行
*/5 * * * * /path/to/script.sh

# 每月 1 号和 15 号执行
0 0 1,15 * * /path/to/script.sh

# 每季度第一天执行
0 0 1 1,4,7,10 * /path/to/script.sh
```

> [!tip]
> **时间表达式速查表：**
>
> | 含义 | 表达式 |
> |------|--------|
> | 每分钟 | `* * * * *` |
> | 每 5 分钟 | `*/5 * * * *` |
> | 每 30 分钟 | `*/30 * * * *` |
> | 每小时 | `0 * * * *` |
> | 每天早上 6 点 | `0 6 * * *` |
> | 每天晚上 10 点 | `0 22 * * *` |
> | 每周一凌晨 3 点 | `0 3 * * 1` |
> | 每月 1 号凌晨 | `0 0 1 * *` |
> | 重启后执行 | `@reboot` |

### 1.3 特殊语法

```bash
# 重启后执行
@reboot /path/to/script.sh

# 每分钟
@yearly   /path/to/script.sh   # 等价于 0 0 1 1 *
@monthly  /path/to/script.sh   # 等价于 0 0 1 * *
@weekly   /path/to/script.sh   # 等价于 0 0 * * 0
@daily    /path/to/script.sh   # 等价于 0 0 * * *
@hourly   /path/to/script.sh   # 等价于 0 * * * *
```

### 1.4 管理 crond 服务

```bash
# 查看 crond 状态
sudo systemctl status cron

# 启动 / 停止 / 重启
sudo systemctl start cron
sudo systemctl stop cron
sudo systemctl restart cron

# 开机自启
sudo systemctl enable cron
```

### 1.5 crontab 日志

```bash
# Debian/Ubuntu 日志位置
sudo tail -f /var/log/syslog | grep CRON

# 查看最近执行的 cron 任务
grep CRON /var/log/syslog | tail -20

# RHEL/CentOS
sudo tail -f /var/log/cron

# 如果任务有输出，默认会发邮件给用户
# 查看本地邮件（如果系统有 MTA）
mail
```

> [!warning]
> cron 的默认 `PATH` 很精简，通常只有 `/usr/bin:/bin`。脚本中用到非标准路径的命令（如 `docker`、`node`）时，要么在脚本内设置 `PATH`，要么在 crontab 开头设置：
> ```bash
> PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
> 0 3 * * * /usr/local/bin/docker-compose up -d
> ```

### 1.6 crontab 的最佳实践

```bash
# 推荐的 crontab 格式（带注释和环境变量）
# ┌─────────────────── 邮件发送给谁
# │ ┌───────────────── 环境变量
# │ │
# MAILTO=admin@example.com
#
# 每天 3 点备份数据库
0 3 * * * /home/bob/scripts/backup_db.sh

# 每 5 分钟监控服务健康
*/5 * * * * /home/bob/scripts/health_check.sh

# 每周一清理日志
0 4 * * 1 /home/bob/scripts/cleanup_logs.sh
```

> [!tip]
> **crontab 注意事项：**
> - 脚本输出会通过邮件发送给用户，开发时可用 `>/dev/null 2>&1` 丢弃输出
> - `%` 在 crontab 中有特殊含义，需要用 `\%` 转义
> - 使用绝对路径调用命令和脚本，避免 PATH 问题
> - 配置前先用 `crontab -l` 确认当前已有任务，避免误覆盖

---

## 2. at — 一次性定时任务

适用于 **仅执行一次** 的任务场景。

```bash
# 在指定时间执行命令
echo "shutdown -h now" | at 23:00

# 交互式方式
at 23:00
warning: commands will be executed using /bin/sh
at> tar czf /backup/home_$(date +%Y%m%d).tar.gz /home
at> <EOT>        # Ctrl+D 结束输入
job 5 at Wed Jul 29 23:00:00 2026
```

**时间格式示例：**

```bash
# 绝对时间
at 15:30
at 15:30 2026-07-30
at now + 5 minutes
at now + 1 hour
at now + 2 days
at 17:00 tomorrow
at 10:00 next week
at 23:00 next month

# 查看等待中的任务
atq

# 删除指定任务
atrm 5

# 查看任务详情
at -c 5
```

> [!tip]
> `at` 常用于：
> - 延迟执行的重启操作（避开高峰时段）
> - 一次性提醒（配合 `notify-send` 或邮件）
> - 临时维护窗口的自动化操作

---

## 3. systemd-timer — 现代替代方案

systemd-timer 是 cron 的现代替代品，与 systemd 深度集成，支持更精细的控制。

### 3.1 基本结构

每个 timer 由 **两个文件** 组成：

```text
/etc/systemd/system/backup.service    ← 定义要执行的任务
/etc/systemd/system/backup.timer      ← 定义调度时间
```

### 3.2 创建 timer

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Daily database backup

[Service]
Type=oneshot
ExecStart=/home/bob/scripts/backup_db.sh
# 可选：失败重试
Restart=on-failure
RestartSec=30
```

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Run backup daily at 3am
Requires=backup.service

[Timer]
# 日历时间表达式（类似 cron）
OnCalendar=daily
# 更精确的写法：每天 3:00
# OnCalendar=*-*-* 03:00:00

# 首次执行延迟（避免同时启动）
RandomizedDelaySec=300

# 如果错过执行时间（如关机），启动后立即执行
Persistent=true

# 单位时间内固定间隔
# OnUnitActiveSec=24h

[Install]
WantedBy=timers.target
```

### 3.3 日历时间表达式

```text
# 基本格式：星期 日期 时间
# 完整：DayOfWeek Year-Month-Day Hour:Minute:Second

OnCalendar=daily                    # 每天凌晨 0 点
OnCalendar=hourly                   # 每小时
OnCalendar=*-*-* 03:00:00          # 每天 3 点
OnCalendar=Mon,Wed,Fri *-*-* 09:00:00  # 工作日早 9 点
OnCalendar=*-*-1..7 02:00:00       # 每月前 7 天凌晨 2 点
OnCalendar=*:0/15                  # 每 15 分钟
```

### 3.4 管理 timer

```bash
# 启动 timer
sudo systemctl start backup.timer

# 开机自启
sudo systemctl enable backup.timer

# 查看 timer 状态
sudo systemctl status backup.timer

# 查看所有 timer
systemctl list-timers --all

# 手动触发一次（不等待调度）
sudo systemctl start backup.service

# 停用
sudo systemctl stop backup.timer
sudo systemctl disable backup.timer
```

### 3.5 cron vs systemd-timer 对比

| 特性 | cron | systemd-timer |
|------|:----:|:-------------:|
| 语法复杂度 | 简单 | 中 |
| 精度 | 分钟级 | 秒级 |
| 依赖管理 | 手动 | 原生支持 |
| 日志集成 | 需手动配置 | 自动 journald |
| 错过执行 | 不补执行 | 可配置 `Persistent=true` |
| 随机延迟 | 不支持 | 原生支持 `RandomizedDelaySec` |
| 资源隔离 | 无 | 通过 cgroup 隔离 |
| 跨系统移植 | 全平台 | 仅 systemd 系统 |
| 适用场景 | 快速配置、全平台 | 复杂调度、现代 Linux |

> [!tip]
> **选型建议：**
> - 简单的周期性任务 → **crontab**（配置快、全平台通用）
> - 需要精确控制、依赖管理、日志集成 → **systemd-timer**（推荐新项目使用）
> - 一次性定时任务 → **at**

---

## 4. anacron — 非 7x24 场景

笔记本、桌面机等**不会全天开机**的场景，anacron 能确保任务在下次开机时补执行。

```bash
# /etc/anacrontab 格式
# period delay job-id command
1      5     daily.backup /home/bob/scripts/backup.sh
7      10    weekly.clean /home/bob/scripts/cleanup.sh
30     15    monthly.update /home/bob/scripts/update.sh
```

| 字段 | 含义 | 示例 |
|------|------|------|
| `period` | 执行频率（天） | `1`=每天, `7`=每周 |
| `delay` | 延迟时间（分钟） | `5`=开机 5 分钟后执行 |
| `job-id` | 任务唯一标识（用于时间戳追踪） | `daily.backup` |
| `command` | 要执行的命令 | `/path/to/script.sh` |

> [!note]
> anacron 适合**桌面/笔记本**环境。服务器通常 7x24 运行，用 crontab 即可。如果服务器上同时安装了 `anacron`，cron 会委托 anacron 处理 `daily`、`weekly`、`monthly` 目录下的任务。

---

## 5. 实践场景

### 场景 1：数据库每日备份 + 保留策略

```bash
# /home/bob/scripts/backup_db.sh
#!/bin/bash
BACKUP_DIR="/backup/mysql"
DB_NAME="myapp"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"
mysqldump --single-transaction "$DB_NAME" | gzip > "$BACKUP_DIR/${DB_NAME}_$DATE.sql.gz"
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "[$(date)] Backup $DB_NAME completed, kept $RETENTION_DAYS days" >> /var/log/backup.log
```

```bash
# crontab -e
0 3 * * * /home/bob/scripts/backup_db.sh
```

### 场景 2：服务器健康巡检 + 告警

```bash
# /home/bob/scripts/health_check.sh
#!/bin/bash
ALERT_EMAIL="admin@example.com"
LOAD_THRESHOLD=5.0
DISK_THRESHOLD=90

# CPU 负载检查
LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk -F',' '{print $1}')
if (( $(echo "$LOAD > $LOAD_THRESHOLD" | bc -l) )); then
    echo "High load: $LOAD" | mail -s "ALERT: Server load high" "$ALERT_EMAIL"
fi

# 磁盘使用率检查
df -h | awk 'NR>1 {print $5, $6}' | while read usage mount; do
    pct=${usage%\%}
    if [ "$pct" -ge "$DISK_THRESHOLD" ]; then
        echo "Disk $mount at $usage" | mail -s "ALERT: Disk full" "$ALERT_EMAIL"
    fi
done
```

```bash
# crontab -e
*/5 * * * * /home/bob/scripts/health_check.sh >/dev/null 2>&1
```

### 场景 3：systemd-timer 实现定时清理临时文件

```ini
# /etc/systemd/system/clean-tmp.service
[Unit]
Description=Clean temporary files

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'find /tmp -type f -atime +7 -delete; find /var/tmp -type f -atime +14 -delete'
```

```ini
# /etc/systemd/system/clean-tmp.timer
[Unit]
Description=Clean temp files weekly

[Timer]
OnCalendar=weekly
RandomizedDelaySec=1800
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now clean-tmp.timer
```

---

## 6. 常见问题

### 6.1 任务没有执行

```bash
# 1. 检查 cron 服务是否运行
sudo systemctl status cron

# 2. 检查 crontab 是否存在
crontab -l

# 3. 检查 cron 日志
sudo tail -20 /var/log/syslog | grep CRON

# 4. 检查脚本是否有执行权限
ls -l /path/to/script.sh
chmod +x /path/to/script.sh

# 5. 手动执行测试
/path/to/script.sh
```

### 6.2 路径问题

cron 默认的 `PATH` 非常精简，远低于交互式 Shell 的环境：

```bash
# 查看 cron 默认 PATH（在脚本中输出）
echo "PATH=$PATH" > /tmp/cron_path.txt

# 解决方案一：在 crontab 中设置 PATH
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 解决方案二：在脚本中使用绝对路径
/usr/bin/docker exec app /usr/local/bin/backup.sh
```

### 6.3 任务重复执行

```bash
# 使用锁文件防止重复（flock）
# crontab -e
*/5 * * * * /usr/bin/flock -n /tmp/backup.lock /home/bob/scripts/backup.sh
```

---

> [!summary]
> **核心命令速查：**
>
> | 操作 | 命令 |
> |------|------|
> | 编辑定时任务 | `crontab -e` |
> | 查看定时任务 | `crontab -l` |
> | 一次性任务 | `echo "cmd" \| at now + 1 hour` |
> | 查看定时器 | `systemctl list-timers` |
> | 即时执行 timer 任务 | `sudo systemctl start xxx.service` |
> | 非 7x24 任务 | 配置 `/etc/anacrontab` |
> | 防止重复执行 | `flock -n /tmp/lock.lock cmd` |
> | 查看 cron 日志 | `sudo tail -f /var/log/syslog \| grep CRON` |
