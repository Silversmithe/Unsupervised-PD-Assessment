#! /usr/bin/python

"""
server.py

by Alexander Adranly, 2018

real credit goes to Paul Malmsten
for providing the example

This example continuously reads the serial 
port and processes IO data recieved from a 
remote Xbee.
"""

# import and initialize xbee
from xbee import Xbee, Zigbee
import serial

PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600        # change later

# open the serial port
ser = serial.Serial(PORT, BAUD_RATE);

# create API object
xbee = Xbee(ser)

# continuously read and print packets
while True:
    try:
        response = xbee.wait_read_frame()
        print response

    except KeyboardInterrupt:
        break

# close the serial port
# send a signal to
ser.close();
