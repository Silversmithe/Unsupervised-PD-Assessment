"""
LOW PASS FILTER

This signal filter will take the raw data and run it all through
a special low-pass filter.
"""
import scipy


class LowPassFilter(object):

    def __init__(self, filename):
        """

        :param filename:
        """
        self.__filename = filename

    def process(self):
        pass
