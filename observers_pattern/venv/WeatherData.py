import abc
from Observer import *
class Subject(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__( cls, subclass ):
        return (hasattr(subclass, 'addObserver') and
                callable(subclass.addObserver) and
                hasattr ( subclass, 'removeObserver' ) and
                callable ( subclass.removeObserver ) and
                hasattr ( subclass, 'notify' ) and
                callable ( subclass.notify ) or
                NotImplemented)

    @abc.abstractmethod
    def addObserver( self, Observer ):
        raise NotImplementedError

    @abc.abstractmethod
    def removeObserver( self, Observer ):
        raise NotImplementedError

    @abc.abstractmethod
    def notify( self ):
        raise NotImplementedError

class WeatherData(Subject):
    
    def __init__(self):
        self.observers = []

    def addObserver( self, Observer ):
        self.observers.append(Observer)

    def removeObserver( self, Observer ):
        if Observer in self.observers:
            self.observers.remove(Observer)

    def notify( self ):
        for observer in self.observers:
            observer.update(self.temperature, self.pressure, self.humidity)

    def measurementChanged( self ):
        self.notify()

    def setMeasurements( self, temperature, pressure, humidity ):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.measurementChanged()
        
        