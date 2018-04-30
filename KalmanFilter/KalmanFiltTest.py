import numpy as np
from math import pow

class S:
    def __init__(self):
        self.A = 0
        self.Q = 0
        self.H = 0
        self.R = 0
        self.B = 0
        self.u = 0
        self.x = 0
        self.P = 0

def KalmanFiltTest(data, mean, var):
    sArr = []
    s = S()
    s.A = 1
    s.Q = pow(0.4, 2)
    s.H = 1
    s.R = var
    s.B = 0
    s.u = 0
    s.x = float('nan')
    s.P = float('nan')
    sArr.append(s)

    tru = []
    for t in range(len(data)):
        tru.append(mean)
        sArr[end].z = data[t]
        sArr.append(kalmanf(s[end]))
