# 批量更新计划：小雅 fnOS 单容器部署笔记集 → 统一 monlor 单一路线

- 生成时间：2026-10-06
- 工作流：batch-note-update-flow ｜ 运行标识 `update-xiaoya-fnos-routes`
- 依据：`00_batch_update_intent.md`、`01_update_inventory.md`
- 输出模式：`patch-in-place` + 全副本同步（`chapters/` → `output/` → vault）

## 一、更新目标与判断依据

**目标**：整套笔记统一采用 monlor 社区镜像 `ghcr.io/monlor/xiaoya-alist` 单一路线，彻底删除官方镜像 `xiaoyaliu/alist` 路线。

**边界（已由用户确认）**：

1. 只删官方镜像路线。
2. 第 4 章 4.2「路线一：官方镜像」**整节删除**，含该节内的整合脚本（ddsrem）入口。
3. xiaoyaDev / DDSRem 整合脚本菜单在第 1、2 章作为「纯净版 / 单容器」概念旁证**保留**。
4. 第 2 章的「两条路线」= Emby 全家桶(E) vs 飞牛影视(F)，与镜像路线无关，**不动**。
5. 第 5 章 5.6（夸克 / 115 / 播放盘）**不动**。

## 二、口径冻结表（本轮所有改动以此为准，逐篇不得自创措辞）

| # | 维度 | 冻结结论 | 回源 |
| --- | --- | --- | --- |
| 1 | 镜像 | 只出现 `ghcr.io/monlor/xiaoya-alist`（可写加速源 `ghcr.nju.edu.cn/monlor/xiaoya-alist`） | `sources/forum/tid-9690.md:36`、`:942` |
| 2 | 表述禁用 | 不再出现「官方镜像 / 官方路线 / 路线一 / 两条镜像路线 / 二选一（指镜像）」 | — |
| 3 | 镜像性质 | 该镜像是 **monlor 社区维护**，不是小雅官方发布（保留此澄清，去掉「别和官方镜像混写」的旧框架） | `sources/p2/monlor-144.md:21` |
| 4 | 凭据注入 | **只有环境变量三件套**：`ALIYUN_TOKEN` / `ALIYUN_OPEN_TOKEN` / `ALIYUN_FOLDER_ID`（均必填）；可选 `QUARK_COOKIE` / `PAN115_COOKIE` | `sources/forum/tid-9690.md:45-49` |
| 5 | 文件凭据三件套 | `mytoken.txt` / `myopentoken.txt` / `temp_transfer_folder_id.txt` 属官方镜像读法，**从正文移除**（素材文件保留归档） | `sources/01_github_com.md:65`、`sources/p3/z-addone/01_www_cnblogs_com.md:23-25` |
| 6 | 端口 | 容器内 `5678`（Web）/ `2345` / `2346`；宿主示例 `5677` / `5345` / `5346`；映射方向恒为「左宿主、右容器」 | `sources/forum/tid-9690.md:40` |
| 7 | 端口来源冲突 | 「官方页写 5678、社区示例映射到 80」这段冲突**删除**（其双方都属官方镜像） | `sources/01_hub_docker_com.md:17`、`sources/p3/gnz48/01_www_cnblogs_com.md:39` |
| 8 | WebDAV | **用户名 `dav`**，默认密码 `guest_Api789`；路径 `/dav` | `sources/p3/monlor-env/01_raw_githubusercontent_com.md:32`、`sources/forum/tid-9690.md:72`、`:280` |
| 9 | WebDAV 旧写法 | 「官方用 `guest`、monlor 用 `dav`，两条并记」**收敛为第 8 条单一值** | — |
| 10 | 单容器定义 | `EMBY_ENABLED=false`、`JELLYFIN_ENABLED=false`，只起 alist 一个容器 | `sources/forum/tid-9690.md:34-71` |
| 11 | 部署入口 | monlor 一键脚本（`raw.githubusercontent.com/monlor/docker-xiaoya/main/install.sh`）与 Compose 两种，同等呈现 | `sources/p2/monlor-144.md:32` |
| 12 | 官方镜像页引文 | `docker.xiaoya.pro/update_new.sh`、`端口：5678`、`webdav 账号密码 用户: guest`、`docker restart xiaoya 重启即更新索引` 四条**全部移除** | `sources/01_hub_docker_com.md:16-19` |
| 13 | 引文对照表 | 删行后**顺序重编号**，正文引文与表格逐条对应 | 校验器 `note-citation-check.py` |
| 14 | 三副本 | `output/` = `chapters/` + YAML frontmatter + 章首导航行 + 章末「---」与返回导航行；vault = `output/` 语义一致 | 本轮已实测 |

## 三、分组与批次

### 批 1（三篇最重、互相耦合：凭据 / 端口 / 更新口径）

| 序 | 文件 | 动作 | 本篇具体目标 | 依赖 |
| --- | --- | --- | --- | --- |
| 1 | `chapters/04_部署实战.md` | update | **先改**（定调件）：删 4.2 整节；章名去「两条镜像路线」；原 4.3 升为 4.2；4.4 对照表按待确认项处置；4.5 自检第 4 条 WebDAV 改 `dav` / `guest_Api789`；引文对照删官方条目并重编号 | 口径冻结表 1–13 |
| 2 | `chapters/03_动手前准备.md` | update | 删「文件凭据三件套」小节与端口冲突段；WebDAV 收敛为 `dav` / `guest_Api789`；改第 22 行纪律句、镜像警告 Callout、小结、下一章预告（按批 1 第 1 篇的新章名回填） | 定调件产出 |
| 3 | `chapters/07_运维与收尾.md` | update | 更新口径表双列改单列（monlor 脚本可重复执行）；删官方「重启即刷新索引」段；改镜像性质 warning、升级比喻、易混点表「ghcr.io 有没有官方小雅镜像」行、小结、引文对照第 9/10 行并重编号 | 定调件产出 |

### 批 2（两篇轻量收口）

| 序 | 文件 | 动作 | 本篇具体目标 | 依赖 |
| --- | --- | --- | --- | --- |
| 4 | `chapters/01_开篇定位.md` | update | 删第 81 行「或直接运行官方镜像 `xiaoyaliu/alist`」；删引文对照第 2 行「官方镜像作者把…内嵌进容器」并重编号；第 74 行「官方来源（官方镜像页、官方脚本仓库）」收窄为「官方脚本仓库等」 | 批 1 定调 |
| 5 | `output/小雅 fnOS 单容器部署（总览）.md` | update | 章节目录第 4 章说明去掉「两条镜像路线」并按新章名回填；第 54 行「以官方仓库说明为准」改口径 | 定调件产出 |

### 副本同步（每篇改完后立即做，防漂移）

```text
chapters/XX.md  ──机械变换──▶  workspace/xiaoya-fnos-deploy/output/XX YYY.md
                ──复制──────▶  流媒体与影音/小雅 fnOS 单容器部署/XX YYY.md
```

## 四、覆盖风险与需确认项

### 需用户确认（本轮已在 P2 检查点提出）

- **R1 第 4 章新章名**：现名含「（两条镜像路线）」，必须改。
- **R2 原 4.4「两条路线差异对照」整表去留**：其每一行都在比较官方 vs monlor，删除官方后表失去对照对象。

### 覆盖风险

| 风险 | 说明 | 处置 |
| --- | --- | --- |
| 误删概念旁证 | 全文 22 处「官方」字样里，第 1、2 章多处在讲整合脚本菜单（概念旁证，须留） | **逐处人工判定**，禁止全局替换「官方」 |
| 章节交叉引用 | 第 3 章「下一章预告」、总览目录、第 4 章 frontmatter `title` 都写着章名 | 以批 1 第 1 篇的最终章名为准逐处回填；邻章导航栏用短名「04 部署实战」，不受影响 |
| 引文对照错位 | 删行后若不重编号，正文与表格失去一一对应，`note-citation-check.py` 会报错 | 每篇删行即重编号，交付前跑一次校验 |
| 三副本漂移 | 第 3 章 vault 副本已被 Obsidian 自动对齐表格（26 行纯格式差异） | 同步时以 `chapters/` 为准覆盖；该格式差异不保留 |
| 第 5 章受牵连 | 第 5 章可能引用 WebDAV 账号或镜像名 | 已核：第 5 章 0 处 `guest_Api789`、0 处 `xiaoyaliu`，判定 skip；批 2 收口时再复查一次 |
| MOC 失效 | MOC 索引指向入口页 | 入口页标题不变，MOC **无需改动** |

## 五、无需共享资料

`shared_research: no`。本轮全部结论均可回溯到 `workspace/xiaoya-fnos-deploy/sources/` 已有素材，唯一新增回源点是 monlor env 模板的 WebDAV 说明（第 8 条），已定位到 `sources/p3/monlor-env/01_raw_githubusercontent_com.md:32`。

## 六、阶段 3 处置

按 `shared_research: no` 且无新增外部资料需求，阶段 3 以 `skip` 记录（保留用户确认后跳过）。
