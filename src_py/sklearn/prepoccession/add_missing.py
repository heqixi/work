import numpy as np 
import re 
from .label import LabelEncoder
from .del_item import missing_infor
from .del_item import del_column
from ..utils.validation import check_is_numeric
from .label import LabelEncoder



""" Thid module deal  add the missing valses 
"""
class fill_value():
    def __init__(self,data,miss_str):
        miss_infor = missing_infor(data,thread =0.8)
        dele_cols = list(miss_infor.keys())
        data = del_column(data,dele_cols)
        data = del_column(data,57)
        self.data = data 
    # the representive string of the missing values 
        self.miss_str = miss_str 
    # check the type of the given data_set 
        if not isinstance(self.data,np.ndarray):
            self.data   = np.asarray(self.data)
            self.shape = self.data.shape

    def _find_missing(self,col_index):
        """
        This method find the missing value and
        return the indexes
        """
        if isinstance(col_index,int):
            template_array = np.zeros(self.data.shape)
            template_array[:,col_index]  = 1
            mask = template_array
        if isinstance(col_index,(list,tuple)):
            mask = np.zeros(self.data.shape)
            for item in col_index:                
                template_array = np.zeros(self.data.shape)
                template_array[:,col_index]  = 1
                mask = template_array + mask
        # construct the masked_array 
        # we only return the mask 

        masked_data = np.ma.array(self.data,mask = mask)
        return masked_data.mask

       
    def _find_numerical_col(self):
        # This method find the indexs of  numerical columns
        shape = self.data.shape
        for k in range(shape[0]):
            if k == 0:
                continue
            if self.miss_str in self.data[k,:]:
                continue
            if not self.miss_str in self.data[k,:]:
                col_index = np.asarray([n for n in range(shape[1]) if not re.search(r"[^0-9,.,^,]+",self.data[k,n])])
                break
        return col_index
            
                
    def fill_mean(self,col_index = -1):
        """
        This method add the missing value with the 
        mean value of the column.
        
        Parameters :
        ----------
            col_index : int,list,or tuple;the column indexs you want 
                to fill ,defauly = -1 ,which means fill add the missing 
                value with the mean value 

        """
        # if the col_index is a int ,just fill the specified column
        # if col_index == -1 ,we fist find all the numerical column
        # and then fill the missing value in these columns
        if col_index == -1:
            print("col_index == -1 ")
            col_index = list(self._find_numerical_col())
            print(col_index)
        if isinstance(col_index,int):
            # get the mean of the target column 
            str2float = np.array(self.data[1:,col_index],dtype = np.float)
            mean = np.mean(str2float)
            #get the index of missing value
            miss_index =self._find_missing(col_index)
            # construct the fill_matric using the mean value 
            fill_matric = np.zeros(self.data.shape) + mean
            #fill the missing value 
            filled_data = np.where(miss_index,fill_matric,self.data)
        if isinstance(col_index,(list,tuple)):
            #  get the mean matric 
            template = np.zeros(self.data.shape)
            for column in col_index:
                # convert string to float 
                print("the untouch data %s !!!!!! "% column)
                print(self.data[1:,column])
                if not check_is_numeric(self.data[1:,column]):
                    print("column %s is non_numeric !!!!!!" %column)
                    myEncoder = LabelEncoder()
                    encoded_column = myEncoder.fit(self.data[1:,column])
                    print("the encoded_column %s !!!!!!!" %column)
                    print(encoded_column)
                    str2float = np.array(encoded_column,dtype = np.float)
                if check_is_numeric(self.data[1:,column]):
                    print("column %s is numeric  !!!!!!!" %column)
                    str2float = np.array(self.data[1:,column],dtype = np.float)
                template[:,column] = np.mean(str2float)
            mean_mat = template 
            miss_index =self._find_missing(col_index)
            filled_data = np.where(miss_index,mean_mat,self.data) 

        return filled_data





