---
url: "https://ubuntu.com/tutorials/create-a-usb-stick-on-windows"
title: "Create a bootable USB stick with Rufus on Windows\n    | Ubuntu"
scraped_at: 2026-09-09T15:15:02+00:00
---

[Skip to main content](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#main-content)
Your submission was sent successfully! [_Close_](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)
Thank you for contacting us. A member of our team will be in touch shortly. [_Close_](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)
You have successfully unsubscribed! [_Close_](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)
Thank you for signing up for our newsletter! In these regular emails you will find the latest updates about Ubuntu and upcoming events where you can meet our team.[_Close_](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)
Your preferences have been successfully updated. [_Close notification_](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)
Please try again or [file a bug report.](https://github.com/canonical/ubuntu.com/issues/new?template=ISSUE_TEMPLATE.yaml) [_Close_](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)
  * [ Canonical ](https://canonical.com/)
Get to know Canonical, the company behind the products.
  * [ Ubuntu ](https://ubuntu.com/)
The world's favorite Linux OS for servers, desktops and IoT.
  * [ Ubuntu Pro ](https://ubuntu.com/pro)
One subscription for security maintenance, support, FIPS and other compliance certifications.
  * [ Snapcraft ](https://snapcraft.io/)
The app store for Linux: secure packages and ultra-reliable updates.
  * A pure-container hypervisor. Run system containers and VMs at scale.
  * Build a bare metal cloud with super fast server provisioning.
  * [ OpenStack ](https://ubuntu.com/openstack)
Upgrades, maintenance, support, and fully managed options for long-term, low-cost infra.
  * Software-defined storage that lowers your total cost of ownership.
  * [ Kubernetes ](https://ubuntu.com/kubernetes)
App portability for K8s on VMware, Amazon, Azure, Google, Oracle, IBM and bare metal.
  * Deploy, integrate and manage applications at any scale, on any infrastructure.


Join Canonical
Be part of the team that builds the products.
Also from Canonical
* Stream Android applications to any device.
* The software collaboration platform behind Ubuntu.
* Optimized Ubuntu for public clouds.
* Spin up Ubuntu VMs on Windows, Mac and Linux.
* Control and customize your cloud instances.
* Systems management and security patching for Ubuntu.
* Simplify and standardize complex network configuration.
* AI and MLOps at any scale, on any cloud.
* Deploy a fully functional cloud in minutes.
About


[ Tutorials ](https://ubuntu.com/tutorials)
# Create a bootable USB stick with Rufus on Windows
## 1. Overview
**New version available** This tutorial has been rewritten and replaced by the [Create a bootable USB stick](https://documentation.ubuntu.com/desktop/en/latest/how-to/create-a-bootable-usb-stick/) guide.
With a bootable Ubuntu USB stick, you can:
  * Install or upgrade Ubuntu
  * Test out the Ubuntu desktop experience without touching your PC configuration
  * Boot into Ubuntu on a borrowed machine or from an internet cafe
  * Use tools installed by default on the USB stick to repair or fix a broken configuration


This tutorial will show you how to create a bootable USB stick on Microsoft Windows using [Rufus](https://rufus.ie/).
For most users we recommend [balenaEtcher](https://www.balena.io/etcher/) instead of Rufus which is simpler to use and also available on MacOS and Ubuntu. Instructions are now included in the primary [Install Ubuntu Desktop](https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview) tutorial.
Creating a bootable Ubuntu USB stick from Microsoft Windows is very simple and we’re going to cover the process in the next few steps.
Alternatively, we also have tutorials to help you create a bootable USB stick from both [Ubuntu](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-ubuntu) and [Apple macOS](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-macos).
## 2. Requirements
You will need:
  * A 4GB or larger USB stick/flash drive
  * Microsoft Windows XP or later
  * [Rufus](https://rufus.ie/), a free and open source USB stick writing tool
  * An Ubuntu ISO file. See [Get Ubuntu](https://www.ubuntu.com/download) for download links


Take note of where your browser saves downloads: this is normally a directory called ‘Downloads’ on your Windows PC. Don’t download the ISO image directly to the USB stick! If using Windows XP or Vista, download version 2.18 of Rufus.
## 3. USB selection
Perform the following to configure your USB device in Rufus:
  1. Launch Rufus
  2. Insert your USB stick
  3. Rufus will update to set the device within the **Device** field
  4. If the **Device** selected is incorrect (perhaps you have multiple USB storage devices), select the correct one from the device field’s drop-down menu


You can avoid the hassle of selecting from a list of USB devices by ensuring no other devices are connected.
## 4. Select the Ubuntu ISO file
To select the Ubuntu ISO file you downloaded previously, click the **SELECT** to the right of “Boot selection”. If this is the only ISO file present in the Downloads folder you will only see one file listed.
Select the appropriate ISO file and click on **Open**.
## 5. Write the ISO
The _Volume label_ will be updated to reflect the ISO selected.
Leave all other parameters with their default values and click **START** to initiate the write process.
## 6. Additional downloads
You may be alerted that Rufus requires additional files to complete writing the ISO. If this dialog box appears, select **Yes** to continue.
## 7. Write warnings
You will then be alerted that Rufus has detected that the Ubuntu ISO is an _ISOHybrid image_. This means the same image file can be used as the source for both a DVD and a USB stick without requiring conversion.
Keep _Write in ISO Image mode_ selected and click on **OK** to continue.
Rufus will also warn you that all data on your selected USB device is about to be destroyed. This is a good moment to double check you’ve selected the correct device before clicking **OK** when you’re confident you have.
If your USB stick contains multiple partitions Rufus will warn you in a separate pane that these will also be destroyed.
## 8. Writing the ISO
The ISO will now be written to your USB stick, and the progress bar in Rufus will give you some indication of where you are in the process. With a reasonably modern machine, this should take around 10 minutes. Total elapsed time is shown in the lower right corner of the Rufus window.
## 9. Installation complete
When Rufus has finished writing the USB device, the Status bar will be filled green and the word **READY** will appear in the center. Select **CLOSE** to complete the write process.
Congratulations! You now have Ubuntu on a USB stick, bootable and ready to go.
To use it you need to insert the stick into your target PC or laptop and reboot the device. It should recognise the installation media automatically during startup but you may need to hold down a specific key (usually F12) to bring up the boot menu and choose to boot from USB.
For a full walkthrough of installing Ubuntu, take a look at our [install Ubuntu desktop tutorial](https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview).
### [Finding help](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#p-39396-finding-help)
If you get stuck, help is always at hand:
  * [Ubuntu Discourse](https://discourse.ubuntu.com/)
  * [IRC-based support](https://wiki.ubuntu.com/IRC/ChannelList)


Was this tutorial useful?
Thank you for your feedback.
© 2026 Canonical Ltd.
Ubuntu and Canonical are registered trademarks of Canonical Ltd.
We use cookies and similar methods to recognize visitors and remember preferences. We also use them to measure campaign effectiveness and analyze traffic on our websites. By selecting ‘Accept‘, you consent to the use of these methods by us and trusted third parties. For further details or to change your consent choices at any time see our [cookie policy](https://canonical.com/legal/data-privacy?cp=hide#cookies).
Manage your tracker settings Accept all
