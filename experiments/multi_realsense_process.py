# import sys
# sys.path.insert(0, '/home/yousof/robotics/libs/librealsense/install_host/python')

import pyrealsense2 as rs
import numpy as np 
import time 
from multiprocessing import Process
print(rs.__file__)


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

def T265(print_stuff):
    pipe = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.pose)
    pipe.start(config)

    for _ in range(50):
        frames = pipe.wait_for_frames()
        for  frame in frames:
            print_stuff(frame)
    

def D435i(print_stuff):
    pipe = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.accel)
    pipe.start(config)

    for _ in range(50):
        frames = pipe.wait_for_frames()
        for  frame in frames:
            print_stuff(frame)

ps = []
ps.append(Process(target=T265, args=(print_stuff,)))
ps.append(Process(target=D435i, args=(print_stuff,)))

[p.start() for p in ps]
[p.join() for p in ps]
[p.terminate() for p in ps]

