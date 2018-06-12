"""
[CLASS] Score

Date:       Tuesday June 12th, 2018
Author:     Senbao Lu and Yousef Zoumot


The Score object is responsible for using all of the
data generated from the previous filters and producing
an estimate of the patient's UPDRS score
"""
import numpy as np
from analysis.MahonyFilter import *
from MatrixBuilder import extract
import os


class Score(object):

    SAMPLING_PERIOD_1 = 33
    SAMPLING_PERIOD_2 = 50
    SAMPLING_PERIOD_3 = 100
    SAMPLING_PERIOD_4 = 300

    def __init__(self, filename):
        self.__filename = filename
        self.variable = None
        self.__num_instances = self.get_num_instances()

        self.__weights_ft_0hz = self.get_weights("W_ft_1_3hz.txt")
        self.__weights_ft_1hz = self.get_weights("W_ft_1hz.txt")
        self.__weights_ft_2hz = self.get_weights("W_ft_2hz.txt")
        self.__weights_ft_3hz = self.get_weights("W_ft_3hz.txt")

        self.__weights_ftin_0hz = self.get_weights("W_ftin_1_3hz.txt")
        self.__weights_ftin_1hz = self.get_weights("W_ftin_1hz.txt")
        self.__weights_ftin_2hz = self.get_weights("W_ftin_2hz.txt")
        self.__weights_ftin_3hz = self.get_weights("W_ftin_3hz.txt")

        self.__weights_hg_0hz = self.get_weights("W_hg_1_3hz.txt")
        self.__weights_hg_1hz = self.get_weights("W_hg_1hz.txt")
        self.__weights_hg_2hz = self.get_weights("W_hg_2hz.txt")
        self.__weights_hg_3hz = self.get_weights("W_hg_3hz.txt")

        self.__weights_hgin_0hz = self.get_weights("W_hgin_1_3hz.txt")
        self.__weights_hgin_1hz = self.get_weights("W_hgin_1hz.txt")
        self.__weights_hgin_2hz = self.get_weights("W_hgin_2hz.txt")
        self.__weights_hgin_3hz = self.get_weights("W_hgin_3hz.txt")

        self.result = {
            'name': str(filename).split(sep='/')[-1],
            'ftap':  [0.0, 0.0],
            'htap':  [0.0, 0.0],
            'ptrem': [0.0, 0.0],
            'ktrem': [0.0, 0.0],
            'rtrem': [0.0, 0.0],
            'crest': [0.0, 0.0]
        }

    def get_result(self):
        return self.result

    def process(self):
        """
        """
        weights1 = self.__weights_ft_0hz
        weights2 = self.__weights_ft_1hz
        weights3 = self.__weights_ft_2hz
        weights4 = self.__weights_ft_3hz

        inputs1 = self.get_input_1_3hz_test("yousef_5.txt")
        inputs2 = self.get_input_1hz_test("yousef_5.txt")
        inputs3 = self.get_input_2hz_test("yousef_5.txt")
        inputs4 = self.get_input_3hz_test("yousef_5.txt")

        dataset4 = self.get_predictions(inputs1, weights1)
        dataset3 = self.get_predictions(inputs2, weights2)
        dataset2 = self.get_predictions(inputs3, weights3)
        dataset1 = self.get_predictions(inputs4, weights4)

        weights5 = self.__weights_ftin_0hz
        weights6 = self.__weights_ftin_1hz
        weights7 = self.__weights_ftin_2hz
        weights8 = self.__weights_ftin_3hz

        inputs5 = self.get_input_1_3hz_test("yousef_6.txt")
        inputs6 = self.get_input_1hz_test("yousef_6.txt")
        inputs7 = self.get_input_2hz_test("yousef_6.txt")
        inputs8 = self.get_input_3hz_test("yousef_6.txt")

        dataset8 = self.get_predictions(inputs5, weights5)
        dataset7 = self.get_predictions(inputs6, weights6)
        dataset6 = self.get_predictions(inputs7, weights7)
        dataset5 = self.get_predictions(inputs8, weights8)

        weights9 = self.__weights_hg_0hz
        weights10 = self.__weights_hg_1hz
        weights11 = self.__weights_hg_2hz
        weights12 = self.__weights_hg_3hz

        inputs9 = self.get_input_1_3hz_test("yousef_7.txt")
        inputs10 = self.get_input_1hz_test("yousef_7.txt")
        inputs11 = self.get_input_2hz_test("yousef_7.txt")
        inputs12 = self.get_input_3hz_test("yousef_7.txt")

        dataset12 = self.get_predictions(inputs9, weights9)
        dataset11 = self.get_predictions(inputs10, weights10)
        dataset10 = self.get_predictions(inputs11, weights11)
        dataset9 = self.get_predictions(inputs12, weights12)

        weights13 = self.__weights_hgin_0hz
        weights14 = self.__weights_hgin_1hz
        weights15 = self.__weights_hgin_2hz
        weights16 = self.__weights_hgin_3hz

        inputs13 = self.get_input_1_3hz_test("yousef_8.txt")
        inputs14 = self.get_input_1hz_test("yousef_8.txt")
        inputs15 = self.get_input_2hz_test("yousef_8.txt")
        inputs16 = self.get_input_3hz_test("yousef_8.txt")

        dataset16 = self.get_predictions(inputs13, weights13)
        dataset15 = self.get_predictions(inputs14, weights14)
        dataset14 = self.get_predictions(inputs15, weights15)
        dataset13 = self.get_predictions(inputs16, weights16)

        # print only htaps and ftaps for patients name
        patient_name = self.__filename.split(sep="/")[-1]
        if patient_name != 'data-3':
            tapin_counter = self.count_tap_interuptions(dataset5, dataset6, dataset7, dataset8, self.__num_instances)
            taps_counter = self.count_taps(dataset1, dataset2, dataset3, dataset4, self.__num_instances)

            graspin_counter = self.count_grasp_interuptions(dataset13, dataset14, dataset15, dataset16, self.__num_instances)
            grasp_counter = self.count_grasps(dataset9, dataset10, dataset11, dataset12, self.__num_instances)

            ratio1 = tapin_counter/taps_counter
            ratio2 = graspin_counter/grasp_counter

            ##########################
            # Finger Taps Scoring    #
            ##########################
            if ratio1 < 0.1:
                print("Finger Tap Score: 0")
                self.result['ftap'][1] = 0.0

            elif ratio1 <= 0.3:
                print("Finger Tap Score: 1")
                self.result['ftap'][1] = 1.0

            elif ratio1 <= 0.5:
                print("Finger Tap Score: 2")
                self.result['ftap'][1] = 2.0

            elif ratio1 <= 1:
                print("Finger Tap Score: 3")
                self.result['ftap'][1] = 3.0

            else:
                print("Finger Tap Score: 3")
                self.result['ftap'][1] = 3.0

            ##########################
            # Hand Movements Scoring #
            ##########################
            if ratio2 <= 0.1:
                print("Hand Movement Score: 0")
                self.result['htap'][1] = 0.0

            elif ratio2 <= 0.3:
                print("Hand Movement Score: 1")
                self.result['htap'][1] = 1.0

            elif ratio2 <= 0.5:
                print("Hand Movement Score: 2")
                self.result['htap'][1] = 2.0

            elif ratio2 <= 1:
                print("Hand Movement Score: 3")
                self.result['htap'][1] = 3.0

            else:
                print("Hand Movement Score: 3")
                self.result['htap'][1] = 3.0

        if patient_name != 'data-1':

            self.score_time_tremor()

            # calculate tremor amplitude
            self.calc_tremor_amplitude()

    def get_input(self):
        """

        :return:
        """
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 56))
        for i in range(total_inputs):
            dataset[i] = lines[i].split(' ')  # split data points of each instance

        # print(dataset_ftaps[1][0])
        print(dataset[0])
        print(dataset[0][54])
        for i in range(total_inputs):
            for k in range(55):
                if(k == 54):
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[i][k])
                    except ValueError:
                        # print("Line {} is corrupt!".format(i))
                        # print("column {} is corrupt!".format(k))
                        break

        return output

    def get_input_test(self, textfile):
        """

        :param textfile:
        :return:
        """
        dir_path = os.getcwd()
        text_file = open(str(dir_path) + "/resources/test_data/" + textfile , "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 56))
        for i in range(total_inputs):
            dataset[i] = lines[i].split(' ')  # split data points of each instance

        # print(dataset_ftaps[1][0])
        print(dataset[0])
        print(dataset[0][54])
        for i in range(total_inputs):
            for k in range(55):
                if(k == 54):
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[i][k])
                    except ValueError:
                        # print("Line {} is corrupt!".format(i))
                        # print("column {} is corrupt!".format(k))
                        break

        return output

    def get_input_1hz(self):
        """

        :return:
        """
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 3801))
        for i in range(total_inputs):
            dataset[i] = lines[i]  # split data points of each instance

        temp_count = 0

        for i in range(int(total_inputs/100)):
            for k in range(3801):
                if(k == 3800):
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[temp_count % total_inputs][k % 38])
                    except ValueError:
                        break

                if k % 38 == 0:
                    temp_count = temp_count + 1

        return output

    def get_input_1_3hz(self):
        """

        :return:
        """
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 11401))
        for i in range(total_inputs):
            dataset[i] = lines[i]  # split data points of each instance

        temp_count = 0

        for i in range(int(total_inputs/300)):
            for k in range(11401):
                if k == 11400:
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[temp_count % total_inputs][k % 38])
                    except ValueError:
                        break

                if k % 38 == 0:
                    temp_count = temp_count + 1

        return output

    def get_input_2hz(self):
        """

        :return:
        """
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 1901))
        for i in range(total_inputs):
            dataset[i] = lines[i]  # split data points of each instance

        temp_count = 0

        # output = float(dataset[1:2, 6:8, 15:17, 24:26, 33:35])

        for i in range(int(total_inputs/50)):
            for k in range(1901):
                if k == 1900:
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[temp_count % total_inputs][k % 38])
                    except ValueError:
                        # print("Line {} is corrupt!".format(i))
                        # print("column {} is corrupt!".format(k))
                        break
                if k % 38 == 0:
                    temp_count = temp_count + 1

        return output

    def get_input_3hz(self):
        """

        :return:
        """
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 1255))
        for i in range(total_inputs):
            dataset[i] = lines[i]  # split data points of each instance

        # print(dataset_ftaps[1][0])
        # print(dataset[0])
        # print(dataset[0][54])
        temp_count = 0

        # output = float(dataset[1:2, 6:8, 15:17, 24:26, 33:35])

        for i in range(int(total_inputs/33)):
            for k in range(1255):
                if(k == 1254):
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[temp_count % total_inputs][k % 38])
                    except ValueError:
                        # print("Line {} is corrupt!".format(i))
                        # print("column {} is corrupt!".format(k))
                        break
                if(k % 38 == 0 ):
                    temp_count = temp_count + 1

        return output

    def get_input_1hz_test(self, textfile):
        """

        :param textfile:
        :return:
        """
        dir_path = os.getcwd()
        text_file = open(str(dir_path) + "/resources/test_data/" + textfile , "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 3801))
        for i in range(total_inputs):
            dataset[i] = lines[i] # split data points of each instance
        temp_count = 0

        for i in range(int(total_inputs/100)):
            for k in range(3801):
                if k == 3800:
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[temp_count % total_inputs][k % 38])
                    except ValueError:
                        break
                if(k % 38 == 0 ):
                    temp_count = temp_count + 1

        return output

    def get_input_1_3hz_test(self, textfile):
        """

        :param textfile:
        :return:
        """
        dir_path = os.getcwd()
        text_file = open(str(dir_path) + "/resources/test_data/" + textfile , "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 11401))
        for i in range(total_inputs):
            dataset[i] = lines[i] # split data points of each instance

        # print(dataset_ftaps[1][0])
        # print(dataset[0])
        # print(dataset[0][54])
        temp_count = 0

        # output = float(dataset[1:2, 6:8, 15:17, 24:26, 33:35])

        for i in range(int(total_inputs/300)):
            for k in range(11401):
                if(k == 11400):
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[temp_count % total_inputs][k % 38])
                    except ValueError:
                        # print("Below values belong to 1_3hz")
                        # print("Line {} is corrupt!".format(i))
                        # print("column {} is corrupt!".format(k))
                        break
                if(k % 38 == 0 ):
                    temp_count = temp_count + 1

        return output

    def get_input_2hz_test(self, textfile):
        """

        :param textfile:
        :return:
        """
        dir_path = os.getcwd()
        text_file = open(str(dir_path) + "/resources/test_data/" + textfile , "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 1901))
        for i in range(total_inputs):
            dataset[i] = lines[i]  # split data points of each instance
        temp_count = 0

        for i in range(int(total_inputs/50)):
            for k in range(1901):
                if(k == 1900):
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[temp_count % total_inputs][k % 38])
                    except ValueError:
                        break
                if k % 38 == 0:
                    temp_count = temp_count + 1

        return output

    def get_input_3hz_test(self, textfile):
        """

        :param textfile:
        :return:
        """
        dir_path = os.getcwd()
        text_file = open(str(dir_path) + "/resources/test_data/" + textfile, "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 1255))
        for i in range(total_inputs):
            dataset[i] = lines[i]  # split data points of each instance

        temp_count = 0

        for i in range(int(total_inputs/33)):
            for k in range(1255):
                if k == 1254:
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[temp_count % total_inputs][k % 38])
                    except ValueError:
                        break
                if k % 38 == 0:
                    temp_count = temp_count + 1

        return output

    def get_weights(self, textfile):
        """

        :param textfile:
        :return:
        """
        dir_path = os.getcwd()
        text_file = open(str(dir_path) + "/resources/weights/" + textfile, "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        # dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        dataset = np.zeros((total_inputs, 1))
        # dataset = [[] for y in range(total_inputs)]
        for i in range(total_inputs):
            dataset[i][0] = float(lines[i])  # split data points of each instance
        # print(dataset[0][0])

        # print(dataset_ftaps[1][0])
        return dataset

    """
    Sigmoid maps a number between 1 and 0
    Sigmoid function:
                    1
    sigmoid(x)= ----------
                1 + e^(-x)
    """
    def sigmoid(self, temp_in):
        return np.float64(1 / (1 + np.exp( - temp_in)))

    """
    By multiplying the new inputs with our calculated
    column weights, we generate a column of prediction
    values to determine whether or not an action occured
    """
    def get_predictions(self, inputs, weights):
        return self.sigmoid(np.matmul(inputs, weights))

    def get_num_instances(self):
        """

        :return:
        """
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        return total_inputs

    def count_taps(self, dataset1, dataset2, dataset3, dataset4, total_instances):
        """

        :param dataset1:
        :param dataset2:
        :param dataset3:
        :param dataset4:
        :param total_instances:
        :return:
        """
        frequency_choice = 0
        max_count = 0
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):
            if float(dataset1[i][0]) > 0.999:
                count = count + 1
        if count > max_count:
            frequency_choice = 1
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if float(dataset2[i][0]) > 0.999:
                count = count + 1
        if count > max_count:
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if float(dataset3[i][0]) > 0.99:
                count = count + 1

        if count > max_count:
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):

            if float(dataset4[i][0]) > 0.75:
                count = count + 1

        if count > max_count:
            frequency_choice = 4
            max_count = count

        count = 0

        if frequency_choice == 1:
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            print("using 3HZ frequency")
            return max_count

        if frequency_choice == 2:
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            print("using 2HZ frequency")
            return max_count

        if frequency_choice == 3:
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            print("using 1HZ frequency")
            return max_count

        if frequency_choice == 4:
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            print("using 1/3HZ frequency")
            return max_count

        if max_count == 0:
            return print("no taps found, looking for tap interruptions")

    def count_tap_interuptions(self, dataset1, dataset2, dataset3, dataset4, total_instances):
        """

        :param dataset1:
        :param dataset2:
        :param dataset3:
        :param dataset4:
        :param total_instances:
        :return:
        """
        frequency_choice = 0
        max_count = 0
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):
            if float(dataset1[i][0]) > 0.999:
                count = count + 1

        if count > max_count:
            frequency_choice = 1
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if float(dataset2[i][0]) > 0.999:
                count = count + 1

        if count > max_count:
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if float(dataset3[i][0]) > 0.99:
                count = count + 1

        if count > max_count:
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):

            if float(dataset4[i][0]) > 0.75:
                count = count + 1

        if count > max_count:
            frequency_choice = 4
            max_count = count
        count = 0

        if frequency_choice == 1:
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            print("using 3HZ frequency")
            return max_count

        if frequency_choice == 2:
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            print("using 2HZ frequency")
            return max_count

        if frequency_choice == 3:
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            print("using 1HZ frequency")
            return max_count

        if frequency_choice == 4:
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            print("using 1/3HZ frequency")
            return max_count

        if max_count == 0:
            print("no tap interruptions found, looking for grasps")

    def count_grasps(self, dataset1, dataset2, dataset3, dataset4, total_instances):
        """

        :param dataset1:
        :param dataset2:
        :param dataset3:
        :param dataset4:
        :param total_instances:
        :return:
        """
        frequency_choice = 0
        max_count = 0
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):

            if float(dataset1[i][0]) > 0.999:
                count = count + 1
        if count > max_count:
            frequency_choice = 1
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if float(dataset2[i][0]) > 0.999:
                count = count + 1
        if count > max_count:
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if float(dataset3[i][0]) > 0.99:
                count = count + 1
        if count > max_count:
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):
            if float(dataset4[i][0]) > 0.75:
                count = count + 1

        if count > max_count:
            frequency_choice = 4
            max_count = count
        count = 0

        if frequency_choice == 1:
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            print("using 3HZ frequency")
            return max_count

        if frequency_choice == 2:
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            print("using 2HZ frequency")
            return max_count

        if frequency_choice == 3:
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            print("using 1HZ frequency")
            return max_count

        if frequency_choice == 4:
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            print("using 1/3HZ frequency")
            return max_count

        if max_count == 0:
            return print("no hand grasps found, looking for grasp interruptions")

    def count_grasp_interuptions(self, dataset1, dataset2, dataset3, dataset4, total_instances):
        """

        :param dataset1:
        :param dataset2:
        :param dataset3:
        :param dataset4:
        :param total_instances:
        :return:
        """
        frequency_choice = 0
        max_count = 0
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):
            if float(dataset1[i][0]) > 0.999:
                count = count + 1
        if count > max_count == 1:
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if float(dataset2[i][0]) > 0.999:
                count = count + 1
        if count > max_count:
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if float(dataset3[i][0]) > 0.99:
                count = count + 1
        if count > max_count:
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):
            if float(dataset4[i][0]) > 0.75:
                count = count + 1
        if count > max_count:
            frequency_choice = 4
            max_count = count
        count = 0

        if frequency_choice == 1:
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            print("using 3HZ frequency")
            return max_count

        if frequency_choice == 2:
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            print("using 2HZ frequency")
            return max_count

        if frequency_choice == 3:
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            print("using 1HZ frequency")
            return max_count

        if frequency_choice == 4:
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            print("using 1/3HZ frequency")
            return max_count

        if max_count == 0:
            return print("no hand grasp interruptions found")

    def score_time_tremor(self):

        # higher sample number will give us higher accuracy later
        # may need to change this later
        text_file = open("{}/bandpass.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 28))
        for i in range(total_inputs):
            dataset[i] = lines[i].split(' ')

        for rows in range(total_inputs):
            for columns in range(28):
                output[rows][columns] = float(dataset[rows][columns])

        true_data = output  # MAKE SURE TO PULL FROM FILE
        channel_num = true_data.shape[1]  # explicitly set to 28 by line: 914

        expected_sample_num = 10
        # fs = 100

        sample_size = int(self.__num_instances/expected_sample_num)

        # df = fs/sample_size
        sample_num = int(self.__num_instances/sample_size)

        test_data = np.zeros((sample_size, 24))

        # used to determine if the data has tremors
        tremor_amp = 3
        tremor_count = 0

        # s = slice(3,4,5,6,7,8,12,13,14,15,16,17,21,22,23,24,25,26,30,31,32,33,34,35)
        for i in range(0, sample_num):
            # true data should then be raw data
            s = slice(((i)*sample_size) , ((i+1)*sample_size) , 1)
            test_data = true_data[s][0:]
            # test_data_fft = sp.fft(test_data)
            mag = np.abs(test_data)

            # freq = 0 : df : fs - df
            # s2 = slice(beginning_index, end_index, 1)
            # mag_tremor = np.linalg.norm(true_data[s2][0:])
            mag_tremor_max = np.max(mag, axis=0)  # max value of mag
            for j in range(24):
                if mag_tremor_max[j] > tremor_amp:
                    tremor_count = tremor_count+1

            tremor_time = tremor_count/(sample_num * channel_num)

        if tremor_time == 0:
            print('Constancy of Tremor: 0 : Normal')
            self.result['crest'][1] = 0.0

        elif tremor_time <= 0.25:
            print('Constancy of Tremor: 1 : Slight')
            self.result['crest'][1] = 1.0

        elif tremor_time <= 0.5:
            print('Constancy of Tremor: 2 : Mild')
            self.result['crest'][1] = 2.0

        elif tremor_time <= 0.75:
            print('Constancy of Tremor: 3 : Moderate')
            self.result['crest'][1] = 3.0

        elif tremor_time <= 1:
            print('Constancy of Tremor: 4 : Severe')
            self.result['crest'][1] = 4.0

        else:
            print('Error')

    def calc_tremor_amplitude(self):
        # testing time: (slice)
        # 3*gravity, 1*hampel, 1*roll
        mat = extract(self.__filename, "GH", "MEk", "OHr")
        mat = np.matrix(mat).transpose()

        fs = 100
        data_for_Postural_Ax = mat[:, 0]  # 67 Hand_Ax
        data_for_Postural_Ay = mat[:, 1]  # 68 Hand_Ay
        data_for_Postural_Az = mat[:, 2]  # 69 Hand_Az

        data_for_Postural_EMG_rect = mat[:, 3]  # 79 EMG_rect
        data_length = self.__num_instances
        data_for_Postural_Vx = np.zeros((data_length, 1))

        for i in range(1, data_length):
            data_for_Postural_Vx[i] = data_for_Postural_Vx[i-1] + data_for_Postural_Ax[i-1] * (1/fs)
            # print(data_for_Postural_Vx[i])

        data_for_Postural_Vy = np.zeros((data_length, 1))

        for i in range(1, data_length):
            data_for_Postural_Vy[i] =data_for_Postural_Vy[i-1] + data_for_Postural_Ay[i-1] * (1/fs)

        data_for_Postural_Vz = np.zeros((data_length,1))

        for i in range(1, data_length):
            data_for_Postural_Vz[i] =data_for_Postural_Vz[i-1] + data_for_Postural_Az[i-1] * (1/fs)

        sample_period=100  # 1 second, can change later
        sample_num = int(data_length/sample_period)
        # times experiencing these tremors
        testing_time_post = np.zeros((data_length,1))
        testing_time_rest = np.zeros((data_length,1))
        testing_time_kine = np.zeros((data_length,1))
        sample_data_avg = np.zeros((1, 3)) # 1,4

        for i in range(1, sample_num+1):
            s = slice((i-1)*sample_period, i*sample_period,1)
            # sample_data = [ data_for_Postural_Vx[s][0], data_for_Postural_Vy[s][0], data_for_Postural_Vz[s][0], data_for_Postural_EMG_rect[s][0]]
            sample_data_avg = [np.abs(np.average(data_for_Postural_Vx[s])), np.abs(np.average(data_for_Postural_Vy[s])), np.abs(np.average(data_for_Postural_Vz[s]))] # was another one here
            sample_data_avg = np.matrix(sample_data_avg)
            # print(sample_data_avg)

            EMG_change = np.max(data_for_Postural_EMG_rect[s]) - np.min(data_for_Postural_EMG_rect[s])
            # print(EMG_change)
            if sample_data_avg.item((0,0)) < 200 and sample_data_avg.item((0,1)) < 50 and sample_data_avg.item((0,2)) < 400: # 0.05
                if EMG_change > 30: # 10
                    testing_time_post[s] = 1 # [s][0]
                else:
                    testing_time_rest[s] = 1 # [s][0]

            # (0,0) - - (0,1)
            if sample_data_avg.item((0,0)) < 200 and sample_data_avg.item((0,1)) < 50 and sample_data_avg.item((0,2)) > 400: # 0.2
                testing_time_kine[s] = 1 # [s][0]

        # real_testing_time = np.dot(testing_time, true_time[1:sample_num*sample_period, 0])
        # 3 steps does here calling the above function in order to do something
        # real_testing_time_post = np.dot(testing_time_post, data[57]) #57

        # calculating amplitude
        raw_data_tremor_amplitude_post = np.multiply(np.expand_dims(mat[:, 4], axis=0), np.transpose(testing_time_post))
        raw_data_tremor_amplitude_kine = np.multiply(np.expand_dims(mat[:, 4], axis=0), np.transpose(testing_time_kine))
        raw_data_tremor_amplitude_rest = np.multiply(np.expand_dims(mat[:, 4], axis=0), np.transpose(testing_time_rest))

        r_hand = 10  # centimeters
        # postural amplitude
        amplitude = np.abs(r_hand * (np.tan(np.abs(np.min(raw_data_tremor_amplitude_post))) + np.tan(np.abs(np.max(raw_data_tremor_amplitude_post)))))

        if amplitude <= 0.1:
            print("Postural Tremor Score: 0 : Normal")
            self.result['ptrem'][1] = 0.0

        elif amplitude <= 1:
            print("Postural Tremor Score: 1 : Slight")
            self.result['ptrem'][1] = 1.0

        elif amplitude <= 3:
            print("Postural Tremor Score: 2 : Mild")
            self.result['ptrem'][1] = 2.0

        elif amplitude <=10:
            print("Postural Tremor Score: 3 : Moderate")
            self.result['ptrem'][1] = 3.0

        elif amplitude > 10:
            print("Postural Tremor Score: 4 : Severe")
            self.result['ptrem'][1] = 4.0

        else:
            print("Postural Tremor amplitude error")
            self.result['ptrem'][1] = 4.0

        # kinetic amplitude
        amplitude = 100 * np.abs(r_hand * (np.tan(np.abs(np.min(raw_data_tremor_amplitude_kine))) + np.tan(np.abs(np.max(raw_data_tremor_amplitude_kine)))))

        if amplitude <= 0.1:
            print("Kinetic Tremor Score: 0 : Normal")
            self.result['ktrem'][1] = 0.0

        elif amplitude <= 1:
            print("Kineti Tcremor Score: 1 : Slight")
            self.result['ktrem'][1] = 1.0

        elif amplitude <= 3:
            print("Kinetic Tremor Score: 2 : Mild")
            self.result['ktrem'][1] = 2.0

        elif amplitude <=10:
            print("Kinetic Tremor Score: 3 : Moderate")
            self.result['ktrem'][1] = 3.0

        elif amplitude > 10:
            print("Kinetic Tremor Score: 4 : Severe")
            self.result['ktrem'][1] = 4.0

        else:
            print("Kinetic Tremor amplitude error")
            self.result['ktrem'][1] = 4.0

        # resting tremor
        amplitude = np.abs(r_hand * (np.tan(np.abs(np.min(raw_data_tremor_amplitude_rest))) + np.tan(np.abs(np.max(raw_data_tremor_amplitude_rest)))))

        if amplitude <= 0.1:
            print("Rest Tremor Score: 0 : Normal")
            self.result['rtrem'][1] = 0.0

        elif amplitude <= 1:
            print("Rest Tremor Score: 1 : Slight")
            self.result['rtrem'][1] = 1.0

        elif amplitude <= 3:
            print("Rest Tremor Score: 2 : Mild")
            self.result['rtrem'][1] = 2.0

        elif amplitude <=10:
            print("Rest Tremor Score: 3 : Moderate")
            self.result['rtrem'][1] = 3.0

        elif amplitude > 10:
            print("Rest Tremor Score: 4 : Severe")
            self.result['rtrem'][1] = 4.0

        else:
            print("Rest Tremor amplitude error")
            self.result['rtrem'][1] = 4.0

    def postural_tremor(self, data):
        """

        :param data:
        :return:
        """
        fs = 100
        data_for_Postural_Ax = data[67]  # 67 Hand_Ax
        data_for_Postural_Ay = data[68]  # 68 Hand_Ay
        data_for_Postural_Az = data[69]  # 69 Hand_Az

        data_for_Postural_EMG_rect = data[79]  # 79 EMG_rect
        data_length = len(data_for_Postural_Ax)

        data_for_Postural_Vx = np.zeros((data_length,1))

        for i in range(1, data_length):
            data_for_Postural_Vx[i][0] = data_for_Postural_Vx[i-1][0] + data_for_Postural_Ax[i][0] * (1/fs)

        data_for_Postural_Vy = np.zeros((data_length, 1))

        for i in range(1, data_length):
            data_for_Postural_Vy[i][0]=data_for_Postural_Vy[i-1][0] + data_for_Postural_Ay[i][0] * (1/fs)

        data_for_Postural_Vz = np.zeros((data_length,1))

        for i in range(1, data_length):
            data_for_Postural_Vz[i][0]=data_for_Postural_Vz[i-1][0] + data_for_Postural_Az[i][1] * (1/fs)

        sample_period=100
        sample_num = np.floor(data_length/sample_period)
        # times experiencing these tremors
        testing_time_post = np.zeros((sample_num*sample_period,1))
        testing_time_rest = np.zeros((sample_num*sample_period,1))
        testing_time_kine = np.zeros((sample_num*sample_period,1))
        sample_data_avg = np.zeros((1, 4))

        for i in range(0, sample_num):
            sample_data = [ data_for_Postural_Vx[(i-1)*sample_period:i*sample_period - 1, 0], data_for_Postural_Vy[(i-1)*sample_period:i*sample_period - 1, 0], data_for_Postural_Vz[(i-1)*sample_period:i*sample_period - 1 ,0], data_for_Postural_EMG_rect[(i-1)*sample_period:i*sample_period-1, 0]]
            sample_data_avg[0] = np.avg(sample_data)
            EMG_change = np.max(sample_data[3]) - np.min(sample_data[3])
            if sample_data_avg[0] < 0.05 and sample_data_avg[2] < 0.05 and sample_data_avg[1] < 0.05:
                if EMG_change > 10:
                    testing_time_post[(i-1)*sample_period:i*sample_period, 0] = 1
                else:
                    testing_time_rest[(i-1)*sample_period:i*sample_period, 0] = 1
            if sample_data_avg[0] < 0.05 and sample_data_avg[2] < 0.05 and sample_data_avg[1] > 0.2:
                testing_time_kine[(i-1)*sample_period:i*sample_period, 0] = 1

        # real_testing_time = np.dot(testing_time, true_time[1:sample_num*sample_period, 0])
        #3 steps does here calling the above function in order to do something
        real_testing_time_post = np.dot(testing_time_post, data[57]) #57
        real_testing_time_kine = np.dot(testing_time_kine, data[57]) #57
        real_testing_time_rest = np.dot(testing_time_rest, data[57]) #57
