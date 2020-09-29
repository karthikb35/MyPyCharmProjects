# import random
# for i in dir(random):
#     print(str(i))
#     try:
#         print("for: " + i+ "\n\n" + help(str(i)) + "\n")
#     except:
#         print("-----")

# i='asd'
# print((''.join(i)).join('qqqqq'))

# vowels = ['a', 'e', 'i', 'o','u']
# word = input("please input :")
# found = []
# for letter in word:
#     if letter.lower() in vowels:
#         if letter.lower() not in found:
#             found.append(letter.lower())
# found.sort()
# print(found)

vowels = {'a','u','i','o','e'}
vowels_list=['a','u','i','o','e']
so=sorted(vowels_list)
print(sorted(vowels))
word='hello'
print(sorted(vowels.union(word)))
print(sorted(vowels.intersection(word)))
print(tuple('hello')[-1:0])
t=set('sdsdsd')
print(t)
print(bool(set('asdfrsx')))