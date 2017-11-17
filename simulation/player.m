function [ x,y,z ] = player(t, pos)
%PLAYER simulate motion of player on field
%   Takes in simulation time and previous position
%   TODO:
%   - should support several modes of motion (e.g. directed gaussian,
%   straight line, sinusoidal)
%   - should take in some sort of ID or object so multiple players can be
%   simulated
    x = t/4;
    y = 20*sin(t/60) + .01;
    z = pos(3) + 0;

end

