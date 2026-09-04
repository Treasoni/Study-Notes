---
url: "https://www.techtarget.com/it-infrastructure/tip/Whats-the-difference-between-Type-1-vs-Type-2-hypervisor"
title: "What's the difference between Type 1 vs. Type 2 hypervisor? | TechTarget"
scraped_at: 2026-09-04T15:57:07+00:00
---



Tech Accelerator [What is server virtualization? The ultimate guide](https://www.techtarget.com/it-infrastructure/definition/What-is-server-virtualization-The-ultimate-guide)
[Prev](https://www.techtarget.com/it-infrastructure/answer/Containers-vs-VMs-What-are-the-key-differences "Containers vs. VMs: What are the key differences?") [Next](https://www.techtarget.com/it-infrastructure/feature/Top-10-disadvantages-of-server-virtualization "Top 10 disadvantages of server virtualization")
Download this guide1
X
Free Download **What is server virtualization? The ultimate guide**
## Virtualization has changed the face of enterprise computing, but its many benefits are sometimes tempered by factors such as licensing and management complexity, as well as potential availability and downtime issues. With this guide, organizations can learn what virtualization is and how it works, as well as its tradeoffs and use cases, in order to adopt and deploy virtualization effectively across the data center.
By
  * [Stephen J. Bigelow,](https://www.techtarget.com/contributor/Stephen-J-Bigelow) Senior Technology Editor
  * [Brian Kirsch,](https://www.techtarget.com/contributor/Brian-Kirsch) Milwaukee Area Technical College


Published: 07 Mar 2024
The main difference between Type 1 vs. Type 2 hypervisors is that Type 1 runs on bare metal and Type 2 runs atop an operating system. Each hypervisor type also has its own pros and cons and specific use cases.
Virtualization works by abstracting physical hardware and devices from the applications running on that hardware. The process of virtualization provisions and manages the system's resources, including processor, memory, storage and network resources. This enables the system to host more than one workload simultaneously, making more cost- and energy-efficient use of the available servers and systems across the organization.
## What are hypervisors?
Virtualization requires the use of a [hypervisor](https://www.techtarget.com/searchitoperations/definition/hypervisor), which was originally called a virtual machine monitor or VMM. A hypervisor abstracts operating systems and applications from their underlying hardware. The physical hardware that a hypervisor runs on is typically referred to as a host machine, whereas the VMs that the hypervisor creates and supports are collectively called guest machines, guest VMs or simply VMs.
A hypervisor lets the host hardware operate multiple VMs independent of each other and share abstracted resources among those VMs. Virtualization with a hypervisor increases a data center's efficiency compared to physical workload hosting.
This article is part of
### [What is server virtualization? The ultimate guide](https://www.techtarget.com/it-infrastructure/definition/What-is-server-virtualization-The-ultimate-guide)
  * Which also includes:
  * [5 types of server virtualization explained](https://www.techtarget.com/it-infrastructure/tip/5-types-of-server-virtualization-explained)
  * [Virtual servers vs. physical servers: What are the differences?](https://www.techtarget.com/it-infrastructure/tip/Virtual-servers-vs-physical-servers-What-are-the-differences)
  * [10 benefits of server virtualization for businesses](https://www.techtarget.com/it-infrastructure/tip/10-benefits-of-server-virtualization-for-businesses)


There are two types of hypervisors: Type 1 and Type 2 hypervisors. Both hypervisor varieties can [virtualize common elements such as CPU](https://www.techtarget.com/searchitoperations/feature/How-to-choose-the-best-CPU-for-virtualization), memory and networking. But based on its location in the stack, the hypervisor virtualizes these elements differently.
There are many differences between Type 1 and Type 2 hypervisors. 
## Type 1 hypervisors
A [Type 1 hypervisor](https://www.techtarget.com/searchitoperations/definition/bare-metal-hypervisor) runs directly on the host machine's physical hardware, and it's [referred to as a bare-metal hypervisor](https://www.techtarget.com/searchitoperations/tip/A-beginners-guide-to-hosted-and-bare-metal-virtualization). The Type 1 hypervisor doesn't have to load an underlying OS. With direct access to the underlying hardware and no other software -- such as OSes and device drivers -- to contend with for virtualization, Type 1 hypervisors are regarded as the most efficient and best-performing hypervisors available for enterprise computing. In fact, Type 1 hypervisors are often referred to as the virtualization or virtual operating system.
Hypervisors that run directly on physical hardware are also highly secure. Virtualization mitigates the risk of attacks that target security flaws and vulnerabilities in OSes because each guest has its own OS. This ensures an attack on a guest VM is logically isolated to that VM and can't spread to others running on the same hardware.
### Type 1 hypervisor uses and capabilities
Type 1 hypervisors have long been preferred and are the de facto standard for enterprise-class virtualization. The ability to [create VMs of almost any size](https://www.techtarget.com/searchitoperations/tip/Right-sizing-VMs-improves-performance-combats-resource-contention) and configuration makes bare metal VMs well-suited for hosting large and complex enterprise workloads. The close connection established between the VM and the underlying hardware allows excellent performance, especially once virtualization command sets were added to modern microprocessors.
The Type 1 hypervisor provides several key benefits for the enterprise:
  * **Reliability.** IT organizations use Type 1 hypervisors for production-level workloads that require increased uptimes, advanced failover and other production-ready features.
  * **Scalability.** The typical Type 1 hypervisor can scale to virtualize workloads across several terabytes of RAM and hundreds of CPU cores.
  * **Advanced features.** In addition, Type 1 hypervisors often provide support for software-defined storage and networking, which creates additional security and portability for virtualized workloads. However, such features come with a much higher initial cost and greater support contract requirements.
  * **Strong management.** The typical Type 1 hypervisor requires some level of external management -- with interfaces such as Microsoft System Center Virtual Machine Manager or VMware vCenter -- to access the full scope of the hypervisor's abilities.
  * **Foundation for the cloud.** Virtualization, and Type 1 hypervisors in particular, played an enormous role in enabling cloud computing technologies. The ability to provision, deploy and manage virtual environments on-demand through software was a pivotal characteristic for computing efficiency and the key to software-based, on-demand, user-driven capabilities that are endemic to successful cloud computing. There can be no cloud without virtualization and its related hypervisors.


## Type 2 hypervisors
A Type 2 hypervisor is typically installed on top of an existing host OS. It is sometimes called a [hosted hypervisor](https://www.techtarget.com/searchitoperations/definition/Type-2-hypervisor-hosted-hypervisor) because it relies on the host machine's preexisting OS to manage calls to CPU, memory, storage and network resources.
Type 2 hypervisors trace their roots back to the early days of x86 virtualization when the hypervisor was added above the existing systems' OSes. Although the purpose and goals of Type 1 and Type 2 hypervisors are identical, the presence of an underlying OS with Type 2 hypervisors introduces unavoidable latency. All the hypervisor's activities and the work of every VM must pass through a single common host OS. Any security flaws or vulnerabilities in the host OS could also potentially compromise all of the VMs running above it.
### Type 2 hypervisor uses and capabilities
The traditional limitations of a Type 2 hypervisor have limited its use to client or end-user systems, or experimental environments where performance and security were lesser concerns than a full production environment. For example, software developers might use a Type 2 hypervisor to create VMs to test a software product prior to release. Similarly, Type 2 hypervisors have seen significant use in smaller high-volume virtual instances, and IT organizations typically use Type 2 hypervisors to create virtual desktops common in VDI deployments.
Still, Type 2 hypervisors have seen a strong surge in popularity because of several attractive benefits:
  * **Small and fast.** Type 2 hypervisors don't need individual operating systems like Type 1 VMs. This results in simpler and smaller logical entities that use far fewer resources, are faster to create, and are easier to migrate or manipulate.
  * **Highly scalable.** Because a Type 2 VM can use far fewer computer resources than a Type 1 VM, a computer can potentially host many more Type 2 VMs than Type 1 VMs.
  * **Foundation for containers.** The concept of Type 2 hypervisors is core to the emergence of virtualized containers. Containers use specialized Type 2 hypervisors called container engines, such as Docker or Apache Mesos, which let containers share a common OS. Container technology has spawned a new and highly efficient type of application architecture called [microservices](https://www.techtarget.com/searchapparchitecture/definition/microservices).
  * **Foundation for cloud.** Most public cloud providers offer native services that directly support the creation and management of virtual containers alongside traditional Type 1 VMs.


In some businesses, container technology has displaced traditional Type 1 VMs as the preferred or most popular virtualization type.
## Key differences between Type 1 and Type 2 hypervisors
When selecting a hypervisor, it's important to understand the key differences between the Type 1 and Type 2 technologies:
  * **Complexity for IT.** A Type 1 hypervisor is the functional OS and focal point of the system typically installed on an enterprise-class server with the intention of creating and hosting multiple VMs. This requires comprehensive knowledge of the Type 1 hypervisor and detailed [server management and administration](https://www.techtarget.com/searchitoperations/tip/6-virtual-server-management-best-practices). A Type 2 hypervisor takes the form of a more traditional end-user application that can be installed and operated on simpler systems by less technical staff, though a solid knowledge of creating and managing Type 2 VMs is still highly recommended.
  * **Installation.** A Type 1 hypervisor is installed directly atop a computer's hardware. No underlying operating system is needed to operate a Type 1 hypervisor. A Type 2 hypervisor requires an underlying operating system (a host OS), and the Type 2 hypervisor operates atop the OS as any other application.
  * **Access to computer resources.** A Type 1 hypervisor has direct access to the computer's memory, CPU and other hardware resources that the hypervisor will virtualize, provision and manage directly. A Type 2 hypervisor must access and virtualize the computer's resources, but this must be accomplished through the host operating system.
  * **VM performance.** A Type 1 hypervisor will offer the best performance for VMs and the workloads running inside each VM because the Type 1 hypervisor has direct access to the computer's underlying hardware resources. A Type 2 hypervisor must operate through an underlying operating system to access the computer's hardware. This results in additional latency and slightly lower performance for Type 2 VMs. Modern microprocessors and computer hardware designs can help to mitigate this performance gap, but it remains an important consideration for performance-sensitive applications.
  * **VM security.** Type 1 hypervisors [provide excellent security](https://www.techtarget.com/searchitoperations/tip/What-to-keep-in-mind-when-securing-virtual-environments) by invoking high levels of logical isolation between VMs -- no resources or services are shared between VMs. A security breach in one VM doesn't place other VMs at risk. Type 2 hypervisors offer good logical isolation as well, but the shared host OS poses a common threat. All of the vulnerabilities and risks of the host OS can affect the Type 2 hypervisor and all of the Type 2 VMs running above the host OS. It's critical to keep BOTH hypervisor types patched and updated, and the host OS must also be aggressively patched and updated on Type 2 hypervisor systems.


## Hardware support for Type 1 and Type 2 hypervisors
Hardware acceleration technologies [are widely available for virtualization's tasks](https://www.techtarget.com/searchitoperations/tip/Understand-hardware-support-for-virtualization). Such technologies include Intel Virtualization Technology extensions for Intel processors and AMD Virtualization extensions for AMD processors. There are numerous other virtualization-based extensions and features, including second-level address translation and support for nested virtualization.
Hardware acceleration technologies perform many of the process-intensive tasks needed to create and manage virtual resources on a computer. Hardware acceleration improves virtualization performance and the practical number of VMs a computer could host is above what the hypervisor can do alone.
Both Type 1 and Type 2 hypervisors use hardware acceleration support, but to varying degrees. Type 1 hypervisors rely on hardware acceleration technologies and typically don't function without those technologies available and enabled through the system's BIOS.
Type 2 hypervisors are generally capable of using hardware acceleration technologies if those features are available. But they typically [fall back on software emulation](https://history-computer.com/whats-the-difference-between-hardware-and-software-emulation/) in the absence of native hardware support. However, computers without hardware acceleration technologies that rely on software emulation will suffer significant performance penalties that restrict the number of VMs and the performance of those VMs on that computer.
Although all enterprise-class servers now include excellent hardware acceleration for virtualization, it's worth checking with your hypervisor vendor to determine a specific hypervisor's hardware support requirements.
## Type 1 and Type 2 hypervisor vendors
The hypervisor market contains several vendors, including VMware, Microsoft, Oracle and Citrix. Below are some popular products for both Type 1 and Type 2 hypervisors.
### Type 1 hypervisor products
  * **VMware vSphere.** VMware vSphere includes the ESXi hypervisor and vCenter management software to provide a suite of virtualization products, such as the vSphere Client, vSphere software development kits, Storage vMotion, the Distributed Resource Scheduler and Fault Tolerance. VMware vSphere is geared toward enterprise data centers; smaller businesses might find it difficult to justify the price.
  * **Microsoft Hyper-V.** Microsoft Hyper-V runs on Windows OSes and lets admins run multiple OSes inside a VM. Admins and developers often use Hyper-V to build test environments to run software on several OSes by creating VMs for each test.
  * **KVM.** The KVM hypervisor is an open source virtualization architecture made for Linux distributions. The KVM hypervisor lets admins convert a Linux kernel into a hypervisor and has direct access to hardware along with any VMs hosted by the hypervisor. Features include live migration, scheduling and resource control.
  * **Xen hypervisor.** The open source Xen Project originally began as a research project at the University of Cambridge in 2003. It later moved under the purview of the Linux Foundation. [Xen is used as the upstream version for other hypervisors](https://www.techtarget.com/searchitoperations/tip/Xen-vs-KVM-What-are-the-differences), including Oracle VM and Citrix Hypervisor. Amazon Web Services uses a customized version of the Xen hypervisor as the foundation for its Elastic Compute Cloud.
  * **Oracle VM.** Oracle VM is an open source virtualization architecture that uses Xen at its core and lets admins deploy OSes and application software in VMs. Oracle VM features include creation and configuration of server pools, creation and management of storage repositories, VM cloning, VM migration and load balancing.
  * **Citrix Hypervisor.** The Citrix Hypervisor, previously known as Citrix XenServer, is an open source server virtualization platform based on the Xen hypervisor. Admins use the Citrix Hypervisor to deploy, host and manage VMs as well as distribute hardware resources to those VMs. Some key features include VM templates, XenMotion and host live patches. The Citrix Hypervisor comes in two versions: Standard and Enterprise.


### Type 2 hypervisor products
  * **Oracle VM VirtualBox.** Oracle VM VirtualBox is an open source hosted hypervisor that runs on a host OS to support guest VMs. VirtualBox supports a variety of host OSes, such as Windows, Apple macOS, Linux and Oracle Solaris. VirtualBox offers multigeneration branched snapshots, Guest Additions, guest multiprocessing, ACPI support and Preboot Execution Environment network boot. Other Oracle hypervisor offerings include Oracle Solaris Zones and Oracle VM Server for x86.
  * **VMware Workstation Pro and VMware Fusion**. VMware Workstation Pro is a 64-bit hosted hypervisor capable of implementing virtualization on Windows and Linux systems. Some of Workstation's features include host/guest file sharing, the creation and deployment of encrypted VMs, and VM snapshots. VMware developed Fusion as an alternative to Workstation. VMware Fusion offers many of the same capabilities as Workstation but is macOS compatible and comes with fewer features at a reduced price.


  * **QEMU.** QEMU is an [open source virtualization tool](https://www.techtarget.com/searchitoperations/tip/5-open-source-software-applications-for-virtualization) that emulates CPU architectures as well as lets developers and admins run applications compiled for one architecture on another. QEMU offers features such as support for non-volatile dual in-line memory module hardware, share file system, secure guests and memory encryption.
  * **Parallels Desktop.** Primarily geared toward macOS admins, Parallels Desktop lets Windows, Linux and Google Chrome OSes and applications run on Apple Mac. Common features include network conditioning; support for 128GB per VM; and Chef/Ohai, Docker and HashiCorp Vagrant integrations. Parallels Desktop comes in three modes: Coherence, Full Screen and Modality mode.


## Considerations for using Type 1 vs. Type 2 hypervisors
When choosing between a Type 1 and Type 2 hypervisor, admins must consider the type and size of their workloads. If admins primarily work in an enterprise or large organization and must deploy hundreds of VMs, a Type 1 hypervisor will suit their needs.
But if admins have a smaller deployment, less-demanding workloads or require a testing environment, Type 2 hypervisors are less complex and have a smaller price tag. Enterprises and organizations can use Type 2 hypervisors as needed for workloads that suit the technology. Virtual containers are founded on Type 2 concepts, and many organizations will deploy containers rather than traditional VMs for some software types.
Ultimately, Type 1 and Type 2 hypervisors aren't mutually exclusive. Both hypervisors serve different purposes, and both can exist simultaneously within the same IT environment. It's even possible to operate both hypervisors on the same computer, such as nesting a Type 2 hypervisor in a Type 1 VM, though such combinations are exceedingly rare.
_Stephen J. Bigelow, senior technology editor at TechTarget, has more than 20 years of technical writing experience in the PC and technology industry._
_Brian Kirsch, an IT architect and Milwaukee Area Technical College instructor, has been in IT for more than 20 years, holds multiple certifications and sits on the VMUG board of directors._
#### Next Steps
[Hyper-V vs. VMware comparison: What are the differences?](https://www.techtarget.com/searchitoperations/answer/How-do-you-analyze-the-costs-of-virtualization-scalability)
[How to perform a Hyper-V to VMware migration](https://www.techtarget.com/searchitoperations/answer/How-do-you-analyze-the-costs-of-virtualization-scalability)
[Compare Nutanix AHV vs. VMware ESXi in the hypervisor battle](https://www.techtarget.com/searchstorage/blog/Storage-Soup/)
####  Related Resources
  * [Scaling Generative AI: Why Outcomes Matter More Than Technology](https://www.brighttalk.com/webcast/9059/674819) –Talk
  * [Cybersecurity After AI: What CISOs Must Unlearn to Stay Ahead](https://www.brighttalk.com/webcast/19566/671041) –Replay
  * [SOC maturity model. What suits your business the most?](https://www.brighttalk.com/webcast/18657/674569) –Replay
  * [Intelligent Biomanufacturing Systems: From Design to Control in Industry 4.0](https://www.brighttalk.com/webcast/10519/668820) –Talk


####  Dig Deeper on IT Operations
  * ##### [What is a virtual machine (VM) and how does it work? By: Alexander Gillis ](https://www.techtarget.com/it-infrastructure/definition/What-is-a-virtual-machine-VM-and-how-does-it-work)
  * ##### [Type 2 hypervisor (hosted hypervisor) By: Rahul Awati ](https://www.techtarget.com/it-infrastructure/definition/Type-2-hypervisor-hosted-hypervisor)
  * ##### [bare-metal hypervisor (Type 1 hypervisor) By: Robert Sheldon ](https://www.techtarget.com/it-infrastructure/definition/bare-metal-hypervisor-Type-1-hypervisor)
  * ##### [virtual machine escape By: Rahul Awati ](https://www.techtarget.com/whatis/definition/virtual-machine-escape)


  * [What businesses really need from an AI off switch](https://www.techtarget.com/ai/feature/What-businesses-really-need-from-an-AI-off-switch)
Turning off an AI feature doesn't necessarily stop AI processing. Businesses need meaningful controls over AI features, data ...
  * [Using AI for revenue growth is elusive but possible, experts say](https://www.techtarget.com/ai/feature/Using-AI-for-revenue-growth-is-elusive-but-possible-experts-say)
Shifting AI's ROI from productivity gains to financial revenue is tricky. Some firms, like TD Bank Group, are leading the way.
  * [Making space for spatial computing](https://www.techtarget.com/ai/tip/Making-space-for-spatial-computing)
Construct spatial computing programs through evidence, not hype. Use this roadmap to ensure that workflow selection is the ...


  * [Making sense of cybersecurity's converging categories](https://www.techtarget.com/cybersecurity/opinion/Making-sense-of-cybersecuritys-converging-categories)
AI is eliminating the dividing lines that once delineated technologies such as vulnerability management and network security. ...
  * [Why cyber resilience fails: 5 obstacles holding orgs back](https://www.techtarget.com/cybersecurity/tip/Why-cyber-resilience-fails-obstacles-holding-orgs-back)
Technical debt, cybersecurity skills shortages and identity risks are among the challenges that can make it difficult for an ...
  * [Cyber insurance explained, from selection to post-purchase](https://www.techtarget.com/cybersecurity/tip/Cyber-insurance-explained-from-selection-to-post-purchase)
Before you sign on the dotted line, make sure you understand what cyber insurance can and can't do -- and what type of policy ...


  * [PayPal exec maps a path to adopting shift-left data governance](https://www.techtarget.com/data-technologies/feature/PayPal-exec-maps-a-path-to-adopting-shift-left-data-governance)
Moving data governance upstream can help build trusted data for users and AI. PayPal governance leader Brandy O'Shields explains ...
  * [Boomi intros layer for controlling AI costs and connections](https://www.techtarget.com/data-technologies/news/366649690/Boomi-intros-layer-for-controlling-AI-costs-and-connections)
The Agent Control Plane combines previously disparate capabilities in one environment to help users better observe and command ...
  * [Qdrant builds dataset to benchmark vector retrieval at scale](https://www.techtarget.com/data-technologies/news/366649627/Qdrant-builds-dataset-to-benchmark-vector-retrieval-at-scale)
With AI tools requiring massive volumes of vectors to perform properly, the public dataset is designed to help organizations test...


  * [How asynchronous tools transform team collaboration](https://www.techtarget.com/enterprise-software/tip/How-asynchronous-tools-transform-team-collaboration)
Asynchronous collaboration tools can reduce costs, improve manageability and combat meeting fatigue. Learn how to choose and ...
  * [Using the Intune Management Extension for PowerShell scripts](https://www.techtarget.com/enterprise-software/tip/Using-the-Intune-management-extension-for-PowerShell-scripts)
Intune and PowerShell have a lot of unique management actions they can take, but with the help of the Intune Management Extension...
  * [Genesys banks on AI customer service agents -- and their orchestration](https://www.techtarget.com/enterprise-software/news/366649826/Genesys-banks-on-AI-customer-service-agents-and-their-orchestration)
The agentic SaaS playbook is emerging: Throw open your platform to agents of all stripes, and provide a harness or orchestration ...


  * [Weekly news roundup: Anthropic’s $35B deal, Nvidia buys Hugging Face and AI banned in schools](https://www.techtarget.com/it-strategy/feature/Weekly-news-roundup-Anthropics-35B-deal-Nvidia-buys-Hugging-Face-and-AI-banned-in-schools)
Stay up to date with the latest U.S. tech news, IPOs and executive moves shaping the industry each week.
  * [Why AI enablement teams shouldn't live within IT](https://www.techtarget.com/it-strategy/feature/Why-AI-enablement-teams-shouldnt-live-within-IT)
AI enablement teams can sit outside IT to stay focused on business needs. That can help CIOs avoid costly AI projects that fail ...
  * [Protecting your business from rogue bots -- a new CIO risk](https://www.techtarget.com/it-strategy/feature/Protecting-your-business-from-rogue-bots-a-new-CIO-risk)
AI-powered bots now operate autonomously, breaking out of controlled environments and exploiting systems without human direction ...


Close
