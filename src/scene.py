from OpenGL.GL import *
import numpy as np
import glm
from loader import load_models
from resources import build_resources

class Camera:
    def __init__(self, pos, front, up):
        self.pos = pos
        self.front = front
        self.up = up

class Scene:
    def __init__(self, program):
        self.program = program
        self.resources = build_resources()
        self.camera = Camera(
            glm.vec3(0.0, 0.0, 1.0),
            glm.vec3(0.0, 0.0, -1.0),
            glm.vec3(0.0, 1.0, 0.0)
        )
        self.polygonal_mode = False

    def prepare(self):
        vertices_list, textures_coord_list, normals_list, resources, texture_map, materials_map = load_models(self.resources)

        self.resources = resources
        self.texture_map = texture_map
        self.materials_map = materials_map

        # Request a buffer slot from GPU
        buffer = glGenBuffers(3)

        vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
        vertices['position'] = vertices_list

        # Upload data
        glBindBuffer(GL_ARRAY_BUFFER, buffer[0])
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)

        textures = np.zeros(len(textures_coord_list), [("position", np.float32, 2)])
        textures['position'] = textures_coord_list

        # Upload data
        glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
        glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
        stride = textures.strides[0]
        offset = ctypes.c_void_p(0)
        loc_texture_coord = glGetAttribLocation(self.program, "texture_coord")
        glEnableVertexAttribArray(loc_texture_coord)
        glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)

        normals = np.zeros(len(normals_list), [("position", np.float32, 3)])
        normals['position'] = normals_list

        # Upload coordenadas normals de cada vertice
        glBindBuffer(GL_ARRAY_BUFFER, buffer[2])
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        stride = normals.strides[0]
        offset = ctypes.c_void_p(0)
        loc_normals_coord = glGetAttribLocation(self.program, "normals")
        glEnableVertexAttribArray(loc_normals_coord)
        glVertexAttribPointer(loc_normals_coord, 3, GL_FLOAT, False, stride, offset)

