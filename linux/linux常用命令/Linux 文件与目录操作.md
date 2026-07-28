---
title: "Linux 文件与目录操作"
created: 2026-07-29
updated: 2026-07-29
tags: [linux, 文件操作, 命令行]
status: completed
source_project: linux-commands
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
