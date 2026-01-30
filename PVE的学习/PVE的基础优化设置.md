
# 1. 软件源设置（debian 源、PVE 源、企业源、ceph 源）

## 1.1科学环境下源修改
这里我主要改的是存储库中的内容：
![3000](assets/PVE的基础优化设置/截屏2026-01-30%2022.30.12.png)
禁用企业源和 Ceph 源，将文件中的内容注释掉（在行前加 `#`）

bash

Copy`nano /etc/apt/sources.list.d/pve-enterprise.list`

bash

Copy`nano /etc/apt/sources.list.d/ceph.list`

然后执行命令添加非订阅 PVE 源（默认为官方订阅源，免费个人用户需要官方提供的非订阅源才可正常更新 PVE）：

bash

Copy`echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list`

移除订阅提示pve8.0：

bash

Copy`sed -i.backup -z "s/res === null || res === undefined || \!res || res\n\t\t\t.data.status.toLowerCase() \!== 'active'/false/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js && systemctl restart pveproxy.service`

移除订阅提示pve9.0（依次执行以下两条命令）：

bash

Copy`   |   |   | |---|---| ||cat <<'EOF' >/etc/apt/apt.conf.d/no-nag-script| ||DPkg::Post-Invoke { "dpkg -V proxmox-widget-toolkit \| grep -q '/proxmoxlib\.js$'; if [ $? -eq 1 ]; then { echo 'Removing subscription nag from UI...'; sed -i '/.*data\.status.*active/{s/!//;s/active/NoMoreNagging/}' /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js; }; fi"; };| ||EOF|   `

sql

Copy`apt --reinstall install proxmox-widget-toolkit && service pveproxy restart`