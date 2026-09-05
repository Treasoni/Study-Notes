## 附录 B GitHub Actions CI 片段

CI 里最容易出问题的往往不是测试本身，而是环境不一致：本地能过、一上 CI 就挂。uv 的思路是把环境声明（`pyproject.toml`）和锁定结果（`uv.lock`）都提交进仓库，让 CI 每次还原出和本地一致的依赖。本附录直接给出可粘贴的最小 workflow，并解释几个在 CI 语境下才显关键的参数（`--locked`、缓存 key、`prune --ci`）。对应速查条目见第 7 章 §7.14。

### B.1 最小 workflow（astral-sh/setup-uv 版）

官方推荐的集成方式是 [`astral-sh/setup-uv`](https://docs.astral.sh/uv/guides/integration/github/) action，它负责安装 uv、加入 PATH、按需安装 Python，并可持久化 uv 缓存[^cb-1]。把下面内容存为 `.github/workflows/ci.yml`：

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1

      - name: Install uv
        uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9 # v9.0.0
        with:
          version: "0.12.10"      # 可选：固定 uv 版本，避免上游更新影响 CI
          enable-cache: true       # 持久化 uv 缓存，缓存 key 默认包含 uv.lock 的哈希
          python-version: "3.12"   # 安装并启用该 Python（会覆盖仓库内 .python-version 的指定）

      - name: Sync locked dependencies
        # 按 uv.lock 精确安装；若 pyproject 声明与 lock 不一致则报错（详见 B.2）
        run: uv sync --locked --all-extras --dev

      - name: Run tests
        # pytest 装在项目 .venv 里，uv run 免激活直接调用
        run: uv run pytest

      - name: Trim uv cache
        # 在 job 结束、缓存回存之前执行，缩小上传体积
        run: uv cache prune --ci
```

要点速读：

- `python-version`：`setup-uv` 会在 runner 上安装该 Python 供本次 job 使用；不加则遵循仓库 `.python-version` / `pyproject.toml` 的 `requires-python`。
- `uv sync --locked --all-extras --dev`：一次装齐普通依赖 + 所有可选 extras + 开发依赖组（pytest 等测试工具一般放在 `dev` 组）[^cb-1][^cb-2]。
- `uv run pytest`：在刚同步出的 `.venv` 里执行测试，不需要手动 `source .venv/bin/activate`。
- `version` 与各 action 的引用都建议固定（见 B.2）。

### B.2 关键点说明

**`--locked` vs `--frozen`（CI 语义）**。`uv sync` 默认会先重新解析（re-lock）再安装；`--locked` 与 `--frozen` 都会跳过 re-lock，但态度不同[^cb-2]：

| 参数 | 行为 | 适合场景 |
| --- | --- | --- |
| `--locked` | 断言 `uv.lock` 与 `pyproject.toml` 声明一致；不一致（漏锁/过期）立即报错 | CI 校验：谁改了依赖却忘了更新 lock，立刻红掉 |
| `--frozen` | 直接把 lock 当唯一事实，只读使用、不核对声明 | 本地想最快复用现成 lock、或明确知道 lock 最新时 |

CI 里优先 `--locked`，因为它把「lock 已同步」变成构建门禁——这正是可复现的根基[^cb-4]。`--frozen` 不检查，跑得快但发现不了漂移。正文参数详解见第 2 章 §2.5、速查见第 7 章 §7.9。

[!tip] 大白话：把 `--locked` 想成「上菜前对账单」——配方单（pyproject）和锁定的成品清单（uv.lock）对不上就拒绝上菜并报错；CI 要的就是它当场喊停。`--frozen` 则是「信清单、不核对」，直接用现有清单做，快，但漏锁不会被发现。

**缓存 key 与 `prune --ci` 的配合**。`setup-uv` 的 `enable-cache: true` 会自动在 job 结束后把 uv 缓存存回 GitHub、下次恢复，缓存 key 默认基于依赖锁定文件生成；若改用 `actions/cache` 手动管理，等价写法是 `key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}`[^cb-1][^cb-3]。意思是：`uv.lock` 没变 → key 命中 → 直接复用缓存的 wheel，省去重新下载/解析。正因如此，**修改依赖后务必重新生成并提交 `uv.lock`**，否则 CI 会一直命中旧缓存（参见坑 3）。

[!tip] 大白话：把 uv 缓存想成「中央食材仓库」，`uv.lock` 的哈希是仓库分柜编号——配方没变，编号就不变，同一柜的食材直接搬来用；配方一变，编号就变，自动开新柜进货，绝不会拿错料。

job 末尾的 `uv cache prune --ci` 则负责「瘦身回存」：它会清掉随时能从网上下回来的预编译 wheel 与解压的 sdist，只保留本地源码编译出的产物（重编最贵）[^cb-3]。放在最后一个 step、趁缓存尚未回存时执行，能让每次写回 GitHub 的缓存体积更小、下次恢复更快。缓存机制详解见第 5 章 §5.1、§5.4。

[!tip] 大白话：`prune --ci` 就像收摊前理仓库——把「网上随时能再下载的半成品」扔掉，只留「本地现做、重做最贵」的东西，让带走（回存）的行李又轻又管用。

**版本固定提示**。示例里 `setup-uv` 的 `version` 与 `uses: owner/repo@<SHA> # vX.Y.Z` 的完整 SHA 都来自官方文档当日快照，属「钉死版本」的推荐做法：action 或 uv 升级不通知你，CI 不会突然被上游改动打破。日常图省事也可把 SHA 换成大版本标签（如 `astral-sh/setup-uv@v9`），代价是失去可复现性，按需取舍。

### B.3 备选：actions/setup-python + python-version-file

若不想让 uv 管理 Python，可改用 GitHub 官方的 `setup-python`——它在 runner 上直接缓存 CPython，冷启动有时更快[^cb-1]。用 `python-version-file` 指向仓库里已固定的 `.python-version`（或 `pyproject.toml`），让两处指定同源、不重复维护：

```yaml
# .github/workflows/ci.yml（仅截取 steps 部分）
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Python
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
        with:
          python-version-file: ".python-version"   # 与 uv python pin 共用同一份指定

      - name: Install uv
        uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9 # v9.0.0
        with:
          version: "0.12.10"
          enable-cache: true

      - name: Sync locked dependencies
        run: uv sync --locked --all-extras --dev

      - name: Run tests
        run: uv run pytest

      - name: Trim uv cache
        run: uv cache prune --ci
```

两种写法的取舍：**一条龙（B.1）** 由 `setup-uv` 同时管 uv 与 Python，配置最集中，适合「信任 uv 全托管」的项目；**拆分（B.3）** 用 GitHub 官方缓存 Python，适合在意冷启动速度、或已有 `setup-python` 历史的仓库。无论哪种，后续的 `uv sync --locked` + `uv run pytest` 与缓存收尾都完全一致，切换成本很低。

---

**本章小结**

- 最小 CI 骨架 = `setup-uv`（可选 `python-version`）→ `uv sync --locked --all-extras --dev` → `uv run pytest` → `uv cache prune --ci`。
- `--locked` 把「lock 与声明一致」变成 CI 门禁；`--frozen` 只读信任现有 lock，不核对。
- `setup-uv` 的 `enable-cache: true` 自动按依赖锁定文件做缓存 key；`prune --ci` 在回存前瘦身，二者配合让缓存又准又轻。
- 版本（action SHA、uv `version`、Python）都建议固定，换取 CI 可复现。

[^cb-1]: astral-sh，*Using uv in GitHub Actions*（官方 GitHub Actions 集成指南）：https://docs.astral.sh/uv/guides/integration/github/
[^cb-2]: astral-sh，*uv CLI Reference —— `uv sync`*（`--locked` / `--frozen` / `--all-extras` / `--dev` 语义）：https://docs.astral.sh/uv/reference/cli/
[^cb-3]: astral-sh，*Caching —— uv cache*（`uv cache prune --ci` 行为）：https://docs.astral.sh/uv/concepts/cache/
[^cb-4]: Real Python，*Python and uv*（以 `--locked` 保证 CI 环境可复现的实战经验）：https://realpython.com/python-uv/
