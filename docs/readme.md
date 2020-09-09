* [The Multivariate Gaussian](https://people.eecs.berkeley.edu/~jordan/courses/260-spring10/other-readings/chapter13.pdf)
* [Mobile Sensing And Robotics 2 (MSR2) 2020 Lecture Videos and Slides](https://www.ipb.uni-bonn.de/msr2-2020-2/)



# Cross compile

Source: https://github.com/zhj-buffer/Cross-Compile-Jetson


download sd card image and extract

### one time only
```sh
cd nv-jetson-nano-sd-card-image-r32.3.1
sudo su - root
cd /home/yousof/robotics/donkeyCarJetson/softwareImages/cross_compile/nv-jetson-nano-sd-card-image-r32.3.1
mkdir -p rootfs-nano
fdisk sd-blob-b01.img
```
```sh
Command (m for help): p
Disk sd-blob-b01.img: 12 GiB, 12884901888 bytes, 25165824 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 43CAB209-E630-440C-8D77-5A7C6BD76C49

Device            Start      End  Sectors  Size Type
sd-blob-b01.img1  28672 25165790 25137119   12G Linux filesystem
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

```

rootfs strats from 28672 with block size 512bytes. So We need to mount 
the image from offset 28672 * 512 = 14680064

```.sh
mount -o loop,offset=14680064 sd-blob-b01.img /mnt
ls /mnt
cp /mnt/* /home/yousof/robotics/donkeyCarJetson/softwareImages/cross_compile/nv-jetson-nano-sd-card-image-r32.3.1/rootfs-nano/ -rapvf
apt install qemu-user-static
git clone https://github.com/zhj-buffer/Cross-Compile-Jetson.git
cp 
apt install qemu-user-static
cp /usr/bin/qemu-arm-static rootfs-nano/usr/bin/
cp /usr/bin/qemu-aarch64-static rootfs-nano/usr/bin/
cp Cross-Compile-Jetson/ch-mount.sh .
cp /etc/resolv.conf rootfs-nano/etc/
```

### end of one time only

```
sudo su - root
cd /home/yousof/robotics/donkeyCarJetson/softwareImages/cross_compile/nv-jetson-nano-sd-card-image-r32.3.1/rootfs-nano
bash ch-mount.sh -m .
apt update && apt -y upgrade
```