 %% read raw data
data=load("sam.txt");  % read the data
% INPUT FORMAT: 
% dt EMG_raw EMG_rect Hand_Ax Hand_Ay Hand_Az Hand_Gx Hand_Gy Hand_Gz 
% Thumb_Ax Thumb_Ay Thumb_Az Thumb_Gx Thumb_Gy Thumb_Gz
% Point_Ax Point_Ay Point_Az Point_Gx Point_Gy Point_Gz
% Ring_Ax Ring_Ay Ring_Az Ring_Gx Ring_Gy Ring_Gz
fs=100;      %sampling frequency in HZ
[data_length,channel_num]=size(data);
true_time=(1/fs:1/fs:data_length/fs)';
EMG_raw=data(:,1);    % EMG raw
EMG_rect=data(:,2);   % EMG rect
Hand_Ax=data(:,3);    % hand a
Hand_Ay=data(:,4);
Hand_Az=data(:,5);
Hand_Gx=data(:,6);    % hand g
Hand_Gy=data(:,7);
Hand_Gz=data(:,8);
Hand_Mx=data(:,9);    % hand m
Hand_My=data(:,10);
Hand_Mz=data(:,11);
Thumb_Ax=data(:,12);  % thumb a
Thumb_Ay=data(:,13);  
Thumb_Az=data(:,14);
Thumb_Gx=data(:,15);  % thumb g
Thumb_Gy=data(:,16);  
Thumb_Gz=data(:,17);
Thumb_Mx=data(:,18);  % thumb g
Thumb_My=data(:,19);  
Thumb_Mz=data(:,20);
Point_Ax=data(:,21);  % point a
Point_Ay=data(:,22);  
Point_Az=data(:,23);
Point_Gx=data(:,24);  % point g
Point_Gy=data(:,25);  
Point_Gz=data(:,26);
Point_Mx=data(:,27);  % point m
Point_My=data(:,28);  
Point_Mz=data(:,29);
Ring_Ax=data(:,30);   % ring a
Ring_Ay=data(:,31);  
Ring_Az=data(:,32);
Ring_Gx=data(:,33);   % ring g
Ring_Gy=data(:,34);  
Ring_Gz=data(:,35);
Ring_Mx=data(:,36);   % ring m
Ring_My=data(:,37);  
Ring_Mz=data(:,38);
Hand_Pp=data(:,39);   % hand position
Hand_Py=data(:,40);
Hand_Pr=data(:,41);
Thumb_Pp=data(:,42);  % thumb position
Thumb_Py=data(:,43);
Thumb_Pr=data(:,44);
Point_Pp=data(:,45);  % point position
Point_Py=data(:,46);
Point_Pr=data(:,47);
Ring_Pp=data(:,48);   % ring position
Ring_Py=data(:,49);
Ring_Pr=data(:,50);
%% visualize sample data  
sample_signal=Hand_Ax;    % Hand_Ax
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
%% Calculate Tremor Amplitude
data_tremor_amplitude=Hand_Pr;

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