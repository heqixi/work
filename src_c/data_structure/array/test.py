print("testing input statement !!!!")
# to see whether  the function "input" has argument "end"
import inspect
def myFun(x,y):
    print(x+y)

print(inspect.signature(myFun))
print(inspect.signature(input))
print("!!!!!!!!")
print(inspect.getsource(myFun))
