#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from object import Object, Color, Coordinates

import numpy as np

class River(Object):
    """
        A class used to represent the river. Child of class Object.

        ...

        Attributes
        ----------
        program : class 'ctypes.c_uint'
        An object to which the shader objects will be attached

        coord : class Coordinates
        Cartesian coordinates of the center of the river. Defaults to Coordinates(0.0, 0.0)

        obj_scale: float
        Initial scale of the river. Defaults to 1.0

        obj_rotation: float
        Initial rotation of the river in radians from the x axis. Defaults to 0.0

        color: class Color
        Initial color of the river. Defaults to Color(0.255, 0.412, 0.882)
    """
    def __init__(self, program, coord = Coordinates(0.0, 0.0), obj_scale = 1.0, obj_rotation = 0.0, color = Color(0.255, 0.412, 0.882)):
        super().__init__(program, coord, obj_scale, obj_rotation, color)

    def create(self):
        '''Define the vertex of the river'''
        vertices = np.zeros(4, [("position", np.float32, 2)])
        vertices['position'] = [
            (-1.0, -1.0),
            (-1.0, -0.7),
            (1.0, -0.5),
            (1.0, -1.0),
        ]
        return vertices
