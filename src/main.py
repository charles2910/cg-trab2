#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

from scene import Scene
from shaders import Shader
from window import Window

import glfw
from OpenGL.GL import *

vertex_code = '''
    attribute vec3 position;
    attribute vec2 texture_coord;
    attribute vec3 normals;

    varying vec2 out_texture;
    varying vec3 out_fragPos;
    varying vec3 out_normal;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    void main() {
        gl_Position = projection * view * model * vec4(position,1.0);
        out_texture = vec2(texture_coord);
        out_fragPos = vec3(model * vec4(position, 1.0));
        out_normal = normals;
    }
    '''

fragment_code = '''
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

    void main() {
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
    '''

if __name__ == "__main__":
    window = Window(1200, 700, "Paisagem").window
    program = Shader(vertex_code, fragment_code).program

    # Create and prepare all scene objects
    scene = Scene(program)
    scene.prepare()

    glfw.show_window(window)

    # Cria listener para teclas e define ações para cada uma delas
    def key_event(window, key, scancode, action, mods):
        pass

    glfw.set_key_callback(window,key_event)


    # Main window loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        # Set sky color
        glClearColor(0.529, 0.808, 0.922, 1.0)

        scene.draw()

        glfw.swap_buffers(window)

    glfw.terminate()
