# 第三章：wget 与 aria2 基础用法

第二章我们用 curl 完成了单文件下载，掌握了 `-O` / `-o` / `-L` / `-fL` 的最小模板。但下载场景不止 curl 一个解：wget 是"镜像与递归"的老牌选手，aria2 是"并发分片"的速度之王。本章把这两个工具的基础下载参数讲透，并在结尾给出三工具下载同一文件的对照，让你拿到 URL 时能随手选对工具、写对参数。

## 3.1 wget 基础：-O / -P / -nH

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

## 3.2 aria2 基础：-d / -o

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

## 3.3 三工具基础下载对比小结

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

## 本章小结

- wget 的 `-O` 把内容拼接写入单文件，运行瞬间截断目标，且与 `-N` 不兼容。
- wget 的 `-P` 设置目录前缀（检索树根），`-nH` 去掉默认的主机名目录层，二者常配合递归下载使用。
- aria2 的 `-d` 是存储目录，`-o` 是文件名；`-o` 相对 `-d` 解析，且只对命令行 URI 生效。
- 三工具参数命名不同，但"指定文件名 / 指定目录"的需求都能满足；选型看场景：灵活 curl、镜像 wget、速度 aria2。

下一章进入可靠性话题：网络中断后怎么续传。三工具的续传行为和限制各不相同，正是实战中容易踩坑的地方。

---

[^c3-1]: GNU Wget Manual，`-O` / `--output-document` 一节，https://www.gnu.org/software/wget/manual/
[^c3-2]: GNU Wget Manual，`-P` / `--directory-prefix` 与 `-nH` / `--no-host-directories` 一节，https://www.gnu.org/software/wget/manual/
[^c3-3]: aria2c Manual，Basic Options 的 `-d` / `--dir` 与 `-o` / `--out` 一节，https://aria2.github.io/manual/en/html/aria2c.html
