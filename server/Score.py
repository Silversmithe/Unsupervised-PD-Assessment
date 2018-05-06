"""
Object responsible for UPDRS scoring
of
"""
import scipy as sp
import numpy as np
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

        pass

    def process(self):
        """
        """
        # weights1 = self.__weights_ft_0hz
        # weights2 = self.__weights_ft_1hz
        # weights3 = self.__weights_ft_2hz
        # weights4 = self.__weights_ft_3hz

        # weights5 = self.__weights_ftin_0hz
        # weights6 = self.__weights_ftin_1hz
        # weights7 = self.__weights_ftin_2hz
        # weights8 = self.__weights_ftin_3hz
        #
        # weights5 = self.__weights_ftin_0hz
        # weights6 = self.__weights_ftin_1hz
        # weights7 = self.__weights_ftin_2hz
        # weights8 = self.__weights_ftin_3hz
        #
        # weights9 = self.__weights_hg_0hz
        # weights10 = self.__weights_hg_1hz
        # weights11 = self.__weights_hg_2hz
        # weights12 = self.__weights_hg_3hz
        #
        # weights13 = self.__weights_hgin_0hz
        # weights14 = self.__weights_hgin_1hz
        # weights15 = self.__weights_hgin_2hz
        # weights16 = self.__weights_hgin_3hz

        # inputs1 = self.get_input_1_3hz()
        # inputs2 = self.get_input_1hz()
        # inputs3 = self.get_input_2hz()
        # inputs4 = self.get_input_3hz()

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
        #
        # print(dataset1)
        # print(dataset2)
        # print(dataset3)
        # print(dataset4)

        taps_counter = self.count_taps(dataset1, dataset2, dataset3, dataset4, 2950)

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

        # print(dataset5)
        # print(dataset6)
        # print(dataset7)
        # print(dataset8)

        tapin_counter = self.count_tap_interuptions(dataset5, dataset6, dataset7, dataset8, 2901)

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

        # print(dataset9)
        # print(dataset10)
        # print(dataset11)
        # print(dataset12)

        grasp_counter = self.count_grasps(dataset9, dataset10, dataset11, dataset12, 2840)

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

        # print(dataset9)
        # print(dataset10)
        # print(dataset11)
        # print(dataset12)

        graspin_counter = self.count_grasp_interuptions(dataset13, dataset14, dataset15, dataset16, 2880)

        ratio1 = tapin_counter/taps_counter
        ratio2 = graspin_counter/grasp_counter

        if(ratio1 < 0.1):
            print("Finger Tap Score: 0")
        elif(ratio1 <= 0.3):
            print("Finger Tap Score: 1")
        elif(ratio1 <= 0.5):
            print("Finger Tap Score: 2")
        elif(ratio1 <= 1):
            print("Finger Tap Score: 3")
        else:
            print("Finger Tap Score: 3")

        if(ratio2 <= 0.1):
            print("Hand Movement Score: 0")
        elif(ratio2 <= 0.3):
            print("Hand Movement Score: 1")
        elif(ratio2 <= 0.5):
            print("Hand Movement Score: 2")
        elif(ratio2 <= 1):
            print("Hand Movement Score: 3")
        else:
            print("Hand Movement Score: 3")


        self.score_rest_tremor()
        # inputs1 = self.get_input_1_3hz_test("yousef_5.txt")
        # inputs2 = self.get_input_1hz_test("yousef_5.txt")
        # inputs3 = self.get_input_2hz_test("yousef_9.txt")
        # inputs4 = self.get_input_3hz_test("yousef_13.txt")

        # print(inputs1)


        #
        # print(dataset1)
        # print(dataset2)
        # print(dataset3)
        # print(dataset4)
        #
        # print(weights1)
        #
        # print(dataset1)

        # self.count_taps(dataset1, dataset2, dataset3, dataset4, 2950)
        # self.count_tap_interuptions(dataset1, dataset2, dataset3, dataset4, self.__num_instances)
        # self.count_grasps(dataset1, dataset2, dataset3, dataset4, self.__num_instances)
        # self.count_grasp_interuptions(dataset1, dataset2, dataset3, dataset4, self.__num_instances)

        # self.count_tap_interuptions(dataset5, dataset6, dataset7, dataset8, self.__num_instances)
        # self.count_grasps(dataset9, dataset10, dataset11, dataset12, self.__num_instances)
        # self.count_grasp_interuptions(dataset13, dataset14, dataset15, dataset16, self.__num_instances)

    def get_input(self):
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
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 3801))
        for i in range(total_inputs):
            dataset[i] = lines[i].split(' ')  # split data points of each instance

        # print(dataset_ftaps[1][0])
        print(dataset[0])
        print(dataset[0][54])
        temp_count = 0

        # output = float(dataset[1:2, 6:8, 15:17, 24:26, 33:35])

        for i in range(int(total_inputs/100)):
            for k in range(3801):
                if(k == 3800):
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

    def get_input_1_3hz(self):
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 11401))
        for i in range(total_inputs):
            dataset[i] = lines[i].split(' ')  # split data points of each instance

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
                        # print("Line {} is corrupt!".format(i))
                        # print("column {} is corrupt!".format(k))
                        break
                if(k % 38 == 0 ):
                    temp_count = temp_count + 1


        return output

    def get_input_2hz(self):
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 1901))
        for i in range(total_inputs):
            dataset[i] = lines[i].split(' ')  # split data points of each instance

        # print(dataset_ftaps[1][0])
        # print(dataset[0])
        # print(dataset[0][54])
        temp_count = 0

        # output = float(dataset[1:2, 6:8, 15:17, 24:26, 33:35])

        for i in range(int(total_inputs/50)):
            for k in range(1901):
                if(k == 1900):
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

    def get_input_3hz(self):
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 1255))
        for i in range(total_inputs):
            dataset[i] = lines[i].split(' ')  # split data points of each instance

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
        dir_path = os.getcwd()
        text_file = open(str(dir_path) + "/resources/test_data/" + textfile , "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 3801))
        for i in range(total_inputs):
            dataset[i] = lines[i] # split data points of each instance

        # print(dataset_ftaps[1][0])
        # print(dataset[0])
        # print(dataset[0][54])
        temp_count = 0

        # output = float(dataset[1:2, 6:8, 15:17, 24:26, 33:35])

        for i in range(int(total_inputs/100)):
            for k in range(3801):
                if(k == 3800):
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[temp_count % total_inputs][k % 38])
                    except ValueError:
                        # print("Below values belong to 1hz")
                        # print("Line {} is corrupt!".format(i))
                        # print("column {} is corrupt!".format(k))
                        break
                if(k % 38 == 0 ):
                    temp_count = temp_count + 1


        return output

    def get_input_1_3hz_test(self, textfile):
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
        dir_path = os.getcwd()
        text_file = open(str(dir_path) + "/resources/test_data/" + textfile , "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 1901))
        for i in range(total_inputs):
            dataset[i] = lines[i]  # split data points of each instance

        # print(dataset_ftaps[1][0])
        # print(dataset[0])
        # print(dataset[0][54])
        temp_count = 0

        # output = float(dataset[1:2, 6:8, 15:17, 24:26, 33:35])

        for i in range(int(total_inputs/50)):
            for k in range(1901):
                if(k == 1900):
                    output[i][k] = 1
                else:
                    try:
                        output[i][k] = float(dataset[temp_count % total_inputs][k % 38])
                    except ValueError:
                        # print("Below values belong to 2hz")
                        # print("Line {} is corrupt!".format(i))
                        # print("column {} is corrupt!".format(k))
                        break
                if(k % 38 == 0 ):
                    temp_count = temp_count + 1


        return output

    def get_input_3hz_test(self, textfile):
        dir_path = os.getcwd()
        text_file = open(str(dir_path) + "/resources/test_data/" + textfile , "r")
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
                        # print("Below values belong to 3hz")
                        # print("Line {} is corrupt!".format(i))
                        # print("column {} is corrupt!".format(k))
                        break
                if(k % 38 == 0 ):
                    temp_count = temp_count + 1


        return output



    def get_weights(self, textfile):
        dir_path = os.getcwd()
        print(os.getcwd())
        text_file = open(str(dir_path) + "/resources/weights/" + textfile , "r")
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
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        return total_inputs

    def count_taps(self, dataset1, dataset2, dataset3, dataset4, total_instances):

        frequency_choice = 0
        max_count = 0
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):
            if(float(dataset1[i][0]) > 0.999):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0


        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(float(dataset2[i][0]) > 0.999):
                count = count + 1
        if(count > max_count):
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
        # else:
        #     return print("use 1HZ frequency by default")

    def count_tap_interuptions(self, dataset1, dataset2, dataset3, dataset4, total_instances):

        frequency_choice = 0
        max_count = 0
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):
            if(float(dataset1[i][0]) > 0.999):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0


        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(float(dataset2[i][0]) > 0.999):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if(float(dataset3[i][0]) > 0.99):
                count = count + 1
        if(count > max_count):
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):
            if(float(dataset4[i][0]) > 0.75):
                count = count + 1
        if(count > max_count):
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

        frequency_choice = 0
        max_count = 0
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):

            if(float(dataset1[i][0]) > 0.999):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(float(dataset2[i][0]) > 0.999):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if(float(dataset3[i][0]) > 0.99):
                count = count + 1
        if(count > max_count):
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
        # else:
        #     return print("use 1HZ frequency by default")

    def count_grasp_interuptions(self, dataset1, dataset2, dataset3, dataset4, total_instances):

        frequency_choice = 0
        max_count = 0
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):
            if(float(dataset1[i][0]) > 0.999):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(float(dataset2[i][0]) > 0.999):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if(float(dataset3[i][0]) > 0.99):
                count = count + 1
        if(count > max_count):
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):
            if(float(dataset4[i][0]) > 0.75):
                count = count + 1
        if(count > max_count):
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

    def score_rest_tremor(self):

        # higher sample number will give us higher accuracy later
        # may need to change this later

        text_file = open("{}/bandpass.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        output = np.zeros((total_inputs, 3801))
        for i in range(total_inputs):
            dataset[i] = lines[i].split(' ')

        for rows in range(total_inputs):
            for columns in range(28):
                output[rows][columns] = float(dataset[rows][columns])

        true_data = output  # MAKE SURE TO PULL FROM FILE

        expected_sample_num = 10
        fs = 100

        sample_size = int(self.__num_instances/expected_sample_num)

        df = fs/sample_size

        sample_num = int(self.__num_instances/sample_size)

        test_data = np.zeros((sample_size, 24))
        frequency = np.zeros((fs/df))

        beginning_index = 0
        beginning_flag = 0

        end_index = 0
        end_flag = 0

        for i in range(fs/df):
            frequency[i] = i * df

            if frequency[i] > 3 and beginning_flag == 0:
                beginning_flag = 1
                beginning_index = i

            if frequency[i] > 7 and beginning_flag == 1:
                end_index = i - 1
                end_flag = 1

            if end_flag:
                break

        # used to determine if the patient has tremors
        tremor_amp = 3
        tremor_count = 0

        for i in range(0, sample_num):
            # true data should then be raw data
            test_data = true_data[(i-1)*sample_size + 1 : i*sample_size[3:8,12:17,21:26,30:35]]
            test_data_fft = sp.fft(test_data)
            mag = np.abs(test_data_fft)

            # freq = 0 : df : fs - df

            mag_tremor = mag[beginning_index:end_index [0:]]
            mag_tremor_max = max(mag_tremor)
            for i in range(24):
                if mag_tremor_max(j) > tremor_amp:
                    tremor_count = tremor_count+1

            tremor_time = tremor_count/(sample_num * channel_num)

        if tremor_time == 0:
            print('0: Normal')

        elif tremor_time <= 0.25:
            print('1: Slight')

        elif tremor_time<=0.5:
            print('2: Mild')

        elif tremor_time<=0.75:
            print('3: Moderate')

        elif(tremor_time<=1):
            print('4: Severe')

        else:
            print('Error')

    def calc_tremor_amplitude(self, data, testing_time):

        raw_data_tremor_amplitude = data[testing_time]

        r_hand = 5
        amplitude_upper = np.abs(np.max(raw_data_tremor_amplitude) - np.mean(raw_data_tremor_amplitude))
        amplitude_lower = np.abs(np.min(raw_data_tremor_amplitude) - np.mean(raw_data_tremor_amplitude))

        amplitude = 2 * r_hand * np.tan(np.max(amplitude_upper, amplitude_lower))

        if amplitude <= 0.1:
            print("Tremor Score: 0 : Normal")
        elif amplitude <= 1:
            print("Tremor Score: 1 : Slight")
        elif amplitude <= 3:
            print("Tremor Score: 2 : Mild")
        elif amplitude <=10:
            print("Tremor Score: 3 : Moderate")
        elif amplitude > 10:
            print("Tremor Score: 4 : Severe")
        else:
            print("Tremor amplitude error")

    def postural_tremor(self, data):

        fs = 100
        data_for_Postural_Ax = data[67] #67 Hand_Ax
        data_for_Postural_Ay = data[68] #68 Hand_Ay
        data_for_Postural_Az = data[69] #69 Hand_Az

        data_for_Postural_EMG_rect = data[79] #79 EMG_rect
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

    # Matlab Code in comments:
    # %% Postural Tremor of Hands
    # % stretch the arms out in front of the body with palms down
    # % rate by roll of hand
    # data_for_Postural_Ax=Hand_Ax;   % from gravity filter
    # data_for_Postural_Ay=Hand_Ay;   % from gravity filter
    # data_for_Postural_Az=Hand_Az;   % from gravity filter
    # data_for_Postural_EMG_rect=EMG_rect;
    # data_length=length(data_for_Postural_Ax);    % call data length from self?
    # data_for_Postural_Vx=zeros(data_length,1);
    # for i=2:data_length
    #     data_for_Postural_Vx(i,1)=data_for_Postural_Vx(i-1,1)+data_for_Postural_Ax(i,1)*fs;
    # end
    # data_for_Postural_Vy=zeros(data_length,1);
    # for i=2:data_length
    #     data_for_Postural_Vy(i,1)=data_for_Postural_Vy(i-1,1)+data_for_Postural_Ay(i,1)*fs;
    # end
    # data_for_Postural_Vz=zeros(data_length,1);
    # for i=2:data_length
    #     data_for_Postural_Vz(i,1)=data_for_Postural_Vz(i-1,1)+data_for_Postural_Az(i,1)*fs;
    # end
    # sample_period=100;   %1 seconds
    # sample_num=floor(data_length/sample_period);
    # testing_time_post=zeros(sample_num*sample_period,1);
    # testing_time_rest=zeros(sample_num*sample_period,1);
    # for i=1:sample_num
    #     sample_data=[data_for_Postural_Vx([(i-1)*sample_period+1,i*sample_period],1);...
    #         data_for_Postural_Vy([(i-1)*sample_period+1,i*sample_period],1);...
    #         data_for_Postural_Vz([(i-1)*sample_period+1,i*sample_period],1);...
    #         data_for_Postural_EMG_rect([(i-1)*sample_period+1,i*sample_period],1)];
    #     sample_data_avg=mean(sample_data);
    #     EMG_change=max(sample_data)-min(sample_data);
    #     if sample_data_avg(1)<0.05 && sample_data_avg(3)<0.05 && sample_data_avg(2)>0.2
    #         if EMG_change>10
    #             testing_time_post((i-1)*sample_period+1,i*sample_period,1)=1;
    #         else
    #             testing_time_rest((i-1)*sample_period+1,i*sample_period,1)=1;
    #         end
    #     end
    # end
    # real_testing_time=testing_time.*true_time([1:1:sample_num*sample_period],1);  %call from self
    # %% Kinetic Tremor of Hands
    # data_for_kinetic_Ax=Hand_Ax;   % from gravity filter
    # data_for_kinetic_Ay=Hand_Ay;   % from gravity filter
    # data_for_kinetic_Az=Hand_Az;   % from gravity filter
    # data_length=length(data_for_kinetic_Ax);    % call data length from self?
    # data_for_kinetic_Vx=zeros(data_length,1);
    # for i=2:data_length
    #     data_for_kinetic_Vx(i,1)=data_for_kinetic_Vx(i-1,1)+data_for_kinetic_Ax(i,1)*fs;
    # end
    # data_for_kinetic_Vy=zeros(data_length,1);
    # for i=2:data_length
    #     data_for_kinetic_Vy(i,1)=data_for_kinetic_Vy(i-1,1)+data_for_kinetic_Ay(i,1)*fs;
    # end
    # data_for_kinetic_Vz=zeros(data_length,1);
    # for i=2:data_length
    #     data_for_kinetic_Vz(i,1)=data_for_kinetic_Vz(i-1,1)+data_for_kinetic_Az(i,1)*fs;
    # end
    # sample_period=100;   %1 seconds
    # sample_num=floor(data_length/sample_period);
    # testing_time=zeros(sample_num*sample_period,1);
    # for i=1:sample_num
    #     sample_data=[data_for_kinetic_Vx([(i-1)*sample_period+1,i*sample_period],1);...
    #         data_for_kinetic_Vy([(i-1)*sample_period+1,i*sample_period],1);...
    #         data_for_kinetic_Vz([(i-1)*sample_period+1,i*sample_period],1)];
    #     sample_data_avg=mean(sample_data);
    #     if sample_data_avg(1)<0.05 && sample_data_avg(3)<0.05 && sample_data_avg(2)>0.2
    #         testing_time((i-1)*sample_period+1,i*sample_period,1)=1;
    #     end
    # end
    # real_testing_time=testing_time.*true_time;  %call from self
