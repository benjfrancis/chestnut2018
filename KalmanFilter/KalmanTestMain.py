import csv
import numpy as np
from GenerateKalmanFilt import *

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


print(xData)
GenerateKalmanFilt(xData, xAvg, xVar)
