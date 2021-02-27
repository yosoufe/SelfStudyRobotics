# Requirements

## Python env
Install pyenv: https://github.com/pyenv/pyenv
then

```bash
env PYTHON_CONFIGURE_OPTS="--enable-shared --enable-optimizations --enable-ipv6 --with-lto" pyenv install 3.8.5
```

## Install realsense
follow the realsense guidelines. I have documented how I compiled it in `hardware/realsense.md`.

## install Pangolin

https://github.com/stevenlovegrove/Pangolin#required-dependencies

```bash
sudo apt install libgl1-mesa-dev \
    libglew-dev \
    cmake \
    libpython3.8-dev \
    ffmpeg libavcodec-dev libavutil-dev libavformat-dev libswscale-dev libavdevice-dev \
    libdc1394-22-dev libraw1394-dev \
    libjpeg-dev libpng++-dev libtiff5-dev libopenexr-dev

git clone https://github.com/stevenlovegrove/Pangolin.git
cd Pangolin
git submodule init && git submodule update
mkdir build && cd build-
cmake -DCMAKE_BUILD_TYPE=Debug .. -DPYTHON_EXECUTABLE=$(python3 -c "import sys; print(sys.executable)") -DCMAKE_INSTALL_PREFIX=install
make -j`nproc` install

echo -e "\n\nexport PYTHONPATH=\$PYTHONPATH:`realpath src`" >> ~/.bashrc

# for jetson you would need the following as well
export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1
# or 
echo -e "\nexport LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1" >> ~/.bashrc
source ~/.bashrc
```

## Other stuff
```bash
# --no-binary numpy for jetson not x86
python3 -m pip install -U numpy --no-cache-dir --no-binary numpy
python -m pip install transformations\
    wheel \
    matplotlib\
    PyOpenGL
```

# Increase performance on jetson
```bash
sudo iwconfig wlan0 power off # turn of the wifi's power management
sudo jetson_clocks # max up the clock speed
sudo sh -c 'echo 255 > /sys/devices/pwm-fan/target_pwm' # turn on the fan
```

## VNC on Jetson
- https://medium.com/@bharathsudharsan023/jetson-nano-remote-vnc-access-d1e71c82492b
- https://developer.nvidia.com/embedded/learn/tutorials/vnc-setup