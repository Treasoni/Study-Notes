## 第 5 章 缓存与索引/镜像：uv cache / 索引配置

本章回答两个日常问题：**下载过的包都存到了哪里、怎么清理**，以及 **uv 默认从 PyPI 装包，想换成国内镜像或私有源该怎么配**。前者讲 `uv cache` 三条命令与三个「旁路开关」（`--refresh` / `--reinstall` / `--no-cache`）各自的语义；后者讲索引的四种写法、`default` 索引的坑、凭据存放与国内镜像配置指引。uv 迭代快，涉及精确参数时请以 `uv --version` 对应官方文档为准。

### 5.1 uv cache：定位 / 清理 / 剪枝

uv 不会把下载的包直接堆在每个 `.venv` 里，而是把 wheel / sdist **统一放进一个全局缓存目录**，装环境时用硬链接把内容链进去。这样建 100 个虚拟环境，同一个包只在第一次真下载，之后都是本地链接，秒级完成。缓存位置可以用 `uv cache dir` 查：

```bash
# 定位缓存目录（Windows 输出形如 C:\Users\<你>\AppData\Local\uv\cache）
uv cache dir

# 全清：移除缓存目录全部条目（默认硬链接模式不影响已建 .venv）
uv cache clean

# 按包清：只移除某个/某几个包的缓存条目
uv cache clean ruff

# 剪枝：只删「未使用」条目与集中式项目环境，仍可能复用的保留
uv cache prune

# CI 专用剪枝：删预构建 wheel 与未解压 sdist，保留源码编译出的 wheel
uv cache prune --ci
```

三者的差别一句话说清：[^c5-1][^c5-2]

| 命令 | 清理范围 | 典型场景 |
| --- | --- | --- |
| `uv cache clean` | 清空整个缓存目录 | 磁盘告急或想彻底重置；代价是之后首次安装全部重下载 |
| `uv cache clean <pkg>` | 只清单个包的条目 | 怀疑某包缓存损坏，想让该包下次强制重取 |
| `uv cache prune` | 未使用的条目 + 集中式项目环境 | 周期性维护，安全、可常跑 |
| `uv cache prune --ci` | 预构建 wheel + 未解压 sdist，**保留源码编译的 wheel** | CI job 末尾（见下） |

`--ci` 的取舍逻辑：CI 里把「下载即得的预构建 wheel」塞进持久缓存，恢复缓存往往比从索引 CDN 重新下载还慢，所以干脆删掉；而**源码编译出的 wheel**（尤其含扩展模块的包）编译一次很贵，值得留缓存跨 job 复用。因此官方建议在 CI job 末尾跑 `uv cache prune --ci` 保缓存最高效。[^c5-1]

> [!warning] 别手删缓存目录
> 缓存设计为并发安全、只追加写入，**永远不要直接进目录删文件**。`uv cache clean` 会等其它 uv 进程结束（默认 5 分钟超时，`UV_LOCK_TIMEOUT` 可调）。另注意：默认硬链接模式下清缓存不影响已装 `.venv`；若你把 link 模式改成了 `symlink`，`uv cache clean` 会连已装环境的源文件一起破坏（官方有专门警告）。[^c5-2]

> [!tip] 大白话
> 把全局缓存想成「小区共用的工具房」：每个新 `.venv` 需要扳手时去工具房领一把（硬链接复制），不用每次网购。所以「清空工具房」（`clean`）不会弄坏你已经领走、放在自家工位（`.venv`）的工具；但 CI 里给每台机器快递整套工具反而慢，`prune --ci` 的意思是「把外面买来的成品工具退掉，只留自己花大力气改装过的那几把」。

### 5.2 缓存旁路开关：--refresh / --reinstall / --no-cache

`uv sync`、`uv run`、`uv add` 等安装类命令共享三个「绕过缓存/已装状态」的开关，语义容易混：[^c5-1]

```bash
# 忽略缓存元数据、重新到索引校验/取最新，但结果仍写回缓存供下次加速
uv sync --refresh

# 连 .venv 里已装好的包也强制重装一遍（隐含 --refresh）
uv sync --reinstall

# 本次完全不读缓存也不写缓存（改用临时目录），相当于模拟一次「全新网络安装」
uv sync --no-cache
```

| 开关 | 忽略缓存元数据 | 忽略 `.venv` 已装 | 本次仍写缓存 | 什么时候用 |
| --- | --- | --- | --- | --- |
| `--refresh` | 是（重新校验） | 否 | 是 | 想「这次确保拿到最新」，又不愿放弃后续缓存加速 |
| `--reinstall` | 是（隐含） | 是 | 是 | `.venv` 被搞乱、缺文件、想整体重装一遍 |
| `--no-cache` | 是（完全不读） | 否 | 否 | 一次性验证纯净网络安装是否成功 |

要点：**多数想用 `--no-cache` 的场景，其实用 `--refresh` 更优** —— 两者都能绕开陈旧缓存拿到最新，但 `--refresh` 会把新结果写回缓存，下次不再重新下载；`--no-cache` 则每次都是冷启动。三个开关还有按包细化的 `--refresh-package <pkg>` / `--reinstall-package <pkg>`，只对单个包生效。

> [!tip] 大白话
> 把缓存想成冰箱、`.venv` 想成厨房操作台：`--refresh` 是「去超市核对一遍保质期，把新买的仍放进冰箱」；`--reinstall` 是「把操作台上已开封的全倒掉、重新拆一包」；`--no-cache` 是「这次不进货，全部现买现做，而且不往冰箱里存」。日常只是想确认没吃过期食品，用第一个就够了，别每次都断掉冰箱。

### 5.3 索引与国内镜像

默认 uv 从 PyPI 解析与安装。需要走国内镜像、内网私有源、或某包只存在于特定源时，就要配置「索引」。uv 支持四个层面的写法，从「写进项目固定」到「单次临时」：[^c5-3]

**① 项目级声明：`pyproject.toml` 的 `[[tool.uv.index]]`（最推荐，随项目走）**

```toml
# pyproject.toml —— 追加一个附加索引
[[tool.uv.index]]
name = "mirror"                                     # 可选；后面固定包、配凭据时要用名字
url  = "https://mirror.example.com/simple"          # 替换成镜像服务当前提供的 simple 地址

# 想让它顶替 PyPI 作「兜底默认索引」，就加一行：
# default = true
#（注意：一旦有任一索引 default = true，PyPI 即被排除，不再兜底）
```

**② 单次命令行：`--index` / `--default-index`（不写进任何文件）**

```bash
# --default-index 指把「默认索引」换成该地址（等价于上面 default = true）
uv add requests --default-index https://mirror.example.com/simple
```

**③ 环境变量：`UV_DEFAULT_INDEX` / `UV_INDEX`（会话级，等价于对应 CLI 参数）**

```bash
# 后续本 shell 所有 uv 命令都走该默认索引（换镜像验证最常用）
export UV_DEFAULT_INDEX=https://mirror.example.com/simple

# Windows PowerShell 写法：
# $env:UV_DEFAULT_INDEX = "https://mirror.example.com/simple"

# 撤消：unset UV_DEFAULT_INDEX
```

**④ 旧 pip 风格兼容：`--index-url` / `--extra-index-url`（已弃用，仅兼容）**

`--index-url` 等价于 `--default-index`，`--extra-index-url` 等价于 `--index`，官方标注 **Deprecated**；配套的 `UV_INDEX_URL` / `UV_EXTRA_INDEX_URL` 环境变量同样建议换成 `UV_DEFAULT_INDEX` / `UV_INDEX`。[^c5-3]

**default 语义与优先级**（最易踩坑的一条）：uv 默认把 PyPI 当作「default 索引」——即其它索引都找不到时兜底的源。default 索引**无论写在哪个位置都恒为最低优先级**；而各附加索引按**声明顺序**被优先咨询，越靠前越先被查。CLI / 环境变量提供的索引优先于配置文件里的索引。所以「设某索引 `default = true` = 明确把 PyPI 从兜底位挤掉」，而不是「加一个平行源」。[^c5-3]

> [!warning] 注意：社区写法不一致，以官方 indexes 文档为准
> 网上搜「uv 换清华源」会看到好几种互相打架的写法：有人写 `uv.toml`（独立配置文件，键在顶层），有人写 `pyproject.toml`（必须包在 `[tool.uv]` 段下），有人用已弃用的 `UV_INDEX_URL`，有人用 `UV_DEFAULT_INDEX`。这几处文件层级与变量新旧各不相同，**不能直接照搬**。本文统一采用官方推荐：项目级用 pyproject `[[tool.uv.index]]`，临时/会话级用 `UV_DEFAULT_INDEX` + `--default-index`。[^c5-3][^c5-5]

**私有索引凭据**：不要写进 pyproject（明文入库），用环境变量按「索引名大写、非字母数字换成下划线」命名——例如索引名 `internal-proxy` 对应 `UV_INDEX_INTERNAL_PROXY_USERNAME` / `UV_INDEX_INTERNAL_PROXY_PASSWORD`；也可临时内嵌在 URL 里。凭据**永远不会写进 `uv.lock`**，因此安装时必须能访问到带认证的 URL。[^c5-3]

**多索引解析策略**：默认 `first-index`——某个包在第一个命中它的索引上找到，就只用该索引的结果，不再到后面索引找。这层「找到即停」是为了防**依赖混淆攻击**（攻击者在 PyPI 抢注你内网包同名，诱导你装上恶意包）。想改成 pip 那种跨索引挑版本，需显式 `--index-strategy unsafe-best-match`，但会暴露依赖混淆风险，非必要别开。[^c5-3]

**国内镜像配置指引**：官方文档不维护镜像清单，具体可用镜像与其 simple 地址以**各镜像服务官方说明为准**（上例 URL 均为占位符）。拿到地址后按上述写法①写进项目、或写法③做会话级临时切换即可，无需给每个命令加参数。

### 5.4 常用场景组合（本族）

| 我要… | 组合 | 锚点 |
| --- | --- | --- |
| CI 末尾保住缓存效率 | `uv cache prune --ci`（配合 setup-uv `enable-cache` + 缓存 key 用 `uv.lock`） | → 见 §5.1、附录 B |
| 换镜像后先单次验证再固化 | `uv add requests --default-index <url>` 验证 OK → 再写进 pyproject `[[tool.uv.index]]` | → 见 §5.3 |
| 本地磁盘告急 | 先 `uv cache prune`（安全增量）→ 还不够再 `uv cache clean` | → 见 §5.1 |
| 确认这次装到最新版且保留缓存 | `uv sync --refresh`（慎用 `--no-cache`） | → 见 §5.2 |

组合逻辑：**日常不需要主动清缓存**，磁盘告急按「`prune` → `clean`」两级来；**索引配置优先「项目级写 pyproject」**，镜像这类换源场景先用 `UV_DEFAULT_INDEX` / `--default-index` 临时验证，避免一上来就改动项目文件。

---

**本章小结**
- 缓存是全局共享目录，`uv cache dir` 定位、`uv cache clean [pkg]` 全清/按包清、`uv cache prune` 安全剪枝、`uv cache prune --ci` 专为 CI 删预构建 wheel 留源码编译 wheel。
- 三个旁路开关：`--refresh` 重校验仍写缓存（多数场景首选）、`--reinstall` 忽略已装强装、`--no-cache` 本次不读不写缓存。
- 索引四种写法：pyproject `[[tool.uv.index]]` / CLI `--index`·`--default-index` / 环境变量 `UV_INDEX`·`UV_DEFAULT_INDEX` / 已弃用的 `--index-url`·`--extra-index-url`；CLI/环境变量优先于配置文件。
- default 索引恒最低优先级；给某索引加 `default = true` 即排除 PyPI；`first-index` 默认策略防依赖混淆，别轻易改成 `unsafe-best-match`。
- 国内镜像没有官方清单，只给官方写法 + 「以镜像服务说明为准」；粘贴社区写法前先分辨是 `uv.toml` 还是 pyproject、是旧 `UV_INDEX_URL` 还是新 `UV_DEFAULT_INDEX`。

下一章进入「构建发布与 pip 兼容层」：`uv build` / `uv publish` 把项目做成发行包传上索引，以及 `uv pip` 这层 pip 兼容命令的适用边界（→ 见第 6 章）。

