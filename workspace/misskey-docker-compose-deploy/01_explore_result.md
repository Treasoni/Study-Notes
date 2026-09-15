# 使用 Docker Compose 部署 Misskey - P1 探测结果

- **项目标识**: `misskey-docker-compose-deploy`
- **阶段**: P1（探测式收集）
- **检索日期**: 2026-09-15
- **探测视角**: 3 个（官方部署文档 / 上游仓库工件与发布说明 / NAS 与自建实战排错）

> 本文件只记录探测到的候选来源与方向判断，不含正文抄录。所有结论待 P2 精读回源确认。

---

## 一、来源表（按 canonical URL 去重）

| ID | 来源 | 层级 | 日期 | 评分 |
| --- | --- | --- | --- | --- |
| S1 | [Misskey Hub - Building Misskey using Docker Compose](https://misskey-hub.net/en/docs/for-admin/install/guides/docker/) | official | unknown | 5 |
| S2 | [Misskey Hub - 安装资源索引](https://misskey-hub.net/en/docs/for-admin/install/resources/) | official | unknown | 4 |
| S3 | [Misskey Hub - Nginx configuration](https://misskey-hub.net/en/docs/for-admin/install/resources/nginx/) | official | unknown | 4 |
| S4 | [Misskey Hub - Troubleshooting](https://misskey-hub.net/en/docs/for-admin/install/resources/troubleshooting/) | official | unknown | 5 |
| S5 | [Misskey Hub - Note search](https://misskey-hub.net/en/docs/for-admin/features/search/) | official | unknown | 5 |
| S6 | [Misskey Hub - Detailed guide to installing Misskey on Ubuntu](https://misskey-hub.net/en/docs/for-admin/install/guides/ubuntu-manual/) | official | unknown | 3 |
| S7 | [misskey-dev/misskey - compose_example.yml](https://github.com/misskey-dev/misskey/blob/develop/compose_example.yml) | primary | 2025-12-14（最近改动该路径的提交） | 5 |
| S8 | [misskey-dev/misskey - .config/docker_example.yml](https://github.com/misskey-dev/misskey/blob/develop/.config/docker_example.yml) | primary | unknown | 5 |
| S9 | [misskey-dev/misskey - .config/docker_example.env](https://github.com/misskey-dev/misskey/blob/develop/.config/docker_example.env) | primary | unknown | 4 |
| S10 | [misskey-dev/misskey - CHANGELOG / Release 2026.9.0、2026.7.0](https://github.com/misskey-dev/misskey/blob/develop/CHANGELOG.md) | official | 2026-09-06 / 2026-07-31 | 5 |
| S11 | [Issue #9613 - Docker 使用时升级后无法访问已上传文件](https://github.com/misskey-dev/misskey/issues/9613) | primary | 2023-01-16（已关闭） | 4 |
| S12 | [Discussion #9254 - Changing Instance Domain](https://github.com/misskey-dev/misskey/discussions/9254) | primary | 2022-12-03 | 4 |
| S13 | [misskey-hub-next 文档源仓库 - docker.md](https://github.com/misskey-dev/misskey-hub-next/blob/master/content/en/docs/3.for-admin/install/guides/docker.md) | official | unknown | 4 |

**关于 S13**：与 S1 是同一篇文档（源仓库 Markdown 与渲染页），内容同源，仅作 S1 的原文锚点参考，不单独计数。

**层级分布**：official 9 / primary 4 / implementation-report 0 / community 0。

---

## 二、修正意图文件中的预设（重要）

阶段 0 意图文件里有几条预设，探测结果显示**与实际不符**，需在 P2 以官方来源为准修正：

| 意图文件预设 | 探测结果 |
| --- | --- |
| 数据库需要 PGroonga 扩展 | **部分不成立**。`fulltextSearch` 默认是 `sqlLike`，依赖标准 PostgreSQL，**不需要扩展**；只有显式选 `sqlPgroonga` 才需要 PGroonga 扩展与索引。 |
| 数据库用带 PGroonga 的镜像 | **不成立**。仓库示例 `db` 服务用 `postgres:18-alpine`。 |
| compose 示例在 `.config/` 下 | **名称与位置已变**。容器编排示例是**仓库根目录 `compose_example.yml`**；`.config/docker_example.yml` 是**应用配置**示例，`.config/docker_example.env` 是密钥示例。 |
| 覆盖对象存储与邮件发送 | **官方文档与示例文件中均无这两类配置指引**（`example.yml` 里只出现 `proxySmtp` 注释）。这一项目前缺一手来源。 |
| 反向代理方案待定 | 官方明确推荐 **nginx**（S3 给样例配置），未提 Caddy/Apache；S2 强烈建议对外实例挂 Cloudflare 等 CDN，不要把 Misskey 直接暴露公网。 |

---

## 三、方向菜单

P2 精读范围默认覆盖 **A**，请从 B/C/D 中选择要一并纳入的部分（可多选）。括号内为预估篇幅。

**A. 最小可运行闭环（基线，必含）**
三服务栈（web / db / redis）逐服务职责、四个示例文件的复制关系、`default.yml` 必改字段、首次初始化（`pnpm run init`）、启动顺序与 healthcheck 依赖。（约 2 章）

**B. 对外服务链路**
nginx 反代样例逐段解释、TLS、CDN 建议、`url` 与 `id` 启动后不可更改的后果与规避，以及**仅内网使用（无公网域名）**的变体方案——注意后者官方文档未覆盖，属需自建的空白区。（约 1-2 章）

**C. NAS 落地与运维**
容器构建 vs 预构建镜像的取舍（官方只给 `build`，这是 NAS 吃内存的根因）、构建内存门槛的多方口径冲突、卷权限（UID/GID 991、EACCES）、镜像标签与升级流程、近期破坏性变更（Node 版本、sharp 要求 SSE4.2、NSFW 判定改外部服务）。（约 2 章）

**D. 全文检索配置**
`fulltextSearch` 三种 provider（`sqlLike` / `sqlPgroonga` / `meilisearch`）的能力与代价对比、`sqlPgroonga` 需手工 `CREATE EXTENSION` 与建索引（迁移不自动创建）、各自无法检索的场景。（约 1 章，可与 A 合并）

---

## 四、覆盖缺口（P2 需要额外补料或明确标注为空白）

1. **仅内网 / 无公网域名的部署方案**：官方 nginx 文档只给公网域名 + Let's Encrypt 的配置，无局域网变体。需自建或明确标注为本文档的推断部分。
2. **NAS 专属一手实操记录**：Synology DSM / fnOS / 通用家庭服务器上容器化 Misskey 的一手记录未找到，只有聚合类二手教程。需在 P2 降级使用并标注。
3. **对象存储与邮件发送**：官方无指导，社区来源也稀薄。建议要么从范围中移除，要么明确标注为「非官方、需自行验证」。
4. **构建 OOM 的当前状态**：只找到 2024 年已关闭的 Issue（经 PR 处理），2025–2026 版本是否仍会 OOM 未能确认。
5. **硬件规格口径冲突**：官方 S4 写构建「至少 2GB」，S6 写约 4GB，安装脚本写「总可用内存至少 3GB」。三点需并列呈现，不合并为单一数字。
6. **文档语言版本差异**：语言切换器确认存在日文与简体/繁体中文版，但**未逐字比对**中日英三版正文差异。

---

## 五、P2 预估范围

- 精读来源：7-9 个（S1、S4、S5、S7、S8、S9、S10 为核心；S3、S11、S12 为按需补充）
- 需新增补料的方向：仅内网方案、NAS 一手记录（若用户选择 B/C）
- 产出：`02_deep_research.md`，含来源表、主张-来源映射、口径冲突、实践指引、遗留问题
- 预估章数：4-6 章（取决于 B/C/D 的选择）

---

## 六、用户决策点

请确认 P2 精读范围（基线 A + 可选的 B/C/D），以及对象存储与邮件发送这两项是**从范围中移除**还是**保留并标注为非官方**。
