"""
GRAVITY FILTER

A filter that can find the direction of gravity given the orientation of the hand. This
direction can be used to discern when a data is resting their hand or they are
using their hand
"""
from math import *
import numpy as np
from MatrixBuilder import extract


class GravityFilter(object):

    GRAVITY = np.matrix([[0.0], [0.0], [9.81]])

    def __init__(self, filename):
        self.__filename = filename
        pass

    def process(self):
        # go to raw file with quads
        outfile = open("{}/gravity.txt".format(self.__filename), "w")

        rawAccel = extract(self.__filename, 'HA', 'TA', 'PA', 'RA', 'Q')
        rawAccelMat = np.matrix(rawAccel).transpose()

        # print("!!! BEFORE !!!")
        # get all the accelerations
        # with open("{}/raw.txt".format(self.__filename), "r") as rawfile:
        #     for line in rawfile:
        #         vals = line.split(sep=' ')
        #         # HAND
        #         Hx = float(vals[2])
        #         Hy = float(vals[3])
        #         Hz = float(vals[4])
        #         # THUMB
        #         Tx = float(vals[11])
        #         Ty = float(vals[12])
        #         Tz = float(vals[13])
        #         # POINT
        #         Px = float(vals[20])
        #         Py = float(vals[21])
        #         Pz = float(vals[22])
        #         # RING
        #         Rx = float(vals[29])
        #         Ry = float(vals[30])
        #         Rz = float(vals[31])
        #
        #         qh = [float(vals[38]), float(vals[39]), float(vals[40]), float(vals[41])]
        #         qt = [float(vals[42]), float(vals[43]), float(vals[44]), float(vals[45])]
        #         qp = [float(vals[46]), float(vals[47]), float(vals[48]), float(vals[49])]
        #         qr = [float(vals[50]), float(vals[51]), float(vals[52]), float(vals[53])]
        try:
            for line in range(0, len(rawAccel[0])):

                # Ha = [0, 2]
                # Ta = [3, 5]
                # Pa = [6, 8]
                # Ra = [9, 11]
                # qh = [12, 15]
                # qt = [16, 19]
                # qp = [20, 23]
                # qr = [24, 27]

                qh = rawAccelMat[line, 12:16]
                qt = rawAccelMat[line, 16:20]
                qp = rawAccelMat[line, 20:24]
                qr = rawAccelMat[line, 24:28]

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
                # print(rr_h.shape)
                # FOR EACH LINE:
                # HAx HAy HAz
                outfile.write(str(rr_h.item((0, 0)) + rawAccelMat[line, 0]) + ' ')
                outfile.write(str(rr_h.item((1, 0)) + rawAccelMat[line, 1]) + ' ')
                outfile.write(str(rr_h.item((2, 0)) + rawAccelMat[line, 2]) + ' ')

                # THUMB
                outfile.write(str(rr_t.item((0, 0)) + rawAccelMat[line, 3]) + ' ')
                outfile.write(str(rr_t.item((1, 0)) + rawAccelMat[line, 4]) + ' ')
                outfile.write(str(rr_t.item((2, 0)) + rawAccelMat[line, 5]) + ' ')

                # POINT
                outfile.write(str(rr_p.item((0, 0)) + rawAccelMat[line, 6]) + ' ')
                outfile.write(str(rr_p.item((1, 0)) + rawAccelMat[line, 7]) + ' ')
                outfile.write(str(rr_p.item((2, 0)) + rawAccelMat[line, 8]) + ' ')

                # RING
                outfile.write(str(rr_r.item((0, 0)) + rawAccelMat[line, 9]) + ' ')
                outfile.write(str(rr_r.item((1, 0)) + rawAccelMat[line, 10]) + ' ')
                outfile.write(str(rr_r.item((2, 0)) + rawAccelMat[line, 11]))
                outfile.write('\n')

        finally:
            # print("!!! AFTER !!!")
            outfile.close()

    @staticmethod
    def generate_rot_mat(q):
        """

        :param q:
        :return:
        """
        # get rid of q[0]^2 from value
        # print("{} {} {}".format(q[1], q[2], q[3]))
        total = (pow(q[0, 1], 2.0) + pow(q[0, 2], 2.0) + pow(q[0, 3], 2.0))

        if total == 0:
            s = 0
        else:
            s = 1.0/total

        r = [
                [1 - 2 * s * (pow(q[0, 2], 2.0) + pow(q[0, 3], 2.0)), 2 * s * (q[0, 1] * q[0, 2] - q[0, 3] * q[0, 0]), 2 * s * (q[0, 1] * q[0, 3] + q[0, 2] * q[0, 0])],
                [2 * s * (q[0, 1] * q[0, 2] + q[0, 3] * q[0, 0]), 1 - 2 * s * (pow(q[0, 1], 2.0) + pow(q[0, 3], 2.0)), 2 * s * (q[0, 2] * q[0, 3] - q[0, 1] * q[0, 0])],
                [2 * s * (q[0, 1] * q[0, 3] - q[0, 2] * q[0, 0]), 2 * s * (q[0, 2] * q[0, 3] + q[0, 1] * q[0, 0]), 1 - 2 * s * (pow(q[0, 1], 2.0) + pow(q[0, 3], 2.0))]
        ]

        return np.matrix(r)
