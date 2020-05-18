import numpy as np

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


def read_relation_file():
  file_path = "../datasets/intel_lab_1/intel.clf"
  with open(file_path) as f:
    content = f.read().splitlines()[11:]
  
  return content


def parse_odom(input_str):
  odom = Odom()
  input_str = input_str.split(" ")
  odom.x = float(input_str[0])
  odom.y = float(input_str[1])
  odom.theta = float(input_str[2])
  odom.tv = float(input_str[3])
  odom.rv = float(input_str[4])
  odom.accel = float(input_str[5])
  odom.ipc_timestamp = float(input_str[6])
  odom.ipc_hostname = input_str[7]
  odom.logger_timestamp  = float(input_str[8])
  return odom

def parse_laser(input_str):
  laser = Laser()
  input_str = input_str.split(" ")
  laser.num_readings = int(input_str[0])
  scan_v = [float(v) for v in input_str[1:-9]]
  laser.scan = np.array(scan_v, dtype=float)
  laser.ipc_timestamp = float(input_str[-3])
  laser.ipc_hostname = input_str[-2]
  laser.logger_timestamp  = float(input_str[-1])
  return laser

def main():
  content = read_relation_file()
