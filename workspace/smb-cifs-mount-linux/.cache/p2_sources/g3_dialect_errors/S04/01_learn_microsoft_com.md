---
url: "https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3"
title: "Detect, enable, and disable SMBv1, SMBv2, and SMBv3 in Windows | Microsoft Learn"
scraped_at: 2026-09-18T07:26:10+00:00
---

Table of contents  Exit editor mode
Ask Learn Ask Learn
Reading mode Table of contents [ Read in English ](https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3?tabs=server) Add to Collections Add to Plans [ Edit ](https://github.com/MicrosoftDocs/windowsserverdocs/blob/main/WindowsServerDocs/storage/file-server/Troubleshoot/detect-enable-and-disable-smbv1-v2-v3.md) Copy Markdown Print
Note
Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3?tabs=server) or changing directories. 
Access to this page requires authorization. You can try changing directories. 
# Detect, enable, and disable SMBv1, SMBv2, and SMBv3 in Windows
  * Applies to: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


Feedback
Summarize this article for me 
This article describes how to enable and disable Server Message Block (SMB) version 1 (SMBv1), SMB version 2 (SMBv2), and SMB version 3 (SMBv3) on SMB client and server components.
If you disable or remove SMBv1, you might encounter compatibility issues with old computers or software. SMBv1 has significant security vulnerabilities, and [we strongly encourage you not to use it](https://techcommunity.microsoft.com/t5/storage-at-microsoft/stop-using-smb1/ba-p/425858). [SMBv1 isn't installed by default](https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/smbv1-not-installed-by-default-in-windows) in any edition of Windows 11 or Windows Server 2019 and later versions. SMBv1 also isn't installed by default in Windows 10, except Home and Pro editions. We recommend that instead of reinstalling SMBv1, you update the SMB server that still requires it. For a list of partners that require SMBv1 and their updates that remove the requirement, see [SMB1 Product Clearinghouse](https://aka.ms/stillneedssmb1).
In Windows 11, version 24H2 and Windows Server 2025, SMB signing is required by default, which can prevent connections to workgroup computers, guest-authenticated shares, or third-party SMB servers that don't support signing. Changing which SMB protocol versions you enable doesn't change this signing requirement. Don't disable SMB protocol versions or SMB signing to work around these connection failures. Instead, enable SMB signing on the remote server, or update or replace devices that don't support SMB signing. For more information, see [Control SMB signing behavior](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing).
## Disable SMBv2 or SMBv3 for troubleshooting
We recommend keeping SMBv2 and SMBv3 enabled, but you might find it useful to disable one temporarily for troubleshooting. For more information, see [Use the command line or Registry Editor to manage SMB protocols](https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3?tabs=server#use-the-command-line-or-registry-editor-to-manage-smb-protocols).
Disabling SMBv3 deactivates the following functionality:
  * Transparent failover: Provides clients with a way to reconnect without interruption to cluster nodes during maintenance or failover
  * Scale-out: Supplies concurrent access to shared data on all file cluster nodes
  * SMB Multichannel: Facilitates aggregation of network bandwidth and fault tolerance if multiple paths are available between the client and server
  * SMB Direct: Adds remote direct memory access (RDMA) networking support for high performance, with low latency and low CPU use
  * Encryption: Provides end-to-end encryption and offers protection from eavesdropping on untrustworthy networks
  * Directory leasing: Improves application response times in branch offices through caching
  * Performance optimization: Optimizes small random read/write I/O operations


Disabling SMBv2 deactivates the following functionality:
  * Request compounding: Supports sending multiple SMBv2 requests as a single network request
  * Larger reads and writes: Improves the use of faster networks
  * Caching of folder and file properties: Gives clients the ability to keep local copies of folders and files
  * Durable handles: Provides a way for a connection to transparently reconnect to the server after a temporary disconnection
  * Improved message signing: Uses a hash-based message authentication code (HMAC) secure hash algorithm (SHA) with a 256-bit digest (HMAC SHA-256) instead of Message-Digest Algorithm 5 (MD5) as a hashing algorithm
  * Improved scalability for file sharing: Greatly increases the number of users, shares, and open files per server
  * Support for symbolic links
  * Client oplock leasing model: Limits the data transferred between the client and server, improving performance on high-latency networks and increasing SMB server scalability
  * Large maximum transmission unit (MTU) support: Supports full use of 10 Gigabit Ethernet (GbE)
  * Improved energy efficiency: Provides a way for clients that have open files to a server to sleep


The SMBv2 protocol was introduced in Windows Vista and Windows Server 2008. The SMBv3 protocol was introduced in Windows 8 and Windows Server 2012. For more information about SMBv2 and SMBv3 capabilities, see the following articles:
  * [Overview of file sharing using the SMB 3 protocol in Windows Server](https://learn.microsoft.com/en-us/windows-server/storage/file-server/file-server-smb-overview)


## Use PowerShell to remove SMBv1
You can use the [Get-WindowsOptionalFeature](https://learn.microsoft.com/en-us/powershell/module/dism/get-windowsoptionalfeature), [Disable-WindowsOptionalFeature](https://learn.microsoft.com/en-us/powershell/module/dism/disable-windowsoptionalfeature), and [Enable-WindowsOptionalFeature](https://learn.microsoft.com/en-us/powershell/module/dism/enable-windowsoptionalfeature) PowerShell commands to detect, disable, and enable an SMBv1 client or server. Run the commands at an elevated command prompt.
Note
The computer restarts after you run the PowerShell commands to disable or enable SMBv1.
  * Detect:

```
Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol

```

  * Disable:

```
Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol

```

  * Enable:

```
Enable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol

```



Tip
You can detect the SMBv1 status without elevation by running the [Get-SmbServerConfiguration](https://learn.microsoft.com/en-us/powershell/module/smbshare/get-smbserverconfiguration) command: `Get-SmbServerConfiguration | Format-List EnableSMB1Protocol`.
### Remove SMBv1


SMBv1 isn't installed by default on Windows Server 2019 and later versions. On earlier versions of Windows Server, you can use Server Manager to remove SMBv1:
  1. On the server that you want to remove SMBv1 from, open Server Manager.
  2. On the Server Manager Dashboard, under **Configure this local server** , select **Add roles and features**.
  3. On the **Before you begin** page, select **Start the Remove Roles and Features Wizard** , and then on the following page, select **Next**.
  4. On the **Select destination server** page, under **Server Pool** , ensure that the server you want to remove the feature from is selected, and then select **Next**.
  5. On the **Remove server roles** page, select **Next**.
  6. On the **Remove features** page, clear the checkbox for **SMB 1.0/CIFS File Sharing Support** , and then select **Next**.
  7. On the **Confirm removal selections** page, confirm that the feature is listed, and then select **Remove**.


On Windows 8.1, Windows 10, and Windows 11, you can use Remove Programs to disable SMBv1.
To disable SMBv1 on these operating systems, take the following steps:
  1. In **Control Panel** , select **Programs and Features**.
  2. Under **Control Panel Home** , select **Turn Windows features on or off** to open the **Windows Features** dialog.
  3. In the **Windows Features** dialog, scroll down the list, clear the checkbox for **SMB 1.0/CIFS File Sharing Support** , and then select **OK**.
  4. After Windows applies the change, on the confirmation page, select **Restart now**.


## Use the command line or Registry Editor to manage SMB protocols
Starting with the Windows 10 Fall Creators Update and Windows Server 2019, SMBv1 is no longer installed by default. For more information, see [SMBv1 is not installed by default in Windows 10 version 1709, Windows Server version 1709, and later versions](https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/smbv1-not-installed-by-default-in-windows).
When you enable or disable SMBv2 in Windows 8 or Windows Server 2012, SMBv3 is also enabled or disabled. This behavior occurs because these protocols share the same stack.


You can use the [Set-SMBServerConfiguration](https://learn.microsoft.com/en-us/powershell/module/smbshare/set-smbserverconfiguration) cmdlet to enable or disable the SMBv1, SMBv2, and SMBv3 protocols on a server component. You can use the [Get-SmbServerConfiguration](https://learn.microsoft.com/en-us/powershell/module/smbshare/get-smbserverconfiguration) cmdlet to retrieve the SMB server configuration.
You don't have to restart the computer after you run the **Set-SMBServerConfiguration** cmdlet.
### SMBv1
  * Detect:

```
Get-SmbServerConfiguration | Select EnableSMB1Protocol

```

  * Disable:

```
Set-SmbServerConfiguration -EnableSMB1Protocol $false

```

  * Enable:

```
Set-SmbServerConfiguration -EnableSMB1Protocol $true

```



For more information, see [Stop using SMB1](https://techcommunity.microsoft.com/blog/filecab/stop-using-smb1/425858).
### SMBv2 and SMBv3
  * Detect:

```
Get-SmbServerConfiguration | Select EnableSMB2Protocol

```

  * Disable:

```
Set-SmbServerConfiguration -EnableSMB2Protocol $false

```

  * Enable:

```
Set-SmbServerConfiguration -EnableSMB2Protocol $true

```



### Enable or disable SMB on Windows 7, Windows Server 2008 R2, Windows Vista, and Windows Server 2008
To enable or disable SMB protocols on an SMB Server that runs Windows 7, Windows Server 2008 R2, Windows Vista, or Windows Server 2008, use Windows PowerShell or Registry Editor, as explained in the following sections.
#### Use Windows PowerShell
You can use the [Get-Item](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-item), [Get-ItemProperty](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-itemproperty), and [Set-ItemProperty](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-itemproperty) cmdlets to detect, enable, and disable SMB protocols.
Note
The commands in the following sections require PowerShell 2.0 or later.
##### SMBv1 on an SMB server
  * Detect:

```
Get-Item HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters | ForEach-Object {Get-ItemProperty $_.pspath}

```

The default configuration is `Enabled`. As a result, no registry named value is created, so the command doesn't return an `SMB1` value.
  * Disable:

```
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" SMB1 -Type DWORD -Value 0 -Force

```

  * Enable:

```
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" SMB1 -Type DWORD -Value 1 -Force

```



Note
You must restart the computer after you make these changes.
For more information, see [Stop using SMB1](https://techcommunity.microsoft.com/blog/filecab/stop-using-smb1/425858).
##### SMBv2 and SMBv3 on an SMB server
  * Detect:

```
Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters | ForEach-Object {Get-ItemProperty $_.pspath}

```

  * Disable:

```
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" SMB2 -Type DWORD -Value 0 -Force

```

  * Enable:

```
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" SMB2 -Type DWORD -Value 1 -Force

```



Note
You must restart the computer after you make these changes.
#### Use Registry Editor
Important
Follow the steps in this section carefully. Serious problems might occur if you modify the registry incorrectly. Before you modify it, [back up the registry for restoration](https://support.microsoft.com/help/322756) in case problems occur.
To enable or disable SMBv1 on an SMB server, open Registry Editor and go to the following registry key path:
**HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters**
Configure an entry that has the following properties:
  * For the name, use **SMB1**.
  * For the type, use **REG_DWORD**.
  * For the data, use **0** for **Disabled** and **1** for **Enabled**. The default value is **1** , or **Enabled**. In this case, no registry key is created.


To enable or disable SMBv2 on an SMB server, open Registry Editor and go to the following registry key path:
**HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters**
Configure an entry that has the following properties:
  * For the name, use **SMB2**.
  * For the type, use **REG_DWORD**.
  * For the data, use **0** for **Disabled** and **1** for **Enabled**. The default value is **1** , or **Enabled**. In this case, no registry key is created.


Note
You must restart the computer after you make these changes.
Here's how to detect the status, enable, and disable SMB protocols on an SMB client that runs Windows client and Windows Server.
### SMBv1 on an SMB client
  * Detect:

```
sc.exe qc lanmanworkstation

```

  * Disable:

```
sc.exe config lanmanworkstation depend= bowser/mrxsmb20/nsi
sc.exe config mrxsmb10 start= disabled

```

  * Enable:

```
sc.exe config lanmanworkstation depend= bowser/mrxsmb10/mrxsmb20/nsi
sc.exe config mrxsmb10 start= auto

```



For more information, see [Stop using SMB1](https://techcommunity.microsoft.com/blog/filecab/stop-using-smb1/425858).
### SMBv2 and SMBv3 on an SMB client
  * Detect:

```
sc.exe qc lanmanworkstation

```

  * Disable:

```
sc.exe config lanmanworkstation depend= bowser/mrxsmb10/nsi
sc.exe config mrxsmb20 start= disabled

```

  * Enable:

```
sc.exe config lanmanworkstation depend= bowser/mrxsmb10/mrxsmb20/nsi
sc.exe config mrxsmb20 start= auto

```



Note
  * You must run these commands at an elevated command prompt.
  * You must restart the computer after you make these changes.


## Use Group Policy to disable SMBv1
This section shows you how to use Group Policy to disable SMBv1. You can use this method on various versions of Windows.


### SMBv1
You can disable SMBv1 on an SMB server by configuring the following new item in the registry:
  * Key path: **HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters**
  * Registry entry: **SMB1**
  * Entry type: **REG_DWORD**
  * Entry data: **0** , for **Disabled**


To use Group Policy to configure this item, take the following steps:
  1. Open Group Policy Management Console. Right-click the Group Policy object (GPO) that should contain the new preference item, and then select **Edit**.
  2. In the console tree under **Computer Configuration** , expand the **Preferences** folder, and then expand the **Windows Settings** folder.
  3. Right-click the **Registry** node, point to **New** , and then select **Registry Item**.
  4. In the **New Registry Properties** dialog, select or enter the following values:
     * **Action** : **Create**
     * **Hive** : **HKEY_LOCAL_MACHINE**
     * **Key Path** : **SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters**
     * **Value name** : **SMB1**
     * **Value type** : **REG_DWORD**
     * **Value data** : **0**


This procedure disables the SMBv1 server components. You must apply this policy to all necessary workstations, servers, and domain controllers in the domain.
Note
You can set Windows Management Instrumentation (WMI) filters to exclude specific operating systems or to exclude client or server operating systems. For more information, see [Group Policy Filtering](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-processing#group-policy-filtering) and [Create WMI Filters for the GPO](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-r2-and-2008/cc947846\(v=ws.10\)).
Important
Some systems require access to the SYSVOL folder or other file shares but don't support SMBv2 or SMBv3. Examples of such systems include legacy Windows systems and older Linux and partner systems. Be careful when you disable SMBv1 on domain controllers on these systems.
### SMBv1
To disable the SMBv1 client, you need to update the services registry key to prevent the start of the **MRxSMB10** driver. Then you need to remove the dependency on **MRxSMB10** from the entry for **LanmanWorkstation** so that it can start normally without requiring **MRxSMB10** to first start.
This section shows you how to update and replace the default values in the following two items in the registry:
  * Key path: **HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\mrxsmb10**
    * Registry entry: **Start**
    * Entry type: **REG_DWORD**
    * Entry data: **4** , for **Disabled**
  * Key path: **HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanWorkstation**
    * Registry entry: **DependOnService**
    * Entry type: REG_MULTI_SZ
    * Entry data: **Bowser** ,**MRxSmb20** ,**NSI**


Note
The default value includes **MRxSMB10** , which is now removed as dependency.
To configure these entries by using Group Policy, take the following steps:
  1. Open Group Policy Management Console. Right-click the GPO that should contain the new preference item, and then select **Edit**.
  2. In the console tree under **Computer Configuration** , expand the **Preferences** folder, and then expand the **Windows Settings** folder.
  3. Right-click the **Registry** node, point to **New** , and then select **Registry Item**.
  4. In the **New Registry Properties** dialog, select or enter the following values:
     * **Action** : **Update**
     * **Hive** : **HKEY_LOCAL_MACHINE**
     * **Key Path** : **SYSTEM\CurrentControlSet\services\mrxsmb10**
     * **Value name** : **Start**
     * **Value type** : **REG_DWORD**
     * **Value data** : **4**
  5. To remove the dependency on the **MRxSMB10** driver that was disabled, open the **New Registry Properties** dialog, and then select or enter the following values:
     * **Action** : **Replace**
     * **Hive** : **HKEY_LOCAL_MACHINE**
     * **Key Path** : **SYSTEM\CurrentControlSet\Services\LanmanWorkstation**
     * **Value name** : **DependOnService**
     * **Value type** : **REG_MULTI_SZ**
     * **Value data** : 
       * **Bowser**
       * **MRxSmb20**
       * **NSI**
Note
Don't include bullet points in the three **Value data** strings. List only the strings, as shown in the following screenshot.
The default value includes **MRxSMB10** in many versions of Windows. By replacing the default value with these three strings, you effectively remove **MRxSMB10** as a dependency for **LanmanWorkstation**. Instead of the four default values, you use these three values.
Note
When you use Group Policy Management Console, you don't have to use quotation marks or commas. Just type each entry on individual lines.
  6. To finish disabling SMBv1, restart the targeted systems.


### Audit SMBv1 usage
To determine which clients attempt to connect to an SMB server by using SMBv1, you can enable auditing on Windows Server and Windows clients. To enable or disable auditing, use the [Set-SmbServerConfiguration](https://learn.microsoft.com/en-us/powershell/module/smbshare/set-smbserverconfiguration) cmdlet. To check the auditing status, use the [Get-SmbServerConfiguration](https://learn.microsoft.com/en-us/powershell/module/smbshare/get-smbserverconfiguration) cmdlet.
  * Enable:

```
Set-SmbServerConfiguration -AuditSmb1Access $true

```

  * Disable:

```
Set-SmbServerConfiguration -AuditSmb1Access $false

```

  * Detect:

```
Get-SmbServerConfiguration | Select AuditSmb1Access

```



After you enable SMBv1 auditing, you can check the `Microsoft-Windows-SMBServer\Audit` event log for access events. Each time a client attempts to use SMBv1 to connect to a server, an entry that has an event ID of 3000 appears in the log.
### Check Group Policy settings
If all the settings are in the same GPO, Group Policy Management displays the following settings:
### Test and validate the policy
After you complete the configuration steps in Group Policy Management Console, give Group Policy time to apply the updates to its settings. If needed for testing, run `gpupdate /force` at a command prompt, and then review the target computers to make sure that the registry settings are applied correctly. Make sure SMBv2 and SMBv3 are functioning for all other systems in the environment.
Note
After you test the policy, restart the target systems.
Reading mode disabled
## Feedback
Was this page helpful? 
Yes
Need help with this topic? 
Want to try using Ask Learn to clarify or guide you through this topic? 
Ask Learn Ask Learn
Suggest a fix? 
##  Additional resources 
  * Last updated on 03/12/2025


