from scipy import linalg
import numpy as np

M = np.array([[1,2], [2,1], [3,4], [4,3]])

# Singular value decomposition of M
U, Sig, VT = linalg.svd(M, full_matrices = False)
print("U = ", U)
print("Sig =", Sig)
print("V^T = ", VT)

# Eigen value decomposition of M^TM 
MTM = np.matmul(np.transpose(M),M)
# print("MTM =\n",MTM)
evals, evecs = linalg.eigh(MTM)


# Sorting and rearranging 
idx = evals.argsort()[::-1]   
evals = evals[idx]
evecs = evecs[:,idx]
print('-'*79)
print("evals =", evals)
print("evecs =\n", evecs)

# check
# print(np.multiply(58, [[0.7],[0.7]]))
# print(np.matmul(MTM, [[0.7],[0.7]]))

# V = evecs
print('-'*79)
print("V =\n", np.transpose(VT))
print("evecs =\n", evecs)


# eigen value of MtM = (singulat values of M)^2
print('-'*79)
print("Singular values of M = ", Sig)
print("Eigen values of MtM = ", evals)
print("sqrt MtM =", np.sqrt(evals))

