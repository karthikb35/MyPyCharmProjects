class WordIterator:
    def __init__(self, string):
        self.string = string
        self.string_list = [w.capitalize() for w in string.split()]
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == len(self.string_list):
            raise StopIteration
        self.current +=1
        return self.string_list[self.current-1]


# class CapitalIterator:
#     def __init__(self, string):
#         self.words = [w.capitalize() for w in string.split()]
#         self.index = 0
#
#     def __next__(self):
#         if self.index == len(self.words):
#             raise StopIteration()
#
#         word = self.words[self.index]
#         self.index += 1
#         return word
#
#     def __iter__(self):
#         return self

