"""
HAMPEL FILTER

description...
"""
import numpy as np
from pandas import *


class HampelFilter(object):

    def __init__(self):
        pass

    def process(self):
        pass

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
        vals = vals_orig.copy()
        # hampel filter
        L = 1.4826
        rolling_median = vals_orig.rolling(k).median()
        difference = np.abs(rolling_median-vals)
        median_abs_deviation = difference.rolling(k).median()
        threshold = t0 * L * median_abs_deviation
        outlier_idx = difference > threshold
        vals[outlier_idx] = np.nan
        return vals
