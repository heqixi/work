"""
    This model display the information of given data set 
"""

class data_infor():
    """The class need a array to initialied 
    """


    def __init__(self,data):
        self.data = data 
    
    # check the type of the given data_set 
    if not isinstance(self.data,np.ndarray):
        self.data   = np.asarray(self.data)
    self.shape = self.data.shape
    def valuesFrequence(self):
        """the input data set must be 1-dimention array
        """
        if 
