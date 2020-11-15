#!/usr/bin/python

# Application for reading data from SDS011, SDS018 and SDS021 dust sensors.
# USAGE: "python dust-sensor-read.py" or "python dust-sensor-read.py /dev/ttyUSB1"
#
# Forked from: https://github.com/aqicn/sds-sensor-reader
# Credits: Matjaz Rihtar, Matej Kovacic

import os
import sys
import time
import serial
#os.system("sudo uhubctl/uhubctl -a on -l 2")

# Reopen sys.stdout with buffer size 0 (unbuffered)
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w')

# Set default USB port
USBPORT = "/dev/ttyUSB0"
time.sleep(5) #booting time for the sensor

class SDS021Reader:

    def __init__(self, inport):
        self.serial = serial.Serial(port=inport, baudrate=9600)

    def readValue( self ):
        step = 0
        while 1: 
            while self.serial.inWaiting() != 0:
                v = ord(self.serial.read())

                if step == 0:
                    if v == 170:
                        step = 1

                elif step == 1:
                    if v == 192:
                        values = [0,0,0,0,0,0,0]
                        step = 2
                    else:
                        step = 0

                elif step > 8:
                    step = 0
                    # Compute PM2.5 and PM10 values
                    pm25 = (values[1]*256 + values[0])/10
                    pm10 = (values[3]*256 + values[2])/10
                    return [pm25,pm10]

                elif step >= 2:
                    values[step - 2] = v
                    step = step + 1


    def read( self ):
        species = [[],[]]
        i =1
        while i<10:
            try:
                values = self.readValue()
                species[0].append(values[0])
                species[1].append(values[1])
                return(values[0], values[1])
            except KeyboardInterrupt:
                print("Quit!")
                sys.exit()
            except:
                e = sys.exc_info()[0]
                print("Can not read sensor data! Error description: " + str(e))
            i = i+1
def loop(usbport):
    os.system("sudo uhubctl/uhubctl -a on -l 2")
    reader = SDS021Reader(usbport)
    pm25 = []
    pm10 = []
    i = 1 
    while i<=30:
        val = reader.read()
        pm10.append(val[0])
        pm25.append(val[1])
        i = i+1
    os.system("sudo uhubctl/uhubctl -a off -l 2") 
    return (sum(pm10)/30,sum(pm25)/30)

#if len(sys.argv)==2:
#    if sys.argv[1].startswith('/dev'):  # Valid are only parameters starting with /dev
#        loop(sys.argv[1])
#    else:
#        loop(USBPORT)
#else:
#    loop(USBPORT)
#	os.system("sudo uhubctl/uhubctl -a off -l 2")
