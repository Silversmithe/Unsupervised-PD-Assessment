"""
POSITIONAL FILTER

The positional filter is used to determine specific moments that are
of interest for the scoring system. Given the raw signal data and the
filtered signal data, this filter will compute metrics to tell the
scoring system what to focus on
"""


class PositionalFilter(object):

    # potential position states
    FINGER_TAP = 0
    HAND_TAP = 1
    NONE = 2

    def __init__(self):
        pass

    def process(self):
        pass
