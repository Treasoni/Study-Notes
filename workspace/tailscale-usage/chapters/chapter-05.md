## 进阶用法

前四章我们一直在把 Tailscale 当「开箱即用的内网穿透」工具：装上、登录、用名字访问，剩下的交给官方云。这一章回答一个更实际的问题——**当默认策略不够用，或者你想把控制权握在自己手里时，应该怎么配**。你会学到 Policy 文件的高级写法（tags / groups / 自动审批 / 自定义 DERP），以及 Headscale 自建控制面、自建 DERP、容器与 Kubernetes 集成的「能用级」配置。

### 5.1 Tailnet Policy 进阶

Policy 文件用 HuJSON（带注释的 JSON）书写。顶层除了你熟悉的 `acls`、`ssh` 分区，还有 `grants`、`groups`、`tagOwners`、`autoApprovers`、`derpMap` 等[^c5-1]。

**新一代访问控制：`grants`**
`grants` 是新一代访问控制，同时管网络层与应用层，默认 deny-by-default。官方会**无限期支持** `acls`，但不再给它加新特性，新配置推荐迁移到 `grants`。上手阶段知道「grants 是 ACL 的演进方向」即可，不必立刻重写现有规则。

**`groups`：用户分组**
带 `group:` 前缀的组，成员写完整邮箱，**不能嵌套**（组里不能再引用另一个组）；改动会自动传播到引用它的规则。适合把「运维」「开发」这类人员分组复用，避免在每条规则里重复列邮箱。

**`tagOwners`：设备身份标签**
tag 必须先定义在 `tagOwners` 里，才能被 ACL 引用——这跟第一章「服务器推荐用 tag 身份 + auth key 接入」呼应。owner 可以是邮箱、组、autogroup 或另一个 tag；写成 `[]` 简写等于 `autogroup:admin`，表示只有管理员能发这个 tag[^c5-1]。

> [!tip] 大白话：把 `tag:server` 想成发给服务器的**临时工牌**。工牌要先在 `tagOwners` 里登记「谁有权发」，设备戴上它才拥有对应身份。所以 ACL 里写 `tag:server` 之前，必须先定义好 `tagOwners`，否则 tag 不存在、规则无法引用。

**`autoApprovers`：路由自动审批**
第二章我们手动在 admin console 审批 subnet router 和 exit node；`autoApprovers` 可以把审批写进策略文件，`routes` 键管子网路由、`exitNode` 键管出口节点，并指定哪些人/组/tag 能被自动批准。

> [!warning] 易错点：`autoApprovers` 只对**首次广播**的路由生效，不追溯。设备如果后来被他人重新认证，会停止广播路由，已批准规则不会自动恢复。规避办法是给这类设备打 tag，让审批跟随 tag 而不是单个设备。

**网络选项：`derpMap` 与 `randomizeClientPort`**
`derpMap` 用于自定义或禁用默认 DERP（5.3 会用它接入自建中继）；`randomizeClientPort: true` 让客户端改用随机 UDP 端口，替代默认固定的 41641，可规避部分防火墙对固定端口的封禁[^c5-1]。

```jsonc
// policy.hujson —— 组合演示 groups / tagOwners / autoApprovers / derpMap / randomizeClientPort
{
  "groups": {
    "group:ops": ["alice@example.com", "bob@example.com"]
  },
  "tagOwners": {
    "tag:server": ["group:ops"],
    "tag:nas": []
  },
  "autoApprovers": {
    "routes": {
      "192.0.2.0/24": ["tag:server"],
      "198.51.100.0/24": ["tag:server"]
    },
    "exitNode": ["group:ops"]
  },
  "derpMap": {
    "OmitDefaultRegions": true,
    "Regions": {
      "900": {
        "RegionID": 900,
        "RegionCode": "mydc",
        "RegionName": "My Data Center",
        "Nodes": [
          { "Name": "mydc1", "RegionID": 900, "HostName": "derp.example.com" }
        ]
      }
    }
  },
  "randomizeClientPort": true
}
```

### 5.2 Headscale：自建控制面

Tailscale 除各 GUI 客户端和控制服务器外基本全开源。**Headscale 就是那个「控制服务器」的自托管替代品**[^c5-2]。

**它做什么、不做什么**
控制面只负责四件事：交换 WireGuard 公钥、分配 `100.x.y.z` IP、维护用户边界、暴露路由；**数据面仍走节点间的 WireGuard**——即使换成 Headscale，设备之间的流量依然是端到端加密的 P2P，不经过控制面。Headscale 的设计目标是**窄范围的单一 tailnet**，面向个人或小型开源组织[^c5-2]。

> [!tip] 大白话：把控制面想成酒店前台：它只负责登记住客（交换公钥）、分配房号（IP）、确认身份（用户边界）；住客之间的行李搬运仍是点对点完成的。所以 Headscale 只替换「前台」，不介入也不影响你的实际数据流量。

**部署注意**
官方不支持也不鼓励把 Headscale 放在反向代理后面，或用容器部署；文档分 stable / development 两版，**必须按发布版本选对应的 GitHub tag**，不要直接拉 master。具体部署细节以 headscale.net/stable 为准——README 不含自定义 DERP 的接入细节[^c5-2]。

```bash
# 创建用户（对应 tailnet 里的身份边界）
headscale users create myuser
# 注册节点：把客户端登录时生成的 node key 绑定到该用户
headscale nodes register --user myuser --key nodekey:xxxxx
```

### 5.3 自建 DERP

DERP 是直连失败且没有 Peer Relay 时的**回退中继**（第四章已讲它如何兜底）。注意：**DERP 目前是 alpha 阶段**，大多数情况用官方默认就够，自建只为合规或降低延迟[^c5-3]。

> [!tip] 大白话：把 DERP 想成小区门口的中转驿站：两家直连不上时，包裹先经驿站中转，但驿站不拆看内容（中继流量仍端到端加密）。所以只有打洞失败才用得上它，多数场景无需自建。带宽与性能影响可参考 [[内网穿透带宽性能分析]]。

**硬性要求**
DERP 靠**源 IP**识别设备，客户端用 HTTP upgrade 建双向通道，所以它必须**直连公网**——不能放在 NAT 或负载均衡后面；需要开放 443（HTTPS/HTTP）与 3478（STUN），并允许 ICMP[^c5-3]。

> [!warning] 易错点：DERP 不能放 NAT / 负载均衡后面。云厂商的 LB 大多不支持 HTTP upgrade 的双向通道，源 IP 也会被改写，导致客户端认不出彼此。硬性要求是 443 + 3478 放通、允许 ICMP。

**部署与接入**

```bash
# 编译安装 derper（需要 Go 环境）
go install tailscale.com/cmd/derper@latest
# 启动：域名要指向这台公网服务器
sudo derper --hostname=example.com
```

在 policy 的 `derpMap` 里声明自己的 region。**region ID 900–999 保留给自定义**；每个 region 放一个 server，想要冗余就配多个 region[^c5-3]。

```jsonc
{
  "derpMap": {
    "OmitDefaultRegions": true,
    "Regions": {
      "900": {
        "RegionID": 900,
        "RegionCode": "mydc",
        "RegionName": "My Data Center",
        "Nodes": [
          { "Name": "mydc1", "RegionID": 900, "HostName": "derp.example.com" }
        ]
      }
    }
  }
}
```

**防蹭与监控**
自建 DERP 默认对所有人开放，可能被当成免费中继。加 `--verify-clients` 可要求客户端在本机跑 tailscaled 校验身份；同仓库还提供 `cmd/derpprobe`，可周期性探测 DERP 的可用性[^c5-3]。

```bash
# 防蹭：只服务本机 tailscaled 认证过的客户端
sudo derper --hostname=example.com --verify-clients
```

### 5.4 容器与 Kubernetes

Tailscale 官方支持在容器和 K8s 里运行，形态分四种：**operator / sidecar / proxy / subnet router**，用途覆盖 Service 入口（ingress）、tailnet 出站（egress）、安全访问 kube-apiserver[^c5-4]。

**认证**：容器里用 auth key 认证——一次性（ephemeral）或可复用（reusable），存到 K8s Secret `TS_AUTHKEY`；如果没配 key，也能从容器日志里拿到登录 URL 完成认证。ephemeral 节点关机后自动从 tailnet 移除[^c5-4]。

**Subnet router**：跟第二章节的步骤一致，只是改用环境变量 `TS_ROUTES` 声明要广播的网段，例如 `TS_ROUTES=10.20.0.0/16,10.42.0.0/15`，然后在 admin console 启用、客户端 `--accept-routes`[^c5-4][^c5-5]。

```yaml
# K8s 部署 tailscale 时注入的环境变量（以 sidecar / subnet router 为例）
env:
  - name: TS_AUTHKEY
    valueFrom:
      secretKeyRef:
        name: tailscale-auth
        key: TS_AUTHKEY
  - name: TS_ROUTES
    value: "10.20.0.0/16,10.42.0.0/15"
  - name: TS_ACCEPT_DNS
    value: "true"
```

> [!warning] 易错点：容器默认没有 DNS 解析（不继承宿主机配置），所以 MagicDNS 在容器里默认不生效。需要 MagicDNS 时，必须显式设 `TS_ACCEPT_DNS=true`，否则只能用 IP 访问其他设备。

### 本章小结

- `grants` 是新一代访问控制（deny-by-default），`acls` 无限期支持但推荐新配置迁移；`groups` 不能嵌套，tag 必须先定义在 `tagOwners` 才能被 ACL 引用。
- `autoApprovers` 只对首次广播的路由生效，重认证会停播；`randomizeClientPort` 用随机端口替代固定 UDP 41641。
- Headscale 自托管控制面只替换「前台」，数据面仍走节点间 WireGuard；不鼓励反代/容器部署，必须按发布版本选 GitHub tag。
- 自建 DERP 处于 alpha，必须直连公网（不能 NAT/LB）、开放 443+3478；region ID 900–999 留给自定义，`--verify-clients` 防蹭、`cmd/derpprobe` 监控。
- 容器/K8s 有四种形态，auth key 放 Secret `TS_AUTHKEY`，subnet router 用 `TS_ROUTES`；容器默认无 DNS，MagicDNS 需 `TS_ACCEPT_DNS=true`。

到这里，五章正文全部完成。下一步会把全部分章节拼成一篇完整的《Tailscale 使用教程》，统一标题层级、检查引用，并做 Obsidian 美化发布。

## 参考来源

[^c5-1]: Tailnet policy file 语法 — <https://tailscale.com/docs/reference/syntax/policy-file>（S07）
[^c5-2]: Headscale GitHub 仓库 — <https://github.com/juanfont/headscale>（S09）
[^c5-3]: 自定义 DERP 服务器 — <https://tailscale.com/docs/reference/derp-servers/custom-derp-servers>（S10）
[^c5-4]: Tailscale on Kubernetes — <https://tailscale.com/docs/kubernetes>（S16）
[^c5-5]: Tailscale CLI 参考 — <https://tailscale.com/docs/reference/tailscale-cli>（S02）
