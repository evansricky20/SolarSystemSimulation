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
        self.orig_rad = radius
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.orig_orbit_speed = orbit_speed
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

        self.initGUI()

    def initGUI(self):
        central_widget = QWidget(self)
        gui_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(gui_layout)

        self.setCentralWidget(central_widget)

        self.glWidget = GLWidget(self)
        gui_layout.addWidget(self.glWidget)

        planetlist = QComboBox()

        # Size slider label
        size_label = QLabel(self)
        size_label.setText("Adjust Size:")
        size_label.setFont(QFont("Arial", 11))
        size_label.setFixedSize(200, 20)

        # Size slider creation
        self.size_slider = QSlider(Qt.Horizontal, self)
        self.size_slider.setTickPosition(QSlider.TicksBelow)
        self.size_slider.setTickInterval(10)  # Setting slider to have interval of every 10 ticks
        self.size_slider.setSingleStep(1)  # Each tick step is 1
        self.size_slider.setValue(100)
        self.size_slider.setMinimum(0)
        self.size_slider.setMaximum(200)
        self.size_slider.valueChanged.connect(self.glWidget.changeSize)

        # Speed slider label
        speed_label = QLabel(self)
        speed_label.setText("Adjust Speed:")
        speed_label.setFont(QFont("Arial", 11))
        speed_label.setFixedSize(200, 20)

        # Speed slider creation
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(10)  # Setting slider to have interval of every 10 ticks
        self.speed_slider.setSingleStep(1)  # Each tick step is 1
        self.speed_slider.setValue(100)
        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(200)
        self.speed_slider.valueChanged.connect(self.glWidget.changeOrbit)

        # Rotation slider label
        rotate_label = QLabel(self)
        rotate_label.setText("Adjust Rotation:")
        rotate_label.setFont(QFont("Arial", 11))
        rotate_label.setFixedSize(200, 20)

        # Rotation slider creation
        self.rotate_slider = QSlider(Qt.Horizontal, self)
        self.rotate_slider.setTickPosition(QSlider.TicksBelow)
        self.rotate_slider.setTickInterval(10)  # Setting slider to have interval of every 10 ticks
        self.rotate_slider.setSingleStep(1)  # Each tick step is 1

        # Using addWidget to add labels and sliders to layout
        gui_layout.addWidget(size_label)
        gui_layout.addWidget(self.size_slider)
        gui_layout.addWidget(speed_label)
        gui_layout.addWidget(self.speed_slider)
        gui_layout.addWidget(rotate_label)
        gui_layout.addWidget(self.rotate_slider)


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QGLWidget.__init__(self, parent)

        self.timer = QTimer(self)
        self.elapsed_timer = QElapsedTimer()  # time to track time passed for continuous translation
        self.elapsed_timer.start() # start timer

        self.timer.timeout.connect(self.update) # timer
        self.timer.start(16)

        self.planet1 =Sphere("planet1", 2, 4, 2, 1)
        self.planet2 = Sphere("planet2", 1.5, 8, 1, 1, 0)

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
        gluLookAt(0.0, 0.0, 20.0,  # Eye position (camera)
                  0.0, 0.0, 0.0,  # Look at position (center of the scene)
                  0.0, 1.0, 0.0)

        elapsed_time = self.elapsed_timer.elapsed() / 1000.0

        # Sun
        glColor3f(1, 1, 0)
        sun = Sphere("sun", 1.5, 0, 0, 1)  # (self, name, radius, orbit_radius, orbit_speed, rotation_speed)
        sun.render(elapsed_time)

        # Planet 1
        glColor3f(0, 0, 1)
        # planet1 = Sphere("planet1", 1.0, 4, 2, 1, 1)
        # planet1.render(elapsed_time)
        self.planet1.render(elapsed_time)

        # Planet 2
        glColor3f(0, 1, 0)
        # planet2 = Sphere("planet2", 1.5, 8, 1, 1, 0)
        self.planet2.render(elapsed_time)

    def changeSize(self, size):
        self.planet1.radius = self.planet1.orig_rad * (size / 100) # Dividing by 100 to conform to coordinate system
        self.update()

    def changeOrbit(self, orbit):
        self.planet1.orbit_speed = self.planet1.orig_orbit_speed * (orbit / 100)
        self.update()

    def changeRotation(self, rotation):
        self.planet1.rotation = rotation
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
