---
url: "https://learn.microsoft.com/en-us/windows/win32/fileio/sparse-file-operations"
title: "Sparse File Operations - Win32 apps | Microsoft Learn"
scraped_at: 2026-09-10T15:41:37+00:00
---

Table of contents  Exit editor mode
Ask Learn Ask Learn
Reading mode Table of contents [ Read in English ](https://learn.microsoft.com/en-us/windows/win32/fileio/sparse-file-operations) Add to Plans [ Edit ](https://github.com/MicrosoftDocs/win32/blob/docs/desktop-src/FileIO/sparse-file-operations.md) Copy Markdown Print
Note
Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/windows/win32/fileio/sparse-file-operations) or changing directories. 
Access to this page requires authorization. You can try changing directories. 
# Sparse File Operations
Feedback
Summarize this article for me 
To determine whether a file system supports sparse files, call the [**GetVolumeInformation**](https://learn.microsoft.com/en-us/windows/desktop/api/FileAPI/nf-fileapi-getvolumeinformationa) function and examine the **FILE_SUPPORTS_SPARSE_FILES** bit flag returned through the _lpFileSystemFlags_ parameter.
Most applications are not aware of sparse files and will not create sparse files. The fact that an application is reading a sparse file is transparent to the application. An application that is aware of sparse-files should determine whether its data set is suitable to be kept in a sparse file. After that determination is made, the application must explicitly declare a file as sparse, using the [**FSCTL_SET_SPARSE**](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_set_sparse) control code.
After an application has set a file to be sparse, the application can use the [**FSCTL_SET_ZERO_DATA**](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_set_zero_data) control code to set a region of the file to zero. In addition, the application can use the [**FSCTL_QUERY_ALLOCATED_RANGES**](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_query_allocated_ranges) control code to speed searches for nonzero data in the sparse file.
When you perform a write operation (with a function or operation other than [**FSCTL_SET_ZERO_DATA**](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_set_zero_data)) whose data consists of nothing but zeros, zeros will be written to the disk for the entire length of the write. To zero out a range of the file and maintain sparseness, use **FSCTL_SET_ZERO_DATA**.
A sparseness-aware application may also set an existing file to be sparse. If an application sets an existing file to be sparse, it should then scan the file for regions which contain zeros, and use [**FSCTL_SET_ZERO_DATA**](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_set_zero_data) to reset those regions, thereby possibly deallocating some physical disk storage. An application upgraded to sparse file awareness should perform this conversion.
When you perform a read operation from a zeroed-out portion of a sparse file, the operating system may not read from the hard disk drive. Instead, the system recognizes that the portion of the file to be read contains zeros, and it returns a buffer full of zeros without actually reading from the disk.
As with any other file, the system can write data to or read data from any position in a sparse file. Nonzero data being written to a previously zeroed portion of the file may result in allocation of disk space. Zeros being written over nonzero data (only with [**FSCTL_SET_ZERO_DATA**](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_set_zero_data)) may result in a deallocation of disk space.
Note
It is up to the application to maintain sparseness by writing zeros with [**FSCTL_SET_ZERO_DATA**](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_set_zero_data).
Defragmentation tools that handle compressed files on NTFS file systems will correctly handle sparse files on NTFS file system volumes. Large and highly fragmented sparse files can exceed the NTFS limitation on disk extents before available space is used.
## Feedback
Was this page helpful? 
Yes
Need help with this topic? 
Want to try using Ask Learn to clarify or guide you through this topic? 
Ask Learn Ask Learn
Suggest a fix? 
##  Additional resources 
  * Last updated on  2022-01-26 


