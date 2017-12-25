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

    def __init__(self, ins_num, pit_range, hms, obj_fun, tol, max_iter, hmcr=0.9, par=0.3, fw_ratio=0.01):
        self.ins_num = ins_num
        self.pit_range = pit_range
        self.hms = hms
        self.fw_ratio = fw_ratio
        self.obj_fun = obj_fun
        self.tol = tol
        self.max_iter = max_iter
        self.hmcr = hmcr
        self.par = par
       
        self.covert_default()
        self.generate_HM()

    def covert_default(self):
        if type(self.hmcr) != type(np.array([1,2])):
            self.hmcr = np.ones(self.ins_num) * self.hmcr
        if type(self.par) != type(np.array([1,2])):
            self.par = np.ones(self.ins_num) * self.par
        self.fw = self.fw_ratio * (self.pit_range[:,1] - self.pit_range[:,0])


    def bool_probability(self, probability):
        return (np.random.random() < probability)

    def random_pit_from_list(self, target_list):
        ind = int(len(target_list) * np.random.random());
        return target_list[ind]

    def select_pitch(self, ins_ind):
        if self.bool_probability(self.hmcr[ins_ind]):
            new_pit = self.random_pit_from_list(self.HM[:,ins_ind])
            if self.bool_probability(self.par[ins_ind]):
                new_pit = new_pit + self.fw[ins_ind] * np.random.uniform(-1.0, 1.0)
        else:
            new_pit = np.random.uniform(self.pit_range[ins_ind,0], self.pit_range[ins_ind,1])
        return new_pit

    def new_harmony_vector(self):
        new_vector = np.zeros(self.ins_num)
        for ins_ind in range(self.ins_num):
            new_vector[ins_ind] = self.select_pitch(ins_ind)
        return new_vector

    def generate_HM(self):
        self.HM = np.zeros((self.hms, self.ins_num))
        self.HM_f = np.zeros(self.hms)
        for i in range(self.hms):
            for ins_ind in range(self.ins_num):
                self.HM[i, ins_ind] = np.random.uniform(self.pit_range[ins_ind,0], self.pit_range[ins_ind,1])
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
            HM_min, HM_f_min = self.Optimized()
            print(HM_min, HM_f_min)
            if HM_f_min <= self.tol:
                break
            
