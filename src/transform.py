#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 17/12/2022
# ---------------------------------------------------------------------------

import glm
import math
import numpy as np

class Coordinates:
    """
        A class used to represent a cartesian coordinate.

        ...
        Attributes
        ----------
        x : float
        x coordinate

        y : float
        y coordinate

        z : float
        z coordinate
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Camera:
    """
        A class used to represent a camera position.

        ...
        Attributes
        ----------
        pos : float
        position of the camera

        front : float
        front parameter of the camera

        up : float
        up parameter of the camera
    """
    def __init__(self, pos, front, up):
        self.pos = pos
        self.front = front
        self.up = up

class Transform:
    """A class that groups all the view pipeline matrix. """
    def __init__(self):
        pass

    def model(self, angle, r, t, s):
        """Return the model matrix"""
        angle = math.radians(angle)
        mat = glm.mat4(1.0)

        mat = glm.translate(mat, glm.vec3(t.x, t.y, t.z))
        mat = glm.rotate(mat, angle, glm.vec3(r.x, r.y, r.z))
        mat = glm.scale(mat, glm.vec3(s.x, s.y, s.z))

        return np.array(mat)

    def view(self, camera : Camera):
        """Return the view matrix"""
        mat = glm.lookAt(camera.pos, camera.pos + camera.front, camera.up);
        return np.array(mat)

    def projection(self, height, width):
        """Return the projection matrix"""

        # perspective parameters: fovy, aspect, near, far
        mat = glm.perspective(glm.radians(45.0), width / height, 0.1, 1000.0)
        return np.array(mat)
