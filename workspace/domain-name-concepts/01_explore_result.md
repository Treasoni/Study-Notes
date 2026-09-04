# 域名概念入门 - 探测结果汇总

> 阶段 1（P1）产出 · run `domain-name-concepts` · 2026-09-04
> 三个镜头各派 1 个并行 subagent 探测，按 canonical URL 去重后共 **11 条候选源**（官方文档 6 / 教程 3 / 一手 2）。

## 方向菜单（P1 → P2 用户选择点）

- **A（推荐）三线并进成短篇**：按「① 域名是什么与层级 → ② 一次 DNS 解析发生了什么 → ③ 记录类型与 TTL 速查」递进串成一篇 5–6 小节概念短篇（正文约 6000–9000 字）。三者是「是什么 → 怎么找 → 用什么控制」的关系，缺一不成篇。
- **B 只做 ① + ②**：砍掉记录速查，最纯粹的「看得懂」路线，约 4000–6000 字。
- **C 只做 ② + ③**：跳过域名层级细讲，偏「DNS 实用速查」，约 4500–6500 字。
- **D 三线并进 + 常见误区小节**：在 A 基础上，末节加「为什么我改了解析老不生效」小问答（承接 ③ 的 TTL/缓存），篇幅略增，更贴实战疑惑。

> 默认走 **A**。也可直接回复「按意图走」表示认可 A，我即进入 P2 深度收集。

## 源清单（去重汇总，11 条）

### 镜头 1：域名基础概念 —— 是什么 / 层级 / 与 IP 区别

| # | 源 | tier | 日期 | 分 | 一句话 |
|---|----|------|------|----|--------|
| 1 | [MDN · 什么是域名？（zh-CN）](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_domain_name) | 官方文档 | 2024 | 5 | 中文零基础；域名与 IP 区别、从右向左读、TLD/二级/子域、租用非购买 |
| 2 | [Cloudflare Learning · What is a domain name?](https://www.cloudflare.com/learning/dns/glossary/what-is-a-domain-name/) | 教程 | 常青 | 5 | 域名≠URL；用 google.co.uk 拆 TLD/2LD/3LD，图解适合零基础（有中文镜像） |
| 3 | [ICANN · About Domain Names](https://www.icann.org/resources/pages/about-domain-names-2018-08-30-en) | 官方文档 | 2018-08 | 4 | 权威；域名层级与逐级授权、TLD 分类、注册局/注册商角色（英文） |

### 镜头 2：DNS 解析过程 —— 输入网址到打开页面之间发生了什么

| # | 源 | tier | 日期 | 分 | 一句话 |
|---|----|------|------|----|--------|
| 4 | [Cloudflare-cn · 什么是 DNS？DNS 如何工作](https://www.cloudflare-cn.com/learning/dns/what-is-dns/) | 官方文档 | 常青 | 5 | 官网配图讲解析流程与缓存，四类服务器 + TTL 全程覆盖，零基础首选 |
| 5 | [Cloudflare-cn · 什么是递归 DNS？](https://www.cloudflare-cn.com/learning/dns/what-is-recursive-dns/) | 官方文档 | 常青 | 4 | 讲透递归解析器职责与缓存，正好承接「第二次更快」主线 |
| 6 | [DNSimple · What Is DNS?](https://support.dnsimple.com/articles/what-is-dns/) | 一手 | 常青 | 4 | 逐步解析链路清晰，关联 howdns.works 图解漫画，可视化强 |
| 7 | [腾讯云社区 · 7 张图详解域名系统 DNS](https://cloud.tencent.com.cn/developer/article/1985080) | 教程 | 常青 | 3 | 中文图解版，七张图串域名结构与解析过程，作配图参考 |

### 镜头 3：记录类型与 TTL —— 初学者速查

| # | 源 | tier | 日期 | 分 | 一句话 |
|---|----|------|------|----|--------|
| 8 | [Cloudflare Learning · What are DNS records?](https://www.cloudflare.com/learning/dns/dns-records/) | 教程 | 常青 | 5 | 逐条讲 A/AAAA/CNAME/MX/TXT/NS 用途与 TTL 缓存含义，最适合入门速查 |
| 9 | [IBM · 什么是 DNS 传播？（cn-zh）](https://www.ibm.com/cn-zh/think/topics/dns-propagation) | 一手 | 常青 | 4 | 用缓存与 TTL 通俗解释「改动后生效慢」，正对 TTL/生效时间目标 |
| 10 | [Google Cloud · DNS 记录概览](https://docs.cloud.google.com/dns/docs/records-overview) | 官方文档 | 常青 | 3 | 官方列出支持记录类型，并说明根域(apex)不能设 CNAME 的原因与 ALIAS 方案 |

### 跨镜头核心（覆盖全部三镜头）

| # | 源 | tier | 日期 | 分 | 一句话 |
|---|----|------|------|----|--------|
| 11 | [阿里云 · 云解析 DNS 基础概念](https://help.aliyun.com/zh/dns/basic-concepts-dns2-0) | 官方文档 | 常青 | 4 | 中文官方术语全集：分层/权威/递归/TTL/各记录类型，带 example.com 逐步示例 |

## 覆盖缺口（P2 视需要补 2–3 条）

1. **根服务器 → TLD → 权威的「层级树」中文图解**较缺：DNSimple/Cloudflare 有英文配图，中文通俗图解少 → 成文时自绘一张 ASCII/Mermaid 或复用腾讯云七图思路。
2. **浏览器 → 系统 → 路由器 → ISP 多层本地缓存优先级**需跨源整合（散在 Cloudflare 递归文与 IBM）。
3. **CNAME 根域限制的入门向绕过方案**（CNAME Flattening/ALIAS/HTTP 跳转）缺一条集中源 → 可用 Google Cloud 第 10 条 + 阿里云第 11 条覆盖，必要时补 1 条。
4. **中文域名/IDN（.中国、Punycode）**零基础材料不足 → 本短篇若提一句，用已发布《[[域名完全上手]]》第 1.7 节口径即可，不必新增源。

## P2 范围预估

- **主体深读 4 篇**：#1 MDN、#4 Cloudflare-cn what-is-dns、#8 Cloudflare dns-records、#11 阿里云基础概念（三镜头 + 术语全集一次覆盖）。
- **补充 3 篇**：#2 Cloudflare what-is-a-domain-name（层级拆解）、#5 Cloudflare 递归 DNS、#9 IBM DNS 传播（TTL/生效时间）。
- **直觉层 1 篇**：#7 腾讯云七图（只作配图参考，不引事实）。
- 其余（#3 ICANN、#6 DNSimple、#10 Google Cloud）作交叉校验/术语权威，按需取段。
