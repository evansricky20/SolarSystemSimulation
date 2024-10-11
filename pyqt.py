import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math


class Sphere:
    instances = []

    def __init__(self, name, radius, orbit_radius, orbit_speed, rotation_speed, moons=None):
        self.name = name
        self.radius = radius
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.rotation = rotation_speed
        self.moons = moons
        Sphere.instances.append(self)
        self.moons = []

    def render(self, time):

        glPushMatrix()
        x_orbit = math.cos(time * self.orbit_speed)
        y_orbit = math.sin(time * self.orbit_speed)
        glTranslatef(x_orbit * self.orbit_radius, y_orbit * self.orbit_radius, 0)
        glRotatef(time * self.rotation, 0, 0, 1)
        sphere = gluNewQuadric()
        gluSphere(sphere, self.radius, 32, 32)

        glPopMatrix()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.resize(800, 600)
        self.setWindowTitle("Computer Graphics - Project 1")

        glWidget = GLWidget(self)
        self.setCentralWidget(glWidget)

        timer = QTimer(self)


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QGLWidget.__init__(self, parent)

        self.timer = QTimer(self)
        self.elapsed_timer = QElapsedTimer()  # Timer to track continuous time

        # Start the elapsed timer
        self.elapsed_timer.start()

        # Set up the timer to update every 16ms (~60fps)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def initializeGL(self):
        self.qglClearColor(QColor(0, 0, 0))
        glEnable(GL_DEPTH_TEST)



    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)

        gluPerspective(90.0, aspect, 1.0, 100.0)  # (field of view, aspect ratio, z near, z far)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        # Camera setup
        gluLookAt(0.0, 0.0, 10.0,  # Eye position (camera)
                  0.0, 0.0, 0.0,  # Look at position (center of the scene)
                  0.0, 1.0, 0.0)

        elapsed_time = self.elapsed_timer.elapsed() / 1000.0

        glColor3f(1, 1, 0)
        sun = Sphere("sun", 1.5, 0, 0, 1)  # (self, name, radius, orbit_radius, orbit_speed, rotation_speed)
        sun.render(elapsed_time)

        # Planet 1
        glColor3f(0, 0, 1)
        planet1 = Sphere("planet1", 1.0, 4, 1.5, 1, 1)
        planet1.render(elapsed_time)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
