# Rubik's Cube Player

[![Rubik's Cube Player](https://img.youtube.com/vi/KB_6W-52S08/0.jpg)](https://www.youtube.com/watch?v=KB_6W-52S08)


What is the Rubik's Cube Player?
================================

The Rubik's Cube Player is a python script written for the Drexel Music Hackathon that took place at the ExCITe Center from 1/28/17-1/29/17. It converts a face of a 3x3 Rubik's Cube into waveform data that is played over a speaker system by taking a picture of it with a webcam. The more solved a face is, the more harmonious it is designed to sound.

* * * 

How to Run
==========
The Rubik's Cube Player is run simply by calling: 

	> python3 main.py
	
within the project folder.

* * * 

Motivation
==========
This project was created as a part of the Drexel Music Hackathon with a goal of combining music and technology together. It was created in a less than 24 hour window.

* * * 

Installation
============
The Rubik's Cube Player is built on top of a couple technologies.

Pillow is used for image processing:
	
	> pip3 install Pillow
	
PyAudio is used to play Waveform:

	> sudo apt-get install python3-pyaudio
	
fswebcam and motion were used to preview the webcamera stream and to take quick pictures of the cube to be processed:

	> sudo apt-get install fswebcam
	> sudo apt-get install motion
	
To set up motion to work correctly, implement the follow tutorial:
https://pimylifeup.com/raspberry-pi-webcam-server/

* * *

Contributors
============
Hunter Heidenreich (me)

Emmanuel Espino (https://github.com/emanespino)

Jason Zogheb (jason.zogheb@gmail.com)
