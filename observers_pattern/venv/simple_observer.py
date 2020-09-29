class subject:
    def __init__(self):
        self.ob = []
        self._a = ''

    @property
    def a( self ):
        return self._a

    @a.setter
    def a( self, val ):
        self._a = val
        self._update_observer()

    def attach_observer( self, observer ):
        self.ob.append(observer)

    def _update_observer(self):
        for ob in self.ob:
            ob()


class Observer:
    def __init__(self, subject):
        self.subject = subject
        self.subject.attach_observer(self)

    def __call__(self, *args, **kwargs):
        print(self.subject.a)
