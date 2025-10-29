#!/usr/bin/env python3
import sys
import numpy as np
import math
import random  # <--- Wymagane dla losowych kolorów

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 30  # Rozdzielczość siatki

# Globalne tablice na współrzędne i kolory
VERTICES = np.zeros((N, N, 3))
COLORS = np.zeros((N, N, 3))  # <--- Tablica na losowe kolory


def startup():
    global VERTICES, COLORS, N

    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    u_values = np.linspace(0.0, 1.0, N)
    v_values = np.linspace(0.0, 1.0, N)
    pi = np.pi

    for i in range(N):
        for j in range(N):
            u = u_values[i]
            v = v_values[j]

            # Równania parametryczne
            u2, u3, u4, u5 = u * u, u * u * u, u * u * u * u, u * u * u * u * u
            P_u = (-90 * u5 + 225 * u4 - 270 * u3 + 180 * u2 - 45 * u)

            x = P_u * np.cos(pi * v)
            z = P_u * np.sin(pi * v)
            y = 160 * u4 - 320 * u3 + 160 * u2 - 5.0

            VERTICES[i][j][0] = x
            VERTICES[i][j][1] = y
            VERTICES[i][j][2] = z

            # --- Wymaganie 4.0: Losowy kolor dla każdego wierzchołka ---
            COLORS[i][j][0] = random.random()  # R
            COLORS[i][j][1] = random.random()  # G
            COLORS[i][j][2] = random.random()  # B
            # --------------------------------------------------------


def shutdown():
    pass


def axes():
    # ... (funkcja axes bez zmian)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0);
    glVertex3f(5.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0);
    glVertex3f(0.0, 5.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0);
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()


def spin(angle):
    # ... (funkcja spin bez zmian)
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    angle = time * 180 / math.pi
    spin(angle)

    axes()

    # --- Wymaganie 4.0: Rysowanie trójkątami (GL_TRIANGLES) ---
    glBegin(GL_TRIANGLES)

    for i in range(N - 1):  # Iterujemy do N-1, aby nie wyjść poza zakres
        for j in range(N - 1):  # Iterujemy do N-1, aby nie wyjść poza zakres

            # Definiujemy 4 wierzchołki "kwadratu" siatki
            v1 = VERTICES[i][j]
            c1 = COLORS[i][j]

            v2 = VERTICES[i + 1][j]
            c2 = COLORS[i + 1][j]

            v3 = VERTICES[i][j + 1]
            c3 = COLORS[i][j + 1]

            v4 = VERTICES[i + 1][j + 1]
            c4 = COLORS[i + 1][j + 1]

            # Trójkąt 1 (główny)
            # (i, j) -> (i+1, j) -> (i, j+1)
            glColor3fv(c1);
            glVertex3fv(v1)
            glColor3fv(c2);
            glVertex3fv(v2)
            glColor3fv(c3);
            glVertex3fv(v3)

            # Trójkąt 2 (dopełniający)
            # (i+1, j) -> (i+1, j+1) -> (i, j+1)
            glColor3fv(c2);
            glVertex3fv(v2)
            glColor3fv(c4);
            glVertex3fv(v4)
            glColor3fv(c3);
            glVertex3fv(v3)

    glEnd()
    # ---------------------------------------------------

    glFlush()


def update_viewport(window, width, height):
    # ... (funkcja update_viewport bez zmian)
    if height == 0: height = 1
    if width == 0: width = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, -10.0, 10.0)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, -10.0, 10.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Lab 3: Jajko 3D (Trójkąty)", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

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