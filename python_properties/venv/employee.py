class emp:
    def __init__(self,f,l):
        self._f = f
        self.l = l

    @property
    def f(self):
        return self._f

    # @f.setter
    # def f( self, f ):
    #     self._f = f

    @property
    def fn(self):
        return f'{self._f} {self.l}'

    @fn.setter
    def fn( self, fn ):
        self._f,self.l = fn.split()


e = emp('k','b')
print(e.fn)
e.fn = 'a y'
print(e.f , e.l)
# e.f = 'k'
print(e.f , e.l)