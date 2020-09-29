import  time, datetime

def logging(f):
    def wrapper_func(*args, **kwargs):
        now = time.time()
        print(f"{f.__name__} called at {time.time()}")
        return_val = f(*args, **kwargs)
        print(f"{f.__name__} finished at {time.time()} with value {return_val}")
        return return_val
    return wrapper_func

@logging
def test(a,b):
    print(f'Calling test and sleeping {b} second(s)')
    time.sleep(b)
    print(f'Value of a is {a}')

test(3,3)

