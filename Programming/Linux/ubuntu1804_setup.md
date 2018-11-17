# Setup after installment of Ubuntu 18.04

## Wireless Driver

1. Connect to internet with Ethernet cable

2. Follow the instruction on [this page](https://askubuntu.com/questions/1067513/ubuntu-18-04-1-and-tp-link-archer-t4ueu-v2-0-nightmare-rtl8812au-chipset):

```shell
cd /tmp
git clone https://github.com/gnab/rtl8812au.git gnab_rtl8812au
cd gnab_rtl8812au
make
sudo insmod 8812au.ko
```