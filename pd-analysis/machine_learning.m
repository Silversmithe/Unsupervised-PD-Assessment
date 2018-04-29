clear 
data=load("1_All.txt");
%% normalization
data_1=normalize(data);
%% creating new matrix
sample_period=300;
[data_length,features_num]=size(data);
X=[zeros(data_length-sample_period+1,features_num*sample_period),ones(data_length-sample_period+1,1)];
for i=1:data_length-sample_period+1
    for j=1:sample_period
        X(i,(j-1)*features_num+1:1:j*features_num)=data_1(i-1+j,:);
    end
end
[output_length,~]=size(X);
Y=ones(output_length,1);
%% output as txt
% dlmwrite("1_All_new.txt",X,'delimiter','\t')
% dlmwrite("1_All_new_result.txt",Y,'delimiter','\t')
%% machine learning
learning_rate=0.1;
percision=0.0001;
goal=0.10;
W=rand(features_num*sample_period+1,1);
rounds=0;
error2=sum(abs(1./(1+exp(-X*W))-Y))/output_length;
while 1
    error=error2;
    W=W+learning_rate.*(X.'*(Y-1./(1+exp(-X*W))));
    error2=sum(abs(1./(1+exp(-X*W))-Y))/output_length;
    rounds=rounds+1;
    if abs(error2-error) < percision 
        if error2 <= goal
            break
        end
    end
end
%% output W
% dlmwrite("W.txt",W,'delimiter','\t')