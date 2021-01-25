# import sys
# sys.path.insert(0, '/home/yousof/robotics/libs/librealsense/install_host/python')

import pyrealsense2 as rs
import numpy as np 
import time 
print(rs.__file__)

import atexit
@atexit.register
def cleanup():
    print('clean up')
    for p in pis:
        try:
            p.stop()
        except:
            pass


# lets play according to the documentation
# https://dev.intelrealsense.com/docs/rs-multicam


# query devices 
ctx = rs.context()

pis = []
for dev in ctx.query_devices():
    print(f'device: {dev.get_info(rs.camera_info.name)}')
    p = rs.pipeline(ctx) # ctx
    cfg = rs.config()
    dev_serial = dev.get_info(rs.camera_info.serial_number)
    cfg.enable_device(dev_serial)
    # if dev == devd:
    #     cfg.enable_all_streams()
    # elif dev == devt:
    #     cfg.enable_stream(rs.stream.pose)
    p.start(cfg) # frame_arrival_cb
    pis.append(p)

print('pipelines started')
s = time.time()
while(time.time() -s < 3):
    time.sleep(1)


# Do Processing on a Background-Thread
# qu = rs.frame_queue(50)