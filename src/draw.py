from OpenGL.GL import *
from resources import create_texture_path
from transform import Transform, Coordinates

def draw_model(program, model_name, model, resource, texture_map, materials):
    model_position = model['position']
    model_light = model['light']
    (start_index, end_index) = resource['position']

    transform = Transform()
    r = Coordinates(0.0, 0.0, 0.0)
    s = Coordinates(0.0, 0.0, 0.0)
    t = Coordinates(0.0, 0.0, 0.0)

    # aplica a matriz model
    (angle, r.x, r.y, r.z, t.x, t.y, t.z, s.x, s.y, s.z) = model_position
    (ka, kd, ks, ns, is_source) = model_light

    mat_model = transform.model(angle, r, t, s)
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
        glUniform3f(loc_light_pos, t.x, t.y, t.z)  ### posicao da fonte de luz

    for i in range(len(materials)):
        texture = create_texture_path(model_name, materials[i]['texture'])
        texture_id = texture_map[texture]
        glBindTexture(GL_TEXTURE_2D, texture_id)
        start_texture_index = start_index + materials[i]['offset']
        size = materials[i + 1]['offset'] - materials[i]['offset'] if i + 1 < len(
            materials) else end_index - start_texture_index
        glDrawArrays(GL_TRIANGLES, start_texture_index, size)


def draw_models(program, models, resources, texture_map, materials_map):
    for model in models:
        draw_model(program, model, models[model], resources[model], texture_map, materials_map[model])
