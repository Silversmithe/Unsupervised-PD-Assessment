"""
Object responsible for UPDRS scoring
of
"""

class Score(object):

    SAMPLING_PERIOD_1 = 33
    SAMPLING_PERIOD_2 = 50
    SAMPLING_PERIOD_3 = 100
    SAMPLING_PERIOD_4 = 300
    
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


    def count_taps(dataset1, dataset2, dataset3, dataset4, total_instances):
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
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            return print("using 3HZ frequency")
        if(frequency_choice == 2):
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            return print("using 2HZ frequency")
        if(frequency_choice == 3):
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            return print("using 1HZ frequency")
        if(frequency_choice == 4):
            print("The finger tap count is: ")
            print(max_count)
            print("\n")
            return print("using 1/3HZ frequency")
        if(max_count == 0):
            return print("no taps found, looking for tap interruptions")
        # else:
        #     return print("use 1HZ frequency by default")



    def count_tap_interuptions(dataset_interupts1, dataset_interupts2, dataset_interupts3, dataset_interupts4, total_instances):
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
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 3HZ frequency")
        if(frequency_choice == 2):
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 2HZ frequency")
        if(frequency_choice == 3):
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 1HZ frequency")
        if(frequency_choice == 4):
            print("The finger tap interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 1/3HZ frequency")
        if(max_count == 0):
            return print("no tap interruptions found, looking for grasps")


    def count_grasps(dataset1, dataset2, dataset3, dataset4, total_instances):
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
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            return print("using 3HZ frequency")
        if(frequency_choice == 2):
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            return print("using 2HZ frequency")
        if(frequency_choice == 3):
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            return print("using 1HZ frequency")
        if(frequency_choice == 4):
            print("The hand grasp count is: ")
            print(max_count)
            print("\n")
            return print("using 1/3HZ frequency")
        if(max_count == 0):
            return print("no hand grasps found, looking for grasp interruptions")
        # else:
        #     return print("use 1HZ frequency by default")



    def count_grasp_interuptions(dataset_interupts1, dataset_interupts2, dataset_interupts3, dataset_interupts4, total_instances):
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
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 3HZ frequency")
        if(frequency_choice == 2):
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 2HZ frequency")
        if(frequency_choice == 3):
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 1HZ frequency")
        if(frequency_choice == 4):
            print("The hand grasp interrupt count is: ")
            print(max_count)
            print("\n")
            return print("using 1/3HZ frequency")
        if(max_count == 0):
            return print("no hand grasp interruptions found")
