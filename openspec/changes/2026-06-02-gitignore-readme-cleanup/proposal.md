# Proposal: Gitignore 与 README 清理

## 问题描述

当前 `.gitignore` 配置不完善：
- 缺少对开发流程文件的排除（openspec changes、comet 状态、codegraph 索引等）
- 一些被注释掉的规则说明之前有过调整但未最终确定
- `docs/superpowers/` 下的开发产物（plans/specs/reports）未被排除

`README.md` 虽然内容丰富，但：
- 缺少清晰的快速开始指引（安装步骤可以更简洁）
- 目录结构说明可以更直观
- 对新用户来说，前置依赖和配置步骤不够突出

## 根因分析

1. `.gitignore` 在项目演进过程中逐步添加规则，未系统性地区分"用户工作文件"和"开发流程文件"
2. `README.md` 早期版本侧重功能介绍，未针对新用户做 onboarding 优化

## 修复目标

1. **`.gitignore`**：明确分离 tracked 和 ignored 文件，排除所有开发流程产物
2. **`README.md`**：重写为面向新用户的快速上手指南，突出安装、配置、使用三个核心步骤
