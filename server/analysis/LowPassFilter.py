"""
[CLASS] LOW PASS FILTER

Date:       Tuesday June 12th, 2018
Author:     Alexander Adranly, Senbao Lu

This signal filter will take the raw data and run it all through
a special low-pass filter.
"""
from scipy.signal import *
import numpy as np
import os
from MatrixBuilder import extract


class LowPassFilter(object):

    COEFFICIENT = str(os.getcwd()) + "/resources/lowpass_coef.txt"

    def __init__(self, filename):
        """
        filtering:
        2* emg  12 * accelerometer, 12 * gyroscope, 16 * positional
        Do we need to filter QUAD??? really??

        [1 x 341] matrix
        :param filename: data name
        """
        self.__filename = filename
        self.__indicies = []
        self.__mat = list

    def process(self):
        # print(os.getcwd())
        rawfile = open("{}/raw.txt".format(self.__filename), "r")
        coefficients = open(self.COEFFICIENT, "r").read().split(sep='\n')
        coefficients = np.matrix(coefficients)
        output = open("{}/lowpass.txt".format(self.__filename), "w")

        self.__mat = extract(self.__filename, "E", "HA", "HG", "TA", "TG", "PA", "PG", "RA", "RG", "Q")
        self.__mat = np.matrix(self.__mat).transpose()

        # print(raw_mat.shape)
        # print("!!! BEFORE!!!")
        convolution = convolve(self.__mat.astype(np.float64), coefficients.astype(np.float64), mode='same').transpose()
        # print("!!! AFTER!!!")
        num_rows, num_cols = convolution.shape
        # print(convolution.shape)

        try:
            # for r in range(0, num_rows):
            #     for c in range(0, num_cols):
            #         output.write("{} ".format(convolution[r][c]))
            #     output.write('\n')

            for c in range(0, num_cols):
                for r in range(0, num_rows):
                    output.write("{} ".format(convolution[r][c]))
                output.write('\n')

        finally:
            output.close()
