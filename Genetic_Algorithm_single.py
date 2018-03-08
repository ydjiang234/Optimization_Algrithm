import numpy as np
import copy
import random
import threading

class Genetic_Algorithm():

    def __init__(self, var_range, var_digit, population, obj_fun, sel_por=0.4, cross_num=1, mutation_prop=0.1, mutation_num=1):
        self.var_num = len(var_digit)
        self.var_range = var_range
        self.var_digit = var_digit
        self.population = population
        self.obj_fun = obj_fun
        self.sel_por = sel_por
        self.cross_num = cross_num
        self.mutation_prop = mutation_prop
        self.mutation_num = mutation_num
        self.group = list([])
        self.fitness = np.array([])
        self.update()

    def update(self):
        self.ini_group()

    def bool_probability(self, probability):
        return (np.random.random() < probability)

    def gen_rand_chrom(self):
        vector = np.zeros(self.var_num)
        for var_ind in range(self.var_num):
            vector[var_ind] = np.random.uniform(self.var_range[var_ind,0], self.var_range[var_ind,1])
        return chromosome(vector, self.var_range, self.var_digit)

    def ini_group(self):
        for i in range(self.population):
            self.add(self.gen_rand_chrom())

    def update_sel_prop(self):
        sort_ind = np.argsort(self.fitness)
        self.sel_prop = np.zeros(len(sort_ind))
        for i in range(len(sort_ind)):
            self.sel_prop[sort_ind[i]] = (i + 1.0) / len(sort_ind)

    def add(self, chrom):
        self.group.append(chrom)
        self.fitness = np.append(self.fitness, self.obj_fun(chrom.vector))
        self.update_sel_prop()

    def delete(self, ind_list):
        temp_group = self.group
        self.group = list([])
        self.fitness = np.array([])
        for i in range(len(temp_group)):
            if i not in ind_list:
                self.add(temp_group[i])

    def select(self):
        sel_num = int(self.population * self.sel_por * 2)
        sel_ind = list([])
        cur_ind = 0
        while (len(sel_ind) < sel_num):
            if cur_ind not in sel_ind:
                if self.bool_probability(self.sel_prop[cur_ind]):
                    sel_ind.append(cur_ind)

            cur_ind += 1
            if cur_ind == self.population:
                cur_ind = 0
        return np.array(sel_ind)

    def eliminate(self):
        cur_ind = 0
        del_ind = list([])
        del_num = len(self.group) - self.population
        while (len(del_ind) < del_num):
            if cur_ind not in del_ind:
                if not self.bool_probability(self.sel_prop[cur_ind]):
                    max_ind = self.fitness.argmax()
                    #if max_ind == cur_ind:
                        #print(self.sel_prop[cur_ind])
                    del_ind.append(cur_ind)

            cur_ind += 1
            if cur_ind == len(self.group):
                cur_ind = 0
        self.delete(del_ind)

    def cross(self, cross_ind):
        fa_ind, ma_ind = np.split(cross_ind, 2)
        for i in range(len(fa_ind)):
            fa = self.group[fa_ind[i]]
            ma = self.group[ma_ind[i]]
            chrom1, chrom2 = fa.crossover(fa, ma, self.cross_num)
            chrom1.mutate(self.mutation_prop, self.mutation_num)
            chrom2.mutate(self.mutation_prop, self.mutation_num)
            self.add(chrom1)
            self.add(chrom2)
        
    def evolve(self):
        cross_ind = self.select()
        self.cross(cross_ind)
        a = max(self.fitness)
        self.eliminate()
        b = max(self.fitness)
        if a > b:
            print('error')

    def Optimized(self):
        ind_max = self.fitness.argmax()
        fitness_max = self.fitness[ind_max]
        vector = self.group[ind_max].vector
        return vector, fitness_max


class chromosome():

    def __init__(self, vector, var_range, var_digit):
        self.vector = vector
        self.var_num = self.vector.size
        self.var_range = var_range
        self.var_digit = var_digit
        self.update_gene_info()
        self.encode()

    def copy(self):
        new_chrom = chromosome(np.copy(self.vector), np.copy(self.var_range), np.copy(self.var_digit))
        return new_chrom

    def update_gene_info(self):
        self.int_range = np.zeros((self.var_num, 2), dtype=int)
        self.bin_limit = list([])
        self.bin_len = np.zeros(self.var_num, dtype=int)
        for i in range(self.var_num):
           temp = (self.var_range[i] - self.var_range[i,0]) * self.var_digit[i]
           self.int_range[i] = temp.astype(int)
           self.bin_limit.append('{0:b}'.format(self.int_range[i,1]))
           self.bin_len[i] = len(self.bin_limit[i])
        self.bin_limit = np.array(self.bin_limit)

    def random_int_list(self, lower, upper, num):
        out = random.sample(range(lower, upper), num)
        out.sort()
        return out

    def dec2bin(self, var, var_ind):
        out = '{0:b}'.format(int((var - self.var_range[var_ind,0]) * self.var_digit[var_ind]))
        return out.zfill(self.bin_len[var_ind])

    def bin2dec(self, var_bin, var_ind):
        out = int(var_bin, 2)
        return out/self.var_digit[var_ind] + self.var_range[var_ind,0]
    
    def encode(self):
        self.gene_group = list([])
        for var_ind in range(self.var_num):
            temp_str = self.dec2bin(self.vector[var_ind], var_ind)
            temp_gene = gene(temp_str, self.bin_limit[var_ind])
            self.gene_group.append(temp_gene)

    def decode(self):
        for var_ind in range(self.var_num):
            temp_gene = self.gene_group[var_ind]
            self.vector[var_ind] = self.bin2dec(temp_gene.bin_str, var_ind)

    def crossover(self, chrom1, chrom2, break_num):
        new_chrom1 = chrom1.copy()
        new_chrom2 = chrom2.copy()
        if self.var_num != 1:
            break_points = self.random_int_list(1, chrom1.var_num, break_num)
            i = 0
            while i < (len(break_points) - 1):
                for j in range(break_points[i], break_points[i+1]):
                    new_chrom1.gene_group[j] = chrom2.gene_group[j]
                    new_chrom2.gene_group[j] = chrom1.gene_group[j]
                i += 2
            if i == (len(break_points) - 1):
                for j in range(break_points[i], self.var_num):
                    new_chrom1.gene_group[j] = chrom2.gene_group[j]
                    new_chrom2.gene_group[j] = chrom1.gene_group[j]
            new_chrom1.decode()
            new_chrom2.decode()
        return new_chrom1, new_chrom2

    def mutate(self, mutation_prop, num=1):
        for var_ind in range(self.var_num):
            self.gene_group[var_ind].mutate(mutation_prop, num)
        self.decode()

class gene():

    def __init__(self, bin_str, bin_limit):
        self.bin_str = bin_str
        self.bin_limit = bin_limit
        self.bin_len = len(bin_str)

    def bool_probability(self, probability):
        return (np.random.random() < probability)

    def bool_outrange(self, bin_str):
        return int(bin_str, 2) > int(self.bin_limit, 2)

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
        num = np.random.randint(low=0, high=self.bin_len)
        if self.bool_probability(prob):
            ind_mut = self.random_int_list(0, self.bin_len, num)
            for ind in ind_mut:
                self.mutate_single(ind)


'''
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
        #if not self.bool_outrange(out):
        self.bin_str = out

    def mutate(self, prob):
        num = np.random.randint(low=0, high=self.bin_len)
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

    def __init__(self, var_num, var_range, var_digit, population, obj_fun, sel_por=0.4, mutation_prop=0.1, cross_num=1):
        self.var_num = var_num
        self.var_range = var_range
        self.var_digit = var_digit
        self.population = population
        self.obj_fun = obj_fun
        self.sel_por = sel_por
        self.mutation_prop = mutation_prop
        self.cross_num = cross_num
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
        self.sel_prop = sort_ind / len(sort_ind)

    def add(self, chrom):
        self.group.append(chrom)
        temp = self.cd.decode(chrom.bin_str)
        self.fitness = np.append(self.fitness, self.obj_fun(temp))
        self.update_sel_prop()

    def delete(self, ind_list):
        temp_group = self.group
        self.group = list([])
        self.fitness = np.array([])
        for i in range(len(temp_group)):
            if i not in ind_list:
                self.add(temp_group[i])
        self.update_sel_prop()

    def select(self):
        sel_num = int(self.population * self.sel_por * 2)
        sel_ind = list([])
        cur_ind = 0
        while (len(sel_ind) < sel_num):
            if cur_ind not in sel_ind:
                if self.bool_probability(self.sel_prop[cur_ind]):
                    sel_ind.append(cur_ind)

            cur_ind += 1
            if cur_ind == self.population:
                cur_ind = 0
        return np.array(sel_ind)

    def eliminate(self):
        cur_ind = 0
        del_ind = list([])
        del_num = len(self.group) - self.population
        while (len(del_ind) < del_num):
            if cur_ind not in del_ind:
                if self.bool_probability(1.0 - self.sel_prop[cur_ind]):
                    del_ind.append(cur_ind)

            cur_ind += 1
            if cur_ind == len(self.group):
                cur_ind = 0
        self.delete(del_ind)


    def cross(self, cross_ind):
        fa_ind, ma_ind = np.split(cross_ind, 2)
        for i in range(len(fa_ind)):
            fa = self.group[fa_ind[i]]
            ma = self.group[ma_ind[i]]
            chrom1, chrom2 = fa.crossover(fa, ma, self.cross_num)
            chrom1.mutate(self.mutation_prop)
            chrom2.mutate(self.mutation_prop)
            self.add(chrom1)
            self.add(chrom2)
        
    def evolve(self):
        cross_ind = self.select()
        self.cross(cross_ind)
        self.eliminate()


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
        #if not self.bool_outrange(out):
        self.bin_str = out

    def mutate(self, prob):
        num = np.random.randint(low=0, high=self.bin_len)
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
'''
