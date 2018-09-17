import numpy as np

M1 = np.array([[1,4,5],[3,6,3],[1,7,6]]) #test-matrix

print(M1)

def eigenvalue(A, v):
    Av = A.dot(v)
    return v.dot(Av)

def power_iteration(A):
    n, d = A.shape

    v = np.ones(d) / np.sqrt(d)
    ev = eigenvalue(A, v)

    while True:
        v_new = (A.dot(v)) / np.linalg.norm(A.dot(v))
        ev_new = eigenvalue(A, v_new)
        if np.abs(ev - ev_new) < 0.01:
            break

        v = v_new
        ev = ev_new

    return ev_new, v_new

eig = []
tolerance = 0.001

while True:
    tup = power_iteration(M1)
    eig.append(tup)
    if (abs(eig[0][0]/eig[len(eig)-1][0]) < tolerance):
        break
    M1 = M1 - eig[len(eig)-1][0]*(eig[len(eig)-1][1].dot(eig[len(eig)-1][1].T))


print(eig)
