---
url: "https://cloud.google.com/learn/what-is-a-virtual-machine"
title: "What is a virtual machine (VM)? Uses & benefits | Google Cloud"
scraped_at: 2026-09-04T15:57:07+00:00
---

# What is a virtual machine?
_Last updated: 06/26/2026_
A virtual machine (VM) is a software-based computer that provides an isolated environment on host hardware. Virtual machines can run programs and operating systems, store data, connect to networks, and do other computing functions. Much of the technology we benefit from today, such as [cloud computing](https://cloud.google.com/learn/what-is-cloud-computing) and [artificial intelligence](https://cloud.google.com/learn/what-is-artificial-intelligence), is rooted in the concept of the virtual machine, which allows operating systems and software to be separated from a physical machine. For instance, VMs in cloud computing are used to virtualize the resources of cloud service providers’ servers, enabling the multi-tenant cloud architecture that allows customers to share resources while being isolated from one another.
Get started for free
Learn more about Compute Engine
### Important resources
  * [Choosing the right VM type](https://cloud.google.com/compute#section-6)
  * [Network load balancing VMs](https://cloud.google.com/use-cases/load-balancing#section-1)


# How do virtual machines work?
Virtual machines use virtualization technology to create virtual hardware—or a virtual version of a computer on a physical machine. The physical machine on which the VMs run is called the host machine, and the VMs running on the host are called guest machines. 
A lightweight software layer called a **hypervisor** divides the host machine's physical hardware resources, such as CPUs, GPUs, TPUs, memory (RAM), storage, and networks. The hypervisor then allocates these resources to each guest VM. This allows you to run multiple "guest" operating systems concurrently and in isolation on a single "host" machine. For example, [Google Compute Engine](https://cloud.google.com/products/compute) uses a KVM-based hypervisor to efficiently manage and allocate resources to the virtual machines you create.
Each guest VM runs on an isolated partition on the host, completely separated from other guests. You can host multiple VMs on a single host machine, often a server. The hypervisor enhances overall efficiency and flexibility by abstracting the physical resources of the host machine into a pool. These resources can then be provisioned and dynamically allocated to guest VMs based on their specific requirements.
## Two main types of hypervisors
  * **Type 1: bare-metal hypervisors:** These run directly on the host's physical hardware. They're commonly used in enterprise data centers for their high performance and efficiency. For example, Google Cloud uses a KVM-based hypervisor to power its [Compute Engine](https://cloud.google.com/products/compute) virtual machines.
  * **Type 2: hosted hypervisors:** These run as an application on top of an existing operating system, making them suitable for desktop use. The most common use case for these is for development and testing.


[ 12:54](https://www.youtube.com/watch?v=U_Of5PL9dQo)
### 
Types of virtual machines 
Generally speaking, there are two types of virtual machines: process VMs and system VMs.
Expand all
#### Process VM
A process VM, also called an application virtual machine or managed runtime environment (MRE), creates a virtual environment of an OS while an app or single process is running and destroys it as soon as you exit. Process VMs enable creating a platform-independent environment that lets an app or process run the same way on any platform. A concrete example of this is the Node.js server on [Cloud Run](https://cloud.google.com/run).Cloud Run provides a fully managed environment where your application runs within a container, abstracted from the underlying infrastructure.
#### System VM
A system VM (sometimes called hardware virtual machines) simulates a complete operating system, allowing multiple OS environments to live on the same machine. Typically, this is the type of VM people are referring to when they talk about “virtual machines.” System VMs can run their own OS and applications, and a hypervisor monitors and distributes the physical host machine’s resources between system VMs.
## Cloud virtual machines 
More recently, you may have also heard people discussing virtual machines in the cloud or a cloud VM. Cloud virtual machines are simply virtual machines that run on virtual servers in the cloud. Many cloud service providers let you create and run cloud virtual machines on their infrastructure, allowing you to use their powerful servers as host machines and leverage other software-defined services such as memory and network storage. These cloud VMs are commonly categorized by their resource optimization:
  * **General-purpose VMs** are suited for a wide variety of tasks and workloads
  * **Compute-optimized VMs** are designed for high-performance computing (HPC) and compute-intensive applications
  * **Memory-optimized VMs** are ideal for large-scale enterprise databases and workloads requiring massive amounts of memory
  * **Specialized VMs** are configured with specific high-end resources, such as GPUs, for AI/ML and advanced scientific computing
  * **Confidential VMs** are a secure type that protects data even while it is being processed in memory


### 
Frequently asked questions
Expand all
#### What’s the difference between a virtual machine and a virtual desktop?
A virtual machine is a software emulation of a physical computer, whereas a virtual desktop is a user interface that allows access to a desktop environment hosted on a remote server. The key difference between them is that a virtual machine emulates an entire computer, whereas a virtual desktop provides remote access to a desktop environment.
#### Are virtual machines secure?
Virtual machines are generally safe as they provide isolation between the host system and the virtual machine, which reduces the risk of malware spreading. However, their safety depends on proper configuration, regular updates, and appropriate security practices. If they are not managed correctly, virtual machines can still be vulnerable to attacks, making it essential to follow security best practices.
#### Does a virtual machine take up storage?
Yes, a virtual machine takes up storage space on the host system. The amount of storage used depends on the size of the virtual hard disk, the operating system, and any installed applications. Furthermore, virtual machines can be configured to dynamically allocate storage as needed or to use a fixed amount of storage.
## VMs versus containers
While both VMs and [containers](https://cloud.google.com/learn/what-are-containers) are used to isolate applications, they do it in fundamentally different ways. A virtual machine virtualizes the entire physical hardware stack, including the operating system. This makes each VM a self-contained, isolated environment, but it also means that VMs tend to be larger and take up more resources.
By contrast, containers are more lightweight because they virtualize only the OS layer. Instead of bundling a full operating system with each application, a container shares the host's OS kernel. This makes containers to use fewer resources than VMs and start up faster while remaining isolated. This makes containers attractive for new application development. Since many of the applications developed over the last 10 years were written for containers, many workloads including e-commerce, back-office, and AI are “container native.
### 
How are virtual machines used?
VMs are the basic building blocks of virtualized computing resources and play a primary role in creating any application, tool, or environment—both in the cloud or on-premises.
Here are a few of the more common ways businesses use virtual machines:
Expand all
#### Consolidate servers
Multiple physical machines can be reconfigured as a VM and run on a host alongside other VMs, allowing organizations to reduce sprawl. VMs have been proven over time to be capable of running even the most performance sensitive applications.
#### Centrally manage IT resources
A central IT organization can provision and manage VMs for each business unit and functional area, speeding access to resources while improving corporate visibility.
#### Create development and test environments
VMs can serve as isolated environments for testing and development that include full functionality but have no impact on the surrounding infrastructure.
#### Support DevOps
VMs can easily be turned off or on, migrated, and adapted, providing maximum flexibility for development and deployment. 
#### Enable workload migration
The flexibility and portability that VMs provide are key to increasing the velocity of migration initiatives.
#### Improve disaster recovery and business continuity
Replicating systems in cloud environments using VMs can provide an extra layer of security and certainty. Cloud environments can also be continuously updated.
#### Create a hybrid environment
VMs provide the foundation for creating a cloud environment alongside an on-premises one, bringing flexibility without abandoning legacy systems.
#### Cross-platform compatibility
VMs allow you to run different operating systems on a single physical machine. For example, you can run a Windows Server VM on Google Cloud's Compute Engine, even if your primary development environment uses Linux. Google Cloud provides a variety of [OS images](https://cloud.google.com/compute/docs/images) to support diverse needs.
#### Improve disaster recovery and business continuity
Replicating systems in cloud environments using VMs can provide an extra layer of security and certainty. Cloud environments can also be continuously updated.
### 
Benefits of virtual machines
Virtual machines offer many benefits, particularly if you opt for a cloud VM, including the following: 
### 
Scalability
Cloud-based VMs make it easier to scale your applications, increasing availability and performance. You can increase your capacity according to demand without having to invest in your own physical servers. 
### 
Portability 
A virtual machine is a single software package with hardware resources, an operating system, and all its applications. You can easily move VMs from one server to another, or even from on-premises hardware into cloud environments. 
### 
Reduced footprint and costs
VMs allow you to run multiple virtual environments from a single machine, helping reduce your physical infrastructure footprint, electricity bill, and maintenance and management costs. 
### 
Faster provisioning 
VMs can be easily duplicated, enabling businesses to spin up new, identical environments without having to set them up from scratch.
### 
Reliability
Virtual machines and their components exist virtually and remain isolated from other guest VMs. If VM crashes, the other guest VMs will remain operational, and the physical host machine won't be affected. 
### 
Better security
Virtual machines allow you to run multiple operating systems without impacting the host operating system. VMs let you create safe, virtual environments to test apps or even study security vulnerabilities without high risk to the host machine. Modern VM offerings, such as [Google Cloud's Confidential VMs](https://docs.cloud.google.com/confidential-computing/confidential-vm/docs/confidential-vm-overview), provide encryption-in-use for data being processed in memory using a hardware-based Trusted Execution Environment (TEE).
## Potential challenges of virtual machines
There are, however, some considerations to keep in mind when running VMs. One of the biggest potential challenges of virtual machines is that running multiple operating systems and a hypervisor layer can come with a performance cost if the host machine isn’t robust enough. In addition, virtual hardware may not be as efficient as the physical hardware of a physical machine. Finally, most cloud providers offer virtual machines that are fixed in the CPU and memory they provide, leading to inefficient usage of resources.
Many of these concerns though can be overcome by choosing to use VMs offered by a cloud service provider. Cloud VMs provide many advantages over traditional VMs since they offer organizations access to the computing power of an entire data center’s worth of computers, rather than a single machine. In addition, [Google Compute Engine](https://cloud.google.com/products/compute) virtual machines sizes offer custom machine types. Rather than selecting from predefined machine types that might include excess capacity, you can tailor the CPU-to-memory ratio specifically for your workloads, so you only pay for resources you actually use. This targeted approach minimizes waste and can significantly reduce your cloud spend, especially when migrating from on-premises to Google Cloud or from other cloud providers. Compute Engine also delivers virtual [machine types](https://cloud.google.com/compute/docs/machine-types) optimized for specific customer needs for enterprise workloads, high memory configurations, or demanding workloads like [machine learning](https://cloud.google.com/learn/what-is-machine-learning) or [high performance computing](https://cloud.google.com/solutions/hpc).
Google Cloud also offers [shielded virtual machines](https://cloud.google.com/compute/shielded-vm/docs/shielded-vm) for extra security and verifiable integrity of your VM instances. [Google Cloud shielded virtual machines](https://cloud.google.com/shielded-vm) leverage advanced platform security capabilities and controls that protect enterprise workloads from threats like remote attacks, privilege escalation, and malicious insiders. 
For certain applications, developers may choose to bypass traditional VMs entirely. Modern deployment models like container orchestration ([Google Kubernetes Engine - GKE](https://cloud.google.com/kubernetes-engine)) and serverless computing ([Cloud Run](https://cloud.google.com/run)) are powerful alternatives for specific use cases, allowing teams to bypass VM operating system management, improving deployment speed, and often achieving greater cost savings.
## Getting Started with virtual machines on Google Compute Engine
If you're ready to start using virtual machines, Google Cloud offers them through [Compute Engine](https://cloud.google.com/products/compute). Compute Engine provides flexible, self-managed VM instances hosted on Google's infrastructure. Here’s a high-level overview of how to create and connect to a VM on Compute Engine:
### Set up your Google Cloud project
You need a Google Cloud project with billing enabled. New users can sign up for a [free trial](https://cloud.google.com/free).
### Enable the Compute Engine API
This API is required to create and manage VMs. You can enable it in the Google Cloud Console or using the gcloud CLI.
### Create a VM instance: 
You can create VM instances using the Google Cloud Console or the gcloud CLI.
  * **Using the Console:** Navigate to "Compute Engine" in the Google Cloud Console and click "Create Instance." You can then configure your VM's name, region, zone, machine type (such as, e2-medium), boot disk image (example Debian, Ubuntu, Windows Server), and other settings.
  * **Using gcloud CLI:** For command-line users, the gcloud compute instances create command is used.


### Connect to your virtual machine
**SSH (Linux VMs):** Securely connect to your Linux instances using SSH.
  * **Using the Google Cloud Console:** The easiest method is often using the "SSH" button available next to your instance in the Compute Engine section of the Console. This opens a browser-based terminal session.


**Using the gcloud CLI:** The gcloud compute ssh command provides a convenient way to connect from your local terminal
  * **SSH key management:** By default, when you use gcloud compute ssh for the first time with a VM, gcloud generates an SSH key pair. It then adds your public key to the VM's metadata or project metadata. The [Google Guest Agent](https://docs.cloud.google.com/compute/docs/images/guest-agent) running on the VM automatically configures sshd to allow access using this key.


**Using OS Login (Recommended):** For enhanced security and streamlined SSH key management, especially across multiple VMs or teams, consider enabling OS Login. OS Login integrates SSH access control with [Google Cloud IAM](https://docs.cloud.google.com/iam/docs). With OS Login enabled, SSH keys are linked to your Google identity, and access is managed using IAM permissions rather than by distributing keys to instance metadata.
To enable OS Login, set the enable-oslogin metadata key to TRUE on your project or individual instances.
  * You can then connect using gcloud compute ssh as usual. Learn more in the [Set up OS Login](https://cloud.google.com/compute/docs/oslogin/set-up-oslogin) documentation


### 
Solve your business challenges with Google Cloud
New customers get $300 in free credits to spend on Google Cloud.
Get started
Talk to a Google Cloud sales specialist to discuss your unique challenge in more detail. 
Contact us
## 
Virtual machine solutions from Google Cloud
  * [ Compute Engine Create and run virtual machines in predefined or custom machine sizes on Google’s infrastructure. ](https://cloud.google.com/compute)
  * [ Custom machine types Create Compute Engine VMs with optimal amounts of vCPU and memory. ](https://cloud.google.com/custom-machine-types)
  * [ Spot VMs Affordable compute instances suitable for batch jobs and fault-tolerant workloads. ](https://cloud.google.com/preemptible-vms)
  * [ Confidential computing Encrypt data in use with Confidential VMs and Confidential GKE Nodes. ](https://cloud.google.com/confidential-computing)
  * [ Persistent disk Reliable, high-performance block storage for virtual machine instances. ](https://cloud.google.com/persistent-disk)
  * [ Solution Virtual desktops Enable secure, scalable access to corporate resources using virtual machines, balancing security and IT resources with the demands of remote work.  ](https://cloud.google.com/solutions/virtual-desktops)
  * [ Solution High performance computing VMs form the basis of Google Cloud’s flexible and powerful high performance computing solutions.  ](https://cloud.google.com/solutions/hpc)


#### Take the next step
Start building on Google Cloud with $300 in free credits and 20+ always free products.
Get started for free
  * ##### Need help getting started?
[Contact sales](https://cloud.google.com/contact/)
  * ##### Work with a trusted partner
[Find a partner](https://cloud.google.com/find-a-partner/)
  * ##### Continue browsing
[See all products](https://cloud.google.com/products/)


