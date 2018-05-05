"""
Filters that process and use the
packet data to produce and anlaysis
"""
from analysis.MahonyFilter import MahoneyFilter


class RawDataFilter(object):

    BROADCAST_MSG = 1    # initializing communication
    NEW_DATASEG_MSG = 2  # new patient file should be made
    OLD_DATASEG_MSG = 3  # previous patient file was not finished, should be continued
    PAYLOAD_MSG = 4      # message containing data to store
    CLOSE_MSG = 5        # wearable telling server to stop
    PROCESS_MSG = 6      # wearable telling server to process the messages

    def __init__(self):
        self.hand_mhf = MahoneyFilter()
        self.thumb_mhf = MahoneyFilter()
        self.point_mhf = MahoneyFilter()
        self.ring_mhf = MahoneyFilter()

    def process(self, raw0, raw1):
        """
        extracts data from the two packets that represent one sampling instance.
        this information is then used to calculate the quaternion coordinate system,
        which is added and returned to the caller as one complete packet, a list of numbers

        payload packet format should be: operation id emg_raw0 emg_raw1 ....

        :param raw0: first packet for instance
        :param raw1: second packet for instance
        :return:

        MESSAGE_TYPE, PAYLOAD_ID, PAYLOAD
        """

        # get command and id
        _command, _pid = int(str(raw0[0]), 16), int(str(raw0[1]), 16)

        # process command
        if _command == self.PAYLOAD_MSG:
            result = list()
            # process the payload
            # 1. extract all information
            # 2. calculate quaternion coordinates and roll, pitch, and yaw --> add to payload
            # 3. pass back to thread for storage

            #########################################
            # CONVERT BYTES TO FLOATS AND HALFWORDS #
            #########################################

            # lets just do EMG for testing purposes
            for i in range(2, 6, 2):
                result.append((raw0[i] << 8) + raw0[i+1])  # store RAW and RECT emg

            # build first half of floats
            # two bytes leftover here
            for i in range(6, 90, 4):
                _real = (raw0[i] << 24) + (raw0[i+1] << 16) + (raw0[i+2] << 8) + raw0[i+3]
                if _real > 0x7fffffff:
                    _real -= 0x100000000
                result.append(float(_real)/100.0)

            # build second half of floats
            # two bytes left over at index 2 and 3
            # total 100 bytes
            for i in range(2, 62, 4):
                _real = (raw1[i] << 24) + (raw1[i+1] << 16) + (raw1[i+2] << 8) + raw1[i+3]
                if _real > 0x7fffffff:
                    _real -= 0x100000000
                result.append(float(_real)/100.0)

            ###############################
            # Mahoney Filter Calculations #
            ###############################
            # emg values -> 0, 1
            # hand values -> 2 - 10
            # thumb values -> 11 - 19
            # pointer values -> 20 - 28
            # ring values -> 29 - 37
            self.hand_mhf.process(ax=result[2], ay=result[3], az=result[4], gx=result[5], gy=result[6], gz=result[7],
                                  mx=result[8], my=result[9], mz=result[10], dt=0.01)

            self.thumb_mhf.process(ax=result[11], ay=result[12], az=result[13], gx=result[14], gy=result[15],
                                   gz=result[16], mx=result[17], my=result[18], mz=result[19], dt=0.01)

            self.point_mhf.process(ax=result[20], ay=result[21], az=result[22], gx=result[23], gy=result[34],
                                   gz=result[25], mx=result[26], my=result[27], mz=result[28], dt=0.01)

            self.ring_mhf.process(ax=result[29], ay=result[30], az=result[31], gx=result[32], gy=result[33],
                                  gz=result[34], mx=result[35], my=result[36], mz=result[37], dt=0.01)

            result.extend(self.hand_mhf.q)
            result.extend(self.thumb_mhf.q)
            result.extend(self.point_mhf.q)
            result.extend(self.ring_mhf.q)
            # return all info
            return self.PAYLOAD_MSG, _pid, result

        else:
            # some sort of weird error...
            print("error reading packet: {} - {}".format(_command, _pid))
            return self.CLOSE_MSG, None, None
