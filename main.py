import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# Class Name: Sphere
#
# Creates a sphere object in opengl, used in the creation of all renderd objects
# Takes the following arguments:
#   name: Name of the object being created
#   radius: Radius of object being created
#   orbit_radius: The radius of the objects orbit around the sun
#   orbit_speed: The speed in which the object orbits the sun
#   rotation_speed: The speed in which the object spins
#   render_flag: Flag to determine if object gets rendered
class Sphere:
    sphereList = []
    asteroidBelt = []

    def __init__(self, name, radius, orbit_radius, orbit_speed, rotation_speed, celestial_type=2, moons=0):
        self.name = name
        self.radius = radius
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.rotation = rotation_speed
        self.moons = moons
        self.celestial_type = celestial_type

        if celestial_type == 4:
            Sphere.asteroidBelt.append(self)
        else:
            Sphere.sphereList.append(self)

        if celestial_type == 1:
            self.color_red = 1
            self.color_green = 0.8
            self.color_blue = 0

        elif celestial_type == 2 or celestial_type == 3:
            self.color_red = random.random()
            self.color_green = random.random()
            self.color_blue = random.random()

        else:
            self.color_red = random.uniform(0.20, 0.23)
            self.color_green = random.uniform(0.20, 0.23)
            self.color_blue = random.uniform(0.23, 0.25)

    # Function to render sphere based on attributes
    def render(self, time):

        glPushMatrix() # Pushing object matrix to be rendered

        # For loop to create variance in render position
        for i in range(180):
            x_orbit = math.cos((time + i) * self.orbit_speed) # orbit for x direction, uses time as baseline multiplied by a factor
            y_orbit = math.sin((time + i) * self.orbit_speed) # orbit for y direction, uses time as baseline multiplied by a facotr

        if self.celestial_type == 3:
            x_orbit = x_orbit * 0.5
            y_orbit = y_orbit * 0.9

        glTranslatef(x_orbit * self.orbit_radius, y_orbit * self.orbit_radius, 0) # Translate function incorporating x and y orbit multiplied by radius size
        glRotatef(time * self.rotation, 0, 0, 1) # Rotation function to rotation object, rotating along z-axis
        glScalef(self.radius, self.radius, self.radius)
        glColor3f(self.color_red, self.color_green, self.color_blue)
        sphere = gluNewQuadric()
        gluSphere(sphere, 1.0, 32, 32) # Creating new sphere with set radius

        # For loop that loops for number of moons to add to planet
        for i in range(self.moons):
            glPushMatrix()

            moon_x_orbit = math.cos(time * (self.orbit_speed * (i+1) * 4))
            moon_y_orbit = math.sin(time * (self.orbit_speed * (i+1) * 4))

            # Multiplying x orbit by double planet radius plus i to prevent overlap between planet and moons
            glTranslatef(moon_x_orbit * ((self.radius * 4) + i), moon_y_orbit * ((self.radius * 4) + i), 0)
            glRotatef(time * 2, 0, 0, 1)  # Rotation function to rotation object, rotating along z-axis
            glColor3f(0.8, 0.8, 0.8)
            sphere = gluNewQuadric()
            gluSphere(sphere, 0.2, 32, 32)  # Creating new sphere with set radius
            glPopMatrix()

        glPopMatrix() # Popping matrix to allow for next



# Class MainWindow
#
# Used to initialize PyQt window and all object rendering
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.resize(800, 900)
        self.setWindowTitle("Solar System Simulation")

        self.initGUI()

    def initGUI(self):
        central_widget = QWidget(self)
        gui_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(gui_layout)

        self.setCentralWidget(central_widget)

        self.glWidget = GLWidget(self)
        gui_layout.addWidget(self.glWidget)

        # planetlist combobox label
        combobox_label = QLabel(self)
        combobox_label.setText("Object Selection:")
        combobox_label.setFont(QFont("Arial", 10))
        combobox_label.setFixedSize(200, 20)

        # Combobox / dropdown box for object selection
        self.planetlist = QComboBox()
        for planet in Sphere.sphereList:
            self.planetlist.addItem(planet.name)
        self.planetlist.currentIndexChanged.connect(self.selectPlanet)
        self.planetlist.setFixedSize(200, 20)

        # Button to add planet to system
        addplanet = QPushButton("Add Planet")
        addplanet.setFixedSize(100, 20)
        addplanet.clicked.connect(lambda: self.newPlanet(2))

        # Button to add asteroid to system
        addasteroid = QPushButton("Add Asteroid")
        addasteroid.setFixedSize(100, 20)
        addasteroid.clicked.connect(lambda: self.newPlanet(3))

        # Label for moon spinbox
        moonlabel = QLabel(self)
        moonlabel.setText("Add Moons:")
        moonlabel.setFont(QFont("Arial", 10))
        moonlabel.setFixedSize(100, 20)

        # Spinbox to add x number of moons to selected planet
        self.moonbox = QSpinBox()
        self.moonbox.setValue(0)
        self.moonbox.setMinimum(0)
        self.moonbox.setMaximum(3)
        self.moonbox.setFixedSize(100, 20)
        self.moonbox.valueChanged.connect(self.addMoons)

        # textbox label
        textbox_label = QLabel(self)
        textbox_label.setText("Object Name:")
        textbox_label.setFont(QFont("Arial", 10))
        textbox_label.setFixedSize(100, 20)

        # Text box to enter name of planet to add
        self.textbox = QLineEdit(self)
        self.textbox.setFixedSize(100, 20)

        # Button to remove planet from system
        removeplanet = QPushButton("Remove Object")
        removeplanet.setFixedSize(100, 20)
        removeplanet.clicked.connect(self.removePlanet)

        # Button to open color dialog box
        colorbutton = QPushButton("Choose Color")
        colorbutton.setFixedSize(100, 20)
        colorbutton.clicked.connect(self.glWidget.colorPicker)

        # button to add asteroid belt
        beltbutton = QPushButton("Add Belt")
        beltbutton.setFixedSize(100, 20)
        beltbutton.clicked.connect(self.asteroidBelt)

        # button to remove asteroid belt
        removebeltbutton = QPushButton("Remove Belt")
        removebeltbutton.setFixedSize(100, 20)
        removebeltbutton.clicked.connect(self.removeBelt)

        # Individual layouts
        buttonlayout = QHBoxLayout()
        firstColumn = QVBoxLayout()
        secondColumn = QVBoxLayout()
        thirdColumn = QVBoxLayout()
        fourthColumn = QVBoxLayout()

        # Adding combo box label and combo box to first column of button layout
        firstColumn.addWidget(combobox_label)
        firstColumn.addWidget(self.planetlist)

        # Adding textbox label and textbox to second column of button layout
        secondColumn.addWidget(textbox_label)
        secondColumn.addWidget(self.textbox)
        secondColumn.addWidget(moonlabel)
        secondColumn.addWidget(self.moonbox)

        # Adding the addplanet, addasteroid, and removeplanet buttons to third column of button layout
        thirdColumn.addWidget(addplanet)
        thirdColumn.addWidget(addasteroid)
        thirdColumn.addWidget(removeplanet)

        # Adding moon label, moon spinbox, and color button to fourth column
        fourthColumn.addWidget(colorbutton)
        fourthColumn.addWidget(beltbutton)
        fourthColumn.addWidget(removebeltbutton)

        # Adding all columns to button layout
        buttonlayout.addLayout(firstColumn)
        buttonlayout.addLayout(secondColumn)
        buttonlayout.addLayout(thirdColumn)
        buttonlayout.addLayout(fourthColumn)

        # Adding button layout to the main gui layout
        gui_layout.addLayout(buttonlayout)

        # Size slider label
        size_label = QLabel(self)
        size_label.setText("Adjust Radius Size:")
        size_label.setFont(QFont("Arial", 11))
        size_label.setFixedSize(200, 20)

        # Size slider creation
        self.size_slider = QSlider(Qt.Horizontal, self)
        self.size_slider.setTickPosition(QSlider.TicksBelow)
        self.size_slider.setTickInterval(10)  # Setting slider to have interval of every 10 ticks
        self.size_slider.setSingleStep(1)  # Each tick step is 1
        self.size_slider.setValue(100)
        self.size_slider.setMinimum(0)
        self.size_slider.setMaximum(300)
        self.size_slider.valueChanged.connect(self.glWidget.changeSize)

        # Speed slider label
        speed_label = QLabel(self)
        speed_label.setText("Adjust Orbit Speed:")
        speed_label.setFont(QFont("Arial", 11))
        speed_label.setFixedSize(200, 20)

        # Speed slider creation
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(1000)  
        self.speed_slider.setSingleStep(1) 
        self.speed_slider.setValue(0)
        self.speed_slider.setMinimum(-10000)
        self.speed_slider.setMaximum(10000)
        self.speed_slider.valueChanged.connect(self.glWidget.changeOrbit)

        # Orbit size slider label
        orbit_radius_label = QLabel(self)
        orbit_radius_label.setText("Adjust Orbit Radius:")
        orbit_radius_label.setFont(QFont("Arial", 11))
        orbit_radius_label.setFixedSize(200, 20)

        # Orbit size slider creation
        self.orbit_radius_slider = QSlider(Qt.Horizontal, self)
        self.orbit_radius_slider.setTickPosition(QSlider.TicksBelow)
        self.orbit_radius_slider.setTickInterval(100)  
        self.orbit_radius_slider.setSingleStep(1)  
        self.orbit_radius_slider.setValue(0)
        self.orbit_radius_slider.setMinimum(0)
        self.orbit_radius_slider.setMaximum(800)
        self.orbit_radius_slider.valueChanged.connect(self.glWidget.changeOrbitRadius)

        # Rotation slider label
        rotate_label = QLabel(self)
        rotate_label.setText("Adjust Rotation Speed:")
        rotate_label.setFont(QFont("Arial", 11))
        rotate_label.setFixedSize(200, 20)

        # Rotation slider creation
        self.rotate_slider = QSlider(Qt.Horizontal, self)
        self.rotate_slider.setTickPosition(QSlider.TicksBelow)
        self.rotate_slider.setTickInterval(10) 
        self.rotate_slider.setSingleStep(1)  
        self.rotate_slider.setValue(100)
        self.rotate_slider.setMinimum(0)
        self.rotate_slider.setMaximum(200)
        self.rotate_slider.valueChanged.connect(self.glWidget.changeRotation)


        # Using addWidget to add labels and sliders to layout
        #gui_layout.addWidget(planetlist)
        gui_layout.addWidget(size_label)
        gui_layout.addWidget(self.size_slider)

        gui_layout.addWidget(speed_label)
        gui_layout.addWidget(self.speed_slider)

        gui_layout.addWidget(orbit_radius_label)
        gui_layout.addWidget(self.orbit_radius_slider)

        gui_layout.addWidget(rotate_label)
        gui_layout.addWidget(self.rotate_slider)


    # selectPlanet function
    #
    # Function  called by combobox to select new planet for editing. Indexes through
    # sphereList and sets as current planet. Then sets sliders to current planet values.
    # Takes the following arguments:
    #   planet_index: The index of planet to choose
    def selectPlanet(self, planet_index):
        if (planet_index >= 0) and (planet_index < len(Sphere.sphereList)):
            selected_planet = Sphere.sphereList[planet_index]
            self.glWidget.selected_planet = selected_planet

            # Setting slider values to the values of the current selected planet
            self.size_slider.setValue(int(selected_planet.radius * 100))
            self.speed_slider.setValue(int(selected_planet.orbit_speed * 100))
            self.rotate_slider.setValue(int(selected_planet.rotation * 100))
            self.orbit_radius_slider.setValue(int(selected_planet.orbit_radius * 100))
        else:
            print("ERROR: Planet index out of range")


    # newPlanet function
    #
    # Function to create a new planet. Connects to the textbox for planet name creation
    def newPlanet(self, type):
        planet_name = self.textbox.text()
        self.textbox.setText("")

        # If textbox is empty, dont create planet
        if planet_name == "":
            print("ERROR: No name entered. No planet will be added.")

        # If name is already added, dont create planet to prevent doubles
        elif any(planet.name == planet_name for planet in Sphere.sphereList):
            print("ERROR: Planet with name (" + planet_name + ") already exists.")

        # If other conditions not met, proceed with planet creation
        else:
            # default values for new planet
            if type == 2:
                radius = random.random()
                orbit_radius = (random.random() * 10)

            elif type == 3:
                radius = 0.2
                orbit_radius = 4 + (random.random() * 10)

            else:
                radius = 1
                orbit_radius = (random.random() * 10)

            Sphere(planet_name, radius, orbit_radius, random.random() * 10, 1, type)

            self.planetlist.addItem(planet_name) # add new planet to combobox
            print("SUCCESS: Planet " + planet_name + " is now added") # test if worked


    # MainWindow class continued
    def addMoons(self):
        num_of_moons = self.moonbox.value()
        self.glWidget.selected_planet.moons = num_of_moons
        self.glWidget.update()


    # removePlanet function
    #
    # Function to remove a planet from the system. Uses the textbox to stop rendering
    # and remove from combobox
    def removePlanet(self):
        planet_name = self.textbox.text()
        self.textbox.setText("")

        # If no name entered, printing error message
        if planet_name == "":
            print("ERROR: No name entered. No planet will be deleted")
            return

        # continue to search through sphere list
        else:
            for planet in Sphere.sphereList:
                if planet.name == planet_name:
                    Sphere.sphereList.remove(planet)

                    index = self.planetlist.findText(planet_name) # finding index through planets name
                    self.planetlist.removeItem(index)

                    print("SUCCESS: Planet (" + planet_name + ") has been removed")
                    return

            # if planet is not found, print error message
            print("ERROR: Planet with name (" + planet_name + ") does not exist.")


    # asteroidBelt function
    #
    # Function to render asteroid belt to screen
    # Function creates 200 spheres, each with random attributes to create
    # variance between asteroids
    # Spheres created here are not editable and not apart of main sphere list
    def asteroidBelt(self):
        for i in range(200):
            radius = random.uniform(0.03, 0.1)
            orbit_radius = random.uniform(5, 6)  # Random orbit radius between 4 and 6
            orbit_speed = random.uniform(1, 1.2)  # Random orbit speed between 1 and 1.2
            rotation_speed = random.uniform(0, 2)  # Random rotation speed
            asteroid = Sphere(f"Asteroid_{i}", radius, orbit_radius, orbit_speed, rotation_speed, 4)

        self.glWidget.update()


    # removeBelt function
    #
    # Function clears the asteroidBelt list, removing from screen
    def removeBelt(self):
        Sphere.asteroidBelt.clear()
        self.glWidget.update()


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QGLWidget.__init__(self, parent)

        self.timer = QTimer(self)
        self.elapsed_timer = QElapsedTimer()  # time to track time passed for continuous translation
        self.elapsed_timer.start() # start timer

        self.timer.timeout.connect(self.update) # timer
        self.timer.start()

        self.sun = Sphere("Sun", 1.5, 0, 0, 1, 1)
        #self.asteroid = Sphere("ast", 0.1, 4, 2, 1, 3)
        #self.planet1 = Sphere("planet1", 1, 5, 1, 1, 2, 1)
        #self.planet1 =Sphere("planet1", 1, 4, 2, 1)
        #self.planet2 = Sphere("planet2", 1.5, 8, 1, 1)

        self.selected_planet = self.sun


    def initializeGL(self):
        self.qglClearColor(QColor(0, 0, 0))
        glEnable(GL_DEPTH_TEST)


    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)

        gluPerspective(50.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        # Camera view setup
        gluLookAt(0.0, 0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        elapsed_time = self.elapsed_timer.elapsed() / 1000.0 # timer to provide for render function

        # Sun
        self.sun.render(elapsed_time)

        # Loop to render all items in sphereList list
        for planet in Sphere.sphereList:
            planet.render(elapsed_time)

        # Loop to render all asteroids in asteroidbelt list
        for asteroid in Sphere.asteroidBelt:
           asteroid.render(elapsed_time)


    # changeSize function
    #
    # Function to modify a planet's radius size
    # Takes the following arguments:
    #   size: Value to apply to planet radius
    def changeSize(self, size):
        self.selected_planet.radius = size / 100 # Dividing by 100 to conform to coordinate system
        self.update()


    # changeOrbit function
    #
    # Function to modify a planet's orbit speed
    # Takes the following arguments:
    #   orbit: Value to apply to orbit speed
    def changeOrbit(self, orbit):
        self.selected_planet.orbit_speed = orbit / 100
        self.update()


    # changeRotation function
    #
    # Function to modify a planet's rotaional speed
    # Takes the following arguments:
    #   rotation: Value to apply to rotational speed
    def changeRotation(self, rotation):
        self.selected_planet.rotation = rotation / 100
        self.update()


    # changeOrbitRadius function
    #
    # Function to modify a planet's orbit radius
    # Takes the following arguments:
    #   radius: Value to apply to orbit radius
    def changeOrbitRadius(self, radius):
        #self.selected_planet.orbit_radius = self.selected_planet.orig_orbit_radius * (radius / 100)
        self.selected_planet.orbit_radius = radius / 100
        self.update()


    # colorPicker function
    #
    # Used to open color dialog box upon button press
    def colorPicker(self):
        self.openColorDialog()


    # openColorDialog function
    #
    # Function to open PyQt color dialog box and apply colors to selected object
    def openColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            print(self.selected_planet.name + " color : " + color.name()) # print object and its color to console
            if self.selected_planet:  # Ensure a planet is selected
                # set the selected objects colors accordingly
                self.selected_planet.color_red = color.red() / 255.0 # dividing by 255 to get decimal within 0 and 1
                self.selected_planet.color_green = color.green() / 255.0
                self.selected_planet.color_blue = color.blue() / 255.0
                self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
