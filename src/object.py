#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from abc import abstractmethod
import numpy as np
from OpenGL.GL import *

class Coordinates:
    """
        A class used to represent a cartesian coordinate

        ...

        Attributes
        ----------
        x : float
        x coordinate that varies from -1 to 1
        y : float
        y coordinate that varies from -1 to 1
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Color:
    """
        A class used to represent a RGB color

        ...

        Attributes
        ----------
        R : float
        red parameter that varies from 0 to 1
        B : float
        blue parameter that varies from 0 to 1
        G : float
        green parameter that varies from 0 to 1
    """

    def __init__(self, R, G, B):
        self.R = R
        self.G = G
        self.B = B

class Object:
    """
        A abstract class used to represent a Object in the window.

        ...

        Attributes
        ----------
        program : class 'ctypes.c_uint'
        An object to which the shader objects will be attached

        coord : class Coordinates
        Cartesian coordinates of the center of the object

        obj_scale: float
        Initial scale of the object

        obj_rotation: float
        Initial rotation of the object in radians from the x axis

        color: class Color
        Initial color of the object
    """
    def __init__(self, program, coord, obj_scale, obj_rotation, color):
        self.program = program
        self.color = color
        self.vao = None
        self.vertices = None
        self.coordinates = coord
        self.obj_scale = obj_scale
        self.obj_rotation = obj_rotation
        # The base object contains the identity transformation matrix
        self.mat_transformation = np.array([[1.0, 0.0, 0.0, 0.0],
                                            [0.0, 1.0, 0.0, 0.0],
                                            [0.0, 0.0, 1.0, 0.0],
                                            [0.0, 0.0, 0.0, 1.0]], np.float32)
        # Se a posição inicial for fora da origem, faça a translação "manual"
        if self.coordinates.x != 0 or self.coordinates.y != 0:
            self.mat_transformation[0][3] = self.coordinates.x
            self.mat_transformation[1][3] = self.coordinates.y

    @abstractmethod
    def create(self):
        """An abstract method to define the vertex of the objects"""
        pass

    def prepare(self):
        """Prepare the vertices to be send to the GPU"""
        self.vertices = self.create()

        # Request a VAO
        self.vao = glGenVertexArrays(1)
        # Request a buffer slot from GPU
        buffer = glGenBuffers(1)
        glBindVertexArray(self.vao)
        # Make this buffer the default one
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        # Upload data
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        # Bind the position attribute
        stride = self.vertices.strides[0]

        loc = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc)

        glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, ctypes.c_void_p(0))
        glBindVertexArray(0)

    def draw(self):
        """Generic draw method for simple objects. For complex objects, this method is overwritten."""
        glBindVertexArray(self.vao)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mat_transformation"), 1, GL_TRUE, self.mat_transformation)

        glUniform4f(glGetUniformLocation(self.program, "color"), self.color.R, self.color.G, self.color.B, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 0, len(self.vertices))

        glBindVertexArray(0)

    def translate(self, t_x, t_y):
        '''Multiply the current matrix by the translation matrix with offset (t_x, t_y)'''
        self.coordinates.x += t_x
        self.coordinates.y += t_y
        transl_matrix = np.array([
            [1.0, 0.0, 0.0, t_x],
            [0.0, 1.0, 0.0, t_y],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]],
            np.float32)
        self.mat_transformation = np.matmul(transl_matrix, self.mat_transformation)

    def scale(self, s_x, s_y):
        '''Multiply the current matrix by the scale matrix (s_x, s_x). Keep ratio s_y = s_x'''
        new_scale = self.obj_scale * s_x
        if new_scale > 0:
            self.obj_scale = new_scale
            mat_scale = np.array([
                [s_x, 0.0, 0.0, self.coordinates.x * (1.0 - s_x)],
                [0.0, s_x, 0.0, self.coordinates.y * (1.0 - s_x)],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]],
                np.float32)
            self.mat_transformation = np.matmul(mat_scale, self.mat_transformation)

    def rotate(self, ang):
        '''Multiply the current matrix by the rotation matrix (ang).'''
        self.obj_rotation += ang
        ref = self.coordinates
        mat_rot = np.array([
            [np.cos(ang), -np.sin(ang),  0.0,  ref.x *(1 - np.cos(ang)) + ref.y * np.sin(ang)],
            [np.sin(ang),  np.cos(ang),  0.0,  ref.y *(1 - np.cos(ang)) - ref.x * np.sin(ang)],
            [0.0,          0.0,          1.0,  0.0],
            [0.0,          0.0,          0.0,  1.0]],
            np.float32)
        self.mat_transformation = np.matmul(mat_rot, self.mat_transformation)
