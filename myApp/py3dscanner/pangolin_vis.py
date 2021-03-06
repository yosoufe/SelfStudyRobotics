import sys 
sys.path.append('/home/yousof/software/graphics/Pangolin/build/src')

import time
import numpy as np


import pypangolin as pango
from OpenGL.GL import *
from OpenGL.arrays import vbo
import multiprocessing  as mp
import queue
from py3dscanner.enums import EFrameType
import transformations
import math

import ctypes 

def axisAngleFromRotation(rotation):
    # https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToAngle/index.htm
    quat = transformations.quaternion_from_matrix(rotation)
    den = math.sqrt(1-quat[0]* quat[0])
    angleAxis =  [
        math.degrees(2* math.acos(quat[0])), # angle
        quat[1]/den,
        quat[2]/den,
        quat[3]/den,
    ]
    # print(angleAxis)
    return angleAxis

class Visualizer:
    def __init__(self, qu, title = "Sensor Visualizer"):
        self.quit_event = mp.Event() # default is False
        self.process = mp.Process(target=self.process_function, args=(qu,title))
        self.process.start()
    
    def init(self, title):
        self.depth_frame_correction = np.array(
            [
                [0.0,0.0,1.0,0],
                [-1.0,0.0,0.0,0],
                [0.0,-1.0,0.0,0],
                [0.0,0.0,0,1],
            ], dtype=np.float32
        )
        self.axisAngle = axisAngleFromRotation(self.depth_frame_correction)

        self.win = pango.CreateWindowAndBind(title, 640, 480)
        glEnable(GL_DEPTH_TEST)
        # Define Projection and initial ModelView matrix
        self.pm = pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.01, 100000)
        # self.mv = pango.ModelViewLookAt(-2,2,-2, 0,0,0, pango.AxisY)
        self.mv = pango.ModelViewLookAt(-1/2,-0.5/2,1/2.0, 0,0,0, pango.AxisZ)
        self.s_cam = pango.OpenGlRenderState(self.pm, self.mv)

        # Create Interactive View in window
        self.handler = pango.Handler3D(self.s_cam)
        self.d_cam = (
            pango.CreateDisplay()
            .SetBounds(
                pango.Attach(0),
                pango.Attach(1),
                pango.Attach(0),
                pango.Attach(1),
                -640.0 / 480.0,
            )
            .SetHandler(self.handler)
        )
        self.points = None
        self.frame = None
        self.vbo = glGenBuffers(1)
    
    def CreateBuffer(self, attributes):
        # refrence https://stackoverflow.com/questions/56787061/is-there-a-way-to-render-points-faster-opengl
        m,n = attributes.shape
        bufferdata = attributes.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        buffersize = m * n * ctypes.sizeof(ctypes.c_float)    # buffer size in bytes 

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, buffersize, bufferdata, GL_STATIC_DRAW) 
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        return self.vbo

    def DrawBuffer(self, vbo, noOfVertices):
        glBindBuffer(GL_ARRAY_BUFFER, vbo)

        stride = 6*4 # (24 bates) : [x, y, z, r, g, b] * sizeof(float)

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, stride, None)

        glEnableClientState(GL_COLOR_ARRAY)
        offset = 3*4 # (12 bytes) : the rgb color starts after the 3 coordinates x, y, z 
        glColorPointer(3, GL_FLOAT, stride, ctypes.c_void_p(offset))

        glPointSize(0.0001)
        # converting from realsense coordinate system to a vehicle like coordinate system
        glRotatef(*self.axisAngle)
        glDrawArrays(GL_POINTS, 0, noOfVertices)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    def draw_frames(self,frame_pose):
        pango.glDrawAxis(frame_pose, 0.15)

    def draw_points(self, points, frame = None):
        noPoints = points.shape[0]

        # Clear screen and activate view to render into
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.d_cam.Activate(self.s_cam)
        colors = np.array([1.0,0,0]*noPoints, dtype='float32').reshape(noPoints, 3)
        points = np.concatenate([points, colors], axis = 1)
        bufferObj = self.CreateBuffer(points)
        noPoints  = points.shape[0]
        self.DrawBuffer(bufferObj, noPoints)
        if isinstance(frame, np.ndarray): # not None
            self.draw_frames(frame)

    def process_function(self, qu, title):
        self.init(title)
        while not pango.ShouldQuit():
            try:
                typ , items = qu.get(block= False) # timeout = 0.0001
                if typ == EFrameType.DEPTH:
                    if isinstance(items, tuple):
                        self.points = items[0]
                        self.frame = items[1]
                    else:
                        self.points = items
            except queue.Empty:
                pass
            if isinstance(self.points, np.ndarray):
                self.draw_points(self.points, self.frame)

            # Swap frames and Process Events
            pango.FinishFrame()
        
        self.quit_event.set()
    
    def join(self):
        self.process.join()
    
    def shoudldQuit(self):
        return self.quit_event.is_set()
    
    def wait_till_end(self):
        self.quit_event.wait()
