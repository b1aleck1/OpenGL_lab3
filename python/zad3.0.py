#!/usr/bin/env python3
import sys
import numpy as np  # Używamy numpy do tablic i obliczeń [cite: 258]

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Ustawiamy rozdzielczość siatki (N x N)
N = 30

# Globalna tablica do przechowywania wierzchołków [cite: 256]
VERTICES = np.zeros((N, N, 3))


def startup():
    """ Oblicza wierzchołki i włącza bufor głębi """
    global VERTICES, N

    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Czarne tło dla lepszej widoczności

    # Włącz mechanizm bufora głębi [cite: 164, 165]
    glEnable(GL_DEPTH_TEST)

    # Generowanie tablic dla u i v (od 0.0 do 1.0) [cite: 259, 260]
    u_values = np.linspace(0.0, 1.0, N)
    v_values = np.linspace(0.0, 1.0, N)

    pi = np.pi

    # Obliczanie współrzędnych x, y, z dla każdej pary (u, v)
    for i in range(N):
        for j in range(N):
            u = u_values[i]
            v = v_values[j]

            # Równania parametryczne dla jajka
            u2 = u * u
            u3 = u2 * u
            u4 = u3 * u
            u5 = u4 * u

            # Wspólna część dla x i z
            P_u = (-90 * u5 + 225 * u4 - 270 * u3 + 180 * u2 - 45 * u)

            x = P_u * np.cos(pi * v)
            z = P_u * np.sin(pi * v)
            y = 160 * u4 - 320 * u3 + 160 * u2 - 5.0

            # Zapisanie wierzchołka w tablicy
            VERTICES[i][j][0] = x
            VERTICES[i][j][1] = y
            VERTICES[i][j][2] = z


def shutdown():
    pass


def axes():
    """ Rysuje osie X (czerwona), Y (zielona), Z (niebieska) """
    glBegin(GL_LINES)

    # X axis (Red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    # Y axis (Green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    # Z axis (Blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time):
    # Czyścimy bufor koloru ORAZ bufor głębi
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()  # Resetujemy macierz modelu

    # Rysujemy osie
    axes()

    # Rysowanie modelu jajka za pomocą punktów
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)  # Kolor punktów (biały)

    # Wyświetlamy współrzędne obliczone w startup()
    for i in range(N):
        for j in range(N):
            glVertex3f(VERTICES[i][j][0], VERTICES[i][j][1], VERTICES[i][j][2])

    glEnd()

    glFlush()


def update_viewport(window, width, height):
    """ Ustawia rzutnię 3D (ortogonalną) """
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    # Ustawiamy rzutnię ortogonalną na podstawie wskazówek
    # Zakresy [-7.5, 7.5] pasują do modelu (Y: -5 do 5, X/Z: ~-3.6 do 3.6)
    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, -10.0, 10.0)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, -10.0, 10.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Lab 3: Model Jajka (Punkty)", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    # Poprawka: Wymuszenie aktualizacji rzutni przy starcie
    width, height = glfwGetFramebufferSize(window)
    update_viewport(window, width, height)

    startup()  # Obliczenie wierzchołków

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    shutdown()
    glfwTerminate()


if __name__ == '__main__':
    main()