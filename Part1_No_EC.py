import numpy as np
import sys
import time


def readdata(filename):
    # read data
    try:
        f = open(filename, 'r')
    except IOError:
        print ("Cannot open file %s\n" % filename)
        sys.exit("bye")
    lines = f.readlines()
    f.close()

    line0 = lines[0].split()
    # print (lines)

    if len(line0) == 0:
        sys.exit("empty first line")

    n = int(line0[1])
    # print ("n = %d" % n)

    lower = np.zeros(n)
    upper = np.zeros(n)
    mu = np.zeros(n)
    x = np.zeros(n)
    covariance = np.zeros((n, n))

    numlines = len(lines)

    # read the index, lower, upper and mean(mu)
    linenum = 5
    while linenum <= 5 + n - 1:
        line = lines[linenum - 1]
        thisline = line.split()
        # print (thisline)
        index = int(thisline[0])
        lower[index] = float(thisline[1])
        upper[index] = float(thisline[2])
        mu[index] = float(thisline[3])
        # move to next line
        linenum += 1

    # read lambda
    linenum = n + 6
    line = lines[linenum - 1]
    thisline = line.split()
    # print (thisline)
    lambdaval = float(thisline[1])
    # print ("lambda = %f" % lambdaval)

    # read covariance matrix
    linenum = n + 10
    while linenum <= n + 10 + n - 1:
        line = lines[linenum - 1]
        thisline = line.split()
        # print (thisline)
        i = linenum - n - 10
        # print (i)
        for j in range(n):
            covariance[i, j] = float(thisline[j])
        linenum += 1

    # print (covariance)

    # present the output in a dictionary
    alldata = {}
    alldata['n'] = n
    alldata['lower'] = lower
    alldata['upper'] = upper
    alldata['mu'] = mu
    alldata['covariance'] = covariance
    alldata['x'] = x
    alldata['lambda'] = lambdaval

    return alldata

def feasible(alldata):
    #step1: Achieve feasibility
    n = alldata['n']
    lower = alldata['lower']
    upper = alldata['upper']
    x = alldata['x']

    print ('initial lower bound: ',lower)
    print ('initial upper bound: ',upper)

    x = np.copy(lower)

    sumx = np.sum(x)

    for j in range(n):
        #print ('for x %d: lower: %f; upper: %f' % (j, lower[j], upper[j]))
        #print ('%d sum %f %f' % (j, sumx, sumx + upper[j] -lower[j]))
        if sumx + (upper[j] - lower[j]) >= 1.0:
            x[j] = 1.0 - sumx + lower[j]
    #        print ('done')
            break
        else:
            x[j] = upper[j]
            delta = upper[j] - lower[j]
            #print (x[j], lower[j], upper[j], delta)
            sumx += upper[j] - lower[j]
    #    print (">>>>",j, x[j], sumx )

    #print (x)
    alldata['x'] = x # feasible x1

    return alldata

def func(x):
    """
    :param all_data: all the data we need, including covariance, mu(mean),lower, upper
    :return: the value of function F
    """
    mu = all_data['mu']
    cov = all_data['covariance']
    lamb = all_data['lambda']

    # calculate the value of function
    tmp = np.dot(cov,x)
    result = lamb * np.dot(x,tmp) - np.dot(mu,x)

    return result

def gradient_func(x):
    """
    :param all_data: all the data we need, including covariance, mu(mean),lower, upper
    :return: a vector of the gradient of F
    """
    mu = all_data['mu']
    #size_mu = len(mu)
    #size_x = len(x)
    #if size_x != size_mu:
    #    print('please enter a another x with size %s' % size_mu)
    #    return 1
    cov = all_data['covariance']
    lamb = all_data['lambda']

    #calculate gradient of function F
    result = 2 * lamb * np.dot(cov,x) - mu

    return result

def compute_s(x,y):
    """
    :param x: feasible variable
    :param y: the direction we should move
    :return:  how far we should move along y
    """
    mu = all_data['mu']
    cov = all_data['covariance']
    lamb = all_data['lambda']

    # compute s
    covY = np.dot(cov,y)
    XcovY = np.dot(x,covY)
    YcovY = np.dot(y,covY)
    muY = np.dot(mu,y)
    result = -(2 * lamb * XcovY - muY) / (2 * lamb * YcovY)

    if result <= 1 and result > 0:
        return result
    else:
        return 0  # what if s < 0 or s = 0  ###################

def compute_y( input_x ):
    #compute gradient
    vect = np.dot( all_data['covariance'], input_x )
    g = 2*all_data['lambda']*(vect) - all_data['mu']
    #now set up linear program
    g_sorted = sorted(g, key=float, reverse=True)
    indexes = sorted(range(len(g)),key=g.__getitem__, reverse=True)
    #print("g ", g)
    #print("indexes are ", indexes)
    #print("g sorted ", g_sorted)
    y = np.zeros(all_data['n'])
    n = all_data['n']
    y_storage = np.zeros( (all_data['n'], all_data['n']) )
    objective = np.zeros(all_data['n'])

    boundary_condition = ( all_data['upper'] - input_x ) < ( all_data['lower'] - input_x)
    if boundary_condition.any() == True :
        #we have achieved optimal?
        return np.zeros(all_data['n'])

    for m in range(0, all_data['n']):
        sum1 = 0
        y = np.zeros(all_data['n'])

        for j in range(0, all_data['n']):
            if (j < m):
                y[j] = all_data['lower'][j] - input_x[j]
            elif (j > m):
                y[j] = all_data['upper'][j] - input_x[j]
            sum1 = sum1 + y[j]
        y[m] = 0 - sum1
        y_storage[m, :] = y
        #print("y vectors are ", y_storage)
        objective[m] = np.dot(g_sorted, y)
    
    #print("y vectors are ", y_storage)
    min_obj = np.min(objective)
    min_obj_idx = np.where( min_obj == np.min(objective) )

    #need to reshuffle y
    y_chosen = np.ravel( y_storage[min_obj_idx, :])
    y_reshuffle = y_chosen[indexes]
    return y_reshuffle

def compute_F( input_x):
    first_sum = 0
    second_sum = 0
    third_sum = np.dot(all_data['mu'], input_x)
    second2_sum = 0
    for i in range(0, all_data['n']):
        term = all_data['x'][i]**2 * (all_data['covariance'][i,i]**2)
        first_sum = first_sum + term

    for i in range(0, all_data['n']):
        for j in range(0, all_data['n']):
            if( i < j ):
                term2 = all_data['covariance'][i,j]*input_x[i]*input_x[j]
                second_sum = second_sum + term2

    F = all_data['lambda']*(first_sum + 2*second_sum) - third_sum
    return(F)

if __name__ == '__main__':

    file = "example.txt"

    dt = readdata(file)  #all the data information
    all_data = feasible(dt) 
    print("Initial x is ", all_data['x'])
    tolerance = 1e-7
    maxi_itera = 100000
    delta = 100 # the initial difference between F(x1) and F(x2)
    i = 1

    # looping part
    x0 = all_data['x']
    vector_x = x0
    while delta >= tolerance and i < maxi_itera:
       # print("current x is: ", x0)
        y = compute_y(x0)
        s = compute_s(x0,y)

        x1 = x0 + s * y
        delta = func(x0) - func(x1)
        print("Objective value F at iteration %d is %f ", i, func(x0) )
       # print("at iteration %d delta is %f ", i, delta)
   #     print("func x0 is ", func(x0))
   #     print("func x1 is ", func(x1))

        vector_x = np.vstack((vector_x,x1))
        x0 = x1
        i += 1
    print("Algorithm terminated.")
    print("Final x value: ", x0)
