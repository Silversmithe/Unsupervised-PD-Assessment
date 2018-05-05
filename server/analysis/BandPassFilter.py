"""
BAND PASS FILTER

This signal filter will take the raw data and run it all through
a special band-pass filter.
"""
import numpy as np
from scipy.signal import *
from analysis.MahonyFilter import q_to_roll


class BandPassFilter(object):

    COEFFICIENT = "../resources/bandpass_coef.txt"
    FEATURE_SIZE = 28

    def __init__(self, filename):
        """
        filtering:
        12 * accelerometer, 12 * gyroscope, 4*roll

        [1 x 341] matrix
        :param filename:
        """
        self.__filename = filename
        self.__indicies = [2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24, 25, 29, 30, 31, 32, 33, 34]
        self.__rawmat = [[] for i in range(0, self.FEATURE_SIZE)]

    def process(self):
        rawfile = open("{}/raw.txt".format(self.__filename), "r")
        coefficients = open(self.COEFFICIENT, "r").read().split(sep='\n')
        coefficients = np.matrix(coefficients)
        output = open("{}/lowpass.txt".format(self.__filename), "w")

        for line in rawfile:
            vals = line.split(sep=' ')

            for i in range(0, self.FEATURE_SIZE-4):
                self.__rawmat[i].append(float(vals[i]))

            # calculate roll and store it
            qh = [float(vals[38]), float(vals[39]), float(vals[40]), float(vals[41])]
            qt = [float(vals[42]), float(vals[43]), float(vals[44]), float(vals[45])]
            qp = [float(vals[46]), float(vals[47]), float(vals[48]), float(vals[49])]
            qr = [float(vals[50]), float(vals[51]), float(vals[52]), float(vals[53])]

            self.__rawmat[24].append(q_to_roll(qh))
            self.__rawmat[25].append(q_to_roll(qt))
            self.__rawmat[26].append(q_to_roll(qp))
            self.__rawmat[27].append(q_to_roll(qr))

        raw_mat = np.matrix(self.__rawmat).transpose()

        convolution = convolve(raw_mat, coefficients, mode='same')
        num_cols = len(convolution)
        num_rows = len(convolution[0])

        for r in range(0, num_rows):
            for c in range(0, num_cols):
                output.write("{} ".format(convolution[r][c]))
            output.write('\n')

        output.close()
