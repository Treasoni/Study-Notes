# 域名概念入门 - 深度收集

> 阶段 2（P2）产出 · run `domain-name-concepts` · 2026-09-04
> 范围：方向 A「三线并进」——①域名是什么与层级 ②DNS 解析过程 ③记录类型与 TTL。
> 面向零基础概念短篇（约 6000–9000 字），本文档为写作素材地图，非最终笔记。

## 1. Scope

纯概念，不含：选购/注册商对比、ICP 备案、实名、HTTPS/反代/内网穿透（这些在《[[域名完全上手]]》已发布分册）。不写死精确步数、不写厂商独断宣传口径。

## 2. Source table

| ID | 源 | URL | tier | 角色 |
|----|----|-----|------|------|
| M | MDN · 什么是域名（zh-CN） | developer.mozilla.org/zh-CN/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_domain_name | 官方 | 单元1/2 主轴 |
| CFd | Cloudflare-cn · What is a domain name?（英文原页 403，用中文镜像） | cloudflare-cn.com/learning/dns/glossary/what-is-a-domain-name/ | 教程 | 域名分层/角色 补充 |
| IC | ICANN · About Domain Names | icann.org/resources/pages/about-domain-names-2018-08-30-en | 官方 | 权威交叉校验 |
| CF1 | Cloudflare-cn · 什么是 DNS？DNS 如何工作 | cloudflare-cn.com/learning/dns/what-is-dns/ | 官方 | 单元3/4 主轴 |
| CF2 | Cloudflare-cn · 什么是递归 DNS？ | cloudflare-cn.com/learning/dns/what-is-recursive-dns/ | 官方 | 递归器职责 |
| AL | 阿里云 · 云解析 DNS 基础概念 | help.aliyun.com/zh/dns/basic-concepts-dns2-0 | 官方 | 中文术语全集（解析+记录+TTL） |
| DS | DNSimple · What Is DNS? | support.dnsimple.com/articles/what-is-dns/ | 一手 | 步骤链图解参照 |
| gcp | Google Cloud · DNS 记录概览 | docs.cloud.google.com/dns/docs/records-overview | 官方 | 记录类型权威 |
| ibm | IBM · 什么是 DNS 传播？（cn-zh） | ibm.com/cn-zh/think/topics/dns-propagation | 一手 | TTL/生效 主轴 |
| — | Cloudflare · What are DNS records? | cloudflare.com/learning/dns/dns-records/ | 教程 | **不可抓取**（403 + JS 挑战），弃用；记录类型由 gcp+AL 全覆盖 |

## 3. Claim map（按写作单元）

### 单元 1｜域名基本概念与层级

- 域名是给人看、好记的文本地址；机器实际靠数字 IP（IPv4/IPv6）互访 [M, IC]
- 域名 ≠ URL ≠ 网站：URL 含协议+域名+路径；有域名仍须配服务器才有网站 [CFd, IC]
- 域名是点分隔的标签串，**从右向左读**，语义由笼统到具体 [M, CFd]
- 最右是顶级域名 TLD：.com/.org/.net 通用、.cn/.uk 国家地区、.gov/.edu 用途受限 [M]；CFd 作 gTLD/ccTLD 二分
- TLD 左侧=二级域名（主域），再左=子域；例 `www.google.co.uk` → uk(TLD)·co(2LD)·google(3LD) [CFd]
- 一个标签 1–63 字符，大小写不敏感，只含字母/数字/连字符且连字符不可在首尾 [M]
- 域名可自建子域分流（如 developer.mozilla.org）；不强制刚好三层 [M]
- **new gTLD（.xyz/.top 等）三源均未展开** → 仅可作「近年新增通用顶级」一句带过，或引 IANA 根库补 1 源；不建议展开

### 单元 2｜谁在管域名（并入单元1尾部或独立小节）

- 注册局（registry）管理 TLD 主数据库，把保留权委托给注册商；注册商面向个人/企业零售 [CFd]
- 注册人**只租不买**：按年租用、续期优先、从无所有权 [M, CFd]
- WHOIS 是公开登记册，可查可用性与归属；WHOIS 隐私可隐藏注册人联系信息 [M, CFd]

### 单元 3｜DNS 解析：输入网址 → 打开页面

- DNS = 把域名翻译成 IP 的分布式「电话簿」[CF1]
- 浏览器先问**递归解析器**（本地 DNS / ISP 分配或公共 DNS 如 223.5.5.5）；解析器替用户问到底，答后缓存 [CF1, CF2, AL, DS]
- 四类角色：递归解析器 → 根服务器 → TLD 服务器 → 权威服务器 [CF1]
- **根服务器只指路不存具体域名**：返回所查 TLD 的服务器地址 [CF1, AL, DS]
- **TLD 服务器**管主机名末段（如 .com），返回该域**权威服务器**地址 [CF1]
- **权威服务器是最后一站**：实际持有记录，仅凭自身数据应答 [CF1]
- 递归（代你问到底）vs 迭代（指路你自己问）；公共 DNS 对用户递归、对上游迭代 [CF2, AL, DS]
- 解析器视角对上游共问 **3 轮**（根→TLD→权威各一）；各源总步数口径 6/8/10 不一 → **正文写「问 3 次路」不写死步数** [CF1, AL, DS]
- 典型冷缓存流程：浏览器 → 解析器 → 根 → TLD → 权威 → 回浏览器 [CF1]

### 单元 4｜缓存与「第二次更快」

- 命中缓存 → 解析器直接回 IP，跳过对根/TLD/权威的全部查询 [CF1, AL]
- 缓存点常见于：浏览器、操作系统（存根解析器）、ISP 递归解析器 [CF1]
- 解析器加速捷径：缓存了 NS 记录就直接查权威；缓存了 TLD 记录就跳过根 [CF1]
- 路由器级缓存：CF1/AL/DS 未列；正文若提「部分路由器也会缓存」须标为实操提示（型号而定）

### 单元 5｜TTL 与「DNS 传播」真相

- TTL = 递归服务器/缓存允许保存该结果的最长时间，到期删除并重新查询 [AL, gcp, CF1]
- TTL 越小 → 记录修改后生效越快，但 DNS 查询频率越高 [AL]
- **「DNS 传播」是误解框架**：改记录后没有全球同步推送，而是各缓存按各自旧 TTL 过期、下次重查才拿到新值 [ibm]
- 生效窗口期内不同用户看到新/旧结果并存 [ibm]
- ISP 可能忽略 TTL、缓存更久，进一步拉长生效时间 [ibm]
- 实操建议（由机制推出的合理推论，写作须标「建议」而非事实）：改解析前先调低 TTL（如 60s）并等旧 TTL 过期，能缩短生效窗口

### 单元 6｜记录类型速查

- **A**：域名 → IPv4 地址（点分十进制）[gcp]
- **AAAA**：域名 → IPv6 地址（十六进制）[gcp]
- **CNAME**：指向另一域名的别名，可指向完全不同域名 [gcp]；**不能放根域（apex）**，也不能与同主机名其它记录共存 [gcp]；根域要「CNAME 效果」用 ALIAS/ANAME 类记录 [AL]
- **MX**：邮件路由，含优先级数字；数值越小优先级越高 [gcp, AL]
- **TXT**：任意文本记录（≤512 字符），常用于 SPF 反垃圾与所有权验证 [AL]
- **NS**：把子域委派给其它 DNS 服务器解析 [AL]

## 4. Contradictions & phrasing notes

1. **IP 措辞**：CF 中文 FAQ 称 IP 为「字母数字地址」（IPv6 含十六进制字母，IPv4 纯数字）；正文统一「数字 IP 地址」。
2. **步数口径**：CF1=8 步、DS=6 环节、AL=含 HTTP 10 步；非事实冲突，正文以「解析器向上游问 3 轮 + 每轮指路」叙述，避免精确步数。
3. **「传播」措辞**：ibm 沿用「传播时间」框架但其机制描述=逐缓存过期；正文直接点破「传播其实不是广播，是等缓存过期」，不必引入厂商「秒级」宣传。
4. **MX 优先级**：gcp 与 AL 一致（小者优先）；仅控制台显示范围（1–50）为平台差异，不写入。
5. **CNAME 根域限制**：gcp 明文禁止 + AL 的 ALIAS 反证，结论一致。

## 5. Coverage gaps & open questions

- **new gTLD** 无本批源展开：若写作需要例举 .xyz/.top，仅作 TLD 类别一句带过（不引事实），或补 IANA 根库。
- **路由器缓存**：无源逐条覆盖；写则标注为实操提示。
- **中文域名/IDN**：本短篇范围外，文末双链指向已发布的《[[域名完全上手]]》1.7 口径即可，不新增源。
- **DoH / 运营商缓存细节**：浅覆盖即可（CF2 提及缓存），零基础笔记不深入。

## 6. Practical guidance（写给下游 writer）

- 每个核心概念配 `[!tip] 大白话` + 一个类比。建议类比库：**电话簿**（域名↔IP 映射）、**快递/邮政地址**（层级：国家→城市→街道→门牌）、**问路**（根/TLD/权威逐级指路）、**便签缓存**（TTL=便签上写的有效期）。
- 单元 3 的链路用「逐步 + 缩进」文字版或简单有序列表串讲即可，Obsidian 中比 Mermaid 更稳（不依赖 vault 插件支持）。
- 单元 6 用速查表；每行给「大白话一句 + 典型用途」。
- 全程避免：精确步数、厂商「秒级生效」、new gTLD 事实断言。
- 文末给「读完后可以打开 [[域名完全上手]] 深入」的出口双链。

## 7. Downstream handoff

建议小节骨架（P3 再细化确认）：

```
1. 域名是什么：互联网的门牌号（与 IP/URL 的关系）
2. 域名长什么样：从右往左读的层级（TLD/二级/子域）
3. DNS 是什么：分布式的电话簿
4. 一次解析发生了什么：问 3 次路 + 缓存（含 TTL 初识与「第二次更快」）
5. 记录类型速查：A/AAAA/CNAME/MX/TXT/NS（+ CNAME 根域限制）
6. 改了解析多久生效：TTL 与「传播」真相 + 实用建议
```

素材量级：三线共约 40 条 claims、8 个源（9 抓取、1 弃用），足够支撑上述 6 小节零基础短篇。
