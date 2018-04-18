#! /usr/bin/python

"""
server.py

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
BAUD_RATE = 9600
SERVER_NAME = "SERVE"
SERVER_64B_ADDR = "0013A2004163FE2F"
SERVER_16B_ADDR = "FE2F"
WEAR_64B_ADDR = "0013A2004163FE31"
WEAR_16B_ADDR = "FE31"
# SD CARD
SD_PATH = "/media/iron-fist/WEARV2"
SD_DATA_PATH = "/media/iron-fist/WEARV2/DATA.txt"
# MESSAGES
DATA_ACK_CONNECT = "ACK_CONNECT"
NULL_ADDR = XBee16BitAddress.from_hex_string("0x0000")


"""
XBEE SERVER 
"""


class Wearable(object):
    
    def __init__(self):
        self.id = "unknown"
        self.address = XBee16BitAddress.from_hex_string("0x0000") 
        self.received_count = 0
        self.sent_count = 0
        self.remote_device = None

    def reset(self):
        self.id = "unknown"
        self.address = XBee16BitAddress.from_hex_string("0x0000") 
        self.received_count = 0
        self.sent_count = 0
        self.remote_device = None


# create a device object
upda_wear = Wearable()


def server():
    """
    Xbee Server
    :return:
    """
    upda_wear.reset()

    # INIT SERVER
    print("starting server...")
     
    device = Raw802Device(PORT, BAUD_RATE)
    remote = RemoteRaw802Device(device, x16bit_addr=XBee16BitAddress.from_hex_string(WEAR_16B_ADDR)) 

    try:
        device.open()


        def msg_callback(xbee_message):
            upda_wear.received_count = upda_wear.received_count + 1
            print("{} >> {}".format(remote.get_16bit_addr(), xbee_message.data.decode()))
            #device.send_data_async(remote, "hello")

        device.add_data_received_callback(msg_callback)

        print("press enter to stop server...")
        input()

    except KeyboardInterrupt:
        pass # just escaping the loop

    except serial.serialutil.SerialException:
        print("Unable to open {}".format(PORT))

    finally:
        if device is not None and device.is_open():
            device.close()

    print("closing server...")


"""
Simple UPDA CONSOLE
"""


def stats(tokens):
    """
    :param tokens:
    :return:
    """
    print("stats from previous server session...")
    print("previosly linked with: {}".format(upda_wear.id))
    print("address: {}".format(upda_wear.address))
    print("received messages: {}".format(upda_wear.received_count))


def start(tokens):
    """
    start server
    start server with render
    :param tokens:
    :return:
    """
    if len(tokens) <= 1:
        print("no object specified...")
        return

    if tokens[1] == "server":
        # start server procedure
        server()

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

            with open(SD_DATA_PATH, 'w') as dfile:
                print("wiping SD card data...")
                try:
                    dfile.truncate()
                    print("process complete!")

                except OSError:
                    print("error: could not clear SD card")

        if len(tokens) > 1:
            if tokens[1] == 'and' and tokens[2] == 'process':
                print("\nloading patient data into scoring process...")
                # pass data off to evaluation

            else:
                print("undefined load conjunction")
                print("try: 'load and process'")


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
        patients = [name for name in os.listdir('./data')]
        print("number of patient records on disk: {}".format(len(patients)))
        # list all the files
        print("./data:")
        for i in patients:
            print(i)

    else:
        print("unknown object to list...")


def list_cmds(tokens):
    """
    :param tokens:
    :return:
    """
    print(" help\t\t\texplains what all the commands do\n",
          "quit\t\t\tterminates the program\n",
          "start server\t\tinitialize a server to read xbee\n",
          "stats\t\t\tinformation on overall server stats\n",
          "load\t\t\tdownload patient information from a certified SD card\n",
          "list <object>\t\tlists all items wrt object specified. try 'patients'")


def terminate(tokens):
    """
    :param tokens:
    :return:
    """
    global RUNNING
    RUNNING = False


command_list = {
    "quit": terminate,
    "exit": terminate,
    "start": start,
    "help": list_cmds,
    "stats": stats,
    "load": load,
    "list": list_items
}


def main():
    """
    create a main console that is responsible for the gathering and control of the
    server
    :return:
    """
    print('*'*50)
    print("\n  .----.-----.-----.-----.\n",
          "/      \     \     \     \\\n",
          "|  \/    |     |   __L_____L__\n",
          "|   |    |     |  (           \\\n",
          "|    \___/    /    \______/    |\n",
          "|        \___/\___/\___/       |\n",
          "|      \     /               /\n",
          "|                        __/\n",
          "\_                   __/\n",
          "|        |         |\n",
          "|                  |\n",
          "|                  |\n\n")

    print("Unsupervised Parkinson's Disease Assessment Console")
    print("Version {}".format(VERSION), '\n')
    print('*' * 50, '\n')

    while RUNNING:
        try:
            message = input(">>> ")

            tokens = message.lower().split(sep=" ")

            if tokens[0] in command_list:
                # in the command list
                command_list[tokens[0]](tokens)
            else:
                # not in the command list
                print("cannot process '{}'".format(message))

            print()

        except KeyboardInterrupt:
            print()
            break

    print("goodbye...")


if __name__ == '__main__':
    main()
