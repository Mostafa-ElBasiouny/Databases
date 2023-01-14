import os
import time
from database import *


# Clears the console.
def clear():
    os.system('cls')


while True:
    clear()

    print('1. List')
    print('2. Add')
    print('3. Generate Report')
    print('4. Stop')

    selection = input('> ')

    match selection:
        case '1':  # List.
            clear()

            print('1. Customers')
            print('2. Orders')
            print('3. Branches')
            print('4. Items')

            inner_selection = input('List > ')

            match inner_selection:
                case '1':  # Customers.
                    clear()
                    print('Listing Customers.')
                    start = time.perf_counter()
                    list_customers()
                    stop = time.perf_counter()
                    print(
                        f'Request Completed In: {(stop - start) * 1000:0.4f}ms')
                    input('Press [ENTER] to continue.')
                case '2':  # Orders.
                    clear()
                    print('Listing Orders.')
                    start = time.perf_counter()
                    list_orders()
                    stop = time.perf_counter()
                    print(
                        f'Request Completed In: {(stop - start) * 1000:0.4f}ms')
                    input('Press [ENTER] to continue.')
                case '3':  # Branches.
                    clear()
                    print('Listing Branches.')
                    start = time.perf_counter()
                    list_branches()
                    stop = time.perf_counter()
                    print(
                        f'Request Completed In: {(stop - start) * 1000:0.4f}ms')
                    input('Press [ENTER] to continue.')
                case '4':  # Items.
                    clear()
                    print('Listing Items.')
                    start = time.perf_counter()
                    list_items()
                    stop = time.perf_counter()
                    print(
                        f'Request Completed In: {(stop - start) * 1000:0.4f}ms')
                    input('Press [ENTER] to continue.')
                case _:
                    print('Invalid entry, please try again!')
                    input('Press [ENTER] to retry.')
                    continue
        case '2':  # Add.
            clear()

            print('1. Customer')
            print('2. Order')
            print('3. Branch')

            inner_selection = input('Add > ')

            match inner_selection:
                case '1':  # Customer.
                    clear()
                    print('Add Customer.')
                    add_customer()
                    input('Press [ENTER] to continue.')
                case '2':  # Order.
                    clear()
                    print('Add Order.')
                    add_order()
                    input('Press [ENTER] to continue.')
                case '3':  # Branch.
                    clear()
                    print('Add Branch.')
                    add_branch()
                    input('Press [ENTER] to continue.')
                case _:
                    print('Invalid entry, please try again!')
                    input('Press [ENTER] to retry.')
                    continue
        case '3':  # Generate Report.
            clear()

            print('1. Employees That Are Customers')
            print('2. Customers That Own an Account')
            print('3. Branches Sales')

            inner_selection = input('Generate > ')

            match inner_selection:
                case '1': # Employees that are customers.
                    clear()
                    print('Querying Employees That Are Customers.')
                    start = time.perf_counter()
                    report_employees_and_customers()
                    stop = time.perf_counter()
                    print(
                        f'Request Completed In: {(stop - start) * 1000:0.4f}ms')
                    input('Press [ENTER] to continue.')
                case '2': # Customers that own an account.
                    clear()
                    print('Querying Customers That Owns an Account.')
                    start = time.perf_counter()
                    report_customers_with_account()
                    stop = time.perf_counter()
                    print(
                        f'Request Completed In: {(stop - start) * 1000:0.4f}ms')
                    input('Press [ENTER] to continue.')
                case '3': # Branches sales.
                    clear()
                    print('Querying Branches Sales.')
                    start = time.perf_counter()
                    report_branches_sales()
                    stop = time.perf_counter()
                    print(
                        f'Request Completed In: {(stop - start) * 1000:0.4f}ms')
                    input('Press [ENTER] to continue.')
                case _:
                    print('Invalid entry, please try again!')
                    input('Press [ENTER] to retry.')
                    continue
        case '4':  # Stop.
            print('Stopping program.')
            close_database()
            exit(0)
        case _:
            print('Invalid entry, please try again!')
            input('Press [ENTER] to retry.')
            continue
