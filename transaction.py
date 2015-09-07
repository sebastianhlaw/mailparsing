__author__ = 'Sebastian.Law'

import datetime

class Sale:
    def __init__(self):
        self.reseller = ''
        self.processTime = datetime.datetime
        self._members = 18
        self.map = {}
        self._keys = ("messageTime", "saleID", "saleDate", "ticketsSold", "artist", "venue", "gigTime", "section",  "row",  "seats", "ticketType", "sent", "paidDate", "postageCosts", "postageRefunded", "otherCosts", "unitSaleValue", "netSaleValue")
        # values = [None]*self._members
        # self.data = dict(zip(self._keys,values))

class SaleSTUB(Sale):
    def __init__(self):
        Sale.__init__(self)
        self.reseller = "STUB"
        self.start_tag = "Sale info"
        self.tags = [None, "Order #:", "Order #:", "Quantity sold:", "Order #:", "Order #:", "Order #:", None, "Order #:", "Order #:", None, None, None, None, None, "Service fee:", "Your price:", "Your net payment:"]
        self.offsets = [None, 0, 0, 1, 1, 1, 2, None, 3, 4, None, None, None, None, None, 1, 1, 1]
        self.regex = [None]*self._members
        self.values = [None]*self._members
        self.map = dict(zip(self._keys, [list(a) for a in zip(self.tags, self.offsets, self.regex, self.values)]))


class SaleGET(Sale):
    def __init__(self):
        Sale.__init__(self)
        self.reseller = "GET"
        self.start_tag = "Order Summary"
        self.tags = [None, "Order Number:", None, "Quantity:", "Event:", "Venue:", "Date of Event:", "Section:", "Row:", "Seat(s):", "Ticket Type:", None, None, None, None, None, "Price per ticket:", None]
        self.offsets = [None, 1, None, 1, 1, 1, 1, 1, 1, 1, 1, None, None, None, None, None, 1, None]
        self.regex = [None]*self._members
        self.values = [None]*self._members
        self.map = dict(zip(self._keys, [list(a) for a in zip(self.tags, self.offsets, self.regex, self.values)]))

class SaleVIA(Sale):
    def __init__(self):
        Sale.__init__(self)
        self.reseller = "VIA"
        self.start_tag = "Order Information"
        self.tags = [None, "Order ID:", None, "Number of Tickets:", "Event:", "Venue:", "Date:", "Ticket(s):", None, None, "Delivery Method:", None, None, None, "Shipping Refund:", None, "Price per Ticket:", "Total Proceeds:"]
        self.offsets = [None, 0, None, 1, 1, 1, 1, 1, None, None, 1, None, None, None, 1, None, 1, 1]
        self.regex = [None]*self._members
        self.values = [None]*self._members
        self.map = dict(zip(self._keys, [list(a) for a in zip(self.tags, self.offsets, self.regex, self.values)]))

class SaleSEAT(Sale):
    def __init__(self):
        Sale.__init__(self)
        self.reseller = "SEAT"
        self.start_tag = "Sale confirmation"
        self.tags = [None, "Your reference number for this ticket sale is:", None, "Quantity:", "Which tickets have I sold?", "Which tickets have I sold?", "Which tickets have I sold?", "Block:", "Row:", None, "Listing ID:", None, None, None, None, None, "Selling price:", None]
        self.offsets = [None, 0, None, 1, 1, 2, 2, 1, 1, None, 2, None, None, None, None, None, 1, None]
        self.regex = [None]*self._members
        self.values = [None]*self._members
        self.map = dict(zip(self._keys, [list(a) for a in zip(self.tags, self.offsets, self.regex, self.values)]))