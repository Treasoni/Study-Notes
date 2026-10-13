---
url: "https://docs.linuxserver.io/images/docker-qbittorrent/"
title: "qbittorrent - LinuxServer.io"
scraped_at: 2026-10-07T14:40:56+00:00
---

#  [linuxserver/qbittorrent](https://github.com/linuxserver/docker-qbittorrent)[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#linuxserverqbittorrent "Permanent link")
The [Qbittorrent](https://www.qbittorrent.org/) is a bittorrent client programmed in C++ / Qt that uses libtorrent (sometimes called libtorrent-rasterbar) by Arvid Norberg.
## Supported Architectures[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#supported-architectures "Permanent link")
We utilise the docker manifest for multi-platform awareness. More information is available from docker [here](https://distribution.github.io/distribution/spec/manifest-v2-2/#manifest-list) and our announcement [here](https://blog.linuxserver.io/2019/02/21/the-lsio-pipeline-project/).
Simply pulling `lscr.io/linuxserver/qbittorrent:latest` should retrieve the correct image for your arch, but you can also pull specific arch images via tags.
The architectures supported by this image are:  
| Architecture  | Available  | Tag  |  
| --- | --- | --- |  
| x86-64  | ✅  | amd64-<version tag>  |  
| arm64  | ✅  | arm64v8-<version tag>  |  
## Version Tags[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#version-tags "Permanent link")
This image provides various versions that are available via tags. Please read the descriptions carefully and exercise caution when using unstable or development tags.  
| Tag  | Available  | Description  |  
| --- | --- | --- |  
| latest  | ✅  | Stable qbittorrent releases using libtorrent v2  |  
| libtorrentv1  | ✅  | Stable qbittorrent releases using libtorrent v1  |  
## Application Setup[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#application-setup "Permanent link")
The web UI is at `<your-ip>:8080` and a temporary password for the `admin` user will be printed to the container log on startup.
You must then change username/password in the web UI section of settings. If you do not change the password a new one will be generated every time the container starts.
If you are running a very old (3.x) kernel you may run into [this issue](https://github.com/linuxserver/docker-qbittorrent/issues/103) which can be worked around using [this method](https://github.com/linuxserver/docker-qbittorrent/issues/103#issuecomment-831238484)
### WEBUI_PORT variable[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#webui_port-variable "Permanent link")
Due to issues with CSRF and port mapping, should you require to alter the port for the web UI you need to change both sides of the -p 8080 switch AND set the WEBUI_PORT variable to the new port.
For example, to set the port to 8123 you need to set -p 8123:8123 and -e WEBUI_PORT=8123
### TORRENTING_PORT[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#torrenting_port "Permanent link")
A bittorrent client can be an active or a passive node. Running your client as an active node has the advantage of being able to connect to both active and passive peers, and can potentially increase the number of incoming connections. This requires an open port on the host machine which might differ from container's internal one.
Similarly to the WEBUI_PORT, to set the port to 6887 you need to pass -p 6887:6887, -p 6887:6887/udp and -e TORRENTING_PORT=6887 arguments to Docker.
## Read-Only Operation[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#read-only-operation "Permanent link")
This image can be run with a read-only container filesystem. For details please [read the docs](https://docs.linuxserver.io/misc/read-only/).
## Non-Root Operation[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#non-root-operation "Permanent link")
This image can be run with a non-root user. For details please [read the docs](https://docs.linuxserver.io/misc/non-root/).
## Usage[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#usage "Permanent link")
To help you get started creating a container from this image you can either use docker-compose or the docker cli.
Info
Unless a parameter is flagged as 'optional', it is _mandatory_ and a value must be provided.
### docker-compose (recommended, [click here for more info](https://docs.linuxserver.io/general/docker-compose))[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#docker-compose-recommended-click-here-for-more-info "Permanent link")

```
services:
qbittorrent:
image:lscr.io/linuxserver/qbittorrent:latest
container_name:qbittorrent
environment:
-PUID=1000
-PGID=1000
-TZ=Etc/UTC
-WEBUI_PORT=8080
-TORRENTING_PORT=6881
volumes:
-/path/to/qbittorrent/appdata:/config
-/path/to/downloads:/downloads#optional
-8080:8080
-6881:6881
-6881:6881/udp
stop_grace_period:"10s"#optional
restart:unless-stopped

```

### docker cli ([click here for more info](https://docs.docker.com/engine/reference/commandline/cli/))[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#docker-cli-click-here-for-more-info "Permanent link")

```
dockerrun-d\
--name=qbittorrent\
-ePUID=1000\
-ePGID=1000\
-eTZ=Etc/UTC\
-eWEBUI_PORT=8080\
-eTORRENTING_PORT=6881\
-p8080:8080\
-p6881:6881\
-p6881:6881/udp\
-v/path/to/qbittorrent/appdata:/config\
-v/path/to/downloads:/downloads`#optional` \
--stop-timeout="10s"`#optional` \
--restartunless-stopped\
lscr.io/linuxserver/qbittorrent:latest

```

## Parameters[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#parameters "Permanent link")
Containers are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. For example, `-p 8080:80` would expose port `80` from inside the container to be accessible from the host's IP on port `8080` outside the container.
### Ports (`-p`)[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#ports-p "Permanent link")  
| Parameter  | Function  |  
| --- | --- |  
| `8080:8080`  | WebUI  |  
| `6881:6881`  | tcp connection port  |  
| `6881:6881/udp`  | udp connection port  |  
### Environment Variables (`-e`)[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#environment-variables-e "Permanent link")  
| Env  | Function  |  
| --- | --- |  
| `PUID=1000`  | for UserID - see below for explanation  |  
| `PGID=1000`  | for GroupID - see below for explanation  |  
| `TZ=Etc/UTC`  | specify a timezone to use, see this [list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List).  |  
| `WEBUI_PORT=8080`  | for changing the port of the web UI, see below for explanation  |  
| `TORRENTING_PORT=6881`  | for changing the port of tcp/udp connection, see below for explanation  |  
### Volume Mappings (`-v`)[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#volume-mappings-v "Permanent link")  
| Volume  | Function  |  
| --- | --- |  
| `/config`  | Contains all relevant configuration files.  |  
| `/downloads`  | Location of downloads on disk.  |  
#### Miscellaneous Options[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#miscellaneous-options "Permanent link")  
| Parameter  | Function  |  
| --- | --- |  
| `--stop-timeout=`  | If you have a large number of torrents you may need to increase the container stop timeout to ensure a clean shutdown.  |  
| `--read-only=true`  | Run container with a read-only filesystem. Please [read the docs](https://docs.linuxserver.io/misc/read-only/).  |  
| `--user=1000:1000`  | Run container with a non-root user. Please [read the docs](https://docs.linuxserver.io/misc/non-root/).  |  
## Environment variables from files (Docker secrets)[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#environment-variables-from-files-docker-secrets "Permanent link")
You can set any environment variable from a file by using a special prepend `FILE__`.
As an example:

```
-eFILE__MYVAR=/run/secrets/mysecretvariable

```

Will set the environment variable `MYVAR` based on the contents of the `/run/secrets/mysecretvariable` file.
## Umask for running applications[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#umask-for-running-applications "Permanent link")
For all of our images we provide the ability to override the default umask settings for services started within the containers using the optional `-e UMASK=022` setting. Keep in mind umask is not chmod it subtracts from permissions based on it's value it does not add. Please read up [here](https://en.wikipedia.org/wiki/Umask) before asking for support.
## User / Group Identifiers[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#user-group-identifiers "Permanent link")
When using volumes (`-v` flags), permissions issues can arise between the host OS and the container, we avoid this issue by allowing you to specify the user `PUID` and group `PGID`.
Ensure any volume directories on the host are owned by the same user you specify and any permissions issues will vanish like magic.
In this instance `PUID=1000` and `PGID=1000`, to find yours use `id your_user` as below:

```
idyour_user

```

Example output:

```
uid=1000(your_user) gid=1000(your_user) groups=1000(your_user)

```

## Docker Mods[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#docker-mods "Permanent link")
We publish various [Docker Mods](https://github.com/linuxserver/docker-mods) to enable additional functionality within the containers. The list of Mods available for this image (if any) as well as universal mods that can be applied to any one of our images can be accessed via the dynamic badges above.
## Support Info[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#support-info "Permanent link")
  * Shell access whilst the container is running:

```
dockerexec-itqbittorrent/bin/bash

```

  * To monitor the logs of the container in realtime:

```
dockerlogs-fqbittorrent

```

  * Container version number:

```
dockerinspect-f'{{ index .Config.Labels "build_version" }}'qbittorrent

```

  * Image version number:

```
dockerinspect-f'{{ index .Config.Labels "build_version" }}'lscr.io/linuxserver/qbittorrent:latest

```



## Updating Info[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#updating-info "Permanent link")
Most of our images are static, versioned, and require an image update and container recreation to update the app inside. With some exceptions (noted in the relevant readme.md), we do not recommend or support updating apps inside the container. Please consult the [Application Setup](https://docs.linuxserver.io/images/docker-qbittorrent/#application-setup) section above to see if it is recommended for the image.
Below are the instructions for updating containers:
### Via Docker Compose[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#via-docker-compose "Permanent link")
  * Update images:
    * All images:

```
docker-composepull

```

    * Single image:

```
docker-composepullqbittorrent

```

  * Update containers:
    * All containers:

```
docker-composeup-d

```

    * Single container:

```
docker-composeup-dqbittorrent

```

  * You can also remove the old dangling images:

```
dockerimageprune

```



### Via Docker Run[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#via-docker-run "Permanent link")
  * Update the image:

```
dockerpulllscr.io/linuxserver/qbittorrent:latest

```

  * Stop the running container:

```
dockerstopqbittorrent

```

  * Delete the container:

```
dockerrmqbittorrent

```

  * Recreate a new container with the same docker run parameters as instructed above (if mapped correctly to a host folder, your `/config` folder and settings will be preserved)
  * You can also remove the old dangling images:

```
dockerimageprune

```



### Image Update Notifications - Diun (Docker Image Update Notifier)[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#image-update-notifications-diun-docker-image-update-notifier "Permanent link")
Tip
We recommend [Diun](https://crazymax.dev/diun/) for update notifications. Other tools that automatically update containers unattended are not recommended or supported.
## Building locally[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#building-locally "Permanent link")
If you want to make local modifications to these images for development purposes or just to customize the logic:

```
gitclonehttps://github.com/linuxserver/docker-qbittorrent.git
cddocker-qbittorrent
dockerbuild\
--no-cache\
--pull\
-tlscr.io/linuxserver/qbittorrent:latest.

```

The ARM variants can be built on x86_64 hardware and vice versa using `lscr.io/linuxserver/qemu-static`

```
dockerrun--rm--privilegedlscr.io/linuxserver/qemu-static--reset

```

Once registered you can define the dockerfile to use with `-f Dockerfile.aarch64`.
To help with development, we generate this dependency graph.
Init dependency graph
qbittorrent:latestBase Imagesdocker-modsbaselegacy-servicescustom servicesinit-servicesci-service-checkinit-migrationsinit-adduserinit-os-endinit-configinit-config-endinit-crontab-configinit-qbittorrent-configinit-mods-endinit-custom-filesinit-device-permsinit-envfileinit-modsinit-mods-package-installsvc-cronsvc-qbittorrentbaseimage-alpine:3.24fix-attr +legacy cont-init
qbittorrent:latestBase Imagesdocker-modsbaselegacy-servicescustom servicesinit-servicesci-service-checkinit-migrationsinit-adduserinit-os-endinit-configinit-config-endinit-crontab-configinit-qbittorrent-configinit-mods-endinit-custom-filesinit-device-permsinit-envfileinit-modsinit-mods-package-installsvc-cronsvc-qbittorrentbaseimage-alpine:3.24fix-attr +legacy cont-init
## Versions[¶](https://docs.linuxserver.io/images/docker-qbittorrent/#versions "Permanent link")
  * **05.07.26:** - Rebase to Alpine 3.24.
  * **04.05.26:** - Switch to static builds for parity with libtorrentv1 branch. Rebase to Alpine 3.23.
  * **17.07.24:** - Restore qbittorrent-cli as it now supports openssl 3.
  * **25.05.24:** - Remove qbittorrent-cli as it still requires openssl 1.1 which is EOL.
  * **14.02.24:** - Only set/override torrenting port if the optional env var is set.
  * **14.02.24:** - Add torrenting port support.
  * **31.01.24:** - Remove obsolete compat packages.
  * **25.12.23:** - Only pull stable releases of qbittorrent-cli.
  * **07.10.23:** - Install unrar from [linuxserver repo](https://github.com/linuxserver/docker-unrar).
  * **10.08.23:** - Bump unrar to 6.2.10.
  * **17.06.23:** - Deprecate armhf as per <https://www.linuxserver.io/armhf>.
  * **10.06.23:** - Bump unrar to 6.2.8.
  * **23.02.23:** - Add qt6-qtbase-sqlite to support SQLite database for resume files.
  * **29.11.22:** - Add openssl1.1-compat for qbittorrent-cli.
  * **31.10.22:** - Add libtorrentv1 branch.
  * **31.08.22:** - Rebase to Alpine Edge again to follow latest releases.
  * **12.08.22:** - Bump unrar to 6.1.7.
  * **16.06.22:** - Rebase to Alpine 3.16 from edge.
  * **25.05.22:** - Fetch qbitorrent-cli from upstream repo.
  * **02.03.22:** - Add unrar, 7zip, and qbitorrent-cli.
  * **01.03.22:** - Add python for search plugin support.
  * **23.02.22:** - Rebase to Alpine Edge, install from Alpine repos.
  * **19.02.22:** - Add jq to build-stage
  * **07.01.22:** - Rebase to Alpine, build from source.
  * **06.01.22:** - Deprecate unstable branch.
  * **10.02.21:** - Rebase to focal.
  * **20.01.21:** - Deprecate `UMASK_SET` in favor of UMASK in baseimage, see above for more information.
  * **12.11.20:** - Stop creating /config/data directory on startup
  * **03.04.20:** - Fix adding search engine plugin
  * **02.08.19:** - Add qbitorrent-cli for processing scripts.
  * **23.03.19:** - Switching to new Base images, shift to arm32v7 tag.
  * **14.01.19:** - Rebase to Ubuntu, add multi arch and pipeline logic.
  * **25.09.18:** - Use buildstage type build, bump qbitorrent to 4.1.3.
  * **14.08.18:** - Rebase to alpine 3.8, bump libtorrent to 1.1.9 and qbitorrent to 4.1.2.
  * **08.06.18:** - Bump qbitorrent to 4.1.1.
  * **26.04.18:** - Bump libtorrent to 1.1.7.
  * **02.03.18:** - Bump qbitorrent to 4.0.4 and libtorrent to 1.1.6.
  * **02.01.18:** - Deprecate cpu_core routine lack of scaling.
  * **19.12.17:** - Update to v4.0.3.
  * **09.02.17:** - Rebase to alpine 3.7
  * **01.12.17:** - Update to v4.0.2.
  * **27.11.17:** - Update to v4 and use cpu_core routine to speed up builds.
  * **16.09.17:** - Bump to 3.3.16, Add WEBUI_PORT variable and notes to README to allow changing port of webui.
  * **01.08.17:** - Initial Release.
  * **12.02.18:** - Initial Release.


Back to top 
