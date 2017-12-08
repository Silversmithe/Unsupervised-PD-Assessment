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
    """
    V = IR
    I = R/V
    
    P = IV
    """
    mA_SUM, V_SUM = 0, 0

    # VOLTAGE
    V_SUM = DEVICES["MCU"]["TI_SENSORTAG_CC2650"]["VDD_MAX"]
    V_SUM += DEVICES["SENSOR"]["KIONIX_KXTJ9"]["VDD_MAX"]
    V_SUM += DEVICES["SENSOR"]["IMU_3000"]["VDD_MAX"]
    V_SUM += DEVICES["SENSOR"]["MPU_9250"]["VDD_MAX"]
    V_SUM += DEVICES["SENSOR"]["MYO_EMG"]["VDD_MAX"]
    print("Total Voltage: {}".format(V_SUM))

    # CURRENT
    mA_SUM = DEVICES["MCU"]["TI_SENSORTAG_CC2650"]["I_OP"]
    mA_SUM += DEVICES["SENSOR"]["KIONIX_KXTJ9"]["I_OP"]
    mA_SUM += DEVICES["SENSOR"]["IMU_3000"]["I_OP"]
    mA_SUM += DEVICES["SENSOR"]["MPU_9250"]["I_OP"]
    mA_SUM += DEVICES["SENSOR"]["MYO_EMG"]["I_OP"]
    print("Total Current Draw: {}".format(mA_SUM))

    ############
    # LIFETIME #
    ############
    # LIFETIME (PWR * sec) = mA * Voltage * Time
    LIFETIME = mA_SUM * V_SUM * 10000

    print(LIFETIME)
