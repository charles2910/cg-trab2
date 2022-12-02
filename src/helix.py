#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from object import Object, Color, Coordinates

from OpenGL.GL import *
import numpy as np
import math


class Helix(Object):
    """
        A class used to represent a cloud. Child of class Object.

        ...

        Attributes
        ----------
        program : class 'ctypes.c_uint'
        An object to which the shader objects will be attached

        coord : class Coordinates
        Cartesian coordinates of the center of the helix

        obj_scale: float
        Initial scale of the helix. Defaults to 1.0

        obj_rotation: float
        Initial rotation of the helix in radians from the x axis. Defaults to 0.0

        color: class Color
        Initial color of the helix
    """
    def __init__(self, program, coord = Coordinates(0.0, 0.0), obj_scale = 1.0, obj_rotation = 0.0, color = Color(1.0, 1.0, 1.0)):
        super().__init__(program, coord, obj_scale, obj_rotation, color)

    def create(self):
        '''Define the vertices for the helix'''
        vertices = np.zeros(16, [("position", np.float32, 2)])
        vertices['position'] = [
            # Pá 1
            (-0.02,  0.00),
            ( 0.02,  0.05),
            ( 0.02, -0.20),
            (-0.02, -0.20),

            # Pá 2
            ( 0.00, -0.02),
            ( 0.00,  0.02),
            (-0.20,  0.02),
            (-0.20, -0.02),

            # Pá 3
            ( 0.02,  0.00),
            ( 0.02,  0.20),
            (-0.02,  0.20),
            (-0.02,  0.00),

            # Pá 4
            ( 0.00, -0.02),
            ( 0.20, -0.02),
            ( 0.20,  0.02),
            ( 0.00,  0.02),
        ]
        return vertices

    def draw(self):
        '''Draw the boat in the window with the proper colors'''
        glBindVertexArray(self.vao)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mat_transformation"), 1, GL_TRUE, self.mat_transformation)

        # Color and draw the hull
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.3, 0.3, 0.3, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)

        glBindVertexArray(0)
