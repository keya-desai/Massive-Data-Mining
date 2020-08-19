# Implementation of page rank algorithm 

import numpy as np

# number of nodes in graph
n = 100
beta = 0.8
# no. of iterations
itr = 40
filepath = 'data/graph.txt'

M = np.zeros((n,n))
r = np.zeros((n,1))
one = np.ones((n,1))

with open(filepath) as fp:
   line = fp.readline()
   while line:
       nodes = line.strip().split()
       # source
       i = nodes[0]   
       # target
       j = nodes[1]
       M[int(j)-1][int(i)-1] += 1
       line = fp.readline()

# compute out-degree of nodes
deg_col = np.sum(M,axis = 0)

# divide each value with out degree
for i in range(n):
    M[:,i] = np.true_divide(M[:,i],deg_col[i])

# computing rank
r = one/n
teleport = np.multiply(one,1-beta)/n
for i in range(itr):
    r =  teleport + np.matmul(beta*M,r)

# sorting nodes by page rank
a = np.transpose(r)
idx = a.argsort()
max_nodes = np.flip(idx[0][-5:]) + 1
min_nodes = idx[0][:5] + 1

print("Nodes IDs with highest page rank: ", max_nodes)
print("\nNode ID \t Page rank")
for i in max_nodes:
    print(i, "\t\t", a[0][i-1])

print("\nNodes IDs with lowest page rank: ", min_nodes)
print("\nNode ID \t Page rank")
for i in min_nodes:
    print(i, "\t\t", a[0][i-1])