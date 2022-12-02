#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from object import Object, Color, Coordinates

import numpy as np
from OpenGL.GL import *

class Mountains(Object):
    """
        A class used to represent the mountains. Child of class Object.

        ...

        Attributes
        ----------
        program : class 'ctypes.c_uint'
        An object to which the shader objects will be attached

        coord : class Coordinates
        Cartesian coordinates of the center of the mountain. Defaults to Coordinates(0.0, 0.0)

        obj_scale: float
        Initial scale of the mountain. Defaults to 1.0

        obj_rotation: float
        Initial rotation of the mountain in radians from the x axis. Defaults to 0.0

        color: class Color
        Initial color of the mountain. Defaults to Color(1.0, 1.0, 1.0)
    """
    def __init__(self, program, coord = Coordinates(0.0, 0.0), obj_scale = 1.0, obj_rotation = 0.0, color = Color(0.627, 0.322, 0.176)):
        super().__init__(program, coord, obj_scale, obj_rotation, color)

    def create(self):
        '''Define the vertex of the mountains'''
        vertices = np.zeros(21, [("position", np.float32, 2)])
        # Each group of three vertices represent a mountain
        vertices['position'] = [
            (-0.20, 0.20),
            (0.03, 0.50),
            (0.20, 0.20),

            (-0.05, 0.20),
            (-0.38, 0.45),
            (-0.60, 0.20),

            (-0.90, 0.20),
            (-0.65, 0.38),
            (-0.50, 0.20),

            (-1.30, 0.20),
            (-0.98, 0.35),
            (-0.75, 0.20),

            (0.56, 0.20),
            (0.38, 0.40),
            (0.10, 0.20),

            (0.82, 0.20),
            (0.67, 0.40),
            (0.43, 0.20),

            (1.3, 0.20),
            (0.89, 0.40),
            (0.71, 0.20),
        ]
        return vertices

    def draw(self):
        '''Draw the mountains in the window with the proper colors'''
        glBindVertexArray(self.vao)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mat_transformation"), 1, GL_TRUE, self.mat_transformation)

        # change the color of the mountains to create a depth effect
        glUniform4f(glGetUniformLocation(self.program, "color"), self.color.R - 0.1, self.color.G, self.color.B, 1.0)

        # each group of three vertex is drawed as a triangule
        glDrawArrays(GL_TRIANGLE_FAN, 0, 3)

        glUniform4f(glGetUniformLocation(self.program, "color"), self.color.R, self.color.G, self.color.B, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 3, 3)
        glDrawArrays(GL_TRIANGLE_FAN, 6, 3)
        glDrawArrays(GL_TRIANGLE_FAN, 9, 3)

        glUniform4f(glGetUniformLocation(self.program, "color"), self.color.R + 0.1, self.color.G, self.color.B, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 3)
        glDrawArrays(GL_TRIANGLE_FAN, 15, 3)
        glDrawArrays(GL_TRIANGLE_FAN, 18, 3)

        glBindVertexArray(0)
