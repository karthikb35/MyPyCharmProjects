from Property import Property, House,Apartment
from RentPurchase import Rental,Purchase

class HouseRental(Rental, House):
    @staticmethod
    def prompt_init( ):
        init = House.prompt_init()
        init.update(Rental.prompt_init())
        return init

class HousePurchase(Purchase,House):
    @staticmethod
    def prompt_init( ):
        init = House.prompt_init()
        init.update(Purchase.prompt_init())
        return init

class ApartmentRental(Rental,Apartment):
    @staticmethod
    def prompt_init( ):
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init

class ApartmentPurchase(Purchase,Apartment):
    @staticmethod
    def prompt_init( ):
        init = Apartment.prompt_init()
        init.update(Purchase.prompt_init())
        return init

