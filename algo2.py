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

    print ('initial lower bound:',lower)
    print ('initial upper bound:',upper)

    x = np.copy(lower)

    sumx = np.sum(x)

    for j in range(n):
        print ('for x %d: lower: %f; upper: %f' % (j, lower[j], upper[j]))
        #print ('%d sum %f %f' % (j, sumx, sumx + upper[j] -lower[j]))
        if sumx + (upper[j] - lower[j]) >= 1.0:
            x[j] = 1.0 - sumx + lower[j]
            print ('done')
            break
        else:
            x[j] = upper[j]
            delta = upper[j] - lower[j]
            #print (x[j], lower[j], upper[j], delta)
            sumx += upper[j] - lower[j]
        print (">>>>",j, x[j], sumx )

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

if __name__ == '__main__':

    file = "example.txt"

    # make all_data a global variable

    dt = readdata(file)  #all the data information
    all_data = feasible(dt)  # is it now global?#####################

    tolarence = 1e-2
    maxi_itera = 1000
    delta = 100 # the initial difference between F(x1) and F(x2)
    i = 1

    # looping part
    x0 = all_data['x']
    vector_x = x0
    while delta >= tolarence and i < maix_itera:

        y = compute_y(x0)
        s = compute_s(x0,y)

        x1 = x0 + s * y
        delta = func(x0) - func(x1)

        vector_x = np.vstack((vector_x,x1))
        x0 = x1
        i += 1