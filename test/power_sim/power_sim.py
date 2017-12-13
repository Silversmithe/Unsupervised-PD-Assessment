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
SECONDS = []

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

    # calculating theoretical lifetime of battery
    battery_rating = DEVICES["BATTERY"]["RATING"]

    device_current_draw = 0
    device_current_draw += DEVICES["MCU"]["TEENSY"]["I_OP"]
    device_current_draw += DEVICES["RADIO"]["XBEE"]["I_OP"]

    device_current_draw += DEVICES["SENSOR"]["MYO_EMG"]["I_OP"]
    device_current_draw += (DEVICES["SENSOR"]["MPU_9250"]["I_OP"] * 3)
    device_current_draw += DEVICES["SENSOR"]["MPU_6050"]["I_OP"]

    battery_life = battery_rating / device_current_draw
    print("Theoretical Worst-Case Battery Life: {} hours".format(battery_life))
