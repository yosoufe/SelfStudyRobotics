import matplotlib.pyplot as plt
import transformations
import numpy as np


class FramePlotter:
    def __init__(self, live=True):
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')
        self.live = live
        if self.live:
            plt.ion()
            plt.show()

    def plot_frame(self, rot, position=None, show=False):
        plt.cla()
        if rot.shape == (4,):
            # quaternions
            trans = transformations.quaternion_matrix(rot)
            pos = position
        elif rot.shape == (4, 4):
            trans = rot
            pos = trans[:3, 3]
        else:
            raise RuntimeError(f'{rot} has wrong dimension.')

        for idx, color in zip(range(3), ['red', 'green', 'blue']):
            xs = [0, trans[0, idx]]
            ys = [0, trans[1, idx]]
            zs = [0, trans[2, idx]]
            self.ax.plot(xs, ys, zs, color=color)
        plt.draw()
        plt.pause(0.0001)
        if show:
            plt.show()

    def show(self):
        plt.show(block=False)

    # def equal_scale(self):
    #     max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
    #     Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
    #     Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
    #     Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
    #     # Comment or uncomment following both lines to test the fake bounding box:
    #     for xb, yb, zb in zip(Xb, Yb, Zb):
    #     ax.plot([xb], [yb], [zb], 'w')


if __name__ == '__main__':
    # Quaternions w+ix+jy+kz are represented as [w, x, y, z].
    test_quat = transformations.random_quaternion()
    print('quaternion:', test_quat)
    test_position = [1, 2, 3]
    print('position', test_position)
    pl = FramePlotter(live=False)
    pl.plot_frame(test_quat, test_position, show=True)
