""" Utilities for input validation """
# Author  : Heqixi
# Date : 3/11/2017
# License : free  

import numpy as np 
import warnings 
from ..exceptions import NotFittedError as _NotFittedError
import re
from collections import Iterable
from ..externals import six
from .deprecation import deprecated 
from ..exceptions import DataConversionWarning as _DataConversionWarning
from ..exceptions import NonBLADotWarning as _NonBLASDotWarning
from .deprecation import deprecated 
import scipy.sparse as  sp 


@deprecated("DataConversionWarning has been moved into the sklearn"
            "exceptions module.It will not e available here form "
            "version 0.19")
class DataConversionWarning(_DataConversionWarning):
    pass  

@deprecated("NonBLADotWarning has been move into the sklearn.exceptions"
        "module .It will not be available from version 0.19")
class NonBLADotWarning(_NonBLASDotWarning):
    pass 
@deprecated("NotFittedError hass been move into the sklearn.exceptions"
        "module,and it will not be availiable since version 0.19")
class NotFittedError(_NotFittedError):
    pass
FLOAT_DTYPES = (np.float64,np.float32,np.float16)
#Silenced by default to reduce verbosity .Turn on at runtime for 
#performance profiling 

warnings.simplefilter('ignore',_NonBLASDotWarning)


def _assert_all_finite(x):
    """ Like assert_all_finite ,but only for ndarray """
    x = np.asanyarray(x)
    # First try an O(n) time space solution for the common case 
    # that everything is finite ;fall back to O(n) space np.isfinite to 
    # prevent false positives from overflow in sum method 
    if (x.dtype.char in np.typecodes['ALLFOAT'] 
            and not np.isfinite(x.sum())
            and not np.isfinite(x).all()):
        raise ValueError("Input contains NaN,infinity"
                        "or a value too large for %r" %x.dtype)
def assert_all_finite(x):
    """ Throw a ValueError if x contains NaN or infinity 
    Input must ba a np.array instace or a scipy.sparse matrix 
    """
    _assert_all_finite(x.data if issparse(x) else x)

def column_or_1d(y,warn = True):
    """ Ravel column or 1d numpy array ,else raises an error 

    Parameter :
    ------------
    y : array-like 

    Returns:

    y :array 

    """
    shape = np.shape(y)
    if len(shape) ==1 :
        return np.ravel(y)
    if len(shape) == 2 and shape[1] == 1:
        if warn:
            warnings.warn("A column-vector y was passed when a 1d array "
                        "was expected .Please change the shape of y to "
                        "(n_samples,) for example using ravel()")
            return np.ravel(y)
    raise ValueError("bad input shape {0}".format(shape))

def check_if_fitted(estimator,attributes,all_or_any = all):
    """ Perform is_fitted validation for estimator 

    Check if the estimator is fitted by verifying the presence of 
    'all_or_any' of the passed attributes and raise a NotFittedError 
    with the given message.

    Parameter:
    --------
    estimator: estimator isinstance
            estimator instance for which the check is performed

    attributes: attribute name(s) given as string of a list/tuple of strings 
            Eg.: ["coef_","estimator_"]

    all_or_any: callable ,(all,any) default all 
            Specify whether all or any of the given attributes must exit

    """
    meg = ("This %(name)s instance is not fitted yet,call 'fit' with"
      "appropriate argments before using this method")
    if not hasattr(estimator,'fit'):
        raise TypeError ("%s is not an estimator instance"
                           %(estimator))
    if not isinstance(attributes,(list,tuple)):
        attributes  = [attributes]
    if not all_or_any (hasattr(estimator,attr) for attr in attributes):
        print(attributes)
        raise _NotFittedError(meg % {'name':type(estimator).__name__} )



def check_is_numeric(ar):
    """ This method check if the elements of an array-like object are 
        string 
    
    Parameters:
    ----------
    ar: array,(or string),
        the target values
    
    Returns:
    is_string: boolen, if the ar is (include) string,return True;
                others:return False

    """
    if isinstance(ar,str):
        non_numeric = re.findall(r"[^0-9,^.]+",ar)
    if hasattr(ar,'__len__') or hasattr(ar,'shape') or hasattr(ar,'__array__'):
        non_numeric = [re.findall(r"[^0-9,^.]+",item) for item in ar]
    non_numeric = sum(non_numeric,[])
    if not non_numeric:
        return True
    else:
        return False

def check_array(array ,accept_sparse= None,dtype = 'numeric',order = None,
                copy = False , force_all_finite =True, ensure_2d = True,
                allow_nd = False ,ensure_min_samples = 1,
                ensure_min_features = 1 ,
                warn_on_dtype = False ,estimator= None ):
    
    """ Input validation on an array ,list ,sparse metrix or similar.
     By default ,the input is converted to an at least 2D numpy array,
     If the dtype of the array is object,attempt converting to float,
     raising on failure .

     Parameters :
     -----------
     array : target object ,
        Input object to check / convert 
    
    accept_sparse: string ,list of a string or None (default)
        String[s] representing allowed sparse matrix formats ,
        such as 'csr','csc',etc . None means that any sparse input raises 
        an error .If the input is sparse but not in the allowed format ,it 
        will be converted to the first listed format .

    dtype : string ,type ,list of types or None (default = None )
        Data type of result ,If None ,the dtype of the input is preserved.
        If 'numeric',dtype is preserved unless array.dtype is object.
        If dtype is a list of types,conversion on the fist type is only 
        performed if the dtype of the input is not in the list .

    order : ‘F','C' or None (default )
        Whether an array will be forced to be fortran or c-style.
        When order is None(default),then if copy = False ,nothing is ensured        about the memory layout of the output array,otherwise (copy = True )
        the memory layout of the returned array is kept as close as possible        to the original array .

    copy : boolen ,default = False 
        Whether a forced copy will be triggered ,If copy is False ,a copy 
        might be triggered by a conversion .

    force_all_finite: boolen,default=True 
        
    ensure_2d: boolen ,default = True 

    allow_nd = boolen,(default = False)

    ensure_min_samples: int ,(default = 1 )

    ensure_min_features: int (default = 1)

    warn_on_dtype: boolean,(default = False )
        Raise DataConversionWarning if the dtype of the input data structure        does not match the requested dtype ,causing a memory copy
    
    estimator: str or etsimator instance (default = None )
        if passed ,include the name if the estimator in warning message .

    Returns :
    -------------
    x_converted :object 
        The converted and validated x .
    """
    if isinstance(accept_sparse,str):
        accept_sparse = [accept_sparse]
    # store whether originally we wanted numeric dtype
    dtype_numeric = dtype == "numeric"
    
    dtype_orig = getattr(array,"dtype",None)
    if not hasattr(dtype_orig,'kind'):
        # not a data type (e.g a colunm named dtype in a paddas DataFrame )
        dtype_orig = None 
    if dtype_numeric:
        if dtype_orig is not None and dtype_orig.kind == '0':
            # if input is object,convert to float 
            dtype = np.float64
        else:
            dtype = None 
    if instance(dtype,(list,tuple)):
        if dtype_orig is not None and dtype_orig in dtype :
            # no dtype conversion required 
            dtype = None 
        else:
            # dtype conversion required ,Let's select the fist element of 
            # the list of passed types 
            dtype = dtype[0]
    if estimator is not None :
        if isinstance (estimator,six.string_types):
            estimator_name = estimator 
        else:
            estimator_name = estimator.__class__.__name__
    else :
        estimator_name = "Estimator"
    context = "by %s"%estimator_name if estimator else""
    
    if sp.issparse(array):
        array = _ensure_sparse_format(array,accept_sparse,dtype,copy,
                                    force_all_finite)
    else :
        array = np.array(array,dtype = dtype,order = order ,copy = copy)
        if ensure_2d :
            if array.ndim == 1 :
                if ensure_min_features >= 2 :
                    raise ValueError("%s expected at least 2 samples "
                                    "provided in a 2 dimensional "
                                    "array-like input"
                                    %estimator_name)
                warnings.warn(
                        "Passing 1d arrays as data is deprecated in " 
                        "0.17 and will raise ValueError in 0.19"
                        "Reshape your data either using x.reshape(-1,1)"
                        "if your data has a single feature or "
                        "x.reshape(1,-1) if it contains a single sample",
                        DeprecationWarning)
            array = np.atleast_2d (array)
            # To ensure that array flags are maitained 
            array = np.array(array,dtype = dtype ,order = order,copy = copy)
        
        # make sure we actually converted to numeric 
        if dtype_numeric and array.dtype.kind == '0':
            array = array.astype(np.float64)
        if not allow_nd and array_ndim > 3:
            raise ValueError("Found array with dim %d,%s expected <=2."
                            % (array.ndim,estimator_name))
        if force_all_finite:
            _assert_all_finite(array)
    shape_repr = _shape_repr(array.shape)
    if ensure_min_samples > 0 :
        n_samples = _num_samples(array)
        if n_samples < ensure_min_samples:
            raise ValueError("Found array with %d sample(s) (shape = %s"
                    ") while a minium of %d is required%s."
                    %(n_samples,shape_repr,ensure_min_samples,context))
    if ensure_min_features > 0 and array.ndim == 2 :
        n_features =array.shape[1]
        if n_features < ensure_min_features:
            raise ValueError ("Found array with %d feature (shape = %d) "
                    "while a minium of %d is required "
                    %(n_features,shape_repr,ensure_min_features))
    if warn_on_dtype and dtype_orig is not None and \
            array.dtype != dtype_orig:
        msg = ("Data with input dtype %s was converted to %s%s"
                % (dtype_orig,array.dtype,context))
        warnings.warn(msg,_DataConversionWarning)
    return array





