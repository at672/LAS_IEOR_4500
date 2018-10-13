#!/usr/bin/python
import numpy as np
import sys
import time

def readdata( file ):
    #open the file
    try:
        f = open(file, 'r')
    except IOError:
        print ("Cannot open file %s\n" % file)
        sys.exit("Quitting program.")
    
    # read data
    lines = f.readlines()
    f.close()

    line0 = lines[0].split()
    #print (lines)

    if len(line0) == 0:
        sys.exit("empty first line")

    n = int(line0[1])
    #print ("n = %d" % n)

    lower = np.zeros(n)
    upper = np.zeros(n)
    mu = np.zeros(n)
    x = np.zeros(n)
    covariance = np.zeros((n,n))

    numlines = len(lines)
    
    #read the index, lower, upper and mean(mu)
    linenum = 5
    while linenum <= 5 + n-1:
        line = lines[linenum-1]
        thisline = line.split()
        #print (thisline)
        index = int(thisline[0])
        lower[index] = float(thisline[1])
        upper[index] = float(thisline[2])
        mu[index] = float(thisline[3])        
        # move to next line
        linenum += 1
    
    #read lambda
    linenum = n + 6
    line = lines[linenum-1]
    thisline = line.split()
    #print (thisline)
    lambdaval = float(thisline[1])
    #print ("lambda = %f" % lambdaval)
    
    #read covariance matrix
    linenum = n + 10
    while linenum <= n+10 + n-1:
        line = lines[linenum-1]
        thisline = line.split()
        #print (thisline)
        i = linenum - n - 10
        #print (i)
        for j in range(n):
            covariance[i,j] = float(thisline[j])
        linenum += 1

    #print (covariance)
    
    #present the output in a dictionary
    alldata = {}
    alldata['n'] = n
    alldata['lower'] = lower
    alldata['upper'] = upper
    alldata['mu'] = mu
    alldata['covariance'] = covariance
    alldata['x'] = x
    alldata['lambda'] = lambdaval

    return alldata

    #cell 2

def feasible(alldata):
    #step1: Achieve feasibility
    n = alldata['n']
    lower = alldata['lower']
    upper = alldata['upper']
    x = alldata['x']

  #  print ('initial lower bound:',lower)
 #   print ('initial upper bound:',upper) 

    x = np.copy(lower)

    sumx = np.sum(x) 

    for j in range(n):
      #  print ('for x %d: lower: %f; upper: %f' % (j, lower[j], upper[j]))
        #print ('%d sum %f %f' % (j, sumx, sumx + upper[j] -lower[j]))
        if sumx + (upper[j] - lower[j]) >= 1.0:
            x[j] = 1.0 - sumx + lower[j]
        #    print ('done')
            break
        else:
            x[j] = upper[j]
            delta = upper[j] - lower[j]
            #print (x[j], lower[j], upper[j], delta)
            sumx += upper[j] - lower[j]
      #  print (">>>>",j, x[j], sumx )

  #  print (x)
    alldata['x'] = x

def compute_F():
    first_sum = 0
    second_sum = 0
    third_sum = np.dot(DATA['mu'], DATA['x'])
    second2_sum = 0
    for i in range(0, DATA['n']):
        term = DATA['x'][i]**2 * (DATA['covariance'][i,i]**2)
        first_sum = first_sum + term

    for i in range(0, DATA['n']):
        for j in range(0, DATA['n']):
            if( i < j ):
                term2 = DATA['covariance'][i,j]*DATA['x'][i]*DATA['x'][j]
                second_sum = second_sum + term2

    F = DATA['lambda']*(first_sum + 2*second_sum) - third_sum
    return(F)

def compute_y( input_x ):
    #compute gradient
    vect = np.dot( DATA['covariance'], input_x )
    grad_F = 2*DATA['lambda']*(vect) - DATA['mu']
    #now set up linear program
    g_sorted = sorted(grad_F, key=float, reverse=True)
    y = np.zeros(DATA['n'])
    n = DATA['n']
    y_storage = np.zeros( (DATA['n'], DATA['n']) )
    objective = np.zeros(DATA['n'])

    boundary_condition = ( DATA['upper'] - input_x ) < ( DATA['lower'] - input_x)
    print(boundary_condition)
    if boundary_condition.any() == True :
        #we have achieved optimal?
        return np.zeros(DATA['n'])

    for m in range(0, DATA['n']):
        sum1 = 0
        y = np.zeros(DATA['n'])

        for j in range(0, DATA['n']):
            if (j < m):
                y[j] = DATA['lower'][j] - input_x[j]
            elif (j > m):
                y[j] = DATA['upper'][j] - input_x[j]
            sum1 = sum1 + y[j]
        y[m] = 0 - sum1
        y_storage[m, :] = y
        objective[m] = np.dot(g_sorted, y)
    min_obj = np.min(objective)
    min_obj_idx = np.where( min_obj == np.min(objective) )
  #  print('obj is ', objective)
  #  print(y_storage)
  #  print(y_storage[min_obj_idx, :])

    return(np.ravel( y_storage[min_obj_idx, :]))


## DRIVER
myFile = "example.txt"
DATA = readdata(myFile)
result = feasible(DATA)

my_y = compute_y( DATA['x'] )
print(my_y)
print("EOF")