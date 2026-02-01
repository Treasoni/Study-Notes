---
tags:
  - linux
---

# 1. 先确认你用的是哪种网络管理方式（很重要）

在 Ubuntu 18.04+，**99% 都是 Netplan**。

执行一条命令看看：

```bash
ls /etc/netplan/
```

如果看到类似：

`00-installer-config.yaml 01-netcfg.yaml`

👉 **就是 Netplan，下面按这个来**

# 2. Netplan 修改网络（推荐 & 官方方式）

## 2.1  编辑配置文件

假设文件叫 `00-installer-config.yaml`（名字可能不同）

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```


## 2.2 静态 IP 配置示例（最常用）

假设：

>- 网卡名：`ens18`（你的可能是 `eth0`、`ens33`、`enp3s0` 等）
>- IP：`192.168.1.100`
>- 网关：`192.168.1.1`
>- DNS：`223.5.5.5`、`8.8.8.8`

```bash
network:
  version: 2
  renderer: networkd
  ethernets:
    ens18:
      dhcp4: no
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses:
          - 223.5.5.5
          - 8.8.8.8

```

> [!warning]

> ⚠️ 这是重点警告
- `yaml 对缩进极度敏感`（只能用空格，不能用 Tab）
- `/24` 不要忘
- 我们们输入的==-==和==数字==要隔一个空格
![](assets/linux如何修改网络信息/截屏2026-02-01%2018.45.35.png)

## 2.3应用配置

```bash
sudo netplan apply
```
