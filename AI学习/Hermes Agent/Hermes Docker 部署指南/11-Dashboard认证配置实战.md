---
title: "Dashboard 认证配置实战"
tags:
  - AI学习
  - Agent
  - Hermes
  - Docker
  - 安全
  - 排错
created: 2026-08-30
updated: 2026-10-06
status: 完成
source_project: hermes-docker-deploy
---

> [[10-安全基线|⬅ 上一章]] · [[README|📖 返回目录]]

# Dashboard 认证配置实战

> [!summary] 一句话结论
> Hermes 检测到 Web 控制台（Dashboard）绑定了**非本机回环地址**（Docker 里默认就是 `0.0.0.0`），或配置了**外部 `public_url`**，却没有注册任何登录认证，于是**拒绝启动**（fail closed，启动即失败）。解决办法是配置认证——最省事的是用户名 + 密码（`HERMES_DASHBOARD_BASIC_AUTH_*`），或改为仅本机监听（`HERMES_DASHBOARD_HOST=127.0.0.1` + 不设 `public_url`）。

---

## 一、错误现场：Dashboard 拒绝启动

启用 Dashboard（`HERMES_DASHBOARD=1`）后容器重启，Dashboard 服务起不来。官方文档对同一场景的原始描述如下。

> [!quote] 官方原文
> If no provider is registered and the bind is non-loopback, the dashboard **fails closed at startup** with a specific error pointing at the missing env var. There is no longer an escape hatch that serves the dashboard unauthenticated on a public bind: `HERMES_DASHBOARD_INSECURE=1` is now a deprecated no-op (it logs a warning and is ignored). Configure a provider, or bind `HERMES_DASHBOARD_HOST=127.0.0.1` and reach the dashboard over an SSH tunnel / Tailscale instead.

| 官方原文（节选） | 说人话 |
| --- | --- |
| fails closed at startup with a specific error pointing at the **missing env var** | 启动直接失败；报错会**点名你少设了哪个环境变量** |
| There is no longer an escape hatch that serves the dashboard unauthenticated on a public bind | 没有「免密公网控制台」这条后路了 |
| `HERMES_DASHBOARD_INSECURE=1` is now a deprecated no-op | 老的免密开关已废弃，设了也只打一条警告、照样拦 |
| Configure a provider, or bind `HERMES_DASHBOARD_HOST=127.0.0.1` | 要么配认证，要么只绑本机回环、再走隧道 |

> [!note] 关键信息
> Hermes 官方**没有「无认证公网控制台」这个选项**。只要绑定地址不是本机回环，或配置了外部 `public_url`，就**必须**启用认证，否则拒绝启动。（实际报错文本随版本变化，核心是"点名缺失的环境变量"。）

---

## 二、问题原因

Dashboard 的认证门（auth gate）只在「绑定非回环」时才要求注册 provider：

| 触发条件 | 结果 |
| --- | --- |
| 绑定地址不是本机回环（Docker 里默认 `HERMES_DASHBOARD_HOST=0.0.0.0`） | 必须注册认证 provider，否则启动即失败 |
| 配置了外部 `HERMES_DASHBOARD_PUBLIC_URL` | 即使后端绑在 `127.0.0.1`，也强制要求认证 |
| 仅本机访问（`HERMES_DASHBOARD_HOST=127.0.0.1` + 不设 `public_url`） | 无需认证，可免密启动 |

核心逻辑：**对外暴露 = 必须有认证**；**仅本机 = 可以免密**。

> [!warning] Docker 的默认值就是"对外暴露"
> 容器里 Dashboard **默认绑 `0.0.0.0`**——否则映射出去的 `-p 9119:9119` 从宿主机根本访问不到。也就是说容器一开 Dashboard 就是"对外暴露"状态，不配认证一定起不来。

---

## 三、解决方案

### 方案一：配置用户名与密码认证（推荐）

#### 1. 生成密码哈希

在装有 Hermes 的机器上运行（把 `MyPassword123` 换成你要设置的密码）：

```bash
# 本机已装 Hermes（在安装树 / repo 根目录下执行）
python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('MyPassword123'))"
```

在运行中的容器里生成（镜像已把 Hermes 装进 `/opt/hermes/.venv`）：

```bash
docker exec hermes /opt/hermes/.venv/bin/python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('MyPassword123'))"
```

运行后输出一段以 **`scrypt$`** 开头的哈希字符串（例如 `scrypt$...`），复制备用。

> [!warning] 是 scrypt，不是 bcrypt
> `hash_password` 生成的是 **scrypt** 哈希（前缀 `scrypt$`，自带随机盐），**不是** bcrypt，也不会长成 `$2b$12$...` 那样。看到 `$2b$12$` 说明来源资料是错的。
> 若容器里提示找不到 `plugins` 模块，就回到本机（装了 Hermes 的环境）跑同一条命令，再粘贴结果。

> [!tip] 大白话
> 哈希就像「保险箱的指纹锁」：`config.yaml` 里只存指纹（哈希），不存钥匙（明文密码）。网页登录时你输入钥匙，Hermes 现场取指纹比对，一致才放行。就算服务器配置文件泄露，拿到指纹也推不出你的钥匙。

#### 2. 配置认证（环境变量优先）

官方约定「密钥只放 `~/.hermes/.env`」，Docker 部署用环境变量最顺手（`docker run -e` 或 compose 的 `environment:`）：

```yaml
# docker-compose.yml（节选）
services:
  hermes:
    environment:
      HERMES_DASHBOARD_BASIC_AUTH_USERNAME: "admin"
      HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH: "scrypt$..."   # 粘贴刚生成的哈希
      HERMES_DASHBOARD_BASIC_AUTH_SECRET: "<32 字节以上随机串>"  # 让登录态在重启后仍然有效
```

> [!tip] 只想「能用」的最短路径
> 不折腾哈希的话，直接给明文环境变量即可：`HERMES_DASHBOARD_BASIC_AUTH_USERNAME` + `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD`（加载时在内存里哈希）。想「配置里不存明文」，就改用 `_PASSWORD_HASH` 存 scrypt 哈希。

也可以写进 `config.yaml` 的 `dashboard.basic_auth`（两者等价，**环境变量优先**）：

```yaml
dashboard:
  # 其他已有配置保持不变...
  basic_auth:
    username: "admin"
    password_hash: "scrypt$..."      # 粘贴刚生成的哈希（推荐：不落明文）
    # password: "明文密码"           # 备选：加载时内存哈希，但不推荐把明文落盘
    secret: "<32+ 字节随机串>"        # 会话签名密钥；留空则每次重启掉登录
    session_ttl_seconds: 0           # 0 = 默认 12 小时
```

#### 3. 重启容器

```bash
docker restart hermes
```

---

### 方案二：仅限本地访问（纯内网免密）

如果只在本地 / 内网测试，不想设置密码：

1. 设 `HERMES_DASHBOARD_HOST=127.0.0.1`（Docker 里默认是 `0.0.0.0`，必须显式改回回环）
2. 确保 `HERMES_DASHBOARD_PUBLIC_URL` **留空或删除该字段**
3. 改完后 `9119` 端口不再对外可达，需要时用 SSH 隧道 / Tailscale 访问

> [!warning] 易错点
> 只要设了外部 `public_url`，即使反向代理（nginx / caddy）只转发到本机回环后端，也**仍然要求认证**——不能靠「反代挡在外面」绕过 Hermes 的认证检查。

---

## 四、登录凭证说明

| 项目 | 内容 |
| --- | --- |
| 账号 Username | `HERMES_DASHBOARD_BASIC_AUTH_USERNAME`（或 config 的 `dashboard.basic_auth.username`）填的值（如 `admin`） |
| 密码 Password | 生成哈希时 `hash_password('你的密码')` 单引号里的**原始明文密码** |
| 配置里为什么只有乱码 | `password_hash` 存的是一段 `scrypt$...` 单向哈希（自带随机盐），服务器文件泄露也推不回明文 |
| 系统校验流程 | 登录时输入明文 → Hermes 用哈希里的盐重算 scrypt → 与 `password_hash` 比对 |

> [!warning] 忘记密码怎么办
> 直接重新生成一段新哈希，覆盖 `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH`（或 config 的 `password_hash`），重启容器即可：

```bash
# 生成新密码（例如设为 12345678）
python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('12345678'))"
```

重启后网页登录密码即变为 `12345678`。

---

## 五、知识点速记

- Hermes Dashboard 内置三种认证 provider，三选一：**用户名/密码**（`HERMES_DASHBOARD_BASIC_AUTH_*`）/ **Nous Portal OAuth**（`HERMES_DASHBOARD_OAUTH_CLIENT_ID`，用 `hermes dashboard register` 申领）/ **自建 OIDC**（`HERMES_DASHBOARD_OIDC_*`，对接你自己的身份提供商）。三种本质上都是注册一个 `DashboardAuthProvider` 插件。
- 密码哈希算法：**scrypt**（前缀 `scrypt$`），由 `hash_password` 生成，自带随机盐。
- `HERMES_DASHBOARD_INSECURE=1` 已废弃：设了也只打一条警告，不再能跳过认证。
- 安全基线：公网 = 必须认证；本机 = 可免密。
- 与第 10 章安全基线的关系：Dashboard 公网暴露的认证要求，属于容器对外暴露的安全收口，配置后不可依赖「反代挡外面」绕过。

---

## 参考

- Hermes 官方文档《Docker Setup》→ 容器内 Dashboard 绑定与三种 auth provider
- Hermes 官方文档《Environment Variables》→ Web Dashboard & Hermes Desktop（`HERMES_DASHBOARD_BASIC_AUTH_*` 全表，明确 `_PASSWORD_HASH` 为 scrypt）
- Hermes 官方文档《Configuration》→ `dashboard` 段（`dashboard.basic_auth.password_hash` 注释为 `scrypt$...`）
- Hermes 官方文档《CLI Commands》→ `hermes dashboard` / `hermes dashboard register`
