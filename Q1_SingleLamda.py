import numpy as np
import sys
import matplotlib.pyplot as plt

filename = "russell_cov.txt"
try:
    f = open(filename, 'r')
except:
    print('Cannot open file %s\n' % filename)

data = f.readlines()
f.close()

line0 = data[0].split()
line1 = data[1].split()
print(line0)
print(line1)

matrix = data[2:-1]
len(matrix)

mat = [x.split() for x in matrix]
mat = np.array(mat)
mat = mat.astype(float)



#####PCA
#set parameters
order = len(mat)
tol = 0.0001
u0 = np.ones(order)
miter = 2000  #the maximun times of iteration


def findEigV(m):

    """

    :param m: matrix to be solved
    :return: eigva : maximum eigenvector for m
             eigve : eigenvector corresponds to eigva
    """
    u = u0

    b = np.linalg.norm(u, np.inf)
    u = u / b  # unify

    for k in range(miter):

        print(k)

        v = np.dot(mat, u)
        b = np.linalg.norm(v, np.inf)

        if b == 0:
            print("mat has eigenvalue 0, please select new vector u0")
            sys.exit()

        w = v / b
        err = np.linalg.norm(w - u, np.inf)
        u = w

        if err < tol:
            return (b, u)

    print("Maximum number of iterations exceeded")

(eigva, eigve) = findEigV(mat)
print("the biggest eigenvalue is %s\n" % eigva)