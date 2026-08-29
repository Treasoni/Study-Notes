## 第 6 章：Docker Desktop 的差异：macOS/Windows 挂载性能

在 macOS 或 Windows 上跑 Docker，bind mount 功能一切正常，但你会遇到一个怪现象：大量小文件读写时性能断崖式下跌。这一章讲清根因，并给出可落地的规避技巧。

### 性能根因：一切都在跨 VM 边界

Docker Desktop 的 Linux 容器跑在一台轻量 VM 内，宿主的 APFS/NTFS 文件系统必须经过虚拟文件系统桥接，每次文件操作都要跨 VM 边界往返。当项目里有成千上万个小文件（典型如 `node_modules`）时，单次操作的开销被无限放大，性能骤降；原生 Linux 没有这层桥接，所以没有此开销 [S10]。

> [!tip] 大白话
> 把跨 VM 读写想成「快递过海关」：大文件是一个集装箱，一次过检；几千个小文件是几千个小包裹，每个都要单独开箱。文件越小越碎，排队越久，整体性能就越难看。

### macOS：三种后端

| 后端 | 说明 |
|------|------|
| VirtioFS | Docker Desktop 4.22+ 默认，最快（比 gRPC-FUSE 快 2–5x） |
| gRPC-FUSE | 旧默认 |
| osxfs | legacy，最慢 |

新版本默认 VirtioFS，无需再手动切换旧后端 [S10]。

### Windows：WSL2 走 9P 协议

WSL2 后端固定走 9P 协议，没有后端可切换。关键结论：**代码放 WSL 文件系统内性能最好**；从 Windows 盘（如 `C:\`）bind 挂载会跨 9P 边界变慢 [S10]。

> [!tip] 大白话
> 把 WSL 文件系统想成「隔壁邻居」，Windows 盘想成「两条街外」。在邻居家干活随叫随到，跨街取文件就要多跑路。所以 Windows 上开发，项目先放进 WSL 里。

### Synchronized file shares（Mutagen）

官方提速方案：在 VM 内建一个 ext4 同步缓存，用 Mutagen 把宿主文件同步进去，容器读写走本地缓存，宣称 2–10x 提速。需 Pro/Team/Business 订阅（4.27+），可用 `.syncignore` 排除 `node_modules`/`.git`；不适用于 WSL、Windows 容器与 K8s hostPath [S10]。

### 社区规避技巧

- `node_modules`、`.git` 用命名卷隔离，绕开大量小文件跨 VM 的开销；
- macOS 只共享最小目录（默认 /Users、/Volumes、/private、/tmp 等），别整盘共享；
- 一致性 flag 可按需降级，例如 `-v /host:/app:delegated`（三档 `consistent`/`cached`/`delegated`，越靠后越宽松、越快）。

> [!tip] 大白话
> 「只共享最小目录」想成「只给访客会议室的钥匙，不把整栋楼的门禁都发出去」。共享范围越小，需要桥接的路径越少，越省事也越安全。

### 本章小结

- 根因是 VM 内桥接：小文件越多，跨 VM 边界的开销被放大得越厉害 [S10]。
- macOS 默认 VirtioFS 最快，gRPC-FUSE / osxfs 为旧后端 [S10]。
- WSL2 走 9P 协议，代码放 WSL 文件系统内性能最好 [S10]。
- 重度文件同步可上 Mutagen（Synchronized file shares，Pro+ 订阅）[S10]。
- 实战上：命名卷隔离依赖目录、只共享最小目录、一致性 flag 降级。

下一章将汇总选型、权限与安全规则，走查一个 Web 服务读写宿主目录的完整配置。
