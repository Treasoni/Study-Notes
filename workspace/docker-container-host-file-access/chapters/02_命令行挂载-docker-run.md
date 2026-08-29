## 第 2 章：命令行挂载：docker run -v 与 --mount

上一章定了选型判据：容器要直接读写宿主机路径，就走 bind mount。本章落地到命令行，讲 `docker run` 的两种写法——简写 `-v` 和显式 `--mount`，以及它们的关键差异。读完你能写出带只读、自动建目录等选项的正确挂载命令，也知道官方明确警告过的坑。

### 2.1 `-v`：冒号分隔、顺序固定

`-v` 是简写，语法是冒号隔开的三段、顺序固定：`host:cont[:opts]`——宿主路径、容器路径、可选项 [S1]。顺序不能换，但可选项可以省略。

```bash
# 把当前目录下的 data 挂到容器 /app/data，默认可写
docker run -v "$(pwd)/data":/app/data alpine ls /app/data
# 输出 /app/data 下的文件列表（目录为空则无输出）
```

`opts` 常见值：`ro`（只读）、`z`/`Z`（SELinux 标签，第 5 章细讲）、bind propagation。只读示例：

```bash
# 宿主配置目录只读挂入，容器内只能读
docker run -v "$(pwd)/config":/app/config:ro nginx
```

### 2.2 `--mount`：key=value、顺序无关

`--mount` 用逗号分隔的 key=value 键值对，**顺序无关**，且必须显式声明 `type`。bind 类型用 `src`/`dst`（也可写 `source`/`target`）[S1]。

```bash
# 与上面 -v 等价：type=bind + src 宿主路径 + dst 容器路径
docker run --mount type=bind,src="$(pwd)/data",dst=/app/data alpine ls /app/data
# 输出与 -v 示例一致

# 只读 + 源目录不存在时自动创建
docker run --mount type=bind,src="$(pwd)/logs",dst=/app/logs,readonly,bind-create-src=true alpine ls /app/logs
```

> [!tip] 大白话
> 把 `-v` 想成发固定格式短信——`收件人:内容:备注`，顺序不能乱；把 `--mount` 想成填带标签的表格——`姓名=张三`，先填哪格都行。所以字段一多，`--mount` 更不容易写错，这也是官方推荐它的原因。

### 2.3 官方推荐与四个必记的坑

官方文档明确推荐 `--mount`：它更显式、支持全部选项（如 `bind-create-src`、`bind-propagation`），`-v` 只覆盖常用子集。简单场景用 `-v` 没问题，复杂场景优先 `--mount` [S1]。

1. **自动建目录的差异**：`-v` 的源路径不存在时会**自动当成目录创建**；`--mount` **默认报错**，要显式加 `bind-create-src=true` 才创建 [S1]。
2. **`dst` 必须是绝对路径**：容器侧目标路径不写绝对路径会直接报错；`src` 才允许相对路径 [S1]。
3. **bind 绑定的是 daemon 所在主机**：`docker run` 是本地命令，真正挂载动作由 daemon 执行。用远程 daemon（如 `DOCKER_HOST=ssh://...`）时，`src` 解析的是**远程主机**路径，不是你的客户端路径 [S1]。
4. **`bind-propagation` 仅 Linux**：它控制子挂载点的联动，默认 `rprivate`，仅 bind 可配、仅 Linux 生效，Docker Desktop（macOS/Windows）不支持 [S1]。

> [!tip] 大白话
> 把 `ro` 想成图书馆样本书——只能看不能改。挂载加 `ro` 后，容器进程改不了宿主文件，是对第 1 章"bind 默认可写"风险最直接的缓解。

### 本章小结

- 命令行 bind 挂载有两种写法：`-v host:cont[:opts]`（顺序固定）与 `--mount type=bind,...`（key=value 顺序无关）[S1]。
- 官方推荐 `--mount`，更显式、支持全部选项；`-v` 适合简单场景 [S1]。
- 只读挂载：`-v ...:ro` 或 `--mount ...,readonly`。
- 四个坑：`-v` 自动建目录 vs `--mount` 默认报错；`dst` 必须绝对；远程 daemon 绑远程路径；`bind-propagation` 仅 Linux、Docker Desktop 不支持 [S1]。

下一章进入 Compose：同样的挂载用 `volumes:` 怎么写，长短语法与顶层声明又对应哪些坑。
