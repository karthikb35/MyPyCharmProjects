from copy import copy, deepcopy

def selection_sort(arr):
    c = 0
    for i in range(len(arr)-1):
        a = i
        for j in range(i,len(arr)):

            if arr[j]<arr[a]:
                a=j
        c += 1
        arr[i] , arr[a] = arr[a], arr[i]     # c+=1
    # print(c)

def bubble_sort(arr):
    flag = True
    c = 0
    j = len(arr)-1
    while flag and j>0:
        flag = False
        # print(arr)
        for i in range(j):
            c += 1
            if arr[i]>arr[i+1]:
                flag = True
                arr[i], arr[i+1] = arr[i+1], arr[i]
        j-=1        # c+=1
    return arr
    # print(c)


def insertion_sort(arr):
    for i in range(1,len(arr)):
        a=arr[i]
        for j in range(i,-1,-1):
            if arr[j]<arr[i]:
                arr[i],arr[j] = arr[j], arr[i]
            else:
                break


# arr = [10,9,8,7,6,5,4,3,2,1]
# # test = deepcopy(arr)
# # selection_sort(arr)
# # print(arr)
# print(bubble_sort(arr))
# # print(test)
# # insertion_sort(test)
# # print(test)