import os
import json
import random
import string

class Database:
    def __init__(self, name):
        self.name = name

        # If the data file does not exist or exists but empty; then create and initialize the file.
        if not os.path.exists(name) or os.stat(name).st_size == 0:
            with open(name, 'w') as _:
                # All records will be added under the list 'records'.
                _.writelines('{"records":[]}')
    
    def insert(self, record):
        # Open the file for read and write.
        with open(self.name, 'r+') as _:
            # Load all data into 'records'.
            records = json.load(_)
            # Append the new user given record onto our list 'records'.
            records['records'].append(record)
            # Change the write pointer to the absolute file position.
            _.seek(0)
            # Dump the updated 'records' back to the data file.
            json.dump(records, _, indent=4)

    def delete(self, spsid):
        # Open the data file for read only.
        with open(self.name, 'r') as _:
            # Counter to keep track of deleted records.
            deletes = 0
            records = json.load(_)

            # Loop through each record and delete records that have matching 'SPSID'.
            for _ in range(len(records['records'])):
                for idx, record in enumerate(records['records']):
                    if record['SPSID'] == spsid:
                        del records['records'][idx]
                        deletes += 1

        # Open the data file for write only.
        with open(self.name, 'w') as _:
            json.dump(records, _, indent=4)

        # Return the number of deleted records.
        return deletes

    def find(self, spsid=None):
        with open(self.name, 'r') as _:
            records = json.load(_)
            records_found = 0

            # Checks if we have to find records by matching 'SPSID'.
            if spsid != None:
                for idx, record in enumerate(records['records']):
                    if record['SPSID'] == spsid:
                        print(f"# {idx + 1}\n(SPSID):\t{record['SPSID']}")
                        print(f"(FieldID):\t{record['FieldID']}")
                        print(f"(LFuel):\t{record['LFuel']}")
                        print(f"(LProduct):\t{record['LProduct']}")
                        print(f"(ProductID):\t{record['ProductID']}")
                        records_found += 1
            # Otherwise just print all records.
            else:
                for idx, record in enumerate(records['records']):
                    print(f"# {idx + 1}\n(SPSID):\t{record['SPSID']}")
                    print(f"(FieldID):\t{record['FieldID']}")
                    print(f"(LFuel):\t{record['LFuel']}")
                    print(f"(LProduct):\t{record['LProduct']}")
                    print(f"(ProductID):\t{record['ProductID']}")
                    records_found += 1

        # Return the number of records found.
        return records_found

    def random(self, amount):
        # Loops x number of time based on the amount specified.
        for _ in range(amount):
            # Randomly generate a combination of characters and digits.
            SPSID = random.choices(string.ascii_uppercase, k=12) + random.choices(string.digits, k=12)
            # Shuffle the generated random string to create mixed characters and digits.
            random.shuffle(SPSID)
            # Join the generated random string from a literal string (list of chars) to a single string.
            SPSID = ''.join(SPSID)
            # Generate a random number between the specified range.
            FieldID = random.randrange(1, 256)
            LFuel = random.randrange(1, 351)
            LProduct = random.randrange(1, 1201)
            ProductID = random.choices(string.ascii_uppercase, k=12) + random.choices(string.digits, k=12)
            random.shuffle(ProductID)
            ProductID = ''.join(ProductID)

            # New dictionary to hold all our data fields.
            record = {}
            record = dict({
                'SPSID': SPSID,
                'FieldID': FieldID,
                'LFuel': LFuel,
                'LProduct': LProduct,
                'ProductID': ProductID
            })

            # Insert the new dictionary (record) to the data file.
            self.insert(record)

        # Print the number of records that were randomly inserted.
        print(f'Inserted ({amount}) new random records!')