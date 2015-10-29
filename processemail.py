__author__ = 'Sebastian.Law'

import email
import datetime
import sys
import transaction
import re

def processemail(path, filename):
    file = open(path + filename, encoding='utf-16')
    file_text = file.read()
    file.close()
    message = email.message_from_string(file_text)

    # check if the message is more hi-tech than we expected
    if message.is_multipart():
        print("message is multipart")
        sys.exit()
    message_body = message.get_payload()

    # create a list/dictionary of vendors available
    vendors = ("GET", "SEAT", "STUB", "VIA")  # tuple, immutable. List: vendors = ["GET","SEAT","STUB","VIA"]
    vendor_tags = ("getmein", "seatwave", "stubhub", "viagogo")
    vendor_list = list(zip(vendors, vendor_tags))

    vendor_bool = [x[1] in message_body.lower() for x in vendor_list]
    temp = 0
    for v in vendor_bool:
        if v is True:
            temp += 1
    if temp != 1:
        print("cannot determine message source")
        sys.exit()

    t = None
    if vendor_bool[0]:
        t = transaction.SaleGET(filename)
    elif vendor_bool[1]:
        t = transaction.SaleSEAT(filename)
    elif vendor_bool[2]:
        t = transaction.SaleSTUB(filename)
    elif vendor_bool[3]:
        t = transaction.SaleVIA(filename)

    n = re.compile('\\n')
    message_array = re.split(n, message_body, maxsplit=0, flags=0)
    message_array = [l.strip() for l in message_array if l.strip() != '']
    for i, line in enumerate(message_array):
        if line == t.start_tag:
            start = i
            break
    message_array = message_array[start:]

    t.process(message_array)

    return t