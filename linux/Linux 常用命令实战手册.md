---
title: Linux 常用命令实战手册
created: 2026-07-29
updated: 2026-07-29
tags: [linux, command, 运维, 命令行]
status: completed
source_project: linux-commands
---

# Linux 常用命令实战手册

> 上手实操 · 面向有一定基础的开发者

---

## 📖 目录

1. [文件与目录操作基础](#1-文件与目录操作基础)
2. [文件内容查看与搜索](#2-文件内容查看与搜索)
3. [文本处理三剑客实战](#3-文本处理三剑客实战)
4. [进程管理与系统监控](#4-进程管理与系统监控)
5. [网络诊断与排障](#5-网络诊断与排障)
6. [权限管理与安全基础](#6-权限管理与安全基础)
7. [磁盘与存储管理](#7-磁盘与存储管理)
8. [软件包管理](#8-软件包管理)
9. [Shell 实用技巧与命令组合](#9-shell-实用技巧与命令组合)

---


---

> [!note]
> 本章是 Linux 命令实战的起点。你将掌握文件与目录操作中最核心的命令：如何查看、复制、移动、删除、创建文件与目录，以及如何用通配符批量操作和查找文件。这些命令在日常开发和运维中几乎每天都在使用，熟练掌握它们是高效使用 Linux 的第一步。

---

## 1.1 文件列表与查看：ls

`ls` 可能是你接触的第一个 Linux 命令。它的功能很简单——列出目录内容，但配合不同选项能提供非常丰富的信息。

### 基本用法

```bash
ls                    # 列出当前目录的文件和目录名
ls /etc               # 列出指定目录的内容
ls -l                 # 长格式显示（权限、链接数、所有者、大小、修改时间）
ls -a                 # 显示所有文件，包括以 . 开头的隐藏文件
ls -lh                # 长格式 + 人类可读大小（KB/MB/GB）
```

**输出示例**：
```bash
$ ls -lh
total 28K
drwxr-xr-x  2 user user 4.0K Jul 28 10:00 Documents
-rw-r--r--  1 user user  884 Jul 28 09:55 notes.txt
-rwxr-xr-x  1 user user  512 Jul 28 09:50 script.sh
```

每一列的含义从左到右分别是：文件类型与权限、链接数、所有者、所属组、大小、最后修改时间、文件名。

> [!tip] 常用组合
> ```bash
> ls -lrt      # 按修改时间倒序，最新文件在最后，适合看最近改了什么
> ls -la       # 所有文件的详细列表（含隐藏文件）
> ls -d */     # 只列出当前目录下的子目录名称
> ```

### 排序与过滤

```bash
ls -lS          # 按文件大小从大到小排序
ls -ltr         # 按修改时间从旧到新（最新在最后）
ls -R           # 递归列出子目录的所有内容
ls --color=auto # 用颜色区分文件类型（多数系统默认已启用）
```

`ls -lrt` 是最常用的组合之一。为什么要把最新的放在最后？因为当目录文件很多时，你通常想看最近刚修改过的文件，它会在终端的最底部，一眼就能看到。

---

## 1.2 复制与移动：cp / mv

### cp — 复制文件和目录

```bash
cp file.txt /tmp/                    # 复制文件到 /tmp 目录
cp file.txt /tmp/backup.txt          # 复制并重命名
cp -r myapp/ /opt/backups/           # 递归复制整个目录
cp -i file.txt /tmp/                 # 覆盖前提示确认（防止误覆盖）
cp -b file.txt /tmp/                 # 覆盖前自动备份，原文件末尾加 ~
cp -v *.log /var/log/archive/        # 显示每个文件的复制过程
```

> [!warning] cp 的一个重要细节
> 当你用 `cp` 覆盖一个已有文件时，**不会**有任何提示。养成带 `-i`（interactive）的习惯，或者设置别名 `alias cp='cp -i'`，能在覆盖前让你确认。

**复制目录必须用 -r**：
```bash
$ cp myapp /tmp/
cp: omitting directory 'myapp'
$ cp -r myapp /tmp/   # 正确做法
```

### mv — 移动与重命名

`mv` 的语义很直白：把一个路径的文件挪到另一个路径。它同时用于重命名（在同一目录内移动就是改名）。

```bash
mv oldname.txt newname.txt            # 重命名文件
mv file.txt /tmp/                     # 移动文件到 /tmp
mv /tmp/file.txt ./                   # 从 /tmp 移回当前目录
mv -i file.txt /tmp/                  # 覆盖前提示
mv file1.txt file2.txt /tmp/          # 一次移动多个文件到目录
```

> [!tip] mv 不需要 -r
> 和 `cp` 不同，`mv` 移动目录时**不需要**加 `-r`，这是新手最容易混淆的地方。

### 理解 cp 和 mv 的区别

| 操作 | 源文件是否保留 | 需要 -r 用于目录 | 跨文件系统 |
|------|:---:|:---:|:---:|
| cp | 保留 | 是 | 支持 |
| mv | 不保留 | 不需要 | 跨文件系统时实际是 cp + rm |

当你 `mv` 一个文件到不同的文件系统（比如从 `/home` 到 `/tmp`，而它们是不同分区），`mv` 在背后做了 `cp` + `rm` 两件事。这意味着如果文件很大，跨文件系统的 `mv` 会比同文件系统下的 `mv` 慢很多。

---

## 1.3 删除与安全删除：rm

### rm 基础

```bash
rm file.txt            # 删除文件
rm -r mydir/           # 递归删除目录及其内容
rm -f file.txt         # 强制删除（不提示确认）
rm -rf mydir/          # ⚠️ 递归强制删除——最危险的命令
```

`rm` 删除的文件不会进入回收站。一旦删除，通过常规手段无法恢复。

### 为什么 rm -rf 是危险命令

`rm -rf /` 是著名的"删库跑路"命令，它会递归强制删除根目录下的所有内容，导致系统完全瘫痪。现代 Linux 发行版对此有一定保护（需要加 `--no-preserve-root`），但误删重要目录的后果仍然很严重。

> [!warning] 安全删除的四个习惯
> 
> 1. **先用 `ls` 确认**：删除前先 `ls` 看看目标是什么
>    ```bash
>    ls mydir/          # 先看里面有什么
>    rm -r mydir/       # 确认后再删
>    ```
> 
> 2. **多用 `-i` 选项**：让 rm 每次删除都询问
>    ```bash
>    rm -ri mydir/      # 逐文件确认
>    ```
> 
> 3. **用相对路径代替绝对路径**：少用 `rm -rf /some/long/path/`，尽量先 `cd` 到附近再删
> 
> 4. **重要数据先备份**：删除前 `cp -r` 或 `tar` 归档

### rm 的实用技巧

```bash
# 交互式删除，逐文件确认
rm -i *.tmp

# 删除空目录（和 rmdir 等效）
rm -d emptydir/

# 删除文件名以 - 开头的文件（如 -f 会被解析为选项）
rm -- -filename.txt    # -- 表示选项结束
rm ./-filename.txt     # 或用相对路径绕过
```

---

## 1.4 目录操作：mkdir / rmdir

### mkdir — 创建目录

```bash
mkdir mydir                    # 创建单个目录
mkdir -p a/b/c/d               # 递归创建多级目录（父目录不存在时自动创建）
mkdir -p project/{src,docs,test}  # 一次创建多个子目录（花括号展开）
```

`mkdir -p` 是最实用的选项。没有它，你要先 `mkdir a`、再 `mkdir a/b`、再 `mkdir a/b/c`。而 `-p` 一次搞定，且如果目录已存在也不会报错。

> [!example] 花括号展开 + mkdir
> ```bash
> $ mkdir -p project/{src,docs,test}
> $ ls project/
> docs  src  test
> ```
> 这条命令等价于：
> ```bash
> mkdir -p project/src project/docs project/test
> ```

### rmdir — 删除空目录

```bash
rmdir emptydir/       # 只删除空目录
rmdir -p a/b/c/       # 递归删除空目录（c 为空则删 c，然后 b 为空则删 b...）
```

> [!warning] rmdir 的局限
> `rmdir` 只能删除空目录。如果目录里有文件，必须用 `rm -r`。实践中 `rmdir` 用得不多，因为大多数情况下你要删除的目录都不为空。

---

## 1.5 通配符与 Glob 模式

通配符（Wildcard）是 Shell 提供的文件名匹配机制，官方术语叫 **Glob 模式**。它让你可以用一个模式匹配多个文件，是批量操作的基石。

### 核心模式

| 模式 | 含义 | 匹配示例 |
|------|------|---------|
| `*` | 匹配任意长度的任意字符 | `*.txt` 匹配所有 `.txt` 文件 |
| `?` | 匹配单个字符 | `file.?` 匹配 `file.a`、`file.b`，不匹配 `file.ab` |
| `[abc]` | 匹配方括号中的任意一个字符 | `file[0-9].txt` 匹配 `file1.txt`、`file9.txt` |
| `[a-z]` | 匹配指定范围 | `[a-c]*` 匹配以 a、b、c 开头的文件 |
| `[!abc]` | 匹配不在方括号中的任意字符 | `[!0-9]*` 匹配不以数字开头的文件 |

### 实战用法

```bash
# 查看所有 PNG 图片
ls *.png

# 删除所有 .tmp 临时文件
rm *.tmp

# 复制所有 .config 文件
cp *.config /backup/

# 匹配 file1.txt ~ file9.txt
ls file[0-9].txt

# 匹配以字母开头、后跟两位数字的文件
ls [a-zA-Z][0-9][0-9].log

# 匹配不以 tmp 开头的文件
ls [!t]*
```

### 理解 Glob 展开时机

```bash
# 先创建一些测试文件
touch a.txt b.txt c.txt

# Shell 会把 *.txt 展开成 a.txt b.txt c.txt
# 然后传给 ls 命令
ls *.txt
# 等价于
ls a.txt b.txt c.txt

# 验证展开结果
echo *.txt
# 输出: a.txt b.txt c.txt
```

> [!tip] 星号 * 不匹配隐藏文件
> `*` 不能匹配以 `.` 开头的隐藏文件。要匹配隐藏文件，需显式指定 `.*`：
> ```bash
> ls *       # 只显示非隐藏文件
> ls .*      # 只显示隐藏文件（包括 . 和 ..）
> ls -la     # 显示所有文件
> ```

### 花括号展开（Brace Expansion）

花括号展开不是严格意义上的 Glob，但它和通配符搭配使用非常强大：

```bash
# 批量创建文件
touch {a,b,c}.txt       # 创建 a.txt b.txt c.txt

# 批量创建目录结构
mkdir -p src/{main,test}/{java,resources}

# 备份文件
cp config.yml{,.bak}    # 等价于 cp config.yml config.yml.bak
```

---

## 1.6 文件查找：find / locate

当你需要在一个大型项目中找到某个文件时，`ls` 就不够用了。这时需要 `find` 或 `locate`。

### find — 查找并处理文件

`find` 的核心用法是：`find <搜索路径> <匹配条件> <处理动作>`

```bash
# 按文件名查找
find . -name "*.txt"                    # 当前目录下所有 .txt 文件
find /var/log -name "*.log"            # /var/log 下所有 .log 文件

# 按文件类型过滤
find . -type f                          # 只查文件（不包含目录）
find . -type d                          # 只查目录
find . -type l                          # 只查符号链接

# 按大小过滤
find . -size +100M                      # 大于 100MB 的文件
find . -size -1k                        # 小于 1KB 的文件

# 按时间过滤（mtime = 修改时间）
find . -mtime +7                        # 7 天前修改的文件
find . -mtime -1                        # 最近 1 天内修改的文件
find . -mmin -30                        # 最近 30 分钟内修改的文件

# 限制搜索深度
find . -maxdepth 2 -name "*.py"         # 最多往下两层

# 找到后执行操作
find . -name "*.tmp" -delete            # 找到后直接删除
find . -name "*.log" -exec rm -f {} \;  # 找到后执行命令（{} 代表每个匹配结果）
find . -name "*.py" -exec wc -l {} +    # + 表示批量传给命令（效率更高）
```

> [!tip] -exec 的两种结束写法
> - `\;` ：每个匹配的文件单独执行一次命令
> - `+`  ：所有匹配的文件合并成一次命令调用
> ```bash
> # \;：每个文件执行一次 ls -l（文件多时慢）
> find . -type f -exec ls -l {} \;
> 
> # +：等价于 ls -l file1 file2 file3 ...（效率高）
> find . -type f -exec ls -l {} +
> ```

### locate — 快速查找（基于数据库）

相比 `find` 遍历目录树，`locate` 基于预建立的数据库进行搜索，速度极快：

```bash
locate nginx.conf                    # 查找 nginx.conf（秒出结果）
locate -i README                     # 忽略大小写查找
locate -c "*.py"                     # 只统计匹配数量，不列出文件

# 更新数据库（新安装的文件可能查不到）
sudo updatedb                        # 刷新 locate 的数据库
```

> [!warning] locate 的局限
> - `locate` 的数据库通常每天自动更新一次。新创建的文件可能搜不到，需要手动 `sudo updatedb`
> - 它依赖系统权限，可能不会显示你没有权限访问的文件
> - 它不适用于实时文件系统状态检查

### find vs locate 选择指南

| 场景 | 用哪个 | 原因 |
|------|--------|------|
| 按文件名、大小、时间精确查找 | find | 条件灵活，实时搜索 |
| 快速搜索整个系统 | locate | 速度极快，适合"我知道文件名"的场景 |
| 找到后执行操作（删除、统计等） | find | 内置 -exec 和 -delete |
| 搜索刚创建的文件 | find | locate 数据库可能滞后 |
| 在脚本中使用 | find | 行为可预测，不依赖数据库更新 |

---

## 1.7 实战案例组合

### 案例 1：清理 30 天前的日志文件

```bash
# 找到 /var/log 下 30 天前的 .log 文件，压缩归档后删除
find /var/log -name "*.log" -mtime +30 -exec gzip {} \;
# 然后删除 .gz 文件是否需要？这里只演示搭配使用
```

### 案例 2：备份配置文件

```bash
# 复制所有 .conf 文件到备份目录，保留目录结构
find /etc -name "*.conf" -exec cp --parents {} /backup/ \;
```

### 案例 3：批量重命名

```bash
# 把所有 .txt 改为 .md（借助 Shell 循环）
for f in *.txt; do
    mv "$f" "${f%.txt}.md"
done
```

### 案例 4：一键创建项目目录结构

```bash
mkdir -p myproject/{src/{main,test}/{java,resources},docs,scripts,config}
# 创建完成后
ls -R myproject/
```

---

## 本章总结

- **ls** 是文件查看的起点，`-l`（长格式）、`-a`（含隐藏）、`-t`（按时间排序）、`-h`（可读大小）是最常用的选项组合
- **cp 需要 `-r` 才能复制目录**，而 **mv 不需要**；两者都建议加 `-i` 防止误覆盖
- **rm -rf 极度危险**，删除前先 `ls` 确认，养成安全删除的习惯
- **mkdir -p** 可以递归创建多级目录，是最实用的选项
- **通配符（Glob）** 是批量操作的基础：`*` 匹配任意、`?` 匹配单字符、`[abc]` 匹配集合
- **find** 灵活但慢，适合精确查找和后续操作；**locate** 极快但数据库可能滞后

## 下一步

在掌握了文件和目录的基本操作后，第二章将深入 **文件内容查看与搜索**，学习如何用 `cat`、`less`、`head`、`tail` 查看文件内容，以及用 `grep` 搜索文本内容——这些是日志分析和日常排查的必备技能。

---

> [!note]
> 上一章我们学会了如何操作文件和目录本身——列出、复制、移动、删除、查找。但这些操作大多停留在"文件外壳"层面。本章我们正式进入文件内部，学习如何查看文件内容、快速搜索需要的信息、实时跟踪日志变化，以及对比文件差异。这些是诊断问题和理解系统状态的必备技能。

---

## 2.1 文件内容查看：从读到查

Linux 下有多种查看文件内容的命令，各自适用不同场景。选择哪个命令取决于你的目的：是看全部内容、只看开头结尾、还是逐页翻阅。

### 2.1.1 cat —— 快速查看小文件

`cat` 是 "concatenate" 的缩写，本意是连接文件，但最常用的场景就是查看文件内容。

```bash
cat /etc/os-release          # 查看系统发行版信息
cat -n /etc/hosts            # 显示行号
```

**输出示例**：
```bash
$ cat -n /etc/hosts
     1  127.0.0.1  localhost
     2  127.0.1.1  my-machine
     3
     4  # The following lines are desirable for IPv6 capable hosts
     5  ::1        ip6-localhost ip6-loopback
```

> [!tip]
> `cat` 适合查看**短文件**。如果文件超过一屏，内容会一闪而过，这时候用 `less` 更合适。

`cat` 还有一个常用技巧——创建短文件：

```bash
cat > hello.txt << EOF
Hello World
This is a test file.
EOF
```

> [!warning]
> `cat > file` 会**覆盖**已有文件。如果只是想追加内容，用 `cat >> file` 或 `tee -a file`。

### 2.1.2 head / tail —— 查看开头和结尾

大多数时候，你不需要看完整文件，只看开头几行（配置文件头部）或结尾几行（日志最新记录）就够了。

```bash
head -n 10 /etc/passwd        # 查看前 10 行（默认 10）
head -c 100 file.txt          # 查看前 100 个字节

tail -n 20 /var/log/syslog    # 查看最后 20 行
tail -f /var/log/syslog       # 实时跟踪文件新增内容（最常用！）
```

**输出示例**：
```bash
$ head -3 /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
```

> [!tip] `tail -f` 实战场景
> `-f` 代表 `--follow`，它会保持打开文件并持续输出新写入的内容。这是**跟踪日志文件**的标配操作：
> ```bash
> tail -f /var/log/nginx/access.log     # 实时查看 web 访问日志
> tail -f /var/log/nginx/error.log      # 实时查看错误日志
> ```
> 按 `Ctrl+C` 退出跟踪模式。

`tail` 还有一个不常用但很实用的 `-n +N` 语法——从第 N 行开始显示到末尾：

```bash
tail -n +100 bigfile.log    # 从第 100 行开始看到末尾
```

这比用 `less` 翻到第 100 行要快得多。

### 2.1.3 less —— 分页浏览利器

当文件太大无法一屏看完时，`less` 是你的首选。它支持前后翻页、搜索、甚至直接跳转到特定行。

```bash
less /var/log/syslog        # 分页查看系统日志
```

**`less` 内的常用快捷键**：

| 按键 | 功能 |
|------|------|
| `空格` / `f` | 下一页 |
| `b` | 上一页 |
| `j` / `k` | 下/上一行（类似 Vim） |
| `g` | 跳转到文件开头 |
| `G` | 跳转到文件末尾 |
| `/keyword` | 向下搜索关键字 |
| `?keyword` | 向上搜索关键字 |
| `n` / `N` | 下一个 / 上一个匹配结果 |
| `q` | 退出 |

> [!tip] `less` 与管道组合
> `less` 最常见的用法是作为管道终点，让任何命令的长输出都支持分页浏览：
> ```bash
> dmesg | less                    # 分页查看内核日志
> journalctl -u nginx | less      # 分页查看 nginx 服务日志
> ps aux | less                   # 分页查看进程列表
> ```

`less` 相比 `more`（一个更古老的分页命令）的优势是：**支持往回翻页**。`more` 只能前进不能后退，`less` 两者都能做——名字本身就是一个双关语："less is more"。

> [!example] 查看大文件实战
> 假设你有一个 500MB 的日志文件，以下做法不可取：
> ```bash
> cat huge.log    # 终端会卡死，刷屏到天荒地老
> ```
> 正确做法是：
> ```bash
> less huge.log                        # 分页浏览，只加载需要部分
> tail -n 100 huge.log                 # 只看最后 100 行
> grep "ERROR" huge.log | less         # 先过滤再分页查看
> ```

---

## 2.2 内容搜索：grep 实战

`grep` 是 Linux 文本搜索的标配工具，全称 "Global Regular Expression Print"。它能在一行中搜索匹配的模式，并输出匹配的行。

### 2.2.1 基本搜索

```bash
grep "error" /var/log/syslog          # 搜索包含 error 的行
grep -i "error" /var/log/syslog       # 忽略大小写
grep -n "listen" nginx.conf           # 显示行号，方便定位位置
grep -c "404" access.log              # 只统计匹配行数
```

**输出示例**：
```bash
$ grep -n "listen" /etc/nginx/nginx.conf
15:    listen 80;
21:    listen [::]:80;
```

### 2.2.2 常用选项速查

| 选项 | 作用 | 示例 |
|------|------|------|
| `-i` | 忽略大小写 | `grep -i "error" log` |
| `-n` | 显示行号 | `grep -n "config" file` |
| `-c` | 计数匹配行 | `grep -c "404" access.log` |
| `-v` | 反向匹配（排除） | `grep -v "^#" nginx.conf` |
| `-r` / `-R` | 递归搜索目录 | `grep -r "api_key" ./config/` |
| `-E` | 扩展正则 | `grep -E "err|fail|warn" log` |
| `-l` | 只显示文件名 | `grep -l "TODO" *.py` |
| `-w` | 匹配整个单词 | `grep -w "is" file` |
| `--color` | 高亮匹配内容 | `grep --color "error" log` |

> [!warning] `-r` 不要遗忘目标路径
> 初学者常犯的错误是写 `grep -r "keyword"` 而没有指定路径，这样 `grep` 会等待标准输入，导致命令"卡住"。
> ```bash
> # 错误：
> grep -r "config"    # 卡住，等待输入
> # 正确：
> grep -r "config" .  # 在当前目录递归搜索
> ```

### 2.2.3 组合搜索技巧

```bash
# 排除注释和空行，看有效配置
grep -v "^#" /etc/nginx/nginx.conf | grep -v "^$"

# 多模式匹配（同时搜索多个关键词）
grep -E "error|fail|critical" /var/log/syslog

# 在前一个 grep 的基础上进一步筛选
grep "ERROR" app.log | grep "user_id=12345"

# 搜索代码中的 TODO 注释，只显示文件名
grep -rn "TODO" --include="*.py" --include="*.js" .

# 统计日志中各严重级别的分布
grep -c "INFO" app.log
grep -c "WARN" app.log
grep -c "ERROR" app.log
```

> [!example] 实战：快速定位代码中的函数调用
> ```bash
> # 搜索某个函数被哪些文件调用了
> grep -rn "getUserById" --include="*.java" src/
> 
> # 输出示例
> src/service/UserService.java:42:    User user = getUserById(123);
> src/controller/UserController.java:18:    return userService.getUserById(id);
> ```

### 2.2.4 grep 正则表达式入门

grep 支持正则表达式，分为三种模式：

| 模式 | 启用方式 | 说明 |
|------|----------|------|
| 基本正则 | `grep` (默认) | `^` `$` `.` `*` `\` 等基础元字符 |
| 扩展正则 | `grep -E` 或 `egrep` | 加 `+` `?` `\|` `()` 支持 |
| 固定字符串 | `grep -F` 或 `fgrep` | 把所有字符当普通文本，不解析正则 |

```bash
# 基本正则示例
grep "^root" /etc/passwd               # 以 root 开头的行
grep "bash$" /etc/passwd               # 以 bash 结尾的行
grep "error\." log.txt                 # 匹配 error.（转义点号）
grep "[0-9]\{3,5\}" file               # 匹配 3 到 5 位数字

# 扩展正则示例（grep -E）
grep -E "error|fail|warn" log.txt      # 多模式匹配，等价于 error 或 fail 或 warn
grep -E "nginx|apache" /etc/passwd     # 匹配包含 nginx 或 apache 的行
grep -E "^[^#]" config.conf            # 不以 # 开头的行
grep -E "tcp|udp" /etc/services        # 匹配 tcp 或 udp 协议
```

> [!tip] 灵活使用 `-E`
> 日常使用建议直接加 `-E` 参数，这样不需要对 `+`、`?`、`|`、`()` 等元字符加反斜杠转义，可读性更好。实际上可以把 `grep -E` 当作默认选项使用。

---

## 2.3 实时日志跟踪：tail -f + grep 黄金组合

这是日常运维中最常用的命令组合之一，没有之一。当你想监控日志中是否出现特定关键词时，`tail -f` 配合 `grep` 是最直接有效的方案。

### 2.3.1 基础组合

```bash
tail -f /var/log/syslog | grep "ERROR"
```

这个命令做了什么：
1. `tail -f` 持续读取 `syslog` 的新增内容
2. 通过管道 `|` 将输出传递给 `grep`
3. `grep` 实时过滤，只显示包含 "ERROR" 的行

### 2.3.2 实战场景

```bash
# 跟踪 Nginx 访问日志，只看 5xx 错误
tail -f /var/log/nginx/access.log | grep -E '"5[0-9]{2}'"

# 实时监控应用日志中的异常，带上行号和颜色
tail -f app.log | grep --color -E "ERROR|Exception|NullPointer"

# 多关键词组合——只看某个用户的错误日志
tail -f app.log | grep "ERROR" | grep "user_9527"

# 排除健康检查等噪声日志
tail -f access.log | grep -v "healthcheck" | grep -v "monitoring"
```

> [!warning] 管道缓冲问题
> 当 `tail -f` 的输出通过管道传给 `grep` 时，由于标准 I/O 缓冲策略，`grep` 的输出可能不会立即刷新到终端。如果发现实时跟踪有延迟，可以使用 `grep --line-buffered` 强制行缓冲：
> ```bash
> tail -f app.log | grep --line-buffered "ERROR"
> ```
> 更彻底的方案是使用 `stdbuf`：
> ```bash
> tail -f app.log | stdbuf -oL grep "ERROR"
> ```

### 2.3.3 保存过滤结果

有时候你不仅想看实时输出，还想把结果保存下来：

```bash
# 实时监控日志并保存到文件（同时在终端显示）
tail -f app.log | grep --line-buffered "ERROR" | tee errors.log

# 分离窗口方案（推荐）：tmux 或新终端窗口
# 窗口 1：跟踪全部日志
tail -f app.log
# 窗口 2：只跟踪错误
tail -f app.log | grep --line-buffered "ERROR"
```

> [!tip] `multitail` 替代方案
> 如果系统安装了 `multitail`，可以在同一个终端窗口中分屏查看多个日志文件：
> ```bash
> multitail /var/log/nginx/access.log /var/log/nginx/error.log
> ```
> 或者用 `tmux` 分屏，每个窗格运行不同的 tail 命令。

---

## 2.4 文件比较：diff

`diff` 用于逐行比较两个文件的差异，在代码审查、配置对比、验证文件变更等场景中非常实用。

### 2.4.1 基本用法

```bash
diff file1.txt file2.txt
```

**输出示例**：
```bash
$ cat version1.txt
hello
world

$ cat version2.txt
hello
linux
world

$ diff version1.txt version2.txt
2a3
> linux
```

输出格式解读：
- `2a3`：在文件1的第2行之后，文件2新增了内容
- `> linux`：新增的内容是 `linux`

### 2.4.2 常用选项

```bash
diff -u old.txt new.txt          # 统一格式输出（最常用，可读性最好）
diff -i file1 file2              # 忽略大小写差异
diff -w file1 file2              # 忽略空白差异
diff -r dir1/ dir2/              # 递归比较两个目录
diff -q file1 file2              # 只报告文件是否不同，不显示具体差异
```

> [!example] `diff -u` 实战：配置变更对比
> ```bash
> $ diff -u nginx.conf.bak nginx.conf
> --- nginx.conf.bak    2026-07-28 10:00:00
> +++ nginx.conf        2026-07-28 12:00:00
> @@ -10,6 +10,7 @@
>  server {
>      listen 80;
> +    listen 443 ssl;
>      server_name example.com;
> +    ssl_certificate /etc/ssl/cert.pem;
>  }
> ```
> 带 `-` 前缀的是被删除的行，带 `+` 前缀的是新增的行。`@@` 部分标明变更的位置。

### 2.4.3 场景对比

| 命令 | 适用场景 |
|------|----------|
| `diff -u` | 查看两个文件的具体差异 |
| `diff -q` | 快速判断两个文件是否相同 |
| `diff -r` | 对比整个目录结构的变化 |
| `diff -w` | 比较代码（忽略格式差异） |

> [!tip] 替代工具
> 对于更友好的差异查看体验，可以考虑：
> - `vimdiff file1 file2`：在 Vim 中并排显示差异
> - `colordiff`：给 diff 输出加上颜色（通常需额外安装）
> - `git diff file1 file2`：即使文件不受 Git 管理，也可以用 `git diff` 查看差异，输出格式更现代
>
> ```bash
> # 用 git diff 替代普通 diff（需要先 git init）
> git diff --no-index file1 file2
> ```

---

## 2.5 本章总结

| 命令 | 核心用途 | 关键选项 |
|------|----------|----------|
| `cat` | 查看小文件内容 | `-n` 显示行号 |
| `head` | 查看文件开头 | `-n` 指定行数，`-c` 指定字节 |
| `tail` | 查看文件结尾或实时跟踪 | `-f` 实时跟踪，`-n +N` 从第N行开始 |
| `less` | 分页浏览大文件 | `/` 搜索，`g`/`G` 跳转首尾，`q` 退出 |
| `grep` | 文本搜索过滤 | `-i` 忽略大小写，`-E` 扩展正则，`-r` 递归，`-v` 反向匹配，`--line-buffered` 实时输出 |
| `diff` | 文件比较 | `-u` 统一格式，`-q` 快速判断，`-r` 递归目录 |
| `tail -f \| grep` | 实时日志过滤（运维黄金组合） | `grep --line-buffered` 防延迟 |

- **小文件用 `cat`，大文件用 `less`，只看首尾用 `head`/`tail`**。
- **`grep -E` 作为默认选项**，避免元字符转义的麻烦。
- **`tail -f app.log | grep --line-buffered "ERROR"`** 是实时日志监控的标准配方。
- **`diff -u` 是最佳差异输出格式**，可读性远超默认格式。
- **管道是 Linux 命令组合的灵魂**：`command | grep | less` 可以让任何长输出变得可控。

> [!tip] 一个命令走天下
> 如果你在工作中只能记住一个组合，记住这个：
> ```bash
> tail -f app.log | grep --line-buffered -E "ERROR|Exception"
> ```
> 它会实时显示应用日志中的异常，是你排查线上问题的第一道防线。

---

**下一章预告**：如果说 `grep` 只是文本处理的"哨兵"，那么 `sed` 和 `awk` 就是真正的"特种部队"。下一章我们将深入文本处理三剑客，学习如何用 `sed` 做流式编辑、用 `awk` 做结构化数据分析，以及如何组合它们完成日志统计、数据提取等实际任务。

---

> [!note]
> 本章是全书篇幅最长、实战性最强的一章。你将系统学习 Linux 文本处理的四大核心工具：sed（流编辑）、awk（结构化分析）、cut（列提取）、sort 与 uniq（排序去重），并通过管道组合它们来解决真实的日志分析和数据处理问题。学完本章后，你将能用一行命令完成许多在其他语言中需要几十行代码才能做到的事情。

---

## 3.1 sed -- 流编辑器

`sed`（Stream Editor）的核心能力是对文本流进行**非交互式编辑**。它不会打开编辑器让你手动改，而是根据你给的规则（脚本）逐行处理输入，把结果输出到标准输出。

### 核心语法

```bash
sed '<脚本>' <文件>
```

脚本的通用格式是：`<范围><操作>`。默认行为是**逐行读取，处理，输出**。

### 3.1.1 替换操作（s///）

替换是 `sed` 最常用的功能，语法借鉴了 `vi` 编辑器。

```bash
sed 's/旧文本/新文本/' file.txt        # 替换每行第一个匹配
sed 's/旧文本/新文本/g' file.txt       # 替换全局（每行所有匹配）
sed 's/旧文本/新文本/2' file.txt       # 只替换每行的第二个匹配
sed 's/旧文本/新文本/gi' file.txt      # 全局替换 + 忽略大小写
```

**为什么 / 是分隔符？** 因为 `s///` 继承自 `vi` 编辑器。你可以改用其他字符避免转义，比如处理路径时用 `#`：

```bash
# 用 # 代替 /，免去转义路径中的斜杠
sed 's#/usr/local#/opt#g' paths.txt
sed 's|/var/log|/data/logs|g' paths.txt  # 也可以用 |
```

> [!tip] 分隔符可任意选择
> `s` 后面的第一个字符就是分隔符。当要替换的文本包含大量 `/` 时，改用 `#`、`|`、`:` 等字符可以省去大量转义。

#### 原地编辑（-i）

默认情况下 `sed` 只输出到终端，不会修改原文件。用 `-i` 直接修改文件：

```bash
# 直接修改文件（谨慎！不可撤销）
sed -i 's/foo/bar/g' config.yaml

# 安全做法：先备份，再修改（加备份后缀）
sed -i.bak 's/foo/bar/g' config.yaml
# 这会生成 config.yaml.bak 作为备份，然后修改 config.yaml

# 恢复备份
mv config.yaml.bak config.yaml
```

> [!warning] sed -i 不可撤销
> 没有备份的 `-i` 操作是不可逆的。强烈建议首次使用时先不加 `-i` 预览结果，确认无误后再加 `-i`，或者同时提供备份后缀：
> ```bash
> # 推荐做法：三步法
> sed 's/foo/bar/g' config.yaml           # 第 1 步：预览输出
> sed -i.bak 's/foo/bar/g' config.yaml    # 第 2 步：确认后原地编辑（留备份）
> diff config.yaml.bak config.yaml        # 第 3 步：检查改动是否正确
> ```

### 3.1.2 地址范围与行操作

sed 可以指定操作的**行范围**，只编辑感兴趣的部分。

```bash
# 按行号
sed -n '10p' file.txt           # 只打印第 10 行（-n 抑制默认输出）
sed '5,10d' file.txt            # 删除第 5~10 行
sed '10q' file.txt              # 打印到第 10 行后退出（大文件高效查看开头）

# 按行号 + 步进
sed -n '1~2p' file.txt          # 打印奇数行（从第 1 行开始，步进 2）
sed -n '0~2p' file.txt          # 打印偶数行（从第 2 行开始，步进 2）

# 按模式匹配
sed -n '/ERROR/p' log.txt       # 只打印包含 ERROR 的行
sed '/^#/d' config.txt          # 删除所有以 # 开头的行（注释行）
sed '/^$/d' file.txt            # 删除所有空行

# 范围模式：从匹配行到匹配行
sed -n '/BEGIN/,/END/p' file.txt    # 打印 BEGIN 到 END 之间的内容
sed '/BEGIN/,/END/d' file.txt       # 删除 BEGIN 到 END 之间的内容
```

**例子：从 Nginx 日志中提取特定时间段的内容**

```bash
# 假设 access.log 每行以 [02/Jul/2026:10:15:30 开头
sed -n '/10:00:/,/11:00:/p' access.log   # 打印 10:00 到 11:00 之间的日志
```

### 3.1.3 多命令组合

可以用 `-e` 或分号组合多个 sed 命令：

```bash
# 用 -e 执行多个操作
sed -e 's/foo/bar/g' -e '/^$/d' file.txt

# 用分号分隔（注意分号前不能有空格，加空格需要引号包裹）
sed 's/foo/bar/g; s/baz/qux/g' file.txt

# 将命令写入文件供复用（适合复杂脚本）
cat << 'EOF' > fix-nginx.sed
s/# server/server/g
s/# listen/listen/g
s/# root/root/g
EOF

sed -f fix-nginx.sed nginx.conf
```

> [!example] 开启和关闭 Nginx 配置中的注释块
> ```bash
> # 场景：nginx.conf 中有一段被注释的 HTTPS 配置，想一次性取消注释
> cat nginx.conf
> #server {
> #    listen 443 ssl;
> #    server_name example.com;
> #    ssl_certificate /etc/ssl/cert.pem;
> #}
> 
> # 取消注释（删除每行开头的 # 和空格）
> sed -i 's/^# *//' nginx.conf
> 
> # 反向操作：注释掉 server 块（行首加 #）
> sed -i '/server {/,/^}/s/^/#/' nginx.conf
> ```

### 3.1.4 高级替换技巧

```bash
# 引用匹配内容
echo "hello world" | sed 's/\([a-z]*\) \([a-z]*\)/\2 \1/'   # 输出: world hello
# 圆括号捕获组用 \1, \2 引用，需要转义括号

# 使用 & 代表整个匹配的内容
echo "error: timeout" | sed 's/error: */[FOUND] &/'  # 输出: [FOUND] error: timeout

# 替换行首/行尾
sed 's/^/  /' file.txt          # 每行行首加两个空格（缩进）
sed 's/$/;/' file.txt           # 每行行尾加分号（生成 SQL）

# 只替换不包含特定模式的行
sed '/^#/!s/foo/bar/g' config.txt   # ! 表示取反：不匹配 # 开头的行才执行替换
```

### 3.1.5 sed 常用操作速查

| 命令 | 含义 | 示例 |
|------|------|------|
| `s/old/new/g` | 全局替换 | `sed 's/foo/bar/g' file` |
| `d` | 删除行 | `sed '/^#/d' file` |
| `p` | 打印行（需配合 -n） | `sed -n '10,20p' file` |
| `q` | 退出 sed | `sed '10q' file` |
| `a\` | 追加行（在匹配行后） | `sed '/error/a\ALERT' log` |
| `i\` | 插入行（在匹配行前） | `sed '/error/i\CHECK' log` |
| `c\` | 替换整行 | `sed '/error/c\FOUND_ERROR' log` |
| `y///` | 字符转换 | `sed 'y/abc/ABC/' file`（a->A, b->B, c->C） |

---

## 3.2 awk -- 结构化文本分析

如果说 `sed` 是"按行处理"的专家，那么 `awk` 就是"按列分析"的利器。`awk` 实际上是一门小型编程语言，有变量、条件、循环、数组和函数，但作为日常命令使用时，掌握几个核心模式就足够了。

### 核心模型

`awk` 的工作模式是：**逐行读取 → 按分隔符拆成列 → 执行模式匹配 → 执行动作**。

```bash
awk '<模式> { <动作> }' <文件>
```

- **缺省模式**：匹配所有行（每行都执行动作）
- **缺省动作**：`{ print }`（等价于打印整行）

**内置变量**：

| 变量 | 含义 |
|------|------|
| `$0` | 整行内容 |
| `$1` | 第 1 列 |
| `$2` | 第 2 列 |
| `$NF` | 最后一列 |
| `$(NF-1)` | 倒数第二列 |
| `NR` | 当前行号（从 1 开始） |
| `NF` | 当前行的总列数 |
| `FS` | 列分隔符（默认空格/制表符） |
| `OFS` | 输出列分隔符（默认空格） |

### 3.2.1 列提取 -- awk 最基础用法

```bash
# 打印第 1 列和第 3 列（默认以空格分隔）
awk '{print $1, $3}' file.txt

# 打印最后一列
awk '{print $NF}' file.txt

# 打印行号和内容
awk '{print NR": "$0}' file.txt

# 指定分隔符（-F 选项）
awk -F: '{print $1, $6}' /etc/passwd         # 用户名和家目录

# 指定多个分隔符
awk -F'[:/]' '{print $1, $5}' /etc/passwd    # 以 : 或 / 作为分隔符

# 自定义输出分隔符
awk -F: 'BEGIN{OFS=" | "} {print $1, $3, $7}' /etc/passwd
```

**实战例子：列出系统中所有可登录用户的用户名和 shell**

```bash
$ awk -F: '$7 ~ /bash|sh$/ {print $1, $7}' /etc/passwd
root /bin/bash
ubuntu /bin/bash
deploy /bin/sh
```

### 3.2.2 条件过滤

awk 的模式部分支持完整的比较运算符和逻辑运算：

```bash
# 数字比较
awk '$3 > 100 {print $1, $3}' scores.txt          # 第 3 列大于 100
awk '$5 >= 90 && $5 <= 100 {print $1}' grades.txt # 分数在 90~100 之间

# 字符串匹配（正则）
awk '$1 ~ /^2026/ {print $0}' access.log           # 第 1 列以 2026 开头
awk '$7 !~ /\.(jpg|png|gif)/ {print $7}' log.txt   # 第 7 列不匹配图片格式

# 行号过滤
awk 'NR > 1 {print $0}' file.txt                    # 跳过标题行
awk 'NR % 2 == 0 {print NR, $0}' log.txt            # 打印偶数行

# 列数过滤
awk 'NF > 5 {print NR, $0}' messy.txt               # 打印列数超过 5 的行
```

**实战例子：分析 df 输出，只显示磁盘使用率超过 80% 的分区**

```bash
$ df -h | awk 'NR > 1 && $5 ~ /%/ {gsub(/%/,"",$5); if ($5+0 > 80) print $1, $5"%"}'
/dev/sda1 85%
/dev/sdb1 92%
```

> [!tip] awk 中的数字比较陷阱
> 当 awk 的列包含 `%` 等符号时，直接用 `$5 > 80` 比较会失败。需要用 `gsub` 去掉 `%`，再用 `$5+0` 强制转为数字：
> ```bash
> # 错误：$5 是字符串 "85%"，不是数字
> df -h | awk '$5 > 80'
> 
> # 正确：去掉 % 后转为数字比较
> df -h | awk '{gsub(/%/,"",$5); if ($5+0 > 80) print $1, $5"%"}'
> ```

### 3.2.3 BEGIN 和 END 块

`BEGIN` 在处理第一行之前执行，用于初始化；`END` 在处理最后一行之后执行，用于汇总。

```bash
# 计算总和
awk '{sum += $1} END {print "Total:", sum}' numbers.txt

# 计算平均值
awk '{sum += $1; count++} END {print "Average:", sum/count}' numbers.txt

# 带格式的输出
awk 'BEGIN {print "=== Report ==="; print "Name\tScore"}
     {print $1 "\t" $2}
     END {print "=== End ==="}' scores.txt

# 统计行数（模拟 wc -l）
awk 'END {print NR}' file.txt
```

**实战：统计 /etc/passwd 中各 shell 类型数量**

```bash
$ awk -F: '{shells[$7]++} END {for (s in shells) print s, shells[s]}' /etc/passwd
/bin/bash 3
/usr/sbin/nologin 12
/bin/sh 1
```

### 3.2.4 统计计算实战

awk 内置的变量和运算使其成为飞快的"命令行计算器"。

```bash
# 多列运算
awk '{sum += $1; sumsq += ($1)^2} END {print "Sum:", sum, "Avg:", sum/NR}' data.txt

# 找出最大值和最小值
awk 'NR==1 {max=$1; min=$1} {if ($1>max) max=$1; if ($1<min) min=$1} END {print "Max:", max, "Min:", min}' data.txt

# 分组统计
awk '{group[$1] += $2} END {for (g in group) print g, group[g]}' sales.txt
```

> [!example] 分析 HTTP 访问日志统计
> ```bash
> # 场景：access.log 格式为：
> # 192.168.1.1 - - [28/Jul/2026:10:15:30 +0800] "GET /api/users HTTP/1.1" 200 1234
> 
> # 统计每个 IP 的请求次数
> awk '{ips[$1]++} END {for (ip in ips) print ip, ips[ip]}' access.log
> 
> # 统计每个 HTTP 状态码的出现次数
> awk '{codes[$9]++} END {for (c in codes) print c, codes[c]}' access.log
> 
> # 统计每个请求路径的请求次数
> awk '{paths[$7]++} END {for (p in paths) print paths[p], p}' access.log | sort -rn | head -10
> ```

### 3.2.5 实用技巧

```bash
# printf 格式化输出
awk '{printf "%-20s %8d\n", $1, $2}' file.txt

# 字符串函数
awk '{print toupper($1), length($0)}' file.txt     # 大写 + 行长度
awk '{print substr($1, 1, 5)}' file.txt             # 取第 1 列的前 5 个字符

# 将 awk 脚本写入文件（适合复杂场景）
cat << 'EOF' > report.awk
BEGIN {print "=== Report ==="}
{
    total[$1] += $2
    count[$1]++
}
END {
    for (key in total) {
        avg = total[key] / count[key]
        printf "%-10s %8.2f\n", key, avg
    }
}
EOF

awk -f report.awk data.txt
```

---

## 3.3 cut -- 快速列提取

如果你只需要最简单的"按分隔符取列"，`cut` 比 `awk` 更轻量、更快。它不能做条件过滤和计算，但提取动作比 awk 更简洁。

### 核心用法

```bash
cut -d'<分隔符>' -f<列号列表> <文件>
```

```bash
# 提取 /etc/passwd 的第 1 和第 7 列（用户名和 shell）
cut -d: -f1,7 /etc/passwd

# 提取第 1 到第 3 列
cut -d: -f1-3 /etc/passwd

# 提取第 3 列及之后的所有列
cut -d: -f3- /etc/passwd

# 排除第 2 列（提取除第 2 列外的所有列）
cut -d: -f1,3- /etc/passwd

# 默认分隔符是制表符（\"），适合处理 TSV 文件
cut -f1,3 data.tsv
```

### cut vs awk 列提取对比

| 场景 | cut | awk |
|------|-----|-----|
| `-d:` 分隔后取第 1、3 列 | `cut -d: -f1,3` | `awk -F: '{print $1,$3}'` |
| 取第 1 列到第 5 列 | `cut -d: -f1-5` | `awk -F: '{print $1,$2,$3,$4,$5}'` |
| 取第 3 列及之后 | `cut -d: -f3-` | 需要循环或特殊处理 |
| 条件过滤（$3 > 100） | 不支持 | 支持 |
| 计算（求和/平均值） | 不支持 | 支持 |
| 重排列 | `cut -f3,1`（先 3 后 1） | `awk '{print $3,$1}'` |
| 处理连续空格 | 不支持（单字符分隔符） | 默认支持 |

> [!tip] 什么时候用 cut？
> 当你的需求仅仅是："按某个字符切分，取第 N 列"，没有任何过滤、计算、重排需求时，用 `cut`。它更快，语法也更简洁。当需求逐渐变复杂时，随时可以切换到 `awk`。

### 字符位置提取

`cut` 还能按**字符位置**提取，这在处理定宽文件时很实用：

```bash
# 提取每行的第 1~5 个字符
cut -c1-5 /etc/passwd

# 提取每行的第 1、3、5 个字符
cut -c1,3,5 /etc/passwd

# 提取每行的第 2 个字符到结尾
cut -c2- /etc/passwd
```

> [!example] 实战：解析 ls -l 的输出提取权限位
> ```bash
> $ ls -l | tail -n +2 | cut -c1-10
> drwxr-xr-x
> -rw-rw-r--
> -rwxr-xr-x
> ```

---

## 3.4 sort -- 排序

`sort` 对输入行进行排序，默认按字典序（字母顺序）。

### 核心选项

| 选项 | 含义 | 示例 |
|------|------|------|
| `-n` | 按数字大小排序 | `sort -n scores.txt` |
| `-r` | 降序（反向） | `sort -rn scores.txt` |
| `-k` | 按指定列排序 | `sort -k2 -n scores.txt` |
| `-t` | 指定分隔符 | `sort -t: -k3 -n /etc/passwd` |
| `-h` | 人类可读数字排序（2K, 1G） | `sort -h sizes.txt` |
| `-u` | 去重（同 uniq） | `sort -u file.txt` |

```bash
# 按数字排序（默认 sort 按字符串，10 < 2）
$ cat scores.txt
Alice 90
Bob 100
Charlie 75

$ sort -k2 -n scores.txt         # 按第 2 列数字升序
Charlie 75
Alice 90
Bob 100

$ sort -k2 -rn scores.txt        # 降序
Bob 100
Alice 90
Charlie 75
```

**按人类可读大小排序**：

```bash
$ du -sh * | sort -rh            # 从大到小排序文件/目录大小
1.2G  videos/
456M  backups/
23M   logs/
4.2M  config/
```

> [!tip] sort -h 的神奇之处
> `-h` 选项能正确识别 `K`、`M`、`G`、`T` 等单位并按照实际大小排序。如果没有 `-h`，`1.2G` 会被排在 `456M` 前面（字典序），这显然是错的。

### 多级排序

```bash
# 先按第 2 列数字降序，相同则按第 3 列数字升序
sort -k2,2rn -k3,3n data.txt

# 示例：学生成绩按总分降序，总分相同则按语文成绩升序
sort -k3,3rn -k2,2n students.txt
```

---

## 3.5 uniq -- 去重与统计

`uniq` 只能去除**相邻**的重复行。所以它几乎总是和 `sort` 配合使用。

### 核心选项

| 选项 | 含义 | 示例 |
|------|------|------|
| 无选项 | 去除相邻的重复行 | `sort file \| uniq` |
| `-c` | 统计每行出现次数 | `sort file \| uniq -c` |
| `-d` | 只显示重复的行 | `sort file \| uniq -d` |
| `-u` | 只显示唯一行（不重复的） | `sort file \| uniq -u` |

```bash
# 基本去重（必须先排序）
sort names.txt | uniq

# 统计词频（最常用的组合之一）
sort words.txt | uniq -c | sort -rn
# 输出示例：
#  142 the
#   89 to
#   75 and
#   56 of

# 只显示重复项
sort names.txt | uniq -d

# 只显示唯一项
sort names.txt | uniq -u

# 忽略前 N 个字段比较去重
sort -k2 file.txt | uniq -f1      # 忽略第 1 列，比较剩余部分去重
```

> [!example] 日志分析经典组合
> ```bash
> # 统计 access.log 中访问次数最多的 10 个 IP
> awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10
> 
> # 输出示例：
>  3425 192.168.1.100
>  2100 10.0.0.55
>  1890 172.16.0.10
> ```

---

## 3.6 管道组合实战

将以上工具用管道 `|` 串联起来，是 Linux 命令行最强大的能力之一。下面覆盖几个真实场景。

### 场景 1：Nginx 访问日志分析

假设 `access.log` 的标准格式（Combined Log Format）：

```
192.168.1.1 - - [28/Jul/2026:10:15:30 +0800] "GET /api/users HTTP/1.1" 200 1234 "https://example.com" "Mozilla/5.0"
```

**任务 1：找出访问最多的前 10 个 IP**

```bash
$ awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10
   4523 192.168.1.100
   3891 10.0.0.55
   2104 203.0.113.50
```

**任务 2：统计每个 HTTP 状态码的出现次数**

```bash
$ awk '{print $9}' access.log | sort | uniq -c | sort -rn
  15200 200
   1200 304
    450 404
     23 500
      5 502
```

**任务 3：找出产生最多 404 错误的 URL 路径**

```bash
$ grep ' 404 ' access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -10
    89 /wp-admin/admin-ajax.php
    67 /old-api/v1/users
    45 /nonexistent-page
```

**任务 4：找出返回时间最慢的 5 个请求**（假设日志格式中有响应时间）

```bash
# 假设日志在第 10 列（NF-1）记录响应时间
$ awk '{print $(NF-1), $7, $1}' access.log | sort -rn | head -5
12.345 /api/reports 192.168.1.1
11.002 /search?q=linux 10.0.0.2
9.876 /data/export 172.16.0.5
```

### 场景 2：系统性能数据统计

**任务 1：找出 /var 下占用空间最大的 10 个目录**

```bash
$ du /var | sort -rn | head -10
# 或者更可读的版本
$ du -sh /var/* | sort -rh | head -10
```

**任务 2：统计当前系统中各用户的进程数**

```bash
$ ps aux | awk 'NR>1 {print $1}' | sort | uniq -c | sort -rn
   45 root
   12 www-data
    5 ubuntu
```

**任务 3：查看最近的登录记录**

```bash
$ last | awk '{print $1}' | sort | uniq -c | sort -rn
   23 ubuntu
   12 root
```

### 场景 3：数据清洗与格式转换

**任务 1：CSV 文件转置和统计**

```bash
# 原始 CSV：name,score,class
# 统计每个班级的平均分
$ awk -F, 'NR>1 {sum[$3]+=$2; count[$3]++} END {for (c in sum) print c, sum[c]/count[c]}' grades.csv
A 85.3
B 78.6
C 92.1
```

**任务 2：从日志中提取特定时间段，统计并排序**

```bash
# 提取 10:00~11:00 的日志，统计各路径访问量
$ awk '$4 ~ /10:|11:/ {print $7}' access.log | sort | uniq -c | sort -rn | head -10
```

**任务 3：多个文件拼接后去重**

```bash
# 合并多个黑名单并去重
$ cat blocklist1.txt blocklist2.txt blocklist3.txt | sort -u > merged_blocklist.txt
```

### 场景 4：寻找进程并批量操作

```bash
# 查找 nginx 进程的内存使用总和（MB）
$ ps aux | grep nginx | grep -v grep | awk '{sum += $6} END {print sum/1024 " MB"}'

# 杀掉所有由 deploy 用户运行的 node 进程
$ ps -u deploy -o pid,comm | grep node | awk '{print $1}' | xargs kill

# 找到占用 CPU 最高的 5 个进程
$ ps aux --sort=-%cpu | head -6
```

> [!warning] xargs 的危险
> 当 `kill` 配合 `xargs` 时，一定要先确认输出的 PID 是否正确。建议先不加管道执行前半部分，确认无误后再加上：
> ```bash
> # 危险做法（一步到位）
> ps aux | grep nginx | awk '{print $2}' | xargs kill
> 
> # 安全做法（分两步）
> ps aux | grep nginx | awk '{print $2}'       # 先确认 PID
> ps aux | grep nginx | awk '{print $2}' | xargs kill  # 确认后再执行
> ```

---

## 3.7 完整实战案例

### 案例 1：Web 服务器日志一键分析脚本

```bash
#!/bin/bash
# 功能：分析 Nginx access.log，输出关键指标
LOG=${1:-/var/log/nginx/access.log}

echo "=== Nginx 访问日志分析报告 ==="
echo "日志文件: $LOG"
echo ""

echo "1. 总请求数"
wc -l < "$LOG"

echo "2. 独立 IP 数"
awk '{print $1}' "$LOG" | sort -u | wc -l

echo "3. 访问最多的 5 个 IP"
awk '{print $1}' "$LOG" | sort | uniq -c | sort -rn | head -5

echo "4. 访问最多的 5 个路径"
awk '{print $7}' "$LOG" | sort | uniq -c | sort -rn | head -5

echo "5. HTTP 状态码分布"
awk '{print $9}' "$LOG" | sort | uniq -c | sort -rn

echo "6. 4XX 错误路径 Top 10"
grep ' 4[0-9][0-9] ' "$LOG" | awk '{print $7}' | sort | uniq -c | sort -rn | head -10

echo "7. 总流量（MB）"
awk '{sum += $10} END {print sum/1024/1024 " MB"}' "$LOG"
```

### 案例 2：CSV 数据处理

```bash
# 假设 data.csv 格式：
# Name,Age,City,Salary
# Alice,30,Beijing,15000
# Bob,25,Shanghai,12000
# Charlie,35,Shenzhen,20000

# 计算平均薪资
$ awk -F, 'NR>1 {sum+=$4; count++} END {print "Avg salary:", sum/count}' data.csv
Avg salary: 15666.7

# 按城市分组统计平均薪资
$ awk -F, 'NR>1 {sum[$3]+=$4; count[$3]++} END {for (city in sum) printf "%s: %.0f\n", city, sum[city]/count[city]}' data.csv
Beijing: 15000
Shanghai: 12000
Shenzhen: 20000

# 找出薪资最高的人
$ awk -F, 'NR>1 {if ($4 > max) {max=$4; name=$1}} END {print name, max}' data.csv
Charlie 20000
```

### 案例 3：配置文件批量修改

```bash
# 场景：批量修改多个 YAML 配置文件中的数据库连接字符串

# 预览所有配置中的数据库主机
$ grep -r "host:" config/*.yaml | awk '{print $3}' | sort -u

# 批量替换旧主机地址为新地址（保留备份）
$ find config/ -name "*.yaml" -exec sed -i.bak 's/db-old.example.com/db-new.example.com/g' {} \;

# 确认替换结果
$ grep -r "host:" config/*.yaml

# 如果确认无误，删除备份文件
$ find config/ -name "*.bak" -delete
```

### 案例 4：大文件高效处理

当处理几百 MB 甚至 GB 级别的文件时，以下技巧能让你等得不要那么久。

```bash
# 只看文件头部和尾部
head -1 huge.log                      # 看第 1 行（了解格式）
tail -1 huge.log                      # 看最后 1 行（最新时间）

# 只看感兴趣的行
grep 'ERROR' huge.log | head -20      # 快速浏览错误类型

# 分段处理：用 split 拆分后并行处理
split -l 100000 huge.log chunk_       # 每 10 万行拆成一个小文件
for f in chunk_*; do
    awk '{...}' "$f" > "result_$f" &  # 并行处理（& 放入后台）
done
wait                                   # 等待所有后台任务完成

# 管道流式处理（不产生中间文件）
zcat huge.log.gz | grep 'ERROR' | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```

> [!tip] 大文件处理的黄金法则
> 1. **能流式就别存中间文件**：用管道串联，避免磁盘 I/O
> 2. **能过滤就早过滤**：把 `grep` 放在管道最前面，让后续处理的数据量尽量小
> 3. **测试时用小数据量**：先用 `head -1000` 或 `tail -f` 验证命令正确性，再跑全量
> 4. **善用 `zcat` / `bzcat`**：直接处理压缩文件，解压到管道，不需要先解压到磁盘

---

## 本章总结

- **sed** 是流编辑器，核心操作是替换 `s///g` 和行操作（删除 `d`、打印 `p`、退出 `q`），`-i` 做原地编辑时务必先预览或留备份
- **awk** 是按列分析的语言级工具，核心模式 `{print $1, $NF}`，支持条件过滤、统计计算、分组聚合，`-F` 指定分隔符，`BEGIN/END` 做初始化和收尾
- **cut** 是最轻量的列提取工具，按分隔符 `-d` 或字符位置 `-c` 取列，适合简单场景
- **sort** 按列排序，`-n` 按数字、`-r` 降序、`-h` 认识单位、`-k` 指定排序列
- **uniq** 去重必须配合 `sort` 使用（因为只去相邻重复），`-c` 统计频率是最常用选项
- **管道组合**是文本处理的核心生产力，学会"先选数据再加工"的思维：`选取 → 转换 → 排序 → 统计 → 截取`
- **复杂场景四步法**：先用小数据测试、确认中间结果、再跑全量、最后验证输出

## 下一步

文本处理三剑客让你拥有了"命令行数据分析"的核心能力。第四章将转向**进程管理与系统监控**，学习如何使用 `ps`、`top`、`systemctl` 来管理和排查系统进程，以及后台作业的灵活控制。

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

---

> [!note]
> 网络问题是日常开发和运维中最常遇到的故障来源之一。本章将系统性地介绍 Linux 下的网络诊断工具链：从连通性测试、DNS 解析、路由追踪，到端口检测、HTTP 服务验证和抓包分析。学完本章，你将掌握一套完整的网络排障方法，遇到网络问题时不再是盲目猜测，而是逐步排查、精准定位。

---

## 5.1 连通性测试：ping

`ping` 是最基础也最常用的网络连通性测试工具。它通过发送 ICMP Echo 请求并等待响应，来判断目标主机是否可达以及网络延迟情况。

### 基本用法

```bash
ping -c 4 example.com              # 发送 4 个 ICMP 包后自动停止
ping -c 4 8.8.8.8                  # 直接 ping IP 地址（跳过 DNS 解析）
ping -c 4 -i 0.2 example.com       # 每 0.2 秒发一个包（默认 1 秒）
ping -c 4 -s 1472 example.com      # 指定包大小为 1472 字节（MTU 测试用）
```

**输出解读**：

```bash
$ ping -c 4 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=12.3 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=118 time=11.8 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=118 time=12.1 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=118 time=11.9 ms

--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 11.794/12.037/12.287/0.173 ms
```

关键指标解释：

| 指标 | 含义 | 正常范围 |
|------|------|---------|
| `time` | 往返延迟（RTT），从发出到收到响应的时间 | 同机房 < 1ms，同城 < 10ms，跨省 < 50ms，跨国 < 200ms |
| `ttl` | 生存时间，每经过一个路由器减 1 | Linux 初始 64，Windows 初始 128 |
| `packet loss` | 丢包率 | 正常应为 0% |
| `mdev` | 延迟抖动，标准差 | 越小越稳定 |

> [!tip] 通过 TTL 判断目标系统类型
> 如果回包的 TTL 在 64 附近（如 52-64），目标很可能是 Linux/Unix 系统；如果在 128 附近，则很可能是 Windows。这是因为不同操作系统 ICMP 包的初始 TTL 不同。
>
> ```bash
> # TTL=118，初始 TTL=64，说明经过了 64-118+1=... 
> # 不对，ping 回显的 TTL 是目标的初始 TTL 减去经过的跳数
> # Linux 通常初始 TTL=64，如果收到 118，说明目标不是 Linux
> # 跳过计算：初始 TTL 128 - 10(跳数) = 118 → Windows
> # 初始 TTL 64 - 10(跳数) = 54 → Linux
> ```

### 常见故障模式

| 现象 | 可能原因 | 下一步排查 |
|------|---------|-----------|
| 100% 丢包 | 目标宕机、网络断开、防火墙拦截 ICMP | 检查本机网络 `ip a`，检查防火墙 |
| 部分丢包 | 网络拥塞、链路不稳定 | 用 `mtr` 追踪丢包发生在哪一跳 |
| 延迟突增 | 跨运营商、链路质量差 | 用 `traceroute` 定位延迟在哪跳增加 |
| 目标域名解析失败 | DNS 问题 | 用 `dig` 检查 DNS 解析 |

> [!warning] 不要用 ping 判断服务是否正常
> 能 ping 通只说明网络层（ICMP）可达，但不能代表应用层（HTTP/SSH/MySQL 等）服务正常。很多服务器会防火墙拦截 ICMP（此时 ping 不通但不代表服务不可用），反过来即使 ping 通，HTTP 服务也可能已挂掉。

---

## 5.2 DNS 查询：dig

`dig`（Domain Information Groper）是最强大的 DNS 查询工具。当遇到"能 ping 通 IP 但域名访问不了"的问题时，首先就该用 `dig` 检查 DNS 解析。

### 基本用法

```bash
dig example.com                      # 标准查询，显示完整信息
dig example.com +short               # 只返回解析结果（最常用）
dig example.com A                    # 查询 A 记录（IPv4）
dig example.com AAAA                 # 查询 AAAA 记录（IPv6）
dig example.com MX                   # 查询 MX 记录（邮件交换）
dig example.com NS                   # 查询 NS 记录（权威域名服务器）
dig example.com CNAME                # 查询 CNAME 记录（别名）
dig -x 8.8.8.8                       # 反向查询（IP → 域名）
dig @1.1.1.1 example.com             # 指定 DNS 服务器查询（不依赖系统配置）
```

**标准输出解读**：

```bash
$ dig example.com

; <<>> DiG 9.18.28-1~deb12u2-Debian <<>> example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;example.com.                   IN      A

;; ANSWER SECTION:
example.com.            86400   IN      A       93.184.216.34

;; Query time: 23 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Tue Jul 28 10:00:00 CST 2026
;; MSG SIZE  rcvd: 56
```

关注 `status` 字段：

| status | 含义 |
|--------|------|
| `NOERROR` | 解析成功 |
| `NXDOMAIN` | 域名不存在（检查是否拼写错误） |
| `SERVFAIL` | DNS 服务器故障 |
| `REFUSED` | 请求被拒绝 |

### 实用技巧

```bash
# 只关心 IP 地址
dig +short example.com
# 输出: 93.184.216.34

# 追踪 DNS 解析路径（从根服务器开始递归）
dig +trace example.com

# 查询特定类型的多条记录
dig github.com A +short
dig github.com CNAME +short

# 批量查询域名
echo -e "google.com\ngithub.com\nstackoverflow.com" | while read d; do
    echo "$d -> $(dig +short $d)";
done
```

> [!tip] /etc/hosts 会绕过 DNS
> 系统首先检查 `/etc/hosts` 文件，如果其中有域名映射，则不会发起 DNS 查询。这就是为什么有时候 `dig` 返回了正确 IP，但 `ping` 或 `curl` 仍然解析到错误地址——检查 `/etc/hosts` 是否有脏条目：
> ```bash
> cat /etc/hosts
> # 127.0.0.1 example.com  ← 如果有这行，所有到 example.com 的请求都会发往本地
> ```

---

## 5.3 路由追踪：traceroute

当 ping 显示丢包或延迟异常时，`traceroute` 能告诉你问题出在网络路径的哪一段。

### 基本用法

```bash
traceroute example.com               # 标准路由追踪
traceroute -n example.com            # 不解析域名（速度快）
traceroute -n -q 1 example.com       # 每跳只发 1 个探测包（默认 3 个）
traceroute -I example.com            # 用 ICMP 代替 UDP（部分防火墙不会拦截）
```

**输出示例**：

```bash
$ traceroute -n 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  192.168.1.1    0.512 ms   0.489 ms   0.512 ms       ← 家用路由器
 2  10.0.0.1       2.123 ms   2.089 ms   2.101 ms       ← 运营商网关
 3  172.16.1.2     5.234 ms   5.211 ms   5.198 ms       ← 省级骨干节点
 4  61.xxx.xxx.1   12.345 ms  12.321 ms  12.298 ms      ← 骨干网出口
 5  * * *                                            ← 该跳无响应（可能防火墙）
 6  72.14.xxx.xxx  25.123 ms  25.089 ms  25.101 ms      ← Google 骨干
 7  8.8.8.8        12.001 ms  11.987 ms  12.034 ms       ← 最终目标
```

**逐行解读**：

- 每一行代表一个网络跳（路由器）
- 三列时间是三次探测的 RTT
- `* * *` 表示该跳无响应（路由器不回应或防火墙拦截）

### 定位故障点

```bash
# 场景：ping 丢包，但不知道路由哪一段出问题
# 观察 traceroute 中哪一跳开始出现 * 或延迟突增

# 更好的替代工具：mtr（traceroute + ping 的结合）
mtr -n 8.8.8.8                    # 实时显示每一跳的丢包率和延迟
mtr -n -r -c 10 8.8.8.8          # 发送 10 个包后输出报告（适合脚本）
```

> [!tip] traceroute vs mtr
> `traceroute` 只做一次快照，而 `mtr` 会持续发送包并统计每一跳的丢包率，更适合诊断间歇性问题。如果系统没有 `mtr`，先安装：`sudo apt install mtr-tiny`。

---

## 5.4 HTTP/HTTPS 测试：curl

`curl` 是命令行 HTTP 客户端的事实标准。调试 Web 服务、API 接口、下载文件都离不开它。

### 常用调试模式

```bash
curl https://example.com                    # GET 请求，输出响应体
curl -I https://example.com                 # 只查看响应头（HEAD 请求）
curl -v https://example.com                 # 详细模式，显示请求和响应头 + TLS 握手
curl -L https://example.com                 # 跟随重定向（默认不跟随）
curl -o output.html https://example.com     # 下载文件到指定名称
curl -s https://example.com                 # 静默模式，不显示进度条和错误
```

**`-v` 详细输出的关键信息**：

```bash
$ curl -v https://api.example.com
*   Trying 93.184.216.34:443...                    ← 解析到 IP，开始 TCP 连接
* Connected to api.example.com (93.184.216.34) port 443 (#0)  ← TCP 连接建立
* ALPN: curl offers h2,http/1.1                    ← TLS 握手开始
*  SSL certificate verify ok.                      ← 证书验证通过
> GET /api/v1/users HTTP/2                         ← 发送 HTTP 请求
> Host: api.example.com
> User-Agent: curl/7.88.1
>
< HTTP/2 200                                       ← 收到响应，状态码 200
< content-type: application/json
< content-length: 234
<
{"users": [...]}                                   ← 响应体
```

### HTTP 状态码速查

| 状态码 | 含义 | 常见原因 |
|--------|------|---------|
| 200 | 成功 | 一切正常 |
| 301/302 | 重定向 | 需要用 `-L` 跟随 |
| 401 | 未授权 | 缺少认证信息 |
| 403 | 禁止访问 | IP 被限制、权限不足 |
| 404 | 未找到 | 路径错误 |
| 500 | 服务器内部错误 | 后端服务挂了 |
| 502 | Bad Gateway | 代理/网关后端不可达 |
| 503 | 服务不可用 | 服务过载或维护中 |
| 504 | 网关超时 | 后端响应超时 |

### HTTP 请求测试

```bash
# 带请求头的 GET 请求
curl -H "Authorization: Bearer token123" https://api.example.com/users

# POST 请求发送 JSON
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"test","email":"test@example.com"}' \
     https://api.example.com/users

# PUT 请求更新资源
curl -X PUT -H "Content-Type: application/json" \
     -d '{"email":"new@example.com"}' \
     https://api.example.com/users/1

# 测试 REST API 并只关注响应码
curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health
# 输出: 200
```

### 耗时分析

这是 `curl` 最强大的功能之一——拆解 HTTP 请求的各个环节耗时。对于排查"为什么接口慢"非常有用。

```bash
curl -o /dev/null -s -w "\
DNS:    %{time_namelookup}s\n\
TCP:    %{time_connect}s\n\
TLS:    %{time_appconnect}s\n\
TTFB:   %{time_starttransfer}s\n\
Total:  %{time_total}s\n\
Speed:  %{speed_download}B/s\n\
Status: %{http_code}\n" https://example.com
```

**输出示例**：

```bash
DNS:    0.023s       ← DNS 解析耗时（23ms，正常）
TCP:    0.045s       ← TCP 三次握手（45ms）
TLS:    0.182s       ← TLS 握手（182ms，包含了 TCP 时间）
TTFB:   0.245s       ← 首字节时间（245ms，服务端处理时间的关键指标）
Total:  0.890s       ← 总耗时（包含下载响应体）
Speed:  1250.0B/s    ← 下载速度
Status: 200
```

**耗时分析指南**：

| 环节耗时长 | 可能原因 |
|-----------|---------|
| DNS 耗时 > 100ms | DNS 服务器响应慢，考虑换 DNS（如 1.1.1.1 或 223.5.5.5） |
| TCP 耗时 > 200ms | 物理距离远或中间路由问题 |
| TLS 耗时 > 500ms | 证书链过长或服务器性能不足 |
| TTFB 耗时异常长 | **后端应用处理慢**（最常见的问题来源） |

> [!example] 把耗时分析封装成脚本
> 每天都要用的话，可以写成函数放在 `.bashrc` 里：
> ```bash
> curltime() {
>   curl -o /dev/null -s -w "\
>   DNS: %{time_namelookup}s\n\
>   TCP: %{time_connect}s\n\
>   TLS: %{time_appconnect}s\n\
>   TTFB: %{time_starttransfer}s\n\
>   Total: %{time_total}s\n\
>   Status: %{http_code}\n" "$@"
> }
> # 使用
> curltime https://api.example.com/health
> ```

---

## 5.5 端口监听检查：ss

需要知道服务器上哪些端口在监听、谁在监听时，`ss`（Socket Statistics）是首选工具。它取代了传统的 `netstat`，速度更快、输出更清晰。

### 基础查询

```bash
ss -tlnp                    # 查看所有 TCP 监听端口（含进程信息）
ss -ulnp                    # 查看所有 UDP 监听端口
ss -tun                     # 查看所有 TCP + UDP 连接（不限于监听）
ss -tlnp | grep :80         # 查看端口 80 是否在监听
ss -tn state established    # 查看所有已建立的 TCP 连接
```

**输出示例**：

```bash
$ ss -tlnp
State    Recv-Q   Send-Q     Local Address:Port      Peer Address:Port   Process
LISTEN   0        128              0.0.0.0:22             0.0.0.0:*       users:(("sshd",pid=1234,fd=3))
LISTEN   0        128                 [::]:22                [::]:*       users:(("sshd",pid=1234,fd=4))
LISTEN   0        511              0.0.0.0:80             0.0.0.0:*       users:(("nginx",pid=2345,fd=8))
LISTEN   0        4096           127.0.0.1:3306           0.0.0.0:*       users:(("mysqld",pid=3456,fd=21))
```

**关键信息解读**：

- `Local Address:Port` — 监听地址和端口。`0.0.0.0:22` 表示在所有网卡上监听 SSH；`127.0.0.1:3306` 表示 MySQL 仅在本机监听（外部无法访问）
- `Process` — 哪个进程在监听，包含 PID
- `Recv-Q / Send-Q` — 接收和发送队列大小，长时间不为 0 说明有积压

### 常见排查场景

```bash
# 1. 检查 Nginx 是否在监听（Web 服务是否起来了）
ss -tlnp | grep nginx
# 输出示例: LISTEN  0  511  0.0.0.0:80  0.0.0.0:*  users:(("nginx",pid=2345,fd=8))

# 2. 检查 SSH 端口（排查连不上的问题）
ss -tlnp | grep :22

# 3. 查看所有已建立的连接（看谁在连我的服务）
ss -tn state established

# 4. 查看所有监听中的端口概览（无进程信息，速度更快）
ss -tln
```

> [!warning] ss 需要 root 才能看到所有进程信息
> 普通用户执行 `ss -tlnp` 时，Process 字段可能为空或显示 `-`。如果需要查看进程信息，加 `sudo`：
> ```bash
> sudo ss -tlnp
> ```

### ss 选项速查

| 选项 | 含义 |
|------|------|
| `-t` | 只显示 TCP 套接字 |
| `-u` | 只显示 UDP 套接字 |
| `-l` | 只显示 LISTEN（监听）状态的套接字 |
| `-n` | 数字格式，不解析服务名（`:80` 而不是 `:http`） |
| `-p` | 显示进程名和 PID |
| `-a` | 显示所有状态（不限于监听） |
| `-4` | 只显示 IPv4 |
| `-6` | 只显示 IPv6 |

---

## 5.6 端口检测：nc

`nc`（netcat）是网络界的瑞士军刀，这里只介绍它最常用的功能——端口可达性检测。当你需要从**另一台机器**测试某端口是否开放时，`nc` 比 `ss` 更合适（因为 `ss` 只能查本机）。

### 端口连通性测试

```bash
nc -zv host port                    # 测试端口是否可达（不发送数据）
nc -zv -w 3 host port               # 超时设置为 3 秒（默认可能等很久）
nc -zvn host port                   # 跳过 DNS 解析，速度更快
nc -zv host 80 443 3306             # 一次测试多个端口
```

**输出示例**：

```bash
$ nc -zv 192.168.1.100 22
Connection to 192.168.1.100 port 22 [tcp/ssh] succeeded!

$ nc -zv 192.168.1.100 3306
nc: connect to 192.168.1.100 port 3306 (tcp) failed: Connection refused
  # 端口未开放或服务没在运行

$ nc -zv 192.168.1.100 8080
nc: connect to 192.168.1.100 port 8080 (tcp) failed: No route to host
  # 目标不可达（网络不通或防火墙拦截）
```

### 端口范围扫描

```bash
# 扫描 1-1024 端口，检查哪些开放
nc -zv 192.168.1.100 1-1024 2>&1 | grep succeeded

# 扫描常见服务端口
nc -zv 192.168.1.100 22 80 443 3306 6379 27017 2>&1 | grep -E "succeeded|refused"
```

> [!tip] nc vs telnet
> 很多人习惯用 `telnet ip port` 来测试端口，但 telnet 需要安装且很多系统默认不带。`nc` 更轻量、功能更强大：
> - `nc -zv` 只测试连接，不进入交互模式
> - 支持超时设置 `-w`
> - 支持端口范围扫描

### nc 的其他用途

```bash
# 简易 TCP 端口监听（可以用来测试防火墙规则）
nc -lvp 9999                          # 在 9999 端口监听

# 测试 UDP 端口
nc -zuv host port                     # 注意：UDP 是无连接的，"成功"不代表服务在监听
```

> [!warning] UDP 端口检测的局限性
> 和 TCP 不同，UDP 是无连接协议。`nc -zuv` 测试 UDP 端口时，如果目标没回复，既可能是端口不可达，也可能是防火墙丢弃了 UDP 包。UDP 端口检测不太可靠，最好用专有客户端（如 `dig` 测试 DNS 的 53 端口）。

---

## 5.7 抓包分析：tcpdump

当其他工具都查不出问题时——网络配置看起来正确、服务在监听、端口可达、但连接就是有问题——就需要抓包来看网络上到底发生了什么。

`tcpdump` 是命令行抓包的王者。它不依赖图形界面，可以在任何 Linux 服务器上使用。

### 基础抓包

```bash
sudo tcpdump -i eth0 -n               # 监听 eth0 网卡，不解析域名
sudo tcpdump -i any -n                # 监听所有网卡
sudo tcpdump -i any -n port 80        # 只抓 80 端口的流量
sudo tcpdump -i any -n host 10.0.0.5  # 只抓与某主机的流量
sudo tcpdump -i any -n -c 100         # 抓 100 个包后自动停止
```

**输出示例**：

```bash
$ sudo tcpdump -i any -n port 80
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on any, link-type LINUX_SLL (Linux cooked v1), snapshot length 262144 bytes
13:42:15.123456 IP 10.0.0.1.54321 > 93.184.216.34.80: Flags [S], seq 1000, win 64240, ...
13:42:15.234567 IP 93.184.216.34.80 > 10.0.0.1.54321: Flags [S.], seq 2000, ack 1001, ...
13:42:15.234678 IP 10.0.0.1.54321 > 93.184.216.34.80: Flags [.], ack 2001, ...
13:42:15.235000 IP 10.0.0.1.54321 > 93.184.216.34.80: Flags [P.], seq 1001:1021, ack 2001, ...
13:42:15.345678 IP 93.184.216.34.80 > 10.0.0.1.54321: Flags [.], ack 1022, ...
```

### TCP 标志解读

TCP 三次握手就是通过这几个标志（Flags）完成的，看懂它们是理解网络问题的关键。

| 标志 | 缩写 | 含义 | 出现时机 |
|------|:----:|------|---------|
| `[S]` | SYN | 发起连接请求 | 客户端发起连接 |
| `[S.]` | SYN-ACK | 确认并同意连接 | 服务端回复握手 |
| `[.]` | ACK | 确认收到数据 | 几乎所有后续包 |
| `[P.]` | PUSH-ACK | 推送应用数据 | 传输数据时 |
| `[F.]` | FIN-ACK | 关闭连接 | 一方主动关闭 |
| `[R]` | RST | 重置连接 | 端口未监听或异常中断 |
| `[R.]` | RST-ACK | 带确认的重置 | 连接被拒绝 |

**三次握手过程**（正常连接）：

```
客户端 ---[S]---> 服务端      # SYN：请求连接
客户端 <--[S.]--- 服务端      # SYN-ACK：收到请求，同意连接
客户端 ---[.]---> 服务端      # ACK：确认收到，连接建立
```

**异常模式诊断**：

```bash
# 场景 1：端口未开放（防火墙没拦截，但服务没在运行）
# 客户端发送 SYN，服务端直接回复 RST
客户端 ---[S]---> 服务端
客户端 <--[R]---- 服务端      # RST 说明"没有进程在监听此端口"

# 场景 2：防火墙拦截
# 客户端发送 SYN，什么都没收到（需要等超时）
客户端 ---[S]---> [?]         # 请求被防火墙丢弃，无任何回应
# 结果：客户端反复重试，直到超时

# 场景 3：防火墙拒绝
# 客户端发送 SYN，收到 RST
客户端 ---[S]---> [?]
客户端 <--[R]---- [?]        # 防火墙主动拒绝连接
```

### 常用过滤表达式

```bash
# 按主机过滤
sudo tcpdump -i any -n host 10.0.0.5              # 与某主机的所有流量
sudo tcpdump -i any -n src host 10.0.0.5           # 从某主机发出的
sudo tcpdump -i any -n dst host 10.0.0.5           # 发往某主机的

# 按端口过滤
sudo tcpdump -i any -n port 443                    # 443 端口流量
sudo tcpdump -i any -n src port 80                 # 源端口 80
sudo tcpdump -i any -n dst port 53                 # 目标端口 53（DNS 查询）

# 组合过滤（用 and/or/not）
sudo tcpdump -i any -n 'port 80 and host 10.0.0.5'     # 与特定主机的 80 端口
sudo tcpdump -i any -n 'tcp[tcpflags] & tcp-syn != 0'  # 只抓 SYN 包
sudo tcpdump -i any -n 'port not 22'                    # 排除 SSH 流量
```

### 保存和分析

```bash
# 保存到文件以供后续分析
sudo tcpdump -i any -n -w capture.pcap           # 写入文件（二进制格式）
sudo tcpdump -i any -n -c 1000 -w capture.pcap   # 抓 1000 个包后保存

# 读取已保存的抓包文件
sudo tcpdump -r capture.pcap                     # 读取并打印
sudo tcpdump -r capture.pcap -n port 80          # 读取时过滤
sudo tcpdump -r capture.pcap -X                  # 以 HEX + ASCII 格式打印
```

> [!tip] 用 Wireshark 分析 pcap 文件
> tcpdump 保存的 `capture.pcap` 文件可以直接用 Wireshark 打开，获得图形化的分析体验。在服务器上用 tcpdump 抓包保存，然后传到本地用 Wireshark 分析，是线上问题排查的标准工作流。

### 排障场景示例：检查 HTTP 响应是否正常

```bash
# 终端 1：启动 tcpdump 抓取 80 端口流量
sudo tcpdump -i any -n port 80 -A

# 终端 2：发送 HTTP 请求
curl http://example.com

# 在 tcpdump 输出中可以看到完整的 HTTP 请求和响应内容
# -A 参数会把包内容按 ASCII 打印出来，直接看到 HTTP 协议头
```

---

## 5.8 网络排障五步法实战

掌握了以上各个工具后，更重要的是知道在什么场景该用什么工具。下面是一个标准化的排障流程——**五步法**，从底到顶逐层排查。

### 排障流程概览

```
步骤 1: 检查本机网络配置       命令: ip a, ip route, ping 127.0.0.1
步骤 2: DNS 解析检查          命令: dig +short example.com
步骤 3: 路由连通性检查        命令: ping -c 4 target_ip, traceroute
步骤 4: 端口与服务检查        命令: ss -tlnp, nc -zv target port
步骤 5: 应用层协议验证        命令: curl -v, tcpdump
```

### 实战案例：网站无法访问

**场景**：用户反馈 `https://myapp.example.com` 无法访问。

#### 步骤 1：检查本机网络配置

先确认本机网络是正常的：

```bash
# 检查 IP 地址是否配置正常
ip a

# 检查默认路由
ip route show | grep default

# 检查本机回环接口（基本网络栈是否正常）
ping -c 1 127.0.0.1
```

**判断**：如果 `127.0.0.1` 都 ping 不通，说明本机网络栈有问题，重启网络服务或检查内核模块。

#### 步骤 2：DNS 解析检查

```bash
# 域名能否解析
dig +short myapp.example.com
# 如果没返回 IP，检查域名拼写或 DNS 服务器

# 对比使用不同 DNS 服务器
dig @8.8.8.8 myapp.example.com +short
dig @1.1.1.1 myapp.example.com +short
```

**判断**：
- 返回 IP → DNS 正常，进入下一步
- 返回 `NXDOMAIN` → 域名不存在，检查是否拼写错误
- 一个 DNS 能解析另一个不能 → 本地 DNS 服务器配置有问题

#### 步骤 3：路由连通性检查

```bash
# 先 ping IP（跳过 DNS），确认网络层是否可达
ping -c 4 93.184.216.34

# 如果丢包或延迟高，追踪路由
traceroute -n 93.184.216.34

# 用 mtr 更精确地检测丢包位置
mtr -n -r -c 10 93.184.216.34
```

**判断**：
- ping 通且延迟正常 → 网络层没问题
- ping 不通 → 防火墙拦截 ICMP 或目标宕机（用上层工具进一步验证）
- traceroute 在某跳后全 `*` → 该段网络故障或防火墙

#### 步骤 4：端口与服务检查

```bash
# 从本机检查目标端口是否开放
nc -zv 93.184.216.34 443

# 如果本机端口开放检查（如果是排查本地服务）
ss -tlnp | grep :443
```

**判断**：
- `succeeded` → 端口开放
- `Connection refused` → 端口没在监听（服务没启动或端口错误）
- `No route to host` → 网络不可达

#### 步骤 5：应用层协议验证

```bash
# 用 curl 验证 HTTP 服务
curl -I https://myapp.example.com

# 详细模式看完整握手过程
curl -v https://myapp.example.com

# 看耗时分布
curl -o /dev/null -s -w "DNS: %{time_namelookup}s\nTCP: %{time_connect}s\nTLS: %{time_appconnect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\nStatus: %{http_code}\n" https://myapp.example.com

# 如果怀疑 HTTPS 问题，测试 HTTP
curl -I http://myapp.example.com

# 如果怀疑网络层问题，抓包确认
sudo tcpdump -i any -n host myapp.example.com -c 100
```

**判断**：
- HTTP 状态码 200 → 服务正常
- 502/504 → 后端代理或应用问题
- SSL 证书错误 → 证书过期或配置错误
- curl 卡住 → 网络连接问题

### 快速诊断速查表

| 现象 | 排查命令 | 常见原因 |
|------|---------|---------|
| 域名访问不了，IP 能访问 | `dig example.com` | DNS 问题 |
| 连接超时 | `traceroute -n IP` | 防火墙拦截或路由不通 |
| 连接被拒绝 | `nc -zv IP PORT` | 服务没启动或端口错误 |
| 网站慢 | `curl -w` 耗时分析 | 后端处理慢，或 CDN 问题 |
| 时通时不通 | `mtr -n IP` | 链路不稳定或 DNS 负载均衡 |
| SSH 连不上 | `ss -tlnp \| grep :22` | SSH 服务没运行或防火墙 |
| 能 ping 通但浏览器打不开 | `curl -v http://IP:PORT` | Web 服务没启动或防火墙拦截端口 |
| HTTPS 报证书错误 | `openssl s_client -connect host:443` | 证书过期或配置错误 |

> [!example] 一键排障脚本
> 把五步法写成脚本，需要时一键执行：
> ```bash
> #!/bin/bash
> # diagnose.sh - 快速网络排障脚本
> TARGET=$1
> 
> echo "=== Step 1: DNS Resolve ==="
> dig +short $TARGET
> 
> echo -e "\n=== Step 2: Ping ==="
> ping -c 4 $TARGET
> 
> echo -e "\n=== Step 3: Route ==="
> traceroute -n -q 1 -w 2 $TARGET
> 
> echo -e "\n=== Step 4: Port Check (80/443) ==="
> nc -zv -w 3 $TARGET 80
> nc -zv -w 3 $TARGET 443
> 
> echo -e "\n=== Step 5: HTTP Check ==="
> curl -o /dev/null -s -w "Status: %{http_code}\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" http://$TARGET
> 
> # 使用：bash diagnose.sh example.com
> ```

---

## 本章总结

- **ping** 测试网络层连通性和延迟，但注意 ICMP 可能被防火墙拦截，能 ping 通不代表服务正常
- **dig** 是 DNS 查询的标准工具，`+short` 参数直接返回 IP，遇到域名解析问题首选
- **traceroute** 定位路由路径中的故障点，`mtr` 是其增强版，能持续检测丢包
- **curl** 是 HTTP 排障的核心工具，`-v` 看详细握手过程，`-w` 做耗时分析可以精确拆解 DNS/TCP/TLS/TTFB 各阶段耗时
- **ss** 替换了旧的 netstat，检查端口监听最快：`ss -tlnp` 查看所有 TCP 监听端口和对应进程
- **nc -zv** 从远程测试端口是否开放，`Connection refused` 和 `No route to host` 含义不同
- **tcpdump** 抓包分析是排障的终极手段，看懂 TCP 标志 `[S]` `[S.]` `[R]` 能快速判断连接状态
- **网络排障五步法**（网络配置 → DNS → 路由 → 端口 → 应用层）是标准化的排障思路，按层排查不跳步

## 下一步

掌握了网络诊断工具后，第六章将转向 **权限管理与安全基础**，学习 Linux 文件权限模型、chmod/chown 的实战用法，以及如何设置安全的默认权限。

---

> [!note]
> 本章将带你系统理解 Linux 的权限模型。从文件的 rwx 权限位到 chmod 的数字/符号模式，从所有者管理到 SUID/SGID/Sticky Bit 特殊权限，再到 umask 默认权限控制。学完本章，你将能精准控制谁可以读、写、执行你的文件——这是 Linux 安全的第一道防线，也是日常运维中最容易出问题的地方。

---

## 6.1 理解文件权限模型

在 Linux 中，**一切皆文件**，每个文件都有一套权限位（Permission Bits）来控制访问。这是多用户系统的基石。

### 查看权限位

用 `ls -l` 查看文件的详细信息，第一列就是权限位：

```bash
$ ls -lh /etc/passwd
-rw-r--r-- 1 root root 2.8K Jul 28 10:00 /etc/passwd

$ ls -ld /tmp
drwxrwxrwt 10 root root 4.0K Jul 28 12:00 /tmp

$ ls -l script.sh
-rwxr-xr-x 1 user user 512 Jul 28 09:50 script.sh
```

第一列的 10 个字符可以分解为：

```
- r w x  r - x  r - x
│ └┬┘  └┬┘  └┬┘
│  │     │    └── Others（其他人）
│  │     └─────── Group（所属组）
│  └───────────── User/Owner（所有者）
└──────────────── 文件类型（- 文件，d 目录，l 链接）
```

### 三种权限的含义

| 权限 | 对文件的意义 | 对目录的意义 |
|------|-------------|-------------|
| **r** (读) | 读取文件内容（如 `cat file`） | 列出目录内容（如 `ls dir`） |
| **w** (写) | 修改文件内容 | 在目录中创建/删除文件 |
| **x** (执行) | 作为程序执行 | 进入目录（如 `cd dir`） |

> [!tip] 目录的执行权限是关键
> 很多人以为目录的 `r` 权限就够了，实际上**没有 `x` 权限，你连 `cd` 进目录都不行**。如果你只有目录的 `r` 权限，可以 `ls` 看到文件名，但无法访问文件内容和元数据。
>
> ```bash
> # 创建测试
> $ mkdir testdir && echo "secret" > testdir/file.txt
> $ chmod 644 testdir        # 去掉目录的 x 权限
> $ ls testdir               # 有 r 权限，可以看到文件名
> file.txt
> $ cat testdir/file.txt     # 但无法访问文件内容
> cat: testdir/file.txt: Permission denied
> ```

### 三种主体（ugo）

| 主体 | 缩写 | 说明 |
|------|:----:|------|
| **u**ser | u | 文件所有者（owner） |
| **g**roup | g | 文件所属组的所有成员 |
| **o**thers | o | 其他所有人 |

### 常用权限组合速查

```bash
-rw-------   (600)   # 私密文件，仅所有者可读写
-rw-r--r--   (644)   # 普通文件默认，所有者写，其他人只读
-rwxr-xr-x   (755)   # 可执行文件/脚本
-rwx------   (700)   # 私密脚本，仅所有者可执行
-rw-rw-rw-   (666)   # 全开放读写（极少用）
-rwxrwxrwx   (777)   # ⚠️ 全开放——绝对不要用
```

---

## 6.2 chmod：修改文件权限

`chmod`（change mode）是修改权限的命令，支持**数字模式**和**符号模式**两种写法。建议两种都掌握，数字模式适合快速设置，符号模式适合微调。

### 数字模式

每个权限用一个数字表示：

```
r = 4    w = 2    x = 1
```

三个数字分别代表 u / g / o 的权限，每个数字是三种权限值的**和**：

```
rwx = 4+2+1 = 7
rw- = 4+2+0 = 6
r-x = 4+0+1 = 5
r-- = 4+0+0 = 4
-wx = 0+2+1 = 3  （极少用）
-w- = 0+2+0 = 2  （极少用）
--x = 0+0+1 = 1  （极少用）
```

**实战示例**：

```bash
# 设置脚本为所有者可读写执行，组和其他人只读执行
chmod 755 script.sh

# 设置配置文件为所有者可读写，其他人只读
chmod 644 config.yml

# 设置私密密钥文件为仅所有者可读
chmod 600 id_rsa

# 递归设置目录下所有文件和子目录
chmod -R 755 /opt/myapp/
```

### 符号模式

格式：`chmod <主体><操作><权限> 文件名`

| 符号 | 含义 |
|:----:|------|
| `u` | user（所有者） |
| `g` | group（组） |
| `o` | others（其他人） |
| `a` | all（所有人，等同于 ugo） |
| `+` | 添加权限 |
| `-` | 移除权限 |
| `=` | 设置精确权限 |

**实战示例**：

```bash
chmod u+x script.sh       # 为所有者添加执行权限
chmod g-w file.txt        # 移除组的写权限
chmod o=r file.txt        # 其他人设置为只读（覆盖原有权限）
chmod a+r file.txt        # 所有人添加读权限
chmod u=rwx,g=rx,o=rx     # 等价于 chmod 755

# 常见微调场景
chmod +x script.sh        # 所有人加执行权限（不指定主体时默认 a）
chmod -R g+w /opt/shared/ # 递归为组添加写权限
```

> [!example] 数字 vs 符号：何时用哪种？
>
> ```bash
> # 数字模式适合：完整设置所有权限
> chmod 644 file.txt      # 清晰、简洁、一次到位
>
> # 符号模式适合：只调整部分权限
> chmod +x script.sh      # 只想加执行位
> chmod g-w file.txt      # 只想移除组的写权限
> chmod -R g+w /shared/   # 递归给组加写权限
> ```
>
> 一个实用的做法：用 `chmod 644` / `chmod 755` / `chmod 600` 三组数字覆盖 90% 的场景，其他情况用符号模式微调。

### 理解 chmod 的递归行为

```bash
chmod 755 /opt/myapp/          # 只改目录本身
chmod -R 755 /opt/myapp/       # 改目录及其所有子文件和子目录

# ⚠️ 但这样有个问题：普通文件不应该有 x 权限
# 更精细的做法是分别设置：
find /opt/myapp/ -type f -exec chmod 644 {} \;   # 文件设 644
find /opt/myapp/ -type d -exec chmod 755 {} \;   # 目录设 755
```

> [!warning] 不要对普通文件加执行权限
> 如果你 `chmod -R 755` 一个目录，里面的所有普通文件（如文本文件、图片等）都会被加上 `x` 执行位。虽然一般不会造成功能性错误，但这是不好的安全习惯。建议对文件和目录分别设置。

---

## 6.3 chown / chgrp：管理文件所有者

### chown — 修改所有者和所属组

```bash
chown user file.txt              # 修改文件所有者为 user
chown user:group file.txt        # 同时修改所有者和组
chown :group file.txt            # 仅修改所属组（省略所有者部分）
chown user: file.txt             # 修改所有者并设为同名的组

# 递归修改目录
chown -R www-data:www-data /var/www/
```

> [!warning] chown 需要 root 权限
> 普通用户无法把自己的文件所有权转给其他用户——这是安全设计，防止你通过"赠送"文件绕过磁盘配额限制。只有 root 可以自由修改所有权。

### chgrp — 仅修改所属组

`chgrp` 是 `chown :group` 的独立版本，功能完全一样，但更语义化：

```bash
chgrp developers project/    # 修改目录的组为 developers
chgrp -R developers /shared/ # 递归修改
```

### 实战场景：部署 Web 应用

这是权限管理最典型的场景。假设你用 `deploy` 用户上传代码，但 Nginx 用 `www-data` 用户运行：

```bash
# 1. 上传代码后，设置所有者
sudo chown -R deploy:www-data /var/www/myapp/

# 2. 文件权限：所有者可写，组和其他人只读
find /var/www/myapp/ -type f -exec chmod 644 {} \;

# 3. 目录权限：所有者可写执行，组和其他人只读执行
find /var/www/myapp/ -type d -exec chmod 755 {} \;

# 4. 让 www-data 用户可以进入目录
chmod g+rx /var/www/myapp/
```

---

## 6.4 特殊权限：SUID / SGID / Sticky Bit

除了基本的 rwx 权限，Linux 还有三个特殊权限位，用于更精细的控制。

### SUID（Set User ID）`u+s`

当可执行文件设置了 SUID，任何用户运行它时，都会以**文件所有者**的身份执行，而不是以运行者的身份。

```
权限位显示：-rwsr-xr-x   （s 出现在所有者的 x 位置）
```

**经典例子：`passwd` 命令**

```bash
$ which passwd
/usr/bin/passwd
$ ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 67976 Jul 15  2024 /usr/bin/passwd
```

`passwd` 的所有者是 root，普通用户需要修改 `/etc/shadow` 文件（仅 root 可写）。通过 SUID，普通用户运行 `passwd` 时临时获得 root 权限，才能更新自己的密码。

```bash
# 设置 SUID
chmod u+s /path/to/program
# 或用数字模式（4 开头）
chmod 4755 /path/to/program   # rwsr-xr-x
```

### SGID（Set Group ID）`g+s`

SGID 有两种行为：
- **对文件**：以文件所属组的身份执行（类似 SUID 但作用于组）
- **对目录**：在该目录下创建的新文件，自动继承目录的所属组

```
权限位显示：drwxrws---   （s 出现在组的 x 位置）
```

**SGID 对目录是最实用的特性**。在协作项目中，团队成员的文件组保持一致，避免反复 `chgrp`：

```bash
# 设置 SGID
sudo chgrp developers /shared/project/
sudo chmod g+s /shared/project/

# 现在，任何用户在 /shared/project/ 下创建的文件
# 都会自动属于 developers 组
touch /shared/project/test.txt
$ ls -l /shared/project/test.txt
-rw-r--r-- 1 alice developers 0 Jul 28 14:00 test.txt
```

```bash
# 设置 SGID
chmod g+s /shared/dir/
# 或用数字模式（2 开头）
chmod 2755 /shared/dir/   # rwxr-sr-x
```

### Sticky Bit `+t`

Sticky Bit 主要用于**共享目录**。设置了 Sticky Bit 的目录，用户只能删除**自己拥有的文件**，不能删除别人的文件。

```
权限位显示：drwxrwxrwt   （t 出现在其他人的 x 位置）
```

**经典例子：`/tmp` 目录**

```bash
$ ls -ld /tmp
drwxrwxrwt 10 root root 4096 Jul 28 12:00 /tmp
```

`/tmp` 是全局可写的共享目录，任何人都可以创建文件，但 Sticky Bit 确保只有文件所有者（或 root）才能删除它。

```bash
# 设置 Sticky Bit
chmod +t /shared/temp/
# 或用数字模式（1 开头）
chmod 1777 /shared/temp/   # rwxrwxrwt
```

### 特殊权限速查表

| 特殊权限 | 数字位 | 符号 | 显示位置 | 核心用途 |
|----------|:------:|:----:|:--------:|----------|
| SUID | 4 | `u+s` | 所有者 x 位 → `s` | 以文件所有者身份执行 |
| SGID | 2 | `g+s` | 组 x 位 → `s` | 目录下新文件继承组 |
| Sticky Bit | 1 | `+t` | 其他人 x 位 → `t` | 防删除共享目录 |

> [!warning] 特殊权限的安全风险
> - **SUID 是双刃剑**：有 SUID 的程序如果有漏洞，攻击者可能利用它提权。你的系统上应该极少有 SUID 文件（通常只有 `passwd`、`sudo`、`ping` 等几个）。
> - **查找所有 SUID 文件**：
>   ```bash
>   find / -perm -4000 -type f 2>/dev/null
>   ```
> - **如果发现不明 SUID 文件，立刻调查**，可能是系统被入侵的迹象。

---

## 6.5 umask：控制默认权限

每次你创建文件或目录时，系统都会给它一个默认权限。`umask` 定义了要从这个默认权限中"扣掉"哪些位。

### umask 的计算规则

```bash
文件默认最大权限：666  (rw-rw-rw-)
目录默认最大权限：777  (rwxrwxrwx)

最终权限 = 最大权限 - umask 值
```

**最常见的 umask 值：022**

```bash
文件：666 - 022 = 644  (rw-r--r--)
目录：777 - 022 = 755  (rwxr-xr-x)
```

### 查看和设置 umask

```bash
# 查看当前 umask
$ umask
0022

# 以符号形式查看
$ umask -S
u=rwx,g=rx,o=rx
```

### 不同 umask 值的效果

| umask 值 | 文件权限 | 目录权限 | 适用场景 |
|:--------:|:--------:|:--------:|----------|
| 022 | 644 (`rw-r--r--`) | 755 (`rwxr-xr-x`) | 默认——其他人可读 |
| 002 | 664 (`rw-rw-r--`) | 775 (`rwxrwxr-x`) | 团队协作——组内可写 |
| 027 | 640 (`rw-r-----`) | 750 (`rwxr-x---`) | 安全——组内只读，他人无权限 |
| 077 | 600 (`rw-------`) | 700 (`rwx------`) | 私密——仅所有者可访问 |

> [!example] 团队协作的 umask 配置
>
> 假设你和团队成员共享一个开发目录，希望组内成员都能读写：
>
> ```bash
> # 在 ~/.bashrc 或 ~/.zshrc 中设置
> umask 002
>
> # 同时在共享目录设置 SGID
> sudo chgrp -R developers /shared/project/
> sudo chmod -R g+s /shared/project/
> ```
>
> 这样团队新创建的文件自动为 `664`（组内可写），且自动继承 `developers` 组。

### 持久化 umask 设置

```bash
# 对当前用户生效，写入 shell 配置文件
echo "umask 027" >> ~/.bashrc
source ~/.bashrc

# 对系统全局生效（影响所有用户）
# 编辑 /etc/profile 或 /etc/bash.bashrc
# 或 /etc/login.defs 中的 UMASK 配置
```

---

## 6.6 实战：Web 服务器权限设置

把前面学的知识综合起来，模拟一个真实的 Nginx Web 服务器权限配置场景。

### 场景描述

- 你通过 `deploy` 用户上传和管理代码
- Nginx 以 `www-data` 用户运行
- 代码部署在 `/var/www/example.com/`
- 需要确保：
  - `deploy` 用户能读写所有文件（负责更新代码）
  - `www-data` 用户能读取静态文件（负责提供 HTTP 服务）
  - 其他人不能访问（安全要求）
  - 上传目录需要 `www-data` 可写（用户上传文件）

### 完整配置流程

```bash
# 第一步：创建目录并设置所有者和组
sudo mkdir -p /var/www/example.com
sudo chown deploy:www-data /var/www/example.com/

# 第二步：设置目录权限
# 所有者（deploy）完全控制，组（www-data）可进入和读取
sudo chmod 750 /var/www/example.com/

# 第三步：设置 SGID，确保新文件继承组
sudo chmod g+s /var/www/example.com/

# 第四步：部署代码后设置文件权限
# 文件：所有者可读写，组可读
find /var/www/example.com/ -type f -exec chmod 640 {} \;
# 目录：所有者可读写执行，组可读执行
find /var/www/example.com/ -type d -exec chmod 750 {} \;

# 第五步：对上传目录特殊处理（需要组可写）
sudo mkdir -p /var/www/example.com/uploads
sudo chmod 770 /var/www/example.com/uploads/
```

### 验证权限配置

```bash
# 以 deploy 用户身份测试
$ su deploy
$ ls -la /var/www/example.com/
total 20K
drwxr-s--- 4 deploy www-data 4.0K Jul 28 15:00 .
drwxr-xr-x 3 root   root     4.0K Jul 28 14:00 ..
-rw-r----- 1 deploy www-data  256 Jul 28 15:00 index.html
drwxr-x--- 2 deploy www-data 4.0K Jul 28 15:00 css
drwxrwx--- 2 deploy www-data 4.0K Jul 28 15:00 uploads

# deploy 可以写任何文件
$ echo "update" >> index.html    # 成功

# 以 www-data 用户测试
$ su www-data
$ cat /var/www/example.com/index.html   # 可以读取
$ rm /var/www/example.com/index.html    # 不能删除（没有 w 权限）
rm: remove write-protected regular file 'index.html'? y
rm: cannot remove 'index.html': Permission denied

# www-data 可以写入 uploads 目录
$ touch /var/www/example.com/uploads/test.txt   # 成功

# 其他用户无法访问
$ su nobody
$ ls /var/www/example.com/
ls: cannot open directory '/var/www/example.com/': Permission denied
```

### 简化检查脚本

```bash
#!/bin/bash
# 检查 /var/www/example.com 的文件权限是否合规
DIR="/var/www/example.com"
echo "=== 权限检查报告 ==="

echo ""
echo "目录结构概览："
ls -laR "$DIR" 2>&1 | head -20

echo ""
echo "合规检查："
# 检查是否存在 777 的权限
BAD_PERMS=$(find "$DIR" -perm /777 -type f 2>/dev/null)
if [ -n "$BAD_PERMS" ]; then
    echo "[WARNING] 发现 777 权限文件："
    echo "$BAD_PERMS"
fi

# 检查所有者是否都是 deploy
BAD_OWNER=$(find "$DIR" ! -user deploy 2>/dev/null)
if [ -n "$BAD_OWNER" ]; then
    echo "[WARNING] 发现非 deploy 所有的文件："
    echo "$BAD_OWNER"
fi
```

> [!tip] 权限管理的黄金法则
> 1. **最小权限原则**：只给所需的最小权限，不给多余的
> 2. **先拒绝再允许**：从严格的权限开始，按需放宽
> 3. **文件 640 / 目录 750**：这是 Web 服务最常用的组合
> 4. **SGID 避免组混乱**：共享目录一定要设 `g+s`
> 5. **定期审计 SUID**：用 `find / -perm -4000` 检查异常

---

## 本章总结

- **文件权限三要素**：读（r=4）、写（w=2）、执行（x=1），分别对文件所有者（u）、所属组（g）、其他人（o）设置
- **chmod 数字模式**（如 `644`、`755`、`600`）适合完整设置，**符号模式**（如 `u+x`、`g-w`）适合微调
- **chown** 修改文件所有者/组，需要 root 权限；**chgrp** 只改所属组
- **特殊权限**：SUID（以所有者身份执行）、SGID（目录下新文件继承组）、Sticky Bit（防删除共享目录）
- **umask** 控制新建文件的默认权限，团队协作时设为 `002`，安全敏感环境设为 `027` 或 `077`
- **Web 服务器权限场景**：所有者完全控制 + 组只读 + 其他人无权限（640/750），配合 SGID 保持组一致性

## 下一步

第七章将进入**磁盘与存储管理**，学习如何查看磁盘空间（`df`/`du`）、分区操作（`fdisk`）、格式化（`mkfs`）、挂载卸载（`mount`/`umount`），以及磁盘空间告警的排查流程。这些是服务器运维的基本功，当你遇到"磁盘满了"的告警时，第七章就是你的救援手册。

---

> [!note]
> 磁盘空间告警是运维工作中最常见的"深夜电话"触发源之一。本章将系统性地讲解 Linux 磁盘与存储管理相关的核心命令：如何查看磁盘空间（df）、统计目录大小（du）、识别块设备（lsblk）、创建分区（fdisk）、格式化文件系统（mkfs）以及挂载和卸载（mount/umount）。学完本章，你不仅能独立完成磁盘管理的日常操作，还能按流程高效排查磁盘空间告警。

---

## 7.1 查看磁盘空间：df

`df`（disk free）用于查看文件系统的磁盘空间使用情况。它是接到磁盘告警后第一个应该敲下的命令。

### 基本用法

```bash
df                     # 查看所有文件系统的空间使用（单位是 KB）
df -h                  # 人类可读格式（MB/GB/TB）——最常用
df -h /                # 只看根分区
df -h /var/log         # 只看 /var/log 所在分区
df -hT                 # 显示文件系统类型（ext4、xfs、tmpfs 等）
df -i                  # 查看 inode 使用情况
```

**输出示例**：
```bash
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        98G   45G   53G  46% /
/dev/sda2       492G  312G  180G  64% /home
tmpfs            32G  2.1G   30G   7% /dev/shm
/dev/sdb1       3.6T  2.8T  800G  78% /data
```

每一列的含义：

| 列 | 说明 |
|----|------|
| Filesystem | 块设备文件（如 `/dev/sda1`）或虚拟文件系统（如 `tmpfs`） |
| Size | 总容量 |
| Used | 已用空间 |
| Avail | 可用空间 |
| Use% | 使用率百分比 |
| Mounted on | 挂载点（在哪个目录下访问该文件系统） |

> [!tip] 关注 Use% 还是 Avail？
> 多数监控系统根据 **Use%** 告警（如超过 80% 警告、90% 严重）。但在大容量磁盘上，就算 Use% 只有 70%，如果还剩几百 GB 也不急于处理。实践中两个指标都要看：
> ```bash
> # 找出使用率超过 80% 的分区
> df -h | awk 'NR>1 && $5 ~ /^[8-9][0-9]%|100%/ {print $0}'
> ```
> 这个命令跳过标题行（NR>1），筛选第五列以 8、9 开头或 100% 的行。

### 为什么还要看 inode

`df -i` 检查 inode（索引节点）使用情况。inode 是文件系统用于存储文件元数据（权限、大小、位置等）的数据结构。每个文件或目录占用一个 inode。

```bash
$ df -i /data
Filesystem     Inodes IUsed  IFree IUse% Mounted on
/dev/sdb1      244M  244M     0   100% /data
```

> [!warning] inode 耗尽：磁盘有空间但写不进文件
> 一个经典场景：`df -h` 显示还有大量剩余空间，但创建新文件时报错 "No space left on device"。原因是 **inode 耗尽了**。常见于：
> - 邮件服务器队列里有海量小文件
> - 缓存目录产生了数百万个 tiny 文件
> - 程序 BUG 导致无限创建空文件
>
> 排查方法：
> ```bash
> df -i              # 查看 inode 使用率
> find /data -type f | wc -l   # 统计文件数，确认是否 inode 耗尽
> ```

---

## 7.2 统计目录大小：du

`du`（disk usage）用于统计文件或目录占用的磁盘空间。和 `df` 不同，`du` 是递归计算目录下所有文件的总大小。

### 基本用法

```bash
du -sh /var/log              # 查看 /var/log 目录总大小
du -sh /var/log/*.log        # 查看特定文件的大小
du -h --max-depth=1 /home    # 查看 /home 下每个子目录的大小（仅一层）
du -h --max-depth=2 /var     # 查看两层深度的子目录大小
```

**输出示例**：
```bash
$ du -sh /var/log
2.3G    /var/log

$ du -h --max-depth=1 /var/log
1.2G    /var/log/journal
600M    /var/log/nginx
200M    /var/log/syslog
150M    /var/log/auth.log
...
```

### 常用选项速查

| 选项 | 说明 |
|------|------|
| `-s` | 汇总（只显示总计，不列出子目录） |
| `-h` | 人类可读格式 |
| `--max-depth=N` | 限制显示深度 |
| `-c` | 最后显示总计 |
| `-d 1` | 等价于 `--max-depth=1` |

### 实战：找出大文件和目录

这是 `du` 最常用的场景——排查什么占了这么多空间：

```bash
# 找到当前目录下最大的 10 个文件/目录
du -sh ./* | sort -rh | head -10

# 如果文件太多，先限制数量
du -sh ./* | sort -rh | head -10

# 隐藏文件也要检查（以 . 开头的文件）
du -sh .[!.]* ./* 2>/dev/null | sort -rh | head -10
```

**输出示例**：
```bash
$ du -sh ./* | sort -rh | head -5
45G     ./docker
23G     ./node_modules
12G     ./logs
8.5G    ./build
3.2G    ./data
```

> [!tip] sort -rh 的含义
> - `-r`：逆序（从大到小）
> - `-h`：按人类可读数字排序（能识别 K、M、G 后缀，而非字母序）
>
> 如果没有 `-h`，"45G" 会被排到 "8.5G" 前面（按字母序 '4' < '8'），这显然是错的。

### 递归查找所有超过指定大小的文件

配合 `find` 可以直接定位大文件而非目录：

```bash
# 查找 /var 下大于 500MB 的文件
find /var -type f -size +500M -exec ls -lh {} \; 2>/dev/null

# 更高效的方式：仅列出大小和路径
find /var -type f -size +500M -exec du -h {} \; 2>/dev/null | sort -rh
```

### du 和 df 的数据为什么不一致

偶尔会遇到 `du -sh /data` 显示用了 500G，但 `df -h /data` 显示用了 800G 的情况。差异通常来自：

1. **已删除但仍在被占用的文件**：某个进程打开了一个大文件，删除了它但未释放文件句柄。`df` 能看到实际占用的空间，而 `du` 算不到已删除的文件。
2. **挂载点隐藏**：如果 `/data` 下还有子挂载点（如 `/data/nfs`），`du` 默认不会跨文件系统统计。

> [!warning] 定位"已删除但未释放"的文件
> 这是磁盘排查的经典场景——`df` 显示空间不足，但 `du` 加总远小于 `df`。
> ```bash
> # 找出已被删除但仍在被进程占用的文件
> sudo lsof | grep deleted
> 
> # 或者针对特定挂载点
> sudo lsof +L1 /data
> ```
> 找到后重启对应进程或 `> /proc/PID/fd/FD` 清空文件内容，空间就会释放。

---

## 7.3 查看块设备：lsblk

`lsblk`（list block devices）以树状结构列出系统中的所有块设备。在你连接一块新硬盘、插上 U 盘或需要了解磁盘拓扑时，这是第一个使用的命令。

### 基本用法

```bash
lsblk                     # 默认树状视图
lsblk -f                  # 显示文件系统类型和 UUID（最常用）
lsblk -l                  # 列表视图（非树状）
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,UUID  # 自定义输出列
```

**输出示例**：
```bash
$ lsblk -f
NAME   FSTYPE LABEL   UUID                                 MOUNTPOINT
sda
├─sda1 ext4           a1b2c3d4-...                         /
├─sda2 ext4           e5f6g7h8-...                         /home
└─sda3 swap           i9j0k1l2-...                         [SWAP]
sdb
└─sdb1 ext4   data    m3n4o5p6-...                         /data
nvme0n1
└─nvme0n1p1 ext4           q7r8s9t0-...                    /mnt/nvme
```

树状结构清晰展示了设备之间的父子关系：

| 层级 | 含义 |
|------|------|
| `sda` | 物理磁盘（父设备） |
| `sda1`, `sda2`, `sda3` | 磁盘上的分区（子设备） |
| `nvme0n1` | NVMe 固态硬盘 |
| `nvme0n1p1` | NVMe 硬盘上的分区 |

> [!tip] 设备命名规则
> - `sd` 开头：SATA/SAS/SCSI 磁盘（sda、sdb、sdc...）
> - `nvme` 开头：NVMe 固态硬盘（nvme0n1、nvme1n1...）
> - `vd` 开头：虚拟磁盘（常见于云服务器和虚拟机）
> - `hd` 开头：老式 IDE 磁盘（基本已淘汰）

### blkid — 查看块设备属性

`blkid` 专注于显示块设备的属性信息（UUID、文件系统类型、LABEL 等），适合脚本解析：

```bash
blkid                      # 查看所有块设备属性
blkid /dev/sdb1            # 查看指定分区
blkid -o value -s UUID /dev/sdb1   # 只输出 UUID 值（脚本友好）
```

**输出示例**：
```bash
$ blkid
/dev/sda1: UUID="a1b2c3d4-..." BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="abc..."
/dev/sda2: UUID="e5f6g7h8-..." BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="def..."
/dev/sdb1: LABEL="data" UUID="m3n4o5p6-..." BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="ghi..."
```

UUID（Universally Unique Identifier）是文件系统的全局唯一标识符。在 `/etc/fstab` 中通过 UUID 引用分区比使用设备名（如 `/dev/sdb1`）更可靠，因为设备名可能因硬件顺序变化而改变，而 UUID 是固定的。

---

## 7.4 磁盘分区：fdisk

当你添加了一块新硬盘，第一步就是对它进行分区。`fdisk` 是最经典的分区工具。

> [!warning] 分区操作有风险
> `fdisk` 是**破坏性操作**。操作前务必确认目标磁盘：
> 1. 用 `lsblk` 确认设备名
> 2. 确认没有重要数据
> 3. 建议在虚拟机或测试环境中练习

### 查看分区表

```bash
sudo fdisk -l                    # 列出所有磁盘的分区表
sudo fdisk -l /dev/sdb           # 只看指定磁盘
```

**输出示例**：
```bash
$ sudo fdisk -l /dev/sdb
Disk /dev/sdb: 1 TiB, 1099511627776 bytes, 2147483648 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt

Device     Start       End   Sectors   Size Type
/dev/sdb1   2048 2147483647 2147481600  1024G Linux filesystem
```

### 交互式分区操作

```bash
sudo fdisk /dev/sdb              # 进入交互模式
```

常用交互命令（在 `fdisk` 提示符下输入）：

| 命令 | 功能 |
|------|------|
| `m` | 显示帮助 |
| `p` | 打印当前分区表 |
| `n` | 创建新分区 |
| `d` | 删除分区 |
| `t` | 修改分区类型 |
| `w` | 写入并退出（**确认无误后才执行**） |
| `q` | 不保存退出 |

> [!example] 创建一个新分区的完整流程
> ```bash
> # 1. 确认设备
> $ lsblk
> sdb                       8:16   0   1T  0 disk
> 
> # 2. 进入 fdisk
> $ sudo fdisk /dev/sdb
> 
> Command (m for help): n           # 创建新分区
> Partition number (1-128, default 1): 1
> First sector (2048-2147483647, default 2048): [直接回车]
> Last sector: [直接回车，使用全部空间]
> 
> Created a new partition 1 of type 'Linux filesystem' and of size 1 TiB.
> 
> Command (m for help): p           # 确认分区表
> 
> Command (m for help): w           # 写入分区表并退出
> The partition table has been altered.
> Calling ioctl() to re-read partition table.
> Syncing disks.
> 
> # 3. 验证
> $ lsblk /dev/sdb
> sdb                       8:16   0   1T  0 disk
> └─sdb1                    8:17   0   1T  0 part
> ```

### parted — 处理 2TB 以上的磁盘

对于 GPT 分区表或 2TB 以上的磁盘，`fdisk` 也能处理，但 `parted` 在脚本化和大容量磁盘场景下更常用：

```bash
# 创建 GPT 分区表（-s 静默模式，无交互）
sudo parted /dev/sdc mklabel gpt

# 创建分区（从 0% 到 100% 使用全部空间）
sudo parted /dev/sdc mkpart primary 0% 100%

# 查看分区表
sudo parted /dev/sdc print
```

> [!tip] MBR vs GPT
> | 特性 | MBR（传统） | GPT（现代） |
> |------|:---:|:---:|
> | 最大磁盘容量 | 2TB | 约 9.4ZB |
> | 最大主分区数 | 4 | 128 |
> | 分区表备份 | 无 | 磁盘头和尾各存一份 |
> | 兼容性 | 所有系统 | 需 UEFI 支持 |
>
> 新磁盘建议一律使用 GPT。如果磁盘是用于老旧的 BIOS 启动系统，可能需要 MBR。

---

## 7.5 格式化文件系统：mkfs

分区创建完成后，还需要在上面创建文件系统（即格式化），才能存储文件。

### 基本用法

```bash
# 格式化为 ext4（最通用的 Linux 文件系统）
sudo mkfs.ext4 /dev/sdb1

# 格式化为 xfs（适合大文件和高并发场景）
sudo mkfs.xfs /dev/sdb1

# 创建时指定卷标（方便识别）
sudo mkfs.ext4 -L data /dev/sdb1

# 格式化时跳过确认（脚本中使用）
sudo mkfs.ext4 -F /dev/sdb1
```

**输出示例**：
```bash
$ sudo mkfs.ext4 -L data /dev/sdb1
mke2fs 1.46.5 (30-Dec-2021)
Creating filesystem with 268435456 4k blocks and 67108864 inodes
Filesystem UUID: m3n4o5p6-...
Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736, ...
Allocating group tables: done
Writing inode tables: done
Creating journal (262144 blocks): done
Writing superblocks and filesystem accounting information: done
```

### 常用文件系统对比

| 文件系统 | 格式命令 | 适用场景 | 最大文件 | 最大分区 |
|----------|----------|----------|----------|----------|
| ext4 | `mkfs.ext4` | 通用场景，最兼容 | 16TB | 1EB |
| xfs | `mkfs.xfs` | 大文件、高并发 | 8EB | 8EB |
| btrfs | `mkfs.btrfs` | 快照、压缩、校验 | 16EB | 16EB |
| ntfs | `mkfs.ntfs` | 与 Windows 交换数据 | 16EB | 256TB |
| vfat | `mkfs.vfat` | U 盘、ESP 分区 | 4GB | 2TB |

> [!tip] 如何选择文件系统
> - **不确定时选 ext4**：它是 Linux 的默认文件系统，稳定、成熟、兼容性最好
> - **大文件存储（如视频、数据库）选 xfs**：在并行 I/O 和大文件处理上性能更优
> - **需要快照/压缩功能选 btrfs**：功能丰富但复杂度更高
> - **要和 Windows 共用选 ntfs**：Linux 支持读写 NTFS

> [!warning] 格式化 = 清空数据
> `mkfs` 会覆盖分区上的所有数据。执行前务必确认设备名是否正确。一个常见的代价高昂的错误：
> ```bash
> # 悲剧：本意是格式化 /dev/sdb1，手误写成 /dev/sda1（系统盘！）
> sudo mkfs.ext4 /dev/sda1   # 系统瞬间崩溃
> ```
> **对策**：格式化前每次都执行 `lsblk` 和 `blkid` 双重确认。

---

## 7.6 挂载与卸载：mount / umount

格式化完成后，你需要把文件系统"挂载"到某个目录下才能访问。挂载是 Linux 文件系统的核心概念——物理上存储设备的文件通过挂载点和目录树建立关联。

### mount — 挂载

```bash
# 基本挂载
sudo mount /dev/sdb1 /mnt/data

# 指定文件系统类型（通常自动检测，大部分场景不需要加 -t）
sudo mount -t ext4 /dev/sdb1 /mnt/data

# 挂载时指定选项
sudo mount -o rw,noatime /dev/sdb1 /mnt/data
```

### umount — 卸载

```bash
# 通过挂载点卸载（推荐）
sudo umount /mnt/data

# 通过设备文件卸载
sudo umount /dev/sdb1

# 如果设备繁忙，强制卸载（慎用）
sudo umount -f /mnt/data
```

> [!warning] umount: target is busy
> 卸载时最常见的错误：
> ```bash
> $ sudo umount /mnt/data
> umount: /mnt/data: target is busy.
> ```
> 原因是有进程正在使用该挂载点下的文件或目录。排查方法：
> ```bash
> # 找出正在使用该挂载点的进程
> sudo lsof /mnt/data
> 
> # 或者用 fuser
> sudo fuser -v /mnt/data
> 
> # 杀掉占用进程（谨慎）
> sudo fuser -km /mnt/data
> 
> # 或使用懒卸载（等待所有占用结束后自动卸载）
> sudo umount -l /mnt/data
> ```

### 配置开机自动挂载：/etc/fstab

每次重启后手动挂载显然不现实。`/etc/fstab` 文件定义了系统启动时自动挂载的文件系统。

**/etc/fstab 文件格式**：
```
<设备>        <挂载点>  <文件系统>  <挂载选项>  <dump>  <pass>
UUID=xxx      /         ext4        defaults    0       1
UUID=yyy      /home     ext4        defaults    0       2
UUID=zzz      /data     ext4        defaults    0       0
//nas/share   /mnt/nfs  nfs4        defaults    0       0
```

每列说明：

| 列 | 含义 | 示例 |
|----|------|------|
| 设备 | 分区设备或 UUID | `UUID="m3n4o5p6-..."` 或 `/dev/sdb1` |
| 挂载点 | 挂载到的目录 | `/data` |
| 文件系统 | 文件系统类型 | `ext4`、`xfs`、`nfs4` |
| 挂载选项 | 挂载参数 | `defaults`、`noatime` 等 |
| dump | 是否备份（0=不备份） | 通常为 `0` |
| pass | 开机检查顺序（0=不检查, 1=根分区, 2=其他） | `0` |

> [!example] 添加新磁盘到 /etc/fstab
> ```bash
> # 1. 获取新分区的 UUID
> $ sudo blkid /dev/sdb1
> /dev/sdb1: LABEL="data" UUID="m3n4o5p6-..." TYPE="ext4"
> 
> # 2. 创建挂载点
> $ sudo mkdir -p /data
> 
> # 3. 添加到 /etc/fstab（建议用 UUID 而非设备名）
> $ echo 'UUID=m3n4o5p6-...  /data  ext4  defaults  0  0' | sudo tee -a /etc/fstab
> 
> # 4. 验证 fstab 配置（无需重启即可测试）
> $ sudo mount -a
> # 如果没有输出，说明配置正确（有错误会直接报错）
> 
> # 5. 确认已挂载
> $ df -h /data
> Filesystem      Size  Used Avail Use% Mounted on
> /dev/sdb1       1.0T   89M 1014G   1% /data
> ```

> [!tip] 为什么用 UUID 而不是 /dev/sdb1
> 设备名（`/dev/sdb1`）由内核按检测顺序分配。如果：
> - 增加了新硬盘
> - 硬盘的 SATA 接口插拔顺序改变
> - 从一台机器移到另一台
>
> 设备名可能变化。而 UUID 是文件系统创建时生成的唯一标识，永不改变。在 `/etc/fstab` 中使用 UUID，磁盘顺序变化后系统仍然能正确挂载。

### 常用挂载选项

| 选项 | 作用 | 适用场景 |
|------|------|----------|
| `defaults` | `rw, suid, dev, exec, auto, nouser, async` | 通用场景 |
| `noatime` | 不更新访问时间，减少写操作 | 日志服务器、数据库存储 |
| `noexec` | 禁止在该分区执行程序 | `/tmp`、`/var/tmp` 等安全敏感目录 |
| `nosuid` | 忽略 SUID 位 | 非系统分区 |
| `ro` | 只读挂载 | 备份光盘、恢复维护 |
| `size=2G` | 设置 tmpfs 大小限制 | `/tmp` 等内存文件系统 |

> [!example] 安全加固：将 /tmp 改为 noexec
> ```bash
> # 编辑 /etc/fstab，将 /tmp 行改为：
> tmpfs   /tmp   tmpfs   defaults,noexec,nosuid,size=2G   0   0
> ```
> 这样即使有恶意程序下载到 `/tmp`，也无法执行。此配置在安全加固场景中很常见。

---

## 7.7 管理交换分区：swap

交换分区（swap）是磁盘上划出来作为"虚拟内存"的区域。当系统物理内存不足时，将不活跃的内存页换出到磁盘。

### 查看 swap

```bash
swapon --show              # 查看当前启用的 swap
free -h                    # 查看内存和 swap 使用情况
```

**输出示例**：
```bash
$ swapon --show
NAME      TYPE  SIZE USED PRIO
/dev/sda3 partition  8G   0K   -2

$ free -h
              total        used        free      shared  buff/cache   available
Mem:           31Gi        15Gi        12Gi       2.1Gi       4.0Gi        14Gi
Swap:         8.0Gi          0B       8.0Gi
```

### 创建 swap 文件（推荐方式）

相比 swap 分区，swap 文件更灵活，无需重新分区：

```bash
# 1. 创建一个 2GB 的 swap 文件
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048 status=progress

# 2. 设置正确权限（swap 文件必须仅 root 可读写）
sudo chmod 600 /swapfile

# 3. 格式化为 swap 格式
sudo mkswap /swapfile

# 4. 启用 swap 文件
sudo swapon /swapfile

# 5. 验证
sudo swapon --show
```

### 启用/禁用 swap

```bash
sudo swapon /dev/sda3       # 启用指定 swap 分区
sudo swapoff /dev/sda3      # 禁用指定 swap 分区
sudo swapoff -a             # 禁用所有 swap
sudo swapon -a              # 启用 /etc/fstab 中所有 swap
```

添加到 `/etc/fstab` 实现开机自动启用：

```
/swapfile  none  swap  defaults  0  0
```

> [!tip] 何时需要 swap
> - 内存较小的服务器（< 4GB）：建议配置 swap 防止 OOM
> - 内存充足的服务器（> 16GB）：swap 主要用于应对突发峰值
> - 数据库服务器：通常不建议使用 swap（会严重影响性能），应配置足够的物理内存
> - 容器的宿主机：建议保留少量 swap 作为安全垫

---

## 7.8 实战：磁盘空间告警排查流程

当收到磁盘空间告警（如根分区使用率超过 90%），以下排查流程可以帮你快速定位问题并恢复。

### 第 1 步：确认告警范围

```bash
# 查看所有分区的使用情况
df -h

# 只看根分区
df -h /

# 如果怀疑 inode 问题
df -i /
```

**预期输出**：确认哪个分区吃紧。可能是根分区 `/`，也可能是 `/var`、`/home`、`/data` 等。

### 第 2 步：定位大目录

```bash
# 从根分区开始逐层定位
cd /
sudo du -sh ./* 2>/dev/null | sort -rh | head -10
```

**预期输出**：
```bash
45G     /var
32G     /home
12G     /usr
8.5G    /opt
```

看到 `/var` 最大，进入下一步。

### 第 3 步：逐层深入

```bash
# 深入最大目录
sudo du -h --max-depth=1 /var | sort -rh | head -10
```

**预期输出**：
```bash
30G     /var/log
8.5G    /var/lib
3.2G    /var/cache
1.8G    /var/tmp
```

发现 `/var/log` 最大，继续深入：

```bash
sudo du -h --max-depth=1 /var/log | sort -rh | head -10
```

### 第 4 步：确认具体问题

| 告警类型 | 表现 | 典型原因 |
|----------|------|----------|
| 日志膨胀 | `/var/log` 下某个日志文件特别大 | Nginx 访问日志未轮转、应用疯狂打日志 |
| 容器镜像堆积 | `/var/lib/docker` 占用大量空间 | 未清理的旧镜像和停止的容器 |
| 缓存文件 | `/var/cache` 或 `/tmp` 占用过高 | 包管理器缓存、临时构建文件 |
| 已删除未释放 | `df` 显示高但 `du` 加总对不上 | 进程持有已删除文件的句柄 |

### 第 5 步：执行清理

**场景 A：日志文件过大**
```bash
# 查看具体哪个日志文件最大
sudo ls -lhS /var/log/*.log | head -5

# 安全清空（使用 truncate，不要 rm 后重启服务）
sudo truncate -s 0 /var/log/nginx/access.log

# 或使用 logrotate 手动轮转
sudo logrotate -f /etc/logrotate.d/nginx
```

> [!tip] 为什么用 truncate 而不是 rm
> ```bash
> # 错误做法
> sudo rm /var/log/nginx/access.log       # 删除后 nginx 仍持有句柄，空间不释放
> sudo systemctl restart nginx            # 重启才能释放，但会造成服务中断
> 
> # 正确做法
> sudo truncate -s 0 /var/log/nginx/access.log  # 清空内容，句柄不受影响
> # 服务无需重启，空间立即释放
> ```

**场景 B：Docker 占用大量空间**
```bash
# 查看 Docker 磁盘使用情况
docker system df

# 清理未使用的容器、镜像、网络
docker system prune -a -f

# 或更精确的清理
docker image prune -a      # 清理未被使用的镜像
docker container prune     # 清理已停止的容器
docker volume prune        # 清理未被使用的卷
```

**场景 C：包管理器缓存**
```bash
# apt 缓存
sudo apt clean                        # 清空 /var/cache/apt/archives
sudo apt autoremove                   # 清理不再需要的依赖

# yum/dnf 缓存（CentOS/RHEL/Fedora）
sudo yum clean all
sudo dnf clean all
```

**场景 D：已删除但未释放的文件**
```bash
# 定位占用进程
sudo lsof /var/log | grep deleted
# 或针对整个根分区
sudo lsof +L1 /

# 确认后，要么重启进程，要么 > 文件描述符
sudo systemctl restart nginx    # 重启服务
# 或直接清空 proc 文件系统中的 fd
# > /proc/PID/fd/FD             # 高风险操作，需确定文件
```

### 第 6 步：预防复发

```bash
# 1. 检查 logrotate 配置是否正常
sudo logrotate -d /etc/logrotate.d/nginx   # dry-run 模式

# 2. 设置日志保留策略（编辑 /etc/logrotate.d/nginx）
```

**示例 logrotate 配置**：
```
/var/log/nginx/*.log {
    daily           # 每天轮转
    rotate 7        # 保留 7 份
    compress        # 压缩旧日志
    delaycompress   # 延迟一天压缩
    missingok       # 日志文件不存在时不报错
    notifempty      # 空文件不轮转
    postrotate
        service nginx reload > /dev/null 2>&1 || true
    endscript
}
```

### 排查流程速查

```bash
# 一行命令快速排查（从根分区下找出最大的 5 个目录）
df -h / && echo "---" && sudo du -sh /* 2>/dev/null | sort -rh | head -5
```

> [!example] 完整排查脚本示例
> ```bash
> #!/bin/bash
> # 磁盘空间告警排查脚本
> 
> ALERT_THRESHOLD=80
> 
> echo "=== 磁盘使用率概览 ==="
> df -h | awk -v threshold=$ALERT_THRESHOLD 'NR>1 && $5+0 > threshold {print "⚠️ " $0}'
> 
> echo ""
> echo "=== 根分区最大目录 Top 10 ==="
> sudo du -sh /* 2>/dev/null | sort -rh | head -10
> 
> echo ""
> echo "=== 检查已删除但未释放的文件 ==="
> deleted_count=$(sudo lsof +L1 / 2>/dev/null | wc -l)
> if [ $deleted_count -gt 0 ]; then
>     echo "⚠️ 发现 $deleted_count 个已删除但未释放的文件"
>     sudo lsof +L1 / 2>/dev/null | head -10
> else
>     echo "✓ 未发现"
> fi
> 
> echo ""
> echo "=== 检查 inode 使用率 ==="
> df -i | awk 'NR>1 && $5+0 > 90 {print "⚠️ " $0}'
> ```

---

## 本章总结

- **df -h** 是检查磁盘空间的第一命令，用于查看整个文件系统的使用概览；**df -i** 检查 inode 是否耗尽
- **du -sh** 统计目录总大小，**du -sh \* | sort -rh** 找出最大的子目录，适用于精准定位空间占用源头
- **lsblk -f** 以树状结构查看块设备，支持显示文件系统类型和 UUID，是新磁盘场景下的**第一个命令**
- **fdisk** 用于磁盘分区操作，交互模式中输入 `m` 查看帮助、`n` 新建分区、`w` 保存写入
- **mkfs.ext4 / mkfs.xfs** 在分区上创建文件系统，格式化前务必用 `lsblk` 和 `blkid` 双重确认设备名
- **mount** 挂载文件系统到目录，**umount** 卸载；使用 UUID 配置 `/etc/fstab` 实现开机自动挂载
- **磁盘告警排查六步走**：确认范围 → 定位大目录 → 逐层深入 → 确认问题 → 执行清理 → 预防复发

## 下一步

掌握了磁盘管理的核心操作后，第八章将转向 **软件包管理**，学习如何在 Debian/Ubuntu、Red Hat 系、Arch Linux 等不同发行版中进行软件安装、更新和卸载，以及如何处理常见的依赖问题和换源配置。

---

> [!note]
> 软件包管理是 Linux 日常使用中最频繁的操作之一。安装软件、更新系统、卸载不需要的程序，都离不开包管理器。不同发行版使用不同的包管理器，但核心操作逻辑是相通的。本章覆盖三大主流包管理器（apt、dnf/yum、pacman）的常用操作，并提供跨发行版对照表和常见问题的解决方案。

---

## 8.1 apt — Debian/Ubuntu 系

`apt` 是 Debian 及其衍生版（Ubuntu、Debian、Linux Mint 等）的包管理工具。它管理 `.deb` 格式的软件包，从配置好的软件源（repository）中下载安装。

### 基础命令

```bash
# 更新软件包列表（首次使用或定期执行）
sudo apt update

# 升级所有已安装的软件包
sudo apt upgrade

# 安装软件包
sudo apt install nginx

# 卸载软件包（保留配置文件）
sudo apt remove nginx

# 卸载并清除配置文件
sudo apt purge nginx

# 搜索软件包
apt search nginx

# 查看已安装的包
apt list --installed

# 查看某个包的信息
apt show nginx

# 清理不再需要的依赖
sudo apt autoremove
```

**输出示例**：
```bash
$ apt search nginx
Sorting... Done
Full Text Search... Done
nginx/stable 1.24.0-1 amd64
  small, powerful, scalable web/proxy server

nginx-extras/stable 1.24.0-1 amd64
  nginx web/proxy server with extra modules
```

### 常用组合

```bash
# 标准更新流程（先更新列表，再升级）
sudo apt update && sudo apt upgrade -y

# 安装时自动确认
sudo apt install -y htop

# 查看可升级的包
apt list --upgradable

# 清理本地下载的缓存（.deb 包）
sudo apt clean

# 只清理过时的缓存
sudo apt autoclean
```

> [!tip]
> 养成习惯：**安装前先 `sudo apt update`**。如果跳过这一步，apt 会使用过时的包列表，可能导致找不到最新版本或安装失败。

> [!warning]
> **不要混用 `apt-get` 和 `apt`？** 两者底层相同，`apt` 是 `apt-get` 的精简优化版，日常使用推荐 `apt`。但写脚本时建议用 `apt-get`，它的输出格式更稳定，适合程序解析。

---

## 8.2 dnf/yum — Red Hat 系

RHEL/CentOS/Fedora 系发行版使用 RPM 包格式。早期用 `yum`，从 RHEL 8 / CentOS 8 起 `dnf` 取代了 `yum` 成为默认包管理器。

### dnf 基础命令

```bash
# 安装软件包
sudo dnf install nginx

# 卸载软件包
sudo dnf remove nginx

# 更新所有包
sudo dnf update

# 搜索包
dnf search nginx

# 查看包信息
dnf info nginx

# 列出已安装
dnf list installed

# 清理缓存
sudo dnf clean all
```

### dnf 特色功能：事务回滚

`dnf` 的一个亮点是支持事务历史记录，可以撤销之前的操作：

```bash
# 查看历史操作
dnf history

# 撤销某次操作（按序号）
sudo dnf history undo 3

# 回滚到某个历史点
sudo dnf history rollback 2
```

### yum（历史兼容）

在 CentOS 7 及更早版本中使用 `yum`，其命令格式与 `dnf` 基本一致：

```bash
yum install nginx
yum remove nginx
yum update
yum search nginx
```

> [!note]
> `yum` 在 RHEL 8+ / CentOS 8+ 中已标记为淘汰。虽然很多系统上 `yum` 命令仍然存在（作为 `dnf` 的符号链接），但建议直接使用 `dnf`。

---

## 8.3 pacman — Arch 系

Arch Linux 及其衍生版（Manjaro、EndeavourOS 等）使用 `pacman`，它管理 `.pkg.tar.zst` 格式的包。

```bash
# 同步包数据库并更新系统
sudo pacman -Syu

# 安装包
sudo pacman -S nginx

# 卸载包（保留配置及依赖）
sudo pacman -R nginx

# 卸载包及其依赖
sudo pacman -Rs nginx

# 卸载包、依赖及配置文件
sudo pacman -Rns nginx

# 搜索包
pacman -Ss nginx

# 查看包信息
pacman -Qi nginx

# 列出所有显式安装的包
pacman -Qe

# 清理未使用的依赖（orphans）
sudo pacman -Rns $(pacman -Qtdq)
```

> [!tip]
> `pacman` 的操作选项很有规律：`-S` 表示同步（sync，安装/搜索），`-R` 表示移除（remove），`-Q` 表示查询（query）。结合后缀字母，`-Ss` 搜索、`-Si` 查看信息、`-Su` 更新。记住这个规律后基本不用查文档。

> [!warning]
> Arch 是滚动更新（rolling release）发行版，建议**定期执行 `pacman -Syu`**（至少每周一次）。长时间不更新会导致系统状态过老，下次更新时可能遇到大量冲突，解决起来更麻烦。

---

## 8.4 跨发行版命令对照

以下表格整理了三大包管理器在相同操作下的对应命令，方便你在不同发行版之间切换时快速参考：

| 操作 | apt (Debian/Ubuntu) | dnf (RHEL 8+/Fedora) | pacman (Arch) |
|------|---------------------|---------------------|--------------|
| 更新包列表 | `apt update` | `dnf check-update` | `pacman -Sy` |
| 安装包 | `apt install pkg` | `dnf install pkg` | `pacman -S pkg` |
| 卸载包 | `apt remove pkg` | `dnf remove pkg` | `pacman -R pkg` |
| 清除配置卸载 | `apt purge pkg` | — | `pacman -Rns pkg` |
| 更新所有包 | `apt upgrade` | `dnf update` | `pacman -Su` |
| 搜索包 | `apt search kw` | `dnf search kw` | `pacman -Ss kw` |
| 查看包信息 | `apt show pkg` | `dnf info pkg` | `pacman -Qi pkg` |
| 列出已安装 | `apt list --installed` | `dnf list installed` | `pacman -Q` |
| 清理缓存 | `apt clean` | `dnf clean all` | `pacman -Sc` |
| 清理孤立依赖 | `apt autoremove` | `dnf autoremove` | `pacman -Rns $(pacman -Qtdq)` |
| 回滚事务 | — | `dnf history undo N` | — |

> [!note]
> `apt` 没有原生的事务回滚功能，但可以通过查看 `/var/log/apt/history.log` 来追溯安装记录。在关键操作前使用快照（如 `timeshift`）是更稳妥的备份方式。

### 快速识别你用的是哪个包管理器

```bash
# 查看系统发行版
cat /etc/os-release

# 或使用 hostnamectl
hostnamectl

# 如果分不清，试试哪个命令存在
which apt dnf yum pacman zypper 2>/dev/null
```

---

## 8.5 常见问题与解决

### 换源（更换国内镜像源）

默认软件源在海外，下载速度可能很慢。更换为国内镜像源是最常见的优化操作。

**apt 换源（Ubuntu 示例）**：

```bash
# 备份原始源文件
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 编辑源列表
sudo vim /etc/apt/sources.list

# 将 archive.ubuntu.com 替换为国内镜像
# 例如：中科大镜像 mirrors.ustc.edu.cn
# 或：阿里云 mirrors.aliyun.com
# 或：清华 mirrors.tuna.tsinghua.edu.cn

# 替换后更新
sudo apt update && sudo apt upgrade
```

**dnf 换源（Fedora 示例）**：

```bash
# 启用最快的镜像（自动选择）
sudo dnf install dnf-plugin-fastestmirror

# 或手动指定源配置文件
# /etc/yum.repos.d/ 下的 .repo 文件可逐个编辑
```

> [!tip]
> 换源后务必执行 `apt update` 或 `dnf check-update` 刷新包列表，否则新源不会生效。

### 依赖修复

**apt**：

```bash
# 修复破损的依赖
sudo apt --fix-broken install

# 重新配置所有未完成的包
sudo dpkg --configure -a

# 如果某个包下载中断，重新安装
sudo apt install --reinstall package-name
```

**dnf**：

```bash
# 检查并修复依赖问题
sudo dnf check
sudo dnf reinstall package-name

# 如果问题复杂，尝试 distro-sync（同步到发行版版本）
sudo dnf distro-sync
```

**pacman**：

```bash
# 重新安装某个包
sudo pacman -S package-name

# 检查损坏的包
pacman -Qk

# 强制刷新并更新
sudo pacman -Syyu
```

### 锁定版本（防止误升级）

有时需要固定某个包的版本，不让它随系统更新：

```bash
# apt：标记为 hold
sudo apt-mark hold nginx
sudo apt-mark showhold          # 查看所有锁定的包
sudo apt-mark unhold nginx      # 解锁

# dnf：在配置中添加 exclude
sudo dnf update --exclude=nginx
# 或写入 /etc/dnf/dnf.conf: exclude=nginx kernel*

# pacman：编辑 /etc/pacman.conf，在 IgnorePkg 中加入包名
IgnorePkg = nginx
```

### 常见问题速查

| 现象 | 大概率原因 | 解决 |
|------|-----------|------|
| `Unable to locate package` | 包列表过期（或包名手误） | 先 `apt update` 再试 |
| `Could not get lock /var/lib/dpkg/lock` | 有其他 apt 进程在运行 | 等它结束，或 `sudo kill` 进程后 `sudo rm /var/lib/dpkg/lock`（慎用） |
| `dpkg: error processing package xxx` | 包安装中断或损坏 | `sudo dpkg --configure -a` |
| `The following packages have been kept back` | 依赖冲突或配置变更 | `apt upgrade --with-new-pkgs` 或 `apt dist-upgrade` |
| `404 Not Found [IP: ...]` | 源地址失效 | 换源或更新源配置 |
| `GPG error: ... NO_PUBKEY` | 缺少 GPG 公钥 | `sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys <KEY_ID>` |

> [!warning]
> `apt` 操作时如果遇到 `Could not get lock` 错误，**优先确认是否有其他进程在运行**（如后台自动更新），不要直接删锁文件。只有确认没有其他 apt 进程时，才删除锁文件。

---

## 本章总结

- **apt** 是 Debian/Ubuntu 系的包管理器，操作直觉且成熟稳定，日常记住 `update` / `install` / `remove` / `autoremove` 四个核心命令即可。
- **dnf** 是 Red Hat 系的新一代包管理器，替代了旧版 `yum`，支持事务回滚是它的一大优势。
- **pacman** 是 Arch 系的包管理器，命令选项规律性极强（`-S` 同步、`-R` 移除、`-Q` 查询），学会规律后效率很高。
- **跨发行版对照表** 可以在不同系统间快速切换，核心操作逻辑是相通的。
- **换源和依赖修复** 是最常见的包管理问题，掌握对应的修复命令能节省大量时间。
- 锁定版本功能在**生产环境**中非常实用，可以防止关键服务被意外升级。

### 下一步

包管理是系统运维的基础，下一章我们将跳出单个命令的视角，学习 **Shell 实用技巧与命令组合**，看看如何通过管道、重定向和别名等技巧，把学过的命令串起来解决更复杂的实际问题。

---

> [!note]
> 本章是全书"从会用到用好"的进阶篇章。你将系统学习 Shell 的高效使用技巧：管道与重定向的灵活组合、环境变量配置、别名与命令历史、终端快捷键，以及大量实用的一行命令案例。掌握这些技巧后，你的命令行效率将提升一个台阶。

---

## 9.1 管道 `|`：命令的"流水线"

管道是 Linux 哲学"**每个命令只做一件事，组合起来做大事**"的核心体现。管道操作符 `|` 将前一个命令的标准输出（stdout）连接到后一个命令的标准输入（stdin），形成处理流水线。

### 基本模型

```bash
命令1 | 命令2 | 命令3
# 命令1 的输出 → 命令2 的输入 → 命令3 的输入
```

数据从左向右流动，每个命令只处理上一级的结果输出自己的结果，不产生中间文件。

### 经典管道组合

```bash
# 分页查看长输出
dmesg | less

# 从进程列表中搜索特定进程
ps aux | grep nginx

# 统计日志中某个关键词出现次数
grep "ERROR" app.log | wc -l

# 查看磁盘占用最大的目录
du -sh ./* | sort -rh | head -5
```

> [!tip] 管道的思维模式
> 把管道想象成工厂流水线：每个工位（命令）只处理一件事，上一个工位的成品直接传给下一个。这种思维可以帮助你逐步搭建复杂命令组合。

### 管道链中的常见误区

**误区 1：管道只传递 stdout，不传递 stderr**

```bash
# 假设当前目录不存在文件 "nonexist"
ls nonexist 2>&1 | grep "No such file"   # 需要把 stderr 重定向到 stdout
```

如果不做 `2>&1`，`ls` 的错误信息走 stderr，不会被管道传递，即使你写 `| grep` 也抓不到。

**误区 2：管道左侧的变量修改不会影响右侧**

```bash
# 下面的代码不会按你预期工作
count=0
ps aux | while read line; do
    ((count++))
done
echo $count   # 输出 0，因为 while 在子 Shell 中运行
```

> [!warning] 管道创建子 Shell
> 管道右侧的命令运行在子 Shell（subshell）中，对变量的修改不会传递到父 Shell。如果要累积结果，考虑使用 `process substitution` 或临时文件。

---

## 9.2 重定向：控制数据的流向

重定向让你决定命令的输入从哪来、输出到哪去。理解重定向是编写可靠脚本和排查问题的前提。

### 三个标准流

| 文件描述符 | 名称 | 符号 | 默认目标 |
|-----------|------|------|---------|
| 0 | stdin（标准输入） | `<` | 键盘 |
| 1 | stdout（标准输出） | `>` / `>>` | 终端屏幕 |
| 2 | stderr（标准错误） | `2>` / `2>>` | 终端屏幕 |

### 输出重定向

```bash
# 覆盖写入（危险！会用空文件覆盖原内容）
echo "hello" > file.txt

# 追加写入（安全，保留原有内容）
echo "world" >> file.txt

# 查看结果
cat file.txt
# 输出:
# hello
# world
```

> [!warning] `>` 的截断风险
> `>` 会**在命令执行前就清空目标文件**。下面的命令会先清空 `config.yaml`，然后 `grep` 从空文件读入，等于什么都没做，但原文件已经没了：
> ```bash
> grep "server" config.yaml > config.yaml   # 灾难！config.yaml 变空
> ```
> **正确做法**：输出到临时文件再重命名
> ```bash
> grep "server" config.yaml > config.tmp && mv config.tmp config.yaml
> ```

### 错误重定向

```bash
# 只将错误信息重定向到文件
find / -name "*.py" 2> errors.log

# 追加错误信息
find / -name "*.py" 2>> errors.log

# 丢弃错误信息
find / -name "*.py" 2> /dev/null
```

### 合并 stdout 和 stderr

这是日常使用频率最高的重定向技巧：

```bash
# 方法 1：传统写法（最通用）
command > output.log 2>&1

# 方法 2：Bash 4+ 简化写法（推荐）
command &> output.log

# 方法 3：追加模式合并
command >> output.log 2>&1
command &>> output.log     # Bash 4+ 追加合并
```

> [!tip] 理解 `2>&1`
> `2>&1` 的意思是"把文件描述符 2（stderr）重定向到文件描述符 1（stdout）当前指向的位置"。注意这里的 `&1` 表示"和 fd 1 一样的位置"，没有 `&` 的话 `1` 会被理解为文件名。
>
> **关键细节**：**`2>&1` 必须放在 `>` 之后**。下面的写法是错误的：
> ```bash
> command 2>&1 > output.log   # 错误！stderr 被指向了终端（当前 stdout），只有 stdout 去了文件
> ```

### 输入重定向

```bash
# 将文件内容作为命令的输入
sort < unsorted.txt

# Here Document：在脚本中嵌入多行输入
cat << EOF > config.txt
server.name=myapp
server.port=8080
EOF

# Here String：将字符串作为命令输入
grep "error" <<< "no error found"
# 等价于 echo "no error found" | grep "error"
```

### 重定向操作符速查表

| 操作符 | 含义 | 示例 |
|--------|------|------|
| `>` | stdout 覆盖写入 | `ls > list.txt` |
| `>>` | stdout 追加写入 | `echo "done" >> log.txt` |
| `2>` | stderr 覆盖写入 | `cmd 2> err.log` |
| `2>>` | stderr 追加写入 | `cmd 2>> err.log` |
| `&>` | stdout + stderr 合并覆盖 | `cmd &> all.log` |
| `&>>` | stdout + stderr 合并追加 | `cmd &>> all.log` |
| `2>&1` | stderr 合并到 stdout | `cmd > log 2>&1` |
| `<` | 文件作为 stdin | `sort < input.txt` |
| `<<` | Here Document | `cat << EOF > file` |
| `<<<` | Here String | `grep "x" <<< "text"` |

---

## 9.3 环境变量与 PATH 配置

### 什么是环境变量

环境变量是操作系统和 Shell 共享的键值对，影响命令和程序的行为。

```bash
# 查看所有环境变量
env

# 查看单个变量
echo $HOME
echo $PATH
echo $SHELL

# 查看变量的另一种方式
printenv HOME
printenv PATH
```

### 核心环境变量

| 变量 | 含义 | 典型值 |
|------|------|--------|
| `HOME` | 当前用户家目录 | `/home/zhang` |
| `PATH` | 命令搜索路径 | `/usr/local/bin:/usr/bin:/bin` |
| `SHELL` | 当前使用的 Shell | `/bin/bash` |
| `USER` | 当前用户名 | `zhang` |
| `LANG` | 系统语言/编码 | `zh_CN.UTF-8` |
| `PWD` | 当前工作目录 | `/home/zhang/project` |
| `OLD_PWD` | 上一个工作目录 | `/tmp` |

### 设置和导出变量

```bash
# 定义 Shell 变量（仅当前 Shell 可见）
MY_VAR="hello"

# 导出为环境变量（子进程也可见）
export MY_VAR="hello"

# 一行内定义并导出
export MY_VAR="hello"

# 临时变量：只对当前命令生效
MY_VAR="hello" command
```

> [!tip] export 的作用域
> ```bash
> # 不 export：子进程看不到
> NAME="world"
> bash -c 'echo $NAME'   # 输出空行
> 
> # export 后：子进程可以看到
> export NAME="world"
> bash -c 'echo $NAME'   # 输出 world
> ```

### 深入理解 PATH

`PATH` 决定了你在终端输入命令时，Shell 去哪里找对应的可执行文件：

```bash
# 查看当前 PATH
echo $PATH
# 输出示例: /usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# 查看某个命令的位置
which python
# 输出: /usr/bin/python

# 查看命令的所有可能位置
whereis python
```

**PATH 的搜索顺序**：Shell 从左到右扫描 `:` 分隔的目录，找到第一个匹配就执行。

**常见 PATH 问题**：

```bash
# 安装了新命令但提示 "command not found"
# 很可能是因为安装目录不在 PATH 中

# 临时添加
export PATH=$PATH:/usr/local/myapp/bin

# 永久添加（写入 Shell 配置文件）
echo 'export PATH=$PATH:/usr/local/myapp/bin' >> ~/.bashrc
source ~/.bashrc
```

> [!warning] PATH 安全风险
> **永远不要把当前目录 `.` 放在 PATH 的开头**。如果有人在你当前目录放了一个叫 `ls` 的恶意脚本，你执行 `ls` 时会中招。
>
> 安全的做法是始终用 `./command` 显式执行当前目录的程序。

### 持久化环境变量

不同 Shell 的配置文件各有不同：

| 配置文件 | 加载时机 | 用途 |
|----------|---------|------|
| `~/.bashrc` | 每次打开新终端 | 别名、函数、PATH 等用户配置 |
| `~/.bash_profile` | 登录 Shell 时 | 环境变量、启动程序 |
| `~/.profile` | 登录 Shell 时（通用） | 跨 Shell 的环境变量 |
| `/etc/environment` | 系统级 | 所有用户共享的变量 |

**推荐做法**：在 `~/.bashrc` 中添加配置，因为它对新开的每个终端窗口都生效：

```bash
# 编辑 ~/.bashrc
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc

# 立即生效
source ~/.bashrc
```

---

## 9.4 命令别名（alias）

别名可以让你用简短的名字执行长命令，减少重复输入。

### 查看和创建别名

```bash
# 查看所有已定义的别名
alias

# 创建临时别名（当前 Shell 有效）
alias ll='ls -lh'
alias la='ls -la'
alias grep='grep --color=auto'

# 使用别名
ll
# 等价于 ls -lh
```

### 常用别名推荐

```bash
# 文件操作安全
alias cp='cp -i'      # 覆盖前提示
alias mv='mv -i'      # 覆盖前提示
alias rm='rm -i'      # 逐文件确认
alias rmrf='rm -rf'   # 不常用的危险操作单独命名

# 目录导航
alias ..='cd ..'
alias ...='cd ../..'
alias ll='ls -lh'
alias la='ls -la'
alias lt='ls -ltr'

# 磁盘使用
alias df='df -h'
alias du='du -sh'

# 网络
alias myip='curl -s ifconfig.me'

# 快捷操作
alias reload='source ~/.bashrc'
alias cls='clear'
```

### 别名持久化

临时别名只在当前终端有效。要永久使用，写入 Shell 配置文件：

```bash
cat >> ~/.bashrc << 'EOF'

# === 个人别名 ===
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'
alias ll='ls -lh'
alias la='ls -la'
alias lt='ls -ltr'
alias grep='grep --color=auto'
alias ..='cd ..'
alias df='df -h'
alias reload='source ~/.bashrc'
EOF

source ~/.bashrc
```

### 别名的高级用法

```bash
# 查看别名的实际内容
alias ll
# 输出: alias ll='ls -lh'

# 临时跳过别名执行原命令
\ls                    # 加反斜杠跳过别名
command ls             # 用 command 命令跳过别名
/bin/ls                # 用绝对路径

# 删除别名
unalias ll
unalias -a             # 删除所有别名

# 在别名中使用参数（需要用函数替代别名无法传参的问题）
mkcd() {
    mkdir -p "$1" && cd "$1"
}
```

> [!tip] 别名 vs 函数
> 简单的命令缩写用 `alias`，需要处理参数的逻辑用**Shell 函数**：
> ```bash
> # 别名不能处理位置参数
> alias mkcd='mkdir $1 && cd $1'   # 不工作！
> 
> # 函数可以
> mkcd() { mkdir -p "$1" && cd "$1"; }
> ```

---

## 9.5 命令历史（history）

Shell 会自动记录你输入过的命令，善用历史功能可以极大减少重复输入。

### 基本用法

```bash
# 查看命令历史（默认显示最近 1000 条）
history

# 查看最近 N 条
history 10

# 清空当前会话历史
history -c

# 立即将当前会话写入历史文件
history -w
```

### 历史展开（History Expansion）

```bash
!!              # 执行上一条命令
!$              # 上一条命令的最后一个参数
!^              # 上一条命令的第一个参数
!:0             # 上一条命令的命令名部分
!:1             # 上一条命令的第 2 个参数
!:2-4           # 上一条命令的第 3~5 个参数
!str            # 执行最近一条以 str 开头的命令
!?str?          # 执行最近一条包含 str 的命令
!1000           # 执行历史中编号为 1000 的命令
```

**实战示例**：

```bash
# 忘记用 sudo，重新执行
apt install nginx
# Permission denied...
sudo !!          # 等价于 sudo apt install nginx

# 查看日志后发现需要编辑配置文件
tail -f /var/log/nginx/error.log
vim !$           # 等价于 vim /var/log/nginx/error.log

# 重复执行某个编号的命令
history | grep docker
# 1234  docker ps
!1234            # 等价于 docker ps
```

### 历史搜索（最实用技巧）

```bash
# 从历史中搜索
history | grep "docker compose"
# 或使用 Ctrl+R 交互式反向搜索

# 查看最近执行的 git 命令
history | grep git | tail -10
```

### 历史相关的 Shell 选项

```bash
# 查看历史配置
echo $HISTSIZE       # 内存中保留的命令数（默认 1000）
echo $HISTFILE       # 历史文件路径（默认 ~/.bash_history）
echo $HISTFILESIZE   # 历史文件最大行数

# 优化配置：忽略重复命令和以空格开头的命令
cat >> ~/.bashrc << 'EOF'

# === 历史配置 ===
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoredups:erasedups
export HISTIGNORE="ls:ll:la:pwd:exit:clear:history"
# 以空格开头的命令不记录（用于不想暴露密码的场景）
export HISTCONTROL=ignorespace
EOF
```

> [!tip] 防止在历史中记录敏感命令
> 在命令前加一个空格，该命令就不会被记录到历史中：
> ```bash
>  mysql -u root -pSecretPassword  # 前面有空格，不会进历史
> ```
> 这需要设置 `HISTCONTROL=ignorespace` 或在 `.bashrc` 中添加。

---

## 9.6 终端快捷键

熟练使用快捷键可以让你在编辑命令时手不离键盘主区域，大幅提升效率。

### 行内编辑

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+A` | 跳到行首 |
| `Ctrl+E` | 跳到行尾 |
| `Ctrl+U` | 从光标处删到行首 |
| `Ctrl+K` | 从光标处删到行尾 |
| `Ctrl+W` | 删除光标前的一个单词 |
| `Ctrl+Y` | 粘贴被删除的内容（类似粘贴板） |
| `Ctrl+LEFT` | 向左跳一个单词 |
| `Ctrl+RIGHT` | 向右跳一个单词 |
| `Alt+B` | 向后跳一个单词（同 Ctrl+LEFT） |
| `Alt+F` | 向前跳一个单词（同 Ctrl+RIGHT） |
| `Ctrl+T` | 交换光标前后两个字符（手滑纠正） |

### 历史搜索与作业控制

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+R` | 反向搜索命令历史（最常用！输入关键字模糊搜索） |
| `Ctrl+G` | 退出历史搜索模式 |
| `Ctrl+P` | 上一条命令（同 ↑ 方向键） |
| `Ctrl+N` | 下一条命令（同 ↓ 方向键） |
| `Ctrl+C` | 终止当前正在运行的命令 |
| `Ctrl+Z` | 暂停当前命令，放到后台 |
| `Ctrl+D` | 退出当前 Shell / 发送 EOF |
| `Ctrl+L` | 清屏（同 `clear` 命令） |
| `Ctrl+S` | 暂停终端输出（用 `Ctrl+Q` 恢复） |

### 最值得记住的 5 个快捷键

```bash
# 1. Ctrl+R — 历史搜索（最高频）
# 按下后输入关键字，Shell 会搜索最近匹配的命令
# 继续按 Ctrl+R 跳到更早的匹配

# 2. Ctrl+U — 清空当前输入
# 输入到一半想重来，一键删除整行

# 3. Ctrl+W — 删除前一个单词
# 比按 Backspace 快得多，特别适合在长命令中逐个删除参数

# 4. Ctrl+A / Ctrl+E — 跳到行首/行尾
# 在长命令开头加 sudo 时极实用

# 5. Ctrl+L — 清屏
# 比输入 clear 省 3 个字符，保持手不离主键盘
```

> [!example] Ctrl+R 实战场景
> 假设你昨天执行过一条很长的 Docker 命令，今天又想用：
> ```text
> # 1. 按下 Ctrl+R
> (reverse-i-search)`': 
> 
> # 2. 输入关键字 "docker"
> (reverse-i-search)`docker': docker run -d --name myapp -p 8080:80 nginx:alpine
> 
> # 3. 按 Enter 执行
> # 或按左右方向键修改后再执行
> ```
> 这比 `history | grep docker` 后再复制粘贴快得多。

---

## 9.7 一行命令实战案例汇总

这一节汇集了全书中最实用的管道组合，覆盖日常开发运维的典型场景。

### 日志分析

```bash
# 统计 Nginx 访问日志中各状态码的出现次数
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# 统计每个 IP 的访问次数（前 10）
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# 找出 5 分钟内修改过的日志文件
find /var/log -name "*.log" -mmin -5

# 实时监控错误日志并高亮关键字
tail -f app.log | grep --color=always -E "ERROR|WARN|FATAL"

# 统计某个 URL 的请求耗时分布
grep "/api/users" access.log | awk '{print $NF}' | sort -n | awk '{count++; sum+=$1} END {print "count:", count, "avg:", sum/count}'
```

### 进程与系统

```bash
# 找到 CPU 占用最高的 5 个进程（无需 top）
ps aux --sort=-%cpu | head -6

# 找到内存占用最高的 5 个进程
ps aux --sort=-%mem | head -6

# 杀掉所有匹配名称的进程（慎用）
ps aux | grep "defunct_process" | awk '{print $2}' | xargs kill -9

# 查看当前目录下所有进程（如 Python 进程数）
ps aux | grep python | wc -l

# 每隔 2 秒刷新一次进程列表
watch -n 2 'ps aux --sort=-%cpu | head -10'
```

### 磁盘与文件

```bash
# 找出当前目录下最大的 10 个文件
find . -type f -exec du -h {} + | sort -rh | head -10

# 统计当前目录下各子目录的磁盘占用
du -sh ./*/ | sort -rh

# 找到超过 100MB 的所有文件
find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null

# 统计各种文件类型（按扩展名）的数量
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10

# 清理 7 天前的归档日志
find /var/log -name "*.gz" -mtime +7 -delete
```

### 网络排查

```bash
# 检查本地监听端口及对应进程
ss -tlnp

# 检查某个端口是否可达
nc -zv 10.0.0.1 3306

# 测试 HTTP 响应时间（替换为你的地址）
curl -o /dev/null -s -w "DNS: %{time_namelookup}s\nTCP: %{time_connect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" https://example.com

# 下载整个网站用于离线查看（谨慎使用）
wget -r -l 3 --no-parent https://example.com

# 列出当前所有网络连接数
ss -tun | awk 'NR>1 {print $1}' | sort | uniq -c
```

### Git 与开发

```bash
# 查看所有分支的最后提交时间
git branch -v | sort -k3

# 统计某人的贡献行数
git log --author="zhang" --pretty=tformat: --numstat | awk '{add+=$1; del+=$2} END {print "added:", add, "deleted:", del}'

# 找出最近修改最大的 5 个文件
git diff --stat HEAD~10..HEAD | sort -k3 -rn | head -5

# 批量删除已合并的本地分支
git branch --merged | grep -v "\*" | grep -v "main" | xargs -n 1 git branch -d
```

### 综合实用案例

```bash
# 一键备份配置文件（带日期）
tar -zcf backup-$(date +%Y%m%d).tar.gz /etc/nginx/ /etc/ssl/

# 将当前目录所有 .txt 文件合并为一个文件
cat *.txt > combined.txt

# 将大文件分割成小文件（每 100MB 一个）
split -b 100M largefile.log part-

# 批量重命名：将所有 .jpeg 改为 .jpg
for f in *.jpeg; do mv "$f" "${f%.jpeg}.jpg"; done

# 监控目录，新文件出现时立即处理
inotifywait -m /data/uploads -e create |
    while read dir action file; do
        echo "New file: $file"
        # 在这里添加处理逻辑
    done

# 快速生成密码（16 位随机）
openssl rand -base64 12

# 文件内容替换并备份（对多个文件）
find . -name "*.conf" -exec sed -i.bak 's/old_host/new_host/g' {} \;
```

---

## 9.8 写好一行命令的原则

### 原则 1：从简单开始，逐步叠加

不要试图一次写出完整的一行命令。先跑通小步骤：

```bash
# 第 1 步：先看原始数据
ps aux

# 第 2 步：过滤目标进程
ps aux | grep nginx

# 第 3 步：提取 PID
ps aux | grep nginx | awk '{print $2}'

# 第 4 步：执行操作
ps aux | grep nginx | awk '{print $2}' | xargs kill
```

每一步先确认输出符合预期，再添加下一个管道。

### 原则 2：用 `echo` 验证危险操作

对于可能造成破坏的命令（如 `rm`、`kill`、`mv`），先用 `echo` 看看实际要执行什么：

```bash
# 危险
find . -name "*.log" -mtime +30 -delete

# 先验证
find . -name "*.log" -mtime +30 -exec echo rm -f {} \;

# 确认无误后再去掉 echo
find . -name "*.log" -mtime +30 -exec rm -f {} \;
```

### 原则 3：善用引号防止空格和通配符展开

```bash
# 文件名含空格时的问题
rm some file.txt      # 等价于 rm some file.txt（删了两个文件）

# 正确：用引号包裹
rm "some file.txt"

# find 中使用变量时防止展开
pattern="*.log"
find . -name "$pattern" -type f   # "$pattern" 防止被 Shell 展开
```

### 原则 4：复杂操作写成脚本，不追求单行

如果一行命令超过 80 个字符或包含超过 4 个管道，考虑写成 Shell 函数或脚本：

```bash
# 太复杂不适合一行
analyze_log() {
    local logfile=$1
    echo "=== 404 统计 ==="
    grep " 404 " "$logfile" | awk '{print $7}' | sort | uniq -c | sort -rn | head -10
    echo "=== 耗时最慢的请求 ==="
    awk '{print $NF, $7}' "$logfile" | sort -rn | head -10
}
```

> [!tip] 一行命令的适用场景
> **适合一行**：日志快速排查、系统状态检查、文件批量操作、进程管理
> **不适合一行**：复杂的多步骤数据处理、有判断逻辑和循环的任务、需要复用的功能
> 判断标准：如果写完 5 分钟后你自己都看不懂了，就该写成脚本。

---

## 本章总结

- **管道 `|`** 是命令组合的核心机制，将命令串联成处理流水线；需注意管道会在子 Shell 中执行右侧命令
- **重定向** 控制数据流向：`>` 覆盖写入，`>>` 追加写入，`2>` 重定向错误，`&>` 合并输出；**`2>&1` 必须放在 `>` 之后**
- **环境变量** 是系统和 Shell 共享的配置键值对；修改 `PATH` 需谨慎，不要将当前目录放在 `PATH` 前面
- **别名** 用于命令缩写，`alias` 查看，写入 `~/.bashrc` 持久化；需要参数时改用 Shell 函数
- **命令历史** 用 `history` 查看，`!!` 执行上一条，`!$` 取上个参数；配置 `HISTCONTROL=ignorespace` 保护敏感命令
- **快捷键** 中 Ctrl+R（历史搜索）效率最高，Ctrl+U/Ctrl+W 是编辑利器，Ctrl+A/Ctrl+E 快速跳到行首尾
- **一行命令** 应从简到繁逐步搭建，用 `echo` 验证危险操作，超过 4 个管道考虑写成脚本

## 下一步

至此，《Linux 常用命令实战手册》的所有章节已全部完成。你可以回到目录页，将全书作为日常参考手册使用。遇到具体问题时，前三章（文件操作、文本查看、三剑客）是最常用的部分，第五到七章可在排查问题时按需查阅。命令行是一把越用越锋利的工具，祝你在日常使用中不断精进！
