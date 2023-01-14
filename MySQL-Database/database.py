from datetime import date, datetime
import time

import mysql.connector

cnx = mysql.connector.connect(user='root', password='1234',
                              host='127.0.0.1',
                              database='arnolda_yourcondorid')  # 8754793.


def list_customers():
    cursor = cnx.cursor()
    query = ("SELECT c.primary_language, p.person_id, p.name, p.telephone, p.dob, a.street, a.city, a.province, a.postal_code FROM customer AS c "
             "INNER JOIN person p "
             "INNER JOIN address a "
             "ON c.person_id = p.person_id AND p.person_id = a.person_id")
    cursor.execute(query)
    print('')

    counter = 0

    for (primary_language, person_id, name, telephone, dob, street, city, province, postal_code) in cursor:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Customer ID:      {}'.format(person_id))
        print('Name:             {}'.format(name))
        print('Telephone:        {}'.format(telephone))
        print('Primary Language: {}'.format(primary_language))
        print('Date of Birth:    {}'.format(dob))
        print('Address:          {}, {}, {}, {}'.format(
            street, city, province, postal_code))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('')
        counter += 1

    print('Retrieved {} Records'.format(counter))

    cursor.close()


def list_orders():
    cursor = cnx.cursor()
    query = ("SELECT p.name, c.person_id, o.date, o.credit_card_authorization, o.order_id FROM arnolda_yourcondorid.order AS o "
             "INNER JOIN customer c "
             "INNER JOIN person p "
             "ON c.person_id = o.person_id AND p.person_id = c.person_id")
    cursor.execute(query)
    print('')

    counter = 0

    for (name, person_id, date, credit_card_authorization, order_id) in cursor:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Order ID:      {}'.format(order_id))
        print('Customer ID:   {}'.format(person_id))
        print('Customer Name: {}'.format(name))
        print('Date of Order: {}'.format(date))
        print('Credit Authorization Status: {}'.format(credit_card_authorization))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        counter += 1
        print('')

    print('Retrieved {} Records'.format(counter))

    cursor.close()


def list_branches():
    cursor = cnx.cursor()
    query = ("SELECT b.branch_id, b.office_location, b.sales, COUNT(c.branch_id) FROM branch b "
             "INNER JOIN customer c ON c.branch_id = b.branch_id "
             "GROUP BY b.branch_id "
             "ORDER BY COUNT(c.branch_id) DESC")
    cursor.execute(query)
    print('')

    counter = 0

    for (branch_id, office_location, sales, customers_count) in cursor:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Branch ID: {}'.format(branch_id))
        print('Office Location: {}'.format(office_location))
        print('Sales: {}'.format(sales))
        print('Number of Customers: {}'.format(customers_count))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        counter += 1
        print('')

    print('Retrieved {} Records'.format(counter))
    
    cursor.close()


def list_items():
    cursor = cnx.cursor()
    query = ("SELECT i.item_id, i.description, i.colour, i.size, i.pattern, i.type, c.description FROM item i "
             "LEFT JOIN item c ON i.contained_item_id = c.item_id "
             "GROUP BY i.item_id ")
    cursor.execute(query)
    print('')

    counter = 0

    for (item_id, description, colour, size, pattern, type, contained_items) in cursor:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Item ID:        {}'.format(item_id))
        print('Description:    {}'.format(description))
        print('Colour:         {}'.format(colour))
        print('Size:           {}'.format(size))
        print('Pattern:        {}'.format(pattern))
        print('Type:           {}'.format(type))
        print('Contained Item: {}'.format(contained_items))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        counter += 1
        print('')

    print('Retrieved {} Records'.format(counter))
    
    cursor.close()


def add_customer():
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

            try:
                start = time.perf_counter()
                cursor = cnx.cursor()
                customer = ("INSERT INTO customer "
                            "(person_id, account_id, branch_id, primary_language) "
                            "VALUES (%s, %s, %s, %s)")
                address = ("INSERT INTO address "
                           "(person_id, street, city, province, postal_code) "
                           "VALUES (%s, %s, %s, %s, %s)")
                person = ("INSERT INTO person "
                          "(name, telephone, dob) "
                          "VALUES (%s, %s, %s)")
                cursor.execute(person, (name, telephone, date(
                    int(dob_y), int(dob_m), int(dob_d))))
                id = cursor.lastrowid
                cursor.execute(
                    address, (id, street, city, province, postal_code))
                cursor.execute(customer, (id, None, branch, primary_language))
                cnx.commit()
                cursor.close()
            except:
                print(
                    'Unable to commit entry, please make sure all fields are properly entered and try again.')
                cursor.close()

        case _:
            print('Aborting.')

    
    stop = time.perf_counter()
    print(f'Request Completed In: {(stop - start) * 1000:0.4f}ms')

    print('')


def add_order():
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

            try:
                start = time.perf_counter()
                cursor = cnx.cursor()
                order = ("INSERT INTO arnolda_yourcondorid.order "
                         "(person_id, item_id, branch_id, date, credit_card_authorization) "
                         "VALUES (%s, %s, %s, %s, %s)")

                cursor.execute(order, (person, item, branch,
                               datetime.now().date(), authorization))
                cnx.commit()
                cursor.close()
            except:
                print(
                    'Unable to commit entry, please make sure all fields are properly entered and try again.')
                cursor.close()
        case _:
            print('Aborting.')

    stop = time.perf_counter()
    print(f'Request Completed In: {(stop - start) * 1000:0.4f}ms')
    
    print('')


def add_branch():
    print('')

    location = input('Office Location: ')

    print('Commit entry to database? (Y, N)')

    choice = input('Choice > ').upper()

    match choice:
        case 'Y':
            print('Committing entry.')

            try:
                start = time.perf_counter()
                cursor = cnx.cursor()
                branch = ("INSERT INTO branch "
                          "(office_location, sales) "
                          "VALUES (%s, %s)")
                cursor.execute(branch, (location, 0))
                cnx.commit()
                cursor.close()
            except:
                print(
                    'Unable to commit entry, please make sure all fields are properly entered and try again.')
                cursor.close()
        case _:
            print('Aborting.')

    stop = time.perf_counter()
    print(f'Request Completed In: {(stop - start) * 1000:0.4f}ms')
    
    print('')


def report_employees_and_customers():
    cursor = cnx.cursor()
    query = ("SELECT e.person_id, e.branch_id, e.date_of_hire, e.title, e.salary, c.primary_language, p.name FROM employee AS e "
             "INNER JOIN customer c "
             "INNER JOIN person p ON p.person_id = c.person_id "
             "ON e.person_id = c.person_id")
    cursor.execute(query)
    print('')

    counter = 0

    for (person_id, branch_id, date_of_hire, title, salary, primary_language, name) in cursor:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Person ID:        {}'.format(person_id))
        print('Branch ID:        {}'.format(branch_id))
        print('Name:             {}'.format(name))
        print('Date of Hire:     {}'.format(date_of_hire))
        print('Title:            {}'.format(title))
        print('Salary:           {}'.format(salary))
        print('Primary Language: {}'.format(primary_language))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        counter += 1
        print('')

    print('Retrieved {} Records'.format(counter))
    
    cursor.close()


def report_customers_with_account():
    cursor = cnx.cursor()
    query = ("SELECT c.person_id, c.primary_language, c.account_id, a.payment_date, a.payment_amount FROM customer AS c "
             "INNER JOIN account a "
             "ON c.account_id = a.account_id")
    cursor.execute(query)
    print('')

    counter = 0

    for (person_id, primary_language, account_id, payment_date, payment_amount) in cursor:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Customer ID:      {}'.format(person_id))
        print('Primary Language: {}'.format(primary_language))
        print('Account ID:       {}'.format(account_id))
        print('Payment Date:     {}'.format(payment_date))
        print('Payment Amount:   {}'.format(payment_amount))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        counter += 1
        print('')

    print('Retrieved {} Records'.format(counter))
    
    cursor.close()


def report_branches_sales():
    cursor = cnx.cursor()
    query = ("SELECT b.branch_id, b.office_location, b.sales FROM branch AS b "
             "ORDER BY sales DESC")
    cursor.execute(query)
    print('')

    counter = 0

    for (branch_id, office_location, sales) in cursor:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Branch ID:       {}'.format(branch_id))
        print('Office Location: {}'.format(office_location))
        print('Sales:           {}'.format(sales))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        counter += 1
        print('')

    print('Retrieved {} Records'.format(counter))
    
    cursor.close()


def close_database():
    cnx.close()
