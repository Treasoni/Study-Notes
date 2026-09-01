---
url: "https://wiki.metacubex.one/en/startup/service/"
title: "Create a running service - mihomo docs"
scraped_at: 2026-08-29T08:38:46+00:00
---

# Create a running service
##  [Using systemd](https://wiki.metacubex.one/en/startup/service/#using-systemd)[¶](https://wiki.metacubex.one/en/startup/service/#using-systemd "Permanent link")
  * Download the binary executable file from [releases](https://github.com/MetaCubeX/mihomo/releases).
  * Rename the downloaded binary executable file to `mihomo` and move it to `/usr/local/bin/`.
  * Run Mihomo as a daemon.


Use the following commands to copy the Mihomo binary file to /usr/local/bin and the configuration file to /etc/mihomo:

```
cpmihomo/usr/local/bin
cpconfig.yaml/etc/mihomo

```

Create a systemd configuration file `/etc/systemd/system/mihomo.service`:

```
[Unit]
Description=mihomo Daemon, Another Clash Kernel.
After=network.target NetworkManager.service systemd-networkd.service iwd.service

[Service]
Type=simple
LimitNPROC=500
LimitNOFILE=1000000
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_RAW CAP_NET_BIND_SERVICE CAP_SYS_TIME CAP_SYS_PTRACE CAP_DAC_READ_SEARCH CAP_DAC_OVERRIDE
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_RAW CAP_NET_BIND_SERVICE CAP_SYS_TIME CAP_SYS_PTRACE CAP_DAC_READ_SEARCH CAP_DAC_OVERRIDE
Restart=always
ExecStartPre=/usr/bin/sleep 1s
ExecStart=/usr/local/bin/mihomo -d /etc/mihomo
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target

```

Reload systemd using the following command:

```
systemctldaemon-reload

```

Enable the Mihomo service:

```
systemctlenablemihomo

```

Start Mihomo immediately with the following command:

```
systemctlstartmihomo

```

Reload Mihomo with the following command:

```
systemctlreloadmihomo

```

Check the status of Mihomo with the following command:

```
systemctlstatusmihomo

```

Check the running logs of Mihomo with the following command:

```
journalctl-umihomo-ocat-e

```

Or

```
journalctl-umihomo-ocat-f

```

Back to top 
