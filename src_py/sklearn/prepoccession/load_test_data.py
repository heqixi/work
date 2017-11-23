
from .load_data import load_data_xls 
import time 
from .add_missing import fill_value
import re
from .del_item import missing_infor
from .del_item import mask_to_int
from .del_item import del_column
import csv 
import numpy as np 
from .del_item import mask_to_int,missing_infor
import pandas

with open('./add_missing.py','r') as test_data_file:
    data = []
    for row,item in enumerate(test_data_file.readlines()):
        item = item.strip(',').split(',')
        item.pop()
        item.pop()
        data.append(item)
data = np.asarray(data)
"""
miss_infor = missing_infor(data,thread=0.8)
print(miss_infor)
dele_columns =list(miss_infor.keys())
data = del_column(data,dele_columns)
"""



"""
shape = data.shape
s = ''
test_array = ['',1]
if s in test_array:
    print("success !!!!")
print(data[1,:])
for k in range(shape[0]):
    if k == 0 :
        continue
    if s in data[k,:]:
        print(k,'not suitable !!,continue !')
        continue

    if not s in data[k,:]:
        print(k,"suitable !! please go on !!")
        col_index = np.asarray([n for n in range(shape[1]) if re.search(r"[^0-9,.,e,^,*]+",data[k,n])])
        break
print(col_index)

"""

# testing the fill_mean  in add_missing.py 
print("test begin !!!!!!!!!")
print(data[1,:])
t1 = time.time()
fill_with_mean = fill_value(data,miss_str='')
filled_data = fill_with_mean.fill_mean()
print("!!!!!!!!")
print(filled_data)
