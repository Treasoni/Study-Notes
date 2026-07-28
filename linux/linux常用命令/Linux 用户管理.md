---
title: "Linux 用户管理"
created: 2026-07-29
updated: 2026-07-29
tags: [linux, 用户管理, user]
status: completed
source_project: linux-commands
---

> [!note]
> Linux 是多用户操作系统，用户管理是系统安全的基石。从创建用户到配置 sudo 提权，从密码策略到用户组权限隔离，本章覆盖日常运维中所有用户管理操作，帮你理解 Linux 的用户体系并安全地管理系统账户。

---

## 1. 理解 Linux 用户体系

### 用户类型

| 类型 | UID 范围 | 说明 | 示例 |
|------|----------|------|------|
| root | `0` | 超级管理员，无权限限制 | `root` |
| 系统用户 | `1-999` (Ubuntu) / `1-499` (CentOS 7) | 运行系统服务 | `daemon`、`sshd`、`nobody` |
| 普通用户 | `1000+` | 日常登录用户 | `alice`、`bob` |

### 核心配置文件

有三个文件构成了 Linux 用户管理的核心数据库：

```bash
# 用户账户信息（所有用户可读）
$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
alice:x:1000:1000:Alice,,,:/home/alice:/bin/bash

# 格式：用户名:密码占位符:UID:GID:描述:家目录:登录Shell
```

```bash
# 密码哈希（仅 root 可读）
$ sudo cat /etc/shadow
root:$y$j9T$xxx:19846:0:99999:7:::
alice:$y$j9T$yyy:19846:5:90:7:3::

# 格式：用户名:加密密码:上次修改日:最小天数:最大天数:警告天数:不活跃天数:过期日:保留
```

```bash
# 用户组信息
$ cat /etc/group
root:x:0:
sudo:x:27:alice
alice:x:1000:

# 格式：组名:组密码:GID:组成员列表
```

> [!tip]
> `/etc/passwd` 中的密码字段统一用 `x` 占位，真正的密码哈希存放在 `/etc/shadow`。这种分离设计确保普通用户无法读取他人的密码哈希，提升安全性。

---

## 2. 用户账户管理

### 2.1 创建用户

```bash
# 最基本创建（自动分配 UID、创建家目录、默认 Shell）
sudo useradd bob

# 创建用户时指定常用参数（推荐方式）
sudo useradd -m -s /bin/bash -G sudo,docker -c "Bob Smith" bob
```

**`useradd` 常用选项：**

| 选项 | 含义 | 示例 |
|------|------|------|
| `-m` | 创建家目录 `/home/用户名` | `useradd -m bob` |
| `-s` | 指定登录 Shell | `useradd -s /bin/zsh bob` |
| `-G` | 附加用户组（逗号分隔） | `useradd -G sudo,docker bob` |
| `-c` | 用户描述（通常是全名） | `useradd -c "Bob Smith" bob` |
| `-u` | 指定 UID | `useradd -u 2000 bob` |
| `-g` | 指定主组 | `useradd -g staff bob` |
| `-e` | 账户过期日期（YYYY-MM-DD） | `useradd -e 2027-12-31 bob` |

> [!tip]
> Debian/Ubuntu 系统建议用 `adduser`（交互式，自动创建家目录和设置密码），RHEL/CentOS 系 `useradd` 和 `adduser` 是同一条命令。

```bash
# Ubuntu/Debian 交互式创建
sudo adduser bob
# 会自动创建家目录、设置密码，交互式填写用户信息
```

### 2.2 修改用户

```bash
# 修改用户名
sudo usermod -l bob_new bob

# 修改主组
sudo usermod -g staff bob

# 添加用户到附加组（保留已有组，追加）
sudo usermod -aG docker bob

# 锁定账户（禁止登录）
sudo usermod -L bob

# 解锁账户
sudo usermod -U bob

# 修改家目录
sudo usermod -d /data/bob -m bob

# 修改账户过期时间
sudo usermod -e 2027-06-30 bob
```

> [!warning]
> `usermod -G` 如果不加 `-a`，会**替换**用户的全部附加组，导致用户脱离 sudo 等关键组。**永远用 `-aG` 追加，而非单独的 `-G`。**

### 2.3 删除用户

```bash
# 删除用户（保留家目录和邮件池）
sudo userdel bob

# 删除用户及其家目录、邮件池
sudo userdel -r bob

# 强制删除（即使用户还在登录中）
sudo userdel -f bob
```

| 选项 | 含义 | 风险 |
|------|------|------|
| （无） | 仅删除账户记录 | 残留家目录和文件 |
| `-r` | 同时删除家目录和邮件池 | ⚠️ 确认无重要数据 |
| `-f` | 强制删除 | ⚠️ 可能删除正在运行进程的文件 |

> [!warning]
> 删除用户前先用 `find / -user bob` 检查该用户拥有的文件，特别是 `/var/www`、`/opt` 等非家目录位置的业务数据。

---

## 3. 密码管理

### 3.1 设置与修改密码

```bash
# 设置或修改密码（交互式）
sudo passwd bob

# 强制用户在下次登录时修改密码
sudo passwd -e bob

# 锁定密码（密码认证不可用，但 SSH 密钥仍可登录）
sudo passwd -l bob

# 解锁密码
sudo passwd -u bob

# 查看密码状态
sudo passwd -S bob
# bob P 05/15/2026 0 99999 7 -1
#   ↑ 状态码: P=可用, L=锁定, NP=无密码
```

### 3.2 密码老化策略

使用 `chage` 管理密码有效期：

```bash
# 交互式修改密码老化信息
sudo chage bob

# 设置密码最长有效期（90 天后必须修改）
sudo chage -M 90 bob

# 设置密码最短有效期（1 天内不能修改）
sudo chage -m 1 bob

# 设置密码过期前警告天数
sudo chage -W 7 bob

# 设置账户过期日期
sudo chage -E 2027-12-31 bob

# 强制用户下次登录修改密码
sudo chage -d 0 bob

# 查看密码老化信息
sudo chage -l bob
```

**密码老化策略参考：**

| 场景 | `-M` 最大天数 | `-m` 最小天数 | `-W` 警告天数 |
|------|:---:|:---:|:---:|
| 普通员工 | 90 | 1 | 7 |
| 管理员 | 60 | 1 | 7 |
| 测试账户 | 0（不限制） | 0 | 0 |
| 服务账户 | 99999（不限制） | 0 | 0 |

### 3.3 批量处理

```bash
# 从文件批量设置密码（适用于批量创建用户）
echo "bob:初始密码123" | sudo chpasswd

# 更安全的方式：使用 --encrypted 传入已加密密码
# 先通过 openssl 生成加密密码
 openssl passwd -6
Password: 
Verifying - Password: 
$6$xxxx...   ← 复制这个加密串

# 然后批量设置
echo "bob:$6$xxxx..." | sudo chpasswd -e
```

> [!tip]
> 生产环境建议用 `chpasswd` 配合 `--encrypted` 批量设置密码，避免明文密码出现在 Shell 历史中。回车后会卡住是正常的，因为 `openssl passwd` 在等密码输入，输入两遍就能拿到加密串。

---

## 4. 用户组管理

### 4.1 创建与删除组

```bash
# 创建组
sudo groupadd devops

# 创建组并指定 GID
sudo groupadd -g 3000 devops

# 创建系统组（GID < 1000）
sudo groupadd -r app_logs

# 删除组（组内无用户主组时才可删除）
sudo groupdel devops

# 修改组名
sudo groupmod -n devteam devops

# 修改 GID
sudo groupmod -g 3500 devops
```

### 4.2 组成员管理

```bash
# 查看用户所属组
groups bob
# bob : bob sudo docker

# 查看更详细的组信息（含 GID）
id bob
# uid=1000(bob) gid=1000(bob) groups=1000(bob),27(sudo),999(docker)

# 添加用户到组
sudo gpasswd -a bob docker

# 从组中移除用户
sudo gpasswd -d bob docker

# 设置组管理员（可管理组成员）
sudo gpasswd -A alice devops

# 设置组密码（非组成员可通过 newgrp 临时加入）
sudo gpasswd devops
```

> [!tip]
> **组配置最佳实践：**
> - 每个用户有自己的同名私有组（user private group, UPG）—— 这是现代 Linux 的默认行为
> - 权限共享通过**附加组**实现，而非修改主组
> - 项目协作：创建项目组（如 `project_x`），将所有成员加入，目录设置 `chown :project_x` + `chmod g+rw`

---

## 5. 用户信息查询

### 5.1 当前登录用户

```bash
# 查看当前登录的用户
who
# bob      pts/0        2026-07-29 09:15 (192.168.1.100)
# alice    pts/1        2026-07-29 09:20 (192.168.1.101)

# 更详细的登录信息（含登录时间、空闲时间、进程）
w
# 09:30:01 up 10 days,  2:15,  2 users,  load average: 0.08, 0.03, 0.01
# USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU  WHAT
# bob      pts/0    192.168.1.100    09:15    2.00s  0.10s  0.02s vim
# alice    pts/1    192.168.1.101    09:20    5:00   0.05s  0.05s bash

# 查看当前用户是谁
whoami
# bob

# 查看当前用户的完整信息
id
# uid=1000(bob) gid=1000(bob) groups=1000(bob),27(sudo),999(docker)
```

### 5.2 用户登录历史

```bash
# 查看最近登录记录
last
# bob      pts/0    192.168.1.100    Wed Jul 29 09:15   still logged in
# bob      pts/0    192.168.1.100    Tue Jul 28 18:30 - 20:15  (01:45)
# alice    pts/1    192.168.1.101    Tue Jul 28 10:00 - 17:30  (07:30)
# reboot   system boot  6.8.0-35-generic Mon Jul 27 06:00   still running

# 查看登录失败记录（排查暴力破解）
sudo lastb
# bob      ssh:notty  192.168.1.200    Wed Jul 29 03:15 - 03:15  (00:00)
# admin    ssh:notty  192.168.1.200    Wed Jul 29 03:14 - 03:14  (00:00)

# 查看指定用户的登录记录
last bob

# 查看登录失败的尝试次数
sudo lastb | head -20
```

### 5.3 系统用户列表

```bash
# 列出所有普通用户（UID >= 1000）
awk -F: '$3 >= 1000 && $3 < 65534 {print $1, $3, $6}' /etc/passwd

# 列出所有可登录用户（Shell 不是 nologin/false）
grep -v '/usr/sbin/nologin\|/bin/false' /etc/passwd

# 查看当前在线用户数
who | wc -l

# 查看最近 N 条 sudo 执行记录
sudo journalctl -t sudo --no-pager -n 20

# 或查看 /var/log/auth.log
sudo tail -20 /var/log/auth.log
```

### 5.4 类 finger 信息

```bash
# 查看用户详细信息（如果安装了 finger）
finger bob
# Login: bob      			Name: Bob Smith
# Directory: /home/bob            	Shell: /bin/bash
# Office: 3F, +86-13800138000
# Last login Wed Jul 29 09:15 (CST) on pts/0 from 192.168.1.100
# No mail.
```

---

## 6. `sudo` 提权

### 6.1 基本使用

```bash
# 以 root 权限执行命令（需输入当前用户密码）
sudo apt update

# 以指定用户身份执行命令
sudo -u alice whoami
# alice

# 切换到 root Shell（相当于 su -，但使用当前用户密码）
sudo -i

# 仅执行单条命令并退出
sudo -s

# 查看当前用户有哪些 sudo 权限
sudo -l
# Matching Defaults entries for bob on host-server:
#     env_reset, mail_badpass, secure_path=/usr/local/sbin:...
#
# User bob may run the following commands on host-server:
#     (ALL : ALL) ALL
```

### 6.2 配置 sudo

**永远使用 `visudo` 编辑 `/etc/sudoers`，不要直接编辑：**

```bash
# 编辑 sudoers 配置
sudo visudo

# 检查配置文件语法
sudo visudo -c
```

**常用配置示例：**

```bash
# /etc/sudoers 或 /etc/sudoers.d/ 下的文件

# 1. 允许 bob 执行任意命令（输入 bob 密码）
bob ALL=(ALL:ALL) ALL

# 2. 允许 alice 执行任意命令（免密码）
alice ALL=(ALL:ALL) NOPASSWD:ALL

# 3. 允许 devops 组执行 sudo
%devops ALL=(ALL:ALL) ALL

# 4. 限制 docker 组的用户仅能执行 docker 命令
%docker ALL=(ALL) /usr/bin/docker *

# 5. 允许用户仅重启特定服务
bob ALL=(root) /usr/bin/systemctl restart nginx, /usr/bin/systemctl restart php*-fpm

# 6. 允许用户以特定用户身份执行命令
operator ALL=(deploy) /usr/bin/systemctl *, /usr/bin/docker *
```

> [!tip]
> **sudo 最佳实践：**
> - 在 `/etc/sudoers.d/` 下为每个用户或组创建独立文件（如 `10-bob`），方便管理
> - 使用 `NOPASSWD` 要谨慎，仅适用于受信任的自动化账户
> - 精细化授权：`%www /usr/sbin/nginx *` 比 `%www ALL` 安全得多

**sudo 日志审计：**

```bash
# 查看 sudo 执行历史
sudo journalctl -t sudo --no-pager

# 或直接查看
sudo cat /var/log/auth.log | grep sudo
```

---

## 7. `su` 切换用户

```bash
# 切换到 root（加载目标的完整环境，相当于重新登录）
su -

# 切换到其他用户
su - alice

# 不加载目标用户环境（保留当前环境变量）
su alice

# 以其他用户执行单条命令
su -c "whoami" bob
# bob
```

> [!warning]
> `su -` 与 `su` 的区别：
> - `su -` 会加载目标用户的 Shell 环境（家目录、PATH、环境变量），完全切换身份
> - `su` 保留当前环境变量，可能导致命令找不到、路径不对等问题
> - **日常推荐用 `su -`** 避免环境不一致的坑
> - 在现代系统中，**优先用 `sudo -i` 而非 `su -`**，因为不需要知道 root 密码

---

## 8. 实践场景

### 场景 1：创建新开发人员账户

```bash
# 在 Ubuntu 上创建新用户 bob
sudo adduser bob                    # 交互式创建，自动设密码
sudo usermod -aG sudo bob          # 加入 sudo 组
sudo usermod -aG docker bob        # 加入 docker 组
sudo chage -M 90 bob               # 密码 90 天过期
sudo chage -W 7 bob                # 提前 7 天警告

# 验证
id bob
sudo -l -U bob                     # 查看 bob 的 sudo 权限
sudo passwd -S bob                 # 查看密码状态
```

### 场景 2：批量创建学生/测试账户

```bash
#!/bin/bash
# batch_create_users.sh
USERS=("student01" "student02" "student03")
PASSWORD_FILE="/tmp/user_passwords.txt"

> "$PASSWORD_FILE"  # 清空密码文件

for USER in "${USERS[@]}"; do
    PASS=$(openssl rand -base64 12)  # 生成随机密码
    useradd -m -s /bin/bash "$USER"
    echo "$USER:$PASS" | sudo chpasswd
    echo "$USER: $PASS" >> "$PASSWORD_FILE"
    chage -M 180 "$USER"  # 密码 180 天过期
done

echo "批量创建完成，密码保存在 $PASSWORD_FILE"
sudo chmod 600 "$PASSWORD_FILE"      # 仅 root 可读
```

### 场景 3：创建仅 SFTP 访问的受限用户

```bash
# 创建只能 SFTP 上传文件、不能 SSH 登录的用户
sudo useradd -m -s /usr/sbin/nologin uploader
sudo passwd uploader

# 配置 sshd 限制（在 /etc/ssh/sshd_config 末尾追加）
sudo tee -a /etc/ssh/sshd_config << 'EOF'

Match User uploader
    ForceCommand internal-sftp
    ChrootDirectory /home/uploader
    PermitTunnel no
    AllowAgentForwarding no
    AllowTcpForwarding no
    X11Forwarding no
EOF

sudo systemctl restart sshd

# 设置目录权限（ChrootDirectory 必须归 root 所有）
sudo chown root:root /home/uploader
sudo chmod 755 /home/uploader
sudo mkdir -p /home/uploader/uploads
sudo chown uploader:uploader /home/uploader/uploads
```

### 场景 4：锁定离职员工账户

```bash
# 1. 立即锁定密码
sudo passwd -l bob

# 2. 强制退出当前会话
sudo pkill -u bob

# 3. 备份家目录
sudo tar czf /backup/bob_$(date +%Y%m%d).tar.gz /home/bob

# 4. 设置为 30 天后自动过期
sudo chage -E "$(date -d '+30 days' +%Y-%m-%d)" bob

# 5. 检查 bob 拥有的所有文件
find / -user bob -type f 2>/dev/null | head -20
# 将这些文件转移给其他用户或 root
sudo find / -user bob -type f -exec chown alice:alice {} \; 2>/dev/null

# 6. 30 天后确认无误再删除
# sudo userdel -r bob
```

---

## 9. 常见问题

### 9.1 用户无法执行 sudo

```bash
# 检查用户是否在 sudo 组中
groups bob

# 如果不在，添加
sudo usermod -aG sudo bob

# 检查 sudoers 配置
sudo -l -U bob
```

### 9.2 SSH 密钥登录导致密码策略失效

`passwd -e`（强制过期）和 `chage` 策略仅影响**密码认证**。如果用户只用 SSH 密钥登录，密码过期不影响其登录。

```bash
# 强制同时要求密钥 + 密码（双重认证）
# 编辑 /etc/ssh/sshd_config
AuthenticationMethods publickey,password
sudo systemctl restart sshd
```

### 9.3 删除用户时 "user is currently used by process"

```bash
# 查找该用户运行的进程
ps -u bob

# 终止所有进程
sudo pkill -u bob

# 或强制删除
sudo userdel -f bob
```

### 9.4 UID 冲突

```bash
# 查找系统中是否有重复 UID
awk -F: '{print $3}' /etc/passwd | sort -n | uniq -d

# 如果冲突，修改其中一个用户的 UID（同时更新其文件所有权）
sudo usermod -u 2001 bob
sudo find / -user 1000 -exec chown -h 2001 {} \; 2>/dev/null
```

---

> [!summary]
> **核心命令速查：**
>
> | 操作 | 命令 |
> |------|------|
> | 创建用户 | `sudo useradd -m -s /bin/bash bob` |
> | 删除用户 | `sudo userdel -r bob` |
> | 修改密码 | `sudo passwd bob` |
> | 锁定用户 | `sudo passwd -l bob` |
> | 查看用户 | `id bob` / `who` / `w` |
> | 登录历史 | `last` / `sudo lastb` |
> | 提权执行 | `sudo -i` / `sudo -u user cmd` |
> | 切换用户 | `su - bob` |
> | 密码策略 | `sudo chage -M 90 bob` |
> | 添加用户到组 | `sudo usermod -aG docker bob` |
> | 查看组信息 | `groups bob` |

> [!tip]
> **学习路径建议：** 结合 [[linux常用命令/Linux 权限管理基础]] 一起学习，用户管理解决"谁可以访问"，权限管理解决"可以做什么"，两者共同构成 Linux 访问控制体系。
