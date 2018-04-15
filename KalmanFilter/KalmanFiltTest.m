function KalmanFiltTest(data, mean, var)
s.A = 1;
% Process noise
%%% adjust this for better/worse results - guess and check
s.Q = .4^2; %stdev^2
% Define the voltimeter to measure the voltage itself:
s.H = 1;
% Measurement error
s.R = var; % stdev^2
% No system input
s.B = 0;
s.u = 0;
% No initial state:
s.x = nan;
s.P = nan;
 
 
leng = length(data);
 
tru=[];
for t=1:leng
    tru(end+1) = mean;
    s(end).z = data(t); %measurement
    s(end+1)=kalmanf(s(end)); % perform a Kalman filter iteration
end
 
 
figure
hold on
grid on
% plot measurement data:
hz=plot([s(1:end-1).z],'r.');
% plot a-posteriori state estimates:
hk=plot([s(2:end).x],'b-');
ht=plot(tru,'g-');
legend('observations','Kalman output','true value')
end
