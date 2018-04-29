"""
Object responsible for UPDRS scoring
of
"""

class Score(object):

    def __init__(self):
        pass

    def pick_method(self, packet):
        """
            @param: packet: a packet of data we would like
                            to score
        """
        pass

    # example methods
    def method1(self):
        # example method
        pass

    def method2(self):
        pass

    # display
    def display_score(self):
        pass


    def get_input(textfile):
        text_file = open(textfile, "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        for i in range(total_inputs):
        #split data points of each instance
            dataset[i] = lines[i]
        # print(dataset_ftaps[1][0])
        return dataset


    def choose_frequency(dataset1, dataset2, dataset3, dataset4, total_instances):
        sampling_period_1 = 33
        sampling_period_2 = 50
        sampling_period_3 = 100
        sampling_period_4 = 300

        frequency_choice = 0
        max_count = 0
        temp_count = 0

        for i in range(0, int(total_instances/sampling_period_1)):
            if(dataset1[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0


        for i in range(0, int(total_instances/sampling_period_2)):
            if(dataset2[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/sampling_period_3)):
            if(dataset3[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/sampling_period_4)):
            if(dataset4[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 4
            max_count = count
        count = 0

        if(frequency_choice == 1):
            return print("use 3HZ frequency")
        if(frequency_choice == 2):
            return print("use 2HZ frequency")
        if(frequency_choice == 3):
            return print("use 1HZ frequency")
        if(frequency_choice == 4):
            return print("use 1/3HZ frequency")
        else:
            return print("use 1HZ frequency by default")



    def count_taps(dataset_taps, dataset_interupts):
