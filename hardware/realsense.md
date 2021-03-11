# Intel RealSense
* Getting Started: https://www.intelrealsense.com/get-started/

### Installations

source: https://github.com/IntelRealSense/librealsense/blob/development/doc/distribution_linux.md

```
sudo apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
sudo add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo bionic main" -u

sudo apt-get install librealsense2-dkms
sudo apt-get install librealsense2-utils librealsense2-dev librealsense2-dbg

# With dev package installed, you can compile an application with librealsense using g++ -std=c++11 filename.cpp -lrealsense2 or an IDE of your choice.
```

### Applications

#### Depth Camera D435i
https://www.intelrealsense.com/get-started-depth-camera/
```
realsense-viewer
```

#### Tracking Camera T265
https://www.intelrealsense.com/get-started-tracking-camera/
```
rs-capture # 2D Visualization.
rs-enumerate-devices # list the IMU and tracking profiles (FPS rates and formats).
rs-data-collect # Store and serialize IMU and Tracking (pose) data in Excel-friendly csv format. The tool uses low-level sensor API to minimize software-imposed latencies. Useful for performance profiling.
realsense-viewer # Provides 2D visualization of IMU and Tracking data. 3D visualization is available for Pose samples:
```


## DataSheets

* [D400 Family](https://www.intel.com/content/dam/support/us/en/documents/emerging-technologies/intel-realsense-technology/Intel-RealSense-D400-Series-Datasheet.pdf)

* [Tracking Camera](https://www.intelrealsense.com/wp-content/uploads/2019/09/Intel_RealSense_Tracking_Camera_Datasheet_Rev004_release.pdf?_ga=2.175132068.786282.1590023533-1409498473.1589762811)

## CAD Files:
Intel: https://dev.intelrealsense.com/docs/cad-files

Nvidia Jetson: https://developer.nvidia.com/embedded/downloads

Intel Real Sense Camera Mount: 
* https://www.prusaprinters.org/prints/32199-intel-real-sense-mount-d435i-and-t265
* Fusion 360: https://a360.co/36ryEeb


# Compile for Jetson Nano
https://github.com/yosoufe/instructions/blob/main/realsense/realsense.md