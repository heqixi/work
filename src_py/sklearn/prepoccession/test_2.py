import numpy as np
import csv 

with open('./test_data.csv','r') as test_data_file:
    data = []
    for row,item in enumerate(test_data_file.readlines()):
        item = item.strip(',').split(',')
        item.pop()
        item.pop()
        data.append(item)
data = np.asarray(data)
print(data)
