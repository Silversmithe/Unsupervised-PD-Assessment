%% read raw data
data=load("fake-tremor-021818.txt");  % read the data
% INPUT FORMAT: 
% dt EMG_raw EMG_rect Hand_Ax Hand_Ay Hand_Az Hand_Gx Hand_Gy Hand_Gz 
% Thumb_Ax Thumb_Ay Thumb_Az Thumb_Gx Thumb_Gy Thumb_Gz
% Point_Ax Point_Ay Point_Az Point_Gx Point_Gy Point_Gz
% Ring_Ax Ring_Ay Ring_Az Ring_Gx Ring_Gy Ring_Gz
fs=100;      %sampling frequency in HZ
[data_length,~]=size(data);
true_time=(0:1/fs:(data_length-1)/fs)';
% EMG_raw=data(:,2);    % EMG raw
% EMG_rect=data(:,3);   % EMG rect
% Hand_Ax=data(:,4);    % hand a
% Hand_Ay=data(:,5);
% Hand_Az=data(:,6);
% Hand_Gx=data(:,7);    % hand g
% Hand_Gy=data(:,8);
% Hand_Gz=data(:,9);
% Thumb_Ax=data(:,10);  % thumb a
% Thumb_Ay=data(:,11);  
% Thumb_Az=data(:,12);
% Thumb_Gx=data(:,13);  % thumb g
% Thumb_Gy=data(:,14);  
% Thumb_Gz=data(:,15);
% Point_Ax=data(:,16);  % point a
% Point_Ay=data(:,17);  
% Point_Az=data(:,18);
% Point_Gx=data(:,19);  % point g
% Point_Gy=data(:,20);  
% Point_Gz=data(:,21);
% Ring_Ax=data(:,22);   % ring a
% Ring_Ay=data(:,23);  
% Ring_Az=data(:,24);
% Ring_Gx=data(:,25);   % ring g
% Ring_Gy=data(:,26);  
% Ring_Gz=data(:,27);
%% visualize sample data  
sample_signal=true_data(:,18);    % Hand_Ax
sample_signal=sample_signal-mean(sample_signal);   
nsample_signal=sample_signal/max(abs(sample_signal));
figure(1)
plot(true_time,nsample_signal)
axis tight
ylabel('sample signal')
xlabel('Time in seconds')
EMG_raw_fft=fft(nsample_signal,data_length);
mag=abs(EMG_raw_fft);
df=fs/data_length;
freq=0:df:fs/2;
figure(2)
plot(freq(1:data_length/2+1),mag(1:data_length/2+1),'-')
grid
ylabel('Magnitude')
xlabel('Frequency in HZ')
%% cut meaningful period
cut_start_time=22.52;
cut_stop_time=61.45;
true_data=data(true_time>cut_start_time&true_time<cut_stop_time,3:26);  % cut EMG
[data_length,channel_num]=size(true_data);
true_time=(0:1/fs:(data_length-1)/fs)';
%% plot meaningful data
for i=1:channel_num
    figure(i)
    plot(true_time,true_data(:,i),'g') %true_time,data(:,i+1),'r',
end
%% Finger Taps
% interruption ratio
interruption_ratio=interruption/taps_count;
if interruption_ratio<1
    interruption_rating=0;
elseif interruption_ratio<3
    interruption_rating=1;
elseif interruption_ratio<5
    interruption_rating=2;
elseif interruption_ratio<10
    interruption_rating=3;
else
    interruption_rating=4;
end
% speed
finger_tap_speed=finger_tap_time/taps_count;
if finger_tap_speed<1
    speed_rating=0;
elseif finger_tap_speed<3
    speed_rating=1;
elseif finger_tap_speed<5
    speed_rating=2;
elseif finger_tap_speed<10
    speed_rating=3;
else
    speed_rating=4;    % cannot perform: how to define
end
% amplitude decrement
decrement=5;
amplitude_rating=0;
if amplitude(2)-amplitude(1)>decrement
    amplitude_rating=3;
end
for i=2:7
    if amplitude(i+1)-amplitude(i)>decrement
        amplitude_rating=2;
    end
end
for i=8:9
    if amplitude(i+1)-amplitude(i)>decrement
        amplitude_rating=1;
    end
end
% Final Rating
finger_tap_rating=mode(interruption_rating,speed_rating,amplitude_rating);
disp(finger_tap_rating)
%% Hand Movements
% interruption ratio
interruption_ratio=interruption/taps_count;
if interruption_ratio<1
    interruption_rating=0;
elseif interruption_ratio<3
    interruption_rating=1;
elseif interruption_ratio<5
    interruption_rating=2;
elseif interruption_ratio<10
    interruption_rating=3;
else
    interruption_rating=4;
end
% speed
finger_tap_speed=finger_tap_time/taps_count;
if finger_tap_speed<1
    speed_rating=0;
elseif finger_tap_speed<3
    speed_rating=1;
elseif finger_tap_speed<5
    speed_rating=2;
elseif finger_tap_speed<10
    speed_rating=3;
else
    speed_rating=4;    % cannot perform: how to define
end
% amplitude decrement
decrement=5;
amplitude_rating=0;
if amplitude(2)-amplitude(1)>decrement
    amplitude_rating=3;
end
for i=2:7
    if amplitude(i+1)-amplitude(i)>decrement
        amplitude_rating=2;
    end
end
for i=8:9
    if amplitude(i+1)-amplitude(i)>decrement
        amplitude_rating=1;
    end
end
% Final Rating
hand_movement_rating=mode(interruption_rating,speed_rating,amplitude_rating);
disp(hand_movement_rating)
%% Postural Tremor of Hands
% stretch the arms out in front of the body with palms down
% rate by roll of hand
amplitude=
%% Kinetic Tremor of Hands

%% Rest Tremor Amplitude

%% Constance of Rest Tremor
expected_sample_num=10;    % cut the data into at least how many pieces
sample_size=floor(data_length/expected_sample_num);
sample_num=floor(data_length/sample_size);
tremor_amp=3;   %to determine the if the subject has tremor 
tremor_count=0;
for i=1:sample_num
    test_data=true_data((i-1)*sample_size+1:i*sample_size,:);
    test_data_fft=fft(test_data);
    mag=abs(test_data_fft);
    df=fs/sample_size;
    freq=0:df:fs-df;
    mag_tremor=mag(freq>3&freq<7,:);
    mag_tremor_max=max(mag_tremor);
    for j=1:channel_num
        if mag_tremor_max(j)>tremor_amp
            tremor_count=tremor_count+1;
        end
    end
end
tremor_time=tremor_count/(sample_num*channel_num);
if tremor_time==0
    disp('0: Normal')
elseif tremor_time<=0.25
    disp('1: Slight')
elseif tremor_time<=0.5
    disp('2: Mild')
elseif tremor_time<=0.75
    disp('3: Moderate')
elseif tremor_time<=1
    disp('4: Severe')
else
    disp('Error')
end
% plot(freq(1:sample_size),mag(1:sample_size,j),'-')