"""
PIPELINE MANAGER

Date:       Tuesday June 12th, 2018
Author:     Alexander Adranly

After the raw data has been produced by the server, the server starts a new
thread called the pipeline manager, which guides the raw data through
several filters and ultimately to the scoring stage, where the system
will produce the UPDRS results
"""
import time
import os
from analysis.LowPassFilter import LowPassFilter
from analysis.BandPassFilter import BandPassFilter
from analysis.HampelFilter import HampelFilter
from analysis.GravityFilter import GravityFilter
from Reporter import Reporter
from Score import Score
from threading import Thread, Lock, ThreadError


"""
[CLASS] PipelineManager

This derivation of the thread class is responsible for passing raw data from
a patient profile through all of the different filters in the pipeline.
"""


class PipelineManager(Thread):

    def __init__(self, patient_path):
        """
        :param patient_path: name of the folder containing all the information about the data
        example: ./data/data-1

        """
        Thread.__init__(self)
        self.__patient_path = patient_path

        self.__low_pass_filter = LowPassFilter(filename=self.__patient_path)
        self.__band_pass_filter = BandPassFilter(filename=self.__patient_path)
        self.__hampel_filter = HampelFilter(filename=self.__patient_path)
        self.__gravity_filter = GravityFilter(filename=self.__patient_path)
        self.__score = Score(filename=self.__patient_path)
        self.__reporter = Reporter(filepath=self.__patient_path)

    def run(self):
        """
        Given a data profile, pass that data's profile through all the
        stages of the UPDA pipeline
        :return:
        """
        ##########
        # Checks #
        ##########
        if not os.path.exists("{}".format(self.__patient_path)):
            print("error: data does not exist")
            return

        if not os.path.exists("{}/raw.txt".format(self.__patient_path)):
            print("error: data does not exist")
            return

        print("processing: {}".format(self.__patient_path))
        start = time.time()

        ###################
        # Low Pass Filter #
        ###################
        print("calling low pass filter...")
        self.__low_pass_filter.process()

        ####################
        # Band Pass Filter #
        ####################
        print("calling band pass filter...")
        self.__band_pass_filter.process()

        ####################
        # Hampel Filter    #
        ####################
        print("calling hampel filter...")
        self.__hampel_filter.process()

        ####################
        # Gravity Filter   #
        ####################
        print("calling gravity filter...")
        self.__gravity_filter.process()

        ##################
        # Scoring Filter #
        ##################
        print("calling score...")
        self.__score.process()

        ##################
        # Report Output  #
        ##################
        print("reporting...")
        self.__reporter.generate_report(self.__score.get_result())

        print("Processing Time: {}".format(time.time() - start))
