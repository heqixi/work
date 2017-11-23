# -*-  coding:utf-8 -*-
# Author :heqixi
# Date: 2017/11/8

import itertools
import numpy as np 
from scipy.spatial import distance 
from scipy.sparse import csr_metrix
from scipy.sparse import issparse 
from ..utils import check_array 
from ..utils import gen_even_slices 
from ..utils import gen_batches
from ..utils.fixs import partial 
from ..utils.extmath import row_norms ,safe_sparse_dot 
from ..externals.joblib import Parallel 
from ..preprocessing import normalize 
from ..externals.joblib import cpu_count 
from .pairwise_fast import _chi2_kernek_fast,_sparse_manhattan 


# Utility Fuctions 
def _return_float_dtype(X,Y):
    """
    1: If dtype of X and Y is float32,the dtype float32 is returned 
    2: Else dtype float is return 
    """
    if not issparse(X) and not isinstance(X,np.ndarray):
        X= np.asarray(X)
    if Y is None:
        Y_dtype = X.dtype
    elif not issparse(Y) and not isinstance(Y,np.ndarray):
        Y = np.asarray(Y)
        Y_dtype = Y.dtype
    else : 
        Y_dtype = Y.dtype
    if X.dtype == Y.dtype == np.float32:
        dtype = np.float32
    else : 
        dtype = np.float 
    return X,Y,dtype

def check_pairwise_arrays(X,Y,precomputed = False,dtype= None):
    """Set X and Y appropriately and check inputs 

    If Y is None ,it is set as a pointer to X 
    If Y is given , this does not happen 
    All distance metrix should use this function fist ro assert that the    given paramaters are correct and safe to use 
    
    Specifically,this function fist ensures that both X and Y ara arrays    then checks that they are at least two dimensions while ensuring that 
    their elements are float (or dtype if provided ) .Finally ,the function 
    checks that the size of the second dimension of the two arrays is equal,    or the equivalent check for a precomputed distance matrix 

    Parameters:
    -----------
    X: { array-like ,sparse_matrix } ,shape (n_sample_a ,n_features)

    Y :{array-like,sparse_matrix},shape (n_sample_b,n_features)

    precomputed : boolean
        True if X is to be treated as precomputed distances to the 
        samples in Y .
    dtype: string ,type ,list of types　or None (default= None )

    Returns:
    -----------
    safe_x : {array-like,sparse_matrix},shape(n_sample_a,n_features)

    safe_y : see safe_x .Notes that is Y is none ,the safe_y is a pointer            to safe_x
    """
    X,Y,dtype_float = _return_float_dtype(X,Y) 
    warn_on_dtype = dtype is not None 
    estimator = 'check_pairwise_arrays'
    if dtype is  None :
        dtype = dtype_float 
    if Y is X or Y is None :
        X = Y = check_array(X,accept_sparse='csr',dtype = dtype,warn_on_dtype = warn_on_dtype,
                estimator = estimator)
    else :
        X = chect_array(X,accept_sparse = 'csr',dtype = dtype ,warn_on_dtype = warn_on_dtype,
                estimator = estimator )
        Y = check_array (Y,accept_sparse = 'csr',dtype = dtype ,warn_on_dtype = warn_on_dtype,
                    estimator = estimator )

    if precomputed:
        if X.shape[1] != Y.shape[0]:
            raise ValueError ("Precomputed metric requires shape (n_queries ,n_indexed)."
                        "Got (%d,%d) for %d indexed "
                            % (X.shape[0],X.shape[1],Y.shape[0]))                               

    elif X.shape[1] != Y.shape[1]:
        raise ValueError ("Incompatibbe dimension for X amd Y matrics "
                            "X.shape[1] == %d while Y.shape[1] == %d"
                            % (X.shape[1],Y.shape[1]))
    return X,Y
        




def euclidean_distances (X,Y = None,Y_norm_squared = None,squared = False ,
                        X_norm_squared = None):
    """
    Considering the rows of X (and Y = x ) as the vectors ,compute the 
    distance matrix between each pair of the vectors 

    for efficiency reasons ,the euclidean distance between a pair of row 
    vectors x and y is compute as ::
            dist(x,y) = sqrt(dot(x,x) - 2 * dot(x,y) + dot (y,y)
    
    Parameters：

    X : (array-like,sparse matrix ) ,shape (n_sample_1,n_features )

    Y : { array-like ,sparse matrix } ,shape (n_sample_2,n_features)

    Y_norm_squared: array-like , shape(n_sample_2,) ,optional 
                Pre-computed dot distance of vectors in Y (e.g.,
                '' (Y ** 3).sum(axis = 1)

    squared: boolean ,optional
        Return squared Euclidean distance 

    X_norm_squared: see Y_norm_squared

    Returns:

    distance : {array,sparse matrix } ,shape (n_sample_1,n_sample_2)

    See alse :
        parse_distance : distances betweens pairs of elements of X and Y .

    """
    


    X,Y = check_pairwise_arrays(X,Y)
    
    if X_norm_squared is not None:

        XX = check_array(X_norm_squared)
        if XX.shape == (1,X.shape[0]):
            XX  = XX.T
        elif XX.shape != (X.shape[0],1):
            raise ValueError(
                        "Incompatibbe dimensions of X and X_norm_squared")
    else:
        XX = row_norms(X,squared = True)[:,np.newaxis]
    if X is Y : #shortcut in the common case euclidean_distance (X,X)
        YY = XX.T
    elif Y_norm_squared is not None:
        YY = np.atleast_2d (Y_norm_squared)

        if YY.shape != (1,Y.shape[0]):
            raise ValueError("Incompatible dimensions for Y and Y_norm_squared !")

    else :
        YY = row_norms(Y,squared = True)[np.newaxis,:]
    distances = safe_sparse_dot(X,Y.T,dense_ouput = True)
    distances *= -2 
    distances += XX 
    distances += YY 
    np.maximum(distances,0,out = distances)

    if X is Y :
        # Ensure that distances between vectors and themselfs are set to 0.0
        # This may not be the case due to floating point rounding errors 
        distances.flat[::distance.shape[0]+1] = 0.0
    return distances if squared else np.sqrt(distances,out=distances)

