"""
PIPELINE MANAGER

After the raw data has been produced by the server, the server starts a new
thread called the pipeline manager, which guides the raw data through
several filters and ultimately to the scoring stage, where the system
will produce the UPDRS results
"""
import os
from analysis.SignalFilter import SignalFilter
from analysis.PositionalFilter import PositionalFilter
from threading import Thread, Lock, ThreadError


class PipelineManager(Thread):

    def __init__(self, patient):
        """
        :param patient: name of the folder containing all the information about the patient

        """
        Thread.__init__(self)
        self.__patient = patient
        self.__signal_filter = SignalFilter()
        self.__position_filter = PositionalFilter()
        pass

    def run(self):
        """
        Given a patient profile, pass that patient's profile through all the
        stages of the UPDA pipeline
        :return:
        """
        #################
        # Signal Filter #
        #################

        #####################
        # Positional Filter #
        #####################

        ##################
        # Scoring Filter #
        ##################

        ##################
        # Scoring Output #
        ##################

        pass
