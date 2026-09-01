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
updated: 2026-08-30
status: 完成
source_project: hermes-docker-deploy
---

> [[10-安全基线|⬅ 上一章]] · [[README|📖 返回目录]]

# Dashboard 认证配置实战

> [!summary] 一句话结论
> Hermes 检测到 Web 控制台（Dashboard）配置了**外部公网访问或非本地监听**，却没有配置任何登录认证。出于安全策略，Hermes **不允许无密码公开暴露控制台**，因此拒绝启动。解决办法是配置 `dashboard.basic_auth`（用户名 + bcrypt 密码哈希），或改为仅本机监听（`127.0.0.1` + 不设置 `public_url`）。

---

## 一、错误现场

启动 Hermes 时控制台报错：

```text
Configure an auth provider before exposing the dashboard:

  • Password: set dashboard.basic_auth.username + password_hash in config.yaml

    (hash with: python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('your-password'))")

  • OAuth: run `hermes dashboard register` (Nous Portal) or install a DashboardAuthProvider plugin.

There is no unauthenticated public-dashboard option. For local-only use, bind 127.0.0.1 and leave dashboard.public_url unset; a configured external public URL requires auth even when a local reverse proxy reaches a loopback backend.

→ Using web dist from HERMES_WEB_DIST: /opt/hermes/hermes_cli/web_dist
```

> [!note] 关键信息
> Hermes 官方**没有「无认证公网控制台」这个选项**。只要你配置了外部 `public_url`，即使本地反向代理只回环到 `127.0.0.1`，也**必须**启用认证，否则拒绝启动。

---

## 二、问题原因

| 触发条件 | 结果 |
| --- | --- |
| `dashboard.public_url` 配置了外部公网地址 | 要求认证，否则拒绝启动 |
| 监听地址不是本机回环（如 `0.0.0.0`） | 同上 |
| 仅本机访问（`127.0.0.1` + 无 `public_url`） | 无需认证，可免密启动 |

核心逻辑：**对外暴露 = 必须有认证**；**仅本机 = 可以免密**。

---

## 三、解决方案

### 方案一：配置用户名与密码认证（推荐）

#### 1. 生成密码哈希

在服务器终端运行（把 `MyPassword123` 换成你要设置的密码）：

本地环境已装 Python / Hermes 依赖：

```bash
python3 -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('MyPassword123'))"
```

如果使用 Docker：

```bash
docker run --rm -it <你的Hermes镜像名> python3 -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('MyPassword123'))"
```

运行后输出一段类似 `$2b$12$e8Y...` 的 bcrypt 哈希字符串，复制备用。

> [!tip] 大白话
> 哈希就像「保险箱的指纹锁」：`config.yaml` 里只存指纹（哈希），不存钥匙（明文密码）。网页登录时你输入钥匙，Hermes 现场取指纹比对，一致才放行。就算服务器配置文件泄露，拿到指纹也推不出你的钥匙。

#### 2. 修改 config.yaml

在 `dashboard` 下添加 `basic_auth`：

```yaml
dashboard:
  # 其他已有配置保持不变...
  basic_auth:
    username: "admin"
    password_hash: "$2b$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 粘贴刚生成的哈希
```

#### 3. 重启容器

```bash
docker restart hermes
```

---

### 方案二：仅限本地访问（纯内网免密）

如果只在本地 / 内网测试，不想设置密码：

1. 打开 `config.yaml`
2. 确保 `dashboard.public_url` **留空或删除该字段**
3. 确保监听地址绑定 **`127.0.0.1`**（不要绑定 `0.0.0.0`）

> [!warning] 易错点
> 只要设了外部 `public_url`，即使反向代理（nginx / caddy）只转发到本机回环后端，也**仍然要求认证**——不能靠「反代挡在外面」绕过 Hermes 的认证检查。

---

## 四、登录凭证说明

| 项目 | 内容 |
| --- | --- |
| 账号 Username | `config.yaml` 里 `username:` 填的值（如 `admin`） |
| 密码 Password | 生成哈希时 `hash_password('你的密码')` 单引号里的**原始明文密码** |
| 配置文件里为什么只有乱码 | `password_hash` 是单向加密密文，防止服务器文件泄露导致密码曝光 |
| 系统校验流程 | 登录时输入明文 → Hermes 现场哈希 → 与 `password_hash` 比对 |

> [!warning] 忘记密码怎么办
> 直接重新生成一段新哈希覆盖 `config.yaml` 的 `password_hash` 字段，重启容器即可：

```bash
# 生成新密码（例如设为 12345678）
python3 -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('12345678'))"
```

重启后网页登录密码即变为 `12345678`。

---

## 五、知识点速记

- Hermes Dashboard 认证三选一：`basic_auth`（密码）/ `hermes dashboard register`（Nous Portal OAuth）/ 自定义 `DashboardAuthProvider` 插件。
- 密码哈希算法：bcrypt（前缀 `$2b$12$`）。
- 安全基线：公网 = 必须认证；本机 = 可免密。
- 与第 10 章安全基线的关系：Dashboard 公网暴露的认证要求，属于容器对外暴露的安全收口，配置后不可依赖「反代挡外面」绕过。

---

## 参考

- Hermes 报错信息自带帮助文本（见上文「错误现场」）
