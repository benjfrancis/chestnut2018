%% Input data here
close all

data = csvread('/Users/celialewis/Dropbox/SeniorDesignData/raw_player-April-22-2018-1301.csv');

avgx = mean(data(:,1));
variancex = var(data(:,1));
stand_devx = sqrt(variancex);
 
avgy = mean(data(:,2));
variancey = var(data(:,2));
stand_devy = sqrt(variancey);
 
for i = 11:length(data(:,1))
    if data(i,1) >= avgx+1*stand_devx || data(i,1) <= avgx-1*stand_devx
        data(i,1) = data((i-1),1);
    end
    if data(i,2) >= avgy+1*stand_devy || data(i,2) <= avgy-1*stand_devy
        data(i,2) = data((i-1),2);
    end
end

f = figure; 

GenerateKalmanFilt(data(:,1), avgx, variancex, f, 1);
title('X Position Kalman Output')
GenerateKalmanFilt(data(:,2), avgy, variancey, f, 2);
title('Y Position Kalman Output')

