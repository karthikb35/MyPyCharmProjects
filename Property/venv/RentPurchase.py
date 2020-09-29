from Property import get_valid_input


class Rental:
    def __init__(self, monthly_rental = '', isFurnished = '', **kwargs):
        super().__init__(**kwargs)
        self.monthly_rental = monthly_rental
        self.isFurnished = isFurnished
        
    def display( self ):
        super().display()
        print("***  RENTAL DETAILS   ***")
        print(f'Monthly Renatal : {self.monthly_rental}')
        print ( f'Is Furnished : {self.isFurnished}')
        
    @staticmethod
    def prompt_init( ):
        return dict(
            monthly_rental = input("What is the monthly rental"),
            isFurnished = get_valid_input("Is it furnished", ("yes" , "no"))
        )

class Purchase:
    def __init__(self, price = '', taxes = '', **kwargs):
        super().__init__(**kwargs)
        self.price = price
        self.taxes = taxes
        
    def display( self ):
        super().display()
        print ( "***  PURCHASE DETAILS   ***" )
        print(f'Price : {self.price}')
        print(f'Taxes: {self.taxes}')
        
    @staticmethod
    def prompt_init( ):
        return dict (
            price=input ( "What is the Price" ),
            taxes=input ( "What is the tax" )
        )
    
