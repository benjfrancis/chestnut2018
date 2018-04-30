import csv
import numpy as np
from Kalman import runKalman
import matplotlib.pyplot as plt

data = []

path = '/Users/BenFrancis/Dropbox/SeniorDesignData/raw_player-April-22-2018-1301.csv'

with open(path, 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        data.append(row)

xData = list(map(lambda x: float(x[0]), data))
yData = list(map(lambda x: float(x[1]), data))


xAvg = np.mean(xData)
xVar = np.var(xData)
xStd = np.std(xData)

yAvg = np.mean(yData)
yVar = np.var(yData)
yStd = np.std(yData)


for i in range(11, len(xData)):
    if xData[i] >= xAvg + xStd or xData[i] <= xAvg - xStd:
        xData[i] = xData[i-1]
    if yData[i] >= yAvg + yStd or yData[i] <= yAvg - yStd:
        yData[i] = yData[i-1]


truX, measureX, outputX = runKalman(xData)
truY, measureY, outputY = runKalman(yData)


fX = plt.figure(1)
plt.plot(range(len(truX)), truX, color="blue", linewidth=1.0, linestyle="-")
plt.scatter(range(len(measureX)), measureX, color="red", marker=".", linewidth=0.1)
plt.scatter(range(len(outputX)), outputX, color="green", marker=".", linewidth=0.1)
plt.title("x data")
fX.show()

fY = plt.figure(2)
plt.plot(range(len(truY)), truY, color="blue", linewidth=1.0, linestyle="-")
plt.scatter(range(len(measureY)), measureY, color="red", marker=".", linewidth=0.1)
plt.scatter(range(len(outputY)), outputY, color="green", marker=".", linewidth=0.1)
plt.title("y data")
fY.show()

input()
