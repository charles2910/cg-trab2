import numpy as np
import glm
from OpenGL.GL import *
from loader import load_models
from model import Models
from resources import build_resources, create_texture_path
from transform import Camera, Transform, Coordinates

class Scene:
    def __init__(self, window, program):
        self.program = program
        self.window = window
        self.resources = build_resources()
        self.models = Models()
        self.transform = Transform()
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

    def draw_model(self, model_name, model):
        (start_index, end_index) = self.resources[model_name]['position']
        materials = self.materials_map[model_name]

        r = Coordinates(0.0, 0.0, 0.0)
        s = Coordinates(0.0, 0.0, 0.0)
        t = Coordinates(0.0, 0.0, 0.0)

        # aplica a matriz model
        (angle, r.x, r.y, r.z, t.x, t.y, t.z, s.x, s.y, s.z) = model['position']
        (ka, kd, ks, ns, is_source) = model['light']

        mat_model = self.transform.model(angle, r, t, s)
        loc_model = glGetUniformLocation(self.program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        loc_ka = glGetUniformLocation(self.program, "ka")  # recuperando localizacao da variavel ka na GPU
        glUniform1f(loc_ka, ka)  ### envia ka pra gpu

        loc_kd = glGetUniformLocation(self.program, "kd")  # recuperando localizacao da variavel kd na GPU
        glUniform1f(loc_kd, kd)  ### envia kd pra gpu

        loc_ks = glGetUniformLocation(self.program, "ks")  # recuperando localizacao da variavel ks na GPU
        glUniform1f(loc_ks, ks)  ### envia ks pra gpu

        loc_ns = glGetUniformLocation(self.program, "ns")  # recuperando localizacao da variavel ns na GPU
        glUniform1f(loc_ns, ns)  ### envia ns pra gpu

        if (is_source):
            loc_light_pos = glGetUniformLocation(self.program, "lightPos")  # recuperando localizacao da variavel lightPos na GPU
            glUniform3f(loc_light_pos, t.x, t.y, t.z)  ### posicao da fonte de luz

        for i in range(len(materials)):
            texture = create_texture_path(model_name, materials[i]['texture'])
            glBindTexture(GL_TEXTURE_2D, self.texture_map[texture])
            start_texture_index = start_index + materials[i]['offset']
            size = materials[i + 1]['offset'] - materials[i]['offset'] if i + 1 < len(materials) else end_index - start_texture_index
            glDrawArrays(GL_TRIANGLES, start_texture_index, size)


    def draw_models(self):
        models = self.models.build()
        for model in models:
            self.draw_model(model, models[model])

    def draw(self):
        if self.polygonal_mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        self.models.angle += 0.00008

        self.draw_models()

        mat_view = self.transform.view(self.camera)
        loc_view = glGetUniformLocation(self.program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

        mat_projection = self.transform.projection(self.window.height, self.window.width)
        loc_projection = glGetUniformLocation(self.program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

        loc_view_pos = glGetUniformLocation(self.program, "viewPos")  # recuperando localizacao da variavel viewPos na GPU
        glUniform3f(loc_view_pos, self.camera.pos[0], self.camera.pos[1], self.camera.pos[2])  ### posicao da camera/observador (x,y,z)
