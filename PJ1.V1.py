import numpy as np
from numpy import linalg as LA
import math

"""
text=np.loadtxt('russell_cov.txt')
text

"""

# suppose we already have the russell matrix
russell = np.array([[1, 2, 3], [3, 4, 6], [7, 2, 8]])

# find the eigenvalue and eigenvector
F, V = LA.eigh(russell)

# the top eigenvalue
r_max = max(F)

# set the tolerance
t = 0.9

# the initial vector
x = np.array([-0.5, -0.4, 0.7])

y = x
r = 0

# continue until the eigenvalue satisfies the tolerance
while abs(r - r_max) > t:
    # use the power method and normalize it
    y = np.dot(russell, y)
    y = y / math.sqrt(np.dot(y, y))

    # use the Rayleigh quotient
    r = np.dot(y, np.dot(russell, y)) / np.dot(y, y)

# print the result
print "the max eigenvalue is %d, under the power method with tolerance %f, the calculated eigenvalue is %f" % (
r_max, t, r)
print "the eigenvector is "
print V
print "the calculated eigenvector is ", y
