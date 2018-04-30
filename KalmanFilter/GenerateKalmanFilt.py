import numpy as np
from math import pow
import matplotlib.pyplot as plt
from kalmanf import *
from functools import reduce

class S:
    def __init__(self):
        self.A = np.array([[0]])
        self.Q = np.array([[0]])
        self.H = np.array([[0]])
        self.R = np.array([[0]])
        self.B = np.array([[0]])
        self.u = np.array([[0]])
        self.x = np.array([[0]])
        self.P = np.array([[0]])

def GenerateKalmanFilt(data, mean, var):
    sArr = []
    s = S()
    s.A = np.array([[1]])
    s.Q = np.array([[pow(0.4,2)]])
    s.H = np.array([[1]])
    s.R = np.array([[var]])
    s.B = np.array([[0]])
    s.u = np.array([[0]])
    s.x = np.array([[float('nan')]])
    s.P = np.array([[float('nan')]])
    sArr.append(s)

    tru = []
    for t in range(len(data)):
        tru.append(mean)
        sArr[-1].z = data[t]
        sArr.append(kalmanf(sArr[-1]))

    zs = list(map(lambda x: x.z, sArr[1:-2]))
    xs = list(map(lambda x: x.x, sArr[2:]))

    plt.plot(range(len(tru)), tru, color="blue", linewidth=1.0, linestyle="-")
    plt.scatter(range(len(zs)), zs, color="red", marker=".", linewidth=0.1)
    plt.scatter(range(len(xs)), xs, color="green", marker=".", linewidth=0.1)


    plt.show()
