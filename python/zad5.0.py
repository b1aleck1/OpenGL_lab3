#!/usr/bin/env python3
import sys
import numpy as np
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Parametr programu: Stopień samopodobieństwa (liczba iteracji)
MAX_RECURSION_LEVEL = 3  # Ustaw na 4 lub 5 dla większej szczegółowości (ale wolniej)

# Globalne definicje wierzchołków i kolorów dla bazowego czworościanu
# Używamy numpy dla łatwiejszych obliczeń na wektorach (np. (v1+v2)/2)
V0 = np.array([0.0, 6.0, 0.0])
V1 = np.array([-6.0, -4.0, 6.0])
V2 = np.array([6.0, -4.0, 6.0])
V3 = np.array([0.0, -4.0, -6.0])

C0 = np.array([1.0, 0.0, 0.0])  # Czerwony
C1 = np.array([0.0, 1.0, 0.0])  # Zielony
C2 = np.array([0.0, 0.0, 1.0])  # Niebieski
C3 = np.array([1.0, 1.0, 0.0])  # Żółty


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)  # Włączenie bufora głębi jest kluczowe dla 3D


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
# NOWE FUNKCJE DLA OCENY 5.0
# =================================================================

def draw_tetrahedron(v0, v1, v2, v3, c0, c1, c2, c3):
    """ Rysuje pojedynczy czworościan (4 ściany) z interpolacją kolorów. """
    glBegin(GL_TRIANGLES)

    # Ściana 1 (v0, v1, v2)
    glColor3fv(c0);
    glVertex3fv(v0)
    glColor3fv(c1);
    glVertex3fv(v1)
    glColor3fv(c2);
    glVertex3fv(v2)

    # Ściana 2 (v0, v2, v3)
    glColor3fv(c0);
    glVertex3fv(v0)
    glColor3fv(c2);
    glVertex3fv(v2)
    glColor3fv(c3);
    glVertex3fv(v3)

    # Ściana 3 (v0, v3, v1)
    glColor3fv(c0);
    glVertex3fv(v0)
    glColor3fv(c3);
    glVertex3fv(v3)
    glColor3fv(c1);
    glVertex3fv(v1)

    # Ściana 4 (Podstawa: v1, v3, v2)
    glColor3fv(c1);
    glVertex3fv(v1)
    glColor3fv(c3);
    glVertex3fv(v3)
    glColor3fv(c2);
    glVertex3fv(v2)

    glEnd()


def draw_sierpinski_tetrahedron(v0, v1, v2, v3, c0, c1, c2, c3, level):
    """ Funkcja rekurencyjna generująca fraktal. """

    # 1. Warunek bazowy (zatrzymania)
    # Jeśli osiągnięto zadaną liczbę iteracji, rysuj czworościan
    if level == 0:
        draw_tetrahedron(v0, v1, v2, v3, c0, c1, c2, c3)
        return

    # 2. Krok rekurencyjny

    # Obliczanie 6 punktów środkowych krawędzi (wierzchołków)
    m01 = (v0 + v1) / 2.0
    m02 = (v0 + v2) / 2.0
    m03 = (v0 + v3) / 2.0
    m12 = (v1 + v2) / 2.0
    m13 = (v1 + v3) / 2.0
    m23 = (v2 + v3) / 2.0

    # Obliczanie 6 kolorów środkowych (interpolacja)
    mc01 = (c0 + c1) / 2.0
    mc02 = (c0 + c2) / 2.0
    mc03 = (c0 + c3) / 2.0
    mc12 = (c1 + c2) / 2.0
    mc13 = (c1 + c3) / 2.0
    mc23 = (c2 + c3) / 2.0

    new_level = level - 1

    # 3. Wywołania rekurencyjne dla 4 mniejszych czworościanów

    # Czworościan 1 (górny)
    draw_sierpinski_tetrahedron(v0, m01, m02, m03, c0, mc01, mc02, mc03, new_level)

    # Czworościan 2 (róg v1)
    draw_sierpinski_tetrahedron(m01, v1, m12, m13, mc01, c1, mc12, mc13, new_level)

    # Czworościan 3 (róg v2)
    draw_sierpinski_tetrahedron(m02, m12, v2, m23, mc02, mc12, c2, mc23, new_level)

    # Czworościan 4 (róg v3)
    draw_sierpinski_tetrahedron(m03, m13, m23, v3, mc03, mc13, mc23, c3, new_level)

    # Centralny ośmiościan (m01, m02, m03, m12, m13, m23) jest pomijany.


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    angle = time * 180 / math.pi
    spin(angle)

    axes()

    # Wywołanie głównej funkcji rysującej fraktal
    draw_sierpinski_tetrahedron(V0, V1, V2, V3, C0, C1, C2, C3, MAX_RECURSION_LEVEL)

    glFlush()


def update_viewport(window, width, height):
    if height == 0: height = 1
    if width == 0: width = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    # Zwiększamy nieco rzutnię, aby zmieścić większy model
    if width <= height:
        glOrtho(-10.0, 10.0, -10.0 / aspect_ratio, 10.0 / aspect_ratio, -15.0, 15.0)
    else:
        glOrtho(-10.0 * aspect_ratio, 10.0 * aspect_ratio, -10.0, 10.0, -15.0, 15.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Lab 3: Piramida Sierpińskiego (5.0)", None, None)
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