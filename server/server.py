#! /usr/bin/python

"""
run_server.py

by Alexander Adranly, 2018

NOTE: use the arg parse library for command-line tools
"""

# !/bin/bash
import os
import time
import serial
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, Raw802Device, RemoteRaw802Device
from digi.xbee.models.address import XBee16BitAddress, XBee64BitAddress

# GLOBALS
VERSION = 1
RUNNING = True
# SERVER
PORT = "/dev/ttyUSB0"
BAUD_RATE = 57600
SERVER_NAME = "SERVE"
SERVER_64B_ADDR = "0013A2004163FE2F"
SERVER_16B_ADDR = "FE2F"
WEAR_64B_ADDR = "0013A2004163FE31"
WEAR_16B_ADDR = "FE31"
# SD CARD
SD_PATH = "/media/iron-fist/UPDA-SD"
SD_DATA_PATH = "/media/iron-fist/UPDA-SD/DATA.txt"


"""
XBEE SERVER 
"""


class Wearable(object):
    
    def __init__(self):
        self.id = "unknown"
        self.address = XBee16BitAddress.from_hex_string("0x0000") 
        self.received_count = 0
        self.sent_count = 0
        self.remote = None
        self.runtime = 0

    def reset(self):
        self.id = "unknown"
        self.address = XBee16BitAddress.from_hex_string("0x0000") 
        self.received_count = 0
        self.sent_count = 0
        self.remote = None
        self.runtime = 0


"""
XBee Wearable Devices
"""
upda_wear = Wearable()


"""
Server
"""


def run_server():
    """
    Xbee Server
    :return:
    """
    # INIT SERVER
    print("starting run_server...")
    upda_wear.reset()

    server = Raw802Device(PORT, BAUD_RATE)
    upda_wear.id = "UPDA-WEAR-1"
    upda_wear.address = XBee16BitAddress.from_hex_string(WEAR_16B_ADDR)
    upda_wear.remote = RemoteRaw802Device(server, upda_wear.address)

    try:
        # might not want this
        if not os.path.exists('./data'):
            print("unable to find './data' to store information")
            raise KeyboardInterrupt

        server.open()

        def msg_callback(message):
            upda_wear.received_count = upda_wear.received_count + 1
            # register the device
            print("got it!")
            # print("{} >> {}".format(server.get_16bit_addr(), message.data.decode()))
            # pass information off to a buffer

        server.add_data_received_callback(msg_callback)

        print("press enter to stop run_server...")
        input()

    except KeyboardInterrupt:
        pass  # just escaping the loop

    except serial.serialutil.SerialException:
        print("Unable to open {}".format(PORT))

    finally:
        if server is not None and server.is_open():
            server.close()

    print("closing run_server...")


"""
Simple UPDA CONSOLE
"""


def stats(tokens):
    """
    :param tokens:
    :return:
    """
    print("stats from previous run_server session...")
    print("previously linked with: {}".format(upda_wear.id))
    print("address: {}".format(upda_wear.address))
    print("received messages: {}".format(upda_wear.received_count))
    print("known wearable runtime: {} seconds".format(0.01 * upda_wear.received_count))


def start(tokens):
    """
    start run_server
    start run_server with render
    :param tokens:
    :return:
    """
    if len(tokens) <= 1:
        print("no object specified...")
        return

    if tokens[1] == "server":
        # start run_server procedure
        run_server()

    else:
        print("unknown object to start...")


def load(tokens):
    """
    :param tokens:
    :return:
    """
    print("downloading patient information from sd...")
    if not os.path.isdir(SD_PATH):
        # cannot find the SD card
        print("SD card {} does not exist".format(SD_PATH))
    
    else:
        # found the SD card
        # check for the DATA file
        print("SD card {} found".format(SD_PATH)) 
        if not os.path.exists(SD_DATA_PATH):
            print("cannot continue: {} not found".format(SD_DATA_PATH))
        else:
            # download file
            with open(SD_DATA_PATH, 'r') as dfile:
                content = dfile.read()
                content = content.split(sep='----- datafile -----')

                print("{} sets of patient data found".format(len(content)-1))
                print("downloading patient data")

                bar_size = 50

                if not (len(content)-1 <= 0):
                    step = int(bar_size/(len(content)-1))

                    # how many patient files exist so far
                    num_patients = len([name for name in os.listdir('./data')]) 

                    # download files
                    for i in range(1, len(content)):
                        print('|','%'*(step*i), ' '*(bar_size - (step*i)), '|', end='\r')
                        try:
                            f = open("data/patient-{}.txt".format(str(i+num_patients)), 'w')
                            f.write(content[i])
                            f.close()

                        except BlockingIOError:
                            print("\nerror: could not open new patient file")
                            break

                    else:
                        print("\ndownload complete!")

            # with open(SD_DATA_PATH, 'w') as dfile:
            #     print("wiping SD card data...")
            #     try:
            #         dfile.truncate()
            #         print("process complete!")
            #
            #     except OSError:
            #         print("error: could not clear SD card")


def list_items(tokens):
    """
    :param tokens:
    :return:
    """
    if len(tokens) <= 1:
        print("specify an object to list:")
        print("patients")
        return

    if tokens[1] == 'patients':
        if os.path.exists('./data'):
            patients = [name for name in os.listdir('./data')]
            print("number of patient records on disk: {}".format(len(patients)))
            # list all the files
            print("./data:")
            for i in patients:
                print(i)
        else:
            print("cannot find path './data'")

    else:
        print("unknown object to list...")
