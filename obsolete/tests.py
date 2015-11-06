__author__ = 'Sebastian.Law'



# stubs = raw_data['STUB']
# text = stubs[0]
#
# array = vendors.text_to_array(text)
#
# stub = vendor_list[0]
# t = stub.extract_transaction(array)

# # get list of unprocessed email files, then process them
# files = [file for file in os.listdir(files.unprocessed_path) if file.endswith('.txt')]
# transactions = []
# for file in files:
#     print("\n" + file + "\n")
#     transactions.append(processemail.processemail(files.unprocessed_path, file))
#
# # Extract the information

#
# # Move the processed emails
# # for file in files:
# #     os.rename(files.unprocessed_path+file, files.processed_path+file)
#
# print('main.py complete')



# # This is to import the regex components
# import files
# import csv
# import transaction
#
#
# def import_regex_parameters():
#     file = open(files.parameters_file, 'r', newline='')
#     reader = csv.reader(file, delimiter=",")
#     data = [r for r in reader]
#     file.close()
#     return data
#
#
#
# regex_parameters = import_regex_parameters()
#
#
#
# t_keys = transaction.Sale().get_data().keys()
#
# _ID = 'STUB'
#
# keys = [r[1] for r in regex_parameters if r[0] == _ID]
# parameters = [r[2:] for r in regex_parameters if r[0] == _ID]
# checks = [False]*len(t_keys)
# for i, k in enumerate(t_keys):
#     for key in keys:
#         if k == key:
#             checks[i] = True
#             break
# check = True
# for i in checks:
#     if i is False:
#         check = False
# if check is False:
#     print("transaction keys do not match those in the source file relating to " + _ID)
#
# _parameters = dict(zip(keys, parameters))

# import processemail
# import transaction
# import re

# s = []
# s.append('Quantity:')
# s.append(' 4 ticket(s) Level 1 Seating')
# s = [l.strip() for l in s]
# tag = 'Quantity:'
# offset = 0
# split_string = 'ticket\(s\)'
# split_element = 0
# specific = ' 4 ticket(s) Level 1 Seating'
# check = re.split(split_string,specific)

# import os
#
# path = 'C:/Users/Sebastian.Law/Dropbox/Shared/Rial Corporate Dev/unprocessed emails/'
# filename = '2015-09-09_142419.txt'
# encodings = ['latin-1', 'utf-16']
#
# files = [file for file in os.listdir(path) if file.endswith('.txt')]
#
# texts = []
# for f in files:
#     for e in encodings:
#         try:
#             file = open(path + f, encoding=e)
#             texts.append(file.read())
#             file.close()
#         except:
#             print("error: e")


# import datetime
#
# strings = []
# strings.append('Sun, 26/07/2015, 19:00 BST')
# strings.append('Thursday, 1 October 2015 19:00')
# strings.append('7 November 2015, 19:00')
# strings.append('30-Oct-2015 19:30:00')
#
# strings[0] = strings[0].replace("BST","").replace("GMT","").strip()
#
# formats = []
# formats.append('%a, %d/%m/%Y, %H:%M')
# formats.append('%A, %d %B %Y %H:%M')
# formats.append('%d %B %Y, %H:%M')
# formats.append('%d-%b-%Y %H:%M:%S')
#
# dates = [datetime.datetime.strptime(strings[i],f) for i, f in enumerate(formats)]
#
#
# print("\ntests.py complete\n")





# import datetime
# import re
#
# def extract(list, tag, offset, split_string=None, split_element=None):
#     s = None
#     for i, l in enumerate(list):
#         if l.startswith(tag):
#             if offset>0:
#                 s = list[i+offset]
#             elif offset==0:
#                 s = l.replace(tag,'')
#             break
#     if s!=None:
#         if split_string!=None and split_element!=None:
#             s = (re.split(split_string,s))[split_element]
#         s = s.replace('£','').strip()
#     return s
#
# class Sale:
#     def __init__(self, fileName):
#         self.reseller = None
#         self.processTime = None
#         self.fileName = fileName
#         # self.map = {}
#         self._keys = ("messageTime", "saleID", "saleDate", "ticketsSold", "artist", "venue", "gigTime", "section",  "row",  "seats", "ticketSaleType", "sent", "paidDate", "postageCosts", "postageRefunded", "otherCosts", "unitSaleValue", "netSaleValue")
#         self._values = [None]*18
#
#     def process(self, message_array):
#         for i, tag in enumerate(self.tags):
#             if tag!=None:
#                 self._values[i] = extract(message_array, self.tags[i], self.offsets[i], self.split_string[i], self.split_element[i])
#         self.processTime = datetime.datetime.now()
#         self.cleanDate(6)
#
#     def get_headings(self):
#         return ['fileName', 'processTime', 'reseller'] + [i for i in self._keys]
#
#     def get_data(self):
#         return [self.fileName, self.processTime, self.reseller] + self._values
#
# class SaleSTUB(Sale):
#     def __init__(self, fileName):
#         Sale.__init__(self, fileName)
#         self.reseller = "STUB"
#         self.start_tag = "Hi Stephen,"
#         self.tags = (None, "Order #:", "Order #:", "Quantity sold:", "Order #:", "Order #:", "Order #:", None, "Order #:", "Order #:", None, None, None, None, None, "Service fee:", "Your price:", "Your net payment:")
#         self.offsets = (None, 0, 0, 1, 1, 1, 2, None, 3, 4, None, None, None, None, None, 1, 1, 1)
#         self.split_string = (None, "\|", "Order date:", "x", "at", "at", None, None, None, None, None, None, None, None, None, None, None, None)
#         self.split_element = (None, 0, 1, 1, 0, 1, None, None, None, None, None, None, None, None, None, None, None, None)
#     def cleanDate(self, i):
#         self._date_format = '%a, %d/%m/%Y, %H:%M'
#         self._values[i] = datetime.datetime.strptime(self._values[i].replace("BST","").replace("GMT","").strip(), self._date_format)
#
# class SaleGET(Sale):
#     def __init__(self, fileName):
#         Sale.__init__(self, fileName)
#         self.reseller = "GET"
#         self.start_tag = "Order Summary"
#         self.tags = (None, "Order Number:", None, "Quantity:", "Event:", "Venue:", "Date of Event:", "Section:", "Row:", "Seat(s):", "Ticket Type:", None, None, None, None, None, "Price per ticket:", None)
#         self.offsets = (None, 1, None, 1, 1, 1, 1, 1, 1, 1, 1, None, None, None, None, None, 1, None)
#         self.split_string = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
#         self.split_element = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
#     def cleanDate(self, i):
#         self._date_format = '%A, %d %B %Y %H:%M'
#         self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)
#
# class SaleVIA(Sale):
#     def __init__(self, fileName):
#         Sale.__init__(self, fileName)
#         self.reseller = "VIA"
#         self.start_tag = "Order Information"
#         self.tags = (None, "Order ID:", None, "Number of Tickets:", "Event:", "Venue:", "Date:", "Ticket(s):", None, None, "Delivery Method:", None, None, None, "Shipping Refund:", None, "Price per Ticket:", "Total Proceeds:")
#         self.offsets = (None, 0, None, 1, 1, 1, 1, 1, None, None, 1, None, None, None, 1, None, 1, 1)
#         self.split_string = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
#         self.split_element = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
#     def cleanDate(self, i):
#         self._date_format = '%d %B %Y, %H:%M'
#         self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)
#
# class SaleSEAT(Sale):
#     def __init__(self, fileName):
#         Sale.__init__(self, fileName)
#         self.reseller = "SEAT"
#         self.start_tag = "Sale confirmation"
#         self.tags = (None, "Your reference number for this ticket sale is:", None, "Quantity:", "Which tickets have I sold?", "Which tickets have I sold?", "Which tickets have I sold?", "Block:", "Row:", None, "Listing ID:", None, None, None, None, None, "Selling price:", None)
#         self.offsets = (None, 0, None, 1, 1, 2, 2, 1, 1, None, 2, None, None, None, None, None, 1, None)
#         self.split_string = (None, None, None, "ticket\(s\)", None, "-", "-", None, None, None, None, None, None, None, None, None, "per ticket", None)
#         self.split_element = (None, None, None, 0, None, 1, 0, None, None, None, None, None, None, None, None, None, 0, None)
#     def cleanDate(self, i):
#         self._date_format = '%d/%m/%Y %H:%M'
#         self._values[i] = datetime.datetime.strptime(self._values[i], self._date_format)
