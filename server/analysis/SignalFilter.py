"""
SIGNAL FILTER

The signal filter is a general-purpose filter for handling the manipulation
of all incoming signals captured by the server. The signal filter is
responsible for producing new data, given the old data, that can be passed
onto filters in the future for scoring and whatnot.
"""


class SignalFilter(object):

    def __init__(self):
        pass

    def process(self):
        pass

    def low_pass(self):
        pass

    def high_pass(self):
        pass

    def fft(self):
        pass
