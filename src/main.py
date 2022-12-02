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
    attribute vec2 position;
    uniform mat4 mat_transformation;

    void main() {
        gl_Position = mat_transformation * vec4(position, 0.0, 1.0);
    }
    '''

fragment_code = '''
    uniform vec4 color;

    void main() {
        gl_FragColor = color;
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
    def key_event(window,key,scancode,action,mods):
        # Movimentos do barco com as setas
        if key == 265:
            scene.objects["Boat"].translate( 0.00, 0.01) # Cima
            scene.objects["Boat"].scale( 0.99, 0.99) # Fica menor == mais longe
        if key == 264:
            scene.objects["Boat"].translate( 0.00,-0.01) # Baixo
            scene.objects["Boat"].scale( 1.01, 1.01) # Fica maior == mais perto
        if key == 263: scene.objects["Boat"].translate(-0.01, 0.00) # Esquerda
        if key == 262: scene.objects["Boat"].translate( 0.01, 0.00) # Direita

        # Movimentos do Sol com aswd
        if key == 87: scene.objects["Sun"].scale(1.02, 1.02) # Aumenta
        if key == 83: scene.objects["Sun"].scale(0.98, 0.98) # Diminui
        if key == 68: scene.objects["Sun"].translate( 0.01, 0.00) # Direita
        if key == 65: scene.objects["Sun"].translate(-0.01, 0.00) # Esquerda

        # Movimentos da Hélice com qe
        if key == 81: scene.objects["Helix"].rotate(0.03) # roda
        if key == 69: scene.objects["Helix"].rotate(-0.03) # roda

    glfw.set_key_callback(window,key_event)


    # Main window loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        # Set sky color
        glClearColor(0.529, 0.808, 0.922, 1.0)

        # Move clouds through the sky
        scene.objects["Cloud1"].translate(0.001, 0.0)
        scene.objects["Cloud2"].translate(0.001, 0.0)
        scene.objects["Cloud3"].translate(0.001, 0.0)

        scene.draw()

        glfw.swap_buffers(window)

    glfw.terminate()
