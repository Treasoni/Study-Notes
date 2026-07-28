---
title: "Linux 文件内容查看与搜索"
created: 2026-07-29
updated: 2026-07-29
tags: [linux, grep, 文本搜索]
status: completed
source_project: linux-commands
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
