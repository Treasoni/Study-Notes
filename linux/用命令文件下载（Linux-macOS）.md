---
title: 用命令文件下载（Linux/macOS）
tags:
  - linux
  - 下载
  - curl
  - wget
  - aria2
  - 命令行
  - bash
created: 2026-08-31
updated: 2026-08-31
status: 已完成
source_project: command-file-download
---

# 用命令文件下载（Linux/macOS）

> [!summary] 笔记简介
> 一份面向 Linux/macOS 终端的命令行下载实战笔记。从 curl / wget / aria2 的选型与基础用法出发，依次覆盖断点续传、并发与重试、校验与安全、批量脚本与错误处理，最后汇聚为一个可直接复用的完整下载脚本。建议按章节顺序边读边在终端验证，动手效果最佳。

## 目录

1. [第一章：下载工具全景与选型（curl / wget / aria2）](#第一章下载工具全景与选型curl--wget--aria2)
2. [第二章：curl 基础用法](#第二章curl-基础用法)
3. [第三章：wget 与 aria2 基础用法](#第三章wget-与-aria2-基础用法)
4. [第四章：断点续传](#第四章断点续传)
5. [第五章：并发与重试](#第五章并发与重试)
6. [第六章：校验与安全](#第六章校验与安全)
7. [第七章：批量下载脚本基础](#第七章批量下载脚本基础)
8. [第八章：错误处理与脚本健壮性](#第八章错误处理与脚本健壮性)
9. [第九章：实战案例：一个完整的批量下载脚本](#第九章实战案例一个完整的批量下载脚本)
10. [结语与下一步](#结语与下一步)

---

## 第一章：下载工具全景与选型（curl / wget / aria2）

> [!note] 本章导读
> 目标：建立 curl / wget / aria2 三者的选型直觉，看懂 `-O` / `-o` 的语义差异，并完成本机环境检查。学完后，你能在任何下载场景里第一时间选对工具。

在 Linux/macOS 的终端里下载文件，绕不开 curl、wget、aria2 这三兄弟。刚入门的人很容易问："它们不都是下载工具吗？随便用哪个不就行了？" 实际上它们定位不同，参数语义甚至互相"打架"——同一对 `-O` / `-o` 字母，在 curl 和 wget 里含义正好相反。本章先把三者摊开对比，帮你建立选型直觉，并确认本机环境就绪。

### 1.1 三种工具的定位与适用场景

| 工具 | 一句话定位 | 强项 | 典型场景 |
|------|-----------|------|----------|
| curl | 网络交互瑞士军刀，支持 HTTP/HTTPS/FTP/SFTP 等 20+ 协议 | 灵活、脚本友好、可精细控制请求 | 单文件下载、API 调用、上传、调试 HTTP |
| wget | 命令行下载器 + 递归镜像工具 | 递归抓取、整站镜像 | 镜像整站、按目录批量抓取 |
| aria2 | 多协议高速下载引擎 | 单文件分片并发、多源加速 | 大文件、慢速/不稳定网络、多镜像 |

三者都能完成"把一个 URL 下载到本地"这件基础事，但侧重点完全不同。[^c1-1][^c1-2][^c1-3]

> [!tip] 大白话
> 把 curl 想成**瑞士军刀**——什么都能干、随身带着用；把 wget 想成**整站搬家公司**——能把一个网站整窝端走；把 aria2 想成**多头挖掘机**——一个文件能开好几个口同时挖。所以：零散下载找 curl，搬整站找 wget，拖大文件找 aria2。

### 1.2 参数体系速览：`-O` / `-o` 的语义差异

这是新手最容易踩的坑：**同一个 `-O`，在 curl 和 wget 里意思完全相反**。

- **curl**：`-O`（大写）保存为远程文件名——取 URL 中的文件名部分、去掉路径，本地已有同名文件则覆盖；`-o`（小写）保存为你指定的本地文件名。[^c1-4]
- **wget**：`-O`（大写）把下载内容**拼接写入你指定的单个文件**；目录控制靠 `-P`（目录前缀）、`-nH`（禁止自动建主机名目录）。[^c1-5]
- **aria2**：目录用 `-d`（存储目录）、文件名用 `-o`（相对 `-d` 目录解析）。[^c1-6]

把常见的意图对照起来：

| 你的意图 | curl | wget | aria2 |
|----------|------|------|-------|
| 指定本地文件名 | `-o 名字` | `-O 名字` | `-o 名字` |
| 指定存储目录 | 用 `-o 目录/名字` 间接实现 | `-P 目录` | `-d 目录` |
| 按远程文件名保存 | `-O` | 默认行为 | 默认行为 |

> [!warning] 易错点
> 想"存成我自己起的名字"时：curl 用小写 `-o`，wget 用大写 `-O`。写反了不会报错，但行为完全不是你以为的那样——curl 的 `-O` 会忽略你给的名字、按远程文件名存；wget 的 `-O` 会把多次下载的内容拼进同一个文件。

> [!tip] 大白话
> 把 `-O` 想成**按原包装收快递**——名字由寄件方（URL）定；`-o` 想成**自己指定收货方式**——叫它什么、放哪儿，都由你定。curl 里大写 O = 存原名、小写 o = 自己起名；wget 恰好反过来。记住这一个反差，就能避开一半的下载坑。

### 1.3 选型建议（何时用哪个）

> [!note] 经验结论
> 以下选型结论由三份官方素材综合推断而来，供实战参考：**curl 灵活（协议多、脚本友好）、wget 递归镜像强、aria2 并发分片最强**。[^c1-7]

- **日常单文件下载 / 脚本里调 HTTP API**：默认 **curl**。它对重定向、失败退出码、代理的控制最细，是脚本编写的首选。
- **把整站镜像下来离线浏览**：选 **wget**。它的递归抓取与目录控制（`-P` / `-nH`）是 curl 不擅长的领域。
- **大文件 / 慢速不稳定网络 / 多镜像加速**：选 **aria2**。它能单文件多连接分片下载，断点续传天然友好，后文第五章会展开。

一个实用的经验法则：**拿不准时先上 curl**，遇到"要搬整站"再切 wget，遇到"文件太大下不动"再上 aria2。本系列以 curl 为主线，wget 和 aria2 作为对照与补充。

### 1.4 环境准备：检查安装

打开终端，先确认三个工具是否就绪：

```bash
# 检查三个命令是否在 PATH 中：找到则打印可执行文件路径，找不到则无输出
which curl wget aria2c
```

```text
/usr/bin/curl
/usr/bin/wget
# ↑ 只打印了两行，说明 aria2c 未安装
```

`which` 会在 PATH 里逐个查找命令，命中就打印绝对路径；查不到时无输出、命令以非零状态退出。所以看输出有几行，就知道缺了谁。

> [!tip] 大白话
> 把 `which` 想成**问路**——"curl 这哥们住哪儿？"它一查 PATH 就告诉你绝对路径；查不到的人，说明没住在这条街上，得先把它请进来（安装）。

若某个工具未安装，需要用系统的包管理器安装。**具体预装情况与安装命令因发行版/平台而异，本章素材未收录，标注「待补充」**；常见做法是用系统包管理器（macOS 常用 Homebrew、Debian/Ubuntu 常用 apt），安装前先搜索确认本机可用的包名。装完重跑一次 `which` 验证。

### 本章小结

- 三工具定位不同：curl 灵活、脚本友好；wget 递归镜像强；aria2 并发分片最强（经验结论）。
- 最易踩坑：curl 用 `-o` 指定文件名，wget 用 `-O` 指定文件名，两者语义相反。
- 选型法则：拿不准先上 curl，搬整站切 wget，拖大文件上 aria2。
- 用 `which curl wget aria2c` 检查环境，缺哪个装哪个。

下一章进入 curl 基础用法：`-O` / `-o`、`-L` 跟随重定向、`-f` 让 HTTP 错误转成非零退出码，最终拼出 `curl -fL -O` 最小安全模板。

---

[^c1-1]: curl 官方教程：<https://curl.se/docs/tutorial.html>
[^c1-2]: GNU Wget 官方手册：<https://www.gnu.org/software/wget/manual/>
[^c1-3]: aria2c 官方手册：<https://aria2.github.io/manual/en/html/aria2c.html>
[^c1-4]: curl 官方教程「Download to a File」及 man page 的 `#--remote-name` / `#--output`。
[^c1-5]: GNU Wget 手册 §2.5 `-O`、§2.6 `-P` / `-nH`。
[^c1-6]: aria2c 手册 Basic Options 的 `-d` / `-o`。
[^c1-7]: 综合 curl / wget / aria2 官方手册的选型推断（素材标注 inference）。

---

## 第二章：curl 基础用法

本章掌握 curl 下载最核心的四个参数：`-O`、`-o`、`-L`、`-f`。

### 2.1 单文件下载：-O 与 -o

下载要先指定输出位置。

**`-O`** 取 URL 最后一段路径作本地文件名 [curl 官方教程](https://curl.se/docs/tutorial.html)：

```bash
curl -O https://example.com/downloads/archive.tar.gz
ls -l archive.tar.gz   # 当前目录出现 archive.tar.gz
```

文件名不做 URL 解码（`file%20name.zip` 落盘即字面量），同名直接覆盖 [curl 手册 --remote-name](https://curl.se/docs/manpage.html)。

**`-o`** 保存为你指定的文件名，适合重命名或远程名无意义的场景 [curl 手册 --output](https://curl.se/docs/manpage.html)：

```bash
curl -o my-backup.tar.gz https://example.com/downloads/archive.tar.gz
ls -l my-backup.tar.gz   # 当前目录出现 my-backup.tar.gz
```

> [!tip] 大白话：`-O` 像「收快递不换标签」，`-o` 是「自己贴新标签」。前者名字由远程决定，后者完全可控。

### 2.2 跟随重定向：-L

很多下载链接返回 30x，真正文件在 `location` 指向的地址。不加 `-L` 会下载到空文件或错误页；加 `-L`（`--location`）自动追到最终地址 [curl 手册 --location](https://curl.se/docs/manpage.html)：

```bash
curl -L -O https://example.com/latest/download   # 跟随重定向，落盘为最终文件名
```

> [!tip] 大白话：重定向像「店搬家」，老地址贴着新地址。`-L` 是愿意顺着新地址找的买家。

三个边界：默认最多跟随 **50 次**；**跨主机不传凭据和 Cookie**；POST 在 301/302/303 转成 GET。

### 2.3 错误转退出码：-f / -fL

**curl 默认不把 HTTP 状态码当失败**：404 时退出码仍是 0。加 `-f`（`--fail`）后，HTTP 400 及以上转为**退出码 22** [curl 手册 --fail](https://curl.se/docs/manpage.html)。

> [!warning] 404 假成功：不带 `-f` 时 `curl -O URL; echo $?` 打印 0。批量脚本里 `-f` 是第一道防线。

> [!tip] 大白话：退出码像「送达确认」。默认 curl 只要「送完」就算成功，哪怕签收的是「查无此人」回执；`-f` 让它报错。

### 2.4 最小可用模板

```bash
curl -fL -O https://example.com/latest/download   # 跟随重定向 + 错误转退出码 + 保存为远程名
echo $?   # 成功 0；失败（如 404）22，且不会把错误页存成文件
```

分工：`-f` 转 22，`-L` 跟随 30x，`-O` 存为远程名。续传、重试在此基础上叠加。

### 本章小结

- `-O` 存为远程文件名（不做 URL 解码）；`-o` 指定本地文件名；同名都会覆盖。
- `-L` 跟随 30x，默认最多 50 次；跨主机不传凭据 / Cookie。
- 默认 404 也是「成功」，`-f` 才转成退出码 22。
- 最小安全模板 `curl -fL -O URL`。

下一章对比 wget 与 aria2——注意 wget 的 `-O` 是拼接单文件，与 curl 不同。

---

## 第三章：wget 与 aria2 基础用法

第二章我们用 curl 完成了单文件下载，掌握了 `-O` / `-o` / `-L` / `-fL` 的最小模板。但下载场景不止 curl 一个解：wget 是"镜像与递归"的老牌选手，aria2 是"并发分片"的速度之王。本章把这两个工具的基础下载参数讲透，并在结尾给出三工具下载同一文件的对照，让你拿到 URL 时能随手选对工具、写对参数。

### 3.1 wget 基础：-O / -P / -nH

wget 的参数体系与 curl 恰好相反：wget 的 `-O`（大写）是 `--output-document`，**把所有下载内容拼接写入一个文件**，行为类似 shell 重定向，而不是"改名另存"[^c3-1]：

```bash
# wget -O：把内容写入指定文件（类似重定向 >）
wget -O mylinux.iso http://example.com/linux.iso
# 结果：当前目录下生成 mylinux.iso
```

> [!warning] wget -O 的两个坑
> 1. **立即截断**：`wget -O file URL` 等价于 `wget -O - URL > file`，命令一运行就把已存在的 `file` 清空再写入新内容。若下载失败，旧文件也已经丢了。
> 2. **与 `-N` 不兼容**：`-N` 按时间戳跳过未更新的文件，而 `-O` 每次都会新建文件，两者语义冲突，同时使用会给出警告。

> [!tip] 大白话
> 把 `wget -O` 想成 shell 的 `>` 重定向：一执行就先"清空重写"，不是"改名另存"。所以拿它做重命名可以，想保留旧文件或配 `-N` 做增量下载就不行。

与 curl 用 `-o` 指定完整路径不同，wget 更常用 `-P`（`--directory-prefix`）指定**目录前缀**，文件名仍取远程文件名；递归下载时默认还会套一层主机名目录，用 `-nH` 去掉[^c3-1][^c3-2]：

```bash
# wget -P：下载到指定目录，文件名保持远程名
wget -P downloads http://example.com/linux.iso
# 结果：downloads/linux.iso（目录不存在会自动创建）

# 递归镜像：-nH 去掉默认的主机名目录层
wget -r -nH -P mirror http://example.com/docs/
# 结果：mirror/docs/index.html，而不是 mirror/example.com/docs/index.html
```

`-P` 是"检索树的根"，默认值是当前目录 `.`。递归下载时 wget 默认会把文件保存在 `主机名/路径/...` 结构里，`-nH`（`--no-host-directories`）禁掉这一层，让目录结构更干净。

### 3.2 aria2 基础：-d / -o

aria2 的命名更接近直觉：`-d` 指定**存储目录**，`-o` 指定**文件名**（注意是小写，与 wget 的 `-O` 语义不同）[^c3-3]：

```bash
# aria2c -d + -o：存储目录 + 自定义文件名
aria2c -d downloads -o mylinux.iso http://example.com/linux.iso
# -o 的文件名始终相对 -d 目录解析
# 结果：downloads/mylinux.iso
```

> [!tip] 大白话
> 把 `-d` 想成"收货地址"，`-o` 想成"包裹上贴的名字"。默认 `aria2c URL` 会用 URL 里最后的文件名当包裹名；不想用原名，就用 `-o` 重新贴一张。

aria2 的 `-o` 有一个容易踩的限定：**只对命令行直接给的 URI 生效**。如果走 `-i` 输入文件、Metalink 或 BitTorrent，`-o` 会被忽略——批量下载时要改名，得在输入文件里逐条写，不能靠命令行 `-o`。

### 3.3 三工具基础下载对比小结

同一目标 URL，三工具各写一遍：

```bash
# 目标：把 http://example.com/linux.iso 下载到本地 downloads/ 目录

curl -o downloads/linux.iso http://example.com/linux.iso   # -o 写完整路径
wget -P downloads http://example.com/linux.iso              # -P 指定目录前缀
aria2c -d downloads http://example.com/linux.iso            # -d 指定存储目录
```

| 需求 | curl | wget | aria2 |
| --- | --- | --- | --- |
| 指定文件名 | `-o 路径/文件` | `-O 文件`（拼接+截断） | `-o 文件`（相对 `-d`） |
| 指定目录 | 用 `-o` 带上目录 | `-P 目录` | `-d 目录` |
| 去掉主机名目录 | 不涉及 | `-nH` | 不涉及 |
| 递归/镜像 | 弱 | 最强（`-r`） | 无 |

一句话选型经验（基于前两章的基础能力，进阶能力后续展开）：**临时下载单个文件用 curl；要镜像整站目录结构用 wget；要快（多连接分片）或批量并发用 aria2**。

### 本章小结

- wget 的 `-O` 把内容拼接写入单文件，运行瞬间截断目标，且与 `-N` 不兼容。
- wget 的 `-P` 设置目录前缀（检索树根），`-nH` 去掉默认的主机名目录层，二者常配合递归下载使用。
- aria2 的 `-d` 是存储目录，`-o` 是文件名；`-o` 相对 `-d` 解析，且只对命令行 URI 生效。
- 三工具参数命名不同，但"指定文件名 / 指定目录"的需求都能满足；选型看场景：灵活 curl、镜像 wget、速度 aria2。

下一章进入可靠性话题：网络中断后怎么续传。三工具的续传行为和限制各不相同，正是实战中容易踩坑的地方。

---

[^c3-1]: GNU Wget Manual，`-O` / `--output-document` 一节，https://www.gnu.org/software/wget/manual/
[^c3-2]: GNU Wget Manual，`-P` / `--directory-prefix` 与 `-nH` / `--no-host-directories` 一节，https://www.gnu.org/software/wget/manual/
[^c3-3]: aria2c Manual，Basic Options 的 `-d` / `--dir` 与 `-o` / `--out` 一节，https://aria2.github.io/manual/en/html/aria2c.html

---

## 第四章：断点续传

下载大文件最怕什么？下到一半断网、误触 Ctrl+C、笔记本合盖，一切从头再来。断点续传让下载工具从已完成的字节数接着下，而不是重来一遍。本章解决"如何让 curl / wget / aria2 在被中断后接着干"，以及各自有哪些坑。

### 4.1 续传的前提：HTTP Range 与服务器支持

断点续传的本质，是 HTTP/1.1 的**字节区间（byte-ranges）**机制：客户端对服务器说"我已经有前 N 个字节，把第 N 字节之后的内容给我"，服务器同意后就只返回剩余部分，下载工具再把新数据接到本地文件末尾 [curl tutorial: Ranges](https://curl.se/docs/tutorial.html)。

所以续传有一个**硬前提：服务器必须支持 Range**。你可以用 `curl -r 0-99` 手动请求"只要前 100 字节"来试探；如果服务器不支持 Range，curl 会忽略这个请求、把整个文档都发给你 [curl man page `-r, --range`](https://curl.se/docs/manpage.html#-r)，或直接报 range 错误（退出码 33）[curl man page: Exit codes](https://curl.se/docs/manpage.html#exitcode)。

> [!tip] 大白话
> 把下载想成逐页抄写一本长书。抄到第 800 页时笔没墨了，从第 1 页重抄太亏。断点续传就是告诉服务器"前 800 页我已经有了，从第 801 页接着给我"——而服务器认不认这个"页码"，取决于它是否支持 Range。服务器不认，续传就无从谈起。

### 4.2 curl：`-C -` 自动计算偏移

curl 用 `-C, --continue-at` 续传。关键是 `-C -` 这种写法：连字符让 curl **自动**根据本地输出文件的大小，推断出该从哪个字节继续，无需你手动报偏移量 [curl man page `-C, --continue-at`](https://curl.se/docs/manpage.html#-C)。它和 `--range` 互斥，同一传输只能二选一。

```bash
# 第一次下载：中途 Ctrl+C 或断网中断，本地留下不完整的 bigfile.iso
curl -fL -o bigfile.iso https://example.com/dist/bigfile.iso

# 第二次：加上 -C -，curl 读本地文件大小自动定位偏移，只下载剩余部分
curl -fL -C - -o bigfile.iso https://example.com/dist/bigfile.iso
# 若服务器支持 Range，会返回"部分内容"响应，传输量远小于整个文件
```

> [!tip] 大白话
> 把 `-C -` 想成书签。你不需要记得"上次抄到第几页"，curl 自己看一眼本地文件已经有多长，就自动算出该从哪个字节接着下。所以命令里写的是 `-`（让工具自己判断），而不是一个具体数字。

若服务器不支持 Range，续传请求会失败并返回非零退出码（range 错误 33、续传失败 36）[curl man page: Exit codes](https://curl.se/docs/manpage.html#exitcode)。脚本里务必配合 `-f`（第二章的最小模板）让 HTTP 错误转成非零退出码。

### 4.3 wget：`-c` 的限制

wget 用 `-c, --continue` 续传，但限制比 curl 多 [GNU Wget Manual: `--continue`](https://www.gnu.org/software/wget/manual/)。先记住一个反直觉的点：**本次调用内连接中断后的自动重试是 wget 的默认行为，不需要 `-c`**；`-c` 只负责续传"上一次 wget（或其他顺序下载程序）留下的、本地文件还在"的那次下载。

```bash
# 续传 wget 之前留下的部分下载文件（会从本地文件长度对应的偏移继续）
wget -c https://example.com/dist/bigfile.iso
# 服务器支持 Range 时，wget 只取剩余字节接到本地文件末尾
```

> [!warning] wget `-c` 的三个坑
> - **仅续传 wget 自己的文件**：它假定本地文件是远程文件的前缀，只认自家（或顺序下载程序）留下的半成品。
> - **服务器不支持时直接覆盖**：若服务器不支持续传，wget 会从零重启下载，并把现有文件**完全覆盖**。
> - **远程文件被修改会损坏**：如果服务器上的文件变大是因为被改动而非追加新内容，wget 无法验证本地文件是不是远程文件的有效前缀，会把新旧内容拼成一份损坏的文件。

> [!tip] 大白话
> 把 wget `-c` 想成只认自家封条的仓库。它放心接着自己贴过封条的半成品干；服务器不配合时，它会把旧货直接撕掉从头重抄；更危险的是，如果远程文件被改动过（不是单纯追加），它没有能力发现，会把新旧内容粘在一起给你一份坏文件。

### 4.4 aria2：中断后自动续传

aria2 是三工具里续传最省心的：**只要是你用 aria2 发起的下载，中断后在同一目录重跑同一条命令就自动续传**，不需要任何额外参数——它用控制文件记录下载进度 [aria2c Manual: Resuming Download](https://aria2.github.io/manual/en/html/aria2c.html#resuming-download)。

```bash
# 第一次下载：中途按 Ctrl+C 停止
aria2c -d /tmp/downloads -o bigfile.iso https://example.com/dist/bigfile.iso

# 同一目录重跑同一条命令，aria2 读取控制文件自动续传
aria2c -d /tmp/downloads -o bigfile.iso https://example.com/dist/bigfile.iso
# 输出会显示已有进度并继续下载，而不是从零开始
```

只有当你需要续传**浏览器或 wget 等顺序下载程序留下的文件**时，才用 `-c, --continue` 选项，它仅适用于 HTTP(S)/FTP 下载 [aria2c Manual: `--continue`](https://aria2.github.io/manual/en/html/aria2c.html#cmdoption-c)。

> [!tip] 大白话
> 把 aria2 想成自带施工记录的装修队。每次下载它都会在旁边记一份台账，中断后你在同一目录重跑同一条命令，它照台账接着干，不用你额外吩咐。只有接别人留下的半成品，才需要专门交代一句（`-c`）。

### 4.5 三工具续传行为对比

| 工具 | 续传触发方式 | 能续传谁留下的文件 | 服务器要求 | 服务器不支持 Range 时 |
|------|-------------|-------------------|-----------|----------------------|
| curl | `-C -` 手动指定，按本地文件自动算偏移 | 任意本地部分文件 | 支持 Range | 续传失败，返回非零退出码（33/36） |
| wget | `-c` 手动指定 | 仅此前 wget（或顺序下载程序）留下的文件 | FTP 或支持 Range 的 HTTP | 从头下载并**覆盖**现有文件 |
| aria2 | 同目录重跑自动续传；`-c` 续传他人文件 | 自身下载默认；`-c` 续传浏览器/wget 文件 | HTTP(S)/FTP | 续传不可用时从头下载 |

### 本章小结

- 断点续传的本质是 HTTP Range：从已下载的字节数处接着取剩余部分，前提是服务器支持 Range。
- curl `-C -` 按本地文件自动计算偏移，与 `--range` 互斥，续传失败返回非零退出码。
- wget `-c` 只续传 wget 自己留下的文件；服务器不支持时覆盖现有文件，远程文件被修改时可能拼出损坏文件。
- aria2 自身发起的下载中断后，同目录重跑即自动续传；`-c` 仅用于续传浏览器/wget 留下的文件。

下一章进入可靠性进阶的第二块拼图：并发与重试——用 curl 并行下载、aria2 分片加速，以及失败时如何自动重试。

---

## 第五章：并发与重试

下载最常遇到的两个问题：一个是**慢**——单个文件排队下，多文件更是望穿秋水；另一个是**脆**——网络一抖就失败，得手动重来。上一章的断点续传解决了「断了从头下」的浪费，本章再加两味药：**并发**让下载变快，**重试**让失败自动痊愈。学完你会掌握 curl / aria2 的两种并发玩法，以及三套工具各自的失败重试与退避策略。

### 5.1 curl 并行下载：`-Z` / `--parallel` 与 globbing

curl 不擅长把一个文件拆开并行，但很擅长**一次并行下载多个 URL**。加上 `-Z`（长写 `--parallel`）后，多个 URL 会同时开始，而不是排队一个个来。默认最多 **50 个并发**，用 `--parallel-max` 可调 [curl man page](https://curl.se/docs/manpage.html)。

```bash
# 并行下载三个文件（-Z 让它们同时开始）
curl -Z -O https://example.com/a.zip -O https://example.com/b.zip -O https://example.com/c.zip
```

`-O` 写在各 URL 前面，表示各自保存为远程文件名。不想重复写时，也可以用 `--remote-name-all` 让所有 URL 都按远程名保存。

> [!tip] 大白话
> 把 `-Z` 想成「同时雇几个搬运工，各搬各的包裹」，比一个人一件件搬快得多。所以一次要下多个文件时，`-Z` 能明显提速。

只写 URL 列表还不过瘾，curl 自带 **globbing**（通配展开）：`{a,b}` 是列表、`[1-100]` 是数字范围，一条命令生成一大堆 URL。注意 URL 要**加引号**，否则 shell 可能抢在 curl 前面把花括号展开掉 [curl man page](https://curl.se/docs/manpage.html)。

```bash
# {a,b,c} 生成 3 个名字，[1-100] 生成 100 个编号，可层层叠加
curl -Z -O "https://example.com/file[1-100].txt"
# 多组叠加：1996-1999 年 × 1-4 卷 × a/b/c 三部分 = 48 个 URL
curl -Z -O "https://example.com/archive[1996-1999]/vol[1-4]/part{a,b,c}.html"
```

支持 `[001-100]` 前导补零和 `[a-z]` 字母范围；不支持嵌套序列，但可以像上面那样**并排多组**。若 URL 里的 `{}`/`[]` 是字面含义而不是要展开，用 `-g` / `--globoff` 关闭 globbing。

> [!tip] 大白话
> globbing 想成「用一张清单批量下单」：`{a,b,c}` 是列出候选名，`[1-100]` 是填数字区间。加引号是告诉 curl 自己解析这份清单，别让 shell 抢着先展开。

### 5.2 aria2 并发模型：`-x` / `-s` / `-j`

aria2 的并发分两层：**单文件内分片**和**多文件条目并行**，三个参数各管一摊 [aria2 manual](https://aria2.github.io/manual/en/html/aria2c.html)。

- `-x` / `--max-connection-per-server=N`：对**同一台服务器**最多开 N 条连接，是上限闸门，防止分片太多把服务器压垮。
- `-s` / `--split=N`：把**同一个文件**切成 N 段，用 N 条连接同时下，最后拼回。若 URL 少于 N 个，同一个 URL 会被复用凑够 N 条连接。
- `-j` / `--max-concurrent-downloads=N`：**队列里同时下载几个文件**（条目数）。它和分片是两码事：`-j 2` 是同时下两个文件，`-s 4` 是每个文件内部拆 4 段。
- `-k` / `--min-split-size=SIZE`：小于 `2×SIZE` 的文件不拆，**默认 20M**。例如 20MiB 文件、`SIZE=10M` 时可拆 2 段；`SIZE=15M` 时 `2×15M > 20MiB`，就不拆，只开 1 条连接。这个默认值避免小文件被过度拆分的开销。

```bash
# 单文件拆 4 段、每台服务器最多 4 条连接、最多同时下 2 个文件
aria2c -x 4 -s 4 -j 2 -d /tmp "https://example.com/big.iso" "https://example.com/other.iso"
```

预期结果：终端同时出现两条下载进度，各自内部又有 4 条连接在抢速。

> [!tip] 大白话
> `-j` 想成「排几条队、各买各的票」；`-s` 想成「一张大图撕成几段，几个人各拿一段同时下，最后拼回一张图」；`-x` 是「一家店最多派几个人进去」。所以 `-j` 管几条队，`-s`/`-x` 管一个文件拆几段。

> [!warning] 待补充
> 素材中 aria2 的 `-x`、`-s`、`-j`、`--max-tries`、`--retry-wait` 默认值缺失。请本机执行 `aria2c --help` 验证后回填，勿臆造。

### 5.3 curl 重试参数与指数退避

`--retry N` 让 curl 遇到**瞬时错误**时自动重试 N 次，**默认 0（不重试）**。瞬时错误包括：超时、FTP 4xx，以及 HTTP 408/429/500/502/503/504/522/524 [curl man page](https://curl.se/docs/manpage.html)。

重试间隔采用**指数退避**：第一次重试前等 1 秒，之后每次翻倍（2s、4s、8s……），直到 **10 分钟**上限，之后固定等 10 分钟。

```bash
# 失败重试 5 次；把指数退避改成固定 3 秒间隔；整个重试过程不超过 60 秒
curl -fL -C - --retry 5 --retry-delay 3 --retry-max-time 60 -O "https://example.com/data.zip"
```

- `--retry-delay N`：把指数退避改成**固定间隔** N 秒（设 0 恢复默认退避）。
- `--retry-max-time N`：给整个重试过程设总时长上限（含等待时间），到点不再重试。
- 404 **默认不重试**——文件不存在，重试多少次也不会变出来。若非要连 4xx/5xx 都重试，需 `--fail` 配 `--retry-all-errors`，但官方明确不建议默认启用（这是「大锤」，可能收到重复数据）[curl man page](https://curl.se/docs/manpage.html)。

> [!tip] 大白话
> 指数退避想成「给客服打电话」：第一次没人接，等 1 秒再打；还没人接，就等 2 秒、4 秒、8 秒……越来越久。这是给服务器留喘气时间，免得它还没缓过来就被你的重试轰炸。

### 5.4 wget 重试与超时

wget 默认就重试 **20 次**，和 curl 的「默认不重试」正好相反。但有两类致命错误默认**不重试**：**connection refused（连接被拒）** 和 404（not found）——连接被拒通常说明服务器根本没在运行，重试也白搭 [GNU Wget Manual](https://www.gnu.org/software/wget/manual/)。

```bash
# 最多重试 5 次；重试间线性退避到 5 秒；网络超时统一设 30 秒；配合 -c 断点续传
wget -t 5 --waitretry=5 --timeout=30 -c "https://example.com/data.zip"
```

- `-t` / `--tries=N`：重试次数；`0` 或 `inf` 表示无限重试。
- `--waitretry=N`：只在失败重试间等待，采用**线性退避**——第一次失败等 1 秒，第二次等 2 秒，逐步加到 N 秒封顶（默认 10 秒）。
- `--timeout=N`：一条命令同时设置 DNS、连接、读取三类超时；默认只启用 900 秒的读超时。
- `--retry-connrefused`：若偏要在连接被拒时也重试（比如镜像服务器时好时坏），加上它。

> [!tip] 大白话
> connection refused 想成「对方根本没开门」，404 想成「你要的货号不存在」——这两种情况重试都是白费，所以 wget 默认不重试。`--retry-connrefused` 是你坚持「多敲几次门」才打开的开关。

### 5.5 aria2 重试：`--max-tries` / `--retry-wait`

aria2 用 `--max-tries=N` 设重试次数，用 `--retry-wait=SEC` 设重试间隔。有个贴心细节：**当 `--retry-wait` 大于 0 时，服务器返回 503 也会触发重试** [aria2 manual](https://aria2.github.io/manual/en/html/aria2c.html)。

```bash
# 最多重试 5 次，每次间隔 5 秒
aria2c --max-tries=5 --retry-wait=5 -d /tmp "https://example.com/data.zip"
```

把本节的重试和 5.2 的并发合体，一条命令就能做到「分片 + 并行 + 重试」——这也是 aria2 相比另两工具的核心卖点：

```bash
aria2c -x 4 -s 4 -j 2 --max-tries=5 --retry-wait=5 -d /tmp "https://example.com/data.zip"
```

---

### 本章小结

- curl 靠 `-Z` 并行下载多个 URL，默认最多 50 个并发；globbing 用 `{a,b}` / `[1-100]` 一条命令生成大量 URL（记得加引号）。
- aria2 并发分两层：`-j` 管同时下几个文件，`-s`/`-x` 管一个文件内拆几段、每台服务器最多几条连接；`-k` 默认 20M 决定小文件不拆。
- curl `--retry` 默认 0 不重试，指数退避 1s→10min，404 不重试；`--retry-delay` 改固定间隔，`--retry-max-time` 限总时长。
- wget 默认重试 20 次，但 connection refused 和 404 不重试；`--waitretry` 用线性退避，`--timeout` 统一管三类超时。
- aria2 `--max-tries` 加重试次数，`--retry-wait>0` 时 503 也重试；`-x`/`-s`/`-j`/`--max-tries`/`--retry-wait` 默认值待本机 `aria2c --help` 验证。

下一章进入**校验与安全**：下载完成的文件怎么确认没被篡改或传坏（`sha256sum`、aria2 `--checksum`），以及代理、TLS 证书和重定向里那些容易踩的坑。

---

## 第六章：校验与安全

下载完成不等于下载成功。一个文件可能因网络中断而残缺，也可能在传输途中被替换成恶意版本。这一章解决两件事：如何用校验和确认文件完整无损，以及代理、TLS 证书、重定向这些网络层参数里藏着哪些必须知道的安全坑。

### 6.1 校验和：sha256sum / sha512sum

> [!tip] 大白话：把校验和想成文件的「指纹」
> 就像每个人的指纹唯一，SHA-256 会给一段内容算出一串固定长度的十六进制串（64 位字符）。内容哪怕只差一个字节，指纹也完全不同。所以「校验和一致」≈「文件一模一样」。

下载软件包时，官方通常会给出一个 `.sha256` 文件或一串哈希值。你在本地算一次，再和官方公布的值比对，就能确认传输过程没有被篡改。

```bash
# 1. 计算单个文件的校验和
sha256sum ubuntu-24.04.iso
# 输出：<64位哈希>  ubuntu-24.04.iso

# 2. 把校验结果存成清单文件（哈希 + 文件名一起记下）
sha256sum ubuntu-24.04.iso > ubuntu-24.04.iso.sha256

# 3. 用 -c 核对（check）：逐条重算并比对，一致输出 OK
sha256sum -c ubuntu-24.04.iso.sha256
# 输出：ubuntu-24.04.iso: OK
```

`-c` 会读取清单里的「哈希 + 文件名」，重新计算当前文件再比对；文件被改动或损坏时输出 `FAILED` 并以非零退出码结束，正好适合写进脚本做下载后检查（见第八章）。`sha512sum` 用法完全相同，哈希更长更保守。此外，`-` 或空参数表示从标准输入读取，可校验管道里的数据。[GNU Coreutils sha2-utilities](https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html)

> [!note] `-c` 是「清单核对」模式
> 官方常发布一份含多个文件哈希的清单，下载后用 `sha256sum -c 清单文件` 一次性核对全部条目，不必手动逐个比对。

### 6.2 aria2 内置校验：--checksum + -V

用 aria2 下载时不必等下载完再单独校验——它可以边下边算，下完自动核对。`--checksum=TYPE=DIGEST` 指定哈希算法与期望值（如 `sha-256=...`），配合 `-V`（`--check-integrity`）开启完整性检查；校验失败时 aria2 会从零重新下载，而不是把坏文件留给你。[aria2c(1) Manual](https://aria2.github.io/manual/en/html/aria2c.html)

```bash
aria2c --checksum=sha-256=<官方公布的64位哈希> -V \
  -d ./iso https://example.com/ubuntu-24.04.iso
```

> [!tip] 大白话：相当于「先报指纹、再收货」
> 你提前告诉 aria2 这个文件应有的指纹，它下完自己核验。对不上就从头重下，省得你手动再算一遍。

### 6.3 TLS 证书：为什么不要用 -k 掩盖问题

HTTPS 的安全基础是证书验证：客户端检查服务器的证书链、域名、有效期，确认自己在和「正主」通信。curl 的 `-k`（`--insecure`）和 wget 的 `--no-check-certificate` 会跳过这套检查——传输仍然是加密的，但你无法确认加密对象是谁，中间人攻击的门就此敞开。[curl man page](https://curl.se/docs/manpage.html) / [GNU Wget Manual](https://www.gnu.org/software/wget/manual/)

> [!warning] 生产环境永远不要用 -k / --no-check-certificate
> 它只该出现在自签名证书的本地测试环境。生产脚本里出现 `-k`，等于对攻击者说「请随意劫持」。正确做法是解决证书信任本身（补装 CA、修正域名），而不是关掉验证。

```bash
# ❌ 错误：跳过证书验证（生产禁止）
curl -k https://example.com/file.zip -O

# ✅ 正确：不做跳过，让 curl 用系统信任的证书链正常验证
curl https://example.com/file.zip -O

# 若服务器是自签名/内网 CA：把 CA 证书交给 curl，而非关掉验证
# curl --cacert my-ca.pem https://example.com/file.zip -O
```

### 6.4 代理：curl -x / aria2 --all-proxy

需要走代理访问外网的场景，curl 用 `-x`（`--proxy`）指定代理，默认按 HTTP 代理处理，也支持 `socks4://`、`socks5://`；`--noproxy` 可排除个别主机不走代理。[curl man page](https://curl.se/docs/manpage.html)

```bash
curl -x http://proxy.example.com:8080 -fL -O https://example.com/file.zip
```

> [!warning] 代理下 URL 内嵌凭据无效
> 通过代理访问时，URL 里的 `user:pass@host` 凭据不会生效，必须用 `-u user:pass` 单独交给代理。也不要图省事把密码写进 URL——它会出现在日志和进程列表里。

aria2 没有裸 `--proxy`，改用 `--all-proxy`（覆盖所有协议）或 `--http-proxy`、`--https-proxy` 分协议指定。也可以不写参数，直接靠环境变量 `http_proxy` / `https_proxy`，curl、wget、aria2 大多会自动读取。

### 6.5 重定向安全：-L 的凭据 / Cookie 行为

下载链接经常跳转（30x），`-L`（`--location`）让 curl 跟随重定向。但 curl 默认最多跟随 50 次，而且跨主机跳转时会有意**不传递** URL 凭据和 Cookie——这是安全保护：避免你把 A 站的密码交给 B 站。另外，POST 请求在遇到 301/302/303 响应后会自动转成 GET。[curl man page](https://curl.se/docs/manpage.html)

> [!tip] 大白话：临时工牌不通用
> 凭据和 Cookie 就像公司工牌。从 A 公司跳到 B 公司，B 不认 A 的工牌——curl 宁可让你重新认证，也不把 A 的工牌递给陌生人。

### 本章小结

- `sha256sum` / `sha512sum` 给文件算「指纹」，`-c` 按清单一次性核对，失败会非零退出，适合脚本化。
- aria2 `--checksum=sha-256=... -V` 下载时内置校验，失败自动从头重下。
- `-k` / `--no-check-certificate` 跳过 TLS 证书验证，生产勿用；应修复证书信任而非关闭验证。
- 代理：curl 用 `-x`、aria2 用 `--all-proxy`；代理下 URL 内嵌凭据无效，改用 `-u`。
- curl `-L` 最多跟随 50 次重定向，跨主机不传递凭据/Cookie，POST 遇 30x 会转 GET。

下一章把这些校验与安全参数放进 bash 脚本，用 URL 列表文件驱动批量下载，并解决逐行安全读取、数组遍历与有限并发。

---

## 第七章：批量下载脚本基础

真实场景里，我们很少只下载一个文件：一整套开源组件、一批数据集、一个网站的全部图片，动辄几十上百个 URL，一条条敲命令显然不现实。这一章把「下载」从单文件升级成「批量」：先用一个列表文件把 URL 收集起来，再用脚本逐行读取、按数组组织，并以可控的并发度一次下载多个文件。

### 7.1 用列表文件驱动下载：`-i` 与多 URL

把要下载的 URL 一行一个写进文本文件，就能让工具自己照着清单下载，这就是 `-i` 选项。它是「用命令文件下载」最直接的形态——你的命令文件就是这份 `urls.txt`。

> [!tip] 大白话
> 把 `urls.txt` 想成一张购物清单。清单上写了什么，程序就照着买什么，不用每买一样都开口说一次。所以有了清单文件，一条命令就能下完整个清单。

wget 的 `-i file` 逐行读取 URL 批量下载，写成 `-` 就从标准输入读，方便配合管道；若配合 `--force-html`，甚至可按 HTML 解析链接[^c7-1]。aria2 的 `-i file` 同样是批量 URI，但更强：**同一文件的多镜像源用 TAB 写在同一行**（一个失败自动换下一个）；支持 gzip 压缩的输入；行首 `#` 可写注释[^c7-1]。

```bash
# urls.txt：wget / aria2 通用，每行一个 URL（aria2 支持 # 注释）
https://example.com/data/a.iso
https://example.com/data/b.iso
# 同一文件的两个镜像，用 TAB 分隔（仅 aria2 支持）
https://mirror1.example.com/b.iso	https://mirror2.example.com/b.iso

# wget：照着清单逐个下载到当前目录
wget -i urls.txt

# aria2：同样用法，还认识多镜像行和注释
aria2c -i urls.txt
```

curl 没有 `-i`，它的批量方式是「一次给多个 URL + 多个 `-O`」、globbing（`{a,b}` / `[1-100]`）或 `-Z` 并行（第五章已详述）[^c7-2]。三者的共同点是：把 URL 先集中到一处，再一次性喂给命令。

### 7.2 bash 逐行读取 URL 列表

`-i` 适合工具自带的批量；但想在下载前过滤、改名、加日志，就得自己写循环。bash 里读取 URL 列表的安全姿势是 `while read -r`[^c7-3]：

```bash
# 逐行安全读取：-r 原样保留反斜杠，避免 URL 里的 \ 被当成转义符
while read -r u; do
  curl -fL -O "$u" || echo "FAIL $u" >> err.log
done < urls.txt
```

`while read -r u; do ...; done < urls.txt` 一行行读文件：每行交给循环体处理一次，处理完自动读下一行。`-r` 是关键修饰符——`read` 默认把反斜杠当转义符，URL 中若带 `\` 会被吞掉；`-r` 让它原样保留。变量 `u` 在使用时**必须加引号**（`"$u"`）。

> [!warning] 引号与分词陷阱
> 别写成 `for u in $(cat urls.txt)`。`$(...)` 的结果会再次经历分词和文件名展开：URL 里带空格会被拆成两个词，带 `&`、`*`、`?` 等字符可能被当成后台符号或通配符。用 `while read -r` + `"$u"` 就是为了绕开这两类陷阱。

### 7.3 数组遍历与防分词（`"${arr[@]}"`）

有时我们希望先把 URL 装进内存，统一处理后再下载（比如过滤空行、去掉注释，再分批并发）。bash 的索引数组正是干这个的。遍历数组的安全写法是 `for u in "${urls[@]}"`[^c7-4]：

```bash
# 一个准备好的 URL 数组（也可先用 7.2 的 while read -r 逐行从文件读入）
urls=(
  "https://example.com/file with space.txt"   # 注意：URL 里有空格
  "https://example.com/api?a=1&b=2"
  "https://example.com/img/icon*.png"
)

# "${urls[@]}"：每个元素独立成一个词，空格/&/通配符都安全
for u in "${urls[@]}"; do
  echo "downloading: $u"
  curl -fL -O "$u"
done
```

> [!tip] 大白话
> 把每个 URL 想成一件货物。bash 默认见到空格就「拆货」，`"${arr[@]}"` 相当于给每件货物贴上独立标签、整件搬运。所以 URL 里再有空格、`&`、通配符，也不会被拆成两段或触发奇怪解释。

`"${arr[@]}"` 的三段缺一不可：`[@]` 表示「逐个元素展开」，外面那层双引号保证**每个元素被当成一个整体**。少了引号写成 `${arr[@]}`，带空格的元素一样会被拆开——这正是 7.2 引号陷阱在数组场景的翻版。

### 7.4 有限并发：后台任务与 `wait`

串行下载几十个文件太慢，但一口气把全部 URL 都丢到后台，又可能压垮服务器或占满内存。折中方案是「有限并发」：同时只开固定 N 个后台任务。bash 的后台符 `&` 让命令立即返回、继续往下执行；`$!` 记录最近一个后台任务的 PID[^c7-5]。

```bash
# 同时只派 3 个后台任务，各自记录 PID
curl -fL -O "$u1" & p1=$!
curl -fL -O "$u2" & p2=$!
curl -fL -O "$u3" & p3=$!

# wait 逐个等任务结束，并取出真实的退出码
wait "$p1"; s1=$?
wait "$p2"; s2=$?
wait "$p3"; s3=$?
echo "退出码：$s1 $s2 $s3"   # 任一非 0 即表示对应下载失败
```

> [!tip] 大白话
> 把 `&` 想成「把活丢给工人去做，自己不等他做完就去派下一单」。工人喊「我接单了」不等于「我干完了」，所以后台命令返回的 0 只是「已接单」；`wait` 才是监工，逐个验收盖章、报告真实成败。所以取退出码必须 `wait "$pid"`。

> [!warning] 后台命令的退出码恒为 0
> 用 `&` 启动的命令，bash 只记录「启动成功」，此时直接取 `$?` 永远是 0，即使下载实际失败了。必须用 `wait "$pid"` 等它真正结束，`wait` 的退出码才是该任务的真实结果。所以「开任务 → 记 PID → wait PID」三步缺一不可。

上面这段一次固定开 3 个任务，简单但「并发数写死」。真正按列表边跑边补、始终保持 N 个并发的写法，放到第九章的完整脚本里串起来。

### 本章小结

- 批量下载的第一步是「列表文件」：wget / aria2 用 `-i` 直接读 URL 清单（aria2 还支持 TAB 多镜像与 `#` 注释）；curl 则用多 `-O`、globbing 或 `-Z`。
- 在脚本里读列表用 `while read -r u; do ...; done < urls.txt`：`-r` 防反斜杠转义，变量必须加引号。
- 数组遍历用 `"${urls[@]}"`：`[@]` 逐个展开、外层引号保整体，防止空格/通配符把 URL 拆坏。
- 有限并发靠「`&` 后台 + `$!` 记 PID + `wait "$pid"` 取真实退出码」三步，别信后台命令直接返回的 0。
- 引号与分词是这一章所有坑的总根源：URL 含空格、`&`、`*` 时必须靠引号和数组保护。

下一章把这些技巧接到错误处理上：学会读 curl/wget 的退出码、用 `set -euo pipefail` 让脚本出错即停、把失败记录进日志，让批量脚本真正「跑得住、查得清」。

---

[^c7-1]: 素材 #2.5「批量下载」：wget `-i` 逐行读 URL / `-` 读 stdin / `--force-html`，见 GNU Wget Manual 2.4；aria2 `-i` 的 TAB 多镜像与 `#` 注释，见 aria2c(1) Manual Basic Options。
[^c7-2]: 素材 #2.5「批量下载」：curl 批量用多 URL + 多个 `-O`、globbing、`-Z` 并行，见 curl man page `--remote-name`、Globbing、`--parallel`。
[^c7-3]: 素材 #2.5「批量下载」：`while read -r u; do ...; done < urls.txt` 逐行安全读取，见 GNU Bash Reference Manual 3.2.5.1。
[^c7-4]: 素材 #2.5、#2.8：`"${arr[@]}"` 每元素独立成词、防空格分裂，见 GNU Bash Reference Manual 6.7 Arrays。
[^c7-5]: 素材 #2.8「脚本组织技巧」：后台 `&` + `$!` + `wait "$p1" "$p2"`，异步命令退出码恒 0 需 wait 取真实结果，见 GNU Bash Reference Manual 3.2.4、3.4.2、7.2。

---

## 第八章：错误处理与脚本健壮性

写下载脚本最大的风险不是"命令写错"，而是"命令失败了脚本却不知道"。这一章我们把错误处理补齐：先学会读懂 curl / wget 的退出码，再给脚本装上 `set -euo pipefail` 三道保险，用引号防住 URL 断裂，最后把失败的 URL 记进日志，让批量下载既不会"假成功"，也不会"带病硬跑"。

### 8.1 退出码语义：命令的"回执"

Linux 里每条命令结束都会返回一个数字——退出码。`0` 表示成功，非 `0` 表示失败，而且数字本身往往能告诉你失败原因。curl 和 wget 各有一套自己的语义。

> [!tip] 大白话：退出码 = 命令的回执
> 把退出码想成"命令办完事给终端的回执"：`0` 是"办成了"，非 `0` 是"没办成，而且数字还能告诉你怎么没办成"。所以脚本不用去"读输出文字"，只看一个数字就能分流处理——这正是 `if` / `||` / `$?` 能自动判断成败的前提。

**curl 常用退出码**（素材 #2.7）：

| 退出码 | 含义 | 备注 |
|--------|------|------|
| 0 | 成功 | |
| 18 | 部分传输（文件只下了一半） | 续传要解决的场景 |
| 22 | HTTP 4xx/5xx（如 404） | **仅配合 `--fail` / `-f` 才会返回** |
| 28 | 超时 | |
| 33 | Range 请求不被服务器支持 | |
| 35 | SSL 连接错误 | |
| 36 | 续传失败 | |

特别注意：退出码 22 只在加了 `-f` 时才出现。没加 `-f` 时，HTTP 404 也会返回 0——这正是前面反复强调"脚本里务必 `-fL`"的原因，否则会把 404 当成下载成功。

**wget 退出码**（素材 #2.7）：

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 通用错误 |
| 2 | 解析错误 |
| 3 | 文件 I/O 错误 |
| 4 | 网络失败 |
| 5 | SSL 校验失败 |
| 6 | 用户名/密码认证失败 |
| 7 | 协议错误 |
| 8 | 服务器返回错误响应 |

wget 在多个错误同时发生时，除 0/1 外编号更小的错误优先报告。

拿到退出码后，有三种常见分支写法（素材 #2.7、#2.8）：

```bash
# 方式一：先捕获到变量再判断（推荐，$? 必须紧跟目标命令）
curl -fL -O "$url"
code=$?                       # 立刻读取，中间插别的命令会覆盖它
if [[ $code -ne 0 ]]; then
  echo "失败，退出码=$code"
fi

# 方式二：|| 短路，失败时执行兜底
curl -fL -O "$url" || echo "失败，退出码=$?"

# 方式三：if 直接把命令当条件
if ! curl -fL -O "$url"; then
  echo "失败"
fi
```

`$?` 存的是"上一条命令"的退出码，所以必须紧跟目标命令读取，中间一旦执行了别的命令，它就变成那条命令的退出码了。

### 8.2 `set -euo pipefail`：让脚本出错即停

单条命令的错误好判断，但脚本一长，任何一条静默失败都会让后面"带病执行"。bash 用三个选项组合解决：

```bash
#!/usr/bin/env bash
# download.sh —— 健壮脚本的最小骨架
set -euo pipefail             # -e 出错即停 | -u 未设变量报错 | pipefail 管道失败可捕获

url="$1"                      # 第一个参数；没传时 -u 会直接报错，而不是带病运行
curl -fL -O "$url"            # -f 让 HTTP 4xx/5xx 转成非零退出码
echo "done: $url"
```

拆开看（素材 #2.7、#2.8）：

- `-e`：任何命令返回非零，脚本立即退出，不再往下跑。
- `-u`：使用未定义变量时报错退出，能抓出拼写错误。
- `pipefail`：管道中任何一条命令失败，整条管道的退出码就算失败。没有它，`curl ... | tee log` 这类写法即使 curl 失败了，管道也可能因为 `tee` 成功而返回 0。

> [!tip] 大白话：三道安全绳
> 把 `set -euo pipefail` 想成工地的三道安全绳：`-e` 是一出事故就停工；`-u` 是材料清单缺项直接叫停，不"带病施工"；`pipefail` 是流水线上任何一环出错，整条线都算失败。所以脚本不会在出错后继续闷头往下跑。

一个必须知道的例外（素材 #2.8）：`-e` 不会在"被检查"的语境里触发退出。当命令出现在 `if` / `while` 的条件里，或者 `&&` / `||` 的左侧时，bash 认为这个失败"正在被处理"，`-e` 不生效。这个行为看起来像漏洞，其实正是 8.4 节能逐条处理失败、而不是整体退出的原因。

### 8.3 引号陷阱：URL 里的特殊字符

变量不加引号时，bash 会对它的值再做一次"分词 + 文件名展开"——这正是 URL 断裂的根源（素材 #2.8）。

- **空格**：`curl -fL -O $u`，当 `u` 含空格时，URL 被拆成多个参数。
- **`&`**：最危险。`&` 是后台执行符，不加引号会把命令从 `&` 处截断，后半段甚至被当成新命令转后台执行，下载几乎必错，还会留下莫名其妙的"后台进程"。
- **通配符**：`*`、`?`、`[` 会被当成文件名通配符展开，命中目录里的文件就把 URL 替换成别的文件名。

一律用双引号包裹变量：

```bash
curl -fL -O "$u"      # 整箱搬运，值里的特殊字符不被重新解释
```

> [!tip] 大白话：引号 = 打包箱
> 把双引号想成打包箱：`"$u"` 是整箱搬运，里面有没有空格都不会散；不加引号等于把箱子拆开，所有空格、`&`、`*` 都会被重新当成分隔符。URL 里全是特殊字符，必须整箱搬。

同理，数组展开用 `"${urls[@]}"`、参数全量传递用 `"$@"`——它们保证每个元素独立成词、不被空格分裂。而 `[[ ]]` 条件测试内部不做分词，所以写 `[[ $code -ne 0 ]]` 时变量可以不加引号也安全。

### 8.4 失败记录：`|| echo "FAIL $u" >> err.log`

批量下载时，我们通常不想"遇到一个失败就整体退出"，而是希望跑完一轮后能知道哪些 URL 失败了、下一轮重试。做法是让每次失败只负责"记账"：

```bash
#!/usr/bin/env bash
# batch.sh —— 逐条下载，失败的 URL 记入 err.log
set -euo pipefail
err="err.log"

while read -r u; do
  curl -fL -O "$u" || echo "FAIL $u" >> "$err"   # 成功静默，失败追加一行日志
done < urls.txt

echo "处理完毕，失败的 URL 见 $err"
```

关键就在 `||` 后面这一句（素材 #2.8）：

- `curl` 成功：短路生效，`||` 右侧不执行，循环继续下一条。
- `curl` 失败：`>>` 把 `FAIL https://...` 这一行**追加**进 `err.log`，循环继续。
- 因为 `curl` 处于 `||` 左侧这个"被检查语境"，即便开着 `set -e` 也不会中途退出——这正是上一节说的那个例外派上用场的地方。

跑完一轮后 `cat err.log`，就能看到类似 `FAIL https://example.com/missing.iso` 的行；下一轮可以从日志里挑出这些 URL 集中重试，不用重下已经成功的文件。

### 本章小结

- 退出码是命令的"回执"：curl 的 0/18/22/28/33/35/36、wget 的 0-8 各有含义；**curl 的 22 只在加 `-f` 后出现**，否则 404 会被当成成功。
- `$?` 必须紧跟目标命令读取；`if` / `||` / `$?` 三种方式都可以按退出码分流。
- `set -euo pipefail` 让脚本出错即停、未设变量即报错、管道失败可捕获；但它在 `if` / `while` 条件、`&&` / `||` 左侧这些"被检查语境"不退出。
- 变量一律用 `"$u"`、`"${arr[@]}"`、`"$@"` 包裹，防止空格、`&`、通配符把 URL 拆断。
- 批量脚本用 `curl -fL -O "$u" || echo "FAIL $u" >> err.log` 逐条记账，跑完后从日志集中重试。

下一章，我们把前八章的内容拼成一个完整的实战脚本：参数解析、列表读取、断点续传、重试、校验、失败报告一次到位。

---

**参考来源**（素材 #2.7、#2.8）：

- [curl 手册：Exit codes](https://curl.se/docs/manpage.html)
- [GNU Wget 手册：Exit Status](https://www.gnu.org/software/wget/manual/)
- [GNU Bash 参考手册：The Set Builtin / Word Splitting](https://www.gnu.org/software/bash/manual/bash.html)

---

## 第九章：实战案例：一个完整的批量下载脚本

> 本章综合素材 #2.1-#2.8，重点 #2.3（重试）、#2.5（批量）、#2.6（校验与安全）、#2.7（错误处理）、#2.8（脚本组织）。
> 素材映射：curl 参数见 [curl tutorial](https://curl.se/docs/tutorial.html) / [curl man page](https://curl.se/docs/manpage.html)，校验和见 [GNU Coreutils sha2-utilities](https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html)，bash 语法见 [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)，wget 见 [GNU Wget Manual](https://www.gnu.org/software/wget/manual/)。

前八章我们把工具选型、单文件下载、断点续传、重试、校验、批量与错误处理分别讲透了。但手动在终端里一条条敲命令，面对几十上百个文件时不现实：中断了要自己续、失败了要自己记、下坏了还浑然不知。这一章就把前面的知识串成一个能直接上手的产物——`download.sh`，一个「断点续传 + 自动重试 + 校验 + 失败日志」的完整批量下载脚本。学完本章，你会拥有一份可以放进自己工具库、反复复用的脚本模板。

### 9.1 需求与脚本骨架

#### 需求分析：这个脚本要解决什么问题

动手写代码前先列需求。把大目标拆成五件事，正好对应脚本的五个区块：

| 需求 | 对应区块 |
|------|----------|
| 输入是「每行一个 URL」的列表文件，默认 `urls.txt` | 参数区 + 读取区 |
| 逐个下载，某个失败不中断整个流程 | 下载区（`if` / `||` 守卫） |
| 中断后可续传，瞬时网络错误自动重试 | 下载区（`-C -` / `--retry`） |
| 下载后如有 `.sha256` 校验文件则校验 | 校验区 |
| 最后输出成功/失败报告，失败明细落盘 | 报告区 |

这套「需求 → 区块」的拆法本身就是一个设计习惯：先把脚本当作一个小产品来规划，而不是想到哪写到哪。

#### 骨架：脚本的第一行与第二行

任何 bash 脚本的骨架都是这两行：

```bash
#!/usr/bin/env bash
set -euo pipefail
```

- `#!/usr/bin/env bash`：告诉系统用 PATH 里的 bash 解释器运行（而不是 sh），Linux/macOS 都通用。
- `set -euo pipefail`：一句话把脚本调成「严谨模式」——`-e` 某条命令失败就退出、`-u` 用到未定义变量立刻报错、`pipefail` 让管道中任一条命令失败都算失败（素材 #2.7，[GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)）。

> [!tip] 大白话：set -euo pipefail 像什么？
> 把它想成一位**严格监理的装修师傅**：一看到墙砌歪了（命令失败）、图纸缺了页（变量未定义），立刻叫停，绝不含糊继续干。
> 所以：脚本一出错就被尽早发现，不会带着隐患往下跑，最后攒成一堆难查的问题。

### 9.2 脚本区块逐段讲解

先睹为快，完整脚本一次看完，再逐区拆讲：

```bash
#!/usr/bin/env bash
# download.sh —— 批量下载脚本（断点续传 + 重试 + 校验 + 失败日志）
# 用法：bash download.sh [urls.txt]

set -euo pipefail

# ===================== 参数区 =====================
URL_LIST="${1:-urls.txt}"   # URL 列表文件，默认 urls.txt
LOG_FILE="err.log"          # 失败记录文件
VERIFY="yes"                # 设为 no 可关闭校验

# ===================== 读取区 =====================
if [[ ! -f "$URL_LIST" ]]; then
    echo "错误：找不到 URL 列表文件 $URL_LIST" >&2
    exit 1
fi

: > "$LOG_FILE"             # 清空旧的失败日志，避免误报上次的失败

downloaded=0
failed=0

# ===================== 下载区 =====================
while read -r u; do
    # 跳过空行与 # 开头的注释行
    [[ -z "$u" || "$u" == \#* ]] && continue

    out="$(basename "$u")"          # 从 URL 提取远程文件名
    echo "==> 下载：$u"

    # -fL：HTTP 错误转非零退出码 + 跟随重定向
    # -C -：断点续传（已有部分文件时自动从偏移继续）
    # --retry 5 --retry-delay 3：瞬时失败重试 5 次，间隔 3 秒
    if curl -fL -C - --retry 5 --retry-delay 3 -O "$u"; then
        downloaded=$((downloaded + 1))
    else
        echo "FAIL $u" >> "$LOG_FILE"   # 失败写入日志，脚本继续
        failed=$((failed + 1))
        continue
    fi

    # ===================== 校验区 =====================
    if [[ "$VERIFY" == "yes" && -f "${out}.sha256" ]]; then
        if sha256sum -c "${out}.sha256"; then
            echo "    校验通过：${out}"
        else
            echo "CHECKSUM $u" >> "$LOG_FILE"
            echo "    校验失败：${out}（文件不完整或被篡改）"
        fi
    fi
done < "$URL_LIST"

# ===================== 报告区 =====================
echo
echo "======== 下载报告 ========"
echo "成功：$downloaded"
echo "失败：$failed"
if [[ -s "$LOG_FILE" ]]; then
    echo "失败明细已写入 $LOG_FILE："
    cat "$LOG_FILE"
    exit 1
fi
echo "全部完成，无失败。"
```

#### 参数区：让脚本可配置

`URL_LIST="${1:-urls.txt}"` 是本章第一个要记的写法：`${1:-默认值}` 表示「第一个位置参数没传就用默认值」。所以你既可以 `bash download.sh urls.txt` 显式指定列表，也可以直接 `bash download.sh` 走默认。`LOG_FILE` 和 `VERIFY` 同理，把「容易变的东西」全部提到文件顶部，改配置不用翻到脚本中间。

#### 读取区：检查输入 + 清空旧日志

`[[ ! -f "$URL_LIST" ]]` 是测试文件不存在，不存在就打印错误到标准错误（`>&2`）并 `exit 1`——失败就要让调用方知道。接着 `: > "$LOG_FILE"` 清空上一次运行的失败日志：冒号 `:` 是 bash 的空命令，重定向它的输出就把文件截断成空。这一步很关键，否则第二次运行时会把上次的失败一起报出来。

#### 下载区：核心循环

`while read -r u; do ... done < "$URL_LIST"` 逐行读取 URL 列表（素材 #2.5，#2.8）。`-r` 禁止反斜杠转义；`[[ -z "$u" || "$u" == \#* ]] && continue` 跳过空行和 `#` 注释行。

> [!warning] 这里有一个经典坑
> 列表文件要用 `< 文件` 重定向，**不要**写成 `cat urls.txt | while read ...`。管道会让 `while` 在子 shell 里执行，循环里累加的 `downloaded` / `failed` 在循环结束后外面根本读不到——报告区永远是 0。

循环体里这一行是整个脚本的心脏：

```bash
curl -fL -C - --retry 5 --retry-delay 3 -O "$u"
```

这是第四章的 `-C -`（续传）、第五章的 `--retry 5 --retry-delay 3`（重试）、第六章的 `-fL`（错误转码 + 跟随重定向）全部合体，也就是素材「实用建议」里给的通用安全下载模板（#2.3、#2.6）。注意在 `set -e` 下必须用 `if curl ...; then` 或 `||` 守卫：否则第一个失败就会让脚本直接退出，后面几十个文件都不下了。失败分支把 `FAIL $u` 追加进 `err.log`，计数器加一，`continue` 跳去下一个。

> [!tip] 大白话：-C - 断点续传像什么？
> 像**拷贝文件拷到一半拔了 U 盘**：重新插上不是从头再拷，而是接着已经拷完的部分继续。`-C -` 就是告诉 curl「看本地已有多少，从那里接着下」。
> 所以：大文件下载中断后重跑脚本，只补剩下的部分，不浪费前面的进度。

> [!tip] 大白话：--retry 5 像什么？
> 像**打电话占线**：一次没打通，隔几秒再拨，最多拨 5 次。`--retry-delay 3` 就是「每次重拨等 3 秒」。
> 所以：网络瞬时抖动时脚本会自己缓过来，而不是立刻报错。

#### 校验区：有侧车校验文件就验

`-f "${out}.sha256"` 判断同目录有没有对应的 `.sha256` 侧车文件（下载目标附带校验文件时，见 #2.6）。有就执行 `sha256sum -c "${out}.sha256"`：`-c` 会读侧车文件里的「哈希 + 文件名」，并和实际文件比对。通过就打印成功，不通过把 `CHECKSUM $u` 写进日志并提示——但同样不中断流程，让其他文件继续下。

> [!tip] 大白话：sha256sum -c 像什么？
> 像**收货验指纹**：每个文件都有唯一的「指纹」（哈希），官方给的 `.sha256` 文件里存着「正品指纹」。`-c` 就是给下载到的文件现场按指纹，再和正品指纹比对。
> 所以：文件在传输中损坏或被篡改都能被发现，而不是默默拿到一个坏文件。

#### 报告区：成败一目了然

最后统计成功/失败数量并打印。`[[ -s "$LOG_FILE" ]]` 判断日志文件非空：有失败就打印明细并 `exit 1`（脚本整体算失败，方便 CI 或调用脚本感知），否则提示全部完成。这一区让「脚本跑完到底怎么样了」三秒钟就能看清。

### 9.3 运行与常见排查

#### 运行方式

```bash
chmod +x download.sh        # 加执行权限
./download.sh urls.txt      # 或用 bash download.sh urls.txt
```

`urls.txt` 每行一个 URL：

```
https://example.com/app.zip
https://example.com/app.zip.sha256
https://mirror.example.com/patch.tar.gz
```

两个注意点：`.sha256` 侧车文件要放在和下载文件同一目录（脚本运行目录）；如果侧车文件也靠脚本下载，让它排在它对应的文件**之前**，校验才会命中。

#### 常见排查表

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| 404 假成功 | curl 没用 `-f`，404 仍返回 0 | 脚本已用 `-fL`；再检查 URL 是否过期 |
| 退出码 28 | 网络超时 | `--retry` 已自动处理；仍失败检查网络/镜像 |
| 退出码 33 | 服务器不支持 Range，续传失败 | 换支持续传的镜像，或删掉半截文件重下 |
| 校验失败 | 文件损坏 / 被篡改 / 侧车文件名不匹配 | 重新下载；确认 `.sha256` 确实属于该文件 |
| 文件名带 `?` 参数 | URL 含查询串，`basename` 结果与 curl 实际保存名不一致 | 改用 `-o` 显式指定本地文件名 |
| 走代理/公司网络 | 需要代理才能联网 | 见 9.4 代理注意事项 |
| 磁盘满 / 权限不足 | I/O 类错误 | 检查磁盘空间与写权限 |

### 9.4 最佳实践清单

1. **通用安全下载模板**：单文件下载一律用 `curl -fL -C - --retry 5 --retry-delay 3 -O URL`——跟随重定向、断点续传、失败重试、HTTP 错误转退出码四件事一次做完（#2.3、#2.6）。这是「最小安全模板」的完整升级版，可以直接背下来。
2. **批量 URL 文件**：每行一个 URL，用 `while read -r u; do curl -fL -O "$u" || echo "FAIL $u" >> err.log; done < urls.txt`（#2.5）。列表文件一律用 `<` 重定向而非管道，避免子 shell 丢失循环变量（#2.8）。
3. **校验**：下载后 `sha256sum -c file.sha256` 验证完整性；官方发布页通常同时给出校验和文件（#2.6，[GNU Coreutils sha2-utilities](https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html)）。
4. **代理注意事项**：脚本内 `export https_proxy=http://proxy:port` 或 `curl -x` 指定代理；代理下 URL 内嵌凭据无效，需改用 `-u`；不要用 `-k`/`--insecure` 掩盖证书问题（#2.6，[curl man page](https://curl.se/docs/manpage.html)）。
5. **退出码判断**：curl 脚本务必 `-f`（或 `-fL`），否则 HTTP 404 仍返回 0，造成「假成功」（#2.7）。
6. **脚本骨架**：`#!/usr/bin/env bash` + `set -euo pipefail` + 数组/循环；所有变量加引号（`"$u"`、`"${out}.sha256"`），防止 URL 含空格、`&`、通配符时被分词破坏（#2.8，[GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)）。

> [!warning] 两条红线
> 1. 别去掉 `-f`：没了它，404 返回 0，脚本会「成功」下载一个错误页，校验也救不回来。
> 2. 别用 `-k` 绕过证书校验来「解决」证书报错：那只是掩盖问题，中间人攻击照样能注入内容。证书真有问题就补正确证书链，而不是关掉检查。

### 本章小结

- 一个可复用批量下载脚本的五个区块：参数区、读取区、下载区、校验区、报告区——先拆需求再写代码。
- 核心一行 `curl -fL -C - --retry 5 --retry-delay 3 -O "$u"` 集成了续传、重试、错误转码与跟随重定向。
- `while read -r` 读 URL 列表用 `< 文件` 重定向，别用管道，避免子 shell 丢变量。
- 失败不中断：用 `if curl ...; then` / `||` 守卫 `set -e`，失败写 `err.log` 后继续处理下一个。
- 校验、代理、退出码三件事是「安全下载」的兜底网，缺一不可。

---

## 相关笔记

- [[linux/linux MOC|Linux 学习笔记 MOC]] — Linux 主题目录索引
- [[linux常用命令/Linux 网络诊断与排障]] — ping、curl、ss 等网络工具速查
- [[Ubuntu curl SSL连接问题排查]] — curl 证书/SSL 故障排查实战
- [[linux/Linux换源]] — 镜像源配置与软件下载加速
- [[Shell脚本入门教程]] — bash 脚本基础入门

---

## 结语与下一步

到这里，九章的内容已经全部完成。我们沿着「选型 → 基础 → 可靠性 → 批量 → 健壮性 → 实战」的路径，把命令行下载从单条命令推进到一个可复用的完整脚本：

- **选型与基础**：curl 灵活、wget 镜像强、aria2 并发快，最小安全模板 `curl -fL -O URL`。
- **可靠性**：`-C -` / `-c` / aria2 自动续传解决中断，`--retry` 系列解决瞬时失败，`-Z` / `-x -s -j` 解决慢。
- **校验与安全**：`sha256sum -c` 与 aria2 `--checksum` 验完整性；代理、TLS 证书、重定向的凭据行为是安全底线。
- **批量与健壮性**：`while read -r` 读列表、`"${urls[@]}"` 防分词、`set -euo pipefail` 出错即停、`err.log` 记失败。
- **实战收尾**：`download.sh` 把上述能力合体，参数区、读取区、下载区、校验区、报告区五大区块清晰可改。

下一步建议：

1. 把第九章的 `download.sh` 复制进自己的脚本库，按需调整参数区（默认列表文件、日志路径、校验开关）。
2. 用真实下载任务跑一遍，观察 `err.log` 与退出码，加深对 `-f`、`--retry`、`-C -` 的直觉。
3. 需要更深的并发控制时，可以研究 aria2 的 `-x` / `-s` / `-j` 默认值（本机 `aria2c --help` 可查），或阅读 curl / wget / aria2 官方手册。
4. 若要将本笔记发布到 Obsidian，可进一步补充标签、Callout 与双链，使其更适合个人知识库阅读。

这份笔记的代码示例都建议在终端亲手敲一遍——命令行下载的坑，往往在亲手踩过之后才真正记住。
