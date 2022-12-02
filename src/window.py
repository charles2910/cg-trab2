#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By: Carlos Henrique Lima Melara (9805380) and Maíra Canal (11819403)
# Created Date: 18/09/2022
# ---------------------------------------------------------------------------

import glfw

class Window:
    """
        A class used to represent the system window.

        ...

        Attributes
        ----------
        x : int
        width of the window
        y : int
        height of the window
        name: str
        name of the window
    """
    def __init__(self, x: int, y: int, name: str):
        glfw.init()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        self.window = glfw.create_window(x, y, name, None, None)
        glfw.make_context_current(self.window)
