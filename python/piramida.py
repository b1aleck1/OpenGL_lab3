#!/usr/bin/env python3
import sys
import numpy as np
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Parametr programu: Stopień samopodobieństwa (liczba iteracji)
MAX_RECURSION_LEVEL = 3  # 4 lub 5 też da radę

# Globalne definicje 5 wierzchołków i 5 kolorów dla bazowej piramidy
V_APEX = np.array([0.0, 6.0, 0.0])
V_B1 = np.array([-6.0, -6.0, 6.0])  # Lewy-górny tył
V_B2 = np.array([6.0, -6.0, 6.0])  # Prawy-górny tył
V_B3 = np.array([6.0, -6.0, -6.0])  # Prawy-dolny przód
V_B4 = np.array([-6.0, -6.0, -6.0])  # Lewy-dolny przód

C_APEX = np.array([1.0, 1.0, 1.0])  # Biały
C_B1 = np.array([1.0, 0.0, 0.0])  # Czerwony
C_B2 = np.array([0.0, 1.0, 0.0])  # Zielony
C_B3 = np.array([0.0, 0.0, 1.0])  # Niebieski
C_B4 = np.array([1.0, 1.0, 0.0])  # Żółty


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    # ... (funkcja axes bez zmian)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-7.5, 0.0, 0.0);
    glVertex3f(7.5, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -7.5, 0.0);
    glVertex3f(0.0, 7.5, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -7.5);
    glVertex3f(0.0, 0.0, 7.5)
    glEnd()


def spin(angle):
    # ... (funkcja spin bez zmian)
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


# =================================================================
# NOWE FUNKCJE DLA OCENY 5.0 (Piramida Kwadratowa)
# =================================================================

def draw_pyramid(v_a, v_b1, v_b2, v_b3, v_b4, c_a, c_b1, c_b2, c_b3, c_b4):
    """ Rysuje pojedynczą piramidę (4 ściany boczne + 2 trójkąty podstawy) """
    glBegin(GL_TRIANGLES)

    # Ściana 1 (Tył)
    glColor3fv(c_a);
    glVertex3fv(v_a)
    glColor3fv(c_b1);
    glVertex3fv(v_b1)
    glColor3fv(c_b2);
    glVertex3fv(v_b2)

    # Ściana 2 (Prawa)
    glColor3fv(c_a);
    glVertex3fv(v_a)
    glColor3fv(c_b2);
    glVertex3fv(v_b2)
    glColor3fv(c_b3);
    glVertex3fv(v_b3)

    # Ściana 3 (Przód)
    glColor3fv(c_a);
    glVertex3fv(v_a)
    glColor3fv(c_b3);
    glVertex3fv(v_b3)
    glColor3fv(c_b4);
    glVertex3fv(v_b4)

    # Ściana 4 (Lewa)
    glColor3fv(c_a);
    glVertex3fv(v_a)
    glColor3fv(c_b4);
    glVertex3fv(v_b4)
    glColor3fv(c_b1);
    glVertex3fv(v_b1)

    # Podstawa (dwa trójkąty)
    glColor3fv(c_b1);
    glVertex3fv(v_b1)
    glColor3fv(c_b3);
    glVertex3fv(v_b3)
    glColor3fv(c_b2);
    glVertex3fv(v_b2)

    glColor3fv(c_b1);
    glVertex3fv(v_b1)
    glColor3fv(c_b4);
    glVertex3fv(v_b4)
    glColor3fv(c_b3);
    glVertex3fv(v_b3)

    glEnd()


def draw_sierpinski_pyramid(v_a, v_b1, v_b2, v_b3, v_b4, c_a, c_b1, c_b2, c_b3, c_b4, level):
    """ Funkcja rekurencyjna generująca fraktal piramidy """

    # 1. Warunek bazowy (zatrzymania)
    if level == 0:
        draw_pyramid(v_a, v_b1, v_b2, v_b3, v_b4, c_a, c_b1, c_b2, c_b3, c_b4)
        return

    # 2. Obliczanie punktów środkowych
    # 4 mid-points na krawędziach bocznych (do wierzchołka)
    m_a1 = (v_a + v_b1) / 2.0;
    m_a2 = (v_a + v_b2) / 2.0
    m_a3 = (v_a + v_b3) / 2.0;
    m_a4 = (v_a + v_b4) / 2.0

    # 4 mid-points na krawędziach podstawy
    m_b12 = (v_b1 + v_b2) / 2.0;
    m_b23 = (v_b2 + v_b3) / 2.0
    m_b34 = (v_b3 + v_b4) / 2.0;
    m_b41 = (v_b4 + v_b1) / 2.0

    # 1 mid-point w centrum podstawy
    m_bc = (v_b1 + v_b2 + v_b3 + v_b4) / 4.0

    # Obliczanie kolorów środkowych (interpolacja)
    mc_a1 = (c_a + c_b1) / 2.0;
    mc_a2 = (c_a + c_b2) / 2.0
    mc_a3 = (c_a + c_b3) / 2.0;
    mc_a4 = (c_a + c_b4) / 2.0
    mc_b12 = (c_b1 + c_b2) / 2.0;
    mc_b23 = (c_b2 + c_b3) / 2.0
    mc_b34 = (c_b3 + c_b4) / 2.0;
    mc_b41 = (c_b4 + c_b1) / 2.0
    mc_bc = (c_b1 + c_b2 + c_b3 + c_b4) / 4.0

    new_level = level - 1

    # 3. Wywołania rekurencyjne dla 5 mniejszych piramid

    # Piramida 1 (Górna)
    draw_sierpinski_pyramid(v_a, m_a1, m_a2, m_a3, m_a4,
                            c_a, mc_a1, mc_a2, mc_a3, mc_a4, new_level)

    # Piramida 2 (Narożnik 1)
    draw_sierpinski_pyramid(m_a1, v_b1, m_b12, m_bc, m_b41,
                            mc_a1, c_b1, mc_b12, mc_bc, mc_b41, new_level)

    # Piramida 3 (Narożnik 2)
    draw_sierpinski_pyramid(m_a2, m_b12, v_b2, m_b23, m_bc,
                            mc_a2, mc_b12, c_b2, mc_b23, mc_bc, new_level)

    # Piramida 4 (Narożnik 3)
    draw_sierpinski_pyramid(m_a3, m_bc, m_b23, v_b3, m_b34,
                            mc_a3, mc_bc, mc_b23, c_b3, mc_b34, new_level)

    # Piramida 5 (Narożnik 4)
    draw_sierpinski_pyramid(m_a4, m_b41, m_bc, m_b34, v_b4,
                            mc_a4, mc_b41, mc_bc, mc_b34, c_b4, new_level)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    angle = time * 180 / math.pi
    spin(angle)

    axes()

    # Wywołanie głównej funkcji rysującej fraktal
    draw_sierpinski_pyramid(V_APEX, V_B1, V_B2, V_B3, V_B4,
                            C_APEX, C_B1, C_B2, C_B3, C_B4,
                            MAX_RECURSION_LEVEL)

    glFlush()


def update_viewport(window, width, height):
    # ... (funkcja update_viewport bez zmian, zakres [-10, 10] pasuje)
    if height == 0: height = 1
    if width == 0: width = 1
    aspect_ratio = width / height
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()
    if width <= height:
        glOrtho(-10.0, 10.0, -10.0 / aspect_ratio, 10.0 / aspect_ratio, -15.0, 15.0)
    else:
        glOrtho(-10.0 * aspect_ratio, 10.0 * aspect_ratio, -10.0, 10.0, -15.0, 15.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    # ... (funkcja main bez zmian)
    if not glfwInit(): sys.exit(-1)
    window = glfwCreateWindow(400, 400, "Lab 3: Piramida Sierpińskiego (5.0)", None, None)
    if not window: glfwTerminate(); sys.exit(-1)
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)
    width, height = glfwGetFramebufferSize(window)
    update_viewport(window, width, height)
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()
    glfwTerminate()


if __name__ == '__main__':
    main()