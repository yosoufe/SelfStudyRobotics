import numpy as np
import os
from py_tools.data_types import *

def read_relation_file():
    file_path = os.path.join(os.path.dirname(__file__),"../datasets/intel_lab_1/intel.clf")
    with open(file_path) as f:
        content = f.read().splitlines()[11:]

    return content


def parse_odom(input_str, index = None):
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
    odom.index = index
    return odom


def parse_laser(input_str, index = None):
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
    laser.index = index
    laser.calculate_XY()
    return laser

def parse_dataset():
    content = read_relation_file()
    dataset = DataSet()
    for idx, line in enumerate(content):
        line = line.split(" ")
        if line[0] == "FLASER":
            laser = parse_laser(line[1:], len(dataset.data))
            dataset.lasers.append(laser)
            dataset.data.append(laser)
        elif line[0] == "ODOM":
            odom = parse_odom(line[1:], len(dataset.data))
            dataset.odoms.append(odom)
            dataset.data.append(odom)
    return dataset


def main():
    pass
