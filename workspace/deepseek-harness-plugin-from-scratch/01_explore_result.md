---
topic: DeepSeek-Harness 从零写插件（空目录手写全文件）
run_id: deepseek-harness-plugin-from-scratch
created: 2026-08-15
status: confirmed
---

# 01 探测结果（P1）

> 三个 lens 并行探测：①工程骨架 ②工具 DSL ③打包安装验证。已按 canonical URL 去重。

## 方向菜单

| 方向 | 写法 | 适合 |
|------|------|------|
| **A. 渐进式从零（推荐）** | 空目录先写「最小 2 文件」（my-plugin.ts + cordis.yml）让插件被加载 → 再补 package.json / tsconfig / 工具文件，把它变成可打包工程。官方 `Your first plugin` 路线 + 工程化补齐 | 最贴「从零开始」直觉：先看到它跑起来，再一步步长大 |
| **B. 六文件一次成型** | 按 example-plugin 的 6 文件清单（package.json / tsconfig / src/index.ts / src/tools/git-log.ts / dev-cordis.yml / cordis.patch.yml）从空目录逐一手写，一次建全 | 喜欢「完整工程结构」一次到位的读者 |
| **C. 打包优先** | 不纠结工程结构，最快写出能 bundle 的插件，重点砸在打包安装链路 | 只想尽快产出可复用插件的读者 |

## 候选来源（去重后）

### 官方（9 个，首选）

| 来源 | 说明 | 分 |
|------|------|----|
| docs/user/develop/basic/index.md（Your first plugin） | 官方从零建插件：2 文件最小骨架即可加载 | 5 |
| docs/cookbook/adding-a-package.md | 从零建包：package.json 不变量、tsconfig、目录布局 | 5 |
| docs/user/develop/basic/publish.md | 打包安装：bundle vs profile、dsh.bundle.patch、git 安装坑 | 5 |
| docs/user/develop/basic/tool.md | defineTool 五件套 + ctx.tools.register / inject | 5 |
| docs/cookbook/adding-a-tool.md | execute() 契约权威：canonical 值 / throw=isError | 5 |
| docs/user/develop/basic/config.md | Config 同名 schema：.default / .required / 响亮失败 | 5 |
| docs/cordis-tutorial/05-config.md | 坏配置 → ValidationError / fiber FAILED | 4 |
| apps/cli/reference/README.md | dsh CLI 全家族：--dump-config / --patch / headless / web | 5 |
| docs/architecture.md | bundle/profile 分层、四层补丁树、整行替换 | 4 |

### 本地 vault（3 个）

| 来源 | 说明 | 分 |
|------|------|----|
| example-plugin/ 脚手架 | 六文件真实内容 + dev/打包双 patch，可反推手写骨架 | 4 |
| 《DeepSeek-Harness 插件实战》 | 已发布分册 = 改造脚手架基线，本册的对照对象 | 4 |
| 《DeepSeek-Harness 配置体系》 | bundle/profile 心智模型 + 最小 bundle 代码 | 3 |

### 社区（线索，P2 按需）

- pingfanfan/hello-dsh（零基础中文实例）
- cnblogs.com/nandanghonghu/articles/22489996（工具插件从开发到真实调用）
- 官方模板 dsh-plugin-onebot / dsh-plugin-template
- vlln/plugin-registry/skills/make-dsh-plugin/SKILL.md

## 覆盖缺口（P2 需落实）

1. **package.json 最小字段**：name/version/main/types/dsh.bundle.patch/scripts.build/prepare 逐行含义（官方 index.md 不覆盖，需 adding-a-package.md + example-plugin 落实）
2. **tsconfig 最小配置**：module/target/outDir/declaration 取值
3. **「四名分离」坑**：export const name（诊断）vs package.json name（包）vs patch id（实例）vs defineTool name（模型可见）——用 publish.md 校准
4. **验证命令链精确语法**：--dump-config 分层 / headless 退出码（0=完成 1=失败）
5. **git 安装 allowBuilds 流程**：pnpm≥10 首 add 拒跑 prepare → 抄包 key 进 allowBuilds 重跑 + #sha 钉 commit
6. **口径差异校准**：本地笔记写「Schemastery 无 .optional()、必填用 .required(true)」，官方 config.md 用裸 .required() —— 以官方为准并标注

## 建议 P2 范围

- 8 个官方 doc（除 architecture 外全部 + index.md）+ 3 个 vault 笔记逐字提取
- 按方向 A 的渐进式结构组织：最小加载 → 工程化 → 打包安装
- 示范工具：git_log（与《插件实战》一致，可对照）
