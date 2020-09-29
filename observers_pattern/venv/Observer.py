import abc,WeatherData

class observer(metaclass=abc.ABCMeta):
    def __subclasshook__( cls, subclass ):
        return (hasattr(subclass, 'update') and
                callable(subclass.update) or
                NotImplemented)

    @abc.abstractmethod
    def update( self,temperature, pressure, humidity ):
        raise NotImplementedError

class DisplayElement(metaclass=abc.ABCMeta):
    def __subclasshook__( cls, subclass ):
        return (hasattr(subclass, 'display') and
                callable(subclass.display) or
                NotImplemented)

    @abc.abstractmethod
    def display( self ):
        raise NotImplementedError


class CurrentConditionsDisplay(observer,DisplayElement):
    def __init__(self, weatherData):
        self.weatherData = weatherData
        weatherData.addObserver(self)

    def update( self,temperature, pressure, humidity ):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.display()

    def display( self ):
        print(f'Current Temp:{self.temperature} \n'\
                  f'Current pressusre: {self.pressure} \n'\
              f'Curent Humidity: {self.humidity}'
              )



class Heatindex(observer, DisplayElement):
    def __init__(self, weatherData):
        self.weatherData = weatherData
        weatherData.addObserver(self)

    def update( self,temperature, pressure, humidity ):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.display()

    def display( self ):
        print(f'Heat Index : {self.temperature + self.humidity/100 }\n')