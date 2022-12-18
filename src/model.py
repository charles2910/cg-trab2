import math

class Models:
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
                # 'gaara': {
                #     'position': (270, 1, 0, 0, 3.5, -0.98, 35, 0.005, 0.005, 0.005),
                #     'light': (1, 0.3, 0.9, 64, False)
                # },
                # 'rock_lee': {
                #     'position': (180, 0, 1, 0, 3.5, -0.98, 37, 0.035, 0.035, 0.035),
                #     'light': (1, 0.3, 0.9, 64, False)
                # },
                # 'naruto': {
                #     'position': (270, 1, 0, 0, -2.8, 2.6, 32, 0.006, 0.006, 0.006),
                #     'light': (1, 0.3, 0.9, 64, False)
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
                # 'boat': {
                #     'position': (0, 0, 0, 0,  0, 0, 0, 1, 1, 1),
                #     'light': (1.0, 0.8, 0.5, 250.0, False)
                # },
                # 'knife': {
                #     'position': (180, 0, 1, 0, 0, -1, 25, 3, 3, 3),
                #     'light': (1, 0.3, 0.9, 64, False)
                # },
                # 'rock': {
                #     'position': (0, 0, 1, 0, -7, -1, 10, 0.2, 0.2, 0.2),
                #     'light': (0.6, 1, 0.5, 200, False)
                # },
                # 'sword': {
                #     'position': (0, 0, 0, 0,  0, 0, 0, 1, 1, 1),
                #     'light': (1.0, 0.8, 0.5, 250.0, False)
                # },
                'table': {
                    'position': (180, 0, 1, 0, 0, -1, 25, 3, 3, 3),
                    'light': (1, 0.3, 0.9, 64, False)
                },
                # 'table-with-glass': {
                #     'position': (0, 0, 0, 0,  0, 0, 0, 10, 10, 10),
                #     'light': (1.0, 0.8, 0.5, 250.0, False)
                # },
                'tree-set': {
                    'position': (0, 0, 1, 0, -7, -1, 10, 0.2, 0.2, 0.2),
                    'light': (0.6, 1, 0.5, 200, False)
                },
                # 'voodoo': {
                #     'position': (25, 300, 300, 300, 3.5, -1.001, min(self.angle * 50, 53) - 30, 1, 1, 1),
                #     'light': (0.6, 1, 0.5, 200, False)
                # },
            }
        )
