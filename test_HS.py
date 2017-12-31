import numpy as np
import matplotlib.pyplot as plt
from Harmony_Search import Harmony_Search

pit_range = np.array([
    [0.0, 100.0],
    [0.0, 100.0],
    [0.0, 100.0],
    [0.0, 100.0],
    ])
hms = 100
fw_ratio = np.array([0.01, 0.01, 0.01, 0.01])
hmcr = np.array([0.9, 0.9, 0.9, 0.9])
par = np.array([0.1, 0.1, 0.1, 0.1])
tol = 1.0e-03
max_iter = 5000

def obj_fun(vector):
    x, y, m, n = vector
    f = (x-3.0)**2 + (y-20.0)**2 + (m-98.0)**2 + (n-68.0)**2
    return -1.0 * f

fitness = np.array([])
vector = np.zeros((1,len(pit_range)))

HS = Harmony_Search(pit_range, hms, obj_fun)
for i in range(max_iter):
    HS.next()
    vector_max, fitness_max = HS.Optimized()
    fitness = np.append(fitness, fitness_max)
    vector = np.vstack((vector, vector_max))
    if i == 0:
        vector = vector[1:]
    if fitness_max >= -tol:
        break


ind = fitness.argmax()
print(vector[ind])
#plt.plot(fitness)
#plt.show()
