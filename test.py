import numpy as np
from Harmony_Search import Harmony_Search

ins_num = 4
pit_range = np.array([
    [0.0, 100.0],
    [0.0, 100.0],
    [0.0, 100.0],
    [0.0, 100.0],
    ])
hms = 10000
fw = np.array([1.0, 1.0, 1.0, 1.0])
tol = 1.0e-05 
max_iter = 500000

def obj_fun(vector):
    x, y, z, k = vector
    f = (x-3.0)**2 + (y-6.0)**2 + (z-88.0)**2 + (k - 50.0)**2
    return f

HS = Harmony_Search(ins_num, pit_range, hms, fw, obj_fun, tol, max_iter, hmcr=0.9, par=0.3)
HS.Optimization()
HS.Optimized()
