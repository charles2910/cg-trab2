#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from object import Object, Color, Coordinates

from OpenGL.GL import *
import numpy as np

class ScotchPineTree(Object):
    """
        A class used to represent a scotch pine tree. Child of class Object.

        ...

        Attributes
        ----------
        program : class 'ctypes.c_uint'
        An object to which the shader objects will be attached

        coord : class Coordinates
        Cartesian coordinates of the center of the tree. Defaults to Coordinates(0.0, 0.0)

        obj_scale: float
        Initial scale of the tree. Defaults to 1.0

        obj_rotation: float
        Initial rotation of the tree in radians from the x axis. Defaults to 0.0

        color: class Color
        Initial color of the tree. Defaults to Color(1.0, 1.0, 1.0)
    """
    def __init__(self, program, coord = Coordinates(0.0, 0.0), obj_scale = 1.0, obj_rotation = 0.0, color = Color(1.0, 1.0, 1.0)):
        super().__init__(program, coord, obj_scale, obj_rotation, color)
        self.coordinates = coord
        self.mat_transformation = np.array([1.0, 0.0, 0.0, self.coordinates.x,
                                            0.0, 1.0, 0.0, self.coordinates.y,
                                            0.0, 0.0, 1.0, 0.0,
                                            0.0, 0.0, 0.0, 1.0], np.float32)

    def create(self):
        '''Define the vertex of the scotch pine tree'''
        vertices = np.zeros(13, [("position", np.float32, 2)])

        # Add random componente to differentiate trees
        trunk_width = np.random.rand() / 50.0 - 0.01
        foliage_width = np.random.rand() / 30.0 - 0.0167

        vertices['position'] = [
            # Trunk
            (-0.04 + trunk_width, -0.2),
            (-0.04 + trunk_width, -0.0),
            (-0.08 - trunk_width, -0.0),
            (-0.08 - trunk_width, -0.2),

            # Foliage
            (-0.18 + foliage_width,-0.00),
            (-0.06 + foliage_width, 0.24),
            ( 0.06 - foliage_width, 0.00),
            (-0.18 + foliage_width, 0.08),
            (-0.06 + foliage_width, 0.32),
            ( 0.06 - foliage_width, 0.08),
            (-0.18 + foliage_width, 0.16),
            (-0.06, 0.40),
            ( 0.06 - foliage_width, 0.16),
        ]
        return vertices

    def draw(self):
        '''Draw the scotch pine tree in the window with the proper colors'''
        glBindVertexArray(self.vao)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mat_transformation"), 1, GL_TRUE, self.mat_transformation)

        # Color and draw the trunk
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.4, 0.2, 0.0, 1.0)
        glDrawArrays(GL_POLYGON, 0, 4)
        # Color and draw the foliage
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.0, 0.5, 0.0, 1.0)
        glDrawArrays(GL_POLYGON, 4, 3)
        glDrawArrays(GL_POLYGON, 7, 3)
        glDrawArrays(GL_POLYGON, 10, 3)

        glBindVertexArray(0)

class SugarPineTree(Object):
    """
        A class used to represent a sugar pine tree. Child of class Object.

        ...

        Attributes
        ----------
        program : class 'ctypes.c_uint'
        an object to which the shader objects will be attached
    """
    def __init__(self, program, coord = Coordinates(0.0, 0.0), obj_scale = 1.0, obj_rotation = 0.0, color = Color(1.0, 1.0, 1.0)):
        super().__init__(program, coord, obj_scale, obj_rotation, color)

    def create(self):
        '''Define the vertex of the sugar pine tree'''
        vertices = np.zeros(7, [("position", np.float32, 2)])

        # Add random componente to differentiate trees
        trunk_width = np.random.rand() / 50.0 - 0.01
        foliage_width = np.random.rand() / 30.0 - 0.0167
        foliage_height = np.random.rand() / 20.0 - 0.025

        vertices['position'] = [
            # Trunk
            (0.65 + trunk_width, 0.0),
            (0.65 + trunk_width, 0.12),
            (0.71 - trunk_width, 0.12),
            (0.71 - trunk_width, 0.0),

            # Foliage
            (0.80 + foliage_width, 0.12),
            (0.56 - foliage_width, 0.12),
            (0.68, 0.5 + foliage_height),
        ]
        return vertices

    def draw(self):
        '''Draw the sugar pine tree in the window with the proper colors'''
        glBindVertexArray(self.vao)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mat_transformation"), 1, GL_TRUE, self.mat_transformation)

        # Color and draw the trunk
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.4, 0.2, 0.0, 1.0)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        # Color and draw the foliage
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.0, 0.5, 0.0, 1.0)
        glDrawArrays(GL_TRIANGLES, 4, 3)

        glBindVertexArray(0)
