import numpy as np
import random

class chromosome():

    def __init__(self, bin_str):
        self.bin_str = bin_str
        #self.bin_limit = bin_limit
        self.bin_len = len(bin_str)

    def bool_probability(self, probability):
        return (np.random.random() < probability)

    #def bool_outrange(self, bin_str):
        #return int(bin_str, 2) > int(self.bin_limit, 2)

    def random_int_list(self, lower, upper, num):
        out = random.sample(range(lower, upper), num)
        out.sort()
        return out

    def change_str_letter(self, string, ind, target):
        temp = list(string)
        temp[ind] = target
        return ''.join(temp)

    def mutate_single(self, ind):
        string = self.bin_str[ind]
        if string=='0':
            out = self.change_str_letter(self.bin_str, ind, '1')
        elif string=='1':
            out = self.change_str_letter(self.bin_str, ind, '0')
        if not self.bool_outrange(out):
            self.bin_str = out

    def mutate(self, prob, num=1):
        if self.bool_probability(prob):
            ind_mut = self.random_int_list(0, self.bin_len, num)
            for ind in ind_mut:
                self.mutate_single(ind)

    def division(self, break_points):
        out = list([])
        for i in range(len(break_points)+1):
            if i==0:
                out.append(self.bin_str[:break_points[i]])
            elif i == len(break_points):
                out.append(self.bin_str[break_points[i-1]:])
            else:
                out.append(self.bin_str[break_points[i-1]: break_points[i]])
        return np.array(out)

    def crossover(self, chrom1, chrom2, break_num):
        break_points = self.random_int_list(1, chrom1.bin_len, break_num)
        parts1 = chrom1.division(break_points)
        parts2 = chrom2.division(break_points)
        print(parts1)
        print(parts2)
        new_str1 = list([]) 
        new_str2 = list([]) 
        for i in range(len(parts1)):
            if i%2 == 0:
                new_str1.append(parts1[i])
                new_str2.append(parts2[i])
            else:
                new_str1.append(parts2[i])
                new_str2.append(parts1[i])
        new_str1 = ''.join(new_str1)
        new_str2 = ''.join(new_str2)
        return chromosome(new_str1), chromosome(new_str2)




class Genetic_Algorithm():

    def __init__(self, var_num, var_range, var_digit, population, obj_fun, mutation_prop=0.1):
        self.var_num = var_num
        self.var_range = var_range
        self.var_digit = var_digit
        self.population = population
        self.obj_fun = obj_fun
        self.mutation_prop = mutation_prop
        self.group = list([])
        self.fitness = np.array([])
        self.update()

    def update(self):
        self.cd = coder(self.var_num, self.var_range, self.var_digit)
        self.ini_group()

    def bool_probability(self, probability):
        return (np.random.random() < probability)

    def gen_rand_chrom(self):
        vector = np.zeros(self.var_num)
        for var_ind in range(self.var_num):
            vector[var_ind] = np.random.uniform(self.var_range[var_ind,0], self.var_range[var_ind,1])
        return chromosome(self.cd.encode(vector))

    def ini_group(self):
        for i in range(self.population):
            self.add(self.gen_rand_chrom())

    def update_sel_prop(self):
        sort_ind = self.fitness.argsort() + 1.0
        self.sel_prop = sort_ind / np.sum(sort_ind)

    def add(self, chrom):
        self.group.append(chrom)
        temp = self.cd.decode(chrom.bin_str)
        self.fitness = np.append(self.fitness, self.obj_fun(temp))
        self.update_sel_prop()

    def delete(self, ind):
        del self.group[ind]
        self.fitness = np.delete(self.fitness, ind)
        self.update_sel_prop()

class coder():

    def __init__(self, var_num, var_range, var_digit):
        self.var_num = var_num
        self.var_range = var_range
        self.var_digit = var_digit
        self.update()

    def update(self):
        self.int_range = np.zeros((self.var_num, 2), dtype=int)
        self.bin_limit = list([])
        self.bin_len = np.zeros(self.var_num, dtype=int)
        for i in range(self.var_num):
           temp = (self.var_range[i] - self.var_range[i,0]) * self.var_digit[i]
           self.int_range[i] = temp.astype(int)
           self.bin_limit.append('{0:b}'.format(self.int_range[i,1]))
           self.bin_len[i] = len(self.bin_limit[i])
        self.bin_limit = np.array(self.bin_limit)

    def dec2bin(self, var, var_ind):
        out = '{0:b}'.format(int((var - self.var_range[var_ind,0]) * self.var_digit[var_ind]))
        return out.zfill(self.bin_len[var_ind])

    def bin2dec(self, var_bin, var_ind):
        out = int(var_bin, 2)
        return out/self.var_digit[var_ind] + self.var_range[var_ind,0]
    
    def encode(self, vector):
        out = ''
        for var_ind in range(self.var_num):
            out += self.dec2bin(vector[var_ind], var_ind)
        return out

    def decode(self, bin_str):
        out = np.zeros(self.var_num)
        for var_ind in range(self.var_num):
            temp1 = np.sum(self.bin_len[:var_ind])
            temp2 = np.sum(self.bin_len[:var_ind+1])
            temp_bin = bin_str[temp1:temp2]
            out[var_ind] = self.bin2dec(temp_bin, var_ind)
        return out

