#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 17/12/2022
# ---------------------------------------------------------------------------

import glfw
from OpenGL.GL import *
import glm
import math
from draw import draw_models
from transform import *
from model import build_model_defs
from scene import Scene
from shader import Shader
from window import Window

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
            out_fragPos = vec3(model * vec4(position, 1.0));
            out_normal = vec3(model *vec4(normals, 1.0));
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

if __name__ == "__main__":
    window = Window(1600, 1200, "Rock Lee vs Gaara")
    program = Shader(vertex_code, fragment_code).program
    scene = Scene(program)

    scene.prepare()

    def key_event(window, key, scancode, action, mods):
        global scene

        camera = scene.camera

        camera_speed = 0.2
        if key == 87 and (action == 1 or action == 2):  # tecla W
            camera.pos += camera_speed * camera.front

        if key == 83 and (action == 1 or action == 2):  # tecla S
            camera.pos -= camera_speed * camera.front

        if key == 65 and (action == 1 or action == 2):  # tecla A
            camera.pos -= glm.normalize(glm.cross(camera.front, camera.up)) * camera_speed

        if key == 68 and (action == 1 or action == 2):  # tecla D
            camera.pos += glm.normalize(glm.cross(camera.front, camera.up)) * camera_speed

        if key == 80 and action == 1 and scene.polygonal_mode == True:
            scene.polygonal_mode = False
        elif key == 80 and action == 1 and scene.polygonal_mode == False:
            scene.polygonal_mode = True

        camera.pos[0] = max(camera.pos[0], -25) if camera.pos[0] < 0 else min(camera.pos[0], 25)
        camera.pos[1] = max(camera.pos[1], -0.5) if camera.pos[1] < 0 else min(camera.pos[1], 25)
        camera.pos[2] = max(camera.pos[2], -20) if camera.pos[2] < 0 else min(camera.pos[2], 45)

    firstMouse = True
    yaw = -90.0
    pitch = 0.0
    lastX = window.width / 2
    lastY = window.height / 2

    def mouse_event(window, xpos, ypos):
        global scene
        global firstMouse, yaw, pitch, lastX, lastY

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
        scene.camera.front = glm.normalize(front)

    glfw.set_key_callback(window.window, key_event)
    glfw.set_cursor_pos_callback(window.window, mouse_event)

    glfw.show_window(window.window)
    glfw.set_cursor_pos(window.window, lastX, lastY)

    glEnable(GL_DEPTH_TEST)  ### importante para 3D

    angle = 0

    while not glfw.window_should_close(window.window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glClearColor(1.0, 1.0, 1.0, 1.0)

        if scene.polygonal_mode == True:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        angle += 0.00005

        draw_models(program, build_model_defs(angle), scene.resources, scene.texture_map, scene.materials_map)

        mat_view = view(scene.camera.pos, scene.camera.front, scene.camera.up)
        loc_view = glGetUniformLocation(program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

        mat_projection = projection(window.height, window.width)
        loc_projection = glGetUniformLocation(program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

        loc_view_pos = glGetUniformLocation(program, "viewPos")  # recuperando localizacao da variavel viewPos na GPU
        glUniform3f(loc_view_pos, scene.camera.pos[0], scene.camera.pos[1], scene.camera.pos[2])  ### posicao da camera/observador (x,y,z)

        glfw.swap_buffers(window.window)

    glfw.terminate()
