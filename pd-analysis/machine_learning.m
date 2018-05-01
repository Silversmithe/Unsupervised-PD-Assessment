% clear
true_data_alex=load("alex_14.txt");
true_data_sam=load("sam_14.txt");
true_data_yousef=load("yousef_14.txt");
true_data=[true_data_alex;true_data_sam];
% ;true_data_yousef
[true_data_length,~]=size(true_data);
false_data_alex=load("alex_13.txt");
false_data_sam=load("sam_13.txt");
false_data_yousef=load("yousef_13.txt");
false_data=[false_data_alex;false_data_sam];
% ;false_data_yousef
data=[true_data;false_data];
% ;false_data
[data_length,features_num]=size(data);
%% normalization
data_avg=mean(data);
data_std=std(data);
data_1=(data-ones(data_length,1)*data_avg)./(ones(data_length,1)*data_std);
% data_1=normalize(data);
%% creating new matrix
sample_period=33;
X=[zeros(data_length-sample_period+1,features_num*sample_period),ones(data_length-sample_period+1,1)];
for i=1:data_length-sample_period+1
    for j=1:sample_period
        X(i,(j-1)*features_num+1:1:j*features_num)=data_1(i-1+j,:);
    end
end
[output_length,~]=size(X);
Y=[ones(true_data_length-sample_period+1,1);zeros(output_length-(true_data_length-sample_period+1),1)];
%% output as txt
% dlmwrite("1_All_new.txt",X,'delimiter','\t')
% dlmwrite("1_All_new_result.txt",Y,'delimiter','\t')
%% machine learning
learning_rate=0.0001;
percision=0.001;
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
%% testing
test_data=true_data_yousef;
[test_data_length,~]=size(test_data);
test_data_avg=mean(test_data);
test_data_std=std(test_data);
test_data_1=(test_data-ones(test_data_length,1)*test_data_avg)./(ones(test_data_length,1)*test_data_std);
% test_X=[zeros(test_data_length-sample_period+1,features_num*sample_period),ones(test_data_length-sample_period+1,1)];
% for i=1:test_data_length-sample_period+1
%     for j=1:sample_period
%         test_X(i,(j-1)*features_num+1:1:j*features_num)=test_data_1(i-1+j,:);
%     end
% end
test_X_length=floor(test_data_length/sample_period)*sample_period;
test_X=reshape(test_data_1(1:1:test_X_length,:),[],sample_period*features_num);
[test_X_length,~]=size(test_X);
test_X=[test_X,ones(test_X_length,1)];
test_Y=1./(1+exp(-test_X*W));
