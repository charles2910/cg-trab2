#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from OpenGL.GL import *
import OpenGL.GL.shaders

class Shader:
    """
        A class used to process the vertex and fragment shaders.

        ...

        Attributes
        ----------
        vertex_code : str
        GLSL vertex shader code

        fragment_code : str
        GLSL fragment shader code
    """
    def __init__(self, vertex_code: str, fragment_code: str):
        # Request a program and shader slots from GPU
        self.program = glCreateProgram()
        vertex = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        # Set shaders source
        glShaderSource(vertex, vertex_code)
        glShaderSource(fragment, fragment_code)

        # Compile shaders
        glCompileShader(vertex)
        if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex).decode()
            raise RuntimeError(error)

        glCompileShader(fragment)
        if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment).decode()
            raise RuntimeError(error)

        # Attach shader objects to the program
        glAttachShader(self.program, vertex)
        glAttachShader(self.program, fragment)

        # Build program
        glLinkProgram(self.program)
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            raise RuntimeError(glGetProgramInfoLog(self.program))

        # Make program the default program
        glUseProgram(self.program)

    def load_model_from_file(filename):
        """Loads a Wavefront OBJ file. """
        vertices = []
        normals = []
        texture_coords = []
        faces = []

        material = None

        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue

            if values[0] == 'v':
                vertices.append(values[1:4])

            if values[0] == 'vn':
                normals.append(values[1:4])

            elif values[0] == 'vt':
                texture_coords.append(values[1:3])

            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'f':
                face = []
                face_texture = []
                face_normals = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    face_normals.append(int(w[2]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)

                faces.append((face, face_texture, face_normals, material))

        model = {}
        model['vertices'] = vertices
        model['texture'] = texture_coords
        model['faces'] = faces
        model['normals'] = normals

        return model
