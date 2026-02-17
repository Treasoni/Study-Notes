---
tags: [pve]
---

# PVE 基础优化设置

> [!info] 概述
> PVE 安装完成后需要进行一些基础优化设置，包括软件源配置、订阅提示移除、CPU 性能模式调整等。
> 类比：就像买了新手机后需要设置应用商店、关闭更新提示、调整性能模式一样。

## 核心概念 💡
- **更新存储库（Repository）**：系统和组件的更新源
- **企业源 vs 非订阅源**：官方企业源需要订阅，个人用户用非订阅源
- **CPU 性能模式**：高性能（performance）vs 省电（powersave）

## 软件源设置

### 1.1 科学环境下源修改

这里主要改的是**更新存储库**中的内容（详见 [[PVE存储库]]）。

#### 禁用企业源和 Ceph 源

**编辑企业源文件**：
```bash
nano /etc/apt/sources.list.d/pve-enterprise.list
```
在行前加 `#` 注释掉：
```bash
#deb https://enterprise.proxmox.com/debian/pve bookworm enterprise
```

**编辑 Ceph 源文件**（如果不用 Ceph）：
```bash
nano /etc/apt/sources.list.d/ceph.list
```
在行前加 `#` 注释掉：
```bash
#deb https://enterprise.proxmox.com/debian/ceph-quincy bookworm enterprise
```

#### 添加非订阅 PVE 源

免费个人用户需要添加官方提供的非订阅源：

**传统格式（PVE 8 / Debian Bookworm）**：
```bash
echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list
```

**DEB822 格式（PVE 9 / Debian Trixie，推荐）**：
```bash
cat > /etc/apt/sources.list.d/pve-no-subscription.sources <<EOF
Types: deb
URIs: http://download.proxmox.com/debian/pve
Suites: bookworm
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
EOF
```

### 1.2 移除订阅提示

#### PVE 8.0

```bash
sed -i.backup -z "s/res === null || res === undefined || \!res || res\n\t\t\t.data.status.toLowerCase() \!== 'active'/false/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js && systemctl restart pveproxy.service
```

#### PVE 9.0（依次执行以下两条命令）

**第一条命令**：
```bash
cat <<'EOF' >/etc/apt/apt.conf.d/no-nag-script
DPkg::Post-Invoke { "dpkg -V proxmox-widget-toolkit | grep -q '/proxmoxlib\.js$'; if [ $? -eq 1 ]; then { echo 'Removing subscription nag from UI...'; sed -i '/.*data\.status.*active/{s/!//;s/active/NoMoreNagging/}' /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js; }; fi"; };
EOF
```

**第二条命令**：
```bash
apt --reinstall install proxmox-widget-toolkit && service pveproxy restart
```

### 1.3 直连网络更换国内源

如果无法访问官方源，可以使用国内镜像源。

#### 中科大源

地址：https://mirrors.ustc.edu.cn/proxmox/

**传统格式（PVE 8）**：
```bash
echo "deb https://mirrors.ustc.edu.cn/proxmox/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list
```

**DEB822 格式（PVE 9）**：
```bash
cat > /etc/apt/sources.list.d/pve-no-subscription.sources <<EOF
Types: deb
URIs: https://mirrors.ustc.edu.cn/proxmox/debian/pve
Suites: bookworm
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
EOF
```

详细说明：https://mirrors.ustc.edu.cn/help/proxmox.html

#### 清华源

地址：https://mirrors.tuna.tsinghua.edu.cn/help/proxmox

**传统格式**：
```bash
echo "deb https://mirrors.tuna.tsinghua.edu.cn/proxmox/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list
```

详细说明：https://mirrors.tuna.tsinghua.edu.cn/help/proxmox

#### CT Templates 源加速

将 CT Templates 下载源替换为国内镜像：

```bash
sed -i.bak 's|http://download.proxmox.com|https://mirrors.ustc.edu.cn/proxmox|g' /usr/share/perl5/PVE/APLInfo.pm
systemctl restart pvedaemon
```

## CPU 性能模式

### 2.1 安装必备工具

```bash
apt install linux-cpupower powertop -y
```

### 2.2 执行命令切换模式

#### 全核高性能

```bash
cpupower frequency-set -g performance
```

#### 全核省电

```bash
cpupower frequency-set -g powersave
```

#### 指定核心高性能（0-15 核心）

```bash
cpupower -c 0-15 frequency-set -g performance
```

### 2.3 查看当前模式

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

可能返回：
- `performance`（高性能）
- `powersave`（省电）

### 2.4 注意事项

> [!warning] 重要提示
> 切换全核省电模式后重启 PVE，会自动变回高性能模式，需要再次执行省电命令。

如果希望永久设置，可以：
1. 创建 systemd 服务
2. 添加到 `/etc/rc.local`
3. 使用 cron 任务

## 更新 PVE

### 3.1 命令行更新

```bash
apt update
apt dist-upgrade
```

### 3.2 Web 界面更新

1. 打开 PVE Web 界面
2. 选择节点 → Updates
3. 点击 `Refresh` 检查更新
4. 点击 `Upgrade` 执行更新

## 操作步骤总结

### 完整优化流程

1. **禁用企业源和 Ceph 源**
   ```bash
   nano /etc/apt/sources.list.d/pve-enterprise.list
   nano /etc/apt/sources.list.d/ceph.list
   ```

2. **添加非订阅源**
   ```bash
   echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list
   ```

3. **移除订阅提示**（根据 PVE 版本选择命令）

4. **更新软件源**
   ```bash
   apt update
   ```

5. **设置 CPU 性能模式**
   ```bash
   cpupower frequency-set -g performance
   ```

6. **执行系统更新**
   ```bash
   apt dist-upgrade
   ```

## 注意事项 ⚠️

1. **源文件修改前建议备份**
   ```bash
   cp /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources.list.d/pve-enterprise.list.bak
   ```

2. **更新前建议先测试**
   - 在测试环境验证源是否可用
   - 确认更新内容

3. **CPU 模式选择**
   - 服务器/高性能需求：performance
   - 家用/省电需求：powersave
   - 重启后需要重新设置

4. **订阅提示移除**
   - 更新 proxmox-widget-toolkit 后可能需要重新执行
   - 不同 PVE 版本命令不同

## 常见问题 ❓

**Q: 不禁用企业源会怎样？**
A: 会一直提示没有有效订阅，更新时会报错但不影响使用。

**Q: 非订阅源稳定吗？**
A: 官方提供的非订阅源是稳定的，只是更新可能比企业源稍激进。

**Q: CPU 性能模式哪个好？**
A: 服务器环境推荐 performance，家用环境推荐 powersave。

**Q: 如何永久设置 CPU 模式？**
A: 可以创建 systemd 服务或使用 cron 任务在启动时设置。

**Q: 更新后需要重启吗？**
A: 如果更新了内核，需要重启。其他更新通常不需要。

**Q: 国内源和官方源选哪个？**
A: 能访问官方源用官方源，访问慢或有问题用国内源。

## 相关文档

[[安装和使用PVE]] | [[PVE存储库]] | [[修改PVE的网络信息]] | [[PVE学习笔记MOC]]
