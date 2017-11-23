from load_data import load_data_xls
import csv

table = load_data_xls('../data/bank_data.xls',1)
data = table.load_data(1)
data = data[:20]
print(data.shape,"-----> the shape of data")
i = 0 
print (data)
for item  in  enumerate(data[0]):
    if i < 10 :
        i += 1 
        print(item)
