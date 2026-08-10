# Environment Variables (.env) 规范
---
paths:
  - ".claude/scripts/check-env-template.sh"
---


本规则用于让 agent 根据当前项目生成、更新和审计环境变量模板。默认目标：“最小必要、可解释、可复制、安全”，不把所有可能用到的服务都塞进 `.env.example`。

权威参考：模板见根目录 `.env.example`；自检脚本 `.claude/scripts/check-env-template.sh`（`--strict` 会额外把未被引用的模板变量视为失败）。

## 文件命名与用途

| 文件 | 用途 | 提交 Git |
|------|------|----------|
| `.env` | 默认环境变量 | ❌ |
| `.env.local` | 本地覆盖（个人） | ❌ |
| `.env.development` | 可共享的开发默认值，不含密钥 | ✅（仅非敏感值） |
| `.env.production` | 生产环境变量清单，不含密钥 | ✅（仅非敏感值） |
| `.env.example` | 变量文档/模板 | ✅ |
| `.env.*.local` | 环境特定本地覆盖 | ❌ |

## Agent 处理流程

1. **识别项目类型**：读根目录入口（`package.json`、`pyproject.toml`、`Cargo.toml`、`go.mod`、`Dockerfile`、`README.md`、`CLAUDE.md`）。
2. **扫描真实引用**：`rg` 查 `process.env.` / `import.meta.env` / `PUBLIC_` / `VITE_` / `os.getenv` / `${VAR}` / `*_API_KEY` / `DATABASE_URL`，默认排除 `.git/`、`.claude/`、`node_modules/`、`dist/`、`build/`、`workspace/`。
3. **分类变量**：Project、Runtime、Paths、Auth、Database、Cache、Storage、LLM、Observability、Feature Flags、Deployment。
4. **只保留项目需要的变量**：未用到的服务变量不默认加入；可选集成放 Optional 区块且留空。
5. **标注必填与来源**：必填变量注释说明用途与获取来源；敏感变量只放空值或 `your-...-here`。
6. **路径自适应**：项目内路径默认相对项目根；只有用户明确要发布到外部目录时才在本地 `.env` 写绝对路径。
7. **同步规则**：修改 agent 专属规则、skills 或检查脚本后，按项目既有的同步与验证规则执行。

## 安全规则

1. **永远不提交** `.env`、`.env.local`、`.env.*.local`
2. **禁止**在代码中硬编码密钥、Token、密码
3. **禁止**在日志中打印环境变量值
4. `.env.example` 只写空值或不可用占位符（如 `your-key-here`）
5. **禁止**把生产域名、内部服务地址、个人目录或 vault 绝对路径写进共享模板，除非本来就是公开配置
6. 变量名含 `KEY`、`SECRET`、`TOKEN`、`PASSWORD`、`PRIVATE`、`DSN` 时，默认视为敏感

## 路径规范

1. **禁止**在代码中硬编码绝对路径（如 `<home>/data/`）
2. 文件路径通过 `.env` 环境变量定义，使用相对路径（如 `./workspace`）
3. 运行时基于当前工作目录自动解析（`path.resolve(process.env.WORKSPACE_PATH)`），不手动设置绝对路径
4. 外部发布路径（Obsidian vault、云盘同步目录）只写入本地 `.env`，不写入 `.env.example` 真实值

## 变量命名

- 大写下划线、前缀表作用域：`APP_*`、`WORKSPACE_PATH`、`OUTPUT_PATH`
- API 密钥加供应商前缀：`OPENAI_API_KEY`、`MINIMAX_API_KEY`
- 布尔值用小写：`DEBUG=true`、`FEATURE_X_ENABLED=false`

## .env.example 模板

```bash
# === Project Identity ===
APP_NAME=study-system
APP_ENV=development
NODE_ENV=development
APP_PORT=3000
APP_URL=http://localhost:3000

# === Workspace Paths ===
# Paths are relative to the project root.
WORKSPACE_PATH=./workspace
OUTPUT_PATH=${WORKSPACE_PATH}/output
CHAPTERS_PATH=${WORKSPACE_PATH}/chapters
WORKFLOW_RUNS_PATH=${WORKSPACE_PATH}/workflow-runs

# Optional external publishing.
OBSIDIAN_VAULT_PATH=
OBSIDIAN_NOTES_DIR=
OBSIDIAN_MOC_PATH=

# === Runtime Behavior ===
LOG_LEVEL=info
DEBUG=false
DRY_RUN=false
AUTO_CONFIRM=false
CODEX_AUTO_GIT=0
CODEX_AUTO_GIT_PUSH=0

# === LLM / Research Providers ===
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
MINIMAX_API_KEY=
DEFAULT_LLM_PROVIDER=
DEFAULT_LLM_MODEL=

# === Optional Services ===
DATABASE_URL=
REDIS_URL=
SENTRY_DSN=
```

## 更新 `.env.example` 的判断标准

- 新变量必须能追溯到代码引用、脚本引用、工作流需要或用户明确要求。
- 删除变量前先确认没有引用点，避免破坏部署。
- 可选集成变量默认空值；必填变量用注释说明什么时候需要填写。
- 前端框架（Vite、Next.js、Nuxt、Expo）只有可暴露到浏览器的变量才能用 `PUBLIC_` / `VITE_` / `NEXT_PUBLIC_` 前缀。
- dotenv 不支持 `${VAR}` 展开时，不要依赖变量嵌套；改用完整相对路径或在启动脚本中解析。
- 每次变更后检查 `.gitignore` 覆盖真实 `.env`（`.env`、`.env.local`、`.env.*.local`）。

## 检查清单

- [ ] `.env` 在 `.gitignore` 中
- [ ] `.env.example` 提交到仓库（无真实密钥）
- [ ] 敏感变量命名带 `_KEY`、`_SECRET`、`_TOKEN` 后缀
- [ ] 启动时校验必需变量
- [ ] 不在 `console.log` 中打印环境变量
- [ ] 文件路径通过环境变量配置，不硬编码绝对路径
- [ ] `.env.example` 只包含当前项目真实需要或明确可选的变量
- [ ] agent 已先扫描项目栈和 env 引用，再改模板
- [ ] `.claude/scripts/check-env-template.sh` 通过
