import numpy as np
from Harmony_Search import Harmony_Search

ins_num = 3
pit_range = np.array([
    [0.0, 100.0],
    [0.0, 100.0],
    [0.0, 100.0],
    ])
hms = 10000
#fw_ratio = np.array([0.01, 0.01, 0.01, 0.01])
#hmcr = np.array([0.9, 0.9, 0.9, 0.9])
#par = np.array([0.1, 0.1, 0.1, 0.1])
tol = 1.0e-03 
max_iter = 500000

def obj_fun(vector):
    x, y, z = vector
    f = (x-3.0)**2 + (y-6.0)**2 + (z-88.0)**2
    return f

HS = Harmony_Search(ins_num, pit_range, hms, obj_fun, tol, max_iter)
HS.Optimization()
HS.Optimized()
