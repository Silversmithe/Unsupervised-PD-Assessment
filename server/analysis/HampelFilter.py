"""
HAMPEL FILTER

description...
"""
import pandas as pd
import numpy as np
from MatrixBuilder import extract
from math import *


class HampelFilter(object):

    AVE_BOUND = 1 

    def __init__(self, filename):
        self.__filename = filename

    def process(self):
        """

        emg rectified
        """
        # rawfile = open("{}/raw.txt".format(self.__filename), "r")
        # emg_rekt = []
        #
        # # storing all emg rect values in list
        # for row in rawfile:
        #     emg_rekt.append(float(row.split(sep=' ')[1]))

        emg_rekt = extract(self.__filename, 'EC')

        # print("!!! BEFORE !!!")
        output = open("{}/hampel.txt".format(self.__filename), "w")

        filtered = self.hampel(vals_orig=emg_rekt[0])
        # print("!!! AFTER !!!")

        for i in range(1, len(filtered)-1):
            count = 0
            total = 0
            top_cutoff = False

            # searching for nans
            if np.isnan(filtered[i]):
                while np.isnan(filtered[i+count]):
                    count += 1
                    if i + count >= len(filtered) - 1:
                        top_cutoff = True
                        break

                # lower bounds of nans
                for r in range(i-self.AVE_BOUND, i):
                    total += filtered[r]

                if not top_cutoff:
                    # upper bound of nans
                    for r in range(i+count, i+count+self.AVE_BOUND):
                        total += filtered[r]
               
                for n in range(i, i+count):
                    if not top_cutoff:
                        filtered[n] = total/(2.0 * self.AVE_BOUND)

                    else:
                        filtered[n] = total / self.AVE_BOUND

                if top_cutoff:
                    filtered[len(filtered)-1] = filtered[n] = total / self.AVE_BOUND
                    break

                # maximum = max(filtered[i-self.AVE_BOUND: i].extend(filtered[i+count: i+count+self.AVE_BOUND]))

                # for n in range(i, i+count):
                #     filtered[nan] = maximum

        try:
            for val in filtered:
                output.write(str(val))
                output.write("\n")

        finally:
            output.close()

    def hampel(self, vals_orig, k=17, t0=3):
        """
        credit goes to: https://ocefpaf.github.io/python4oceanographers/blog/2015/03/16/outlier_detection/
        https://stackoverflow.com/questions/46819260/filtering-outliers-how-to-make-median-based-hampel-function-faster

        :param vals_orig: pandas series of values from which to remove outliers
        :param k: size of the window (including the sample; 7 is equal to 3 on either side of value)
        :param t0:
        :return:
        """
        # make copy so original not edited
        vals = pd.Series(vals_orig.copy())

        # hampel filter
        L = 1.4826
        rolling_median = vals.rolling(k).median()
        difference = np.abs(rolling_median-vals)
        median_abs_deviation = difference.rolling(k).median()
        threshold = t0 * L * median_abs_deviation
        outlier_idx = difference > threshold

        vals[outlier_idx] = np.nan
        return vals
