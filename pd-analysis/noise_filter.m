%% read raw data
data=load("3-4-ftap-f.txt");  % read the data
% INPUT FORMAT: 
% dt EMG_raw EMG_rect Hand_Ax Hand_Ay Hand_Az Hand_Gx Hand_Gy Hand_Gz 
% Thumb_Ax Thumb_Ay Thumb_Az Thumb_Gx Thumb_Gy Thumb_Gz
% Point_Ax Point_Ay Point_Az Point_Gx Point_Gy Point_Gz
% Ring_Ax Ring_Ay Ring_Az Ring_Gx Ring_Gy Ring_Gz
fs=100;      %sampling frequency in HZ
[data_length,channel_num]=size(data);
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
%% plot all raw data
% figure(1)                      % plot raw data
% subplot(3,1,1)
% plot(true_time,Hand_Ax)
% subplot(3,1,2)
% plot(true_time,Hand_Ay)
% subplot(3,1,3)
% plot(true_time,Hand_Az)
% figure(2)
% subplot(3,1,1)
% plot(true_time,Thumb_Ax)
% subplot(3,1,2)
% plot(true_time,Thumb_Ay)
% subplot(3,1,3)
% plot(true_time,Thumb_Az)
% figure(3)
% subplot(3,1,1)
% plot(true_time,Point_Ax)
% subplot(3,1,2)
% plot(true_time,Point_Ay)
% subplot(3,1,3)
% plot(true_time,Point_Az)
% figure(4)
% subplot(3,1,1)
% plot(true_time,Ring_Ax)
% subplot(3,1,2)
% plot(true_time,Ring_Ay)
% subplot(3,1,3)
% plot(true_time,Ring_Az)
%% visualize sample data  
sample_signal=data(:,9);    % Hand_Ax
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
%% filter noise parameters
cut_low=8;   % cut-off freqency for the low pass filter
df=fs/data_length;
freq=df/fs:df:fs;
%% filter noise sample
raw_signal=data(:,3);
raw_signal_fft=fft(raw_signal);             
raw_signal_fft(abs(freq)>cut_low)=0;
filtered_signal=ifft(raw_signal_fft);
figure(3)
plot(true_time,raw_signal,'r',true_time,filtered_signal,'g')
% true_time,raw_signal,'r',
%% filter noise
data_filtered=zeros(data_length,channel_num);
for i=1:channel_num
    raw_signal=data(:,i);
    raw_signal_fft=fft(raw_signal);             
    raw_signal_fft(abs(freq)>cut_low)=0;
    filtered_signal=ifft(raw_signal_fft);
    data_filtered(:,i)=filtered_signal;
end
%% add time
data_filtered_with_time=horzcat(true_time,data_filtered);
%% plot filtered data for one senser
figure
subplot(3,1,1)
plot(true_time,data_filtered(:,15),'g') %true_time,data(:,i+1),'r',
subplot(3,1,2)
plot(true_time,data_filtered(:,16),'g') %true_time,data(:,i+1),'r',
subplot(3,1,3)
plot(true_time,data_filtered(:,17),'g') %true_time,data(:,i+1),'r',
%% plot filtered data
for i=1:channel_num-1
    figure(i)
    plot(true_time,data_filtered(:,i),'g') %true_time,data(:,i+1),'r',
end
%% cut meaningful period
data_filtered_real=real(data_filtered);
cut_start_time=2.2;
cut_stop_time=5.42;
meaningful_information=data_filtered_real(true_time>cut_start_time&true_time<cut_stop_time,:);
%% plot with time
plot(meaningful_information(:,1),meaningful_information(:,4))
xlabel('time');
%% output data
dlmwrite('3-4-ftap-e-8hz.txt',meaningful_information,'delimiter','\t')