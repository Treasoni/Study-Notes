---
url: "https://developers.cloudflare.com/dns/dnssec/"
title: "DNSSEC · Cloudflare DNS docs"
scraped_at: 2026-09-04T04:45:33+00:00
---

[Skip to content](https://developers.cloudflare.com/dns/dnssec/#main-content)
> Documentation IndexFetch the complete documentation index at: https://developers.cloudflare.com/dns/llms.txtUse this file to discover all available pages before exploring further.
# DNSSEC
Last updated Jun 24, 2026|Copy as Markdown|[View as Markdown](https://developers.cloudflare.com/dns/dnssec/index.md)|[Agent setup](https://developers.cloudflare.com/agent-setup/)
DNS Security Extensions (DNSSEC) adds an extra layer of authentication to DNS, ensuring requests are not routed to a spoofed domain.
For additional background on DNSSEC, visit the [Cloudflare Learning Center ↗](https://www.cloudflare.com/learning/dns/dns-security/).
## Disable DNSSEC
If you are onboarding an existing domain to Cloudflare, make sure DNSSEC **is disabled** at your registrar (where you purchased your domain name). Otherwise, your domain will experience connectivity errors when you change your nameservers.
Provider-specific DNSSEC instructions
This is not an exhaustive list, but the following links may be helpful:
  * [DNSimple ↗](https://support.dnsimple.com/articles/cloudflare-ds-record/)
  * [Domaindiscount24 ↗](https://support.domaindiscount24.com/hc/articles/4409759478161)
  * [DreamHost ↗](https://help.dreamhost.com/hc/en-us/articles/219539467)
  * [Dynadot ↗](https://www.dynadot.com/help/question/set-DNSSEC)
  * [Enom ↗](https://support.enom.com/support/solutions/articles/201000065386)
  * [Gandi ↗](https://docs.gandi.net/en/domain_names/advanced_users/dnssec.html)
  * [GoDaddy ↗](https://www.godaddy.com/help/add-a-ds-record-23865)
  * [Hostinger ↗](https://www.hostinger.com/support/3667267-how-to-use-dnssec-records-at-hostinger/)
  * [Hover ↗](https://support.hover.com/support/solutions/articles/201000064716)
  * [Infomaniak ↗](https://faq.infomaniak.com/2187)
  * [InMotion Hosting ↗](https://www.inmotionhosting.com/support/edu/cpanel/enable-dnssec-cloudflare/)
  * [INWX ↗](https://kb.inwx.com/en-us/3-nameserver/131)
  * [Joker.com ↗](https://joker.com/faq/books/jokercom-faq-en/page/dnssec)
  * [Name.com ↗](https://www.name.com/support/articles/205439058-managing-dnssec)
  * [Namecheap ↗](https://www.namecheap.com/support/knowledgebase/article.aspx/9722/2232/managing-dnssec-for-domains-pointed-to-custom-dns/)
  * [NameISP ↗](https://support.nameisp.com/knowledgebase/dns)
  * [Namesilo ↗](https://www.namesilo.com/support/v2/articles/domain-manager/ds-records)
  * [Squarespace ↗](https://support.squarespace.com/hc/articles/4404183898125-Nameservers-and-DNSSEC-for-Squarespace-managed-domains#toc-dnssec)
  * [Registro.br ↗](https://registro.br/tecnologia/dnssec/?secao=tutoriais-dns)
  * [Porkbun ↗](https://kb.porkbun.com/article/93-how-to-install-dnssec) (do not fill out **keyData**)
  * [TransIP ↗](https://www.transip.eu/knowledgebase/150-secure-domains-custom-nameservers-dnssec/)


Why you have to disable DNSSEC
When your domain has [DNSSEC enabled ↗](https://www.cloudflare.com/learning/dns/dns-security/#what-is-dnssec), your DNS provider digitally signs all your DNS records. This action prevents anyone else from issuing false DNS records on your behalf and redirecting traffic intended for your domain.
However, having a single set of signed records also prevents Cloudflare from issuing new DNS records on your behalf (which is part of using Cloudflare for your authoritative nameservers). So if you change your nameservers without disabling DNSSEC, DNSSEC will prevent Cloudflare's DNS records from resolving properly.
## Enable DNSSEC
When you enable DNSSEC, Cloudflare signs your zone, publishes your public signing keys, and generates your **DS** record.
### 1. Activate DNSSEC in Cloudflare
  1. In the Cloudflare dashboard, go to the **DNS Settings** page.
[Go to **Settings** ↗](https://dash.cloudflare.com/?to=/:account/:zone/dns/settings)
  2. For **DNSSEC** , click **Enable DNSSEC**.
  3. In the dialog, you have access to several necessary values to help you create a **DS** record at your registrar. Once you close the dialog, you can access this information by clicking **DS record** on the **DNSSEC** card.


### 2. Add DS record to your registrar
Add the **DS** record to your registrar. If Algorithm 13 - Cloudflare's preferred cipher choice - is not listed by your registrar, it may also be called _ECDSA Curve P-256 with SHA-256_.
Provider-specific DNSSEC instructions
This is not an exhaustive list, but the following links may be helpful:
  * [DNSimple ↗](https://support.dnsimple.com/articles/cloudflare-ds-record/)
  * [Domaindiscount24 ↗](https://support.domaindiscount24.com/hc/articles/4409759478161)
  * [DreamHost ↗](https://help.dreamhost.com/hc/en-us/articles/219539467)
  * [Dynadot ↗](https://www.dynadot.com/help/question/set-DNSSEC)
  * [Enom ↗](https://support.enom.com/support/solutions/articles/201000065386)
  * [Gandi ↗](https://docs.gandi.net/en/domain_names/advanced_users/dnssec.html)
  * [GoDaddy ↗](https://www.godaddy.com/help/add-a-ds-record-23865)
  * [Hostinger ↗](https://www.hostinger.com/support/3667267-how-to-use-dnssec-records-at-hostinger/)
  * [Hover ↗](https://support.hover.com/support/solutions/articles/201000064716)
  * [Infomaniak ↗](https://faq.infomaniak.com/2187)
  * [InMotion Hosting ↗](https://www.inmotionhosting.com/support/edu/cpanel/enable-dnssec-cloudflare/)
  * [INWX ↗](https://kb.inwx.com/en-us/3-nameserver/131)
  * [Joker.com ↗](https://joker.com/faq/books/jokercom-faq-en/page/dnssec)
  * [Name.com ↗](https://www.name.com/support/articles/205439058-managing-dnssec)
  * [Namecheap ↗](https://www.namecheap.com/support/knowledgebase/article.aspx/9722/2232/managing-dnssec-for-domains-pointed-to-custom-dns/)
  * [NameISP ↗](https://support.nameisp.com/knowledgebase/dns)
  * [Namesilo ↗](https://www.namesilo.com/support/v2/articles/domain-manager/ds-records)
  * [Squarespace ↗](https://support.squarespace.com/hc/articles/4404183898125-Nameservers-and-DNSSEC-for-Squarespace-managed-domains#toc-dnssec)
  * [Registro.br ↗](https://registro.br/tecnologia/dnssec/?secao=tutoriais-dns)
  * [Porkbun ↗](https://kb.porkbun.com/article/93-how-to-install-dnssec) (do not fill out **keyData**)
  * [TransIP ↗](https://www.transip.eu/knowledgebase/150-secure-domains-custom-nameservers-dnssec/)


## Other DNSSEC setup options
If you are using Cloudflare as your Secondary DNS provider and want to configure DNSSEC on your secondary zone(s), you have [three options](https://developers.cloudflare.com/dns/zone-setups/zone-transfers/cloudflare-as-secondary/dnssec-for-secondary/) depending on your setup.
If you want to set up DNSSEC on a subdomain zone, refer to [Subdomain DNSSEC](https://developers.cloudflare.com/dns/zone-setups/subdomain-setup/dnssec/).
## Migrate to Cloudflare with DNSSEC active
If your current DNS provider supports adding external DNSKEY records, you can use the [active migration](https://developers.cloudflare.com/dns/dnssec/dnssec-active-migration/) path for zero-downtime DNSSEC migration using multi-signer DNSSEC.
If your current provider does not support this, use the following approach. This involves a brief window without DNSSEC protection.
  1. Remove the DS record at your registrar.
  2. Wait for the DS record TTL to fully expire at the parent zone. 
     * Verify with `dig DS example.com` — commonly 24–48 hours for most TLDs.
  3. Change your nameservers to Cloudflare.
  4. Wait for the previous NS record TTL to expire (typically one hour or less).
  5. [Enable DNSSEC in Cloudflare](https://developers.cloudflare.com/dns/dnssec/#enable-dnssec) and add the new DS record at your registrar.


## Roll back DNSSEC
If you need to disable DNSSEC after enabling it:
  1. Remove the DS record at your registrar (or disable DNSSEC if using Cloudflare Registrar).
  2. Keep zone signing enabled in Cloudflare until the DS TTL has fully expired at the parent zone.
  3. The rollback window depends on the DS TTL, which varies by TLD.


## Limitations
If your registrar does not support DNSSEC with Cloudflare's preferred cipher choice (Algorithm 13), you have several options:
  * Contact your registrar to ask for DNSSEC with modern encryption.
  * Transfer your domain to a different registrar that supports DNSSEC with Algorithm 13
  * File a [complaint with ICANN ↗](https://www.icann.org/compliance/complaint), citing your registrar's lack of compliance.


If your top-level domain does not support DNSSEC with Algorithm 13 (also known as _ECDSA Curve P-256 with SHA-256_), [contact that top-level domain ↗](https://www.iana.org/domains/root/db).
Was this helpful?
Yes
