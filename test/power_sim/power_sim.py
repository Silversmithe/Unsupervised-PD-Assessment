#!/usr/bin/python3
"""
FILE:           power_sim.py

AUTHOR:         Alexander S. Adranly

DESCRIPTION:    Read in device specifications of the wearable device from
                'device.yaml' and use this to produce statistics on how
                the wearable device will run
"""
import sys
import yaml

# list of times to check
TIMES = []

if __name__ == '__main__':
    ##################
    # DEVICE BUILDER #
    ##################
    DEVICES = None

    with open('/Users/Silversmith/PycharmProjects/Natural-PD-Quantification/test/power_sim/device.yaml', 'r') as file:
        try:
            # load object data into the DEVICES file
            DEVICES = yaml.load(file)
        except yaml.YAMLError as exc:
            print(exc)

    # check if devices file is loaded correctly
    # if loaded continue
    print('loading wearable components...')
    print(yaml.dump(DEVICES), '\n')

    ###############
    # CALCULATION #
    ###############
    """
    V = IR
    I = R/V
    
    P = IV
    """
    # LIFETIME (PWR * sec) = mA * Voltage * Time
    mA_SUM, V_SUM = 0, 0

    # get the sum of all voltages
    DEVICES[""]



