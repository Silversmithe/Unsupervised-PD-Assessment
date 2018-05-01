"""
Object responsible for UPDRS scoring
of
"""
import numpy as np

class Score(object):

    SAMPLING_PERIOD_1 = 33
    SAMPLING_PERIOD_2 = 50
    SAMPLING_PERIOD_3 = 100
    SAMPLING_PERIOD_4 = 300

    def __init__(self):
        self.__num_instances = get_num_instances(filename=self.__patient_path)
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

    def get_num_instances(textfile):
        text_file = open(textfile, "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        return total_inputs


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


    # %% Constance of Rest Tremor
    # expected_sample_num=10;    % cut the data into at least how many pieces
    # sample_size=floor(data_length/expected_sample_num);
    # sample_num=floor(data_length/sample_size);
    # tremor_amp=3;   %to determine the if the subject has tremor
    # tremor_count=0;
    # for i=1:sample_num
    #     test_data=true_data((i-1)*sample_size+1:i*sample_size,[3:8,12:17,21:26,30:35]);
    #     test_data_fft=fft(test_data);
    #     mag=abs(test_data_fft);
    #     df=fs/sample_size;
    #     freq=0:df:fs-df;
    #     mag_tremor=mag(freq>3&freq<7,:);
    #     mag_tremor_max=max(mag_tremor);
    #     for j=1:channel_num
    #         if mag_tremor_max(j)>tremor_amp
    #             tremor_count=tremor_count+1;
    #         end
    #     end
    # end
    # tremor_time=tremor_count/(sample_num*channel_num);
    # if tremor_time==0
    #     disp('0: Normal')
    # elseif tremor_time<=0.25
    #     disp('1: Slight')
    # elseif tremor_time<=0.5
    #     disp('2: Mild')
    # elseif tremor_time<=0.75
    #     disp('3: Moderate')
    # elseif tremor_time<=1
    #     disp('4: Severe')
    # else
    #     disp('Error')
    # end

    def score_rest_tremor():

        # higher sample number will give us higher accuracy later
        # may need to change this later
        expected_sample_num = 10
        fs = 100

        sample_size = np.floor(self.__num_instances/expected_sample_num)

        df = fs/sample_size

        sample_num = np.floor(self.__num_instances/sample_size)

        test_data = np.zeros((sample_size,24))
        frequency = np.zeros((fs/df))

        beginning_index = 0
        beginning_flag = 0

        end_index = 0
        end_flag = 0


        for i in range(fs/df):
            frequency[i] = i * df
            if(frequency[i] > 3 and beginning_flag == 0):
                beginning_flag = 1
                beginning_index = i
            if(frequency[i] > 7 and beginning_flag == 1):
                end_index = i - 1
                end_flag = 1
            if(end_flag):
                break



        # used to determine if the patient has tremors
        tremor_amp = 3
        tremor_count = 0

        for i in range(0, sample_num):
            test_data = true_data[(i-1)*sample_size + 1 : i*sample_size[3:8,12:17,21:26,30:35]]
            test_data_fft = np.fft(test_data)
            mag = np.abs(test_data_fft)

            # freq = 0 : df : fs - df

            mag_tremor = mag[beginning_index:end_index [0:]]
            mag_tremor_max = max(mag_tremor)
            for i in range(24):
                if (mag_tremor_max(j) > tremor_amp):
                    tremor_count=tremor_count+1

            tremor_time=tremor_count/(sample_num*channel_num);

        if (tremor_time==0):
            print('0: Normal')
        elif(tremor_time<=0.25):
            print('1: Slight')
        elif(tremor_time<=0.5):
            print('2: Mild')
        elif(tremor_time<=0.75):
            print('3: Moderate')
        elif(tremor_time<=1):
            print('4: Severe')
        else:
            print('Error')
