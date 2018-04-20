h = 160;
w = 120;

% Some example data

% data = [0.306103, 0.431096, -3.40221, 2.984374, 0.01805, -6.238098];

%data = [5.180696,-3.209169,-29.291536,3.967077,0.286022,-2.921849];

%data = [-3.257970,-4.593473,-11.454717,2.672334,5.861568,-5.982584];
data = [67, 56, 0, 2, -0.27438, -2.787124, -8.845457, 2.895061, 0.361846, -0.989036, 19];
% 
% Tx = data(5);
% Ty = data(6);
% Tz = data(7);
% 
% Rx = data(8);
% Ry = data(9);
% Rz = data(10);

%rotationCCW from world to camera:
% X: pi-Rx
% Y: -Ry
% Z: -Rz

Tx = 5;
Ty = 4;
Tz = -10;

Rx = pi/4;
Ry = -pi/8;
Rz = pi/4;

% From here we can build a rotation matrix, used by many of the calcuations
% we need to solve this problem

R_x = [1       ,  0      ,        0;
       0       ,  cos(Rx),  sin(Rx);
       0       , -sin(Rx),  cos(Rx)];

R_y = [ cos(Ry),  0      ,  -sin(Ry);
        0      ,  1      ,        0;
        sin(Ry),  0      ,  cos(Ry)];

R_z = [ cos(Rz),  sin(Rz),        0;
       -sin(Rz),  cos(Rz),        0;
        0      ,  0      ,        1];
   
R = R_x*R_y*R_z;

% We can define the plane of the field using "point-normal." We have our
% point (Tx, Ty, Tz) but now we must construct our normal vector. We can
% construct using trigonometry. We know:
% - Each component of the normal does not depend on the angle to its own
% axis

nz = cosd(Ry)*cosd(Rx);
ny = sind(Rx)*cosd(Rz);
nx = sind(Ry)*cosd(Rz);




t = [Tx, Ty, Tz];
X = [t, 1];

% Find the camera origin in the world coordinates

A = [R ; 0 0 0];
A = [A X'];

X_cam = [0 0 0 1];
%X_world = -A\X_cam';
X_world  = R*(-t)';

% plane eq: nx(x - Tx) + ny(y - Ty) + nz(z - Tz) = 0
%           = nx*x + ny*y + nz*z -(nx*Tx + ny*Ty + nz*Tz)
pi_1 = nx;
pi_2 = ny;
pi_3 = nz;
pi_4 = -(nx*Tx + ny*Ty + nz*Tz);

P = [pi_1; pi_2; pi_3; pi_4];

% This should be zero if our point lies on this plane
check = dot(P,X);

% Given calibration matrix K, where
% fx is the focal length in the X direction, or, "the lens focal length
% in mm, divided by the camera sensor length in the X direction multiplied 
% by the number of camera sensor pixels in the X direction." The same
% principle follows for fy. cx and cy are the image height and width /2
% There calculations are from the openMV documentation

%fx = (2.8/3.984)*656;
%fy = (2.8/2.952)*488;
fx = (2.8/3.984)*160;% + 50;
fy = (2.8/2.952)*120;% + 50/160*120;
cx = 160/2;
cy = 120/2;

K = [fx, 0, cx;
     0, fy, cy;
     0, 0 , 1];
 
% We can build homography matrix H using this
% TODO: this is wrong! R is from camera to world not world to camera like
% this equation
R_wc = R';
RT = [R_wc(:,1) R_wc(:,2) t'];
H = K*RT;



% Now we project our image coordinated to 2D plane coordinates
% x_img = H*x_p => H\x_img = x_p
pix = [86, 64];

x_img = [cx-10, cy, 1];
%x_img = [2*cx - data(1), data(2), 1];
%x_img = [2*cx - pix(1), pix(2), 1];
%cx - x = p
%cx = p + x
%x = cx - p
%cx + x = cx + cx - p
% = 2*cx - p

x_p = H\x_img';
x_coord = x_p(1)/x_p(3);
y_coord = x_p(2)/x_p(3);

figure
hold on
scatter3(x_coord, y_coord, 0, 'rd')
scatter3(X_world(1), X_world(2), X_world(3), "g*")
n = R*([0; 0; -1]);
quiver3(X_world(1), X_world(2), X_world(3), n(1), n(2), n(3), 3, 'b')
scatter3(0, 0, 0, 'bo')
hold off
xlabel('x')
ylabel('y')
zlabel('z')
axis([-10 10 -10 10 0 20])
%expect -3, -3
figure
hold on
scatter(x_coord, y_coord, 'rd')
scatter(0, 0, 'bo')
hold off
xlabel('x')
ylabel('y')
axis([-10 10 -10 10])



