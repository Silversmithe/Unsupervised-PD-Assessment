"""
GRAVITY FILTER

A filter that can find the direction of gravity given the orientation of the hand. This
direction can be used to discern when a data is resting their hand or they are
using their hand

RM_hand=[2.*(hqi.*hqk+hqj.*hqr).*g,2.*s.*(hqj.*hqk-hqi.*hqr).*g,(hqr.^2-hqi.^2-hqj.^2+hqk.^2).*g];

b = i
a = r
c = j
d = k

2(bd+ac) * g
2(cd - ab) * g
(a^2 - b^2 - c^2 + d^2) * g

"""
from math import *
import numpy as np
from MatrixBuilder import extract


class GravityFilter(object):

    GRAVITY = -9.81

    def __init__(self, filename):
        self.__filename = filename
        pass

    def process(self):
        # go to raw file with quads
        outfile = open("{}/gravity.txt".format(self.__filename), "w")

        def calc_accel(q, a):
            """
            :param q: [r, i, j, k] : quaternions
            :param a: [x, y, z] : raw acceleration
            :return: (list) "true" acceleration
            """
            x_comp = 2.0 * (q[0, 1] * q[0, 3] + q[0, 0] * q[0, 2]) * self.GRAVITY
            y_comp = 2.0 * (q[0, 2] * q[0, 3] - q[0, 0] * q[0, 1]) * self.GRAVITY
            z_comp = (pow(q[0, 0], 2.0) - pow(q[0, 1], 2.0) - pow(q[0, 2], 2.0) + pow(q[0, 3], 2.0)) * self.GRAVITY
            return [x_comp + a[0, 0], y_comp + a[0, 1], z_comp + a[0, 2]]

        rawAccel = extract(self.__filename, 'HA', 'TA', 'PA', 'RA', 'Q')
        rawAccelMat = np.matrix(rawAccel).transpose()

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
                true_h = calc_accel(qh, rawAccelMat[line, 0:3])
                true_t = calc_accel(qt, rawAccelMat[line, 3:6])
                true_p = calc_accel(qp, rawAccelMat[line, 6:9])
                true_r = calc_accel(qr, rawAccelMat[line, 9:12])

                # store scores
                # HAND
                # print(rr_h.shape)
                # FOR EACH LINE:
                # HAx HAy HAz
                outfile.write("{} {} {} ".format(true_h[0], true_h[1], true_h[2]))
                # THUMB
                outfile.write("{} {} {} ".format(true_t[0], true_t[1], true_t[2]))
                # POINT
                outfile.write("{} {} {} ".format(true_p[0], true_p[1], true_p[2]))
                # RING
                outfile.write("{} {} {}\n".format(true_r[0], true_r[1], true_r[2]))

        finally:
            # print("!!! AFTER !!!")
            outfile.close()
