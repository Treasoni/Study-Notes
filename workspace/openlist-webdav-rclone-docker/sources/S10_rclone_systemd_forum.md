---
url: "https://forum.rclone.org/t/how-to-mount-rclone-persistently-on-fedora-linux-on-boot/53738"
title: "How to mount Rclone persistently on Fedora Linux (on boot) - Howto Guides - rclone forum"
scraped_at: 2026-09-11T17:05:11+00:00
---

[ Skip to main content ](https://forum.rclone.org/t/how-to-mount-rclone-persistently-on-fedora-linux-on-boot/53738#main-container)
#  [ How to mount Rclone persistently on Fedora Linux (on boot) ](https://forum.rclone.org/t/how-to-mount-rclone-persistently-on-fedora-linux-on-boot/53738)
You have selected **0** posts.
[ select all ](https://forum.rclone.org/t/how-to-mount-rclone-persistently-on-fedora-linux-on-boot/53738)
[ cancel selecting ](https://forum.rclone.org/t/how-to-mount-rclone-persistently-on-fedora-linux-on-boot/53738)
[ May 3  ](https://forum.rclone.org/t/how-to-mount-rclone-persistently-on-fedora-linux-on-boot/53738/1 "Jump to the first post")
1 / 1 
May 3 
[ ](https://forum.rclone.org/t/how-to-mount-rclone-persistently-on-fedora-linux-on-boot/53738/1)
##  post by The-Lirio on May 3 
[ The-Lirio ](https://forum.rclone.org/u/the-lirio)
[ ](https://forum.rclone.org/t/how-to-mount-rclone-persistently-on-fedora-linux-on-boot/53738 "Post date")
How to auto-mount rclone on boot with systemd on Fedora
  1. Enable user_allow_other in FUSE (without it, it will not work) The --allow-other flag (which lets other users access the mount) requires explicit permission in /etc/fuse.conf. sed command: bashsudo sed -i 's/# user_allow_other/user_allow_other/' /etc/fuse.conf Verify: bashgrep user_allow_other /etc/fuse.conf


#  should output: user_allow_other
  1. Create the log file directory The service runs as your user, so it can't write to /var/log/. Use a user-owned directory instead: bashmkdir -p ~/.local/log
  2. Create the systemd service file bashsudo nano /etc/systemd/system/rclone-gdrive.service Paste the following, adjusting the remote name and paths to match yours: ini[Unit] Description=rclone Google Drive AssertPathIsDirectory=/home/YOUR_USER/google_drive After=network-online.target


[Service] Type=notify User=YOUR_USER ExecStart=/usr/bin/rclone mount --config=/home/YOUR_USER/.config/rclone/rclone.conf --vfs-cache-mode full --vfs-cache-max-age 4h --vfs-fast-fingerprint --vfs-refresh --allow-other --log-file=/home/YOUR_USER/.local/log/rclone_gdrive.log --log-level INFO "YourRemote:" /home/YOUR_USER/google_drive ExecStop=/bin/fusermount3 -u /home/YOUR_USER/google_drive Restart=always RestartSec=10
[Install] WantedBy=default.target Key notes vs. other guides you may find:
Type=notify instead of Type=simple — rclone supports sd_notify, so systemd will know when the mount is actually ready (I saw another guide recommending simple) fusermount3 instead of fusermount — Fedora uses FUSE3 Log file under ~/.local/log/ instead of /var/log/ — the service runs as a regular user and has no write access to /var/log/
  1. Enable and start the service bashsudo systemctl daemon-reload sudo systemctl enable --now rclone-gdrive.service
  2. Verify bashsystemctl status rclone-gdrive.service You should see Active: active (running).


If the service fails, check the log file directly rather than relying solely on journalctl: bashcat ~/.local/log/rclone_gdrive.log
(It is more detailed this way)
388 views 
Reply
###  New & Unread Topics   
Topic list, column headers with buttons are sortable.  
|  Topic   |  Replies   |  Views   |  Activity   |  
| --- | --- | --- | --- |  
|  [Autofs + rclone mount for Google Drive](https://forum.rclone.org/t/autofs-rclone-mount-for-google-drive/53243)  |  
|   |  
|  [macOS, `rclone mount` with fuse-t via FSKit](https://forum.rclone.org/t/macos-rclone-mount-with-fuse-t-via-fskit/53608)  |  
|  [How to prevent KDE Dolphin from freezing when using rclone FUSE mounts (Google Drive, OneDrive, etc.)](https://forum.rclone.org/t/how-to-prevent-kde-dolphin-from-freezing-when-using-rclone-fuse-mounts-google-drive-onedrive-etc/53829)  |  
|  [Build a Reproducible rclone Transfer Evidence Pack](https://forum.rclone.org/t/build-a-reproducible-rclone-transfer-evidence-pack/54059)  |  
###  Want to read more? Browse other topics in [Howto Guides](https://forum.rclone.org/c/howto/10) or [view latest topics](https://forum.rclone.org/latest). 
[ Powered by Discourse ](https://discourse.org/powered-by)
