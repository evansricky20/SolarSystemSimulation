import pygame
import pygame_gui
from pygame.locals import *
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys


# def Sphere(radius):
#     quadric = gluNewQuadric()
#     gluSphere(quadric, radius, 32, 32)



class Sphere:
    instances = []

    def __init__(self, name, radius, orbit_radius, orbit_speed, rotation_speed):
        self.name = name
        self.radius = radius
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.rotation = rotation_speed
        Sphere.instances.append(self)
        self.moons = []

    def __str__(self):
        return f"{self.name}: {self.radius}"

    def render(self):
        time = pygame.time.get_ticks() * 0.001

        glPushMatrix()
        x_orbit = math.cos(time * self.orbit_speed)
        y_orbit = math.sin(time * self.orbit_speed)
        glTranslatef(x_orbit * self.orbit_radius, y_orbit * self.orbit_radius, 0)
        glRotatef(time * self.rotation, 0, 0, 1)
        quadric = gluNewQuadric()
        gluSphere(quadric, self.radius, 32, 32)

        glPushMatrix()
        x_orbit = math.cos(time * 4)
        y_orbit = math.sin(time * 4)
        glTranslatef(x_orbit * 2, y_orbit * 2, 0)
        glRotatef(time * 1, 0, 0, 1)
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.25, 32, 32)

        glPopMatrix()
        glPopMatrix()


def main():
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    manager = pygame_gui.UIManager((800, 600))
    clock = pygame.time.Clock()

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -30)

    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 550), (100, 50)),
                                          text='Press Me',
                                          manager=manager)

    glClearColor(0, 0, 0, 1)
    while True:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            manager.process_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                if event.key == pygame.K_TAB:
                    print("Tab pressed")  # use for menu
                if event.key == pygame.K_KP_PLUS:
                    glTranslatef(0, 0, 1.0)
                if event.key == pygame.K_KP_MINUS:
                    glTranslatef(0, 0, -1.0)
                if event.key == pygame.K_1:
                    # print all objects
                    for sphere in Sphere.instances:
                        print(sphere)

        manager.update(time_delta)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Sun
        glColor3f(1, 1, 0)
        sun = Sphere("sun", 1.5, 0, 0, 1)  # (self, name, radius, orbit_radius, orbit_speed, rotation_speed)
        sun.render()

        # Planet 1
        glColor3f(0, 0, 1)
        planet1 = Sphere("planet1", 1.0, 4, 1.5, 1)
        planet1.render()


        # Planet 1 moon
        # glPushMatrix()
        # orbit_radius = 2
        # x_orbit = math.cos(time * 4)
        # y_orbit = math.sin(time * 4)
        # glTranslatef(x_orbit * orbit_radius, y_orbit * orbit_radius, 0)
        # glRotatef(time * 30, 0, 0, 1)
        # glColor3f(1, 1, 1)
        # planet1moon = Sphere("planet1moon", 0.25)
        # planet1moon.render()
        # glPopMatrix()
        # glPopMatrix()

        # Planet 2
        glColor3f(0, 1, 0)
        planet2 = Sphere("planet2", 0.5, 7, 1, 1)
        planet2.render()

        # steroid 1
        glColor3f(1, 0, 1)
        asteroid1 = Sphere("asteroid1", 0.2, 5, 2, 1)
        asteroid1.render()

        # Planet 3
        glColor3f(0, 1, 1)
        planet3 = Sphere("planet3", 0.7, 9, 0.8, 1)
        planet3.render()

        # Planet 4
        glColor3f(1, 1, 1)
        planet4 = Sphere("planet4", 1.75, 11, 0.2, 1)
        planet4.render()

        glDisable(GL_DEPTH_TEST)
        manager.draw_ui(screen)
        glEnable(GL_DEPTH_TEST)

        pygame.display.flip()
        pygame.time.wait(10)


main()
