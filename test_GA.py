import numpy as np
from Genetic_Algorithm import chromosome, Genetic_Algorithm

var_num = 2
var_range = np.array([
    [0.0, 100.0],
    [0.0, 100.0],
    ])
var_digit = [1000, 1000]
population = 10
mutation_prop = 0.1

#fw_ratio = np.array([0.01, 0.01, 0.01, 0.01])
#hmcr = np.array([0.9, 0.9, 0.9, 0.9])
#par = np.array([0.1, 0.1, 0.1, 0.1])
tol = 1.0e-03 
max_iter = 500

def obj_fun(vector):
    x, y = vector
    f = (x-3.0)**2 + (y-6.0)**2
    return f

GA = Genetic_Algorithm(var_num, var_range, var_digit, population, obj_fun)
