"""
Data Types for the system
"""


class Sample(object):
    """
    Object for storing an instance of data
    """

    def __init__(self):
        self.emg = [0, 0]  # empty EMG list

        self.hand = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.hand_pos = [0, 0, 0]

        self.thumb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.thumb_pos = [0, 0, 0]

        self.point = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.point_pos = [0, 0, 0]

        self.ring = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ring_pos = [0, 0, 0]

        self.delta_t = 0.0
