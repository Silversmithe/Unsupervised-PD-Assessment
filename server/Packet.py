"""
A container for the pipeline
of analysis
"""
from threading import Thread, ThreadError, Lock
from Sample import Sample

file_lock = Lock()


class SampleLoader(Thread):

    def __init__(self, file, raw_samples):
        Thread.__init__(self)
        self.__samples = raw_samples
        self.__file = file  # file to be written to

    def run(self):
        """
        Given a list of samples, open up or append a new file and start
        writing the information there
        :return:
        """
        with file_lock:

            with open(self.__file, 'a') as file:

                for sample in self.__samples:
                    # process each sample
                    # write the sample into a place
                    pass


class Packet(object):

    def __init__(self):
        self.sample_set = []
        self.result_set = []

    def add_sample(self, s):
        """
            @param: s: a Sample to store in the list
        """
        self.sample_set.append(s)

    def add_result(self, r):
        """
            @param: r: a  result to store in the list
        """
        self.result_set.append(r)
