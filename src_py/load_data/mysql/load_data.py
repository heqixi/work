import numpy as np 
import xlrd as xr 
import xlwt as xw  
class load_data_xls():

    def __init__(self,file_dir,sheet_index = -1):
        self.file_dir = file_dir 
        self.sheet_index = sheet_index 
        self.workbook = xr.open_workbook(self.file_dir)
        print("open file success !!!!")

    def check_parameter(self):
        if not  isinstance(self.file_dir,str):
            raise ValueError("this input argument %s is not a valid diretory"
                                %self.file_dir)

        sheet_len = len([self.workbook.sheet_names])
        if not isinstance(self.sheet_index,int):
            raise ValueError("the input Parameter 'sheet_index' :%s"
                                "expected to a int type number"
                                "but a type of  %s is is given "
                               % (self.sheet_index,type(self.sheet_index)))
            if self.sheet_index != -1 or 0 < self.sheet_index or self.sheet_index > sheet_len:
                raise ValueError ("the value of sheet_index should be -1 or int between"
                                    "0 and %s"
                                    % sheet_len)
    def get_header(self,sheet_index = -1):
        """
            This method is to get the header of the target table 
        Parameter:
        ---------
        sheet_index : int ,the index of the target table 
        """
        n_sheets = len([self.workbook.sheet_names])
        if sheet_index != -1:
            current_sheet =self.workbook.sheet_by_index(sheet_index-1)
            return current_sheet.row_values(0)
        else:
            headers = []
            for i in range(n_sheets):
                current_sheet = self.workbook.sheet_by_index(i)
                headers.append(current_sheet.row_values(0))
            return headers

    def load_data(self,sheet_index = -1):
        """
        This methods read data from a xls file.
        
        Parameters :
        -----------
        file:  URL, the diretory of the target file in your computer

        sheet_index : int ,optional ,the sheet index you want to read from 
                    your file. the default value is '-1',which means return 
                    all the sheets in the file .
        Return:
        -------
        """
  
        my_sheet =[self.workbook.sheet_names]  # get the sheet of the workbook
        sheet_len = len(my_sheet)  #get the number of the sheet in the workbook

        # read the data from the workbook,
        # We use a np.array to store the data in each sheet 
        # and we use a np_array to store all the asarray
        data = []
        for i in range(sheet_len):
            current_sheet =self.workbook.sheet_by_index(i)
            # get the number of row and column of the sheet 
            n_rows = current_sheet.nrows 
            n_cols = current_sheet.ncols 
            print(n_rows,"->>the row of current_sheet")
            # read the data from the current_sheet 
            data.append(np.asarray([current_sheet.row_values(i) for i in range(n_rows)]))
        # retrun data 
        data = np.asarray(data)
        if sheet_index == -1:
            return_data = data 
        else:
            return_data = np.asarray([data[i-1] for i in range(sheet_index)])
        return return_data
            
    
           
        

