from PIL import Image
from OpenGL.GL import *

def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """
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

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

def load_model(resource, texture_map):
    vertices = []
    textures_coord = []
    normals = []
    materials = []
    current_material = None

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

