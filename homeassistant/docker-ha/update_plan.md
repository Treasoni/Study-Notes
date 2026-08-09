# 更新计划：04_HACS安装_Docker三种路径与国内加速.md

- 目标文件：`homeassistant/docker-ha/04_HACS安装_Docker三种路径与国内加速.md`
- 更新模式：patch-in-place（仅局部 patch，不重写全文）
- 更新日期：2026-08-08
- 触发原因：`get.hacs.vip` 一键安装脚本 443 拒连（用户实测），4.4 节代理域名可用性发生变化

## Stale Map

### 保留
- 4.1 全部（HACS 是什么 / Docker 版为何手动装，未过时）
- 4.2 全部（官方脚本 `get.hacs.xyz` 域名 2026-08-08 实测仍存活，6 步逻辑不变）
- 4.3 三条路径（逻辑不变；路径二/三示例用的是直连 GitHub，加速前缀统一在 4.4 讲）
- 4.4 大白话说明、高频坑警示（「代理域名可用性易变」已被本次事故验证，保留并加强）
- 本章小结、前后导航双链

### 需要更新
| 位置 | 现状 | 更新为 |
|------|------|--------|
| 4.4 第 1 条 | 推荐 `mirror.ghproxy.com`、`ghfast.top` 替代 | 两者均已失效；实测可用名单改为 `gh-proxy.com` / `ghproxy.net` |
| 4.4 第 2 条 | `get.hacs.vip` 标注「可用性待实测」 | 已确认失效（2026-08-08，443 拒连），标注勿用；补 Gitee 手动安装兜底 |
| 4.4 第 3 条 | 推荐 `ghapi.hacs.vip/api` | 已随 get.hacs.vip 一并失效，从推荐中移除；保留 `ghapi-cf.hacs.vip/api` 等 |
| 文末 | 无更新记录 | 追加 `## 更新记录` |

### 需要删除
- `get.hacs.vip` / `ghapi.hacs.vip` 作为「可行」方案的表述（改为「已失效，勿用」）

### 需要新增
- `ghproxy.net` 代理前缀
- Gitee 手动安装兜底路径（gitee.com/hacs-china，2026-08-08 实测存活）

## 验证记录（2026-08-08 实测）
| 域名 | 结果 |
|------|------|
| get.hacs.vip | 443 拒连（FAIL） |
| gh-proxy.com | 200，可拉 hacs.zip |
| ghproxy.net | 200，可拉 hacs.zip（2.0.5） |
| mirror.ghproxy.com | FAIL |
| ghfast.top | FAIL |
| ghapi.hacs.vip/api | FAIL（同基础设施） |
| gitee.com/hacs-china | 200 |
| get.hacs.xyz | 301（官方脚本存活） |
