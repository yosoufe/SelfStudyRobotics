import numpy as np
from math import sin, cos, radians

class Message:
    def __init__(self):
        self.message_name = str()
        self.ipc_timestamp = float()
        self.ipc_hostname = str()
        self.logger_timestamp = float()
        self.index = int()


class Odom(Message):
    def __init__(self):
        super().__init__()
        self.x = float()
        self.y = float()
        self.theta = float()
        self.tv = float()
        self.rv = float()
        self.accel = float()


class Laser(Message):
    def __init__(self):
        super().__init__()
        self.num_readings = int()
        self.scan = None
        self.XY = None
        self.x = float()
        self.y = float()
        self.theta = float()
        self.odom_x = float()
        self.odom_y = float()
        self.odom_theta = float()
    
    def calculate_XY(self):
        points = []
        for idx in range(self.num_readings):
            ro = self.scan[idx]
            if ro > 80:
                # invalid measurement
                continue
            angle = radians(float(idx))
            p = np.array([[ro * cos(angle)], [ro * sin(angle)]], dtype=np.float)
            points.append(p)
        self.XY = np.concatenate(points, axis=1)

class DataSet:
    def __init__(self):
        self.data = []
        self.odoms = []
        self.lasers = []
        self.length_lasers = []