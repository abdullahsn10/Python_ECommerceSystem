class User:
    '''
    This class intended for creating user objects with the following proprties: 

    ● User_id (unique integer): a 6-digit unique code for the user
    ● User name (String)
    ● User date of birth (Date)
    ● Role (Integer): the role of the user admin or shopper
    ● Active (Integer): one for active users otherwise not active

For every added user, the system should define two additional attributes:
    ● Basket (dictionary {product_id: number of items}): a dictionary that contains products 
      and the number of items from each product selected for purchase by the user.
      The basket will be empty if the user does not select any items.
    ● Order (integer): one if the user finished adding items to the basket 
      and wants to make an order, otherwise zero.

    '''

    def __init__(self, user_id, user_name, user_dob, role,
                  active, basket=dict(), order=0):
        self.user_id = user_id
        self.user_name = user_name
        self.user_dob = user_dob
        self.role = role
        self.active = int(active)
        self.basket = basket 
        self.order = int(order)
    

    # this function added items for the basket
    def add_item_to_basket(self, product_id, no_of_items): 
        self.basket[product_id] = no_of_items

    # this function make the user order flag 1
    def create_order(self): 
        self.order = 1

    # returns a string represents the user in the file format
    def file_str(self):
        return f'{self.user_id};{self.user_name};{self.user_dob};{self.role};{self.active};{User.format_dict_without_spaces(self.basket)};{self.order}\n'
    
    # this function user for formatting the dictionary
    @staticmethod
    def format_dict_without_spaces(user_dict):
      formatted_str = '{' + ','.join([f'{k}:{v}' for k, v in user_dict.items()]) + '}'
      return formatted_str
    
    # returns a string representing the user
    def __str__(self):
        basket_info = '\t'
        for key,value in self.basket.items():
            basket_info+=f'<Product ID = {key} --> Amount = {value}>\n\t '
        return f'User ID = {self.user_id}\nUser Name = {self.user_name}\nUser DOB = {self.user_dob}\
\nUser Role = {self.role}\nUser Active = {self.active}\nUser Basket = \n{basket_info}\nHas Order = {self.order}'
    

    # update the amount of a product in the basket
    def update_product_amount(self,product_id,new_amount):
        # check for the product if exists in the basket 
        if product_id in self.basket:
            self.basket[product_id] = new_amount
            return True
        else:
            return False
        
    # delete a product from the basket
    def delete_product(self,product_id):
        if product_id in self.basket:
            del self.basket[product_id]
            return True
        else:
            return False

    # clear the user's basket   
    def clear_basket(self):
        self.basket.clear()
