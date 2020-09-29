from TxnHandler import HouseRental,HousePurchase,ApartmentRental,ApartmentPurchase
from Property import get_valid_input

class agent:
    type_map = {
        ("house", "rental"): HouseRental,
        ("house", "purchase"): HousePurchase,
        ("apartment", "rental"): ApartmentRental,
        ("apartment", "purchase"): ApartmentPurchase
    }

    def __init__(self):
        self.property_list = []

    def displayPropery( self ):
        for property in self.property_list:
            print()
            property.display()
            print()

    def add_property( self ):
        property = get_valid_input("What type of Property?", ("house", "apartment"))
        payment = get_valid_input("What type of Payment?", ("rental", "purchase"))
        Prop_class = agent.type_map[(property, payment)]
        x=Prop_class.prompt_init()
        self.property_list.append(Prop_class(**x))

    def action( self ):
        while True:
            menu_dict = {
                "1" : self.displayPropery,
                "2" : self.add_property,
                "3" : exit
            }
            disp = input("1. Display all properties\n"
                         "2. Add Properties\n"
                         "3. Exit\n"
                         "Enter your input: ")
            menu_dict[disp]()

if __name__ == "__main__":
    agent().action()

