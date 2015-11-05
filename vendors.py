__author__ = 'Sebastian.Law'

# todo: not sure it's appropriate to have 'text_to_array' and 'extract' functions in this file

import re
import csv
import ast
import files
import transaction


def text_to_array(text, start_from=None):
    array = re.split('\\n', text, maxsplit=0, flags=0)
    array = [l.strip() for l in array if l.strip() != '']
    if start_from is not None:
        for i, line in enumerate(array):
            if line == start_from:
                break
        if i != len(array)-1:
            array = array[i:]
    return array


def extract(lines, parameter):
    assert(len(parameter) == 4)
    tag = parameter[0]
    offset = parameter[1]
    split_string = parameter[2]
    split_element = parameter[3]
    if tag is None:
        return None
    else:
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


def load_vendors():
    vendors = [Stubhub(), Getmein(), Viagogo(), Seatwave()]
    return vendors


class Vendor:
    def __init__(self):
        self._ID = None
        self._tag = None
        self._sale_start_tag = None
        self._date_format = None
        self._key_parameters = None
        self.processTime = None

    def _import_parameters(self):
        file = open(files.parameters_file, 'r', newline='')
        reader = csv.reader(file, delimiter=",")
        regex_parameters = [r for r in reader]
        file.close()
        keys = [r[1] for r in regex_parameters if r[0] == self._ID]
        parameters = [r[2:] for r in regex_parameters if r[0] == self._ID]
        transaction_keys = transaction.Sale().get_dict().keys()
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
            print("transaction keys do not match those in the source file relating to " + self._ID)
        for p, parameter in enumerate(parameters):
            if parameters[p][0] == 'None':
                parameters[p][0] = None
            parameters[p][1] = ast.literal_eval(parameters[p][1])
            if parameters[p][2] == 'None':
                parameters[p][2] = None
            parameters[p][3] = ast.literal_eval(parameters[p][3])
        self._key_parameters = dict(zip(keys, parameters))

    def get_id(self):
        return self._ID

    def gmail_folder(self):
        return 'SaleConfirms/' + self._ID

    def extract_transaction(self, lines):
        if self._key_parameters is not None:
            t = transaction.Sale()
            for key, value in self._key_parameters.items():
                result = extract(lines, value)
                t.set_data_item(key, result)
            return t
        else:
            print("Parameters not imported")
            return None


class Stubhub(Vendor):
    def __init__(self):
        self._ID = 'STUB'
        self._tag = 'stubhub'
        self._sale_start_tag = "Hi Stephen,"
        self._date_format = '%a, %d/%m/%Y, %H:%M'
        self._import_parameters()


class Getmein(Vendor):
    def __init__(self):
        self._ID = 'GET'
        self._tag = 'getmein'
        self._sale_start_tag = "Order Summary"
        self._date_format = '%A, %d %B %Y %H:%M'
        self._import_parameters()


class Viagogo(Vendor):
    def __init__(self):
        self._ID = 'VIA'
        self._tag = 'viagogo'
        self._sale_start_tag = "Order Information"
        self._date_format = '%d %B %Y, %H:%M'
        self._import_parameters()


class Seatwave(Vendor):
    def __init__(self):
        self._ID = 'SEAT'
        self._tag = 'seatwave'
        self._sale_start_tag = "Sale confirmation"
        self._date_format = '%d/%m/%Y %H:%M'
        self._import_parameters()
