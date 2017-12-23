import numpy as np

class Harmony_Search():
    #For instruments with continous range
    #Input parameters
    #pit_range: range of the instrument - 
    #hms: Harmonic Memory Size - an int
    #hmcr: Harmonic Memory Conisdering Rate - 
    #par: Pitch Adjusting Rate - 
    #fw: Fret Width
    #obj_fun: Objective Function
    #tol: Tolerance
    #max_iter: Maximum Iteration Number - an int

    def __init__(self, pit_range, hms, fw, obj_fun, tol, max_iter, hmcr=0.9, par=0.3):
        self.pit_range = pit_range
        self.hms = hms
        self.fw = fw
        self.obj_fun = obj_fun
        self.tol = tol
        self.max_iter = max_iter
        self.hmcr = hmcr
        self.par = par
        
        self.generate_HM()

    def random_pitch(self, pit_range):
        return np.random.uniform(pit_range[0], pit_range[1])

    def generate_HM(self):
        self.HM = np.zeros((self.hms,1))
        self.HM_f = np.zeros(self.hms)
        for i in range(self.hms):
            self.HM[i,0] = self.random_pitch(self.pit_range)
            self.HM_f[i] = self.obj_fun(self.HM[i])
        return 0

    def bool_probability(self, probability):
        return (np.random.random() < probability)
