# 更新报告

## 笔记信息
- **标题**: Claude Code 使用指南
- **路径**: `AI学习/Claude Code 教程/01-入门/如何使用Claude code.md`
- **前次更新**: 2026-07-12
- **本次更新**: 2026-07-31

## 更新摘要

| 类型 | 内容 | 说明 |
|------|------|------|
| 🔄 更新 | frontmatter `updated` | 2026-07-12 → 2026-07-31 |
| ➕ 新增 | 0️⃣ 国内网络安装（重点） | 放在「快速安装」最前，含需放行域名表 + 4 个方案 |
| ➕ 新增 | 方案 A 终端代理 + 官方安装器 | 幂等原生安装器 + 代理示例，链接到代理配置/FAQ |
| ➕ 新增 | 方案 B npm + npmmirror | 无代理首选；原理（壳包+平台子包）、Node 22+、镜像安装命令、native binary 修复、手动升级 |
| ➕ 新增 | 方案 C Homebrew | stable / `@latest` 双 cask，国内镜像说明 |
| ➕ 新增 | 方案 D GitHub 加速 / 社区脚本 | cc-download、claude-code-bootstrap |
| 🔄 更新 | 版本号注记 | v2.1.207 → v2.1.220（latest）/ v2.1.212（stable），npm registry 实测确认 |
| 🔄 更新 | 其他安装方式表 npm 行 | 「已废弃」→「官方仍支持，国内无代理首选」；新增 Linux apt/dnf/apk 行 |
| 🔄 更新 | 前置依赖 Node.js | v18+ → **22+**（v2.1.198 起，官方文档确认） |
| ➕ 新增 | FAQ：native binary not installed | 镜像未同步平台包 / postinstall 未执行的排查与修复 |
| ➕ 新增 | 更新记录 | 追加更新历史 |

## 关键事实核对
- **npm 安装未废弃**：官方文档（code.claude.com/docs/en/setup）仍将 `npm install -g @anthropic-ai/claude-code` 列为 Advanced installation options。
- **Node.js 22+**：官方文档「As of v2.1.198, the npm package requires Node.js 22 or later」。
- **npmmirror 已同步平台包**：实测 `registry.npmmirror.com/@anthropic-ai/claude-code-win32-x64` 存在，dist-tags.latest = 2.1.220，modified 2026-07-25。
- **最新版本**：npm registry 实测 latest = 2.1.220，stable = 2.1.212。
- **壳包机制**：主包为分发壳包，二进制在 8 个平台 optionalDependencies 子包中，postinstall（install.cjs）替换 stub。

## 未处理事项
- 版本号是动态值，建议用户以 `claude --version` 自检为准。
- 第三方加速前缀（`gh-proxy.com` 等）与服务（cc-download、claude-code-bootstrap）会随时间变化，使用前自行确认。

## MOC 同步
- **MOC 文件**: `AI学习/Claude Code 教程/Claude Code MOC.md`、`AI学习/00-索引/AI学习 MOC.md`
- **操作**: 索引条目描述「安装、免登录、配置、日常速查、记忆系统」仍准确，无需修改。

## 资料来源
- [Claude Code 官方 Setup 文档](https://code.claude.com/docs/en/setup)
- [npmmirror registry - @anthropic-ai/claude-code](https://registry.npmmirror.com/@anthropic-ai/claude-code)
- [npm 官方 registry - @anthropic-ai/claude-code](https://registry.npmjs.org/@anthropic-ai/claude-code)
- [ipfred/cc-download](https://github.com/ipfred/cc-download)
- [ErgeAIA/claude-code-bootstrap](https://github.com/ErgeAIA/claude-code-bootstrap)
- [Claude Code 国内安装配置完整指南（2026 版）](https://segmentfault.com/a/1190000047828859)
