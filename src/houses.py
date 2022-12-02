#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from object import Object, Color, Coordinates

from OpenGL.GL import *
import numpy as np

class RedHouse(Object):
    """
        A class used to represent the red house. Child of class Object.

        ...

        Attributes
        ----------
        program : class 'ctypes.c_uint'
        An object to which the shader objects will be attached

        coord : class Coordinates
        Cartesian coordinates of the center of the house. Defaults to Coordinates(0.0, 0.0)

        obj_scale: float
        Initial scale of the house. Defaults to 1.0

        obj_rotation: float
        Initial rotation of the house in radians from the x axis. Defaults to 0.0

        color: class Color
        Initial color of the house. Defaults to Color(1.0, 1.0, 1.0)
    """
    def __init__(self, program, coord = Coordinates(0.0, 0.0), obj_scale = 1.0, obj_rotation = 0.0, color = Color(1.0, 1.0, 1.0)):
        super().__init__(program, coord, obj_scale, obj_rotation, color)

    def create(self):
        '''Define the vertex of the red house'''
        vertices = np.zeros(20, [("position", np.float32, 2)])
        vertices['position'] = [
            # Main Body
            (-0.91, -0.32),
            (-0.91, -0.04),
            (-0.63, -0.04),
            (-0.63, -0.32),

            # Roof
            (-0.95, -0.04),
            (-0.91, 0.10),
            (-0.63, 0.10),
            (-0.59, -0.04),

            # Door
            (-0.81, -0.09),
            (-0.81, -0.32),
            (-0.73, -0.32),
            (-0.73, -0.09),

            # Window 1
            (-0.89, -0.08),
            (-0.89, -0.20),
            (-0.82, -0.20),
            (-0.82, -0.08),

            # Window 2
            (-0.72, -0.08),
            (-0.72, -0.20),
            (-0.65, -0.20),
            (-0.65, -0.08),
        ]
        return vertices

    def draw(self):
        '''Draw the red house in the window with the proper colors'''
        glBindVertexArray(self.vao)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mat_transformation"), 1, GL_TRUE, self.mat_transformation)

        # Color and draw the main body
        glUniform4f(glGetUniformLocation(self.program, "color"), 1.0, 0.14, 0.0, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        # Color and draw the door and the roof
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.38, 0.19, 0.0, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        # Color and draw the windows
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.0, 0.31, 0.31, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)

        glBindVertexArray(0)

class GreenHouse(Object):
    """
        A class used to represent the green house. Child of class Object.

        ...

        Attributes
        ----------
        program : class 'ctypes.c_uint'
        an object to which the shader objects will be attached
    """
    def __init__(self, program, coord = Coordinates(0.0, 0.0), obj_scale = 1.0, obj_rotation = 0.0, color = Color(1.0, 1.0, 1.0)):
        super().__init__(program, coord, obj_scale, obj_rotation, color)

    def create(self):
        '''Define the vertex of the green house'''
        vertices = np.zeros(20, [("position", np.float32, 2)])
        vertices['position'] = [
            # Main Body
            (0.19, -0.20),
            (0.19, 0.12),
            (0.47, 0.12),
            (0.47, -0.20),

            # Roof
            (0.15, 0.12),
            (0.19, 0.26),
            (0.47, 0.26),
            (0.51, 0.12),

            # Door
            (0.29, -0.20),
            (0.29, 0.10),
            (0.37, 0.10),
            (0.37, -0.20),

            # Window 1
            (0.20, -0.01),
            (0.20, 0.10),
            (0.27, 0.10),
            (0.27, -0.01),

            # Window 2
            (0.39, -0.01),
            (0.39, 0.10),
            (0.46, 0.10),
            (0.46, -0.01),
        ]
        return vertices

    def draw(self):
        '''Draw the green house in the window with the proper colors'''
        glBindVertexArray(self.vao)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mat_transformation"), 1, GL_TRUE, self.mat_transformation)

        # Color and draw the main body
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.0, 0.65, 0.42, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        # Color and draw the roof
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.26, 0.17, 0.18, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        # Color and draw the windows and the door
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.0, 0.31, 0.31, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)

        glBindVertexArray(0)
