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


    def choose_frequency(dataset1, dataset2, dataset3, dataset4):
        

    def count_taps(dataset_taps, dataset_interupts):
