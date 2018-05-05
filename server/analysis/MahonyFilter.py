"""
MAHONEY FILTER

A type of kallman filter that fuses acceleration, radians per second,
microtesslas, and a time differential to estimate the position of
the imu in space. This is then recorded into the

credits for the math:
https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
"""
from math import *


class MahoneyFilter(object):

    Kp = 2.0 * 5.0
    Ki = 0.0
    GyroMeasError = pi * (40.0 / 180.0)
    GyroMeasDrift = pi * (0.0 / 180.0)
    Beta = sqrt(3.0 / 4.0) * GyroMeasError
    Zeta = sqrt(3.0 / 4.0) * GyroMeasDrift

    def __init__(self):
        self.q = [1.0, 0.0, 0.0, 0.0]  # w x y z
        self.eint = [0.0, 0.0, 0.0]

    def process(self, ax, ay, az, gx, gy, gz, mx, my, mz, dt):
        """
        instance:

        emg_raw emg_rect Hand_Axyz_Gxyz_Mxyz Thumb_Axyz_Gxyz_Mxyz Pointer_Axyz_Gxyz_Mxyz Ring_Axyz_Gxyz_Mxyz

        one instance consists of:
        Hand_Axyz_Gxyz_Mxyz

        :param ax: acceleration in the x-direction
        :param ay: acceleration in the y-direction
        :param az: acceleration in the z-direction
        :param gx: radians/second in the x-direction
        :param gy: radians/second in the y-direction
        :param gz: radians/second in the z-direction
        :param mx: micro tesslas in the x direction
        :param my: micro tesslas in the y direction
        :param mz: micro tesslas in the z direction
        :param dt: time in seconds since the last update
        :return: None
        Information is stored in 'self._q' for future work
        """
        q1 = self.q[0]
        q2 = self.q[1]
        q3 = self.q[2]
        q4 = self.q[3]

        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q1q4 = q1 * q4
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q2q4 = q2 * q4
        q3q3 = q3 * q3
        q3q4 = q3 * q4
        q4q4 = q4 * q4

        # normalize accel
        norm = sqrt(ax * ax + ay * ay + az * az)
        if norm == 0.0:
            return
        norm = 1.0 / norm
        ax *= norm
        ay *= norm
        az *= norm

        # normalize mag
        norm = sqrt(mx * mx + my * my + mz * mz)
        if norm == 0.0:
            return
        norm = 1.0 / norm
        mx *= norm
        my *= norm
        mz *= norm

        # reference direction of magnetic field
        hx = 2.0 * mx * (0.5 - q3q3 - q4q4) + 2.0 * my * (q2q3 - q1q4) + 2.0 * mz * (q2q4 + q1q3)
        hy = 2.0 * mx * (q2q3 + q1q4) + 2.0 * my * (0.5 - q2q2 - q4q4) + 2.0 * mz * (q3q4 - q1q2)
        bx = sqrt((hx * hx) + (hy * hy))
        bz = 2.0 * mx * (q2q4 - q1q3) + 2.0 * my * (q3q4 + q1q2) + 2.0 * mz * (0.5 - q2q2 - q3q3)

        # estimated direction of gravity and magnetic field
        vx = 2.0 * (q2q4 - q1q3)
        vy = 2.0 * (q1q2 + q3q4)
        vz = q1q1 - q2q2 - q3q3 + q4q4
        wx = 2.0 * bx * (0.5 - q3q3 - q4q4) + 2.0 * bz * (q2q4 - q1q3)
        wy = 2.0 * bx * (q2q3 - q1q4) + 2.0 * bz * (q1q2 + q3q4)
        wz = 2.0 * bx * (q1q3 + q2q4) + 2.0 * bz * (0.5 - q2q2 - q3q3)

        # error is cross product between estimated direction and measured direction of gravity
        ex = (ay * vz - az * vy) + (my * wz - mz * wy)
        ey = (az * vx - ax * vz) + (mz * wx - mx * wz)
        ez = (ax * vy - ay * vx) + (mx * wy - my * wx)

        if self.Ki > 0.0:
            self.eint[0] += ex
            self.eint[1] += ey
            self.eint[2] += ez

        else:
            # prevent integral windup
            self.eint[0] = 0.0
            self.eint[1] = 0.0
            self.eint[2] = 0.0

        # apply feedback terms
        gx = gx + self.Kp * ex + self.Ki * self.eint[0]
        gy = gy + self.Kp * ey + self.Ki * self.eint[1]
        gz = gz + self.Kp * ez + self.Ki * self.eint[2]

        # integrate rate of change of quaternion
        pa = q2
        pb = q3
        pc = q4
        q1 = q1 + (-q2 * gx - q3 * gy - q4 * gz) * (0.5 * dt)
        q2 = pa + (q1 * gx + pb * gz - pc * gy) * (0.5 * dt)
        q3 = pb + (q1 * gy - pa * gz + pc * gx) * (0.5 * dt)
        q4 = pc + (q1 * gz + pa * gy - pb * gx) * (0.5 * dt)

        # normalize quaternion
        norm = sqrt(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4)
        norm = 1.0 / norm
        self.q[0] = q1 * norm
        self.q[1] = q2 * norm
        self.q[2] = q3 * norm
        self.q[3] = q4 * norm

    def to_roll(self, deg=False):
        """
        Converts the current Q into roll

        :param deg: (bool) should it be converted to degrees
        :return: current estimated roll position in either degrees or radians
        """
        t0 = 2.0 * (self.q[0] * self.q[1] + self.q[2] * self.q[3])
        t1 = self.q[0] * self.q[0] - self.q[1] * self.q[1] - self.q[2] * self.q[2] + self.q[3] * self.q[3]

        if deg:
            return degrees(atan2(t0, t1))

        else:
            return atan2(t0, t1)

    def to_pitch(self, deg=False):
        """
        Converts the current Q into pitch

        :param deg: (bool) should it be converted to degrees
        :return: current estimated pitch position in either degrees or radians
        """
        t0 = 2.0 * (self.q[1] * self.q[3] - self.q[0] * self.q[2])

        if deg:
            return degrees(-1.0 * asin(t0)) - 8.5  # according to sparkfun code. declination angle

        else:
            return asin(-1.0 * t0)

    def to_yaw(self, deg=False):
        """
        Converts the current Q into yaw

        :param deg: (bool) should it be converted to degrees
        :return: current estimated yaw position in either degrees or radians
        """
        t0 = 2.0 * (self.q[1] * self.q[2] + self.q[0] * self.q[3])
        t1 = self.q[0] * self.q[0] + self.q[1] * self.q[1] - self.q[2] * self.q[2] - self.q[3] * self.q[3]

        if deg:
            return degrees(atan2(t0, t1))

        else:
            return atan2(t0, t1)


# calculations outside of the class
def q_to_roll(q, deg=False):
    """
    Converts the current Q into roll

    :param: q: (list) contains quaternion coordinates
    :param deg: (bool) should it be converted to degrees
    :return: current estimated roll position in either degrees or radians
    """
    t0 = 2.0 * (q[0] * q[1] + q[2] * q[3])
    t1 = q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]

    if deg:
        return degrees(atan2(t0, t1))

    else:
        return atan2(t0, t1)


def q_to_pitch(q, deg=False):
    """
    Converts the current Q into pitch

    :param: q: (list) contains quaternion coordinates
    :param deg: (bool) should it be converted to degrees
    :return: current estimated pitch position in either degrees or radians
    """
    t0 = 2.0 * (q[1] * q[3] - q[0] * q[2])

    if deg:
        return degrees(-1.0 * asin(t0)) - 8.5  # according to sparkfun code. declination angle

    else:
        return asin(-1.0 * t0)


def q_to_yaw(q, deg=False):
    """
    Converts the current Q into yaw

    :param: q: (list) contains quaternion coordinates
    :param deg: (bool) should it be converted to degrees
    :return: current estimated yaw position in either degrees or radians
    """
    t0 = 2.0 * (q[1] * q[2] + q[0] * q[3])
    t1 = q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3]

    if deg:
        return degrees(atan2(t0, t1))

    else:
        return atan2(t0, t1)