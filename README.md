Decibels to Input
This is a Python program that converts sound levels (decibels) into an input action using the PyAutoGUI library. The program listens for sounds above a set decibel threshold and triggers an input action (default is left mouse click).

Features
Microphone Selection
At the start of the program, you'll be prompted to select your microphone from a list of available input devices. Simply type the number next to your desired device to set it as the input source.

Adjustable Decibel Threshold
Set the minimum decibel level required to trigger the input action. Modify this in line 11.

Customizable Input Action
Change the input action triggered when the decibel threshold is met (default is left mouse click). Update this setting on line 38 using PyAutoGUI.

Duration Control
Define how long the program will run for (default is 120 seconds). Change this in line 8.
