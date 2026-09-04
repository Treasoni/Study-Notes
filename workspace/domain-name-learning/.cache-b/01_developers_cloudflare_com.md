---
url: "https://developers.cloudflare.com/registrar/get-started/transfer-domain-to-cloudflare/"
title: "Transfer your domain to Cloudflare · Cloudflare Registrar docs"
scraped_at: 2026-09-04T04:45:07+00:00
---

[Skip to content](https://developers.cloudflare.com/registrar/get-started/transfer-domain-to-cloudflare/#main-content)
> Documentation IndexFetch the complete documentation index at: https://developers.cloudflare.com/registrar/llms.txtUse this file to discover all available pages before exploring further.
# Transfer your domain to Cloudflare
Last updated Apr 24, 2026|Copy as Markdown|[View as Markdown](https://developers.cloudflare.com/registrar/get-started/transfer-domain-to-cloudflare/index.md)|[Agent setup](https://developers.cloudflare.com/agent-setup/)
Transferring a domain moves your registration from your current registrar to Cloudflare.
  * **Active work:** About 30 minutes.
  * **Total time:** Up to 10 days, depending on your registrar.
  * **Cost:** Cloudflare domains are at-cost with no markup fees. Most transfers include a one-year extension from your current expiration date. Some country-code domains (such as `.uk`) have no transfer fee.


Before you begin
Confirm the following before you start:
  * You have a [Cloudflare account](https://developers.cloudflare.com/fundamentals/account/create-account/) with a [verified email address](https://developers.cloudflare.com/fundamentals/user-profiles/verify-email-address/).
  * Your Cloudflare account has a valid payment method on file.
  * Your domain was registered at least 60 days ago and has not been transferred in the last 60 days (ICANN requirement).
  * You have not changed your registrant name, organization, or email address in the last 60 days. Under ICANN rules, changes to these fields trigger a 60-day transfer lock. Some registrars let you opt out of this lock during the change, but not all do.
  * Your account at your current registrar is active. If your domain has expired, renew it at your current registrar first.
  * Your domain uses only standard characters (letters, numbers, hyphens). Cloudflare does not support domains with non-Latin characters (for example, `例え.jp`).
  * If you are transferring a `.us` domain, refer to [Additional requirements for .US domains](https://developers.cloudflare.com/registrar/top-level-domains/us-domains/).
  * If you are transferring multiple domains, notify your bank to prevent fraud alerts on multiple charges.
  * Cloudflare Registrar requires your domain to use Cloudflare for [authoritative DNS](https://developers.cloudflare.com/dns/zone-setups/full-setup/) (full setup). You cannot use another DNS provider while registered with Cloudflare.


## 1. Add your domain to Cloudflare
Before you can transfer your registration, your domain must be [active on Cloudflare](https://developers.cloudflare.com/dns/zone-setups/full-setup/). This is what allows Cloudflare to protect your site with performance and security features during and after the transfer. You will not be able to enter an authorization code or proceed with the transfer until this step is complete.
### Disable DNSSEC
If DNSSEC is enabled at your current registrar, disable it before you change nameservers. DNSSEC validates DNS responses using cryptographic signatures tied to your current provider. When you point nameservers to Cloudflare, those signatures will no longer match, which causes DNS resolution failures and can prevent your domain from becoming active.
**At your current registrar:**
  1. Check your domain settings for DNSSEC or DS records. If there are none, DNSSEC is not active and you can skip to [Add your domain](https://developers.cloudflare.com/registrar/get-started/transfer-domain-to-cloudflare/#add-your-domain-and-update-your-nameservers).
  2. Remove or disable DNSSEC (sometimes labeled "DS records").
  3. Wait at least 24 hours for the change to propagate before changing nameservers.


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


After your transfer completes, you can re-enable DNSSEC through Cloudflare with one click. Refer to [Enable DNSSEC](https://developers.cloudflare.com/dns/dnssec/#1-activate-dnssec-in-cloudflare).
### Add your domain and update your nameservers
Follow the steps in [Set up Cloudflare DNS](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/) to add your domain, review your DNS records, and get your assigned nameservers. Then [update the nameservers](https://developers.cloudflare.com/dns/nameservers/update-nameservers/) at your current registrar to the ones Cloudflare assigned.
Nameserver instructions for popular registrars
Each registrar has a different interface for updating nameservers. These links explain the process at popular registrars:
  * [Enom ↗](https://support.enom.com/support/solutions/articles/201000065324-preparing-your-domain-for-transfer)
  * [GoDaddy ↗](https://www.godaddy.com/help/transfer-my-domain-away-from-godaddy-3560)
  * [Ionos by 1&1 ↗](https://www.ionos.com/help/domains/domain-transfers/#acc4514)
  * [Namecheap ↗](https://www.namecheap.com/support/knowledgebase/article.aspx/258/84/what-should-i-do-to-transfer-a-domain-from-namecheap/)
  * [Network Solutions ↗](https://www.networksolutions.com/help/article/transfer-out-of-network-solutions)
  * [Squarespace ↗](https://support.squarespace.com/hc/articles/205812338-Transferring-a-domain-away-from-Squarespace)


### Wait for your domain to become active
**In the Cloudflare dashboard:**
Wait for your domain status to change from **Pending** to **Active**. This usually takes a few minutes but can take up to 24 hours.
If your zone has been pending for more than 24 hours, verify that you updated the nameservers correctly at your current registrar and that DNSSEC is disabled.
## 2. Transfer your registration
Once your domain is active on Cloudflare, you can transfer the registration. This moves your domain record from your current registrar to Cloudflare. You will go back and forth between your current registrar and Cloudflare during this process.
### Unlock your domain
**At your current registrar:**
Remove the lock on your domain so Cloudflare can process the transfer. Most registrars apply a lock by default (sometimes called registrar lock, domain lock, or transfer lock) to prevent unauthorized transfers. In WHOIS, this appears as `clientTransferProhibited`.
### Request an authorization code
**At your current registrar:**
Request an authorization code for your domain. This is also called an auth code, EPP code, authinfo code, or transfer code. Cloudflare uses this code to verify that the transfer is authorized by the domain owner.
Authorization codes are usually only valid for a limited period. Request the code when you are ready to enter it in the next step.
### Enter your authorization code and confirm payment
**In the Cloudflare dashboard:**
[Go to **Transfer domains** ↗](https://dash.cloudflare.com/?to=/:account/registrar/transfer)
Select your domain and enter the authorization code. For most generic TLDs (such as `.com`, `.net`, and `.org`), the transfer price includes a one-year registration extension from your current expiration date. This is an ICANN requirement for gTLD transfers. Country-code domains follow their own registry policies — for example, `.uk` transfers do not add an extra year or charge a transfer fee.
If you do not have a payment method on file, add one before proceeding.
For information about registration limits and the one-year extension, refer to [Transfer rejected due to registration limits](https://developers.cloudflare.com/registrar/troubleshooting/#transfer-rejected-due-to-registration-limits).
### Confirm your contact information
**In the Cloudflare dashboard:**
Enter the contact information for your registration. Cloudflare Registrar redacts this information from public WHOIS by default, but ICANN requires Cloudflare to collect accurate contact details. Providing inaccurate information may result in domain suspension.
You can [modify your contact information](https://developers.cloudflare.com/registrar/account-options/domain-contact-updates/) later.
After entering the contact information, agree to the domain registration terms of service by selecting **Confirm transfer**.
### Approve the transfer at your current registrar
After you submit the transfer, Cloudflare will begin processing it and send a Form of Authorization (FOA) email to the registrant if the information is available in the public WHOIS database.
Your current registrar will email you confirming the transfer or asking for your approval. Afterwards, most registrars process it within 5 business days (but some TLDs, such as `.mx`, can take up to 10 business days).
## Transfer from Shopify, Block, or Wix
Some commerce and site-building platforms (such as Shopify, Block, and Wix) act as both your hosting provider and domain registrar. These platforms typically do not allow you to change nameservers while the domain is registered with them. Because Cloudflare requires your nameservers to point to Cloudflare before a transfer can begin, a direct transfer is not possible.
The workaround is to transfer your domain to another registrar first, wait 60 days, then transfer to Cloudflare:
  1. **Get your authorization code from your current platform.** Each platform has a different process. Refer to your platform documentation for instructions on transferring your domain away.
  2. **Transfer to another registrar** that allows nameserver changes. Enter the authorization code there and complete the transfer. This usually takes 3-5 days.
  3. **Update nameservers to Cloudflare.** Once the domain is at the new registrar, update the nameservers to Cloudflare. You can use all Cloudflare features (CDN, DNS, security) immediately after this step.
  4. **Transfer to Cloudflare Registrar after 60 days.** ICANN requires a 60-day wait between transfers. After that period, initiate the transfer to Cloudflare from the [Transfer Domains](https://developers.cloudflare.com/registrar/get-started/transfer-domain-to-cloudflare/#enter-your-authorization-code-and-confirm-payment) page.


## Transfer statuses
You can check the status of your transfer on the **Transfer Domains** page in the dashboard.
  * **Transfer in progress** : Cloudflare has submitted the request to your current registrar. If this status persists for more than 24 hours, verify that you have unlocked the domain at your current registrar.
  * **Pending approval** : Your current registrar has received the transfer request and can take up to five days to release the domain. To speed this up, approve the transfer through the email or dashboard of your current registrar.
  * **Transfer rejected** : The transfer was rejected by your current registrar. This can happen if you declined the transfer request, or if the registrar determined the domain is not eligible. Select **Retry** to start a new transfer request.


## Bulk domain transfers
The process for transferring domains in bulk is the same as transferring a single domain. Each domain is charged individually.
## Common transfer issues
Here are suggestions for how to handle common transfer issues:
  * [Domain is still locked](https://developers.cloudflare.com/registrar/troubleshooting/#domain-is-still-locked)
  * [Authorization code is invalid or expired](https://developers.cloudflare.com/registrar/troubleshooting/#authorization-code-is-invalid-or-expired)
  * [Cannot find where to enter your authorization code](https://developers.cloudflare.com/registrar/troubleshooting/#cannot-find-where-to-enter-your-authorization-code)
  * [Transfer is taking too long](https://developers.cloudflare.com/registrar/troubleshooting/#transfer-is-taking-too-long)
  * [Payment failed during transfer](https://developers.cloudflare.com/registrar/troubleshooting/#payment-failed-during-transfer)


For a full list of issues, refer to [Troubleshoot failed domain transfers](https://developers.cloudflare.com/registrar/troubleshooting/).
## Next steps
As mentioned in [Review DNS records in Cloudflare](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/#2-review-your-dns-records), when moving your domain to Cloudflare Registrar, you might need to configure your DNS records to correctly point traffic to your web host. Cloudflare automatically scans for common records and adds them to your account's DNS page, but the scan is not guaranteed to find all existing DNS records.
Refer to your web host's documentation to learn what type of records you need to configure and where they should point, to avoid downtime.
Example
For example, Netlify asks customers that host websites with them to add a `CNAME` record pointing `<YOUR-DOMAIN>` to `apex-loadbalancer.netlify.com`, and another `CNAME` record pointing `www` to `<YOUR-DOMAIN>.netlify.app`, depending on which one is the primary domain.
You may also want to [enable DNSSEC](https://developers.cloudflare.com/dns/dnssec/#1-activate-dnssec-in-cloudflare).
Was this helpful?
Yes
