from merge_sort import merge_sort
from selection_sort import selection_sort, bubble_sort, insertion_sort
from quicksort import quickie
from random import randint
from copy import deepcopy
import time

l = [randint(1,1000000) for i in range(10000)]
# merge_list = deepcopy(l)
# selection_list = deepcopy(l)
# bubble_list = deepcopy(l)
# insertion_list = deepcopy(l)
# quick_list = deepcopy(l)

def timer(sorting_algo, array):
    now = time.time()
    sorting_algo(array)
    after = time.time()
    print(f'Time taken for {sorting_algo.__name__} is {after-now}')
    # print(f"")


if __name__ == '__main__':
    start = time.time()
    
    for i in [quickie,  insertion_sort, merge_sort, bubble_sort, selection_sort ]:
        timer(i, deepcopy(l))
    
    BIn = deepcopy(l)
    
    now = time.time()
    BIn.sort()
    then = time.time()
    print(f"Time taken for Built-in sort is {then-now}")
    print('++'*10)
    print(f'Time taken to test = {time.time()-start}')