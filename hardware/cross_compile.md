# DISCLAIMER:
Only for my personal documentation. I see some un-stability. 
I do not take any responsibility regarding this repo. 
Use it at your own risk if you want.

# Sources:
* https://github.com/zhj-buffer/Cross-Compile-Jetson
* https://www.plop.at/en/ploplinux/arm/crossbuildchroot.html

# How to cross compile for Jetson Nano

Find the compressed `Jetson Nano Developer Kit SD Card Image`.
Download and un-compress it.
You can download it from `Jetson Download Center`.
For example the latest one is `JP 4.4.1` at the time of writing
this document.

```bash
export WS=~/my/cross/compile/workspace
# for me I am choosing it as 
export WS=/home/yousof/robotics/jetson/cross_compile
```

**START of one-time only for each new jetson Linux image**

### Get the file System from the iso file:
```bash
$ fdisk sd-blob-b01.img 

Welcome to fdisk (util-linux 2.31.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): p
Disk sd-blob-b01.img: 13.4 GiB, 14400094208 bytes, 28125184 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: C066C102-48BC-423D-8133-E2F90E371708

Device            Start      End  Sectors  Size Type
sd-blob-b01.img1  28672 28121087 28092416 13.4G Linux filesystem
sd-blob-b01.img2   2048     2303      256  128K Linux filesystem
sd-blob-b01.img3   4096     4991      896  448K Linux filesystem
sd-blob-b01.img4   6144     7295     1152  576K Linux filesystem
sd-blob-b01.img5   8192     8319      128   64K Linux filesystem
sd-blob-b01.img6  10240    10623      384  192K Linux filesystem
sd-blob-b01.img7  12288    13055      768  384K Linux filesystem
sd-blob-b01.img8  14336    14463      128   64K Linux filesystem
sd-blob-b01.img9  16384    17279      896  448K Linux filesystem
sd-blob-b01.img10 18432    19327      896  448K Linux filesystem
sd-blob-b01.img11 20480    22015     1536  768K Linux filesystem
sd-blob-b01.img12 22528    22655      128   64K Linux filesystem
sd-blob-b01.img13 24576    24735      160   80K Linux filesystem
sd-blob-b01.img14 26624    26879      256  128K Linux filesystem

Partition table entries are not in disk order.

```

the start of first partition is `28672`. We need `28672*512 = 14680064` number
in the following command. Exit the previous command.
```bash
mkdir temp_root
sudo mount -o loop,offset=14680064 sd-blob-b01.img temp_root
```

It is recommended to copy the content to some folder to avoid changing the image itself and
also not being limited by 12GB of size in that root after `chroot`
```bash
sudo mkdir -p $WS/rootfs
sudo cp temp_root/*  $WS/rootfs -rapvf

# un-mount and remove the temp dir
sudo umount temp_root && rm -rf temp_root
```


```bash
export REPO=$(pwd)
export WS=/home/yousof/robotics/jetson/cross_compile
cp $REPO/ch-mount.sh $WS

sudo su - root
export WS=/home/yousof/robotics/jetson/cross_compile
cd $WS/rootfs

apt install qemu-user-static
cp /usr/bin/qemu-arm-static usr/bin/
rm /etc/resolv.conf && cp /etc/resolv.conf etc/
cp ../ch-mount.sh .
```

**END of one-time only**

Now to enter the cross compile environment
```bash
sudo su - root
export WS=/home/yousof/robotics/jetson/cross_compile

cd $WS/rootfs
bash ch-mount.sh -m .
```

You now can check with `uname -m` if everything worked which should
show `aarch64` instead of `x86_64` in the host.

# Example

I would like to cross compile the Intel RealSense Lib for Jetson nano. 
For that Please read the [`realsense.md`](https://github.com/yosoufe/SelfStudyRobotics/blob/master/hardware/realsense.md) file after doing the above preparation.