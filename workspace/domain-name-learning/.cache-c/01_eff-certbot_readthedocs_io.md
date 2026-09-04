---
url: "https://eff-certbot.readthedocs.io/en/stable/using.html"
title: "User Guide — Certbot 5.8.0 documentation"
scraped_at: 2026-09-04T04:45:27+00:00
---

  * User Guide
  * [ View page source](https://eff-certbot.readthedocs.io/en/stable/_sources/using.rst.txt)


# User Guide[](https://eff-certbot.readthedocs.io/en/stable/using.html#user-guide "Link to this heading")
##  [Certbot Commands](https://eff-certbot.readthedocs.io/en/stable/using.html#id7)[](https://eff-certbot.readthedocs.io/en/stable/using.html#certbot-commands "Link to this heading")
Certbot uses a number of different commands (also referred to as “subcommands”) to request specific actions such as obtaining, renewing, or revoking certificates. The most important and commonly-used commands will be discussed throughout this document; an exhaustive list also appears near the end of the document.
The `certbot` script on your web server might be named `letsencrypt` if your system uses an older package. Throughout the docs, whenever you see `certbot`, swap in the correct name as needed.
##  [Getting certificates (and choosing plugins)](https://eff-certbot.readthedocs.io/en/stable/using.html#id8)[](https://eff-certbot.readthedocs.io/en/stable/using.html#getting-certificates-and-choosing-plugins "Link to this heading")
Certbot helps you achieve two tasks:
  1. Obtaining a certificate: automatically performing the required authentication steps to prove that you control the domain(s), saving the certificate to `/etc/letsencrypt/live/` and renewing it on a regular schedule.
  2. Optionally, installing that certificate to supported web servers (like Apache or nginx) and other kinds of servers. This is done by automatically modifying the configuration of your server in order to use the certificate.


To obtain a certificate and also install it, use the `certbot run` command (or `certbot`, which is the same).
To just obtain the certificate without installing it anywhere, the `certbot certonly` (“certificate only”) command can be used.
Some example ways to use Certbot:

```
# Obtain and install a certificate:
certbot

# Obtain a certificate but don't install it:
certbot certonly

# You may specify multiple domains with -d and obtain and
# install different certificates by running Certbot multiple times:
certbot certonly -d example.com -d www.example.com
certbot certonly -d app.example.com -d api.example.com

```

To perform these tasks, Certbot will ask you to choose from a selection of authenticator and installer plugins. The appropriate choice of plugins will depend on what kind of server software you are running and plan to use your certificates with.
**Authenticators** are plugins which automatically perform the required steps to prove that you control the domain names you’re trying to request a certificate for. An authenticator is always required to obtain a certificate.
**Installers** are plugins which can automatically modify your web server’s configuration to serve your website over HTTPS, using the certificates obtained by Certbot. An installer is only required if you want Certbot to install the certificate to your web server.
Some plugins are both authenticators and installers and it is possible to specify a distinct [combination](https://eff-certbot.readthedocs.io/en/stable/using.html#combination) of authenticator and plugin.  
| Plugin  | Auth  | Inst  | Notes  | Challenge types (and port)  |  
| --- | --- | --- | --- | --- |  
|   |  Automates obtaining and installing a certificate with Apache.  | [http-01](https://datatracker.ietf.org/doc/html/rfc8555#section-8.3) (80)  |  
|   |  Automates obtaining and installing a certificate with Nginx.  | [http-01](https://datatracker.ietf.org/doc/html/rfc8555#section-8.3) (80)  |  
|   |  Obtains a certificate by writing to the webroot directory of an already running webserver.  | [http-01](https://datatracker.ietf.org/doc/html/rfc8555#section-8.3) (80)  |  
| [standalone](https://eff-certbot.readthedocs.io/en/stable/using.html#standalone)  |  Uses a “standalone” webserver to obtain a certificate. Requires port 80 to be available. This is useful on systems with no webserver, or when direct integration with the local webserver is not supported or not desired.  | [http-01](https://datatracker.ietf.org/doc/html/rfc8555#section-8.3) (80)  |  
| [DNS plugins](https://eff-certbot.readthedocs.io/en/stable/using.html#dns-plugins)  |  This category of plugins automates obtaining a certificate by modifying DNS records to prove you have control over a domain. Doing domain validation in this way is the only way to obtain wildcard certificates from Let’s Encrypt.  | [dns-01](https://datatracker.ietf.org/doc/html/rfc8555#section-8.4) (53)  |  
|   |  Obtain a certificate by manually following instructions to perform domain validation yourself. Certificates created this way do not support autorenewal. Autorenewal may be enabled by providing an authentication hook script to automate the domain validation steps.  | [http-01](https://datatracker.ietf.org/doc/html/rfc8555#section-8.3) (80) or [dns-01](https://datatracker.ietf.org/doc/html/rfc8555#section-8.4) (53)  |  
Under the hood, plugins use one of several ACME protocol [challenges](https://datatracker.ietf.org/doc/html/rfc8555#section-8) to prove you control a domain. The options are [http-01](https://datatracker.ietf.org/doc/html/rfc8555#section-8.3) (which uses port 80) and [dns-01](https://datatracker.ietf.org/doc/html/rfc8555#section-8.4) (requiring configuration of a DNS server on port 53, though that’s often not the same machine as your webserver). A few plugins support more than one challenge type, in which case you can choose one with `--preferred-challenges`.
There are also many [third-party-plugins](https://eff-certbot.readthedocs.io/en/stable/using.html#third-party-plugins) available. Below we describe in more detail the circumstances in which each plugin can be used, and how to use it.
The Apache plugin currently [supports](https://github.com/certbot/certbot/blob/main/certbot/src/certbot/_internal/plugins/apache/entrypoint.py) modern OSes based on Debian, Fedora, SUSE, Gentoo, CentOS and Darwin. This automates both obtaining _and_ installing certificates on an Apache webserver. To specify this plugin on the command line, simply include `--apache`.
If you’re running a local webserver for which you have the ability to modify the content being served, and you’d prefer not to stop the webserver during the certificate issuance process, you can use the webroot plugin to obtain a certificate by including `certonly` and `--webroot` on the command line. In addition, you’ll need to specify `--webroot-path` or with the top-level directory (“web root”) containing the files served by your webserver. For example, `--webroot-path /var/www/html` or `--webroot-path /usr/share/nginx/html` are two common webroot paths.
If you’re getting a certificate for many domains at once, the plugin needs to know where each domain’s files are served from, which could potentially be a separate directory for each domain. When requesting a certificate for multiple domains, each domain will use the most recently specified `--webroot-path`. So, for instance,

```
certbot certonly --webroot -w /var/www/example -d www.example.com -d example.com -w /var/www/other -d other.example.net -d another.other.example.net

```

would obtain a single certificate for all of those names, using the `/var/www/example` webroot directory for the first two, and `/var/www/other` for the second two.
The webroot plugin works by creating a temporary file for each of your requested domains in `${webroot-path}/.well-known/acme-challenge`. Then the Let’s Encrypt validation server makes HTTP requests to validate that the DNS for each requested domain resolves to the server running certbot. An example request made to your web server would look like:

```
66.133.109.36 - - [05/Jan/2016:20:11:24 -0500] "GET /.well-known/acme-challenge/HGr8U1IeTW4kY_Z6UIyaakzOkyQgPr_7ArlLgtZE8SX HTTP/1.1" 200 87 "-" "Mozilla/5.0 (compatible; Let's Encrypt validation server; +https://www.letsencrypt.org)"

```

Note that to use the webroot plugin, your server must be configured to serve files from hidden directories. If `/.well-known` is treated specially by your webserver configuration, you might need to modify the configuration to ensure that files inside `/.well-known/acme-challenge` are served by the webserver.
Under Windows, Certbot will generate a `web.config` file, if one does not already exist, in `/.well-known/acme-challenge` in order to let IIS serve the challenge files even if they do not have an extension.
The Nginx plugin should work for most configurations. We recommend backing up Nginx configurations before using it (though you can also revert changes to configurations with `certbot --nginx rollback`). You can use it by providing the `--nginx` flag on the commandline.

```
certbot --nginx

```

###  [Standalone](https://eff-certbot.readthedocs.io/en/stable/using.html#id12)[](https://eff-certbot.readthedocs.io/en/stable/using.html#standalone "Link to this heading")
Use standalone mode to obtain a certificate if you don’t want to use (or don’t currently have) existing server software. The standalone plugin does not rely on any other server software running on the machine where you obtain the certificate.
To obtain a certificate using a “standalone” webserver, you can use the standalone plugin by including `certonly` and `--standalone` on the command line. This plugin needs to bind to port 80 in order to perform domain validation, so you may need to stop your existing webserver.
It must still be possible for your machine to accept inbound connections from the Internet on the specified port using each requested domain name.
By default, Certbot first attempts to bind to the port for all interfaces using IPv6 and then bind to that port using IPv4; Certbot continues so long as at least one bind succeeds. On most Linux systems, IPv4 traffic will be routed to the bound IPv6 port and the failure during the second bind is expected.
Use `--<challenge-type>-address` to explicitly tell Certbot which interface (and protocol) to bind.
###  [DNS Plugins](https://eff-certbot.readthedocs.io/en/stable/using.html#id13)[](https://eff-certbot.readthedocs.io/en/stable/using.html#dns-plugins "Link to this heading")
If you’d like to obtain a wildcard certificate from Let’s Encrypt or run `certbot` on a machine other than your target webserver, you can use one of Certbot’s DNS plugins.
These plugins are not included in a default Certbot installation and must be installed separately. They are available in many OS package managers, as Docker images, and as snaps. Visit <https://certbot.eff.org> to learn the best way to use the DNS plugins on your system.
Once installed, you can find documentation on how to use each plugin at:
  * [certbot-dns-cloudflare](https://certbot-dns-cloudflare.readthedocs.io)
  * [certbot-dns-digitalocean](https://certbot-dns-digitalocean.readthedocs.io)
  * [certbot-dns-dnsimple](https://certbot-dns-dnsimple.readthedocs.io)
  * [certbot-dns-dnsmadeeasy](https://certbot-dns-dnsmadeeasy.readthedocs.io)
  * [certbot-dns-gehirn](https://certbot-dns-gehirn.readthedocs.io)
  * [certbot-dns-google](https://certbot-dns-google.readthedocs.io)
  * [certbot-dns-linode](https://certbot-dns-linode.readthedocs.io)
  * [certbot-dns-luadns](https://certbot-dns-luadns.readthedocs.io)
  * [certbot-dns-nsone](https://certbot-dns-nsone.readthedocs.io)
  * [certbot-dns-ovh](https://certbot-dns-ovh.readthedocs.io)
  * [certbot-dns-rfc2136](https://certbot-dns-rfc2136.readthedocs.io)
  * [certbot-dns-route53](https://certbot-dns-route53.readthedocs.io)
  * [certbot-dns-sakuracloud](https://certbot-dns-sakuracloud.readthedocs.io)


If you’d like to obtain a certificate running `certbot` on a machine other than your target webserver or perform the steps for domain validation yourself, you can use the manual plugin. While hidden from the UI, you can use the plugin to obtain a certificate by specifying `certonly` and `--manual` on the command line. This requires you to copy and paste commands into another terminal session, which may be on a different computer.
The manual plugin can use either the `http` or the `dns` challenge. You can use the `--preferred-challenges` option to choose the challenge of your preference.
The `http` challenge will ask you to place a file with a specific name and specific content in the `/.well-known/acme-challenge/` directory directly in the top-level directory (“web root”) containing the files served by your webserver. In essence it’s the same as the [webroot](https://eff-certbot.readthedocs.io/en/stable/using.html#webroot) plugin, but not automated.
When using the `dns` challenge, `certbot` will ask you to place a TXT DNS record with specific contents under the domain name consisting of the hostname for which you want a certificate issued, prepended by `_acme-challenge`.
For example, for the domain `example.com`, a zone file entry would look like:

```
_acme-challenge.example.com. 300 IN TXT "gfj9Xq...Rg85nM"

```

**Renewal with the manual plugin**
Certificates created using `--manual` **do not** support automatic renewal unless combined with an [authentication hook script](https://eff-certbot.readthedocs.io/en/stable/using.html#hooks) via `--manual-auth-hook` to automatically set up the required HTTP and/or TXT challenges.
If you can use one of the other [plugins](https://eff-certbot.readthedocs.io/en/stable/using.html#plugins) which support autorenewal to create your certificate, doing so is highly recommended.
To manually renew a certificate using `--manual` without hooks, repeat the same `certbot --manual` command you used to create the certificate originally. As this will require you to copy and paste new HTTP files or DNS TXT records, the command cannot be automated with a cron job.
###  [Combining plugins](https://eff-certbot.readthedocs.io/en/stable/using.html#id15)[](https://eff-certbot.readthedocs.io/en/stable/using.html#combining-plugins "Link to this heading")
Sometimes you may want to specify a combination of distinct authenticator and installer plugins. To do so, specify the authenticator plugin with `--authenticator` or and the installer plugin with `--installer` or .
For instance, you could create a certificate using the [webroot](https://eff-certbot.readthedocs.io/en/stable/using.html#webroot) plugin for authentication and the [apache](https://eff-certbot.readthedocs.io/en/stable/using.html#apache) plugin for installation.

```
certbot run -a webroot -i apache -w /var/www/html -d example.com

```

Or you could create a certificate using the [manual](https://eff-certbot.readthedocs.io/en/stable/using.html#manual) plugin for authentication and the [nginx](https://eff-certbot.readthedocs.io/en/stable/using.html#nginx) plugin for installation. (Note that this certificate cannot be renewed automatically.)

```
certbot run -a manual -i nginx -d example.com

```

###  [Third-party plugins](https://eff-certbot.readthedocs.io/en/stable/using.html#id16)[](https://eff-certbot.readthedocs.io/en/stable/using.html#third-party-plugins "Link to this heading")
There are also a number of third-party plugins for the client, provided by other developers. Many are beta/experimental, but some are already in widespread use:  
| Plugin  | Auth  | Inst  | Notes  |  
| --- | --- | --- | --- |  
|   | Integration with the HAProxy load balancer  |  
|   | Integration with Amazon CloudFront distribution of S3 buckets  |  
|   | Obtain certificates via the Gandi LiveDNS API  |  
|   | Obtain certificates via a Varnish server  |  
| [external-auth](https://github.com/EnigmaBridge/certbot-external-auth)  | A plugin for convenient scripting  |  
|   | Install certificates in pritunl distributed OpenVPN servers  |  
|   | Install certificates in Proxmox Virtualization servers  |  
| [dns-standalone](https://github.com/siilike/certbot-dns-standalone)  | Obtain certificates via an integrated DNS server  |  
| [dns-ispconfig](https://github.com/m42e/certbot-dns-ispconfig)  | DNS Authentication using ISPConfig as DNS server  |  
| [dns-cloudns](https://github.com/inventage/certbot-dns-cloudns)  | DNS Authentication using ClouDNS API  |  
| [dns-clouddns](https://github.com/vshosting/certbot-dns-clouddns)  | DNS Authentication using CloudDNS API  |  
| [dns-lightsail](https://github.com/noi/certbot-dns-lightsail)  | DNS Authentication using Amazon Lightsail DNS API  |  
|   | DNS Authentication for INWX through the XML API  |  
|   | DNS Authentication using Azure DNS  |  
| [dns-godaddy](https://github.com/miigotu/certbot-dns-godaddy)  | DNS Authentication using Godaddy DNS  |  
| [dns-yandexcloud](https://github.com/PykupeJIbc/certbot-dns-yandexcloud)  | DNS Authentication using Yandex Cloud DNS  |  
|   | DNS Authentication using BunnyDNS  |  
|   | DNS Authentication for njalla  |  
|   | DNS Authentication for DuckDNS  |  
|   | DNS Authentication for Porkbun  |  
|   | DNS Authentication using Infomaniak Domains API  |  
|   | DNS authentication of 100+ providers using go-acme/lego  |  
| [dns-dnsmanager](https://github.com/stayallive/certbot-dns-dnsmanager)  | DNS Authentication for dnsmanager.io  |  
| [standalone-nfq](https://github.com/alexzorin/certbot-standalone-nfq)  | HTTP Authentication that works with any webserver (Linux only)  |  
| [dns-solidserver](https://gitlab.com/charlyhong/certbot-dns-solidserver)  | DNS Authentication using SOLIDserver (EfficientIP)  |  
| [dns-stackit](https://github.com/stackitcloud/certbot-dns-stackit)  | DNS Authentication using STACKIT DNS  |  
|   | DNS Authentication using IONOS Cloud DNS  |  
| [dns-mijn-host](https://github.com/mijnhost/certbot-dns-mijn-host)  | DNS Authentication using mijn.host DNS  |  
| [nginx-unit](https://github.com/kea/certbot-nginx-unit)  | Automates obtaining and installing a certificate with Nginx Unit  |  
|   | DNS Authentication using cdmon’s API  |  
| [dns-synergy-wholesale](https://github.com/ALameLlama/certbot-dns-synergy-wholesale)  | DNS Authentication using Synergy Wholesale DNS  |  
|   | Install certificates as PKCS#12 archives  |  
| [dns-hetzner-cloud](https://github.com/rolschewsky/certbot-dns-hetzner-cloud)  | DNS Authentication for Hetzner Cloud DNS  |  
| [dns-czechia](https://github.com/CZECHIA-COM/certbot-dns-czechia)  | DNS Authentication for czechia.com  |  
| [dns-eurodns](https://pypi.org/project/certbot-dns-eurodns/)  | DNS Authentication for EuroDNS  |  
| [dns-dnscale](https://github.com/dnscaleou/certbot-dns-dnscale)  | DNS Authenticator for DNScale  |  
|   | DNS Authentication using the FENO (feno.no) API for .no domains  |  
If you’re interested, you can also [write your own plugin](https://eff-certbot.readthedocs.io/en/stable/contributing.html#dev-plugin).
##  [Managing certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#id17)[](https://eff-certbot.readthedocs.io/en/stable/using.html#managing-certificates "Link to this heading")
To view a list of the certificates Certbot knows about, run the `certificates` subcommand:
`certbot certificates`
This returns information in the following format:

```
Found the following certificates:
  Certificate Name: example.com
    Domains: example.com, www.example.com
    Expiry Date: 2017-02-19 19:53:00+00:00 (VALID: 30 days)
    Certificate Path: /etc/letsencrypt/live/example.com/fullchain.pem
    Key Type: RSA
    Private Key Path: /etc/letsencrypt/live/example.com/privkey.pem

```

`Certificate Name` shows the name of the certificate. Pass this name using the `--cert-name` flag to specify a particular certificate for the `run`, `certonly`, `certificates`, `renew`, and `delete` commands. The certificate name cannot contain filepath separators (i.e. ‘/’ or ‘\’, depending on the platform). Example:

```
certbot certonly --cert-name example.com

```

###  [Re-creating and Updating Existing Certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#id18)[](https://eff-certbot.readthedocs.io/en/stable/using.html#re-creating-and-updating-existing-certificates "Link to this heading")
You can use `certonly` or `run` subcommands to request the creation of a single new certificate even if you already have an existing certificate with some of the same domain names.
If a certificate is requested with `run` or `certonly` specifying a certificate name that already exists, Certbot updates the existing certificate. Otherwise a new certificate is created and assigned the specified name.
The `--force-renewal`, `--duplicate`, and `--expand` options control Certbot’s behavior when re-creating a certificate with the same name as an existing certificate. If you don’t specify a requested behavior, Certbot may ask you what you intended.
`--force-renewal` tells Certbot to request a new certificate with the same domains as an existing certificate. Each domain must be explicitly specified via . If successful, this certificate is saved alongside the earlier one and symbolic links (the “`live`” reference) will be updated to point to the new certificate. This is a valid method of renewing a specific individual certificate.
`--duplicate` tells Certbot to create a separate, unrelated certificate with the same domains as an existing certificate. This certificate is saved completely separately from the prior one. Most users will not need to issue this command in normal circumstances.
`--expand` tells Certbot to update an existing certificate with a new certificate that contains all of the old domains and one or more additional new domains. With the `--expand` option, use the option to specify all existing domains and one or more new domains.
Example:

```
certbot --expand -d existing.com,example.com,newdomain.com

```

If you prefer, you can specify the domains individually like this:

```
certbot --expand -d existing.com -d example.com -d newdomain.com

```

Consider using `--cert-name` instead of `--expand`, as it gives more control over which certificate is modified and it lets you remove domains as well as adding them.
`--allow-subset-of-names` tells Certbot to continue with certificate generation if only some of the specified domain authorizations can be obtained. This may be useful if some domains specified in a certificate no longer point at this system.
Whenever you obtain a new certificate in any of these ways, the new certificate exists alongside any previously obtained certificates, whether or not the previous certificates have expired. The generation of a new certificate counts against several rate limits that are intended to prevent abuse of the ACME protocol, as described [here](https://letsencrypt.org/docs/rate-limits/).
###  [Changing a Certificate’s Domains](https://eff-certbot.readthedocs.io/en/stable/using.html#id19)[](https://eff-certbot.readthedocs.io/en/stable/using.html#changing-a-certificate-s-domains "Link to this heading")
The `--cert-name` flag can also be used to modify the domains a certificate contains, by specifying new domains using the or `--domains` flag. If certificate `example.com` previously contained `example.com` and `www.example.com`, it can be modified to only contain `example.com` by specifying only `example.com` with the or `--domains` flag. Example:

```
certbot certonly --cert-name example.com -d example.com

```

The same format can be used to expand the set of domains a certificate contains, or to replace that set entirely:

```
certbot certonly --cert-name example.com -d example.org,www.example.org

```

###  [RSA and ECDSA keys](https://eff-certbot.readthedocs.io/en/stable/using.html#id20)[](https://eff-certbot.readthedocs.io/en/stable/using.html#rsa-and-ecdsa-keys "Link to this heading")
Certbot supports two certificate private key algorithms: `rsa` and `ecdsa`.
As of version 2.0.0, Certbot defaults to ECDSA `secp256r1` (P-256) certificate private keys for all new certificates. Existing certificates will continue to renew using their existing key type, unless a key type change is requested.
The type of key used by Certbot can be controlled through the `--key-type` option. You can use the `--elliptic-curve` option to control the curve used in ECDSA certificates and the `--rsa-key-size` option to control the size of RSA keys.
Warning
If you obtain certificates using ECDSA keys, you should be careful not to downgrade to a Certbot version earlier than 1.10.0 where ECDSA keys were not supported. Downgrades like this are possible if you switch from something like the snaps or pip to packages provided by your operating system which often lag behind.
####  [Changing a certificate’s key type](https://eff-certbot.readthedocs.io/en/stable/using.html#id21)[](https://eff-certbot.readthedocs.io/en/stable/using.html#changing-a-certificate-s-key-type "Link to this heading")
Unless you are aware that you need to support very old HTTPS clients that are not supported by most sites, you can safely transition your site to use ECDSA keys instead of RSA keys.
If you want to change a single certificate to use ECDSA keys, you’ll need to create or renew a certificate while setting `--key-type ecdsa` on the command line:

```
certbotrenew--key-typeecdsa--cert-nameexample.com--force-renewal

```

If you want to use ECDSA keys for all certificates in the future (including renewals of existing certificates), you can add the following line to Certbot’s [configuration file](https://eff-certbot.readthedocs.io/en/stable/using.html#config-file):

```
key-type=ecdsa

```

which will take effect upon the next renewal of each certificate.
###  [Revoking certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#id22)[](https://eff-certbot.readthedocs.io/en/stable/using.html#revoking-certificates "Link to this heading")
If you need to revoke a certificate, use the `revoke` subcommand to do so.
A certificate may be revoked by providing its name (see `certbot certificates`) or by providing its path directly:

```
certbot revoke --cert-name example.com

certbot revoke --cert-path /etc/letsencrypt/live/example.com/cert.pem

```

If the certificate being revoked was obtained via the `--staging`, `--test-cert` or a non-default `--server` flag, that flag must be passed to the `revoke` subcommand.
Note
After revocation, Certbot will (by default) ask whether you want to **delete** the certificate. Unless deleted, Certbot will try to renew revoked certificates the next time `certbot renew` runs.
You can also specify the reason for revoking your certificate by using the `reason` flag. Reasons include `unspecified` which is the default, as well as `keycompromise`, `affiliationchanged`, `superseded`, and `cessationofoperation`:

```
certbot revoke --cert-name example.com --reason keycompromise

```

####  [Revoking by account key or certificate private key](https://eff-certbot.readthedocs.io/en/stable/using.html#id23)[](https://eff-certbot.readthedocs.io/en/stable/using.html#revoking-by-account-key-or-certificate-private-key "Link to this heading")
By default, Certbot will try revoke the certificate using your ACME account key. If the certificate was created from the same ACME account, the revocation will be successful.
If you instead have the corresponding private key file to the certificate you wish to revoke, use `--key-path` to perform the revocation from any ACME account:

```
certbot revoke --cert-path /etc/letsencrypt/live/example.com/cert.pem --key-path /etc/letsencrypt/live/example.com/privkey.pem

```

###  [Deleting certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#id24)[](https://eff-certbot.readthedocs.io/en/stable/using.html#deleting-certificates "Link to this heading")
If you need to delete a certificate, use the `delete` subcommand.
Note
Read this and the [Safely deleting certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#safely-deleting-certificates) sections carefully. This is an irreversible operation and must be done with care.
Certbot does not automatically revoke a certificate before deleting it. If you’re no longer using a certificate and don’t plan to use it anywhere else, you may want to follow the instructions in [Revoking certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#revoking-certificates) instead. Generally, there’s no need to revoke a certificate if its private key has not been compromised, but you may still receive expiration emails from Let’s Encrypt unless you revoke.
Note
Do not manually delete certificate files from inside `/etc/letsencrypt/`. Always use the `delete` subcommand.
A certificate may be deleted by providing its name with `--cert-name`. You may find its name using `certbot certificates`.
Otherwise, you will be prompted to choose one or more certificates to delete:

```
certbot delete --cert-name example.com
# or to choose from a list:
certbot delete

```

####  [Safely deleting certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#id25)[](https://eff-certbot.readthedocs.io/en/stable/using.html#safely-deleting-certificates "Link to this heading")
Deleting a certificate without following the proper steps can result in a non-functioning server. To safely delete a certificate, follow all the steps below to make sure that references to a certificate are removed from the configuration of any installed server software (Apache, nginx, Postfix, etc) _before_ deleting the certificate.
To explain further, when installing a certificate, Certbot modifies Apache or nginx’s configuration to load the certificate and its private key from the `/etc/letsencrypt/live/` directory. Before deleting a certificate, it is necessary to undo that modification, by removing any references to the certificate from the webserver’s configuration files.
Follow these steps to safely delete a certificate:
  1. Find all references to the certificate (substitute `example.com` in the command for the name of the certificate you wish to delete):

```
sudo bash -c 'grep -R live/example.com /etc/{nginx,httpd,apache2}'

```

If there are no references found, skip directly to Step 4.
If some references are found, they will look something like:

```
/etc/apache2/sites-available/000-default-le-ssl.conf:SSLCertificateFile /etc/letsencrypt/live/example.com/fullchain.pem
/etc/apache2/sites-available/000-default-le-ssl.conf:SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem

```

  2. You will need a self-signed certificate to replace the certificate you are deleting. The following command will generate one for you, saving the certificate at `/etc/letsencrypt/self-signed-cert.pem` and its private key at `/etc/letsencrypt/self-signed-privkey.pem`:

```
sudo openssl req -nodes -batch -x509 -newkey rsa:2048 -keyout /etc/letsencrypt/self-signed-privkey.pem -out /etc/letsencrypt/self-signed-cert.pem -days 356

```

  3. For each reference found in Step 1, open the file in a text editor and replace the reference to the existing certificate with a reference to the self-signed certificate.
Continuing from the previous example, you would open `/etc/apache2/sites-available/000-default-le-ssl.conf` in a text editor and modify the two matching lines of text to instead say:

```
SSLCertificateFile /etc/letsencrypt/self-signed-cert.pem
SSLCertificateKeyFile /etc/letsencrypt/self-signed-privkey.pem

```

  4. It is now safe to delete the certificate. Do so by running:

```
sudo certbot delete --cert-name example.com

```



###  [Renewing certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#id26)[](https://eff-certbot.readthedocs.io/en/stable/using.html#renewing-certificates "Link to this heading")
See also
Most Certbot installations come with automatic renewal out of the box. See [Automated Renewals](https://eff-certbot.readthedocs.io/en/stable/using.html#automated-renewals) for more details.
See also
Users of the [Manual](https://eff-certbot.readthedocs.io/en/stable/using.html#manual) plugin should note that `--manual` certificates will not renew automatically, unless combined with authentication hook scripts. See [Renewal with the manual plugin](https://eff-certbot.readthedocs.io/en/stable/using.html#manual-renewal).
Certbot supports a `renew` action to check all installed certificates for impending expiry and attempt to renew them. The simplest form is simply
`certbot renew`
This command attempts to renew any previously-obtained certificates which are ready for renewal. As of Certbot 4.0.0, a certificate is considered ready for renewal when less than 1/3rd of its lifetime remains. For certificates with a lifetime of 10 days or less, that threshold is 1/2 of the lifetime. Prior to Certbot 4.0.0 the threshold was a fixed 30 days.
The same plugin and options that were used at the time the certificate was originally issued will be used for the renewal attempt, unless you specify other plugins or options. Unlike `certonly`, `renew` acts on multiple certificates and always takes into account whether each one is near expiry. Because of this, `renew` is suitable (and designed) for automated use, to allow your system to automatically renew each certificate when appropriate. Since `renew` only renews certificates that are near expiry it can be run as frequently as you want - since it will usually take no action.
The `renew` command includes hooks for running commands or scripts before or after a certificate is renewed. For example, if you have a single certificate obtained using the [standalone](https://eff-certbot.readthedocs.io/en/stable/using.html#standalone) plugin, you might need to stop the webserver before renewing so standalone can bind to the necessary ports, and then restart it after the plugin is finished. Example:

```
certbot renew --pre-hook "service nginx stop" --post-hook "service nginx start"

```

If a hook exits with a non-zero exit code, the error will be printed to `stderr` but renewal will be attempted anyway. A failing hook doesn’t directly cause Certbot to exit with a non-zero exit code, but since Certbot exits with a non-zero exit code when renewals fail, a failed hook causing renewal failures will indirectly result in a non-zero exit code. Hooks will only be run if a certificate is due for renewal, so you can run the above command frequently without unnecessarily stopping your webserver.
When Certbot detects that a certificate is due for renewal, `--pre-hook` and `--post-hook` hooks run before and after each attempt to renew it. If you want your hook to run only after a successful renewal, use `--deploy-hook` in a command like this.
`certbot renew --deploy-hook /path/to/deploy-hook-script`
You can also specify hooks by placing files in subdirectories of Certbot’s configuration directory. Assuming your configuration directory is `/etc/letsencrypt`, any executable files found in `/etc/letsencrypt/renewal-hooks/pre`, `/etc/letsencrypt/renewal-hooks/deploy`, and `/etc/letsencrypt/renewal-hooks/post` will be run as pre, deploy, and post hooks respectively. These hooks are run in alphabetical order. (The order the hooks are run is determined by the byte value of the characters in their filenames and is not dependent on your locale.)
Prior to certbot 3.2.0, hooks in directories were only run when certificates were renewed with the `renew` subcommand, but as of 3.2.0, they are run for any subcommand.
Hooks specified in the command line, [configuration file](https://eff-certbot.readthedocs.io/en/stable/using.html#config-file), or [renewal configuration files](https://eff-certbot.readthedocs.io/en/stable/using.html#renewal-config-file) are run as usual after running all hooks in these directories. One minor exception to this is if a hook specified elsewhere is simply the path to an executable file in the hook directory of the same type (e.g. your pre-hook is the path to an executable in `/etc/letsencrypt/renewal-hooks/pre`), the file is not run a second time. You can stop Certbot from automatically running executables found in these directories by including `--no-directory-hooks` on the command line.
More information about hooks can be found by running `certbot --help renew`.
If you’re sure that this command executes successfully without human intervention, you can add the command to `crontab` (since certificates are only renewed when they’re determined to be near expiry, the command can run on a regular basis, like every week or every day). In that case, you are likely to want to use the or `--quiet` quiet flag to silence all output except errors.
If you are manually renewing all of your certificates, the `--force-renewal` flag may be helpful; it causes the expiration time of the certificate(s) to be ignored when considering renewal, and attempts to renew each and every installed certificate regardless of its age. (This form is not appropriate to run daily because each certificate will be renewed every day, which will quickly run into the certificate authority rate limit.)
Starting with Certbot 2.7.0, certbot provides the environment variables `RENEWED_DOMAINS` and `FAILED_DOMAINS` to all post renewal hooks. These variables contain a space separated list of domains. These variables can be used to determine if a renewal has succeeded or failed as part of your post renewal hook.
Note that options provided to `certbot renew` will apply to _every_ certificate for which renewal is attempted; for example, `certbot renew --rsa-key-size 4096` would try to replace every near-expiry certificate with an equivalent certificate using a 4096-bit RSA public key. If a certificate is successfully renewed using specified options, those options will be saved and used for future renewals of that certificate.
An alternative form that provides for more fine-grained control over the renewal process (while renewing specified certificates one at a time), is `certbot certonly` with the complete set of subject domains of a specific certificate specified via flags. You may also want to include the or `--noninteractive` flag to prevent blocking on user input (which is useful when running the command from cron).
`certbot certonly -n -d example.com -d www.example.com`
All of the domains covered by the certificate must be specified in this case in order to renew and replace the old certificate rather than obtaining a new one; don’t forget any `www.` domains! Specifying a subset of the domains creates a new, separate certificate containing only those domains, rather than replacing the original certificate. When run with a set of domains corresponding to an existing certificate, the `certonly` command attempts to renew that specific certificate.
Please note that the CA will send notification emails to the address you provide if you do not renew certificates that are about to expire.
Certbot is working hard to improve the renewal process, and we apologize for any inconvenience you encounter in integrating these commands into your individual environment.
Note
`certbot renew` exit status will only be 1 if a renewal attempt failed. This means `certbot renew` exit status will be 0 if no certificate needs to be updated. If you write a custom script and expect to run a command only after a certificate was actually renewed you will need to use the `--deploy-hook` since the exit status will be 0 both on successful renewal and when renewal is not necessary.
###  [Renaming certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#id27)[](https://eff-certbot.readthedocs.io/en/stable/using.html#renaming-certificates "Link to this heading")
While certbot does not have an internal rename function, it is possible to rename certs by requesting a new certificate using certbot’s `--cert-name` flag.
  1. View certificates with `certbot certificates`
The output might be something like:

```
Found the following certs:
  Certificate Name: yourdomain.com-0001
    Serial Number: 2ce74f4e2b822211dd7648ea26c8927bdef6
    Key Type: ECDSA
    Domains: yourdomain.com subdomain.yourdomain.com
    Expiry Date: 2025-11-16 20:27:27+00:00 (INVALID: TEST_CERT)
    Certificate Path: /etc/letsencrypt/live/yourdomain.com-0001/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/yourdomain.com-0001/privkey.pem
  Certificate Name: yourdomain.com
    Serial Number: 2c72aa8cf58aa9fe9a33208d82304642d9ed
    Key Type: ECDSA
    Domains: yourdomain.com
    Expiry Date: 2025-11-16 19:22:47+00:00 (INVALID: TEST_CERT)
    Certificate Path: /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/yourdomain.com/privkey.pem

```

In this example, we will rename certificate `yourdomain.com-0001` to `yourdomain.com`.
  2. If the name you want is in use and you’re not using that cert, delete it using the instructions in the [Deleting certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#deleting-certificates) section.
You’ll then have:

```
Found the following certs:
  Certificate Name: yourdomain.com-0001
    Serial Number: 2ce74f4e2b822211dd7648ea26c8927bdef6
    Key Type: ECDSA
    Domains: yourdomain.com subdomain.yourdomain.com
    Expiry Date: 2025-11-16 20:27:27+00:00 (INVALID: TEST_CERT)
    Certificate Path: /etc/letsencrypt/live/yourdomain.com-0001/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/yourdomain.com-0001/privkey.pem

```

  3. If you’re not sure how you set the cert up initially, note relevant configuration options by inspecting `/etc/letsencrypt/renewal/yourdomain.com-0001.conf`
It will look something like:

```
version = 4.2.0
archive_dir = /etc/letsencrypt/archive/yourdomain.com-0001
cert = /etc/letsencrypt/live/yourdomain.com-0001/cert.pem
privkey = /etc/letsencrypt/live/yourdomain.com-0001/privkey.pem
chain = /etc/letsencrypt/live/yourdomain.com-0001/chain.pem
fullchain = /etc/letsencrypt/live/yourdomain.com-0001/fullchain.pem
[renewalparams]
account = abcdef12345678910
server = https://acme-staging-v02.api.letsencrypt.org/directory
authenticator = standalone
key_type = ecdsa
post_hook = "echo 'shut down server'"

```

You’ll want to note the authenticator, installer, server, any hooks, etc.
  4. Create a new cert with the options and name you want by running `certbot certonly --cert-name yourdomain.com -d yourdomain.com -d otherdomain.com --any-other-options`. The value for `--cert-name` can be anything you want; by default it is the first domain listed on the cert.
  5. Make sure that any links to your certificates are updated. If you’re using certbot to manage the installation of certs on your webserver, you can run `certbot install --cert-name yourdomain.com`.
  6. Restart your webserver, if applicable.
  7. You can now delete the old certificate, again using the [Deleting certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#deleting-certificates) section.


###  [Modifying the Renewal Configuration of Existing Certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#id28)[](https://eff-certbot.readthedocs.io/en/stable/using.html#modifying-the-renewal-configuration-of-existing-certificates "Link to this heading")
When creating a certificate, Certbot will keep track of all of the relevant options chosen by the user. At renewal time, Certbot will remember these options and apply them once again.
Sometimes, you may encounter the need to change some of these options for future certificate renewals. To achieve this, you will need to perform the following steps:
####  [Certbot v2.3.0 and newer](https://eff-certbot.readthedocs.io/en/stable/using.html#id29)[](https://eff-certbot.readthedocs.io/en/stable/using.html#certbot-v2-3-0-and-newer "Link to this heading")
The `certbot reconfigure` command can be used to change a certificate’s renewal options. This command will use the new renewal options to perform a test renewal against the Let’s Encrypt staging server. If this is successful, the new renewal options will be saved and will apply to future renewals.
You will need to specify the `--cert-name`, which can be found by running `certbot certificates`.
A list of common options that may be updated with the `reconfigure` command can be found by running `certbot help reconfigure`.
As a practical example, if you were using the `webroot` authenticator and had relocated your website to another directory, you can change the `--webroot-path` to the new directory using the following command:

```
certbotreconfigure--cert-nameexample.com--webroot-path/path/to/new/location

```

####  [Certbot v2.2.0 and older](https://eff-certbot.readthedocs.io/en/stable/using.html#id30)[](https://eff-certbot.readthedocs.io/en/stable/using.html#certbot-v2-2-0-and-older "Link to this heading")
  1. Perform a _dry run renewal_ with the amended options on the command line. This allows you to confirm that the change is valid and will result in successful future renewals.
  2. If the dry run is successful, perform a _live renewal_ of the certificate. This will persist the change for future renewals. If the certificate is not yet due to expire, you will need to force a renewal using `--force-renewal`.


Note
Rate limits from the certificate authority may prevent you from performing multiple renewals in a short period of time. It is strongly recommended to perform the second step only once, when you have decided on what options should change.
As a practical example, if you were using the `webroot` authenticator and had relocated your website to another directory, you would need to change the `--webroot-path` to the new directory. Following the above advice:
  1. Perform a _dry-run renewal_ of the individual certificate with the amended options:

```
certbot renew --cert-name example.com --webroot-path /path/to/new/location --dry-run

```

  2. If the dry-run was successful, make the change permanent by performing a _live renewal_ of the certificate with the amended options, including `--force-renewal`:

```
certbot renew --cert-name example.com --webroot-path /path/to/new/location --force-renewal

```

`--cert-name` selects the particular certificate to be modified. Without this option, all certificates will be selected.
`--webroot-path` is the option intended to be changed. All other previously selected options will be kept the same and do not need to be included in the command.


For advanced certificate management tasks, it is also possible to manually modify the certificate’s renewal configuration file, but this is discouraged since it can easily break Certbot’s ability to renew your certificates. These renewal configuration files are located at `/etc/letsencrypt/renewal/CERTNAME.conf`. If you choose to modify the renewal configuration file we advise you to make a backup of the file beforehand and test its validity with the `certbot renew --dry-run` command.
Warning
Manually modifying files under `/etc/letsencrypt/renewal/` can damage them if done improperly and we do not recommend doing so.
###  [Automated Renewals](https://eff-certbot.readthedocs.io/en/stable/using.html#id31)[](https://eff-certbot.readthedocs.io/en/stable/using.html#automated-renewals "Link to this heading")
Most Certbot installations come with automatic renewals preconfigured. This is done by means of a scheduled task which runs `certbot renew` periodically.
If you are unsure whether you need to configure automated renewal:
  1. Review the instructions for your system and installation method at <https://certbot.eff.org/instructions>. They will describe how to set up a scheduled task, if necessary. If no step is listed, your system comes with automated renewal pre-installed, and you should not need to take any additional actions.
  2. On Linux and BSD, you can check to see if your installation method has pre-installed a timer for you. To do so, look for the `certbot renew` command in either your system’s crontab (typically `/etc/crontab` or `/etc/cron.*/*`) or systemd timers (`systemctl list-timers`).
  3. If you’re still not sure, you can configure automated renewal manually by following the steps in the next section. Certbot has been carefully engineered to handle the case where both manual automated renewal and pre-installed automated renewal are set up.


####  [Setting up automated renewal](https://eff-certbot.readthedocs.io/en/stable/using.html#id32)[](https://eff-certbot.readthedocs.io/en/stable/using.html#setting-up-automated-renewal "Link to this heading")
If you think you may need to set up automated renewal, follow these instructions to set up a scheduled task to automatically renew your certificates in the background. If you are unsure whether your system has a pre-installed scheduled task for Certbot, it is safe to follow these instructions to create one.
Note
If you’re using Windows, these instructions are not necessary as Certbot on Windows comes with a scheduled task for automated renewal pre-installed.
If you are using macOS and installed Certbot using Homebrew, follow the instructions at <https://certbot.eff.org/instructions> to set up automated renewal. The instructions below are not applicable on macOS.
Run the following line, which will add a cron job to `/etc/crontab`:

```
SLEEPTIME=$(awk'BEGIN{srand(); print int(rand()*(3600+1))}');echo"0 0,12 * * * root sleep $SLEEPTIME && certbot renew -q"|sudotee-a/etc/crontab>/dev/null

```

If you needed to stop your webserver to run Certbot, you’ll want to add `pre` and `post` hooks to stop and start your webserver automatically. For example, if your webserver is HAProxy, run the following commands to create the hook files in the appropriate directory:

```
sudosh-c'printf "#!/bin/sh\nservice haproxy stop\n" > /etc/letsencrypt/renewal-hooks/pre/haproxy.sh'
sudosh-c'printf "#!/bin/sh\nservice haproxy start\n" > /etc/letsencrypt/renewal-hooks/post/haproxy.sh'
sudochmod755/etc/letsencrypt/renewal-hooks/pre/haproxy.sh
sudochmod755/etc/letsencrypt/renewal-hooks/post/haproxy.sh

```

Congratulations, Certbot will now automatically renew your certificates in the background.
If you are interested in learning more about how Certbot renews your certificates, see the [Renewing certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#renewing-certificates) section above.
##  [Where are my certificates?](https://eff-certbot.readthedocs.io/en/stable/using.html#id33)[](https://eff-certbot.readthedocs.io/en/stable/using.html#where-are-my-certificates "Link to this heading")
All generated keys and issued certificates can be found in `/etc/letsencrypt/live/$domain`, where `$domain` is the certificate name (see the note below). Rather than copying, please point your (web) server configuration directly to those files (or create symlinks). During the [renewal](https://eff-certbot.readthedocs.io/en/stable/using.html#renewal), `/etc/letsencrypt/live` is updated with the latest necessary files.
Note
The certificate name `$domain` used in the path `/etc/letsencrypt/live/$domain` follows this convention:
  * it is the name given to `--cert-name`,
  * if `--cert-name` is not set by the user it is the first domain given to `--domains`,
  * if the first domain is a wildcard domain (eg. `*.example.com`) the certificate name will be `example.com`,
  * if a name collision would occur with a certificate already named `example.com`, the new certificate name will be constructed using a numerical sequence as `example.com-001`.


For historical reasons, the containing directories are created with permissions of `0700` meaning that certificates are accessible only to servers that run as the root user. **If you will never downgrade to an older version of Certbot** , then you can safely fix this using `chmod 0755 /etc/letsencrypt/{live,archive}`.
For servers that drop root privileges before attempting to read the private key file, you will also need to use `chgrp` and `chmod 0640` to allow the server to read `/etc/letsencrypt/live/$domain/privkey.pem`.
The following files are available: 

`privkey.pem`
    
Private key for the certificate.
Warning
This **must be kept secret at all times**! Never share it with anyone, including Certbot developers. You cannot put it into a safe, however - your server still needs to access this file in order for SSL/TLS to work.
Note
As of Certbot version 0.29.0, private keys for new certificate default to `0600`. Any changes to the group mode or group owner (gid) of this file will be preserved on renewals.
This is what Apache needs for [SSLCertificateKeyFile](https://httpd.apache.org/docs/2.4/mod/mod_ssl.html#sslcertificatekeyfile), and Nginx for [ssl_certificate_key](https://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_certificate_key). 

`fullchain.pem`
    
All certificates, **including** server certificate (aka leaf certificate or end-entity certificate). The server certificate is the first one in this file, followed by any intermediates.
This is what Apache >= 2.4.8 needs for [SSLCertificateFile](https://httpd.apache.org/docs/2.4/mod/mod_ssl.html#sslcertificatefile), and what Nginx needs for [ssl_certificate](https://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_certificate). 

`cert.pem` and `chain.pem` (less common)
    
`cert.pem` contains the server certificate by itself, and `chain.pem` contains the additional intermediate certificate or certificates that web browsers will need in order to validate the server certificate. If you provide one of these files to your web server, you **must** provide both of them, or some browsers will show “This Connection is Untrusted” errors for your site, [some of the time](https://whatsmychaincert.com/).
Apache < 2.4.8 needs these for [SSLCertificateFile](https://httpd.apache.org/docs/2.4/mod/mod_ssl.html#sslcertificatefile). and [SSLCertificateChainFile](https://httpd.apache.org/docs/2.4/mod/mod_ssl.html#sslcertificatechainfile), respectively.
If you’re using OCSP stapling with Nginx >= 1.3.7, `chain.pem` should be provided as the [ssl_trusted_certificate](https://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_trusted_certificate) to validate OCSP responses.
Note
All files are PEM-encoded. If you need other format, such as DER or PFX, then you could convert using `openssl`. You can automate that with `--deploy-hook` if you’re using automatic [renewal](https://eff-certbot.readthedocs.io/en/stable/using.html#renewal).
##  [Pre and Post Validation Hooks](https://eff-certbot.readthedocs.io/en/stable/using.html#id34)[](https://eff-certbot.readthedocs.io/en/stable/using.html#pre-and-post-validation-hooks "Link to this heading")
Certbot allows for the specification of pre and post validation hooks when run in manual mode. The flags to specify these scripts are `--manual-auth-hook` and `--manual-cleanup-hook` respectively and can be used as follows:

```
certbot certonly --manual --manual-auth-hook /path/to/http/authenticator.sh --manual-cleanup-hook /path/to/http/cleanup.sh -d secure.example.com

```

This will run the `authenticator.sh` script, attempt the validation, and then run the `cleanup.sh` script. Additionally certbot will pass relevant environment variables to these scripts:
  * `CERTBOT_IDENTIFIER`: The domain or IP address being authenticated
  * `CERTBOT_VALIDATION`: The validation string
  * `CERTBOT_TOKEN`: Resource name part of the HTTP-01 challenge (HTTP-01 only)
  * `CERTBOT_REMAINING_CHALLENGES`: Number of challenges remaining after the current challenge
  * `CERTBOT_ALL_IDENTIFIERS`: A comma-separated list of all identifiers challenged for the current certificate


Additionally for cleanup:
  * `CERTBOT_AUTH_OUTPUT`: Whatever the auth script wrote to stdout


Certbot also sets `CERTBOT_DOMAIN` and `CERTBOT_ALL_DOMAINS` to the same values as `CERTBOT_IDENTIFIER` and `CERTBOT_ALL_IDENTIFIERS` respectively for backwards compatibility, however, the variables names containing “identifier” are preferred since Certbot has added support for obtaining certificates for IP addresses.
Example usage for HTTP-01:

```
certbot certonly --manual --preferred-challenges=http --manual-auth-hook /path/to/http/authenticator.sh --manual-cleanup-hook /path/to/http/cleanup.sh -d secure.example.com

```

/path/to/http/authenticator.sh

```
#!/bin/bash
echo $CERTBOT_VALIDATION > /var/www/htdocs/.well-known/acme-challenge/$CERTBOT_TOKEN

```

/path/to/http/cleanup.sh

```
#!/bin/bash
rm -f /var/www/htdocs/.well-known/acme-challenge/$CERTBOT_TOKEN

```

Example usage for DNS-01 (Cloudflare API v4) (for example purposes only, do not use as-is)

```
certbot certonly --manual --preferred-challenges=dns --manual-auth-hook /path/to/dns/authenticator.sh --manual-cleanup-hook /path/to/dns/cleanup.sh -d secure.example.com

```

/path/to/dns/authenticator.sh

```
#!/bin/bash

# Get your API key from https://www.cloudflare.com/a/account/my-account
API_KEY="your-api-key"
EMAIL="your.email@example.com"

# Strip only the top domain to get the zone id
DOMAIN=$(expr match "$CERTBOT_IDENTIFIER" '.*\.\(.*\..*\)')

# Get the Cloudflare zone id
ZONE_EXTRA_PARAMS="status=active&page=1&per_page=20&order=status&direction=desc&match=all"
ZONE_ID=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=$DOMAIN&$ZONE_EXTRA_PARAMS" \
     -H     "X-Auth-Email: $EMAIL" \
     -H     "X-Auth-Key: $API_KEY" \
     -H     "Content-Type: application/json" | python -c "import sys,json;print(json.load(sys.stdin)['result'][0]['id'])")

# Create TXT record
CREATE_DOMAIN="_acme-challenge.$CERTBOT_IDENTIFIER"
RECORD_ID=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
     -H     "X-Auth-Email: $EMAIL" \
     -H     "X-Auth-Key: $API_KEY" \
     -H     "Content-Type: application/json" \
     --data '{"type":"TXT","name":"'"$CREATE_DOMAIN"'","content":"'"$CERTBOT_VALIDATION"'","ttl":120}' \
             | python -c "import sys,json;print(json.load(sys.stdin)['result']['id'])")
# Save info for cleanup
if [ ! -d /tmp/CERTBOT_$CERTBOT_IDENTIFIER ];then
        mkdir -m 0700 /tmp/CERTBOT_$CERTBOT_IDENTIFIER
fi
echo $ZONE_ID > /tmp/CERTBOT_$CERTBOT_IDENTIFIER/ZONE_ID
echo $RECORD_ID > /tmp/CERTBOT_$CERTBOT_IDENTIFIER/RECORD_ID

# Sleep to make sure the change has time to propagate over to DNS
sleep 25

```

/path/to/dns/cleanup.sh

```
#!/bin/bash

# Get your API key from https://www.cloudflare.com/a/account/my-account
API_KEY="your-api-key"
EMAIL="your.email@example.com"

if [ -f /tmp/CERTBOT_$CERTBOT_IDENTIFIER/ZONE_ID ]; then
        ZONE_ID=$(cat /tmp/CERTBOT_$CERTBOT_IDENTIFIER/ZONE_ID)
        rm -f /tmp/CERTBOT_$CERTBOT_IDENTIFIER/ZONE_ID
fi

if [ -f /tmp/CERTBOT_$CERTBOT_IDENTIFIER/RECORD_ID ]; then
        RECORD_ID=$(cat /tmp/CERTBOT_$CERTBOT_IDENTIFIER/RECORD_ID)
        rm -f /tmp/CERTBOT_$CERTBOT_IDENTIFIER/RECORD_ID
fi

# Remove the challenge TXT record from the zone
if [ -n "${ZONE_ID}" ]; then
    if [ -n "${RECORD_ID}" ]; then
        curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
                -H "X-Auth-Email: $EMAIL" \
                -H "X-Auth-Key: $API_KEY" \
                -H "Content-Type: application/json"
    fi
fi

```

##  [Changing the ACME Server](https://eff-certbot.readthedocs.io/en/stable/using.html#id35)[](https://eff-certbot.readthedocs.io/en/stable/using.html#changing-the-acme-server "Link to this heading")
By default, Certbot uses Let’s Encrypt’s production server at <https://acme-v02.api.letsencrypt.org/directory>. You can tell Certbot to use a different CA by providing `--server` on the command line or in a [configuration file](https://eff-certbot.readthedocs.io/en/stable/using.html#config-file) with the URL of the server’s ACME directory. For example, if you would like to use Let’s Encrypt’s staging server, you would add `--server https://acme-staging-v02.api.letsencrypt.org/directory` to the command line.
Note
`--dry-run` uses the Let’s Encrypt staging server, unless `--server` is specified on the CLI or in the [cli.ini configuration file](https://eff-certbot.readthedocs.io/en/stable/using.html#config-file). Take caution when using `--dry-run` with a custom server, as it may cause real certificates to be issued and discarded.
If Certbot does not trust the SSL certificate used by the ACME server, you can use the [REQUESTS_CA_BUNDLE](https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification) environment variable to override the root certificates trusted by Certbot. Certbot uses the `requests` library, which does not use the operating system trusted root store. Make sure that `REQUESTS_CA_BUNDLE` is set globally in the environment and not only on the CLI, or scheduled renewal will not succeed.
##  [Lock Files](https://eff-certbot.readthedocs.io/en/stable/using.html#id36)[](https://eff-certbot.readthedocs.io/en/stable/using.html#id5 "Link to this heading")
When processing a validation Certbot writes a number of lock files on your system to prevent multiple instances from overwriting each other’s changes. This means that by default two instances of Certbot will not be able to run in parallel.
Since the directories used by Certbot are configurable, Certbot will write a lock file for all of the directories it uses. This include Certbot’s `--work-dir`, `--logs-dir`, and `--config-dir`. By default these are `/var/lib/letsencrypt`, `/var/log/letsencrypt`, and `/etc/letsencrypt` respectively. Additionally if you are using Certbot with Apache or nginx it will lock the configuration folder for that program, which are typically also in the `/etc` directory.
Note that these lock files will only prevent other instances of Certbot from using those directories, not other processes. If you’d like to run multiple instances of Certbot simultaneously you should specify different directories as the `--work-dir`, `--logs-dir`, and `--config-dir` for each instance of Certbot that you would like to run.
##  [Configuration file](https://eff-certbot.readthedocs.io/en/stable/using.html#id37)[](https://eff-certbot.readthedocs.io/en/stable/using.html#configuration-file "Link to this heading")
Certbot accepts a global configuration file that applies its options to all invocations of Certbot. Certificate-specific configuration choices are stored in the `.conf` files that can be found in `/etc/letsencrypt/renewal`. See [Modifying the Renewal Configuration of Existing Certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#modifying-the-renewal-configuration-of-existing-certificates) for more information about modifying certificate-specific options. Note that it is not recommended to modify these certificate-specific renewal configuration files manually.
By default no cli.ini file is created (though it may exist already if you installed Certbot via a package manager, for instance). After creating one it is possible to specify the location of this configuration file with `certbot --config cli.ini` (or shorter `-c cli.ini`). An example configuration file is shown below:

```
# This is an example of the kind of things you can do in a configuration file.
# All flags used by the client can be configured here. Run Certbot with
# "--help" to learn more about the available options.
#
# Note that these options apply automatically to all use of Certbot for
# obtaining or renewing certificates, so options specific to a single
# certificate on a system with several certificates should not be placed
# here.

# Use ECC for the private key
key-type = ecdsa
elliptic-curve = secp384r1

# Use a 4096 bit RSA key instead of 2048
rsa-key-size = 4096

# Uncomment and update to register with the specified e-mail address
# email = foo@example.com

# Uncomment to use the standalone authenticator on port 80
# authenticator = standalone

# Uncomment to use the webroot authenticator. Replace webroot-path with the
# path to the public_html / webroot folder being served by your web server.
# authenticator = webroot
# webroot-path = /usr/share/nginx/html

# Uncomment to automatically agree to the terms of service of the ACME server
# agree-tos = true

# An example of using an alternate ACME server that uses EAB credentials
# server = https://acme.sectigo.com/v2/InCommonRSAOV 
# eab-kid = somestringofstuffwithoutquotes
# eab-hmac-key = yaddayaddahexhexnotquoted

```

By default, the following locations are searched:
  * `/etc/letsencrypt/cli.ini`
  * `$XDG_CONFIG_HOME/letsencrypt/cli.ini` (or `~/.config/letsencrypt/cli.ini` if `$XDG_CONFIG_HOME` is not set).


Since this configuration file applies to all invocations of certbot it is incorrect to list domains in it. Listing domains in cli.ini may prevent renewal from working. Additionally due to how arguments in cli.ini are parsed, options which wish to not be set should not be listed. Options set to false will instead be read as being set to true by older versions of Certbot, since they have been listed in the config file.
##  [Log Rotation](https://eff-certbot.readthedocs.io/en/stable/using.html#id38)[](https://eff-certbot.readthedocs.io/en/stable/using.html#log-rotation "Link to this heading")
By default certbot stores status logs in `/var/log/letsencrypt`. By default certbot will begin rotating logs once there are 1000 logs in the log directory. Meaning that once 1000 files are in `/var/log/letsencrypt` Certbot will delete the oldest one to make room for new logs. The number of subsequent logs can be changed by passing the desired number to the command line flag `--max-log-backups`. Setting this flag to 0 disables log rotation entirely, causing certbot to always append to the same log file.
Note
Some distributions, including Debian and Ubuntu, disable certbot’s internal log rotation in favor of a more traditional logrotate script. If you are using a distribution’s packages and want to alter the log rotation, check `/etc/logrotate.d/` for a certbot rotation script.
##  [Certbot command-line options](https://eff-certbot.readthedocs.io/en/stable/using.html#id39)[](https://eff-certbot.readthedocs.io/en/stable/using.html#certbot-command-line-options "Link to this heading")
Certbot supports a lot of command line options. Here’s the full list, from `certbot --help all`:

```
usage: 
  certbot [SUBCOMMAND] [options] [-d DOMAIN] [-d DOMAIN] ...

Certbot can obtain and install HTTPS/TLS/SSL certificates.  By default,
it will attempt to use a webserver both for obtaining and installing the
certificate. The most common SUBCOMMANDS and flags are:

obtain, install, and renew certificates:
    (default) run   Obtain & install a certificate in your current webserver
    certonly        Obtain or renew a certificate, but do not install it
    renew           Renew all previously obtained certificates that are near expiry
    enhance         Add security enhancements to your existing configuration
   -d DOMAINS       Comma-separated list of domains to obtain a certificate for

  --apache          Use the Apache plugin for authentication & installation
  --standalone      Run a standalone webserver for authentication
  --nginx           Use the Nginx plugin for authentication & installation
  --webroot         Place files in a server's webroot folder for authentication
  --manual          Obtain certificates interactively, or using shell script hooks

   -n               Run non-interactively
  --test-cert       Obtain a test certificate from a staging server
  --dry-run         Test "renew" or "certonly" without saving any certificates to disk

manage certificates:
    certificates    Display information about certificates you have from Certbot
    revoke          Revoke a certificate (supply --cert-name or --cert-path)
    delete          Delete a certificate (supply --cert-name)
    reconfigure     Update a certificate's configuration (supply --cert-name)

manage your account:
    register        Create an ACME account
    unregister      Deactivate an ACME account
    update_account  Update an ACME account
    show_account    Display account details
  --agree-tos       Agree to the ACME server's Subscriber Agreement
   -m EMAIL         Email address for important account notifications

options:
  -h, --help            show this help message and exit
  -c, --config CONFIG_FILE
                        path to config file (default: /etc/letsencrypt/cli.ini
                        and ~/.config/letsencrypt/cli.ini)
  -v, --verbose         This flag can be used multiple times to incrementally
                        increase the verbosity of output, e.g. -vvv. (default:
                        0)
  --max-log-backups MAX_LOG_BACKUPS
                        Specifies the maximum number of backup logs that
                        should be kept by Certbot's built in log rotation.
                        Setting this flag to 0 disables log rotation entirely,
                        causing Certbot to always append to the same log file.
                        (default: 1000)
  -n, --non-interactive, --noninteractive
                        Run without ever asking for user input. This may
                        require additional command line flags; the client will
                        try to explain which ones are required if it finds one
                        missing (default: False)
  --force-interactive   Force Certbot to be interactive even if it detects
                        it's not being run in a terminal. This flag cannot be
                        used with the renew subcommand. (default: False)
  -d, --domains, --domain DOMAIN
                        Domain names to include. For multiple domains you can
                        use multiple -d flags or enter a comma separated list
                        of domains as a parameter. All domains will be
                        included as Subject Alternative Names on the
                        certificate. The first domain will be used as the
                        certificate name, unless otherwise specified or if you
                        already have a certificate with the same name. In the
                        case of a name conflict, a number like -0001 will be
                        appended to the certificate name. (default: Ask)
  --ip-address IP_ADDRESSES
                        IP addresses to include. For multiple IP addresses you
                        can use multiple --ip-address flags. All IP addresses
                        will be included as Subject Alternative Names on the
                        certificate. (default: [])
  --eab-kid EAB_KID     Key Identifier for External Account Binding (default:
                        None)
  --eab-hmac-key EAB_HMAC_KEY
                        HMAC key for External Account Binding (default: None)
  --eab-hmac-alg EAB_HMAC_ALG
                        HMAC algorithm for External Account Binding (default:
                        HS256)
  --cert-name CERTNAME  Certificate name to apply. This name is used by
                        Certbot for housekeeping and in file paths; it doesn't
                        affect the content of the certificate itself.
                        Certificate name cannot contain filepath separators
                        (i.e. '/' or '\', depending on the platform). To see
                        certificate names, run 'certbot certificates'. When
                        creating a new certificate, specifies the new
                        certificate's name. (default: the first provided
                        domain or the name of an existing certificate on your
                        system for the same domains)
  --dry-run             Perform a test run against the Let's Encrypt staging
                        server, obtaining test (invalid) certificates but not
                        saving them to disk. This can only be used with the
                        'certonly' and 'renew' subcommands. It may trigger
                        webserver reloads to temporarily modify & roll back
                        configuration files. --pre-hook and --post-hook
                        commands run by default. --deploy-hook commands do not
                        run, unless enabled by --run-deploy-hooks. The test
                        server may be overridden with --server. (default:
                        False)
  --debug-challenges    After setting up challenges, wait for user input
                        before submitting to CA. When used in combination with
                        the `-v` option, the challenge URLs or FQDNs and their
                        expected return values are shown. (default: False)
  --required-profile REQUIRED_PROFILE
                        Request the given profile name from the ACME server.
                        If the ACME server returns an error, issuance (or
                        renewal) will fail. For long-term reliability, setting
                        preferred_profile instead may be preferable because it
                        allows fallback to a default. Use this setting when
                        renewal failure is preferable to fallback. (default:
                        None)
  --preferred-profile PREFERRED_PROFILE
                        Request the given profile name from the ACME server,
                        or fallback to default. If the given profile name
                        exists in the ACME directory, use it to request a a
                        certificate. Otherwise, fall back to requesting a
                        certificate without a profile (which means the CA will
                        use its default profile). This allows renewals to
                        succeed even if the CA deprecates and removes a given
                        profile. (default: None)
  --preferred-chain PREFERRED_CHAIN
                        Set the preferred certificate chain. If the CA offers
                        multiple certificate chains, prefer the chain whose
                        topmost certificate was issued from this Subject
                        Common Name. If no match, the default offered chain
                        will be used. (default: None)
  --preferred-challenges PREF_CHALLS
                        A sorted, comma delimited list of the preferred
                        challenge to use during authorization with the most
                        preferred challenge listed first (Eg, "dns" or
                        "http,dns"). Not all plugins support all challenges.
                        See https://certbot.eff.org/docs/using.html#plugins
                        for details. ACME Challenges are versioned, but if you
                        pick "http" rather than "http-01", Certbot will select
                        the latest version automatically. (default: [])
  --issuance-timeout ISSUANCE_TIMEOUT
                        This option specifies how long (in seconds) Certbot
                        will wait for the server to issue a certificate.
                        (default: 90)
  --user-agent USER_AGENT
                        Set a custom user agent string for the client. User
                        agent strings allow the CA to collect high level
                        statistics about success rates by OS, plugin and use
                        case, and to know when to deprecate support for past
                        Python versions and flags. If you wish to hide this
                        information from the Let's Encrypt server, set this to
                        "". (default: CertbotACMEClient/5.8.0 (certbot;
                        OS_NAME OS_VERSION) Authenticator/XXX Installer/YYY
                        (SUBCOMMAND; flags: FLAGS) Py/major.minor.patchlevel).
                        The flags encoded in the user agent are: --duplicate,
                        --force-renew, --allow-subset-of-names, -n, and
                        whether any hooks are set.
  --user-agent-comment USER_AGENT_COMMENT
                        Add a comment to the default user agent string. May be
                        used when repackaging Certbot or calling it from
                        another tool to allow additional statistical data to
                        be collected. Ignored if --user-agent is set.
                        (Example: Foo-Wrapper/1.0) (default: None)

automation:
  Flags for automating execution & other tweaks

  --keep-until-expiring, --keep, --reinstall
                        If the requested certificate matches an existing
                        certificate, always keep the existing one until it is
                        due for renewal (for the 'run' subcommand this means
                        reinstall the existing certificate). (default: Ask)
  --expand              If an existing certificate is a strict subset of the
                        requested names, always expand and replace it with the
                        additional names. (default: Ask)
  --version             show program's version number and exit
  --force-renewal, --renew-by-default
                        If a certificate already exists for the requested
                        domains, renew it now, regardless of whether it is
                        near expiry. (Often --keep-until-expiring is more
                        appropriate). Also implies --expand. (default: False)
  --renew-with-new-domains
                        If a certificate already exists for the requested
                        certificate name but does not match the requested
                        domains, renew it now, regardless of whether it is
                        near expiry. (default: False)
  --reuse-key           When renewing, use the same private key as the
                        existing certificate. (default: False)
  --no-reuse-key        When renewing, do not use the same private key as the
                        existing certificate. Not reusing private keys is the
                        default behavior of Certbot. This option may be used
                        to unset --reuse-key on an existing certificate.
                        (default: False)
  --new-key             When renewing or replacing a certificate, generate a
                        new private key, even if --reuse-key is set on the
                        existing certificate. Combining --new-key and --reuse-
                        key will result in the private key being replaced and
                        then reused in future renewals. (default: False)
  --allow-subset-of-names
                        When performing domain validation, do not consider it
                        a failure if authorizations can not be obtained for a
                        strict subset of the requested domains. This may be
                        useful for allowing renewals for multiple domains to
                        succeed even if some domains no longer point at this
                        system. This option cannot be used with --csr.
                        (default: False)
  --agree-tos           Agree to the ACME Subscriber Agreement (default: Ask)
  --duplicate           Allow making a certificate lineage that duplicates an
                        existing one (both can be renewed in parallel)
                        (default: False)
  -q, --quiet           Silence all output except errors. Useful for
                        automation via cron. Implies --non-interactive.
                        (default: False)

security:
  Security parameters & server settings

  --rsa-key-size N      Size of the RSA key. (default: 2048)
  --key-type {rsa,ecdsa}
                        Type of generated private key. Only *ONE* per
                        invocation can be provided at this time. (default:
                        ecdsa)
  --elliptic-curve N    The SECG elliptic curve name to use. Please see RFC
                        8446 for supported values. (default: secp256r1)
  --must-staple         Adds the OCSP Must-Staple extension to the
                        certificate. Autoconfigures OCSP Stapling for
                        supported setups (Apache version >= 2.3.3 ). (default:
                        False)
  --redirect            Automatically redirect all HTTP traffic to HTTPS for
                        the newly authenticated vhost. (default: redirect
                        enabled for install and run, disabled for enhance)
  --no-redirect         Do not automatically redirect all HTTP traffic to
                        HTTPS for the newly authenticated vhost. (default:
                        redirect enabled for install and run, disabled for
                        enhance)
  --hsts                Add the Strict-Transport-Security header to every HTTP
                        response. Forcing browser to always use SSL for the
                        domain. Defends against SSL Stripping. (default:
                        False)
  --uir                 Add the "Content-Security-Policy: upgrade-insecure-
                        requests" header to every HTTP response. Forcing the
                        browser to use https:// for every http:// resource.
                        (default: False)
  --staple-ocsp         Enables OCSP Stapling. A valid OCSP response is
                        stapled to the certificate that the server offers
                        during TLS. (default: False)
  --strict-permissions  Require that all configuration files are owned by the
                        current user; only needed if your config is somewhere
                        unsafe like /tmp/ (default: False)
  --auto-hsts           Gradually increasing max-age value for HTTP Strict
                        Transport Security security header (default: False)

testing:
  The following flags are meant for testing and integration purposes only.

  --run-deploy-hooks    When performing a test run using `--dry-run` or
                        `reconfigure`, run any applicable deploy hooks. This
                        includes hooks set on the command line, saved in the
                        certificate's renewal configuration file, or present
                        in the renewal-hooks directory. To exclude directory
                        hooks, use --no-directory-hooks. The hook(s) will only
                        be run if the dry run succeeds, and will use the
                        current active certificate, not the temporary test
                        certificate acquired during the dry run. This flag is
                        recommended when modifying the deploy hook using
                        `reconfigure`. (default: False)
  --test-cert, --staging
                        Use the Let's Encrypt staging server to obtain or
                        revoke test (invalid) certificates; equivalent to
                        --server https://acme-
                        staging-v02.api.letsencrypt.org/directory (default:
                        False)
  --debug               Show tracebacks in case of errors (default: False)
  --no-verify-ssl       Disable verification of the ACME server's certificate.
                        The root certificates trusted by Certbot can be
                        overridden by setting the REQUESTS_CA_BUNDLE
                        environment variable. (default: False)
  --http-01-port HTTP01_PORT
                        Port used in the http-01 challenge. This only affects
                        the port Certbot listens on. A conforming ACME server
                        will still attempt to connect on port 80. (default:
                        80)
  --http-01-address HTTP01_ADDRESS
                        The address the server listens to during http-01
                        challenge. (default: )
  --https-port HTTPS_PORT
                        Port used to serve HTTPS. This affects which port
                        Nginx will listen on after a LE certificate is
                        installed. (default: 443)
  --break-my-certs      Be willing to replace or renew valid certificates with
                        invalid (testing/staging) certificates (default:
                        False)

paths:
  Flags for changing execution paths & servers

  --cert-path CERT_PATH
                        Path to where certificate is saved (with certonly
                        --csr), installed from, or revoked (default: None)
  --key-path KEY_PATH   Path to private key for certificate installation or
                        revocation (if account key is missing) (default: None)
  --fullchain-path FULLCHAIN_PATH
                        Accompanying path to a full certificate chain
                        (certificate plus chain). (default: None)
  --chain-path CHAIN_PATH
                        Accompanying path to a certificate chain. (default:
                        None)
  --config-dir CONFIG_DIR
                        Configuration directory. (default: /etc/letsencrypt)
  --work-dir WORK_DIR   Working directory. (default: /var/lib/letsencrypt)
  --logs-dir LOGS_DIR   Logs directory. (default: /var/log/letsencrypt)
  --server SERVER       ACME Directory Resource URI. (default:
                        https://acme-v02.api.letsencrypt.org/directory)

manage:
  Various subcommands and flags are available for managing your
  certificates:

  certificates          List certificates managed by Certbot
  delete                Clean up all files related to a certificate
  renew                 Renew all certificates (or one specified with --cert-
                        name)
  revoke                Revoke a certificate specified with --cert-path or
                        --cert-name
  reconfigure           Update renewal configuration for a certificate
                        specified by --cert-name

run:
  Options for obtaining & installing certificates

certonly:
  Options for modifying how a certificate is obtained

  --deploy-hook DEPLOY_HOOK
                        Command to be run in a shell once for each
                        successfully issued certificate, including on
                        subsequent renewals. Unless --disable-hook-validation
                        is used, the command’s first word must be the absolute
                        pathname of an executable or one found via the PATH
                        environment variable. For this command, the shell
                        variable $RENEWED_LINEAGE will point to the config
                        live subdirectory (for example,
                        "/etc/letsencrypt/live/example.com") containing the
                        new certificates and keys; the shell variable
                        $RENEWED_DOMAINS will contain a space-delimited list
                        of renewed certificate domains (for example,
                        "example.com www.example.com") (default: None)
  --csr CSR             Path to a Certificate Signing Request (CSR) in DER or
                        PEM format. Currently --csr only works with the
                        'certonly' subcommand. (default: None)

renew:
  The 'renew' subcommand will attempt to renew any certificates previously
  obtained if they are close to expiry, and print a summary of the results.
  By default, 'renew' will reuse the plugins and options used to obtain or
  most recently renew each certificate. You can test whether future renewals
  will succeed with `--dry-run`. Individual certificates can be renewed with
  the `--cert-name` option. Hooks are available to run commands before and
  after renewal; see https://certbot.eff.org/docs/using.html#renewal for
  more information on these.

  --pre-hook PRE_HOOK   Command to be run in a shell before obtaining any
                        certificates. Unless --disable-hook-validation is
                        used, the command’s first word must be the absolute
                        pathname of an executable or one found via the PATH
                        environment variable. Intended primarily for renewal,
                        where it can be used to temporarily shut down a
                        webserver that might conflict with the standalone
                        plugin. This will only be called if a certificate is
                        actually to be obtained/renewed. When renewing several
                        certificates that have identical pre-hooks, only the
                        first will be executed. (default: None)
  --post-hook POST_HOOK
                        Command to be run in a shell after attempting to
                        obtain/renew certificates. Unless --disable-hook-
                        validation is used, the command’s first word must be
                        the absolute pathname of an executable or one found
                        via the PATH environment variable. Can be used to
                        deploy renewed certificates, or to restart any servers
                        that were stopped by --pre-hook. This is only run if
                        an attempt was made to obtain/renew a certificate. If
                        multiple renewed certificates have identical post-
                        hooks, only one will be run. (default: None)
  --disable-hook-validation
                        Ordinarily the commands specified for --pre-
                        hook/--post-hook/--deploy-hook will be checked for
                        validity, to see if the programs being run are in the
                        $PATH, so that mistakes can be caught early, even when
                        the hooks aren't being run just yet. The validation is
                        rather simplistic and fails if you use more advanced
                        shell constructs, so you can use this switch to
                        disable it. (default: False)
  --no-directory-hooks  Disable running executables found in Certbot's hook
                        directories. (default: False)
  --disable-renew-updates
                        Disable automatic updates to your server configuration
                        that would otherwise be done by the selected installer
                        plugin, and triggered when the user executes "certbot
                        renew", regardless of if the certificate is renewed.
                        This setting does not apply to important TLS
                        configuration updates. (default: False)
  --no-autorenew        Disable auto renewal of certificates. (default: False)

certificates:
  List certificates managed by Certbot

delete:
  Options for deleting a certificate

revoke:
  Options for revocation of certificates

  --reason {unspecified,keycompromise,affiliationchanged,superseded,cessationofoperation}
                        Specify reason for revoking certificate. (default:
                        unspecified)
  --delete-after-revoke
                        Delete certificates after revoking them, along with
                        all previous and later versions of those certificates.
                        (default: Ask)
  --no-delete-after-revoke
                        Do not delete certificates after revoking them. This
                        option should be used with caution because the 'renew'
                        subcommand will attempt to renew undeleted revoked
                        certificates. (default: Ask)

register:
  Options for account registration

  -m, --email EMAIL     Email used for registration and recovery contact. Use
                        comma to register multiple emails, ex:
                        u1@example.com,u2@example.com. (default: Ask).
  --eff-email           Share your e-mail address with EFF (default: Ask)
  --no-eff-email        Don't share your e-mail address with EFF (default:
                        Ask)

update_account:
  Options for account modification

unregister:
  Options for account deactivation.

  --account ACCOUNT_ID  Account ID to use (default: None)

install:
  Options for modifying how a certificate is deployed

rollback:
  Options for rolling back server configuration changes

  --checkpoints N       Revert configuration N number of checkpoints.
                        (default: 1)

plugins:
  Options for the "plugins" subcommand

  --init                Initialize plugins. (default: False)
  --prepare             Initialize and prepare plugins. (default: False)
  --authenticators      Limit to authenticator plugins only. (default: None)
  --installers          Limit to installer plugins only. (default: None)

enhance:
  Helps to harden the TLS configuration by adding security enhancements to
  already existing configuration.

show_account:
  Options useful for the "show_account" subcommand:

reconfigure:
  Common options that may be updated with the "reconfigure" subcommand:

plugins:
  Plugin Selection: Certbot client supports an extensible plugins
  architecture. See 'certbot plugins' for a list of all installed plugins
  and their names. You can force a particular plugin by setting options
  provided below. Running --help <plugin_name> will list flags specific to
  that plugin.

  --configurator CONFIGURATOR
                        Name of the plugin that is both an authenticator and
                        an installer. Should not be used together with
                        --authenticator or --installer. (default: Ask)
  -a, --authenticator AUTHENTICATOR
                        Authenticator plugin name. (default: None)
  -i, --installer INSTALLER
                        Installer plugin name (also used to find domains).
                        (default: None)
  --apache              Obtain and install certificates using Apache (default:
                        False)
  --nginx               Obtain and install certificates using Nginx (default:
                        False)
  --standalone          Obtain certificates using a "standalone" webserver.
                        (default: False)
  --manual              Provide laborious manual instructions for obtaining a
                        certificate (default: False)
  --webroot             Obtain certificates by placing files in a webroot
                        directory. (default: False)
  --dns-cloudflare      Obtain certificates using a DNS TXT record (if you are
                        using Cloudflare for DNS). (default: False)
  --dns-digitalocean    Obtain certificates using a DNS TXT record (if you are
                        using DigitalOcean for DNS). (default: False)
  --dns-dnsimple        Obtain certificates using a DNS TXT record (if you are
                        using DNSimple for DNS). (default: False)
  --dns-dnsmadeeasy     Obtain certificates using a DNS TXT record (if you are
                        using DNS Made Easy for DNS). (default: False)
  --dns-gehirn          Obtain certificates using a DNS TXT record (if you are
                        using Gehirn Infrastructure Service for DNS).
                        (default: False)
  --dns-google          Obtain certificates using a DNS TXT record (if you are
                        using Google Cloud DNS). (default: False)
  --dns-linode          Obtain certificates using a DNS TXT record (if you are
                        using Linode for DNS). (default: False)
  --dns-luadns          Obtain certificates using a DNS TXT record (if you are
                        using LuaDNS for DNS). (default: False)
  --dns-nsone           Obtain certificates using a DNS TXT record (if you are
                        using NS1 for DNS). (default: False)
  --dns-ovh             Obtain certificates using a DNS TXT record (if you are
                        using OVH for DNS). (default: False)
  --dns-rfc2136         Obtain certificates using a DNS TXT record (if you are
                        using BIND for DNS). (default: False)
  --dns-route53         Obtain certificates using a DNS TXT record (if you are
                        using Route53 for DNS). (default: False)
  --dns-sakuracloud     Obtain certificates using a DNS TXT record (if you are
                        using Sakura Cloud for DNS). (default: False)

apache:
  Apache Web Server plugin (Please note that the default values of the
  Apache plugin options change depending on the operating system Certbot is
  run on.)

  --apache-enmod APACHE_ENMOD
                        Path to the Apache 'a2enmod' binary (default: None)
  --apache-dismod APACHE_DISMOD
                        Path to the Apache 'a2dismod' binary (default: None)
  --apache-le-vhost-ext APACHE_LE_VHOST_EXT
                        SSL vhost configuration extension (default: -le-
                        ssl.conf)
  --apache-server-root APACHE_SERVER_ROOT
                        Apache server root directory (default: /etc/apache2)
  --apache-vhost-root APACHE_VHOST_ROOT
                        Apache server VirtualHost configuration root (default:
                        None)
  --apache-logs-root APACHE_LOGS_ROOT
                        Apache server logs directory (default:
                        /var/log/apache2)
  --apache-challenge-location APACHE_CHALLENGE_LOCATION
                        Directory path for challenge configuration (default:
                        /etc/apache2)
  --apache-handle-modules APACHE_HANDLE_MODULES
                        Let installer handle enabling required modules for you
                        (Only Ubuntu/Debian currently) (default: False)
  --apache-handle-sites APACHE_HANDLE_SITES
                        Let installer handle enabling sites for you (Only
                        Ubuntu/Debian currently) (default: False)
  --apache-ctl APACHE_CTL
                        Full path to Apache control script (default:
                        apache2ctl)
  --apache-bin APACHE_BIN
                        Full path to apache2/httpd binary (default: None)

dns-cloudflare:
  Obtain certificates using a DNS TXT record (if you are using Cloudflare
  for DNS).

  --dns-cloudflare-propagation-seconds DNS_CLOUDFLARE_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 10)
  --dns-cloudflare-credentials DNS_CLOUDFLARE_CREDENTIALS
                        Cloudflare credentials INI file. (default: None)

dns-digitalocean:
  Obtain certificates using a DNS TXT record (if you are using DigitalOcean
  for DNS).

  --dns-digitalocean-propagation-seconds DNS_DIGITALOCEAN_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 10)
  --dns-digitalocean-credentials DNS_DIGITALOCEAN_CREDENTIALS
                        DigitalOcean credentials INI file. (default: None)

dns-dnsimple:
  Obtain certificates using a DNS TXT record (if you are using DNSimple for
  DNS).

  --dns-dnsimple-propagation-seconds DNS_DNSIMPLE_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 30)
  --dns-dnsimple-credentials DNS_DNSIMPLE_CREDENTIALS
                        DNSimple credentials INI file. (default: None)

dns-dnsmadeeasy:
  Obtain certificates using a DNS TXT record (if you are using DNS Made Easy
  for DNS).

  --dns-dnsmadeeasy-propagation-seconds DNS_DNSMADEEASY_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 60)
  --dns-dnsmadeeasy-credentials DNS_DNSMADEEASY_CREDENTIALS
                        DNS Made Easy credentials INI file. (default: None)

dns-gehirn:
  Obtain certificates using a DNS TXT record (if you are using Gehirn
  Infrastructure Service for DNS).

  --dns-gehirn-propagation-seconds DNS_GEHIRN_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 30)
  --dns-gehirn-credentials DNS_GEHIRN_CREDENTIALS
                        Gehirn Infrastructure Service credentials file.
                        (default: None)

dns-google:
  Obtain certificates using a DNS TXT record (if you are using Google Cloud
  DNS for DNS).

  --dns-google-propagation-seconds DNS_GOOGLE_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 60)
  --dns-google-credentials DNS_GOOGLE_CREDENTIALS
                        Path to Google Cloud DNS service account JSON file to
                        use instead of relying on Application Default
                        Credentials (ADC). (See https://cloud.google.com/docs/
                        authentication/application-default-credentials for
                        information about ADC, https://developers.google.com/i
                        dentity/protocols/OAuth2ServiceAccount#creatinganaccou
                        nt for information about creating a service account,
                        and https://cloud.google.com/dns/access-
                        control#permissions_and_roles for information about
                        the permissions required to modify Cloud DNS records.)
                        (default: None)
  --dns-google-project DNS_GOOGLE_PROJECT
                        The ID of the Google Cloud project that the Google
                        Cloud DNS managed zone(s) reside in. This will be
                        determined automatically if not specified. (default:
                        None)

dns-linode:
  Obtain certificates using a DNS TXT record (if you are using Linode for
  DNS).

  --dns-linode-propagation-seconds DNS_LINODE_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 120)
  --dns-linode-credentials DNS_LINODE_CREDENTIALS
                        Linode credentials INI file. (default: None)

dns-luadns:
  Obtain certificates using a DNS TXT record (if you are using LuaDNS for
  DNS).

  --dns-luadns-propagation-seconds DNS_LUADNS_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 30)
  --dns-luadns-credentials DNS_LUADNS_CREDENTIALS
                        LuaDNS credentials INI file. (default: None)

dns-nsone:
  Obtain certificates using a DNS TXT record (if you are using NS1 for DNS).

  --dns-nsone-propagation-seconds DNS_NSONE_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 30)
  --dns-nsone-credentials DNS_NSONE_CREDENTIALS
                        NS1 credentials file. (default: None)

dns-ovh:
  Obtain certificates using a DNS TXT record (if you are using OVH for DNS).

  --dns-ovh-propagation-seconds DNS_OVH_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 120)
  --dns-ovh-credentials DNS_OVH_CREDENTIALS
                        OVH credentials INI file. (default: None)

dns-rfc2136:
  Obtain certificates using a DNS TXT record (if you are using BIND for
  DNS).

  --dns-rfc2136-propagation-seconds DNS_RFC2136_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 60)
  --dns-rfc2136-credentials DNS_RFC2136_CREDENTIALS
                        RFC 2136 credentials INI file. (default: None)

dns-route53:
  Obtain certificates using a DNS TXT record (if you are using AWS Route53
  for DNS).

dns-sakuracloud:
  Obtain certificates using a DNS TXT record (if you are using Sakura Cloud
  for DNS).

  --dns-sakuracloud-propagation-seconds DNS_SAKURACLOUD_PROPAGATION_SECONDS
                        The number of seconds to wait for DNS to propagate
                        before asking the ACME server to verify the DNS
                        record. (default: 90)
  --dns-sakuracloud-credentials DNS_SAKURACLOUD_CREDENTIALS
                        Sakura Cloud credentials file. (default: None)

manual:
  Authenticate through manual configuration or custom shell scripts. When
  using shell scripts, an authenticator script must be provided. The
  environment variables available to this script depend on the type of
  challenge. $CERTBOT_IDENTIFIER will always contain the domain or IP
  address being authenticated. For HTTP-01 and DNS-01, $CERTBOT_VALIDATION
  is the validation string, and $CERTBOT_TOKEN is the filename of the
  resource requested when performing an HTTP-01 challenge. An additional
  cleanup script can also be provided and can use the additional variable
  $CERTBOT_AUTH_OUTPUT which contains the stdout output from the auth
  script. For both authenticator and cleanup script, on HTTP-01 and DNS-01
  challenges, $CERTBOT_REMAINING_CHALLENGES will be equal to the number of
  challenges that remain after the current one, and $CERTBOT_ALL_IDENTIFIERS
  contains a comma-separated list of all identifiers that are challenged for
  the current certificate.

  --manual-auth-hook MANUAL_AUTH_HOOK
                        Path or command to execute for the authentication
                        script (default: None)
  --manual-cleanup-hook MANUAL_CLEANUP_HOOK
                        Path or command to execute for the cleanup script
                        (default: None)

nginx:
  Nginx Web Server plugin

  --nginx-server-root NGINX_SERVER_ROOT
                        Nginx server root directory. (default: /etc/nginx or
                        /usr/local/etc/nginx)
  --nginx-ctl NGINX_CTL
                        Path to the 'nginx' binary, used for 'configtest' and
                        retrieving nginx version number. (default: nginx)
  --nginx-sleep-seconds NGINX_SLEEP_SECONDS
                        Number of seconds to wait for nginx configuration
                        changes to apply when reloading. (default: 1)

null:
  Null Installer

standalone:
  Runs an HTTP server locally which serves the necessary validation files
  under the /.well-known/acme-challenge/ request path. Suitable if there is
  no HTTP server already running. HTTP challenge only (wildcards not
  supported).

webroot:
  Saves the necessary validation files to a .well-known/acme-challenge/
  directory within the nominated webroot path. A separate HTTP server must
  be running and serving files from the webroot path. HTTP challenge only
  (wildcards not supported).

  --webroot-path, -w WEBROOT_PATH
                        public_html / webroot path. This can be specified
                        multiple times to handle different identifiers; each
                        identifier will have the webroot path that preceded
                        it. For instance: `-w /var/www/example -d example.com
                        -d www.example.com -w /var/www/thing -d thing.net -d
                        m.thing.net` (default: Ask)
  --webroot-map WEBROOT_MAP
                        JSON dictionary mapping identifiers to webroot paths;
                        this implies -d or --ip-address for each entry. You
                        may need to escape this from your shell. E.g.:
                        --webroot-map '{"eg1.is,m.eg1.is":"/www/eg1/",
                        "eg2.is":"/www/eg2"}' This option is merged with, but
                        takes precedence over, -w / -d entries. At present, if
                        you put webroot-map in a config file, it needs to be
                        on a single line, like: webroot-map =
                        {"example.com":"/var/www"}. (default: {})

```

##  [Getting help](https://eff-certbot.readthedocs.io/en/stable/using.html#id40)[](https://eff-certbot.readthedocs.io/en/stable/using.html#getting-help "Link to this heading")
If you’re having problems, we recommend posting on the Let’s Encrypt [Community Forum](https://community.letsencrypt.org).
If you find a bug in the software, please do report it in our [issue tracker](https://github.com/certbot/certbot/issues). Remember to give us as much information as possible:
  * copy and paste exact command line used and the output (though mind that the latter might include some personally identifiable information, including your email and domains)
  * copy and paste logs from `/var/log/letsencrypt` (though mind they also might contain personally identifiable information)
  * copy and paste `certbot --version` output
  * your operating system, including specific version
  * specify which installation method you’ve chosen


