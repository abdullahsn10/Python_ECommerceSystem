class Product:
    '''
    This class intended for creating product objects with the following proprties:

    --> Product_id (unique integer): a 6-digit unique code for the product
    --> Product_name (String): item name such as orange juice bottles, apple juice bottles, banana,
        minced meat (1 kg), teeth brush, …, etc;
    --> Product_category (ENUM): the class of the product. In the system, products are classified into
        categories such as “clothes”, “beauty”, “shoes”, …, etc)
    --> Price (Integer): the price of the product in dollars
    --> Inventory (Integer): number of items available for sale from the product
    --> Supplier (String): the company made the item or the provider how imported the item
    --> Has_on_offer (integer): one if the product is on sale otherwise zero.
    *--> offer_price (integer) : which represents the new reduced price for the product
    *--> valid_until (date) : in which the product will be valid for the offer price until
        some date

    '''

    def __init__(self, product_id, product_name, product_category, price, inventory,
                 supplier, has_an_offer, offer_price=0, valid_until='0/0/0'):
        self.product_id = product_id
        self.product_name = product_name
        self.product_category = product_category
        self.price = int(price)
        self.inventory = int(inventory)
        self.supplier = supplier 
        self.has_an_offer = int(has_an_offer)
        self.offer_price = int(offer_price)
        self.valid_until = str(valid_until.strip())
        
    
    #this function put the product on sale
    def place_on_sale(self, offer_price, valid_until): 
        # update has an offer flag
        self.has_an_offer = 1

        # add new additional info
        self.offer_price = offer_price
        self.valid_until = valid_until


    # this function returns a string represents the product
    def __str__(self):
        return f'Product ID = {self.product_id}\nProduct Name = {self.product_name}\n\
Product Category = {self.product_category}\nPrice = {self.price}\nInventory = {self.inventory}\n\
Supplier = {self.supplier}\nHas an Offer = {self.has_an_offer}\nOffer Price = {self.offer_price}\n\
Valid Until = {self.valid_until}'
    

    # this function returns a string represents the product for the file format
    def file_str(self):
        return f'{self.product_id};{self.product_name};{self.product_category};{self.price};{self.inventory};{self.supplier};{self.has_an_offer};{self.offer_price};{self.valid_until}\n'
    

    

    
