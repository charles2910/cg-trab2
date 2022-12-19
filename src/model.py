#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 17/12/2022
# ---------------------------------------------------------------------------

import math

class Models:
    """
        A class used to define the position and light of all the models involved.
        ...
        Attributes
        ----------
        angle : float
        parameter to move models, such as the sun
    """
    def __init__(self):
        self.angle = 0

    def build(self):
        return dict(
            ## position: angle, r_x, r_y, r_z, t_x, t_Y, t_z, s_x, s_y, s_z
            ## light: ka, kd, ks, ns
            {
                'terrain': {
                    'position': (0, 1, 0, 0, 0, -1, 0, 60, 60, 60),
                    'light': (0.6, 0.3, 0.7, 1.5, False)
                },
                'abandoned-cottage-house': {
                    'position': (180, 0, 1, 0, 0, -1, 25, 0.5, 0.5, 0.5),
                    'light': (0.6, 1, 0.5, 200, False)
                },
                # 'madara': {
                #     'position': (0, 1, 0, 0, 3.5, -1.001, min(self.angle * 50, 53) - 30, 0.35, 0.35, 0.35),
                #     'light': (0.6, 1, 0.5, 200, False)
                # },
                'sky': {
                    'position': (0, 1, 0, 0, 0, 0, 0, 60, 60, 60),
                    'light': (0.8, 1, 0.2, 0.5, False)
                },
                'sun': {
                    'position': (self.angle, 1, 1, 1, 3.5, math.cos(self.angle) * 50, math.sin(self.angle) * 50, 2, 2, 2),
                    'light': (1, 1, 1, 1000000, True)
                },
                'street': {
                    'position': (0, 1, 0, 0, -4.3, -0.99, 0, 0.8, 1, 80),
                    'light': (0.6, 1, 0.5, 200, False)
                },
                'wooden-watch-tower': {
                    'position': (180, 0, 1, 0, 8.5, -1.8, 0, 1, 1, 1),
                    'light': (0.6, 1, 0.5, 200, False)
                },
                'boat': {
                    'position': (0, 1, 1, 0,  0, -0.9, 15, 0.4, 0.4, 0.4),
                    'light': (1.0, 0.8, 0.5, 250.0, False)
                },
                #'knife': {
                #    'position': (180, 0, 1, 0, 0, 0, 25, 3, 3, 3),
                #    'light': (1, 0.3, 0.9, 64, False)
                #},
                'rock': {
                    'position': (0, 0, 1, 0, -7, -1, 9, 0.2, 0.2, 0.2),
                    'light': (0.6, 1, 0.5, 200, False)
                },
                'sword': {
                    'position': (210, 0, 1, 0, 0, 0.1, 25, 0.025, 0.025, 0.025),
                    'light': (1, 0.8, 0.5, 100, False)
                },
                'table': {
                    'position': (180, 0, 1, 0, 0, -0.5, 25, 3, 3, 3),
                    'light': (1, 0.8, 0.5, 100, False)
                },
                'table-with-glass': {
                    'position': (0, 0, 1, 0,  5, -0.5, 21.6, 1.5, 1.5, 1.5),
                    'light': (1.0, 0.8, 0.5, 250.0, False)
                },
                # 'table-with-glass': {
                #     'position': (0, 0, 0, 0,  0, 0, 25, 3, 3, 3),
                #     'light': (1.0, 0.8, 0.5, 250.0, False)
                # },
                'tree-set': {
                    'position': (0, 0, 1, 0, -7, -1, 10, 0.2, 0.2, 0.2),
                    'light': (0.6, 1, 0.5, 200, False)
                },
                'voodoo': {
                    'position': (0, 1, 1.5, 1, -4.5, -1.001, min(self.angle * 50, 53) - 30, 1, 1, 1),
                    'light': (0.6, 1, 0.5, 200, False)
                },
            }
        )
