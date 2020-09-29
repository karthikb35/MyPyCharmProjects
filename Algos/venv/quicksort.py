def quickie(arr):
    if len(arr)<2:
        return arr
    else:
        left, centre, right = [] , [], []
        pivot = arr[-1]
        for a in arr:
            if a < pivot:
                left.append(a)
            elif a == pivot:
                centre.append(a)
            else:
                right.append(a)
        # centre.append(pivot)
        return quickie(left) + centre + quickie(right)


# l = [9,5,4,1,6]
# r = [2,7,3,8,10]
# print(quickie([8,6,5,1,2,5]))
