from datetime import datetime
#from memory_profiler import profile

def empty_dec(func_):
    return func_

try:
    profile
except NameError:
    profile = empty_dec

def time_this(func_):
    def inner(*args, **kwargs):
        start_time =  datetime.now()
        ret_vals = func_(*args, **kwargs)
        end_time = datetime.now()
        print("Total time for {}: {}".format(func_.__name__,end_time-start_time))
        return ret_vals
    return inner

@time_this
@profile
def sample():
    print("testing memory and time")
    tmp_ = []
    for i in range(200):
        for j in range(200):
            tmp_.append(i+j)
    print("Length of tmp_",len(tmp_))
    del tmp_

@time_this
@profile
def sample1():
    print("testing memory and time")
    return [range(i) for i in range(500) for j in range(500)] 

sample()
val_ = sample1()
print("Length of sample - out is: ",len(val_))
