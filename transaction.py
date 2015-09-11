__author__ = 'Sebastian.Law'

# TODO: subclass specific tags should be pulled in from an external file, not embedded in the class definitions
# TODO: tags/offsets/split_x shhould be a collated data type, so only 1 array holds all the elements. for easier maintenance

import datetime
import re

def extract(list, tag, offset, split_string=None, split_element=None):
    # TODO: this function should probably be in the transaction class
    s = None
    for i, l in enumerate(list):
        if l.startswith(tag):
            if offset>0:
                s = list[i+offset]
            elif offset==0:
                s = l.replace(tag,'')
            break
    if s!=None:
        if split_string!=None and split_element!=None:
            s = (re.split(split_string,s))[split_element]
        s = s.replace('£','').strip()
    return s

class Sale:
    def __init__(self, fileName):
        self.reseller = None
        self.processTime = None
        self.fileName = fileName
        # self.map = {}
        self._keys = ("messageTime", "saleID", "saleDate", "ticketsSold", "artist", "venue", "gigTime", "section",  "row",  "seats", "ticketSaleType", "sent", "paidDate", "postageCosts", "postageRefunded", "otherCosts", "unitSaleValue", "netSaleValue")
        self._values = [None]*18

    def process(self, message_array):
        for i, tag in enumerate(self.tags):
            if tag!=None:
                self._values[i] = extract(message_array, self.tags[i], self.offsets[i], self.split_string[i], self.split_element[i])
        self.processTime = datetime.datetime.now()
        self.cleanDate(6)

    def get_headings(self):
        return ['fileName', 'processTime', 'reseller'] + [i for i in self._keys]

    def get_data(self):
        return [self.fileName, self.processTime, self.reseller] + self._values

class SaleSTUB(Sale):
    def __init__(self, fileName):
        Sale.__init__(self, fileName)
        self.reseller = "STUB"
        self.start_tag = "Hi Stephen,"
        self.tags = (None, "Order #:", "Order #:", "Quantity sold:", "Order #:", "Order #:", "Order #:", None, "Order #:", "Order #:", None, None, None, None, None, "Service fee:", "Your price:", "Your net payment:")
        self.offsets = (None, 0, 0, 1, 1, 1, 2, None, 3, 4, None, None, None, None, None, 1, 1, 1)
        self.split_string = (None, "\|", "Order date:", "x", "at", "at", None, None, None, None, None, None, None, None, None, None, None, None)
        self.split_element = (None, 0, 1, 1, 0, 1, None, None, None, None, None, None, None, None, None, None, None, None)
    def cleanDate(self, i):
        self._date_format = '%a, %d/%m/%Y, %H:%M'
        self._values[i] = datetime.datetime.strptime(self._values[i].replace("BST","").replace("GMT","").strip(), self._date_format)

class SaleGET(Sale):
    def __init__(self, fileName):
        Sale.__init__(self, fileName)
        self.reseller = "GET"
        self.start_tag = "Order Summary"
        self.tags = (None, "Order Number:", None, "Quantity:", "Event:", "Venue:", "Date of Event:", "Section:", "Row:", "Seat(s):", "Ticket Type:", None, None, None, None, None, "Price per ticket:", None)
        self.offsets = (None, 1, None, 1, 1, 1, 1, 1, 1, 1, 1, None, None, None, None, None, 1, None)
        self.split_string = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
        self.split_element = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
    def cleanDate(self, i):
        self._date_format = '%A, %d %B %Y %H:%M'
        self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)

class SaleVIA(Sale):
    def __init__(self, fileName):
        Sale.__init__(self, fileName)
        self.reseller = "VIA"
        self.start_tag = "Order Information"
        self.tags = (None, "Order ID:", None, "Number of Tickets:", "Event:", "Venue:", "Date:", "Ticket(s):", None, None, "Delivery Method:", None, None, None, "Shipping Refund:", None, "Price per Ticket:", "Total Proceeds:")
        self.offsets = (None, 0, None, 1, 1, 1, 1, 1, None, None, 1, None, None, None, 1, None, 1, 1)
        self.split_string = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
        self.split_element = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
    def cleanDate(self, i):
        self._date_format = '%d %B %Y, %H:%M'
        self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)

class SaleSEAT(Sale):
    def __init__(self, fileName):
        Sale.__init__(self, fileName)
        self.reseller = "SEAT"
        self.start_tag = "Sale confirmation"
        self.tags = (None, "Your reference number for this ticket sale is:", None, "Quantity:", "Which tickets have I sold?", "Which tickets have I sold?", "Which tickets have I sold?", "Block:", "Row:", None, "Listing ID:", None, None, None, None, None, "Selling price:", None)
        self.offsets = (None, 0, None, 1, 1, 2, 2, 1, 1, None, 2, None, None, None, None, None, 1, None)
        self.split_string = (None, None, None, "ticket\(s\)", None, "-", "-", None, None, None, None, None, None, None, None, None, "per ticket", None)
        self.split_element = (None, None, None, 0, None, 1, 0, None, None, None, None, None, None, None, None, None, 0, None)
    def cleanDate(self, i):
        self._date_format = '%d/%m/%Y %H:%M'
        self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)
