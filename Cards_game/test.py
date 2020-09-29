def count_hi ( str ):
    c = 0
    it=0
    global i
    for i in range ( len ( str ) - 1 ):
        it= it+1
        if (str[i] + str[i + 1]) == 'hi':
            c = c + 1
            next(i)
    print(it)
    return c
print(count_hi('hihihi hihihi'))