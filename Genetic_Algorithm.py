import numpy as np
import random

class chromosome():

    def __init__(self, bin_str, bin_limit):
        self.bin_str = bin_str
        self.bin_limit = bin_limit
        self.bin_len = len(bin_str)

    def bool_probability(self, probability):
        return (np.random.random() < probability)

    def bool_outrange(self, bin_str):
        return int(bin_str, 2) > int(self.bin_limit, 2)

    def random_int_list(self, lower, upper, num):
        return random.sample(range(lower, upper), num)

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

class Genetic_Algorithm():

    def __init__(self, var_num, var_range, var_digit, population, obj_fun, mutation_prop=0.1):
        self.var_num = var_num
        self.var_range = var_range
        self.var_digit = var_digit
        self.population = population
        self.obj_fun = obj_fun
        self.mutation_prop = mutation_prop

class convertor():

    def __init__(self, dec, dec_range, dec_digit):
        self.dec = dec;
        self.dec_range = dec_range
        self.dec_digit = dec_digit
        self.update()

    def update(self):
        self.shift_range = (self.dec_range - self.dec_range[0]) * self.dec_digit
        self.shift_range = self.shift_range.astype(int)
        up_limit = '{0:b}'.format(self.shift_range[1])
        bottom_limit = '{0:b}'.format(self.shift_range[0])
        self.bin_digit = len(up_limit)
        self.bin_range = np.array([bottom_limit.zfill(self.bin_digit), up_limit.zfill(self.bin_digit)])
        self.update_bin()

    def bool_probability(self, probability):
        return (np.random.random() < probability)

    def change_str_letter(self, string, ind, target):
        temp = list(string)
        temp[ind] = target
        return ''.join(temp)

    def mutate_single(self, ind):
        string = self.bin[ind]
        if string=='0':
            self.bin = self.change_str_letter(self.bin, ind, '1')
        elif string=='1':
            self.bin = self.change_str_letter(self.bin, ind, '0')

    def mutate(self, prob, num=1):
        if self.bool_probability(prob):
            ind_mut = np.random.randint(self.bin_digit, size=num)
            for ind in ind_mut:
                self.mutate_single(ind)

    def dec2bin(self, dec):
        out = '{0:b}'.format(int((dec - self.dec_range[0]) * self.dec_digit))
        return out.zfill(self.bin_digit)

    def bin2dec(self, bin):
        out = int(bin, 2)
        return out/self.dec_digit + self.dec_range[0]

    def update_bin(self):
        self.bin = self.dec2bin(self.dec)
