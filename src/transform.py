import glm
import math
import numpy as np

class Coordinates:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Camera:
    def __init__(self, pos, front, up):
        self.pos = pos
        self.front = front
        self.up = up

class Transform:
    def __init__(self):
        pass

    def model(self, angle, r, t, s):
        angle = math.radians(angle)
        mat = glm.mat4(1.0)

        mat = glm.translate(mat, glm.vec3(t.x, t.y, t.z))
        mat = glm.rotate(mat, angle, glm.vec3(r.x, r.y, r.z))
        mat = glm.scale(mat, glm.vec3(s.x, s.y, s.z))

        return np.array(mat)

    def view(self, camera : Camera):
        mat = glm.lookAt(camera.pos, camera.pos + camera.front, camera.up);
        return np.array(mat)

    def projection(self, height, width):
        # perspective parameters: fovy, aspect, near, far
        mat = glm.perspective(glm.radians(45.0), width / height, 0.1, 1000.0)
        return np.array(mat)
