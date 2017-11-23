"""Extended math utilities """
# Author: Heqixi
# Date : 11/20/2017
from __future__ import division 
from functools import partial 
import warnings 
import numpy as np 
from scipy import linalg
from scipy.sparse import issparse,csr_matrix 
from .fixes import np_version
from .validation import check_array 
from .sparsefuncs_fast import csr_row_norms




def norms(x):
    """ Computed the Euclidean or Frobenius norm of x .
    Returns the Euclidean norm when x is a vector ,the Frobenius norm when x 
    is a matrix (2-d array) .More precise than sqrt(squared_norm(x)).
    """
    x = np.asarray(x)
    nrm2, = linalg.get_blas_funcs(['nrm2'],[x])
    return nrm2(x)

# Newer Numpy has a ravel that needs less copying
if np.version < (1,7,1):
    _ravel = np.ravel 
else:
    _ravel = partial(np.ravel,order = 'K')

def squared_norm(x):
    """
    Squared Euclidean or Frobenius norm of x.
    
    Returns the Euclidean norm when x is a vector ,the Frobenius norm whem x 
    is a matrix (2-d array ).More precise than sqrt (squred_norm(x))
    """
    x =_ravel(x)
    return np.dot(x,x)

def row_norms(x,squared = False):
    """ Row-wise (squared) Euclidean norm of x 

    Equivalent to np.sqrt((X*X).sum(axis = 1) ,but also supports sparse 
    matrces and does not create an X.shape-sized temporary

    Perform no input validation .
    """
    if issparse(x):
        if not isinstance(x,csr_matrix):
            x =csr_matrix(x)
        norms = csr_row_norms(x)
    else:
        norms = np.einsum('ij,ij->i',X,X)
    if not squared:
        np.sqrt(norms,norms)
    return norms 
    
