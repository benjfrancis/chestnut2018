import serial
import csv
import numpy as np
import transform as tf
import datetime
import json
import requests
import sys
sys.path.insert(0, '../KalmanFilter/')
from Kalman import *
from time import sleep

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

HEIGHT = 7
WIDTH = 4

offsets = [[0, HEIGHT],[WIDTH,HEIGHT],[0,0],[WIDTH,0]]

# taken from a dataset of small field - will likely have to change
xVar = 247.486260975
yVar = 805.731984567

# left as per connor's suggestion
xQ = pow(0.4, 2)
yQ = pow(0.4, 2)

sX = initKalman(xVar, xQ)
sY = initKalman(yVar, yQ)

MOVEMENT_THRESH = 2

pos_buffer = []
i = 0

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

	R = tf.make_R(rx, ry, rz)
	t = tf.make_t(tx, ty, tz)
	position = tf.pos(R,t)
	plr_pos = tf.player_pos(player_x,player_y,R,t)

	#print(position)
	#print(plr_pos)
	if(0 <= tag_id <= 3):
		plr_x = plr_pos[0] + offsets[tag_id][0]
		plr_y = plr_pos[1] + offsets[tag_id][1]

	#data = {'x': str(plr_pos[0]), 'y': str(plr_pos[1])}
	data = {'x': str(plr_x), 'y': str(plr_y), 'color': '0'}
	j = json.dumps(data)
	resp = requests.post('http://silklab.fctn.io:1234/push', data=j)

	if(plr_x <= pos_buff[0][i-1] - MOVEMENT_THRESH || plr_x >= pos_buff[0][i-1] + MOVEMENT_THRESH):
		plr_x = pos_buff[0][i-1]

	if(plr_y <= pos_buff[1][i-1] - MOVEMENT_THRESH || plr_y >= pos_buff[1][i-1] + MOVEMENT_THRESH):
		plr_y = pos_buff[0][i-1]

	sX = kalmanIter(sX, plr_x)
	sY = kalmanIter(sY, plr_y)
	print(sX.x[0][0])
	print(sY.x[0][0])

	pos_buff[0][i] = sX.x[0][0]
	pos_buff[1][i] = sY.x[0][0]

	data = {'x': str(sX.x[0][0]), 'y': str(sY.x[0][0]), 'color': '1'}
	j = json.dumps(data)
	resp = requests.post('http://silklab.fctn.io:1234/push', data=j)

	i = (i+1)%N

	#sleep(0.01)






# date_str = datetime.datetime.now().strftime("%B-%d-%Y-%H%M")

# with open('/Users/ashtonknight/Dropbox/SeniorDesignData/raw_player-{}.csv'.format(date_str), 'w') as out_file:
# 	writer = csv.writer(out_file)
# 	writer.writerows(raw_player)

# with open('/Users/ashtonknight/Dropbox/SeniorDesignData/raw_tags-{}.csv'.format(date_str), 'w') as out_file:
# 	writer = csv.writer(out_file)
# 	writer.writerows(raw_tags)
