#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 17/12/2022
# ---------------------------------------------------------------------------

import glfw
from OpenGL.GL import *
import numpy as np
import glm
import math
from PIL import Image

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
altura = 1200
largura = 1600
window = glfw.create_window(largura, altura, "Rock Lee vs Gaara", None, None)
glfw.make_context_current(window)

vertex_code = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        attribute vec3 normals;


        varying vec2 out_texture;
        varying vec3 out_fragPos;
        varying vec3 out_normal;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
            out_fragPos = vec3(  model * vec4(position, 1.0));
            out_normal = vec3( model *vec4(normals, 1.0));
        }
        """

fragment_code = """

        // parametro com a cor da(s) fonte(s) de iluminacao
        uniform vec3 lightPos; // define coordenadas de posicao da luz
        vec3 lightColor = vec3(1.0, 1.0, 1.0);

        // parametros da iluminacao ambiente e difusa
        uniform float ka; // coeficiente de reflexao ambiente
        uniform float kd; // coeficiente de reflexao difusa

        // parametros da iluminacao especular
        uniform vec3 viewPos; // define coordenadas com a posicao da camera/observador
        uniform float ks; // coeficiente de reflexao especular
        uniform float ns; // expoente de reflexao especular



        // parametros recebidos do vertex shader
        varying vec2 out_texture; // recebido do vertex shader
        varying vec3 out_normal; // recebido do vertex shader
        varying vec3 out_fragPos; // recebido do vertex shader
        uniform sampler2D samplerTexture;



        void main(){

            // calculando reflexao ambiente
            vec3 ambient = ka * lightColor;

            // calculando reflexao difusa
            vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
            vec3 lightDir = normalize(lightPos - out_fragPos); // direcao da luz
            float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
            vec3 diffuse = kd * diff * lightColor; // iluminacao difusa

            // calculando reflexao especular
            vec3 viewDir = normalize(viewPos - out_fragPos); // direcao do observador/camera
            vec3 reflectDir = normalize(reflect(-lightDir, norm)); // direcao da reflexao
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
            vec3 specular = ks * spec * lightColor;

            // aplicando o modelo de iluminacao
            vec4 texture = texture2D(samplerTexture, out_texture);
            vec4 result = vec4((ambient + diffuse + specular),1.0) * texture; // aplica iluminacao
            gl_FragColor = result;

        }
        """

# Request a program and shader slots from GPU
program = glCreateProgram()
vertex = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)

# Set shaders source
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)

# Compile shaders
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")

glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")

# Attach shader objects to the program
glAttachShader(program, vertex)
glAttachShader(program, fragment)

# Build program
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')

# Make program the default program
glUseProgram(program)

def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """
    objects = {}
    vertices = []
    normals = []
    texture_coords = []
    faces = []

    material = None

    # abre o arquivo obj para leitura
    for line in open(filename, "r"):  ## para cada linha do arquivo .obj
        if line.startswith('#'): continue  ## ignora comentarios
        values = line.split()  # quebra a linha por espaço
        if not values: continue

        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(values[1:4])

        ### recuperando vertices
        if values[0] == 'vn':
            normals.append(values[1:4])

        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces
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

glEnable(GL_TEXTURE_2D)

def load_texture_from_file(texture_id, img_textura):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    img = Image.open(img_textura)
    img_width = img.size[0]
    img_height = img.size[1]
    image_data = img.tobytes("raw", "RGB", 0, -1)
    #image_data = np.array(list(img.getdata()), np.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

from os import listdir, getcwd
from os.path import isfile, join, dirname

RESOURCES_PATH = join(getcwd(), 'resources')

def list_resources():
    path = RESOURCES_PATH
    return [f for f in listdir(path) if not isfile(join(path, f))]


def create_texture_path(resource, texture):
    path = join(RESOURCES_PATH, resource, 'textures', texture)
    return path


def list_textures(resource):
    path = create_texture_path(resource, '')
    return [create_texture_path(resource, f) for f in listdir(path) if isfile(join(path, f))]


def create_obj_path(resource):
    return join(RESOURCES_PATH, resource, 'figure.obj')


def build_resources():
    metadata = dict()
    resources = list_resources()
    for resource in resources:
        metadata[resource] = {
            'obj': create_obj_path(resource),
            'textures': list_textures(resource)
        }

    return metadata

def load_model(resource, texture_map):
    vertices = []
    textures_coord = []
    normals = []
    materials = []
    current_material = None

    objects_map = dict()
    glGenTextures(len(resource['textures']))

    # Read textures
    for i in range(len(resource['textures'])):
        texture = resource['textures'][i]
        texture_map[texture] = len(texture_map)
        texture_id = texture_map[texture]
        load_texture_from_file(texture_id, texture)

    model = load_model_from_file(resource['obj'])
    # Read OBJ
    for face in model['faces']:
        if (face[3] != current_material):
            current_material = face[3];
            materials.append(dict({'texture': current_material, 'offset': len(vertices)}))
        for vertice_id in face[0]:
            vertices.append(model['vertices'][vertice_id - 1])

        for texture_id in face[1]:
            textures_coord.append(model['texture'][texture_id - 1])
        for normal_id in face[2]:
            normals.append(model['normals'][normal_id - 1])

    return vertices, textures_coord, normals, materials, texture_map


def load_models(resources):
    vertices_list = []
    normals_list = []
    textures_coord_list = []
    materials_map = dict()
    texture_map = dict()
    for resource in resources:
        start_position = len(vertices_list)
        print(f'Processando modelo {resource}. Vertice inicial:', start_position)
        vertices, texture_coord, normals, materials, texture_map = load_model(resources[resource], texture_map)
        materials_map[resource] = materials
        normals_list = normals_list + normals
        vertices_list = vertices_list + vertices
        textures_coord_list = textures_coord_list + texture_coord
        end_position = len(vertices_list)
        resources[resource]['position'] = (start_position, end_position)
        print(f'Processando modelo {resource}. Vertice final:', end_position)

    return vertices_list, textures_coord_list, normals_list, resources, texture_map, materials_map

vertices_list, textures_coord_list, normals_list, resources, texture_map, materials_map = load_models(build_resources())

# Request a buffer slot from GPU
buffer = glGenBuffers(3)

vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
vertices['position'] = vertices_list

# Upload data
glBindBuffer(GL_ARRAY_BUFFER, buffer[0])
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)
loc_vertices = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc_vertices)
glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)

textures = np.zeros(len(textures_coord_list), [("position", np.float32, 2)])  # duas coordenadas
textures['position'] = textures_coord_list

# Upload data
glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
stride = textures.strides[0]
offset = ctypes.c_void_p(0)
loc_texture_coord = glGetAttribLocation(program, "texture_coord")
glEnableVertexAttribArray(loc_texture_coord)
glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)

normals = np.zeros(len(normals_list), [("position", np.float32, 3)])  # três coordenadas
normals['position'] = normals_list

# Upload coordenadas normals de cada vertice
glBindBuffer(GL_ARRAY_BUFFER, buffer[2])
glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
stride = normals.strides[0]
offset = ctypes.c_void_p(0)
loc_normals_coord = glGetAttribLocation(program, "normals")
glEnableVertexAttribArray(loc_normals_coord)
glVertexAttribPointer(loc_normals_coord, 3, GL_FLOAT, False, stride, offset)

def draw_model(model_name, model_position, model_light, resource, texture_map, materials):
    (start_index, end_index) = resource['position']

    # aplica a matriz model
    (angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z) = model_position
    (ka, kd, ks, ns, is_source) = model_light

    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

    loc_ka = glGetUniformLocation(program, "ka")  # recuperando localizacao da variavel ka na GPU
    glUniform1f(loc_ka, ka)  ### envia ka pra gpu

    loc_kd = glGetUniformLocation(program, "kd")  # recuperando localizacao da variavel kd na GPU
    glUniform1f(loc_kd, kd)  ### envia kd pra gpu

    loc_ks = glGetUniformLocation(program, "ks")  # recuperando localizacao da variavel ks na GPU
    glUniform1f(loc_ks, ks)  ### envia ks pra gpu

    loc_ns = glGetUniformLocation(program, "ns")  # recuperando localizacao da variavel ns na GPU
    glUniform1f(loc_ns, ns)  ### envia ns pra gpu

    if (is_source):
        loc_light_pos = glGetUniformLocation(program, "lightPos")  # recuperando localizacao da variavel lightPos na GPU
        glUniform3f(loc_light_pos, t_x, t_y, t_z)  ### posicao da fonte de luz

    for i in range(len(materials)):
        texture = create_texture_path(model_name, materials[i]['texture'])
        texture_id = texture_map[texture]
        glBindTexture(GL_TEXTURE_2D, texture_id)
        start_texture_index = start_index + materials[i]['offset']
        size = materials[i + 1]['offset'] - materials[i]['offset'] if i + 1 < len(
            materials) else end_index - start_texture_index
        glDrawArrays(GL_TRIANGLES, start_texture_index, size)


def draw_models(models, resources, texture_map, materials_map):
    for model in models:
        draw_model(model, models[model]['position'], models[model]['light'], resources[model], texture_map,
                   materials_map[model])

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

cameraPos = glm.vec3(0.0, 0.0, 1.0);
cameraFront = glm.vec3(0.0, 0.0, -1.0);
cameraUp = glm.vec3(0.0, 1.0, 0.0);

polygonal_mode = False

def key_event(window, key, scancode, action, mods):
    global cameraPos, cameraFront, cameraUp, polygonal_mode

    cameraSpeed = 0.2
    if key == 87 and (action == 1 or action == 2):  # tecla W
        cameraPos += cameraSpeed * cameraFront

    if key == 83 and (action == 1 or action == 2):  # tecla S
        cameraPos -= cameraSpeed * cameraFront

    if key == 65 and (action == 1 or action == 2):  # tecla A
        cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed

    if key == 68 and (action == 1 or action == 2):  # tecla D
        cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed

    if key == 80 and action == 1 and polygonal_mode == True:
        polygonal_mode = False
    else:
        if key == 80 and action == 1 and polygonal_mode == False:
            polygonal_mode = True

    cameraPos[0] = max(cameraPos[0], -25) if cameraPos[0] < 0 else min(cameraPos[0], 25)
    cameraPos[1] = max(cameraPos[1], -0.5) if cameraPos[1] < 0 else min(cameraPos[1], 25)
    cameraPos[2] = max(cameraPos[2], -20) if cameraPos[2] < 0 else min(cameraPos[2], 45)

firstMouse = True
yaw = -90.0
pitch = 0.0
lastX = largura / 2
lastY = altura / 2


def mouse_event(window, xpos, ypos):
    global firstMouse, cameraFront, yaw, pitch, lastX, lastY
    if firstMouse:
        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos
    lastX = xpos
    lastY = ypos

    sensitivity = 0.3
    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset;
    pitch += yoffset;

    if pitch >= 90.0: pitch = 90.0
    if pitch <= -90.0: pitch = -90.0

    front = glm.vec3()
    front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    front.y = math.sin(glm.radians(pitch))
    front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    cameraFront = glm.normalize(front)


glfw.set_key_callback(window, key_event)
glfw.set_cursor_pos_callback(window, mouse_event)

def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    angle = math.radians(angle)

    matrix_transform = glm.mat4(1.0)  # instanciando uma matriz identidade

    # aplicando translacao
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))

    # aplicando rotacao
    matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))

    # aplicando escala
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))

    matrix_transform = np.array(matrix_transform)

    return matrix_transform


def view():
    global cameraPos, cameraFront, cameraUp
    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
    mat_view = np.array(mat_view)
    return mat_view


def projection():
    global altura, largura
    # perspective parameters: fovy, aspect, near, far
    mat_projection = glm.perspective(glm.radians(45.0), largura / altura, 0.1, 1000.0)
    mat_projection = np.array(mat_projection)
    return mat_projection

glfw.show_window(window)
glfw.set_cursor_pos(window, lastX, lastY)

glEnable(GL_DEPTH_TEST)  ### importante para 3D

angle = 0
while not glfw.window_should_close(window):

    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glClearColor(1.0, 1.0, 1.0, 1.0)

    if polygonal_mode == True:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    if polygonal_mode == False:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    angle = (angle + 0.00005)

    draw_models(build_model_defs(angle), resources, texture_map, materials_map)

    mat_view = view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)


    mat_projection = projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

    loc_view_pos = glGetUniformLocation(program, "viewPos")  # recuperando localizacao da variavel viewPos na GPU
    glUniform3f(loc_view_pos, cameraPos[0], cameraPos[1], cameraPos[2])  ### posicao da camera/observador (x,y,z)

    glfw.swap_buffers(window)

glfw.terminate()