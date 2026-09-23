---
url: "https://debian-handbook.info/browse/stable/sect.supervision.html"
title: "14.3. Supervision: Prevention, Detection, Deterrence"
scraped_at: 2026-09-23T05:54:53+00:00
---

  * The Debian Administrator's Handbook


##  14.3. Supervision: Prevention, Detection, Deterrence
Monitoring is an integral part of any security policy for several reasons. Among them, that the goal of security is usually not restricted to guaranteeing data confidentiality, but it also includes ensuring availability of the services. It is therefore imperative to check that everything works as expected, and to detect in a timely manner any deviant behavior or change in quality of the service(s) rendered. Monitoring activity can help detecting intrusion attempts and enable a swift reaction before they cause grave consequences. This section reviews some tools that can be used to monitor several aspects of a Debian system. As such, it completes [Section 12.4, “Monitoring”](https://debian-handbook.info/browse/stable/sect.monitoring.html). 
###  14.3.1. Monitoring Logs with `logcheck`
The `logcheck` program monitors log files every hour by default. It sends unusual log messages in emails to the administrator for further analysis. 
The list of monitored files is stored in `/etc/logcheck/logcheck.logfiles`; the default values work fine if the `/etc/rsyslog.conf` file has not been completely overhauled. 
`logcheck` can work in one of three more or less detailed modes: _paranoid_ , _server_ and _workstation_. The first one is _very_ verbose, and should probably be restricted to specific servers such as firewalls. The second (and default) mode is recommended for most servers. The last one is designed for workstations, and is even terser (it filters out more messages). 
In all three cases, `logcheck` should probably be customized to exclude some extra messages (depending on installed services), unless the admin really wishes to receive hourly batches of long uninteresting emails. Since the message selection mechanism is rather complex, `/usr/share/doc/logcheck-database/README.logcheck-database.gz` is a required — if challenging — read. 
The applied rules can be split into several types: 
  * those that qualify a message as a cracking attempt (stored in a file in the `/etc/logcheck/cracking.d/` directory); 
  * those canceling such a qualification (`/etc/logcheck/cracking.ignore.d/`); 
  * those classifying a message as a security alert (`/etc/logcheck/violations.d/`); 
  * those canceling this classification (`/etc/logcheck/violations.ignore.d/`); 
  * finally, those applying to the remaining messages (considered as _system events_). 


**_CAUTION_ Ignoring a message**
Any message tagged as a cracking attempt or a security alert (following a rule stored in a `/etc/logcheck/violations.d/myfile` file) can only be ignored by a rule in a `/etc/logcheck/violations.ignore.d/myfile` or `/etc/logcheck/violations.ignore.d/myfile-_extension_`file.
A system event is always signaled unless a rule in one of the `/etc/logcheck/ignore.d.{paranoid,server,workstation}/` directories states the event should be ignored. Of course, the only directories taken into account are those corresponding to verbosity levels equal or greater than the selected operation mode. 
###  14.3.2. Monitoring Activity
####  14.3.2.1. In Real Time
`top` is an interactive tool that displays a list of currently running processes. The default sorting is based on the current amount of processor use and can be obtained with the key. Other sort orders include a sort by occupied memory ( key), by total processor time ( key) and by process identifier ( key). The key allows killing a process by entering its process identifier. The key allows _renicing_ a process, i.e. changing its priority. 
When the system seems to be overloaded, `top` is a great tool to see which processes are competing for processor time or consume too much memory. In particular, it is often interesting to check if the processes consuming resources match the real services that the machine is known to host. An unknown process running as the www-data user should really stand out and be investigated, since it is probably an instance of software installed and executed on the system through a vulnerability in a web application. 
`top` is a very flexible tool and its manual page gives details on how to customize its display and adapt it to one's personal needs and habits. 
The `gnome-system-monitor` graphical tool is similar to `top` and it provides roughly the same features. 
####  14.3.2.2. History
Processor load, network traffic and free disk space are information that are constantly varying. Keeping a history of their evolution is often useful in determining exactly how the computer is used. 
There are many dedicated tools for this task. Most can fetch data via SNMP (_Simple Network Management Protocol_) in order to centralize this information. An added benefit is that this allows fetching data from network elements that may not be general-purpose computers, such as dedicated network routers or switches. 
This book deals with Munin in some detail (see [Section 12.4.1, “Setting Up Munin”](https://debian-handbook.info/browse/stable/sect.monitoring.html#sect.munin)) as part of [Chapter 12: “ _Advanced Administration_ ”](https://debian-handbook.info/browse/stable/advanced-administration.html). Debian also provides a similar tool, cacti. Its deployment is slightly more complex, since it is based solely on SNMP. Despite having a web interface, grasping the concepts involved in configuration still requires some effort. Reading the HTML documentation (`/usr/share/doc/cacti/html/Table-of-Contents.html`) should be considered a prerequisite. 
**_ALTERNATIVE_ `mrtg`**
`mrtg` (in the similarly-named package) is an older tool. Despite some rough edges, it can aggregate historical data and display them as graphs. It includes a number of scripts dedicated to collecting the most commonly monitored data such as processor load, network traffic, web page hits, and so on. 
The mrtg-contrib and mrtgutils packages contain example scripts that can be used directly. 
###  14.3.3. Avoiding Intrusion
Attackers try to get access to servers by guessing passwords, which is why strong passwords must always be used. Even then, you should also establish measures against brute-force attacks. A brute-force attack is an attempt to log into an unauthorized software system by performing multiple login attempts in a short period of time. 
The best way to stop a brute-force attack is to limit the number of login attempts coming from the same origin, usually by temporarily banning an IP address. 
Fail2Ban is an intrusion prevention software suite that can be configured to monitor any service that writes login attempts to a log file. It can be found in the package fail2ban. 
Fail2Ban is configured through a simple protocol by `fail2ban-client`, which also reads configuration files and issues corresponding configuration commands to the server, `fail2ban-server`. It has four configuration file types, all stored in `/etc/fail2ban/`: 
  * `fail2ban.conf`. Global configuration (such as logging). 
  * `filter.d/*.conf`. Filters specifying how to detect authentication failures. The Debian package already contains filters for many common programs. 
  * `action.d/*.conf`. Actions defining the commands for banning and “unbanning“ of IP addresses. 
  * `jail.conf`. It is where _jails_ , the combinations of filters and actions, are defined. 


Let us have a look at the configuration of `sshd` in `/etc/fail2ban/jail.conf` to better understand how Fail2Ban works... 

```
[...]
[DEFAULT]
[...]
bantime   = 10m
[...]
findtime  = 10m
[...]
maxretry  = 5
[...]
[sshd]
port     = ssh
logpath  = %(sshd_log)s
backend  = %(sshd_backend)s

```

Fail2Ban will check for failed login attempts for `sshd` using Python regular expressions defined in `/etc/fail2ban/filter.d/sshd.conf` against the log file of `sshd`, which is defined in the variable `sshd_log` in the file `/etc/fail2ban/paths-common.conf`. If Fail2Ban detects five failed login attempts within 10 minutes, it will ban the IP address where those attempts originated for 10 minutes. 
To enable, disable, or configure “jails“, the main configuration file `/etc/fail2ban/jail.conf` is not supposed to be altered. Instead this is supposed to be done in `/etc/fail2ban/jail.d/defaults-debian.conf` or files within the same directory. 
Fail2Ban is a very simple and effective way to protect against the most common brute-force attacks, but it cannot protect against distributed brute-force attacks, which is when an attacker uses a large number of machines spread around the Internet. 
A good way to provide extra protection against distributed brute force attacks is to artificially increase the login time after each failed attempt. 
###  14.3.4. Detecting Changes
Once the system is installed and configured, and barring security upgrades, there is usually no reason for most of the files and directories to evolve, data excepted. It is therefore interesting to make sure that files actually do not change: any unexpected change would therefore be worth investigating. This section presents a few tools able to monitor files and to warn the administrator when an unexpected change occurs (or simply to list such changes). 
####  14.3.4.1. Auditing Packages with `dpkg --verify`
**_GOING FURTHER_ Protecting against upstream changes**
`dpkg --verify` and `debsums` are useful in detecting changes to files coming from a Debian package, but they will be useless if the package itself is compromised, for instance, if the Debian mirror is compromised. Protecting against this class of attacks involves using APT's digital signature verification system (see [Section 6.6, “Checking Package Authenticity”](https://debian-handbook.info/browse/stable/sect.package-authentication.html)), and taking care to only install packages from a certified origin. 
`dpkg --verify` (or `dpkg -V`) is an interesting tool since it allows finding what installed files have been modified (potentially by an attacker), but this should be taken with a grain of salt. To do its job it relies on checksums stored in dpkg's own database which is stored on the hard disk (they can be found in `/var/lib/dpkg/info/_package_.md5sums`); a thorough attacker will therefore update these files so they contain the new checksums for the subverted files.
**_BACK TO BASICS_ File fingerprint**
As a reminder: a fingerprint is a value, often a number (even though in hexadecimal notation), that contains a kind of signature for the contents of a file. This signature is calculated with an algorithm, e.g. MD5 via `md5sum` or SHA* via various `sha*` commands being well-known examples, that more or less guarantee that even the tiniest change in the file contents implies a change in the fingerprint; this is known as the “avalanche effect”. This allows a simple numerical fingerprint to serve as a litmus test to check whether the contents of a file have been altered. These algorithms are not reversible; in other words, for most of them, knowing a fingerprint doesn't allow finding the corresponding contents. Recent mathematical advances seem to weaken the absoluteness of these principles, but their use is not called into question so far, since creating different contents yielding the same fingerprint still seems to be quite a difficult task. 
Running `dpkg -V` will verify all installed packages and will print out a line for each file with a failing test. The output format is the same as the one of `rpm -V` where each character denotes a test on some specific meta-data. Unfortunately `dpkg` does not store the meta-data needed for most tests and will thus output question marks for them. Currently only the checksum test can yield a "5" on the third character (when it fails). 

```
# **dpkg -V**
??5??????   /lib/systemd/system/ssh.service
??5?????? c /etc/libvirt/qemu/networks/default.xml
??5?????? c /etc/lvm/lvm.conf
??5?????? c /etc/salt/roster
```

In the sample above, dpkg reports a change to SSH's service file that the administrator made to the packaged file instead of using an appropriate `/etc/systemd/system/ssh.service.d/override.conf` override (which would be stored below `/etc` like any configuration change should be). It also lists multiple configuration files (identified by the "c" letter on the second field) that had been legitimately modified. 
####  14.3.4.2. Auditing Packages: `debsums` and its Limits
`debsums` is the ancestor of `dpkg -V` and is thus mostly obsolete. It suffers from the same limitations than dpkg. Fortunately, some of the limitations can be worked-around (whereas dpkg does not offer similar workarounds). 
Since the data on the disk cannot be trusted, `debsums` offers to do its checks based on `.deb` files instead of relying on dpkg's database. To download trusted `.deb` files of all the packages installed, we can rely on APT's authenticated downloads. This operation can be slow and tedious, and should therefore not be considered a proactive technique to be used on a regular basis. 

```
# **apt-get --reinstall -d install `grep-status -e 'Status: install ok installed' -n -s Package`
**[ ... ]
# **debsums -p /var/cache/apt/archives --generate=all**
```

Note that this example uses the `grep-status` command from the dctrl-tools package, which is not installed by default. 
`debsums` can be run frequently as a cronjob setting `CRON_CHECK` in `/etc/default/debsums`. To ignore certain files outside the `/etc` directory, which have been altered on purpose or which are expected to change (like `/usr/share/misc/pci.ids`) you can add them to `/etc/debsums-ignore`. 
####  14.3.4.3. Monitoring Files: AIDE
The AIDE tool (_Advanced Intrusion Detection Environment_) allows checking file integrity, and detecting any change against a previously recorded image of the valid system. This image is stored as a database (`/var/lib/aide/aide.db`) containing the relevant information on all files of the system (fingerprints, permissions, timestamps and so on). This database is first initialized with `aideinit`; it is then used daily (by the `/etc/cron.daily/aide` script) to check that nothing relevant changed. When changes are detected, AIDE records them in log files (`/var/log/aide/*.log`) and sends its findings to the administrator by email. 
**_IN PRACTICE_ Protecting the database**
Since AIDE uses a local database to compare the states of the files, the validity of its results is directly linked to the validity of the database. If an attacker gets root permissions on a compromised system, they will be able to replace the database and cover their tracks. A possible workaround would be to store the reference data on read-only storage media. 
Many options in `/etc/default/aide` can be used to tweak the behavior of the aide package. The AIDE configuration proper is stored in `/etc/aide/aide.conf` and `/etc/aide/aide.conf.d/` (actually, these files are only used by `update-aide.conf` to generate `/var/lib/aide/aide.conf.autogenerated`). Configuration indicates which properties of which files need to be checked. For instance, the contents of log files changes routinely, and such changes can be ignored as long as the permissions of these files stay the same, but both contents and permissions of executable programs must be constant. Although not very complex, the configuration syntax is not fully intuitive, and reading the aide.conf(5) manual page is therefore recommended. 
A new version of the database is generated daily in `/var/lib/aide/aide.db.new`; if all recorded changes were legitimate, it can be used to replace the reference database. 
**_ALTERNATIVE_ Tripwire and Samhain**
Tripwire is very similar to AIDE; even the configuration file syntax is almost the same. The main addition provided by tripwire is a mechanism to sign the configuration file, so that an attacker cannot make it point at a different version of the reference database. 
Samhain also offers similar features, as well as some functions to help detecting rootkits (see the sidebar [_QUICK LOOK_ The checksecurity and chkrootkit/rkhunter packages](https://debian-handbook.info/browse/stable/sect.supervision.html#sidebar.the-checksecurity-and-chkrootkit-rkhunter-packages)). It can also be deployed globally on a network, and record its traces on a central server (with a signature). 
**_QUICK LOOK_ The checksecurity and chkrootkit/rkhunter packages**
The first of these packages contains several small scripts performing basic checks on the system (empty passwords, new setuid files, and so on) and warning the administrator if required. Despite its explicit name, an administrator should not rely solely on it to make sure a Linux system is secure. 
The chkrootkit and rkhunter packages allow looking for _rootkits_ potentially installed on the system. As a reminder, these are pieces of software designed to hide the compromise of a system while discreetly keeping control of the machine. The tests are not 100% reliable, but they can usually draw the administrator's attention to potential problems. 
rkhunter also performs checks to see if commands have been modified, if the system startup files have been modified, and various checks on the network interfaces, including checks for listening applications. 
###  14.3.5. Detecting Intrusion (IDS/NIDS)
**_BACK TO BASICS_ Denial of service**
A “denial of service” attack has only one goal: to make a service unavailable. Whether such an attack involves overloading the server with queries or exploiting a bug, the end result is the same: the service is no longer operational. Regular users are unhappy, and the entity hosting the targeted network service suffers a loss in reputation (and possibly in revenue, for instance if the service was an e-commerce site). 
Such an attack is sometimes “distributed”; this usually involves overloading the server with large numbers of queries coming from many different sources so that the server becomes unable to answer the legitimate queries. These types of attacks have gained well-known acronyms: DDoS and DoS (depending on whether the denial of service attack is distributed or not). 
`suricata` (in the Debian package of the same name) is an NIDS — a _Network Intrusion Detection System_. Its function is to listen to the network and try to detect infiltration attempts and/or hostile acts (including denial of service attacks). All these events are logged in multiple files in `/var/log/suricata`. There are third party tools (Kibana/logstash) to better browse all the data collected. 
→ <https://suricata.io>
→ <https://www.elastic.co/products/kibana>
**_CAUTION_ Range of action**
The effectiveness of `suricata` is limited by the traffic seen on the monitored network interface. It will obviously not be able to detect anything if it cannot observe the real traffic. When plugged into a network switch, it will therefore only monitor attacks targeting the machine it runs on, which is probably not the intention. The machine hosting `suricata` should therefore be plugged into the “mirror” port of the switch, which is usually dedicated to chaining switches and therefore gets all the traffic. 
Configuring suricata involves reviewing and editing `/etc/suricata/suricata.yaml`, which is very long because each parameter is abundantly commented. A minimal configuration requires describing the range of addresses that the local network covers (`HOME_NET` parameter). In practice, this means the set of all potential attack targets. But getting the most of it requires reading it in full and adapting it to the local situation. 
On top of this, you should also edit it to define the network `interface`. You might also want to set `LISTENMODE=pcap` because the default `LISTENMODE=nfqueue` requires further configuration to work properly (the netfilter firewall must be configured to pass packets to some user-space queue handled by suricata via the `NFQUEUE` target). 
To detect bad behavior, `suricata` needs a set of monitoring rules: you can find such rules in the snort-rules-default package. `snort` is the historical reference in the IDS ecosystem and `suricata` is able to reuse rules written for it. 
Alternatively, `oinkmaster` (in the package of the same name) can be used to download Snort rule sets from external sources. 
**_GOING FURTHER_ Integration with `prelude`**
Prelude brings centralized monitoring of security information. Its modular architecture includes a server (the _manager_ in prelude-manager) which gathers alerts generated by _sensors_ of various types. 
Suricata can be configured as such a sensor. Other possibilities include _prelude-lml_ (_Log Monitor Lackey_) which monitors log files (in a manner similar to `logcheck`, described in [Section 14.3.1, “Monitoring Logs with `logcheck`”](https://debian-handbook.info/browse/stable/sect.supervision.html#sect.logcheck)). 
  * [**Prev** 14.2. Firewall or Packet Filtering](https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html)
  * [**Next** 14.4. Introduction to AppArmor](https://debian-handbook.info/browse/stable/sect.apparmor.html)


