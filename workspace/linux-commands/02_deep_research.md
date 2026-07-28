# Linux常用命令 - 深度研究资料

收集时间: 2026-07-28
搜索关键词: 文件操作、文本处理(grep/sed/awk)、进程管理(ps/top/systemctl)、
网络诊断(ping/curl/ss/tcpdump)、权限管理(chmod/chown)、磁盘管理(df/du)、包管理(apt/dnf)、Shell基础

---

## 一、文件与目录操作命令

### ls — 列出目录内容

| 选项 | 说明 |
|------|------|
| `-l` | 长格式，显示权限、链接数、所有者、大小、修改时间 |
| `-a` | 显示所有文件（包括以 `.` 开头的隐藏文件） |
| `-h` | 人类可读的文件大小（配合 `-l` 使用） |
| `-R` | 递归列出子目录 |
| `-t` | 按修改时间排序（最新在前） |
| `-S` | 按文件大小排序（最大在前） |
| `-d` | 列出目录本身而非内容 |

**常用组合**:
```bash
ls -lh       # 长格式 + 人类可读大小
ls -lrt      # 按时间倒序（最新在最后），方便看最近修改的文件
ls -la       # 显示所有文件（含隐藏文件）
```

### cp — 复制文件/目录

| 选项 | 说明 |
|------|------|
| `-r` | 递归复制目录 |
| `-i` | 覆盖前提示 |
| `-b` | 覆盖前创建备份（文件名加 `~` 后缀） |
| `-p` | 保留文件属性（权限、时间戳等） |
| `-v` | 显示复制过程 |

### mv — 移动/重命名

```bash
mv oldname newname    # 重命名
mv file dir/          # 移动文件到目录
mv -i file target     # 覆盖前提示
mv file1 file2 dir/   # 移动多个文件
```

### rm — 删除

```bash
rm file               # 删除文件
rm -r dir/            # 递归删除目录
rm -f file            # 强制删除（不提示）
rm -rf dir/           # ⚠️ 递归强制删除（危险！）
```

### find — 查找文件

```bash
find . -name "*.txt" -type f              # 查找所有 txt 文件
find . -name "*docs*" -type d             # 查找名为 docs 的目录
find . -name "*.log" -mtime +7 -delete    # 删除 7 天前的 .log 文件
find . -name "*.gz" -mtime +7 -exec rm -f {} \;  # 查找并处理
find . -maxdepth 2 -name "*.py"           # 限制搜索深度
```

### tar — 归档压缩

```bash
tar -cvf archive.tar dir/        # 创建归档
tar -xvf archive.tar             # 解包
tar -zcvf archive.tar.gz dir/    # 创建 gzip 压缩归档
tar -zxvf archive.tar.gz         # 解压 gzip 归档
tar -tvf archive.tar             # 查看归档内容（不提取）
tar -zxvf file.tar.gz -C /path   # 解压到指定目录
```

### 通配符

| 模式 | 含义 |
|------|------|
| `*` | 匹配任意字符 |
| `?` | 匹配单个字符 |
| `[abc]` | 匹配集合中任一字符 |
| `[a-z]` | 匹配范围中任一字符 |

---

## 二、文本处理三剑客：grep、sed、awk

### grep — 文本搜索

| 选项 | 说明 |
|------|------|
| `-i` | 忽略大小写 |
| `-v` | 反向匹配（显示不匹配的行） |
| `-n` | 显示行号 |
| `-c` | 计数匹配行数 |
| `-r` / `-R` | 递归搜索目录 |
| `-E` | 扩展正则表达式（或直接用 `egrep`） |
| `--color` | 高亮匹配内容 |

**示例**:
```bash
grep "error" /var/log/syslog                          # 搜索关键词
grep -ri "config" /etc/nginx/                         # 递归搜索目录
tail -f app.log \| grep --color 'ERROR'                # 实时过滤日志
grep -E "error\|fail\|warning" log.txt                 # 多模式匹配
ps aux \| grep nginx \| grep -v grep                   # 查找进程（排除自身）
```

### sed — 流编辑器

| 选项 | 说明 |
|------|------|
| `-i` | 原地编辑文件（直接修改） |
| `-n` | 静默模式，仅打印被 `p` 标记的行 |

**示例**:
```bash
sed 's/old/new/g' file.txt              # 替换所有 old 为 new（输出到 stdout）
sed -i 's/foo/bar/g' config.yaml        # 原地替换
sed -i '/^#/d' file.txt                  # 删除所有注释行
sed -n '10,20p' file.txt                 # 打印 10-20 行
sed 's/^/  /' file.txt                   # 每行前加两个空格缩进
sed -n '/ERROR/,/END/p' log.txt         # 打印从 ERROR 到 END 之间的行
```

### awk — 结构化文本分析

**内置变量**: `$0`(整行), `$1`..`$N`(各列), `NF`(列数), `NR`(行号), `FS`(字段分隔符)

```bash
awk '{print $1, $NF}' file.txt          # 打印首列和末列
awk -F: '{print $1, $3}' /etc/passwd   # 以 : 为分隔符
awk '$5 > 100 {print $0}' data.txt     # 条件过滤
awk '{sum += $1} END {print sum}' data.txt       # 求和
awk '{sum += $1} END {print sum/NR}' data.txt    # 求平均值
ls -l \| awk '{print $5, $9}'           # 打印文件大小和名称
```

### 管道组合实战

```bash
# 统计 access.log 中各路径 404 次数
grep '404' access.log \| awk '{print $7}' \| sort \| uniq -c \| sort -nr

# 找到并杀掉 nginx 进程
ps aux \| grep nginx \| awk '{print $2}' \| xargs kill

# 找出最大的 5 个文件
du -sh ./* \| sort -rh \| head -5

# 统计 .py 文件行数
find . -name "*.py" -type f \| xargs wc -l \| tail -1
```

### cut、sort、uniq

```bash
cut -d',' -f1,3 data.csv               # 提取 CSV 第1、3列
sort -k2 -n scores.txt                  # 按第2列数字排序
sort file.txt \| uniq                   # 去重（需先排序）
sort file.txt \| uniq -c \| sort -nr    # 统计频率
```

---

## 三、系统管理与进程监控

### ps — 进程快照

```bash
ps aux                   # 所有进程详细信息（BSD 风格）
ps -ef                   # 所有进程（标准风格）
ps aux --sort=-%cpu      # 按 CPU 使用率排序
ps aux --sort=-%mem      # 按内存使用率排序
ps -ejH                  # 进程树
ps -p PID -o pid,pcpu,pmem,comm  # 查询特定进程
```

**进程状态码**: R(运行), S(睡眠), D(不可中断), Z(僵尸), T(停止)

### top/htop — 实时监控

**top 交互快捷键**:
| 键 | 功能 |
|------|--------|
| `P` | 按 CPU 排序 |
| `M` | 按内存排序 |
| `N` | 按 PID 排序 |
| `k` | 杀掉指定进程 |
| `r` | 修改进程优先级 (renice) |
| `1` | 展开/折叠每个 CPU 核心 |
| `q` | 退出 |

**htop** 是 top 的增强版，支持颜色、鼠标操作、树状视图，更直观。

### kill / pkill — 终止进程

```bash
kill PID                 # 默认发送 SIGTERM (15)，请求正常终止
kill -9 PID              # SIGKILL (9)，强制终止
kill -15 PID             # SIGTERM，安全终止
pkill nginx              # 按进程名终止
killall nginx            # 终止所有同名进程
```

### systemctl — systemd 服务管理

| 命令 | 说明 |
|------|------|
| `systemctl start svc` | 启动服务 |
| `systemctl stop svc` | 停止服务 |
| `systemctl restart svc` | 重启服务 |
| `systemctl reload svc` | 重载配置（不重启） |
| `systemctl status svc` | 查看服务状态 |
| `systemctl enable svc` | 设置开机自启 |
| `systemctl disable svc` | 禁止开机自启 |
| `systemctl list-units --type=service` | 列出所有服务 |

### journalctl — 日志查询

```bash
journalctl -u nginx                  # 查看 nginx 服务日志
journalctl -u nginx -f               # 实时跟踪 nginx 日志
journalctl -u ssh --since "1 hour ago"  # 最近1小时日志
journalctl -xn                       # 查看最近错误日志
```

### 后台作业控制

```bash
command &                # 后台运行
Ctrl+Z                   # 暂停前台进程
jobs                     # 列出后台作业
fg %1                    # 将作业 1 调到前台
bg %1                    # 在后台继续运行暂停的作业
nohup command &          # 退出终端后继续运行
disown %1                # 将作业从 shell 分离
```

---

## 四、网络诊断与调试

### ping — 连通性测试

```bash
ping -c 4 example.com                      # 发 4 个包
ping -c 4 -s 1472 example.com              # 指定包大小（MTU 测试）
ping -c 4 -i 0.2 example.com               # 每 0.2 秒发一个
```

### ss — 套接字统计（netstat 替代品）

| 选项 | 说明 |
|------|------|
| `-t` | TCP 套接字 |
| `-u` | UDP 套接字 |
| `-l` | 仅监听状态 |
| `-n` | 数字格式（不解析名称） |
| `-p` | 显示进程名/PID |

```bash
ss -tlnp                   # 所有 TCP 监听端口（含进程）
ss -ulnp                   # 所有 UDP 监听端口
ss -tnp state established  # 已建立的连接
ss -tlnp \| grep :80       # 检查 :80 端口是否在监听
```

### curl — HTTP/HTTPS 测试

```bash
curl https://example.com                      # GET 请求
curl -I https://example.com                    # 仅查看响应头
curl -v https://example.com                    # 详细输出（含 TLS 握手）
curl -L https://example.com                    # 跟随重定向
curl -o output.zip https://example.com/file    # 下载文件

# HTTP 耗时分析
curl -o /dev/null -s -w "\
DNS: %{time_namelookup}s\n\
TCP: %{time_connect}s\n\
TLS: %{time_appconnect}s\n\
TTFB: %{time_starttransfer}s\n\
Total: %{time_total}s\n\
Status: %{http_code}\n" https://example.com
```

### tcpdump — 抓包分析

```bash
sudo tcpdump -i eth0 -n                     # 监听 eth0 网卡
sudo tcpdump -i any -n port 80              # 监听 80 端口
sudo tcpdump -i eth0 -n host 10.0.0.5       # 过滤特定主机
sudo tcpdump -i eth0 -n 'port 80 and host 10.0.0.5'  # 组合过滤
sudo tcpdump -i eth0 -n -w capture.pcap     # 保存到文件
sudo tcpdump -r capture.pcap                # 读取文件分析
sudo tcpdump -i eth0 -A -n port 80          # ASCII 输出（看 HTTP 内容）
```

**TCP 标志解读**: `[S]`=SYN, `[S.]`=SYN-ACK, `[.]`=ACK, `[R]`=RST, `[F]`=FIN
- SYN 无 SYN-ACK → 防火墙 DROP
- SYN → SYN-ACK → RST → 端口无监听
- SYN → SYN-ACK → ACK → 连接成功

### 其他网络工具

```bash
dig +short example.com                     # DNS 查询
traceroute example.com                     # 路由追踪
ip a                                      # 查看 IP 地址（替代 ifconfig）
ip route show                              # 查看路由表（替代 route -n）
nc -zv host port                           # 端口可达性检测
```

### 网络排查流程

```
1. dig → DNS 解析是否正常
2. ping → 主机是否可达
3. ss -tlnp → 端口是否在监听
4. curl -v → HTTP 服务是否正常
5. tcpdump → 抓包分析网络层问题
6. journalctl → 查看系统/服务日志
```

---

## 五、权限管理

### chmod — 修改文件权限

**数字模式**（r=4, w=2, x=1）:

| 权限 | 数字 | 说明 |
|------|:----:|------|
| `rwx------` | 700 | 仅所有者可读写执行 |
| `rw-r--r--` | 644 | 文件默认权限 |
| `rwxr-xr-x` | 755 | 脚本/目录默认权限 |
| `rw-------` | 600 | 私密文件 |
| `rwxrwxrwx` | 777 | ⚠️ 全开放（不安全） |

```bash
chmod 755 script.sh        # 数字模式
chmod u+x script.sh        # 符号模式：为所有者加执行权限
chmod g-w file.txt         # 移除组的写权限
chmod o=r file.txt         # 其他人只读
chmod -R 755 dir/          # 递归修改目录
```

**特殊权限**:
```bash
chmod u+s file    # SUID (4xxx) — 以文件所有者身份执行
chmod g+s dir     # SGID (2xxx) — 目录下新文件继承组
chmod +t dir      # Sticky Bit (1xxx) — 防删除，如 /tmp
```

### chown — 修改所有者

```bash
chown user file.txt              # 修改所有者
chown user:group file.txt        # 同时修改所有者和组
chown :group file.txt            # 仅修改组
chown -R user:group dir/         # 递归修改
```

### umask — 默认权限掩码

当前 umask 值（如 `022`）从最大默认权限中减去：
- 文件：`666 - 022 = 644`（`rw-r--r--`）
- 目录：`777 - 022 = 755`（`rwxr-xr-x`）

---

## 六、磁盘存储管理

### df — 查看磁盘空间

```bash
df -h         # 人类可读格式
df -h .       # 当前目录所在分区
df -hT        # 显示文件系统类型
df -i         # 查看 inode 使用情况
```

### du — 查看目录大小

```bash
du -sh dir/               # 目录总大小
du -sh * \| sort -rh       # 当前目录下所有项目按大小排序
du -h --max-depth=1       # 仅一层深度
```

### 磁盘分区与挂载

```bash
fdisk -l                      # 查看分区表
lsblk                         # 查看块设备
mount /dev/sdb1 /mnt/data     # 挂载分区
umount /mnt/data              # 卸载
mkfs.ext4 /dev/sdb1           # 格式化为 ext4
```

---

## 七、包管理

### apt (Debian/Ubuntu)

| 命令 | 说明 |
|------|------|
| `apt update` | 更新软件包列表 |
| `apt upgrade` | 升级所有已安装包 |
| `apt install pkg` | 安装包 |
| `apt remove pkg` | 卸载包 |
| `apt purge pkg` | 卸载并清除配置 |
| `apt search keyword` | 搜索包 |
| `apt list --installed` | 列出已安装包 |
| `apt autoremove` | 清理不再需要的依赖 |

### dnf (Fedora/RHEL 8+)

```bash
dnf install pkg          # 安装
dnf remove pkg           # 卸载
dnf update               # 更新系统
dnf search keyword       # 搜索
dnf history undo N       # 回滚事务（dnf 特有）
```

> **注意**: yum 已标记为淘汰，CentOS 8+ 应使用 dnf。

### 其他发行版

```bash
# Arch Linux
pacman -S pkg            # 安装
pacman -R pkg            # 卸载
pacman -Syu              # 同步并更新

# openSUSE
zypper install pkg       # 安装
zypper update            # 更新
```

---

## 八、Shell 基础与组合

### 管道 `|`

将前一个命令的 stdout 接到后一个命令的 stdin：

```bash
command1 | command2 | command3
```

**经典组合**:
```bash
dmesg | less                           # 分页查看内核日志
history | grep "git"                   # 搜索命令历史
ps aux | grep nginx | awk '{print $2}' | xargs kill
```

### 重定向

| 操作符 | 含义 | 示例 |
|--------|------|------|
| `>` | stdout → 文件（覆盖） | `ls > list.txt` |
| `>>` | stdout → 文件（追加） | `echo "log" >> file.log` |
| `2>` | stderr → 文件 | `wc x 2> err.log` |
| `2>&1` | stderr → stdout 相同位置 | `cmd > all.log 2>&1` |
| `&>` | stdout+stderr → 文件 | `cmd &> output.log` |
| `<` | 文件 → stdin | `sort < unsorted.txt` |

### 环境变量

```bash
echo $PATH              # 查看 PATH
export MYVAR="value"    # 设置/导出环境变量
env                     # 查看所有环境变量
unset MYVAR             # 删除变量
```

**关键变量**: `PATH`(命令搜索路径), `HOME`(家目录), `SHELL`(当前 shell), `USER`(用户名)

---

## 综合参考资料

| 主题 | 参考链接 |
|------|---------|
| Linux 命令速查表 (DevOps) | https://last9.io/blog/essential-unix-commands-cheat-sheet/ |
| DevOps 必备 Linux 命令 | https://www.alibabacloud.com/blog/linux-commands-every-devops-engineer-should-have-in-their-back-pocket_602022 |
| 进程管理指南 (2026) | https://dargslan.com/blog/linux-process-management-monitoring-guide |
| 包管理指南 (2026) | https://dargslan.com/blog/linux-package-management-apt-dnf-zypper-guide |
| 文件权限详解 | https://www.strongdm.com/blog/linux-file-permissions |
| 网络故障排查手册 | https://azureossd.github.io/2026/03/12/Basic-Network-Troubleshooting-in-Linux/ |
| Linux 命令综合指南 | https://kelvinintech.hashnode.dev/mastering-linux-one-command-at-a-time-my-linux-study-cheatsheet |
