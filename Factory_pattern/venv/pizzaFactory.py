from abc import ABC
import abc
from pizza import pizza

class pizzaFactory(ABC):

    def orderPizza( self, type ):
        pizza = createPizza(type)

        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.pack()

        return pizza

    @abc.abstractmethod
    def createPizza( self, type ):
        raise NotImplemented

class NYPizzaFactory(pizzaFactory):
    def createPizza( self, type ):
        if type == "cheese":
            return NYcheesePizza()
        elif type == "veg":
            return NYvegPizza()
        

class DCPizzaFactory(pizzaFactory):
    def createPizza( self, type ):
        if type == "cheese":
            return DCcheesePizza()
        elif type == "veg":
            return DCvegPizza()

