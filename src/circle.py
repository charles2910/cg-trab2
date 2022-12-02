#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from object import Object, Color, Coordinates

from OpenGL.GL import *
import numpy as np
import math

class Circle(Object):
    """
        A class used to represent a circle. Child of class Object.

        ...

        Attributes
        ----------
        program : class 'ctypes.c_uint'
        an object to which the shader objects will be attached

        radius: float
        radius of the circle

        coord : class Coordinates
        cartesian coordinates of the center of the circle

        obj_scale: float
        Initial scale of the circle. Defaults to 1.0

        obj_rotation: float
        Initial rotation of the circle in radians from the x axis. Defaults to 0.0

        color: class Color
        Initial color of the circle. Defaults to Color(1.0, 1.0, 1.0)
    """
    def __init__(self, program, radius, coord = Coordinates(0.0, 0.0), obj_scale = 1.0, obj_rotation = 0.0, color = Color(1.0, 1.0, 1.0)):
        super().__init__(program, coord, obj_scale, obj_rotation, color)
        self.num_vertices = 200
        self.radius = radius

    def create(self):
        '''Define 200 vertices to draw the circle in the position especified by the coordinates'''
        vertices = np.zeros(self.num_vertices, [("position", np.float32, 2)])

        # Calcula a coordenada de cada ponto
        for i in range(self.num_vertices):
            angle = (2 * i * math.pi) / 25
            x = (self.radius - .07) * math.cos(angle)
            y = self.radius * math.sin(angle)
            vertices[i] = [x, y]

        return vertices

    def translate(self, t_x, t_y):
        '''Executes a translation with offset (t_x, t_y)'''
        new_x = self.coordinates.x + t_x

        # Condições de controle (respectivamente):
        # - Ao mover, o círculo passará seu centro pela direita da janela?
        # - Ao mover, o círculo passará seu centro pela esquerda da janela?
        # Se sim, condição de contorno: aparecer do outro lado
        if new_x > 1:
            t_x -= 2.0
            new_x = self.coordinates.x + t_x
        if new_x < -1:
            t_x += 2.0
            new_x = self.coordinates.x + t_x

        super().translate(t_x, t_y)
