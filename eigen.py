#!/usr/bin/python

import numpy as np
from numpy import linalg as LA
import sys
import math
# import random
import time

if len(sys.argv) != 2:  # the program name and the datafile
    # stop the program and print an error message
    sys.exit("usage: eigen.py datafile ")

filename = sys.argv[1]

print "input", sys.argv[1]

try:
    f = open(filename, 'r')
except IOError:
    print ("Cannot open file %s\n" % filename)
    sys.exit("bye")

# read data
data = f.readlines()
f.close()

nrows = len(data) - 3
print "read", nrows, "rows"

# create the covariance matrix from file

sigma = np.zeros((nrows, nrows))

row = data[0]
line = row.split()
num_eig = int(line[3])
print "num_eig =", num_eig

for i in xrange(nrows):
    row = data[2 + i]
    line = row.split()
    for j in xrange(nrows):
        sigma[i][j] = float(line[j])

# compute the eigenvalues and eigenvectors

start = time.clock()
F, V = LA.eigh(sigma)
end = time.clock()
print "Numpy took", end-start, "seconds to compute all the", nrows, "eigenvalues."

# the eigenvalues are in decreasing order

# save the results in file, only the eigenvalues/vectors we asked for

f = open('diag_F_numpy.txt', 'w')
for i in range(num_eig):
    #    print F[-1-i]
    f.write(str(F[-1 - i]))
    f.write('\n')
f.close()

f = open('V_numpy.txt', 'w')
for i in range(num_eig):
    for j in range(nrows):
        f.write(str(V[j, -1-i]))
        f.write(" ")
    f.write('\n')
f.close()
