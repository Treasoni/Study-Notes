# Windows 文件系统、注册表与 PowerShell - 意图文件

## 基本信息

- **主题**: Windows 文件系统、注册表与 PowerShell
- **项目标识**: windows-file-system-registry-powershell
- **运行标识**: windows-file-system-registry-powershell
- **工作流**: learning-note-flow
- **创建时间**: 2026-09-10
- **当前阶段**: 阶段 0（意图澄清）
- **输出目标**: project-output
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
概念笔记 + 实战笔记（兼重）

- 概念笔记：讲清原理与结构，建立心智模型
- 实战笔记：给出可复制的命令清单与操作步骤

### 学习深度
入门

### 用户基础
零基础（从概念讲起，术语先解释再使用）

### 组织方式
文件系统 / 注册表 / PowerShell 三个主题并列、各自成章，最后一章串联三者（用 PowerShell 操作文件系统与注册表）。

## 研究计划

### 探索方向
1. Windows 文件系统：驱动器与盘符、目录结构、路径规则、NTFS 特性与权限
2. Windows 注册表：Hive / 键 / 值结构、常见路径、读取、修改与备份
3. Windows PowerShell：Cmdlet、对象管道、提供程序、脚本基础
4. 三者串联：用 PowerShell 查询与操作文件系统、注册表

### 重点收集
- **核心概念**:
  - 盘符与卷、挂载点、目录层次（系统目录 vs 用户目录）
  - 路径规则：绝对/相对路径、UNC 路径、长路径限制、环境变量展开
  - NTFS 关键特性：ACL 权限、文件属性、备用数据流、硬链接与符号链接
  - 注册表：5 个根键、Hive 文件位置、键/子键/值（字符串、DWORD、QWORD、二进制）
  - PowerShell：对象模型、管道、Cmdlet 动词-名词命名、Provider 与 PSDrive、执行策略、版本差异
- **实战代码**:
  - 文件/目录浏览、查找、复制、移动、批量重命名
  - 磁盘与卷信息查询、空间占用分析
  - 注册表读取、新建、修改、导出备份
  - 常用 Cmdlet 与管道组合（Where-Object / Select-Object / ForEach-Object）
- **常见坑**:
  - 权限不足（管理员 vs 标准用户，UAC）
  - 路径含空格、中文、超长路径的处理
  - 执行策略（ExecutionPolicy）阻止脚本运行
  - 误改注册表导致系统异常，以及修改前的备份意识
  - 控制台编码与中文输出乱码
  - Windows PowerShell 5.1 与 PowerShell 7 的差异
- **工具链**:
  - 文件资源管理器、命令提示符（cmd）、Windows 终端
  - Windows PowerShell 5.1 / PowerShell 7（pwsh）
  - 注册表编辑器（regedit）、注册表命令行工具（reg）
  - 磁盘管理、任务管理器、系统信息工具
  - 内置帮助：Get-Help / Get-Command / Get-Member

### 信源偏好
- 官方文档: 是（优先 Microsoft Learn）
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 零基础读者：每个新术语首次出现时先解释含义与用途，再给命令。
- 命令示例需标注执行位置（cmd / PowerShell / 注册表编辑器）和是否需要管理员权限。
- 涉及注册表修改的内容必须包含备份与回滚步骤。
- 未指定 Obsidian 位置前，所有产物先保存在项目工作区，最终笔记落到 `workspace/output/final_note.md`。
