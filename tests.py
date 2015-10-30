__author__ = 'Sebastian.Law'


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