---
url: "https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing"
title: "Control SMB signing behavior | Microsoft Learn"
scraped_at: 2026-09-18T07:25:51+00:00
---

Table of contents  Exit editor mode
Ask Learn Ask Learn
Reading mode Table of contents [ Read in English ](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing) Add to Plans [ Edit ](https://github.com/MicrosoftDocs/windowsserverdocs/blob/main/WindowsServerDocs/storage/file-server/smb-signing.md) Copy Markdown Print
Note
Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing) or changing directories. 
Access to this page requires authorization. You can try changing directories. 
# Control SMB signing behavior
  * Applies to: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


Feedback
Summarize this article for me 
## How SMB signing works
Server Message Block (SMB) signing is a security feature that uses the session key and cipher suite to add a signature to a message going across a connection. This signature contains a hash of the entire message in the SMB header. If someone tampers with the message in transit, the data in the tampered message doesn't match the hash in the signature. The hash also includes the identities of the original sender and the intended recipient. Signature mismatches alert users to possible foul play, helping them protect their deployments from relay and spoofing attacks.
SMB signing requirements can involve both outbound signing, which covers traffic from the SMB client, and inbound signing, which covers traffic to the server. Windows and Windows Server can require outbound signing only, inbound signing only, both, or neither. For example:
  * Windows 11, version 24H2 Enterprise, Pro, and Education require both outbound and inbound SMB signing.
  * Windows Server 2025 requires outbound SMB signing only.
  * Windows 11, version 24H2 Home edition doesn't require outbound or inbound SMB signing.


## SMB signing behavior
Although all versions of Windows and Windows Server support SMB signing, a third-party might opt to disable or not support it. If you try to connect to a remote share on a third-party SMB server that doesn't allow SMB signing, you might encounter one of the following error messages:

```
0xc000a000
-1073700864
STATUS_INVALID_SIGNATURE
The cryptographic signature is invalid.

```

To resolve this issue, adjust the settings on your third-party SMB server to allow (enable) SMB signing.
When you try to connect to third-party devices that use guest accounts to simplify access, you might receive one of these error messages:

```
You can't access this shared folder because your organization's security policies block
unauthenticated guest access. These policies help protect your PC from unsafe or malicious
devices on the network.

```

```
Error code: 0x80070035
The network path was not found.

```

```
System error 3227320323 has occurred.

```

Disabling SMB signing might be necessary if you're unable to disable guest usage for your third-party. However, this means that you're using guest access and preventing your client from ensuring signing to a trusted device.
Caution
We don't recommend disabling SMB signing as a workaround for third-party servers. We also don't recommend trying to sign with guest accounts.
## Prerequisites
In order to control SMB signing behavior and maximize its capabilities, your system must be running one of the following two operating systems:
  * Windows 11, version 24H2 or later
  * Windows Server 2025 or later


You should also follow these recommendations to ensure your SMB signatures are effective at securing your data:
  * Use Kerberos instead of NTLMv2.
  * Don't connect to shares using IP addresses.
  * Don't use CNAME Domain Name System (DNS) records. Instead, assign alternate computer names with `netdom.exe`.


## Disable SMB signing
SMB signing is required by default on the latest Insider Preview builds of Windows 11 and Windows Server 2025. All Windows environments support SMB signing. However, if your environment uses third-party servers and the third-party server doesn't support SMB signing, you can't connect to the remote share.
Requiring SMB signing also disables guest access to shares. In these cases, you must disable SMB signing manually to restore access for guest accounts. You can manually disable SMB signing through Group Policy, PowerShell, and Windows Admin Center.
Note
If you need to modify the Active Directory domain-based group policy, use **Group Policy Management** (gpmc.msc).
  * [Windows Admin Center](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing#tabpanel_1_wac)


To disable SMB signing in Group Policy, perform the following steps:
  1. Select **Start** , type **gpedit.msc** , then hit `Enter`.
  2. In the **Local Group Policy Editor** , navigate to **Computer Configuration\Windows Settings\Security Settings\Local Policies\Security Options**.
  3. Open **Microsoft network client: Digitally sign communications (always)** , select **Disabled** , then select **OK**.


  1. Open an elevated PowerShell window.
  2. To disable SMB client signing for outbound connections, run this command:

```
Set-SmbClientConfiguration -RequireSecuritySignature $false

```

  3. To disable SMB server signing for inbound connections, run this command:

```
Set-SmbServerConfiguration -RequireSecuritySignature $false

```



  1. Open **Windows Admin Center**.
  2. Select the name of the server you want to edit.
  3. Select **Settings**.
  4. Select **File Shares (SMB server)**.
  5. Under **SMB signing** , select **Not required**.
  6. Select **Save**.


Disabling SMB client for outbound connections can only be accomplished through Group Policy and PowerShell.
## Enable SMB signing
SMB signing ensures data integrity by verifying that data isn't tampered with during transmission. Additionally, SMB signing provides authentication by verifying the identity of the server and client, which helps prevent adversary-in-the-middle attacks.
  * [Windows Admin Center](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing#tabpanel_2_wac)


To enable SMB signing in Group Policy, perform the following steps:
  1. Select **Start** , type **gpedit.msc** , then hit `Enter`.
  2. In the **Local Group Policy Editor** , navigate to **Computer Configuration\Windows Settings\Security Settings\Local Policies\Security Options**.
  3. Open **Microsoft network client: Digitally sign communications (always)** , select **Enabled** , then select **OK**.


  1. Open an elevated PowerShell window.
  2. To enable SMB client signing for outbound connections, run this command:

```
Set-SmbClientConfiguration -RequireSecuritySignature $true

```

  3. To enable SMB server signing for inbound connections, run this command:

```
Set-SmbServerConfiguration -RequireSecuritySignature $true

```



  1. Open **Windows Admin Center**.
  2. Select the name of the server you want to edit.
  3. Select **Settings**.
  4. Select **File Shares (SMB server)**.
  5. Under **SMB signing** , select **Required**.
  6. Select **Save**.


Enabling SMB client for outbound connections can only be accomplished through Group Policy and PowerShell.
## Verify SMB signing status
To check if SMB signing is enabled or disabled on your SMB client or SMB server, run the following command:

```
Get-SmbClientConfiguration | FL RequireSecuritySignature

```

```
Get-SmbServerConfiguration | FL RequireSecuritySignature

```

If the returned information is **True** , then SMB signing is enabled, otherwise, if the returned information is **False** , then SMB signing is disabled.
## See also
  * [Overview of File Sharing using the SMB 3 protocol in Windows Server](https://learn.microsoft.com/en-us/windows-server/storage/file-server/file-server-smb-overview)
  * [SMB over QUIC](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-over-quic)
  * [SMB security enhancements](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-security)
  * [How to enable insecure guest logons in SMB2 and SMB3](https://learn.microsoft.com/en-us/windows-server/storage/file-server/enable-insecure-guest-logons-smb2-and-smb3)


## Feedback
Was this page helpful? 
Yes
Need help with this topic? 
Want to try using Ask Learn to clarify or guide you through this topic? 
Ask Learn Ask Learn
Suggest a fix? 
##  Additional resources 
  * Last updated on  2025-08-13 


