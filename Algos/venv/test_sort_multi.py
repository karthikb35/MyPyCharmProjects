from merge_sort import merge_sort
from selection_sort import selection_sort, bubble_sort, insertion_sort
from quicksort import quickie
from random import randint
from copy import deepcopy
import time

def builtin_sort(arr):
    arr.sort()

from test_sort import timer, l
from multiprocessing import Process

if __name__ == '__main__':
    start = time.time()
    sorting_algos = [ selection_sort, bubble_sort, quickie,  insertion_sort, merge_sort, builtin_sort  ]
    process_lists=[]
    for algo in sorting_algos:
        process = Process(target=timer, args=(algo,deepcopy(l)))
        process_lists.append(process)
        process.start()

    for process in process_lists:
        process.join()

    print(f'Entire test-script ran in {time.time()-start}')

