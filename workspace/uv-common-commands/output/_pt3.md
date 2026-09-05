### §2.6 `uv lock` —— 只解析、不安装

**用途**：只做依赖解析并更新 `uv.lock`，**不碰 `.venv`**（不安装）；用于「升级某包 / 预先锁定版本」而不想立刻动环境的时候 [^c2-07]。

```bash
uv lock                               # 首次生成 uv.lock；依赖没变则空跑
uv lock --upgrade-package requests    # 只把 requests 升到最新兼容版，其余锁不变
uv lock --upgrade                     # 全部依赖一起升到最新兼容
```

**常用参数 / 注意点**：

- 解析时把现有 `uv.lock` 内容当作**偏好**：所以依赖没变时 `uv lock` 是无操作的，除非给 `--upgrade` / `--upgrade-package` [^c2-07]。
- **升级单包用 `--upgrade-package requests`**（`-P requests`），它只动这一个包，保持 lock 其余部分不动——这是"我想升 requests 又不想连带升别的"的正解 [^c2-02][^c2-07]。
- **日常不必手跑**：`uv add` / `uv sync` / `uv run` 在需要时都会自动 re-lock。手跑 `uv lock` 的典型时机是：单独升级、或在 CI 前预生成/预检 lock。
- 参数上的 `--locked`（`--check`）断言 lock 已最新、不一致即报错；`--frozen` 只断言存在、不查是否最新 [^c2-07]。
- **坑 3 回顾：`uv.lock` 提交 Git、勿手改**（详见 §2.1）。它属于"生成物 + 复现依据"双重身份，是项目里唯一要提交的"产物文件"。

> [!tip] 大白话
> `uv lock` 只负责**给购物清单算账出物流单**，不负责搬货。平时 `uv add`/`uv sync` 顺手就把账算了，所以你不常单独喊它；只有当你想"只把某一个快递升级到最新、其他都不动"时，才专门找它。

### §2.7 `uv tree` / `uv export` —— 查看与导出

**`uv tree`：查看依赖树**——回答"我到底装了什么、谁依赖谁"。

```bash
uv tree                    # 全量树（重复出现的包默认折叠为 *）
uv tree -d 2               # 只看两层（--depth N）
uv tree --invert requests  # 反查：谁依赖了 requests（--reverse 同义）
uv tree --package requests # 只看某包的子树
```

- 深度默认 255（即全展开）；`-d` 控制层数，树大了先限深 [^c2-08]。
- `--invert` 用来做「依赖归因」：想知道升级某包会影响谁、或排查谁悄悄拖进了某个传递依赖时很好用 [^c2-08]。
- `--format json` 可输出机器可读的树（默认 `text`）[^c2-08]。

**`uv export`：导出 lock 为其他格式**——把 `uv.lock` 转成 `requirements.txt` / `pylock.toml`(PEP 751) / CycloneDX v1.5 JSON [^c2-09]。

```bash
uv export -o requirements.txt              # 默认格式 requirements.txt
uv export --frozen -o requirements.txt     # 跳过 re-lock，照现有 lock 导出
```

- **默认先 re-lock**：export 与 sync 一样，默认会先重新解析一遍项目；加 `--locked` 或 `--frozen` 可跳过。只读/快速导出用 `--frozen`（lock 缺失会报错）[^c2-09]。
- `-o` / `--output-file` 指定输出文件；不写 `-o` 则打到 stdout（方便管道）[^c2-09]。
- 产物典型用途：把 requirements.txt 交给不用 uv 的同事/旧部署（`pip install -r requirements.txt`），或用 `--format cyclonedx-json` 做依赖清单审计。
- workspace 里默认导出根项目，可用 `--package` 指定成员 [^c2-09]。

> [!tip] 大白话
> `uv tree` 是**看仓库货架图**：谁压在谁上面一目了然；`uv export` 则是把 uv 的"精确物流单"翻译成外面 pip 世界也认得的旧式单据——给还没用 uv 的人看。

### §2.8 本族常用场景组合

三个高频组合，覆盖「日常循环 / 彻底重建 / 复现拉取」三类需求（完整的 14 条"我要…"清单在第 7 章，那里只给跳转锚点、不重复参数）。

**① 日常循环：`uv add` + `uv run`（自动同步，最省事）**

```bash
uv add flask
uv run flask run -p 3000    # 加完即用：免 activate、免手动 uv sync
```

改 `pyproject.toml` 里的依赖后直接 `uv run` 也一样——run 前会自动补齐 sync。

**② 彻底重建环境：`rm -rf .venv && uv sync`（坑 2 的正解）**

```bash
rm -rf .venv                # Windows PowerShell: Remove-Item -Recurse -Force .venv
uv sync                     # 按 uv.lock 全新安装，环境"脏了/坏了"就这招
```

`.venv` 不是宝贝，只是安装现场；依赖全在 `uv.lock` 里，删了重建几乎无损。

**③ 复现拉取 / CI：`uv sync --locked`**

```bash
git clone <repo> && cd <repo>
uv sync --locked    # 断言 lock 最新后精确同步（CI 用；详见附录 B）
uv run pytest
```

`uv.lock` 已提交 Git，clone 下来就能用 `--locked` 得到与开发机一致的环境；lock 与 `pyproject.toml` 不同步时它会立刻报错——这正是 CI 想要的防呆。只想"照 lock 装、别啰嗦校验"时用 `uv sync --frozen`。

**小结一句口诀**：日常 `add` + `run`；弄脏了 `rm -rf .venv && uv sync`；要复现 `sync --locked`。

---

**本章小结**

- 四个文件一条链：`pyproject.toml` + `.python-version`（声明）→ `uv.lock`（锁定）→ `.venv`（安装现场）；`uv.lock` 提交 Git、勿手改，`.venv` 可删可重建。
- `uv init` 只搭骨架，`.venv` 与 `uv.lock` 在首次 `run`/`sync`/`lock` 时惰性创建；目标已有 `pyproject.toml` 会报错。
- `uv add`/`uv remove` 是"改声明三连"（pyproject + lock + 环境）；支持版本约束、git 源、`-r`、`--dev`、`--editable`、`--upgrade`。
- `uv run` 免 activate、跑前自动同步，但默认不清多余包；`uv sync` 默认 exact 会删多余包，`--locked`（防呆断言）与 `--frozen`（只读照 lock）语义相反。
- `uv lock` 只解析不安装，升级单包用 `--upgrade-package`；`uv tree` 看依赖树，`uv export` 转 requirements.txt/CycloneDX。

下一章进入本手册第二个命令族：`uv python` / `uv venv`（第 3 章）——`.python-version` 从哪来、怎么装指定版本的解释器、`.venv` 怎样手动创建与激活，正好补上本章留的"解释器"缺口。

