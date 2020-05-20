from py_tools.intel_dataset_parser import *
import numpy as np
import pytest


def test_read_relation_file():
    content = read_relation_file()
    assert(content[0] == "ODOM 0.000000 0.000000 -0.002458 0.000000 0.000000 0.000000 976052857.337284 nohost 0.000000")


def test_parse_odom():
    input_str = "0.000000 0.000000 -0.002458 0.000000 0.000000 0.000000 976052857.337284 nohost 0.000000"
    input_str = input_str.split(" ")
    odom = parse_odom(input_str)
    assert(pytest.approx(odom.x) == 0)
    assert(pytest.approx(odom.y) == 0)
    assert(pytest.approx(odom.theta) == -0.002458)
    assert(pytest.approx(odom.tv) == 0.000000)
    assert(pytest.approx(odom.rv) == 0.000000)
    assert(pytest.approx(odom.accel) == 0.000000)
    assert(pytest.approx(odom.ipc_timestamp) == 976052857.337284)
    assert(odom.ipc_hostname == "nohost")
    assert(pytest.approx(odom.logger_timestamp) == 0.000000)


def test_parse_laser():
    input_str = "180 1.07 1.07 1.08 1.08 1.08 1.08 1.08 1.08 1.08 1.09 1.09 1.09 1.09 1.09 1.10 1.10 1.11 1.11 1.12 1.11 1.12 1.13 1.13 1.14 1.16 1.17 1.17 1.17 1.19 1.20 1.21 1.22 1.23 1.25 1.27 1.28 1.30 1.30 1.31 1.33 1.35 1.37 1.39 1.41 1.43 1.46 1.49 1.51 1.53 1.57 1.59 1.63 1.65 1.69 1.72 1.77 1.81 1.86 1.90 1.94 2.00 2.06 2.12 2.18 2.24 2.32 2.41 2.49 2.58 2.68 2.80 2.92 3.06 3.21 3.37 3.57 3.78 4.01 4.29 4.60 4.95 5.37 5.86 11.16 10.82 10.78 10.71 81.83 11.58 81.83 17.12 81.83 81.83 9.18 81.83 81.83 81.83 81.83 81.83 81.83 81.83 81.83 81.83 81.83 81.83 7.56 7.61 4.12 3.85 3.62 3.43 3.26 3.12 2.98 2.85 2.73 2.62 2.51 2.42 2.34 2.27 2.19 2.14 2.07 2.01 1.95 1.92 1.86 1.82 1.78 1.72 1.69 1.65 1.62 1.58 1.55 1.52 1.50 1.47 1.44 1.44 1.40 1.37 1.35 1.34 1.32 1.30 1.29 1.27 1.24 1.23 1.23 1.21 1.20 1.19 1.18 1.16 1.15 1.15 1.13 1.13 1.12 1.12 1.10 1.11 1.10 1.11 1.09 1.08 1.08 1.07 1.07 1.06 1.06 1.05 1.06 1.05 1.05 1.05 1.05 0.000000 0.000000 -0.002458 0.000000 0.000000 -0.002458 976052857.337530 nohost 0.000246"
    input_str = input_str.split(" ")
    laser = parse_laser(input_str)
    assert(laser.num_readings == 180)
    assert(laser.scan.shape[0] == 180)
    assert(pytest.approx(laser.scan[0]) == 1.07)
    assert(pytest.approx(laser.scan[179]) == 1.05)
    assert(pytest.approx(laser.ipc_timestamp) == 976052857.337530)
    assert(laser.ipc_hostname == "nohost")
    assert(pytest.approx(laser.logger_timestamp) == 0.000246)


def test_parse_dataset():
    dataset = parse_dataset()
    assert(len(dataset.data))