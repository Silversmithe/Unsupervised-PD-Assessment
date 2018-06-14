"""
[CLASS] BAND PASS FILTER

Date:       Tuesday June 12th, 2018
Author:     Alexander Adranly, Senbao Lu

This signal filter will take the raw data and run it all through
a special band-pass filter.
"""
import numpy as np
from scipy.signal import *
from MatrixBuilder import extract
import os


class BandPassFilter(object):

    COEFFICIENT = str(os.getcwd()) + "/resources/bandpass_coef.txt"
    FEATURE_SIZE = 28

    def __init__(self, filename):
        """
        filtering:
        12 * accelerometer, 12 * gyroscope, 4*roll

        [1 x 341] matrix
        :param filename:
        """
        self.__filename = filename
        self.__mat = list

    def process(self):
        # rawfile = open("{}/raw.txt".format(self.__filename), "r")
        coefficients = open(self.COEFFICIENT, "r").read().split(sep='\n')
        coefficients = np.matrix(coefficients)
        output = open("{}/bandpass.txt".format(self.__filename), "w+")

        self.__mat = extract(self.__filename, "HA", "HG", "TA", "TG", "PA", "PG", "RA", "RG", "OHr", "OTr", "OPr", "ORr")
        self.__mat = np.transpose(self.__mat)

        # print("!!! BEFORE !!!")
        convolution = convolve(self.__mat.astype(np.float64), coefficients.astype(np.float64), mode='same').transpose()
        num_rows, num_cols = convolution.shape
        # print("!!! AFTER !!!")

        try:
            for c in range(0, num_cols):
                for r in range(0, num_rows):
                    output.write("{} ".format(convolution[r][c]))
                output.write('\n')

        finally:
            output.close()
