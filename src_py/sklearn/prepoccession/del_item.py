import numpy as np 
from numpy import ma

"""
    This file is to deliete item from original data set 
according to the the give condition .
    You can delite items (rows) by calling the del_rows()
    or to delite columns by calling the function del_cols()
"""
def del_row(data,dict_index_value):
    """ This function delite rows according to the given index 
    and Value 

    Parameters :
    -----------
    data: array_like ,the input data array 

    dict_index_value: dictionary ,whose key include the column numbers ,
                    and  the coresponding Values give the specify 
                    Values according to which you want to deliete
    Return:
    ----------
    del_data: array_like ,the Return del_data """
    # if the type of input data is numpy.ndarray
    # we use the buildin_function in package:numpy
    
    if not isinstance(data,np.ndarray):
        data = np.asarray(data)
    if  isinstance(data,np.ndarray):
        if not isinstance(dict_index_value,(int,dict,str)):
            raise ValueError("the type of  parameter dict_index_value "
                            "should be string  or dict,but a %s is passed "
                            %(type(dict_index_value)))
        # if the parameter dict_index_value is a string or int 
        # We just find the rows that contain the given string 
        # and delete 
        else:
            if isinstance(dict_index_value,str):
                # select the target index 
                print("This call")
                target_row_ind = np.argwhere(data==dict_index_value)

            elif isinstance(dict_index_value,dict):
                 # select the index for original data set 
                 target_row_ind = np.unique(([np.argwhere(data[:,col_ind] == value for col_ind,value in dict_index_value)]))
    origin_row = data.shape[0]
    del_data = np.delete(data,target_row_ind,axis = 0)
    del_row = origin_row - del_data.shape[0]
    print("delete %s rows from given data  "
        % del_row )
    return del_data 

def del_column (data,col_indx):
    if not isinstance(data,np.ndarray):
        data = np.asarray(data)
    if not isinstance(col_indx,(int,list,tuple,str)):
        raise ValueError("The parameter col_indx should be a type"   
                    "of (int,list,tuple)"
                    ".but a type of %s is passed"
                     %type(col_indx))
    target_cols = col_indx 
    if isinstance(col_indx ,str):
        target_cols = np.argwhere(data[0] == col_indx)
        print(target_cols)
    if isinstance(col_indx,(list,tuple)) and isinstance(col_indx[0],str):
        target_cols =[ np.argwhere(data[0] == col_name ) for col_name in col_indx]
    print(target_cols,"target_cols !!!!!!!!")
    oring_col = data.shape[1]
    del_data = np.delete(data,target_cols,axis = 1)
    del_col = oring_col - del_data.shape[1]
    print("delete succeed !!  %s column were deleted from given data "
            % del_col )
    return del_data 
def mask_to_int(data,miss_str):
    """This method construct a int_matrix according to a mask_matrxi
    """
    masked_data = ma.array(data,mask = (data == miss_str))
    mask2int = np.where(masked_data.mask,np.ones(masked_data.mask.shape),np.zeros(masked_data.mask.shape))
    return mask2int

def missing_infor (data,miss_str= "",thread = 0.9):
    """
    This method dislpay the missing information of tha data set 
    
    Parameter:
    ---------
        data :array_like ,the input data set 

        miss_str: str or list of str ,the representive of the miss valus,
                  default  = "  "
    Return :
     
        miss_info: array_like,each row :[[values],[presentages],[miss_info]]

    """
    if not isinstance(data,np.ndarray):
        data = np.asarray(data)
    if isinstance (miss_str,(str,int)):
        miss_str = miss_str
        mask2int = mask_to_int(data,miss_str)
    elif isinstance(miss_str,(list,tuple)):
        miss_str = [str(item) for item in miss_str]
    # construct the mask_matrxi of the input data 
        mask2int = mask_to_int(data,miss_str[0])
        for item in miss_str:
            mask2int = mask2int + mask_to_int(data,item)
        # recostruct the mask2int to 0-1 
        mask2int = np.where(mask2int >0 ,np.ones(mask2int.shape),np.zeros(mask2int.shape))
    # count the sum of the miss_value in each group
    count_miss = np.sum(mask2int,axis = 0)
    #select the columns which miss value 
    col_lens = mask2int.shape[0]
    miss_percentage = count_miss / col_lens
    print(miss_percentage)
    print('11111')
    # the return dict:{column_index:percentage}
    return_dict = {}
    for k,item in enumerate(miss_percentage):
        if item > 0:
            print(str(k) + ': ' + str(item))
        if item > thread:
            return_dict[k] = item 
    return return_dict

            
    
    
