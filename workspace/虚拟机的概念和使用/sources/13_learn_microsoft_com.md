---
url: "https://learn.microsoft.com/zh-cn/virtualization/windowscontainers/about/containers-vs-vm"
title: "容器与虚拟机 | Microsoft Learn"
scraped_at: 2026-09-04T15:57:07+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/en-us/virtualization/windowscontainers/about/containers-vs-vm "使用英语阅读") 添加到集合 Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/virtualization/windowscontainers/about/containers-vs-vm)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# 容器与虚拟机
> 适用于：Windows Server 2025、Windows Server 2022、Windows Server 2019、Windows Server 2016
本主题讨论容器和虚拟机（VM）之间的一些主要相似性和差异，以及何时可能想要使用每个虚拟机。 容器和 VM 各自都有其用途，事实上，许多容器部署都使用 VM 作为主机操作系统，而不是直接在硬件上运行，尤其是在云中运行容器时。
有关容器的概述，请参阅 [Windows 和容器](https://learn.microsoft.com/zh-cn/virtualization/windowscontainers/about/)。
## 容器体系结构
容器是一个隔离的轻量级环境，用于在主机操作系统上运行应用程序。 容器基于主机操作系统的内核（可视为操作系统的掩埋管道），并且仅包含应用和一些在用户模式下运行的轻型操作系统 API 和服务，如下图所示。
上运行
## 虚拟机体系结构
与容器相比，VM 运行完整的操作系统（包括自己的内核），如下图所示。
## 容器与虚拟机
下表显示了这些互补技术的一些相似性和差异。  
| 功能  | 虚拟机  | 容器  |  
| --- | --- | --- |  
| 隔离  | 提供与主机操作系统和其他 VM 的完整隔离。 当强安全边界至关重要时，这非常有用，例如在同一服务器或群集上托管来自竞争公司的应用。  | 通常提供与主机和其他容器的轻型隔离，但不提供与 VM 相同的强安全边界。 （可以使用 [Hyper-V 隔离模式](https://learn.microsoft.com/zh-cn/virtualization/windowscontainers/manage-containers/hyperv-container) 隔离轻型 VM 中的每个容器来提高安全性）。  |  
| 操作系统  | 运行包括内核在内的完整操作系统，因此需要更多系统资源（CPU、内存和存储）。  | 运行操作系统的用户模式部分，并可以定制为仅包含应用所需的服务，使用更少的系统资源。  |  
| 访客兼容性  | 几乎可以在虚拟机内运行任何操作系统。  | 在与主机 [相同的操作系统版本上运行](https://learn.microsoft.com/zh-cn/virtualization/windowscontainers/deploy-containers/version-compatibility)（隔离Hyper-V 能让你在轻量级 VM 环境中运行同一操作系统的早期版本）。  |  
| 部署  | 使用 Windows Admin Center 或 Hyper-V Manager 部署单个 VM;使用 PowerShell 或 System Center Virtual Machine Manager 部署多个 VM。  | 使用 Docker 通过命令行部署单个容器;使用业务流程协调程序（例如 Azure Kubernetes 服务）部署多个容器。  |  
| 操作系统更新和升级  | 在每个 VM 上下载并安装操作系统更新。 安装新的操作系统版本需要升级，或者通常只需创建全新的 VM。 这很耗时，尤其是在有很多 VM 的情况下。  | 更新或升级容器中的操作系统文件是相同的：
  1. 编辑容器映像的生成文件（称为 Dockerfile），以指向最新版本的 Windows 基础映像。 
  2. 使用此新的基础映像重新生成容器映像。
  3. 将容器映像推送到容器注册表。
  4. 使用协调工具重新部署。业务流程协调程序提供强大的自动化功能，用于大规模执行此操作。 有关详细信息，请参阅 [教程：在 Azure Kubernetes 服务中更新应用程序](https://learn.microsoft.com/zh-cn/azure/aks/tutorial-kubernetes-app-update)。

 |  
| 持久性存储  | 将虚拟硬盘（VHD）用于单个 VM 的本地存储，或将 SMB 文件共享用于由多个服务器共享的存储。  | 将 Azure 磁盘用于单个节点的本地存储，或者将 Azure 文件存储（SMB 共享）用于由多个节点或服务器共享的存储。  |  
| 负载均衡  | 虚拟机负载均衡会将正在运行的 VM 移到故障转移群集中的其他服务器。  | 容器本身不会移动;相反，业务流程协调程序可以自动启动或停止群集节点上的容器，以管理负载和可用性的更改。  |  
| 容错  | VM 可以故障转移到群集中的另一台服务器，VM 的操作系统会在新服务器上重启。  | 如果群集节点发生故障，则其他群集节点上的业务流程协调程序会快速重新创建其上运行的任何容器。  |  
| 联网  | 使用虚拟网络适配器。  | 使用对虚拟网络适配器的隔离视图，这种方式提供较少的虚拟化，因为主机的防火墙与容器共享，因此占用的资源更少。 有关详细信息，请参阅 [Windows 容器网络](https://learn.microsoft.com/zh-cn/virtualization/windowscontainers/container-networking/architecture)。  |  
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on 2025/02/08


