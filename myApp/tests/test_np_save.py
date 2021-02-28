from py3dscanner import daq
import multiprocessing as mp
import numpy as np

def test_numpy_save():
    print('writing to file')
    with open('test_npy.npy','wb') as f:
        for i in range(3):
            a = np.random.random((1, 3)).astype('float32') * 4 - 2
            print(a)
            np.save(f, a)
    
    print('loading from file')
    with open('test_npy.npy','rb') as f:
        while True:
            try:
                b = np.load(f)
            except ValueError as e:
                if (str(e)=='Cannot load file containing pickled data when allow_pickle=False'):
                    break
                else:
                    raise e
            print(b)

if __name__ == "__main__":
    # test_numpy_save()
    test_recorder()