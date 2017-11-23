# Authors:Heqixi
# Date:10/11/2017
# ! python 
# cython :boundscheck = False ,wraparound = False, cdivision = True 
from libc.math cimport fabs,sqrt,pow 
cimport numpy as  np 
import scipy.sparse as np 
cimport cython 
from cython cimport floating
np.import_array()

ctypedef fused intergral:
    int 
    long long 
ctypedef np.float64_t DOUBLE

def csr_row_norms (X):
    """L2 norm of each row in CSR matrix X. """
    if X.dtype != np.float32:
        X = X.astype(np.float64)
    return _csr_row_norms(X.data,X.shape,X.indices,X.indptr)

def _csr_row_norms(np.ndarray[floating,ndim = 1,mode = "c"] X_data,shape,
                    np.ndarray[intergral,ndim = 1,mode = "c"] X_indices,
                    np.ndarray[intergral,ndim = 1,mode = "c"] X_indptr):
    cdef:
        unsigned long long n_samples = shape[0]
        unsigned long long n_features = shape [1]
        np.ndarray[DOUBLE,ndim = 1,mode = "c"] norms 

        np.npy_intp i ,j 
        double sum_
    norms = np.zeros(n_samples,dtype = np.float64)
    for i in range(n_samples):
        sum_ = 0.0
        for j in range (X_indptr[i],X_indptr[i+1]):
            sum_ += X_data[j] * X_data[j]
        norms[i] = sum_
    return norms
