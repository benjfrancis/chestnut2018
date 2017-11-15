function [ A ] = getAoA(pos, drone)
%GETAOA Summary of this function goes here
%   Detailed explanation goes here
    A = atan((pos(1)-drone(1))/drone(3));

end

