import numpy as np
from Genetic_Algorithm import chromosome

dec = 50.0
dec_range = np.array([-13.0, 108.0])
dec_digit = 1000
chrom = chromosome(dec, dec_range, dec_digit)
chrom.mutate(0.5, 5)
