import numpy as np
from Harmony_Search import Harmony_Search

pit_range = (0.0, 9.0)
hms = 10
fw = 0.5
tol = 1.0e-05 
max_iter = 100

def obj_fun(x):
    return x - np.pi

HS = Harmony_Search(pit_range, hms, fw, obj_fun, tol, max_iter, hmcr=0.9, par=0.3)
print(HS.bool_probability(0.5))

