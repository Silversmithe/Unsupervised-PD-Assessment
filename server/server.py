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
from threading import Thread, Lock
from MatrixBuilder import extract
from analysis.MahonyFilter import MahoneyFilter
from analysis.RawDataFilter import RawDataFilter
from PipelineManager import PipelineManager
from digi.xbee.devices import Raw802Device, RemoteRaw802Device
from digi.xbee.models.address import XBee16BitAddress

# GLOBALS
VERSION = 1
RUNNING = True
# SERVER
PORT = "/dev/ttyUSB0"
BAUD_RATE = 38400  # 57600
SERVER_16B_ADDR = "FE2F"
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
        __packet_extend = False
        try:
            print("starting instance loader thread...")
            while __running:

                # if MessageBuffer past Sample threshold, take them and start processing them
                # eventually would be nice: len(MessageBuffer) >= 200
                if len(MessageBuffer) > 0 and len(self.__raw_instances) <= 1:
                    with BufferLock:
                        self.__raw_instances.extend(MessageBuffer)  # extend, do not overwrite what you already have
                        MessageBuffer.clear()

                elif len(self.__raw_instances) == 1:
                    instance = int(str(self.__raw_instances[0][0]), 16)
                    if instance == self.raw_filter.OLD_DATASEG_MSG:
                        print("msg: continuing previous session")
                        self.__raw_instances.pop(0)

                    if instance == self.raw_filter.CLOSE_MSG:
                        __running = False
                        self.__raw_instances.pop(0)
                        continue

                elif len(self.__raw_instances) > 1:
                    # process the values that are in your buffer
                    # instances are byte arrays
                    # payloads are twins

                    while len(self.__raw_instances) > 1:
                        # look at opcode
                        instance = int(str(self.__raw_instances[0][0]), 16)

                        ######################
                        # BROADCAST MESSAGES #
                        ######################
                        if instance == self.raw_filter.BROADCAST_MSG:
                            # okay cool, do not need to store
                            print("msg: received device broadcast")
                            pass

                        #####################
                        # OLD DATA MESSAGES #
                        #####################
                        elif instance == self.raw_filter.OLD_DATASEG_MSG:
                            # okay cool, do not need to store FOR NOW
                            print("msg: continuing previous session")
                            pass

                        #####################
                        # NEW DATA MESSAGES #
                        #####################
                        elif instance == self.raw_filter.NEW_DATASEG_MSG:
                            # okay need to open a new file
                            self.__file_count += 1          # increment file count for new file name
                            if self.__file is not None:     # close any previously open file
                                self.__file.close()

                            # create a new folder for raw file
                            if not os.path.exists("./data/data-{}".format(self.__file_count)):
                                os.mkdir("./data/data-{}".format(self.__file_count))

                            # create a new file to write to
                            self.__file = open("./data/data-{}/raw.txt".format(self.__file_count), "w")
                            print("msg: created new data session")

                        ####################
                        # PAYLOAD MESSAGES #
                        ####################
                        elif instance == self.raw_filter.PAYLOAD_MSG:
                            # pass data through payload filter
                            if len(self.__raw_instances) > 1:
                                # check packet id's 
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
                                    print("{} {}".format(int(str(self.__raw_instances[0][1]), 16), int(str(self.__raw_instances[1][1]),16)))
                                    # continue  # see if it shows up later

                            else:
                                # if there is 1 or zero packets, do not throw them away
                                # wait for the next batch to come in to see if the 
                                # twin is there
                                print("did i get here?")
                                pass

                        ####################
                        # PROCESS MESSAGES #
                        ####################
                        # tell a thread to handle the scoring of the current patients so far

                        ##################
                        # CLOSE MESSAGES #
                        ##################
                        else:
                            # should be the CLOSE Message
                            # close all files
                            print("closing instance loader thread...")
                            if self.__file is not None:
                                self.__file.close()
                            __running = False
                            break

                        # always remove message after using it
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

        # get data count to make a new file
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
    start process
    start process data-1
    :param tokens:
    :return:
    """
    if len(tokens) <= 1:
        print("no object specified...")
        return

    if tokens[1] == "server":
        # start run_server procedure
        run_server()

    # command to explicitly start processing data
    if tokens[1] == "process":

        if len(tokens) > 2:
            # specifying an object to process
            patient_name = tokens[2]
            print("process {}".format(patient_name))
            # check if data exists
            if not os.path.exists("./data/{}".format(patient_name)):
                print("error: unable to find ./data/{} to process".format(patient_name))

            # check if data has been processed
            # if data has a pdf score, then it has been processed
            if os.path.exists("./data/{}/UPDAReport.pdf"):
                print("{} has already been processed".format(patient_name))

            # process
            manager = PipelineManager(patient_path="./data/{}".format(patient_name))
            manager.start()
            manager.join()
            print("{} processing complete".format(patient_name))

        else:
            # FEATURE TO COME
            # just process the first (or all)
            print("process all patients")
            # get all patients
            # check if data has been processed
            # process
            pass

    else:
        print("unknown object to start...")
        print("options to run:\nstart server\nstart process\nstart process <data-name>")


def load(tokens):
    """
    :param tokens:
    :return:
    """
    print("downloading data information from sd...")
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

                print("{} sets of data data found".format(len(content)-1))
                print("downloading data data")

                bar_size = 50

                if not (len(content)-1 <= 0):
                    step = int(bar_size/(len(content)-1))

                    # how many data files exist so far
                    num_patients = len([name for name in os.listdir('./data')]) 

                    # download files
                    for i in range(1, len(content)):
                        print('|','%'*(step*i), ' '*(bar_size - (step*i)), '|', end='\r')
                        # mahoney filters for each imu
                        hand_filter = MahoneyFilter()
                        thumb_filter = MahoneyFilter()
                        point_filter = MahoneyFilter()
                        ring_filter = MahoneyFilter()

                        try:
                            lines = content[i].split(sep='\n')
                            os.mkdir("./data/data-{}".format(str(i+num_patients)))
                            f = open("./data/data-{}/raw.txt".format(str(i+num_patients)), 'w')

                            for line in lines:
                                # row = line.split(sep=' ')
                                row = line.split(sep='\t')
                                if not len(row) == 38:
                                    continue

                                # hand IMU
                                hand_filter.process(float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]), float(row[10]), 0.01)
                                row.extend(hand_filter.q)

                                # hand IMU
                                thumb_filter.process(float(row[11]), float(row[12]), float(row[13]), float(row[14]), float(row[15]), float(row[16]), float(row[17]), float(row[18]), float(row[19]), 0.01)
                                row.extend(thumb_filter.q)

                                # hand IMU
                                point_filter.process(float(row[20]), float(row[21]), float(row[22]), float(row[23]), float(row[24]), float(row[25]), float(row[26]), float(row[27]), float(row[28]), 0.01)
                                row.extend(point_filter.q)

                                # hand IMU
                                ring_filter.process(float(row[29]), float(row[30]), float(row[31]), float(row[32]), float(row[33]), float(row[34]), float(row[35]), float(row[36]), float(row[37]), 0.01)
                                row.extend(ring_filter.q)

                                for item in row:
                                    f.write("{} ".format(str(item)))
                                f.write('\n')

                            # f.write(content[i])
                            f.close()

                            # calculate the mahoney filter of each

                        except BlockingIOError:
                            print("\nerror: could not open new data file")
                            break

                    else:
                        print("\ndownload complete!")


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
            print("number of data records on disk: {}".format(len(patients)))
            # list all the files
            print("./data:")
            for i in patients:
                print(i)
        else:
            print("cannot find path './data'")

    else:
        print("unknown object to list...")


def test_module(tokens):
    """

    :param tokens:
    :return:
    """
    print("Testing Module")
    matrix = extract('./data/patient-4', 'HAx', 'TAx', 'PAx', 'RAx')
    print(matrix)
