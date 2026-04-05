---
sortspec-version: 1.0
generated: 2026-04-06
description: Docker 文件夹排序配置
---

# Sortspec - Docker 文件夹

此文件定义了 Docker 文件夹中笔记的排序规则，用于 Obsidian Custom Sort 插件。

## 排序规则

```custom-sort
// 置顶文件
'Docker MOC.md'             // 索引文件置顶

// 按主题分组排序
// 1. 入门安装
'Windows-DockerDesktop安装指南-国内网络版.md'
'docker里的GID和UID.md'

// 2. 网络配置（核心）
'镜像加速器vs代理-概念对比.md'     // 核心概念
'DockerDesktop镜像加速器配置.md'
'docker进行代理.md'
'Docker网络结构详解.md'

// 3. 容器管理
'docker容器如何更新.md'
'docker容器搭建错误的知识讲解.md'

// 4. 实战应用
'如何搭建漫画库.md'
'github文件直链方式.md'
```

## 文件夹说明

| 分组 | 文件 | 说明 |
|------|------|------|
| **索引** | `Docker MOC.md` | 知识索引，置顶显示 |
| **入门** | `Windows-DockerDesktop安装指南-国内网络版.md` | 安装指南 |
| **入门** | `docker里的GID和UID.md` | 权限基础 |
| **网络** | `镜像加速器vs代理-概念对比.md` | 核心概念对比 |
| **网络** | `DockerDesktop镜像加速器配置.md` | 镜像加速配置 |
| **网络** | `docker进行代理.md` | 代理配置 |
| **网络** | `Docker网络结构详解.md` | 网络原理 |
| **管理** | `docker容器如何更新.md` | 容器更新 |
| **管理** | `docker容器搭建错误的知识讲解.md` | 故障排查 |
| **实战** | `如何搭建漫画库.md` | 漫画库搭建 |
| **实战** | `github文件直链方式.md` | GitHub 链接 |

## 排除项

- `assets/` - 图片资源文件夹
