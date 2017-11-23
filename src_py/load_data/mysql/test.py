# get the table and return type :warning
from load_data import load_data_xls
import numpy
import xlrd 

                
# get the table 
table = load_data_xls('./bank_data.xls',1)
# get the header of the table 
header = table.get_header()
print(header)
