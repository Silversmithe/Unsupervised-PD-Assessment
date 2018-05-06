"""
HAMPEL FILTER

description...
"""
import pandas as pd
import numpy as np


class HampelFilter(object):


    def __init__(self, filename):
        self.__filename = filename
                

    def process(self):
        """
        emg rectified 
        """
        rawfile = open("{}/raw.txt".format(self.__filename), "r")
        emg_rekt = []

        # storing all emg rect values in list
        for row in rawfile:
            emg_rekt.append(float(row.split(sep=' ')[1]))

        print("!!! BEFORE !!!")
        output = open("{}/hampel.txt".format(self.__filename), "w")
  
        filtered = self.hampel(vals_orig=emg_rekt)
        print("!!! AFTER !!!")
    
        for i in range(1, len(filtered)-1):
            if np.isnan(filtered[i]):
                filtered[i] = (filtered[i+1] + filtered[i-1])/2.0

        try:
            for val in filtered:
                output.write(str(val))
                output.write("\n")

        finally:
            output.close()

    def hampel(self, vals_orig, k=7, t0=3):
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
