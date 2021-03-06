import numpy as np
import matplotlib.pyplot as plt
from Genetic_Algorithm import chromosome, Genetic_Algorithm

var_num = 4
var_range = np.array([
    [0.0, 100.0],
    [0.0, 100.0],
    [0.0, 100.0],
    [0.0, 100.0],
    ])
var_digit = [1000, 1000, 1000, 1000]
population = 100
mutation_prop = 0.1
#fw_ratio = np.array([0.01, 0.01, 0.01, 0.01])
#hmcr = np.array([0.9, 0.9, 0.9, 0.9])
#par = np.array([0.1, 0.1, 0.1, 0.1])
tol = 1.0e-03 
max_iter = 5000

def obj_fun(vector):
    x, y, m, n = vector
    f = (x-3.0)**2 + (y-20.0)**2 + (m-98.0)**2 + (n-68.0)**2
    return -1.0 * f

GA = Genetic_Algorithm(var_range, var_digit, population, obj_fun, cross_num=1, sel_por=0.3, mutation_prop=0.1)
fitness = np.array([])
vector = np.zeros((1,var_num))
for i in range(max_iter):
    GA.evolve()
    vector_max, fitness_max = GA.Optimized()
    fitness = np.append(fitness, fitness_max)
    vector = np.vstack((vector, vector_max))
    if i == 0:
        vector = vector[1:]
    if fitness_max >= -tol:
        break

ind = fitness.argmax()
print(vector[ind])
'''
a = chromosome(np.array([12.0, 15.0,4.0,90.0]),var_range, var_digit)
b = chromosome(np.array([80.0, 2.0, 54.0,27.0]),var_range, var_digit)
m, n = a.crossover(a,b,2)
'''
#plt.plot(fitness)
#plt.show()
