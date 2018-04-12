#! /usr/bin/python

"""
server.py

by Alexander Adranly, 2018



"""

# !/bin/bash
import time
from digi.xbee.devices import XBeeDevice

# GLOBALS
VERSION = 1
RUNNING = True

"""
XBEE SERVER 
"""


def server():
    """
    Xbee Server
    :return:
    """
    print("starting server...")


"""
Simple UPDA CONSOLE
"""


def stats(tokens):
    """

    :param tokens:
    :return:
    """
    pass


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


def list_cmds(tokens):
    """

    :param tokens:
    :return:
    """
    print("help\texplains what all the commands do\n",
          "quit\tterminates the program\n",
          "start server\tinitialize a server to read xbee\n",
          "stats\tinformation on overall server stats")


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
    "stats": stats
}


def main():
    """
    create a main console that is responsible for the gathering and control of the
    server
    :return:
    """
    print('_'*50)
    print("Unsupervised Parkinson's Disease Assessment Console")
    print("Version {}".format(VERSION))
    print('_' * 50, '\n')

    while RUNNING:
        try:
            message = input(">>> ")

            tokens = message.lower().split(sep=" ")

            if tokens[0] in command_list:
                # in the command list
                command_list[tokens[0]](tokens)
            else:
                # not in the command list
                print("cannot process'{}'".format(message))

            print()

        except KeyboardInterrupt:
            break

    print("goodbye...")


if __name__ == '__main__':
    main()
