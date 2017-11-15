A = imread('./football.png');
[cx,cy,cz] = size(A);

drone = [0, 0, 20];
ben = [0,0,0];


xImage = [-50 50; -50 50];   %# The x data for the image corners
yImage = [-25 -25; 25 25];   %# The y data for the image corners
zImage = [0 0; 0 0];   %# The z data for the image corners
surf(xImage,yImage,zImage,...    %# Plot the surface
     'CData',A,...
     'FaceColor','texturemap');
figure('pos',[10 10 1280 720])

rotate3d on


for t = 1:160
    
    surf(xImage,yImage,zImage,...    %# Plot the surface
     'CData',A,...
     'FaceColor','texturemap');
    hold on
    plot3(drone(1), drone(2), drone(3), 'hexagram');

    
    [ben(1), ben(2), ben(3)] = player(t,ben);
    angle = getAoA(ben,drone);
    
    [xguess, xerr] = transformAoA(angle,drone);
    xD = [(xguess-xerr) (xguess+xerr); (xguess-xerr) (xguess+xerr)];   %# The x data for the image corners
    yD = [-25 -25; 25 25];   %# The y data for the image corners
    zD = [0.1 0.1; 0.1 0.1];   %# The z data for the image corners
    surf(xD,yD,zD);
    plot3(ben(1),ben(2),ben(3)+.5,'*');
    
    %pause(0.01);
    
    
    F(t) = getframe;

    hold off
end
rotate3d on



v = VideoWriter('touchdown','MPEG-4');

open(v)
writeVideo(v,F)
close(v)
