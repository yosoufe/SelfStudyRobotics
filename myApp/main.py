"""
Main file for my application
"""

import daq
import pangolin_vis as vis
import time
import multiprocessing as mp

if __name__ == "__main__":
    qu = mp.Queue()
    vz = vis.Visualizer(qu)
    dq = daq.DAQ(qu)


    vz.wait_till_end()

    dq.stop()
    dq.join()
    vz.join()
        
