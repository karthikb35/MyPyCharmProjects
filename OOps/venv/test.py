class test:
    def __init__(self):
        self.a = 'abc'
        

t1 = None

def init_t1():
    global t1
    t1 = test()
    # print(t1.a)
    
