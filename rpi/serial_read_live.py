import serial
import csv
import numpy as np
import datetime
import json
import requests


def pos(R, t):
    C_tilde = R*(-t)
    out = (C_tilde.item(0), C_tilde.item(1), C_tilde.item(2))
    return out

def make_R(rx, ry, rz):
    Rx = np.matrix([[ 1         ,  0         ,  0         ],
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

    R_inv = np.linalg.inv(R)

    RT = np.matrix([[R_inv.item((0,0)), R_inv.item((1,0)), t.item(0)],
                    [R_inv.item((0,1)), R_inv.item((1,1)), t.item(1)],
                    [R_inv.item((0,2)), R_inv.item((1,2)), t.item(2)]])

    H = K*RT

    x_img = np.matrix([[160 - px],
                       [py],
                       [1]])

    x_player = np.linalg.solve(H,x_img)

    x_coord = x_player.item(0)/x_player.item(2)
    y_coord = x_player.item(1)/x_player.item(2)

    return (x_coord, y_coord)

def msg_decode(line):

	l = [elem.strip() for elem in line.split(',')]

	l[0] = int(l[0])
	l[1] = int(l[1])
	l[2] = int(l[2])
	l[3] = int(l[3])
	l[4] = float(l[4])
	l[5] = float(l[5])
	l[6] = float(l[6])
	l[7] = float(l[7])
	l[8] = float(l[8])
	l[9] = float(l[9])
	l[10] = int(l[10])

	return l

cam = serial.Serial("/dev/cu.usbmodem1411", 115200)
N = 1000 #for now total samples of tags+players, feel free to change this to somehting more precise
i = 0
raw_tags = []
raw_player = []
error = 0

while(i < N):
	byte = cam.readline()
	s = byte.decode("ascii")
	s = s.replace("\n","")
	s = s.replace("\r","")
	if (s == ""):
		continue

	try:
		l = msg_decode(s)
	except:
		error += 1
		continue

	
	player_x 	= l[0]
	player_y 	= l[1]
	player_age 	= l[2]
	tag_id 		= l[3]
	tx 			= l[4]
	ty 			= l[5]
	tz 			= l[6]
	rx 			= l[7] - np.pi
	ry 			= l[8]
	rz 			= -l[9]
	tag_age 	= l[10]

	R = make_R(rx, ry, rz)
	t = make_t(tx, ty, tz)
	position = pos(R,t)
	plr_pos = player_pos(player_x,player_y,R,t)

	#print(position)
	print(plr_pos)
	data = {'x': str(plr_pos[0]), 'y': str(plr_pos[1])}
	j = json.dumps(data)
	resp = requests.post('http://silklab.fctn.io:1234/push', data=j)




# date_str = datetime.datetime.now().strftime("%B-%d-%Y-%H%M")

# with open('/Users/ashtonknight/Dropbox/SeniorDesignData/raw_player-{}.csv'.format(date_str), 'w') as out_file:
# 	writer = csv.writer(out_file)
# 	writer.writerows(raw_player)

# with open('/Users/ashtonknight/Dropbox/SeniorDesignData/raw_tags-{}.csv'.format(date_str), 'w') as out_file:
# 	writer = csv.writer(out_file)
# 	writer.writerows(raw_tags)