from multiprocessing import Process, cpu_count
from threading import Thread
import time
import os

class test(Process):
    def run( self ):
        print(os.getpid())
        for i in range(20000000):
            # time.sleep(1)
            pass


if __name__ == '__main__':
    t = time.time()
    print(cpu_count())
    process_lists = [test() for c in range(cpu_count())]
    for p in process_lists:
        p.start()

    for p in process_lists:
        p.join()

    print(f' Work took : {time.time()-t} seconds')