---
title: "Linux 远程连接与文件传输"
created: 2026-07-29
updated: 2026-07-29
tags: [linux, SSH, rsync, scp]
status: completed
source_project: linux-commands
---

> [!note]
> 远程连接和文件传输是 Linux 运维的日常操作。从 SSH 远程登录到安全文件复制，从增量同步到端口转发，本章覆盖你在服务器管理中最常用的远程操作命令，帮你高效安全地管理远端机器。

---

## 1. SSH 远程连接

### 1.1 基本连接

```bash
# 使用默认端口（22）连接
ssh user@192.168.1.100

# 指定端口
ssh -p 2222 user@192.168.1.100

# 使用密钥文件登录
ssh -i ~/.ssh/id_rsa user@192.168.1.100

# 以其他用户名登录（当前用户不是 remote 用户时）
ssh bob@192.168.1.100

# 退出连接
exit
# 或 Ctrl+D
```

### 1.2 常用选项

```bash
# 后台运行远程命令（即使断开连接也不中断）
ssh -f user@host "long-running-script.sh"

# 启用压缩（适合慢速网络）
ssh -C user@host

# 详细模式（排查连接问题）
ssh -vvv user@host

# 跳过 host key 检查（首次连接或 IP 变动时，⚠️ 有安全风险）
ssh -o StrictHostKeyChecking=no user@host

# 保持连接存活（防止 SSH 超时断开）
ssh -o ServerAliveInterval=60 user@host

# X11 转发（远程运行 GUI 程序）
ssh -X user@host
xclock  # 远程执行，显示在本机
```

> [!tip]
> 频繁使用的连接可以配置 `~/.ssh/config` 简化：
>
> ```
> # ~/.ssh/config
> Host myserver
>     HostName 192.168.1.100
>     Port 22
>     User bob
>     IdentityFile ~/.ssh/id_rsa
>     ServerAliveInterval 60
> ```
>
> 然后用 `ssh myserver` 即可连接，无需再输完整参数。

### 1.3 在远程执行命令

```bash
# 在远程执行单条命令
ssh user@host "ls -la /var/log"

# 管道远程输出到本地处理
ssh user@host "cat /var/log/syslog" | grep ERROR

# 加载远程环境变量（注意：非登录 Shell 不加载 /etc/profile）
ssh user@host "source ~/.bashrc && python3 script.py"

# 执行多行脚本
ssh user@host << 'EOF'
cd /var/www
git pull
npm install
sudo systemctl reload nginx
EOF
```

> [!warning]
> SSH 执行远程命令时，默认是非登录 Shell，不会加载 `/etc/profile`、`~/.bashrc` 等文件。如果脚本依赖特定环境变量，要么显式 source，要么用 `ssh -t user@host "bash -lc 'command'"`。

### 1.4 SSH 端口转发

```bash
# 本地转发：将本地 8080 转发到远程的 80（访问远程内网 Web）
ssh -L 8080:localhost:80 user@host
# 然后访问 http://localhost:8080

# 远程转发：将远程的 8080 转发到本地的 80（让远程访问本地服务）
ssh -R 8080:localhost:80 user@host
# 在远程服务器上访问 http://localhost:8080 -> 你的本地 80

# 动态转发（SOCKS 代理，浏览器配置后通过远程访问网络）
ssh -D 1080 user@host
# 浏览器设置 SOCKS5 代理 127.0.0.1:1080

# 跳板机转发（通过中继连接内网服务器）
ssh -J jumpuser@jump-host:22 target-user@10.0.1.100
```

> [!tip]
> **端口转发常用场景：**
> - `-L`：访问公司内网的数据库、管理后台（无需 VPN）
> - `-R`：让远程服务器能连接到你的本地开发环境
> - `-D`：全局代理，所有流量从远程服务器出口
> - `-J`：跳板机访问生产环境内网机器
> - 配合 `-N` 不执行命令，只做转发：`ssh -NL 3306:localhost:3306 user@host`

---

## 2. scp — 安全复制

### 2.1 基本用法

```bash
# 本地文件 → 远程
scp file.txt user@host:/home/user/

# 远程文件 → 本地
scp user@host:/home/user/file.txt .

# 本地目录 → 远程（递归）
scp -r ./project/ user@host:/home/user/

# 远程目录 → 本地
scp -r user@host:/var/log/ ./logs/

# 指定端口
scp -P 2222 file.txt user@host:/home/user/
```

### 2.2 常用选项

```bash
# 保持文件属性（时间戳、权限）
scp -p file.txt user@host:/dest/

# 启用压缩（慢速网络场景）
scp -C bigfile.iso user@host:/dest/

# 限制带宽（不占用全部带宽）
scp -l 1000 bigfile.iso user@host:/dest/
# -l 单位是 Kbit/s，1000 = 约 125KB/s

# 显示传输进度
scp -v file.txt user@host:/dest/
```

> [!warning]
> - `scp` 不会自动覆盖目录中的同名目录结构，它会直接覆盖同名文件
> - 默认不保留源文件的 owner/group（保留了也因为在远程没有对应的 UID/GID 而被映射）
> - 大量小文件传输用 `rsync` 比 `scp` 快得多

---

## 3. rsync — 高效增量同步

`rsync` 是文件同步的首选工具，支持增量传输、压缩、权限保留、断点续传。

### 3.1 基本用法

```bash
# 本地 → 本地（备份）
rsync -av /source/ /backup/

# 本地 → 远程（推送）
rsync -av /local/dir/ user@host:/remote/dir/

# 远程 → 本地（拉取）
rsync -av user@host:/remote/dir/ /local/dir/
```

### 3.2 常用选项

```bash
# 归档模式（保留权限、时间戳、递归等）
rsync -av /src/ /dst/
# -a = -rlptgoD（递归 + 保留几乎所有属性）

# 显示进度和速度
rsync -avh --progress /src/ /dst/

# 增量同步（只传输变化部分）
rsync -av --update /src/ /dst/
# --update 仅在目标文件较旧时覆盖

# 删除目标端多余文件（使两端完全一致）
rsync -av --delete /src/ /dst/
# ⚠️ 谨慎使用，确认源端是完整的

# 排除文件和目录
rsync -av --exclude='*.log' --exclude='.git/' /src/ /dst/

# 限速传输
rsync -av --bwlimit=1000 /src/ /dst/
# 单位 KB/s，1000 = 约 1MB/s

# 断点续传（大文件传输中断后继续）
rsync -av --partial /src/ /dst/

# 通过 SSH 连接（默认）
rsync -av -e "ssh -p 2222" /src/ user@host:/dst/
```

### 3.3 实用场景

```bash
# 场景 1：网站/项目部署
rsync -av --delete --exclude='.git/' --exclude='node_modules/' \
  ./dist/ user@host:/var/www/myapp/

# 场景 2：增量日志备份
rsync -av --remove-source-files /var/log/ /backup/logs/
# --remove-source-files 传输后删除源文件（释放空间）

# 场景 3：跨网络大量小文件（比 scp 快数倍）
rsync -av --no-compress user@host:/many-small-files/ ./target/
# 局域网内 --no-compress 可以加速，CPU 不浪费在压缩上

# 场景 4：使用 SSH 密钥文件连接
rsync -av -e "ssh -i ~/.ssh/prod_key -p 2222" /src/ user@host:/dst/

# 场景 5：试运行（看会做什么，不实际执行）
rsync -av --dry-run /src/ user@host:/dst/
```

> [!tip]
> `rsync` 末尾的`/` 很关键：
> - `rsync -av /src/ /dst/`：将 src/ **内容** 同步到 dst/
> - `rsync -av /src /dst/`：将 src **目录本身** 放到 dst/ 下（即 dst/src/）

### 3.4 rsync vs scp

| 特性 | scp | rsync |
|------|:---:|:-----:|
| 增量传输 | ❌ 每次都全量 | ✅ 只传差异部分 |
| 断点续传 | ❌ | ✅ `--partial` |
| 权限保留 | ✅ `-p` | ✅ `-a` 自动 |
| 传输大文件 | ❌ 中断重来 | ✅ 可续传 |
| 慢速网络 | 慢（全量） | 快（增量 + 压缩） |
| 简单传输 | ✅ 命令更短 | ❌ 参数稍多 |
| 删除文件同步 | ❌ | ✅ `--delete` |

---

## 4. sftp — 交互式文件传输

```bash
# 连接（基于 SSH，同端口和密钥）
sftp user@host

# 交互命令
sftp> ls                    # 列出远程目录
sftp> ll                    # 列出本地目录
sftp> pwd                   # 远程当前路径
sftp> lpwd                  # 本地当前路径
sftp> cd /var/log           # 切换远程目录
sftp> lcd /tmp              # 切换本地目录

sftp> get remote_file.txt   # 下载文件
sftp> get -r /remote/dir/   # 下载目录
sftp> put local.txt         # 上传文件
sftp> put -r ./local/dir/   # 上传目录

sftp> rm file.txt           # 删除远程文件
sftp> mkdir new_dir         # 创建远程目录
sftp> rmdir dir             # 删除远程空目录
sftp> chmod 755 script.sh   # 修改远程文件权限
sftp> chown user file.txt   # 修改远程文件所有者

sftp> !ls                   # 执行本地 Shell 命令
sftp> exit                  # 退出
```

> [!tip]
> sftp 相比 scp 的优势是交互式浏览，适合不确定路径时的文件操作。日常脚本自动化推荐 rsync，简单上传下载用 scp，目录浏览和单文件操作用 sftp。

---

## 5. SSH 密钥认证

### 5.1 生成密钥对

```bash
# 生成 RSA 密钥（默认）
ssh-keygen -t rsa -b 4096 -C "bob@example.com"

# 生成 Ed25519 密钥（推荐，更安全更快）
ssh-keygen -t ed25519 -C "bob@example.com"

# 指定输出文件（默认 ~/.ssh/id_rsa）
ssh-keygen -t ed25519 -f ~/.ssh/prod_key -C "prod-server"
```

### 5.2 复制公钥到服务器

```bash
# 一键复制（将本机公钥追加到远程 ~/.ssh/authorized_keys）
ssh-copy-id user@host

# 指定密钥文件和端口
ssh-copy-id -i ~/.ssh/prod_key.pub -p 2222 user@host

# 手动方式（如果远程没有 ssh-copy-id）
cat ~/.ssh/id_ed25519.pub | ssh user@host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### 5.3 SSH 代理（ssh-agent）

避免每次使用密钥时输入密码（passphrase）：

```bash
# 启动 ssh-agent（通常自动启动）
eval "$(ssh-agent -s)"

# 添加密钥（输入一次 passphrase，后续不再询问）
ssh-add ~/.ssh/id_ed25519

# 列出已添加的密钥
ssh-add -l

# 移除所有密钥
ssh-add -D

# 在 Mac/Linux 上自动加载
# 编辑 ~/.ssh/config
# Host *
#     AddKeysToAgent yes
#     UseKeychain yes
```

> [!tip]
> **密钥管理建议：**
> - Ed25519 比 RSA 更安全、速度更快，新系统优先用 `ssh-keygen -t ed25519`
> - 每个服务器或环境生成独立密钥对（如 `prod_key`、`dev_key`）
> - 使用 passphrase（密码短语）保护私钥，配合 ssh-agent 免密使用
> - 定期审计 `~/.ssh/authorized_keys`，移除不需要的密钥

---

## 6. SSH 安全加固

### 6.1 基本安全配置

```bash
# /etc/ssh/sshd_config 关键安全设置

# 禁止 root 直接登录（日常运维通过 sudo）
PermitRootLogin no

# 仅允许密钥认证，禁用密码认证
PasswordAuthentication no
ChallengeResponseAuthentication no

# 限制登录用户（白名单）
AllowUsers bob alice

# 修改默认端口（减少扫描）
Port 2222

# 空闲超时断开（秒）
ClientAliveInterval 300
ClientAliveCountMax 0

# 限制 SSH 登录尝试次数
MaxAuthTries 3
MaxSessions 10

# 禁用不安全的协议和配置
Protocol 2
```

```bash
# 修改后重启服务
sudo systemctl restart sshd
```

> [!warning]
> 修改 SSH 配置时**永远保留一个备用连接**。错误的配置可能导致自己被锁在门外。建议：
> 1. 先在一个终端窗口保持 root 登录
> 2. 在另一个窗口修改配置并重启
> 3. 测试新连接正常后再关闭备用窗口

---

> [!summary]
> **核心命令速查：**
>
> | 操作 | 命令 |
> |------|------|
> | SSH 连接 | `ssh user@host -p 22` |
> | 远程执行命令 | `ssh user@host "command"` |
> | 本地端口转发 | `ssh -L 8080:localhost:80 user@host` |
> | 跳板机 | `ssh -J jump@host1 user@host2` |
> | 复制文件 | `scp file user@host:/path/` |
> | 增量同步 | `rsync -av /src/ user@host:/dst/` |
> | 交互式传输 | `sftp user@host` |
> | 生成密钥 | `ssh-keygen -t ed25519` |
> | 上传公钥 | `ssh-copy-id user@host` |
