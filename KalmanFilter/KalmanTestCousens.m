%% Cousen Results data

data = csvread('testdata1.csv');

avgx = mean(data(:,1));
variancex = var(data(:,1));
stand_devx = sqrt(variancex);
 
avgy = mean(data(:,2));
variancey = var(data(:,2));
stand_devy = sqrt(variancey);
 
avgz = mean(data(:,3));
variancez = var(data(:,3));
stand_devz = sqrt(variancez);

KalmanFiltTest(data(:,1), avgx, variancex);
title('X Position Kalman Output')
KalmanFiltTest(data(:,2), avgy, variancey);
title('Y Position Kalman Output')
KalmanFiltTest(data(:,3), avgz, variancez);
title('Z Position Kalman Output')

