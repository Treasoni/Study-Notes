# 用命令文件下载 - 深度素材（阶段 2）

> 主题：用命令文件下载（Linux/macOS）
> 生成时间：2026-08-31
> 覆盖方向：A（工具基础与选型）+ B（下载可靠性）+ C（批量脚本实战）
> 素材来源：6 个本地缓存源文件（官方为主），见下表

---

## 一、范围与来源表

| ID | 来源 | 层级 | 抓取状态 |
|----|------|------|----------|
| S1 | [curl tutorial](https://curl.se/docs/tutorial.html) → `sources/02_curl_se.md` | 官方 | ✅ 完整（36KB） |
| S2 | [curl man page](https://curl.se/docs/manpage.html) → `sources/03_curl_se.md` | 官方 | ✅ 完整（355KB） |
| S3 | [GNU Wget Manual](https://www.gnu.org/software/wget/manual/) → `sources/05_wget_manual.md` | 官方 | ✅ 完整（223KB） |
| S4 | [aria2c(1) Manual](https://aria2.github.io/manual/en/html/aria2c.html) → `sources/04_aria2_github_io.md` | 官方 | ✅ 完整（205KB） |
| S5 | [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html) → `sources/06_bash_manual.md` | 官方 | ✅ 完整（545KB） |
| S6 | [GNU Coreutils sha2-utilities](https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html) → `sources/01_www_gnu_org.md` | 官方 | ✅ 完整 |

**层级分布**：官方 6 / 教程 0 / 社区 0（P1 中的教程来源未纳入精读，仅作 P3 补充参考）。
**覆盖缺口状态**：P1 缺口 4 项全部补齐（校验和 S6、代理/TLS S2+S3、Range 续传前提 S2+S3、wget 手册验证 S3）。

---

## 二、Claim / 来源映射

### 2.1 工具选型（方向 A）

| Claim | 来源/锚点 |
|-------|----------|
| curl：`-O` 保存为远程文件名（取 URL 文件名部分，去路径，已存在则覆盖）；`-o` 保存为指定本地文件 | S1「Download to a File」、S2 `#--remote-name`/`#--output` |
| wget：`-O` 将所有内容拼接写入单文件；`-P` 设置目录前缀；`-nH` 禁用主机名目录 | S3 2.5/2.6 |
| aria2：`-d` 存储目录、`-o` 文件名（相对 `--dir` 解析，仅命令行 URI 有效） | S4 Basic Options `-d`/`-o` |
| 选型要点：curl 灵活（协议多、脚本友好）、wget 递归镜像强、aria2 并发分片最强 | 推断（综合 S2/S3/S4，标记为 inference） |

### 2.2 断点续传（方向 B）

| Claim | 来源/锚点 |
|-------|----------|
| curl `-C -`：按本地已有文件自动计算偏移续传；与 `--range` 互斥 | S2 `#--continue-at`、S1「Resuming File Transfers」 |
| wget `-c`：仅续传此前 wget 留下的文件；**仅支持 FTP 与支持 Range 头的 HTTP 服务器**；服务器不支持时从头下载覆盖；远程文件被修改（非追加）会损坏 | S3 2.5 `--continue` |
| aria2 自身发起的中断无需 `-c`，同目录重跑即续传；`-c` 用于续传浏览器/wget 留下的文件，仅 HTTP(S)/FTP | S4 Basic Options `-c`「Resuming Download」 |
| HTTP Range 前提：`curl -r` 字节范围需服务器支持，失败退出码 33；续传本质依赖服务端 Range | S1「Ranges」、S2 Exit codes |

### 2.3 重试与可靠性（方向 B）

| Claim | 来源/锚点 |
|-------|----------|
| curl `--retry N`：默认 0 不重试；瞬时错误含超时、HTTP 408/429/500/502/503/504/522/524；指数退避 1s→10min 上限；`--retry-delay` 改固定间隔；`--retry-max-time` 限总时长 | S2 `#--retry`/`#--retry-delay`/`#--retry-max-time` |
| curl 默认不把 404 当重试条件；要对 4xx/5xx 都重试需 `--fail` 配合 `--retry-all-errors`（官方不建议默认启用） | S2 `#--fail`/`#--retry-all-errors` |
| wget `-t`：默认重试 20 次；0/inf 无限；**connection refused 默认不重试**（需 `--retry-connrefused`）；404 等致命错误不重试 | S3 2.5 `--tries`/`--retry-connrefused` |
| wget `--waitretry`：失败重试间线性退避（1s, 2s...默认上限 10s）；`--wait` 每次检索间等待 | S3 2.5 `--wait`/`--waitretry` |
| aria2 `--max-tries` + `--retry-wait`：设重试次数与间隔；`--retry-wait>0` 时 503 也触发重试 | S4 cmdoption-m / cmdoption-retry-wait |
| 超时：wget `--timeout` 统一设 DNS/连接/读取三类，默认 900s 读超时 | S3 2.5 `--timeout` |

### 2.4 并发下载（方向 B）

| Claim | 来源/锚点 |
|-------|----------|
| curl `-Z`/`--parallel`：多 URL 并行，默认最多 50 个并发（`--parallel-max` 可调） | S2 `#--parallel` |
| curl globbing：`{a,b}` 列表、`[1-100]` 范围一次生成多 URL，需加引号；`-g`/`--globoff` 关闭 | S2 Globbing、`#--globoff` |
| aria2 `-x`：每服务器最大连接数；`-s`/`--split`：N 条连接分片下载同一文件；`-k`/`--min-split-size`：小于 2×SIZE 不分割（默认 20M） | S4 cmdoption-x / cmdoption-s / cmdoption-k |
| aria2 `-j`：并发下载条目数（区别于单文件内分片连接数） | S4 Basic Options `-j` |
| wget 并发：官方手册无内置分片并发；批量并行靠 `-i` 多 URL + 外部脚本/aria2 | 推断（S3 无对应，标记为 inference） |

### 2.5 批量下载（方向 B+C）

| Claim | 来源/锚点 |
|-------|----------|
| wget `-i file`：逐行读 URL 批量下载；`-` 读 stdin；配合 `--force-html` 按 HTML 解析 | S3 2.4 `--input-file` |
| aria2 `-i file`：批量 URI；同文件多镜像用 TAB 分隔；支持 gzip；`#` 注释；条目内选项行以空格开头、去 `--` 前缀 | S4 Basic Options `-i` |
| curl 批量：多 URL + 多个 `-O`，或 globbing，或 `-Z` 并行 | S2 `#--remote-name`/`#--parallel`/Globbing |
| bash `while read -r u; do ...; done < urls.txt`：逐行安全读取 URL 列表 | S5 3.2.5.1 `while` |
| bash `for u in "${urls[@]}"`：数组遍历；`"${arr[@]}"` 每元素独立成词（防空格分裂） | S5 6.7 Arrays |

### 2.6 校验与安全（方向 B+C）

| Claim | 来源/锚点 |
|-------|----------|
| `sha256sum`/`sha512sum`：计算 SHA-2 校验和；`-` 或空参数从 stdin 读；可判断文件与校验和一致性（Untagged 格式） | S6 6.7 sha2 utilities |
| aria2 `--checksum=TYPE=DIGEST`（如 sha-1=...）+ `-V`/`--check-integrity`：整文件哈希校验，失败从头重下 | S4 cmdoption-checksum / cmdoption-V |
| TLS 坑：curl `-k`/`--insecure` 跳过证书校验（生产避免）；wget `--no-check-certificate` 自签名场景（机密数据勿用） | S2 `#--insecure`、S3 2.8 `--no-check-certificate` |
| 代理：curl `-x`/`--proxy`（默认 HTTP 代理，支持 socks4/5，`--noproxy` 排除主机；代理下 URL 内嵌凭据无效需 `-u`）；aria2 无裸 `--proxy`，用 `--all-proxy`/`--http-proxy` 等 | S2 `#--proxy`、S1 Proxy、S4 cmdoption-all-proxy |
| 重定向安全：curl `-L` 跨主机不传递凭据/Cookie；默认最多跟随 50 次；POST 在 301/302/303 转 GET | S2 `#--location` |

### 2.7 错误处理与退出码（方向 B+C）

| Claim | 来源/锚点 |
|-------|----------|
| curl 退出码：0 成功、22 HTTP 400+（需 `--fail`）、28 超时、18 部分传输、33 range 错误、35 SSL 错误、36 续传失败 | S2 Exit codes |
| wget 退出码：0 成功、1 通用、2 解析、3 I/O、4 网络、5 SSL、6 认证、7 协议、8 服务器错误响应 | S3 2.13 Exit Status |
| bash `$?` 取最近命令退出码；`||`/`if` 依据退出码分支；`curl -f` 使 HTTP 错误转非零退出码 | S5 3.7.5 / 3.2.5.2 / S2 `#--fail` |
| bash `set -euo pipefail`：`-e` 出错即退（被检查语境除外）、`-u` 未设变量报错、`pipefail` 让管道任一条失败被捕获 | S5 4.3.1 The Set Builtin |

### 2.8 脚本组织技巧（方向 C）

| Claim | 来源/锚点 |
|-------|----------|
| bash `for ((i=0; i<N; i++))` C 风格循环 + `{1..N}` 花括号展开（左闭右闭，可零填充） | S5 3.2.5.1 / 3.5.1 Brace Expansion |
| 索引数组/关联数组（`declare -A`）；`"${arr[@]}"` 防分词；`${!arr[@]}` 取下标/键 | S5 6.7 Arrays |
| 后台并行：`cmd & p=$!; ...; wait "$p1" "$p2"`；`$!` 最近后台 PID；异步命令退出码恒 0 需 wait 取真实结果 | S5 3.2.4 Lists of Commands / 3.4.2 / 7.2 wait、jobs |
| 引号陷阱：不引号会再次分词/文件名展开，URL 含空格/`&`/通配符会断裂；`[[ ]]` 内不分词且 `==` 支持模式匹配 | S5 3.5.7 Word Splitting / 3.2.5.2 |

---

## 三、矛盾与注意点

| 差异点 | curl | wget | aria2 |
|--------|------|------|-------|
| 续传触发 | `-C -`（需手动传） | `-c`（仅续传 wget 自己的文件） | 同目录重跑自动续传 |
| 404 重试 | 默认不重试 | 默认不重试 | 需配合 `--max-file-not-found` |
| 代理选项名 | `-x`/`--proxy` | 环境变量 + wgetrc | `--all-proxy`/`--http-proxy` |
| 并发模型 | 多 URL 并行（`-Z`） | 无内置分片 | 单文件分片（`-s`/`-x`）+ 多条目并行（`-j`） |

**未解决歧义**：
- S6 页面未逐字列出 `-c`/`--check` 选项名（仅注明可判断一致性）；P3/P4 如需可补抓 cksum 页，或直接以 `sha256sum -c file.sha256` 常识用法为准（标记 inference）。
- aria2 多项默认值（`-x`、`-s`、`--retry-wait`、`--summary-interval`）在转换文本中缺失，为避免臆造未填写；写作时若需准确默认值，建议本机 `aria2c --help` 验证。

---

## 四、实用建议（下游写作直接可用）

1. **通用安全下载模板**：`curl -fL -C - --retry 5 --retry-delay 3 -O URL`（跟随重定向、断点续传、失败重试、HTTP 错误转退出码）。
2. **批量 URL 文件**：每行一个 URL，用 `while read -r u; do curl -fL -O "$u" || echo "FAIL $u" >> err.log; done < urls.txt`。
3. **校验**：下载后 `sha256sum -c file.sha256`；或 aria2 `--checksum=sha-256=... -V`。
4. **脚本骨架**：`#!/usr/bin/env bash; set -euo pipefail` + 数组/循环 + `wait` 做有限并发；引号包裹所有变量。
5. **代理**：脚本内 `export https_proxy=...` 或 curl `-x`；不要用 `-k` 掩盖证书问题。
6. **退出码判断**：curl 脚本务必 `-f`（或 `-fL`），否则 HTTP 404 仍返回 0 造成假成功。

---

## 五、开放问题（留给大纲/写作阶段确认）

1. 笔记需要覆盖几个工具？全选三工具对比，还是以 curl 为主 + aria2 补充？（影响章节结构）
2. 是否需要 Windows/WSL 适配说明（当前限定 Linux/macOS）？
3. 是否需要补充教程层来源（P1 的腾讯云/CSDN/阿里云/DataCamp/php.cn）作为中文阅读参考？官方文档为主、教程为附。

---

## 六、下游交接

- **大纲输入**：`03_outline.md` 可由以上 2.1–2.8 结构映射（选型 → 单工具基础 → 可靠性 → 批量脚本 → 校验安全 → 错误处理）。
- **素材路径**：本地缓存 `workspace/command-file-download/sources/*.md`（S1–S6），写作阶段按需定点读取，避免重复抓取。
- **source 层级**：全部官方，事实可靠；含 3 处明确标注的 inference 需写作时注意措辞。
- **运行状态**：阶段 2 完成后等待用户确认素材质量，再进入大纲模式决策点。
