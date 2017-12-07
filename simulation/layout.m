A = imread('./football.png');
%get image right side up
A = fliplr(A);

%figure out size of playing field
[cx,cy,cz] = size(A);

%inital positions
drone = [0, 0, 20];
ben = [0,0,0];

xImage = [-50 50; -50 50];      %# The x data for the image corners
yImage = [-25 -25; 25 25];      %# The y data for the image corners
zImage = [0 0; 0 0];            %# The z data for the image corners
surf(xImage,yImage,zImage,...   %# Plot the surface
     'CData',A,...
     'FaceColor','texturemap');
 
%resize figure for capture
figure('pos',[10 10 1280 720])

rotate3d on

for t = 1:160
    
    %replot image
    surf(xImage,yImage,zImage,...    %# Plot the surface
     'CData',A,...
     'FaceColor','texturemap');
    %keep plot for loop iteration
    hold on
    plot3(drone(1), drone(2), drone(3), 'hexagram');

    
    [ben(1), ben(2), ben(3)] = player(t,ben);
    angle = getAoA(ben,drone);
    
    [xguess, xerr] = transformAoA(angle,drone);
    
    %plot the new stripe
    xD = [(xguess-xerr) (xguess+xerr); (xguess-xerr) (xguess+xerr)];    %# The x data for the stripe
    yD = [-25 -25; 25 25];                                              %# The y data for the stripe
    zD = [0.1 0.1; 0.1 0.1];                                            %# Position stripe so we can see it
    surf(xD,yD,zD);
    plot3(ben(1),ben(2),ben(3)+.5,'*');
    xlim([-50,50]);
    ylim([-25,25]);
    %axis off;
    
    %pause(0.01);
    
    %Record frome for video
    F(t) = getframe;
    
    %reset figure
    hold off
end

%make video file
v = VideoWriter('touchdown','MPEG-4');

%add frames to video
open(v)
writeVideo(v,F)
close(v)
