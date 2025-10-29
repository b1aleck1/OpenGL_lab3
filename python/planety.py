#!/usr/bin/env python3
import sys
import numpy as np
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 20  # Rozdzielczość siatki sfery
VERTICES = np.zeros((N, N, 3))

def startup():
    global VERTICES, N
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    u_values = np.linspace(0.0, 1.0, N)
    v_values = np.linspace(0.0, 1.0, N)
    pi = np.pi
    radius = 1.0
    for i in range(N):
        for j in range(N):
            phi = u_values[i] * pi
            theta = v_values[j] * 2 * pi
            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.cos(phi)
            z = radius * math.sin(phi) * math.sin(theta)
            VERTICES[i][j][0] = x
            VERTICES[i][j][1] = y
            VERTICES[i][j][2] = z

def shutdown():
    pass

def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-7.5, 0.0, 0.0); glVertex3f(7.5, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -7.5, 0.0); glVertex3f(0.0, 7.5, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -7.5); glVertex3f(0.0, 0.0, 7.5)
    glEnd()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def draw_sphere_model():
    global VERTICES, N
    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glVertex3fv(VERTICES[i][j])
            glVertex3fv(VERTICES[i + 1][j])
        glEnd()

def draw_orbit(radius_a, radius_b):
    # Rysuje elipsę w płaszczyźnie XZ (orbita)
    glBegin(GL_LINE_LOOP)
    glColor3f(0.5, 0.5, 0.5) # Szary

    segments = 100
    for i in range(segments):
        angle = (i / segments) * 2 * math.pi
        # Używam różnych promieni dla X i Z
        x = radius_a * math.cos(angle)
        z = radius_b * math.sin(angle)
        glVertex3f(x, 0.0, z) # Rysujemy na płaszczyźnie Y=0

    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    angle = time * 30.0
    spin(angle)

    axes()


    # Słońce (w centrum)
    glPushMatrix()
    glColor3f(1.0, 1.0, 0.0) # Żółty
    glScalef(1.5, 1.5, 1.5)
    draw_sphere_model()
    glPopMatrix()

    # PLANETA 1 (Niebieska)

    # Definiujemy półoś wielką (a) i małą (b)
    orbit_radius_a_1 = 7.0 # Półos wielka (rozciągnięcie w X)
    orbit_radius_b_1 = 5.0 # Półos mała (rozciągnięcie w Z)
    orbit_speed_1 = 1.0

    # Orbita 1 (eliptyczną)
    glPushMatrix()
    draw_orbit(orbit_radius_a_1, orbit_radius_b_1)
    glPopMatrix()

    # Planetę 1 (ruch po elipsie)
    glPushMatrix()
    orbit_angle_1 = time * orbit_speed_1
    # Używamy różnych promieni dla X i Z
    planet_x_1 = orbit_radius_a_1 * math.cos(orbit_angle_1)
    planet_z_1 = orbit_radius_b_1 * math.sin(orbit_angle_1)

    glTranslatef(planet_x_1, 0.0, planet_z_1)
    glRotatef(time * 100.0, 0.0, 1.0, 0.0)

    glColor3f(0.2, 0.5, 1.0) # Niebieski
    draw_sphere_model()
    glPopMatrix()

    # PLANETA 2 (Czerwona)

    orbit_radius_a_2 = 10.0 # Dalsza orbita, bardziej rozciągnięta
    orbit_radius_b_2 = 8.0
    orbit_speed_2 = 0.5  # Wolniejszy ruch

    # Orbita 2 (eliptyczną)
    glPushMatrix()
    draw_orbit(orbit_radius_a_2, orbit_radius_b_2)
    glPopMatrix()

    # Planeta 2 (ruch po elipsie)
    glPushMatrix()
    orbit_angle_2 = time * orbit_speed_2
    planet_x_2 = orbit_radius_a_2 * math.cos(orbit_angle_2)
    planet_z_2 = orbit_radius_b_2 * math.sin(orbit_angle_2)

    glTranslatef(planet_x_2, 0.0, planet_z_2)
    glRotatef(time * 50.0, 0.0, 1.0, 0.0) # Wolniejszy obrót własny

    glColor3f(1.0, 0.3, 0.2) # Czerwony/Pomarańczowy
    glScalef(0.7, 0.7, 0.7)  # Mniejsza planeta
    draw_sphere_model()
    glPopMatrix()

    glFlush()


def update_viewport(window, width, height):
    # Zwiększam nieco zakres, aby zmieścić większe orbity
    if height == 0: height = 1
    if width == 0: width = 1
    aspect_ratio = width / height
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()
    if width <= height:
        glOrtho(-12.0, 12.0, -12.0 / aspect_ratio, 12.0 / aspect_ratio, -20.0, 20.0)
    else:
        glOrtho(-12.0 * aspect_ratio, 12.0 * aspect_ratio, -12.0, 12.0, -20.0, 20.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit(): sys.exit(-1)
    window = glfwCreateWindow(400, 400, "Lab 3: Symulacja (Orbity Eliptyczne)", None, None)
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