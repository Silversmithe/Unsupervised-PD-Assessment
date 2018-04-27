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
from threading import Thread, ThreadError, Lock
from Filter import RawDataFilter
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
WEARABLE DEVICE

Keeps track of general statistics and characteristics of the radio
mounted on the wearable device in communication with this specific
server.
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
GLOBAL VARIABLES

Used for IPC between threads as well as general book keeping for 
the entire console system with reference to the wearable device
in communication.
"""

UpdaWear = Wearable()
MessageBuffer = list()
BufferLock = Lock()

"""
INSTANCE LOADER

takes all the raw data over the radio and passes it through a filter
Listens to an array that is populated by the XBee server and uses it to 
filter and process instances for certain files
"""


class InstanceLoader(Thread):

    def __init__(self, file_count):
        Thread.__init__(self)
        self.__raw_instances = list()
        self.__file_count = file_count  # file count
        self.raw_filter = RawDataFilter()
        self.__file = None

    def run(self):
        """
        Given a list of samples, open up or append a new file and start
        writing the information there
        :return:
        """
        __running = True
        try:
            while __running:

                # if MessageBuffer past Sample threshold, take them and start processing them
                # eventually would be nice: len(MessageBuffer) >= 200
                if len(MessageBuffer) > 0 and len(self.__raw_instances) <= 1:
                    with BufferLock:
                        self.__raw_instances = list(MessageBuffer)
                        MessageBuffer.clear()

                elif len(self.__raw_instances) > 0:
                    # process the values that are in your buffer
                    # instances are byte arrays
                    # payloads are twins

                    while len(self.__raw_instances) > 0:
                        # look at opcode
                        instance = int(str(self.__raw_instances[0][0]), 16)

                        if instance == self.raw_filter.BROADCAST_MSG:
                            # okay cool, do not need to store
                            print("msg: received device broadcast")
                            pass

                        elif instance == self.raw_filter.OLD_DATASEG_MSG:
                            # okay cool, do not need to store FOR NOW
                            pass

                        elif instance == self.raw_filter.NEW_DATASEG_MSG:
                            # okay need to open a new file
                            self.__file_count += 1          # increment file count for new file name
                            if self.__file is not None:     # close any previously open file
                                self.__file.close()

                            # create a new file to write to
                            self.__file = open("./data/patient-{}.txt".format(self.__file_count), "w")
                            print("msg: created new patient session")

                        elif instance == self.raw_filter.PAYLOAD_MSG:
                            # pass data through payload filter
                            if len(self.__raw_instances) > 1:
                                if int(str(self.__raw_instances[0][1]), 16) == int(str(self.__raw_instances[1][1]), 16):
                                    _, _, _data = self.raw_filter.process(self.__raw_instances[0], self.__raw_instances[1])
                                    self.__raw_instances.pop(0)  # pop the first val, the next is popped at end of loop
                                    # write to file
                                    for value in _data:
                                        self.__file.write('{}\t'.format(value))
                                    self.__file.write('\n')  # end with a newline

                                else:
                                    # second part of packet did not show up, so the packet is not useful
                                    print("warning: unable to find packet pair")
                                    pass

                        else:
                            # should be the CLOSE Message
                            # close all files
                            print("closing instance manager thread...")
                            if self.__file is not None:
                                self.__file.close()
                            __running = False
                            break

                        self.__raw_instances.pop(0)

                else:
                    time.sleep(1)

        finally:

            if self.__file is not None:
                self.__file.close()


"""
SERVER

code to run the actual server that communicates with the wearable
device via the XBee connected via USB serial port.
"""


def run_server():
    """
    Xbee Server
    :return:
    """
    # INIT SERVER
    print("starting run_server...")
    UpdaWear.reset()
    MessageBuffer.clear()

    server = Raw802Device(PORT, BAUD_RATE)
    UpdaWear.id = "UPDA-WEAR-1"
    UpdaWear.address = XBee16BitAddress.from_hex_string(WEAR_16B_ADDR)
    UpdaWear.remote = RemoteRaw802Device(server, UpdaWear.address)
    instance_manager = None
    exit_message = bytearray([0x05, 0x00])

    try:
        # might not want this
        if not os.path.exists('./data'):
            print("unable to find './data' to store information")
            raise KeyboardInterrupt

        # get patient count to make a new file
        num_patients = len([name for name in os.listdir('./data')])

        instance_manager = InstanceLoader(num_patients)
        instance_manager.start()  # start the thread
        server.open()

        def msg_callback(message):
            UpdaWear.received_count = UpdaWear.received_count + 1
            # register the device
            # print("{} >> {}".format(server.get_16bit_addr(), message.data.decode()))
            # pass information off to a buffer
            # store the data (byte array)
            with BufferLock:
                MessageBuffer.append(message.data)

        server.add_data_received_callback(msg_callback)

        print("press enter to stop run_server...")
        input()

    except KeyboardInterrupt:
        print()  # add a space so everything is nearly on a different line

    except serial.serialutil.SerialException:
        print("Unable to open {}".format(PORT))

    finally:

        if instance_manager is not None:
            # close instance manager
            with BufferLock:
                MessageBuffer.append(exit_message)
            instance_manager.join()

        if server is not None and server.is_open():
            server.close()

    print("closing run_server...")


"""
Simple UPDA CONSOLE

functions that are triggered based on input from the actual 
console system.
"""


def stats(tokens):
    """
    :param tokens:
    :return:
    """
    print("stats from previous run_server session...")
    print("previously linked with: {}".format(UpdaWear.id))
    print("address: {}".format(UpdaWear.address))
    print("received messages: {}".format(UpdaWear.received_count))
    print("known wearable runtime: {} seconds".format(0.01 * UpdaWear.received_count))


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
