
#! /usr/bin/python

import sys
import csv
import numpy as np
from KLcluster import *

def main():
    num_topics = sys.argv[1]
    filepath = "../data/KLs/kl_dists{0}.csv".format(num_topics)
    names = []
    dat_rows = []
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        next(reader, None)
        for row in reader:
            names.append(row[0])
            dat_rows.append([float(x) for x in row[1:]])
        
    data = np.array(dat_rows)
    pairs = KL_pair(data)
    KMC(pairs,4)
    print pairs

if __name__ == "__main__":
    main()
    
