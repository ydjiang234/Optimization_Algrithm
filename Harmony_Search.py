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

    def bool_probability(self, probability):
        return (np.random.random() < probability)

    def random_pitch(self, pit_range):
        return np.random.uniform(pit_range[0], pit_range[1])

    def random_harmony_vector(self):
        return np.array([self.random_pitch(self.pit_range)])

    def random_pit_from_list(self, target_list):
        ind = int(len(target_list) * np.random.random());
        return target_list[ind]

    def new_harmony_vector(self):
        if self.bool_probability(self.hmcr):
            new_pit = np.array([self.random_pit_from_list(self.HM[:,0])])
            if self.bool_probability(self.par):
                new_pit = new_pit + self.fw * np.random.uniform(-1.0, 1.0)
        else:
            new_pit = self.random_pitch(self.pit_range)

        return np.array([new_pit])

    def generate_HM(self):
        self.HM_f = np.zeros(self.hms)
        for i in range(self.hms):
            if i == 0:
                self.HM = self.random_harmony_vector()
            else:
                self.HM = np.vstack((self.HM, self.random_harmony_vector()))
            self.HM_f[i] = self.obj_fun(self.HM[i])
        return 0

    def update_HM(self, harmony_vector):
        new_vector = harmony_vector
        new_f = self.obj_fun(new_vector)
        ind_max = self.HM_f.argmax()
        HM_f_max = self.HM_f[ind_max]
        if new_f < HM_f_max:
            self.HM_f[ind_max] = new_f
            self.HM[ind_max] = new_vector

    def Optimized(self):
        ind_min = self.HM_f.argmin()
        HM_f_min = self.HM_f[ind_min]
        HM_min = self.HM[ind_min]
        return HM_min, HM_f_min

    def Optimization(self):
        for i in range(self.max_iter):
            self.update_HM(self.new_harmony_vector())
            print(self.Optimized())
            
