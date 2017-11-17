function [ x,err ] = transformAoA( A, drone )
%TRANSFORMAOA Performs cooridinate transformation back to cartesian coords
%   This function should operate like the final function on the drone which
%   will calculate where to locate the stripe
%   TODO:
%   - Support velocity AND position estimators
%   - Support noise level estimates
%   - Support transforms in x,y,z
%   - Support changing drone positions
    x = drone(3)*tan(A)+2*rand();
    err = 5;
end

