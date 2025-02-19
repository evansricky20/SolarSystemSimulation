<h1>User Manual</h1>
This document is the user manual for my submission for the star system project. This document will provide details on how to run, launch, and operate the program. Additional details on code and operations not with the user interface will be provided as well.

<h2>SET UP</h2>
This program requires you to have a recent version of Python, at least version 3.10.11 installed on your system. In addition to this, multiple libraries are used. You must have the PyQt5, OpenGL.GL, OpenGL.GLU, sys, math, and random libraries installed. Specific imports are as follows:
<br/>1.	import sys
<br/>2.	from PyQt5.QtCore import *
<br/>3.	from PyQt5.QtGui import *
<br/>4.	from PyQt5.QtOpenGL import *
<br/>5.	from PyQt5.QtWidgets import *
<br/>6.	from OpenGL.GL import *
<br/>7.	from OpenGL.GLU import *
<br/>8.	import math
<br/>9.	import random

<h2>USER INTERFACE</h2>
With the program running and the main window launched, you should be presented with a window titled “Solar System Simulation”. It is here where all will take place. If all is running as it should, the OpenGL window should contain a single yellow sphere. This is the star of your system. It is the basis in which all objects will rotate around. Below the OpenGL window will be the user interface. It is here where you will interact with the star system. 

<h3>Object Selection</h3>
Starting at the top left, you will see a label that says “Object Selection”. Below it is the object selection drop down box. Clicking on it will display all currently rendered objects in the system. Since only the sun is rendered, the dropdown should only contain one object named “Sun”. With the creation of planets and asteroids, the dropdown box will be filled with their names. The names of these objects are up to you.

<h3>Object Naming and Moon Creation</h3>
Moving on to the right, you will see two labels, “Object Name” and “Add Moons”. It is here where you can enter a name for your desired object as well as create moons for your selected object. When an object is selected in the object selection dropdown box, you can use the spin box to add up to 3 moons to it. These moons will have default settings. Presenting with a small gray appearance. Moons rotate based on the orbital speed of its planet, the higher the planet's orbital speed, the faster the moons orbit the planet. 

<h3>Planet and Asteroid Creation and Removal</h3>
Moving on to the right you will see three buttons in a vertical layout: Add Planet, Add Asteroid, and Remove object. The Add Planet button will create a new planet with the name entered in the Object Name text box. If no name is given, an error message will appear in the Python console, and no planet will be added. If you attempt to create a planet of the same name as one currently being rendered, an error message will appear in the python console and the planet will not be created. This functionality also applies to the Add Asteroid button.
The Remove Object button does the opposite. After entering an object's name in the Object Name textbox, you can select the Remove Object button to remove it from the scene. This will delete the object and any of its moons from being rendered as well as from the list. There is no undoing a deletion.

<h3>Object Color and Asteroid Belt Creation and Removal</h3>
Moving on to the far right of the interface you will be presented with another three buttons: Choose Color, Add Belt, and Remove Belt. Starting from the top, the Choose Color button makes use of PyQt’s color dialog window. Clicking this button will open a new window titled “Select Color”. Here you can pick any color by either using the interactive color display, inputting RGB values, inputting Hex values, or by using the pick screen color tool to choose a color from anywhere on your screen. To make use of this feature, you must first select the desired object in the “Object Selection” drop down box. Once you have a celestial body selected, click the “Choose Color” button to proceed with color customization. Once you have a color selected, press the “OK” button to see your newly colored object.
Moving on to the “Add Belt” button, it is here where you can choose to display an asteroid belt in your system. Much like our own solar system, this button will create an asteroid belt made up of 200 asteroids, each with its own variance in shape, orbital speed, and color. If you decide you no longer want an asteroid belt, you can click the “Remove Belt” button to simple stop rendering. 

<h3>Object Sliders</h3>
Last but not least are the sliders. Located on the bottom portion of the window are four individual sliders. These sliders from top to bottom perform the following: Adjust the radius size of the selected object, adjust the orbital speed of the selected object, adjust the orbital radius of the selected object, adjust the rotation of the selected object. 
Starting with the “Adjust Radius Size” slider, you can edit your selected object to have a radius anywhere from 0 to 3 units. Moving the slider to the left will decrease the radius size, while moving to the right will increase it. 
Next is the “Adjust Orbit Speed” slider. Here you can adjust the orbital speed to be anywhere from -1000 to 1000 units. Negative speed will result in a counterclockwise orbit, with positive speed resulting in a clockwise orbit. The closer to 0 you get the slower the object will orbit the sun. 
Next up is the “Adjust Orbit Radius” slider. With this slider you can adjust the orbital radius of your selected object from 0 to 8 units. 0 units will result in a smaller radius closer to the center of the screen, with 8 units being at the far edges.
At the very bottom we have the “Adjust Rotation Speed” slider. It is here where you can adjust the rotation speed of your selected object. You can adjust the rotation to be anywhere from 0 units to 2 units, with 0 being no rotation.
