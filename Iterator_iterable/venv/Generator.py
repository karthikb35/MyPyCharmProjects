# class squaregen:
#     def __init__(self, x):
#         self.x = x
#         self.current = 0
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         if self.current == len(self.x):
#             raise StopIteration
#         a = self.x[self.current] ** 2
#         self.current +=1
#         return a

# def squaregen(l):
#     for _ in l:
#         yield (_*_)
#
# a = squaregen([1,2,3,4])
# for i in a:
#     print(i)
#


from random import random


def generate_colors(count=100):
    for i in range(count):
        yield (random(), random(), random())

i = generate_colors()
for c in i:
    print(c)
x = random()
print(x)