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

ctx = rs.context()

for dev in ctx.query_devices():
    print(f'device: {dev.get_info(rs.camera_info.name)}')
    p = rs.pipeline(ctx) # ctx
    cfg = rs.config()
    dev_serial = dev.get_info(rs.camera_info.serial_number)
    cfg.enable_device(dev_serial)
    p.start(cfg) ## <<<<------------------------------------ it errors out here for the T265
    pipelines.append(p)

print('pipelines started')
s = time.time()
time.sleep(1)