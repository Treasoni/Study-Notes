---
url: "https://selfhosting.sh/foundations/docker-volume-permissions/"
title: "Docker Volume Permissions Explained | selfhosting.sh"
scraped_at: 2026-08-29T15:23:05+00:00
---

## The Permission Problem
Volume permission errors are the #1 cause of self-hosted Docker containers failing to start or losing data. The container process runs as one user. The mounted directory is owned by a different user. The result: `Permission denied`.
Understanding how Docker maps users between the container and host is the key to fixing these issues permanently.
## Prerequisites
  * Docker and Docker Compose installed ([Docker Compose Basics](https://selfhosting.sh/foundations/docker-compose-basics/))
  * Linux file permissions basics ([Linux Permissions](https://selfhosting.sh/foundations/linux-permissions/))
  * Docker volumes basics ([Docker Volumes](https://selfhosting.sh/foundations/docker-volumes/))


## How Container Users Work
Every process inside a container runs as a specific user with a UID (User ID) and GID (Group ID). By default, most containers run as root (UID 0). Security-conscious images run as a non-root user.

```
# Check what user a container runs as
docker exec mycontainer id
# uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)

# Check from the image (without running)
docker inspect myimage:tag --format='{{.Config.User}}'
```

The key insight: **Docker doesn’t map UIDs between the container and host.** UID 1000 inside the container is the same UID 1000 on the host. The usernames may differ, but the numeric UID is what the filesystem checks.
## Bind Mount Permission Errors
### The Scenario

```
services:
  myapp:
    image: myapp:v1.0
    volumes:
/opt/myapp/data:/data
```

The container runs as UID 1000. The host directory `/opt/myapp/data` is owned by root (UID 0). The container gets `Permission denied` when trying to write to `/data`.
### Fix 1: Match Host Ownership to Container User

```
# Find the container's UID
docker exec mycontainer id
# uid=1000(appuser) gid=1000(appuser)

# Change host directory ownership to match
sudo chown -R 1000:1000 /opt/myapp/data
```

This is the most common and reliable fix.
### Fix 2: Run Container as a Specific User

```
services:
  myapp:
    image: myapp:v1.0
    user: "1000:1000"  # Run as UID 1000, GID 1000
    volumes:
/opt/myapp/data:/data
```

**Caution:** Not all images support running as an arbitrary user. Some require specific UIDs or root access during initialization.
### Fix 3: LinuxServer.io PUID/PGID
LinuxServer.io images provide `PUID` and `PGID` environment variables that handle user mapping for you:

```
services:
  myapp:
    image: lscr.io/linuxserver/myapp:latest
    environment:
PUID=1000
PGID=1000
    volumes:
/opt/myapp/config:/config
/opt/myapp/data:/data
```

The container’s entrypoint script changes file ownership to match the specified UID/GID at startup.

```
# Find your user's UID/GID

# uid=1000(youruser) gid=1000(youruser)
```

## Named Volume Permissions
Named volumes are managed by Docker and typically have fewer permission issues.

```
services:
  myapp:
    volumes:
mydata:/data

volumes:
  mydata# Docker manages this
```

Docker initializes named volumes with the correct ownership based on the container image’s filesystem. If the image has `/data` owned by UID 1000, the named volume will be initialized with that ownership.
### When Named Volumes Have Permission Issues
If you switch images (e.g., from one app version to another that uses a different UID), the existing volume retains the old ownership.

```
# Find the named volume's location
docker volume inspect mydata --format '{{.Mountpoint}}'
# /var/lib/docker/volumes/myproject_mydata/_data

# Check ownership
sudo ls -ln /var/lib/docker/volumes/myproject_mydata/_data

# Fix ownership
sudo chown -R NEW_UID:NEW_GID /var/lib/docker/volumes/myproject_mydata/_data
```

## Common App-Specific Permission Issues
### PostgreSQL
PostgreSQL runs as UID 999 internally and requires ownership of its data directory.

```
# If using a bind mount
sudo chown -R 999:999 /opt/postgres/data

# Or use a named volume (recommended)
volumes:
  postgres_data:
```

PostgreSQL will refuse to start if the data directory is owned by the wrong user:

```
FATAL: data directory "/var/lib/postgresql/data" has wrong ownership
```

### Nextcloud
Nextcloud runs as `www-data` (UID 33 on Debian-based images).

```
sudo chown -R 33:33 /opt/nextcloud/data
```

Or use the `NEXTCLOUD_TRUSTED_DOMAINS` and let the entrypoint handle permissions.
### Immich
Immich v1.99+ uses specific paths. The upload location must be writable by the container user.

```
environment:
  UPLOAD_LOCATION: /usr/src/app/upload
volumes:
/opt/immich/upload:/usr/src/app/upload
```

```
# Check container UID and fix ownership
docker exec immich-server id
sudo chown -R $(docker exec immich-server id -u):$(docker exec immich-server id -g) /opt/immich/upload
```

### Plex/Jellyfin
Media files need to be readable by the container user. Media directories often have restrictive permissions.

```
# Allow the container to read media
# Option 1: Change ownership
sudo chown -R 1000:1000 /media

# Option 2: Make world-readable (simpler but less secure)
sudo chmod -R o+rX /media
```

## Shared Volumes Between Containers
When multiple containers mount the same volume, they must agree on the UID/GID.

```
services:
  writer:
    user: "1000:1000"
    volumes:
shared:/data
  reader:
    user: "1000:1000"
    volumes:
shared:/data:ro  # Read-only for the reader

volumes:
  shared:
```

If the containers run as different UIDs, use a shared group:

```
# Create a shared group on the host
sudo groupadd -g 2000 shared
sudo usermod -aG shared user1

# Set group ownership and setgid bit
sudo chown -R :2000 /path/to/shared
sudo chmod -R g+rwX /path/to/shared
sudo chmod g+s /path/to/shared  # New files inherit the group
```

## SELinux and AppArmor
### SELinux (CentOS/RHEL/Fedora)

```
Permission denied (13)
```

Even with correct ownership, SELinux may block container access.

```
# Check if SELinux is enforcing
getenforce

# Quick test: temporarily set permissive
sudo setenforce 0

# Proper fix: add SELinux label to volume mount
volumes:
 /opt/myapp/data:/data:Z    # Private label (one container)
 /opt/shared/data:/data:z   # Shared label (multiple containers)
```

### AppArmor (Ubuntu/Debian)
AppArmor rarely causes Docker permission issues with the default profile. If it does:

```
# Check AppArmor status
sudo aa-status

# Test with AppArmor disabled for a container
docker run --security-opt apparmor=unconfined myimage
```

## Rootless Docker Permissions
Rootless Docker adds user namespace remapping. UID 1000 inside the container maps to a different UID on the host.

```
# Check the UID mapping
cat /etc/subuid
# youruser:100000:65536

# Container UID 0 maps to host UID 100000
# Container UID 1000 maps to host UID 101000
```

For bind mounts with rootless Docker:

```
# The host directory must be owned by the remapped UID
# Container runs as root (UID 0) → host UID 100000
sudo chown -R 100000:100000 /opt/myapp/data

# Container runs as UID 1000 → host UID 101000
sudo chown -R 101000:101000 /opt/myapp/data
```

## Debugging Permissions

```
# 1. Check container user
docker exec mycontainer id

# 2. Check host directory ownership
ls -ln /path/to/volume

# 3. Check inside the container
docker exec mycontainer ls -ln /data

# 4. Test write access from inside
docker exec mycontainer touch /data/test-write
# If "Permission denied" → ownership mismatch

# 5. Check effective permissions
docker exec mycontainer stat /data

# 6. Check if SELinux/AppArmor is blocking
# SELinux
ls -lZ /path/to/volume
# AppArmor
docker inspect mycontainer --format '{{.HostConfig.SecurityOpt}}'
```

## Permission Fix Checklist
When you get a permission error:
  1. **Find the container’s UID/GID:** `docker exec container id`
  2. **Find the host directory’s owner:** `ls -ln /path/to/data`
  3. **Do they match?** If not, `sudo chown -R CONTAINER_UID:CONTAINER_GID /path/to/data`
  4. **Still failing?** Check SELinux (`getenforce`) or use `:Z` label
  5. **Still failing?** Try a named volume instead of a bind mount
  6. **Still failing?** Check container logs for the specific file/path causing the error


## FAQ
### Should I use named volumes or bind mounts?
Named volumes have fewer permission issues and are managed by Docker. Bind mounts give you direct filesystem access and are easier to backup with standard tools. For databases, named volumes are recommended. For media and config files where you want direct access, use bind mounts.
### Can I just run everything as root to avoid permission issues?
Running containers as root works but is a security risk. If a container is compromised, the attacker has root access to mounted volumes. Use non-root users where possible, especially for internet-facing services.
### What does the `:Z` or `:z` suffix on volumes do?
These are SELinux labels. `:Z` applies a private label (only this container can access the volume). `:z` applies a shared label (multiple containers can access). On non-SELinux systems, these have no effect and are safe to include.
### My container creates files as root inside a bind mount. How do I fix this?
The container is running as root (UID 0). Either set `user: "1000:1000"` in your Compose file or use PUID/PGID if the image supports it. For images that require root, use a named volume.
## Related
  * [Linux File Permissions](https://selfhosting.sh/foundations/linux-permissions/)
  * [Docker Compose Basics](https://selfhosting.sh/foundations/docker-compose-basics/)
  * [Docker Common Issues](https://selfhosting.sh/foundations/docker-common-issues/)
  * [Docker Container Won’t Start](https://selfhosting.sh/foundations/docker-container-not-starting/)


## Related Articles
[foundationsBacking Up Docker Volumes Back up Docker volumes and container data — named volumes, bind mounts, database dumps, automated backup scripts, and re...](https://selfhosting.sh/foundations/backup-docker-volumes/)[foundationsDocker Common Issues and Quick Fixes Solutions to the most frequent Docker problems — image pulls, build failures, daemon errors, resource exhaustion, and co...](https://selfhosting.sh/foundations/docker-common-issues/)[foundationsDocker Container Won't Start — Fixes Diagnose why your Docker container won't start — exit codes, missing images, config errors, resource limits, and depende...](https://selfhosting.sh/foundations/docker-container-not-starting/)[foundationsDocker Networking Issues — Fixes Solve Docker networking problems — containers can't communicate, DNS failures, port binding errors, bridge network issue...](https://selfhosting.sh/foundations/docker-networking-issues/)[foundationsDocker Troubleshooting Guide Fix common Docker and Docker Compose problems — container won't start, port conflicts, permission errors, networking iss...](https://selfhosting.sh/foundations/docker-troubleshooting/)[foundationsDocker Volumes and Persistent Data Master Docker volumes, bind mounts, and data persistence — keep your self-hosted app data safe across container updates ...](https://selfhosting.sh/foundations/docker-volumes/)
Read Next [ Backing Up Docker Volumes ](https://selfhosting.sh/foundations/backup-docker-volumes/)
### Get self-hosting tips in your inbox
Get the Docker Compose configs, hardware picks, and setup shortcuts we don't put in articles. Weekly. No spam.
## Comments
