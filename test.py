import numpy as np
from Harmony_Search import Harmony_Search

pit_range = (0.0, 9.0)
hms = 10
fw = 0.1
tol = 1.0e-05 
max_iter = 100000

def obj_fun(x):
    return np.abs(x - np.pi)

HS = Harmony_Search(pit_range, hms, fw, obj_fun, tol, max_iter, hmcr=0.9, par=0.3)
HS.Optimization()
HS.Optimized()
