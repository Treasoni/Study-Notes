---
url: "https://learn.microsoft.com/zh-cn/windows/win32/shell/knownfolderid"
title: "KNOWNFOLDERID (Knownfolders.h) - Win32 apps | Microsoft Learn"
scraped_at: 2026-09-10T15:41:14+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows/win32/shell/knownfolderid) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows/win32/shell/knownfolderid)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# KNOWNFOLDERID
**KNOWNFOLDERID** 常量表示将注册到系统的标准文件夹标识为[已知文件夹](https://learn.microsoft.com/zh-cn/windows/win32/shell/known-folders)的 GUID。 这些文件夹随 Windows Vista 及更高版本的操作系统一起安装，并且计算机将仅安装适合它的文件夹。 有关这些文件夹的说明，请参阅 [**CSIDL**](https://learn.microsoft.com/zh-cn/windows/win32/shell/csidl)。
## 示例

```
HRESULT CExplorerBrowserHostDialog::_FillViewWithKnownFolders(IResultsFolder *prf)
{
    IKnownFolderManager *pManager;
    HRESULT hr = CoCreateInstance(CLSID_KnownFolderManager, NULL, CLSCTX_INPROC_SERVER, IID_PPV_ARGS(&pManager));
    if (SUCCEEDED(hr))
    {
        UINT cCount;
        KNOWNFOLDERID *pkfid;

        hr = pManager->GetFolderIds(&pkfid, &cCount);
        if (SUCCEEDED(hr))
        {
            for (UINT i = 0; i < cCount; i++)
            {
                IKnownFolder *pKnownFolder;
                hr = pManager->GetFolder(pkfid[i], &pKnownFolder);
                if (SUCCEEDED(hr))
                {
                    IShellItem *psi;
                    hr = pKnownFolder->GetShellItem(0, IID_PPV_ARGS(&psi));
                    if (SUCCEEDED(hr))
                    {
                        hr = prf->AddItem(psi);
                        psi->Release();
                    }
                    pKnownFolder->Release();
                }
            }
            CoTaskMemFree(pkfid);
        }
        pManager->Release();
    }
    return hr;
}


```

GitHub 上 [Windows 经典示例中的示例](https://github.com/microsoft/Windows-classic-samples/blob/1d363ff4bd17d8e20415b92e2ee989d615cc0d91/Samples/Win7Samples/winui/shell/appplatform/ExplorerBrowserCustomContents/ExplorerBrowserCustomContents.cpp) 。
## 常量  
| 常数  | 说明  |  
| --- | --- |  
|  

**FOLDERID_AccountPictures** 
 |   
 | GUID  | {008ca0b1-55b4-4c56-b8a8-4de4b299d3be}  |  
| --- | --- |  
| 显示名称  | 帐户图片  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\AccountPictures  |  
| CSIDL 等效项  | 无，Windows 8 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_AddNewPrograms** 
 |   
 | GUID  | {de61d971-5ebc-4f02-a3a9-6c82895e5c04}  |  
| --- | --- |  
| 显示名称  | 获取程序  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无  |  
| 旧版显示名称  | 添加新程序 (控制面板) 的**“添加或删除程序”** 项中找到  |  
| 旧版默认路径  | 不适用 - 虚拟文件夹  |  
 |  
|  

**FOLDERID_AdminTools** 
 |   
 | GUID  | {724EF170-A42D-4FEF-9F26-B60E846FBA4F}  |  
| --- | --- |  
| 显示名称  | “管理工具”  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Start Menu\Programs\Administrative Tools  |  
| CSIDL 等效项  | CSIDL_ADMINTOOLS  |  
| 旧版显示名称  | “管理工具”  |  
| 旧版默认路径  | %USERPROFILE%\开始菜单\程序\管理工具  |  
 |  
|  

**FOLDERID_AppDataDesktop** 
 |   
 | GUID  | {B2C5E279-7ADD-439F-B28C-C41FE1BBF672}  |  
| --- | --- |  
| 显示名称  | AppDataDesktop  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Desktop  |  
| CSIDL 等效项  | 无，Windows 10版本 1709 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
.NET 应用程序在内部使用此 FOLDERID 来启用跨平台应用功能。 它不应直接在应用程序中使用。
 |  
|  

**FOLDERID_AppDataDocuments** 
 |   
 | GUID  | {7BE16610-1F7F-44AC-BFF0-83E15F2FFCA1}  |  
| --- | --- |  
| 显示名称  | AppDataDocuments  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Documents  |  
| CSIDL 等效项  | 无，Windows 10版本 1709 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
.NET 应用程序在内部使用此 FOLDERID 来启用跨平台应用功能。 它不应直接在应用程序中使用。
 |  
|  

**FOLDERID_AppDataFavorites** 
 |   
 | GUID  | {7CFBEFBC-DE1F-45AA-B843-A542AC536CC9}  |  
| --- | --- |  
| 显示名称  | AppDataFavorites  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Favorites  |  
| CSIDL 等效项  | 无，Windows 10版本 1709 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
.NET 应用程序在内部使用此 FOLDERID 来启用跨平台应用功能。 它不打算直接从应用程序使用。
 |  
|  

**FOLDERID_AppDataProgramData** 
 |   
 | GUID  | {559D40A3-A036-40FA-AF61-84CB430A4D34}  |  
| --- | --- |  
| 显示名称  | AppDataProgramData  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\ProgramData  |  
| CSIDL 等效项  | 无，Windows 10版本 1709 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
.NET 应用程序在内部使用此 FOLDERID 来启用跨平台应用功能。 它不打算直接从应用程序使用。
 |  
|  

**FOLDERID_ApplicationShortcuts** 
 |   
 | GUID  | {A3918781-E5F2-4890-B3D9-A7E54332328C}  |  
| --- | --- |  
| 显示名称  | 应用程序快捷方式  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows\Application Shortcuts  |  
| CSIDL 等效项  | 无，Windows 8 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_AppsFolder** 
 |   
 | GUID  | {1e87508d-89c2-42f0-8a7e-645a0f50ca58}  |  
| --- | --- |  
| 显示名称  | 应用程序  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无，Windows 8 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_AppUpdates** 
 |   
 | GUID  | {a305ce99-f527-492b-8b1a-7e76fa98d6e4}  |  
| --- | --- |  
| 显示名称  | 已安装更新  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 无，Windows Vista 中引入的值。 在早期版本的 Windows 中，如果选中了“**显示更新** ”框，则此页面上的信息将包含在**“添加或删除程序** ”中。  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_CameraRoll** 
 |   
 | GUID  | {AB5FB87B-7CE2-4F83-915D-550846C9537B}  |  
| --- | --- |  
| 显示名称  | 相机胶卷  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Pictures\Camera Roll  |  
| CSIDL 等效项  | 无，Windows 8.1中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_CDBurning** 
 |   
 | GUID  | {9E52AB10-F80D-49DF-ACB8-4330F5687855}  |  
| --- | --- |  
| 显示名称  | 临时燃烧文件夹  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows\Burn\Burn  |  
| CSIDL 等效项  | CSIDL_CDBURN_AREA  |  
| 旧显示名称  | CD 燃烧  |  
| 旧版默认路径  | %USERPROFILE%\Local Settings\Application Data\Microsoft\CD Burning  |  
 |  
|  

**FOLDERID_ChangeRemovePrograms** 
 |   
 | GUID  | {df7266ac-9274-4867-8d55-3bd661de872d}  |  
| --- | --- |  
| 显示名称  | “程序和功能”  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无  |  
| 旧版显示名称  | 添加或删除程序  |  
| 旧版默认路径  | 不适用 - 虚拟文件夹  |  
 |  
|  

**FOLDERID_CommonAdminTools** 
 |   
 | GUID  | {D0384E7D-BAC3-4797-8F14-CBA229B392B5}  |  
| --- | --- |  
| 显示名称  | “管理工具”  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs\Administrative Tools  |  
| CSIDL 等效项  | CSIDL_COMMON_ADMINTOOLS  |  
| 旧版显示名称  | “管理工具”  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\开始菜单\程序\管理工具  |  
 |  
|  

**FOLDERID_CommonOEMLinks** 
 |   
 | GUID  | {C1BAE2D0-10DF-4334-BEDD-7AA20B227A9D}  |  
| --- | --- |  
| 显示名称  | OEM 链接  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %ALLUSERSPROFILE%\OEM 链接  |  
| CSIDL 等效项  | CSIDL_COMMON_OEM_LINKS  |  
| 旧版显示名称  | OEM 链接  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\OEM 链接  |  
 |  
|  

**FOLDERID_CommonPrograms** 
 |   
 | GUID  | {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}  |  
| --- | --- |  
| 显示名称  | Programs  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs  |  
| CSIDL 等效项  | CSIDL_COMMON_PROGRAMS  |  
| 旧版显示名称  | Programs  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\“开始”菜单\“程序”  |  
 |  
|  

**FOLDERID_CommonStartMenu** 
 |   
 | GUID  | {A4115719-D62E-491D-AA7C-E74B8BE3B067}  |  
| --- | --- |  
| 显示名称  | “开始”菜单  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %ALLUSERSPROFILE%\Microsoft\Windows\Start Menu  |  
| CSIDL 等效项  | CSIDL_COMMON_STARTMENU  |  
| 旧版显示名称  | “开始”菜单  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\“开始”菜单  |  
 |  
|  

**FOLDERID_CommonStartup** 
 |   
 | GUID  | {82A5EA35-D9CD-47C5-9629-E15D2F714E6E}  |  
| --- | --- |  
| 显示名称  | 启动  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs\StartUp  |  
| CSIDL 等效项  | CSIDL_COMMON_STARTUP、CSIDL_COMMON_ALTSTARTUP  |  
| 旧版显示名称  | 启动  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\开始菜单\Programs\StartUp  |  
 |  
|  

**FOLDERID_CommonTemplates** 
 |   
 | GUID  | {B94237E7-57AC-4347-9151-B08C6C32D1F7}  |  
| --- | --- |  
| 显示名称  | 模板  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %ALLUSERSPROFILE%\Microsoft\Windows\Templates  |  
| CSIDL 等效项  | CSIDL_COMMON_TEMPLATES  |  
| 旧显示名称  | 模板  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\Templates  |  
 |  
|  

**FOLDERID_ComputerFolder** 
 |   
 | GUID  | {0AC0837C-BBF8-452A-850D-79D08E667CA7}  |  
| --- | --- |  
| 显示名称  | Computer  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | CSIDL_DRIVES  |  
| 旧显示名称  | 我的电脑  |  
| 旧版默认路径  | 不适用 - 虚拟文件夹  |  
 |  
|  

**FOLDERID_ConflictFolder** 
 |   
 | GUID  | {4bfefb45-347d-4006-a5be-ac0cb0567192}  |  
| --- | --- |  
| 显示名称  | 冲突  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧显示名称  | 不适用。 此 **KNOWNFOLDERID** 是指 Windows Vista 同步管理器。 它不是较旧的 [**ISyncMgrConflictFolder**](https://learn.microsoft.com/zh-cn/windows/desktop/api/Syncmgr/nn-syncmgr-isyncmgrconflictfolder) 引用的文件夹。  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_ConnectionsFolder** 
 |   
 | GUID  | {6F0CD92B-2E97-45D1-88FF-B0D186B8DEDD}  |  
| --- | --- |  
| 显示名称  | 网络连接  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | CSIDL_CONNECTIONS  |  
| 旧显示名称  | 网络连接  |  
| 旧版默认路径  | 不适用 - 虚拟文件夹  |  
 |  
|  

**FOLDERID_Contacts** 
 |   
 | GUID  | {56784854-C6CB-462b-8169-88E350ACB882}  |  
| --- | --- |  
| 显示名称  | 联系人  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Contacts  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_ControlPanelFolder** 
 |   
 | GUID  | {82A74AEB-AEB4-465C-A014-D097EE346D63}  |  
| --- | --- |  
| 显示名称  | 控制面板  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | CSIDL_CONTROLS  |  
| 旧显示名称  | 控制面板  |  
| 旧版默认路径  | 不适用 - 虚拟文件夹  |  
 |  
|  

**FOLDERID_Cookies** 
 |   
 | GUID  | {2B0F765D-C0E9-4171-908E-08A611B84FF6}  |  
| --- | --- |  
| 显示名称  | Cookie  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Cookies  |  
| CSIDL 等效项  | CSIDL_COOKIES  |  
| 旧显示名称  | Cookie  |  
| 旧版默认路径  | %USERPROFILE%\Cookies  |  
 |  
|  

**FOLDERID_Desktop** 
 |   
 | GUID  | {B4BFCC3A-DB2C-424C-B029-7FE99A87C641}  |  
| --- | --- |  
| 显示名称  | 桌面  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Desktop  |  
| CSIDL 等效项  | CSIDL_DESKTOP、CSIDL_DESKTOPDIRECTORY  |  
| 旧版显示名称  | 桌面  |  
| 旧版默认路径  | %USERPROFILE%\Desktop  |  
 |  
|  

**FOLDERID_DeviceMetadataStore** 
 |   
 | GUID  | {5CE4A5E9-E4EB-479D-B89F-130C02886155}  |  
| --- | --- |  
| 显示名称  | DeviceMetadataStore  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %ALLUSERSPROFILE%\Microsoft\Windows\DeviceMetadataStore  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_Documents** 
 |   
 | GUID  | {FDD39AD0-238F-46AF-ADB4-6C85480369C7}  |  
| --- | --- |  
| 显示名称  | 文档  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Documents  |  
| CSIDL 等效项  | CSIDL_MYDOCUMENTS、CSIDL_PERSONAL  |  
| 旧版显示名称  | 我的文档  |  
| 旧版默认路径  | %USERPROFILE%\My Documents  |  
 |  
|  

**FOLDERID_DocumentsLibrary** 
 |   
 | GUID  | {7B0DB17D-9CD2-4A93-9733-46CC89022E7C}  |  
| --- | --- |  
| 显示名称  | 文档  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Libraries\Documents.library-ms  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_Downloads** 
 |   
 | GUID  | {374DE290-123F-4565-9164-39C4925E467B}  |  
| --- | --- |  
| 显示名称  | 下载  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Downloads  |  
| CSIDL 等效项  | 无  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_Favorites** 
 |   
 | GUID  | {1777F761-68AD-4D8A-87BD-30B759FA33DD}  |  
| --- | --- |  
| 显示名称  | 收藏夹  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Favorites  |  
| CSIDL 等效项  | CSIDL_FAVORITES、CSIDL_COMMON_FAVORITES  |  
| 旧版显示名称  | 收藏夹  |  
| 旧版默认路径  | %USERPROFILE%\Favorites  |  
 |  
|  

**FOLDERID_Fonts** 
 |   
 | GUID  | {FD228CB7-AE11-4AE3-864C-16F3910AB8FE}  |  
| --- | --- |  
| 显示名称  | 字体  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %windir%\Fonts  |  
| CSIDL 等效项  | CSIDL_FONTS  |  
| 旧版显示名称  | 字体  |  
| 旧版默认路径  | %windir%\Fonts  |  
 |  
|  

**FOLDERID_Games** 
 |  **注意：** 此 FOLDERID 在 Windows 10 版本 1803 及更高版本中已弃用。 在这些版本中，它返回 **0x80070057 - E_INVALIDARG**  
 | GUID  | {CAC52C1A-B53D-4edc-92D7-6B2E8AC19434}  |  
| --- | --- |  
| 显示名称  | 游戏  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_GameTasks** 
 |   
 | GUID  | {054FAE61-4DD8-4787-80B6-090220C4B700}  |  
| --- | --- |  
| 显示名称  | GameExplorer  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows\GameExplorer  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_History** 
 |   
 | GUID  | {D9DC8A3B-B784-432E-A781-5A1130A75963}  |  
| --- | --- |  
| 显示名称  | 历史记录  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows\History  |  
| CSIDL 等效项  | CSIDL_HISTORY  |  
| 旧版显示名称  | 历史记录  |  
| 旧版默认路径  | %USERPROFILE%\Local Settings\History  |  
 |  
|  

**FOLDERID_HomeGroup** 
 |   
 | GUID  | {52528A6B-B9E3-4ADD-B60D-588C2DBA842D}  |  
| --- | --- |  
| 显示名称  | 家庭组  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_HomeGroupCurrentUser** 
 |   
 | GUID  | {9B74B6A3-0DFD-4f11-9E78-5F7800F2E772}  |  
| --- | --- |  
| 显示名称  | 用户的用户名 (%USERNAME%)   |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无，Windows 8 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_ImplicitAppShortcuts** 
 |   
 | GUID  | {BCB5256F-79F6-4CEE-B725-DC34E402FD46}  |  
| --- | --- |  
| 显示名称  | ImplicitAppShortcuts  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Internet Explorer\Quick Launch\User Pinned\ImplicitAppShortcuts  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_InternetCache** 
 |   
 | GUID  | {352481E8-33BE-4251-BA85-6007CAEDCF9D}  |  
| --- | --- |  
| 显示名称  | Internet 临时文件  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows\Temporary Internet Files  |  
| CSIDL 等效项  | CSIDL_INTERNET_CACHE  |  
| 旧显示名称  | Internet 临时文件  |  
| 旧版默认路径  | %USERPROFILE%\本地设置\临时 Internet 文件  |  
 |  
|  

**FOLDERID_InternetFolder** 
 |   
 | GUID  | {4D9F7874-4E0C-4904-967B-40B0D20C3E4B}  |  
| --- | --- |  
| 显示名称  | Internet  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | CSIDL_INTERNET  |  
| 旧显示名称  | Internet Explorer  |  
| 旧版默认路径  | 不适用 - 虚拟文件夹  |  
 |  
|  

**FOLDERID_Libraries** 
 |   
 | GUID  | {1B3EA5DC-B587-4786-B4EF-BD1DC332AEAE}  |  
| --- | --- |  
| 显示名称  | 库  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Libraries  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_Links** 
 |   
 | GUID  | {bfb9d5e0-c6a9-404c-b2b2-ae6db6af4968}  |  
| --- | --- |  
| 显示名称  | 链接  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Links  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_LocalAppData** 
 |   
 | GUID  | {F1B32785-6FBA-4FCF-9D55-7B8E7F157091}  |  
| --- | --- |  
| 显示名称  | Local  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA% (%USERPROFILE%\AppData\Local)   |  
| CSIDL 等效项  | CSIDL_LOCAL_APPDATA  |  
| 旧显示名称  | 应用程序数据  |  
| 旧版默认路径  | %USERPROFILE%\本地设置\应用程序数据  |  
 |  
|  

**FOLDERID_LocalAppDataLow** 
 |   
 | GUID  | {A520A1A4-1780-4FF6-BD18-167343C5AF16}  |  
| --- | --- |  
| 显示名称  | LocalLow  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\AppData\LocalLow  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_LocalizedResourcesDir** 
 |   
 | GUID  | {2A00375E-224C-49DE-B8D1-440DF7EF3DDC}  |  
| --- | --- |  
| 显示名称  | 无  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %windir%\resources\0409 (代码页)   |  
| CSIDL 等效项  | CSIDL_RESOURCES_LOCALIZED  |  
| 旧显示名称  | 无  |  
| 旧版默认路径  | %windir%\resources\0409 (代码页)   |  
 |  
|  

**FOLDERID_Music** 
 |   
 | GUID  | {4BD8D571-6D19-48D3-BE97-422220080E43}  |  
| --- | --- |  
| 显示名称  | Music  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Music  |  
| CSIDL 等效项  | CSIDL_MYMUSIC  |  
| 旧显示名称  | 我的音乐  |  
| 旧版默认路径  | %USERPROFILE%\My Documents\My Music  |  
 |  
|  

**FOLDERID_MusicLibrary** 
 |   
 | GUID  | {2112AB0A-C86A-4FFE-A368-0DE96E47012E}  |  
| --- | --- |  
| 显示名称  | Music  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Libraries\Music.library-ms  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_NetHood** 
 |   
 | GUID  | {C5ABBF53-E17F-4121-8900-86626FC2C973}  |  
| --- | --- |  
| 显示名称  | 网络快捷方式  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Network Shortcuts  |  
| CSIDL 等效项  | CSIDL_NETHOOD  |  
| 旧显示名称  | NetHood  |  
| 旧版默认路径  | %USERPROFILE%\NetHood  |  
 |  
|  

**FOLDERID_NetworkFolder** 
 |   
 | GUID  | {D20BEEC4-5CA8-4905-AE3B-BF251EA09B53}  |  
| --- | --- |  
| 显示名称  | 网络  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | CSIDL_NETWORK、CSIDL_COMPUTERSNEARME  |  
| 旧显示名称  | 网上邻居  |  
| 旧版默认路径  | 不适用 - 虚拟文件夹  |  
 |  
|  

**FOLDERID_Objects3D** 
 |   
 | GUID  | {31C0DD25-9439-4F12-BF41-7FF4EDA38722}  |  
| --- | --- |  
| 显示名称  | 3D 对象  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\3D 对象  |  
| CSIDL 等效项  | 无，Windows 10版本 1703 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_OriginalImages** 
 |   
 | GUID  | {2C36C0AA-5812-4b87-BFD0-4CD0DFB19B39}  |  
| --- | --- |  
| 显示名称  | 原始图像  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows 照片库\原始图像  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_PhotoAlbums** 
 |   
 | GUID  | {69D2CF90-FC33-4FB7-9A0C-EBB0F0FCB43C}  |  
| --- | --- |  
| 显示名称  | 幻灯片放映  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Pictures\幻灯片放映  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_PicturesLibrary** 
 |   
 | GUID  | {A990AE9F-A03B-4E80-94BC-9912D7504104}  |  
| --- | --- |  
| 显示名称  | 图片  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Libraries\Pictures.library-ms  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_Pictures** 
 |   
 | GUID  | {33E28130-4E1E-4676-835A-98395C3BC3BB}  |  
| --- | --- |  
| 显示名称  | 图片  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Pictures  |  
| CSIDL 等效项  | CSIDL_MYPICTURES  |  
| 旧版显示名称  | 图片收藏  |  
| 旧版默认路径  | %USERPROFILE%\My Documents\My Pictures  |  
 |  
|  

**FOLDERID_Playlists** 
 |   
 | GUID  | {DE92C1C7-837F-4F69-A3BB-86E631204A23}  |  
| --- | --- |  
| 显示名称  | 播放列表  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Music\Playlists  |  
| CSIDL 等效项  | 无  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_PrintersFolder** 
 |   
 | GUID  | {76FC4E2D-D6AD-4519-A663-37BD56068185}  |  
| --- | --- |  
| 显示名称  | 打印机  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | CSIDL_PRINTERS  |  
| 旧版显示名称  | 打印机和传真  |  
| 旧版默认路径  | 不适用 - 虚拟文件夹  |  
 |  
|  

**FOLDERID_PrintHood** 
 |   
 | GUID  | {9274BD8D-CFD1-41C3-B35E-B13F55A758F4}  |  
| --- | --- |  
| 显示名称  | 打印机快捷方式  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Printer Shortcuts  |  
| CSIDL 等效项  | CSIDL_PRINTHOOD  |  
| 旧版显示名称  | PrintHood  |  
| 旧版默认路径  | %USERPROFILE%\PrintHood  |  
 |  
|  

**FOLDERID_Profile** 
 |   
 | GUID  | {5E6C858F-0E22-4760-9AFE-EA3317B67173}  |  
| --- | --- |  
| 显示名称  | 用户的用户名 (%USERNAME%)   |  
| 文件夹类型  | FIXED  |  
| Default Path  | %USERPROFILE% (%SystemDrive%\Users\%USERNAME%)   |  
| CSIDL 等效项  | CSIDL_PROFILE  |  
| 旧版显示名称  | 用户的用户名 (%USERNAME%)   |  
| 旧版默认路径  | %USERPROFILE% (%SystemDrive%\Documents and Settings\%USERNAME%)   |  
 |  
|  

**FOLDERID_ProgramData** 
 |   
 | GUID  | {62AB5D82-FDC1-4DC3-A9DD-070D1D495D97}  |  
| --- | --- |  
| 显示名称  | ProgramData  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %ALLUSERSPROFILE% (%ProgramData%，%SystemDrive%\ProgramData)   |  
| CSIDL 等效项  | CSIDL_COMMON_APPDATA  |  
| 旧显示名称  | 应用程序数据  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\Application Data  |  
 |  
|  

**FOLDERID_ProgramFiles** 
 |  有关更多信息，请参见备注。  
 | GUID  | {905e63b6-c1bf-494e-b29c-65b732d3d21a}  |  
| --- | --- |  
| 显示名称  | Program Files  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %ProgramFiles% (%SystemDrive%\Program Files)   |  
| CSIDL 等效项  | CSIDL_PROGRAM_FILES  |  
| 旧显示名称  | Program Files  |  
| 旧版默认路径  | %ProgramFiles% (%SystemDrive%\Program Files)   |  
 |  
|  

**FOLDERID_ProgramFilesX64** 
 |  32 位操作系统不支持此值。 在 64 位操作系统上运行的 32 位应用程序也不支持它。 尝试在任一情况下使用 FOLDERID_ProgramFilesX64 都会导致错误。 有关更多信息，请参见备注。  
 | GUID  | {6D809377-6AF0-444b-8957-A3773F02200E}  |  
| --- | --- |  
| 显示名称  | Program Files  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %ProgramFiles% (%SystemDrive%\Program Files)   |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | Program Files  |  
| 旧版默认路径  | %ProgramFiles% (%SystemDrive%\Program Files)   |  
 |  
|  

**FOLDERID_ProgramFilesX86** 
 |  有关更多信息，请参见备注。  
 | GUID  | {7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}  |  
| --- | --- |  
| 显示名称  | Program Files  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %ProgramFiles% (%SystemDrive%\Program Files)   |  
| CSIDL 等效项  | CSIDL_PROGRAM_FILESX86  |  
| 旧显示名称  | Program Files  |  
| 旧版默认路径  | %ProgramFiles% (%SystemDrive%\Program Files)   |  
 |  
|  

**FOLDERID_ProgramFilesCommon** 
 |  有关更多信息，请参见备注。  
 | GUID  | {F7F1ED05-9F6D-47A2-AAAE-29D317C6F066}  |  
| --- | --- |  
| 显示名称  | 通用文件  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %ProgramFiles%\Common Files  |  
| CSIDL 等效项  | CSIDL_PROGRAM_FILES_COMMON  |  
| 旧显示名称  | 通用文件  |  
| 旧版默认路径  | %ProgramFiles%\Common Files  |  
 |  
|  

**FOLDERID_ProgramFilesCommonX64** 
 |  有关更多信息，请参见备注。  
 | GUID  | {6365D5A7-0F0D-45E5-87F6-0DA56B6A4F7D}  |  
| --- | --- |  
| 显示名称  | 通用文件  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %ProgramFiles%\Common Files  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 通用文件  |  
| 旧版默认路径  | %ProgramFiles%\Common Files  |  
 |  
|  

**FOLDERID_ProgramFilesCommonX86** 
 |  有关更多信息，请参见备注。  
 | GUID  | {DE974D24-D9C6-4D3E-BF91-F4455120B917}  |  
| --- | --- |  
| 显示名称  | 通用文件  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %ProgramFiles%\Common Files  |  
| CSIDL 等效项  | CSIDL_PROGRAM_FILES_COMMONX86  |  
| 旧显示名称  | 通用文件  |  
| 旧版默认路径  | %ProgramFiles%\Common Files  |  
 |  
|  

**FOLDERID_Programs** 
 |   
 | GUID  | {A77F5D77-2E2B-44C3-A6A2-ABA601054A51}  |  
| --- | --- |  
| 显示名称  | Programs  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Start Menu\Programs  |  
| CSIDL 等效项  | CSIDL_PROGRAMS  |  
| 旧显示名称  | Programs  |  
| 旧版默认路径  | %USERPROFILE%\开始菜单\Programs  |  
 |  
|  

**FOLDERID_Public** 
 |   
 | GUID  | {DFDF76A2-C82A-4D63-906A-5644AC457385}  |  
| --- | --- |  
| 显示名称  | 公用  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %PUBLIC% (%SystemDrive%\Users\Public)   |  
| CSIDL 等效项  | 无，Windows Vista 新增功能  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_PublicDesktop** 
 |   
 | GUID  | {C4AA340D-F20F-4863-AFEF-F87EF2E6BA25}  |  
| --- | --- |  
| 显示名称  | 公共桌面  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\Desktop  |  
| CSIDL 等效项  | CSIDL_COMMON_DESKTOPDIRECTORY  |  
| 旧显示名称  | 桌面  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\Desktop  |  
 |  
|  

**FOLDERID_PublicDocuments** 
 |   
 | GUID  | {ED4824AF-DCE4-45A8-81E2-FC7965083634}  |  
| --- | --- |  
| 显示名称  | 公用文档  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\Documents  |  
| CSIDL 等效项  | CSIDL_COMMON_DOCUMENTS  |  
| 旧显示名称  | 共享文档  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\Documents  |  
 |  
|  

**FOLDERID_PublicDownloads** 
 |   
 | GUID  | {3D644C9B-1FB8-4f30-9B45-F670235F79C0}  |  
| --- | --- |  
| 显示名称  | 公用下载  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\Downloads  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_PublicGameTasks** 
 |   
 | GUID  | {DEBF2536-E1A8-4c59-B6A2-414586476AEA}  |  
| --- | --- |  
| 显示名称  | GameExplorer  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %ALLUSERSPROFILE%\Microsoft\Windows\GameExplorer  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_PublicLibraries** 
 |   
 | GUID  | {48DAF80B-E6CF-4F4E-B800-0E69D84EE384}  |  
| --- | --- |  
| 显示名称  | 库  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %ALLUSERSPROFILE%\Microsoft\Windows\Libraries  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_PublicMusic** 
 |   
 | GUID  | {3214FAB5-9757-4298-BB61-92A9DEAA44FF}  |  
| --- | --- |  
| 显示名称  | 公用音乐  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\Music  |  
| CSIDL 等效项  | CSIDL_COMMON_MUSIC  |  
| 旧显示名称  | 共享音乐  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\Documents\My Music  |  
 |  
|  

**FOLDERID_PublicPictures** 
 |   
 | GUID  | {B6EBFB86-6907-413C-9AF7-4FC2ABF07CC5}  |  
| --- | --- |  
| 显示名称  | 公用图片  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\Pictures  |  
| CSIDL 等效项  | CSIDL_COMMON_PICTURES  |  
| 旧显示名称  | 共享图片  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\Documents\My Pictures  |  
 |  
|  

**FOLDERID_PublicRingtones** 
 |   
 | GUID  | {E555AB60-153B-4D17-9F04-A5FE99FC15EC}  |  
| --- | --- |  
| 显示名称  | 铃声  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %ALLUSERSPROFILE%\Microsoft\Windows\Ringtones  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_PublicUserTiles** 
 |   
 | GUID  | {0482af6c-08f1-4c34-8c90-e17ec98b1e17}  |  
| --- | --- |  
| 显示名称  | 公共帐户图片  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\AccountPictures  |  
| CSIDL 等效项  | 无，Windows 8 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_PublicVideos** 
 |   
 | GUID  | {2400183A-6185-49FB-A2D8-4A392A602BA3}  |  
| --- | --- |  
| 显示名称  | 公用视频  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\Videos  |  
| CSIDL 等效项  | CSIDL_COMMON_VIDEO  |  
| 旧显示名称  | 共享视频  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\Documents\My Videos  |  
 |  
|  

**FOLDERID_QuickLaunch** 
 |   
 | GUID  | {52a4f021-7b75-48a9-9f6b-4b87a210bc8f}  |  
| --- | --- |  
| 显示名称  | 快速启动  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Internet Explorer\Quick Launch  |  
| CSIDL 等效项  | 无  |  
| 旧版显示名称  | 快速启动  |  
| 旧版默认路径  | %APPDATA%\Microsoft\Internet Explorer\快速启动  |  
 |  
|  

**FOLDERID_Recent** 
 |   
 | GUID  | {AE50C081-EBD2-438A-8655-8A092E34987A}  |  
| --- | --- |  
| 显示名称  | 最近使用的项目  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Recent  |  
| CSIDL 等效项  | CSIDL_RECENT  |  
| 旧版显示名称  | 我最近使用的文档  |  
| 旧版默认路径  | %USERPROFILE%\Recent  |  
 |  
|  

**FOLDERID_RecordedTV** 
 | 未使用。 从 Windows 7 起，此值未定义。  |  
|  

**FOLDERID_RecordedTVLibrary** 
 |   
 | GUID  | {1A6FDBA2-F42D-4358-A798-B74D745926C5}  |  
| --- | --- |  
| 显示名称  | 录制的电视  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\RecordedTV.library-ms  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_RecycleBinFolder** 
 |   
 | GUID  | {B7534046-3ECB-4C18-BE4E-64CD4CB7D6AC}  |  
| --- | --- |  
| 显示名称  | 回收站  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | CSIDL_BITBUCKET  |  
| 旧版显示名称  | 回收站  |  
| 旧版默认路径  | 不适用 - 虚拟文件夹  |  
 |  
|  

**FOLDERID_ResourceDir** 
 |   
 | GUID  | {8AD10C31-2ADB-4296-A8F7-E4701232C972}  |  
| --- | --- |  
| 显示名称  | 资源  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %windir%\Resources  |  
| CSIDL 等效项  | CSIDL_RESOURCES  |  
| 旧版显示名称  | 资源  |  
| 旧版默认路径  | %windir%\Resources  |  
 |  
|  

**FOLDERID_Ringtones** 
 |   
 | GUID  | {C870044B-F49E-4126-A9C3-B52A1FF411E8}  |  
| --- | --- |  
| 显示名称  | 铃声  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows\Ringtones  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_RoamingAppData** 
 |   
 | GUID  | {3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}  |  
| --- | --- |  
| 显示名称  | 漫游  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA% (%USERPROFILE%\AppData\Roaming)   |  
| CSIDL 等效项  | CSIDL_APPDATA  |  
| 旧版显示名称  | 应用程序数据  |  
| 旧版默认路径  | %APPDATA% (%USERPROFILE%\Application Data)   |  
 |  
|  

**FOLDERID_RoamedTileImages** 
 |   
 | GUID  | {AAA8D5A5-F1D6-4259-BAA8-78E7EF60835E}  |  
| --- | --- |  
| 显示名称  | RoamedTileImages  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows\RoamedTileImages  |  
| CSIDL 等效项  | 无，Windows 8 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_RoamingTiles** 
 |   
 | GUID  | {00BCFC5A-ED94-4e48-96A1-3F6217F21990}  |  
| --- | --- |  
| 显示名称  | RoamingTiles  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows\RoamingTiles  |  
| CSIDL 等效项  | 无，Windows 8 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SampleMusic** 
 |   
 | GUID  | {B250C668-F57D-4EE1-A63C-290EE7D1AA1F}  |  
| --- | --- |  
| 显示名称  | 示例音乐  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\Music\Sample Music  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 示例音乐  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\Documents\My Music\Sample Music  |  
 |  
|  

**FOLDERID_SamplePictures** 
 |   
 | GUID  | {C4900540-2379-4C75-844B-64E6FAF8716B}  |  
| --- | --- |  
| 显示名称  | 示例图片  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\Pictures\Sample Pictures  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 示例图片  |  
| 旧版默认路径  | %ALLUSERSPROFILE%\Documents\My Pictures\Sample Pictures  |  
 |  
|  

**FOLDERID_SamplePlaylists** 
 |   
 | GUID  | {15CA69B3-30EE-49C1-ACE1-6B5EC372AFB5}  |  
| --- | --- |  
| 显示名称  | 示例播放列表  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\Music\Sample Playlists  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SampleVideos** 
 |   
 | GUID  | {859EAD94-2E85-48AD-A71A-0969CB56A6CD}  |  
| --- | --- |  
| 显示名称  | 示例视频  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %PUBLIC%\Videos\Sample Videos  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SavedGames** 
 |   
 | GUID  | {4C5C32FF-BB9D-43b0-B5B4-2D72E54EAAA4}  |  
| --- | --- |  
| 显示名称  | 保存的游戏  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Saved Games  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SavedPictures** 
 |   
 | GUID  | {3B193882-D3AD-4eab-965A-69829D1FB59F}  |  
| --- | --- |  
| 显示名称  | 保存的图片  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Pictures\Saved Pictures  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SavedPicturesLibrary** 
 |   
 | GUID  | {E25B5812-BE88-4bd9-94B0-29233477B6C3}  |  
| --- | --- |  
| 显示名称  | 保存的图片库  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Libraries\SavedPictures.library-ms  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SavedSearches** 
 |   
 | GUID  | {7d1d3a04-debb-4115-95cf-2f29da2920da}  |  
| --- | --- |  
| 显示名称  | 搜索  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\搜索  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_Screenshots** 
 |   
 | GUID  | {b7bede81-df94-4682-a7d8-57a52620b86f}  |  
| --- | --- |  
| 显示名称  | 屏幕截图  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Pictures\屏幕截图  |  
| CSIDL 等效项  | 无，Windows 8 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SEARCH_CSC** 
 |   
 | GUID  | {ee32e446-31ca-4aba-814f-a5ebd2fd6d5e}  |  
| --- | --- |  
| 显示名称  | 脱机文件  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SearchHistory** 
 |   
 | GUID  | {0D4C3DB6-03A3-462F-A0E6-08924C41B5D4}  |  
| --- | --- |  
| 显示名称  | 历史记录  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows\ConnectedSearch\History  |  
| CSIDL 等效项  | 无，Windows 8.1中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SearchHome** 
 |   
 | GUID  | {190337d1-b8ca-4121-a639-6d472d16972a}  |  
| --- | --- |  
| 显示名称  | 搜索结果  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SEARCH_MAPI** 
 |   
 | GUID  | {98ec0e18-2098-4d44-8644-66979315a281}  |  
| --- | --- |  
| 显示名称  | Microsoft Office Outlook  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SearchTemplates** 
 |   
 | GUID  | {7E636BFE-DFA9-4D5E-B456-D7B39851D8A9}  |  
| --- | --- |  
| 显示名称  | 模板  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows\ConnectedSearch\Templates  |  
| CSIDL 等效项  | 无，Windows 8.1中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SendTo** 
 |   
 | GUID  | {8983036C-27C0-404B-8F08-102D10DCFD74}  |  
| --- | --- |  
| 显示名称  | SendTo  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\SendTo  |  
| CSIDL 等效项  | CSIDL_SENDTO  |  
| 旧版显示名称  | SendTo  |  
| 旧版默认路径  | %USERPROFILE%\SendTo  |  
 |  
|  

**FOLDERID_SidebarDefaultParts** 
 |   
 | GUID  | {7B396E54-9EC5-4300-BE0A-2482EBAE1A26}  |  
| --- | --- |  
| 显示名称  | 产品  |  
| 文件夹类型  | COMMON  |  
| Default Path  | %ProgramFiles%\Windows 边栏\小工具  |  
| CSIDL 等效项  | 无，Windows 7 新增功能  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SidebarParts** 
 |   
 | GUID  | {A75D362E-50FC-4fb7-AC2C-A8BEAA314493}  |  
| --- | --- |  
| 显示名称  | 产品  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Microsoft\Windows 边栏\小工具  |  
| CSIDL 等效项  | 无，Windows 7 新增功能  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SkyDrive** 
 |   
 | GUID  | {A52BBA46-E9E1-435f-B3D9-28DAA648C0F6}  |  
| --- | --- |  
| 显示名称  | OneDrive  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\OneDrive  |  
| CSIDL 等效项  | 无，Windows 8.1中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SkyDriveCameraRoll** 
 |   
 | GUID  | {767E6811-49CB-4273-87C2-20F355E1085B}  |  
| --- | --- |  
| 显示名称  | 本机照片  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\OneDrive\Pictures\Camera Roll  |  
| CSIDL 等效项  | 无，Windows 8.1中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SkyDriveDocuments** 
 |   
 | GUID  | {24D89E24-2F19-4534-9DDE-6A6671FBB8FE}  |  
| --- | --- |  
| 显示名称  | 文档  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\OneDrive\Documents  |  
| CSIDL 等效项  | 无，Windows 8.1中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SkyDrivePictures** 
 |   
 | GUID  | {339719B5-8C47-4894-94C2-D8F77ADD44A6}  |  
| --- | --- |  
| 显示名称  | 图片  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\OneDrive\Pictures  |  
| CSIDL 等效项  | 无，Windows 8.1中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_StartMenu** 
 |   
 | GUID  | {625B53C3-AB48-4EC1-BA1F-A1EF4146FC19}  |  
| --- | --- |  
| 显示名称  | “开始”菜单  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Start Menu  |  
| CSIDL 等效项  | CSIDL_STARTMENU  |  
| 旧版显示名称  | “开始”菜单  |  
| 旧版默认路径  | %USERPROFILE%\“开始”菜单  |  
 |  
|  

**FOLDERID_Startup** 
 |   
 | GUID  | {B97D20BB-F46A-4C97-BA10-5E3608430854}  |  
| --- | --- |  
| 显示名称  | 启动  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Start Menu\Programs\StartUp  |  
| CSIDL 等效项  | CSIDL_STARTUP、CSIDL_ALTSTARTUP  |  
| 旧版显示名称  | 启动  |  
| 旧版默认路径  | %USERPROFILE%\开始菜单\Programs\StartUp  |  
 |  
|  

**FOLDERID_SyncManagerFolder** 
 |   
 | GUID  | {43668BF8-C14E-49B2-97C9-747784D784B7}  |  
| --- | --- |  
| 显示名称  | 同步中心  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SyncResultsFolder** 
 |   
 | GUID  | {289a9a43-be44-4057-a41b-587a76d7e7f9}  |  
| --- | --- |  
| 显示名称  | 同步结果  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧版显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_SyncSetupFolder** 
 |   
 | GUID  | {0F214138-B1D3-4a90-BBA9-27CBC0C5389A}  |  
| --- | --- |  
| 显示名称  | 同步设置  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无，Windows Vista 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_System** 
 |   
 | GUID  | {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}  |  
| --- | --- |  
| 显示名称  | System32  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %windir%\system32  |  
| CSIDL 等效项  | CSIDL_SYSTEM  |  
| 旧显示名称  | system32  |  
| 旧版默认路径  | %windir%\system32  |  
 |  
|  

**FOLDERID_SystemX86** 
 |   
 | GUID  | {D65231B0-B2F1-4857-A4CE-A8E7C6EA7D27}  |  
| --- | --- |  
| 显示名称  | System32  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %windir%\system32  |  
| CSIDL 等效项  | CSIDL_SYSTEMX86  |  
| 旧显示名称  | system32  |  
| 旧版默认路径  | %windir%\system32  |  
 |  
|  

**FOLDERID_Templates** 
 |   
 | GUID  | {A63293E8-664E-48DB-A079-DF759E0509F7}  |  
| --- | --- |  
| 显示名称  | 模板  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Templates  |  
| CSIDL 等效项  | CSIDL_TEMPLATES  |  
| 旧显示名称  | 模板  |  
| 旧版默认路径  | %USERPROFILE%\Templates  |  
 |  
|  

**FOLDERID_TreeProperties** 
 | 不在 Windows Vista 中使用。 自 Windows 7 起不受支持。  |  
|  

**FOLDERID_UserPinned** 
 |   
 | GUID  | {9E3995AB-1F9C-4F13-B827-48B24B6C7174}  |  
| --- | --- |  
| 显示名称  | 用户已固定  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Internet Explorer\Quick Launch\User Pinned  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_UserProfiles** 
 |   
 | GUID  | {0762D272-C50A-4BB0-A382-697DCD729B80}  |  
| --- | --- |  
| 显示名称  | 用户  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %SystemDrive%\Users  |  
| CSIDL 等效项  | 无，Windows Vista 新增功能  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_UserProgramFiles** 
 |   
 | GUID  | {5CD7AEE2-2219-4A67-B85D-6C9CE15660CB}  |  
| --- | --- |  
| 显示名称  | Programs  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Programs  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_UserProgramFilesCommon** 
 |   
 | GUID  | {BCBD3057-CA5C-4622-B42D-BC56DB0AE516}  |  
| --- | --- |  
| 显示名称  | Programs  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %LOCALAPPDATA%\Programs\Common  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_UsersFiles** 
 |   
 | GUID  | {f3ce0f7c-4901-4acc-8648-d5d44b04ef8f}  |  
| --- | --- |  
| 显示名称  | 例如，创建用户帐户时，) 输入用户的全名 (Jean Philippe Bagel。  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_UsersLibraries** 
 |   
 | GUID  | {A302545D-DEFF-464b-ABE8-61C8648D939B}  |  
| --- | --- |  
| 显示名称  | 库  |  
| 文件夹类型  | 虚拟  |  
| Default Path  | 不适用 - 虚拟文件夹  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_Videos** 
 |   
 | GUID  | {18989B1D-99B5-455B-841C-AB7C74E4DDFC}  |  
| --- | --- |  
| 显示名称  | 视频  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %USERPROFILE%\Videos  |  
| CSIDL  | CSIDL_MYVIDEO  |  
| 旧显示名称  | 我的视频  |  
| 旧版默认路径  | %USERPROFILE%\My Documents\My Videos  |  
 |  
|  

**FOLDERID_VideosLibrary** 
 |   
 | GUID  | {491E922F-5643-4AF4-A7EB-4E7A138D8174}  |  
| --- | --- |  
| 显示名称  | 视频  |  
| 文件夹类型  | PERUSER  |  
| Default Path  | %APPDATA%\Microsoft\Windows\Libraries\Videos.library-ms  |  
| CSIDL 等效项  | 无，Windows 7 中引入的值  |  
| 旧显示名称  | 不适用  |  
| 旧版默认路径  | 不适用  |  
 |  
|  

**FOLDERID_Windows** 
 |   
 | GUID  | {F38BF404-1D43-42F2-9305-67DE0B28FC23}  |  
| --- | --- |  
| 显示名称  | Windows  |  
| 文件夹类型  | FIXED  |  
| Default Path  | %windir%  |  
| CSIDL 等效项  | CSIDL_WINDOWS  |  
| 旧显示名称  | WINDOWS  |  
| 旧版默认路径  | %windir%  |  
 |  
## 备注
某些 **KNOWNFOLDERID** 值的解释取决于文件夹是 32 位还是 64 位应用程序的一部分，以及该应用程序是在 32 位还是 64 位操作系统上运行。 如果应用程序需要区分程序**文件和****程序文件 (x86)** ，则必须使用正确的 **KNOWNFOLDERID** 来应对这种情况。
下表总结了在这些情况下 **的 KNOWNFOLDERID** 用法。
**FOLDERID_ProgramFiles**  
| 操作系统  | 应用程序  | KNOWNFOLDERID  | Default Path  | CSIDL 等效项  |  
| --- | --- | --- | --- | --- |  
| 32 位  | 32 位  | FOLDERID_ProgramFiles  | %SystemDrive%\Program Files  | CSIDL_PROGRAM_FILES  |  
| 32 位  | 32 位  | FOLDERID_ProgramFilesX86  | %SystemDrive%\Program Files  | CSIDL_PROGRAM_FILESX86  |  
| 32 位  | 32 位  | ) 32 位操作系统不支持FOLDERID_ProgramFilesX64 (  | 不适用  | 不适用  |  
| 64 位  | 64 位  | FOLDERID_ProgramFiles  | %SystemDrive%\Program Files  | CSIDL_PROGRAM_FILES  |  
| 64 位  | 64 位  | FOLDERID_ProgramFilesX86  | %SystemDrive%\Program Files (x86)   | CSIDL_PROGRAM_FILESX86  |  
| 64 位  | 64 位  | FOLDERID_ProgramFilesX64  | %SystemDrive%\Program Files  | 无  |  
| 64 位  | 32 位  | FOLDERID_ProgramFiles  | %SystemDrive%\Program Files (x86)   | CSIDL_PROGRAM_FILES  |  
| 64 位  | 32 位  | FOLDERID_ProgramFilesX86  | %SystemDrive%\Program Files (x86)   | CSIDL_PROGRAM_FILESX86  |  
| 64 位  | 32 位  | 32 位应用程序不支持FOLDERID_ProgramFilesX64 ()   | 不适用  | 不适用  |  
**FOLDERID_ProgramFilesCommon**  
| 操作系统  | 应用程序  | KNOWNFOLDERID  | Default Path  | CSIDL 等效项  |  
| --- | --- | --- | --- | --- |  
| 32 位  | 32 位  | FOLDERID_ProgramFilesCommon  | %ProgramFiles%\Common Files  | CSIDL_PROGRAM_FILES_COMMON  |  
| 32 位  | 32 位  | FOLDERID_ProgramFilesCommonX86  | %ProgramFiles%\Common Files  | CSIDL_PROGRAM_FILES_COMMONX86  |  
| 32 位  | 32 位  | FOLDERID_ProgramFilesCommonX64 (未定义的)   | 不适用  | 不适用  |  
| 64 位  | 64 位  | FOLDERID_ProgramFilesCommon  | %ProgramFiles%\Common Files  | CSIDL_PROGRAM_FILES_COMMON  |  
| 64 位  | 64 位  | FOLDERID_ProgramFilesCommonX86  | %ProgramFiles (x86) %\Common Files  | CSIDL_PROGRAM_FILES_COMMONX86  |  
| 64 位  | 64 位  | FOLDERID_ProgramFilesCommonX64  | %ProgramFiles%\Common Files  | 无  |  
| 64 位  | 32 位  | FOLDERID_ProgramFilesCommon  | %ProgramFiles (x86) %\Common Files  | CSIDL_PROGRAM_FILES_COMMON  |  
| 64 位  | 32 位  | FOLDERID_ProgramFilesCommonX86  | %ProgramFiles (x86) %\Common Files  | CSIDL_PROGRAM_FILES_COMMONX86  |  
| 64 位  | 32 位  | FOLDERID_ProgramFilesCommonX64  | %ProgramFiles%\Common Files  | 无  |  
**FOLDERID_System**  
| 操作系统  | 应用程序  | KNOWNFOLDERID  | Default Path  | CSIDL 等效项  |  
| --- | --- | --- | --- | --- |  
| 32 位  | 32 位  | FOLDERID_System  | %windir%\system32  | CSIDL_SYSTEM  |  
| 32 位  | 32 位  | FOLDERID_SystemX86  | %windir%\system32  | CSIDL_SYSTEMX86  |  
| 64 位  | 64 位  | FOLDERID_System  | %windir%\system32  | CSIDL_SYSTEM  |  
| 64 位  | 64 位  | FOLDERID_SystemX86  | %windir%\syswow64  | CSIDL_SYSTEMX86  |  
| 64 位  | 32 位  | FOLDERID_System  | %windir%\system32  | CSIDL_SYSTEM  |  
| 64 位  | 32 位  | FOLDERID_SystemX86  | %windir%\syswow64  | CSIDL_SYSTEMX86  |  
我们已使用环境字符串在整个本主题中提供泛型路径。 下表提供了这些环境字符串表示的路径的示例。 在某些情况下，这些路径可能与特定计算机上的路径不匹配，因为在安装过程中或以后的文件夹重定向期间进行了选择。 请注意，Windows Vista 的某些路径已更改。
**Windows Vista 及更高版本**  
| 环境字符串  | 示例路径  |  
| --- | --- |  
| %ALLUSERSPROFILE%  | C:\ProgramData  |  
| %APPDATA%  | C：\Users\_username_ \AppData\Roaming  |  
| %LOCALAPPDATA%  | C：\Users\_username_ \AppData\Local  |  
| %ProgramData%  | C:\ProgramData  |  
| %ProgramFiles%  | C:\Program Files  |  
| %ProgramFiles(x86)%  | C：\Program Files (x86)   |  
| %PUBLIC%  | C：\Users\Public  |  
| %SystemDrive%  | C:  |  
| %USERPROFILE%  | C：\Users\_username_  |  
| %windir%  | C:\Windows  |  
**Windows XP 及更早版本**  
| 环境字符串  | 示例路径  |  
| --- | --- |  
| %ALLUSERSPROFILE%  | C：\Documents and Settings\All Users  |  
| %APPDATA%  | C：\Documents and Settings\_username_ \Application Data  |  
| %ProgramFiles%  | C:\Program Files  |  
| %SystemDrive%  | C:  |  
| %USERPROFILE%  | C：\Documents and Settings\_username_  |  
| %windir%  | C:\Windows  |  
## 要求  
| 标头   |  

Knownfolders.h
 |  
| --- | --- |  
## 请参阅 


[ **CSIDL**](https://learn.microsoft.com/zh-cn/windows/win32/shell/csidl)







[在应用程序中使用已知文件夹](https://learn.microsoft.com/zh-cn/windows/win32/shell/working-with-known-folders)




[如何使用自定义文件夹扩展已知文件夹](https://learn.microsoft.com/zh-cn/windows/win32/shell/how-to-extend-known-folders-with-custom-folders)





## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2023-06-13 


