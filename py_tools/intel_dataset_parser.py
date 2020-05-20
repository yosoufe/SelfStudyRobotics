import numpy as np
import os
from math import sin, cos, radians

class Message:
    def __init__(self):
        self.message_name = str()
        self.ipc_timestamp = float()
        self.ipc_hostname = str()
        self.logger_timestamp = float()


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



def read_relation_file():
    file_path = os.path.join(os.path.dirname(__file__),"../datasets/intel_lab_1/intel.clf")
    with open(file_path) as f:
        content = f.read().splitlines()[11:]

    return content


def parse_odom(input_str):
    odom = Odom()
    odom.x = float(input_str[0])
    odom.y = float(input_str[1])
    odom.theta = float(input_str[2])
    odom.tv = float(input_str[3])
    odom.rv = float(input_str[4])
    odom.accel = float(input_str[5])
    odom.ipc_timestamp = float(input_str[6])
    odom.ipc_hostname = input_str[7]
    odom.logger_timestamp = float(input_str[8])
    return odom


def parse_laser(input_str):
    laser = Laser()
    laser.num_readings = int(input_str[0])
    scan_v = [float(v) for v in input_str[1:-9]]
    laser.scan = np.array(scan_v, dtype=float)
    laser.ipc_timestamp = float(input_str[-3])
    laser.ipc_hostname = input_str[-2]
    laser.logger_timestamp = float(input_str[-1])

    laser.x = float(input_str[-9])
    laser.y = float(input_str[-8])
    laser.theta = float(input_str[-7])
    laser.odom_x = float(input_str[-6])
    laser.odom_y = float(input_str[-5])
    laser.odom_theta = float(input_str[-4])
    laser.calculate_XY()
    return laser

class DataSet:
    def __init__(self):
        self.data = []
        self.odoms = []
        self.lasers = []

def parse_dataset():
    content = read_relation_file()
    dataset = DataSet()
    for idx, line in enumerate(content):
        line = line.split(" ")
        if line[0] == "FLASER":
            laser = parse_laser(line[1:])
            dataset.data.append((laser,len(dataset.lasers)))
            dataset.lasers.append((laser, idx))
        elif line[0] == "ODOM":
            odom = parse_odom(line[1:])
            dataset.data.append((odom,len(dataset.lasers)))
            dataset.odoms.append((odom, idx))
    return dataset


def main():
    pass
