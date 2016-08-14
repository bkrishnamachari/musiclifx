#!/usr/bin/env python
"""  Sets lifx light bulb brightness according to amplitude in 
         data file, in real time. 
      Bhaskar Krishnamachari, 8/14/16
      see License file for license details
"""
import sys
from time import sleep
import logging as log

VERBOSE = True   

if VERBOSE:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose output.")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")


import numpy

try:
    from lifxlan import *    #must have lifxlan 
except:
    log.error("lifxlan not installed.") 
    log.error("Please get it from https://github.com/mclarkk/lifxlan")
    sys.exit(1)
 
    
 


INIT_AMP= 32768                   #half of the max amplitude
SAMPLE_TIME = 0.04
DATA_FILENAME = "light_amp.dat"   #file to read amplitude values from
LAMP_COLOR = BLUE                 


lifx = LifxLAN(1)                 #initialize lifxLAN
# assuming only one light bulb

try:
    devices = lifx.get_lights()   
    bulb = devices[0]
    log.info("Acquired light bulb.")
except:
    log.error("Light bulb acquisition unsuccessful. Quitting.")
    sys.exit(2)

log.info("Turning on the light.")
bulb.set_power("on")
bulb.set_color(LAMP_COLOR)

try:
    h, s, b, k = bulb.get_color()
except:
    log.error("Unable to get color. Quitting!")
    sys.exit(3)

amp_old = INIT_AMP 

while (True):
    sleep(SAMPLE_TIME)

    try: 
        f = open(DATA_FILENAME)  	
    except:
        log.error("Unable to open data file. Quitting!")
        sys.exit(4)

    try: 
        amp  = int(f.readline())
    except:      
        log.warning("Unable to read line in data file.")
        amp  = amp_old    	#fill in with prev value 

    log.info("Setting brightness to "+str(amp)) 
    try:
        bulb.set_color((h, s, amp, k))
    except:    
        log.warning("Unable to set color.")
        pass			#in case of any comm failure

    amp_old = amp
    f.close()


"""
# ACKNOWLEDGEMENTS: this program uses code from:
# http://stackoverflow.com/questions/5980042/how-to-implement-the-verbose-or-v-option-into-a-script
"""
