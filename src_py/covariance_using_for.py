import numpy as np

def sum_ij(row_1,row_2):
    return sum([row_1[i] * row_2[i] for i in range(len(row_1))])
    

def covariance (array):
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
    
