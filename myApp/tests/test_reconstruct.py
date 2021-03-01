from py3dscanner import daq
import numpy as np
import multiprocessing as mp
from py3dscanner import pangolin_vis as vizz
from py3dscanner.enums import EFrameType
import time



if __name__ == "__main__": 
    depths, poses = daq.load_data(filename='/home/yousof/robotics/data/test_data.npy')
    print(f'{depths.shape=}')
    print(f'{poses.shape=}')
    assert poses.shape[0]==depths.shape[0], f'{poses.shape}!={depths.shape}'
    poses = poses[40:]
    depths = depths[40:]
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
    viz = vizz.Visualizer(qu)

    idx = 0

    while not viz.shoudldQuit():
        points = transformed[idx]
        # print(f'{points.shape=}')
        qu.put((EFrameType.DEPTH, points))
        time.sleep(0.5)
        idx += 1
        idx = idx % transformed.shape[0]

    viz.join()