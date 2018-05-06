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
        self.__filename = filename
        self.variable = None
        self.__num_instances = self.get_num_instances()
        pass

    def process(self):
        """
        """
        dataset1 = self.get_input()
        dataset2 = self.get_input()
        dataset3 = self.get_input()
        dataset4 = self.get_input()

        self.count_taps(dataset1, dataset2, dataset3, dataset4, self.__num_instances)
        self.count_tap_interuptions(dataset1, dataset2, dataset3, dataset4, self.__num_instances)
        self.count_grasps(dataset1, dataset2, dataset3, dataset4, self.__num_instances)
        self.count_grasp_interuptions(dataset1, dataset2, dataset3, dataset4, self.__num_instances)

    def get_input(self):
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        dataset = [[float(0) for x in range(1)] for y in range(total_inputs)]
        for i in range(total_inputs):
            dataset[i] = lines[i].split("\t")  # split data points of each instance

        # print(dataset_ftaps[1][0])
        return dataset

    def get_num_instances(self):
        text_file = open("{}/raw.txt".format(self.__filename), "r")
        lines = text_file.read().split("\n")
        total_inputs = len(lines) - 1
        text_file.close()

        return total_inputs

    """
    Sigmoid maps a number between 1 and 0
    Sigmoid function:
                    1
    sigmoid(x)= ----------
                1 + e^(-x)
    """
    def sigmoid(temp_in):
        return np.float64(1 / (1 + np.exp( - temp_in)))


    """
    By multiplying the new inputs with our calculated
    column weights, we generate a column of prediction
    values to determine whether or not an action occured
    """
    def get_predictions(inputs, weights):
        return sigmoid(np.matmul(inputs, weights))

    def count_taps(self, dataset1, dataset2, dataset3, dataset4, total_instances):

        frequency_choice = 0
        max_count = 0
        temp_count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_1)):
            if(float(dataset1[i][0]) >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0


        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(float(dataset2[i][0]) >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if float(dataset3[i][0] >= 0.5):
                count = count + 1

        if count > max_count:
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):

            if float(dataset4[i][0] >= 0.5:
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
            if(float(dataset1[i][0]) >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0


        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(float(dataset2[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if(float(dataset3[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):
            if(float(dataset4[i][0] >= 0.5):
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

            if(float(dataset1[i][0]) >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(float(dataset2[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if(float(dataset3[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):
            if float(dataset4[i][0] >= 0.5:
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
            if(float(dataset1[i][0]) >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 1
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_2)):
            if(float(dataset2[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 2
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_3)):
            if(float(dataset3[i][0] >= 0.5):
                count = count + 1
        if(count > max_count):
            frequency_choice = 3
            max_count = count
        count = 0

        for i in range(0, int(total_instances/self.SAMPLING_PERIOD_4)):
            if(float(dataset4[i][0] >= 0.5):
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
        data_length = length(data_for_Postural_Ax)

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
