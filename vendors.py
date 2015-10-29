__author__ = 'Sebastian.Law'

import datetime
import re
import transaction


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
        self._sale_tags = (None, "Order #:", "Order #:", "Quantity sold:", "Order #:", "Order #:", "Order #:", None, "Order #:", "Order #:", None, None, None, None, None, "Service fee:", "Your price:", "Your net payment:")
        self._sale_offsets = (None, 0, 0, 1, 1, 1, 2, None, 3, 4, None, None, None, None, None, 1, 1, 1)
        self._sale_splits = (None, "\|", "Order date:", "x", "at", "at", None, None, None, None, None, None, None, None, None, None, None, None)
        self._sale_elements = (None, 0, 1, 1, 0, 1, None, None, None, None, None, None, None, None, None, None, None, None)
        self._date_format = '%a, %d/%m/%Y, %H:%M'

    def cleanDate(self, i):
        self._values[i] = datetime.datetime.strptime(self._values[i].replace("BST", "").replace("GMT", "").strip(), self._date_format)

class Getmein(Vendor):
    def __init__(self):
        self._ID = 'GET'
        self._tag = 'getmein'
        self._sale_start_tag = "Order Summary"
        self._sale_tags = (None, "Order Number:", None, "Quantity:", "Event:", "Venue:", "Date of Event:", "Section:", "Row:", "Seat(s):", "Ticket Type:", None, None, None, None, None, "Price per ticket:", None)
        self._sale_offsets = (None, 1, None, 1, 1, 1, 1, 1, 1, 1, 1, None, None, None, None, None, 1, None)
        self._sale_splits = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
        self._sale_elements = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
        self._date_format = '%A, %d %B %Y %H:%M'

    def cleanDate(self, i):
        self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)

class Viagogo(Vendor):
    def __init__(self):
        self._ID = 'VIA'
        self._tag = 'viagogo'
        self._sale_start_tag = "Order Information"
        self._sale_tags = (None, "Order ID:", None, "Number of Tickets:", "Event:", "Venue:", "Date:", "Ticket(s):", None, None, "Delivery Method:", None, None, None, "Shipping Refund:", None, "Price per Ticket:", "Total Proceeds:")
        self._sale_offsets = (None, 0, None, 1, 1, 1, 1, 1, None, None, 1, None, None, None, 1, None, 1, 1)
        self._sale_splits = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
        self._sale_elements = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
        self._date_format = '%d %B %Y, %H:%M'

    def cleanDate(self, i):
        self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)

class Seatwave(Vendor):
    def __init__(self):
        self._ID = 'SEAT'
        self._tag = 'seatwave'
        self._sale_start_tag = "Sale confirmation"
        self._sale_tags = (None, "Your reference number for this ticket sale is:", None, "Quantity:", "Which tickets have I sold?", "Which tickets have I sold?", "Which tickets have I sold?", "Block:", "Row:", None, "Listing ID:", None, None, None, None, None, "Selling price:", None)
        self._sale_offsets = (None, 0, None, 1, 1, 2, 2, 1, 1, None, 2, None, None, None, None, None, 1, None)
        self._sale_splits = (None, None, None, "ticket\(s\)", None, "-", "-", None, None, None, None, None, None, None, None, None, "per ticket", None)
        self._sale_elements = (None, None, None, 0, None, 1, 0, None, None, None, None, None, None, None, None, None, 0, None)
        self._date_format = '%d/%m/%Y %H:%M'

    def cleanDate(self, i):
        self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)
