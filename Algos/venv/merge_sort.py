def merge_sort(arr):
    if len ( arr ) > 1:
        mid = len ( arr ) // 2  # Finding the mid of the array
        L = arr[:mid]  # Dividing the array elements
        R = arr[mid:]  # into 2 halves

        merge_sort ( L )  # Sorting the first half
        merge_sort ( R )  # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len ( L ) and j < len ( R ):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len ( L ):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len ( R ):
            arr[k] = R[j]
            j += 1
            k += 1



def merge_call(arr):
    if len(arr)<2:
        return arr[:]
    else:
        mid = len(arr)//2
        l = merge_call(arr[:mid])
        r = merge_call(arr[mid:])
        return merge_sort(l,r)


# l = [9,5,4,1,6]
# r = [2,7,3,8,10]
# 
# # print(merge_sort(l,r))
# arr = l+r
# print(merge_sort(arr))
# print(arr)