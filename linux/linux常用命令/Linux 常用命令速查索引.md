---
title: Linux 常用命令速查索引
created: 2026-07-29
updated: 2026-07-29
tags: [linux, index, 目录]
status: completed
source_project: linux-commands
---

# Linux 常用命令速查索引

> 本索引将《Linux 常用命令实战手册》拆分为独立主题笔记，按需查阅。

---

## 基础操作

- [[linux常用命令/Linux 文件与目录操作]] — ls、cp、mv、rm、find、tar、通配符
- [[linux常用命令/Linux 文件内容查看与搜索]] — cat、less、head、tail、grep

## 文本处理

- [[linux常用命令/Linux 文本处理三剑客]] — sed、awk、cut、sort、uniq + 管道组合

## 系统管理

- [[linux常用命令/Linux 进程管理与系统监控]] — ps、top、systemctl、journalctl、nohup
- [[linux常用命令/Linux 定时任务与自动化]] — crontab、systemd-timer、at、anacron
- [[linux常用命令/Linux 系统信息与硬件管理]] — uname、lscpu、free、dmidecode、dmesg
- [[linux常用命令/Linux 日志管理]] — journalctl、rsyslog、logrotate
- [[linux常用命令/Linux 磁盘与存储管理]] — df、du、fdisk、mount、lsblk

## 网络

- [[linux常用命令/Linux 网络诊断与排障]] — ping、curl、ss、tcpdump、dig

## 远程管理

- [[linux常用命令/Linux 远程连接与文件传输]] — SSH、scp、rsync、sftp、端口转发

## 安全与维护

- [[linux常用命令/Linux 权限管理基础]] — chmod、chown、umask、SUID/SGID/Sticky
- [[linux常用命令/Linux 用户管理]] — useradd、passwd、sudo、用户组管理
- [[linux常用命令/Linux 软件包管理]] — apt、dnf、pacman

## 进阶

- [[linux常用命令/Linux Shell 实用技巧]] — 管道、重定向、别名、环境变量、一行命令

---

> 建议学习顺序：文件 → 搜索 → 三剑客 → 进程 → 网络 → 权限 → 磁盘 → 包管理 → Shell
