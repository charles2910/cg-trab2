#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from object import Object, Color, Coordinates

from OpenGL.GL import *
import numpy as np

class Boat(Object):
    """
        A class used to represent the boat. Child of class Object.

        ...

        Attributes
        ----------
        program : class 'ctypes.c_uint'
        An object to which the shader objects will be attached

        coord : class Coordinates
        Cartesian coordinates of the center of the boat. Defaults to Coordinates(0.0, 0.0)

        obj_scale: float
        Initial scale of the boat. Defaults to 1.0

        obj_rotation: float
        Initial rotation of the boat in radians from the x axis. Defaults to 0.0

        color: class Color
        Initial color of the boat. Defaults to Color(1.0, 1.0, 1.0)
    """
    def __init__(self, program, coord = Coordinates(0.0, 0.0), obj_scale = 1.0, obj_rotation = 0.0, color = Color(1.0, 1.0, 1.0)):
        super().__init__(program, coord, obj_scale, obj_rotation, color)

    def create(self):
        '''Define the vertex of the boat'''
        vertices = np.zeros(11, [("position", np.float32, 2)])
        vertices['position'] = [
            # Hull
            (-0.16, -0.12),
            (-0.22,  0.00),
            ( 0.22,  0.00),
            ( 0.16, -0.12),

            # Sail
            ( 0.00,  0.02),
            (-0.26,  0.02),
            ( 0.00,  0.20),

            # Mast
            ( 0.00,  0.00),
            ( 0.00,  0.20),
            ( 0.04,  0.00),
            ( 0.04,  0.20),
        ]
        return vertices

    def draw(self):
        '''Draw the boat in the window with the proper colors'''
        glBindVertexArray(self.vao)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "mat_transformation"), 1, GL_TRUE, self.mat_transformation)

        # Color and draw the hull
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.0, 0.0, 0.5, 1.0)
        glDrawArrays(GL_QUADS, 0, 4)
        # Color and draw the sail
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.7, 0.2, 0.2, 1.0)
        glDrawArrays(GL_TRIANGLE_STRIP, 4, 3)
        # Color and draw the mast
        glUniform4f(glGetUniformLocation(self.program, "color"), 0.2, 0.3, 0.3, 1.0)
        glDrawArrays(GL_TRIANGLE_STRIP, 7, 4)

        glBindVertexArray(0)

    def translate(self, t_x, t_y):
        '''Executes a translation with offset (t_x, t_y)'''
        new_x = self.coordinates.x + t_x
        new_y = self.coordinates.y + t_y

        # Condições de controle (respectivamente):
        # - Ao mover, o barco passará seu centro pela direita da janela?
        # - Ao mover, o barco passará seu centro pela esquerda da janela?
        # - Ao mover, o barco passará seu centro para baixo da janela?
        # - Ao mover, o barco passará seu centro para o gramado?
        # Se sim, condição de contorno: aparecer do outro lado (direita ou esquerda)
        # ou ficar parado (para cima e para baixo)
        if new_x > 1:
            t_x -= 2.0
            new_x = self.coordinates.x + t_x
        if new_x < -1:
            t_x += 2.0
            new_x = self.coordinates.x + t_x
        if new_y < -0.89:
            t_y = 0.0
        elif new_y - 0.1 * new_x > -0.6:
            t_y = 0.0
            t_x = 0.0
        super().translate(t_x, t_y)

    def scale(self, s_x, s_y):
        '''Multiply the current matrix by the scale matrix (s_x, s_x). Keep ratio s_y = s_x'''
        new_scale = self.obj_scale * s_x
        # Limita o quanto o barco pode crescer ou diminuir
        if new_scale > 1.13:
            s_x = 1.0
        elif new_scale < 0.77:
            s_x = 1.0
        super().scale(s_x, s_x)
