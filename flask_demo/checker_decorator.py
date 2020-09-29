from flask import session
from functools import wraps

def check_login(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if 'logged_in' in session:
            return func(*args,**kwargs)
        return ' You are not logged in'
    return wrapper

class Student:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    def print_name( self ):
        print(self.first + self.last)

    @classmethod
    def cla_me(cls ):
        print('Class method')

    @staticmethod
    def stat_me(  ):
        print('Static method')


a=Student("a","b")
a.print_name()
a.cla_me()
Student.cla_me()
a.stat_me()
Student.stat_me()