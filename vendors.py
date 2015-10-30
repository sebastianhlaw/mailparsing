__author__ = 'Sebastian.Law'

# External libraries
import datetime
import re
import csv

# Local files
import files
import transaction


# Load the regex parameters from external csv file for a given id
def get_parameter_map(id):
    file = open(files.parameters_file, 'r', newline='')
    reader = csv.reader(file, delimiter=",")
    regex_parameters = [r for r in reader]
    file.close()
    keys = [r[1] for r in regex_parameters if r[0] == id]
    parameters = [r[2:] for r in regex_parameters if r[0] == id]
    transaction_keys = transaction.Sale().get_data().keys()
    checks = [False]*len(transaction_keys)
    for i, k in enumerate(transaction_keys):
        for key in keys:
            if k == key:
                checks[i] = True
                break
    check = True
    for i in checks:
        if i is False:
            check = False
    if check is False:
        print("transaction keys do not match those in the source file relating to " + id)
    return dict(zip(keys, parameters))


def extract(lines, tag, offset, split_string=None, split_element=None):
    # TODO: this function should probably be in the transaction class
    s = None
    for i, l in enumerate(lines):
        if l.startswith(tag):
            if offset > 0:
                s = lines[i+offset]
            elif offset is 0:
                s = l.replace(tag, '')
            break
    if s is not None:
        if split_string is not None and split_element is not None:
            s = (re.split(split_string, s))[split_element]
        s = s.replace('£', '').strip()
    return s


class Vendor:
    def __init__(self):
        self._ID = None
        self._tag = None
        self.processTime = None

    def gmail_folder(self):
        return 'SaleConfirms/' + self._ID

    def extract_transaction(self, lines):
        t = transaction.Sale

        return t

    def get_headings(self):
        return ['processTime', 'reseller'] + [i for i in self._sale_keys]

    def get_data(self):
        return [self.processTime, self._ID] + self._values

class Stubhub(Vendor):
    def __init__(self):
        self._ID = 'STUB'
        self._tag = 'stubhub'
        self._sale_start_tag = "Hi Stephen,"

        self._date_format = '%a, %d/%m/%Y, %H:%M'

    def cleanDate(self, i):
        self._values[i] = datetime.datetime.strptime(self._values[i].replace("BST", "").replace("GMT", "").strip(), self._date_format)

class Getmein(Vendor):
    def __init__(self):
        self._ID = 'GET'
        self._tag = 'getmein'
        self._sale_start_tag = "Order Summary"
        self._date_format = '%A, %d %B %Y %H:%M'

    def cleanDate(self, i):
        self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)

class Viagogo(Vendor):
    def __init__(self):
        self._ID = 'VIA'
        self._tag = 'viagogo'
        self._sale_start_tag = "Order Information"
        self._date_format = '%d %B %Y, %H:%M'

    def cleanDate(self, i):
        self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)

class Seatwave(Vendor):
    def __init__(self):
        self._ID = 'SEAT'
        self._tag = 'seatwave'
        self._sale_start_tag = "Sale confirmation"
        self._date_format = '%d/%m/%Y %H:%M'

    def cleanDate(self, i):
        self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)
