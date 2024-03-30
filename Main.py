# Python E-Commerce System Project - Linux Lab
# Student Name : Abdullah Sami Naser 
# Student ID: 1201952 
# -------------------------------------------------------

from Product import *
from User import *
import Category
from datetime import datetime
from termcolor import termcolor
import pyfiglet

# --------------------------------------------------------------------------

# a list of products in the system
products_list = []

# a list of users in the system
users_list = []

# a list of valid categories, roles
valid_cat = [cat.value for cat in Category.Category] 
valid_roles = ['shopper', 'admin']

# the role , name and index in list of the user who login to the system
role = ''
name = ''
user_index = -1

# --------------------------------------------------------------------------

def is_valid_date(date_str):
    '''
    This function checks if the date is in the form of (DD/MM/YY) or not
    Using the module of datetime

    '''
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True  
    except ValueError:
        return False  
    
# --------------------------------------------------------------------------
def is_user_id_unique(id):
    '''
    This function checks if the id is redundant or not for the user
    '''
    if id in [user.user_id for user in users_list]:
        return False
    else:
        return True

def is_product_id_unique(id):
    '''
    This function checks if the product id is redundant or not
    '''
    if id in [product.product_id for product in products_list]:
        return False
    else:
        return True


# --------------------------------------------------------------------------
def is_this_a_valid_id(id):
    '''
    This function check if the id is valid
    valid means: it is 6 digits ID
    '''
    if len(id) == 6:
        if id.isdigit():
            return True
        else:
            return False

    else:
        return False
# --------------------------------------------------------------------------
def find_product_index(product_id):
    '''
    This function returns two integers found and index
    found: 0 if the product does not exist and 1 if it exists
    index: -1 if the product does not exist and its location in the list if exists
    '''
    found,index = 0,-1
    for idx,prod in enumerate(products_list):
            if prod.product_id == product_id:
                index = idx
                found = 1
    return found,index


def find_user_index(user_id):
    '''
    This function returns two integers found and index
    found: 0 if the user does not exist and 1 if it exists
    index: -1 if the user does not exist and its location in the list if exists
    '''
    found,index = 0,-1
    for idx,user in enumerate(users_list):
            if user.user_id == user_id:
                index = idx
                found = 1
    return found,index

# --------------------------------------------------------------------------
def load_products_file():
    '''
    This function loads the products from a default products.txt file
    and put them in a global products list file

    '''
    # use the global variables
    global products_list
    try: 
        with open('products.txt') as file:
            # read file lines and store in a list of lines
            lines = file.read().splitlines()

            print(termcolor.colored('>> Checking Product File Fields in Progress ...',"blue"))

            # get information from each line, validate and then create prod. object
            for line in lines: 
                data = line.strip().split(';') 
                if len(data) == 9:
                    # checking id field
                    if not is_this_a_valid_id(data[0]) or not is_product_id_unique(data[0]) :
                        print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The '
                                                f'Products File\nID Value Error: {data[0]}', "red"))
                        continue
   
                    # checking category field
                    if  data[2] not in valid_cat:
                        print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The '
                                                f'Products File\nCategory Value Error: {data[2]}', "red"))
                        continue
                    # checking price
                    if  not data[3].isdigit():
                        print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The '
                                                f'Products File\nPrice Value Error: {data[3]}', "red"))
                        continue
                    # checking inventory
                    if  not data[4].isdigit():
                        print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The '
                                                f'Products File\nInventory Value Error: {data[4]}', "red"))
                        continue
                    # checking flag value
                    if  data[6] not in ['0','1']:
                        print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The '
                                                f'Products File\nFlag Value Error: {data[6]}', "red"))
                        continue
                    # checking offer price
                    if  not data[7].isdigit():
                        print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The\
                                                Products File\nOffer Price Value Error: {data[7]}', "red"))
                        continue
                    # checking valid until date
                    if data[8] != '0/0/0' :
                        if  not is_valid_date(data[8]) :
                            print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The '
                                                    f'Products File\nDate Value Error: {data[8]}', "red"))
                            continue

                    # create the product object and append it to the list
                    product_obj = Product(*data)
                    products_list.append(product_obj)
        return True
    except:
        return False
    
# --------------------------------------------------------------------------

def load_users_file():
    '''
    This function loads the users to the system from a default users.txt file
    and put them in a global users_list 
    '''
    global users_list 
    try: 
        with open('users.txt') as file:
            lines = file.read().splitlines()
            print(termcolor.colored('>> Checking Users File Fields in Progress ...',"blue"))

            # split each line's data and create objects
            for line in lines:
                data = line.strip().split(';')
                if len(data) == 7:
                    # checking id field
                    if not is_this_a_valid_id(data[0]) or not is_user_id_unique(data[0]):
                        print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The '
                                                    f'Users File\nID Value Error: {data[0]}', "red"))
                        continue
                    # checking dob 
                    if not is_valid_date(data[2]):
                        print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The '
                                                    f'Users File\nDate Value Error: {data[2]}', "red"))
                        continue
                    # checking role
                    if data[3].lower() not in valid_roles:
                        print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The '
                                                    f'Users File\nRole Value Error: {data[3]}', "red"))
                        continue
                    # checking flag values
                    if data[4] not in ['0','1'] or data[6] not in ['0','1']:
                        print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The '
                                                    f'Users File\nFlag Value Error: {data[4]}', "red"))
                        continue
                    # checking basket
                    try:
                        user_basket = dict() #create an empty basket
                        try:
                            # splitting the fields inside {}
                            basket_pairs = data[5].strip('{}').split(',')
                            for pair in basket_pairs:
                                key, value=pair.split(':')
                                user_basket[key] = int(value)
                        except:
                            pass
                    except:
                        print(termcolor.colored(f'>> ERROR: Invalid Data Detected in The '
                                                    f'Users File\nBasket Error for User: {data[0]}', "red"))
                        continue
                    
                    # create user object and append to the list
                    user_obj = User(data[0],data[1],data[2],data[3].lower(),data[4],user_basket,data[6])
                    users_list.append(user_obj)
        return True
    except:
        return False
    
# --------------------------------------------------------------------------


def add_new_product():
    '''
    This function added a new product to the system with all its fields

    '''
    global products_list
    while True: 
        try: 
            print(termcolor.colored('>> Please Enter The Following Information','blue'))

            # get product id and check its validity
            product_id = input(termcolor.colored('\t\t>> PRODUCT ID: ','blue')).strip()
            if not is_this_a_valid_id(product_id):
                print(termcolor.colored('>> ERROR: Please Enter a 6-digits ID','red'))
                continue
            
            # check if the product id exists already in the system
            if not is_product_id_unique(product_id):
                print(termcolor.colored('>> ERROR: This Is Already an Existing ID','red'))
                return False
            
            # get product name
            product_name = input(termcolor.colored('\t\t>> PRODUCT NAME: ','blue')).strip()

            # get category 
            print(termcolor.colored('\t\tCATEGORIES: ','blue'))
            for idx,cat in enumerate(valid_cat) : 
                print(termcolor.colored(f'\t\t\t{idx}. {cat}','blue'))
            cat_no = int(input(termcolor.colored('\t\t>> CATEGORY NO.: ','blue')).strip())
            try:
                product_category = valid_cat[cat_no]
            except:
                print(termcolor.colored('>> ERROR: Please Enter a Valid Category Number','red'))
                continue

            # get price,inventory and supplier 
            product_price = int(input(termcolor.colored('\t\t>> PRODUCT PRICE $: ','blue')).strip())
            product_inventory = int(input(termcolor.colored('\t\t>> PRODUCT INVENTORY: ','blue')).strip())
            product_supplier = input(termcolor.colored('\t\t>> PRODUCT SUPPLIER: ','blue')).strip()

            # check if the user wants it on the sale
            on_sale = input(termcolor.colored('\t\t>> DO YOU WANT TO PUT THE PRODUCT ON SALE? [Y/N]: ','blue')).strip().lower()
            if on_sale == 'y':
                has_an_offer = 1
            else :
                has_an_offer = 0
                        
            # create the product object
            new_product = Product(product_id,product_name,product_category,
                        product_price,product_inventory,
                        product_supplier,has_an_offer)
            products_list.append(new_product)
            return True

        except:
            print(termcolor.colored('>> ERROR: Please Enter a Valid Input','red'))
            return False

# --------------------------------------------------------------------------


def list_all_products():
    '''
    This function list all products of the system according choices
    1) all products
    2) products with offers
    3) belonging to a specific category
    4) have the same name

    '''
    global products_list
    try:
        # choices 
        print(termcolor.colored('\t\t1. Display All Products\n\t\t2. Display Products with Offers','blue'))
        print(termcolor.colored('\t\t3. Display All Category\'s Products\n\t\t4. Display Products According Name','blue'))
        display_choice = int(input(termcolor.colored('>> Please Enter a Choice for Display: ','blue')).strip())

        print(termcolor.colored('Products in The Shop: ','magenta'))
        print(termcolor.colored('-'*10,'magenta'))

        # display all products
        if display_choice == 1:
            for prod in products_list:
                print(termcolor.colored(prod.__str__(),'magenta'))
                print(termcolor.colored('-'*10,'magenta'))   

        # display products with offer
        elif display_choice == 2:
            for prod in products_list:
                if prod.has_an_offer == 1:
                    print(termcolor.colored(prod.__str__(),'magenta'))
                    print(termcolor.colored('-'*10,'magenta'))  

        # display products belonging to a specefic category
        elif display_choice == 3:
            print(termcolor.colored('\t\tCATEGORIES: ','blue'))
            for idx,cat in enumerate(valid_cat) : 
                print(termcolor.colored(f'\t\t\t{idx}. {cat}','blue'))
            cat_no = int(input(termcolor.colored('>> Please Enter  CATEGORY NO.: ','blue')).strip())
            try:
                for prod in products_list:
                    if prod.product_category == valid_cat[cat_no]:
                        print(termcolor.colored(prod.__str__(),'magenta'))
                        print(termcolor.colored('-'*10,'magenta')) 

            except:
                raise Exception
        
        # display products with specefic name
        elif display_choice == 4:
            prod_name = input(termcolor.colored('>> Please Enter Product Name: ','blue')).strip()
            for prod in products_list:
                if prod.product_name == prod_name:
                    print(termcolor.colored(prod.__str__(),'magenta'))
                    print(termcolor.colored('-'*10,'magenta')) 
        else:
            raise Exception
    except:
        print(termcolor.colored('>> ERROR: Please Enter a Valid Input','red'))
        return
# --------------------------------------------------------------------------

def place_item_on_sale():
    '''
    This function places a product on the sale according its ID
    '''
    global products_list
    try:
        print(termcolor.colored('>> Please Enter The Following Information','blue'))
        # get product id and check its validity
        product_id = input(termcolor.colored('\t\t>> PRODUCT ID: ','blue')).strip()

        # search for the product if it exists and return its index
        found, index = find_product_index(product_id)

        if found:
            print(termcolor.colored('>> Please Enter Sale Information: ','blue'))
            offer_price = int(input(termcolor.colored('\t\t>> OFFER PRICE $: ','blue')).strip())
            valid_until = input(termcolor.colored('\t\t>> VALID UNTIL(DD/MM/YY): ','blue')).strip()

            if not is_valid_date(valid_until):
                raise Exception
            
            # update product info (put on sale)
            products_list[index].place_on_sale(offer_price,valid_until)
            return True
        
        else :
            print(termcolor.colored('>> ERROR: Product Does Not Exist','red'))
            return False
    
    except:
        print(termcolor.colored('>> ERROR: Please Enter a Valid Input','red'))
        return False
    
# --------------------------------------------------------------------------

def update_product():
    '''
    This function update the product fields according its ID
    '''

    global products_list
    try:
        print(termcolor.colored('>> Please Enter The Product ID that You Want to Update its Info: ','blue'))
        # get product id and check its validity
        product_id = input(termcolor.colored('\t\t>> PRODUCT ID: ','blue')).strip()

        # check for the product if it exists 
        found, index = find_product_index(product_id)

        # if the product found in the system
        if found:
            while True:
                # update choices
                print(termcolor.colored('\t\t1. PRODUCT NAME\n\t\t2. PRICE\n\t\t3. CATEGORY','blue'))
                print(termcolor.colored('\t\t4. INVENTORY\n\t\t5. SUPPLIER\n\t\t6. UPDATE HAS AN OFFER','blue'))
                print(termcolor.colored('\t\t7. OFFER PRICE\n\t\t8. OFFER VALID UNTIL DATE','blue'))
                update_choice = int(input(termcolor.colored('>> Please Select Which Field Do You Want to Update: ','blue').strip()))

                # update product name
                if update_choice == 1:
                    product_name = input(termcolor.colored('\t\t>> NEW PRODUCT NAME: ','blue').strip())
                    products_list[index].product_name = product_name
                    cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                    if cont != 'y':
                        return True
                
                # update price
                elif update_choice == 2:
                    product_price = int(input(termcolor.colored('\t\t>> NEW PRICE: ','blue').strip()))
                    products_list[index].price = product_price
                    cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                    if cont != 'y':
                        return True
                    
                # update cateogory 
                elif update_choice == 3:
                    print(termcolor.colored('\t\tCATEGORIES: ','blue'))
                    for idx,cat in enumerate(valid_cat) : 
                        print(termcolor.colored(f'\t\t\t{idx}. {cat}','blue'))
                    cat_no = int(input(termcolor.colored('\t\t>> NEW CATEGORY NO.: ','blue')).strip())
                    try:
                        product_category = valid_cat[cat_no]
                        products_list[index].product_category = product_category
                        cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                        if cont != 'y':
                            return True
                    except:
                        print(termcolor.colored('>> ERROR: Please Enter a Valid Category Number','red'))
                        continue

                # update inventory
                elif update_choice == 4:
                    product_inventory = int(input(termcolor.colored('\t\t>> NEW INVENTORY: ','blue').strip()))
                    products_list[index].inventory = product_inventory
                    cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                    if cont != 'y':
                        return True
                
                # update supplier
                elif update_choice == 5:
                    product_supplier = input(termcolor.colored('\t\t>> NEW SUPPLIER: ','blue').strip())
                    products_list[index].supplier = product_supplier
                    cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                    if cont != 'y':
                        return True
                
                # update has an offer flag
                elif update_choice == 6:
                    print(termcolor.colored(f'\t\t>> CURRENT HAS AN OFFER = {products_list[index].has_an_offer}','blue'))
                    if products_list[index].has_an_offer == 0:
                        products_list[index].has_an_offer = 1
                    else:
                        products_list[index].has_an_offer = 0
                    cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                    if cont != 'y':
                        return True
                
                # update offer price, but first the product must be has an offer
                elif update_choice == 7:
                    if products_list[index].has_an_offer != 1:
                        print(termcolor.colored('>> ERROR: Please Place the Item on Offer First, Or Update the Offer Flag','red'))
                    else:
                        product_offprice = int(input(termcolor.colored('\t\t>> OFFER PRICE: ','blue').strip()))
                        products_list[index].offer_price = product_offprice
                        cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                        if cont != 'y':
                            return True

                # update validity date, but first the product must be has an offer
                elif update_choice == 8:
                    if products_list[index].has_an_offer != 1:
                        print(termcolor.colored('>> ERROR: Please Place the Item on Offer First, Or Update the Offer Flag','red'))
                    else:
                        product_date = input(termcolor.colored('\t\t>> OFFER DATE: ','blue').strip())
                        if not is_valid_date(product_date):
                            raise Exception
                        else:
                            products_list[index].valid_until = product_date
                            cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                            if cont != 'y':
                                return True
        
        else :
            print(termcolor.colored('>> ERROR: Product Does Not Exist','red'))
            return False
    
    except:
        print(termcolor.colored('>> ERROR: Please Enter a Valid Input','red'))
        return False
    
# --------------------------------------------------------------------------

def save_products_to_file(default=True):
    '''
    This function saves the products to a file 
    if default =True --> then the products will be save to a default file (products.txt)
    if default = False --> then the user must input the file name
    '''
    global products_list
    try:
        if not default:
            file_name = input(termcolor.colored('\t\t>> Please Enter the File Name(ends with .txt): ','blue')).strip()
        else:
            file_name = 'products.txt'
        with open(file_name,'a') as file:
            file.truncate(0)
            for prod in products_list:
                file.write(prod.file_str())
            return True

    except:
        print(termcolor.colored('>> ERROR: Something Wrong!!!','red'))
        return False

 # --------------------------------------------------------------------------

def add_new_user():
    '''
    This function added a new user to the system
    '''
    global users_list
    while True: 
        try: 
            print(termcolor.colored('>> Please Enter The Following Information','blue'))

            # get user id and check its validity
            user_id = input(termcolor.colored('\t\t>> USER ID: ','blue')).strip()
            if not is_this_a_valid_id(user_id):
                print(termcolor.colored('>> ERROR: Please Enter a 6-digits ID','red'))
                continue

            # check if the user id exists already in the system
            if not is_user_id_unique(user_id):
                print(termcolor.colored('>> ERROR: This Is Already an Existing ID','red'))
                return False
            
            # get user name
            user_name = input(termcolor.colored('\t\t>> USER NAME: ','blue')).strip()

            # get user dob
            user_dob = input(termcolor.colored('\t\t>> USER DOB (DD/MM/YY) $: ','blue')).strip()
            if not is_valid_date(user_dob):
                print(termcolor.colored('>> ERROR: Please Enter a Valid Date','red'))
                continue

            # get user role
            print(termcolor.colored('\t\t1. Admin\n\t\t2. Shopper','blue'))
            role_choice = int(input(termcolor.colored('\t\t>> Please Enter User Role Choice: ','blue')).strip())
            if role_choice == 1:
                user_role = 'admin'
            elif role_choice == 2:
                user_role = 'shopper'
            else:
                print(termcolor.colored('>> ERROR: Please Enter a Role Choice (1-2)','red'))
                continue

            # get user activity
            active_choice = input(termcolor.colored('\t\t>> IS THE USER ACTIVE [Y/N]: ','blue')).lower()
            if active_choice == 'y':
                user_active = 1
            elif active_choice == 'n':
                user_active = 0
            else:
                print(termcolor.colored('>> ERROR: Please Enter Y/N Only','red'))
                continue

            # create user object
            new_user = User(user_id,user_name,user_dob,user_role,user_active)
            users_list.append(new_user)
            return True

        except:
            print(termcolor.colored('>> ERROR: Please Enter a Valid Input','red'))
            return False
        
 # --------------------------------------------------------------------------

def display_all_users():
    '''
    This function displays all users in the system
    '''
    global users_list

    print(termcolor.colored('Users in The System: ','magenta'))
    print(termcolor.colored('-'*10,'magenta'))

    for user in users_list:
        print(termcolor.colored(user.__str__(),'magenta'))
        print(termcolor.colored('-'*10,'magenta')) 

 # --------------------------------------------------------------------------

def save_users_to_file(default=True):
    '''
    This function saves the users to a file 
    if default = True --> then the users will be save in (users.txt) default file
    if default = False --> then the user must input the file name
    '''
    global users_list
    try:
        if not default:
            file_name = input(termcolor.colored('\t\t>> Please Enter the File Name(ends with .txt): ','blue')).strip()
        else:
            file_name = 'users.txt'
        with open(file_name,'a') as file:
            file.truncate(0)
            for user in users_list:
                file.write(user.file_str())
            return True

    except:
        print(termcolor.colored('>> ERROR: Something Wrong!!!','red'))
        return False

 # --------------------------------------------------------------------------

def update_user():
    '''
    This function intended for updating a user fields , can be accessed by admin only
    all fields of the user can be updated other that its ID

    '''
    global users_list

    try:
        print(termcolor.colored('>> Please Enter The User ID that You Want to Update his/her Info: ','blue'))
        # get user id and check its validity (exists or not)
        usr_id = input(termcolor.colored('\t\t>> USER ID: ','blue')).strip()


        # search for the user if it exists 
        found,index = find_user_index(usr_id)

        # if the user exists then start updating , otherwise error
        if found:
            # menu of updates
            while True:
                print(termcolor.colored('\t\t1. USER NAME\n\t\t2. USER DOB\n\t\t3. ROLE','blue'))
                print(termcolor.colored('\t\t4. ACTIVE\n\t\t5. PLACE ORDER\n\t\t6. USER BASKET','blue'))
                update_choice = int(input(termcolor.colored('>> Please Select Which Field Do You Want to Update: ','blue').strip()))

                # according choice of update , perform operation

                # update name
                if update_choice == 1:
                    user_name = input(termcolor.colored('\t\t>> NEW USER NAME: ','blue').strip())
                    users_list[index].user_name = user_name
                    cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                    if cont != 'y':
                        return True
                
                # update dob
                elif update_choice == 2:
                    user_date = input(termcolor.colored('\t\t>> USER DATE OF BIRTH(DD/MM/YY): ','blue').strip())
                    if not is_valid_date(user_date):
                        raise Exception
                    else:
                        users_list[index].user_dob = user_date
                        cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                        if cont != 'y':
                            return True

                # update role
                elif update_choice == 3:
                    print(termcolor.colored('\t\tROLES: ','blue'))
                    for idx,role in enumerate(valid_roles) : 
                        print(termcolor.colored(f'\t\t\t{idx}. {role}','blue'))
                    role_no = int(input(termcolor.colored('\t\t>> NEW ROLE NO.: ','blue')).strip())
                    try:
                        user_role = valid_roles[role_no]
                        users_list[index].role = user_role
                        cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                        if cont != 'y':
                            return True
                    except:
                        print(termcolor.colored('>> ERROR: Please Enter a Valid Role Choice Number','red'))
                        continue
                
                # update activation
                elif update_choice == 4:
                    print(termcolor.colored(f'\t\t>> CURRENT ACTIVATION = {users_list[index].active}','blue'))
                    if users_list[index].active == 0:
                        users_list[index].active = 1
                    else:
                        users_list[index].active = 0
                    cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                    if cont != 'y':
                        return True
                
                # update order flag
                elif update_choice == 5:
                    print(termcolor.colored(f'\t\t>> CURRENT ORDER FLAG = {users_list[index].order}','blue'))
                    if users_list[index].order == 0:
                        users_list[index].order = 1
                    else:
                        users_list[index].order = 0
                    cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                    if cont != 'y':
                        return True
                
                # update basket
                elif update_choice == 6:
                    # display the basket first
                    print(termcolor.colored(f'\t\t>> USER BASKET CONTENTS: ','blue'))
                    for key,value in users_list[index].basket.items():
                        print(termcolor.colored(f'\t\t\t| PRODUCT: {key} --> AMOUNT: {value} |','blue'))
                    
                    # ask user which type of updates want to do
                    print(termcolor.colored(f'\t\t\t1. UPDATE PRODUCT AMOUNT\n\t\t\t2. REMOVE PRODUCT\n\t\t\t3. ADD PRODUCT','blue'))
                    basket_update_choice = int(input(termcolor.colored(f'\t\t>> PLEASE CHOOSE WHAT OPERATION YOU WANT TO DO: ','blue')))

                    # update a product amount
                    
                    if basket_update_choice == 1:
                        prod_id = input(termcolor.colored(f'\t\t>> PLEASE ENTER PRODUCT ID: ','blue')).strip()
                        new_amount = int(input(termcolor.colored(f'\t\t>> PLEASE ENTER NEW AMOUNT: ','blue')).strip())
                        if users_list[index].update_product_amount(prod_id,new_amount):
                            cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                            if cont != 'y':
                                return True
                        else:
                            print(termcolor.colored('>> ERROR: Product Does Not Exist','red'))
                            continue
                    
                    # remove a product
                    elif basket_update_choice == 2:
                        prod_id = input(termcolor.colored(f'\t\t>> PLEASE ENTER PRODUCT ID: ','blue')).strip()
                        if users_list[index].delete_product(prod_id):
                                cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                                if cont != 'y':
                                    return True
                        else:
                            print(termcolor.colored('>> ERROR: Product Does Not Exist','red'))
                            continue
                    
                    # add a new product
                    elif basket_update_choice == 3:
                        prod_id = input(termcolor.colored(f'\t\t>> PLEASE ENTER PRODUCT ID: ','blue')).strip()
                        found_prod = 0 #flag to tell if the product exists in the system 

                        # search for the product in the system
                        found_prod,_ = find_product_index(prod_id)

                        # if the product found in the system
                        if found_prod:
                            new_amount = int(input(termcolor.colored(f'\t\t>> PLEASE ENTER AMOUNT: ','blue')).strip())
                            users_list[index].basket[prod_id] = new_amount
                            cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                            if cont != 'y':
                                return True
                        else:
                            print(termcolor.colored('>> ERROR: Product Does Not Exist','red'))
                            continue
        
        else :
            print(termcolor.colored('>> ERROR: User Does Not Exist','red'))
            return False
    
    except:
        print(termcolor.colored('>> ERROR: Please Enter a Valid Input','red'))
        return False
# --------------------------------------------------------------------------

def list_all_shoppers():
    '''
    This function list shoppers in the system according some options
    1) all shoppers
    2) shoppers with items in their baskets
    3) shoppers with unprocessed orders (order = 1)

    '''
    try:
        # display choices 
        print(termcolor.colored('\t\t1. Display All Shoppers\n\t\t2. Display Shoppers With Items in Basket','blue'))
        print(termcolor.colored('\t\t3. Display Shoppers with Unprocesses Order','blue'))
        display_choice = int(input(termcolor.colored('>> Please Enter a Choice for Display: ','blue')).strip())

        print(termcolor.colored('Shoppers in The System: ','magenta'))
        print(termcolor.colored('-'*10,'magenta'))

        # display all shoppers
        if display_choice == 1:
            for user in users_list:
                if user.role == 'shopper':
                    print(termcolor.colored(user.__str__(),'magenta'))
                    print(termcolor.colored('-'*10,'magenta'))  

        # display shoppers with items in the basket
        elif display_choice == 2:
            for user in users_list:
                if user.role == 'shopper' and len(user.basket) > 0:
                    print(termcolor.colored(user.__str__(),'magenta'))
                    print(termcolor.colored('-'*10,'magenta')) 

        # display shoppers with unprocessed order
        elif display_choice == 3:
            for user in users_list:
                if user.role == 'shopper' and user.order == 1:
                    print(termcolor.colored(user.__str__(),'magenta'))
                    print(termcolor.colored('-'*10,'magenta')) 
        else:
            raise Exception
    except:
        print(termcolor.colored('>> ERROR: Please Enter a Valid Input','red'))
        return
    
# --------------------------------------------------------------------------

def add_product_to_the_basket():
    '''
    This function add a product to the shopper basket
    The shopper must first logged in to the system
    the product will be added if it is not already exists in its basket

    '''
    # get the global value of the user index (which is shopper location in the list of users)
    global user_index

    try:
        # get the product ID from the user
        prod_id = input(termcolor.colored(f'\t\t>> PLEASE ENTER PRODUCT ID: ','blue')).strip()

        # search for the product in the list of products in the system
        found_prod,prod_loc = find_product_index(prod_id)

        # if the product exists in the system then add it   
        if found_prod:
            if products_list[prod_loc].inventory > 0:
                # if the product was not already in the shopper's basket
                if not prod_id in users_list[user_index].basket:
                    prod_amount = int(input(termcolor.colored(f'\t\t>> PLEASE ENTER AMOUNT: ','blue')).strip())
                    users_list[user_index].add_item_to_basket(prod_id,prod_amount)
                    return True
                else:
                    print(termcolor.colored('>> ERROR: Product is Already Exists in The Basket','red'))
                    return False
            else:
                print(termcolor.colored('>> ERROR: No More items available in this product inventory','red'))
                return False
            
        else:
            print(termcolor.colored('>> ERROR: Product Does Not Exist','red'))
            return False
    except:
        print(termcolor.colored('>> ERROR: Please Enter a Valid Input','red'))
        return False

# --------------------------------------------------------------------------

def exit_menu():
    '''
    This function Exiting the Menu and Asks user to Save Changes in files
    '''

    try:
        save_data = input(termcolor.colored('>> Do You Want To Save Changes Before Exit [Y/N]? ','blue')).lower()
        if save_data == 'y':
            save_products_to_file()
            save_users_to_file()
            print(termcolor.colored('>> Data Saved Successfully in (users.txt) and (products.txt) files','green'))
        elif save_data == 'n':
            pass
        else:
            raise Exception
        
        print(termcolor.colored(pyfiglet.figlet_format('Good Luck <3'),'yellow'))
        return True
    
    except:
        print(termcolor.colored('>> ERROR: Something Wrong Happen!!!','red'))
        return False
    
# --------------------------------------------------------------------------

def display_main_menu():
    '''
    This function prints the main menu choices on the terminal
    '''
    print(termcolor.colored('Main Menu: ',"yellow"))
    print(termcolor.colored("1) Add product\n2) Place an item on sale\n3) Update product",'yellow'))
    print(termcolor.colored("4) Add a new user\n5) Update user\n6) Display all users\n7) List products"
                                ,"yellow"))
    print(termcolor.colored("8) List shoppers\n9) Add product to the basket\n10) Display basket","yellow"))
    print(termcolor.colored("11) Update basket\n12) Place order\n13) Execute order","yellow"))
    print(termcolor.colored("14) Save products to a file\n15) Save Users to a file\n16) Exit","yellow"))

# --------------------------------------------------------------------------

def disply_shopper_basket():

    try:
        print(termcolor.colored('Basket Contents: ','cyan'))
        print(termcolor.colored('-'*10,'magenta'))

        # move for all products in the basket
        for prod,amount in users_list[user_index].basket.items():
            for sys_product in products_list:
                if sys_product.product_id == prod:
                    print(termcolor.colored(sys_product.__str__(),'cyan'))
                    print(termcolor.colored(f'Amount = {amount}','cyan'))
                    print(termcolor.colored(f'Cost of purchase for the product = {int(amount) * sys_product.offer_price}' 
                            if sys_product.has_an_offer else f'Cost of purchase for the product = {int(amount) * sys_product.price}','cyan'))
                    print(termcolor.colored('-'*10,'magenta'))
        print(termcolor.colored(f'Basket total Cost = {get_total_basket_cost(users_list[user_index].basket)}','cyan'))

    except:
        print(termcolor.colored('>> ERROR: Something Wrong Happen!!!','red'))
        return 
    
# --------------------------------------------------------------------------

def get_total_basket_cost(basket):
    '''
    This function return the total cost of items in the basket
    '''
    total_cost = 0
    for prod,amount in basket.items():
        for sys_product in products_list:
            if sys_product.product_id == prod:
                if sys_product.has_an_offer:
                    total_cost += sys_product.offer_price * amount
                else:
                    total_cost += sys_product.price * amount

    return total_cost

# --------------------------------------------------------------------------

def update_shopper_basket():
    '''
    This function updates a shopper's basket :
    1) Update amount of a product in the basket
    2) Remove specific product according ID
    3) Clear all products
    '''

    try:
        while True:
            # display the basket first
            print(termcolor.colored(f'\t\t>> USER BASKET CONTENTS: ','blue'))
            for key,value in users_list[user_index].basket.items():
                print(termcolor.colored(f'\t\t\t| PRODUCT: {key} --> AMOUNT: {value} |','blue'))
                        
            # ask user which type of updates want to do
            print(termcolor.colored(f'\t\t\t1. UPDATE PRODUCT AMOUNT\n\t\t\t2. REMOVE PRODUCT\n\t\t\t3. CLEAR','blue'))
            basket_update_choice = int(input(termcolor.colored(f'\t\t>> PLEASE CHOOSE WHAT OPERATION YOU WANT TO DO: ','blue')))

            # update a product amount
            if basket_update_choice == 1:
                prod_id = input(termcolor.colored(f'\t\t>> PLEASE ENTER PRODUCT ID: ','blue')).strip()
                new_amount = int(input(termcolor.colored(f'\t\t>> PLEASE ENTER NEW AMOUNT: ','blue')).strip())
                if users_list[user_index].update_product_amount(prod_id,new_amount):
                    cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                    if cont != 'y':
                        return True
                else:
                    print(termcolor.colored('>> ERROR: Product Does Not Exist','red'))
                    continue

                        
            # remove a product
            elif basket_update_choice == 2:
                prod_id = input(termcolor.colored(f'\t\t>> PLEASE ENTER PRODUCT ID: ','blue')).strip()
                if users_list[user_index].delete_product(prod_id):
                    cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                    if cont != 'y':
                        return True
                else:
                    print(termcolor.colored('>> ERROR: Product Does Not Exist','red'))
                    continue
                        
            elif basket_update_choice ==3:
                users_list[user_index].clear_basket()
                cont = input(termcolor.colored('>> Do You Want to Continue Updating [Y/N]?: ','blue')).strip().lower()
                if cont != 'y':
                    return True
            
            else:
                raise Exception

    except:
        print(termcolor.colored('>> ERROR: Something Wrong Happen!!!','red'))
        return 

# --------------------------------------------------------------------------

def place_an_order():
    '''
    This function Place an order and displays order information for the shopper
    '''

    try:
       print(termcolor.colored('Order Info: ','cyan'))
       print(termcolor.colored('-'*10,'magenta')) 
       print(termcolor.colored(f'\t\tTotal Cost to Purchase = {get_total_basket_cost(users_list[user_index].basket)}$ ','cyan'))
       users_list[user_index].create_order()
       return True

    except:
        print(termcolor.colored('>> ERROR: Something Wrong Happen!!!','red'))
        return False
    
# --------------------------------------------------------------------------
def execute_order():
    '''
        This function executes an order of a shopper by its ID
        the execution process do these things:
        1) Deduce the amount of the product in the system
        2) clear the user basket
        -----------------
        The execution can be done on a user basket if and only if all products 
        are available
        -----------------

    '''
    try:
        # get the user id from the input
        user_id = input(termcolor.colored('\t\t>>Please Eneter the User ID: ','blue')).strip()
        # check if the user does not exists
        # check if the user placed an order
        user_loc = -1
        for idx,u in enumerate(users_list):
            if u.user_id == user_id:
                if u.order == 1:
                    user_loc = idx

        all_products_in_the_basket = len(users_list[user_loc].basket) #how many products in the basket
        all_done = 0  #this var tells if all products in the basket purchased or not
        purchased_products = [] #list of purchased products

        if user_loc != -1:
            # move for each item in the basket and execute the order
            for user_prod_id,amount in users_list[user_loc].basket.items():
                for product in products_list:
                    if product.product_id == user_prod_id:
                        if product.inventory >= amount:
                            # deduce the amount from the inventory
                            product.inventory -= amount
                            print(termcolor.colored(f'\t\t ✓✓ Product {user_prod_id} Purchased','green'))
                            # put this product in purchased list
                            purchased_products.append(user_prod_id)
                            # increment all_done var
                            all_done += 1
                        
                        else:
                            print(termcolor.colored(f'\t\t XX Product {user_prod_id} Not Available','red'))
                            continue
            if all_done == all_products_in_the_basket:
                # convert order flag for the user
                users_list[user_loc].order = 0
                # remove the basket contents
                users_list[user_loc].basket.clear()

                return True
            else:
                # delete purchased items from the basket
                for prod in purchased_products:
                    del users_list[user_loc].basket[prod]
                    
                print(termcolor.colored('>> Not all Products Available, The Order is not Executed Correctly','red'))
                return False
  
        else:
            print(termcolor.colored('>> ERROR: User Does Not Exist or No Order For this User','red'))
            return False


    except:
        print(termcolor.colored('>> ERROR: Something Wrong Happen!!!','red'))
        return False












# --------------------------------------------------------------------------



def main():
    '''
    This is the main menu function that do all operations of the system

    '''
    # override global var
    global user_index
    global role
    global name
    global users_list
    global products_list

    # welcoming message 
    print(termcolor.colored('-<>-'*6 + 'WELCOME TO OUR ONLINE SHOPPING SYSTEM' + '-<>-'*6, 'yellow') )

    # loading files
    print(termcolor.colored(">> Loading System Files, Please Wait ...", "blue"))
        # products file
    if load_products_file():
        print(termcolor.colored(">> Products File Loaded Successfully", "green"))
    else:
        print(termcolor.colored(">> Products File Loading Failes", "red"))
        exit(0)

        # users files
    if load_users_file():
        print(termcolor.colored(">> Users File Loaded Successfully", "green"))
    else:
        print(termcolor.colored(">> User File Loading Failed", "red"))
        exit(0)
    
    # login the user to the system
    print("")
    print(termcolor.colored('-<>-'*6 + 'LOGIN PAGE' + '-<>-'*6, 'yellow') )
    user_id = input(termcolor.colored('Please Enter User ID: ',"blue")).strip()
    user_found = 0 #flag 
        # check if the user id exists then get its info
    for idx,user in enumerate(users_list):
        if user.user_id == user_id:
            role = user.role
            name = user.user_name
            user_index = idx
            user_found = 1
            print(termcolor.colored('>> Login Successfully', 'green') )

    if not user_found:
        print(termcolor.colored('>> ERROR: Access Denied, User Does not Exists', 'red') )
        exit()
    
    # Menu of the program
    print(termcolor.colored('-<>-'*6 + f'WELCOME {role} {name} TO THE MAIN MENU' + '-<>-'*6, 'yellow') )
    while True:
        if role == 'shopper':
            print(termcolor.colored(f'| Your Basket Total Cost: {get_total_basket_cost(users_list[user_index].basket)}$ | ','cyan'))
        display_main_menu()
        user_choice = int(input(termcolor.colored('>> Please Enter a Choice From The Menu Above: ',"blue")).strip())
        print("")
        # make the operation according to the user choice

        # adding a product 
        if user_choice == 1:
            if role == 'admin' :
                if add_new_product():
                    print(termcolor.colored('>> Product Addedd Successfully','green'))
                else:
                    continue
            else:
                print(termcolor.colored('>> ERROR: Access Denied, Available for Admins Only','red'))
                continue

        # place item on sale
        elif user_choice == 2:
            if role == 'admin':
                if place_item_on_sale():
                    print(termcolor.colored('>> Product Placed on Sale Successfully','green'))
                else:
                    continue
            else:
                print(termcolor.colored('>> ERROR: Access Denied, Available for Admins Only','red'))
                continue

        # update a product info
        elif user_choice == 3:
            if role == 'admin':
                if update_product():
                    print(termcolor.colored('>> Product Updated Successfully','green'))
                else:
                    continue
            else:
                print(termcolor.colored('>> ERROR: Access Denied, Available for Admins Only','red'))
                continue

        # add new user
        elif user_choice == 4:
            if role == 'admin':
                if add_new_user():
                    print(termcolor.colored('>> User Added Successfully','green'))
                else:
                    continue

            else:
                print(termcolor.colored('>> ERROR: Access Denied, Available for Admins Only','red'))
                continue

        # update user info
        elif user_choice == 5:
            if role == 'admin':
                if update_user():
                    print(termcolor.colored('>> User Updated Successfully','green'))
                else:
                    continue
            else:
                print(termcolor.colored('>> ERROR: Access Denied, Available for Admins Only','red'))
                continue

        # display all users
        elif user_choice == 6:
            if role == 'admin':
                display_all_users()
            else:
                print(termcolor.colored('>> ERROR: Access Denied, Available for Admins Only','red'))
                continue

        # list all products
        elif user_choice == 7:
            list_all_products()

        # list all shoppers
        elif user_choice == 8:
            if role == 'admin':
                list_all_shoppers()
            else:
                print(termcolor.colored('>> ERROR: Access Denied, Available for Admins Only','red'))
                continue

        # add product to the basket
        elif user_choice == 9:
            if role == 'shopper':
                if add_product_to_the_basket():
                    print(termcolor.colored('>> Product Added Successfully','green'))
                else:
                    continue
            else:
                print(termcolor.colored('>> ERROR: Access Denied, Available for Shoppers Only','red'))
                continue

        elif user_choice == 10:
            if role == 'shopper':
                disply_shopper_basket()

            else: 
                print(termcolor.colored('>> ERROR: Access Denied, Available for Shoppers Only','red'))
                continue

        elif user_choice == 11:
            if role == 'shopper':
                if update_shopper_basket():
                    print(termcolor.colored('>> Your Basket Updated Successfully','green'))
                else:
                    continue

            else:
               print(termcolor.colored('>> ERROR: Access Denied, Available for Shoppers Only','red'))
               continue 

        elif user_choice == 12:
            if role == 'shopper':
                if place_an_order():
                    print(termcolor.colored('>> Order Created Successfully ','green'))
                else:
                    continue
            else:
               print(termcolor.colored('>> ERROR: Access Denied, Available for Shoppers Only','red'))
               continue 

        elif user_choice == 13:
            if role == 'admin':
                if execute_order():
                    print(termcolor.colored('>> User Order Executed Successully','green'))
                else:
                    continue
            else:
                print(termcolor.colored('>> ERROR: Access Denied, Available for Admins Only','red'))
                continue

        # save products to a file
        elif user_choice == 14:
            if role == 'admin':
                if save_products_to_file(default=False):
                    print(termcolor.colored('>> Products Saved Successfully','green'))
                else:
                    continue
            else:
                print(termcolor.colored('>> ERROR: Access Denied, Available for Admins Only','red'))
                continue

        # save users to a file
        elif user_choice == 15:
            if role == 'admin':
                if save_users_to_file(default=False):
                    print(termcolor.colored('>> Users Saved Successfully','green'))
                else:
                    continue
            else:
                print(termcolor.colored('>> ERROR: Access Denied, Available for Admins Only','red'))
                continue
        
        # exiting the program
        elif user_choice == 16:
            if exit_menu():
                exit()
            else:
                continue
            
        else:
            print(termcolor.colored('>> ERROR: Please choose only from (1-16)\n','red'))
            continue
    

# -------------------------------

if __name__ == '__main__': 
    main()
