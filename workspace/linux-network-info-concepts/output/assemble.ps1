param()

$ErrorActionPreference = "Stop"

$projectDir = "C:\note\Study-Notes\workspace\linux-network-info-concepts"
$chaptersDir = "$projectDir\chapters"
$outputDir = "$projectDir\output"
$finalPath = "$outputDir\final_note.md"

# Chapter file list in order
$chapters = @(
    @{ File = "01_网络信息查询概览与工具链.md";   Num = "第一章";   Short = "概览与工具链" }
    @{ File = "02_网络接口与链路层信息.md";       Num = "第二章";   Short = "网络接口与链路层" }
    @{ File = "03_IP地址与子网信息.md";           Num = "第三章";   Short = "IP 地址与子网" }
    @{ File = "04_路由表信息.md";                 Num = "第四章";   Short = "路由表" }
    @{ File = "05_DNS解析与域名信息.md";          Num = "第五章";   Short = "DNS 解析与域名" }
    @{ File = "06_ARP与邻居发现.md";              Num = "第六章";   Short = "ARP 与邻居发现" }
    @{ File = "07_Socket连接与传输层信息.md";     Num = "第七章";   Short = "Socket 连接与传输层" }
    @{ File = "08_无线网络信息.md";               Num = "第八章";   Short = "无线网络" }
    @{ File = "09_网络监控与统计.md";             Num = "第九章";   Short = "网络监控与统计" }
    @{ File = "10_抓包与协议分析基础.md";         Num = "第十章";   Short = "抓包与协议分析" }
)

# Build full document
$lines = New-Object System.Collections.Generic.List[string]

# ── Frontmatter ──
$lines.Add("---")
$lines.Add('title: "Linux 网络信息获取与概念"')
$lines.Add('subtitle: "从概念到命令，系统掌握 Linux 网络信息查询"')
$lines.Add('tags: [linux, network, iproute2, dns, tcpdump, ip, ss, dig]')
$lines.Add("created: 2026-07-29")
$lines.Add("updated: 2026-07-29")
$lines.Add("status: complete")
$lines.Add("source_project: linux-network-info-concepts")
$lines.Add("---")
$lines.Add("")

# ── Title ──
$lines.Add("# Linux 网络信息获取与概念")
$lines.Add("")
$lines.Add("> 从概念到命令，系统掌握 Linux 网络信息查询")
$lines.Add("")
$lines.Add("**笔记类型**：实战笔记（概念解释 + 查询命令 + 实战示例）  |  **总章节**：10 章  |  **预计学习时间**：带实操约 8–12 小时")
$lines.Add("")
$lines.Add("---")
$lines.Add("")

# ── About ──
$lines.Add("## 关于本笔记")
$lines.Add("")
$lines.Add("这是一本系统性学习 Linux 上网络信息查询命令与概念的实战笔记。从网络接口、IP 地址、路由表、DNS 解析到 Socket 连接、无线网络、监控统计和抓包分析，覆盖 Linux 网络栈的各个层次。")
$lines.Add("")
$lines.Add("如果你已经知道 `ifconfig` 和 `ping`，但想系统掌握 `ip`、`ss`、`dig`、`tcpdump` 等现代工具的完整用法，并理解背后的网络概念，这本笔记就是为你准备的。")
$lines.Add("")
$lines.Add("### 前置要求")
$lines.Add("")
$lines.Add("- 基本的 Linux 命令行操作能力（能运行命令、理解管道和重定向）")
$lines.Add("- 了解 IP 地址的基本概念（知道 IPv4 是类似 `192.168.1.1` 的数字）")
$lines.Add("- 能使用包管理器安装软件（`apt install` / `pacman -S`）")
$lines.Add("")
$lines.Add("### 建议学习顺序")
$lines.Add("")
$lines.Add("1. **第一章必读**：奠定分层模型和工具家族的全局认知，后续各章都基于此框架")
$lines.Add("2. **第二至七章建议按序阅读**：从 L2 到 L7 层层递进，每章概念依赖前一章")
$lines.Add("3. **第八章（无线）**：如果当前设备没有无线网卡，可跳读或仅了解命令结构")
$lines.Add("4. **第九章（监控）与第十章（抓包）**：属于独立进阶技能，可在前面七章之后任意顺序学习")
$lines.Add("")
$lines.Add("---")
$lines.Add("")

# ── Table of Contents ──
$lines.Add("## 目录")
$lines.Add("")
$tocItems = @(
    "1. [第一章：网络信息查询概览与工具链](#第一章网络信息查询概览与工具链)"
    "2. [第二章：网络接口与链路层信息](#第二章网络接口与链路层信息)"
    "3. [第三章：IP 地址与子网信息](#第三章ip-地址与子网信息)"
    "4. [第四章：路由表信息](#第四章路由表信息)"
    "5. [第五章：DNS 解析与域名信息](#第五章dns-解析与域名信息)"
    "6. [第六章：ARP 与邻居发现](#第六章arp-与邻居发现)"
    "7. [第七章：Socket 连接与传输层信息](#第七章socket-连接与传输层信息)"
    "8. [第八章：无线网络信息](#第八章无线网络信息)"
    "9. [第九章：网络监控与统计](#第九章网络监控与统计)"
    "10. [第十章：抓包与协议分析基础](#第十章抓包与协议分析基础)"
)
foreach ($item in $tocItems) { $lines.Add($item) }
$lines.Add("")
$lines.Add("---")
$lines.Add("")

# ── Process each chapter ──
foreach ($ch in $chapters) {
    $filePath = Join-Path $chaptersDir $ch.File
    if (-not (Test-Path $filePath)) {
        Write-Warning "Missing chapter file: $filePath"
        continue
    }

    $content = Get-Content $filePath
    $inCodeBlock = $false

    foreach ($line in $content) {
        # Track code blocks
        if ($line.TrimStart() -match '^```') {
            $inCodeBlock = -not $inCodeBlock
            $lines.Add($line)
            continue
        }

        if ($inCodeBlock) {
            $lines.Add($line)
            continue
        }

        # Transform headings
        if ($line -match '^# (?!\#)(.*)') {
            $titleText = $matches[1].Trim()
            $newLine = "## ${ch.Num}：$titleText"
            $lines.Add($newLine)
        }
        elseif ($line -match '^## (?!\#)(.*)') {
            $lines.Add("### $($matches[1].Trim())")
        }
        elseif ($line -match '^### (?!\#)(.*)') {
            $lines.Add("#### $($matches[1].Trim())")
        }
        elseif ($line -match '^#### (?!\#)(.*)') {
            $lines.Add("##### $($matches[1].Trim())")
        }
        else {
            $lines.Add($line)
        }
    }

    # Add separator between chapters
    $lines.Add("")
    $lines.Add("---")
    $lines.Add("")
}

# ── Conclusion ──
$lines.Add("## 结语")
$lines.Add("")
$lines.Add("至此，整本《Linux 网络信息获取与概念》的十章内容全部完成。")
$lines.Add("")
$lines.Add("我们从最底层的**网络接口与链路层**出发（MAC 地址、MTU、`ip link`、`ethtool`），向上经过 **IP 地址与子网**（CIDR、`ip addr`、特殊地址），进入**路由表**（最长前缀匹配、`ip route get`、策略路由），再到 **DNS 解析**（`dig`、`resolvectl`、systemd-resolved 体系），回到 **ARP 与邻居发现**（IP→MAC 映射、邻居状态机），升入传输层 **Socket 连接**（TCP 状态机、`ss` 命令、Recv-Q/Send-Q），途径 **无线网络**（`iw`、`nmcli`、信号质量），横跨**网络监控与统计**（`iftop`、`nload`、`nethogs`、`vnstat`），最终以 **tcpdump 抓包分析** 收尾——走通了一条从"看配置"到"看线缆"的完整学习路径。")
$lines.Add("")
$lines.Add("### 核心收获")
$lines.Add("")
$lines.Add("1. **分层思维是排查的根本框架**——问题出在哪一层，就用哪一层的工具查。链路层查 `ip link`，网络层查 `ip addr` / `ip route`，传输层查 `ss`，应用层查 `dig`。")
$lines.Add("2. **`iproute2` 是现代标准**——`ip`、`ss`、`bridge` 三位一体替代了 `ifconfig`、`netstat`、`arp`、`route` 四个旧工具。`ip -j` JSON 输出让脚本化运维更可靠。")
$lines.Add("3. **缓存是排障的第一道关卡**——DNS 缓存（`resolvectl flush-caches`）、ARP 缓存（`ip neigh flush`）、浏览器缓存——排查前先清缓存，排除"幽灵问题"。")
$lines.Add("4. **状态机思维**——TCP 状态机（LISTEN/ESTABLISHED/TIME-WAIT/CLOSE-WAIT）、邻居状态机（REACHABLE/STALE/FAILED）本质上都是"有限状态自动机"，理解它们才能准确解读工具输出。")
$lines.Add("5. **从统计到真相**——`ss` 告诉你连接状态，`iftop` 告诉你带宽用量，但 `tcpdump` 告诉你真正的报文交换过程。三者结合构成完整的排查链。")
$lines.Add("")
$lines.Add("### 推荐后续学习方向")
$lines.Add("")
$lines.Add("- **深入 iptables/nftables**：理解防火墙规则如何影响网络信息查询（比如 ICMP 被过滤导致 ping 假阳性）")
$lines.Add("- **网络性能调优**：`ss -i` 中看到的 cwnd、RTT、BBR 拥塞控制算法等参数的深入理解和调优")
$lines.Add("- **容器网络**：Docker bridge、CNI、Overlay 网络（VXLAN/Geneve）对网络信息查询的影响")
$lines.Add("- **Wireshark 深度分析**：用 `tcpdump` 抓包后用 Wireshark 做 TCP 流追踪、HTTP 请求分析、TLS 握手分析")
$lines.Add("")
$lines.Add("> **记住**：网络排查的核心不是背命令，而是建立"分层 → 定位 → 工具 → 验证"的问题解决回路。命令只是工具，思维才是武器。")
$lines.Add("")

# Write final file
$fullText = $lines -join "`n"
[System.IO.File]::WriteAllText($finalPath, $fullText, [System.Text.UTF8Encoding]::new($false))

Write-Host "=== Assembly complete ==="
Write-Host "Output: $finalPath"
$totalLines = $lines.Count
Write-Host "Total lines: $totalLines"

# Per-chapter stats
Write-Host "`n--- Per-chapter stats ---"
foreach ($ch in $chapters) {
    $filePath = Join-Path $chaptersDir $ch.File
    if (Test-Path $filePath) {
        $chLines = (Get-Content $filePath).Count
        Write-Host "  $($ch.Num) ($($ch.Short)): $chLines lines"
    }
}
Write-Host "--- End stats ---"
