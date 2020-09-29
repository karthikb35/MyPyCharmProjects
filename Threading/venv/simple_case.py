from threading import Thread

class InputReader(Thread):
    def run(self):
        self.test = input('Provide sample input: ')

t = InputReader()
t.start()

c = 1
res = 0

while t.is_alive():
    res = c**2
    c = c+1

print(f'When you were typing: "{t.test}"  i calculated squares of numbers upto : {c} and the result = {res}')
