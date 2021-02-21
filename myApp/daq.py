"""
for data aquisition for the realsesnes sensosrs:
    
    - start the realsense sensor pipelines for both sensors
    - capture the incoming frames
    - pass the frames to the visualizer via a queue 
"""

import sys
sys.path.insert(0, '/home/yousof/robotics/libs/librealsense/install_host/python')

import pyrealsense2 as rs
import numpy as np 
import time 
import transformations
import math
import traceback, sys, queue
import multiprocessing as mp
from enum import Enum

class EFrameType(Enum):
    POSE = 1
    DEPTH = 2


class DAQ:
    def __init__(self, qu):
        self.quit_event = mp.Event()
        self.pipelines_lock = mp.Lock()
        self.process = mp.Process(target=self.process_function, args=(qu,))
        self.process.start()
    
    def process_function(self, qu):
        # initialize and start the pipelines
        self.init(qu)

        # wait for the quit event
        self.quit_event.wait()

        # close the pipelines
        self.stop_pipelines()
            

    def init(self, qu):
        self.qu = qu
        self.pipelines = []
        self.ctx = rs.context()
        self.pc = rs.pointcloud()
        self.start_pipelines()
    
    def start_pipelines(self):
        with self.pipelines_lock:
            for dev in self.ctx.query_devices():
                device_name = dev.get_info(rs.camera_info.name)
                print(f'device found: "{device_name}"')
                p = rs.pipeline(self.ctx) 
                cfg = rs.config()
                dev_serial = dev.get_info(rs.camera_info.serial_number)
                if device_name == 'Intel RealSense T265':
                    del dev ## <<<<------------------------------------ This line is my workaround
                    cfg.enable_device(dev_serial)
                    cfg.enable_stream(rs.stream.pose)
                elif device_name == 'Intel RealSense D435I':
                    cfg.enable_device(dev_serial)
                    cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
                p.start(cfg, self.process_frames) 
                self.pipelines.append(p)
            print('pipelines started')
    
    def stop_pipelines(self):
        with self.pipelines_lock:
            for p in self.pipelines:
                try:
                    p.stop()
                except:
                    pass

    def stop(self):
        self.quit_event.set()
    
    def join(self):
        self.process.join()
    
    def process_frames(self,frame):
        try:
            # print_frame_type(frame)
            if frame.is_frameset():
                frameset = frame.as_frameset()
                if frameset:
                    depth = frameset.get_depth_frame()
                    if depth:
                        self.process_depth_frame(depth)
            
            if frame.is_pose_frame():
                pose_frame = frame.as_pose_frame()
                if pose_frame:
                    self.process_pose_frame(pose_frame)

        except Exception as e:
            # I do not know what is wrong with the realsense 
            # that it does not generate the error message withou the following mess
            # I need to manually print the error message and re-raise it.
            traceback.print_exc()
            self.stop()
            raise e
    
    def process_depth_frame(self, depth):
        depth_array = np.asanyarray(depth.get_data())
        self.qu.put((EFrameType.DEPTH, depth_array))
    
    def process_pose_frame(self, pose_frame):
        pose_data = pose_frame.pose_data
        q = pose_data.rotation
        t = pose_data.translation
        t = np.array([t.x, t.y , t.z])
        q = [q.w, q.x, q.y , q.z]
        tran_matrix = transformations.quaternion_matrix(q)
        tran_matrix[:3,3] = t
        self.qu.put((EFrameType.POSE, tran_matrix))
    
    def shoudldQuit(self):
        return self.quit_event.is_set()




def save_array(array):
    with open('rotation_matrices.npy', 'wb') as f:
        np.save(f, array)

def print_frame_type(frame):
    s = f'stream name: {frame.profile.stream_name()},\ttime: {frame.timestamp} \t'
    if frame.is_depth_frame():
        s += 'is_depth_frame\t'
    if frame.is_motion_frame():
        s += 'is_motion_frame\t'
    if frame.is_pose_frame():
        s += 'is_pose_frame\t'
    if frame.is_points():
        s += 'is_points\t'
    if frame.is_video_frame():
        s += 'is_video_frame\t'
    if frame.is_frameset():
        s += 'is_frameset\t'
    print(s)





if __name__ == "__main__": 
    # create a queue
    qu = mp.Queue()

    # pass the queue to the DAQ
    daq = DAQ(qu)

    try:
        while not daq.shoudldQuit():
            # receive frames from the queue
            try:
                frame_type, values = qu.get(timeout=0.001)

                # print their type
                print(frame_type, values)
            except queue.Empty:
                pass
        daq.join()
    except KeyboardInterrupt as e:
        daq.stop()
        daq.join()
        raise e


    