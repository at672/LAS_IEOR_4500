
# coding: utf-8

# In[198]:

"""
Sorry that I have not fixed the I/O problem yet because I am not familiar wit pandas.
I am expected to fix it and proceed to question 2 before Tuesday 18th.

Below is the power method using a fake data.
"""

import numpy as np
from numpy import linalg as LA

x1=[5.0,6.0,1.0,3.0,8.0,9.0,7.0]
x2=[3.0,2.0,6.0,7.0,4.0,5.0,7.0]
x3=[1.0,2.0,3.0,2.0,1.0,2.0,3.0]

data=np.array([x1,x2,x3])
#every line is an asset price over time

LL,CC=data.shape
predata=(data[:,1:CC]-data[:,0:CC-1])/data[:,0:CC-1] # returns
rdata=predata-(predata.mean(axis=1))[:,np.newaxis]    
cov=np.matmul(rdata,rdata.transpose())/(CC-1)         
print "covariance matrix is:"
print cov


# In[202]:

#power method
def findMaxEigen(cov,eps=0.000001):
    ll,cc=cov.shape
    vector=np.random.rand(ll)
    vector=vector.reshape(ll,1)
    vector=vector/LA.norm(vector)
    count=0
    while(True):
        tempv=np.matmul(cov,vector)
        tempv=tempv/LA.norm(tempv)
        if LA.norm(tempv-vector)<eps:
            vector=tempv
            break
        else:
            vector=tempv
        count+=1
    tempv=np.matmul(cov,vector)
    eigenvalue=LA.norm(tempv)/LA.norm(vector)
    return eigenvalue,vector

ty=np.array([1,0,0,0,2,0,0,0,5])
print ty
ty=ty.reshape(3,3)
print ty
res=findMaxEigen(ty)
print "eigenvalue is:"
print res[0]
print "eigenvector is"
print res[1]


# In[200]:


mcov=cov
evalue=[]
evector=[]
# the following loop gives all the eigenvalue and eigenvectors
for i in range(len(cov)):
    value,vector=findMaxEigen(mcov)
    #print "########################"
    #print i+1
    #print "eigenvalue is:"
    #print value
    #print "eigenvector is"
    #print vector
    evalue.append(value)
    evector.append(vector)
    mcov=mcov-value*np.matmul(vector,vector.transpose())
print cov
print evalue
print evector

