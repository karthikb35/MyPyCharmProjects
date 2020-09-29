from WeatherData import WeatherData
from Observer import CurrentConditionsDisplay, Heatindex

s = WeatherData()
o = CurrentConditionsDisplay(s)
h = Heatindex(s)
s.setMeasurements(25, 30.1, 43)
s.setMeasurements(31, 42, 54)
