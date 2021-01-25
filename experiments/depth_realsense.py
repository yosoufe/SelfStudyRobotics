import pyrealsense2 as rs
import numpy as np 
import time 


# lets play according to the documentation
# https://dev.intelrealsense.com/docs/api-how-to

# this seems to only stream depth camera


# query devices 
ctx = rs.context()
devices = ctx.query_devices()


devd = None # depth device 
devt = None # tracking device

# assert(devices.size() == 2) # I expect two devices one tracking and one depth


# get devices
for dev in devices:
    if dev.get_info(rs.camera_info.name) == 'Intel RealSense D435I':
        print('D435 detected')
        devd = dev
    if dev.get_info(rs.camera_info.name) == 'Intel RealSense T265':
        print('T265 detected')
        devt = dev

# start streaming
pipe = rs.pipeline()
config = rs.config()
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# config.enable_stream(rs.stream.accel)
# config.enable_stream(rs.stream.pose) # this does not work for streaming using callback
config.enable_all_streams()

pipe.start(config)

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

# Wait for Coherent Set of Frames
frames = pipe.wait_for_frames()
for  frame in frames:
    print_stuff(frame)
    
pipe.stop()


# using callback
def frame_arrival_cb(frames):
    print_stuff(frames)

pipe.start(config, frame_arrival_cb)

s = time.time()
while(time.time() -s < 3):
    time.sleep(1)
pipe.stop()

# Do Processing on a Background-Thread
# qu = rs.frame_queue(50)
