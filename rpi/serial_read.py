import serial
import numpy as np
import csv

# position calculation
# 
# Creates a rotation matrix from the three rotations and translations that the
# openMV board has generated from the april tags in its image. We place the
# in a coordinate system whos origin in the center of the april tag and whos
# axes are aligned with those of the april tag.
def pos(tx, ty, tz, rx, ry, rz):
	Rx = np.matrix([	[ 1         ,  0         ,  0         ],
						[ 0         ,  np.cos(rx), -np.sin(rx)],
						[ 0         ,  np.sin(rx),  np.cos(rx)]	])


	Ry = np.matrix([	[ np.cos(ry),  0         ,  np.sin(ry)],
						[ 0         ,  1         ,  0         ],
						[-np.sin(ry),  0         ,  np.cos(ry)]	])

	Rz = np.matrix([	[ np.cos(rz), -np.sin(rz),  0         ],
						[ np.sin(rz),  np.cos(rz),  0         ],
						[ 0         ,  0         ,  1         ]	])

	R = Rx*Ry*Rz

	t = np.matrix([[tx], [ty], [tz]])
	# X = [t[0], t[1], t[2], 1]

	# A = np.matrix([	[R.item(0,0), R.item(0,1), R.item(0,2), X[0]],
	# 				[R.item(1,0), R.item(1,1), R.item(1,2), X[1]],
	# 				[R.item(2,0), R.item(2,1), R.item(2,2), X[2]],
	# 				[0          , 0          , 0          , X[3]]])

	# X_cam = np.matrix([[0],
	# 					[0],
	# 					[0],
	# 					[1]])

	# X_world = np.linalg.solve(-A, X_cam)
	C_tilde = R*(t)
	out = (C_tilde.item(0), C_tilde.item(1), C_tilde.item(2))
	return out

# Read the april tag data from the serial input for N data points
cam = serial.Serial("/dev/cu.usbmodem1411", 115200)
N = 2000; #for now total samples of tags+players, feel free to change this to somehting more precise
i = 0;
raw_tags = [];
raw_player = [];
collected_data = [];
while(i < N):
	byte = cam.readline()
	s = byte.decode("utf-8")
	l = [elem.strip() for elem in s.split(',')]
	msg_id = l(0)
	l = l(1:)
	if(msg_id == 'tag'):
		l = [float(elem) for elem in l]
		l[0] = int(l[0])
		tag_id = l[0]
		tx = l[1]
		ty = l[2]
		tz = l[3]
		rx = l[4]
		ry = l[5]
		time = l[6]
		raw_tags.append(l)
		#position = pos(tx, ty, tz, rx, ry, rz)
		collected_data.append(list(position))

		i += 1
	elif(msg_id == 'player'):
		l = [int(elem) for elem in l]
		player_x = l[0]
		player_y = l[1]
		time = l[6]
		raw_player.append(l)

		i += 1

# Write collected data to a csv file
# with open('position_data.csv', 'w') as out_file:
# 	writer = csv.writer(out_file)
# 	writer.writerows(collected_data)

with open('raw_player.csv', 'w') as out_file:
	writer = csv.writer(out_file)
	writer.writerows(raw_player)

with open('raw_tags.csv', 'w') as out_file:
	writer = csv.writer(out_file)
	writer.writerows(raw_tags)