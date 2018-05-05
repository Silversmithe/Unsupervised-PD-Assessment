"""
Object responsible for UPDRS scoring
of
"""
import scipy as sp
import numpy as np


class Score(object):

    SAMPLING_PERIOD_1 = 33
    SAMPLING_PERIOD_2 = 50
    SAMPLING_PERIOD_3 = 100
    SAMPLING_PERIOD_4 = 300

    def __init__(self, filename):
        self.__patient_path = filename
        self.variable = None
        self.__num_instances = self.get_num_instances(textfile=self.__patient_path)
        pass

    def process(self, textfile, dataset1, dataset2, dataset3, dataset4):
        """
        """
        self.get_input(textfile)
        self.count_taps(dataset1, dataset2, dataset3, dataset4, self.__num_instances)
        self.count_tap_interuptions(dataset1, dataset2, dataset3, dataset4, self.__num_instances)
        self.count_grasps(dataset1, dataset2, dataset3, dataset4, self.__num_instances)
        self.count_grasp_interuptions(dataset1, dataset2, dataset3, dataset4, self.__num_instances)
        
    def get_input(self, textfile):
        text_file = open(textfile, "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        for i in range(total_inputs):
            dataset[i] = lines[i].split('\t')  # split data points of each instance

        # print(dataset_ftaps[1][0])
        return dataset

    def get_num_instances(self, textfile):
        text_file = open(textfile, "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        return total_inputs

    def count_taps(self, dataset1, dataset2, dataset3, dataset4, total_instances):

        frequency_choice = 0
        max_count = 0
        temp_count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):
            if(dataset1[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0


        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(dataset2[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if dataset3[i][0] >= 0.5:
                count = count + 1

        if count > max_count:
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):

            if dataset4[i][0] >= 0.5:
                count = count + 1

        if count > max_count:
            frequency_choice = 4
            max_count = count

        count = 0

        if frequency_choice == 1:
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            return print("using 3HZ frequency")

        if frequency_choice == 2:
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            return print("using 2HZ frequency")

        if frequency_choice == 3:
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            return print("using 1HZ frequency")

        if frequency_choice == 4:
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            return print("using 1/3HZ frequency")

        if max_count == 0:
            return print("no taps found, looking for tap interruptions")
        # else:
        #     return print("use 1HZ frequency by default")

    def count_tap_interuptions(self, dataset1, dataset2, dataset3, dataset4, total_instances):

        frequency_choice = 0
        max_count = 0
        temp_count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):
            if(dataset1[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0


        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(dataset2[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if(dataset3[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):
            if(dataset4[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 4
            max_count = count
        count = 0

        if frequency_choice == 1:
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 3HZ frequency")

        if frequency_choice == 2:
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 2HZ frequency")

        if frequency_choice == 3:
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 1HZ frequency")

        if frequency_choice == 4:
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 1/3HZ frequency")

        if max_count == 0:
            return print("no tap interruptions found, looking for grasps")

    def count_grasps(self, dataset1, dataset2, dataset3, dataset4, total_instances):

        frequency_choice = 0
        max_count = 0
        temp_count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):

            if(dataset1[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(dataset2[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if(dataset3[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):
            if dataset4[i][0] >= 0.5:
                count = count + 1

        if count > max_count:
            frequency_choice = 4
            max_count = count
        count = 0

        if frequency_choice == 1:
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            return print("using 3HZ frequency")

        if frequency_choice == 2:
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            return print("using 2HZ frequency")

        if frequency_choice == 3:
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            return print("using 1HZ frequency")

        if frequency_choice == 4:
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            return print("using 1/3HZ frequency")

        if max_count == 0:
            return print("no hand grasps found, looking for grasp interruptions")
        # else:
        #     return print("use 1HZ frequency by default")

    def count_grasp_interuptions(self, dataset1, dataset2, dataset3, dataset4, total_instances):

        frequency_choice = 0
        max_count = 0
        temp_count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):
            if(dataset1[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(dataset2[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if(dataset3[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):
            if(dataset4[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 4
            max_count = count
        count = 0

        if frequency_choice == 1:
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 3HZ frequency")

        if frequency_choice == 2:
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 2HZ frequency")

        if frequency_choice == 3:
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 1HZ frequency")

        if frequency_choice == 4:
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 1/3HZ frequency")

        if max_count == 0:
            return print("no hand grasp interruptions found")

    def score_rest_tremor(self, bandpass_data):

        # higher sample number will give us higher accuracy later
        # may need to change this later

        true_data = bandpass_data  # MAKE SURE TO PULL FROM FILE

        expected_sample_num = 10
        fs = 100

        sample_size = np.floor(self.__num_instances/expected_sample_num)

        df = fs/sample_size

        sample_num = np.floor(self.__num_instances/sample_size)

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
            test_data_fft = np.fft(test_data)
            mag = np.abs(test_data_fft)

            # freq = 0 : df : fs - df

            mag_tremor = mag[beginning_index:end_index [0:]]
            mag_tremor_max = max(mag_tremor)
            for i in range(24):
                if mag_tremor_max(j) > tremor_amp:
                    tremor_count = tremor_count+1

            tremor_time = tremor_count/(sample_num*channel_num)

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
