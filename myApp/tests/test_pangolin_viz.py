import multiprocessing as mp
from py3dscanner import pangolin_vis as vizz
from py3dscanner.enums import EFrameType
import numpy as np
import time

def heart_filter(p):
    within_heart = ((np.matmul(p*p, np.array([1,9/4.0, 1])) - 1) ** 3 - p[:,0]**2 * p[:,2]**3 - 9.0/200 * p[:,1]**2 * p[:,2]**3) < 0
    return p[within_heart]

if __name__ == "__main__":
    # drawing a heart using the visualizer above
    qu = mp.Queue()
    viz = vizz.Visualizer(qu)

    while not viz.shoudldQuit():
        points = np.random.random((50000, 3)).astype('float32') * 4 - 2
        points = heart_filter(points)
        qu.put((EFrameType.DEPTH, points))
        time.sleep(1)

    viz.join()


