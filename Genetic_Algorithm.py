import numpy as np

class chromosome():

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

    def dec2bin(self, dec):
        out = '{0:b}'.format(int((dec - self.dec_range[0]) * self.dec_digit))
        return out.zfill(self.bin_digit)

    def bin2dec(self, bin):
        out = int(bin, 2)
        return out/self.dec_digit + self.dec_range[0]

    def update_bin(self):
        self.bin = self.dec2bin(self.dec)
