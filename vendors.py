__author__ = 'Sebastian.Law'

# todo: not sure it's appropriate to have 'text_to_array' functions in this file

import re
import csv
import ast
import files
import transaction
import datetime


def text_to_array(text, start_from=None):
    text = text.replace(">", " ").replace("<", " ").replace("\t", " ").replace("*", " ").replace("|", "\n")  # todo: put these in the approporiate trade-specific replacement
    array = re.split("\\n", text, maxsplit=0, flags=0)
    array = [l.strip() for l in array if l.strip() != '']
    if start_from is not None:
        for i, line in enumerate(array):
            if line == start_from:
                break
        if i != len(array)-1:
            array = array[i:]
    return array


def load_vendors():
    vendors = [Stubhub(), Getmein(), Viagogo(), Seatwave()]
    # vendors = [Stubhub(), Getmein(), Viagogo(), Seatwave(), Stubhub2()]
    return vendors


class Vendor:
    def __init__(self):
        self._ID = None
        self._tag = None
        self._sale_start_tag = None
        self._date_format = None
        self._time_format = None
        self._key_parameters = [None]
        self._versions = None
        # self.processTime = None

    def _bespoke_replacements(self, text):
        return text

    def _get_parameter_version(self, text):
        return 1

    def _import_parameters(self):
        file = open(files.parameters_file, 'r', newline='')
        reader = csv.reader(file, delimiter=",")
        regex_parameters = [r for r in reader]
        file.close()
        self._key_parameters = [None]*self._versions
        for v in range(self._versions):
            identifier = self._ID if v == 0 else self._ID+str(v+1)
            keys = [r[1] for r in regex_parameters if r[0] == identifier]
            parameters = [r[2:] for r in regex_parameters if r[0] == identifier]
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
                print("transaction keys do not match those in the source file relating to " + identifier)
            for p, parameter in enumerate(parameters):
                if parameters[p][0] == 'None':
                    parameters[p][0] = None
                parameters[p][1] = ast.literal_eval(parameters[p][1])
                if parameters[p][2] == 'None':
                    parameters[p][2] = None
                parameters[p][3] = ast.literal_eval(parameters[p][3])
            self._key_parameters[v] = dict(zip(keys, parameters))

    def get_id(self):
        return self._ID

    def get_gmail_folder(self):
        return 'SaleConfirms/' + self._ID

    def extract_transaction(self, text):
        if self._key_parameters is [None]:
            print("Parameters not imported")
            return
        text = self._bespoke_replacements(text)
        version = self._get_parameter_version(text) - 1
        lines = text_to_array(text, self._sale_start_tag)
        # print("version:", version)
        t = transaction.Sale()
        for key, parameter in self._key_parameters[version].items():
            result = self.extract(lines, parameter, key)
            t.set_data_item(key, result)
        t.set_process_time()
        return t

    def extract(self, lines, parameter, key):
        assert(len(parameter) == 5)
        tag = parameter[0]
        offset = parameter[1]
        split_string = parameter[2]
        split_element = parameter[3]
        data_type = parameter[4]
        if tag is None:
            return None
        else:
            string = None
            for i, l in enumerate(lines):
                if l.startswith(tag):
                    if offset is None:
                        if l.replace(tag, '').strip() == '':
                            offset = 1
                        else:
                            offset = 0
                    if offset == 0:
                        string = l.replace(tag, '')
                    else:
                        string = lines[i+offset]
                    break  # exit once we've found the tag
            if string is not None:
                if split_string is not None and split_element is not None:
                    try:
                        string = (re.split(split_string, string))[split_element]
                    except Exception as e:
                        print("Error: ", str(e))
                        print(" key:          \t", key)
                        print(" tag:          \t", tag)
                        print(" string:       \t", string)
                        print(" split_string: \t", split_string)
                        print(" split_element:\t", split_element)
                        print("--------------------------------------------------------")
                        string = "ERROR"
                string = string.strip()
                try:
                    if data_type == 'int':
                        string = ast.literal_eval(string.replace(" ", ""))
                    elif data_type == 'price':
                        string = ast.literal_eval(string.replace(" ", "").replace("£", "").replace("GBP", ""))
                    elif data_type == 'date':
                        string = str(datetime.datetime.strptime(string.strip(), self._date_format).date())
                    elif data_type == 'time':
                        string = str(datetime.datetime.strptime(
                            string.replace("BST", "").replace("GMT", "").strip(), self._time_format))
                except Exception as e:
                    print("Error: ", str(e))
                    print(" key:          \t", key)
                    print(" tag:          \t", tag)
                    print(" string:       \t", string)
                    print(" data_type:    \t", data_type)
                    print("--------------------------------------------------------")
                    string = "ERROR"
                return string


class Stubhub(Vendor):
    def __init__(self):
        self._ID = 'STUB'
        self._tag = 'stubhub'
        self._sale_start_tag = "Hi Stephen,"
        self._date_format = '%d/%m/%Y'
        self._time_format = '%a, %d/%m/%Y, %H:%M'
        self._versions = 2
        self._import_parameters()

    def _get_parameter_version(self, text):
        if "----------------------------------------" in text:
            return 2
        else:
            return 1


class Getmein(Vendor):
    def __init__(self):
        self._ID = 'GET'
        self._tag = 'getmein'
        self._sale_start_tag = "Order Summary"
        self._date_format = '%A, %d %B %Y'
        self._time_format = '%A, %d %B %Y %H:%M'
        self._versions = 1
        self._import_parameters()


class Viagogo(Vendor):
    def __init__(self):
        self._ID = 'VIA'
        self._tag = 'viagogo'
        self._sale_start_tag = "Order Information"
        self._date_format = '%d %B %Y'
        self._time_format = '%d %B %Y, %H:%M'
        self._versions = 1
        self._import_parameters()

    def _bespoke_replacements(self, text):
        return text.replace("  Shipping Refund:", "\nShipping Refund:")


class Seatwave(Vendor):
    def __init__(self):
        self._ID = 'SEAT'
        self._tag = 'seatwave'
        self._sale_start_tag = "Sale confirmation"
        self._date_format = '%d/%m/%Y'
        self._time_format = '%d/%m/%Y %H:%M'
        self._versions = 1
        self._import_parameters()


# class Stubhub2(Vendor):
#     def __init__(self):
#         self._ID = 'STUB2'
#         self._tag = 'stubhub'
#         self._sale_start_tag = "Hi Stephen,"
#         self._date_format = '%d/%m/%Y'
#         self._time_format = '%a, %d/%m/%Y, %H:%M'
#         self._import_parameters()
