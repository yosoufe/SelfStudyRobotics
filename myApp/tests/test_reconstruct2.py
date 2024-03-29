from py3dscanner import daq
import numpy as np
import multiprocessing as mp
from py3dscanner import pangolin_vis as vizz
from py3dscanner.enums import EFrameType
import time

# at each frame
t265_to_d435 = np.identity(4, dtype=float)
t265_to_d435[1,1]=-1.0
t265_to_d435[2,2]=-1.0
# t265_to_d435[0,3]=22.08886  / 1000.0
# t265_to_d435[1,3]=32.76069  / 1000.0
# t265_to_d435[2,3]=-47.06099 / 1000.0
d435_to_t265 = np.linalg.inv(t265_to_d435)
print(f'{t265_to_d435=}')

if __name__ == "__main__": 
    depths, poses = daq.load_data(filename='/home/yousof/robotics/data/test_data.npy')
    print(f'{depths.shape=}')
    print(f'{poses.shape=}')
    assert poses.shape[0]==depths.shape[0], f'{poses.shape}!={depths.shape}'
    poses = poses[20:]
    poses = t265_to_d435 @ poses @ d435_to_t265
    depths = depths[20:]
    new_ones_shape = (depths.shape[0], depths.shape[1], 1)
    depths = np.concatenate((depths, np.ones(shape=new_ones_shape)), axis = 2)
    depths = np.transpose(depths, (0,2,1))
    print(f'{poses.shape=},{depths.shape=}')
    transformed = np.matmul(poses,depths)
    # print(f'{transformed.shape=}')
    transformed = np.transpose(transformed, (0,2,1))
    transformed = transformed[:,:,:3]
    transformed = transformed.astype('float32')
    print(f'{transformed.shape=}')

    qu = mp.Queue()
    viz = vizz.Visualizer(qu, title = "Sensor Visualizer- Without calibration")

    idx = 0

    while not viz.shoudldQuit():
        points = transformed[idx]
        # print(f'{points.shape=}')
        qu.put((EFrameType.DEPTH, (points, poses[idx])))
        time.sleep(0.01)
        idx += 1
        idx = idx % transformed.shape[0]

    viz.join()