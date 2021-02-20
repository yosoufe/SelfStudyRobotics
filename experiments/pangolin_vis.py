import sys 
sys.path.append('/home/yousof/software/graphics/Pangolin/build/src')

import time
import numpy as np


import pypangolin as pango
from OpenGL.GL import *
from OpenGL.arrays import vbo


import ctypes 

class Visualizer:
    def __init__(self):
        self.win = pango.CreateWindowAndBind("Sensor Visualizer", 640, 480)
        glEnable(GL_DEPTH_TEST)
        # Define Projection and initial ModelView matrix
        self.pm = pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.1, 1000)
        self.mv = pango.ModelViewLookAt(-2,2,-2, 0,0,0, pango.AxisY)
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

        glPointSize(5)
        glDrawArrays(GL_POINTS, 0, noOfVertices)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw_points(self, noPoints):
        # Clear screen and activate view to render into
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.d_cam.Activate(self.s_cam)


        # noPoints = 100000
        points = np.random.random((noPoints, 3)).astype('float32') * 4 - 2
        points = heart_filter(points)
        noPoints = points.shape[0]
        colors = np.array([1.0,0,0]*noPoints, dtype='float32').reshape(noPoints, 3)
        points = np.concatenate([points, colors], axis = 1)
        bufferObj = self.CreateBuffer(points)
        noPoints  = points.shape[0]
        self.DrawBuffer(bufferObj, noPoints)


def heart_filter(p):
    within_heart = ((np.matmul(p*p, np.array([1,9/4.0, 1])) - 1) ** 3 - p[:,0]**2 * p[:,2]**3 - 9.0/200 * p[:,1]**2 * p[:,2]**3) < 0
    return p[within_heart]
    

def draw_single_point():
    glEnable(GL_POINT_SMOOTH)
    glPointSize(5)

    glBegin(GL_POINTS)
    glColor3d(1, 0, 0)
    glVertex3d(0, 0, 0)
    glEnd()

def visulaizer():
    viz = Visualizer()
    while not pango.ShouldQuit():
        viz.draw_points(10000)

        # Swap frames and Process Events
        pango.FinishFrame()

if __name__ == "__main__":
    visulaizer()