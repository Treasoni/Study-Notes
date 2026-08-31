# 第二章：curl 基础用法

本章掌握 curl 下载最核心的四个参数：`-O`、`-o`、`-L`、`-f`。

## 2.1 单文件下载：-O 与 -o

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

## 2.2 跟随重定向：-L

很多下载链接返回 30x，真正文件在 `location` 指向的地址。不加 `-L` 会下载到空文件或错误页；加 `-L`（`--location`）自动追到最终地址 [curl 手册 --location](https://curl.se/docs/manpage.html)：

```bash
curl -L -O https://example.com/latest/download   # 跟随重定向，落盘为最终文件名
```

> [!tip] 大白话：重定向像「店搬家」，老地址贴着新地址。`-L` 是愿意顺着新地址找的买家。

三个边界：默认最多跟随 **50 次**；**跨主机不传凭据和 Cookie**；POST 在 301/302/303 转成 GET。

## 2.3 错误转退出码：-f / -fL

**curl 默认不把 HTTP 状态码当失败**：404 时退出码仍是 0。加 `-f`（`--fail`）后，HTTP 400 及以上转为**退出码 22** [curl 手册 --fail](https://curl.se/docs/manpage.html)。

> [!warning] 404 假成功：不带 `-f` 时 `curl -O URL; echo $?` 打印 0。批量脚本里 `-f` 是第一道防线。

> [!tip] 大白话：退出码像「送达确认」。默认 curl 只要「送完」就算成功，哪怕签收的是「查无此人」回执；`-f` 让它报错。

## 2.4 最小可用模板

```bash
curl -fL -O https://example.com/latest/download   # 跟随重定向 + 错误转退出码 + 保存为远程名
echo $?   # 成功 0；失败（如 404）22，且不会把错误页存成文件
```

分工：`-f` 转 22，`-L` 跟随 30x，`-O` 存为远程名。续传、重试在此基础上叠加。

## 本章小结

- `-O` 存为远程文件名（不做 URL 解码）；`-o` 指定本地文件名；同名都会覆盖。
- `-L` 跟随 30x，默认最多 50 次；跨主机不传凭据 / Cookie。
- 默认 404 也是「成功」，`-f` 才转成退出码 22。
- 最小安全模板 `curl -fL -O URL`。

下一章对比 wget 与 aria2——注意 wget 的 `-O` 是拼接单文件，与 curl 不同。
