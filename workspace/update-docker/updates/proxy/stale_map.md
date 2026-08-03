# stale_map — docker进行代理.md

> 运行标识：update-docker
> 笔记：docker/docker进行代理.md
> 更新目标：全面刷新到 2026 最新（Docker daemon / 容器代理 2026 最佳实践）
> 生成时间：2026-08-03

## 过时项 / 变更映射

| 原文位置 | 状态 | 说明 | 依据 |
|---|---|---|---|
| （无 frontmatter） | ➕ add | 补 YAML frontmatter：title、tags: [docker, 代理, proxy]、created/updated=2026-08-03、status、source_project | 项目 Obsidian 规范 |
| 第 1 节 HTTP / SOCKS 代理（1.1 宿主机代理 + 1.2 验证） | ✅ keep | 容器 env 代理写法与验证方法，2026 仍正确 | 时效性内容，未变 |
| 第 2 节 账号密码判断与写法（2.1–2.4） | ✅ keep | 鉴权判断方法、带账号密码的 HTTP/SOCKS5 写法，2026 仍适用；Docker Desktop 代理 URL 同样支持账号密码 | 非时效 |
| 第 3 节 HTTP vs SOCKS5 原理（3.1–3.4） | ✅ keep | 原理性内容，无时效性 | 非时效 |
| 4.1 方法一：改 compose 重建 | ✅ keep（微调格式） | 正确做法；仅把原第 2/3 步的无语言代码块补上 `bash` 标识 | 项目规范（代码块需语言标识） |
| 4.2 方法二：daemon 代理 | 🔄 update（澄清） | 明确限定为**非 Desktop 的 Linux daemon**；补 `NO_PROXY`；加 [!warning] 将 Docker Desktop 用户导向 4.3 | S9 |
| 4.2 之后 | ➕ add | 新增 4.3 方法三：Docker Desktop Settings → Resources → Proxies（**Docker Desktop 忽略 daemon.json 代理**） | S8 |
| 4.2 之后 | ➕ add | 新增 4.4 方法四：`~/.docker/config.json` 的 `proxies.default` 自动注入构建 / 容器代理 | S10 |
| 文末 | ➕ add | 追加 `## 更新记录`（2026-08-03 变更摘要） | 项目规范 |
| 删除项 | 无 | 无需要删除的内容 | — |
