function [ x,err ] = transformAoA( A, drone )
%TRANSFORMAOA Summary of this function goes here
%   Detailed explanation goes here
    x = drone(3)*tan(A)+2*rand();
    err = 5;
end

