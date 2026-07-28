---
title: "Linux 进程管理与系统监控"
created: 2026-07-29
updated: 2026-07-29
tags: [linux, 进程管理, systemctl]
status: completed
source_project: linux-commands
---

> [!note]
> 服务器上某个服务突然响应变慢了，是哪个进程占满了 CPU？深夜运行的脚本退出终端后就中断了怎么办？服务挂了该怎么重启？这些问题都绕不开进程管理。本章将系统性地覆盖 Linux 进程查看、实时监控、进程终止、服务管理、日志查询以及后台作业控制，让你能从容应对日常运维中的"进程类"问题。

---

## 4.1 进程基础概念

在动手操作之前，先建立几个关键概念：

**进程（Process）** 是正在执行的程序的实例。你在终端输入 `ls`，Shell 会创建一个进程来执行它，输出结果后进程退出。

**进程的状态**：
| 状态码 | 含义 | 说明 |
|:---:|------|------|
| R | Running | 正在运行或可运行（在运行队列中） |
| S | Sleeping | 正在等待某个事件完成（可中断睡眠） |
| D | Disk Sleep | 不可中断睡眠，通常在等待 I/O |
| Z | Zombie | 僵尸进程，已终止但未被父进程回收 |
| T | Stopped | 已停止（收到 SIGSTOP 或 Ctrl+Z） |

**PID（Process ID）** 是每个进程的唯一编号。你可以把它理解为进程的"身份证号"，后续 `kill`、`renice` 等操作都需要通过 PID 来指定目标进程。

每个进程都有一个父进程，用 `PPID` 标识。整个进程树从 `systemd`（PID 1）开始。查看进程树是理解进程父子关系最直观的方式。

---

## 4.2 ps — 进程快照

`ps`（process snapshot）用来查看当前系统的进程快照——它只显示执行瞬间的进程状态，不会持续更新。

### 两种风格

`ps` 有 BSD 风格和 Unix 风格两种写法，区别在于选项前是否加横线。两种都常用，记住最常见的即可：

```bash
# BSD 风格（选项前不加横线）
ps aux

# Unix 风格（选项前加横线）
ps -ef
```

这两个命令的输出几乎是等价的，都会列出系统中所有进程。

```bash
$ ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 168400 11964 ?        Ss   Jul27   0:30 /sbin/init
root       315  0.0  0.0  28188  3424 ?        Ss   Jul27   0:00 /lib/systemd/systemd-journald
user      1843  0.0  1.2 974252 102048 ?       Ssl  Jul27   0:08 /usr/bin/gnome-shell
user      4500  0.3  0.1 518912 12524 pts/0    Ss+  10:30   0:02 -bash
user      5600  1.2  0.2 425984 20560 ?        Sl   10:45   0:45 /usr/bin/python3 app.py
```

各列含义：
- `USER`：启动进程的用户
- `PID`：进程 ID
- `%CPU`：CPU 使用率
- `%MEM`：内存使用率
- `VSZ` / `RSS`：虚拟内存 / 实际物理内存（KB）
- `TTY`：关联的终端（`?` 表示没有终端）
- `STAT`：进程状态（见上面的状态表）
- `START`：启动时间
- `TIME`：累计占用的 CPU 时间
- `COMMAND`：命令名

### 实用筛选与排序

```bash
# 按 CPU 使用率降序（最耗 CPU 的排前面）
ps aux --sort=-%cpu

# 按内存使用率降序
ps aux --sort=-%mem

# 只看某个用户的进程
ps -u nginx

# 只看某个特定进程
ps -p 1234 -o pid,pcpu,pmem,comm

# 显示进程树（父子关系一目了然）
ps -ejH

# 使用 forest 参数也能看到树状图
ps auxf
```

> [!tip] --sort 的符号含义
> `--sort=-%cpu` 中的减号表示降序（最大的在前）。如果不加减号，默认升序。按 CPU 排序是排查"哪个进程占满了 CPU"的第一步。

**输出示例——按 CPU 排序**：
```bash
$ ps aux --sort=-%cpu | head -5
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
user      5600  1.2  0.2 425984 20560 ?        Sl   10:45   0:45 /usr/bin/python3 app.py
user      1843  0.0  1.2 974252 102048 ?       Ssl  Jul27   0:08 /usr/bin/gnome-shell
...
```

### 用 ps + grep 精确查找进程

这是查找某个进程最经典的组合：

```bash
# 查找 nginx 进程
ps aux | grep nginx

# 排除 grep 自身（grep --color=auto nginx 也会出现在结果中）
ps aux | grep nginx | grep -v grep

# 或者用 pgrep（更简洁）
pgrep nginx
pgrep -l nginx          # 同时显示 PID 和进程名
pgrep -u www-data       # 查找 www-data 用户的进程
```

> [!warning] grep -v grep 的必要性
> 执行 `ps aux | grep nginx` 时，`grep nginx` 本身也是一个进程，它的命令行中包含"nginx"，所以也会被匹配到。用 `grep -v grep` 排除自身。更优雅的方式是用 `pgrep` 或 `pidof`。

---

## 4.3 top / htop — 实时监控

`ps` 是静态快照，而 `top` 是实时更新的进程监控器。

### top 基础操作

直接输入 `top` 进入交互界面：

```bash
top
```

你会看到一个实时刷新的界面，上半部分是系统概览，下半部分是进程列表：

```
top - 11:30:15 up 2 days,  3:45,  3 users,  load average: 0.08, 0.03, 0.01
Tasks: 123 total,   1 running, 122 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.5 us,  0.3 sy,  0.0 ni, 97.1 id,  0.0 wa,  0.0 hi,  0.0 si
MiB Mem :   7864.2 total,   2056.3 free,   3120.5 used,   2687.4 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   4112.3 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 5600 user      20   0  425984  20560  10240 S   1.2   0.3   0:45.23 python3
 1843 user      20   0  974252 102048  38400 S   0.7   1.3   0:08.45 gnome-shell
```

**系统概览解读**：
- **load average**：1/5/15 分钟的平均负载，数值接近 CPU 核心数表示负载高
- **us/sy/id/wa**：用户态 CPU / 内核态 CPU / 空闲 / 等待 I/O 的占比
- **Mem/Swap**：物理内存和交换分区使用情况

### top 的交互快捷键

进入 `top` 后，可以按以下键实时操作：

| 按键 | 功能 |
|------|------|
| `P` | 按 CPU 使用率排序（大写 P） |
| `M` | 按内存使用率排序 |
| `N` | 按 PID 排序 |
| `T` | 按累计 CPU 时间排序 |
| `k` | 杀掉指定进程（会提示输入 PID 和信号） |
| `r` | 修改进程优先级（renice） |
| `1` | 展开/折叠每个 CPU 核心 |
| `c` | 显示完整命令行（不截断） |
| `H` | 切换线程模式（查看进程内各线程） |
| `u` | 只显示指定用户的进程 |
| `q` | 退出 top |

> [!tip] top 的输出持久化
> 如果你想把 top 的瞬间状态保存下来，可以用批处理模式：
> ```bash
> top -b -n 1 > top_snapshot.txt
> ```
> `-b` 是批处理模式（不进入交互界面），`-n 1` 表示只采集一次。

### htop — top 的现代替代品

`htop` 是 `top` 的增强版本，界面更友好，支持鼠标操作和颜色区分。大多数系统需要额外安装：

```bash
# Debian/Ubuntu
sudo apt install htop

# Fedora/RHEL
sudo dnf install htop
```

htop 的优势：
- **彩色显示**：CPU、内存、进程列表用不同颜色区分
- **鼠标操作**：可以直接点击列标题排序、点击进程选择
- **树状视图**：按 `F5` 可看到进程的父子层级
- **垂直/水平滚动**：可以看到更多列信息
- **更直观的 kill 操作**：选中进程后按 `F9` 即可选择发送什么信号

```bash
# 启动 htop（安装后）
htop

# 树状视图模式
htop -t
```

> [!tip] 什么时候用 top，什么时候用 htop
> - **top**：默认已安装，适合快速查看或刚登录的服务器
> - **htop**：体验更好，适合日常开发和维护，前提是你有权限安装它

---

## 4.4 kill / pkill — 进程终止

### 理解 Linux 信号

`kill` 本质不是"杀死"，而是向进程发送信号。进程收到信号后如何处理，取决于信号类型：

| 信号 | 编号 | 含义 | 行为 |
|:---:|:---:|------|:----:|
| SIGTERM | 15 | 请求终止 | 进程可以捕获并优雅退出（默认） |
| SIGKILL | 9 | 强制终止 | 进程无法捕获或忽略，直接杀死 |
| SIGHUP | 1 | 挂起 | 通常让进程重新读取配置 |
| SIGINT | 2 | 中断 | 相当于 Ctrl+C |
| SIGSTOP | 19 | 暂停 | 进程无法捕获，停止运行 |
| SIGCONT | 18 | 继续 | 让暂停的进程继续运行 |

> [!tip] 优先用 SIGTERM，再用 SIGKILL
> SIGTERM（默认信号）让进程有机会清理临时文件、释放资源、保存状态后再退出。SIGKILL 是最后手段——强制杀死可能导致数据损坏或文件残留。

### kill — 按 PID 终止

```bash
# 默认发送 SIGTERM (15)
kill 1234

# 发送不同的信号
kill -15 1234          # SIGTERM —— 请求优雅退出
kill -9 1234           # SIGKILL —— 强制杀死
kill -1 1234           # SIGHUP —— 让进程重载配置

# 检查信号名
kill -l                # 列出所有信号名称和编号
```

### pkill / killall — 按名称终止

```bash
# 按进程名终止（匹配进程名中的任意部分）
pkill nginx            # 终止所有包含 nginx 的进程

# 精确匹配进程名
killall nginx          # 只终止名为 nginx 的进程

# 发送特定信号
pkill -9 python3       # 强制杀死所有 python3 进程

# 确认后再杀（先用 pgrep 确认）
pgrep -l nginx         # 查看匹配的 PID
pkill nginx            # 确认无误后杀死
```

> [!warning] pkill 的匹配规则
> `pkill nginx` 会匹配任何命令行中包含 "nginx" 的进程。先用 `pgrep -l nginx` 确认匹配的是你想杀的目标，尤其是在生产环境中。

### 实战：查找并终止进程的三种方式

```bash
# 方式 1：ps + grep + awk + kill
ps aux | grep python3 | awk '{print $2}' | xargs kill

# 方式 2：pgrep + kill（推荐）
kill $(pgrep -f python3)

# 方式 3：pkill 一条命令
pkill -f python3
```

方式 1 虽然经典但有些冗余。方式 2 和方式 3 更简洁，推荐优先使用。

---

## 4.5 systemctl — systemd 服务管理

现代 Linux 发行版（Ubuntu 16.04+、CentOS 7+、Debian 8+、Fedora）都使用 **systemd** 作为初始化系统和服务管理器。`systemctl` 是操作 systemd 的核心命令。

### 服务的生命周期

```bash
# 启动服务
sudo systemctl start nginx

# 停止服务
sudo systemctl stop nginx

# 重启服务
sudo systemctl restart nginx

# 重载配置（不中断服务，仅重读配置文件）
sudo systemctl reload nginx

# 查看服务状态
sudo systemctl status nginx

# 设置开机自启
sudo systemctl enable nginx

# 禁止开机自启
sudo systemctl disable nginx

# 检查服务是否已启用开机自启
sudo systemctl is-enabled nginx

# 检查服务是否正在运行
sudo systemctl is-active nginx
```

> [!example] systemctl status 的输出解读
> ```bash
> $ sudo systemctl status nginx
> ● nginx.service - A high performance web server and a reverse proxy server
>      Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
>      Active: active (running) since Mon 2026-07-27 09:15:30 CST; 2 days ago
>     Process: 1234 ExecStart=/usr/sbin/nginx -g daemon on; (code=exited, status=0/SUCCESS)
>    Main PID: 1456 (nginx)
>       Tasks: 2 (limit: 2345)
>      Memory: 15.2M
>         CPU: 30.245s
>      CGroup: /system.slice/nginx.service
>              ├─1456 "nginx: master process /usr/sbin/nginx -g daemon on;"
>              └─1457 "nginx: worker process"
> 
> Jul 27 09:15:30 hostname systemd[1]: Starting A high performance web server...
> Jul 27 09:15:30 hostname systemd[1]: Started A high performance web server.
> ```
> 关键信息：**Active** 行告诉你是否在运行及运行了多久；**Main PID** 是主进程 ID；日志尾部展示了最近的启动记录。

### start/restart/reload 的区别

| 操作 | 是否中断服务 | 是否重新读取配置 | 适用场景 |
|------|:---:|:---:|:---------|
| `start` | 未运行才启动 | — | 首次启动或停止后启动 |
| `restart` | 会（完整停+启） | 是 | 更新配置或程序版本 |
| `reload` | 不会（热加载） | 是 | 仅修改了配置文件，无需重启进程 |

> [!tip] 支持 reload 的服务优先用 reload
> 不是所有服务都支持 `reload`。不确定时可以试试，如果服务不支持，systemctl 会提示。不支持时再 `restart`。

### 列出所有服务

```bash
# 列出所有运行中的服务
systemctl list-units --type=service --state=running

# 列出所有服务（包括未运行的）
systemctl list-units --type=service --all

# 列出已启用开机自启的服务
systemctl list-unit-files --type=service --state=enabled

# 列出启动失败的服务
systemctl --failed --type=service
```

---

## 4.6 journalctl — 日志查询

systemd 的另一大组件是 `journald`，它统一管理系统的所有日志。`journalctl` 是查询这些日志的工具。

### 查看特定服务的日志

```bash
# 查看 nginx 服务的日志
sudo journalctl -u nginx

# 实时跟踪日志（类似 tail -f）
sudo journalctl -u nginx -f

# 查看最近 1 小时的日志
sudo journalctl -u nginx --since "1 hour ago"

# 查看从特定时间到现在的日志
sudo journalctl -u nginx --since "2026-07-27 00:00:00" --until "2026-07-27 23:59:59"
```

### 按优先级过滤

```bash
# 只查看错误级别及以上的日志
sudo journalctl -u nginx -p err

# 查看最近 10 条错误
sudo journalctl -u nginx -p err -n 10

# 优先级从低到高：debug, info, notice, warning, err, crit, alert, emerg
```

### 其他常用场景

```bash
# 查看内核日志
sudo journalctl -k

# 查看上次启动后的所有日志
sudo journalctl -b

# 查看上一次启动的日志（排查启动问题）
sudo journalctl -b -1

# 查看最近 20 行日志
sudo journalctl -n 20

# 实时跟踪系统所有日志
sudo journalctl -f
```

> [!example] 排查服务启动失败
> ```bash
> # 一条命令：查看 nginx 最近一次启动失败的原因
> sudo systemctl status nginx       # 看状态和 Main PID
> sudo journalctl -u nginx -n 50    # 看最近 50 行日志
> ```
> 这是排查服务问题的标准两步走：先看服务状态，再看日志详情。

### 日志管理与维护

journalctl 的日志默认持续累积，可能占用较多磁盘空间：

```bash
# 查看当前日志占用的磁盘空间
journalctl --disk-usage

# 只保留最近 500MB 的日志
sudo journalctl --vacuum-size=500M

# 只保留最近 7 天的日志
sudo journalctl --vacuum-time=7d
```

---

## 4.7 后台作业控制

当你通过终端启动一个进程，默认它会"挂"在终端上——你关掉终端，它就被杀了。后台作业控制让你能绕过这一限制。

### & — 后台运行

在命令末尾加上 `&`，让它在后台运行：

```bash
# 前台运行——终端被占用
sleep 30

# 后台运行——终端可以继续用
sleep 30 &
```

```bash
$ sleep 30 &
[1] 12345
$ echo "我还能继续敲命令"
```

Shell 会返回作业编号 `[1]` 和 PID `12345`。

### Ctrl+Z / fg / bg — 前后台切换

```bash
# 正在前台运行的程序，按 Ctrl+Z 暂停
# （假设你在运行 vim 或 top）

# 查看所有后台作业
$ jobs
[1]-  Stopped                 vim
[2]+  Stopped                 top

# 把作业 1 调到前台继续运行
fg %1

# 把作业 2 在后台继续运行（暂停状态 → 运行状态）
bg %2

# fg 不带编号默认回到最近一个被暂停的作业（有 + 标记的那个）
fg
```

> [!tip] jobs 的输出格式
> ```bash
> $ jobs
> [1]-  Running                 sleep 100 &
> [2]+  Stopped                 vim
> ```
> - `[1]` `[2]`：作业编号
> - `+`：当前默认作业（fg/bg 不加编号时操作这个）
> - `-`：上一个当前默认作业
> - `Running` / `Stopped`：作业状态

### nohup — 退出终端也不中断

`&` 只能把进程放到后台，但关掉终端时，后台进程仍然会收到 SIGHUP 信号而终止。`nohup` 的作用就是忽略 SIGHUP 信号：

```bash
# 退出终端后继续运行
nohup python3 long_running_script.py &

# 输出会被重定向到 nohup.out
```

```bash
$ nohup python3 long_running_script.py &
[1] 14680
nohup: ignoring input and appending output to 'nohup.out'
$ exit    # 退出终端
# 重新登录，脚本仍在运行
```

> [!tip] 指定日志文件替代 nohup.out
> ```bash
> nohup python3 app.py > app.log 2>&1 &
> ```
> 这样 stdout 和 stderr 都会写入 `app.log`，避免日志散落在 `nohup.out` 中。

### disown — 从终端分离已运行的进程

如果你忘了用 `nohup` 启动了一个长时间运行的命令，不想等它跑完才关终端，可以用 `disown` 把它从当前 shell 中分离：

```bash
# 启动一个耗时任务
python3 train_model.py &

# 把它从 shell 的作业表中移除
disown %1

# 现在可以安全退出终端了
```

```bash
$ python3 train_model.py &
[1] 15020

$ disown %1
$ jobs
# jobs 列表已为空，进程仍会继续运行
$ exit    # 安全退出
```

### 四种后台运行方式对比

| 方式 | 命令 | 关终端后是否继续 | 使用场景 |
|:----|:-----|:---:|:---------|
| `&` | `cmd &` | 否 | 临时在后台运行，不关终端 |
| `nohup` | `nohup cmd &` | 是 | 生产环境跑长任务 |
| `disown` | `cmd &; disown` | 是 | 忘记用 nohup 时的补救 |
| `tmux/screen` | `tmux new -s session` | 是 | 需要随时 reconnect 的长期任务 |

> [!tip] 生产环境推荐 tmux
> 对于需要长期运行的进程，`nohup` 是最简单的方案，但 **tmux** 或 **screen** 更强大——你可以在 tmux 会话中启动进程，随时重新连接查看输出，甚至是多窗口协作。如果你的服务器上有 tmux，优先用它。

---

## 4.8 实战案例组合

### 案例 1：排查 CPU 飙升

```bash
# 第 1 步：找到最耗 CPU 的进程
ps aux --sort=-%cpu | head -5

# 或者用 top（P 键按 CPU 排序）
top

# 第 2 步：查看该进程的详细信息
ps -p <PID> -o pid,pcpu,pmem,comm,user,etime

# 第 3 步：查看该进程打开了哪些文件
lsof -p <PID>

# 第 4 步：如果是你的进程，判断是否应该杀掉
kill <PID>          # 先发 SIGTERM
# 等几秒看是否退出
kill -9 <PID>       # 不退出的情况下强制杀
```

### 案例 2：重启一个服务并确认

```bash
# 一条命令完成：重启 + 确认状态
sudo systemctl restart nginx && sudo systemctl status nginx

# 如果 status 显示 active (running) 就是重启成功了
# 如果是 failed，用 journalctl 查原因
sudo journalctl -u nginx -n 20 --no-pager
```

### 案例 3：在后台跑一个长任务并安全退出

```bash
# 方案 A：使用 nohup（推荐生产环境）
nohup ./backup.sh > backup.log 2>&1 &
echo $! > backup.pid    # 记录 PID 方便后续管理

# 方案 B：使用 tmux（适合需要回看输出的场景）
tmux new -s backup
./backup.sh
# Ctrl+B, D 分离会话
# 随时 tmux attach -t backup 重新连接
```

### 案例 4：查询昨天某段时间的系统日志

```bash
# 昨天下午 2 点到 4 点的错误日志
sudo journalctl --since "yesterday 14:00" --until "yesterday 16:00" -p err

# 查看这段时间内 nginx 服务的日志
sudo journalctl -u nginx --since "yesterday 14:00" --until "yesterday 16:00"
```

### 案例 5：一键清理系统日志释放空间

```bash
# 查看日志占用
journalctl --disk-usage

# 如果占用过大，保留最近 200MB
sudo journalctl --vacuum-size=200M
```

---

## 本章总结

- **ps** 查看进程快照，`ps aux` 是最常用组合，`--sort=-%cpu` 按 CPU 排序找最耗资源的进程
- **top/htop** 用于实时监控，交互快捷键 `P`（CPU 排序）、`M`（内存排序）、`k`（杀进程）必须记住
- **kill** 默认发 SIGTERM（优雅退出），只有在进程不响应时才用 `kill -9`（强制杀死）
- **systemctl** 管理 systemd 服务：`start/stop/restart/reload/status/enable/disable`
- **journalctl -u 服务名** 查看服务日志，`-p err` 过滤错误级别，`-f` 实时跟踪
- 后台运行：`&` 放入后台但不防终端退出，`nohup` 防终端退出，`disown` 用于补救已运行的进程

## 下一步

进程和服务管理是排查问题的核心技能。下一章我们将转向 **网络诊断与排障**，学习如何用 `ping`、`curl`、`ss`、`tcpdump` 等工具诊断网络连通性问题——这是排查"为什么服务访问不了"这类问题的必备技能。
