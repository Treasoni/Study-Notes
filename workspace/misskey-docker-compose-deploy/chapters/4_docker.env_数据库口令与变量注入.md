# 第四章：`.config/docker.env`——数据库口令与变量注入

前两章分别处理了「起哪些容器」（`compose.yml`）和「Misskey 自己怎么跑」（`default.yml`）。还差一环：数据库容器的账号密码从哪来。答案就是这个只有 11 行的 `.config/docker.env`。它一分钟能读完，却埋着全篇唯一一个「不改就一定出事」的安全陷阱，所以单独成章。

---

## 4.1 先看全文

它是从 `.config/docker_example.env` 拷来的，全文如下（`【官方】`：与仓库示例逐字一致，`master` 与 `develop` 分支相同[^c4-1]）：

```env
# .config/docker.env
# misskey settings
# MISSKEY_URL=https://example.tld/

# db settings
POSTGRES_PASSWORD=example-misskey-pass
# DATABASE_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_USER=example-misskey-user
# DATABASE_USER=${POSTGRES_USER}
POSTGRES_DB=misskey
# DATABASE_DB=${POSTGRES_DB}
DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"
```

逐行拆开，只有 4 行真正生效，其余全被 `#` 注释掉 `【官方】`：

| 变量 | 值 | 状态 | 作用 |
| --- | --- | --- | --- |
| `MISSKEY_URL` | `https://example.tld/` | 注释 | 未说明用途（见 4.4） |
| `POSTGRES_PASSWORD` | `example-misskey-pass` | **生效** | 数据库口令——**必须改** |
| `DATABASE_PASSWORD` | `${POSTGRES_PASSWORD}` | 注释 | 备选写法（见 4.3） |
| `POSTGRES_USER` | `example-misskey-user` | **生效** | 数据库用户名 |
| `DATABASE_USER` | `${POSTGRES_USER}` | 注释 | 备选写法 |
| `POSTGRES_DB` | `misskey` | **生效** | 数据库名 |
| `DATABASE_DB` | `${POSTGRES_DB}` | 注释 | 备选写法 |
| `DATABASE_URL` | `postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}` | **生效** | 拼出来的连接串 |

所以这个文件的职责只有一件事：**给数据库容器一组账号、口令、库名，再顺手拼一个连接串。**

> [!tip] 大白话
> 把它想成「出租屋的水电开户单」——户名（`POSTGRES_USER`）、门锁密码（`POSTGRES_PASSWORD`）、房号（`POSTGRES_DB`），最后一行 `DATABASE_URL` 是把这三项抄成一句「门牌+钥匙」的完整地址。它不决定 Misskey 长什么样，只决定**数据库这扇门怎么开**——这也正是下一节那个陷阱危险的原因：门锁密码印在公开说明书上。

---

## 4.2 最大的坑：占位口令是一把真的能用的钥匙

这是本章最重要的一点 `【官方】`：`POSTGRES_PASSWORD=example-misskey-pass` 里的 `example-misskey-pass` **不是空占位符，也不是格式非法的假值**，而是一个语法完全合法、容器启动后立刻被采纳为真实口令的字符串[^c4-1]。也就是说：

- `cp` 完示例直接 `docker compose up`，数据库**会正常跑起来**，不会有任何报错提示你「密码没改」；
- 与此同时，你的实例口令就是 `example-misskey-pass`——一个写在 GitHub 公开仓库里、谁都能 `curl` 到的字符串。

【官方】把它列为必改清单的首要项[^c4-2]。危险恰恰在于它「不报错」：空口令会失败，非法格式可能被拒，而一个可用的弱口令会安静地跑下去。

改动时要连带处理一致性 `【官方】`：`default.yml` 的 `db.user` / `db.pass` 示例值同样是 `example-misskey-user` / `example-misskey-pass`，与这里必须对得上[^c4-3]。两处填的不是两个密码，而是**同一把钥匙的两份副本**，只改一边就连不上库。

> [!warning] 易错点
> 改口令要同时改两处：`.config/docker.env` 的 `POSTGRES_PASSWORD`（数据库容器用）与 `.config/default.yml` 的 `db.pass`（Misskey 应用用）。注意 `default.yml` 有一行注释说 `user` / `pass` **也可由环境变量提供**，但示例没写出变量名，所以默认仍按「写死在 YAML 里」理解。

---

## 4.3 `DATABASE_URL` 是拼出来的；另有三行注释备选

最后一行值得单独看：

```env
# .config/docker.env
DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"
```

`${...}` 是**变量插值**：加载方先把大括号里的名字替换成上面几行的值，再得到最终字符串。代入示例默认值，它展开成 `【官方】`：

```text
postgres://example-misskey-user:example-misskey-pass@db:5432/misskey
          └── POSTGRES_USER ──┘ └─ POSTGRES_PASSWORD ─┘ │    └ POSTGRES_DB
                                                         └── 主机名 db，端口 5432
```

两个可直接落地的结论：主机名 `db` / 端口 `5432` 必须与 `compose.yml` 的服务名、`default.yml` 的 `db.host` 一致；改口令只需动 `POSTGRES_PASSWORD` 一处，`DATABASE_URL` 展开后自动跟着变，反之若把连接串写成明文，就等于把口令抄了第二份，日后必然遗忘同步。

【推断】文件把连接串交给 `${VAR}` 插值而非写死字面量，意味着加载它的程序（Compose / dotenv 类实现）必须支持变量展开；若某环境不展开 `${}`，这行拿到的就是带花括号的原始字符串。文件本身没说展开由谁负责。

紧跟每个 `POSTGRES_*` 之后各有一行「镜像」写法，全部被注释 `【官方】`：`DATABASE_PASSWORD=${POSTGRES_PASSWORD}`、`DATABASE_USER=${POSTGRES_USER}`、`DATABASE_DB=${POSTGRES_DB}`。这说明 Misskey 也接受**把连接信息分项给**，由程序自己组装。三行都用 `${...}` 回指上面的 `POSTGRES_*`，可见作者本意不是让你另填一份值，而是换个变量名走另一条读取路径。至于两者同时存在时谁优先、哪种写法在哪些版本生效，示例没说，本笔记不猜 `【官方】`。

---

## 4.4 `MISSKEY_URL`：存在，但文件没说它是干什么的

第一行 `# MISSKEY_URL=https://example.tld/` 被注释，所以默认不生效 `【官方】`。它是文件里唯一的 `MISSKEY_*` 变量，位于 `# misskey settings` 注释组下，值是 `https://example.tld/`——与 `default.yml` 里 `url` 的占位值一模一样。

本笔记对此**不作断言**。若要给方向性判断，那只能是：【推断】它很可能与 `default.yml` 的 `url` 对应，用于从环境变量提供实例地址；但文件既把它注明为可选（已注释），又没给任何说明，因此不影响照抄示例跑通流程。

---

## 4.5 谁在真正读这个文件——「改了全局生效」是错的

这是本章第二个必须记住的点。回到 `compose.yml`，看两个服务的差别 `【官方】`[^c4-4]：

```yaml
# compose.yml（节选）
services:
  web:
    build: .
    # env_file:              ← 整行被注释掉
    #   - .config/docker.env
    volumes:
      - ./.config:/misskey/.config:ro   # 实际配置从只读挂载进容器

  db:
    image: postgres:18-alpine
    env_file:
      - .config/docker.env               # ← 这一行是生效的
```

| 服务 | 是否读 `docker.env` | 实际配置来源 |
| --- | --- | --- |
| `db` | **读**（`env_file` 生效） | `.config/docker.env` |
| `web` | **不读**（`env_file` 被注释） | `.config/` 只读挂载 → 即 `default.yml` |

由此得到两个必须记住的推论：

1. **改 `docker.env` 不会全局重配 Misskey。** 它只喂给 `db` 容器；`web`（Misskey 本体进程）拿配置的通道是 `.config` 只读挂载，读的是 `default.yml`。所以「我改了 `docker.env`，Misskey 就该用新口令」是**错误预期**：应用侧口令在 `default.yml` 的 `db.pass`，两个文件各管一半。
2. **这个文件是隐式必需的。** 因为 `db` 的 `env_file` 确实生效，`.config/docker.env` 一旦不存在，`db` 启动就失败——不像 `web` 有「不读也行」的余地。第一章「三连拷贝」不能漏掉任何一份，这里给出了其中一份的硬理由。

> [!tip] 大白话
> 把 `env_file` 想成「这张卡能刷开哪个房间的门」：`db` 那行没被注释，是「能刷开数据库房间」；`web` 那行加了 `#`，等于「刷不开 Misskey 房间的门」，而 Misskey 房间的钥匙挂在另一面墙（`.config/default.yml`）上。所以指望「改一次 `docker.env`，全楼换锁」不成立。

---

## 小结

- 职责单一：给 `db` 容器提供 `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB`，并拼出 `DATABASE_URL` `【官方】`。
- **首要必改项**：`POSTGRES_PASSWORD=example-misskey-pass` 是可直接生效的占位口令，照抄不改会得到一个口令公开可知的实例 `【官方】`。
- `POSTGRES_USER` 默认 `example-misskey-user`、`POSTGRES_DB` 默认 `misskey`；同名的 `DATABASE_*` 三行是注释备选写法，说明 Misskey 也能分项读取连接信息 `【官方】`。
- `DATABASE_URL` 由 `${VAR}` 插值拼出，改 `POSTGRES_*` 会自动同步；主机名 `db` / 端口 `5432` 必须与 `compose.yml`、`default.yml` 一致 `【官方】`。
- `MISSKEY_URL` 存在但被注释、未说明用途；**改 `docker.env` 不等于重配 Misskey**——`web` 的 `env_file` 被注释，应用配置走 `.config` 只读挂载，而 `db` 的 `env_file` 生效使本文件成为隐式必需文件 `【官方】`。

---

三份产物到这里全部处理完：编排、应用配置、数据库口令。下一章进入执行环节——按官方三步走 `build` → `run --rm web pnpm run init` → `up -d`，并在上机前对照内存地板与 CPU 指令集门槛做一次自查。

[^c4-1]: Misskey 仓库示例文件 `.config/docker_example.env`，见 `sources/S09_docker_example.env.md`。
[^c4-2]: 必改清单将 `POSTGRES_PASSWORD` 列为首要项，见 `02_deep_research.md`「5.1 必改清单」。
[^c4-3]: Misskey 仓库示例文件 `.config/docker_example.yml` 的 `db.user` / `db.pass`，见 `sources/S08_docker_example.yml.md`。
[^c4-4]: Misskey 仓库示例文件 `compose_example.yml`，见 `sources/S07_compose_example.yml.md`。
