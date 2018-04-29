"""
PIPELINE MANAGER

After the raw data has been produced by the server, the server starts a new
thread called the pipeline manager, which guides the raw data through
several filters and ultimately to the scoring stage, where the system
will produce the UPDRS results
"""
import os
from analysis.LowPassFilter import LowPassFilter
from analysis.BandPassFilter import BandPassFilter
from analysis.PositionalFilter import PositionalFilter
from threading import Thread, Lock, ThreadError


class PipelineManager(Thread):

    def __init__(self, patient_path):
        """
        :param patient_path: name of the folder containing all the information about the patient
        example: ./data/patient-1

        """
        Thread.__init__(self)
        self.__patient_path = patient_path
        self.__low_pass_filter = LowPassFilter(filename=self.__patient_path)
        self.__position_filter = PositionalFilter(filename=self.__patient_path)
        self.__band_pass_filter = BandPassFilter(filename=self.__patient_path)
        pass

    def run(self):
        """
        Given a patient profile, pass that patient's profile through all the
        stages of the UPDA pipeline
        :return:
        """
        ##########
        # Checks #
        ##########
        if not os.path.exists("{}".format(self.__patient_path)):
            print("error: patient does not exist")
            return

        if not os.path.exists("{}/raw.txt".format(self.__patient_path)):
            print("error: patient does not exist")
            return

        print("processing: {}".format(self.__patient_path))

        ###################
        # Low Pass Filter #
        ###################
        try:
            print("low pass filter")
            self.__low_pass_filter.process()

        except:
            print("warning: uncaught error")

        #####################
        # Positional Filter #
        #####################
        try:
            print("positional filter")
            self.__position_filter.process()

        except:
            print("warning: uncaught error")

        ####################
        # Band Pass Filter #
        ####################
        try:
            print("band pass filter")
            self.__band_pass_filter.process()

        except:
            print("warning: uncaught error")

        ##################
        # Scoring Filter #
        ##################

        ##################
        # Scoring Output #
        ##################

        pass
