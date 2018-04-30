import numpy as np
from copy import deepcopy
from math import pow
import matplotlib.pyplot as plt
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

def kalman(s_orig):
    s = deepcopy(s_orig)
    if not hasattr(s, 'z'):
        print("Observation vector missing")
        return None
    if not hasattr(s, 'x'):
        # s.x = float('nan')*s.z
        # try this
        s.x = float('nan')
    if not hasattr(s, 'P'):
        s.P = float('nan')
    if not hasattr(s, 'u'):
        s.u = 0
    if not hasattr(s, 'A'):
        s.A = np.identity(len(s.x))
    if not hasattr(s, 'B'):
        s.B = 0
    if not hasattr(s, 'Q'):
        s.Q = np.zeros(len(s.x), len(s.x))
    if not hasattr(s, 'R'):
        print("Observation covariance mssing")
        return None
    if not hasattr(s, 'H'):
        s.H = identity(len(s.x))

    if np.isnan(s.x): # probably won't work
        # initialize state estimate from first observation
        if not s.H.shape[0] == s.H.shape[1]:
            print("Observation matrix must be square and invertible for stable autolocalization")
        s.x = np.linalg.inv(s.H)*s.z
        s.P = np.linalg.inv(s.H)*s.R*np.linalg.inv(np.transpose(s.H))
    else:
    # prediction for state vector and covariance
        s.x = s.A*s.x + s.B*s.u
        s.P = s.A * s.P * np.transpose(s.A) + s.Q

        # compute Kalman gain factor
        K  = s.P*(np.transpose(s.H))*np.linalg.inv(s.H*s.P*np.transpose(s.H)+s.R)


        # correction based on observation
        s.x = s.x + K*(s.z-s.H*s.x)
        s.P = s.P - K*s.H*s.P

    return s


def initKalman(var, Q):
    s = S()
    s.A = np.array([[1]])
    s.Q = np.array([[Q]])
    s.H = np.array([[1]])
    s.R = np.array([[var]])
    s.B = np.array([[0]])
    s.u = np.array([[0]])
    s.x = np.array([[float('nan')]])
    s.P = np.array([[float('nan')]])
    return s

def runKalman(data):
    mean = np.mean(data)
    var = np.var(data)

    sArr = []
    s = initKalman(var, pow(0.4, 2))
    sArr.append(s)

    tru = []
    for t in range(len(data)):
        tru.append(mean)
        sArr[-1].z = data[t]
        sArr.append(kalman(sArr[-1]))
    # measurement
    zs = list(map(lambda x: x.z, sArr[1:-2]))
    # kalman output
    xs = list(map(lambda x: x.x, sArr[2:]))

    return tru, zs, xs

    # plt.plot(range(len(tru)), tru, color="blue", linewidth=1.0, linestyle="-")
    # plt.scatter(range(len(zs)), zs, color="red", marker=".", linewidth=0.1)
    # plt.scatter(range(len(xs)), xs, color="green", marker=".", linewidth=0.1)
    # plt.title(title)
    #
    # plt.show()

def kalmanIter(s, point):
    s.z = point
    newS = kalman(s)
    return newS
