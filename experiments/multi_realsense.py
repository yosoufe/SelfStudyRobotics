# let's try this tutorial in python
# https://dev.intelrealsense.com/docs/rs-multicam
# import sys
# sys.path.insert(0, '/home/yousof/robotics/libs/librealsense/build_host/wrappers/python')

import pyrealsense2 as rs
import numpy as np 
import time 
import transformations
import math
import traceback, sys
from plot3d import *
from threading import Lock, Event

lock = Lock()

print(rs.__file__)

import atexit

pipelines = []
ctx = rs.context()
pc = rs.pointcloud()
pl = FramePlotter(live = True)
rotation_matrices = np.array([], dtype = np.float).reshape(0,4,4)
new_frame = Event()

def save_array(array):
    with open('rotation_matrices.npy', 'wb') as f:
        np.save(array)

@atexit.register
def cleanup():
    print('clean up')
    save_array(rotation_matrices)
    for p in pipelines:
        try:
            p.stop()
        except:
            pass


def process_t265(frame):
    try:
        global rotation_matrices, new_frame
        if frame.is_pose_frame():
            pose_frame = frame.as_pose_frame()
            pose_data = pose_frame.pose_data
            q = pose_data.rotation
            t = pose_data.translation
            q = [q.w, q.x, q.y , q.z]
            eu = transformations.euler_from_quaternion(q)
            # print(("euler:"+"{:.4f},\t"*3).format(*[math.degrees(e) for e in eu]))
            # print(("trans:"+"{:.4f},\t"*3).format(*[t.x, t.y, t.z]))
        
            t = np.array([t.x, t.y , t.z])
            # tran_matrix = np.zeros(dtype = np.float, shape = (4,4))
            tran_matrix = transformations.quaternion_matrix(q)
            tran_matrix[:3,3] = t
            with lock:
                rotation_matrices = np.concatenate((rotation_matrices, tran_matrix.reshape(1,4,4)), axis=0)
                new_frame.set()
    except Exception as e:
        # I do not know what is wrong with the realsense 
        # that it does not generate the message
        # I need to manually print it.
        traceback.print_exc()
        raise e


def process_d435(frame):
    if frame.is_points():
        pass


def process_frames(frame):
    # s = f'stream name: {frame.profile.stream_name()},\ttime: {frame.timestamp} \t'
    # if frame.is_depth_frame():
    #     s += 'depth frame\t'
    # if frame.is_motion_frame():
    #     s += 'motion frame\t'
    # if frame.is_pose_frame():
    #     s += 'pose_frame\t'
    # if frame.is_points():
    #     s += 'is_points\t'
    # if frame.is_video_frame():
    #     s += 'is_video_frame\t'
    # print(s)

    process_t265(frame)
    process_d435(frame)

for dev in ctx.query_devices():
    device_name = dev.get_info(rs.camera_info.name)
    print(f'device: {device_name}')
    p = rs.pipeline(ctx) 
    cfg = rs.config()
    dev_serial = dev.get_info(rs.camera_info.serial_number)
    del dev ## <<<<------------------------------------ This line is my workaround
    cfg.enable_device(dev_serial)
    if device_name == 'Intel RealSense T265':
        cfg.enable_stream(rs.stream.pose)
    elif device_name == 'Intel RealSense D435I':
        cfg.enable_all_streams()
    p.start(cfg, process_frames) 
    pipelines.append(p)

print('pipelines started')
s = time.time()
# pl.show()
while True:
    if new_frame.wait():
        new_frame.clear()
        with lock:
            last_frame = rotation_matrices[-1]
            last_idx = rotation_matrices.shape[0]
            print(last_idx)
        pl.plot_frame(last_frame, None)