#!/usr/bin/env python3
import sys
import numpy as np
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 20
VERTICES = np.zeros((N, N, 3))

# STAŁE FIZYCZNE I GEOMETRYCZNE (Dla Praw Keplera)
G_GRAV = 1.0;
M_SUN = 100.0
A1 = 7.0;
E1 = 0.2;
B1 = A1 * math.sqrt(1 - E1 ** 2);
FOCAL_DIST_1 = A1 * E1
A2 = 10.0;
E2 = 0.4;
B2 = A2 * math.sqrt(1 - E2 ** 2);
FOCAL_DIST_2 = A2 * E2
ORBIT_SPEED_FAC_1 = math.sqrt(G_GRAV * M_SUN / (A1 ** 3))
ORBIT_SPEED_FAC_2 = math.sqrt(G_GRAV * M_SUN / (A2 ** 3))


def startup():
    global VERTICES, N
    update_viewport(None, 400, 400);
    glClearColor(0.0, 0.0, 0.0, 1.0);
    glEnable(GL_DEPTH_TEST)
    u_values = np.linspace(0.0, 1.0, N);
    v_values = np.linspace(0.0, 1.0, N)
    pi = np.pi;
    radius = 1.0
    for i in range(N):
        for j in range(N):
            phi = u_values[i] * pi;
            theta = v_values[j] * 2 * pi
            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.cos(phi)
            z = radius * math.sin(phi) * math.sin(theta)
            VERTICES[i][j][0] = x;
            VERTICES[i][j][1] = y;
            VERTICES[i][j][2] = z


def shutdown(): pass


def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0);
    glVertex3f(-12.0, 0.0, 0.0);
    glVertex3f(12.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0);
    glVertex3f(0.0, -12.0, 0.0);
    glVertex3f(0.0, 12.0, 0.0)
    glColor3f(0.0, 0.0, 1.0);
    glVertex3f(0.0, 0.0, -12.0);
    glVertex3f(0.0, 0.0, 12.0)
    glEnd()


# Nowa funkcja obracająca całą scenę (nie tylko kamerę)
def rotate_system(angle):
    glRotatef(30.0, 1.0, 0.0, 0.0)  # Stałe pochylenie osi X, aby widzieć 3D
    glRotatef(angle, 0.0, 1.0, 0.0)  # Obrót całego układu wokół osi Y


def draw_sphere_model():
    global VERTICES, N
    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glVertex3fv(VERTICES[i][j]);
            glVertex3fv(VERTICES[i + 1][j])
        glEnd()


# ... (draw_orbit i get_kepler_position bez zmian)

def get_kepler_position(A, E, time, orbit_speed_fac):
    M = time * orbit_speed_fac
    E_anomaly = M
    for _ in range(5):
        E_anomaly = E_anomaly - (E_anomaly - E * math.sin(E_anomaly) - M) / (1 - E * math.cos(E_anomaly))
    x_pos = A * (math.cos(E_anomaly) - E)
    z_pos = A * math.sqrt(1 - E ** 2) * math.sin(E_anomaly)
    return x_pos, z_pos


def draw_orbit(A, B, FOCAL_DIST):
    glBegin(GL_LINE_LOOP);
    glColor3f(0.5, 0.5, 0.5);
    segments = 150
    for i in range(segments):
        angle = (i / segments) * 2 * math.pi
        x_ellip = A * math.cos(angle);
        z_ellip = B * math.sin(angle)
        x = x_ellip + FOCAL_DIST;
        z = z_ellip
        glVertex3f(x, 0.0, z)
    glEnd()


# ... (Koniec draw_orbit)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # --- PRZESUNIĘCIE I OBRÓT CAŁEGO SYSTEMU ---
    # Zaczynamy od macierzy jednostkowej, a potem obracamy cały układ.

    angle = time * 30.0
    rotate_system(angle)  # Obrót sceny
    # ---------------------------------------------

    axes()

    # 1. Rysujemy Słońce (znajduje się w ognisku: 0,0,0)
    glPushMatrix()
    glColor3f(1.0, 1.0, 0.0);
    glScalef(1.5, 1.5, 1.5)
    draw_sphere_model()
    glPopMatrix()

    # === PLANETA 1 (Niebieska) ===
    planet_x_1, planet_z_1 = get_kepler_position(A1, E1, time, ORBIT_SPEED_FAC_1)

    # Rysujemy Orbitę 1
    glPushMatrix()
    draw_orbit(A1, B1, FOCAL_DIST_1)
    glPopMatrix()

    # Przesunięcie i Rysowanie Planety 1
    glPushMatrix()
    glTranslatef(planet_x_1, 0.0, planet_z_1)  # PRZESUNIĘCIE W NIE-OBRÓCONEJ PŁASZCZYŹNIE!
    glRotatef(time * 100.0, 0.0, 1.0, 0.0)
    glColor3f(0.2, 0.5, 1.0)
    draw_sphere_model()
    glPopMatrix()

    # === PLANETA 2 (Czerwona) ===
    planet_x_2, planet_z_2 = get_kepler_position(A2, E2, time, ORBIT_SPEED_FAC_2)

    # Rysujemy Orbitę 2
    glPushMatrix()
    draw_orbit(A2, B2, FOCAL_DIST_2)
    glPopMatrix()

    # Przesunięcie i Rysowanie Planety 2
    glPushMatrix()
    glTranslatef(planet_x_2, 0.0, planet_z_2)
    glRotatef(time * 50.0, 0.0, 1.0, 0.0)
    glColor3f(1.0, 0.3, 0.2)
    glScalef(0.7, 0.7, 0.7)
    draw_sphere_model()
    glPopMatrix()

    glFlush()


def update_viewport(window, width, height):
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
    window = glfwCreateWindow(400, 400, "Lab 3: Symulacja (PEŁNY KEPLER POPRAWIONY)", None, None)
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