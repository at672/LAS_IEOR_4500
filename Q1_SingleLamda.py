import numpy as np
import sys
import matplotlib.pyplot as plt


####### Read the fill
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
A = mat.astype(float)





######## Power Method for PCA

order = len(A)
eps = 0.001 # cannot be too small, or else the the error will culmulate and then cause a bad answer
u0 = np.ones(order)  # intial vector
tol = 0.001


def findEigV(m, eps):

    """

    :param m: matrix to be solved
           eps: tolarence of stopping
    :return: eigva : maximum eigenvector for m
             eigve : eigenvector corresponds to eigva
    """
    u = u0
    maxi = np.max(u)
    u = u / maxi


    while True:
        #print(k)

        mu = np.dot(m, u)
        #maxi = np.linalg.norm(Au, np.inf)
        maxi = np.max(mu)
        if maxi == 0:
            print("mat has eigenvalue 0, please select new vector u0")
            sys.exit()

        w = mu / maxi
        err = np.linalg.norm(w - u, np.inf)
        u = w

        if err < eps:
            return (maxi, u)

    #print("Maximum number of iterations exceeded")

Eigva_list = []
count = 0

while True:

    (eigva, eigve) = findEigV(A,eps)
    print(eigva)

    Eigva_list.append(eigva)
    count += 1
    if abs(Eigva_list[-1] / Eigva_list[0]) < tol:
        break
    else:
        n = np.linalg.norm(eigve,2)

    eigve = eigve / n
    A = A - eigva * np.outer(eigve,eigve)

print(count)

plt.plot(range(1,count+1), Eigva_list, color='r', linewidth=1, marker='*', markerfacecolor='g', markeredgecolor='g', linestyle='--')
plt.ylabel('eigenvalue')
#plt.title('top %s\n eigenva)

plt.show()