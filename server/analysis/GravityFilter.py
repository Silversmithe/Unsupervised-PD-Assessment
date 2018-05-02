"""
GRAVITY FILTER

A filter that can find the direction of gravity given the orientation of the hand. This
direction can be used to discern when a patient is resting their hand or they are
using their hand
"""
from math import *
import numpy as np


class GravityFilter(object):

    GRAVITY = np.matrix([0.0, 0.0, 1.0])

    def __init__(self, filename):
        self.__filename = filename
        pass

    def process(self):
        # go to raw file with quads
        with open("{}/raw.txt".format(self.__filename), "r") as rawfile:
            for line in rawfile:
                # extract quads
                elts = line.split(sep=' ')
                q = [elts[38], elts[39], elts[40], elts[41]]
                # generate rotation matrix
                rot = self.generate_rot_mat(q)
                q = np.matrix(q)
                # multiply gravity by rotation matrix to get gravity in new reference frame
                rotated_ref = rot * q
                # display or store rotated reference
                print(rotated_ref)

    @staticmethod
    def generate_rot_mat(q):
        """

        :param q:
        :return:
        """
        s = pow(sqrt(pow(q[0], 2.0) + pow(q[1], 2.0) + pow(q[2], 2.0) + pow(q[3], 2.0)), -2.0)

        r = [
                [1 - 2 * s * (pow(q[2], 2.0) + pow(q[3], 2.0)), 2 * s * (q[1] * q[2] - q[3] * q[0]), 2 * s * (q[1] * q[3] + q[2] * q[0])],
                [2 * s * (q[1] * q[2] + q[3] * q[0]), 1 - 2 * s * (pow(q[1], 2.0) + pow(q[3], 2.0)), 2 * s * (q[2] * q[3] - q[1] * q[0])],
                [2 * s * (q[1] * q[3] - q[2] * q[0]), 2 * s * (q[2] * q[3] + q[1] * q[0]), 1 - 2 * s * (pow(q[1], 2.0) + pow(q[3], 2.0))]
        ]

        return np.matrix(r)
