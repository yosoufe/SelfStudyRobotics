import sys 
sys.path.append('/home/yousof/software/graphics/Pangolin/build/src')

import time
import numpy as np


import pypangolin as pango
from OpenGL.GL import *
from OpenGL.arrays import vbo


import ctypes 

def CreateBuffer(attributes):
    m,n = attributes.shape
    bufferdata = attributes.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    buffersize = m * n * ctypes.sizeof(ctypes.c_float)    # buffer size in bytes 

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, buffersize, bufferdata, GL_STATIC_DRAW) 
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo

def DrawBuffer(vbo, noOfVertices):
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    stride = 6*4 # (24 bates) : [x, y, z, r, g, b] * sizeof(float)

    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, stride, None)

    glEnableClientState(GL_COLOR_ARRAY)
    offset = 3*4 # (12 bytes) : the rgb color starts after the 3 coordinates x, y, z 
    glColorPointer(3, GL_FLOAT, stride, ctypes.c_void_p(offset))

    glDrawArrays(GL_POINTS, 0, noOfVertices)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

def draw_points():
    noPoints = 100000
    points = np.random.random((100000, 3)).astype('float32') * 10
    colors = np.array([1.0,0,0]*noPoints, dtype='float32').reshape(noPoints, 3)
    points = np.concatenate([points, colors], axis = 1)
    bufferObj = CreateBuffer(points)
    noPoints  = points.shape[0]
    DrawBuffer(bufferObj, noPoints)


def draw_single_point():
    glEnable(GL_POINT_SMOOTH)
    glPointSize(5)

    glBegin(GL_POINTS)
    glColor3d(1, 0, 0)
    glVertex3d(0, 0, 0)
    glEnd()

def visulaizer():
    win = pango.CreateWindowAndBind("Sensor Visualizer", 640, 480)
    glEnable(GL_DEPTH_TEST)


    # Define Projection and initial ModelView matrix
    pm = pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.1, 1000)
    mv = pango.ModelViewLookAt(-2,2,-2, 0,0,0, pango.AxisY)
    s_cam = pango.OpenGlRenderState(pm, mv)
    
    # Create Interactive View in window
    handler = pango.Handler3D(s_cam)
    d_cam = (
        pango.CreateDisplay()
        .SetBounds(
            pango.Attach(0),
            pango.Attach(1),
            pango.Attach(0),
            pango.Attach(1),
            -640.0 / 480.0,
        )
        .SetHandler(handler)
    )


    while not pango.ShouldQuit():
        # Clear screen and activate view to render into
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        d_cam.Activate(s_cam)

        # Render OpenGL Cube
        # pango.glDrawColouredCube()

        draw_points()

        # Swap frames and Process Events
        pango.FinishFrame()

if __name__ == "__main__":
    visulaizer()