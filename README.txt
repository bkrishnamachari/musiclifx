Play music with synchronized LIFX light bulb

Bhaskar Krishnamachari, August 14, 2016

This software allows the user to play a wave file
and synchronize the brightness of a lifx lamp to it in real time. 

The code needs a file named chopin.wav to be placed in the directory. This file can be obtained from: 
https://archive.org/details/Chopin-NocturneOp.9No.2
(The file name could of course be changed in the code if a different file is used).

There are two main python files included here; they must both be run simultaneously (say in different terminals):

1. playmusic.py: reads the wav file and sets amplitude in data file, in real time. uses pyaudio (pyaudio can be installed using sudo apt-get install python-pyaudio python3-pyaudio) 

2. playlight.py: Sets lifx light bulb brightness according to amplitude in data file, in real time. uses lifxlan, from https://github.com/mclarkk/lifxlan

There is one additional python file included called mute_alsa.py, this is optional, and could help suppress some alsa/pyaudio error messages that pop up when running playmusic.py

There is one shell script included as well: 

play.sh: a bash script file that runs both of the above programs as background process. Provided just for convenience. May be best to run the two programs separately.

The program will create a dat file in the working directory for logging and reading amplitude values


Notes: 

* To stop printing all information, set VERBOSE=False in both files; to turn on printing of all information, set VERBOSE = True

* Tested on Python version 2.7.12, Ubuntu 16.04.1 LTS

tags: lifx music 
