__author__ = 'Sebastian.Law'

import email
import datetime
import sys
import transaction
import re

# def extract_inline(list, tag):
#     s = None
#     for l in list:
#         if tag in l:
#             s = l
#             break
#     t = re.compile(tag)
#     components = re.split(t, s, maxsplit=0, flags=0)
#     s = components[1].strip()
#     return s

def extract(list, tag, offset=1, regex=None):
    s = None
    if offset>0:
        for i, l in enumerate(list):
            if l.startswith(tag):
                s = list[i+offset]
                break
    return s

def processemail(path, filename):
    file = open(path + filename)
    file_text = file.read()
    file.close()
    message = email.message_from_string(file_text)

    # check if the message is more hi-tech than we expected
    if message.is_multipart():
        print("message is multipart")
        sys.exit()
    message_body = message.get_payload()

    # create a list/dictionary of vendors available
    vendors = ("GET","SEAT","STUB","VIA") # tuple, immutable. List: vendors = ["GET","SEAT","STUB","VIA"]
    vendor_tags = ("getmein","seatwave","stubhub","viagogo")
    vendor_list = list(zip(vendors,vendor_tags))

    vendor_bool = [x[1] in message_body.lower() for x in vendor_list]
    temp = 0
    for v in vendor_bool:
        if v==True:
            temp +=1
    if temp!=1:
        print("cannot determine message source")
        sys.exit()

    t = None
    if(vendor_bool[0]):
        t = transaction.SaleGET()
    elif(vendor_bool[1]):
        t = transaction.SaleSEAT()
    elif(vendor_bool[2]):
        t = transaction.SaleSTUB()
    elif(vendor_bool[3]):
        t = transaction.SaleVIA()
    # t.processTime = datetime.datetime.now()
    # t.messageTime = datetime.datetime.strptime(message['Sent'],'%d %B %Y %H:%M')

    n = re.compile('\\n')
    message_array = re.split(n, message_body, maxsplit=0, flags=0)
    message_array = [l.strip() for l in message_array if l.strip()!='']
    for i, line in enumerate(message_array):
        if line == t.start_tag:
            start = i
            break
    message_array = message_array[start:]
    
    # tickets = extract(message_array,'Order #:')
    for i, d in t.map.items():
        if d[0]!=None:
            d[3] = extract(message_array,d[0],d[1],d[2])
            print(i,d)

    return t