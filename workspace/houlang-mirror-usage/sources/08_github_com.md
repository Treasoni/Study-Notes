---
url: "https://github.com/moby/moby/issues/42022"
title: "Docker Hub Credentials Leaking to Registry Mirrors · Issue #42022 · moby/moby"
scraped_at: 2026-09-13T16:04:45+00:00
---

[Skip to content](https://github.com/moby/moby/issues/42022#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/moby/moby/issues/42022) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/moby/moby/issues/42022) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/moby/moby/issues/42022) to refresh your session. Dismiss alert
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/moby/moby/issues/42022).
/ Public
  * [ Notifications ](https://github.com/login?return_to=%2Fmoby%2Fmoby) You must be signed in to change notification settings
  * [ Fork 19.2k ](https://github.com/login?return_to=%2Fmoby%2Fmoby)
  * [ Star  72.1k ](https://github.com/login?return_to=%2Fmoby%2Fmoby)


#  Docker Hub Credentials Leaking to Registry Mirrors #42022
New issue
Copy link
New issue
Copy link
[Docker Hub Credentials Leaking to Registry Mirrors](https://github.com/moby/moby/issues/42022#top)#42022
Copy link
Labels
[area/authentication](https://github.com/moby/moby/issues?q=state%3Aopen%20label%3A%22area%2Fauthentication%22)[area/distributionImage Distribution](https://github.com/moby/moby/issues?q=state%3Aopen%20label%3A%22area%2Fdistribution%22)Image Distribution
## Description
opened [on Feb 13, 2021](https://github.com/moby/moby/issues/42022#issue-807803924)
Issue body actions
**Description**
If dockerd has registry mirrors configured, when you log into Docker Hub the mirrors start receiving the credentials on image pulls. This is a security risk, as mirrors shouldn't have access to your Docker Hub tokens.
It also has the side effect of preventing some registry mirrors from working properly. GCR for example tries to authenticate with the Docker Hub credentials sent and fails, making all requests return an unauthorized error response.
This is related to [#30880](https://github.com/moby/moby/issues/30880). Registry mirrors should not use Docker Hub credentials and instead use their own.
**Steps to reproduce the issue:**
  1. Instal and configure some proxy the allows you to inspect HTTPS requests, like <https://mitmproxy.org>.
  2. Run dockerd with `--debug` and `--registry-mirror=https://mirror.gcr.io`.
  3. Run `docker pull docker`.
  4. Check the HTTP request sent to the registry mirror.


**Describe the results you received:**
The authorization header of the request contains the Docker Hub credential and the account is specified on the query string of the URL.
**Describe the results you expected:**
No account parameter or authorization header is sent on the request to the mirror.
**Additional information you deem important (e.g. issue happens only occasionally):** I've also tested this against a compiled version of the master branch and the behavior is still the same.
**Output of`docker version` :**

```
Client:
 Version:           19.03.8
 API version:       1.40
 Go version:        go1.13.8
 Git commit:        afacb8b7f0
 Built:             Fri Dec 18 12:15:19 2020
 OS/Arch:           linux/amd64
 Experimental:      false

Server:
 Engine:
  Version:          19.03.8
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.13.8
  Git commit:       afacb8b7f0
  Built:            Fri Dec  4 23:02:49 2020
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.3.3-0ubuntu2.2
  GitCommit:        
 runc:
  Version:          spec: 1.0.1-dev
  GitCommit:        
 docker-init:
  Version:          0.18.0
  GitCommit:        

```

**Output of`docker info` :**

```
Client:
 Debug Mode: false

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 2
 Server Version: 19.03.8
 Storage Driver: overlay2
  Backing Filesystem: <unknown>
  Supports d_type: true
  Native Overlay Diff: true
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
 Swarm: active
  NodeID: 6c3hbzigxwg580kiit5yx3hvu
  Is Manager: true
  ClusterID: ukfrk51l1kjhf9dc7p9d6xs2v
  Managers: 1
  Nodes: 1
  Default Address Pool: 10.0.0.0/8  
  SubnetSize: 24
  Data Path Port: 4789
  Orchestration:
   Task History Retention Limit: 5
  Raft:
   Snapshot Interval: 10000
   Number of Old Snapshots to Retain: 0
   Heartbeat Tick: 1
   Election Tick: 10
  Dispatcher:
   Heartbeat Period: 5 seconds
  CA Configuration:
   Expiry Duration: 3 months
   Force Rotate: 0
  Autolock Managers: false
  Root Rotation In Progress: false
  Node Address: 127.0.0.1
  Manager Addresses:
   127.0.0.1:2377
 Runtimes: runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 
 runc version: 
 init version: 
 Security Options:
  apparmor
  seccomp
   Profile: default
 Kernel Version: 5.4.0-53-generic
 Operating System: Ubuntu 20.04.1 LTS
 OSType: linux
 Architecture: x86_64
 CPUs: 8
 Total Memory: 30.07GiB
 Name: ubuntu
 ID: KSM4:TM6V:Z5TF:4YA6:OKU5:Z26N:2OTT:3HB3:VBKY:CKEI:RZWD:54FI
 Docker Root Dir: /var/lib/docker
 Debug Mode: true
  File Descriptors: 35
  Goroutines: 147
  System Time: 2021-02-13T15:27:10.906409609-03:00
  EventsListeners: 0
 HTTP Proxy: http://localhost:8080/
 HTTPS Proxy: http://localhost:8080/
 No Proxy: localhost,127.0.0.0/8,::1
 Username: t0rr3sp3dr0
 Registry: https://index.docker.io/v1/
 Labels:
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
 Registry Mirrors:
  https://mirror.gcr.io/
 Live Restore Enabled: false

WARNING: No swap limit support

```

**Additional environment details (AWS, VirtualBox, physical, etc.):** Parallels Virtual Machine
👍React with 👍7Reacted by Danil Beltyukov, Paulo Lieuthier, Gabriel Mendes, Eric Lafontaine, Michael Korn, cnietzschmann and lovetheguitar
## Activity
### SpComb commented on Mar 3, 2021 
Last edited by SpComb
More actions
It looks like fixing this as-is would break the use of authenticated [docker registry proxies](https://docs.docker.com/registry/recipes/mirror/) with `registry-mirrors`. The only way to use these currently seems to be:
  * Register a username + password on Docker Hub
  * Configure the same username + password on your own docker-registry proxy (auth htpasswd)
  * Configure the docker host to use your own `{"registry-mirrors": [...]}`
  * Use `docker login` against the default `https://index.docker.io/v1/` server on the Docker host with the username + password that works with both Docker Hub and your own docker-registry proxy
  * Use `docker pull` -> the Docker engine authenticates against the `registry-mirrors` -> your own docker-registry proxy using your Docker Hub credentials


### yaskoo commented on Dec 2, 2021 
Last edited by yaskoo
More actions
I think another possible workaround is to use separate client configs based on where you need to authenticate e.g.

```
DOCKER_CONFIG=$HOME/.docker_mirror docker login mirror.example.com
DOCKER_CONFIG=$HOME/.docker_mirror docker image pull ubuntu:bionic
```

and use the default for the hub
👀React with 👀1Reacted by David Volm
### MichaelKorn commented on Sep 22, 2022 
Last edited by MichaelKorn
More actions
Thanks for this ticket, I would like to Artifactory as product, which also does not work any more as mirror (no login needed) after login to docker hub: `Attempting next endpoint for pull after error: Head "...": unknown: Bad credentials`
[bsousaa](https://github.com/bsousaa)
added 
[area/distributionImage Distribution](https://github.com/moby/moby/issues?q=state%3Aopen%20label%3A%22area%2Fdistribution%22)Image Distribution
[on Mar 13, 2023](https://github.com/moby/moby/issues/42022#event-8730143566)
[thaJeztah](https://github.com/thaJeztah)
added [on Sep 14, 2023](https://github.com/moby/moby/issues/42022#event-10369591605)
### FabianSchurig commented on Mar 7, 2026 
More actions
Right now I need to enable the anonymous user access to my docker remote on my mirror (Artifactory), which I do not like.
If someone could provide guidance where to implement it maybe someone else could create a PR?
[@thaJeztah](https://github.com/thaJeztah)
[Sign up for free](https://github.com/signup?return_to=https://github.com/moby/moby/issues/42022)**to join this conversation on GitHub.** Already have an account? [Sign in to comment](https://github.com/login?return_to=https://github.com/moby/moby/issues/42022)
## Metadata
## Metadata
### Assignees
No one assigned
### Labels
[area/authentication](https://github.com/moby/moby/issues?q=state%3Aopen%20label%3A%22area%2Fauthentication%22)[area/distributionImage Distribution](https://github.com/moby/moby/issues?q=state%3Aopen%20label%3A%22area%2Fdistribution%22)Image Distribution
No type
### Projects
No projects
### Milestone
No milestone
### Relationships
None yet
### Development
No branches or pull requests
## Issue actions
  * Open in GitHub Copilot app


You can’t perform that action at this time. 
