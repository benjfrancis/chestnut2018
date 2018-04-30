import csv
import numpy as np
from Kalman import *
from math import pow

data = []

path = '/Users/BenFrancis/Dropbox/SeniorDesignData/raw_player-April-22-2018-1301.csv'

with open(path, 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        data.append(row)

xData = list(map(lambda x: float(x[0]), data))
yData = list(map(lambda x: float(x[1]), data))
xVar = np.var(xData)
yVar = np.var(yData)

print(xVar)
print(yVar)

sX = initKalman(xVar, pow(0.4, 2))
sY = initKalman(yVar, pow(0.4, 2))

zs = []
xs = []

for x in xData:
    sX = kalmanIter(sX, x)
    xs.append(sX.x)
    zs.append(x)

print(zs)

plt.scatter(range(len(zs)), zs, color="red", marker=".", linewidth=0.1)
plt.scatter(range(len(xs)), xs, color="green", marker=".", linewidth=0.1)

plt.show()
