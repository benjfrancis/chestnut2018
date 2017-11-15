function [ x,y,z ] = player(t, pos)
%RECORD Summary of this function goes here
%   Detailed explanation goes here
    x = t/4;
    y = 20*sin(t/60) + .01;
    z = pos(3) + 0;

end

