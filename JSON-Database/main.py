import time
from database import *

# Create a new database object and pass the data file name.
database = Database('records.json')

# Clears the console.
def clear():
    os.system('cls')

# Validates user input.
# If 'max' is passed then the 'value' is treated as an int and validated accordingly.
# If 'max' is not passed then the 'value' is treated as a string and validated accordingly.
def validate(value, max=0):
    if not max:
        if len(value) > 0 and len(value) <= 24:
            return True
    else:
        try:
            if int(value) > 0 and int(value) <= max:
                return True
        except: pass
    
    return False

# Main program loop.
while True:
    clear()

    # Display the menu.
    print('1: STOP')
    print('2: INSERT')
    print('3: DELETE')
    print('4: FIND')
    print('5: RANDOM')

    selection = input('> ')

    # Match the user selection.
    match selection:
        case '1': # Stop the program.
            print('Stopping.')
            exit(0)
        case '2': # Insert a new record.
            clear()
            print('Insert new record.')

            # Get all the data fields from the user.
            SPSID = input('SPSID: ')
            while not validate(SPSID):
                print('(SPSID) can not be less than 1 character or more than 24 characters, try again!')
                SPSID = input('SPSID: ')

            FieldID = input('FieldID: ')
            while not validate(FieldID, 255):
                print('(FieldID) can not be less than 1 or more than 255, try again!')
                FieldID = input('FieldID: ')

            LFuel = input('LFuel: ')
            while not validate(LFuel, 350):
                print('(LFuel) can not be less than 1 or more than 350, try again!')
                LFuel = input('LFuel: ')

            LProduct = input('LProduct: ')
            while not validate(LProduct, 1200):
                print('(LProduct) can not be less than 1 or more than 1200, try again!')
                LProduct = input('LProduct: ')

            ProductID = input('ProductID: ')
            while not validate(ProductID):
                print('(ProductID) can not be less than 1 character or more than 24 characters, try again!')
                ProductID = input('ProductID: ')
            
            # Create a new dictionary (record) using the user input.
            record = {key: eval(key) for key in ['SPSID', 'FieldID', 'LFuel', 'LProduct', 'ProductID']}

            # Start the timer before calling the database.
            start = time.perf_counter()
            database.insert(record)
            # Stop the timer after the database executes.
            stop = time.perf_counter()
            print('Record inserted!')
            # Print the time taken by the operation.
            print(f'Time taken: {(stop - start) * 1000:0.4f}ms')
            input('Press [ENTER] to continue.')
        case '3': # Deletes records by their 'SPSID'.
            clear()
            print('Delete record by (SPSID).')

            SPSID = input('SPSID: ')
            while not validate(SPSID):
                print('(SPSID) can not be less than 1 character or more than 24 characters, try again!')
                SPSID = input('SPSID: ')
            
            start = time.perf_counter()
            records_deleted = database.delete(SPSID)
            stop = time.perf_counter()

            if records_deleted > 0:
                print(f'({records_deleted}) record(s) deleted!')
                print(f'Time taken: {(stop - start) * 1000:0.4f}ms')
                input('Press [ENTER] to continue.')
            else:
                print('No records found matching given (SPSID).')
                input('Press [ENTER] to continue.')
        case '4': # Finds records by their 'SPSID' or finds all records.
            clear()
            print('Find a record by (SPSID) or show all records.')

            loop = True

            while loop:
                print('1: Find by (SPSID)')
                print('2: Show all records')

                selection = input('> ')

                match selection:
                    case '1':
                        SPSID = input('SPSID: ')
                        while not validate(SPSID):
                            print('(SPSID) can not be less than 1 character or more than 24 characters, try again!')
                            SPSID = input('SPSID: ')

                        start = time.perf_counter()
                        records_found = database.find(SPSID)
                        stop = time.perf_counter()

                        if records_found > 0:
                            print(f'({records_found}) record(s) found matching given (SPSID)!')
                            print(f'Time taken: {(stop - start) * 1000:0.4f}ms')
                        else:
                            print('No records found matching given (SPSID).')

                        input('Press [ENTER] to continue.')
                        loop = False
                    case '2':
                        start = time.perf_counter()
                        records_found = database.find()
                        stop = time.perf_counter()

                        if records_found > 0:
                            print(f'({records_found}) record(s) found!')
                            print(f'Time taken: {(stop - start) * 1000:0.4f}ms')
                        else:
                            print('There are no records.')

                        input('Press [ENTER] to continue.')
                        loop = False
                    case _:
                        print('Invalid entry, please try again!\n')
        case '5': # Randomly generates x number of records.
            clear()
            print('Random records generation.')

            loop = True

            while loop:
                records_count = input('Number of records: ')

                try:
                    if int(records_count) > 0:
                        start = time.perf_counter()
                        database.random(int(records_count))
                        stop = time.perf_counter()
                        print(f'Time taken: {(stop - start) * 1000:0.4f}ms')
                        loop = False
                        input('Press [ENTER] to continue.')
                except:
                    print('Invalid entry, please try again!')
        case _: # Catches any invalid entries.
            print('Invalid entry, please try again!')
            input('Press [ENTER] to retry.')