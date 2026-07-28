---
title: "Linux 系统信息与硬件管理"
created: 2026-07-29
updated: 2026-07-29
tags: [linux, 系统信息, 硬件, 内核]
status: completed
source_project: linux-commands
---

> [!note]
> 排查问题、配置系统、申请资源时，快速获取系统信息是基本功。从内核版本到 CPU 架构，从内存大小到磁盘硬件信息，本章整理所有常用的系统查询命令，帮你一眼看透机器的软硬件全貌。

---

## 1. 系统基本信息

### 1.1 内核与发行版

```bash
# 查看内核版本
uname -r
# 6.8.0-35-generic

# 查看内核完整信息
uname -a
# Linux host-server 6.8.0-35-generic #35~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon May 20 17:40:50 UTC 2 x86_64 x86_64 x86_64 GNU/Linux

# 查看发行版信息
cat /etc/os-release
# PRETTY_NAME="Ubuntu 22.04.4 LTS"
# NAME="Ubuntu"
# VERSION_ID="22.04"
# VERSION="22.04.4 LTS (Jammy Jellyfish)"
# ...

lsb_release -a
# No LSB modules are available.
# Distributor ID: Ubuntu
# Description:    Ubuntu 22.04.4 LTS
# Release:        22.04
# Codename:       jammy

# 查看主机名
hostname
# host-server

# 查看完整主机名（含域名）
hostname -f
# host-server.example.com

# 设置主机名
sudo hostnamectl set-hostname web-server-01
```

### 1.2 系统启动与运行时间

```bash
# 查看系统运行时间
uptime
# 09:30:01 up 15 days,  2:15,  2 users,  load average: 0.08, 0.03, 0.01
#   ↑ 当前时间 ↑ 运行时长     ↑ 在线用户   ↑ 1/5/15 分钟平均负载

# 查看上次启动时间
who -b
# system boot  2026-07-14 07:15

# 查看系统启动日志
journalctl --list-boots
# -5 5b8a...  Mon 2026-07-14 07:15:01 CST—Tue 2026-07-14 10:30:01 CST
# -4 1a2b...  Wed 2026-07-15 07:15:01 CST—Thu 2026-07-16 18:00:01 CST
#  0 e3f4...  Mon 2026-07-14 07:15:01 CST—still running
```

> [!tip]
> `uptime` 显示的 **load average**（平均负载）解读：
> - 理想值 < CPU 核心数（如 4 核机器 load < 4）
> - load > 核心数说明有进程在排队，需要关注
> - 看趋势：`uptime` 多看几次，判断负载在上升还是下降

---

## 2. CPU 信息

```bash
# 查看 CPU 概要
lscpu
# Architecture:             x86_64
# CPU op-mode(s):           32-bit, 64-bit
# Address sizes:            48 bits physical, 48 bits virtual
# Byte Order:               Little Endian
# CPU(s):                   8
# On-line CPU(s) list:      0-7
# Vendor ID:                GenuineIntel
# Model name:               Intel(R) Core(TM) i7-10700 CPU @ 2.90GHz
# CPU family:               6
# Model:                    165
# Thread(s) per core:       2
# Core(s) per socket:       4
# Socket(s):                1
# Stepping:                 5
# CPU max MHz:              4800.0000
# CPU min MHz:              800.0000
# Virtualization:           VT-x
# L1d cache:                128 KiB
# L1i cache:                128 KiB
# L2 cache:                 1 MiB
# L3 cache:                 16 MiB

# 查看 /proc/cpuinfo（原始数据）
cat /proc/cpuinfo | grep "model name" | uniq
cat /proc/cpuinfo | grep "cpu cores" | uniq

# 查看 CPU 当前频率
watch -n 1 "cat /proc/cpuinfo | grep 'cpu MHz'"

# 查看 CPU 架构
arch
# x86_64

# 查看 CPU 是否支持虚拟化
grep -E 'vmx|svm' /proc/cpuinfo
# vmx  → Intel VT-x
# svm  → AMD-V
```

> [!tip]
> `lscpu` 输出快速解读：
>
> | 字段 | 含义 | 计算示例 |
> |------|------|---------|
> | Socket(s) | 物理 CPU 颗数 | 1 |
> | Core(s) per socket | 每颗 CPU 的物理核心数 | 4 |
> | Thread(s) per core | 每核心的线程数（超线程） | 2 |
> | **CPU(s)** | **逻辑 CPU 总数** | **1 × 4 × 2 = 8** |

---

## 3. 内存信息

```bash
# 查看内存容量和使用情况
free -h
#               total        used        free      shared  buff/cache   available
# Mem:            31Gi        12Gi       5.2Gi       1.2Gi        14Gi        18Gi
# Swap:          2.0Gi       256Mi       1.7Gi

# 查看详细信息
free -h -t
# 会在末尾添加 Total 行，包含 Swap

# 以 MB 为单位（脚本友好）
free -m

# 查看原始内存信息
cat /proc/meminfo | head -20
# MemTotal:       32456784 kB
# MemFree:         5421056 kB
# MemAvailable:   18765432 kB
# Buffers:         1234567 kB
# Cached:         12345678 kB
# SwapTotal:      2097152 kB
# SwapFree:       1782579 kB

# 查看内存硬件信息（需要 root）
sudo dmidecode -t memory | grep -E "Size|Type|Speed|Manufacturer"
# Size: 16 GB
# Type: DDR4
# Type Detail: Synchronous
# Speed: 3200 MT/s
# Manufacturer: Kingston
# ...
```

> [!tip]
> `free -h` 关键解读：
> - **total**：物理内存总量（不含 Swap）
> - **available**：**真正可用的内存**（包括可回收的缓存），这是最关心的值
> - **used** 不等于 total - free，因为 buff/cache 在需要时可以回收
> - 关注 available，不是 free。available 快归零时才是内存紧张

```bash
# 查看内存占用 Top 10
ps aux --sort=-%mem | head -11

# 查看进程实际使用的物理内存（RSS）
ps -eo pid,ppid,cmd,%mem,%cpu,rss --sort=-rss | head -10

# 查看内存映射
sudo cat /proc/1/maps | head -10
```

---

## 4. 磁盘信息

```bash
# 查看磁盘使用情况
df -h
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1       468G  120G  348G  26% /
# /dev/sdb1       1.8T  800G  1.0T  45% /data

# 查看磁盘硬件信息（设备型号、序列号）
sudo fdisk -l | grep "Disk /dev"
sudo blkid

# 查看磁盘设备详细信息
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE,MODEL
# NAME    SIZE TYPE MOUNTPOINT FSTYPE MODEL
# sda   476.9G disk                    WDC WDS512G
# ├─sda1   512M part /boot     ext4
# └─sda2 476.4G part /         ext4
# sdb     1.8T disk                    ST2000DM008
# └─sdb1   1.8T part /data     ext4

# 查看磁盘 I/O 统计
sudo iostat -x 1 5
# 每 1 秒输出一次，共 5 次

# 查看磁盘挂载参数
mount | grep /data
# /dev/sdb1 on /data type ext4 (rw,relatime,errors=remount-ro)

# 查看磁盘 UUID
blkid /dev/sda2
# /dev/sda2: UUID="a1b2c3d4-..." TYPE="ext4"
```

> [!tip]
> `iostat -x` 关键指标：
> - **%util**：磁盘忙时间占比（100% = 满负荷）
> - **await**：I/O 请求平均等待时间（ms），数值高说明磁盘瓶颈
> - **r_await / w_await**：读写分别的等待时间
> - **svctm**：服务时间（现代磁盘此值不可靠，多参考 await）

---

## 5. 硬件详细信息

### 5.1 dmidecode — 全面硬件信息

```bash
# 查看 BIOS 信息
sudo dmidecode -t bios
# BIOS Information
#     Vendor: American Megatrends Inc.
#     Version: 1.2.3
#     Release Date: 01/15/2024

# 查看系统信息（厂商、型号、序列号）
sudo dmidecode -t system
# Manufacturer: Dell Inc.
# Product Name: PowerEdge R750
# Serial Number: ABC123...

# 查看主板信息
sudo dmidecode -t baseboard

# 查看 CPU 硬件信息
sudo dmidecode -t processor

# 查看内存硬件
sudo dmidecode -t memory

# 查看所有硬件信息
sudo dmidecode
```

### 5.2 lspci — PCI 设备列表

```bash
# 列出所有 PCI 设备
lspci
# 00:00.0 Host bridge: Intel Corporation Device 9b53
# 00:02.0 VGA compatible controller: Intel Corporation UHD Graphics 630
# 00:14.0 USB controller: Intel Corporation Cannon Lake PCH USB 3.1 xHCI
# 00:1f.6 Ethernet controller: Intel Corporation I219-V

# 显示详细信息
lspci -v

# 显示设备厂商和型号（更易读）
lspci -vmm

# 按设备类型过滤
lspci | grep -i ethernet
lspci | grep -i vga
lspci | grep -i nvme

# 查看 USB 设备
lsusb
# Bus 001 Device 002: ID 8087:0026 Intel Corp. Integrated Camera
# Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

### 5.3 其他硬件工具

```bash
# 查看块设备（磁盘、分区）
lsblk

# 查看 SCSI/SATA 设备
sudo lsscsi

# 查看 DMI 信息
sudo dmidecode -s system-manufacturer
sudo dmidecode -s system-product-name
sudo dmidecode -s system-serial-number

# 查看硬件摘要（需安装）
sudo lshw -short
# H/W path        Device      Class          Description
# =====================================================
#                             system         PowerEdge R750
# /0/0                        processor      Intel Xeon Gold 6338
# /0/1/0                      memory         64 GiB DDR4
# /0/100/1c.0    eno1        network        Ethernet Controller I219-V

# 查看网卡信息
lspci | grep -i ethernet
ip link show
ethtool eno1
```

> [!tip]
> **硬件排查速查：**
> - 服务器型号：`sudo dmidecode -t system | grep "Product Name"`
> - 内存规格：`sudo dmidecode -t memory | grep -E "Size|Type|Speed"`
> - 网卡型号：`lspci | grep Ethernet`
> - 显卡型号：`lspci | grep VGA`
> - 硬盘型号：`lsblk -o NAME,MODEL,SIZE`
> - 固件版本：`sudo dmidecode -t bios | grep Version`

---

## 6. 内核与模块管理

### 6.1 内核参数

```bash
# 查看内核参数
sysctl -a | head -20

# 查看单个参数
sysctl net.ipv4.ip_forward
# net.ipv4.ip_forward = 0

# 查看内核模块
lsmod | head -20

# 查看模块详细信息
modinfo nf_conntrack
# filename:       /lib/modules/6.8.0-35-generic/kernel/net/netfilter/nf_conntrack.ko
# license:        GPL
# depends:        nf_defrag_ipv6,nf_defrag_ipv4
# parm:           hashsize:int

# 加载 / 卸载模块
sudo modprobe nf_conntrack
sudo modprobe -r nf_conntrack
```

### 6.2 内核日志

```bash
# 查看内核日志
dmesg | tail -20

# 查看硬件识别日志（硬盘、网卡等）
dmesg | grep -i "sda\|nvme\|eth"

# 跟踪实时内核日志
dmesg -w

# 查看特定级别的内核日志
dmesg --level=err,warn

# 查看上次关机原因
journalctl -k | grep -i "shutdown\|poweroff"
```

> [!tip]
> `dmesg` 是硬件排查第一站：
> - 新加磁盘不识别 → `dmesg | tail`
> - 网卡掉线 → `dmesg | grep -i eth`
> - 硬件报错 → `dmesg --level=err`
> - USB 设备不识别 → `dmesg | grep -i usb`

---

## 7. 时间管理

```bash
# 查看系统时间和时区
timedatectl
#                Local time: Wed 2026-07-29 09:30:01 CST
#            Universal time: Wed 2026-07-29 01:30:01 UTC
#                  RTC time: Wed 2026-07-29 01:30:00
#                 Time zone: Asia/Shanghai (CST, +0800)
# System clock synchronized: yes
#               NTP service: active
#           RTC in local TZ: no

# 设置时区
sudo timedatectl set-timezone Asia/Shanghai

# 列出可用时区
timedatectl list-timezones | grep Asia

# 手动设置时间
sudo timedatectl set-time "2026-07-29 09:30:00"

# 启用 NTP 自动同步
sudo timedatectl set-ntp yes

# 查看日历
cal
#      七月 2026
# 日 一 二 三 四 五 六
#           1  2  3  4
#  5  6  7  8  9 10 11
# ...

# 查看日历（含周数）
ncal -w
```

---

> [!summary]
> **核心命令速查：**
>
> | 操作 | 命令 |
> |------|------|
> | 内核版本 | `uname -r` |
> | 发行版信息 | `cat /etc/os-release` |
> | 运行时间 | `uptime` |
> | CPU 信息 | `lscpu` / `cat /proc/cpuinfo` |
> | 内存使用 | `free -h` / `cat /proc/meminfo` |
> | 磁盘使用 | `df -h` / `lsblk` |
> | 磁盘 I/O | `sudo iostat -x 1` |
> | 硬件信息 | `sudo dmidecode -t system` |
> | PCI 设备 | `lspci` |
> | USB 设备 | `lsusb` |
> | 内核日志 | `dmesg \| tail` |
> | 内核参数 | `sysctl -a` |
> | 时间与时区 | `timedatectl` |
