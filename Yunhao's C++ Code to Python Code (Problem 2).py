import numpy as np
import pandas as pd
import numpy.matlib


# function defined for the dot product # 
def dot_product(N,x,y):
    return np.dot(x,y)

# function defined to generate uniform distribution # 
def uni_rv():
    return np.random.uniform(0,1,1)

# feasibility detection #
def initial(N, upbound, lowbound, x):
    mark = True
    sumlow = 0
    sumup = 0
    sumgap = 0
    gap = [0]*N
    for i in range(N):
        if upbound[i] < lowbound[i]:
            print("upbound < lowbound at " + i)
            return False
        sumlow = sumlow + lowbound[i]
        sumup = sumup + upbound[i]
        gap[i] = uni_rv()*(upbound[i] - lowbound[i])
        sumgap = sumgap + gap[i]

    if(sumlow>=1):
        if(sumlow == 1):
            print("portfolio vector should be the low bound")
            return False
        else:
            print("Too big low bound")
            return False
    if(sumup<=1):
        if(sumup==1):
            print("portfolio vector should be the up bound")
            return False
        else:
            print("Too small upbound")
            return False

    print("problem is feasible")
    weight = (1- sumlow)/sumgap
    collect = 0
    for i in range(N):
        x[i] = lowbound[i] + gap[i]*weight
        collect += x[i]

    print("normalization examination:" + collect)
    return True

def GiveY(N, g, y, x, cov, mu, lambada, upbound, lowbound):
    return 0

def GiveS(N, g, y, cov, lambada):
    s = dot_product(N, g, y)
    temp = [0]* N
    for i in range(N):
        temp[i] = dot_product(N, cov[i,:], y)
    s= s/dot_product(N, temp, y)
    s = s/ (-2*lambada)
    if (s>1):
        s=0.99
    print("s is " + s)
    if(s>1):
        return 0.99
    elif(s < -0.01):
        print("find a s smaller than zero!")
    return s

def GiveStep(N, x, cov, mu lambada, lowbound, upbound):
    y = [0]*N
    g = [0]*N
    GiveY(N, g, y, x, cov, mu, lambada, upbound, lowbound)
    s= GiveS( N, g, y, cov, lambada)
    move_max = 0
    for i in range(N):
        temp = s*y[i]
        x[i] = x[i] + temp
        if (abs(temp))> move_max:
            move_max = abs(temp)
    return move_max

NN = 2

upbound = [0]* NN
lowbound = [0]* NN
cov = np.zeros((NN, NN))
mu = [0]* NN
x = [0]* NN
lambada = 1
upbound[0] = 1 upbound[1] = 1 lowbound[0] = 0 lowbound[1] = 0
cov[0] = 4 cov[1] = -1 cov[2] = -1 cov[3] = 1
mu[0] = 2 mu[1] = 1

feasible = initial(NN, upbound, lowbound, x)
if(feasible==false):
    print("problem-infeasible")
    return 1
eps = 0.01
while(True):
    size = GiveStep(NN, x, cov, mu, lambada, lowbound, upbound)
    if size < eps:
        break


return 0;






    
    
    

        
    

