import numpy as np
import transform as tf

player_x = 80 + 10
player_y = 60

tx       = 0
ty       = 0
tz       = -10
rx       = 0
ry       = 0
rz       = np.pi/4

R = tf.make_R(rx, ry, rz)
print(R)
t = tf.make_t(tx, ty, tz)
position = tf.pos(R,t)
plr_pos = tf.player_pos(player_x,player_y,R,t)

print(t)
print(position)
print(plr_pos)