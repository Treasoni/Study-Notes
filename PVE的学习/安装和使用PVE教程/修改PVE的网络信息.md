#  1.方法一（官方推荐）：**用 PVE Web UI 改**

这是 **最稳**、**不会被回滚** 的方式。

## 1.1操作步骤：

**1️⃣ 打开 PVE Web**

`https://192.168.2.10:8006`

**2️⃣ 进入**  
**节点 → System → Network**

**3️⃣ 找到 `vmbr0`**

**4️⃣ 点 Edit**

填成这样（示例）：

![4000](assets/修改PVE的网络信息/file-20260203173647080.png)
> ⚠️ **不要乱填网卡名**，从列表里选

5️⃣ 点 **Apply Configuration**或**重启**PVE

# 2. 方法二：用命令行修改

## 2.1 操作步骤
### **①确认真实网卡名**

`ip link`

你会看到类似：

`enp3s0 ens18 eno1`

👉 用**真实存在的那个**

### ② 改文件（示例）

```bash
nano /etc/network/interfaces
```

```bash
auto lo
iface lo inet loopback

auto enp3s0
iface enp3s0 inet manual

auto vmbr0
iface vmbr0 inet static
    address 192.168.2.10/24
    gateway 192.168.2.1
    bridge-ports enp3s0
    bridge-stp off
    bridge-fd 0

```


### ③ ⚠️ 关键一步（你现在大概率漏了）

`ifreload -a`

或（老版本）：

`systemctl restart networking`

📌 **只 reboot 很多时候是不生效的**
> [!warning]

> ⚠️ 即使我们进行了修改但是我们重启后显示屏显示的还是最初我们进行设置的地址，但是==实际上已经改了==

