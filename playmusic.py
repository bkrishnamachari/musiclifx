#!/usr/bin/env python
""" 
    Program to play a given wav audio file and 
    print scaled amplitude values to a data file in real time. 
    Bhaskar Krishnamachari, 8/14/16
    see License file for license details
"""

import sys
import wave
import logging as log

import numpy
import pyaudio

try: 
    import mute_alsa  #not essential, just to mute some error messages
except:
    pass

log.basicConfig(format="%(levelname)s: %(message)s")

## file names
FILENAME = "chopin.wav"		#audio file 
DATA_FILENAME = "light_amp.dat" #file to write amp data to

#number of audio samples to process at each time
CHUNKSIZE = 1024

#scaling parameters
OFFSET = 3000
GAIN   = 12

#filter parameter
FILTER_WEIGHT = 0.5

#constants related to amplitude
MAX_AMP    = 65535
MIN_AMP    = 1
HALF_AMP =  32768

def filter(ar, a_old):
    """ scales, filters, and clamps raw amplitude values """ 
    a = (ar-OFFSET)*GAIN                                #scaling
    a = FILTER_WEIGHT*a_old + (1-FILTER_WEIGHT)*a   	#filter
    a = max(min(int(a), MAX_AMP), MIN_AMP)   		#clamp
    a_old = a                                           #last value
    return a, a_old

def write_to_file(a):
    """ write amplitude to data file """
    try:
        f = open(DATA_FILENAME, 'w')
        f.write(str(a))
        f.close()
    except:
        log.error("Data file I/O error.")
        sys.exit(2)

# open wav file 
try:
    wf = wave.open(FILENAME, 'rb')   
except:
    log.error("Unable to open wav file: %s ... Quitting!" % FILENAME)
    sys.exit(1)

# open and set up audio stream
p = pyaudio.PyAudio()
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# read the first chunk
data = wf.readframes(CHUNKSIZE)
    
amp_old = HALF_AMP

# keep reading the file and writing the amp from it to file
while data != '':
    stream.write(data)   #play the sound

    npdata = numpy.fromstring(data, dtype=numpy.int16)  #read it as array

    raw_amp = int(numpy.max(npdata))   #max of array is raw amp
    amp, amp_old = filter(raw_amp, amp_old) #get scaled, filtered amplitude
    write_to_file(amp)

    data = wf.readframes(CHUNKSIZE)

# close stream
stream.stop_stream()
stream.close()
p.terminate()

"""
#ACKNOWLEDGEMENTS: This program utilizes code from: 
#* http://stackoverflow.com/questions/6951046/pyaudio-help-play-a-file  
#* http://stackoverflow.com/questions/24974032/reading-realtime-audio-data-into-numpy-array
#* http://stackoverflow.com/questions/7088672/pyaudio-working-but-spits-out-error-messages-each-time
#* http://stackoverflow.com/questions/36956083/how-can-the-terminal-output-of-executables-run-by-python-functions-be-silenced-i/36966379#36966379
"""
