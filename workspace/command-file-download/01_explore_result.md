# 用命令文件下载 - 探测结果（阶段 1）

> 主题：用命令文件下载（Linux/macOS）
> 生成时间：2026-08-31
> 状态：待用户选择方向

---

## 一、研究透镜与候选来源

### 透镜 1：下载命令基础（curl / wget / aria2）

| # | 来源 | 层级 | 分数 | 相关性 | 日期 |
|---|------|------|------|--------|------|
| 1 | [curl tutorial](https://curl.se/docs/tutorial.html) | 官方 | 5 | curl 基础用法官方教程 | 持续更新 |
| 2 | [GNU Wget Manual](https://www.gnu.org/software/wget/manual/) | 官方 | 5 | wget 官方手册，下载/递归/配置 | 持续维护 |
| 3 | [Aria2 Manual](https://aria2.github.io/manual/en/html/) | 官方 | 5 | aria2 官方手册，多线程与续传 | v1.37.0 |
| 4 | [curl vs Wget（Daniel Stenberg）](https://daniel.haxx.se/docs/curl-vs-wget.html) | 教程 | 4 | curl 作者对比二者差异，选型参考 | unknown |
| 5 | [腾讯云：curl和wget到底该用哪个](https://cloud.tencent.com.cn/developer/article/2572636) | 教程 | 3 | 中文入门对比 curl/wget | unknown |

### 透镜 2：断点续传 / 并发 / 镜像 / 重试

| # | 来源 | 层级 | 分数 | 相关性 | 日期 |
|---|------|------|------|--------|------|
| 1 | [curl man page](https://curl.se/docs/manpage.html) | 官方 | 5 | `-C` 续传、`--retry` 重试权威参考 | 持续更新 |
| 2 | [aria2c(1) 官方手册](https://aria2.github.io/manual/en/html/aria2c.html) | 官方 | 5 | `-x`/`-s` 并发、镜像、重试参数权威 | 持续更新 |
| 3 | [GNU Wget Manual](https://www.gnu.org/software/wget/manual/) | 官方 | 5 | `-c` 续传、`-t` 重试、`-m` 镜像规范 | 1.21.x |
| 4 | [aria2 使用详解（CSDN）](https://blog.csdn.net/ymz641/article/details/148429226) | 教程 | 4 | 中文详解 aria2 并发/镜像/续传 | unknown |
| 5 | [阿里云：Linux wget 命令详解](https://developer.aliyun.com/article/1665900) | 教程 | 3 | 中文续传与重试参数组合 | unknown |

### 透镜 3：shell 批量下载脚本

| # | 来源 | 层级 | 分数 | 相关性 | 日期 |
|---|------|------|------|--------|------|
| 1 | [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html) | 官方 | 5 | for/while 循环与数组语法权威 | 持续更新 |
| 2 | [ShellCheck](https://github.com/koalaman/shellcheck) | 官方 | 5 | 静态检查工具，规避引号/循环陷阱 | 持续更新 |
| 3 | [curl man page](https://curl.se/docs/manpage.html) | 官方 | 4 | `--fail`/`-O`/批量 glob 与退出码 | 持续更新 |
| 4 | [DataCamp: Downloading Data on the Command Line](https://campus.datacamp.com/courses/data-processing-in-shell/downloading-data-on-the-command-line?ex=11) | 教程 | 3 | wget/curl 批量下载实操 | unknown |
| 5 | [php.cn: Linux 怎么批量下载文件](https://www.php.cn/faq/1823277.html) | 教程 | 3 | 中文批量下载脚本 for/while 示例 | unknown |

---

## 二、去重后唯一来源汇总

按规范 URL 去重后共 **12 个唯一来源**，层级分布：

- **官方（8）**：curl tutorial、curl man page、GNU Wget Manual、Aria2 Manual、aria2c(1)、GNU Bash Manual、ShellCheck
- **教程（4）**：curl vs Wget、腾讯云、CSDN aria2、阿里云 wget、DataCamp、php.cn → 实际教程 5（其中 2 篇中文入门）

> 注：php.cn 与 DataCamp 为入门教程，CSDN/腾讯云/阿里云为社区/厂商博客，用于标注操作性经验即可。

---

## 三、覆盖缺口（Coverage Gaps）

P1 探测未覆盖以下主题，P2 需要补充：

1. **校验和验证**（sha256sum / checksum 下载后校验）——意图文件中列为重点，尚无专属来源
2. **代理与 TLS 证书坑**（HTTP_PROXY 环境变量、`--insecure`、证书错误）——常见坑之一
3. **断点续传服务端前提**（HTTP Range 支持、服务端不支持时的行为）——仅在 man page 中隐式覆盖
4. **wget 官方手册**在透镜 3 未被搜索直接验证（透镜 1/2 已确认存在），P2 以 gnu.org 为准

---

## 四、方向菜单（请选择）

| 选项 | 方向 | 说明 | P2 预估深度 |
|------|------|------|------------|
| **A** | 命令工具基础与选型 | curl / wget / aria2 核心命令、参数、适用场景对比 | 中 |
| **B** | 下载可靠性进阶 | 断点续传、并发、镜像源、失败重试、校验 | 中高 |
| **C** | 批量下载脚本实战 | 用 .sh/.bash 组织多文件批量下载、循环、错误处理 | 高 |

> 可多选；P2 深度收集将围绕所选方向抓取 3–5 个核心来源并补齐覆盖缺口。
