#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from object import Color, Coordinates

class Scene:
    """
        A class used to group all objects in the scene.

        ...

        Attributes
        ----------
        program : class 'ctypes.c_uint'
        an object to which the shader objects will be attached
    """
    def __init__(self, program):
        # List of all the objects in the scene
        self.objects = {
        }

    def prepare(self):
        '''Prepare all the objects in the scene'''
        for key in self.objects:
            self.objects[key].prepare()

    def draw(self):
        '''Draw all the objects in the scene'''
        for key in self.objects:
            self.objects[key].draw()
