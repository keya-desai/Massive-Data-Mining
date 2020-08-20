# ** CS550 Massive Data Mining - Homework-3 								   **
# ** Q2) Spectral clustering - Finding optimal graph partition using 0 as boundary **

from scipy import linalg
import numpy as np

# Laplacia matrix
L = np.array([[4, -1, -1, -1, 0, 0, -1, 0],
		[-1, 3, -1, -1, 0, 0, 0, 0],
		[-1, -1, 3, -1, 0, 0, 0, 0],
		[-1, -1, -1, 3, 0, 0, 0, 0],
		[0, 0, 0, 0, 2, -1, -1, 0],
		[0, 0, 0, 0, -1, 2, -1, 0],
		[-1, 0, 0, 0, -1, -1, 4, -1],
		[0, 0, 0, 0, 0, 0, -1, 1]])

node_mapping = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H'}


# Eigen values and eigen vectors
evals, evecs = linalg.eigh(L)
print("\nEigen values: \n", evals)
print("\nEigen vectors: \n", evecs)


# second smallest eigen value
lambda2 = evals[1]
# eigen vector corresponding to lambds_2
x = evecs[:,1]
print("\nlambda_2 = ", lambda2)
print("Eigen vector corresponding to lambda_2 = \n", x)


# 1st cluster
print("\n1st cluster")
for n in np.argwhere(x>0):
	print(node_mapping[n[0]])

# 2nd cluster 
print("2nd cluster")
for n in np.argwhere(x<0):
	print(node_mapping[n[0]])