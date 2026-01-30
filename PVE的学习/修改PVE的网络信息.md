#  1.方法一（官方推荐）：**用 PVE Web UI 改**

这是 **最稳**、**不会被回滚** 的方式。

## 1.1操作步骤：

**1️⃣ 打开 PVE Web**

`https://192.168.2.10:8006`

2️⃣ 进入  
**节点 → System → Network**

3️⃣ 找到 `vmbr0`

4️⃣ 点 **Edit**

填成这样（示例）：

|项目|值|
|---|---|
|IPv4|Static|
|Address|`192.168.2.10/24`|
|Gateway|`192.168.2.1`|
|Bridge ports|`enpXsY`（你真实网卡）|

> ⚠️ **不要乱填网卡名**，从列表里选

5️⃣ 点 **Apply Configuration**