import multiprocessing as mp
from py3dscanner import daq
import queue

if __name__ == "__main__": 
    # create a queue
    qu = mp.Queue()

    # pass the queue to the DAQ
    dq = daq.DAQ(qu, filename='test_data.npy')

    try:
        while not dq.shoudldQuit():
            # receive frames from the queue
            try:
                frame_type, values = qu.get(timeout=0.001)

                # print their type
                print(frame_type, values.shape)
            except queue.Empty:
                pass
        dq.join()
    except KeyboardInterrupt as e:
        dq.stop()
        dq.join()
        raise e
