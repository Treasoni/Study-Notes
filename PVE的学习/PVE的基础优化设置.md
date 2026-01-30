
# 1. 软件源设置（debian 源、PVE 源、企业源、ceph 源）

## 1.1科学环境下源修改
这里我主要改的是==**更新存储库**==中的内容：（看[PVE存储库](PVE存储库.md)）
![3000](assets/PVE的基础优化设置/截屏2026-01-30%2022.30.12.png)
### 禁用企业源和 Ceph 源
将文件中的内容注释掉（在行前加 `#`）

```bash
nano /etc/apt/sources.list.d/pve-enterprise.list
```

```bash
nano /etc/apt/sources.list.d/ceph.list
```

然后执行命令添加非订阅 PVE 源（默认为官方订阅源，免费个人用户需要官方提供的非订阅源才可正常更新 PVE）：
```bash
echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list
```
### 移除订阅提示
**pve8.0：**
```bash
sed -i.backup -z "s/res === null || res === undefined || \!res || res\n\t\t\t.data.status.toLowerCase() \!== 'active'/false/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js && systemctl restart pveproxy.service
```

**pve9.0（依次执行以下两条命令）：**

```bash
cat <<'EOF' >/etc/apt/apt.conf.d/no-nag-script
DPkg::Post-Invoke { "dpkg -V proxmox-widget-toolkit | grep -q '/proxmoxlib\.js$'; if [ $? -eq 1 ]; then { echo 'Removing subscription nag from UI...'; sed -i '/.*data\.status.*active/{s/!//;s/active/NoMoreNagging/}' /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js; }; fi"; };
EOF  `
```

```bash
apt --reinstall install proxmox-widget-toolkit && service pveproxy restart
```
## 2.2 直连网络更换国内源
这个用于更新PVE源和debian源：
中科大源：

[https://mirrors.ustc.edu.cn/help/proxmox.html](https://mirrors.ustc.edu.cn/help/proxmox.html)

清华源：

[https://mirrors.tuna.tsinghua.edu.cn/help/proxmox](https://mirrors.tuna.tsinghua.edu.cn/help/proxmox)
# 3.更新 PVE
用命令：
```bash
apt update
apt dist-upgrade
```
或是直接在更新选项中搞：
![](assets/PVE的基础优化设置/截屏2026-01-30%2022.43.36.png)
# 4. 开启CPU节能模式

## 4.1 **安装必备工具**

```
apt install linux-cpupower powertop -y
```

## 4.2执行以下命令开启高性能或者省电模式

**全核高性能**

```bash
cpupower  frequency-set -g performance
```

**全核省电**

```bash
cpupower  frequency-set -g powersave
```

**0-16 开启高性能**

```bash
cpupower -c 0-15  frequency-set -g  performance
```

切换全核省点模式后重启PVE会自动变回高性能模式，需要再次执行省电命令即可！