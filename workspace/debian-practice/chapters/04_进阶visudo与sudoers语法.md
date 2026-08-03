# 第 4 章：进阶——visudo 与 sudoers 语法

**结论先行**：第 3 章用的是「入组即授权」——把用户丢进 sudo 组，套用现成的宽泛规则。但生产环境往往需要更细的控制：只让某个部署用户能 reload nginx，而不给它整个 root。这一切都要改 sudoers，而 sudoers 是「改错一行就全盘崩溃」的配置文件。本章讲清楚为什么必须用 visudo、sudoers 的条目语法、片段文件，以及改完如何校验。

## 4.1 为什么必须用 visudo

sudo 启动时会读取 `/etc/sudoers` 并逐行解析。如果文件里有语法错误，sudo 会认为整个配置非法而拒绝工作——结果是**所有用户的 sudo 全部失效** [DigitalOcean — How To Edit the Sudoers File](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)。

visudo 是 sudo 官方提供的 sudoers 专属编辑器，提供三重保障：

| 保障 | 作用 |
|------|------|
| 排他锁 | 同一时刻只允许一个管理员编辑，防止并发写入互相覆盖 |
| 保存时语法校验 | 编辑无效时拒绝保存，并保留上一可用版本 |
| 语法错误回滚 | 已保存但解析失败时，自动回滚到备份，不至于锁死 |

对比：用 vim/nano 直接编辑 `/etc/sudoers`，保存退出后如果语法错了，sudo 直接罢工，而你可能已经退出了唯一能提权的会话——被锁在 sudo 之外 [Baeldung — Guide to Linux visudo Command](https://www.baeldung.com/linux/visudo-command-tutorial)。

> **核心规则：任何时候都不要用 vim/nano 直接编辑 `/etc/sudoers`，只经 visudo。** visudo 会调用系统默认编辑器（Debian 上是 nano），想换成 vim 只需 `export EDITOR=vim`。

## 4.2 sudoers 条目格式

sudoers 一条规则的基本格式：

```text
user host=(runas:runas) command
```

| 字段 | 含义 | 说明 |
|------|------|------|
| `user` | 授权对象 | 用户名、`%组名` 或别名 |
| `host` | 主机范围 | `ALL` = 任意主机 |
| `(runas:runas)` | 以谁的身份执行 | `用户:组`；省略默认以 root 执行 |
| `command` | 允许的命令 | 必须写**绝对路径** |

**`%` 前缀表示组，无 `%` 是用户**。两个典型示例 [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)：

```text
myuser  ALL=(ALL:ALL) ALL
%deploy ALL=(root) NOPASSWD: /usr/bin/systemctl reload nginx
```

逐条解读：
- `myuser ALL=(ALL:ALL) ALL`：用户 `myuser` 可在任意主机、以任意用户身份（含 root）执行任意命令，需要密码。这就是第 3 章 `%sudo` 规则的单用户版。
- `%deploy ALL=(root) NOPASSWD: /usr/bin/systemctl reload nginx`：`deploy` 组的成员可在任意主机、**只**以 root 身份执行 `/usr/bin/systemctl reload nginx` 这一条命令，且免密。

命令必须写绝对路径：`/usr/bin/systemctl reload nginx`，而不是 `systemctl reload nginx`，否则 sudo 无法匹配命令 [Baeldung](https://www.baeldung.com/linux/visudo-command-tutorial)。

**别名**：规则变多时可把命令、用户分组。别名定义以 `_Alias` 结尾，名字全大写 [Baeldung](https://www.baeldung.com/linux/visudo-command-tutorial)：

```text
Cmnd_Alias OPS = /bin/systemctl reload nginx, /bin/systemctl status nginx
User_Alias DEV = zhq, alice

%DEV  ALL=(root) OPS
```

**主机限制**：`host` 字段可写具体主机名，规则只在对应主机生效，如 `zhq webserver01=(ALL) ALL` [Baeldung](https://www.baeldung.com/linux/visudo-command-tutorial)。

> 注意：sudoers 从上到下读取，冲突时**最后匹配的规则生效** [RHEL9 — 管理 sudo 访问](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/managing-sudo-access_configuring-basic-system-settings)。这就是为什么第 6 章会讲到片段文件可能「覆盖」主配置——后面的规则盖住前面的。

## 4.3 片段文件 `/etc/sudoers.d/`

官方建议：本地定制规则放 `/etc/sudoers.d/` 下的新文件，而不是直接改主文件——系统更新期间能保留、也更好修 [RHEL9](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/managing-sudo-access_configuring-basic-system-settings)。Debian 同样支持。

用 visudo 定向编辑片段文件：

```bash
sudo visudo -f /etc/sudoers.d/99-custom-ops
```

文件名规范（**来源：sudoers(5) man page / Debian 打包约定**，非博客正文）：
- **文件名不得含点 `.`**，如 `99.custom` 会被忽略。
- **不得以 `~` 结尾**，编辑器备份如 `99-custom-ops~` 会被忽略。
- 建议前缀数字控制加载顺序，如 `99-custom-ops`。

**权限要求（来源：sudoers(5) man page / Debian 打包约定）**：mode `0440`、属主 `root:root`。权限不对（例如组/其他用户可写）sudo 会拒绝读取：

```bash
chown root:root /etc/sudoers.d/99-custom-ops
chmod 0440 /etc/sudoers.d/99-custom-ops
```

片段能生效的前提是主文件里有 `#includedir /etc/sudoers.d`。注意这一行的 `#` 是**语法的一部分，不是注释**——不要把它当成注释删掉 [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)。向该目录添加新片段即生效，无需重启服务。

## 4.4 校验与验证命令

改完配置，按下面这条链走一遍，避免把坏语法留到下次：

```bash
sudo visudo -c        # 语法校验，确认 parsed OK
sudo -k               # 清空凭据缓存，强制下次重新认证
sudo -v               # 预验证：做一次模拟 sudo，刷新凭据租约
sudo -l               # 列出当前用户的有效规则
```

预期输出：

```text
$ sudo visudo -c
/etc/sudoers: parsed OK

$ sudo -l
User zhq may run the following commands on host:
    (ALL : ALL) ALL
```

如果语法出错，`visudo -c` 会精确定位到行 [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)：

```text
>>> /etc/sudoers.d/99-custom-ops: syntax error near 'ALL'  <<<
```

想看**指定用户**被允许哪些命令，用 `-U`，无需切换到那个用户 [Baeldung](https://www.baeldung.com/linux/visudo-command-tutorial)：

```bash
sudo -l -U deploy
```

输出 `deploy` 用户能执行的规则列表。

## 本章小结

- sudoers 一个语法错误会让全部 sudo 失效，所以只经 visudo 编辑：排他锁 + 保存时校验 + 回滚三重保障。
- 规则格式 `user host=(runas:runas) command`；`%` 是组、无 `%` 是用户；命令必须绝对路径；省略 `(runas)` 默认以 root 执行。
- 用 `Cmnd_Alias` / `User_Alias` 分组、用 host 字段做主机限制；规则冲突时最后匹配的生效。
- 本地定制放 `/etc/sudoers.d/`：文件名不得含 `.`、不得以 `~` 结尾，权限 0440 root:root（来源 sudoers(5) / Debian 打包约定）；`#includedir` 的 `#` 是语法不是注释。
- 改完用 `sudo visudo -c` 校验，验证链 `sudo -k` → `sudo -v` → `sudo -l`；查指定用户用 `sudo -l -U <user>`。

下一章把语法里的 `NOPASSWD:` 展开：哪些场景值得免密、哪些必须避免。
