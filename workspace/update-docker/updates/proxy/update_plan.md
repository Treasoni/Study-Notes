# update_plan — docker进行代理.md

> 运行标识：update-docker
> 笔记：docker/docker进行代理.md
> 输出模式：project-output-only（原文不动，写 updates/proxy/updated_note.md）

## 变更清单

1. **补 frontmatter**
   - 原文完全没有 YAML frontmatter。
   - 新增：title、tags: [docker, 代理, proxy]、created/updated=2026-08-03、status、source_project。

2. **4.2 澄清适用范围（update）**
   - 原 4.2 把「daemon 代理」写得像是所有场景通用，但官方文档（S8）明确 Docker Desktop 忽略 daemon.json 代理。
   - 限定 4.2 为「非 Desktop 的 Linux daemon」：systemd drop-in 方法 2026 年仍正确（S9）。
   - 补充 `NO_PROXY`（S9 推荐项）。
   - 加 [!warning] callout，把 Docker Desktop 用户导向 4.3。

3. **新增 4.3 Docker Desktop 设置界面代理（add，S8）**
   - 关键修正：Docker Desktop（Windows/macOS）必须用 Settings → Resources → Proxies → Manual proxy configuration（HTTP/HTTPS/SOCKS5 + no-proxy），Apply & Restart。
   - 说明影响 pull/build、自动传播代理环境变量到容器、支持带账号密码的代理 URL。

4. **新增 4.4 ~/.docker/config.json 容器内代理（add，S10）**
   - `proxies.default`（httpProxy/httpsProxy/noProxy）在 `docker run` / `docker compose` 构建时自动注入。
   - 附验证命令 `docker info | grep -i proxy`。

5. **追加 `## 更新记录`（add）**
   - 记录 2026-08-03 变更摘要。

6. **代码块语言标识补齐（微调）**
   - 4.1 第 2、3 步原为无语言代码块，补 `bash`；4.2 的 systemd 配置块由 `bash` 改为更准确的 `ini`。

## 不修改的部分与原因

- 第 1、2、3 节（容器 env 代理、鉴权判断与写法、HTTP vs SOCKS5 原理）为时效性稳定内容，无过时项。
- 4.1（compose 重建）为正确做法，保留。

## 资料来源（共享来源库 source_bank.md）

- **S8**：Docker Desktop 忽略 daemon.json 代理，须用 Settings → Resources → Proxies（官方，2026）。
- **S9**：Linux daemon 用 systemd drop-in 设 HTTP_PROXY/HTTPS_PROXY/NO_PROXY，只影响 pull/build（官方，2026）。
- **S10**：容器/构建代理用 ~/.docker/config.json 的 proxies.default（官方，2026）。

## 覆盖风险

- destination_mode = project-output-only，原文件 `docker/docker进行代理.md` 不会被改动，零覆盖风险。
- 输出：`updates/proxy/updated_note.md`。
