""" 
    The :mod :'sklearn.exception ' module includes all custom 
wainings and error classes used across scikit-learn .
"""
__all__ = ['NotFittedError']

class NotFittedError(ValueError,AttributeError):
    """ Exception classes to raise if estimator is used before fitting

    This class inherits from both ValueError and AttributeError to 
    help with Exception handling and backward compatibility.

    Example:
#   >>> from sklearn.svm import LinearSVC
#   >>> from sklearn.exceptions import NotFittedError 
#    try:
#       LinearSVC().predict([1,3],[3,5]]
#    except NotFittedError as e :
#        print(repr(e))
    """
    
    

