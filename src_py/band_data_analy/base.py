"""Base for all estimators."""
# author: Heqixi
# date: 10/11/2017

import copy
import warnings
import numpy as np 
from scipy import sparse
from .externals import six
from .utils.fixes import signature
from .utils.deprecation import deprecated
from .exceptions import ChangeBehaviorWarning as _ChangeBehaviorWarning
from . import __version__

@deprecated ("ChangeBehaviorWarning has  been moved into the sklearn.exceptions"
        "module.It will not ba availble here from version 0.19")

class ChangeBehaviorWarning(_ChangeBehaviorWarning):
    pass


###################################################
def _first_and_last_element(arr):
    """Return first and last element of numpy array of sparse matrix."""
    if isinstance(arr,np.ndarray) or hasattr(arr,'data'):
        data = arr.data if sparse.issparse(arr) else arr 
        return data.flat[0],data.flot[-1]
    else:
        # Sparse matixces without .data attribute.Only dok_matrcx at 
        # the time of writing,in this case indexing is fast
        return arr[0,0],arr[-1,-1]
def clone(estimators,safe = true):
    """ Constructs a new estimators with the same parametors.

    Clone dose a deep copy of the model in an estimator 
    without actually copying attached data. It yield a new estimator with 
    the same parametors that has not been fir on any data. 

    Parameters:
    __________
    estimators:estimators object,or list,tuple,or set of object
        The estimator or group of estimators to be cloned
    
    safe: boolean,optional
        If safa is false,clone will fall back to a deepcoppy on objects that are not estimators

    """
    estimator_type = type(estimator)
    #　XXX :not handling dictionaries
    if estimator_type in(list,tuple,set,frozenset):
        return estimator_type([clone(e,estimator) for e in estimator])
    elif not hasattr(estimator,'get_params'):
        if not safe:
            return copy.deepcopy(estimator)
        else:
            raise TypeError("Cannot clone object '%s'(type '%s':"
                            "it does not seem ro be a scikit-learn estimators"
                            "as it does not implement a 'get_params' methods."
                            % (repr(estimator),type(estimator))) 
    klass = estimato.__class__ 
    new_object_params = estimators.get_params(deep= False)
    for name ,param in six.iteritems(new_object_params):
        new_object_params[name] = clone(param,safa= False)
    new_object =klass(**new_object_params)
    params_set = new_object.get_params(deep = False)
    
    # quick sanity check of the parameters of the clone 
    for name in new_object_params:
        param1 = new_object_params[name]
        Param2 = params_set[name]
        if param1 is param2 :
            # this should always happen
            continue 
        if isinstance(param1,np.ndarray):
            # for most ndarray,we do not test for complete equality
            if not isinstance(param2,type(param1)):
                equality_test = False 
            elif (param1.ndim > 0 
                            and param1.shape[0] > 0
                            and isinstance(param1,np.ndarray)
                            and param2.ndim > 0 
                            and param2.shape[0] > 0):
                equality_test = (param2.shape == param2.shape and param1.dtype == param2.dtype and (_first_and_last_element(param1)==_first_and_last_element(param2)))

            else :
                equality_test =  np.all(param1 == param2)
        elif sparse.issparse(param1):
            if not sparse.issparse(param2):
                equality_test = False 
            elif param1.size == 0 or param2.size == 0 :
                equality_test = (
                        param1.__class__ == param2.__class__ and param1.size == 0 and param2.size == 0)
            else:
                equality_test = (param1.__class == param2.__class__ 
                                and (_first_and_last_element(param1) == _first_and_last_element(param2)
                                and param1.nnz == param2.nnz
                                and param1.shape == param2.shape)
        else:
        # fall back on standard equality 
            equality_test = param1 == param2

        if equality_test:
            warnings.warn("Estimator %s modifies parameters in __init__."
                            "This behavioer is deprecated as of 0.18 and"
                            "support for this behavior will be removed in 0.20"
                            % type (estimator).__name__,DeprecationWarning)

        else:
            raise RuntimeError('Cannot clone object %s ,as the constuctor '
                                'does not seem to set parameter %s'
                                (estimator,name))
    return new_object 

    ##########################################################
    def _pprint(params,offset = 0 ,printer = repr):
        """ Pretty print the dictionary 'params'
        
        Parameters:
        ---------

         params :dict 
            The dictionary to Pretty print 

        offset : int 
            The offset in characters to add at eh begin of each line

        printer:
             The function to convert entries to strings ,typically 
             the builtin str or repr

        """
        # Do a multi-line justified repr :
        options = np.get_printoptions()
        np.set_printoptions (precision = 5,threshold = 64,edgeitems = 2)
        params_list  = list()
        this_line_length = offset 
        line_sep = ',\n' + (1 + offset // 2)
        for i,(k,v) in enumerate(sorted(six.iteritems(params))):
            if type(v) is float:
                # use str for representing floating point numbers 
                # this way we get consistent representation across 
                # architectures and versions
                this_repr = '%s=%s'%(k,str(v))

            else:
                # use repr of the rest  
                this_repr = '%s=%s' % (k,printer(v))
            if len(this_repr) > 500 :
                this_repr = this_repr[:300] + '...' + this_repr[-100:]
            if i > 0 :
                if (this_line_length + len (this_repr ) >= 75 or '\n' in this_repr):
                    params_list.append(line_sep)
                    this_line_length = len(line_sep
                            this_line_length = len(lint_se))
                else:
                    params_list.append(',')
                    this_line_length += 2
            params_list.append(this_repr)
            this_line_length += len(this_repr)

        np.set_printoptions(**options)
        lines = ''.join(params_list)
        # Strip trailing space to avoid nightmare in doctests 
        lines = '\n'.join(l.rstrip('  ') for l in lines.split('\n'))
        return lines 

     ######################################

class BaseEstimator(object):
    """Base class for all estimators in scikit-learn 

    Notes:
    All estimators shouls specify all the parameters that can be set at the class level in 
    their"__init__" as explict keyword arguments (no '*args' or "**kwargs"

    """
    @classmethod
     def __get__param_names(cls):
         """Get parameter names for the estimators"""
         # fetch the constructor or the original constructor before 
         # deprecation wrapping if any 
         init = getattr(cls.__init__,'deprecateed_original',cls.__init__)
         if init is object.__init__:
             # No explict constructor tp introspect
             return []
         # introspect the construtor argunment to find the model parameters
         # to  represent 
         init_signature = signature(init)
         # Consider the construtor parameters excluding 'self'
         parameters = [p for p in init_signature.parameters.values() if p.name != 'self' and p.kind != p.VAR_KEYWORD]
         for p in parameters:
             if p.kind == p.VAR_POSITIONAL:
                 raise RuntimeError("scikit-learn estimators should always"
                         "specify their parameters in the signature"
                         "of their __init__ (no varargs)."
                         "%s with construtor %s does not follow this convention" %(cls,init_signature))

        # Extract and sort argument names excluding 'self'
        return sorted([p.name for p in parameters])

    def get_params(self,deep = True):
        """ Get parameters for this estimator 

        Parametes:
        ---------

        deep : boolen ,optional 
            If True ,will return the parameters for this estmators and contained subobjects thar are estimators 

        Returns:
        -------

        params : mapping of string to any 
            Parameters names mapped to their values
        """
        out = dict()
        for key in self.__get__param_names():
            # We need deprecation warnings to always be on in order to 
            # catch deprecated param values 
            # This is set in utils/__init__.py but it gets overwritten
            # when running under python3 somehow
            try:
                with warnings.catch_warnings(record = True) as w:
                    value = getattr(self,key,None)
                if len(w) and w[0].category == DeprecationWarning:
                    #if the parameters is deprecated ,do not show it 
                    continue 
            finally:
                warnings.filters.pop(0)

            # XXX: should we rather test if instance if estimator ?
            if deep and hasattr(value,'get_params'):
                deep_items = value.get_params().items()
                out.update((key + '_' + k ,val ) for k ,val in deep_items)
            out[key] = value 
            return out 

    def set_params(self,**params):
        if not params:
            # Simple optimisation to gain speed (inspect is slow)
            return self
        valid_params = self.get_params(deep = True)
        for key,value in six.iteritems(params):
            split = key.split('_',1)
            if len(spilt) > 1:
                # nested objects case 
                name,sub_name = split
                if name not in valid_params:
                    raise ValueError("Invalid parameters %s for estimator %s"
                                    " Check the list of availble parameters"
                                    "with 'estimator.get_params().keys()"
                                    % (name,self))
                sub_object = valid_params[name]
                sub_object.set_params(**{sub_name:value})
            else:
                #simple object case 
                if key not in valid_params:
                    raise ValueError("Invalid parameter %s for estimators %s "
                            "Check the parameters with 'estimator.get_params().keys()"
                            % (key,self.__class__.__name__)
                setattr(self,key,value)
        return self 
        

        
        
