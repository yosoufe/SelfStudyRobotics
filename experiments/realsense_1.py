import pyrealsense2 as rs
import numpy as np
import time

def main():
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()

    config = rs.config()
    #config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)
    #config.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 30)
    #config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    
    profile = pipeline.start(config)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    while True:
        # This call waits until a new coherent set of frames is available on a device
        # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will 
        # return stable values until wait_for_frames(...) is called
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()

        if not depth: 
            print('missing depth frame')
            continue

        depth_f = np.asanyarray(depth.get_data(), dtype= np.float)
        distance = depth_f * depth_scale

        # Print a simple text-based representation of the image, 
        # by breaking it into 10x20 pixel regions and approximating 
        # the coverage of pixels within one meter
        coverage = [0]*64
        to_print = ""
        for y in range(480):
            for x in range(640):
                dist = distance[y, x]
                if 0 < dist and dist < 1:
                    coverage[x//10] += 1
            
            if y%20 is 19:
                line = ""
                for c in coverage:
                    line += " .:nhBXWW"[c//25]
                coverage = [0]*64
                to_print += line + '\n'
        print(to_print + '\n\n\n')


if __name__ == "__main__":
    main()
