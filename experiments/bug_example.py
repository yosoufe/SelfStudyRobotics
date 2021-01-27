import sys
sys.path.insert(0, '/home/yousof/robotics/libs/librealsense/build_host/wrappers/python')

import pyrealsense2 as rs
import numpy as np 
import time 
print(rs.__file__)

import atexit

pipelines = []

@atexit.register
def cleanup():
    print('clean up')
    for p in pipelines:
        try:
            p.stop()
        except:
            pass

def print_stuff(frame):
    print(f'stream name: {frame.profile.stream_name()},\ttime: {frame.timestamp}')
    if frame.is_depth_frame():
        print ('depth frame')
    if frame.is_motion_frame():
        print('motion frame')
    if frame.is_pose_frame():
        print('pose_frame')
    if frame.is_points():
        print('is_points')
    if frame.is_pose_frame():
        print('is_pose_frame')
    if frame.is_video_frame():
        print('is_video_frame')


ctx = rs.context()

for dev in ctx.query_devices():
    print(f'device: {dev.get_info(rs.camera_info.name)}')
    p = rs.pipeline(ctx) 
    cfg = rs.config()
    dev_serial = dev.get_info(rs.camera_info.serial_number)
    del dev ## <<<<------------------------------------ This line is my workaround
    cfg.enable_device(dev_serial)
    p.start(cfg, print_stuff) 
    pipelines.append(p)

print('pipelines started')
s = time.time()
time.sleep(1)