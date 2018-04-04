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

#!/bin/bash
# import and initialize xbee
from xbee import *
import serial

"""
GLOBAL VARIABLES
"""
# Parameters
VERSION = 1
PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600                # change later to higher most likely
# Status variables
SERV_RADIO_ON = False
MODE = RENDER

"""
    Function Definitions
"""
def error(msg):
    print("error: {}".format(msg))

def die():
    pass


if __name__ == '__main__':
    """
        Print Banner for Program
    """
    print("*** UPDA Server v{} ***".format(VERSION))

    """
        Establishing Serial Connection
        with the Xbee
    """
    # open the serial port
    try:
        serial_port = serial.Serial(PORT, BAUD_RATE);
        SERV_RADIO_ON = True
    except serial.SerialException:
        error("unable to find server radio")

    # start the loop if and only if the server radio
    # has established a connection with the servial port
    if SERV_RADIO_ON:
        # create API object
        xbee = Zigbee(serial_port)

        # continuously read and print packets
        while True:
            try:
                # prossess and send the information
                response = xbee.wait_read_frame()
                print(response)
                # should send an acknowledgement
                # process data and store somewhere

            except KeyboardInterrupt:
                break

        # close the serial port
        # send a signal to
        ser.close();

    # closing the program
    print("*** server closing ***")
    # die function
    die()
    print("*** goodbye ***")
