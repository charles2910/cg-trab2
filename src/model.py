import math

def build_model_defs(angle):
    return dict(
        ## position: angle, r_x, r_y, r_z, t_x, t_Y, t_z, s_x, s_y, s_z
        ## light: ka, kd, ks, ns
        {
            'terrain': {
                'position': (0, 1, 0, 0, 0, -1, 0, 60, 60, 60),
                'light': (0.6, 0.3, 0.7, 1.5, False)
            },
            'chunnin_room': {
                'position': (180, 0, 1, 0, 0, -25.85, 175, 3, 3, 3),
                'light': (0.6, 0.5, 0.5, 200, False)
            },
            'madara': {
                'position': (0, 1, 0, 0, 3.5, -1.001, min(angle *50, 53) - 30, 0.35, 0.35, 0.35),
                'light': (0.6, 1, 0.5, 200, False)
            },
            'gaara': {
                'position': (270, 1, 0, 0, 3.5, -0.98, 35, 0.005, 0.005, 0.005),
                'light': (1, 0.3, 0.9, 64, False)
            },
            'rock_lee': {
                'position': (180, 0, 1, 0, 3.5, -0.98, 37, 0.035, 0.035, 0.035),
                'light': (1, 0.3, 0.9, 64, False)
            },
            'naruto': {
                'position': (270, 1, 0, 0, -2.8, 2.6, 32, 0.006, 0.006, 0.006),
                'light': (1, 0.3, 0.9, 64, False)
            },
            'sky': {
                'position': (0, 1, 0, 0, 0, 0, 0, 60, 60, 60),
                'light': (0.8, 1, 0.2, 0.5, False)
            },
            'sun': {
                'position': (angle, 1, 1, 1, 3.5, math.cos(angle) * 50, math.sin(angle) * 50, 2, 2, 2),
                'light': (1, 1, 1, 1000000, True)
            },
            'street': {
                'position': (0, 1, 0, 0, 3.6, -0.99, 0, 1, 1, 60),
                'light': (0.6, 1, 0.5, 200, False)
            },
            'ramen_shop': {
                'position': (270, 0, 1, 0, 8.5, -1.05, 0, 0.005, 0.005, 0.005),
                'light': (0.8, 1, 1, 200, False)
            }
        }
    )

