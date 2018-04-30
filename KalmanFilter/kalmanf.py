import numpy as np
from copy import deepcopy


def kalmanf(s_orig):
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
