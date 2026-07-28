# Linux常用命令 - 探测式收集结果

收集时间: 2026-07-28
搜索维度: 4 个并行方向

---

## 探测结果总览

| # | 维度 | 核心命令 | 素材评分 | 
|---|------|---------|---------|
| 1 | 📄 文件操作与文本处理 | ls, cp, mv, grep, sed, awk, cut, sort | 5/5 |
| 2 | ⚙️ 系统管理与进程监控 | ps, top, htop, kill, systemctl, journalctl, nice, strace, nohup | 5/5 |
| 3 | 🌐 网络诊断与调试 | ping, curl, wget, ss, netstat, tcpdump, traceroute, nc, dig | 5/5 |
| 4 | 🔐 权限/磁盘/包管理 | chmod, chown, df, du, fdisk, mount, apt, dnf, yum, pacman | 5/5 |

---

## 各维度详情

### 1. 📄 文件操作与文本处理

**核心命令**: ls, cp, mv, rm, find, grep, sed, awk, cut, sort, wc, head, tail

**发现的高质量素材**:
- Linux 三剑客（grep/sed/awk）超实用操作示例 — 腾讯云教程（评分 5/5）
- grep/sed/awk 实战指南，含管道组合案例和 20+ 实战案例（评分 5/5）
- 5个必学文本处理工具，含 cut、sort 与三剑客串联使用（评分 4/5）

**关键要点**:
- grep 注重搜索过滤，sed 注重流式编辑替换，awk 注重结构化分析
- 命令组合 > 单一工具，管道组合是核心技能

---

### 2. ⚙️ 系统管理与进程监控

**核心命令**: ps, top, htop, kill, pkill, systemctl, journalctl, nice, renice, strace, nohup, bg, fg, jobs, cron

**发现的高质量素材**:
- ps/top/htop/kill/systemctl 中文教程，含进程状态码速查表（评分 5/5）
- 2026年更新完整指南，从进程管理到 systemd 服务单元（评分 5/5）
- 系统管理员参考手册，涵盖 journalctl、strace、df/du 等（评分 4/5）

**关键要点**:
- ps aux 组合用法、top 交互快捷键（P/M/k/r）
- systemctl 管理服务单元，journalctl 查看日志
- nohup/disown 后台任务管理

---

### 3. 🌐 网络诊断与调试

**核心命令**: ping, curl, wget, ss, netstat, tcpdump, traceroute, nc, dig, ip, ethtool

**发现的高质量素材**:
- 从 ping 到 tcpdump 的 12 个核心命令详解（评分 5/5）
- ip 替代 ifconfig、ss 替代 netstat 的迁移路径 + 生产排错案例（评分 5/5）
- OSI 分层工具链方法，自顶向下排错（评分 4/5）

**关键要点**:
- 新旧命令迁移：ip → ifconfig, ss → netstat, ip route → route
- 自顶向下排错法：应用层 → 传输层 → 网络层 → 链路层
- tcpdump 抓包分析、curl -w 性能分析

---

### 4. 🔐 权限/磁盘/包管理

**核心命令**: chmod, chown, chgrp, df, du, fdisk, mkfs, mount, umount, apt, dnf, yum, pacman

**发现的高质量素材**:
- chmod/chown/chgrp 实战详解 + 特殊权限 SUID/SGID/Sticky Bit（评分 5/5）
- df/du/fdisk 磁盘管理三件套 + mkfs/mount/fsck（评分 5/5）
- apt/yum/dnf 包管理全面解析 + 发行版对照表（评分 4/5）

**关键要点**:
- 数字权限（755/644）和符号模式（ugoa+-=rwx）
- df -h 查看整体磁盘、du -sh 定位大目录、fdisk 分区
- Debian 系用 apt、Red Hat 系用 dnf（yum 已淘汰）

---

## 推荐笔记方向

基于以上探测结果，建议将笔记按以下分类组织，覆盖日常开发运维最高频使用的命令：

| 方向 | 内容 | 优先级 |
|------|------|--------|
| A. 完整系统速查 | 涵盖以上所有 4 个维度的全面命令参考 | 全面参考 |
| B. 开发运维聚焦 | 偏重文本处理 + 系统管理 + 网络诊断，适合开发者 | 高效实战 |
| C. 基础入门向 | 文件操作 + 权限 + 简单系统管理，适合新手 | 轻量入门 |

---

## 已发现的素材

### 高评分素材（供深度收集参考）

| # | 标题 | URL | 评分 | 类型 |
|---|------|-----|------|------|
| 1 | Linux 三剑客超实用操作示例 | https://cloud.tencent.com.cn/developer/article/2490249 | 5/5 | 教程 |
| 2 | Linux进程管理完整指南(2026) | https://dargslan.com/blog/linux-process-management-monitoring-guide | 5/5 | 教程 |
| 3 | 网络故障排查12个核心命令 | https://blog.csdn.net/roruby/article/details/83070901 | 5/5 | 博客 |
| 4 | 权限/磁盘/包管理实战 | 多篇综合 | 5/5 | 多源 |
