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

To add it to any new kernels installed by Ubuntu, configure it via DKMS as follows:

```shell
cd /tmp
sudo cp -R gnab_rtl8812au /usr/src/8812au-4.2.2
sudo dkms add -m 8812au -v 4.2.2
sudo dkms build -m 8812au -v 4.2.2
sudo dkms install -m 8812au -v 4.2.2
```

## Generate SSH keys and upload to github

1. Generate ssh key

```shell
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

## Install Nvidia graphic driver

1. Check graphic card model: `ubuntu-drivers devices`

2. Install the driver: `sudo ubuntu-drivers autoinstall`

3. Reboot

## Alternative way to install Nvidia driver

```shell
sudo add-apt-repository ppa:graphics-drivers/ppa 
sudo apt-get update 
sudo apt-get install nvidia-390
sudo add-apt-repository --remove ppa:graphics-drivers/ppa
```

## Install Sogou input

From [this blog](https://www.jianshu.com/p/c936a8a2180e)

1. Run the shell script

```shell
sudo apt-get remove ibus # 卸载ibus
sudo apt-get purge ibus # 清除ibus配置。
sudo  apt-get remove indicator-keyboard # 卸载顶部面板任务栏上的键盘指示。
sudo apt install fcitx-table-wbpy fcitx-config-gtk #安装fcitx输入法框架
im-config -n fcitx # 切换为 Fcitx输入法
sudo shutdown -r now # im-config 配置需要重启系统才能生效
# 下载搜狗输入法
wget http://cdn2.ime.sogou.com/dl/index/1524572264/sogoupinyin_2.2.0.0108_amd64.deb?st=ryCwKkvb-0zXvtBlhw5q4Q&e=1529739124&fn=sogoupinyin_2.2.0.0108_amd64.deb
sudo dpkg -i sogoupinyin_2.2.0.0108_amd64.deb # 安装搜狗输入法
sudo apt-get install -f # 修复损坏缺少的包
fcitx-config-gtk3 # 打开 Fcitx 输入法配置
```
2. 问题:输入法皮肤透明

`fcitx设置 >>附加组件>>勾选高级 >>取消经典界面`

`Configure>>  Addon  >>Advanced>>Classic`
