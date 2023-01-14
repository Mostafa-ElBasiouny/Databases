from pymongo import MongoClient
from pprint import pprint
from datetime import date, datetime
import time

client = MongoClient('mongodb://localhost:27017')

database = client['arnolda_8754793']

def validate_integer_input(prompt):
    while True:

        try:
            _ = int(input(prompt + ' > '))
            return _
        except ValueError:
            print('Invalid entry, input not a number.')
            continue

def list_customers():
    customers = database['Customer']
    persons = database['Person']

    print('')
    counter = 0

    for customer in customers.find():
        for person in persons.find():
            if (person['person_id'] == customer['person_id']):
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('Customer ID:      {}'.format(customer['person_id']))
                print('Name:             {}'.format(person['name']))
                print('Telephone:        {}'.format(person['telephone']))
                print('Primary Language: {}'.format(customer['primary_language']))
                print('Date of Birth:    {}'.format(person['dob']))
                print('Address:          {}, {}, {}, {}'.format(person['address']['street'], person['address']['city'], person['address']['province'], person['address']['postal_code']))
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('')
                counter += 1
    
    print('Retrieved {} Records'.format(counter))

def list_orders():
    orders = database['Order']
    persons = database['Person']

    print('')
    counter = 0

    for order in orders.find():
        for person in persons.find():
            if (person['person_id'] == order['person_id']):
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('Order ID:                    {}'.format(order['order_id']))
                print('Customer ID:                 {}'.format(person['person_id']))
                print('Customer Name:               {}'.format(person['name']))
                print('Date of Order:               {}'.format(order['date']))
                print('Credit Authorization Status: {}'.format(order['credit_card_authorization']))
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('')
                counter += 1

    print('Retrieved {} Records'.format(counter))

def list_branches():
    branches = database['Branch']
    customers = database['Customer']

    print('')
    counter = 0
    customers_per_branch = 0

    for branch in branches.find():
        customers_per_branch = 0

        for customer in customers.find():
            if (customer['branch_id'] == branch['branch_id']):
                customers_per_branch += 1

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Branch ID:           {}'.format(branch['branch_id']))
        print('Office Location:     {}'.format(branch['office_location']))
        print('Sales:               {}'.format(branch['sales']))
        print('Number of Customers: {}'.format(customers_per_branch))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('')
        counter += 1

    print('Retrieved {} Records'.format(counter))

def list_items():
    items = database['Item']
    contained_items = database['Item']

    print('')
    counter = 0

    for item in items.find():
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Item ID:        {}'.format(item['item_id']))
            print('Description:    {}'.format(item['description']))
            print('Colour:         {}'.format(item['colour']))
            print('Size:           {}'.format(item['size']))
            print('Pattern:        {}'.format(item['pattern']))
            print('Type:           {}'.format(item['type']))
            for contained_item in contained_items.find():
                if (item['contained_item_id'] == contained_item['item_id']):
                    print('Contained Item: {}'.format(contained_item['description']))

            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('')
            counter += 1

    print('Retrieved {} Records'.format(counter))

def add_customer():
    customer = database['Customer']
    person = database['Person']

    print('')

    branch = input('Branch Number:    ')
    street = input('Street:           ')
    city = input('City:             ')
    province = input('Province:         ')
    postal_code = input('Postal Code:      ')
    name = input('Name:             ')
    telephone = input('Telephone:        ')
    dob_y = input('Year of Birth:    ')
    dob_m = input('Month of Birth:   ')
    dob_d = input('Day of Birth:     ')
    primary_language = input('Primary Language: ')

    print('')
    print('Commit entry to database? (Y, N)')

    choice = input('Choice > ').upper()

    match choice:
        case 'Y':
            print('Committing entry.')
            count = 0
            for i in person.find():
                count += 1

            try:
                person.insert_one({"person_id": count, "name": name, "telephone": telephone, "dob": "{}-{}-{}".format(dob_y, dob_m, dob_d), "address": {"street": street, "city": city, "province": province, "postal_code": postal_code}})
                customer.insert_one({"person_id": count + 1, "account_id": None, "branch_id": branch, "primary_language": primary_language})
            except:
                print('Unable to commit entry, please make sure all fields are properly entered and try again.')
        case _:
            print('Aborting.')

def add_order():
    order = database['Order']

    print('')

    person = input("Customer ID:               ")
    item = input("Item ID:                   ")
    branch = input("Branch ID:                 ")
    authorization = input("Credit Card Authorization: ")

    print('')
    print('Commit entry to database? (Y, N)')

    choice = input('Choice > ').upper()

    match choice:
        case 'Y':
            print('Committing entry.')

            count = 0
            for i in order.find():
                count += 1

            try:
                start = time.perf_counter()
            
                order.insert_one({"order_id": count + 1, "person_id": person, "item_id": item, "branch_id": branch, "date": datetime.now().ctime(), "credit_card_authorization": authorization})
            except:
                print('Unable to commit entry, please make sure all fields are properly entered and try again.')
        case _:
            print('Aborting.')

    stop = time.perf_counter()
    print(f'Request Completed In: {(stop - start) * 1000:0.4f}ms')
    
    print('')

def add_branch():
    branch = database['Branch']

    print('')

    location = input('Office Location: ')

    print('')
    print('Commit entry to database? (Y, N)')

    choice = input('Choice > ').upper()

    match choice:
        case 'Y':
            print('Committing entry.')

            count = 0
            for i in branch.find():
                count += 1

            try:
                start = time.perf_counter()

                branch.insert_one({"branch_id": count + 1, "office_location": location, "sales": 0})
            except:
                print('Unable to commit entry, please make sure all fields are properly entered and try again.')
        case _:
            print('Aborting.')

    stop = time.perf_counter()
    print(f'Request Completed In: {(stop - start) * 1000:0.4f}ms')
    
    print('')

def generate_sales_by_location():
    branches = database['Branch']
    print('')

    counter = 0
    sales = validate_integer_input('Locations with sales greater than')

    print('')
    for branch in branches.find():
        if (branch['sales'] > sales):
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('Branch ID:       {}'.format(branch['branch_id']))
            print('Office Location: {}'.format(branch['office_location']))
            print('Sales:           {}'.format(branch['sales']))
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('')
            counter += 1

    print('Retrieved {} Records'.format(counter))

    print('')

def generate_product_popularity():
    orders = database['Order']
    items = database['Item']
    print('')

    counter = 0
    item_counter = 0
    previous_item_idx = 0
    popularity_dict = {}
    popularity = validate_integer_input('Minimum number of sales')

    print('')
    for order in orders.find().sort("item_id"):
        if (order['item_id'] != previous_item_idx):
            previous_item_idx = order['item_id']
            item_counter = 1
            popularity_dict[previous_item_idx] = item_counter
        else:
            item_counter += 1
            popularity_dict[previous_item_idx] = item_counter

    popularity_dict = dict(sorted(popularity_dict.items(), key=lambda x: x[1], reverse=True))

    for i in popularity_dict:
        for item in items.find().sort("item_id"):
            if (i == item['item_id'] and popularity_dict[i] >= popularity):
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('Product ID:  {}'.format(item['item_id']))
                print('Description: {}'.format(item['description']))
                print('Popularity:  {}'.format(popularity_dict[i]))
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('')
                counter += 1

    print('Retrieved {} Records'.format(counter))

    print('')

def generate_customer_loyalty():
    orders = database['Order']
    customers = database['Customer']
    persons = database['Person']
    print('')

    counter = 0
    item_counter = 0
    previous_item_idx = 0
    popularity_dict = {}
    popularity = validate_integer_input('Minimum number of purchases')

    print('')
    for order in orders.find().sort("person_id"):
        if (order['person_id'] != previous_item_idx):
            previous_item_idx = order['person_id']
            item_counter = 1
            popularity_dict[previous_item_idx] = item_counter
        else:
            item_counter += 1
            popularity_dict[previous_item_idx] = item_counter

    popularity_dict = dict(sorted(popularity_dict.items(), key=lambda x: x[1], reverse=True))

    for i in popularity_dict:
        for customer in customers.find().sort("person_id"):
            if (i == customer['person_id'] and popularity_dict[i] >= popularity):
                for person in persons.find():
                    if (person['person_id'] == customer['person_id']):
                        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                        print('Customer ID:      {}'.format(customer['person_id']))
                        print('Name:             {}'.format(person['name']))
                        print('Primary Language: {}'.format(customer['primary_language']))
                        print('Purchases:        {}'.format(popularity_dict[i]))
                        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                        print('')
                        counter += 1

    print('Retrieved {} Records'.format(counter))

    print('')
