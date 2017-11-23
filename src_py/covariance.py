""" The model include methods that count the covariance metrix
of the input matrix
    When using the methods in this module,notice that the similar 
    method in numpy compute the covariances between rows of the 
    input matrix,while methods in this module compute the covariances 
    between columns of the input matrix !!!
"""

import numpy as np 
import warnings

def check_array(array):
    """ This method validate the input array 
    Parameters:
    -----------
    array: array-like, the input array
        
    Returns:
            if the input array is not suitable,we 
            raise a warning or error .
    """
    if not isinstance(array,np.ndarray):
        array = np.asarray(array)
    array_shape = array.shape
    if array.ndim == 1 :
        warnings.warn("The input array's dimension is 1 ,but we"
                    "expect a 2-d array for covariance countint ,"
                    "instead we count the variance of 1-D array !!!")
    if array.ndim > 2 :
        raise ValueError("The given array's dimension is %s ,"
                        "but a 2-D array is expected !!!"
                        % array_shape)
    return array 

def covariance(array):
    """This method compute the covariance matrix of the input array 
    
    Parameters:
    ----------
    array: array-like,
        The input array 

    Returns:
    covariance_array : array-like 
        The covariance matrix (or variance for 1-D input)
    """
    array = check_array(array)
    if array.ndim == 1 :
        # This means that we compute the variance instead of the covariance 
        array_column_sums = array.sum() 
        array_minus_mean = array - array_column_sums / array.shape[0]
        # compute the variance 
        variance = np.sum(array_minus_mean * array_minus_mean)
        return variance
    if array.ndim == 2:
        shape = array.shape
        # compute the covariance matrix 
        array_column_sums = np.sum(array,axis = 1)
        columns_means = array_column_sums / shape[0]
        array_minus_mean = array - columns_means
        # compute tha covariance matrix using the np.dot()
        covariance = np.dot(array_minus_mean.T,array_minus_mean)
        return covariance 


def sum_ij(row_1,row_2):
    return sum([row_1[i] * row_2[i] for i in range(len(row_1))])

def covariance_using_for (array):
    """This method only using the base data structure 
    and control flow,(not using the numpy method)
        Howerver,it is not recommended,for it's  time and 
        source consuming !!!
    """
    # get the shape of the input array
    n_rows= 0
    n_columns = 0
    for i in array:
        n_rows += 1 
    for j in array[0][:]:
        n_columns += 1
    # we fist transpose the array for computation conveinence 
    # and then compute the sum of each row 
    columns_sums = []
    array_transpose = [[row[i] for row in array] for i in range(n_columns) ]
    for column in array_transpose:
        column_sum =sum(column)
        columns_sums.append(column_sum)
    #then compute the means of columns 
    columns_means = [column_sum/n_rows for column_sum in columns_sums]
    # then we minus the mean of each columns
    for i  in range(n_columns):
        mean = columns_means[i]
        array_transpose[i] -= mean 
    # then we compute the covariance matrix 
    covariance_mat = []
    for j in range(n_columns):
        temp = []
        for i in range(n_columns):
            temp_sum = sum_ij(array_transpose[j][:],array_transpose[i][:])
            temp.append(temp_sum)
        covariance_mat.append(temp)
    return covariance_mat
         
