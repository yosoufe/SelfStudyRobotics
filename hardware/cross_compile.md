# DISCLAIMER:
Only for my personal documentation. I see some un-stability. 
I do not take any responsibility regarding this repo. 
Use it at your own risk if you want.

# Sources:
* https://github.com/zhj-buffer/Cross-Compile-Jetson
* https://www.plop.at/en/ploplinux/arm/crossbuildchroot.html

# How to cross compile for Jetson Nanoe

Find the Jetpack compressed filesystem. I am
using `sdkmanager` and download them in `~/nvidia/nvidia_sdk/`.
For example current version is called `JetPack_4.4.1_Linux_JETSON_NANO_DEVKIT`.

```
export WS=~/my/cross/compile/workspace
# for me I am choosing it as 
export WS=/home/yousof/robotics/jetson/cross_compile
```

**START of one-time only for each new jetson Linux image**
```
sudo su - root
export WS=/home/yousof/robotics/jetson/cross_compile
export JETSON_FOLDER=JetPack_4.4.1_Linux_JETSON_NANO_DEVKIT
export REPO=$(pwd)
cd $WS
cp $REPO/ch-mount.sh $WS
cp -r /home/yousof/nvidia/nvidia_sdk/$JETSON_FOLDER/Linux_for_Tegra/rootfs $WS
cd $WS/rootfs

apt install qemu-user-static
cp /usr/bin/qemu-arm-static usr/bin/
cp /etc/resolv.conf etc/
cp ch-mount.sh rootfs/
```

**END of one-time only**

Now to enter the cross compile environment
```
sudo su - root
export WS=/home/yousof/robotics/jetson/cross_compile

cd $WS/rootfs
bash ch-mount.sh -m ./
```
