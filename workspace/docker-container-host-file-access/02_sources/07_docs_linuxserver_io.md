---
url: "https://docs.linuxserver.io/general/understanding-puid-and-pgid/"
title: "Understanding PUID and PGID - LinuxServer.io"
scraped_at: 2026-08-29T15:23:05+00:00
---

# Understanding PUID and PGID[¶](https://docs.linuxserver.io/general/understanding-puid-and-pgid/#understanding-puid-and-pgid "Permanent link")
Info
We are aware that recent versions of the Docker engine have introduced the `--user` flag. Our images are not yet compatible with this, so we recommend continuing usage of PUID and PGID.
## Why use these?[¶](https://docs.linuxserver.io/general/understanding-puid-and-pgid/#why-use-these "Permanent link")
Docker runs all of its containers under the `root` user domain because it requires access to things like network configuration, process management, and your filesystem. This means that the processes running inside your containers also run as `root`. This kind of elevated access is not ideal for day-to-day use, and potentially gives applications the access to things they shouldn't (although, a strong understanding of volume and port mapping will help with this).
Another issue is file management within the container's mapped volumes. If the process is running under `root`, all files and directories created during the container's lifespan will be owned by `root`, thus becoming inaccessible by you.
Using the `PUID` and `PGID` allows our containers to map the container's internal user to a user on the host machine. All of our containers use this method of user mapping and should be applied accordingly.
## Using the variables[¶](https://docs.linuxserver.io/general/understanding-puid-and-pgid/#using-the-variables "Permanent link")
When creating a container from one of our images, ensure you use the `-e PUID` and `-e PGID` options in your docker command:

```
dockercreate--name=beets-ePUID=1000-ePGID=1000linuxserver/beets

```

Or, if you use `docker-compose`, add them to the `environment:` section:

```
environment:
-PUID=1000
-PGID=1000

```

It is most likely that you will use the `id` of yourself, which can be obtained by running the command below. The two values you will be interested in are the `uid` and `gid`.

```
id$user

```

Back to top 
