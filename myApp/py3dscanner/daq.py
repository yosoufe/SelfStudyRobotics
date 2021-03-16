"""
for data aquisition for the realsesnes sensosrs:
    
    - start the realsense sensor pipelines for both sensors
    - capture the incoming frames
    - pass the frames to the visualizer via a queue 
"""

import sys, os, signal
sys.path.insert(0, '/home/yousof/robotics/libs/librealsense/install_host/python')

import pyrealsense2 as rs
import numpy as np 
import time 
import transformations
import math
import traceback, sys, queue
import multiprocessing as mp
import threading as th
from py3dscanner.enums import EFrameType


class DAQ:
    def __init__(self, qu, filename = None):
        signal.signal(signal.SIGINT, self.signal_handler)
        if filename != None:
            self.recorder = Recorder(filename)
        else:
            self.recorder = None
        self.quit_event = mp.Event()
        self.quit_lock = mp.Lock()
        self.qu = qu # queues
    
    def run(self):
        self.process = mp.Process(target=self.process_function)
        self.process.start()
    
    def process_function(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN) # disable signal handler in the sub process
        # initialize and start the pipelines
        self.init()

        # wait for the quit event
        self.quit_event.wait()
        print("QUITITNG DAQ")

        # close the pipelines
        self.stop_pipelines()
        print("Pipeline Stopped")
            

    def init(self):
        self.pipelines_lock = mp.Lock()
        self.pipelines = []
        self.ctx = rs.context()
        self.pc = rs.pointcloud()
        self.depth_frame_correction = np.array(
            [
                [0.0,0.0,1.0],
                [-1.0,0.0,0.0],
                [0.0,-1.0,0.0],
            ], dtype=np.float32
        ).transpose()
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
                    cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 6)
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
        with self.quit_lock:
            if not self.quit_event.is_set():
                self.quit_event.set()

    
    def join(self):
        self.process.join(timeout=0.5)
        self.process.terminate()
    
    def process_frames(self,frame):
        try:
            if self.shoudldQuit():
                return

            with self.quit_lock:
                # print_frame_type(frame)
                if not self.qu.empty():
                    return

                if frame.is_frameset():
                    frameset = frame.as_frameset()
                    if frameset:
                        depth = frameset.get_depth_frame()
                        if depth:
                            self.process_depth_frame(depth)
                            # print(f'{depth.get_units()=}')
                
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
    
    def process_depth_frame(self, depth_frame):
        points = self.pc.calculate(depth_frame)
        v = points.get_vertices()
        verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)  # xyz
        # verts = np.matmul(verts, self.depth_frame_correction)
        self.write_data(typ=EFrameType.DEPTH, val=verts)
        self.qu.put((EFrameType.DEPTH, verts))
    
    def process_pose_frame(self, pose_frame):
        pose_data = pose_frame.pose_data
        q = pose_data.rotation
        t = pose_data.translation
        t = np.array([t.x, t.y , t.z])
        q = [q.w, q.x, q.y , q.z]
        tran_matrix = transformations.quaternion_matrix(q)
        tran_matrix[:3,3] = t
        # self.qu.put((EFrameType.POSE, tran_matrix))
        self.write_data(typ = EFrameType.POSE, val=tran_matrix)
    
    def write_data(self, typ, val):
        if self.recorder:
            self.recorder.add_new_data(typ= typ, val= val)

    
    def shoudldQuit(self):
        return self.quit_event.is_set()
    
    def signal_handler(self, sigum, frame):
        # print(f'{self.quit_event.is_set()=}')
        self.stop()




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



class Recorder:
    """ Synchronise and write to a file
    """
    def __init__(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
        self.filename = filename
        self.last_pose = None
        self.last_depth = None
        self.lock = mp.Lock()

    def add_new_data(self,typ, val):
        if typ == EFrameType.DEPTH:
            self.last_depth = val
        elif typ == EFrameType.POSE:
            self.last_pose = val
        with self.lock:
            if isinstance(self.last_depth, np.ndarray) and isinstance(self.last_pose, np.ndarray):
                self.write_to_file(self.last_depth)
                self.write_to_file(self.last_pose)
                self.last_depth, self.last_pose = None, None

    
    def write_to_file(self, array):
        with open(self.filename,'ab') as f:
            np.save(f, array)
            # print(array.shape)


def load_data(filename):
    """ returns tuples of (depths, poses)
    """
    def is_correct_format(arr):
        if isinstance(arr, type(None)):
            return False
        
        return True

    with open(filename, 'rb') as f:
        depths = None
        poses = None
        while True:
            try:
                arr = np.load(f)
            except ValueError as e:
                if 'allow_pickle=False' in str(e) or 'cannot reshape array of size' in str(e):
                    break
                else:
                    raise e
            if not is_correct_format(arr):
                break
            arr = np.expand_dims(arr, axis=0)
            if arr.shape == (1,4,4):
                if isinstance(poses,type(None)):
                    poses = arr
                else:
                    poses = np.concatenate((poses, arr), axis=0)
            else:
                if isinstance(depths,type(None)):
                    depths = arr
                else:
                    depths = np.concatenate((depths, arr), axis=0)
        mi = min(depths.shape[0],poses.shape[0])
        print(f'{mi} samples loaded')
        depths, poses = depths[:mi], poses[:mi]
        assert depths.shape[0]==poses.shape[0], f'{depths.shape}!={poses.shape}'
    return (depths, poses)