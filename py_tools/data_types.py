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
        self.XY = np.zeros((2, self.num_readings), dtype=np.float)
        for idx in range(self.num_readings):
            angle = radians(float(idx))
            ro = self.scan[idx]
            self.XY[0, idx] = ro * cos(angle)
            self.XY[1, idx] = ro * sin(angle)
        

class DataSet:
    def __init__(self):
        self.data = []
        self.odoms = []
        self.lasers = []