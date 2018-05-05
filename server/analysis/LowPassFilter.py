"""
LOW PASS FILTER

This signal filter will take the raw data and run it all through
a special low-pass filter.
"""
from scipy.signal import *
import numpy as np


class LowPassFilter(object):

    COEFFICIENT = "../resources/lowpass_coef.txt"
    NOT_INDICIES = [8, 9, 10, 17, 18, 19, 26, 27, 28, 35, 36, 37]
    FEATURE_SIZE = 40

    def __init__(self, filename):
        """
        filtering:
        2* emg  12 * accelerometer, 12 * gyroscope, 16 * positional

        [1 x 341] matrix
        :param filename: patient name
        """
        self.__filename = filename
        self.__indicies = []
        self.__rawmat = [[] for i in range(0, self.FEATURE_SIZE)]

        for i in range(0, 54):
            if i not in self.NOT_INDICIES:
                self.__indicies.append(i)

    def process(self):
        rawfile = open("{}/raw.txt".format(self.__filename), "r")
        coefficients = open(self.COEFFICIENT, "r").read().split(sep='\n')
        coefficients = np.matrix(coefficients)
        output = open("{}/lowpass.txt".format(self.__filename), "w")

        for line in rawfile:
            vals = line.split(sep=' ')

            for i in range(0, self.FEATURE_SIZE):
                self.__rawmat[i].append(float(vals[i]))

        raw_mat = np.matrix(self.__rawmat).transpose()

        convolution = convolve(raw_mat, coefficients, mode='same')
        num_cols = len(convolution)
        num_rows = len(convolution[0])

        for r in range(0, num_rows):
            for c in range(0, num_cols):
                output.write("{} ".format(convolution[r][c]))
            output.write('\n')

        output.close()
