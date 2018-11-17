# Setup after installment of Ubuntu 18.04

## Wireless driver for "TP-Link Archer T4U V2" adapter

1. Connect to internet with Ethernet cable

2. Follow the instruction on [this page](https://askubuntu.com/questions/1067513/ubuntu-18-04-1-and-tp-link-archer-t4ueu-v2-0-nightmare-rtl8812au-chipset):

```shell
cd /tmp
git clone https://github.com/gnab/rtl8812au.git gnab_rtl8812au
cd gnab_rtl8812au
make
sudo insmod 8812au.ko
```

## Generate SSH keys and upload to github

1. Generate ssh key

```shell
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

2. Add to Github account `profile icon -> settings -> SSH and GPG keys -> New SSH key`.

## Install Nvidia graphic driver

1. Check graphic card model: `ubuntu-drivers devices`

2. Install the driver: `sudo ubuntu-drivers autoinstall`

3. Reboot