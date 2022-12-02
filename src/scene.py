#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from houses import RedHouse, GreenHouse
from mountains import Mountains
from sun import Sun
from field import Field
from river import River
from tree import ScotchPineTree, SugarPineTree
from boat import Boat
from clouds import Cloud
from windmill import Windmill
from helix import Helix
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
            "Sun": Sun(program),
            "River": River(program),
            "Field": Field(program),
            "Mountains": Mountains(program),
            "RedHouse": RedHouse(program),
            "GreenHouse": GreenHouse(program),
            "SugarTreePine1": SugarPineTree(program),
            "ScotchTreePine1": ScotchPineTree(program, Coordinates( -0.3 , 0.0)),
            "ScotchTreePine2": ScotchPineTree(program, Coordinates( 0.89 , -0.24)),
            "Cloud1": Cloud(program, 0.0),
            "Cloud2": Cloud(program, 1.1),
            "Cloud3": Cloud(program, 1.5),
            "Windmill": Windmill(program, Coordinates( 0.27 , -0.42)),
            "Helix": Helix(program, Coordinates( -0.03 , 0.03)),
            "Boat": Boat(program, Coordinates( 0.65 , -0.75))
        }

    def prepare(self):
        '''Prepare all the objects in the scene'''
        for key in self.objects:
            self.objects[key].prepare()

    def draw(self):
        '''Draw all the objects in the scene'''
        for key in self.objects:
            self.objects[key].draw()
