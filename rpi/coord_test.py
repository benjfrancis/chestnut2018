import numpy as np
import transform as tf

player_x = 80 + 10
player_y = 60

tx       = 5
ty       = 4
tz       = -10
rx       = np.pi/4
ry       = -np.pi/8
rz       = np.pi/4

R = tf.make_R(rx, ry, rz)
print(R)
t = tf.make_t(tx, ty, tz)
position = tf.pos(R,t)
plr_pos = tf.player_pos(player_x,player_y,R,t)

print(t)
print('drone pos:')
print(position)
print('player:')
print(plr_pos)