# Authors : Heqixi
# Date: 2017-11-2 

from ..utils.validation import check_if_fitted
import numpy as np 
from ..utils.validation import column_or_1d

class LabelEncoder():
    """
    Encode labels with value between 0 and n_classes-1

    Attributes:
    -----------
    classes_:array of shape (n_classes,),hold the lables for each class 

    Example:
    -----------
    LabelEncoder can be used to normalize labels    

#  >>> le = LabelEncoder()
#  >>> le.fit([1,2,3,6])
#    LabelEncoder()
#  >>> le.classes_
#  aray([1,2,6])
#  >>> le.transfrom([1,1,2,6])
#    array([0,0,1,2])
#  >>>le.inverse_transfrom([0,0,1,2])
    array([1,1,2,6])
    It can also transfrom non-numerical lables (as long as they are hashable
            and comparable ) to numerical labels 
    """ 
    
    def fit(self,y):
        """ fit label encoder 
        Parameter :
        --------
        y :array_like if shape(n_samples,)
            Target values.
        
        Return :
        ---------
        self : return  an  instance  of  self.
        
        """
        y = column_or_1d(y,warn = True)
        self.classes_,y = np.unique(y,return_inverse = True)
        return y 

    def transfrom(self,y):
        """ Transform labels to normalized enconding .

        Parameters:
        ----------
        y : array-like of shape (n_samples)
            Target valuses 

        Returns:
        --------
        y: array-like of shape (n_samples)
        """
        check_if_fitted (self,'classes_')
        y = column_or_1d(y,warn = True)
        classes = np.unique(y)
        if len(np.intersect1d(classes,self.classes_)) < len(classes):
            diff = np.setdiff1d(classes,self.classes_)
            raise ValueError("y contains new labels : %s " % str(diff))
        return np.searchsorted(self.classes_,y)

    def fit_transform(self,y):
        """ Fit label encoder and return encoders labels
        
        Parameters:
        -----------
        y:  array_like of shape (n_samples,)
            Target values 

        Returns:
        y:  array_like of shape (n_samples,)
            
        """
        y = column_or_1d(y,warn = True)
        self.classes_ ,y = np.unique(y,return_inverse = True)
        return y 

    def _inverse_transform(self,y):
        """ Transform labels back to original encoding 
        
        Parameters :
        -----------
        y : numpy array of shape (n_samples,)
            Target values 
        
        Returns:
        --------
        y : numpy array of shape (n_samples，）
        
        """
        check_if_fitted(self,'classes_')
        diff = np.setdiff1d(y,np.arange(len(self.classes_)))
        if diff:
            raise ValueError ("y contains new labels  %s" % str(diff))
        y = np.asarray(y)
        return self.classes_[y]



