# Environment Variables (.env) 规范

## 文件命名与用途

| 文件 | 用途 | 提交 Git |
|------|------|----------|
| `.env` | 默认环境变量 | ❌ |
| `.env.local` | 本地覆盖（个人） | ❌ |
| `.env.development` | 开发环境 | ✅ |
| `.env.production` | 生产环境 | ✅ |
| `.env.example` | 变量文档/模板 | ✅ |
| `.env.*.local` | 环境特定本地覆盖 | ❌ |

## 安全规则

1. **永远不提交** `.env`、`.env.local`、`.env.*.local`
2. **禁止**在代码中硬编码密钥、Token、密码
3. **禁止**在日志中打印环境变量值
4. `.env.example` 中用占位符代替真实值（如 `sk-xxxxx`）

## 路径规范

1. **禁止**在代码中硬编码绝对路径（如 `/Users/xxx/data/`、`C:\Users\xxx\`）
2. **文件路径**应通过 `.env` 中的环境变量定义，使用相对路径（如 `./workspace`）
3. **示例**：路径变量统一在 `.env` 中管理，代码中通过 `process.env.WORKSPACE_PATH` + `path.resolve()` 引用
4. **自动配置**：运行项目时，路径基于当前工作目录自动解析，无需手动设置绝对路径

## 变量命名

```bash
# 格式：大写下划线，前缀表示作用域
APP_NAME=study-system
APP_PORT=3000

# API 密钥加前缀
API_KEY=sk-xxxxx
MINIMAX_API_KEY=xxxxx

# 数据库
DATABASE_URL=postgresql://localhost:5432/mydb

# 路径（相对路径，不硬编码绝对路径）
WORKSPACE_PATH=./workspace
NOTES_OUTPUT_PATH=${WORKSPACE_PATH}/output
CHAPTERS_PATH=${WORKSPACE_PATH}/chapters

# 布尔值用小写
DEBUG=true
FEATURE_X_ENABLED=false
```

## .env.example 模板

```bash
# === Application ===
APP_NAME=study-system
APP_PORT=3000
NODE_ENV=development

# === Paths (relative to project root) ===
# 所有路径基于项目根目录，不要使用绝对路径
WORKSPACE_PATH=./workspace
NOTES_OUTPUT_PATH=${WORKSPACE_PATH}/output
CHAPTERS_PATH=${WORKSPACE_PATH}/chapters

# === API Keys ===
# Get from: https://platform.minimax.io
MINIMAX_API_KEY=your-key-here

# === Debug ===
DEBUG=false
```

## 代码中使用

```javascript
// Node.js
const apiKey = process.env.API_KEY;

// 必需变量启动时校验
const required = ['API_KEY', 'DATABASE_URL'];
for (const key of required) {
  if (!process.env[key]) {
    throw new Error(`Missing required env: ${key}`);
  }
}

// 路径解析：使用 path.resolve 相对路径
const path = require('path');
const workspacePath = path.resolve(process.env.WORKSPACE_PATH);
const outputPath = path.resolve(process.env.NOTES_OUTPUT_PATH);
```

## .gitignore 确保覆盖

```gitignore
# 已配置
.env
.env.local
.env.*.local
```

## 检查清单

- [ ] `.env` 在 `.gitignore` 中
- [ ] `.env.example` 提交到仓库（无真实密钥）
- [ ] 敏感变量命名带 `_KEY`、`_SECRET`、`_TOKEN` 后缀
- [ ] 启动时校验必需变量
- [ ] 不在 `console.log` 中打印环境变量
- [ ] 文件路径通过环境变量配置，不硬编码绝对路径
