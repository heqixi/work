import xlrd
import numpy as np 
def load_data():
    my_file = xlrd.open_workbook("./data/data_zdn_1.xls")
    table = my_file.sheet_by_index(0)
    n_rows = table.nrows 
    n_cols = table.ncols 
    print (table.row_values(1))
    data = np.array(table.row_values(i) for i in range(n_rows))
    return data
data = load_data()
print(data.shape)


