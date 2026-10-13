---
url: "https://wiki.archlinux.org/title/Deluge"
title: "Deluge - ArchWiki"
scraped_at: 2026-10-07T14:41:06+00:00
---

[Jump to content](https://wiki.archlinux.org/title/Deluge#bodyContent)
From ArchWiki
Related articles


[Deluge](https://deluge-torrent.org/) is a full-featured BitTorrent application written in Python 3. It has a variety of features, including but not limited to: a client/server model, DHT support, magnet links, a plugin system, UPnP support, full-stream encryption, proxy support, and three different client applications. When the server daemon is running, users can connect to it via a console client, a GTK-based GUI, or a Web-based UI. A full list of features can be viewed [here](https://dev.deluge-torrent.org/wiki/About). 
## Installation
[Install](https://wiki.archlinux.org/title/Install "Install") and optionally install . Be sure to read and install the optional dependencies for the gtk client to enable desktop notifications and appindicator notifications. 
## Daemon
Deluge works with a client/server model. The server is referred to as the daemon and runs in the background, waiting for a client (console, gtk, or web-based) to connect. The client can disconnect, but the daemon continues to run, transferring the torrent files in the queue. 
Upon installation, pacman will create a non-privileged **deluge** user. This user is meant to run the provided daemon, `/usr/bin/deluged`. Users are able to start the daemon several ways: 
  1. systemd system service (runs as the deluge user).
  2. systemd user service (runs as another user).
  3. Running it directly (runs as another user).


**Tip** For the highest level of security, running `deluged` via the systemd system service (`deluged.service`) is recommended since the deluge user has no shell access (limited account) or other group affiliation on the host system. In addition to the security benefits of running as the non-privileged deluge user, the system service can also run at boot without the need to start Xorg or a client.
### System service
[Start](https://wiki.archlinux.org/title/Start "Start")/[enable](https://wiki.archlinux.org/title/Enable "Enable") `deluged.service`. 
### User service
**Warning** If multiple users are running a daemon, the default port (58846) will need to be changed for each user.
A user service will allow `deluged` to run when `systemd --user` is started. This is accomplished by creating a user service file: 

```
/etc/systemd/user/deluged.service
```

```
[Unit]
Description=Deluge Daemon
After=network.target

[Service]
ExecStart=/usr/bin/deluged -d -P %h/.config/deluge/deluge.pid

[Install]
WantedBy=default.target

```

The deluge user service can now be [started](https://wiki.archlinux.org/title/Start "Start") and enabled by the user. 
The `deluged` user service can also be placed in `$HOME/.config/systemd/user/`. See [systemd/User](https://wiki.archlinux.org/title/Systemd/User "Systemd/User") for more information on user services. 
## Configuration
Deluge can be configured through any of the clients as well as by simply editing the JSON-formatted configuration files located in `$HOME/.config/deluge/`. **$HOME** refers to the home directory of the user that `deluged` is running as. This means that if the daemon is running as the **deluge** user, the default home directory is `/srv/deluge/`. 
### Shared directories for downloads/uploads
When using the systemd deluged.service, the shared directory/directories need to be shared so that other users on the system are able to access the data. The general strategy is to: 
  1. Change the owner and group of the shared directory to deluge:deluge.
  2. Set the [File permissions and attributes](https://wiki.archlinux.org/title/File_permissions_and_attributes "File permissions and attributes") on the shared directory to at least 770.
  3. Add your user (or the user/users needing to access the files) to the deluge group.


Example using `/mnt/torrent_data`: 

```
# chown -R deluge:deluge /mnt/torrent_data
# chmod 770 /mnt/torrent_data
# usermod -a -G deluge YOURUSER

```

**Note** When usermod is used to change group affiliation, a logout/login is required before changes take effect.
### Firewall
Deluge requires at least one port open for TCP and UDP to allow incoming connections for seeding. If deluge complains that it cannot open a port for incoming connections, users must open port(s) to be used. In this example, ports 56881 through 56889 are opened for TCP and UDP: 

```
# iptables -A INPUT -p tcp --dport 56881:56889 -j ACCEPT
# iptables -A INPUT -p udp --dport 56881:56889 -j ACCEPT

```

Users who are behind a NAT router/firewall must setup the corresponding ports to be forwarded. UPnP may also be used, but that will not work with the local firewall on the system because it requires predefined ports. 
**Note** One can limit this to a single port; just be sure to enable both TCP and UDP.
On many default configurations, when using iptables with connection tracking (conntrack) set to drop "INVALID" packets, sometimes a great deal of legitimate torrent traffic (especially DHT traffic) is dropped as "invalid." This is typically caused by either conntrack's memory restrictions, or from long periods between packets among peers (see [[1]](https://github.com/rakshasa/rtorrent/wiki/Using-DHT#dht-and-ip-connection-tracking) and [[2]](https://www.linuxquestions.org/questions/showthread.php?p=5145026)). Symptoms of this problem include torrents not seeding, especially when the torrent client has been active for more than a day or two continuously, and consistently low overhead traffic (in one experience, less than 3KiB/s in either in or out) with DHT enabled, even when deluge/libtorrent has been continuously running for more than forty-eight hours and many torrents are active. For this reason, it may be necessary to disable connection tracking of all torrent traffic for optimal performance, even with the listening ports set to ACCEPT (as the causes for dropping INVALID packets, for instance conntrack's memory problems, may supercede any rules to accept traffic to/from those ports). 
To fully turn off connection tracking for torrents, specify ports for both Incoming and Outgoing traffic in Deluge, for instance, 56881-56889 for incoming connections and 56890-57200 for outgoing connections. 
**Note** Limiting incoming connections is not recommended with libtorrent as this will limit the ability to keep multiple connections to the same client, even for different torrents.
Then issue the following commands (after substituting the relevant port ranges): 

```
# iptables -t raw -I PREROUTING -p udp --dport 56881:57200 -j NOTRACK
# iptables -t raw -I OUTPUT -p udp --sport 56881:57200 -j NOTRACK
# iptables -t raw -I PREROUTING -p tcp --dport 56881:57200 -j NOTRACK
# iptables -t raw -I OUTPUT -p tcp --sport 56881:57200 -j NOTRACK
# iptables -I INPUT -p icmp --icmp-type 3 -j ACCEPT
# iptables -I INPUT -p icmp --icmp-type 4 -j ACCEPT
# iptables -I INPUT -p icmp --icmp-type 11 -j ACCEPT
# iptables -I INPUT -p icmp --icmp-type 12 -j ACCEPT

```

The ICMP allowances are desirable because once connection tracking is disabled on those ports, those important ICMP messages (types 3 (Destination Unreachable), 4 (Source Quench), 11 (Time Exceeded) and 12 (Parameter Problem)) would otherwise be declared INVALID themselves (as netfilter would not know of any connections that they are associated with), and they would potentially be blocked. 
**Warning** A port range of 1024:65535 would break every DNS query.
### Plugins
A complete list of plugins can be found on the [Deluge Wiki](https://dev.deluge-torrent.org/wiki/Plugins). 
[ltConfig](https://github.com/zakkarry/deluge-ltconfig) is a useful plugin that lets you modify libtorrent-rasterbar internal settings directly from a list and has profile support, allowing for default libtorrent preset support ("High Performance Seed", "Minimum Memory Usage", "libtorrent Default Presets") and keeps your pre-ltConfig settings stored in a "Pre-ltConfig" profile. 
It offers additional settings like `announce_ip` (IP to announce to trackers), `half_open_limit` (unblock maximum half-open connections limit) and many more privacy and performance improvements (speed increases). 
The settings for libtorrent-rasterbar are available officially in the [libtorrent manual](https://www.libtorrent.org/reference-Settings.html). An optimized preset and write up about hardware considerations is available via the ltConfig repository, or directly stickied at the top [of the Plugins section of deluge-torrent.org](https://forum.deluge-torrent.org/viewtopic.php?t=56921). 
## Clients
### Console
The console client can be run with: 

```
$ deluge-console

```

Enter the `help` command for a list of available commands. 
### GTK
**Note** It is necessary to select Thin Client Mode in _Edit - > Preferences -> Interface_ for daemon (server) setups.
The GTK client can be run with: 

```
$ deluge-gtk

```

or: 

```
$ deluge

```

The GTK client has a number of useful plugins: 
  * AutoAdd - Monitors directories for .torrent files
  * Blocklist - Downloads and imports an IP blocklist
  * Execute - Event-based command execution
  * Extractor - Extracts archived files upon completion _**(beware of random high disk I/O usage)**_
  * Label - Allows labels to be assigned to torrents, as well as state, tracker, and keyword filters
  * Notifications - Provides notifications (email, pop-up, blink, sound) for events as well as other plugins
  * Scheduler - Limits active torrents and their speed on a per-hour, per-day basis
  * WebUi - Allows the Web UI to be started via the GTK client


### Web
Just as with deluge daemon mentioned above, the web client can be started several different ways: 
  1. systemd system service (runs as the deluge user).
  2. systemd user service (runs as another user).
  3. Running it directly (runs as another user).


**Note**
  * The default password for the web interface is _deluge_.
  * The web client offers many of the same features of the GTK UI, including the plugin system.
  * It is recommended to use HTTPS for the Web client to protect against a man-in-the-middle attack.
  * Users may be greeted by a warning from the browser that the SSL certificate is untrusted. Add an exception to this in the browser to continue on. See the [OpenSSL](https://wiki.archlinux.org/title/OpenSSL "OpenSSL") page for information on creating your own certificate.
  * If multiple users are running a daemon, the default port (8112) will need to be changed for each user.


**Tip** For the highest level of security, running `deluge-web` via the systemd system service (`deluge-web.service`) is recommended since the deluge user has no shell access (limited account) or other group affiliation on the host system. In addition to the security benefits of running as the non-privileged deluge user, the system service can also run at boot without the need to start Xorg or a client.
Once running, users may connect to the web client by browsing to <http://127.0.0.1:8112>, if using encryption on <https://127.0.0.1:8112> and/or by the host IP-address. 
#### System service
Deluge ships with `deluge-web.service`, a systemd system unit, which is used to [start](https://wiki.archlinux.org/title/Start "Start") the Deluge Web UI. The Deluge Web UI uses a Connection Manager, allowing managing of multiple Deluge clients running under the same host or on an entirely different one. Remember to [start](https://wiki.archlinux.org/title/Start "Start") and optionally [enable](https://wiki.archlinux.org/title/Enable "Enable") the `deluged` service to allow the Web UI connect to the host Deluge client. 
#### User service
A user service will allow `deluge-web` to run when `systemd --user` is started. This is accomplished by creating a user service file: 

```
/etc/systemd/user/deluge-web.service
```

```
[Unit]
Description=Deluge Web UI
After=deluged.service

[Service]
ExecStart=/usr/bin/deluge-web -d --ssl

[Install]
WantedBy=default.target

```

The deluge user service can now be [started](https://wiki.archlinux.org/title/Start "Start") and enabled by the user. 
The `deluge-web` user service can also be placed in `$HOME/.config/systemd/user/`. See [systemd/User](https://wiki.archlinux.org/title/Systemd/User "Systemd/User") for more information on user services. 
## Headless setup
Deluge is quite useful on a headless system, often referred to as a seed box, because of its client/server model. To set up deluge on a headless system, set up the daemon as shown above. 
### Create a user
To allow interaction with the server remotely, create a user in `$HOME/.config/deluge/auth`. For example: 

```
$ echo "delugeuser:p422WoRd:10" >> $HOME/.config/deluge/auth

```

**Note**
  * The user/password created does not have to match any system users, and to maintain good security practices it should **not**!
  * The user/password in this file are not hashed or salted like in the web client config.
  * The user/password must match the user/password found in /srv/deluge/.config/deluge/auth otherwise the authentication fails.


The number **10** corresponds to a level of **Admin**. Refer to the following table for additional values:   
| Level Name  | Level Value   |  
| --- | --- |  
| None  | 0   |  
| Read-Only  | 1   |  
| Normal  | 5   |  
| Admin  | 10   |  
**Note** In Deluge 1.35, these values have no effect, but multiuser options are under development.
### Allow remote
The default settings disallow remote connections. Change the "allow_remote" setting in `$HOME/.config/deluge/core.conf`: 

```
"allow_remote": true

```

**Note**
1. `$HOME/.config/deluge/core.conf` is automatically created at the first configuration change, if it does not exist, set the value via `deluge-console`: 

```
config --set allow_remote true

```

2. Changes made while the service is running will not be read into the daemon, therefore, stop the service before making changes to this file. 
### Firewall
Open the port for remote access. The following example uses the default daemon port (58846): 

```
# iptables -A INPUT -p tcp --dport 58846 -j ACCEPT

```

See [iptables](https://wiki.archlinux.org/title/Iptables "Iptables") for more information on firewall rules. 
Users behind a NAT router/firewall must forward the port to access the daemon from outside the network if this behavior is desired. 
### Connect
In the console client: 

```
connect <host>[:<port>] <user> <password>

```

In the GTK client, _Edit > Connection Manager > Add_. 
In the Web client, _Connection Manager > Add_. 
#### SSH Tunnel
An SSH tunnel can be created to use an encrypted connection on any client. This requires an extra loopback address to be added, but this can be automated at boot. Without this step, the connection would be considered local. The actual command to establish an SSH tunnel cannot be automated as it requires user input. There are a few possible ways to go about doing that. 

```
/etc/systemd/system/extra_lo_addr.service
```

```
[Unit]
Description=extra loopback address
Wants=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/ip addr add 127.0.0.2/8 dev lo
ExecStop=/usr/bin/ip addr del 127.0.0.2/8 dev lo

[Install]
WantedBy=multi-user.target

```

```
$ ssh -fNL 127.0.0.2:58846:localhost:58846 <ssh host>

```

The port **58846** should be replaced with the port the deluge server is running on and **< ssh host>** should be replaced with the server hosting both deluge and the SSH server. 
## Troubleshooting
### No module named service_identity
Upon running `deluged` or `deluge-console`, one may receive a message like the following: 

```
:0: UserWarning: You do not have a working installation of the service_identity module: 'No module named service_identity'.  
Please install it from <https://pypi.python.org/pypi/service_identity[](https://pypi.python.org/pypi/service_identity)> and make sure all of its dependencies are satisfied.  
Without the service_identity module and a recent enough pyOpenSSL to support it, Twisted can perform only rudimentary TLS 
client hostname verification.  Many valid certificate/hostname mappings may be rejected.

```

, an optional dependency to , is likely missing. See [FS#43806](https://bugs.archlinux.org/task/43806). 
### Web ui .torrent upload does not work
Users running the web ui behind a reverse proxy need to allow embedding for .torrent upload to work (X-Frame-Options ALLOW) 
### Execute script not found or not executable
When using the [Execute](https://dev.deluge-torrent.org/wiki/Plugins/Execute) plugin, the following error message is logged when deluge tries to execute the script: 

```
[ERROR   ][deluge_execute.core           :145 ] Execute script not found or not executable

```

If `deluged` is running as a system service, note that it likely will not be able to access the home directory of other users. Consider putting custom scripts in `/usr/local/bin/`. 
Script permission issues can be debugged as the `deluge` user: 

```
[deluge]$ _/path/to/script_

```

### Torrents list has completely disappeared after an unexpected shutdown
This usually means the state file has gotten corrupted. It [has been an intermittent issue since last decade.](https://forum.deluge-torrent.org/viewtopic.php?t=55087) There should be one backup state file along with a copy of all the previously-running torrents in your deluge profile folder (for systemd users this is usually `/srv/deluge/.config/deluge/state`) that can be restored to remedy this issue. However, it can get overwritten pretty quickly, especially if you only notice your torrents list after several reboots. A suggested course of action to keep it from happening again is to automate a daily backup of the state file and the torrents. 
### Console is unusable
If you run Deluge using the `deluge` user, you should access `deluge-console` via the `deluge` user, or else you can run into various Python exceptions and bugs. 

```
[deluge]$ deluge-console

```

or 

```
# deluge-console -c /srv/deluge/.config/deluge

```

## See also


Retrieved from "[https://wiki.archlinux.org/index.php?title=Deluge&oldid=884132](https://wiki.archlinux.org/index.php?title=Deluge&oldid=884132)"
[Category](https://wiki.archlinux.org/title/Special:Categories "Special:Categories"): 


Search
Deluge
[ Add topic ](https://wiki.archlinux.org/title/Deluge)
