import numpy as np 
import functools 
import time
"""
test_array = np.ones((2,5))
print(np.all(test_array > 1,axis = 1))
all_result = test_array.all(axis = 1)

test_meg = "testing decorator !!!!!!!!"
print(test_meg)
def test_fun():
    print ( time.time())
def log(fun):
    def wrapper(*args,**kwargs):
        print("this is the decorated message !!")
    return wrapper
@log
def new_fun(meg = "this is the new fuction !!!!"):
    print(meg)

new_fun()

msg =" the 2-layer decorator !!!!"
print (msg)
def log(text):
    
    def decorator(fun): 
        @functools.wraps(fun)
        def wrapper (*args,**kwargs):
            fun(*args,**kwargs)
            print(text)
        return wrapper
    return decorator
@log("this is a 2-layer decorator !!!!")
def new_fun(x,y):
    print (x+y ,"the result !!!!")

new_fun(1,2)
print(new_fun.__name__)
"""
from covariance_using_for import covariance 
from covariance import covariance as covariance_1 

test_array =np.array([[1,1],[2,2],[1,1]]).T
test_array_1 = test_array.T
print(test_array_1)
print("!!!!!!")
result = covariance(test_array_1)
result_2 = covariance_1(test_array_1)
print("!!!!!")
print(result)
print(result_2)
result_1 = np.cov(test_array)
print('!!!!!!!')
print(result_1)
