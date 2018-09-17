
# coding: utf-8

# In[27]:

#!/usr/bin/python

#Python 2.7.0 code, power iteration
#Avi Thakore
#LAS team, IEOR 4500

####
#IMPORT STATEMENTS and timer set up.
import time
systime0 = time.clock()
import os
import numpy as np
import math

# Load CSV dataset
from csv import reader
import csv

print("Running script ... ")

##### IMPORTANT: DIRECTORY CREATION NOT YET FINALIZED ######

# Directory Creation
#Create folder to store outputs
#DO NOT RUN until system has been organized
#newpath = os.path.join('E:', os.sep, 'ECE_4950', 'Assignment 4-5', 'plots')
#if not os.path.exists(newpath):
#    os.makedirs(newpath)

# Load a CSV file
def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return np.matrix(dataset).astype(np.float)

# CLOSE THE OPEN FILE BEFORE YOU RUN THIS SCRIPT
def write_csv(filename, list1, list2):
	with open(filename, 'w') as csvfile:
		writer = csv.writer(csvfile, lineterminator = '\n')
		writer.writerow([('ID'),('TARGET')])
		rows = zip(list1,list2)
		for row in rows:
			writer.writerow(row)
            
    
####### PYTHON CALLING CONVENTION #######
#for numpy python matrixes: use [i, j] to get element of row i col j
# use [:,0] to get 0th column
# use [0,:] to get 0th row
#
# for python LISTS
# use [i][j] to get element j of sublist i in the entire list


#[('Result_1', 1, 5), ('Result_2', 2, 6), ('Result_3', 3, 7), ('Result_4', 4, 8)]
# Load datasets
print( "Loading data ... ")

#Russel_Returns = load_csv('files/russell.csv')
#Russel_Test = load_csv('files/russell_cov.csv')

print( "Data Loaded")
#print("Pre processing data ... ")
#print(" Organizing data in memory ...")





# In[22]:

#COMPUTATION CODE (BASIC!)

def eigenvalue(A, v):
    Av = A.dot(v)
    return v.dot(Av)

def power_iteration(A, tolerance):
    n, d = A.shape

    v = np.ones(d) / np.sqrt(d)
    ev = eigenvalue(A, v)

    while True:
        Av = A.dot(v)
        v_new = Av / np.linalg.norm(Av)

        ev_new = eigenvalue(A, v_new)
        if np.abs(ev - ev_new) < tolerance:
            break

        v = v_new
        ev = ev_new

    return ev_new, v_new


# In[25]:

test1 = np.array( [[1.0, 2.0, 0.0], [-2.0, 1.0, 2.0], [1.0, 3.0, 1.0]] )


val = power_iteration(test1, 0.001)
#val should return the eigenvalue followed by the normalized eigenvector
#for above example its 3, [0.5 0.5 1]
print val


# In[ ]:




# In[26]:

print('Program Done')
systime1 = time.clock()
print('Total Execution Time: %f' % systime1)


# In[ ]:



