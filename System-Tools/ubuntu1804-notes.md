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

## Package Management

- Add a ppa: `sudo add-apt-repository ppa:whatever/ppa`

- Remove a ppa: `sudo add-apt-repository --remove ppa:whatever/ppa`

- Install or upgrade a package `sudo apt install <package-name>`

- Update all packages information: `sudo apt update`

- Upgrade all packages `sudo apt upgrade`

- Find an installed package `dpkg -l <package-name-w/o-wild-card>`

- Uninstall an package but keep all configuration file `sudo apt remove <package-name>`

- Uninstall an package and delete all configuration file `sudo apt purge <package-name>`

- Clean dependencies `sudo apt autoremove`

## Mouse Sensitivity Setup

1. Find the mouse device by listing all usb devices: `xinput list`. 

2. List properties of the device: `xinput list-props <device-index>`. The device should have two properties: `Coordinate Transformation Matrix` and `Accel Speed`.

3. Increase the `Accel Speed` up to 1: `xinput set-prop '<device-name>'(or device index) 'Accel Speed'(or property index) 1`.

4. If the mouse speed is still too slow, update the `Coordinate Transformation Matrix`: `xinput set-prop '<device-name>'(or device index) 'Coordinate Transformation Matrix'(or property index) 1.5 0 0 0 1.5 0 0 0 1`. Try different x and y coordinates (position with value 1.5).

5. Discussion and references:

    - https://unix.stackexchange.com/questions/90572/how-can-i-set-mouse-sensitivity-not-just-mouse-acceleration

    - https://wiki.ubuntu.com/X/InputCoordinateTransformation

## Boot order

1. Remember the index of images, e.g. Ubuntu: 0, Windows 2.
2. Open the default grub setting: `sudo vim /etc/default/grub`
3. Update the `GRUB_DEFAULT=0` to the index you want (e.g. 2 for Windows)
4. `sudo update-grub`