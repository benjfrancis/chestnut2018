function [ A ] = getAoA(pos, drone)
%GETAOA simulate AoA estimate from real position
%   Stand in function for AoA hardware, returns a single angle as the AoA
%   system would.
%   TODO: 
%   - should noise be added here?
%   - Support changing drone position
    A = atan((pos(1)-drone(1))/drone(3));

end

