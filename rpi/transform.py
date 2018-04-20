import numpy as np

# position calculation
# 
# Creates a rotation matrix from the three rotations and translations that the
# openMV board has generated from the april tags in its image. We place the
# in a coordinate system whos origin in the center of the april tag and whos
# axes are aligned with those of the april tag.
def pos(R, t):
    C_tilde = R*(-t)
    out = (C_tilde.item(0), C_tilde.item(1), C_tilde.item(2))
    return out

def make_R(rx, ry, rz):
    Rx = np.matrix([	[ 1         ,  0         ,  0         ],
                    	[ 0         ,  np.cos(rx),  np.sin(rx)],
                    	[ 0         , -np.sin(rx),  np.cos(rx)]	])


    Ry = np.matrix([	[ np.cos(ry),  0         , -np.sin(ry)],
                        [ 0         ,  1         ,  0         ],
                        [ np.sin(ry),  0         ,  np.cos(ry)]	])

    Rz = np.matrix([	[ np.cos(rz),  np.sin(rz),  0         ],
                        [-np.sin(rz),  np.cos(rz),  0         ],
                        [ 0         ,  0         ,  1         ]	])

    R = Rx*Ry*Rz

    return R

def make_t(tx, ty, tz):
    t = np.matrix([[tx], [ty], [tz]])
    return t

def player_pos(px, py, R, t):
    fx = (2.8/3.984)*160
    fy = (2.8/2.952)*120
    cx = 160/2
    cy = 120/2

    K = np.matrix([	[fx, 0, cx],
                    [0, fy, cy],
                    [0,  0,  1]])

    R_inv = R.transpose()

    RT = np.matrix([[R_inv.item((0,0)), R_inv.item((0,1)), t.item(0)],
                    [R_inv.item((1,0)), R_inv.item((1,1)), t.item(1)],
                    [R_inv.item((2,0)), R_inv.item((2,1)), t.item(2)]])

    H = K*RT

    x_img = np.matrix([[160 - px],
                       [py],
                       [1]])

    x_player = np.linalg.solve(H,x_img)

    x_coord = x_player.item(0)/x_player.item(2)
    y_coord = x_player.item(1)/x_player.item(2)

    return (x_coord, y_coord)
