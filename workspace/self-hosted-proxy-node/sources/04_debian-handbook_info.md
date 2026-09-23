---
url: "https://debian-handbook.info/browse/stable/security.html"
title: "Chapter 14. Security"
scraped_at: 2026-09-23T05:53:34+00:00
---

  * The Debian Administrator's Handbook


#  Chapter 14. Security 

[14.1. Defining a Security Policy](https://debian-handbook.info/browse/stable/security.html#sect.defining-security-policy)


[14.2. Firewall or Packet Filtering](https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html)
     

[14.2.1. nftables Behavior](https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html#sect.netfilter)


[14.2.2. Moving from iptables to nftables](https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html#id-1.17.5.14)


[14.2.3. Syntax of `nft`](https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html#sect.nftables)


[14.2.4. Installing the Rules at Each Boot](https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html#sect.install-rules-at-boot)


[14.3. Supervision: Prevention, Detection, Deterrence](https://debian-handbook.info/browse/stable/sect.supervision.html)
     

[14.3.1. Monitoring Logs with `logcheck`](https://debian-handbook.info/browse/stable/sect.supervision.html#sect.logcheck)


[14.3.2. Monitoring Activity](https://debian-handbook.info/browse/stable/sect.supervision.html#sect.monitoring-activity)


[14.3.3. Avoiding Intrusion](https://debian-handbook.info/browse/stable/sect.supervision.html#id-1.17.6.6)


[14.3.4. Detecting Changes](https://debian-handbook.info/browse/stable/sect.supervision.html#id-1.17.6.7)


[14.3.5. Detecting Intrusion (IDS/NIDS)](https://debian-handbook.info/browse/stable/sect.supervision.html#sect.intrusion-detection)


[14.4. Introduction to AppArmor](https://debian-handbook.info/browse/stable/sect.apparmor.html)
     




[14.4.2. Enabling AppArmor and managing AppArmor profiles](https://debian-handbook.info/browse/stable/sect.apparmor.html#sect.apparmor-setup)


[14.4.3. Creating a new profile](https://debian-handbook.info/browse/stable/sect.apparmor.html#sect.apparmor-new-profile)


[14.5. Introduction to SELinux](https://debian-handbook.info/browse/stable/sect.selinux.html)
     




[14.5.2. Setting Up SELinux](https://debian-handbook.info/browse/stable/sect.selinux.html#sect.selinux-setup)


[14.5.3. Managing an SELinux System](https://debian-handbook.info/browse/stable/sect.selinux.html#sect.selinux-management)


[14.5.4. Adapting the Rules](https://debian-handbook.info/browse/stable/sect.selinux.html#sect.selinux-custom-rules)


[14.6. Other Security-Related Considerations](https://debian-handbook.info/browse/stable/sect.other-security-considerations.html)
     

[14.6.1. Inherent Risks of Web Applications](https://debian-handbook.info/browse/stable/sect.other-security-considerations.html#id-1.17.9.3)


[14.6.2. Knowing What To Expect](https://debian-handbook.info/browse/stable/sect.other-security-considerations.html#id-1.17.9.4)


[14.6.3. Choosing the Software Wisely](https://debian-handbook.info/browse/stable/sect.other-security-considerations.html#sect.choosing-the-software-wisely)


[14.6.4. Managing a Machine as a Whole](https://debian-handbook.info/browse/stable/sect.other-security-considerations.html#sect.managing-a-machine-as-a-whole)


[14.6.5. Users Are Players](https://debian-handbook.info/browse/stable/sect.other-security-considerations.html#sect.users-are-players)


[14.6.6. Physical Security](https://debian-handbook.info/browse/stable/sect.other-security-considerations.html#sect.physical-security)


[14.6.7. Legal Liability](https://debian-handbook.info/browse/stable/sect.other-security-considerations.html#id-1.17.9.9)


[14.7. Dealing with a Compromised Machine](https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html)
     

[14.7.1. Detecting and Seeing the Cracker's Intrusion](https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html#id-1.17.10.3)


[14.7.2. Putting the Server Off-Line](https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html#id-1.17.10.4)


[14.7.3. Keeping Everything that Could Be Used as Evidence](https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html#sect.keeping-everything-that-could-be-used-as-evidence)





[14.7.5. Forensic Analysis](https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html#sect.forensic-analysis)


[14.7.6. Reconstituting the Attack Scenario](https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html#sect.reconstituting-the-attack-scenario)

An information system can have a varying level of importance depending on the environment. In some cases, it is vital to a company's survival. It must therefore be protected from various kinds of risks. The process of evaluating these risks, defining and implementing the protection is collectively known as the “security process”. 
##  14.1. Defining a Security Policy
**_CAUTION_ Scope of this chapter**
Security is a vast and very sensitive subject, so we cannot claim to describe it in any kind of comprehensive manner in the course of a single chapter. We will only delineate a few important points and describe some of the tools and methods that can be of use in the security domain. For further reading, literature abounds, and entire books have been devoted to the subject. 
The word “security” itself covers a vast range of concepts, tools and procedures, none of which apply universally. Choosing among them requires a precise idea of what your goals are. Securing a system starts with answering a few questions. Rushing headlong into implementing an arbitrary set of tools runs the risk of focusing on the wrong aspects of security. 
The very first thing to determine is therefore the goal. A good approach to help with that determination starts with the following questions: 
  * _What_ are we trying to protect? The security policy will be different depending on whether we want to protect computers or data. In the latter case, we also need to know which data. 
  * What are we trying to protect _against_? Is it leakage of confidential data? Accidental data loss? Revenue loss caused by disruption of service? 
  * Also, _who_ are we trying to protect against? Security measures will be quite different for guarding against a typo by a regular user of the system than they would be when protecting against a determined attacker group. 


The term “risk” is customarily used to refer collectively to these three factors: what to protect, what needs to be prevented from happening, and who will try to make it happen. Modeling the risk requires answers to these three questions. From this risk model, a security policy can be constructed, and the policy can be implemented with concrete actions. 
**_NOTE_ Permanent questioning**
Bruce Schneier, a world expert in security matters (not only computer security) tries to counter one of security's most important myths with a motto: “Security is a process, not a product”. Assets to be protected change in time, and so do threats and the means available to potential attackers. Even if a security policy has initially been perfectly designed and implemented, one should never rest on one's laurels. The risk components evolve, and the response to that risk must evolve accordingly. 
Extra constraints are also worth taking into account, as they can restrict the range of available policies. How far are we willing to go to secure a system? This question has a major impact on the policy to implement. The answer is too often only defined in terms of monetary costs, but the other elements should also be considered, such as the amount of inconvenience imposed on system users or performance degradation. 
Once the risk has been modeled, one can start thinking about designing an actual security policy. 
**_NOTE_ Extreme policies**
There are cases where the choice of actions required to secure a system is extremely simple. 
For instance, if the system to be protected only comprises a second-hand computer, the sole use of which is to add a few numbers at the end of the day, deciding not to do anything special to protect it would be quite reasonable. The intrinsic value of the system is low. The value of the data is zero since they are not stored on the computer. A potential attacker infiltrating this “system” would only gain an unwieldy calculator. The cost of securing such a system would probably be greater than the cost of a breach. 
At the other end of the spectrum, we might want to protect the confidentiality of secret data in the most comprehensive way possible, trumping any other consideration. In this case, an appropriate response would be the total destruction of these data (securely erasing the files, shredding of the hard disks to bits, then dissolving these bits in acid, and so on). If there is an additional requirement that data must be kept in store for future use (although not necessarily readily available), and if cost still isn't a factor, then a starting point would be storing the data on iridium–platinum alloy plates stored in bomb-proof bunkers under various mountains in the world, each of which being (of course) both entirely secret and guarded by entire armies… 
Extreme though these examples may seem, they would, nevertheless, be an adequate response to defined risks, insofar as they are the outcome of a thought process that takes into account the goals to reach and the constraints to fulfill. When coming from a reasoned decision, no security policy is less respectable than any other. 
In most cases, the information system can be segmented in consistent and mostly independent subsets. Each subsystem will have its own requirements and constraints, and so the risk assessment and the design of the security policy should be undertaken separately for each. A good principle to keep in mind is that a short and well-defined perimeter is easier to defend than a long and winding frontier. The network organization should also be designed accordingly: the sensitive services should be concentrated on a small number of machines, and these machines should only be accessible via a minimal number of check-points; securing these check-points will be easier than securing all the sensitive machines against the entirety of the outside world. It is at this point that the usefulness of network filtering (including by firewalls) becomes apparent. This filtering can be implemented with dedicated hardware, but a possibly simpler and more flexible solution is to use a software firewall such as the one integrated in the Linux kernel. 
  * [**Prev** 13.9. Real-Time Communications software](https://debian-handbook.info/browse/stable/sect.rtc-clients.html)
  * [**Next** 14.2. Firewall or Packet Filtering](https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html)


