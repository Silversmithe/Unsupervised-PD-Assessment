"""
Filters that process and use the
packet data to produce and anlaysis
"""


class Filter(object):

    def __init__(self):
        pass

    def process(self, packet):
        """
        filter processes a packet to
        produce a result
        """
        pass


class RawDataFilter(object):

    BROADCAST_MSG = 1    # initializing communication
    NEW_DATASEG_MSG = 2  # new patient file should be made
    OLD_DATASEG_MSG = 3  # previous patient file was not finished, should be continued
    PAYLOAD_MSG = 4      # message containing data to store
    CLOSE_MSG = 5        # wearable telling server to stop

    def __init__(self):
        self.__quaternion = (0.0, 0.0, 0.0, 0.0)  # quaternion coordinates to track

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
        _command, _pid = int(raw0[0], 16), int(raw0[1], 16)

        # process command
        if _command == self.PAYLOAD_MSG:
            result = list()
            # process the payload
            # 1. extract all information
            # 2. calculate quaternion coordinates and roll, pitch, and yaw --> add to payload
            # 3. pass back to thread for storage

            # lets just do EMG for testing purposes
            for i in range(2, 6, 2):
                result.append((raw0[i] << 8) + raw0[i+1])  # store RAW and RECT emg

            # calculations could be here

            # return all info
            return self.PAYLOAD_MSG, _pid, result

        else:
            # some sort of weird error...
            print("error reading packet: {} - {}".format(_command, _pid))
            return self.CLOSE_MSG, None, None

    def mahoney_filter(self, instance):
        """

        :param instance:
        :return:
        """
        pass
