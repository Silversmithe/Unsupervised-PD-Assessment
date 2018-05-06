"""
GRAVITY FILTER

A filter that can find the direction of gravity given the orientation of the hand. This
direction can be used to discern when a patient is resting their hand or they are
using their hand
"""
from math import *
import numpy as np


class GravityFilter(object):

    GRAVITY = np.matrix([[0.0], [0.0], [-9.81]])

    def __init__(self, filename):
        self.__filename = filename
        pass

    def process(self):
        # go to raw file with quads
        outfile = open("{}/gravity.txt".format(self.__filename), "w")

        raw_accels = [[] for i in range(0, 12)]
        adjusted_accel = [[] for i in range(0, 12)]

        # get all the accelerations
        with open("{}/raw.txt".format(self.__filename), "r") as rawfile:
            for line in rawfile:
                vals = line.split(sep=' ')
                # HAND
                raw_accels[0].append(float(vals[3]))
                raw_accels[1].append(float(vals[4]))
                raw_accels[2].append(float(vals[5]))
                # THUMB
                raw_accels[3].append(float(vals[12]))
                raw_accels[4].append(float(vals[13]))
                raw_accels[5].append(float(vals[14]))
                # POINT
                raw_accels[6].append(float(vals[21]))
                raw_accels[7].append(float(vals[22]))
                raw_accels[8].append(float(vals[23]))
                # RING
                raw_accels[9].append(float(vals[30]))
                raw_accels[10].append(float(vals[31]))
                raw_accels[11].append(float(vals[32]))

        with open("{}/raw.txt".format(self.__filename), "r") as rawfile:
            for line in rawfile:
                # extract quads
                elts = line.split(sep=' ')
                qh = [float(elts[38]), float(elts[39]), float(elts[40]), float(elts[41])]
                qt = [float(elts[42]), float(elts[43]), float(elts[44]), float(elts[45])]
                qp = [float(elts[46]), float(elts[47]), float(elts[48]), float(elts[49])]
                qr = [float(elts[50]), float(elts[51]), float(elts[52]), float(elts[53])]

                # generate rotation matrix
                rot_h = self.generate_rot_mat(qh)
                rot_t = self.generate_rot_mat(qt)
                rot_p = self.generate_rot_mat(qp)
                rot_r = self.generate_rot_mat(qr)

                # multiply gravity by rotation matrix to get gravity in new reference frame
                rr_h = np.matmul(rot_h, self.GRAVITY)
                rr_t = np.matmul(rot_t, self.GRAVITY)
                rr_p = np.matmul(rot_p, self.GRAVITY)
                rr_r = np.matmul(rot_r, self.GRAVITY)

                # store scores
                # HAND
                adjusted_accel[0].append(rr_h[0])
                adjusted_accel[1].append(rr_h[1])
                adjusted_accel[2].append(rr_h[2])
                # THUMB
                adjusted_accel[3].append(rr_t[0])
                adjusted_accel[4].append(rr_t[1])
                adjusted_accel[5].append(rr_t[2])
                # POINT
                adjusted_accel[6].append(rr_p[0])
                adjusted_accel[7].append(rr_p[1])
                adjusted_accel[8].append(rr_p[2])
                # RING
                adjusted_accel[9].append(rr_r[0])
                adjusted_accel[10].append(rr_r[1])
                adjusted_accel[11].append(rr_r[2])

        # calculate adjusted accel
        if len(adjusted_accel) != len(raw_accels):
            print("adjusted does not equal raw!")

        for i in range(0, len(adjusted_accel)):
            adjusted_accel[0][i] += raw_accels[0][i]
            adjusted_accel[1][i] += raw_accels[1][i]
            adjusted_accel[2][i] += raw_accels[2][i]
            adjusted_accel[3][i] += raw_accels[3][i]
            adjusted_accel[4][i] += raw_accels[4][i]
            adjusted_accel[5][i] += raw_accels[5][i]
            adjusted_accel[6][i] += raw_accels[6][i]
            adjusted_accel[7][i] += raw_accels[7][i]
            adjusted_accel[8][i] += raw_accels[8][i]
            adjusted_accel[9][i] += raw_accels[9][i]
            adjusted_accel[10][i] += raw_accels[10][i]
            adjusted_accel[11][i] += raw_accels[11][i]

        # PRINT HAND
        for r in range(0, len(adjusted_accel)):
            for c in range(0, len(adjusted_accel[0])):
                print("{}".format(adjusted_accel[r][c]), end=' ')
            print()

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
