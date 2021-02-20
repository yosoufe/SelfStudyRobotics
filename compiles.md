# Python env
Install pyenv: https://github.com/pyenv/pyenv
then

```
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install -v 3.8.5
```

# install Pangolin

https://github.com/stevenlovegrove/Pangolin#required-dependencies

```
sudo apt install install libgl1-mesa-dev \
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
```